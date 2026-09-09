# Observations and activation

Read before using an Observation Condition, `when.some(...)`, `<OnActivation fn>`, the `key` prop, or a resettable component. Before writing observation text, read [authoring](../writing/authoring.md). For a flag stored across turns, read [runtime and state](runtime-state.md). Before asserting on activation or re-arming, read [simulation assertions](../gates/simulation-assertions.md).

Observation Conditions batch into shared classification calls and latch once per conversation, which suits "did X ever happen" detection. Many crisp single-topic observations combined with `when.some(...)` cost no more than one compound observation, so prefer them.

`<OnActivation fn>` runs after render. The only reliable effect inside `fn` is a store update, visible next exchange. Set a flag and let a render-path element act on it next turn. Latching and re-arming depend on per-node identity, the `key` prop, and `useResettableComponent`. The activation tests that spell this out live in the SDK monorepo and are not reachable here. Confirm the mechanic with `ask_sierra_assistant` or prove it in a simulation before designing around it.

If an activation emits transient prompt text, read [prompt lifetime](prompt-lifetime.md). If it replaces a monitor or observes an agent reply, read [monitors](monitors.md).
