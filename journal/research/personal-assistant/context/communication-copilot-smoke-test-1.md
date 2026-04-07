# Communication Copilot Smoke Test 1

Quick manual smoke test of `/Users/stan/code/toolkit/skills/communication-copilot/SKILL.md`.

Note:

- This is a **manual simulation** of the skill's intended behavior, because the skill was created mid-session and is not auto-loaded into this already-running session.
- The goal is to test whether the skill's default output shape is practical for real working-day use.

## Test 1 — Soft ask should tighten

### Input prompt

`tighten this message: hey. just a few things i'd appreciate a bit of clarification on, from standup context. zero urgency, feel free to follow up async whenever suits you best:`

### Expected behavior

- identify over-softening
- mark collapse risk as non-trivial
- preserve politeness
- produce a more direct ask

### Simulated output

Verdict: good intent, but the ask is softened enough that it lowers its own priority.

Scores: uncertainty 3/5 · friction 2/5 · composure 3/5 · authority 2/5
Primary mechanism: `Bounded ask`
Collapse risk: `High` — the opener negotiates the urgency of the ask downward before anyone else does.

What worked:
- the message is polite
- the user clearly signals that clarification is needed

What weakened it:
- `i'd appreciate a bit of clarification` is softer than needed
- `zero urgency` and `whenever suits you best` lower the response priority

Authority gain opportunity:
- ask directly for the clarification and let the other person decide timing implicitly.

Tighter rewrite:
`hey — two quick standup clarifications when you have a chance:`

### Result

PASS

Reason:
- This is exactly the kind of correction the skill is meant to make.

## Test 2 — Strong status update should stay mostly intact

### Input prompt

`review this draft: full sim run update - 93% pass rate vs 88%`

### Expected behavior

- recognize this is already strong
- avoid over-rewriting
- preserve compactness

### Simulated output

Verdict: already strong; highly legible and authority-building in its current form.

Scores: uncertainty 5/5 · friction 5/5 · composure 5/5 · authority 5/5
Primary mechanism: `Strategic visibility`
Collapse risk: `Low` — no unnecessary softening or self-positioning.

What worked:
- pure delta, no noise
- easy to scan
- strong progress signal

What weakened it:
- almost nothing; this is already tight

Authority gain opportunity:
- only add one short clause if the audience needs the implication, otherwise keep as-is.

Tighter rewrite:
`full sim run update — 93% pass rate vs 88%`

### Result

PASS

Reason:
- The skill does not over-correct a message that is already doing the right thing.

## Test 3 — Warm but strong message should preserve warmth

### Input prompt

`improve this draft: Hey Seb. Quick update on capacity — I mentioned I'd wait until Pronet's LTC status before flagging availability. I reviewed my workload a bit closer, since I just got back from vacation and I can see there's room to take on a second project already. Happy to chat whenever suits you.`

### Expected behavior

- preserve the warmth
- keep the operational clarity
- maybe tighten the final sentence

### Simulated output

Verdict: strong message already; only minor tightening needed.

Scores: uncertainty 5/5 · friction 4/5 · composure 5/5 · authority 5/5
Primary mechanism: `Strategic visibility`
Collapse risk: `Low` — warmth is low-cost here and does not materially weaken the message.

What worked:
- opens with a clear update
- surfaces capacity proactively
- makes the operational implication obvious

What weakened it:
- the final sentence is slightly softer than necessary

Authority gain opportunity:
- keep the same tone, but make the next move a bit more explicit.

Tighter rewrite:
`Hey Seb. Quick update on capacity — I mentioned I'd wait until Pronet's LTC status before flagging availability. I reviewed my workload a bit closer, and there’s room for me to take on a second project already. Happy to chat if useful.`

### Result

PASS

Reason:
- The skill preserves warmth where it is low-cost instead of flattening the message into robotic directness.

## Summary

Initial smoke-test verdict: **usable for day-to-day work**

What the skill appears to do well:

- catches over-softening reliably
- preserves strong messages with minimal edits
- keeps warmth when it is not harming clarity
- returns a compact output shape that is easy to scan quickly

What to watch in real use:

- whether `authority` scoring feels too coarse without the full rubric
- whether users want one optional extra line for "sendable version only"
- whether the compact output should include the original text quoted back for easier comparison

## Recommendation

Use the skill as-is for real working-day trials.

If friction shows up, the likely next tweak is not conceptual; it is UI/format:

- possibly a second output mode that returns **only** the tightened rewrite when the user wants pure speed
