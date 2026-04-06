# Examples

GOOD/BAD pairs for skill-engineer's key decision points.

---

## Crystallization Question (CREATE Phase 2)

### GOOD

> "What must this skill NEVER do? Based on the domain, I'd expect constraints like:
> (a) never modify files outside the target directory, (b) never skip the dry-run step,
> (c) never assume the user wants destructive operations. Which of these apply? Any others?"

Reasoning: Bounded options with domain-inferred defaults. The user evaluates and selects
rather than generating constraints from scratch. Follows Rule 2 (recognition over recall).

### BAD

> "What constraints should the skill have?"

Reasoning: Bare open-ended question. Forces the user to generate constraints from nothing.
Violates Rule 2. The agent has enough domain context to propose likely constraints — asking
the user to do the generative work is lazy.

---

## Dimension Evaluation (REVIEW Phase 1)

### GOOD

> ### 4. Example Coverage: FAIL
> **Finding:** The skill requires "structured output" (line 47) but provides no example of
> what structured output looks like. Lines 50-55 describe the format in prose ("use headers,
> include a summary") but a single concrete example would eliminate ambiguity.
> **Fix:** Add a GOOD example showing a complete structured output block after line 55.

Reasoning: Cites specific lines. Names what's missing and why it matters. The fix is
actionable — it says WHERE to add WHAT.

### BAD

> ### 4. Example Coverage: NEEDS WORK
> **Finding:** Could use more examples.
> **Fix:** Add examples.

Reasoning: No line references, no specifics. "Could use more" is not a finding. The fix is
unactionable — add WHICH examples WHERE? This verdict would pass the template check but
fail the substance check.

---

## Challenge Verdict (REVIEW Phase 3)

### GOOD

> ### Redundancy: NOT REDUNDANT
> Without this skill, an agent asked to "bootstrap a workspace" would create the directory
> and stop. The skill adds: branch naming convention, Linear ticket creation, simulation
> gap analysis, and issue-context fetch — none of which are default agent behaviors.
> Evidence: conversations abc123 and def456 both show the agent performing all 4 steps
> that wouldn't occur without the skill.

Reasoning: Cites specific behaviors the skill adds. References conversation evidence.
The verdict is grounded in observable behavioral delta.

### BAD

> ### Redundancy: NOT REDUNDANT
> This skill seems useful and does things the agent wouldn't do on its own.

Reasoning: No specific behaviors cited. No evidence referenced. "Seems useful" is not
a finding. An agent producing this verdict has skipped the actual analysis.

---

## Improvement Proposal (REVIEW Phase 4)

### GOOD

> ### Change 1: Add skip condition to Phase 2 interview
> **Problem:** Agent asks for target platform even when the user's message says "for my
> Cursor setup" (conversations abc123, ghi789).
> **Evidence:** Phase 2, dimension 8; conversations abc123 turn 3, ghi789 turn 2.
> **Before:**
> > 2. **Target platform** — "Where will this run?"
> **After:**
> > 2. **Target platform** — "Where will this run?" Skip if the user already named a
> >    platform in their request.
> **Expected impact:** Eliminates redundant questions when platform is stated upfront.

Reasoning: Traces from evidence (specific conversations) to problem to fix. The change
is minimal, scoped, and testable.

### BAD

> ### Change 1: Improve the skill
> **Problem:** The skill could be better.
> **Fix:** Rewrite the whole thing.

Reasoning: No evidence, no specificity, no before/after. "Rewrite the whole thing"
violates the one-change-at-a-time principle and is untestable.
