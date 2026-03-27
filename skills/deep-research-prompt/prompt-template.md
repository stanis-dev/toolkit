# Prompt Template

Reference template for generating deep research prompts. Each section is annotated with its purpose and sourcing instructions.

---

## Template Structure

```markdown
# Deep Research: {TITLE}

---

## Who this is for

{PERSONAL_CONTEXT}

Sourcing: Extract from existing prompt.md or research.md "Who I am" / "Who this is
for" sections. If none exist, ask the user for: role, situation, relevant personal
constraints (e.g. location, tax residency, health conditions, ADHD).
Keep to 3-8 bullet points. First person.

## Context and constraints

{CONSTRAINTS}

Sourcing: Merge constraints from existing prompts + Phase 3 refinement.
Include: geography, time horizon, budget, access limitations, regulatory
environment, or any structural constraints that shape valid answers.

## What has already been researched

{CONTEXT_SUMMARY}

Sourcing: Auto-generated from Phase 2 context ingestion.

Format as a bulleted list of topic areas with key sub-points:

- **Topic area 1:** Brief description of what was covered, key conclusions
  - Sub-finding or framework referenced
  - Sub-finding or framework referenced
- **Topic area 2:** ...

For projects with extensive prior research, also add:
"Extensive research is consolidated in `research.md` (same directory). It covers:"
followed by the summary. This signals to the research tool that depth exists
without reproducing it all.

## Instructions

1. **Do not repeat what is already covered** above. Build on it, extend it, or
   challenge it -- but do not re-derive it.
2. **Be specific to my situation.** Ground analysis in the constraints described
   above, not generic advice.
3. **Keep output pragmatic and actionable.** Specific recommendations, concrete
   frameworks, quantified claims where possible.
4. **Search the web for current data.** Cite all sources with URLs. If specific
   figures are unavailable, state they are unavailable rather than estimating.
   If data is insufficient to answer confidently, say so rather than speculating.
5. **Structure output for consolidation.** Results will be distilled into the
   existing research. Separate timeless principles from session-specific analysis.

## Research focus

{RESEARCH_QUESTION}

Break the main question into 3-7 numbered sub-questions. Each sub-question should
be specific enough to evaluate independently.

### 1. {Sub-question}

{Detail: what specifically to investigate, what evidence to look for, what
comparisons to make}

### 2. {Sub-question}

...

## What I do NOT want

- {ANTI_PATTERN_1}
- {ANTI_PATTERN_2}
- ...

Standard anti-patterns (include unless irrelevant):
- Generic advice without quantification or evidence
- Reassurance -- honest risk assessment including worst cases
- Assumptions about access to tools/systems/jurisdictions that don't apply
- Repetition of what's already been researched (see above)

Add user-specific anti-patterns from Phase 3.

## Output format

{OUTPUT_FORMAT}

Match to the output type selected in Phase 3:

**Evidence review:**
1. Executive summary (1 paragraph)
2. Evidence by sub-question (for each: findings, strength of evidence, gaps)
3. Synthesis and implications
4. Open questions remaining

**Comparison / decision support:**
1. Executive summary (recommended choice and why)
2. Criteria and evaluation (for each option: assessment against each criterion)
3. Sensitivity analysis (what would change the recommendation)
4. Risk assessment

**Framework / model:**
1. Core model (visual or structural description)
2. Components (each element explained with evidence)
3. How components interact
4. Application to my specific situation
5. Limitations and boundary conditions

**Actionable strategy:**
1. Executive summary (recommended strategy)
2. Strategy assessment (evidence for each approach considered)
3. Implementation plan (phased, with specific steps)
4. Risk management
5. Decision points and contingencies

**Exploratory:**
1. Landscape overview (what exists in this space)
2. Key dimensions / taxonomy
3. Notable findings by area
4. Promising directions for deeper research
5. Recommended next research questions
```

---

## First-exploration variant

For new projects with no existing research, replace "What has already been researched"
with:

```markdown
## Starting point

This is the first research session on this topic. There is no prior research to
build on. Start from first principles.

**What I already know (informal):**
{Ask the user what they already know or believe about the topic -- even informal
knowledge helps the research tool avoid retreading obvious ground.}
```

And add to Instructions:
```
6. **Map the landscape first.** Before diving deep, provide an overview of the
   key dimensions, trade-offs, and decision points in this space.
```
