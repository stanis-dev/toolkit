---
name: add-knowledge
description:
    REQUIRED before connecting knowledge bases to an agent. Invoke this skill when you need to add a
    knowledge tool, connect a knowledge base, enable article search, or set up RAG-powered answers.
    Without it you will produce knowledge tools with wrong source IDs, bad names, or incorrect mode.
---

# Adding a Knowledge Tool

A knowledge tool connects the agent to a knowledge base via a built-in RAG pipeline. No
implementation file is needed -- the platform handles retrieval, ranking, and answer generation.

Knowledge bases are typically built by crawling the customer's website, internal docs, reference
material, and similar sources. They tend to be a rich source of information covering policies,
workflows, product features, and more.

KB articles may have been written for a different context than a live agent conversation -- someone
browsing a help center, an internal team, etc. The default RAG prompting can't make assumptions
about this either way, so it stays bland. During discovery, pay attention to how articles are
written and who they were written for. That understanding should inform the tool description and
`supervisor_instructions` so the agent uses the content well in conversation.

Work through the phases below in order.

---

## Phase 1: Discover available knowledge sources

Use the `list_knowledge_sources` MCP tool to see what knowledge bases exist in the workspace. Note
the IDs, names, and **partition parameters** -- you need the IDs for `knowledge_source_ids` and
partition params tell you how the content is segmented.

Then use `search_knowledge_base_articles` with a few different queries to understand what content
each knowledge base contains. The content may cover topics you'd otherwise need to ask the user
about, so exploring thoroughly here saves work later.

If no suitable source exists yet, stop here and invoke `/create-knowledge-base`. Resume this skill
only after a real source ID exists and the source is searchable.

**Exit criteria:** You know the knowledge source IDs, whether any sources have partition parameters,
and have a clear picture of the content available (topics, depth, article types).

---

## Phase 2: Design the knowledge tool

**Prefer one tool across all knowledge sources.** The RAG pipeline scores effectively across
different knowledge bases -- the source distinction exists for independent crawling, not for search
quality. Only split into multiple tools when the content domains are so different that they need
distinct descriptions to drive correct tool-calling (rare).

**Understand partition parameters.** Some knowledge sources have partition parameters (e.g.,
`locale`, `product_line`). These segment the content -- at search time, the agent LLM fills in
partition values and the search is scoped to matching articles. If a partition param is marked
`required`, the search fails without it. Partitioned and unpartitioned sources generally should not
be combined into one tool since partition scoping only applies to partitioned sources.

**Name and description drive tool-calling.** The agent decides whether to call a knowledge tool
based entirely on its name and description. Get these wrong and the tool either never fires or fires
on every turn.

- With `mode: "answer"` (default, recommended): name the tool `AnswerFrom{Domain}` or
  `Answer{Topic}Questions` (e.g., `AnswerProductQuestions`, `AnswerFromHelpCenter`). The description
  should say the tool _answers_ questions -- because it does. The RAG pipeline synthesizes a
  response; it does not return raw articles.
- With `mode: "search"`: name the tool `Search{Domain}` (e.g., `SearchKnowledgeBase`). The
  description should say the tool _searches_ for information.

**Use `mode: "answer"` unless you have a reason not to.** Answer mode keeps context tight -- the
tool returns a synthesized answer, not raw articles injected back into the conversation. This means
the agent's context window stays clean. When using answer mode, make the description clear that the
tool should be called for each question, especially when conversations span multiple turns.

**Place knowledge tools at the top level, not behind triggers or conditions.** Knowledge tools work
best when always available. Hiding them behind conditions means the agent can't answer questions
until the condition fires, creating dead zones in the conversation.

**Before writing config, present your design to the user.**

---

## Phase 3: Write config

Add the `knowledge_tool` block as a top-level block in `.composer/blocks/`. See
[Block Reference](docs/block-reference.md) for the full field spec. Minimal example:

```json
{
    "_source_reasoning": "User wants the agent to answer questions from their help center KB.",
    "_policy_reasoning": "Knowledge tools are the backbone for article-backed answers.",
    "type": "knowledge_tool",
    "name": "AnswerFromHelpCenter",
    "description": "Answer customer questions using help center articles. Call this tool for each question the customer asks that could be covered by help center content.",
    "knowledge_source_ids": ["ks-01JMRP7QXBCVN8GHTY3WF0K9E4"]
}
```

**Exit criteria:** `pnpm sierra ghostwriter --lint` passes.

---

## Quality checklist

| #   | Check                                                                              |
| --- | ---------------------------------------------------------------------------------- |
| 1   | Knowledge source IDs are real (from `list_knowledge_sources`, not invented)        |
| 2   | Tool name matches mode: `AnswerFrom...` for answer mode, `Search...` for search    |
| 3   | Description tells the agent _when_ to call it, not just _what_ it does             |
| 4   | One tool covers all sources unless domains differ or partitions require separation |
| 5   | Partitioned sources have `partition_params` configured                             |
| 6   | Tool is top-level (not hidden behind a condition or trigger)                       |
| 7   | No `supervisor_instructions` unless user provided specific guidance                |
