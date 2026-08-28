# Logs

One file per session: `YYYY-MM-DD-<session-slug>.md`.

**Gitignored.** Session logs carry bodyweight, sleep, injury notes and training loads. They stay
on your machine.

## Format

YAML front-matter carries the structure; markdown below carries how it felt.

```markdown
---
date: 2026-08-31
venue: gym            # gym | home | mat
block: meso-1-density
week: 1
session: G2
bodyweight_kg: 75.0   # weekly, same conditions
sleep_h: 7.5
readiness: 3          # 1-5, gut feel
soreness: [chest, hamstrings]     # ordinary DOMS
symptoms:                         # something that is NOT ordinary soreness
  - site: upper-trap
    side: right                   # optional
    severity: 2                   # 1-5
    note: Stiffness after the top set of overhead pressing.
exercises:
  - name: db-incline-press      # must be a slug in exercises/
    sets:
      - {reps: 10, load_kg: 20, rir: 2}
      - {reps: 8,  load_kg: 22, rir: 1}
---

Elbow fine after the ramp. Cut the last pair, ran out of time.
```

## soreness vs symptoms

`soreness` is expected muscle soreness after training. It is normal, it resolves, and it needs no
action.

`symptoms` is anything else: pain, stiffness, tingling, a joint that objects. Recorded separately
because the two demand different responses, and because a symptom is only useful if it can be read
as a **series**. One sore trap is noise. The same site appearing three weeks running, always after
the same movement, is a finding. `scripts/weekly_volume.py` lists recent symptoms so they do not
get buried under volume numbers.

Record the site even when it seems trivial. The cost is one line; the alternative is reconstructing
a pattern from memory months later.

## rest_pause

A set broken into clusters with brief pauses, each cluster taken to or near failure, to reach a
rep target that a straight set could not.

Mark it `rest_pause: true` on the set. It is a legitimate intensity technique, but the rep count
it produces is **not comparable to a straight set** — the same number represents more approaches
to failure at higher fatigue. Flagging it keeps a progression from being read across two things
that are not the same.

Repeated rest-pause on a movement usually means the prescription is wrong rather than the effort:
the load is too heavy for the rep target, so the only way to hit the number is to stop being a set.

Conditioning and skill entries omit `rir` and use their own metrics instead — `calories`,
`duration_s`, `duration_min`, `intensity`.

## You are not meant to write this by hand

Describe the session in prose to the agent; it resolves exercises to catalogue slugs, asks when
something is ambiguous, and writes the file. See the root README.

Validate whatever accumulates with `python3 scripts/weekly_volume.py`.
