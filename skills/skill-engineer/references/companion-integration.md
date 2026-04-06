# Companion Skills Integration

This skill works with **skill-creator** (Anthropic's official plugin) for controlled testing
and benchmarking. If both skills activate on the same request, skill-engineer takes the lead —
skill-creator's creation workflow is subsumed by skill-engineer's CREATE mode, which adds
crystallization, challenge, and quality rubric features on top.

## Division of Labor

- skill-engineer owns the WHAT (requirements, quality standards, challenge, chat history
  analysis, improvement proposals).
- skill-creator owns the HOW TO TEST (subagent test runs, eval viewer, grading, benchmarks,
  description optimization, packaging).

## Integration Points

- After generating a skill (CREATE Phase 4a), delegate to skill-creator for controlled
  test runs and benchmarks.
- After chat history analysis (REVIEW, between Phase 2 and Phase 3), offer controlled
  testing via skill-creator to reproduce discovered failure patterns.
- After proposing improvements (REVIEW Phase 4), delegate to skill-creator for
  before/after comparison of the old vs new skill.
- For description optimization, delegate to skill-creator's automated optimization loop.

## Delegation Guidance

When delegating, describe WHAT you need (e.g., "run these test prompts with and without
the skill, benchmark the results") and let skill-creator handle HOW. Do not reference
skill-creator's internal scripts or file structures — read its SKILL.md for current
implementation details.

## Writing Guide Pointer

When generating a skill (CREATE Phase 3), also read skill-creator's SKILL.md — specifically
the "Skill Writing Guide", "Writing Style", and "Improving the skill > How to think about
improvements" sections for Anthropic's latest guidance on writing patterns and progressive
disclosure.

## Fallback

If skill-creator is not installed, all phases still work — testing becomes manual
(the user tries the skill themselves and reports back).
