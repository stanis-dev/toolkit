---
name: Sierra Powertool
description: This skill must always be used when working on any sierra agent
---

# sierras CLI

CLI for Sierra journey visualization, simulation management, workspace management, and
issues tracking. All examples below assume `--bot <name>` is passed (see Scope).

## Scope

All commands require `--bot <name>` to identify the agent (e.g., `--bot triage`, `--bot base`).
Use `--target <name>` to select a non-default workspace (e.g., `--target baseline-pre-dedup`).
Default target is `default`.

**JSON envelope:** All `--json` output is wrapped in `{"workspace":"...","command":"...","data":...,"next":[...]}`.
Parse the `data` field for the command-specific payload.

## Sim Evaluation Workflow

### Running an evaluation

```bash
sierras sim bench start --bot triage --group triage --count 5
```

Triggers all matching sims, polls for completion, collects results into the database, and
prints a summary. Runs until all sims complete. Background it to do other work while it runs.

Flags: `--group` or `--category` (select which sims to run), `--count` (runs per sim, default 3).

The command prints the bench run ID on the first line. All query commands use this ID.

### Analyzing results

After the bench completes, use the run ID from the output:

| You want to... | Command |
|---|---|
| See overall pass rate | `sim bench query <id>` |
| Find broken sims | `sim bench query <id> --failed` |
| Find unreliable sims | `sim bench query <id> --flaky` |
| Drill into a specific sim | `sim bench query <id> --sim "Name"` |
| Get JSON for processing | `sim bench query <id> --failed --json` |
| List all bench runs | `sim bench list` |

### Recovery (if session interrupted)

If the bench command is interrupted (session death, Ctrl+C), partial results are saved.

```bash
sierras sim bench list --bot triage                    # Find the interrupted run
sierras sim bench collect <run-id> --bot triage        # Collect whatever completed
sierras sim bench query <run-id> --failed              # Inspect collected results
```

`status` and `collect` are recovery tools for interrupted runs.

### Guardrails

- Code uploads via `sierra watch` change the workspace version. `sim bench` handles this
  automatically -- results from the trigger-time version are still collected. If `sim list`
  shows a status reset after an upload, the results are still there; use `sim bench collect`.
- The platform limits 1200 concurrent runs. `sim bench` chunks automatically.
- If this tool hits a limitation for your workflow, stop and tell the user. Suggest a
  specific tool or skill improvement. If the workflow seems to need a custom script, the
  tool likely has a gap worth reporting.

---

## Command Reference

### Simulation Commands

```bash
sierras sim list [--group <g>] [--category <c>]             # List sims with pass/fail status
sierras sim status                                           # Suite summary (pass/fail/running counts)
sierras sim run <name> [--count <n>] [--timeout <duration>]  # Run a single sim (blocks until done)
sierras sim replay <name>                                    # Latest result in turn-grouped format
sierras sim replay <name> --id <id>                          # Specific result by ID
sierras sim replay <name> --list                             # List all available results
sierras sim replay <name> --transcript                       # Conversation only (no metadata)
sierras sim replay <name> --verbose                          # Flat event timeline
sierras sim replay <name> --trace <turn>                     # All LLM API calls for a turn
sierras sim diff --left <ws> --right <ws> [--detailed]       # Compare results between workspaces
```

```bash
sierras sim bench start --group <g> --count <n>              # Bench evaluation (see workflow above)
sierras sim bench query <run-id> [--failed] [--flaky]        # Query bench results
sierras sim bench list                                       # List all bench runs
sierras sim bench status <run-id>                            # Check progress of running bench
sierras sim bench collect <run-id>                           # Collect results for interrupted bench
```

**Behavior:**

- `sim run` blocks until completion and prints the replay. For bulk evaluation, use `sim bench start`.
- `sim list` and `sim status` accept `--group` and `--category` for subset filtering
  (case-insensitive substring match).
- `sim diff` compares latest sim results between two workspaces by name or ID. `--detailed`
  fetches replay history for per-condition miss rate changes (slower).
- `sim replay` default output is turn-grouped. See Debugging Simulation Replays below.
- `sim replay --trace <turn>` shows all decision-relevant LLM API calls for a turn.
- All API requests automatically retry on transient errors (up to 5 retries with backoff).

### Simulation CRUD

```bash
sierras sim create --name "My sim" --group "Group" \
  --message "User instruction" --outcome "Expected behavior" \
  [--category cat] [--tag tag] [--device VOICE_WEB] \
  [--critical] [--config '<json>']

sierras sim update "My sim" --outcome "Existing" --outcome "New"

sierras sim delete "My sim"
sierras sim delete --id replaytestmeta-...
```

- `sim update --outcome` replaces the entire expected-outcomes list. Pass every outcome to keep.
- `--config` accepts inline JSON for `initialMemory`, `mockToolData`, `conversationInfo`,
  `simulationOptions`. Example:

```bash
--config '{
  "initialMemory": {
    "variables": [{ "name": "VAR", "value": "foo" }],
    "secrets": [{ "name": "SECRET", "value": "bar" }]
  },
  "mockToolData": [{
    "toolID": "journeytool-123",
    "isToolBlock": false,
    "pairs": [{ "inputJSON": "{}", "outputJSON": "{}" }]
  }],
  "conversationInfo": { "locale": "en-US" },
  "simulationOptions": { "temperature": 0.2 }
}'
```

### Conversation Commands

