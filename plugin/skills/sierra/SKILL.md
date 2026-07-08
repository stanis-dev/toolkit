---
name: sierra
description: Critical guidance for Sierra agent development. Must always be loaded when working with Sierra agents.
---

# Sierra Agent Development Guidance

Sierra Agents are developed with a custom SDK based on React, with components rendering agent context instead of UI. The
final context is compiled from the combination of the following items and all of them must be tracked to avoid having
only partial understanding of agent context:

- Studio Journey definition: `sierras journey ...`
- Studio Configuration
- Knowledge Base
- Codebase context. Changes require `pnpm sierra upload/watch` to take effect.

You will use these tools for development process. All must be available and accessible. If any of these are not fully
functional - stop immediately and inform the user:

- sierra mcp
- sierra cli
- sierras cli powertool

## Constraints

- **Sierra SDK is private.** You must ground your understanding with:
    - use `sierra` mcp tool: `ask_sierra_assistant`
    - sdk source files in `node_modules`

## Sierras CLI (Powertool) `sierras ...`

All commands require --target <path> pointing at a .targets file, e.g. --target agents/<bot>/.targets/default. The
file is the sole source of org, workspace, and bot scope. The old scope flags (--org, --bot, --bot-id,
--workspace-id, --workspace-name) no longer exist and fail as unknown flags. Missing --target fails with a typed
validation_failed error plus a recovery command. Exception: sim resume/results/history and sim cancel <run-id> work
without --target — scope is restored from the run record; passing a mismatching --target with a run-id errors.

`--json` wrapper `{"workspace":"...","command":"...","data":...,"next":[...]}`: `data` field contains the payload.

There is ONE command for running sims: `sierras sim run`. It always blocks until completion and reports (there is
no fire-and-forget mode; background the process if you need to keep working). Every invocation is recorded with a
run ID (`run-...`) for later inspection. The old commands sim run-all, sim wait-all, sim bench *, sim cancel-all,
and sim run --async were removed and fail with a pointer to the replacement.

```bash
sierras --target agents/<bot>/.targets/default sim list [--group <g>] [--category <c>] [--rg <pat>] # List sims with pass/fail status (scope flag shown once; every non-run-id command needs it)

sierras sim status                                           # Suite summary (pass/fail/running counts)

sierras sim run <name>                                       # Run one sim (exact name, else regex), waits, renders full replay
sierras sim run [--group <g>] [--category <c>] [--rg <pat>]  # Run a filtered set; no filters = every sim in the workspace
sierras sim run --count <n>                                  # n runs per sim (default 1); use 3+ for flake detection
sierras sim run ... --peek                                   # Preview matched sims without running
sierras sim resume <run-id>                                  # Re-attach to an interrupted run (Ctrl+C, cap handback)
sierras sim results [run-id] [--failed] [--flaky] [--sim <n>] [--collect]  # Results/progress; no run-id = most recent run
sierras sim history [--status <s>]                           # List recorded runs, newest first
sierras sim cancel <run-id>                                  # Cancel that run's queued/running sims
sierras sim cancel --all                                     # Cancel ALL running sims in workspace (needs --target)

sierras sim replay <name>                                    # Latest result in turn-grouped format
sierras sim replay <name> --id <id>                          # Specific result by ID
sierras sim replay <name> --list                             # List all available results
sierras sim replay <name> --transcript                       # Conversation only (no metadata)
sierras sim replay <name> --verbose                          # Flat event timeline
sierras sim replay <name> --trace <turn>                     # All LLM API calls for a turn

sierras sim search <term> [--rg <pat>] [--cross-workspace]   # Search replay content by substring

sierras sim diff --left <ws> --right <ws> [--detailed]       # Compare results between workspaces
```

## Simulations

Simulations evaluate a scenario based on expected/forbidden tags and judge LLM conditions.

Simulations must be evaluated:

- LLM user must play its role in a way that will allow the target scenario to happen.
- Declared conditions must be worded correctly. The wording is correct when Judge LLM comments reveal that it is
  evaluating what matters.
- Only then the pass or fail becomes relevant.

## Synthesis Rewrites (voice)

Regex substitutions applied to agent text just before TTS. **Audio-only**: transcripts, chat, sims, and
issue snippets all keep the original text. Right tool when text is correct but spoken wrong
(pronunciation); wrong tool when the text itself is the defect (use prompt guidance / KB fix instead).

- **Pacing**: spaced capitals (`D E`) make TTS insert long pauses between letters; dash-joined letters
  (`D-E`) give a shorter but still audible separation — use dashes for spelling at natural cadence
  (e.g. German domain endings: `.de` → ` Punkt D-E`).
- **String patterns match literal substrings** (grounded via `ask_sierra_assistant`, 2026-06): no regex
  interpretation, and case-sensitive — so regex syntax inside a string (`"\\b\\d{4}\\b"`) is a silently
  dead rule, and case variants need either explicit pairs (`www.` / `WWW.`) or a RegExp.
- **RegExp patterns are fully supported**: flags honored end-to-end, applied in-memory before TTS (no
  JSON serialization boundary). Use `/\.de/gi` style — the `g` flag matters, a non-global regex replaces
  only the first occurrence.
- **Replacements are passed verbatim** to the TTS engine — no normalization, and SSML is effectively
  unsupported on OpenAI tts-1, so encode pronunciation in plain text. Start the replacement with a
  leading space when the pattern can directly follow a word (`".de"` → `" Punkt D-E"`).
- **Verify by ear in Studio**: Preview chat in voice mode renders TTS with in-progress synthesis rules —
  no publish or phone call needed. TTS pronunciation can drift across provider updates; test empirically.
- Punctuation pause/pronunciation reference (pause ladder, spoken-vs-silent, stability per element):
  see `references/tts-punctuation.md`.
- Rules apply **in array order** — specific patterns must precede generic ones they overlap with.

## Useful diagnostic steps

1. Explore the conversation and find the earliest deviation from spec. Don't just evaluate agent's responses, but also
   tags for internal flow and tool/api responses, calls and their data.
1. Create a simulation with the sole goal of forcing agent into the same situation and observe replay.

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
