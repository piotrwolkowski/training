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
soreness: [chest, hamstrings]
exercises:
  - name: db-incline-press      # must be a slug in exercises/
    sets:
      - {reps: 10, load_kg: 20, rir: 2}
      - {reps: 8,  load_kg: 22, rir: 1}
---

Elbow fine after the ramp. Cut the last pair, ran out of time.
```

Conditioning and skill entries omit `rir` and use their own metrics instead — `calories`,
`duration_s`, `duration_min`, `intensity`.

## You are not meant to write this by hand

Describe the session in prose to the agent; it resolves exercises to catalogue slugs, asks when
something is ambiguous, and writes the file. See the root README.

Validate whatever accumulates with `python3 scripts/weekly_volume.py`.
