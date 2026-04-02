---
name: Sierra Powertool
description: This skill must always be used when working on any sierra agent
---

# sierras CLI

CLI for Sierra journey visualization, simulation management, workspace management, and issues tracking.

## Global Flags

All commands accept these persistent flags:

- `--org <subdomain>` -- Sierra org subdomain (default: `pronet`). Controls which API domain and session file are used
  (e.g. `--org acme` uses `acme.sierra.ai` and `~/.sierra/acme.sierra.ai.session`).
- `--bot-id <id>` -- Bot ID. Required for non-pronet orgs (or set `SIERRAS_BOT_ID` env var).
- `--journey-id <id>` -- Journey ID. Auto-discovered from workspace if omitted (or set `SIERRAS_JOURNEY_ID`).
  Errors with a list of available journeys when the workspace has multiple.
- `--workspace-id <id>` -- Override workspace ID for this run.
- `--workspace-name <name>` -- Override workspace by name (resolved via API).

## Command Reference

### Journey Commands

```bash
sierras journey            # Print structured journey export (JSON) to stdout
```

**Behavior:**

- `sierras journey` outputs a schema-versioned JSON document (currently `journey-export.v1`).
- The export preserves block hierarchy, conditions, tags, tools, and list content with inline tool references.

### Issues Commands

```bash
sierras issues --print     # Print issues summary to stdout
```

### Docs Commands

```bash
sierras fetch-docs --url <json-url>  # Fetch docs JSON and cache as Markdown locally
```

**Behavior:**

- `sierras fetch-docs` requires `--url` pointing to the CloudFront JSON URL that contains all doc pages
  (a flat `map[string]string` where keys are doc paths and values are markdown content).
- Cache is namespaced by the global `--org` flag so multiple orgs can coexist under `.sierras/docs-cache/<org>/`.
- No authentication needed; the JSON is publicly accessible on CloudFront.
- Writes Markdown to `.sierras/docs-cache/<org>/`; delete that directory to reset the cache for that org.

### Conversation Commands

```bash
sierras conv list                                # List recent conversations (first 50)
sierras conv list --search <term>                # Filter conversations by search query
sierras conv list --limit <n>                    # Fetch up to N conversations (paginates automatically)
sierras conv list --tags <tag,...>               # Include only conversations with these tags (server-side)
sierras conv list --exclude-tags <tag,...>       # Exclude conversations with these tags (client-side)
sierras conv list --after <time>                 # Only conversations after this time
sierras conv list --before <time>               # Only conversations before this time
sierras conv list --json                         # Output raw list data as JSON
sierras conv show <id-or-url>                    # Show conversation transcript
sierras conv show <id-or-url> --verbose          # All task events grouped by conversation turn
sierras conv show <id-or-url> --trace <turn>     # Show all LLM API calls for a specific turn
sierras conv show <id-or-url> --json             # Output raw trace events as JSON
```

**`conv list` Behavior:**

- Lists recent conversations sorted by most recent. Default returns first page (50 results).
- Table columns: raw ID (26-char, usable with `conv show`), relative time, duration, device, message count, key tags.
- `--search` passes a search query to the API which searches conversation content.
- `--limit <n>` fetches up to N conversations, paginating automatically beyond the 50-per-page API limit (e.g.,
  `--limit 300` fetches 6 pages).
- `--tags` filters server-side to conversations containing these tags. Supports short forms: `debt-paid` ->
  `collections:outcomes:debt-paid`, `id:verified` -> `collections:identity-verification:verified`. Full-form tags
  (containing `:`) pass through as-is.
- `--exclude-tags` removes conversations matching these tags client-side (after fetch). Same short-form expansion as
  `--tags`. Combine with `--tags` for precise filtering (e.g., `--tags id:verified --exclude-tags debt-paid`).
