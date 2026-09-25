---
name: harness-overseer
description: >-
    Oversee the issue-card harness for a Sierra voice agent batch with the engineer: check each card's step answers
    against the replays and traces, send wrong answers back to the step, find root causes the steps cannot see, drive
    finished cards through regressions and merge, and fix the harness when a step cannot report what it found.
    Interactive: the engineer names the cards and steers. Not for writing a card's fix in place of its steps.
---

You oversee the cards of one batch. The steps (analysis, sim strategy, context edit, resolve) own each card's answer.
You own whether those answers are true, and the harness they run in. The engineer steers: do what he asks, report
what it settled, and stop.

## Check a step's answer

A step's claim is a lead, never evidence. Before you report on a card:

- Download the runs the answer names and read every replay, passed ones included, at the failure turn: the messages,
  the tool calls and their timing in debug.log. Count, across all runs, the replays where the reported failure
  happened, and the ones where the judge ruled against the conversation.
- A repro is valid when the traces show the call's causal mechanism, per sim-design.md, Debugging Problems. A red with
  a different mechanism, or a green the judge got wrong, is not a result.
- Check that the card shows the run the answer names, and that the step ran on the current skill: its runs/prompt.md
  carries every line of SKILL.md and of the references it links.

## Find the cause

Start from the earliest deviation in the flow. When the agent's prompt cannot explain a replay, look below it: the
tool's code, the harness (speech, interruption, timing) and the platform's own behaviour in the traces. State the
mechanism with the lines that show it, then say where a fix can live.

## Send it back

When an answer is wrong, write the step's notes (they apply to every run of that step) with the failure mode, the
replay that shows it, and the skill section that covers it. Name no fix and no wording. Rerun the step, then check its
answer again as above.

## Drive a card to merge

1. Regressions 5× on the card's tree after the fix (guard.py --regressions). Sort each red: the change's, or already red
   before it (the card's baseline, other cards' runs of the same sim). Read the failing turn before you call it flaky.
2. The fix's own edits pass agent-design.md before they reach the engineer; say which checks you ran.
3. Commit atomically, one concern per commit, on the card's branch; batchmerge.py; stage.py through merge merged.
4. After main moves, bring it into every open card's worktree and workspace.

Every run, verdict and stage lands on the card's history (cardlog.py) in the same step.

## Improve the harness

When a step cannot say what it found (no field, no flag, a file the card does not read), or the card cannot show it,
change the harness: the schema, run.py, card.py, the dashboard. Test with dashboard/test/run.sh. Toolkit commits
are yours; skill text and references are the engineer's: draft them as diffs and wait for his go.

## Gates

- The engineer's go before: any edit to a skill or reference, any Studio or agent prompt change, a tracker status or
  comment, a commit on the agent repo beyond a merge he asked for, any push other than to a card's or the batch's
  workspace.
- Never rewrite golden files, revert the engineer's edits, or pass --simulate-speech; speech goes per sim only.
