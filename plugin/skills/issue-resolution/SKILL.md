---
name: issue-resolution
description: Takes the card from its three step answers to a verified fix, with the engineer.
---

You take the card from its three answers to a verified fix, with the engineer, who reads and answers in the page this
session streams to. Work in the repository; read the pages dir; touch nothing else. Write in English; quote agent and
customer lines in their language. The problem can come from:

- An issue: the card's source is the issue and its linked calls.
- A simulation: the card's source is the failing simulation and its replay.
- Free ask: a change I request.

The brief that opened the session gives the card's values, its source, the three answers and the card's history. In
the values:

- `<checkout>`: the card's own checkout, the working directory; `<agent-dir>` in it holds `simulations/` and
  `.composer/blocks/`; `<workspace>`, its Studio workspace; `<runs>`, this session's run files.
- `<baseline>`: the Sim Strategy's regression run before any edit.
- `<batch-branch>`, `<batch-workspace>`, `<batch-worktree>`: the batch's branch, its Studio workspace and the worktree
  bound to it.
- `<pages>`: the pages dir; the card's folder `cards/<n>/` holds `source.json`, `conversations/<id>/` and each step's
  `answer.json`.

The strategy step wrote the guard and ran it red, the context step applied the edit and pushed it to `<workspace>`;
both left their changes uncommitted in `<checkout>`: everything uncommitted there is the card's work. When the engineer
reruns a step with feedback, a message says which steps reran: re-read their answers, say what differs, review them
again. Pull `<workspace>` only with `python3 <scripts>/pull.py <agent> <checkout>`.

At each change of stage or verdict, run `python3 <scripts>/stage.py <agent> <n> <stage> <state>`. Stages and their
states, in order: `review` working, holds, wrong, contested; `repro` writing, reproduces, does-not-reproduce,
wrong-reason; `fix` applying, solved, refine, misguided; `regressions` running, found, fixing, clean; `merge` ready,
merged. `review wrong`, `review contested` and `fix misguided` take `--step`, the step at fault, and `--note`, one line
on what it got wrong and the skill passage or the turn it rests on, quoted.

Runs as `<references>/tooling.md`, Simulation runs, says.

## 1. Review

Say, one line each:

- whether the analysis names the right turn and the two items that decided it;
- whether the guard reproduces that turn's condition, per `<references>/sims/sim-diagnose.md`,
  from the transcripts of the strategy's `guard-red.json` run;
- whether the applied edits are the context answer's `item` and `gate` edits, `old` to `new` (`git -C <checkout> diff`),
  a pull of `<workspace>` leaves no diff, and every edit follows `<references>/agent/agent-design.md`;
- whether the regression list passes through every item the edits change.

If one does not hold, name the step at fault, the check and what that step should have said, run `stage.py … review
wrong`, and stop.

A rerun step may dispute your points in its `feedback`. Concede a point its basis settles; hold one it does not, with
the passage or turn that shows why. This reply is your last word on those points. If you hold any, run `stage.py …
review contested` with each held point and stop: the engineer rules, and a ruling settles its points.

## 2. Guard green

Apply the context answer's `tool` edits and any `flags.code` change. Run the guard and every expected red 5×; read the transcripts. Green is
5/5; less is a pass count and the turns that missed. An expected red that stays green, or a green sim that turned red,
is reported as such.

## 3. Regressions

With the guard 5/5, run the regression list 5× into `<runs>/regressions.json` and compare:
`python3 <scripts>/runset.py summary <runs>/regressions.json --vs <baseline>`. A regression passed 5/5 on the baseline,
fails now, and its failing turn follows from the edit; below 5/5 on the baseline is unstable, listed and not counted.
Fixing one is another edit, with the go, pushed as tooling.md, Studio content, says; then sections 2 and 3 again. Clean
is no regression left and the guard still 5/5.

## 4. Report

Write `<pages>/cards/<n>/resolve/report.md` and render it with `python3 <scripts>/card.py rs <agent> <n>`: the guard's
and the regression list's counts before and after with run ids, the failure turn's old and new line, the verdict
(solved, needs another pass, or which step was wrong) in one sentence, and what to try next when not solved. Anything
for the engineer to decide goes in the session, not the report.

## 5. Ready to merge

With the guard 5/5 and regressions clean, say so and list what goes. Then, each with the engineer's go:

1. Commit the card's work in `<checkout>`, one commit per concern, no attribution line.
2. `python3 <scripts>/batchmerge.py <agent> <batch> <the card's branch>`. Exit 0: merged and synced. Exit 2: the batch
   workspace holds Studio changes the batch branch never had. Exit 3: merge conflict, aborted. Exit 4: the workspace
   does not hold the merge. On any exit but 0, report what it printed and stop. Run no pull, merge or push in
   `<batch-worktree>` yourself.

Push the branch nowhere.
