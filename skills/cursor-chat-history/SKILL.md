---
name: cursor-chat-history
description:
    Find, filter, and reconstruct Cursor agent chat histories from on-disk storage. Use when the user asks about past
    agent conversations, wants to export or search chat history, recover lost chats, or analyze what an agent did in a
    previous session.
---

# Cursor Chat History Recovery

## Storage Locations (macOS)

### 1. Agent Transcripts (best source — structured JSONL)

```
~/.cursor/projects/<project-slug>/agent-transcripts/<uuid>/<uuid>.jsonl
```

- One JSONL file per conversation, one JSON object per line
- Format: `{"role":"user|assistant","message":{"content":[{"type":"text","text":"..."}]}}`
- Subagent transcripts in `subagents/` subdirectory
- Project slug derived from path: `/Users/stan/code/sky` → `Users-stan-code-sky`
- **Limitation**: only `type: "text"` content is captured; tool_use/tool_result blocks are not stored. If an agent says "reading skill X" and subsequently references skill-specific details, treat that as evidence the skill was read — the Read tool call itself won't appear in the transcript.

### 2. Global State DB (largest store — all workspaces mixed)

```
~/Library/Application Support/Cursor/User/globalStorage/state.vscdb
```

- SQLite. Tables: `ItemTable`, `cursorDiskKV`
- `cursorDiskKV` has `agentKv:blob:<hash>` keys with raw message content
- `ItemTable` has `conversationClassificationScoredConversations` — JSON array of `{conversationId, timestamp}` for
  indexing
- `ItemTable` keys like `workbench.panel.composerChatViewPane.<uuid>.hidden` list conversation UUIDs

### 3. Per-Chat SQLite DBs (older format)

```
~/.cursor/chats/<workspace-hash>/<conversation-uuid>/store.db
```

- Tables: `blobs` (id TEXT, data BLOB), `meta` (key TEXT, value TEXT)
- Blobs contain full messages (system prompts, user queries, assistant responses)
- Map workspace hash to project by reading first blob's `Workspace Path`

### 4. Per-Workspace State DBs

```
~/Library/Application Support/Cursor/User/workspaceStorage/<hash>/state.vscdb
```

- Map hash → project via `workspace.json` in same directory
- Same schema as global state DB but scoped to one workspace

## Auxiliary Artifacts

| Artifact          | Path                                               | Content                                                                            |
| ----------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Agent tool output | `~/.cursor/projects/<slug>/agent-tools/<uuid>.txt` | Web fetches, long command output, large results                                    |
| AI code tracking  | `~/.cursor/ai-tracking/ai-code-tracking.db`        | SQLite: `ai_code_hashes` (file→conversation), `scored_commits` (AI vs human lines) |
| Plans             | `~/.cursor/plans/*.plan.md`                        | Agent-generated execution plans                                                    |
| Prompt history    | `~/.cursor/prompt_history.json`                    | JSON array of raw user prompt strings (no responses)                               |
| Snapshots         | `~/.cursor/snapshots/<hash>/`                      | Git bare repos — pre-edit checkpoints                                              |
| Screenshots       | `~/.cursor/projects/<slug>/assets/*.png`           | Browser screenshots from agent sessions                                            |
| PR data           | `~/.cursor/projects/<slug>/pull-requests/pr-<N>/`  | Diffs, comments, summaries                                                         |
| Terminal logs     | `~/.cursor/projects/<slug>/terminals/<pid>.txt`    | Live terminal output from agent commands                                           |

## Common Operations

### List all projects with transcripts

```bash
for d in ~/.cursor/projects/*/agent-transcripts; do
  [ -d "$d" ] && echo "$(basename $(dirname $d)): $(ls -d $d/*/ 2>/dev/null | wc -l) conversations"
done
```

### Extract user queries from a transcript

```bash
python3 -c "
import json, re, sys
for line in open(sys.argv[1]):
    d = json.loads(line)
    if d.get('role') == 'user':
        for c in d['message']['content']:
            if c.get('type') == 'text':
                m = re.search(r'<user_query>\s*(.*?)\s*</user_query>', c['text'], re.DOTALL)
                if m: print(m.group(1)[:200])
" PATH_TO_JSONL
```

### Map workspace storage hash to project

```bash
for f in ~/Library/Application\ Support/Cursor/User/workspaceStorage/*/workspace.json; do
  echo "$(basename $(dirname $f)): $(python3 -c "import json; print(json.load(open('$f')).get('folder','') or json.load(open('$f')).get('workspace',''))")"
done
```

### Query conversation index from global DB

```bash
sqlite3 ~/Library/Application\ Support/Cursor/User/globalStorage/state.vscdb \
  "SELECT substr(CAST(value AS TEXT), 1, 500) FROM ItemTable WHERE key = 'conversationClassificationScoredConversations';"
```

### Trace which files a conversation touched

```bash
sqlite3 ~/.cursor/ai-tracking/ai-code-tracking.db \
  "SELECT fileName, model, datetime(timestamp/1000,'unixepoch','localtime') FROM ai_code_hashes WHERE conversationId = 'CONVERSATION_UUID' ORDER BY timestamp;"
```
