# Programme

One file per mesocycle: four weeks, three loading and one deload.

**Gitignored.** A programme is built around a specific person's loads, constraints and schedule.

## What a programme file carries

- **Theme** — what the variable layer emphasises for these four weeks.
- **Anchors** — the lifts held constant, their schemes, and their weekly progression. Front-matter
  so they can be read mechanically.
- **The rotation** — each session, its venue, its anchor, and its pairs.
- **Week-by-week** — what changes across the loading weeks and what the deload looks like.

## The two layers

Anchors are the measuring stick and do not change within a block. Everything else is governed by
the theme and changes every four weeks. See
[ADR 0002](../docs/adr/0002-fixed-anchors-themed-mesocycles.md) for why.

## After editing

Always re-run the validator. Changing set counts changes the weekly volume balance, and a
rotation that looked fine can push a muscle outside its band:

```bash
python3 scripts/weekly_volume.py
```