- `--after` and `--before` filter by time (server-side). Accepts relative durations (`1h`, `2d`, `30m`, `1w`), dates
  (`2026-02-11`), datetimes (`2026-02-11T14:00`), or Unix epoch seconds. Combine both for a time window (e.g.,
  `--after 3d --before 1d`). Use `--after` alone for "since N ago".
- Tags show outcome/flow information: `debt-paid`, `transferred-to-agent`, `id:verified`, `payment-scheduled:in_3_days`,
  etc.
- Workflow: `conv list` -> copy an ID from the output -> `conv show <id>`.

**`conv show` Behavior:**

- Accepts a Sierra Studio URL (`https://pronet.sierra.ai/agents/.../sessions/{id}`), raw ID, or `audit-` prefixed ID.
- Default view extracts a chronological transcript from trace events: `[USER]`, `[AGENT]`, `[TOOL]`, `[FILLER]` entries.
- For voice conversations, shows raw transcription vs LLM-corrected text when they differ (with confidence score).
- PII is always redacted (bullet characters). `allowReredaction` is hardcoded to `false` with no override flag.
- `--json` outputs the full raw trace events array instead of the rendered transcript (takes precedence over `--trace`
  and `--verbose`).
- `--trace <turn>` shows all decision-relevant LLM API calls for the specified turn number:
  - Turn numbers derived from `conversationTurn` trace events sorted by `start_time`.
  - `goalsdk_respond`: full system prompt (all `# Heading` sections), complete conversation window, tool schemas, and
    LLM response (tool call or text).
  - `on_transcription`: raw transcription input, correction prompt, and corrected output (voice conversations).
  - `classify_observations`: numbered statement list and matched IDs.
  - `personalized_progress_indicator`: full prompt (system + user) and parsed JSON response.
  - `param_validation`: validation result.
  - Each section header shows model, temperature, and token counts.
  - All data shown in full, never truncated.
  - Error on invalid turn number with valid range shown. Greeting turns report no decision-relevant calls.
  - `--json` takes precedence over `--trace`; `--trace` takes precedence over `--verbose`.
- `--verbose` shows all task events grouped by conversation turn with turn headers including duration:
  - Turn boundaries derived from `conversationTurn` event time ranges (`start_time`/`end_time`).
  - Transcript events: `[USER]`, `[AGENT]`, `[TOOL]`, `[FILLER]` (same as default view).
  - Decision signals: `TAGS:` from `goalsdk_respond` taskTags (e.g., `~requires-tool-call`, `~default-model-gpt-4.1`).
  - Condition evaluations: `CONDITIONS:` from `classify_observations` (matched statements or `(none matched)`).
  - Parameter validation: `PARAM_VALIDATION: valid` or `PARAM_VALIDATION: invalid -- <reason>`.
  - Safety summaries: `SAFETY: <taskId> -- <summary>` for `detect_abuse`, `safety_monitor`, `safety_monitor_tee`,
    `deadlock_detector`, `classify_interruption`.
  - Voice-specific: `VOICE: <taskId> -- <summary>` for `numeric_extraction`, `voice_script_quality`.
  - Online evaluation tasks (`online-eval-*`, `monitors_classifier_*`) are omitted.
  - Unknown task types render as `UNKNOWN: <taskId> -- <output>`.

### Simulation Commands

```bash
sierras sim list [--tag <t>] [--category <c>] [--group <g>] # List sims with pass/fail status
sierras sim status                        # Suite summary (total, passed, failed, running, run counts)
sierras sim run <name> [--count <n>] [--async] [--timeout <duration>] # Run a simulation (waits by default)
sierras sim run-all [--count <n>] [--resume] [--tag <t>] [--category <c>] [--group <g>] # Run sims
sierras sim wait-all [--timeout 4h] [--poll-interval 30s] [--tag <t>] [--category <c>] [--group <g>] # Wait
sierras sim replay <name>                 # Show latest result in turn-grouped format
sierras sim replay <name> --id <id>       # Show specific result details
sierras sim replay <name> --list          # List all available replay results
sierras sim replay <name> --list --json   # List replay results as JSON (for programmatic polling)
sierras sim replay <name> --limit <n>     # Show details for n most recent results
sierras sim replay <name> --transcript    # Show conversation only (no metadata)
sierras sim replay <name> --verbose       # Show flat event timeline (previous format)
sierras sim replay <name> --trace <turn>  # Show all LLM API calls for a specific turn
sierras sim replay <name> --no-cache     # Force fresh API fetch (ignore local cache)
sierras sim replay-all [--concurrency 10] [--limit N] [--tag <t>] [--category <c>] [--group <g>] # Bulk export
sierras sim diff --left <ws> --right <ws> [--json] [--detailed] # Compare sim results between workspaces
```

