---
name: debug-conversations
description:
    Guidance for finding and analyzing conversation history to debug agent behavior. Invoke this
    skill when you need to investigate why the agent responded a certain way, identify tool call
    failures, trace observation classification, or understand the sequence of events in a
    conversation.
---

# Analyzing Conversations

Conversation data is located in `.composer/conversations/`. Each conversation has its own directory.
Use this skill to understand agent behavior from real conversation artifacts.

---

## Phase 1: Context assembly

Read `.composer/docs/agent-traces-reference.md` for the synced artifact layout and shared
`debug.log` and `traces/` format.

**Exit criteria:** You understand the conversation data format.

---

## Phase 2: Identify conversations

Search in `.composer/conversations/` to find the conversation(s) relevant to your investigation.
Strategies include:

- If the user provides an Agent Studio URL, read `.composer/docs/url-reference.md` first, extract
  the clean path or query ID from the URL, and normalize it to the internal typed ID before
  searching or syncing.
- Search `summary.json` files for matching tags, message counts, or other metadata
- Use `rg` across `debug.log` files for specific messages, tags, or tool names
- Look up a specific conversation by ID if already known
- Semantic search: `pnpm sierra ghostwriter --search-conversations "<query>"` (`--limit <n>`, up to
  50; `--days <n>` window, default 30); sync hits with `--sync-conversations --ids <id1,id2>`. A
  "search is not enabled" error means the org is not enrolled.

Do not treat an Agent Studio URL as insufficient just because it omits object prefixes. Normalize
the URL-derived ID yourself first, then continue the investigation.

**Exit criteria:** You have the conversation ID(s) to investigate.

---

## Phase 3: Diagnose

Read `debug.log` (CSV format) in the conversation directory to understand the sequence of events.
OBSERVATIONS, GOALSDK_RESPOND, TOOL_CALL, and FETCH rows have corresponding agent traces in
`traces/` -- only open these if you need to dig deeper into a specific task.

For latency issues, see `.composer/docs/agent-traces-reference.md#diagnosing-turn-latency`.

**Exit criteria:** You have a clear understanding of what happened during the conversation.

---

## Phase 4: Report findings

Report findings grounded in the synced artifacts. Cite specific content when it clarifies your
point; summarize the rest. Tailor depth, tone, and structure to who's asking -- an agent builder
debugging one rule wants different detail than a PM reviewing patterns or a CS lead triaging an
incident. Use markdown naturally: blockquotes for cited content, lists where items are parallel,
headings for sections in longer responses, and inline code for names and identifiers.

**Exit criteria:** Response is grounded in the artifacts and stays scannable.

---

## Quality checklist

| #   | Check                                                                            |
| --- | -------------------------------------------------------------------------------- |
| 1   | Read the logging reference doc before starting analysis                          |
| 2   | Identified the correct conversation(s) based on the investigation criteria       |
| 3   | Read the full debug.log to understand the conversation flow                      |
| 4   | Inspected agent traces for any tasks that needed deeper investigation            |
| 5   | Conclusions are grounded in data from the logs and agent traces, not assumptions |
| 6   | Findings are grounded, cited where helpful, and pitched to the reader            |
