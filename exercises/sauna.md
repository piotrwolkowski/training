---
slug: sauna
name: Sauna
pattern: recovery
primary: []
secondary: []
venue: [gym, home]
loads_joints: []
grip_demand: low
unilateral: false
load_increment_kg: 0.0
anchor: false
failure_allowed: false
metric: duration_min
---

# Sauna

Passive heat exposure, typically after training. Recorded with `duration_min` and, where the
figure is known, `temp_c`.

Carries no load and no hard sets - the `recovery` pattern is excluded from volume entirely. It
is logged because it is a deliberate intervention with a dose, and a dose that changes is worth
being able to see against how training went.

Post-session heat is genuinely useful for cardiovascular adaptation and for perceived recovery.
What it does not do is repair a training load that is simply too high; treat it as an addition
to recovery, never as permission to skip a deload.
