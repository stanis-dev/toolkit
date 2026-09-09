# Prompt lifetime and tool visibility

Read before changing a conditional rule, a transient instruction, or a tool's availability. For self-scoped rule wording, read [authoring](../writing/authoring.md). For a cross-turn store flag, read [runtime and state](runtime-state.md). Before asserting on a correction path, read [simulation assertions](../gates/simulation-assertions.md).

Rendering is additive. Once a `<Rule>` or any other prompt element renders, it stays in context for the rest of the conversation. Turning its JSX guard false later does not retract it. Tools are the exception: a tool is available to the LLM only on the turns it renders, though rules that referenced it can still be in scope.

For transient state like "while X is pending", write the condition into the rule text so it self-scopes ("If the subscription is not yet confirmed, ..."), or carry the state in a store flag that a render-path element reads next turn. Reserve `<Rule>` for invariants that hold from the first render onward. When a rendered element becomes wrong mid-conversation, correct it the same way: flip a one-way store flag, render the correction plus a tag, and assert on that tag.

For an instruction returned by a tool, read [tool results](tool-results.md). For the callback or observation that triggers the change, read [observations](observations.md).
