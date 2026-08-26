#!/usr/bin/env python3
"""Validate the training logs and report weekly hard-set volume per muscle.

This is not a convenience script. Because the markdown files are the source of truth
(ADR 0001), this is the schema validator - it is what turns "the files look fine" into
"the files are actually consistent". Run it whenever logs accumulate.

It does three jobs:

  1. Validates every log against the exercise catalogue (ADR 0003). Unknown slugs and
     malformed front-matter are errors, not warnings.
  2. Enforces joint constraints mechanically. Each exercise declares which joints
     it loads (loads_joints); profile/joint-constraints.yaml declares which of the
     athlete's joints need protecting and how hard they may be pushed (min_rir),
     plus movements to avoid entirely. A logged set that breaks a rule is reported.
     Safety becomes a checkable property rather than something a planner remembers.
  3. Reports hard sets per muscle per week against the 10-20 target, and exposures
     per muscle against the target of 2.

Exit code is non-zero if anything failed, so it works as a pre-commit check.

Usage:
    python3 scripts/weekly_volume.py [--weeks N]
"""

import argparse
import datetime as dt
import pathlib
import sys
from collections import defaultdict

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXERCISES = ROOT / "exercises"
LOGS = ROOT / "logs"

HARD_SET_RIR = 3          # a working set at RIR <= 3 counts toward volume
SECONDARY_WEIGHT = 0.5    # a set counts half for muscles listed as secondary
NON_VOLUME_PATTERNS = {"conditioning", "carry", "skill", "recovery"}
TARGETS = ROOT / "profile" / "volume-targets.yaml"
TARGETS_EXAMPLE = ROOT / "profile" / "volume-targets.example.yaml"
JOINTS = ROOT / "profile" / "joint-constraints.yaml"
JOINTS_EXAMPLE = ROOT / "profile" / "joint-constraints.example.yaml"


