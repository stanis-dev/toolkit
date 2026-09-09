# Workspace CLI

Read before registering a target, running watch or upload, or deleting a workspace. [Setup](setup.md) decides whether setup is needed; [lifecycle](../shipping/lifecycle.md) controls snapshot and deletion authorization.

Run from `agents/{agent}`: the workspace registry is directory-scoped, so a command run elsewhere misses the existing targets. Confirm flags with `--help` before execution. The forms below match SDK 0.20260813.

```sh
pnpm sierra add-workspace <subdomain> <agent-name> <workspace-name> --create
pnpm sierra watch <workspace-name> --mcp --mcp-client claude-code
pnpm sierra upload <workspace-name>
pnpm sierra delete-workspace <workspace-name>
```

`add-workspace` with both name positionals connects to an existing workspace only. `--create` requires both names, creates the workspace when it is absent, and connects when it exists, so success does not establish ownership. When the same local name exists for several orgs, qualify it as `<subdomain>.sierra.ai/<name>`.

The `watch` positional names the local target that `add-workspace` created. It cannot be combined with `--agent`, `--workspace`, or `--non-interactive`; those belong to the alternate resolution path with no local target. Watch hot-reloads code. `upload` sends it once and is the only form to use on the main branch.

`--mcp` writes the MCP server entry for the chosen `--mcp-client` into the project config. `--mcp-server-name` picks the key: the default is `sierra`, `auto` derives `sierra-<agent>` in a multi-agent repo, and a literal value names it explicitly. `--mcp-global` writes to the home config instead. `pnpm sierra setup-mcp <workspace-name>` writes the same entry without starting a watcher. Read [MCP connection](mcp-connection.md) when enabling MCP.

`delete-workspace` has no confirmation prompt and deletes server state. Pass the exact thread workspace name, delete only a workspace this thread created, and never use it as a diagnostic probe. `cleanup-targets` removes local targets whose remote workspace is already gone.

Run a long-lived watcher in the background and preserve unrelated processes. A background job does not survive a session refresh; restart it when the session resumes.