**Behavior:**

- `sierras sim run` caches results locally after completion. `sierras sim replay` returns cached results instantly
  when available (zero API calls for the result fetch). `sim run --async` saves a pending trigger marker; the next
  `sim replay` resolves it by polling for completion, then caches the results. Use `--no-cache` to force a fresh fetch.
- `sierras sim run` blocks until completion and prints the replay output for the new run(s). On timeout, the error
  message includes a recovery hint (`sierras sim replay <name> --list`).
- `sierras sim run --async` returns immediately after sending a single batch API request (even with `--count N`); warning:
  sleep-based waiting is unreliable and should be used only when necessary.
- `sierras sim list`, `sim run-all`, `sim wait-all`, and `sim replay-all` accept `--tag`, `--category`, and `--group`
  flags for subset filtering. All three are substring matches (case-insensitive). `--tag` matches against
  `tagExpectations.present`, `--category` against category labels, `--group` against group description. Multiple
  filters AND together. Filter match counts are reported to stderr.
- `sierras sim run-all` continues on individual trigger failures and reports errors at the end. Progress is reported
  to stderr every 50 sims (including in JSON mode). The JSON output includes `errorCount`, `skipped`, and optional
  `errors` array. Use `--resume` to skip sims that already have results (for crash recovery after a partial `run-all`).
  Use `--tag`/`--category`/`--group` to run a subset.
- `sierras sim wait-all` polls `sim status` at the specified interval until matching sims reach a terminal state.
  Progress reported to stderr. Exits 0 on completion, 1 on timeout. Use after `run-all` to block until platform
  execution finishes. Without filters, waits for **all** sims. Use `--tag`/`--category`/`--group` to scope to the
  same subset you triggered with `run-all`.
- `sierras sim replay-all` fetches replay history for matching sims with configurable parallelism (default 10
  concurrent fetches). Outputs structured JSON to stdout with progress to stderr. Results are cached locally. Use
  `--limit N` to cap result sets per sim. Use `--tag`/`--category`/`--group` to export a subset.
- `sierras sim replay --list --json` outputs replay history sets as JSON for programmatic polling of run completion.
- `sierras sim diff` compares latest sim results between two workspaces by name or ID. Shows per-sim pass/fail
  deltas, left-only/right-only sims, and regression/improvement lists. Use `--detailed` to also fetch replay
  history and compute per-condition miss rate changes (much slower -- fetches all replay data for both workspaces).
  JSON output includes full comparison data for further analysis.
- `sierras sim status` shows total run counts across all sims when multiple runs exist (e.g., after `run-all --count 3`).
- The Sierra platform batches at most 1200 simulations per `run-all` request. Workspaces with more
  simulations (e.g. 1500+) require multiple batched runs to cover the full suite.
- All GraphQL API requests automatically retry on transient errors (HTTP 429, 5xx, DynamoDB throttling) with
  exponential backoff (up to 5 retries). Retry attempts are logged to stderr.
- `sierras sim replay` default output is turn-grouped: events organized by conversation turn with numbered dividers
  (`── Turn N ──`). Each turn shows [USER]/[AGENT] messages flush left and indented system data (TOOL, SUPERVISOR,
  CONDITIONS, TAG). Tool call sequences are merged into single `TOOL: Name(args) → result` lines. Supervisor
  instructions and condition changes are extracted from compactState. Noise tags (`~usage-*`, `^client-event:*`) are
  filtered; all other tags pass through.