def front_matter(path):
    """Return the parsed YAML front-matter of a markdown file, or None."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path.name}: no front-matter block")
    _, _, rest = text.partition("---")
    block, sep, _ = rest.partition("\n---")
    if not sep:
        raise ValueError(f"{path.name}: unterminated front-matter block")
    data = yaml.safe_load(block)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: front-matter is not a mapping")
    return data


def load_joint_constraints():
    """Return ({joint: rule}, known_joints). Absent config means no constraints."""
    path = JOINTS if JOINTS.exists() else JOINTS_EXAMPLE
    if not path.exists():
        return {}, set()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rules = data.get("constraints") or {}
    for joint, rule in rules.items():
        if not isinstance(rule, dict):
            raise ValueError(f"joint '{joint}': rule must be a mapping")
        rule.setdefault("min_rir", 0)
        rule.setdefault("avoid", [])
        rule.setdefault("allow_failure", [])
    return rules, set(data.get("known_joints") or [])


def load_targets():
    path = TARGETS
    if not path.exists():
        if not TARGETS_EXAMPLE.exists():
            raise ValueError("no volume targets: copy profile/volume-targets.example.yaml "
                             "to profile/volume-targets.yaml")
        path = TARGETS_EXAMPLE
        print(f"note: {TARGETS.name} not found, using {TARGETS_EXAMPLE.name}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return (data["muscles"],
            set(data.get("untracked") or []),
            int(data.get("exposures", 2)))


def is_doc(path):
    """README/notes files live alongside data files and are not data."""
    return path.stem.upper() in {"README", "NOTES", "TEMPLATE"}


def load_catalogue():
    catalogue = {}
    for path in sorted(EXERCISES.glob("*.md")):
        if is_doc(path):
            continue
        data = front_matter(path)
        slug = data.get("slug")
        if not slug:
            raise ValueError(f"{path.name}: missing 'slug'")
        if slug != path.stem:
            raise ValueError(f"{path.name}: slug '{slug}' does not match filename")
        catalogue[slug] = data
    return catalogue


def iso_week(date):
    if isinstance(date, str):
        date = dt.date.fromisoformat(date)
    year, week, _ = date.isocalendar()
    return f"{year}-W{week:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weeks", type=int, default=4,
                    help="how many recent weeks to report (default: 4)")
    args = ap.parse_args()

    try:
        catalogue = load_catalogue()
        bands, untracked, exposure_target = load_targets()
        joint_rules, known_joints = load_joint_constraints()
    except ValueError as exc:
        print(f"CONFIG ERROR: {exc}", file=sys.stderr)
        return 2
    errors_pre = []
    print(f"catalogue: {len(catalogue)} exercises")
    if joint_rules:
        caps = ", ".join(f"{j} (RIR>={r['min_rir']})" for j, r in sorted(joint_rules.items()))
        print(f"joints:    {caps}")
    avoided = {slug: j for j, r in joint_rules.items() for slug in r["avoid"]}

    if known_joints:
        for slug, meta in catalogue.items():
            for joint in meta.get("loads_joints") or []:
                if joint not in known_joints:
                    errors_pre.append(f"exercises/{slug}.md: unknown joint '{joint}' "
                                      f"(not in known_joints)")

    errors = list(errors_pre)
    violations = []
    # week -> muscle -> hard sets
    volume = defaultdict(lambda: defaultdict(float))
    # week -> muscle -> set of session ids
    exposures = defaultdict(lambda: defaultdict(set))
    sessions = 0

    for path in sorted(LOGS.glob("*.md")):
        if is_doc(path):
            continue
        try:
            data = front_matter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        date = data.get("date")
        if not date:
            errors.append(f"{path.name}: missing 'date'")
            continue
        week = iso_week(date)
        sessions += 1

        for ex in data.get("exercises") or []:
            slug = ex.get("name") or ex.get("slug")
            if slug not in catalogue:
                errors.append(f"{path.name}: unknown exercise '{slug}' "
                              f"(add exercises/{slug}.md or fix the log)")
                continue
            meta = catalogue[slug]

            if slug in avoided:
                violations.append(
                    f"{path.name}: {slug} is on the avoid list for "
                    f"{avoided[slug]} - it should not be prescribed at all")

            loaded = [j for j in (meta.get("loads_joints") or []) if j in joint_rules]
            for st in ex.get("sets") or []:
                rir = st.get("rir")
                if rir is None:
                    continue
                for joint in loaded:
                    if slug in joint_rules[joint]["allow_failure"]:
                        continue
                    floor = joint_rules[joint]["min_rir"]
                    if rir < floor:
                        violations.append(
                            f"{path.name}: {slug} logged at RIR {rir}; it loads the "
                            f"{joint}, which requires RIR >= {floor}")

            if meta.get("pattern") in NON_VOLUME_PATTERNS:
                continue

            weighted = [(m, 1.0) for m in (meta.get("primary") or [])]
            weighted += [(m, SECONDARY_WEIGHT) for m in (meta.get("secondary") or [])]
            weighted = [(m, w) for m, w in weighted if m not in untracked]
            for st in ex.get("sets") or []:
                rir = st.get("rir")
                if rir is None:
                    errors.append(f"{path.name}: {slug} has a set with no 'rir'")
                    continue
                if rir <= HARD_SET_RIR:
                    for m, w in weighted:
                        volume[week][m] += w
                        exposures[week][m].add(path.stem)

    print(f"logs:      {sessions} sessions\n")

    for exc in errors:
        print(f"ERROR      {exc}", file=sys.stderr)
    for v in violations:
        print(f"VIOLATION  {v}", file=sys.stderr)
    if errors or violations:
        print(file=sys.stderr)

    if not volume:
        print("No hard sets logged yet - nothing to report.")
        return 1 if (errors or violations) else 0

    for week in sorted(volume)[-args.weeks:]:
        print(f"{week}   (secondary involvement counts as {SECONDARY_WEIGHT} of a set)")
        print(f"  {'muscle':<12} {'sets':>5} {'target':>9} {'exp':>4}")
        seen = volume[week]
        for muscle in sorted(bands, key=lambda m: -seen.get(m, 0)):
            lo, hi = bands[muscle]
            sets = seen.get(muscle, 0)
            exp = len(exposures[week].get(muscle, ()))
            flags = []
            if sets < lo:
                flags.append("under-volume")
            elif sets > hi:
                flags.append("over-volume")
            if exp < exposure_target:
                flags.append("under-frequency")
            mark = "   <-- " + ", ".join(flags) if flags else ""
            print(f"  {muscle:<12} {sets:>5.1f} {f'{lo}-{hi}':>9} {exp:>4}{mark}")
        extra = sorted(m for m in seen if m not in bands and m not in untracked)
        if extra:
            print(f"  untargeted muscles seen in logs: {', '.join(extra)}")
        print()

    return 1 if (errors or violations) else 0


if __name__ == "__main__":
    sys.exit(main())
