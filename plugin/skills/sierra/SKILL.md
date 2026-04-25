---
name: sierra
description: Guidance for Sierra agent development
---

# Sierra Agent Development Guidance

Sierra Agents are developed with a custom SDK based on React, with components rendering agent context instead of UI.

User will interact most frequently with:

- Studio Journey definition
- Studio Configuration
- Knowledge Base
- Simulations
- Codebase context - interacts with Studio. Changes require `pnpm sierra upload/watch` to take effect.

At the beginning of each session check that `Sierra` MCP is available and functional, comprehend its tools. If
unavailable, stop immediately and notify user.

## Constraints

- **Sierra SDK is private.** You must ground your understanding with:
    - use `sierra` mcp tool: `ask_sierra_assistant`
    - sdk source files in `node_modules`

## Sierra SDK

## Sierras CLI (Powertool) `sierras ...`

All commands require --bot <name> to identify the agent (e.g., `--bot triage/base`). Use --target <name> to select a
workspace, e.g. --target default/baseline-pre-dedup. `--json` wrapper
`{"workspace":"...","command":"...","data":...,"next":[...]}`: `data` field contains the payload.

```bash
sierras sim list [--group <g>] [--category <c>] [--rg <pat>] # List sims with pass/fail status

sierras sim status                                           # Suite summary (pass/fail/running counts)

sierras sim run <name> [--count <n>] [--timeout <duration>]  # Run a single sim (blocks until done)

sierras sim replay <name>                                    # Latest result in turn-grouped format
sierras sim replay <name> --id <id>                          # Specific result by ID
sierras sim replay <name> --list                             # List all available results
sierras sim replay <name> --transcript                       # Conversation only (no metadata)
sierras sim replay <name> --verbose                          # Flat event timeline
sierras sim replay <name> --trace <turn>                     # All LLM API calls for a turn

sierras sim search <term> [--rg <pat>] [--cross-workspace]   # Search replay content by substring

sierras sim diff --left <ws> --right <ws> [--detailed]       # Compare results between workspaces

sierras sim cancel-all                                       # Cancel ALL running sims in workspace (clean slate)

sierras sim bench start --rg <pat> --count <n> [--peek]      # Bench evaluation with regex sim filter
sierras sim bench start --group <g> --count <n>              # Bench evaluation by group
sierras sim bench start --rg <pat> --count <n> --peek        # Preview matched sims without running
sierras sim bench cancel <run-id>                            # Cancel all running/pending sims in a bench run
sierras sim bench query <run-id> [--failed] [--flaky]        # Query bench results
sierras sim bench list                                       # List all bench runs
sierras sim bench status <run-id>                            # Check progress of running bench
sierras sim bench collect <run-id>                           # Collect results for interrupted bench
```

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

## Simulations

Simulations evaluate a scenario based on expected/forbidden tags and judge LLM conditions.

## Development Flow

### In all cases

- Always keep Studio context synced.

### New Feature

1. Create a failing simulation for the feature first.

### Bug Fix

1. Check whether there's an existing simulation that covers the failing behaviour.
    - if exists: check sim quality
    - if not: create one
