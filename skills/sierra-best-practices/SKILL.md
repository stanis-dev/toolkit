---
name: sierra-best-practices
description: >-
  Rules and constraints for Sierra agent development: journey/tool implementation, simulation design,
  workspace operations, and code review. Not for browsing issues, reading conversations, or triaging.
---

# Sierra Agent Development Guidelines

Must apply whenever working on Sierra Agent.

## Constraints

- **Sierra libraries are private.** Never use Context7, web search, or pre-training knowledge for Sierra SDK questions.
  The only source of truth is `~/code/agent-ctx/sierra-docs`. Consult [docs-routing.md](references/docs-routing.md) for
  the exact file.
- **Retrieval over generation.** Do not guess at Sierra APIs, component props, hook signatures, or skill patterns.
  Always verify from docs before writing or recommending Sierra code.
- **Default workspace is standard.** Use the default workspace for most development. Feature workspaces are available
  when the user requests isolation — create and manage them via `sierras` CLI with `--workspace-name` flag.
- **Simulation TDD.** Design and validate simulations before implementing fixes. Read
  [simulations.md](references/simulations.md) for the structured format and validity checklist.
- **Journey context is mandatory for behavior work.** Keep the current journey definition in context when analyzing
  failures, proposing fixes, or implementing behavior-affecting changes in tools, prompts, simulations, or features.
  If the workspace version changes, re-fetch the journey definition before continuing so you do not collide with or
  duplicate current journey behavior.
- **Workspace diffs via sierras CLI only.** Use `sierra-powertool` skill for CLI reference.

## References

- **Documentation routing**: [docs-routing.md](references/docs-routing.md) — lookup table for all Sierra SDK, Studio,
  and integration docs. Consult before answering Sierra-specific questions.
- **Simulation guidelines**: [simulations.md](references/simulations.md) — structured format for sim instructions,
  validity checklist, evaluation rules.
- **CLI reference**: Use `sierra-powertool` skill for sierras CLI commands, sim evaluation workflow, and replay
  debugging.
- **Feature specs**: Located in `./context-docs/specs`, named after the Linear ticket ID.

## Debug Notes

- If `pnpm sierra watch` is not running against the target workspace, upload code manually via sierras CLI and remind
  the user to restart `watch` for ongoing sync.

## Anti-Patterns

| Temptation | Reality |
|---|---|
| Skip docs-routing lookup because you "know" the Sierra API | Sierra is private. Your pre-training has zero Sierra SDK knowledge. Docs are the only source. |
| Treat a simulation as passing because tags matched | Tag match without conversation validity is a false positive. Run the validity checklist from simulations.md. |
| Answer Sierra architecture questions from general LLM knowledge | Sierra has unique patterns (supervisor instructions, condition-driven prompts). Always verify from docs. |

## Examples

### GOOD — Sierra SDK question
> User: "How do I add a condition that triggers when the customer mentions a complaint?"
> Agent: *Reads docs-routing.md, identifies `reference/skills/goal-oriented-skills/` as the relevant path,
> reads `Condition` component reference, then answers with cited doc snippets.*

Reasoning: Verified the answer from Sierra docs before responding. Cited the source.

### BAD — Sierra SDK question
> User: "How do I add a condition that triggers when the customer mentions a complaint?"
> Agent: "You can use a Condition component with a `when` prop that matches the customer's intent."

Reasoning: Answered from pre-training. Sierra's Condition API may differ from what the model assumes. No doc
verification, no citation.

## Interaction Rules

- Before answering Sierra SDK questions or making implementation decisions, verify against docs via
  [docs-routing.md](references/docs-routing.md). If docs are not cached locally, say so and suggest
  `sierras fetch-docs`.
- After every simulation create or update, apply the full validity checklist from
  [simulations.md](references/simulations.md). Do not consider a simulation ready until validity passes.
- When the user requests a feature workspace, create it via `sierras` CLI and use `--workspace-name` for all
  subsequent operations. Prefer workspace-name flag for idiomatic invocations.
