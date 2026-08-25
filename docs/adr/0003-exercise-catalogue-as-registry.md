# 3. An exercise catalogue is the shared registry

Date: 2026-08-24

## Status

Accepted

## Context

Nothing inherently prevents the same movement being recorded as "incline DB press" one week and
"DB incline" the next. To any aggregation those are two unrelated exercises, and the progression
history silently splits in half. This is the most common way a long-lived training log rots, and
it rots quietly — the files still look fine.

There is also a safety requirement that needs somewhere to live. A joint constraint in the
athlete profile can mean that no set loading that joint may be taken to failure. Left as prose in
a profile document, such a rule depends on being remembered every time a session is planned.
Remembering is not a control.

A third pressure is the possible future app, which will need an exercise picker with movement
patterns and muscle mappings — a data set that would otherwise be built twice.

Options considered:

- **Free text, normalised on read.** Fine for a month, degrades steadily, needs a cleanup pass
  over a year of inconsistent history.
- **A flat list of allowed slugs.** Fixes naming with near-zero upkeep, but movement patterns,
  muscle coverage and joint safety must be re-derived by reasoning every time something is
  planned — slower, and wrong occasionally rather than never.
- **A catalogue file per exercise.**

## Decision

One file per exercise under `exercises/`, keyed by a canonical slug that both logs and programmes
reference. Each file carries `pattern`, `primary`, `secondary`, `venue`, `loads_joints`,
`grip_demand`, `unilateral`, and `load_increment_kg`.

The athlete does not interact with slugs. They describe sessions in prose; the agent resolves the
description to a catalogue entry and asks when a description is ambiguous. The catalogue is
infrastructure for the agent, not friction for the athlete.

## Consequences

Volume per muscle per week becomes computable rather than estimated, because sets join to muscles
through the catalogue.

The joint rule becomes mechanical instead of remembered: an exercise that loads a constrained
joint, logged at an intensity the athlete's profile forbids, is a detectable contradiction, and
`scripts/weekly_volume.py` checks for it. Safety moves from vigilance to a property that can be
verified.

This originally shipped as a single `loads_elbow` boolean, which fused an exercise property with a
personal limitation. [ADR 0004](./0004-joint-constraints-as-a-two-sided-model.md) separates them.

The future app inherits its exercise picker as data rather than as a build task.

The cost is a small ongoing obligation: a movement cannot be logged until it exists in the
catalogue. In practice adding an entry is a few lines, and the obligation is a feature — it is
the moment where "is this the same lift as that other one?" gets answered deliberately rather
than by accident.
