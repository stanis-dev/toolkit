---
name: context-edit
description: Edits the context that decided the failure turn.
---

You find the context responsible for the card's failure turn, write the edit that makes the good turn the agent's
natural one, and apply it. The problem can come from:

- An issue: you get the analysis, the strategy and the linked call with its request at the failure turn.
- A simulation: you get the analysis, the strategy and the failing replay with its request at the failure turn.
- Free ask: you get the analysis and the strategy of a change I request.

1. Diagnose from the request at the failure turn per [agent-diagnose.md](../sierra/references/agent/agent-diagnose.md),
   its Relevant context and Known failure modes, starting from the analysis's two `context` items.
2. Write the edit per [agent-design.md](../sierra/references/agent/agent-design.md): the analysis's good turn must follow
   from the edited request, and the guard's expectations must pass by it.
3. Apply each `item` and `gate` edit at its pointer and push them to `<workspace>` as
   [tooling.md](../sierra/references/tooling.md), Studio content, says; this push needs no go. A `tool` edit or a change
   `flags.code` names is not applied. Leave the files uncommitted.
4. Return only the JSON object that [schema.json](schema.json) describes.

When the run carries feedback on your previous answer, weigh it as [feedback.md](../sierra/references/feedback.md) says
and fill `feedback`.

Everything you need is in the brief below this text. In it:

- Studio content, `# <file>` is `.composer/<file>`; `› si` lines gate a block; `supervised` items outweigh the rest for
  one turn.
- The request is the truth of the turn; the outline is where it came from. Blocks reach it as sections: journey as
  `<goal>`, rules as `<rules>`, policies as `<policies>`, response phrasing as `<language_tone_and_structure>`, custom
  blocks as `<reference_information>`, glossary as `<glossary>`; tool descriptions as function schemas, verbatim from
  code; progress indicators as assistant turns.
- In a conversation, each line carries its `turn`; `tools[k]` is the k-th tool call of the next agent turn.

For another turn's request: in the conversation's folder (the brief's `cached at`), that turn's `GOALSDK_RESPOND` row in
`debug.log` names `traces/<seq>.trace`, whose `traces[0].llm_chat.raw_request` is the request. Whether a predicate fired
is in that log's `OBSERVATIONS` rows.
