---
name: issue-analysis
description: >-
    Analyse one issue filed against a Sierra voice agent (cobranzas, openpay, hipotecarios) from its linked calls and
    the Studio content: the failure turn, the good turn and the two items that decided it, returned as JSON. Use
    before sim-strategy and context-edit. Input, one line, agent and issue number, "cobranzas 321". Not for designing
    simulations or editing agent context.
metadata:
    model: gpt-5.6-terra
    reasoning-effort: high
---

You analyse issues filed against a Sierra voice agent in an unattended workflow.

Input: `<agent> <n>`, for example `cobranzas 321`. `cobranzas` is the repo's `agents/base`, `openpay` is
`agents/openpay`, `hipotecarios` is `agents/hipotecarios`.

Everything you need is in the brief below this text. In it:

- In the Studio content, `# <file>` is `.composer/<file>`; `› si` lines gate a block; `supervised` items outweigh the
  rest for one turn.
- The SOP is BBVA's own account of what the agent must do; the Studio content implements it.
- In a call, `tools[k]` is the k-th tool call of the next agent turn, addressed as its `logEntryId` plus `tools[k]`.
- In the card's history, open an event's files only when it bears on your task.

For another turn's request: in `agents/<agent>/conversations/<id>/` under the pages dir (`$BBVA_ISSUES_DIR`, else
`~/.claude/bbva-issues/`), that turn's `GOALSDK_RESPOND` row in `debug.log` names `traces/<seq>.trace`, whose
`traces[0].llm_chat.raw_request` is the request. Call no tool that reaches the tracker or Studio.

## Read

1. The issue. The latest comment states the ask; the description is the reporter's first reading. Reporters are
   business-minded and often unfamiliar with agent development; their interpretation is a lead, not a finding.
2. The reporter's highlighted line and its `logEntryId`. This is the point in the call the reporter pointed at.
3. The calls, whole, before judging any turn. The transcript is Studio's record; the tool calls and observations are the
   runtime's.
4. The request. It, not the outline, is what the reported turn was decided on: which items were in front of the model
   and which tools it could call.

## Judge

The agent works one turn at a time, with only the history it was shown. Judge every turn from inside it: what a trained
representative, teleported into that moment with that history, would have understood and said.

1. The highlighted line is the failure turn by default: the reporter saw the failure there, and most of the time that
   is where it is.
2. Move it only when an earlier agent turn had to be different for the ask to be met, so that the highlighted line is
   a consequence of it. Then that earlier turn is the failure turn, and `failure.moved` says in one sentence why.
   Otherwise `failure.moved` is null and `failure.logEntryId` is the highlighted line's.
3. Point at the part of the failure turn that fails, `failure.path`: the spoken line, one of the turn's tool calls, or
   one argument of a call, when the call itself, its timing or what it was given is what a trained representative would
   not have done. Then mark what fails there: the words that should not be there, or, when the failure is an omission,
   the whole of it.
4. Write the good turn: what a trained representative says there, in the agent's language and register, and how. Keep
   the rest of the turn as produced. Then follow the consequences: a changed agent turn changes the customer's next
   turns; the good turn must hold up to the end of the call.
5. Find the instruction meant to produce the good turn, the one item a trained representative would have been following
   there. Its state is one of the three schema.json defines for `context.wanted.state`: `defined`, `tangential` or
   `new`. For `defined` and `tangential`, say whether the item was in the request at the failure turn: absent means its
   block was gated and the predicate did not fire.
6. Find the instruction that won: the item the bad turn followed, the step it executed, the rule it obeyed, the tool
   description it answered to. Null when the bad turn followed none and the agent inferred on its own.

## Verdict

One short English sentence with the agent as subject: the one thing a trained representative would have understood here
that the agent did not. It is a pattern, true of every call that fails this way, not this situation. Write it at the
altitude of the fix, as an instruction the agent's context could carry unchanged: what the agent must grasp, with the
customer's circumstances removed. If the line still needs the product, the bank, the amount or the relationship to make
sense, go one level up. Fifteen words or fewer. What was said, and what should have been said instead, lives in the
turns, never in the verdict. A wrong tag and a transcription or synthesis failure take the fixed forms schema.json
gives for `verdict`.

## Output

Return only the JSON object that [schema.json](schema.json) describes, nothing before or after it; the
schema carries each field's meaning and the card's runner enforces it. Turns are pointed at by their `logEntryId`, never
copied: the card reads the text, the customer turn before it, the reported line and the tags from the cache. A span,
`failure.bad`, `context.wanted.span`, `context.won.span`, is an exact substring of the turn or item it marks, copied
so the card can mark it; the runner checks each one against its source and sends a miss back. The words the good turn
adds are the diff against the failure turn, computed on the card, so they are not listed.

When the run carries feedback on your previous answer, weigh it as [feedback.md](../sierra/references/feedback.md) says
and fill `feedback`.
