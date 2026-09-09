# Ghostwriter credential scope

Read when `pull`, `lint`, or `push` cannot mint a credential, or when an older `--sync`/`--upload` recipe is being replaced. This page describes interface behavior, not permission to change credentials or routes. For the affected operation, read [ghostwriter files](ghostwriter-files.md). If blocked work must move to another session, read [handoff](../writing/handoff.md).

The subcommands use a workspace-scoped credential minted from the interactive login session and re-minted on expiry. Normal subcommands need no manual token handling. For headless use, `pnpm sierra ghostwriter token mint <org>` exchanges an admin API token with the "Ghostwriter API" scope, supplied as `SIERRA_GHOSTWRITER_API_TOKEN`, for a short-lived workspace-scoped credential stored apart from the login. `pnpm sierra ghostwriter workspace <command>` creates and deletes workspaces minted for that headless path. Never print a token value in diagnosis.

The legacy flags `--sync`, `--lint`, and `--upload` with a workspace-name positional use the org-scoped login instead. The legacy `--upload` path could downgrade on a scoping 403 to a blocks-import route carrying only journey blocks and intents, which does not preserve tools, knowledge, config, or other resources.

A scope or validation rejection does not authorize broader credentials or a lower-level route. Stop the rejected operation and report it. Use a documented alternative only after its authorization and resource coverage are established, and then verify every changed resource that landed, not just blocks.
