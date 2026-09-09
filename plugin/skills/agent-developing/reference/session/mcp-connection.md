# Agent Studio MCP connection

Read when the Sierra tools are absent, a connection is reloaded, or a tool appears to target the wrong workspace. [Setup](setup.md) controls setup and permissions.

The agent-scoped Agent Studio MCP is the server the CLI writes into `.mcp.json` at the root of the checkout. Its key defaults to `sierra`, so the tools load as `mcp__sierra__*`. This repo hosts several agents and registers one server per agent under distinct keys (`sierra`, `sierra-base`, `sierra-358` today), each scoped to its own agent and workspace. Confirm the loaded prefix and the server's workspace with a read before any write. Another server's presence does not establish access to this agent.

`pnpm sierra add-workspace`, `pnpm sierra watch --mcp`, and `pnpm sierra setup-mcp` write the bot and workspace IDs into that config. Workspace scoping lives in the file, but the live connection keeps the values loaded at connection time. Rewriting the file does not retarget already-loaded tools.

To switch to another workspace: rerun the CLI command against it so the config is rewritten, reload the MCP connection through the client's mechanism, then confirm a tool reports the new workspace before any MCP write. If a new turn or a restart is required, record the continuation point instead of assuming immediate effect.

The authoritative tool inventory is the connected server's own listing. Read [result access](../gates/simulation-results.md) only when reading conversation or simulation evidence.