```bash
sierras conv list                                # List recent conversations (first 50)
sierras conv list --search <term>                # Search conversation content
sierras conv list --limit <n>                    # Fetch up to N conversations (auto-paginates)
sierras conv list --tags <tag,...>               # Filter by tags (full tag strings, server-side)
sierras conv list --exclude-tags <tag,...>       # Exclude by tags (client-side)
sierras conv list --after <time>                 # After this time (1h, 2d, 2026-02-11, epoch)
sierras conv list --before <time>               # Before this time
sierras conv show <id-or-url>                    # Show conversation transcript
sierras conv show <id-or-url> --verbose          # All task events grouped by turn
sierras conv show <id-or-url> --trace <turn>     # All LLM API calls for a specific turn
sierras conv show <id-or-url> --json             # Raw trace events as JSON
```

**conv list behavior:**

- Lists conversations sorted by most recent. `--limit` paginates automatically.
- `--tags` requires full tag strings (e.g., `collections:outcomes:debt-paid`).
- `--after` / `--before` accept relative durations (`1h`, `2d`, `1w`), dates, datetimes, or epoch.
- Workflow: `conv list` -> copy ID -> `conv show <id>`.

**conv show behavior:**

- Accepts a Sierra Studio URL, raw ID, or `audit-` prefixed ID.
- Default view: chronological transcript with `[USER]`, `[AGENT]`, `[TOOL]`, `[FILLER]` markers.
- PII is always redacted.
- `--trace <turn>` shows full system prompt, conversation window, tool schemas, LLM response,
  condition evaluations, and progress indicator reasoning for the specified turn.
- `--verbose` shows all task events grouped by turn: transcript, tags, conditions, param validation,
  safety summaries.

### Journey, Issues, Docs

```bash
sierras journey                          # Structured journey export (JSON)
sierras issues [--json]                  # Issues summary
sierras fetch-docs --url <json-url>      # Fetch and cache Sierra docs as Markdown
```

### Workspace Commands

```bash
sierras workspace list                                        # List workspaces
sierras workspace create --name <name> --project-dir <path>   # Create workspace
sierras workspace delete <workspaceId> --project-dir <path>   # Delete workspace
```

- `--project-dir` must point to the agent's folder (containing `package.json`).

### Diff Command

```bash
sierras diff --left <workspace-name> [--baseline <snapshot>]
```

Compares a workspace's journey/tools/sims configuration against a baseline snapshot.
`--baseline` accepts a snapshot number, name, or workspace version ID. Defaults to latest.

Note: this compares *configuration*. To compare sim *results* between workspaces, use
`sierras sim diff --left <ws> --right <ws>`.

---

## Error Recovery

When a command fails, the error includes a recovery command.

| Error Code | Meaning | Recovery |
|---|---|---|
| `not_found` | Resource missing | Follow recovery command (often `sim list` or `workspace list`) |
| `validation_failed` | Invalid input or flags | Fix input per error message |
| `permission_denied` | Auth failure | `sierra login` |
| `timeout` | Operation exceeded limit | Retry with higher `--timeout` |
| `rate_limited` | API throttling | Wait and retry |
| `internal_error` | API error | Retry |

---

## Debugging Simulation Replays

### Replay Output Format

The default `sierras sim replay` output groups events by conversation turn:

- `[USER]` / `[AGENT]` -- spoken messages. The only lines the customer hears.
- `TOOL: Name(args) -> result` -- SDK-executed tool call. `[forced]` = SDK-injected.
- `SUPERVISOR:` -- journey instruction to the LLM. Primary signal for what the journey wanted.
- `CONDITIONS:` -- condition evaluation results. Shown when conditions change.
- `TAG:` -- platform signals. Key patterns: `~requires-tool-call`, `~requires-no-tool-call`,
  `~goal:param-validation:valid`, `transfer`, `collections:*`.
- `FILLER[tool-wait]:` -- progress indicator from a separate LLM call. Has its own prompt.
- `-- Turn N --` -- turn boundary. Use turn numbers with `--trace <turn>`.

### Agent Architecture

- The LLM is text-in/text-out. It outputs tool call requests or text responses. The SDK
  executes tools, injects supervisor instructions, evaluates conditions, assembles the prompt.
- Each tool-call turn involves 2 LLM calls: (1) decide to call tool, (2) generate response
  after SDK executes the tool and injects a supervisor instruction.
- The system prompt is computed from platform sections + journey-injected sections. Conditions
  can add sections as the conversation progresses. Use `--trace <turn>` to see the full prompt.
- `RequestSupervisorInstruction` is the journey's decision engine. If the agent says something
  wrong, the supervisor instruction is the first place to look.

### Debugging Workflows

| Symptom | Look at | What to check |
|---|---|---|
| Agent says something wrong | SUPERVISOR line, `--trace <turn>` | Journey instruction correct? Relevant policy in system prompt? |
| Agent doesn't use expected tool | TAG `~requires-no-tool-call`, `--trace <turn>` | Tool in the tools list? Supervisor instruction mention it? |
| Agent uses wrong tool/args | TOOL line, `--trace <turn>` for param_validation | param_validation flagged issues? |
| Agent loops or repeats | Multiple turns with same SUPERVISOR | Journey giving same instruction repeatedly |
| Transfer doesn't happen | TAG `transfer` absent, CONDITIONS | Escalation condition matched? |
| Filler message wrong phrasing | FILLER text, `--trace <turn>` | Check progress indicator prompt and reasoning |
| Condition should match but didn't | CONDITIONS, `--trace <turn>` for classify_observations | Statement wording in journey correct? |
