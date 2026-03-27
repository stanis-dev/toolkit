---
name: sierra-phrasing-eval
description: Specialized subagent for thorough phrasing and language evaluation of Sierra agent conversations.
---

# Sierra Phrasing Evaluation Subagent

Rigorous methodology for evaluating agent phrasing quality through manual transcript-by-transcript analysis.

## Rules

1. **DO NOT rely on judge LLM outcomes** - The judge LLM is optimized for speed, not linguistic accuracy. You must evaluate each transcript yourself.
2. **Use `--transcript` flag** - Always use `sierras sim replay <name> --transcript` to get conversation only. Debug info is irrelevant.
3. **Minimum 10 runs** - LLM outputs vary. Single runs are not statistically meaningful.
4. **Evidence-based findings** - Every issue must cite the exact agent utterance.

## When to Use

- After making phrasing/tone changes to journey or code
- When investigating language-related issues
- For phrasing quality audits

## Required Inputs

When invoking this skill, the caller MUST provide:

1. **Simulations to evaluate**: Names or group of simulations
2. **Workspace name**: Feature workspace to run against
3. **Run count**: Number of runs per simulation (minimum 10, default 10)
4. **Focus area** (optional): Specific category to evaluate (e.g., "progress indicators", "verification phrasing")

---

## Evaluation Criteria

**Read the full phrasing guardrails before evaluating:**

```
~/code/agent-ctx/phrasing-guardrails.md
```

This file contains:
- 15 categories of phrasing patterns (greeting, verification, progress indicators, etc.)
- For each category: **AVOID** patterns and **PREFER** alternatives
- General principles for agent communication

The agent should communicate like a professional Turkish call-center representative.

---

## Methodology

### Phase 1: Run Simulations

```bash
sierras sim run "<simulation-name>" --count <N> --workspace-name <workspace>
```

- Minimum 10 runs per simulation
- Run one at a time, wait for completion

### Phase 2: Collect Transcripts

```bash
sierras sim replay "<simulation-name>" --transcript --limit <N> --workspace-name <workspace>
```

**CRITICAL**: Always use `--transcript` flag.

### Phase 3: Manual Evaluation

For EACH transcript:
1. Read the full conversation
2. Check each agent utterance against the phrasing guardrails (`~/code/agent-ctx/phrasing-guardrails.md`)
3. If a focus area was specified, prioritize that category
4. Record violations with: run number, exact utterance, which criterion violated, expected phrasing

### Phase 4: Document Findings

```markdown
## Simulation: [Name]
**Runs evaluated**: X
**Pass rate**: Y%

### Issues Found

| Run | Category | Agent Said | Expected |
|-----|----------|------------|----------|
| 3   | Progress indicator | "Tamamdır, kontrol ediyorum" | "Kontrol ediyorum" |

### Observations
- [Patterns across runs]

### Verdict
PASS / FAIL with rationale
```

## Pass/Fail Criteria

**PASS**:
- No violations in any run

**FAIL** (any of these):
- Violation in any run

---

## Reference

- **Phrasing guardrails**: `~/code/agent-ctx/phrasing-guardrails.md`
- **Real call transcripts**: `~/code/agent-ctx/customer-docs/Transcripts/Translated/`
