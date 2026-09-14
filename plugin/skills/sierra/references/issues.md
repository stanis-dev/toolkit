# Agent Studio Issues

When dealing with an issue, your goal is to understand what needs to be done in order to close the issue.

- Reporters are frequently unfamiliar with even the basics of agent development and are business minded. Their interpretation is frequently unreliable and requires translating to agent development.
- Don't expect the format of the issue to be observed by reporters. It's common for an issue to not have suggested correct behaviour.

## Types of Issues

Issues are not created only for bugs, but for all type of feedback for the agent. Two axes
describe one: what kind of problem it is, and what kind of change closes it.

- Bug vs Improvement: agent broke an existing contract vs reporter requests new behaviour agent didn't have.

Change types:
- Behaviour: the agent does something different. A rule, a flow, tool logic.
- Wording: the agent says something different and does the same. Naturalness, register and a
  requested substitution are all this one.
- Voice: the fix is on the synthesis side, the rewrite list or a spelling.
- Transcription: the fix is on the STT side.
- No change: already fixed, not reproducible, or waiting on a BBVA decision.

## Bucket

The analysis names the mechanism that broke, in Spanish: «Pedido de humano», «Cierre de
llamada». Issues with the same mechanism share a bucket, whatever the reporter called them.
Before naming one, read the ones that exist,
`grep -h bucket: ~/.claude/bbva-issues/agents/<agent>/cards/*.html | sort -u`; reuse a name when
the mechanism is the same, write a new one only when none fits. An analysis that changes the
mechanism moves the issue: change its line.

## Report

Report back per the Issue Analysis section in [info.md](./info.md) and nothing else. I will
request details if I need to. What goes in each part:

### Top part

- Reporter's words: reporter's ask, paraphrased into a single, short sentence.
- Closes it: 3-10 word tldr on customer-facing agent change that'd close the issue.

### Conversation

Turns that matter and one surrounding turn. Read [agent-diagnose.md](./agent/agent-diagnose.md) and [agent-design.md](./agent/agent-design.md), then mark 3 spans:

1. turn reporter chose.
2. what agent did/said (bad). 
3. what agent whould have done/said (good).

The last row is the call's post-call tags, `ti-webhook` in the gutter, name and value as the
tracker holds them. When the fix changes a tag, that row is the failure row and takes the diff.

When considering "good" agent turn:
- consider what a trained human professional would say in given situation. do so with the whole conversation in mind.
- changing agent turn can lead to different customer responses. make sure that the "good" proposition accounts for all the effects until the end of the conversation.
- pay attention not only to "what" agent would say, but also to "how".

## Recipies

- Issue already fixed: stop workflow, gather proof and report to me.
- Transcription: unless mis-transcribed word/expression is very common and critical, stop analysis and just let me know.
- Multi-turn effects: ask will potentially affect several agent turns or transform one-turn behaviour into multi-turn. Let me know asap, multiturn changes are especially complicated.
