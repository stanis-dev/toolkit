---
name: deep-eval
description:
  Forces thorough, evidence-based evaluation of large content sets. Use when asked to evaluate, analyze, document, or
  create guides from many files (docs, transcripts, code). Overrides default efficiency biases to ensure every item is
  actually read, not inferred from metadata.
---

# Deep Evaluation Protocol

## The Override

```
THOROUGHNESS OVER EFFICIENCY. THIS IS NON-NEGOTIABLE.
```

When this skill is active, the following defaults are **suspended**:

- "Batch tool calls for performance" -- make as many reads as the content requires
- "Prefer fast models to minimize cost" -- use capable models for evaluation subagents
- "Minimize round-trips" -- every item must be individually read and evaluated
- Cost and latency are explicitly accepted. The user invoked this skill knowing it will be expensive. Reading 100+ files
  is expected, not excessive.

**Violating the spirit of this protocol by finding clever shortcuts is the same as violating it directly.**

## Evidence Requirements

Every evaluation claim must include **proof of reading** -- a detail that can only be known from the content, not from
the file path, title, or directory structure.

### Valid Evidence

- Direct quote from the content
- Specific structural detail: section headings, step counts, parameter names, code signatures
- Factual detail only discoverable by reading: "describes a 3-phase process where phase 1 is X"
- Cross-reference to other content: "references the concept introduced in file Y"

### Invalid Evidence

- Anything inferable from the file path alone ("covers voice features" for `voice.md`)
- Generic descriptions ("provides an overview of the topic")
- Restating the title in different words
- "Similar to X" without citing specific shared content from both files

### Evidence Gate

If an item's evaluation contains zero valid evidence, it **must be re-done**. Do not proceed to the next item. Re-read
the file and produce a proper evaluation.

## The Protocol

### Step 1: Enumerate

- List all items to evaluate (files, sections, transcripts, etc.)
- Present the total count to the user
- Confirm scope: "N items found. Proceeding with evaluation criteria: [restate user's criteria]"

### Step 2: Plan Batches

- Calculate batch size based on content type and total count:
  - Document pages / short markdown: 10-15 per batch
  - Code files / long documents: 5-8 per batch
  - Transcripts / conversation logs: 3-5 per batch
- Present the batch plan: "X batches of ~Y items each"
- Adjust if user requests different sizing

### Step 3: Process Batch

For each item in the current batch:

1. **Read full content** -- no offset/limit unless file exceeds 500 lines. For long files, read in sections covering the
   full file.
2. **Apply evaluation criteria** -- whatever the user specified in their invocation
3. **Include evidence** -- at least one valid evidence item per evaluated piece
4. **Flag anomalies** -- note anything unexpected, missing, or contradictory

### Step 4: Checkpoint

Present batch results to the user with a progress header:

```
--- Batch 2/8 | 25/120 items evaluated ---
```

Then **stop and wait** for user confirmation before continuing. The user may:

- Confirm and continue
- Adjust evaluation criteria based on what they've seen
- Skip remaining batches if they have enough
- Request re-evaluation of specific items

### Step 5: Iterate

Repeat Steps 3-4 for each remaining batch.

### Step 6: Assemble

Once all batches are complete (or user signals to stop):

- Compile all batch results into the final output format
- If user specified a document/guide as output, assemble it now
- Preserve the evidence in the final output or in a companion artifact

### Step 7: Verify Completeness

- Count evaluated items vs total enumerated items
- Report: "Evaluated X/Y items (Z%)"
- If any items were skipped, list them explicitly with reason

## Anti-Pattern Prevention

| Temptation                                              | Reality                                         |
| ------------------------------------------------------- | ----------------------------------------------- |
| "This file is clearly about X based on the name"        | Open and read it. Names mislead.                |
| "Similar to the previous file"                          | Prove it with content from both.                |
| "I can group these by directory and describe the group" | Each item gets individual evaluation.           |
| "The manifest/index has enough metadata"                | Metadata describes structure, not content.      |
| "Reading all these files would be excessive"            | That is literally the task.                     |
| "I'll sample representative files and extrapolate"      | Sampling is estimation, not evaluation.         |
| "I can use a fast subagent for this"                    | Use a capable model. Speed is not the goal.     |
| "I already know what this SDK/framework does"           | Pre-training knowledge is stale. Read the file. |
| "The user won't notice if I skip a few"                 | The evidence gate will.                         |

## Subagent Delegation

When the content set is large enough to benefit from parallel subagents:

### Prompt Rules

- Include the full Evidence Requirements section in every subagent prompt
- Never use "quickly", "briefly", "summarize", or "skim" in subagent instructions
- Specify: "Read each file in full. For each item, include at least one direct quote or content-specific structural
  detail as proof of reading."
- Do not use `model: "fast"` for evaluation subagents

### Verification

- Parent agent must spot-check at least 2 items per subagent batch
- Spot-check means: re-read the file, verify the subagent's evidence is accurate and present in the actual content
- If a spot-check fails, reject the entire subagent batch and re-process

## Adaptation Notes

This protocol is content-type agnostic. The user's invocation defines **what** to evaluate and **what output** to
produce. This skill defines **how thoroughly**. Examples:

- "Evaluate all docs and create a content guide" -- evaluation criteria = what each doc covers; output = guide document
- "Review all transcripts for phrasing issues" -- evaluation criteria = phrasing quality; output = issue list with
  citations
- "Analyze all test files for coverage gaps" -- evaluation criteria = what's tested vs what isn't; output = gap report
- "Compare old and new versions of these files" -- evaluation criteria = what changed; output = change summary with
  before/after evidence