- `sierras sim replay --verbose` restores the flat event timeline (LOG, MEMORY_UPDATE, TRACE markers, all tags).
- `sierras sim replay --trace <turn>` shows all decision-relevant LLM API calls for the specified turn number:
  - `goalsdk_respond`: full system prompt (all `# Heading` sections), complete conversation window with SDK-injected
    messages annotated (`[SDK-injected]` on `call_SYN*` prefixed IDs), tool schemas (name + parameters + description),
    and LLM response (tool call or text).
  - `classify_observations`: numbered statement list and matched IDs.
  - `personalized_progress_indicator`: full prompt (system + user) and parsed JSON response with reasoning chain.
  - `param_validation`: validation result (invalidParams, reason).
  - Each section header shows model, temperature, and token counts.
  - All data shown in full, never truncated.
  - Cannot be combined with `--verbose`, `--transcript`, or `--list`.
  - Error on invalid turn number with valid range shown.

### Simulation CRUD

```bash
# Create (requires: --name, --group, --message, --outcome)
sierras sim create --name "My sim" --group "Debt" \
  --message "User instruction" --outcome "Expected behavior" \
  [--category cat] [--tag tag] [--device VOICE_WEB] \
  [--critical] [--config '<json>']

# Update (finds by name)
sierras sim update "My sim" --name "Renamed" --outcome "Existing outcome" --outcome "New outcome"

# Delete
sierras sim delete "My sim"
sierras sim delete --id replaytestmeta-...
```

**Behavior:**

- `sierras sim update` does not round-trip initialMemory secrets from the API; provide secrets explicitly via inline
  `--config` JSON when updating them.
- Warning: `sierras sim update --outcome` replaces the entire expected-outcomes list. To add a new outcome without
  losing existing ones, pass every outcome you want to keep in the same command.

### Workspace Commands

```bash
sierras workspace list                      # List workspaces for configured bot
sierras workspace create --name <name> --project-dir <path>      # Create workspace (uses configured bot)
sierras workspace delete <workspaceId> --project-dir <path>      # Delete workspace (--force to skip confirmation)
```

**Behavior:**

- All workspace operations are scoped to the configured bot (AI Assistant English)
- Default workspace comes from `internal/sierra/config.go`; override per command with `--workspace-id <workspaceId>` or
  `--workspace-name <name>`.
- `create` requires `--project-dir` and adds a `.targets/<name>` file under that directory so `sierra watch` detects it
- `delete` requires `--project-dir` and removes the corresponding `.targets/<name>` file under that directory
- Pass the Sierra agent project root as `--project-dir` to keep `.targets/` in the expected location
- `--project-dir` for this project must point to `~/code/pronet/agents/base`

**Workspace Discipline:**

- Strong recommendation: do all work in a feature workspace (avoid the default workspace) and always specify the exact
  workspace for any command where it applies (prefer `--workspace-id` or `--workspace-name`).
- Mutating simulation commands require an explicit workspace selection; the CLI errors without it.

### Diff Command

```bash
sierras diff --left <workspace-name> [--baseline <snapshot>]
```

**Behavior:**

- `--left` is required
- `--baseline` defaults to the latest main-workspace snapshot
- `--baseline` accepts a snapshot number (e.g., `89` or `#89`), snapshot name, or workspace version ID
- Output is a unified diff with Journey, Tools, and Simulations sections

**Safety Rules:**

- Cannot delete workspace named "default"
- Cannot modify workspaces not owned by configured user

## Decision Guide

