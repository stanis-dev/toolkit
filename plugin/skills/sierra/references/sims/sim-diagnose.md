# Guide for choosing the simulation that guards a problem

Runs as [tooling.md](../tooling.md), Simulation runs, says. When there is no workspace, nothing runs: say where a run
would have settled the point.

1. Guard: reuse a simulation that already reproduces the failure without guarding it, that can carry it as an
   intermediate path, or that judges the opposite behaviour; otherwise add one. Delete those that judged the bad
   behaviour good and the change leaves redundant. Design and review every simulation you change per
   [sim-design.md](sim-design.md) and [notes.md](notes.md).
2. Before choosing an existing candidate, run it 3× as it is: its conversations must reach the failure turn and its
   expectations must judge it. A failing simulation's replay already shows this.
3. Guard red: write the changes, uncommitted, and run the guard 5× into `<runs>/guard-red.json`. The transcripts must
   show it red for the analysis's reason; red for another reason, fix it and run it again.
4. Regressions: the simulations whose conversations pass through the analysis's items or its failure turn's point of
   the journey, and the guard's neighbours in its group. Run them 5× into `<runs>/regressions.json` with
   `--run-id-file <runs>/regressions.id`. On a rerun, «Before the fix · already recorded» stands: run only the
   simulations you add, into the file it names.
