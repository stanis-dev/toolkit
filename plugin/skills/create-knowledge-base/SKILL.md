---
name: create-knowledge-base
description:
    REQUIRED before creating or editing a knowledge base or knowledge integration. Invoke this skill
    when you need to create a source, choose a crawler origin, seed articles directly, or validate
    that a source is actually searchable.
---

# Creating a Knowledge Base

Read [Knowledge Authoring](docs/knowledge-reference.md) first.

There are two creation paths:

- **Source-backed** -- mirrors an upstream system (website, Zendesk, etc.) via a crawler. Requires
  `origin` and a follow-up `run_knowledge_source_crawl`.
- **Article-seeded** -- content is provided directly as articles. No crawler or crawl needed. Use
  this when the user provides content directly (product guides, troubleshooting steps, policies,
  transcripts). Indexing is asynchronous -- search results may take up to 30 seconds to appear.

## Model

Keep these layers separate:

- **crawler definition** -- code or built-in logic that knows how to fetch content
- **knowledge source** -- configured Sierra object with source ID and origin
- **`knowledge_tool`** -- runtime search block over source IDs

Important runtime distinction:

- `origin.type="agent"` selects a code-defined `ExternalKnowledgeBase` from `knowledge.ts` by name
- `origin.type="integration"` selects a code-defined `ExternalKnowledgeBase` from an installed
  integration by `integration:<handle>`
- the Knowledge API targets source IDs, not crawler definitions

## Phase 1: Discover

Check live state before designing anything:

1. `list_knowledge_sources`
2. `search_knowledge_base_articles` on likely sources
3. `get_knowledge_source_creation_options` only if a new source-backed KB is needed

Exit criteria:

- you know whether an existing source is reusable
- if not, you know whether the user is providing content directly (article-seeded path) or has an
  upstream system to crawl (source-backed path)

## Phase 2a: Article-seeded creation

Use this path when the user provides content directly -- product knowledge, troubleshooting guides,
policies, transcript-derived playbooks, or any text the user wants the agent to be able to search.

Call `create_knowledge_source` with `articles` (not `origin`). Each article needs:

- `title` (required) -- descriptive title for retrieval
- `body` (required) -- the article content
- `alternativeTitles` (optional) -- variant titles that improve search recall
- `sourceUrl` (optional) -- auto-generated if omitted

Article-seeded knowledge bases default to draft mode (`isDraft: true`) so the user can review the
content before it goes live. No crawl is needed (`crawlRequired` will be `false` in the response).

This tool is slow -- article indexing happens asynchronously after creation. Search may return empty
for up to 30 seconds after the tool returns. Create the knowledge base early in your workflow, then
continue with other tasks (building tools, journeys, policies) before validating with search.

Exit criteria:

- the source exists with `articleCount > 0`
- proceed directly to Phase 3 (Validate)

## Phase 2b: Source-backed creation

Use this path when the content lives in an upstream system.

Pick the origin that matches the real upstream:

- `website` for Sierra-managed crawl
- `agent` for `knowledge.ts`
- `integration` for installed integrations with knowledge middleware
- `zendesk`, `reamaze`, `googleDrive`, `aiResearch` only when the source is actually one of those

Reason from the model, not habit:

- creating code changes what crawlers are available
- creating a source binds one crawler to a real Sierra source ID
- Knowledge API uploads only matter after that source exists

Call `create_knowledge_source` with `origin`. Then call `run_knowledge_source_crawl` to ingest.

Exit criteria:

- the source exists
- crawl is enqueued
- `knowledgeBaseName` / `integrationHandle` came from discovery, not invention

## Phase 3: Validate

Validate with live data:

1. source appears in `list_knowledge_sources` with expected `articleCount`
2. `search_knowledge_base_articles` returns relevant articles

For source-backed KBs, also verify the crawl completed successfully. If search is empty, the likely
failure is:

- wrong source or name / handle
- wrong build target
- crawl still in progress or returned no articles
- empty upstream content

For article-seeded KBs, indexing is asynchronous. If search is empty despite `articleCount > 0`,
wait 15-30 seconds and retry -- the indexes are still being built.

Exit criteria:

- the source is real, searchable, and belongs to the intended domain

## Phase 4: Hand off

Only after validation:

1. invoke `/add-knowledge`
2. use the real source ID
3. design the tool around actual contents

## Quality checklist

| #   | Check                                                                |
| --- | -------------------------------------------------------------------- |
| 1   | Existing sources were checked first                                  |
| 2   | Creation path matches the content source (articles vs origin)        |
| 3   | For source-backed: origin and names came from live discovery         |
| 4   | For article-seeded: each article has title and body                  |
| 5   | Search returned real articles before handing off to `/add-knowledge` |
