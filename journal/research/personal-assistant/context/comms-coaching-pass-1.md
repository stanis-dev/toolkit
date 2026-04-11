# Communication Coaching Pass 1

First larger-pass synthesis using the current coaching artifacts and the default instruction block.

## Scope

This pass covers **30 authored async messages**:

- 12 items from `/Users/stan/code/toolkit/journal/research/personal-assistant/context/comms-coaching-eval-set.md`
- 10 items from `/Users/stan/code/toolkit/journal/research/personal-assistant/context/comms-coaching-sierra-supplement.md`
- 8 additional Sierra Slack items reviewed in this pass

Overall category mix across the 30 reviewed items:

- **Strong:** 15
- **Ambiguous:** 9
- **Weak:** 6

This is enough for a first directional read. It is not yet a frozen benchmark.

## Additional Sierra items reviewed in this pass

### P01 — Quick-look request on PR is good but a little too softened `[Ambiguous]`
- Source: Sierra Slack DM
- Timestamp: `2026-01-21 10:29`
- Context file:
  - `/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/Daniel_Book.md`
- Message:
  - `hey, i addressed comments from email/sms pr. since changes are not just cosmetic, would appreciate a quick look at it. if all good, we can ship it today`
- Verdict:
  - Clear and useful, but slightly softer than needed for the environment
- What worked:
  - clear object of review
  - explicit urgency via `we can ship it today`
- What weakened it:
  - `would appreciate a quick look` is softer than necessary when action is needed
- Collapse risk:
  - `Medium` — not harmful, but mildly down-rates your own ask
- Tighter version:
  - `hey — i addressed the comments on the email/sms PR. since the changes are not just cosmetic, could you give it a quick look? if all good, we can ship today`
- Confidence:
  - `high`

### P02 — Merge-ready update is strong and appropriately direct `[Strong]`
- Source: Sierra Slack DM
- Timestamp: `2026-02-02 11:28`
- Context file:
  - `/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/Daniel_Book.md`
- Message:
  - `hey. i added a few changes based on your feedback. if that part looks good - it's ready for merge`
- Verdict:
  - Good default behavior for the target style
- What worked:
  - states exactly what changed
  - makes the decision gate explicit
- What weakened it:
  - little to nothing; opener could be slightly crisper
- Collapse risk:
  - `Low`
- Tighter version:
  - `hey — i added a few changes based on your feedback. if that looks good on your side, it's ready to merge`
- Confidence:
  - `high`

### P03 — Canceling an unnecessary sync is excellent low-friction behavior `[Strong]`
- Source: Sierra Slack DM
- Timestamp: `2026-02-02 16:48`
- Context file:
  - `/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/Daniel_Book.md`
- Message:
  - `all good, everything seems to be working now, so feel free to skip the call`
- Verdict:
  - Very strong: useful, low-drama, and trust-building
- What worked:
  - closes the loop immediately
  - gives time back
  - avoids performative syncing
- What weakened it:
  - nothing meaningful
- Collapse risk:
  - `Low`
- Tighter version:
  - no rewrite needed
- Confidence:
  - `high`

### P04 — Scope-clarification question to Seb is strong `[Strong]`
- Source: Sierra Slack DM
- Timestamp: `2026-03-27 13:45`
- Context file:
  - `/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/Seb_Tranæus.md`
- Message:
  - `to make sure i understand the scope, before release date, in order of priority, we need: 1. fix all requirement sims (must) 2. all sims (must) 3. polish the journey for any obvious rough spots 4. be on the lookout for issues if those come in. does this sound right?`
- Verdict:
  - Strong example of reducing uncertainty upward
- What worked:
  - converts vague expectations into an explicit priority stack
  - easy yes/no validation from the other side
- What weakened it:
  - nothing major
- Collapse risk:
  - `Low`
- Tighter version:
  - no rewrite needed
- Confidence:
  - `high`

### P05 — Phrasing-propagation writeup is technically strong but over-disclaims `[Ambiguous]`
- Source: Sierra Slack DM
- Timestamp: `2026-02-25 16:01`
- Context file:
  - `/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/Seb_Tranæus.md`
- Message excerpt:
  - `Something i believe German told me when I started ... Def don't quote on that - at the time i was drinking information from a firehose, could've easily misinterpreted something. But if that is the intention on the org level - it's important to know that branding != phrasing_instructions`
- Verdict:
  - The technical content is good, but the disclaimer dilutes authority
- What worked:
  - strong technical diagnosis
  - clear propagation matrix
- What weakened it:
  - the self-undercutting disclaimer is broader than needed
- Collapse risk:
  - `Medium`
