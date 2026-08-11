---
name: sierra
description: Critical guidance for Sierra agent development. Must always be loaded when working with Sierra agents.
---

# Sierra Agent Development Guidance

Sierra Agents are developed with a custom SDK based on React, with components rendering agent context instead of UI. The
final context is compiled from the combination of the following items and all of them must be tracked to avoid having
only partial understanding of agent context:

- Studio Journey definition: synced to `.composer/` by `pnpm sierra ghostwriter --sync`
- Studio Configuration
- Knowledge Base
- Codebase context. Changes require `pnpm sierra upload/watch` to take effect.

You will use these tools for development process. All must be available and accessible. If any of these are not fully
functional - stop immediately and inform the user:

- sierra mcp
- sierra cli

## Constraints

- **Sierra SDK is private.** You must ground your understanding with:
    - use `sierra` mcp tool: `ask_sierra_assistant`
    - sdk source files in `node_modules`

## Replays, conversations and traces

`pnpm sierra ghostwriter <workspace> --sync-conversations [--ids <id>,...]` and
`--sync-simulations --run-id <replaytestrunset-...>` download conversation and simulation
artifacts into `.composer/`. Neither flag appears in `--help`; both are documented in
`.composer/docs/agent-traces-reference.md`. Pass the workspace positionally or the command
prompts. Conversation ids need the `audit-` prefix.

Layout is identical for a conversation and a simulation result:

- `summary.json` / `result.json` — metadata
- `debug.log` — CSV event log (`seq,timestamp,event_type,message`); the reference doc lists which
  event types have a trace file
- `traces/<turn>.trace` — one file per turn that made an LLM call

Each `.trace` holds `llm_chat` (purpose, plus `raw_request` carrying model, temperature,
max_output_tokens, tools, reasoning effort), `llm_chat_response` (input/output tokens, cached,
retries, raw response) and `task` (task_id, input, output).

Read `summary.json`/`result.json` first, then `debug.log`, then only the traces for the rows that
matter. The `personalized_progress_indicator` call is not captured in these traces.

Running sims: `pnpm sierra test --names <name> --num-runs <n>` (server caps `--num-runs` at 5;
invoke twice for more) or the `run_test` MCP tool. `get_test_results` with `verbose:true` returns
trace spans, prompt contexts with full bodies, and the model, but carries no temperature or token
counts, and reaches only a test's latest result.

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
