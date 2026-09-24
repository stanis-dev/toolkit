---
name: context-edit
description: >-
    Find the Studio context responsible for a failure turn on a Sierra voice agent (cobranzas, openpay, hipotecarios)
    and write the wording change that makes the good turn the natural one, returned as JSON: cause, what the model saw,
    the edit as old and new text with its ripple; then apply it to the issue's own Studio workspace. Use after
    sim-strategy. Input, one line, agent and issue number, "cobranzas 321". Not for pushing to any other workspace.
metadata:
    model: gpt-5.6-terra
    reasoning-effort: high
---

You find the context responsible for the failure turn and write the edit that makes the good turn the agent's natural
one, and apply it to the issue's own workspace. No tracker; Studio only through the push in Apply. Say in
`flags.missing` when something you needed is not there.

Input: `<agent> <n>`, for example `cobranzas 321`. `cobranzas` is the repo's `agents/base`, `openpay` is
`agents/openpay`, `hipotecarios` is `agents/hipotecarios`.

Everything you need is in the brief below this text. In it:

- In the Studio content, `# <file>` is `.composer/<file>`; `› si` lines gate a block; `supervised` items outweigh the
  rest for one turn.
- In a call, `tools[k]` is the k-th tool call of the next agent turn.
- In the card's history, open an event's files only when it bears on your task.

Read from disk only for the request of another turn, from the call's cache path: the `GOALSDK_RESPOND` row of that turn
in `debug.log` names its `traces/<seq>.trace`, and `traces[0].llm_chat.raw_request` there is the request; and for a
tool's source file in the repository, when the cause is a description or an instruction in code.

## Non Negotiables

- Read `/Users/stan/code/toolkit/plugin/skills/sierra/references/agent/agent-design.md`: the edit follows it.
- Read `/Users/stan/code/toolkit/plugin/skills/sierra/references/agent/agent-diagnose.md`, its Relevant context and
  Known failure modes. Skip its numbered steps.

## Read

1. The analysis and its two `context` items. Start from those two items; do not search for them again. The strategy:
   the guard, whose expectations the edit must make pass.
2. The request at the failure turn. Blocks reach it as sections: journey as `<goal>`, rules as `<rules>`, policies as
   `<policies>`, response phrasing as `<language_tone_and_structure>`, custom blocks as `<reference_information>`,
   glossary as `<glossary>`; tool descriptions arrive as function schemas, verbatim from code. Progress indicators sit
   in the transcript as assistant turns. This request is the truth of the turn; the outline is only where it came from.
3. The outline: where each item lives in the tree and what gates it. Tool descriptions and instructions are strings in
   the agent's code.
4. When the item you point at reads differently in the outline than in the request, the tree has moved since the call:
   report both.

## Judge

Judge the failure turn from inside its request.

1. The two items from the analysis are layer 1 of the relevant context. Read the request around both. Add an entry from
   layer 2 or 3 only when the cause sits there.
2. Why did the wanted item not decide the turn? Absent from the request: find its gate and, in debug.log's
   `OBSERVATIONS` rows, whether the predicate fired. Present: read how the item that won outweighed it. Tangential: what
   a turn instruction would have to say that the mention does not. New: where in the tree the behaviour belongs, next to
   which items.
3. Name the `cause`; for `overpowered`, say how.
4. Write the edit as agent-design.md says. The good turn from the analysis must follow from the edited request; the
   guard's expectations must pass by it.
5. When two edits compete, return the one with the smaller ripple and put the other in `alternatives`, one sentence
   each.

## Apply

Apply the edit to the block file at the pointer, the `old` and `new` of your answer and nothing else, and push it to
`<workspace>` as tooling.md, Studio content, says; this push needs no go. When
lint fails or the diff after the second pull is not empty, say what it reported in `flags.push`. A change `flags.code`
names is not applied. Leave the file uncommitted: it stays the card's work until merge.

## Flags, instead of stopping

What the engineer decides on goes in `flags`, the four schema.json describes; nothing stops the step.

## Output

Return only the JSON object that [schema.json](schema.json) describes, nothing before or after it. Point at items by
block file and JSON pointer as blocks.py prints them; copy item text only where you mark or edit it. An `also` span is
an exact substring of the item it marks; `also` is empty in the common case. A flag is `null` when it does not apply,
otherwise one sentence with its proof.

When the run carries feedback on your previous answer, weigh it as [feedback.md](../sierra/references/feedback.md) says
and fill `feedback`.
