---
name: batch-driver
description: >-
    Drive one batch of Sierra voice agent issues (cobranzas, openpay, hipotecarios) once its cards are done: align it
    with main, run the combined check, sort each failure as the batch's, main's or flaky, send the batch's back to the
    cards that own them, and keep the draft PR current. Interactive: the engineer starts and steers each step. Input,
    the batch brief. Not for fixing an issue.
---

You drive one batch after its cards are done, with the engineer, who reads and answers in the page this session
streams to. The cards own the fixes and you own the batch: you change no Studio content, no skill, no tracker status,
and push nothing to a workspace but the batch's and your own main workspace. Anything that needs a fix goes back to the
card that owns it. Write in English; quote agent and customer lines in their language.

The engineer steers: do the step he asks for, report what it settled, and stop. Never start the next step on your own.

The brief carries the values:

- `<agent>`, `<batch>`: the agent and the batch's MMDD; `<batch-branch>`, `<batch-worktree>`, `<batch-workspace>`: its
  branch, the worktree that has it checked out, and its Studio workspace.
- `<main-worktree>`, `<main-workspace>`: your own worktree on origin/main and its workspace; they hold main and nothing
  else, and exist only to count a simulation on main alone.
- `<cards>`: the batch's issues, each with its state, branch, guard, regression list, and its runs: the sim strategy's
  guard run and regression baseline before the fix, the resolution's guard and regression runs after it, each with the
  commit of main it ran on and its pass counts.
- `<pr>`: the batch's draft PR, if any.
- `<pages>`, `<scripts>`, `<references>` as for the resolution.

The page shows where the batch stands from one command, which you run at each change of stage:
`python3 <scripts>/batchstage.py <agent> <batch> <stage> <state> [--note "one line"]`. Stages and their states, in
order: `align` working, done, conflict; `check` running, clean, found; `sort` done; `route` sent, waiting, back;
`pr` written, pushed.

## 1. Align

Run `python3 <scripts>/mainsync.py <agent> <batch-worktree>`. Exit 0: the batch holds main and its workspace holds the
batch. On any other exit, report what it printed and stop.

## 2. Check

The list: every card's guard, the union of the cards' regression lists, and the simulations main's merges since the
batch started changed or that pass through the Studio items those merges changed. Run it once, 5×, on
`<batch-workspace>`, the launch in tooling.md, Simulation runs, into `<pages>/agents/<agent>/batches/<batch>/check/`.
Read the transcripts of every result below n/n, not the judge alone.

## 3. Sort

Give each simulation below n/n its before count, the latest of the cards' runs of it: the resolution's after-fix run,
else the strategy's baseline. A card run is usable only when main has not changed, since the commit it ran on, the
Studio items the simulation's conversations pass through; otherwise, and for a simulation no card ran, refresh your main
workspace (`python3 <scripts>/mainws.py <agent> <batch>`) and run it 5× on `<main-workspace>`: that count is its before
count. Then:

- **flaky**: one run off its before count. Run it 5× again on `<batch-workspace>`; still two or more below over the
  ten, it is not flaky.
- **main's**: it fails the same way on main alone: the same expectation, the same turn.
- **the batch's**: everything else. Its owner is the card whose guard it is, else each card whose regression list
  names it, else the card whose edit its failing turn passes through.

Report the three lists, one line per simulation: before, now, the failing turn and, for the batch's, the owner.

## 4. Route

When the engineer says so, send each of the batch's failures to its owner:
`python3 <scripts>/reopen.py <agent> <n> --batch <batch> --evidence <file>`, the file holding the simulation, before
and now counts with their run links, the judge lines and the failing turn quoted, and main's merges since the card's
run. The card reopens for a second pass and its resolution session takes it from there. Report main's and the flaky
ones to the engineer; do nothing else with them.

## 5. Recheck

When a reopened card has merged again, run 1 for the batch, then only what failed, and sort again. After two passes
with no progress on a simulation, stop and ask the engineer.

## 6. PR

Write the description as [pr.md](../sierra/references/pr.md) says, from the cards and the latest check: each fix and
its evidence, the check's counts, main's and the flaky ones named. Push `<batch-branch>` to origin, open the draft PR
if there is none, and update its description. Never mark it ready: that is the engineer's.
