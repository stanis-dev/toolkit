# Ghostwriter (no-code definitions)

`pnpm sierra ghostwriter` carries the no-code half. Code reaches the workspace through the watcher or the point-in-time upload per [workspace CLI](workspace-cli.md); verify both halves when a behavior crosses them. Run it from `agents/{agent}` after [setup](setup.md) has verified the target, one subcommand per invocation. Discover the current subcommands with `pnpm sierra ghostwriter --help`. The legacy `--sync`, `--upload`, `--watch`, `--lint` and `--typegen` flags on the bare `ghostwriter <target>` form still run, and `pnpm sierra composer` is an alias for that legacy form, but neither is a guide to the current interface.

Read [ghostwriter files](ghostwriter-files.md) before a file operation and [canonical guidance](canonical-guidance.md) before an edit. Read [ghostwriter credentials](ghostwriter-auth.md) only for a credential or legacy-compatibility concern. When a workspace diff exposes a conflict or a foreign object, read [conflicts](../shipping/conflicts.md). Before changing authored prompt text, read [authoring](../writing/authoring.md).

## No-code edits

The server is the source of truth. `push` publishes the complete materialized copy, not only the intended delta.

1. Initialize the working copy once for the exact thread workspace when it is absent: `pnpm sierra ghostwriter init <workspace-name>`. Treat `.composer/` as a gitignored working copy, not the permanent source.
2. Pull current workspace content before editing: `pnpm sierra ghostwriter pull`. It backs up the previous local files under `.composer/history/working/` before overwriting. Keep the pull-to-push interval short; Studio changes between turns are the normal case.
3. Read the matching canonical skills and the resource docs the pull materialized. Edit only the required resources. Let lint assign identities to new blocks. After changing a tool's `definition.json`, run `pnpm sierra ghostwriter generate types` to regenerate the `implementation.ts` wrapper types.
4. Lint the affected resources: `pnpm sierra ghostwriter lint [paths..]`. It validates locally and runs a server-side dry run. Inspect the full intended change set, including deletions: a deleted local block file deletes that block on push.
5. Push: `pnpm sierra ghostwriter push`. Verify what landed and record the resulting workspace version before tests or handoff. If the server changed concurrently, pull and reconcile rather than overwriting unrelated work.

A validation or credential-scope rejection is not permission to use broader credentials or a legacy import route. Stop the affected operation and report the rejection. Use a documented alternative only after its authorization and resource coverage are established. A blocks-only transfer does not preserve tools, knowledge, or other resources.

## Canonical skills in `.composer/`

`init` and `pull` also materialize Sierra's canonical agent-building skills and reference docs into the working copy: `.composer/.claude/skills/<name>/SKILL.md` for the per-task skills and `.composer/docs/` for the block, tool, knowledge, simulation, and config references. Load the matching canonical skills before any change, no-code or code alike; [canonical guidance](canonical-guidance.md) carries the rule. This skill covers only what the bundle does not: gates, runtime semantics, and session mechanics.
