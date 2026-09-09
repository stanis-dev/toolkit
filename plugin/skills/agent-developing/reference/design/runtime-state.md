# Runtime and cross-turn state

Read before relying on a JavaScript feature, a global, a React-like SDK API, stored state, or a time-sensitive decision.

Agent code runs in Goja, a pure-Go JavaScript engine embedded in the Sierra service. It is not Node or a browser, and its standard-library coverage is partial. Confirm a global, method, or language feature exists in Goja before using it, even when it works in local Node tests.

The VM is reconstructed each turn. Module-level variables, closures, and component locals all reset. Root store and memory are the only cross-turn state, and everything written to them must be serializable. That state round-trips through JSON at every turn boundary, and the round trip rewrites JS-only values: an `undefined` property comes back as `null` on the next turn, so a `=== undefined` check breaks across turns. Write `null` explicitly, or delete the key, and test the round trip in a simulation.

Recompute every time-dependent decision at consumption time with a fresh clock: holds, cutoffs, and eligibility windows. For an environment-controlled toggle, read [agent config](agent-config.md).

The SDK looks like React, with JSX, components, and hook-shaped calls, but it is a separate implementation. Matching names do not guarantee matching behavior. Treat React intuition as a hypothesis. Read the definition in the installed SDK before relying on any method, hook, type, or JS primitive, and treat an existing call site as one candidate, not proof of the best supported method. When a runtime question stays open, ask `ask_sierra_assistant`. For prompt and observation timing, read the matching leaf through [rendering](rendering.md).

When runtime behavior is in doubt, prove it in a simulation. Emit a tag from the code path under test and assert on it, so you confirm the segment ran and was not short-circuited by the simulation runner. Read [simulation assertions](../gates/simulation-assertions.md) before writing that assertion.
