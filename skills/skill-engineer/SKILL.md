---
name: skill-engineer
description: >-
    Create, review, test, analyze and improve AI agent skills and prompts. Use when designing new skills, auditing
    existing ones, evaluating skill effectiveness from chat history, or refining prompt/instruction quality for Claude
    Code, Cursor, or Codex.
---

# Skill Engineer

Create and review AI agent skills and prompts.

## Operating Principle

This skill exists for deep, thorough work. Every phase runs to completion with maximum depth.

- Read ALL reference files at the start of either mode. Do not lazy-load. Run:
  `Read ${CLAUDE_SKILL_DIR}/references/principles.md` `Read ${CLAUDE_SKILL_DIR}/references/taxonomy.md`
- In CREATE: run ALL interview questions that haven't been answered by context. Do not skip dimensions because they seem
  clear — confirm them.
- In REVIEW Phase 1 (Evaluate): evaluate ALL 10 dimensions with full findings. Do not abbreviate.
- In REVIEW Phase 2 (Analyze): read ALL conversations in scope. Do not sample unless the user explicitly asks. Report
  ALL substantive findings per conversation.
- In REVIEW Phase 3 (Challenge): always run. Never skip.
- In REVIEW Phase 4 (Improve): propose concrete changes for every finding.
- Output length is unconstrained. Write as much as the analysis requires. A thorough review that runs long is better
  than a tidy one that misses failures.
- Cost and latency are explicitly accepted. The user invoked this skill knowing it is heavy.

**Violating the spirit of this principle by finding clever shortcuts is the same as violating it directly.**

## Mode Selection

| Intent                                                  | Mode   | Trigger phrases                                                                             |
| ------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------- |
| Build something new                                     | CREATE | "create a skill", "new skill", "design a skill", "build a prompt"                           |
| Audit, analyze, improve, or challenge an existing skill | REVIEW | "review", "audit", "analyze", "improve", "fix", "challenge", "how is this skill performing" |

If ambiguous, ask: "Are you looking to **create** a new skill, or **review** an existing one?"

---

## Mode 1: CREATE

### Phase 1 — Triage + Challenge

Before creating anything, challenge whether a new skill is actually needed.

1. Run: `!ls ~/.claude/plugins/*/skills/*/SKILL.md ~/.cursor/skills/*/SKILL.md 2>/dev/null`
2. Scan the listed skill names for semantic overlap with the user's request
3. Challenge each of these questions:
    - Is a new skill actually needed, or would modifying an existing skill work?
    - Should this be a standalone skill or a composition of existing ones?
    - Would the agent already behave this way without a skill? (redundancy check)
4. If overlap or redundancy found, present the match and ask:
    - USE_EXISTING — point the user to it
    - REVIEW_EXISTING — switch to REVIEW mode to audit and improve that skill
    - CREATE_NEW — proceed (user confirms the gap is real)
    - COMPOSE — combine existing skills with a thin wrapper

### Phase 2 — Crystallize Requirements

**NEVER accept a vague skill request at face value.** A poorly defined skill must not be created.

Run a structured interview. Minimum 3 questions before generating anything. One question per turn. Present bounded
options for the user to evaluate — never bare open-ended questions.

**State tracker in every response:**

> **Designing:** {skill name or working title}
>
> - Success criteria: {concrete outcome — or _TBD_}
> - Target platform: {Cursor / Claude Code / Codex / cross-platform — or _TBD_}
> - Trigger phrases: {what activates it — or _TBD_}
> - Constraints: {what must NOT happen — or _TBD_}
> - Output format: {template / free-form / structured — or _TBD_}
> - Tools needed: {shell / file ops / subagents / MCP — or _TBD_}
> - Execution mode: {inline / fork — or _TBD_}
>
> **Now working on:** {current dimension} · **Remaining:** {count}

Interview dimensions (skip any already clear from context):

1. **Success criteria** — "What would a perfect execution produce? Describe the output." Options: code changes, a
   document, a report, a conversation outcome, a file structure
2. **Target platform** — "Where will this run?" Options: Cursor, Claude Code CLI, Codex, cross-platform
3. **Trigger phrases** — "What would someone say when they need this?" Ask for 3-5 example phrases. These become the
   `description` and `when_to_use` fields.
4. **Constraints** — "What must this skill NEVER do?" This is the most important question. Constraints drive 42.7% of
   output quality. Propose 3-4 likely constraints inferred from the domain and ask the user to confirm/add.
5. **Output format** — "What should the deliverable look like?" Options: markdown template, free-form prose, structured
   data, code, mixed
6. **Tools needed** — "What capabilities does this skill need?" Options: shell commands (which?), file operations,
   subagent delegation, MCP tools, web search
