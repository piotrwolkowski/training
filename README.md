# Training

A file-based system for recording resistance training and planning it with an AI agent.

Plain markdown, no database, no app. You describe a session in ordinary language; the agent
resolves it against an exercise catalogue and writes a structured log. A script validates what
accumulates and reports weekly volume per muscle.

**Your personal data never enters git.** The repo tracks the *system*; your body, your numbers and
your training history stay on your machine. See [The split](#the-split).

Start with **[`CONTEXT.md`](./CONTEXT.md)** — the glossary. Terms like *anchor*, *pair*, *exposure*
and *buy-in* have specific meanings here, and the rest of the repo depends on them.

---

## The loop

**1. Train** against the current file in `programme/`.

**2. Describe it in plain language.** Never write YAML.

> "Squat 80 for four sets of five, felt like two in the tank. Row 60 for 3×8. Calves 3×12, last
> one to failure. Slept about six and a half."

The agent resolves that to catalogue slugs, asks when something is ambiguous — *"34 kg per
dumbbell or total?"* — and writes the log. Ambiguity produces a question, never a guess.

**3. Log other training too.** A martial art, a sport, a long ride. It carries no hard sets but it
carries load, and it's the difference between diagnosing a stall as under-recovery rather than
under-stimulus.

**4. Weekly, the agent reviews.** Logs against programme: did the anchors progress, what was
skipped, what changes next week.

**5. Every four weeks, a new mesocycle.** Week 4 is always a deload. The theme changes; the
anchors do not.

---

## The split

| Tracked in git — the system | Gitignored — your instance |
|---|---|
| `CONTEXT.md` — the glossary | `profile/` — age, bodyweight, injuries, baselines |
| `docs/adr/` — decisions and their alternatives | `logs/` — sessions, sleep, bodyweight |
| `exercises/` — the catalogue | `programme/` — built around your loads |
| `scripts/` — validation and reporting | `reviews/` — quotes your logs |
| `profile/*.example.*` — templates | `cards/` — generated from your programme |

The boundary is conceptual, not arbitrary: **method versus instance.** Anything that describes how
training is organised is tracked. Anything that describes a particular body is not.

Each ignored directory keeps a tracked `README.md` explaining what belongs there and in what
format, so a fresh clone is self-explanatory rather than a set of empty folders.

---

## Getting started

```bash
cp profile/athlete.example.md        profile/athlete.md
cp profile/constraints.example.md    profile/constraints.md
cp profile/volume-targets.example.yaml profile/volume-targets.yaml
```

Fill those in — they're gitignored. `constraints.md` matters most: it is where injuries become
**rules a programme can be checked against**, rather than things someone has to remember.

Then ask the agent to build a first mesocycle. It will need your available days, session length,
equipment per venue, and any joint limitations.

---

## Validation

```bash
python3 scripts/weekly_volume.py
```

Not a convenience script. Because markdown files are the source of truth, this **is** the schema
validator, and it exits non-zero on failure. It:

- rejects logs referencing an exercise not in the catalogue, or with malformed front-matter;
- **enforces joint constraints mechanically** — anything flagged `loads_elbow: true` recorded at
  RIR 0 is a violation, so safety is a checkable property rather than a remembered one;
- reports hard sets and exposures per muscle per week against your volume targets, counting
  secondary involvement as half a set.

Run it after logging, and **always after editing a programme** — changing set counts changes the
weekly balance, and a rotation that looks fine can push a muscle outside its band.

---

## How the programme is shaped

Two layers, deliberately separated
([ADR 0002](./docs/adr/0002-fixed-anchors-themed-mesocycles.md)):

**Anchors** — a handful of lifts, one per movement pattern. Present every week, same scheme, load
progressed on a defined schedule. First in the session, full rest, never paired. These are the
measuring stick.

**The variable layer** — accessories, pairing, rep ranges, where failure is permitted. Governed by
the mesocycle theme, which changes every four weeks.

That split exists because rotating the method weekly — which is genuinely more fun — makes it
impossible to tell a bad week from a fatigued one. Progressive overload needs something held
constant to measure against. The anchors keep the signal; the variable layer supplies the variety.

**On methodology.** The volume literature is the skeleton: 10–20 hard sets per muscle per week,
two exposures per muscle, most sets at RIR 1–3 — budgeted down to what the available session
length can actually deliver, which is what `profile/volume-targets.yaml` is for. High-intensity
training is borrowed narrowly: true failure on the last isolation movement of a muscle group,
never on an anchor, never on anything a joint constraint rules out.

---

## Design decisions

Recorded in [`docs/adr/`](./docs/adr/), with the alternatives that were rejected and why:

1. [Markdown with YAML front-matter is the source of truth](./docs/adr/0001-markdown-yaml-as-source-of-truth.md)
2. [Fixed anchors, variable everything else](./docs/adr/0002-fixed-anchors-themed-mesocycles.md)
3. [An exercise catalogue is the shared registry](./docs/adr/0003-exercise-catalogue-as-registry.md)

---

## A note on the catalogue

The shipped `exercises/` entries reflect one working configuration: which lifts are anchors, and
which are permitted to go to failure. Those are **instance decisions living in shared files** —
the honest place for them would be the profile. Fork and adjust; the objective fields (`pattern`,
`primary`, `secondary`, `grip_demand`, `loads_elbow`, `load_increment_kg`) transfer unchanged.
