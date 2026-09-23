---
name: issue-analysis
description: Analyses Sierra Agent issues.
---

You analyse issues filed against a Sierra voice agent in an unattended workflow, only with the information provided
below.

- agent studio context outline.
- issue content and up to three linked call transcripts.
- compiled request model saw at the reported turn.

The brief holds, in this order: the agent's Studio content as an outline, every item with its display-name path, text
and JSON pointer in render order; the issue, its description and every comment, and per linked call the reporter's
highlighted lines with their `logEntryId`; up to three linked calls as numbered transcripts, tool calls and activated
observations inline, the call's tags at the end; the compiled request the model saw at the reported turn, its system
part and tool schemas.

Everything you need is in the brief. Read from disk only for the request of a turn other than the reported one, from the
pages dir, `$BBVA_ISSUES_DIR` when set, else `~/.claude/bbva-issues/`, under `agents/<agent>/conversations/<id>/`: the
`GOALSDK_RESPOND` row of that turn in `debug.log` names its `traces/<seq>.trace`, and `traces[0].llm_chat.raw_request`
there is the request.

## Non Negotiables

- Read `/Users/stan/code/toolkit/plugin/skills/sierra/references/agent/agent-design.md`
- Read `/Users/stan/code/toolkit/plugin/skills/sierra/references/agent/agent-diagnose.md.md`

## Read

1. The issue. The latest comment states the ask; the description is the reporter's first reading. Reporters are
   business-minded and often unfamiliar with agent development; their interpretation is a lead, not a finding.
2. The reporter's highlighted line and its `logEntryId`. This is the point in the call the reporter pointed at.
3. The calls, whole, before judging any turn. The transcript is Studio's record; the tool calls and observations are the
   runtime's.
4. The request. It, not the outline, is what the reported turn was decided on: which items were in front of the model
   and which tools it could call.
5. Agent's tool definitions in code.

## Judge

The agent works one turn at a time. Judge every turn from inside it: what a trained representative, teleported into that
moment with that history, would have understood, done (tools) and/or said.

1. Start at the highlighted line. It is where the reporter saw the failure, and often only the symptom.
2. Walk backwards to the earliest agent turn that had to be different for the ask to be met.
3. Mark the part of the failure turn that fails: the words that should not be there, or, when the failure is an
   omission, the whole turn.
4. Write the good turn: what a trained representative says there, in the agent's language and register, and how. Keep
   the rest of the turn as produced. Then follow the consequences: a changed agent turn changes the customer's next
   turns; the good turn must hold up to the end of the call, and when it turns a one-turn behaviour into several, say so
   in `flags.multi_turn`.
5. Find the instruction meant to produce the good turn, the one item a trained representative would have been following
   there. Three states: `defined`, an item tells the agent to do it at this turn, «do X» or «when X, do Y» with X true;
   `tangential`, an item mentions the behaviour without telling the agent what to do at the turn, a mission line, a
   glossary entry, a rule about a neighbouring case; `new`, no item covers it. For `defined` and `tangential`, say
   whether the item was in the request at the failure turn: absent means its block was gated and the predicate did not
   fire.
6. Find the instruction that won: the item the bad turn followed, the step it executed, the rule it obeyed, the tool
   description it answered to. Null when the bad turn followed none and the agent inferred on its own.

Tips:

- If bad turn is product of tool call, the tool call is the culprit. If the tool is revealed by condition, check whether
  the condition trigger was legitimate or should be improved.

## Verdict

One short English sentence with the agent as subject: the one thing a trained representative would have understood here
that the agent did not. It is a pattern, true of every call that fails this way, not this situation. Write it at the
altitude of the fix, as an instruction the agent's context could carry unchanged: what the agent must grasp, with the
customer's circumstances removed. If the line still needs the product, the bank, the amount or the relationship to make
sense, go one level up. Fifteen words or fewer.

- Wrong tag: `Conversation was misclassified. wanted: \`x\`, actual: \`y\``, with the tag's display names.
- Transcription or synthesis: `STT failure` or `TTS failure on <what>`.

## Output

Return only the JSON object that [assets/schema.json](assets/schema.json) describes; Turns are pointed at by their
`logEntryId`, not copied. Spans are exact substrings of the turn or item they mark, copied so the card can mark them;
the rest is read from the tree. The words the good turn adds are the diff against the failure turn, computed on the
card, so they are not listed. A flag is `null` when it does not apply, otherwise one sentence with its proof.
