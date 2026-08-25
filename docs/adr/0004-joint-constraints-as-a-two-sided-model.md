# 4. Joint constraints are a two-sided model

Date: 2026-08-25

## Status

Accepted. Supersedes the `loads_elbow` flag introduced in
[ADR 0003](./0003-exercise-catalogue-as-registry.md).

## Context

ADR 0003 established that a safety rule needs a mechanical home rather than living as prose in a
profile document, and implemented that as a boolean: `loads_elbow: true` on any exercise loading
the elbow, with a hard-coded check rejecting such a set logged at RIR 0.

That worked, and it caught a real violation within a week of being written. But it fused two
different kinds of fact into one field:

- **Whether an exercise loads the elbow** is a property of the exercise. It is true for everyone,
  and it belongs in the shared catalogue.
- **Whether the elbow needs protecting, and how much** is a property of a person. It belongs in
  the gitignored profile.

Fusing them made the catalogue personal. `loads_elbow` only exists as a field because one athlete
has an elbow problem — a fork with knee trouble would have to rename the field, edit 39 files, and
patch the validator. The flag also encoded exactly one severity: "not to failure". Real
limitations vary. A tendinopathy may want two reps left rather than one; a disc history may want a
movement not to appear at all, at any intensity.

Elbows, knees and lower backs are the common cases, and a system that handles only elbows is not
shareable.

Options considered:

- **More booleans** — `loads_knee`, `loads_back`, `loads_shoulder`. Trivial to add, and wrong in
  the same way: the schema still grows a field per joint that anyone happens to have injured, and
  severity is still not expressible.
- **Per-exercise severity** — `loads: {knee: high, hip: moderate}`. More expressive, but it asks
  the catalogue to grade how badly an exercise loads a joint, which is a judgement that varies by
  person, technique and load. That is exactly the judgement being pushed out of the catalogue.
- **A list plus a separate rule set.**

## Decision

Split the model in two.

**The catalogue declares what an exercise loads.** `loads_joints: [knee, hip, lower-back]` — the
joints under meaningful load, not every joint that moves. Objective, shared, tracked in git.

**The profile declares what needs protecting.** `profile/joint-constraints.yaml`, gitignored, with
a template alongside it:

```yaml
constraints:
  knee:
    reason: Patellar tendinopathy; painful at depth under load.
    min_rir: 2
    avoid: [leg-extension]
```

`min_rir` is the floor for any set on an exercise loading that joint; `avoid` lists movements that
should never be prescribed at all. A `known_joints` vocabulary catches typos, so `knees` is an
error rather than a silently unenforced rule.

The validator joins the two. Neither half means anything alone, which is the point.

## Consequences

The catalogue becomes genuinely shareable. Someone with knee trouble and healthy elbows writes one
config file and changes nothing else; the 39 exercise entries and the validator are already
correct for them.

Severity becomes expressible. "Leave a rep" and "leave two" and "never prescribe this" are three
different rules, and tendon problems, joint problems and disc histories genuinely want different
ones.

An exercise can be constrained through more than one joint at once, and each is reported
separately — a squat under both knee and lower-back constraints produces two findings, which is
correct, because the reasons differ.

The cost is a judgement call now baked into the catalogue: **which joints count as "meaningfully
loaded"**. Tag too few and real risk goes unflagged; tag too many and the validator cries wolf
until it gets ignored. The rule applied here is *joints a limitation would plausibly change the
prescription for* — so a bench press loads elbow and shoulder but not wrist, while a push-up loads
all three.

`loads_joints` is also incomplete as a safety model. It says nothing about range of motion, tempo,
or grip position, which are frequently what actually determines whether a movement hurts. Those
stay in profile prose. This decision makes the *intensity* rule checkable, not the whole problem.
