---
name: agent-history
description: >-
  Search or export AI agent session history across Cursor, Claude Code, Codex, and OpenCode.
  Trace which files a conversation modified or extract user queries from transcripts. Use for
  cross-project session search, skill performance analysis, or conversation reconstruction.
---

# Agent History

Unified access to agent session transcripts across four platforms.

## Platform Reference

### Cursor

| Field | Value |
|-------|-------|
| Format | JSONL |
| Path | `~/.cursor/projects/<slug>/agent-transcripts/<uuid>/<uuid>.jsonl` |
| Subagents | `<uuid>/subagents/<sub-uuid>.jsonl` |
| Slug rule | Replace `/` and `.` with `-`, strip leading `-` |
| Timestamps | Not in transcripts. Only via `ai_code_hashes` in `~/.cursor/ai-tracking/ai-code-tracking.db` |
| Tool calls | Stored (`tool_use` with name + input) |
| Tool results | NOT stored |
| User queries | Inside `<user_query>` tags in user-role text blocks |

### Claude Code

| Field | Value |
|-------|-------|
| Format | JSONL |
| Path | `~/.claude/projects/<slug>/<uuid>.jsonl` |
| Subagents | `<uuid>/subagents/agent-<hash>.jsonl` |
| Session index | `~/.claude/projects/<slug>/sessions-index.json` (has title, messageCount, created, modified, gitBranch) |
| Slug rule | Replace `/` with `-`, keep leading `-` |
| Timestamps | Yes (ISO 8601 per record) |
| Tool calls | Stored |
| Tool results | Stored |
| Thinking | Stored (with signatures) |
| Model / tokens | Stored per assistant message |
| User queries | Records with top-level `"type":"user"`, content in `message.content` (plain string) |

### Codex

| Field | Value |
|-------|-------|
| Format | JSONL |
| Path | `~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<uuid>.jsonl` |
| Archived | `~/.codex/archived_sessions/rollout-*.jsonl` |
| Timestamps | Yes (ISO 8601) |
| Tool calls | Stored (`response_item` with `function_call`) |
| Tool results | Stored (`function_call_output`) |
| Reasoning | Stored |
| User queries | `event_msg` records where `payload.type == "user_message"` |

### OpenCode

| Field | Value |
|-------|-------|
| Format | SQLite |
| DB path | `~/.local/share/opencode/opencode.db` |
| Schema | 3-tier: `session` -> `message` -> `part` |
| Timestamps | Yes (unix ms in `time_created`) |
| Tool calls | Stored (part `type: "tool"`) |
| Tool results | Stored |
| Reasoning | Stored (part `type: "reasoning"`) |
| User queries | `message` with `role: user` + `part` with `type: text` |

Quick SQL pattern:
```sql
SELECT s.id, s.title, s.time_created
FROM session s
WHERE s.id IN (
  SELECT DISTINCT p.session_id FROM part p
  WHERE p.data LIKE '%search_term%'
)
ORDER BY s.time_created DESC;
```

## Recipes

### Search across platforms

```bash
bash <skill-dir>/scripts/search-sessions.sh [--platform cursor|claude|codex|opencode|all] [--peek] [search-term]
```

Default platform: `all`. Without a search term: lists all projects/sessions per platform with
counts. With a search term: returns matching session paths. Add `--peek` to include the first
user query from each match.

### Extract user queries from a session

```bash
python3 <skill-dir>/scripts/extract-queries.py <path-to-file> [max-chars]
python3 <skill-dir>/scripts/extract-queries.py --session-id <id> --platform opencode [max-chars]
```

Auto-detects platform from path. Use `--session-id` + `--platform opencode` for OpenCode
(SQLite, not file-based).

### Trace file modifications (Cursor only)

```bash
bash <skill-dir>/scripts/trace-files.sh <conversation-uuid>
```

Queries `ai_code_hashes` in `~/.cursor/ai-tracking/ai-code-tracking.db`. Returns filenames,
source, and timestamps. This is Cursor-specific — no equivalent tracking DB exists on other
platforms. For Claude Code, Codex, and OpenCode, file modifications can be inferred from tool
call results (write/edit calls), which ARE stored on those platforms.
