# Simulation gate

Two test layers exist. Plain unit tests (the repo's JS runner) cover deterministic logic. Simulations are Sierra end-to-end tests where an LLM customer converses with the LLM agent and an LLM judge evaluates the result. Neither layer establishes correctness outside its tested cases.

Load the technical detail for the operation at hand: [simulation CLI](simulation-cli.md) before running or parsing tests; [assertions](simulation-assertions.md) before writing an assertion; [result access](simulation-results.md) before fetching a transcript or a raw call; [networking](simulation-network.md) for a knowledge setup or egress failure.

## Coverage before the gate

The gate proves stability, not coverage. First map every scenario and path the change touches: each journey branch, tool success and failure mode, eligibility or auth outcome, conditional rule, and emitted tag. A simulation that reaches a path but asserts nothing about it does not cover it. Extend an existing simulation's assertions where it already drives a path. Write a new one where none reaches. Run the gate only after every affected path has a simulation asserting on it. Report the map and the covering simulation for each path.

## Pass bar

Every covering simulation passes five consecutive clean runs: `--num-runs 5 --pass-rate 100`. Simulations are stochastic, so one green run proves nothing. A 4-of-5 result, a lowered pass rate, zero matched tests, or a missing run is not a pass. Report the actual N-of-5. Only the user can waive the gate, explicitly and per change; record the waiver and its scope.

Do not run the whole suite for general confidence. Run the covering simulations, and a baseline comparison when a failure needs one.

## Execution

Before running, verify the org, agent, thread workspace, and data permissions. `pnpm sierra test` uploads the local working copy before it runs, so it exercises uncommitted edits. MCP `run_test` runs the saved workspace and misses them. Verify the artifact that actually executed.

Request `--json` and parse the verdict from the complete record. A matching `success` string alone is insufficient: check completion, the verdict, the selected test identities, and the run counts. Use a fresh output file or run identity so an earlier success cannot satisfy a later run. Bind the record to the code, no-code, configuration, and fixture versions it exercised.

Five runs across several simulations outlast a foreground command. Run the gate in the background with the JSON written to a file, and work on the correctness review while it runs. When the parallel work runs out, wait on the file with one bounded wait, not a polling loop, and end the turn if the run is still going. A background process does not survive a session refresh: state what remains and how to resume.

## Diagnosis

Investigate a failed run before retrying. Compare against the unchanged baseline when needed to separate a regression from an existing failure. A pre-existing flake still needs five clean runs or a waiver. When knowledge-dependent tests fail together, read [networking](simulation-network.md) before touching code.

Green assertions alone do not clear the gate. Read each run's transcript and assertion results end to end. A green run whose transcript shows wrong behavior is a failure: tighten the assertion to catch it, fix the behavior, and rerun. A red run over a correct transcript is a judge defect: establish it from the transcript before changing the outcome wording. Keep observed failures in the record instead of rerunning until green without explanation.

If the session cannot access the required results, hand off the named check per [handoff](../writing/handoff.md). Do not claim transcript verification from a judge summary.

After any later behavior-affecting edit, rerun the affected simulations. The final result must match the artifact being handed off or shipped. Read [correctness review](verification.md) for evidence freshness and the joint gate report.
