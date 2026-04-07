# Knowledge Wiki Schema

This schema governs the editorial pipeline for `knowledge-wiki/`.

## Canonical Contract

Each canonical page must begin with YAML frontmatter containing:

```yaml
---
title: Example Page
status: fact
domain: operating
confidence: medium
source_refs:
  - raw/ingest/20260406-120000-example/source-01-notes.md
last_reviewed: 2026-04-06
review_basis: explicit_source
contradicts: []
supersedes: []
---
```

Required fields:

- `title`: human-readable page title.
- `status`: `fact` or `hypothesis`.
- `domain`: free-form domain label such as `operating`, `projects`, `preferences`, or `people`.
- `confidence`: `low`, `medium`, or `high`.
- `source_refs`: one or more paths under `raw/ingest/`.
- `last_reviewed`: ISO date in `YYYY-MM-DD`.
- `review_basis`: `explicit_source`, `self_report`, `observed_behavior`, or `inference`.
- `contradicts`: list of canonical page paths contradicted by this page.
- `supersedes`: list of canonical page paths superseded by this page.

Rules:

- `review_basis: inference` may not publish as `status: fact`.
- `source_refs` must resolve to copied raw files, not journal paths or external absolute paths.
- `contradicts` and `supersedes` entries must point at canonical markdown files when present.
- Published pages must not contain placeholder markers such as `TBD`.

## Candidate Report Contract

Each report in `candidate/reports/` must include frontmatter:

```yaml
---
proposal_id: 20260406-120000-example
title: Example Proposal
status: fact
domain: operating
review_basis: explicit_source
recommendation: pending
source_refs:
  - raw/ingest/20260406-120000-example/source-01-notes.md
target_paths:
  - canonical/example.md
neighbor_paths:
  - canonical/related-page.md
---
```

And body sections:

1. `Why this deserves canon`
2. `Proposed changes`
3. `Impacted existing pages`
4. `Uncertainty and contradictions`
5. `Publication recommendation`

## Candidate Patch Contract

Each patch in `candidate/patches/` must include frontmatter:

```yaml
---
proposal_id: 20260406-120000-example
title: Example Proposal
target_paths:
  - canonical/example.md
---
```

Then one fenced block per target:

````md
## Target: canonical/example.md
```md
<full markdown file content to publish>
```
````

Patch rules:

- Paths must live under `canonical/`.
- A single proposal may target at most two canonical pages.
- The fenced content is the full file body that will be published.

## Lint Rules

`lint` enforces or reports:

- Missing metadata
- Invalid `status`, `confidence`, or `review_basis`
- Missing or broken `source_refs`
- `inference` pages incorrectly marked as `fact`
- Broken local markdown links
- Stale review dates
- Weak provenance for high-confidence facts
- Duplicate canonical titles
- Orphan pages with no canonical links
- Superseded pages needing review

Local lint checks touched pages plus neighbors. Full lint checks the entire canonical corpus.
