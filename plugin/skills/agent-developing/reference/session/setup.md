# Session setup

Configure only what the task needs. An assessment, a read-only review, or a code-only check needs no new Agent Studio workspace. For the CLI target commands, read [workspace CLI](workspace-cli.md). For MCP configuration or reload, read [MCP connection](mcp-connection.md). Load either only when that concern applies.

1. Inspect the current repository, agent folder, connected workspace, loaded tools, and running services. Resolve the org and agent from trusted configuration: the agent folder under `agents/`, the targets registered in that folder, and the session branch. Ask only when identity stays ambiguous.
2. Reuse the workspace already assigned to this thread after verifying its identity and ownership. For workspace writes with no dedicated target, create a thread workspace per [workspace CLI](workspace-cli.md), named after the session branch in lowercase kebab-case. Never write into an unrelated or production workspace to avoid setup.
3. Sierra CLI auth lives in `~/.sierra/<subdomain>.sierra.ai.session`, and any server-touching command probes it. When it fails, refresh with `pnpm sierra login <subdomain>`. Discover commands and flags with `--help` at use time. Run workspace commands from `agents/{agent}` and pass the exact thread workspace wherever the command accepts one.
4. For active code iteration, run the watcher in the background. For stable code and post-merge uploads, use the point-in-time upload instead. Preserve unrelated services, and do not assume a background process survives a session refresh.
5. Reload MCP only when the connection is absent or its target changed, per [MCP connection](mcp-connection.md). Do not end a healthy session for setup.
6. Before any MCP write, confirm a read reports the intended org, agent, and workspace. Rewriting config alone does not verify the live connection.

## Capability boundaries

A model name does not establish tool availability or data permission. Discover the live tool surface before connecting anything. Use approved provisioning and authentication only. If access fails, report the missing capability. Do not substitute broader credentials, a different account, or a lower-level route.

Work in the session's primary checkout so edits show in the diff view. Preserve existing changes. An Agent Studio workspace is separate from a git worktree.

The CLI workspace registry is directory-scoped. Keep setup, watch, upload, tests, and deletion in the agent directory. Commands run elsewhere cannot see the registered targets.

## Evidence tools

The Sierra MCP tools read and write Agent Studio: conversations, LLM calls, knowledge, issues, tests, reports, agent checks. Enumerate the loaded server and its tools at use time; the authoritative list is the connected server's own listing. Prefer the verbose option when one exists, request only the necessary detail, and run large reads in a subagent so only the findings reach the main context. Real conversations use the `audit-` prefix and simulation results use different identifiers, so read [result access](../gates/simulation-results.md) before those lookups.

Cleanup follows [lifecycle](../shipping/lifecycle.md). Record whether this thread created or merely reused the workspace.
