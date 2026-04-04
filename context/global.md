# Global Context

Personal preferences and cross-tool reference that applies to every session.

## Codex Bare Profile

A minimal-context profile for Codex CLI, modeled after Claude Code's `--bare` flag. Use it for
scripted tasks, SDK calls, or any situation where startup speed and token efficiency matter more
than rich behavioral guidance.

### What it strips

| Layer | Normal mode | `bare` profile |
|---|---|---|
| Base instructions | ~3K chars (prompt.md + personality) | ~180 chars (bare-instructions.md) |
| Permissions block | Full sandbox policy explanation | Stripped (`include_permissions_instructions = false`) |
| Apps block | Connector instructions | Stripped (`include_apps_instructions = false`) |
| Environment block | CWD, shell, OS version | Stripped (`include_environment_context = false`) |
| AGENTS.md | Up to 32KB loaded | Zero bytes (`project_doc_max_bytes = 0`) |
| Tools | Shell, apply_patch, web search, multi-agent, apps | Shell + apply_patch only |
| Hooks | hooks.json lifecycle hooks | Disabled |
| Reasoning | Model default | Minimal effort |

### What still works

- Shell command execution and file editing (apply_patch)
- Sandboxing (workspace-write)
- MCP servers defined in global config (cannot be per-profile disabled)
- Conversation history and compaction
- Resume/fork sessions

### Usage

```bash
codex -p bare "your prompt here"     # one-shot
codex -p bare                        # interactive with minimal context
codex exec -p bare "your prompt"     # headless
```

### Files

- Profile: `~/.codex/config.toml` under `[profiles.bare]`
- Instructions: `~/.codex/prompts/bare-instructions.md`

### Undocumented config keys used

These booleans are in the Codex Rust source (`codex-rs/core/src/config/mod.rs`) but not in the
official docs. They are per-profile configurable and directly strip message blocks from the prompt:

- `include_permissions_instructions` (default: true) -- the `<permissions>` developer block
- `include_apps_instructions` (default: true) -- the `<apps>` developer block
- `include_environment_context` (default: true) -- the `<environment>` user block

### Comparison with Claude Code --bare

Claude Code's `--bare` additionally strips: OAuth/keychain auth (API-key-only), all hooks,
LSP, plugin sync, auto-memory, CLAUDE.md walk, background prefetches, and reduces the tool set
to 3 (Bash + FileRead + FileEdit). The Codex bare profile achieves a comparable prompt reduction
but cannot filter the tool set or disable MCP servers per-profile.
