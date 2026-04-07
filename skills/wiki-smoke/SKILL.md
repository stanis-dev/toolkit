---
name: wiki-smoke
description: >-
  Run the knowledge-wiki smoke battery through scenario worker subagents. Use for regression
  checks on `wiki-editorial`, its file effects, and startup-hook integration. Not for editing
  canonical pages or ad hoc linting.
---

# Wiki Smoke

Parent orchestration workflow for the `knowledge-wiki` smoke battery.

## Constraints

- Treat smoke runs as an operational gate for `wiki-editorial`, not as a generic test harness.
- Use one isolated temp workspace per scenario.
- Mutating scenarios must target temp wiki roots only, never `/Users/stan/code/toolkit/knowledge-wiki`.
- Run scenario commands with `TZ=UTC`.
- Keep worker scope narrow: one scenario per worker.
- Do not hand-wave warnings. A warning scenario passes only when the expected warning class appears and no errors appear.
- If a worker crashes or does not return strict JSON, mark the scenario `INCONCLUSIVE`.

## Workflow

### 1. Discover Scope

Run:

```bash
python3 <skill-dir>/scripts/wiki_smoke.py list --json
```

Choose:

- full battery
- one batch
- one scenario

Done when: the exact scenario ids are locked.

### 2. Prepare Scenario Workspaces

For each chosen scenario, create a dedicated temp workspace and materialize the scenario:

```bash
python3 <skill-dir>/scripts/wiki_smoke.py prepare \
  --scenario-id publish_new_page \
  --workspace-root /tmp/wiki-smoke/publish_new_page
```

This writes a run descriptor containing:

- `scenario_id`
- `wiki_root`
- `cli_path`
- `fixture_root`
- `setup_steps`
- `command`
- `expected_exit`
- `expected_stdout`
- `expected_stderr`
- `expected_files`
- `expected_warnings`
- `forbidden_paths`

Done when: every scenario has its own prepared workspace and run descriptor.

### 3. Dispatch Worker Subagents

Spawn `wiki-smoke-worker` once per scenario, passing the prepared descriptor fields. Group scenarios into these batches:

- CLI guardrails
- proposal scaffolding
- publish gating + happy path
- full lint + integration

Done when: every scenario returns a JSON verdict file.

### 4. Aggregate

Collect result files and aggregate:

```bash
python3 <skill-dir>/scripts/wiki_smoke.py aggregate \
  --result-file /tmp/wiki-smoke/*/artifacts/result.json
```

Done when: you have a final report with scenario counts, failures by category, artifact pointers, and `GREEN` / `YELLOW`
 / `RED` release status.

## GOOD / BAD

### GOOD

- Prepare one temp workspace per scenario.
- Run one worker per scenario.
- Aggregate all JSON result files into a release-gate report.

Reasoning: isolation keeps command/file-effect failures easy to localize.

### BAD

- Reuse one temp root across scenarios.
- Run mutating publish scenarios against the real toolkit wiki root.
- Accept warning scenarios without checking the exact warning class.

Reasoning: this hides regression sources and breaks the safety contract of the battery.

## Anti-Patterns

| Temptation | Reality |
| --- | --- |
| “This is a simple CLI, I’ll just run a couple commands manually.” | The smoke battery exists to make file effects and gating repeatable. Use the catalog and worker agent. |
| “One temp directory is enough for the whole run.” | Scenario leakage invalidates results. Use one workspace per scenario. |
| “A worker failure probably means the scenario failed.” | A worker crash is `INCONCLUSIVE` until the scenario itself is re-run cleanly. |
| “Warnings are non-blocking, so I won’t assert them.” | Warning scenarios are only useful if they prove the correct warning appears and no errors slip in. |

## Output

Parent final report should include:

- `total_scenarios`
- `pass`
- `fail`
- `inconclusive`
- `failures_by_category`
- `artifact_pointers`
- `release_gate`
