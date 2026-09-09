# Model guidance

Read when selecting a model or diagnosing model-specific behavior. Keep the session's model unless the user asks for a change. Discover the supported model IDs, effort levels, and capabilities from the current host. Model guidance never expands permission or weakens a gate.

Vendor guidance checked September 5, 2026. Reopen the exact model's official guide before changing these notes.

## Fable 5.1

Anthropic recommends evaluating `high` effort first. Watch for scope creep, premature stopping, oversized edits, and low progress visibility. Preserve constraints across compaction. Append-only history is the harness's responsibility.

Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1

## GPT-6 Astra

OpenAI emphasizes resolving conflicting instructions, avoiding unnecessary approval pauses, and bounding repeated verification. Define useful delegation opportunities. Preserve supported effort when migrating. Async tools and mid-turn steering require host support.

Source: https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra

## Application

Treat these recommendations as evaluation candidates, not measured Sierra results. Apply only the guidance relevant to an observed failure. Keep hard authorization boundaries explicit. Do not copy consumer-app system prompts into a coding skill or silently remap one vendor's models to another's.

Read [evaluation](../maintenance/evaluation.md) before claiming a model-specific improvement.
