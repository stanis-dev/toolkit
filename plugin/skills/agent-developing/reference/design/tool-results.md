# Tool results and instruction channels

Read before changing a tool's return value or an instruction attached to a result. Before a code edit, load the matching canonical skill per [canonical guidance](../session/canonical-guidance.md). For the wording of an instruction or a result, read [authoring](../writing/authoring.md). When a result depends on a persisted flag or a fresh clock, read [runtime and state](runtime-state.md).

Return a plain string when the tool hands back only a result. Use the structured `ToolResult`, built with `controls.result`, for structured data or an attached instruction. Read its shape in the installed SDK types under `node_modules/@sierra/agent` and in `.composer/docs/tool-code-implementation.md`. Keep `data` a clean, semantic record. It renders verbatim as the tool response, so distill a raw API response into semantic fields first.

Choose the instruction channel by how long the guidance must hold. One turn: the top-level `instructions`. Several turns: an instruction field inside `data`. The whole conversation: PromptContext, which is append-only and cannot be retracted. The SDK source that implements these channels is not reachable here. When the exact lifetime matters, confirm it with `ask_sierra_assistant` or prove it in a simulation with a tag on the path.

For which surface carries an instruction in the first place, read [placement](placement.md). When the guidance must expire or a result can become wrong later, read [prompt lifetime](prompt-lifetime.md).
