---
name: wiki-editorial
description: >-
  Review-gated workflow for the toolkit knowledge wiki. Use to propose, publish, or lint durable
  knowledge in `knowledge-wiki/`. Not for journal notes, broad memory capture, or auto-ingesting
  whole sessions.
---

# Wiki Editorial

High-friction editorial workflow for `/Users/stan/code/toolkit/knowledge-wiki`.

## Constraints

- `knowledge-wiki/` is separate from `/Users/stan/journal`. Do not repurpose journal files as canonical storage.
- Never auto-ingest session state. Only work from explicitly selected source files.
- A proposal cycle may target **at most two** canonical pages.
- `propose` may write only under `raw/ingest/` and `candidate/`.
- `publish` may run only after explicit user approval in the conversation.
- Inferred personal-pattern claims default to `status: hypothesis`.
- `review_basis: inference` must never publish as `status: fact`.
- Canonical pages must trace back to copied `raw/ingest/` files, not external absolute paths.
- Re-read impacted canonical neighbors before publishing any change.
- Never dump canonical content into startup context. Retrieval is on-demand.

## Workflow

### 1. Choose Mode

Modes:

- `propose` for a new review cycle
- `publish` for an approved candidate
- `lint` for local or full validation

Done when: the mode and exact scope are explicit.

### 2. Propose

1. Confirm the source files are explicit and the canonical targets are no more than two.
2. Run:

```bash
python3 <skill-dir>/scripts/wiki_editorial.py propose \
  --title "Short proposal title" \
  --domain operating \
  --status fact \
  --review-basis explicit_source \
  --source /absolute/path/to/source.md \
  --target-path canonical/example.md
```

3. Read the copied raw files and impacted canonical neighbors in full.
4. Fill in the generated report and patch files.

Done when: the candidate report explains the case for canon and the candidate patch contains full publishable file
contents for every target.

### 3. Publish

1. Re-read the candidate report, candidate patch, touched pages, and neighbors.
2. Ensure the user has explicitly approved publication.
3. Run:

```bash
python3 <skill-dir>/scripts/wiki_editorial.py publish --proposal-id <proposal-id>
```

Done when: canonical files are written, `system/index.md` is regenerated, `system/log.md` is appended, and local lint
passes.

### 4. Lint

Use local lint before or after publication:

```bash
python3 <skill-dir>/scripts/wiki_editorial.py lint --proposal-id <proposal-id>
```

Use full lint for maintenance:

```bash
python3 <skill-dir>/scripts/wiki_editorial.py lint --full
```

Done when: errors and warnings are reported clearly, with file paths.

## GOOD / BAD

### GOOD

- Copy one explicit source file into `raw/ingest/`.
- Scaffold one report and one patch.
- Publish only after approval, with local lint.

Reasoning: the pipeline stays narrow, auditable, and reversible.

### BAD

- Read a long session and promote “what seems durable” straight into `canonical/`.
- Treat inferred traits as facts.
- Publish while the patch still contains `TBD`.

Reasoning: this creates false canon and makes the wiki less trustworthy than not having one.

## Anti-Patterns

| Temptation | Reality |
| --- | --- |
| “This feels durable enough; I’ll just add it directly.” | Direct canonization is the main failure mode. Use `propose`, then review, then publish. |
| “The source is obvious from context.” | Canonical pages must cite copied `raw/ingest/` files, not session memory. |
| “It’s only one little inferred trait, so `fact` is fine.” | Inference without separate confirmation remains `hypothesis`. |
| “I can clean up neighboring pages later.” | Every publish must re-check impacted neighbors in the same cycle. |

## Interaction Rules

- Ask for source paths if they are not explicit.
- Ask for approval before running `publish` if it has not already been given in the conversation.
- Act without asking when the mode, inputs, and target paths are already explicit.
- Prefer one narrow proposal over batching unrelated changes together.

## Output Expectations

- `propose`: return the proposal id and the generated report/patch paths.
- `publish`: return the published canonical paths plus any lint warnings.
- `lint`: return errors first, then warnings, with concise remediation notes.
