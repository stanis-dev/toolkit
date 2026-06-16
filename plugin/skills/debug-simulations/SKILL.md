---
name: debug-simulations
description:
    Guidance for analyzing downloaded simulation runs to debug a specific test result or compare
    multiple results from the same run. Invoke this skill when you need to inspect simulation agent
    traces, understand why a test passed or failed, or correlate a simulation result with its test
    definition.
---

# Analyzing Simulation Runs

Simulation run data is located in `.composer/simulations/`. Each downloaded run has its own
directory keyed by simulation run ID.

---

## Phase 1: Context assembly

Read `.composer/docs/agent-traces-reference.md` for the run/result files and shared `debug.log` and
`traces/` format.

If the user pasted an Agent Studio URL and you need to recover the internal run, test, or result ID,
also read `.composer/docs/url-reference.md` before guessing.

**Exit criteria:** You understand the simulation run data format.

---

## Phase 2: Identify the run and result

Find the simulation run and result you need to inspect.

- Use the known full `simulationRunId` from `run_test`, `get_test_run_summary`, or
  `get_test_results`
- If the user pasted an Agent Studio URL, extract the relevant clean IDs from the path or query
  string, then normalize them using `.composer/docs/url-reference.md` before searching local
  artifacts or syncing data.
- Search `result.json` files for failed statuses, tags, or expected outcomes
- Use `rg` across `debug.log` files for tool names, agent errors, or specific messages

**Exit criteria:** You have the simulation run ID and result ID(s) relevant to the investigation.

---

## Phase 3: Diagnose

Inspect files in this order:

1. `result.json` for status, tags, and assertions
2. `debug.log` for the chronological event flow
3. `traces/*.trace` only when a specific task needs deeper investigation

**Exit criteria:** You can explain why the result behaved the way it did based on the exported data.