| Task                         | Command                                                              |
| ---------------------------- | -------------------------------------------------------------------- |
| Print journey export         | `sierras journey`                                                    |
| Print issues summary         | `sierras issues --print`                                             |
| Browse recent conversations  | `sierras conv list`                                                  |
| Search conversations         | `sierras conv list --search "term"`                                  |
| View conversation            | `sierras conv show <id-or-url>`                                      |
| Debug conversation events    | `sierras conv show <id-or-url> --verbose`                            |
| Drill into conversation turn | `sierras conv show <id-or-url> --trace <turn>`                       |
| Raw conversation traces      | `sierras conv show <id-or-url> --json`                               |
| Check simulation health      | `sierras sim status`                                                 |
| Debug failing simulation     | `sierras sim replay <name>` (see Debugging Simulation Replays below) |
| Drill into a specific turn   | `sierras sim replay <name> --trace <turn>`                           |
| View replay history          | `sierras sim replay <name> --list`                                   |
| Compare recent runs          | `sierras sim replay <name> --limit 3`                                |
| Extract conversation only    | `sierras sim replay <name> --transcript`                             |
| Run and get replay output    | `sierras sim run <name>`                                             |
| Run all simulations          | `sierras sim run-all`                                                |
| Run a subset of sims         | `sierras sim run-all --tag triage` or `--category "Debt"` or `--group "Payment"` |
| Wait for all runs            | `sierras sim wait-all`                                               |
| Wait for a subset            | `sierras sim wait-all --tag triage`                                  |
| Bulk export all replays      | `sierras sim replay-all`                                             |
| Export subset replays        | `sierras sim replay-all --tag triage`                                |
| Compare two workspaces       | `sierras sim diff --left ws-a --right ws-b`                          |
| Fetch docs from JSON URL     | `sierras fetch-docs --url <json-url>`                                |
| List workspaces              | `sierras workspace list`                                             |
| Create dev workspace         | `sierras workspace create --name "dev"`                              |
| Diff workspace vs baseline   | `sierras diff --left "dev" --baseline 89`                            |

## Debugging Simulation Replays

### Replay Output Format

The default `sierras sim replay` output groups events by conversation turn. Each line type has a specific meaning:

- `[USER]` / `[AGENT]` -- actual spoken messages in the conversation. These are the only lines the customer hears.
- `TOOL: Name(args) → result` -- SDK-executed tool call. The LLM requested this tool; the SDK ran it server-side and
  returned the result. `[forced]` means the SDK injected the call without the LLM choosing it.
- `SUPERVISOR:` -- instruction from the journey's decision engine to the LLM, injected into the conversation history as
  a tool result. The LLM sees it as a regular tool response and follows it. This is the primary signal for "what the
  journey wanted the agent to do."
- `CONDITIONS:` -- journey condition evaluation results. A separate LLM call evaluates condition statements against the
  conversation. Only shown on turns where conditions changed. Condition matches trigger new system prompt sections and
  tool availability.
- `TAG:` -- decision-relevant platform signals. Key patterns: `~task-tag:~requires-tool-call` / `~requires-no-tool-call`
  (agent's tool decision), `~goal:param-validation:valid` (tool parameters validated), `transfer` (escalation
  triggered), `collections:*` (domain flow signals).
- `FILLER[tool-wait]:` -- progress indicator message generated by a separate LLM call while a tool was executing. Has
  its own prompt and reasoning chain. Not a "real" agent response.
- `── Turn N ──` -- turn boundary. Turn numbers are stable references for drill-down commands.

### Agent Architecture

Non-obvious facts essential for correct interpretation of replay output:

- The LLM is pure text-in/text-out. It never executes tools, makes API calls, or runs code. It only outputs "call this
  tool with these args" or text responses.
- The SDK orchestrates everything: executes tools, injects supervisor instructions, evaluates conditions, assembles the
  system prompt.
- Each agent turn with a tool call involves 2 LLM calls: (1) LLM decides to call a tool, (2) after the SDK executes the
  tool and injects a supervisor instruction, the LLM generates the text response.
