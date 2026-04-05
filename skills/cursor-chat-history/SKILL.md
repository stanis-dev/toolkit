---

name: cursor-chat-history
description:
    Search or export Cursor agent chat history across multiple projects, trace which files a conversation modified, or
parse transcript JSONL format. NOT needed for simple recent-chat lookups in the current project.

---

# Cursor Chat History

Agent transcripts are the single source of truth. Each conversation is a JSONL file at:

```
~/.cursor/projects/<project-slug>/agent-transcripts/<uuid>/<uuid>.jsonl
```

## Transcript Format

Each line is one JSON object: `{"role":"user|assistant","message":{"content":[...]}}`

Content blocks have a `type` field:

- `text` — conversation text. User queries are inside `<user_query>` tags within user-role text blocks.
- `tool_use` — tool calls with `name` and `input` fields. Stored in transcripts.
- `tool_result` — NOT stored. You can see what tools were called but not what they returned.

Subagent transcripts live in `<uuid>/subagents/<sub-uuid>.jsonl` (same format).

Slug derivation: replace `/` and `.` with `-`, strip leading `-`. Example: `/Users/stan/code/sky` becomes `Users-stan-code-sky`.

Transcripts have no timestamps. The only timestamp source is `ai_code_hashes` (see below).

## Recipes

### Find a conversation in the current project

List transcript directories sorted by recency, then read the JSONL:

```bash
ls -lt ~/.cursor/projects/<slug>/agent-transcripts/
```

### Search across all projects

Run `scripts/search-chats.sh` from this skill's directory:

```bash
bash <skill-dir>/scripts/search-chats.sh [--peek] [search-term]
```

Without arguments: lists all projects and conversation counts. With a search term: returns matching transcript paths. Add `--peek` to include the first user query from each match inline — useful when results are broad.

### Extract user queries from a transcript

Run `scripts/extract-queries.py` from this skill's directory:

```bash
python3 <skill-dir>/scripts/extract-queries.py <path-to-jsonl> [max-chars]
```

### Trace which files a conversation modified

Run `scripts/trace-files.sh` from this skill's directory:

```bash
bash <skill-dir>/scripts/trace-files.sh <conversation-uuid>
```

Queries `ai_code_hashes` in `~/.cursor/ai-tracking/ai-code-tracking.db` by `conversationId`. Returns filenames, source (composer/tab/cli), and timestamps. This is the only artifact with a verified structural link to transcript conversation IDs.