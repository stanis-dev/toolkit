# Canonical agent guidance

Read before any code or no-code edit. Load the matching per-task skill, not the whole bundle.

`pnpm sierra ghostwriter init` and `pull` materialize Sierra's canonical task skills at `.composer/.claude/skills/<name>/SKILL.md` and the resource references at `.composer/docs/`. In this checkout the same skills are also exposed to the Skill tool by name (`add-simulation-test`, `fix-issue`, `update-config`, and the rest). The `add-*`, `create-*`, and `update-config` skills mark themselves REQUIRED before their task. The bundle describes the workspace's supported blocks, tools, knowledge, simulations, and config: use it for file shapes and editing instructions. A code edit under `agents/{agent}` is gated on the matching canonical skill the same way as a no-code change.

This skill adds what the bundle does not carry: runtime semantics, session mechanics, and the gates. The `sierra-inc/sierra` monorepo and `sudo_search_docs` are not reachable in this environment. When the bundle leaves a concept unresolved, ground it with `ask_sierra_assistant` and check the answer against the installed SDK version. Do not substitute a newer schema for the installed one.

When the bundle is missing or stale, read [ghostwriter](ghostwriter.md) and [ghostwriter files](ghostwriter-files.md) to materialize it. Do not initialize a workspace only because this page was loaded.
