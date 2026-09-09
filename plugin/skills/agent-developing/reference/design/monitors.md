# Conditions and monitors

Read before using `useAgentMonitors`, detecting a conversation-final agent reply, or migrating between a monitor and a Condition. For an effect persisted to the next turn, read [runtime and state](runtime-state.md). When changing a final-reply consumer or its tests, read [simulation assertions](../gates/simulation-assertions.md) and [correctness review](../gates/verification.md). Before writing observation text or a tag name, read [authoring](../writing/authoring.md).

Conditions evaluate during the turn, so their effects land in the same turn's prompt, and they never see the in-flight reply, so never a conversation-final agent reply. `useAgentMonitors` runs after the reply is emitted, sees it, and its effects land next turn. Both share one latch pool keyed by observation text.

Customer-behavior observations move from a monitor to a Condition cleanly and land a turn earlier. Agent-behavior observations migrate only when nothing consumes the flag after a conversation-final reply: post-conversation hooks, analytics tags, simulation assertions. Check every consumer before migrating. The turn loop that fixes the evaluation order is not reachable here. Confirm it with `ask_sierra_assistant` before designing around it.

For latching or re-arming, read [observations](observations.md). For a prompt effect that must expire, read [prompt lifetime](prompt-lifetime.md).
