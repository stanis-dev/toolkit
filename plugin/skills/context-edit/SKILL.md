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
one, and apply it to the issue's own workspace, where the engineer reviews it before anything is merged. They know the
agent; your output is the diagnosis and the diff. No tracker; Studio only through the push in Apply. Say in
`flags.missing` when something you needed is not there.

Input: `<agent> <n>`, for example `cobranzas 321`. `cobranzas` is the repo's `agents/base`, `openpay` is
`agents/openpay`, `hipotecarios` is `agents/hipotecarios`.

You work from the brief that follows this text. It holds, in this order:

- The agent's Studio content as an outline: one line per item, path, text and JSON pointer, tab-separated, in render
  order. A `# <file>` line opens each file; the item's file is `.composer/<file>`. `› si` lines are the predicates that
  gate a block; `supervised` marks items that outweigh the rest for one turn.
- The issue: its description, every comment, and per linked call the reporter's highlighted lines with their
  `logEntryId`.
- The Issue Analysis answer, `agents/<agent>/analysis/<n>.json`, and the Sim Strategy answer,
  `agents/<agent>/strategy/<n>.json`, when it exists.
- The linked call the analysis names, with its cache path, as a numbered transcript: turn number, speaker (A agent, U
  customer), `logEntryId`, text; under a line, `[obs]` is an observation activated after it and `tools[k]` the k-th tool
  call of the agent turn printed right after, with its arguments. The call's tags close it. The call's release is in the
  heading.
- The compiled request the model saw at the failure turn: its trace path, its system parts and its tool schemas. The
  request's conversation messages are the call's transcript up to that turn.
- The lane: the values the Apply section names.

Read from disk only for the request of another turn, from the call's cache path: the `GOALSDK_RESPOND` row of that turn
in `debug.log` names its `traces/<seq>.trace`, and `traces[0].llm_chat.raw_request` there is the request; and for a
tool's source file in the repository, when the cause is a description or an instruction in code.

## Non Negotiables

- Read `/Users/stan/code/toolkit/plugin/skills/sierra/references/agent/agent-design.md`: the edit follows it.
- Read `/Users/stan/code/toolkit/plugin/skills/sierra/references/agent/agent-diagnose.md`, its Relevant context and
  Known failure modes. Its numbered steps are for a session with the engineer; this one runs unattended.

## Read

1. The analysis: the verdict, the failure turn by `logEntryId`, its bad spans, the good turn, and `context`: the
   instruction meant to produce the good turn with its state, `defined`, `tangential` or `new`, and whether it was
   present at the turn, and the instruction that won. Start from those two items; do not search for them again. The
   strategy: the guard, whose expectations the edit must make pass.
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
3. Name the cause, one of the seven schema.json defines for `cause`; for `overpowered`, say how.
4. Write the edit as agent-design.md says. The good turn from the analysis must follow from the edited request; the
   guard's expectations must pass by it.
5. When two edits compete, return the one with the smaller ripple and put the other in `alternatives`, one sentence
   each.

## Apply

Apply the edit to the block file at the pointer, the `old` and `new` of your answer and nothing else, and push it to
`<workspace>` as tooling.md, Studio content, says; this push needs no go, the engineer reviews it before merge. When
lint fails or the diff after the second pull is not empty, say what it reported in `flags.push`. A change `flags.code`
names is not applied. Leave the file uncommitted: the runner commits it.

## Flags, instead of stopping

What the engineer decides on goes in `flags`, the four schema.json describes; nothing stops the step.

## Output

Return only the JSON object that [schema.json](schema.json) describes, nothing before or after it; the schema carries
each field's meaning and the runner enforces it. Items are pointed at by block file and JSON pointer as blocks.py prints
them; item text is copied only where it is marked or edited, the card reads the rest from the tree. An `also` span is an
exact substring of the item it marks; the runner checks it and sends a miss back. `also` is empty in the common case:
the card's Studio Context part is built from the analysis, the wanted item as role A and the item that won as role B. A
flag is `null` when it does not apply, otherwise one sentence with its proof.

When the run carries feedback on your previous answer, weigh it as [feedback.md](../sierra/references/feedback.md) says
and fill `feedback`.
