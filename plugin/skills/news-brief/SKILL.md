---
name: news-brief
description: Triggered by explicit invocation only
---

# News brief

All necessary env vars must be sourced from `~/code/toolkit/plugin/skills/news-brief/.env`

## Task

- Search the web for recent articles across: AI, gaming, software engineering, cinema/TV, psychology, Hacker News
  front-page, science curiosities.
- For each candidate, check `stash` for a near-duplicate via embedding cosine similarity; skip paraphrases.
- Reject drama, clickbait, and empty content with no substance.
- Keep up to 30 items per period.
- Write an HTML brief to `briefs/brief-<date>.html`

- Articles that have absolutely no value must be inserted into `trash` table when:
    - article regurgitates in verbose form someone's post or a thread on social media. That post/thread already contains
      that information, so article should be permanently excluded from any future search.
    - article contains information for which a more complete source has already been found.
    - article content is based purely on dramatisation of an event.
- Use this table to de-noise your results and avoid analysing bad content.
- If an article has already been used in a report, avoid re-reporting it, unless new information has surfaced that
  changes or completes the previous report.
- All articles used for a report must be added to `stash` table

## Report Format

- Single page html with a list of articles. Header and short summary visible. Full content hidden and can be un-folded
  by user.
- Strip all clickbaits and bloat. Rewrite content in format of the "good journalism"
- Preserve picture where relevant and good for context
- Main article content can be as short or as long as necessary. The goal is to remove all content that is used for
  attention grabbing, while preserving as much as possible of what genuinely matters.

## RAG

Storage at `$DATABASE_URL`.

Embedding model: OpenAI `text-embedding-3-small` at 768 dims (Matryoshka-truncated):

```bash
curl -s https://api.openai.com/v1/embeddings \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"text-embedding-3-small","input":"<text>","dimensions":768}'
```

Schema:

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS stash (
  url_hash    TEXT PRIMARY KEY,
  url         TEXT,
  title       TEXT,
  summary     TEXT,
  embedding   VECTOR(768),
  seen_date   DATE,
  metadata    JSONB DEFAULT '{}'::jsonb
);
CREATE INDEX IF NOT EXISTS idx_stash_embedding ON stash USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_stash_date ON stash (seen_date);

CREATE TABLE IF NOT EXISTS trash (
  url_hash    TEXT PRIMARY KEY,
  url         TEXT,
  reason      TEXT,
  seen_date   DATE,
  metadata    JSONB DEFAULT '{}'::jsonb
);
CREATE INDEX IF NOT EXISTS idx_trash_url ON trash (url);
CREATE INDEX IF NOT EXISTS idx_trash_url_hash ON trash (url_hash);


```
