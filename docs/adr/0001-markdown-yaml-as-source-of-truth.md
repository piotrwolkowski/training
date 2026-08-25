# 1. Markdown files with YAML front-matter are the source of truth

Date: 2026-08-24

## Status

Accepted

## Context

This repo records every training session, indefinitely. A live-capture app may eventually be
built to write session data during training rather than after it.

That future app creates a trap. The obvious move is to log informally now — prose in a diary —
and design a proper data model when the app arrives. But by then there would be a year or more
of freeform history, and the app would either start from an empty database (throwing away the
history that makes recommendations possible) or require a parsing migration over inconsistent
prose.

The competing pressure is that until the app exists, every log entry is produced by hand. A
format optimised purely for machines is a format that stops getting filled in.

Options considered:

- **Prose markdown.** Zero friction, but weekly volume and progression cannot be computed
  reliably, only re-interpreted.
- **JSONL append-only log.** Ideal for the app, unreadable at a glance, and unpleasant to
  write or correct by hand for however many months precede the app.
- **SQLite.** Real relational storage and the best querying, but a binary blob in a git repo:
  no diffs, no review of what changed, no editing a mistyped set from a phone.
- **Markdown with YAML front-matter.** Structure and prose in one file.

## Decision

Each session is one file, `logs/YYYY-MM-DD-<slug>.md`. A strict YAML front-matter block carries
the structured data — date, venue, session type, sleep, readiness, soreness, exercises, sets,
reps, load, RIR. Free markdown below carries subjective notes.

These files are the source of truth. Any future app reads and writes this exact shape; it does
not own a separate database that the files are exported to.

A companion decision makes this workable in practice: the athlete does not write the YAML. They
describe the session conversationally and the agent writes the file, asking a follow-up question
where the description is ambiguous. The structure is paid for by the agent, not the athlete.

## Consequences

The history accumulated before the app exists is the history the app launches with. No
migration, no cold start.

Every change is a readable diff, so a mis-logged set is visible and correctable, and the record
of what was corrected survives.

The cost is that YAML is order-sensitive and easy to break subtly — a mis-indented set silently
becomes a different shape. This is mitigated by `scripts/weekly_volume.py`, which parses every
log and fails loudly on anything malformed. That script is not a convenience; it is the schema
validator, and it should be run whenever logs accumulate.

Querying is worse than a database would give. Aggregation means parsing files. This is accepted
while the corpus is small; if it ever becomes painful, a derived database can be built *from*
the files without the files ceasing to be authoritative.
