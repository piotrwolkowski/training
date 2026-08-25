# Constraints

> Copy this to `constraints.md` and fill it in. That file is gitignored.

Hard boundaries on what can be programmed. Not preferences — these are not overridden by a good
week, high motivation, or a mesocycle theme.

---

## Injuries and joint limitations

For each one, record: **history**, **what provokes it**, and critically **what makes it better**.
That last one decides the response. A joint that eases as load is worked up has a load-tolerance
problem, and the treatment is graded exposure — routing around it entirely makes it worse. A joint
that worsens with load needs the opposite.

Then write **rules**, in the imperative, that a programme can be checked against:

1. Movements never prescribed, and what replaces them.
2. Which anchor variants are permitted — an anchor is loaded progressively for months, so this is
   the highest-cost decision here.
3. Where warm-up ramps are mandatory.
4. **How hard the affected joint may be pushed.** This is not prose — put it in
   `joint-constraints.yaml`, where the validator enforces it. Every exercise already declares
   which joints it loads, so a `min_rir` floor and an `avoid` list are all that is needed. See
   [ADR 0004](../docs/adr/0004-joint-constraints-as-a-two-sided-model.md).

---

## Time

State sessions per week and minutes per session, then the consequences:

- **Hard sets per session** the budget actually supports.
- Whether **frequency** must carry weekly volume — with short sessions it does.
- Whether accessories run as **pairs** to fit.

A fragmented budget is not a small one. Six 35-minute sessions is the same weekly total as four
50-minute ones, but it cannot host long-rest, high-set compound work.

---

## Scheduling around other training

If you train another sport, write a **rule rather than a calendar** — schedules slip. Identify
which session in the rotation has the lowest `grip_demand` and make that the designated
double-day session.

---

## Venues and equipment

One section per venue, with a complete inventory. Be honest about what a venue cannot do: a venue
that cannot load an anchor progressively should carry a different kind of session rather than a
degraded copy of the same one.
