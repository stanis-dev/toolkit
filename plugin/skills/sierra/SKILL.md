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

## At the beginning of each session:

1. Check that `Sierra` MCP is available and functional, comprehend its tools. If unavailable, stop immediately and
   notify user.
1. Grab latest journey from `sierras journey ...`. Refresh if journey is edited

## Constraints

- **Sierra SDK is private.** You must ground your understanding with:
    - use `sierra` mcp tool: `ask_sierra_assistant`
    - sdk source files in `node_modules`

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

sierras knowledge search "query"                             # workspace-scoped
sierras knowledge search "query" --live                      # live published view
sierras knowledge search "query" --source <id>,<id>

```

## Simulations

Simulations evaluate a scenario based on expected/forbidden tags and judge LLM conditions.

Simulations must be evaluated:

- LLM user must play its role in a way that will allow the target scenario to happen.
- Declared conditions must be worded correctly. The wording is correct when Judge LLM comments reveal that it is
  evaluating what matters.
- Only then the pass or fail becomes relevant.

## Development Flow

### New Feature

1. Create a failing simulation for the feature first.

### Bug Fix

1. Check whether there's an existing simulation that covers the failing behaviour.
    - if exists: check sim quality
    - if not: create one

### Issue

1. Fetch the issues
1. Fetch the related conversation/s
1. Produce short report on the source of the problem
