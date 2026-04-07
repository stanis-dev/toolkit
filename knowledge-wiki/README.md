# Knowledge Wiki

Gated personal wiki compiler stored inside the toolkit repo.

This is a separate system from [`/Users/stan/journal`](/Users/stan/journal). The journal remains a notes and research
workspace. `knowledge-wiki/` is a high-friction publication pipeline for durable knowledge that has earned canonical
status.

## Layers

- `raw/ingest/` stores immutable copied inputs for each proposal cycle.
- `candidate/reports/` stores human-readable review reports for proposed changes.
- `candidate/patches/` stores exact canonical file contents proposed for publication.
- `canonical/` stores published wiki pages only.
- `system/` stores the schema, generated index, and publication log.

## Workflow

1. `propose` copies explicitly selected source files into `raw/ingest/<proposal-id>/` and scaffolds one report plus one
   patch file for at most two canonical targets.
2. A review cycle fills in the report and patch files. Canonical pages are untouched at this stage.
3. `publish` is run only after explicit approval. It validates the proposal, writes canonical files, regenerates the
   index, appends the log, and runs local lint.
4. `lint` checks canonical metadata, provenance, contradictions, stale pages, duplicates, broken links, and orphaned
   pages.

## Rules

- This system does **not** auto-ingest session context.
- `propose` may only scaffold 1-2 canonical additions or modifications per cycle.
- Inferred personal-pattern claims default to `hypothesis`, not `fact`.
- Canonical content must always trace back to files copied into `raw/ingest/`.
- Retrieval stays on-demand. Canonical pages must never be dumped wholesale into startup context.