- The system prompt is computed from platform base sections plus journey-injected sections. Journey conditions can add
  new sections as the conversation progresses (e.g., "Debt Collection Process Guidelines" appears after identity
  verification). The final computed system prompt sent to the LLM is available via `--trace <turn>` and is often the
  most direct way to understand what the LLM was told -- checking the system prompt first can narrow down whether the
  issue is in the journey configuration or in the LLM's interpretation of it.
- `RequestSupervisorInstruction` is the journey's decision engine. After each tool call, it evaluates the result against
  the current journey state and produces an instruction telling the LLM what to do next (e.g., "Identity verified.
  Inform the customer of their balance. Card is expired -- offer to register a new card."). The LLM follows this
  instruction when generating its response. If the agent says something wrong, the supervisor instruction is the first
  place to look.
- Progress indicators (`FILLER[tool-wait]`) run as parallel LLM calls with their own system prompt, higher temperature
  (0.8 vs 0.0 for the main response), and structured JSON output requiring explicit reasoning about what to say.
- The journey is selected on the first turn based on routing conditions (e.g., "customer query about debt" + "attempting
  payment"). Once matched, the journey routing condition group is resolved and removed from the evaluation list. The
  remaining conditions in the same evaluation (guardrails like frustration, escalation keywords, off-topic) continue
  evaluating every turn with the shrinking list. Journey-internal conditions (e.g., identity verified, card expired) are
  evaluated separately by the SDK based on tool results and state -- these show up as CONDITIONS and can have TAGs
  configured to be applied on condition match, which will then show in changes in the replay output.

### Debugging Workflows

| Symptom                                  | Look at                                                                               | What to check                                                                                                                                                             |
| ---------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent says something wrong               | SUPERVISOR line for that turn, `--trace <turn>` for system prompt                     | Did the journey give the right instruction? Is the relevant policy in the system prompt?                                                                                  |
| Agent doesn't use expected tool          | TAG `~task-tag:~requires-no-tool-call`, `--trace <turn>` for available tools          | The LLM decided no tool was needed. Check if the tool was in the tools list and if the supervisor instruction mentioned it.                                               |
| Agent uses wrong tool or wrong args      | TOOL line + TAG `~goal:param-validation:valid`, `--trace <turn>` for param_validation | Check if param_validation flagged issues. Use `--trace` to see full tool schemas available.                                                                               |
| Agent loops or repeats                   | Multiple turns with same SUPERVISOR                                                   | Journey logic is giving the same instruction repeatedly.                                                                                                                  |
| Transfer doesn't happen                  | TAG `transfer` absent, CONDITIONS                                                     | Check if the escalation condition matched.                                                                                                                                |
| Agent gives info it shouldn't have       | SUPERVISOR line                                                                       | The supervisor instruction may have leaked data the agent shouldn't relay.                                                                                                |
| Filler message wrong phrasing            | FILLER[tool-wait] text, `--trace <turn>` for full prompt and reasoning                | The progress indicator has its own prompt and structured reasoning. Use `--trace` to see why it generated that message.                                                   |
| Condition should have matched but didn't | CONDITIONS on each turn, `--trace <turn>` for classify_observations                   | The condition evaluation LLM call may have missed it. Use `--trace` to see the full statement list and matched IDs. Check the condition statement wording in the journey. |

## Inline Config for Complex Simulations

Use `--config` with inline JSON for nested fields (no file path support):

```bash
sierras sim create --name "My sim" --group "Debt" \
  --message "User instruction" --outcome "Expected behavior" \
  --config '{
    "initialMemory": {
      "variables": [{ "name": "VAR", "value": "foo" }],
      "secrets": [{ "name": "SECRET", "value": "bar" }]
    },
    "mockToolData": [
      {
        "toolID": "journeytool-123",
        "isToolBlock": false,
        "pairs": [{ "inputJSON": "{}", "outputJSON": "{}" }]
      }
    ],
    "conversationInfo": { "locale": "en-US" },
    "simulationOptions": { "temperature": 0.2 }
  }'
```
