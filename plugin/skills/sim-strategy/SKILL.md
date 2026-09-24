---
name: sim-strategy
description: >-
    Design the simulation that guards the behaviour an Issue Analysis asks for on a Sierra voice agent (cobranzas,
    openpay, hipotecarios): the guard reused, changed or new, with persona, expectations and tags, and what it displaces
    in the suite, returned as JSON; then write the guard and run it red. Use after issue-analysis and before any agent
    edit. Input, one line, agent and issue number, "cobranzas 321". Not for editing agent context.
metadata:
    model: gpt-5.6-terra
    reasoning-effort: high
---

You receive the analysis for an issue that was filed for Sierra agent. Your job is to evaluate the strategy for
simulation suite, then write the simulation changes and run the guard red.

Input: `<agent> <n>`, for example `cobranzas 321`. `cobranzas` is the repo's `agents/base`, `openpay` is
`agents/openpay`, `hipotecarios` is `agents/hipotecarios`. The agent's simulations are the `*.tests.ts` files under its
directory; `harness.ts` next to them holds the persona fixtures.

Everything you need is in the brief below this text. In it:

- The suite index gives id, name and categories only: read a simulation's persona, expectations and `assertions` in
  its file. `!tag` is a tag that must not appear; the `describe` a simulation sits in is its group.
- In a call, `tools[k]` is the k-th tool call of the next agent turn.
- In the card's history, open an event's files only when it bears on your task.

Read from disk the simulation files you need, `<agent-dir>/simulations/<file>`, and whatever else the run below
needs. Call no tool that reaches the tracker or Studio.

## Read

1. The analysis.
2. The linked call. Build the persona from it.
3. The suite. Read the file of the group the scenario belongs to, whole, before deciding; read neighbouring groups when
   the journey point is shared.
4. The tags the agent can emit. Never assert a tag that exists nowhere.

## Decide

You must decide whether to modify an existing simulation or create a new one to reproduce the failure.

Reuse a simulation if:

- an existing simulation already reproduces the failure, but doesn't guard it.
- an exisiting simulation that reproduces the scenario and failure case can be included as an intermediate path.
- an exisiting simulation/s evaluates the opposite behaviour and needs to be flipped.

If you identify a potentially reusable simulation, launch it once and read its transcripts to ensure that the
resulting conversation can indeed provide the situation you expect. See Run section.

If you identified a simualtion to modify, review it for bad practices and potential improvements towards best practices
and include those changes along with those addressing the issue failure.

Simulations should be deleted if:

- bad behaviour was being evaluated positively and the change does not need all of them flipped (e.g. change removes
  behaviour and a group of sims focused on it is now redundant)

Follow [sim-design.md](../sierra/references/sims/sim-design.md) and [notes.md](../sierra/references/sims/notes.md).

## Run

A candidate guard is run before it is chosen: one launch of three runs, on the simulation as it is. What settles the
point is the transcripts, not the pass count: the conversation must reach the failure turn's condition with the persona
as it is, and the expectations must judge that turn. Name the run in `guard.run`, its id and one sentence on the shape
the conversations took and what that settled.

[tooling.md](../sierra/references/tooling.md), Simulation runs, gives the launch, the wait and the readers; use
`--num-runs 3`. When the brief says the issue has no workspace, nothing can run: say in `guard.why` where a run would
have settled the point.

## Guard red

Write the changes `sims` describes, the guard and any other simulation you modify or delete, in the files and groups
you name, and change nothing else. Leave them uncommitted: they stay the card's work until merge. Run the guard 5×, the launch in
tooling.md, Simulation runs, with `--num-runs 5` into `<runs>/guard-red.json`. Read the transcripts, not the judge
alone: the guard is red for the reason the analysis names, the same customer move going unanswered the same way. Red
for another reason means the guard is wrong: fix it and run it again. Put the last run in `guard.red`. Green on the
tree as it is means the issue does not reproduce; red for another reason after a second try means the guard needs the
engineer: say which in `flags`.

## Regressions

List the simulations the change could break: those whose conversations pass through the items the analysis names, the
failure turn's wanted and won items, or through the failure turn's point of the journey, and the guard's neighbours in
its group. Leave the guard out; keep the list to 240. Run the list once, 5×, on the suite as it is, the launch in
tooling.md, Simulation runs, with `--num-runs 5` into `<runs>/regressions.json` and `--run-id-file <runs>/regressions.id`:
that run is the baseline the resolution compares against after the fix. Put the list in `regressions.sims`, each with
one sentence on how the change could reach it, and the run id in `regressions.run`.

When the brief has «Before the fix · already recorded», this is a rerun: the guard's red run and the regression runs
listed there stay the card's before counts. Run neither again; keep `guard.red` and `regressions.run` from them. Run
only the simulations you add to the list, once, 5×, into the file that section names: their counts are their
baseline.

## Output

Return only the JSON object that [schema.json](schema.json) describes, nothing before or after it. Persona text,
expectations and tags are written in full for a new simulation and as changes for a modified one. Leave pass counts
outside `guard.red` empty. `sims` holds only the simulations that change; a `modify`
with nothing in `changes`, `reworded`, `added` and `removed` is not a modification, leave it out. A flag is `null` when
it does not apply, otherwise one sentence with its proof.

When the run carries feedback on your previous answer, weigh it as [feedback.md](../sierra/references/feedback.md) says
and fill `feedback`.