- Tighter version:
  - `My understanding is that phrasing instructions were expected to live primarily in the journey rather than config, though I may be missing some org-level context. If that is indeed the intended model, it's important to note that branding != phrasing_instructions`
- Confidence:
  - `medium`

### P06 — Alignment note about issue noise is very strong `[Strong]`
- Source: Sierra Slack channel
- Timestamp: `2026-03-03 10:49`
- Context file:
  - `/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/pronet-working-group.md`
- Message excerpt:
  - `I've been triaging issues and it's clear that we can benefit from explicit alignment ... Noise delays action on genuine critical issues`
- Verdict:
  - One of the strongest messages in the corpus
- What worked:
  - names the problem in system terms
  - explains impact from both sides
  - avoids blame
  - creates a clear case for alignment
- What weakened it:
  - little; it is long, but the length is justified by the problem
- Collapse risk:
  - `Low`
- Tighter version:
  - maybe add a one-line executive summary at the top, but otherwise keep
- Confidence:
  - `high`

### P07 — Release update + capacity heads-up is strong `[Strong]`
- Source: Sierra Slack channel
- Timestamp: `2026-03-25 17:20`
- Context file:
  - `/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/pronet-working-group.md`
- Message excerpt:
  - `:pr:to release tomorrow ... Heads-up - at current agent scope, I'm likely to run out of clear work items soon ... I've already flagged availability with Seb, but wanted to surface it here too`
- Verdict:
  - Strong combination of execution update and staffing-risk visibility
- What worked:
  - states shipped work clearly
  - raises utilization risk without dramatizing it
  - signals proactive coordination
- What weakened it:
  - nothing major
- Collapse risk:
  - `Low`
- Tighter version:
  - no rewrite needed
- Confidence:
  - `high`

### P08 — InsertAI clarification is useful but over-qualified `[Ambiguous]`
- Source: Sierra Slack channel
- Timestamp: `2026-03-04 10:43`
- Context file:
  - `/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/pronet-working-group.md`
- Message:
  - `@Daniel Book i wan't present on conversations regarding insert ai call so not sure about the interface. any of these properties look like a good candidate to throw this additional piece of data? Or should I sync with Pronet first?`
- Verdict:
  - Useful question, but more self-qualification than necessary
- What worked:
  - clear technical question
  - asks for the right next routing decision
- What weakened it:
  - `i wasn't present ... not sure about the interface` is more self-positioning than the question needs
- Collapse risk:
  - `Medium`
- Tighter version:
  - `@Daniel Book quick check on insertAI: do any of these properties look like the right place for the additional data, or should I sync with Pronet first?`
- Confidence:
  - `high`

## Main findings

### 1. Your intuition about collapse is directionally right, but too global

The corpus does show real collapse-pattern errors.

But the pattern is **not** "too friendly overall" and not "warmth is bad."

It is much narrower:

- you sometimes lower the urgency of your own ask before anyone else does
- you sometimes add self-undermining commentary after competent work
- you sometimes explain your communication stance instead of just communicating
- you occasionally apologize where a clean state update would have been stronger

That means the intervention should be precise, not personality-wide.

### 2. Warmth is often an asset

Multiple strong items keep warmth without paying a meaningful price:

- Sierra intro to Daniel
- capacity update to Seb
- farewell / coordination messages in the general eval set

So the rule should remain:

- keep warmth when it is low-cost
- remove warmth when it weakens clarity, priority, or authority

### 3. Your strongest messages are unusually good when you switch into system language

The most consistently strong items do one or more of the following:

- convert ambiguity into explicit priority order
- frame blockers as routing problems
- summarize state/action/risk cleanly
- make the next move easy
- avoid defensiveness even when raising uncomfortable truths

This is the real default mode to reinforce.

### 4. The highest-risk failure mode is not friendliness, it is self-undermining clarity

The most costly pattern is not being "too nice."

It is:

- softening a message so much that the action becomes optional
- adding humor or self-deprecation where it makes your own stance look less solid
- talking about your communication process instead of the work state

## What changes after this pass

The current default instruction block is directionally correct.

The main refinements this pass supports are:

1. When uncertain, scope the uncertainty to the **specific claim**, not to your competence globally.
2. In hard contexts, ask directly before adding social cushioning.
3. Do not explain that you "slightly over communicate" or similar; just communicate well.
4. After competent work, avoid self-undermining jokes unless the social upside is clearly worth it.

## Bottom line

Across a 30-message first pass, the default standard should remain:

- action/state/risk first
- one ask / one outcome
- no apology unless actual repair is needed
- warmth preserved only where it stays low-friction
- collapse treated as a **specific behavioral drift**, not as your whole communication identity
