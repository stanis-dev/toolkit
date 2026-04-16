# OpenCode

This subtree holds OpenCode-specific local integrations that belong in `toolkit`
but are not part of the Claude/Codex plugin setup.

## Cursor ACP

`plugins/cursor-acp.ts` is a local OpenCode plugin that bridges the `cursor-acp`
provider to `cursor-agent` through a small OpenAI-compatible proxy.

The active installation is expected to load this file from the user OpenCode
config directory via a symlink, so the source of truth stays in this repo.

Current goals:

- Keep `cursor-acp` as the provider id.
- Replace `@rama_nigg/open-cursor` with a toolkit-owned implementation.
- Refresh models from `cursor-agent models` at startup.
- Preserve OpenCode-owned tool execution by intercepting native Cursor tool calls.

## Configuration

The runtime plugin is now the source of truth for `cursor-acp` provider config.

That means the user OpenCode config should stay minimal:

- keep the toolkit skills path
- keep any unrelated providers like `openai`
- do not hand-maintain a giant static `cursor-acp` model list

The plugin injects:

- provider registration
- current model list
- proxy `baseURL`
- dummy API key for the local OpenAI-compatible transport
