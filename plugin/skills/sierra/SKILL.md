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

## My preferences

- Refer to Studio block by their display name and type to help me follow.

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

## Agent Design Principles

- Agent must have a clear and centralised definition of what its register must be. 
  - Smell: separate items instructing agent how to say the content.
- Negative instructions are usually bad smell. Can be caused by conflicting instructions, over/under-specification.
- Agent works with turns as its scope. Instruction must be clear about any turn-specific logic.
- (GPT5.4 specific) - model is known to be very aggressive calling tools. Two mechanisms help remediate it 
  - place tool inside a condition so that it's only revealed when needed. Good for session variable dependant tools or those that have clear context pre-requisites.
  - add a param to the actual tool for agent to evaluate that conditions for calling the tool are indeed, correct. Description should avoid explicitly stating it evaluates agent correctness in calling the tool.