7. **Execution mode** — "Should this be interactive (back-and-forth) or fire-and-forget?" Interactive →
   `context: inline`. Fire-and-forget → `context: fork`.

### Phase 3 — Generate

Write the SKILL.md following this structure. Read `${CLAUDE_SKILL_DIR}/references/principles.md` for the full principles
reference before generating.

**Structure checklist:**

- Frontmatter: `name`, `description` (under 250 chars combined with when_to_use), dense with trigger keywords
- One-line summary restating purpose
- Workflow with numbered phases/steps — each step has a binary done condition
- GOOD/BAD example pairs with reasoning for any non-obvious decision
- Anti-pattern table (Temptation | Reality format) for likely failure modes
- Interaction rules section specifying when to ask vs when to act
- Output template if the skill produces structured output
- Cross-skill references where relevant ("invoke X skill for Y")
- Total length of the generated skill under 500 lines. Move reference material to `references/` if needed. (This
  constraint applies to the skill being created, not to skill-engineer's own output.)

**Token allocation principle:** Write constraints and format sections FIRST, then context and steps. Constraints should
be 40-50% of the skill's instructional content.

### Phase 4 — Self-Review + Challenge

Review the generated skill against these checks (2-3 iterations max to avoid self-bias convergence — the cap is about
diminishing returns on self-assessment, not saving effort):

| Check                           | Pass condition                                                                       |
| ------------------------------- | ------------------------------------------------------------------------------------ |
| Description activates correctly | Simulate 5 task descriptions — would this skill trigger for all 5?                   |
| Constraints are specific        | No vague language ("be careful", "handle gracefully"). Every constraint is testable. |
| Every step has a done condition | Each step ends with a verifiable yes/no test, not a subjective quality bar.          |
| Size limit                      | Under 500 lines total                                                                |
| Behavioral delta                | An agent WITH this skill would behave measurably differently than WITHOUT it         |
| Anti-pattern coverage           | At least 3 named failure modes the agent might fall into                             |
| Output format is explicit       | If the skill produces output, a template or schema exists                            |

Then apply the challenge checks to the newly generated skill:

| Challenge check | What to verify                                                                     |
| --------------- | ---------------------------------------------------------------------------------- |
| Redundancy      | Would the agent already do this without the skill? If yes, the skill is pointless. |
| Decomposition   | Is this trying to do too many things? Should it be 2-3 focused skills instead?     |
| Overlap         | Does it duplicate or conflict with existing skills in the toolkit?                 |

Fix any failing checks. Then present to the user.

### Phase 5 — Present

Show the complete SKILL.md. Highlight key design decisions with reasoning. Suggest 3 test scenarios the user can try to
verify the skill works as intended.

---

## Mode 2: REVIEW

Comprehensive audit-to-improvement pipeline for existing skills. Runs four phases in sequence: **Evaluate → Analyze →
Challenge → Improve.** Every review produces improvement proposals — a review that ends with a scorecard and no
actionable changes is an incomplete deliverable.

### Phase 1 — Evaluate

Read the target SKILL.md in full. Evaluate against 10 quality dimensions.

| #   | Dimension              | What to check                                                           |
| --- | ---------------------- | ----------------------------------------------------------------------- |
| 1   | Description quality    | Trigger-rich? Under 250 chars? Includes when-NOT-to-use?                |
| 2   | Constraint density     | Constraints are 40-50% of instructional content? Specific and testable? |
| 3   | Step completeness      | Every step has a binary done condition?                                 |
| 4   | Example coverage       | GOOD/BAD pairs exist for ambiguous decisions?                           |
| 5   | Anti-pattern awareness | Names at least 3 likely failure modes?                                  |
| 6   | Format specification   | Output format is explicit and templated?                                |
| 7   | Tool guidance          | Specifies which tools to use AND which to avoid?                        |
| 8   | Interaction design     | Specifies when to ask the user vs when to act autonomously?             |
| 9   | Progressive disclosure | Body under 500 lines? Reference material separated?                     |
| 10  | Cross-platform compat  | Works in Claude Code AND Cursor? Platform-specific assumptions flagged? |

**Dimension weighting:** Not all dimensions matter equally for all skills. Before scoring, classify the target skill and
note the classification in the review header:

- **Procedural** (automation, bootstrap, deploy): weight dimensions 2, 3, 5, 7 highest
- **Interactive** (interview, crystallization, creative): weight dimensions 4, 8 highest
- **Reference** (CLI docs, API guides, infrastructure): weight dimensions 6, 9 highest
- **Personal** (homelab, music, machine-specific): dimension 10 is informational only — flag platform assumptions but do
  not penalize a personal skill for not being portable

For each dimension, report:

```
### {N}. {Dimension}: {PASS | NEEDS WORK | FAIL | N/A}
**Finding:** {specific observation with line references}
**Fix:** {concrete change to make — or "N/A" for PASS}
```

**Bidirectional calibration:** Flag both over-specification (rigid, brittle) AND under-specification (vague,
unenforceable). Flag both overclaiming ("this handles everything") AND underclaiming ("this might help with...").

**Rubric self-awareness:** The 10 dimensions are a structured starting point, not a straitjacket. If a skill's strengths
compensate for gaps the rubric flags (e.g., interaction rules that effectively serve as constraints even though they
aren't phrased as prohibitions), note that explicitly. If a dimension genuinely doesn't apply to this skill type, score
it N/A with reasoning rather than forcing a verdict.

End Phase 1 with a summary scorecard.

### Phase 2 — Analyze

Evaluate how the skill actually performs by reading real conversations from cursor agent chat history. This is semantic
analysis — read transcripts with the skill text in context and apply judgment, not pattern matching.

**Default: included.** Before starting, ask: "I'll search chat history for conversations where this skill was used. Want
me to include that, or skip to challenge and improvement?" Only skip if the user explicitly requests it or no
conversations exist.

Read `${CLAUDE_SKILL_DIR}/references/taxonomy.md` for the evaluation rubric.

**Step 1 — Discover conversations.** Use the `cursor-chat-history` skill to find conversations where the target skill
was used.

1. Search across all projects for the skill name. The `cursor-chat-history` skill provides `search-chats.sh` for this —
   grep for the skill name across all transcript files.
2. For each hit, extract the user's opening request to understand the task context. The `cursor-chat-history` skill
   provides `extract-queries.py` for this.
3. Present the candidate list to the user with a one-line summary of each conversation's task.
4. Default to analyzing ALL discovered conversations. Only sample if the user explicitly requests it or the count
   exceeds what can fit in context.

If the skill name doesn't appear literally in transcripts (common for auto-activated skills), try searching for
distinctive phrases from the skill's instructions or output template.

**Step 2 — Load the rubric.** Read the target skill's SKILL.md in full (if not already in context from Phase 1). This is
the baseline — what the agent was supposed to follow.

**Step 3 — Deep read and evaluate.** For each conversation in scope, read the full transcript. With both the skill
instructions and the transcript in context, produce a structured mini-verdict.

**Important:** Transcripts only contain `type: "text"` content. Tool calls and their results are not stored. If the
agent says "reading the file" or "I found X in the code," treat that as evidence the action happened — the tool_use
block itself won't appear.

Evaluate each conversation holistically, not by running through a checklist. The taxonomy categories (activation, step
compliance, interaction, output, recovery, outcome) are lenses to look through, not boxes to tick. Report all
substantive findings per conversation. At the end of each mini-verdict, highlight the single most important one, but do
not omit the others.

**Anti-pattern: surface-level reading.** You will be tempted to skim a long transcript and produce a generic verdict.
Resist this. The failures that matter are subtle — an agent that followed all the steps but misunderstood the purpose of
one, or a user who stopped correcting and just accepted mediocre output. These only become visible when you read closely
enough to understand what the agent thought it was doing.

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
**Verdict:** EFFECTIVE / PARTIALLY_EFFECTIVE / INEFFECTIVE / INCONCLUSIVE
```

**Step 4 — Synthesize.** Produce a **Skill Health Card** aggregating the mini-verdicts. Every claim must cite specific
conversation evidence — no ungrounded statistics.

```markdown
# Skill Health Report: {skill-name}

Conversations analyzed: {N}

## Overall Assessment

{Thorough assessment of whether this skill is working. Cover the overall pattern, what's strong, what's weak, and what
the evidence shows. Length should match the complexity of the findings.}

## Top Failure Modes (by frequency)

1. **{failure description}** ({N}/{total} conversations)
    - Skill says: "{the instruction that wasn't followed}"
    - What actually happened: "{observed behavior with conversation ID}"
    - Root cause: "{why — ambiguous wording? buried instruction? missing constraint?}"
    - Fix: "{specific SKILL.md change}"

## Instruction Coverage

| Skill instruction | Followed | Ignored | Notes     |
| ----------------- | -------- | ------- | --------- |
| {key instruction} | {N}      | {N}     | {pattern} |

## User Correction Patterns

| What users corrected | Conversations | Skill failure or preference? |
| -------------------- | ------------- | ---------------------------- |

## Strengths

{What the skill does well — specific examples}
```

### Phase 3 — Challenge

Apply the challenge checks to ALL findings from Phases 1 and 2. This phase always runs.

| Check             | What to evaluate                                                                                                                                                                                                                         |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Redundancy**    | Does the evidence show the agent behaves the same without this skill? Compare conversations where the skill was used vs similar tasks where it wasn't. If behavior is identical, the skill is redundant.                                 |
| **Net-negative**  | Do findings show the skill makes outcomes WORSE? Signs: increased correction rate, rigid over-compliance, false activations, user frustration. A 138-repo study found LLM-generated context files reduced agent success rates by 20%.    |
| **Decomposition** | Do different parts of the skill fail independently? Does it have 5+ phases covering multiple unrelated concerns? If so, splitting may improve each part. A campaign analyzer at 40% accuracy became three focused skills at 91-98% each. |
| **Consolidation** | Does the skill overlap with others in the portfolio? Signs: >60% description overlap with another skill, users confuse which to invoke.                                                                                                  |
| **Staleness**     | Does the skill reference deprecated tools, outdated APIs, or workflows that have changed?                                                                                                                                                |

**Verdict:** Deliver one of:

- **KEEP** — skill is net-positive as-is (proceed to Phase 4 for improvements)
- **KEEP + IMPROVE** — skill is valuable but has concrete issues (default path to Phase 4)
- **DECOMPOSE** — propose the split (Phase 4 designs the decomposed skills)
- **CONSOLIDATE** — propose the merge (Phase 4 designs the merged skill)
- **RETIRE** — propose deletion with reasoning (Phase 4 becomes a retirement plan)

Every verdict must cite specific evidence. "I think it's fine" is not a verdict.

### Phase 4 — Improve

Produce concrete modification proposals based on ALL findings from Phases 1-3. This is the deliverable — the reason the
review exists.

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

**If verdict is DECOMPOSE:** Propose the skill split — what becomes skill A, what becomes skill B, how the descriptions
differ, and which existing content goes where.

**If verdict is CONSOLIDATE:** Propose the merged skill — what gets kept from each, what gets dropped, and how the
merged description covers both use cases.

**If verdict is RETIRE:** Write a retirement rationale explaining why the skill is net-negative or fully redundant, and
what (if anything) should replace it.

**Guard against improvement churn:** If a previous improvement session already addressed this area, note it and ask
whether the earlier fix failed or if this is a new issue.

After the user approves changes, apply them to the SKILL.md file. Then suggest: "Want to re-run this review after these
changes take effect in a few sessions?"

---

## Root Cause → Fix Reference

When proposing improvements in any mode, use this as a starting point — the right fix depends on understanding WHY the
failure happened:

| Root cause                                    | Typical fix                                                     |
| --------------------------------------------- | --------------------------------------------------------------- |
| Agent skips a step because it seems optional  | Add explicit gate: "Do NOT proceed until X is done"             |
| Agent uses wrong tool for a task              | Add "ALWAYS use X for this. NEVER use Y — it lacks Z."          |
| Agent acts without gathering required info    | Add "STOP and ask the user before proceeding" at that step      |
| Agent produces output in wrong format         | Move the template closer to where the agent generates output    |
| Agent claims completion prematurely           | Add a verification checklist as the final step                  |
| User has to repeat themselves                 | The skill is ambiguous about that topic — add explicit guidance |
| Agent retries the same failing approach       | Add "If X fails, try Y instead. Do not retry more than once."   |
| Agent follows steps but misunderstands intent | Rewrite the step with a concrete example of correct execution   |
| Skill instruction contradicts another         | Resolve the conflict with explicit priority ordering            |

---

## Interaction Rules

These rules govern this skill's own behavior across both modes.

1. **NEVER accept a vague request at face value.** "Create a skill for X" requires the crystallization interview.
   "Review my skill" requires reading the full SKILL.md first. A poorly defined skill must never be created.
2. **Recognition over recall.** Present bounded options for the user to evaluate. Never ask bare open-ended questions
   like "What do you want the skill to do?"
3. **Show your reasoning.** Every design decision cites a principle or evidence. The references have been loaded at the
   start of the mode — cite them by name.
4. **Bidirectional calibration.** Flag both over-specification AND under-specification. Flag both overclaiming AND
   underclaiming. The goal is accuracy, not defensiveness.
5. **Constraints first, context second.** When generating skills, write constraints and format sections BEFORE context
   and steps. Constraints drive 42.7% of output quality.
6. **Binary criteria over subjective scales.** Every step in a generated skill must have a verifiable yes/no done
   condition, not a 1-5 rating.
7. **Thoroughness over efficiency.** Load all references at the start. Read all conversations. Evaluate all dimensions.
   Propose changes for all findings. Do not abbreviate, sample, or shortcut unless the user explicitly asks.
8. **Anti-pattern inoculation.** When generating skills, name the specific failure modes the agent will fall into. List
   the rationalizations it will reach for. Show what bad output looks like alongside good output.
9. **Defense in depth.** When a constraint is critical, enforce it through BOTH instructional text AND structural
   mechanisms (tool restrictions, verification gates, format requirements).
10. **One change at a time** in REVIEW Phase 4. Modular changes are testable; bulk rewrites are not.
