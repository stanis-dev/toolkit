# Rendering concern routing

This page routes older links. Read every matching leaf, not the whole set.

- A rule surviving a guard change, transient guidance, or tool visibility: [prompt lifetime](prompt-lifetime.md).
- Observation Conditions, `OnActivation`, latching, keys, or resets: [observations](observations.md).
- Monitors, in-flight or final replies, or migration to Conditions: [monitors](monitors.md).

The semantics are implemented in the SDK monorepo, which is not reachable here. Before designing around a timing or ordering mechanic, confirm it with `ask_sierra_assistant` or prove it in a simulation.
