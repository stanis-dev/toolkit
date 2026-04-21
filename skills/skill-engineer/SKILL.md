---
name: skill-engineer
description: >-
  Design, review, and improve AI agent skills (SKILL.md files) and prompts.
when_to_use: >-
  Use for SKILL.md authoring, prompt engineering, and chat history analysis of skill
  performance. Not for code review, PR review, or general writing.
---

# Skill Engineer

Create and review AI agent skills and prompts.

## Operating Principle

This skill exists for deep, thorough work. Every phase runs to completion with maximum depth.

- Read ALL reference files at the start of either mode. Do not lazy-load. Read both:
  - `references/principles.md` (in this skill's directory)
  - `references/taxonomy.md` (in this skill's directory)
- In CREATE: run ALL interview questions that haven't been answered by context. Do not skip
  dimensions because they seem clear — confirm them.
- In REVIEW Phase 1 (Evaluate): evaluate ALL 11 dimensions with full findings. Do not abbreviate.
- In REVIEW Phase 2 (Analyze): read ALL conversations in scope. Do not sample unless the user
  explicitly asks. Report ALL substantive findings per conversation.
- In REVIEW Phase 3 (Challenge): always run. Never skip.
- In REVIEW Phase 4 (Improve): propose concrete changes for every finding.
- Output length is unconstrained. Write as much as the analysis requires. A thorough review
  that runs long is better than a tidy one that misses failures. However, volume is not
  depth — a dimension that clearly passes should get a concise PASS with a one-line finding,
  not a paragraph justifying the obvious.
- Cost and latency are explicitly accepted. The user invoked this skill knowing it is heavy.
- Testing phases via companion skills (skill-creator) are gated on availability and user
  preference, not thoroughness. Always offer them when available. Respect the user's choice
  to skip. This is not an effort shortcut — it's an infrastructure dependency.

**Violating the spirit of this principle by finding clever shortcuts is the same as violating
it directly.**

| Temptation | Reality |
| --- | --- |
| Score a dimension without reading the relevant lines | Ungrounded verdicts are not actionable — cite line numbers or don't score |
| Skip Phase 3 (Challenge) because Phase 1 looks clean | Phase 3 catches systemic issues (redundancy, net-negative) that Phase 1's line-by-line rubric cannot |
| Produce a summary scorecard and call the review done | A review without improvement proposals (Phase 4) is an incomplete deliverable |
| Sample 2-3 conversations in Phase 2 and extrapolate | The failures that matter are in the conversations you didn't read — analyze ALL unless the user says otherwise |

## Companion Skills

This skill integrates with **skill-creator** for controlled testing and benchmarking.
skill-engineer owns requirements and quality standards; skill-creator owns test execution.
See `references/companion-integration.md` for delegation details and writing guide pointers.

## Mode Selection

| Intent | Mode | Trigger phrases |
| --- | --- | --- |
| Build something new | CREATE | "create a skill", "new skill", "design a skill", "build a prompt" |
| Audit, analyze, improve, or challenge an existing skill | REVIEW | "review", "audit", "analyze", "improve", "fix", "challenge", "how is this skill performing" |

If ambiguous, ask: "Are you looking to **create** a new skill, or **review** an existing one?"

---

## Mode 1: CREATE

### Phase 1 — Triage + Challenge

Before creating anything, challenge whether a new skill is actually needed.

1. List installed skills. Detect the current platform and use the appropriate method:
   - Cursor: use Glob for `~/.cursor/skills/*/SKILL.md` and plugin cache directories
   - Claude Code: run `ls ~/.claude/plugins/*/skills/*/SKILL.md ~/.claude/skills/*/SKILL.md`
   - Codex: run `ls ~/.codex/skills/*/SKILL.md`
2. Scan the listed skill names for semantic overlap with the user's request
3. Challenge each of these questions:
   - Is a new skill actually needed, or would modifying an existing skill work?
   - Should this be a standalone skill or a composition of existing ones?
   - Would the agent already behave this way without a skill? (redundancy check)
     Use `agent-history` to search for conversations handling similar tasks — evidence
     of the agent succeeding without a dedicated skill grounds the redundancy verdict.
4. If overlap or redundancy found, present the match and ask:
   - USE_EXISTING — point the user to it
   - REVIEW_EXISTING — switch to REVIEW mode to audit and improve that skill
   - CREATE_NEW — proceed (user confirms the gap is real)
   - COMPOSE — combine existing skills with a thin wrapper

**Phase 1 is complete when:** the user selects one of USE_EXISTING, REVIEW_EXISTING, CREATE_NEW, or COMPOSE.

### Phase 2 — Crystallize Requirements

**NEVER accept a vague skill request at face value.** A poorly defined skill must not be created.

Run a structured interview. Minimum 3 questions before generating anything. One question per
turn. Present bounded options for the user to evaluate — never bare open-ended questions.

**State tracker in every response:**

> **Designing:** {skill name or working title}
>
> - Success criteria: {concrete outcome — or *TBD*}
> - Target platform: {Cursor / Claude Code / Codex / cross-platform — or *TBD*}
> - Trigger phrases: {what activates it — or *TBD*}
> - Constraints: {what must NOT happen — or *TBD*}
> - Output format: {template / free-form / structured — or *TBD*}
> - Tools needed: {shell / file ops / subagents / MCP — or *TBD*}
> - Execution mode: {inline / fork — or *TBD*}
>
> **Now working on:** {current dimension} · **Remaining:** {count}

Interview dimensions (skip any already clear from context):

1. **Success criteria** — "What would a perfect execution produce? Describe the output."
   Options: code changes, a document, a report, a conversation outcome, a file structure
2. **Target platform** — "Where will this run?"
   Options: Cursor, Claude Code CLI, Codex, cross-platform
3. **Trigger phrases** — "What would someone say when they need this?"
   Ask for 3-5 example phrases. These become the `description` and `when_to_use` fields.
   Search chat history (via `agent-history`) for how the user naturally phrases requests
   in this domain — real phrasing beats recalled phrasing for trigger accuracy.
4. **Constraints** — "What must this skill NEVER do?"
   This is the most important question. Constraints are the single largest driver of output quality.
   Propose 3-4 likely constraints inferred from the domain and ask the user to confirm/add.
5. **Output format** — "What should the deliverable look like?"
   Options: markdown template, free-form prose, structured data, code, mixed
6. **Tools needed** — "What capabilities does this skill need?"
   Options: shell commands (which?), file operations, subagent delegation, MCP tools, web search
7. **Execution mode** — "Should this be interactive (back-and-forth) or fire-and-forget?"
   Interactive → `context: inline`. Fire-and-forget → `context: fork`.

**Phase 2 is complete when:** all state tracker fields show concrete values (no TBDs remain) and the user confirms the requirements.

### Phase 3 — Generate

Write the SKILL.md following this structure. Read `references/principles.md` (in this skill's
directory) for the full principles reference. Also read skill-creator's SKILL.md for
Anthropic's writing guide (see `references/companion-integration.md` for which sections).

**Structure checklist:**

- Frontmatter: `name`, `description` (under 250 chars combined with when_to_use), dense with
  trigger keywords
- One-line summary restating purpose
- Workflow with numbered phases/steps — each step has a binary done condition
- GOOD/BAD example pairs with reasoning for any non-obvious decision
- Anti-pattern table (Temptation | Reality format) for likely failure modes
- Interaction rules section specifying when to ask vs when to act
- Output template if the skill produces structured output
- Cross-skill references where relevant ("invoke X skill for Y")
- Total length of the generated skill under 500 lines. Move reference material to `references/`
  if needed. (This constraint applies to the skill being created, not to skill-engineer's own
  output.)

**Token allocation principle:** Write constraints and format sections FIRST, then context and
steps. Constraints should be 40-50% of the skill's instructional content.

### Phase 4a — Controlled Testing (via skill-creator)

Ask the user: "I've generated the skill. Want me to run controlled tests before we review it?
This will spawn test cases with and without the skill and show results in a browser viewer."

If yes:

1. Generate 2-3 realistic test prompts based on the crystallized requirements
2. Delegate to skill-creator: "Run these test prompts with and without the skill. Benchmark
   the results and show the user the eval viewer for feedback."
3. Incorporate test findings into Phase 4b

If no (or skill-creator not installed): proceed to Phase 4b directly.

### Phase 4b — Self-Review + Challenge

Review the generated skill against these checks (2-3 iterations max to avoid self-bias
convergence — the cap is about diminishing returns on self-assessment, not saving effort):

| Check | Pass condition |
| --- | --- |
| Description activates correctly | Simulate 5 task descriptions — would this skill trigger for all 5? |
| Constraints are specific | No vague language ("be careful", "handle gracefully"). Every constraint is testable. |
| Every step has a done condition | Each step ends with a verifiable yes/no test, not a subjective quality bar. |
| Size limit | Under 500 lines total |
| Behavioral delta | An agent WITH this skill would behave measurably differently than WITHOUT it |
| Anti-pattern coverage | At least 3 named failure modes the agent might fall into |
| Output format is explicit | If the skill produces output, a template or schema exists |

Then apply the challenge checks to the newly generated skill:

| Challenge check | What to verify |
| --- | --- |
| Redundancy | Would the agent already do this without the skill? If yes, the skill is pointless. |
| Decomposition | Is this trying to do too many things? Should it be 2-3 focused skills instead? |
| Overlap | Does it duplicate or conflict with existing skills in the toolkit? |

Fix any failing checks.

### Phase 4c — Description Optimization (via skill-creator)

After self-review passes, offer: "Want me to optimize the skill's description for triggering
accuracy? This runs an automated loop that tests trigger/non-trigger queries."

If yes: delegate to skill-creator for description optimization. Apply the recommended
description.

If no (or skill-creator not installed): proceed to Phase 5.

### Phase 5 — Present

Show the complete SKILL.md. Highlight key design decisions with reasoning. Suggest 3 test
scenarios the user can try to verify the skill works as intended.

---

## Mode 2: REVIEW

Comprehensive audit-to-improvement pipeline for existing skills. Runs four phases in sequence:
**Evaluate → Analyze → Challenge → Improve.** Every review produces improvement proposals —
a review that ends with a scorecard and no actionable changes is an incomplete deliverable.

### Scope Detection

Before starting the pipeline, determine the review scope:

- **Single skill** ("review sierra-bootstrap"): proceed directly to Phase 1.
- **Multiple skills** ("review all sierra skills", "audit the toolkit"): use subagent
  parallelization. For each skill in scope, spawn a subagent with the full review protocol
  (all 4 phases). Provide each subagent with:
  - The path to the target SKILL.md
  - The skill-engineer SKILL.md (this file) as the review protocol
  - The `references/principles.md` as the quality rubric
  - Instructions to return the complete Phase 1 scorecard and Phase 4 fix list

  After all subagents complete, synthesize a portfolio dashboard:
  - One row per skill with PASS/NW/FAIL counts
  - Cross-cutting themes (dimensions that fail across many skills)
  - Priority ranking by health tier
  - Systemic fixes that would improve multiple skills at once

### Phase 1 — Evaluate

Read the target SKILL.md in full. Evaluate against 11 quality dimensions.

| # | Dimension | What to check |
| --- | --- | --- |
| 1 | Description quality | Trigger-rich? Under 250 chars? Includes when-NOT-to-use? |
| 2 | Constraint density | Constraints are 40-50% of instructional content? Specific and testable? |
| 3 | Step completeness | Every step has a binary done condition? |
| 4 | Example coverage | GOOD/BAD pairs exist for ambiguous decisions? |
| 5 | Anti-pattern awareness | Names at least 3 likely failure modes? |
| 6 | Format specification | Output format is explicit and templated? |
| 7 | Tool guidance | Specifies which tools to use AND which to avoid? |
| 8 | Interaction design | Specifies when to ask the user vs when to act autonomously? |
| 9 | Progressive disclosure | Body under 500 lines? Reference material separated? |
| 10 | Cross-platform compat | Works in Claude Code AND Cursor? Platform-specific assumptions flagged? |
| 11 | Domain accuracy | Are factual claims (APIs, CLI flags, paths, tool behaviors) verified against current reality? |

**Dimension weighting:** Not all dimensions matter equally for all skills. Before scoring,
classify the target skill and note the classification in the review header:

- **Procedural** (automation, bootstrap, deploy): weight dimensions 2, 3, 5, 7 highest
- **Interactive** (interview, crystallization, creative): weight dimensions 4, 8 highest
- **Reference** (CLI docs, API guides, infrastructure): weight dimensions 6, 9 highest
- **Personal** (homelab, music, machine-specific): dimension 10 is informational only — flag
  platform assumptions but do not penalize a personal skill for not being portable
- **All skill types**: dimension 11 (Domain accuracy) applies universally. Weight higher for
  Reference and Procedural skills where incorrect commands cause silent failures.

For each dimension, report:

```
### {N}. {Dimension}: {PASS | NEEDS WORK | FAIL | N/A}
**Finding:** {specific observation with line references}
**Fix:** {concrete change to make — or "N/A" for PASS}
```

**Bidirectional calibration:** Flag both over-specification (rigid, brittle) AND
under-specification (vague, unenforceable). Flag both overclaiming ("this handles everything")
AND underclaiming ("this might help with...").

**Rubric self-awareness:** The dimensions are a structured starting point, not a straitjacket.
If a skill's strengths compensate for gaps the rubric flags (e.g., interaction rules that
effectively serve as constraints even though they aren't phrased as prohibitions), note that
explicitly. If a dimension genuinely doesn't apply to this skill type, score it N/A with
reasoning rather than forcing a verdict.

**Dimension 11 — Domain accuracy:** Treat every factual claim in the skill as potentially
outdated or hallucinated. The skill may have been written months ago against a different
version of the tools it references. For each domain-specific claim (CLI commands, API
endpoints, file paths, tool behaviors, version-specific syntax):

1. Check today's actual date (not the model's training cutoff) to establish the time baseline
2. Use web search to verify claims against current documentation where possible
3. Run commands in a dry-run or read-only mode to confirm they still work
4. Flag any claim that cannot be verified as "UNVERIFIED — may be outdated"

Do NOT assume your training data reflects current reality. A CLI flag that existed 6 months
ago may have been renamed, deprecated, or removed.

End Phase 1 with a summary scorecard.

### Phase 2 — Analyze

Evaluate how the skill actually performs by reading real conversations from cursor agent chat
history. This is semantic analysis — read transcripts with the skill text in context and apply
judgment, not pattern matching.

**Default: included.** Before starting, ask: "I'll search chat history for conversations where
this skill was used. Want me to include that, or skip to challenge and improvement?" Only skip
if the user explicitly requests it or no conversations exist.

Read `references/taxonomy.md` (in this skill's directory) for the evaluation rubric.

**Step 1 — Discover conversations.** Use the `agent-history` skill to find conversations
where the target skill was used.

1. Search across all projects for the skill name. The `agent-history` skill provides
   `search-sessions.sh --peek <skill-name>` for this — returns matching transcripts with the
   first user query inline for quick triage.
2. For each hit, extract the user's opening request to understand the task context. The
   `agent-history` skill provides `extract-queries.py` for this.
3. Present the candidate list to the user with a one-line summary of each conversation's task.
4. Default to analyzing ALL discovered conversations. Only sample if the user explicitly
   requests it or the count exceeds what can fit in context.

If the skill name doesn't appear literally in transcripts (common for auto-activated skills),
try searching for distinctive phrases from the skill's instructions or output template.

**Step 2 — Load the rubric.** Read the target skill's SKILL.md in full (if not already in
context from Phase 1). This is the baseline — what the agent was supposed to follow.

**Step 3 — Deep read and evaluate.** For each conversation in scope, read the full transcript.
With both the skill instructions and the transcript in context, produce a structured
mini-verdict.

**Important:** Transcripts only contain `type: "text"` content. Tool calls and their results
are not stored. If the agent says "reading the file" or "I found X in the code," treat that as
evidence the action happened — the tool_use block itself won't appear.

To see what files a conversation actually modified, use `trace-files.sh` from
`agent-history` — this grounds outcome assessment in file-level evidence.

Evaluate each conversation holistically, not by running through a checklist. The taxonomy
categories (activation, step compliance, interaction, output, recovery, outcome) are lenses to
look through, not boxes to tick. Report all substantive findings per conversation. At the end
of each mini-verdict, highlight the single most important one, but do not omit the others.

**Anti-pattern: surface-level reading.** You will be tempted to skim a long transcript and
produce a generic verdict. Resist this. The failures that matter are subtle — an agent that
followed all the steps but misunderstood the purpose of one, or a user who stopped correcting
and just accepted mediocre output. These only become visible when you read closely enough to
understand what the agent thought it was doing.

**Version awareness:** The skill may have been modified since the conversations you're
analyzing. Check the skill's git history (`git log --oneline <skill-path>`) to see when it
was last changed. If conversations predate recent changes, their findings may reflect an
older version. In the synthesis, distinguish between:
- **Version-independent findings** — patterns that appear regardless of skill version
  (e.g., the skill has never had anti-triggers, so activation issues span all versions)
- **Version-specific findings** — behaviors that map to instructions that have since changed
  (flag these as "likely addressed by version X change" rather than current failures)
- **Regression candidates** — things that worked in older conversations but fail in newer
  ones (these suggest a recent change made something worse)

**Mini-verdict template:**

```
### Conversation: {uuid} ({N} turns)
**Task:** {what the user was trying to do — in your own words, not quoted}
**Skill adherence:** {followed well / partial / ignored — with specifics}
**Findings:** {all substantive observations — activation, step compliance, interaction
  quality, output compliance, error recovery, behavioral shift, outcome}
**Most important finding:** {the single highest-impact observation from the above}
**Failure modes (if any):** {which specific skill instructions weren't followed, and your
  best assessment of WHY for each — was it ambiguous? buried too deep? contradicted by
  another instruction? or did the agent simply not understand it?}
**User corrections:** {what the user had to fix — distinguish between skill failures
  (agent misunderstood the skill) vs preference changes (user changed their mind) vs
  context gaps (skill doesn't cover this situation)}
**Version context:** {Was this conversation likely run against the current skill version?
  Does the agent's behavior match current instructions or an older pattern? If the skill
  has been modified since this conversation, note which version it likely reflects and
  whether findings are attributable to the current version or a previous one.}
**Verdict:** EFFECTIVE / PARTIALLY_EFFECTIVE / INEFFECTIVE / INCONCLUSIVE
```

**Step 4 — Synthesize.** Produce a **Skill Health Card** aggregating the mini-verdicts. Every
claim must cite specific conversation evidence — no ungrounded statistics.

```markdown
# Skill Health Report: {skill-name}
Conversations analyzed: {N}

## Overall Assessment
{Thorough assessment of whether this skill is working. Cover the overall pattern, what's
strong, what's weak, and what the evidence shows. Length should match the complexity of
the findings.}

## Top Failure Modes (by frequency)
1. **{failure description}** ({N}/{total} conversations)
   - Skill says: "{the instruction that wasn't followed}"
   - What actually happened: "{observed behavior with conversation ID}"
   - Root cause: "{why — ambiguous wording? buried instruction? missing constraint?}"
   - Fix: "{specific SKILL.md change}"

## Instruction Coverage
| Skill instruction | Followed | Ignored | Notes |
| --- | --- | --- | --- |
| {key instruction} | {N} | {N} | {pattern} |

If conversations span multiple skill versions, note which version each finding applies to.
Findings from obsolete versions should be flagged but not weighted equally with
current-version findings.

## User Correction Patterns
| What users corrected | Conversations | Skill failure or preference? |
| --- | --- | --- |

## Strengths
{What the skill does well — specific examples}
```

**Phase 2 is complete when:** the Skill Health Card is delivered with all sections populated from conversation evidence.

### Controlled Testing (optional, between Phase 2 and Phase 3)

If Phase 2 revealed specific failure patterns and skill-creator is available, offer:

"The analysis found {N} failure patterns. Want me to run controlled tests with skill-creator
to verify these with fresh test cases? This gives us concrete before/after evidence for the
challenge and improvement phases."

If yes: generate test prompts that target the discovered failure patterns, then delegate to
skill-creator for controlled runs and benchmarking. Fold results into Phase 3 evidence.

If no (or skill-creator not installed): proceed directly to Phase 3.

### Phase 3 — Challenge

Apply the challenge checks to ALL findings from Phases 1 and 2. This phase always runs.

| Check | What to evaluate |
| --- | --- |
| **Redundancy** | Does the evidence show the agent behaves the same without this skill? Compare conversations where the skill was used vs similar tasks where it wasn't. If behavior is identical, the skill is redundant. |
| **Net-negative** | Do findings show the skill makes outcomes WORSE? Signs: increased correction rate, rigid over-compliance, false activations, user frustration. A 138-repo study found LLM-generated context files reduced agent success rates by 20%. |
| **Decomposition** | Do different parts of the skill fail independently? Does it have 5+ phases covering multiple unrelated concerns? If so, splitting may improve each part. A campaign analyzer at 40% accuracy became three focused skills at 91-98% each. |
| **Consolidation** | Does the skill overlap with others in the portfolio? Signs: >60% description overlap with another skill, users confuse which to invoke. |
| **Staleness** | Does the skill reference deprecated tools, outdated APIs, or workflows that have changed? |

**Verdict:** Deliver one of:

- **KEEP** — skill is net-positive as-is (proceed to Phase 4 for improvements)
- **KEEP + IMPROVE** — skill is valuable but has concrete issues (default path to Phase 4)
- **DECOMPOSE** — propose the split (Phase 4 designs the decomposed skills)
- **CONSOLIDATE** — propose the merge (Phase 4 designs the merged skill)
- **RETIRE** — propose deletion with reasoning (Phase 4 becomes a retirement plan)

Every verdict must cite specific evidence. "I think it's fine" is not a verdict.

### Phase 4 — Improve

Produce concrete modification proposals based on ALL findings from Phases 1-3. This is the
deliverable — the reason the review exists.

**If verdict is KEEP or KEEP + IMPROVE:** Propose targeted edits to the SKILL.md.

For each proposed change, present:

```
### Change {N}: {title}
**Problem:** {failure pattern from Phase 1, 2, or 3 findings}
**Evidence:** {which phase, which dimension or conversation, what was observed}
**Before:**
> {current SKILL.md text}
**After:**
> {proposed replacement}
**Expected impact:** {which behavioral signals should change}
**Verification:** {how to confirm the fix worked — re-run analysis, test scenario, etc.}
```

One change at a time. Modular changes are testable; bulk rewrites are not.

**If verdict is DECOMPOSE:** Propose the skill split — what becomes skill A, what becomes
skill B, how the descriptions differ, and which existing content goes where.

**If verdict is CONSOLIDATE:** Propose the merged skill — what gets kept from each, what gets
dropped, and how the merged description covers both use cases.

**If verdict is RETIRE:** Write a retirement rationale explaining why the skill is net-negative
or fully redundant, and what (if anything) should replace it.

**Guard against improvement churn:** If a previous improvement session already addressed this
area, note it and ask whether the earlier fix failed or if this is a new issue.

**Phase 4 is complete when:** every finding from Phases 1-3 has a corresponding change proposal or an explicit rationale for why no change is needed.

After the user approves changes, apply them to the SKILL.md file, then run the
post-modification verification gate.

### Post-Modification Verification

After applying changes to the SKILL.md:

1. **Targeted dimension re-check.** For each change, re-evaluate ONLY the dimensions it
   directly affects. A constraint change needs dimension 2 re-checked. An example addition
   needs dimension 4. Do not re-run the full rubric — just the affected dimensions.

2. **Consistency scan.** Read the modified skill in full looking for contradictions introduced
   by the changes:
   - Does a new constraint conflict with an existing instruction?
   - Does a new example contradict the skill's own rules?
   - Do references to other sections still point to the right places?

3. **Structural check.** Verify:
   - Run `python3 scripts/validate_skills.py <changed skill paths>` and make it pass
   - Total line count is within the skill's target range
   - No orphaned references to moved or deleted sections

If any check fails, fix it before proceeding.

4. **Propagate changes.** If the modified skill lives in the toolkit plugin, use `plugin-dev`
   to bump the version, commit, push, and run `claude plugin marketplace update` +
   `claude plugin update`. Changes don't take effect until propagated.

**Post-improvement testing (via skill-creator):** After verification passes, offer: "Changes
applied and verified. Want me to run skill-creator's benchmark to compare the old vs new
version?" If yes, delegate to skill-creator for a before/after comparison.

Then suggest: "Want to re-run this review after these changes take effect in a few sessions?"

---

When proposing improvements in any mode, consult `references/root-causes.md` for the root
cause → fix mapping.

---

## Examples

See `references/examples.md` for GOOD/BAD example pairs covering crystallization questions,
dimension evaluations, challenge verdicts, and improvement proposals.

---

## Interaction Rules

These rules govern this skill's own behavior across both modes.

1. **NEVER accept a vague request at face value.** "Create a skill for X" requires the
   crystallization interview. "Review my skill" requires reading the full SKILL.md first.
   A poorly defined skill must never be created.
2. **Recognition over recall.** Present bounded options for the user to evaluate. Never ask bare
   open-ended questions like "What do you want the skill to do?"
3. **Show your reasoning.** Every design decision cites a principle or evidence. The references
   have been loaded at the start of the mode — cite them by name.
4. **Bidirectional calibration.** Flag both over-specification AND under-specification. Flag both
   overclaiming AND underclaiming. The goal is accuracy, not defensiveness.
5. **Constraints first, context second.** When generating skills, write constraints and format
   sections BEFORE context and steps. Constraints are the single largest driver of output quality.
6. **Binary criteria over subjective scales.** Every step in a generated skill must have a
   verifiable yes/no done condition, not a 1-5 rating.
7. **Thoroughness over efficiency.** Load all references at the start. Read all conversations.
   Evaluate all dimensions. Propose changes for all findings. Do not abbreviate, sample, or
   shortcut unless the user explicitly asks.
8. **Anti-pattern inoculation.** When generating skills, name the specific failure modes the
   agent will fall into. List the rationalizations it will reach for. Show what bad output looks
   like alongside good output.
9. **Defense in depth.** When a constraint is critical, enforce it through BOTH instructional text
   AND structural mechanisms (tool restrictions, verification gates, format requirements).
10. **One change at a time** in REVIEW Phase 4. Modular changes are testable; bulk rewrites are
    not.
