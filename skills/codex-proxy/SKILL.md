---
name: codex-proxy
description:
    Direct ChatGPT API proxy using Codex auth tokens. Use for lightweight text-in/text-out
    LLM calls with near-zero overhead (~24 tokens vs ~31K through Codex CLI).
---

# codex-proxy

A thin CLI wrapper that calls the ChatGPT Responses API directly using Codex's stored auth tokens,
bypassing all Codex tool registration and system prompt overhead.

## Prerequisites

- Python 3.6+
- Codex CLI installed and authenticated (`codex login`)
- `~/code/toolkit/scripts/` on your PATH

## Usage

```bash
# One-shot prompt
codex-proxy "What is 2+2?"

# Pipe stdin
echo "Summarize this document" | codex-proxy

# Custom model and reasoning effort
codex-proxy -m gpt-5.4 -e high "Explain monads"

# Custom system instructions
codex-proxy -i "You are a haiku bot" "Write about rain"

# JSON output with usage stats
codex-proxy --json "What is 2+2?"

# Buffer full response before printing
codex-proxy --no-stream "Tell me a joke"
```

Positional prompt and stdin are mutually exclusive. If a prompt argument is given, stdin is ignored.
To combine file content with an instruction, construct the prompt in the pipe:

```bash
(echo "Summarize:"; cat doc.txt) | codex-proxy
```

## Options

| Flag | Default | Description |
|---|---|---|
| `-m, --model` | `gpt-5.4-mini` | Model to use |
| `-e, --effort` | `low` | Reasoning effort: `low`, `medium`, `high` |
| `-i, --instructions` | `You are a helpful assistant.` | System instructions |
| `--json` | off | Output JSON with text + usage |
| `--no-stream` | off | Buffer full response locally before printing (API always streams) |

## How it works

1. Reads the access token from `~/.codex/auth.json` (written by `codex login`)
2. Checks JWT expiry -- if within 1 hour, shells out to `codex features list` to trigger refresh
3. Sends a streaming POST to `https://chatgpt.com/backend-api/codex/responses` with zero tools
4. Parses SSE events and outputs text (streaming or buffered)

## Token overhead comparison

Measured against Codex v0.118.0:

| Approach | Input tokens |
|---|---|
| codex-proxy (this tool) | ~24 |
| `codex exec` (default) | ~31K |

## Caveats

- The ChatGPT backend endpoint is not a public API and could change in future Codex versions.
- Depends on Codex being installed and authenticated for token refresh.
- Rate limits and quota come from your ChatGPT subscription tier.
- No tool execution -- purely text-in/text-out.
