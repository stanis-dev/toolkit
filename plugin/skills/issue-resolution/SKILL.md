---
name: issue-resolution
description: >-
    Take one Sierra voice agent issue (cobranzas, openpay, hipotecarios) from its three step answers to a verified fix,
    with the engineer in the loop: review the analysis, the guard the sim strategy ran red and the edit the context
    step applied, run the guard green, check the regressions, report, merge into the batch. Interactive. Input, the
    resolve brief of the issue. Not for producing the three answers.
---

You take the issue from its three answers to a verified fix, with the engineer, who reads and answers in the page this
session streams to. Work in the repository; read the pages dir; touch nothing else. Write in English; quote agent and
customer lines in their language.

The brief that opened the session gives this issue's values, then the issue and the three answers, and ends with the
card's history; open an event's files only when it bears on what you are doing. The values:

- `<checkout>`: the issue's own git checkout, the working directory.
- `<agent-dir>`: the agent's directory in it; its simulations under `simulations/`, its Studio content under
  `.composer/blocks/`; `<sierra>`, the CLI binary in it; `<workspace>`, the issue's own Studio workspace; `<runs>`, the
  folder for this session's run files.
- `<agent>`, `<n>`: the agent and the issue number.
- `<baseline>`: the Sim Strategy's regression run, the file it wrote with its list run 5× before any edit.
- `<batch>`: the batch's MMDD; `<batch-branch>`, `<batch-workspace>`, `<batch-worktree>`: the batch's branch, its
  Studio workspace and the worktree that has the branch checked out and Ghostwriter bound to that workspace;
  `<batch-agent-dir>`, the agent's directory in that worktree, its CLI at `<batch-agent-dir>/node_modules/.bin/sierra`.
- `<pages>`: the pages dir; the card's folder `cards/<n>/`: `card.html`, the issue as `source.json`, the linked calls
  under `conversations/<id>/` (details.json, debug.log, traces/), the answers `analysis/answer.json`,
  `strategy/answer.json`, `context/answer.json`.

The strategy step wrote the guard and ran it red, the context step applied the edit and pushed it to `<workspace>`;
both left their changes uncommitted in `<checkout>`. Everything uncommitted there is the card's work; HEAD is the branch
before it. The engineer can rerun a step with feedback: the step works on the tree as it is, and a message tells you
which steps reran and where their new answers are. Re-read those answers, say what differs, and review them again.
Pull `<workspace>` only with `python3 <scripts>/pull.py <agent> <checkout>`: it commits what main's merges brought as
base and leaves the card's work uncommitted.
- `<scripts>`: brief.py, card.py, blocks.py, runset.py, sync.py, pull.py, batchmerge.py.
- `<references>`: the workflow's reference, issues.md, sims/, tooling.md.

The page shows where the issue stands from one command, which you run at each change of stage or verdict:
`python3 <scripts>/stage.py <agent> <n> <stage> <state>`. Stages and their states, in order: `review` working, holds,
wrong, contested; `repro` writing, reproduces, does-not-reproduce, wrong-reason; `fix` applying, solved, refine, misguided;
`regressions` running, found, fixing, clean; `merge` ready, merged. `review wrong` and `fix misguided` take `--step`,
the step at fault (analysis, strategy or context), and `--note`, one line on what it got wrong and the skill passage
or the turn it rests on, quoted. `review contested` takes `--step` and `--note` too, as below.

## 1. Review

Read the three answers against the card and the linked call. Say, one line each:

- whether the analysis names the right turn: the failure turn is where the customer's move went unanswered, the good
  turn is what the Studio content asks for, and the two items it points at are the ones that decided the turn;
- whether the guard reproduces that turn's condition: read the transcripts of the strategy's red run, `guard.red`;
  the persona makes the customer's move at the same point of the journey, and the guard is red on the behaviour the
  analysis names, not on something else; a `no_repro` or `wrong_reason` flag fails this check;
- whether the applied edit is the context answer's: `git -C <checkout> diff` the edited block against the answer's
  `old` and `new`, and a pull of
  `<workspace>` leaves no diff;
- Verify that proposed edit aligns with `/Users/stan/code/toolkit/plugin/skills/sierra/references/agent/agent-design.md`
  best practices.
- whether the strategy's regression list covers the edit: one or more listed simulations pass through the item it
  changes.

If one of these does not hold, name the step at fault (analysis, strategy or context), which check failed, why, and what
that step should have said. Then stop: the engineer reruns the step or overrules you.

The rerun step weighs your points against its own skill and may dispute some: its answer's `feedback` holds a verdict
per point, with the passage or turn it rests on. Read each disputed point against the same skill text and evidence.
Concede a point its basis settles; hold one it does not, with the passage or turn that shows why. This reply is your
last word on those points. If you concede them all, review the new answer as usual. If you hold any, run
`stage.py <agent> <n> review contested --step <step> --note "<each held point: why, with its basis>"` and stop: the
engineer rules. A ruling for the step settles its points: do not raise them again.

If everything holds - continue to #2.

## 2. Guard green

With the go, apply any code change the context step flagged. Run the guard 5× and every expected red the strategy
lists: `<references>/tooling.md`, Simulation runs, gives the launch, the wait and the readers. Read the transcripts. Green is 5/5; less is a pass count and
the turns that missed, with the customer's move and the agent's line. An expected red that stays green, or a green sim
that turned red, is reported as such.

## 3. Regressions

With the guard 5/5, run the strategy's regression list 5× on the workspace, the launch in `<references>/tooling.md`,
Simulation runs, into `<runs>/regressions.json`, and compare it with the baseline:
`python3 <scripts>/runset.py summary <runs>/regressions.json --vs <baseline>`. A regression is a simulation that passed
5/5 on the baseline and fails one or more runs now, with failing transcripts whose turn follows from the edit; one below
5/5 on the baseline is unstable, listed and not counted. Say each regression, one line: the simulation, the turn, what
the edit did to it. Fixing one is another edit, with the go: edit the block file, push it to `<workspace>` as
tooling.md, Studio content, says, and run nothing until the diff after the second pull is empty; then sections 2 and 3
again. Clean is
no regression left and the guard still 5/5.

## 4. Report

Write `<pages>/cards/<n>/resolve/report.md` and render it with `python3 <scripts>/card.py rs <agent> <n>`:

- the guard's count before and after the edit, with the run ids;
- the regression list's count on the baseline and after the edit, with the run ids, each regression with its cause and
  the unstable ones by name;
- what changed in the transcripts at the failure turn, the old line and the new line;
- the verdict: solved, needs another pass, or the strategy or the edit was wrong; one sentence why;
- what to try next when it is not solved.

Nothing else on the card. Anything you want the engineer to decide goes in the session, not in the report.

## 5. Ready to merge

When the guard is 5/5 and the regressions are clean, say the issue is ready to merge and list what goes: the simulation
and code files, and the Studio items the edit changed. Then, each with the engineer's go:

1. Commit the card's work in `<checkout>`, everything uncommitted there: one commit per concern (the simulations, the
   Studio edit, anything you changed since), with no attribution line.
2. Merge into the batch with one command: `python3 <scripts>/batchmerge.py <agent> <batch> <the issue's branch>`. It
   waits for any other merge into the batch, pulls `<batch-workspace>`, merges, pushes the merged Studio content back
   and checks it. Exit 0: merged and synced. Exit 2: the batch workspace holds Studio changes the batch branch never
   had. Exit 3: a merge conflict, aborted. Exit 4: the workspace does not hold the merge. On any exit but 0, report what
   it printed and stop. Run no pull, merge or push in `<batch-worktree>` yourself.

Push the branch nowhere.
