# CONTEXT

The ubiquitous language of this training knowledge base. Definitions only — no programming,
no prescriptions, no implementation detail. If a term here is used loosely anywhere in the
repo, that is a bug.

## Session

One training bout. The atomic unit of the log. Exactly one file in `logs/`.

A session always has a **venue** and a position in the **rotation**. It may or may not carry
an **anchor**.

## Venue

Where a session happens, and therefore what equipment is available. Two values:

- **gym** — mid-to-well equipped: barbells, dumbbells, kettlebells, machines, cables.
- **home** — 16 kg and 20 kg kettlebells, and a skipping rope.
- **gym-limited** — a gym with partial equipment. Anchors may or may not be possible; check
  before assuming.
- **mat** — grappling or martial arts training. Not a lifting venue; carries no anchors and no
  hard sets, but counts fully toward training load.

Venue is not incidental metadata. It determines which exercises are possible, and therefore
whether a session can carry an anchor at all. Home sessions cannot.

## Anchor

A lift that appears every week for the whole of a **mesocycle**, with a fixed rep scheme and a
load that is progressed on a defined schedule.

Anchors exist to be the *measuring stick*. Everything else in the programme may change; the
anchors do not, and that is what makes it possible to answer "am I getting stronger?"

An anchor is always performed first in its session, at full rest, and is never **paired**.

## Exposure

One instance of a muscle being trained hard within a week. "Chest gets two exposures" means
chest is trained hard in two separate sessions that week — not that it accumulates a given
number of sets.

Frequency is counted in exposures. Volume is counted in **hard sets**.

## Hard set

A working set taken to **RIR** 3 or lower. Warm-up sets, ramp sets and technique sets are not
hard sets and do not count toward weekly volume.

## RIR (Reps In Reserve)

How many more reps could have been completed with good form when the set was stopped.
RIR 0 means **failure** — no further rep was possible.

RIR is the unit of intensity in this repo. Percentages of a one-rep max are not used, and a
true one-rep max is never tested.

## Failure

RIR 0. A set stopped because no further rep was possible, not because a target was reached.

Failure is a deliberate, sparingly-applied tool, not a default. Where it is permitted is a
programming decision, not a matter of how motivated the session feels.

## Pair

Two exercises alternated with **no rest between them**, targeting **non-competing** muscles —
for example a squat and a pull-up.

The purpose of a pair is **density**: doing productive work during the interval one muscle
needs to recover anyway. It is a way of buying volume with time, not a way of buying fatigue.

Two exercises may only be paired if they share neither lower-back demand, nor grip demand, nor
significant systemic demand. A deadlift and a barbell row are not a legal pair.

## Superset

Two exercises performed back-to-back on the **same** muscle.

The purpose of a superset is **fatigue**, which is the opposite of a pair's purpose. The two
terms are never used interchangeably in this repo, and "superset" is never used as a loose
synonym for "two exercises together".

## Double progression

A progression method with two stages. Load is held constant while reps are added, until the
top of the prescribed rep range is reached on every set. Only then is load increased, and reps
drop back to the bottom of the range.

Reps are the fine-grained instrument; load is the coarse one. This is what makes equipment with
large load jumps — dumbbells, kettlebells — progressable at all.

## Mesocycle

A block of four consecutive weeks: three loading weeks followed by one **deload**.

A mesocycle is the unit at which the programme changes. It has exactly one **theme**, and it is
the lifetime of a set of anchor prescriptions.

## Theme

The organising idea of a mesocycle — what the variable layer of the programme emphasises for
those four weeks. Examples: density, intensity, volume.

The theme governs accessories, rep ranges, rest, pairing and where failure is permitted.
It never governs the anchors.

## Deload

The fourth week of every mesocycle. A planned reduction in load and volume, taken whether or
not it feels necessary.

A deload is scheduled, not earned. Its purpose is to arrive *before* accumulated fatigue
becomes visible, because by the time fatigue is visible it is already weeks old.

## Rotation

The fixed cyclical order of session types. Sessions are consumed in order.

Because the rotation is a cycle rather than a calendar, a missed day is not a skipped muscle —
the next session is simply the next one in the cycle.

## Readiness

A subjective 1–5 rating of how prepared the body feels before a session, recorded at logging
time. Deliberately coarse and deliberately subjective.

## Grip demand

A property of an exercise: how much it depletes grip and forearms. `high`, `moderate` or `low`.

Grip is a shared, slowly-recovering resource, and it is the resource grappling depletes most.
Grip demand exists so that sessions can be scheduled around mat work without having to reason
about it session by session.

## Droppable session

A session deliberately designed so that missing it costs nothing: low systemic load, no anchor,
no movement that another session depends on.

It exists because a schedule with no planned rest day still needs somewhere for the rest to come
from. Rather than protecting a rest day that life will overwrite anyway, one session is made
cheap enough to lose. The rest day is then whichever day gets interrupted.

The trade is real and worth stating: unplanned rest lands wherever life puts it, which may be
after the hardest session rather than before it. A droppable session manages that; it does not
eliminate it. If a fortnight passes with nothing missed, one should be taken deliberately.

## Double day

A day carrying both a mat session and a lifting session. The lifting session begins
pre-fatigued and grip-depleted, so it must be one with low grip demand.

A double day is not a scheduling failure. Stacking two sessions onto one day is what protects a
genuine rest day elsewhere in the week — spreading nine sessions evenly across seven days leaves
no rest day at all.

## Buy-in

A conditioning piece performed at the **start** of a session, before the anchor. It serves as
general warm-up and as conditioning work in the same few minutes.

A buy-in is scored, not just performed. Its score is a performance measure in its own right, and
because it is sensitive to fatigue and sleep it doubles as an objective **readiness** signal.

The cost of a buy-in is that it pre-fatigues whatever follows. A conditioning piece placed before
an **anchor** lowers the load that anchor can carry — which is acceptable only if it is done
*consistently*, because the anchor measures change over time and an inconsistent warm-up makes
consecutive weeks incomparable.

## Cash-out

The same thing performed at the **end** of a session, after the lifting. Costs nothing in anchor
performance; delivers the same conditioning.

## Warm-up ramp

A graded series of ascending sub-working sets performed before an anchor. Distinct from a
general warm-up: a ramp is specific to the lift about to be performed, and its purpose is
tissue preparation under progressively increasing load.
