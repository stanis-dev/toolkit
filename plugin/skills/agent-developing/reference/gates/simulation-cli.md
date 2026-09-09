# Simulation commands and verdicts

Read before selecting simulations, running them, or parsing the CLI output. [Testing](testing.md) holds the coverage rule and the five-run gate; this page does not change them.

Run from `agents/{agent}` and pass the exact thread workspace as the positional. `pnpm sierra test` uploads the local working copy first, so it exercises uncommitted edits; MCP `run_test` runs the saved workspace instead. Confirm flags with `pnpm sierra test --help`. The ones below match SDK 0.20260813.

- `--names` takes space-separated names or IDs. A comma-joined list silently matches zero tests and exits green. Confirm the run report names every simulation you asked for.
- `--categories` selects by category, also space-separated. `--list` prints the locally registered tests without running them; UI-authored simulations do not appear in it.
- The gate settings are `--num-runs 5 --pass-rate 100`. The CLI caps `--num-runs` at 5. `--retries` is not the gate: a retried pass hides a flake.
- `--workspace-id` makes the workspace's Agent Studio content part of the run. Without it the server resolves the agent's main workspace.
- `--json` prints the verdict as JSON. Write it to a file and parse the whole record. The terminal prints it last, and truncation can drop a failure.
- Never pass `--simulate-speech` for a gate run. It turns a run into an hour-long one and the scores are not comparable.

The verdict is a JSON object containing `success`. Its presence alone is not sufficient: check completion, the value, the selected tests, and the run counts. Use a fresh output file per run so an earlier verdict cannot satisfy a later one. For an empty selection, check the names before debugging agent code.

Run a long gate in the background with its output redirected to a file, then wait on that file with one bounded wait. For transcripts or raw calls, read [result access](simulation-results.md).
