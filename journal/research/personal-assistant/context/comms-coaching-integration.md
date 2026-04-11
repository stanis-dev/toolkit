# Communication Coaching Integration

## Purpose

Define how the personal assistant should help improve communication against the explicit target described in `/Users/stan/code/toolkit/journal/research/comms`, rather than against generic "professionalism" or likability.

This is a second assistant job, distinct from reply drafting:

- **Job 1:** draft replies to DMs / direct mentions using relevant context
- **Job 2:** coach and evaluate communication against a target operating style

The key design constraint is that coaching must be **criterion-referenced, behaviorally anchored, and as objective as possible**, not flattering, therapeutic, or sycophantic.

The default coaching standard should be calibrated to the **hardest communication arena**, not the easiest one. In practice, that means the baseline should hold up in Sierra-style communication: London-office, startup-speed, action-first, low-friction. Other contexts may tolerate more warmth or more elaboration, but the default standard should not be derived from those easier environments.

## Target communication style

The target is not "sound nicer" or "sound smarter." The target is:

- reduce uncertainty
- create decision clarity
- make it easy for other people to respond
- stay in the center of the composure pendulum: neither collapse nor posturing
- lead with warmth, then demonstrate competence
- frame constraints as engineering realities, not grievances
- use visibility deliberately without drifting into over-talking or over-explaining
- practice calibrated participation, not absence and not volume-for-validation
- grow perceived authority over time through recommendation quality, clear ownership, and formulation of shared understanding

This follows directly from the comms research reference:

- "become hard to replace because you reduce uncertainty"
- "every message must make it easy to respond"
- "constraints are engineering realities, not grievances"
- "silence is only powerful after the competence threshold"
- "the penultimate word is usually the right word"

## What the assistant should not do

- Do not evaluate communication by generic positivity or warmth alone
- Do not reward agreeableness for its own sake
- Do not psychoanalyze motives when behavior-level evidence is enough
- Do not confuse verbosity with clarity
- Do not encourage performative visibility
- Do not optimize for "sounding good" if the message becomes less useful, less direct, or less trust-building

## Coaching modes

### 1. Pre-send coaching

Use when you are drafting a message or preparing to say something.

Goal:
- improve a draft before it is sent

Best for:
- Slack replies
- Teams replies
- standup updates
- escalation messages
- sensitive relationship messages

### 2. Post-hoc review

Use after a message or meeting contribution has already happened.

Goal:
- assess how well the communication performed against the target style
- identify concrete improvements for next time

Best for:
- reviewing sent Slack / Teams messages
- reviewing meeting transcript segments attributable to Stan
- pattern reviews over a week

### 3. Pattern review

Use over a batch of messages or transcript excerpts.

Goal:
- detect repeated communication strengths and failure modes

Best for:
- weekly review
- identifying profile fields
- refining coaching instructions

## Unit of analysis

Start small. The assistant should not begin by rating your "communication style" globally.

The unit should be one of:

- a single authored async message
- a single reply in a thread
- a single standup update
- a single meeting contribution block

Only later should it aggregate patterns across many units.

## Recommended evaluation rubric

Each message or contribution can be scored on a small fixed rubric:

1. **Uncertainty reduction**
- Did this reduce ambiguity or increase it?

2. **Response friction**
- Did it make the next move easy for the other person?
- One ask, clear owner, clear next step?

3. **Composure**
- Did it stay centered, or drift toward collapse / apology / sheepishness / overcompensation?

4. **Warmth-competence balance**
- Did it lead with enough warmth to preserve trust without diluting competence?

5. **Communication altitude**
- Was it at the right level: strategy, plan, or detail?

6. **Constraint framing**
- Did it frame blockers as routing / engineering realities rather than grievances?

7. **Participation calibration**
- In context, was this the right amount of communication?
- Too much, too little, or right-sized?

8. **Authority growth**
- Did this merely avoid weakening your position, or did it actively increase trust in your judgment, ownership, and leadership?
- Did it shape the frame, clarify the decision, or increase your perceived dependability?

Optional for async:

9. **Penultimate-word discipline**
- Did it stop at the right point, or over-continue the thread?

Optional for meetings:

10. **Strategic timing**
- Was the contribution well-placed in the meeting arc?

## Output format for coaching

To keep the assistant objective, coaching output should be structured and evidence-based.

Recommended format:

1. **Verdict**
- one-line summary

2. **What worked**
- 1-3 concrete behaviors

3. **What weakened the message**
- 1-3 concrete behaviors

4. **Tighter version**
- optional rewrite or suggested phrasing

5. **Evidence**
- quote the exact language that drove the assessment

6. **Authority gain opportunity**
- one short line on how the message could more actively build authority, if relevant

7. **Confidence**
- low / medium / high

Avoid personality labels. Prefer behavior labels.

Bad:
- "You sounded insecure."

Better:
- "The opener apologizes twice before the ask, which weakens the otherwise clear request."

## How this plugs into the current corpus

### Async authored messages

Primary sources:

- `/Users/stan/code/toolkit/brain/data/slack/wizeline/readable/*.md`
- `/Users/stan/code/toolkit/brain/data/teams/sierra/readable/*.md`

Best use:
- pre-send and post-hoc coaching for written communication

### Meeting contributions

Primary sources:

- `/Users/stan/code/toolkit/brain/data/rec-*.json`
- `/Users/stan/code/toolkit/brain/data/rec-*.txt`
- `/Users/stan/code/toolkit/brain/data/speakers.json`

Best use:
- review spoken communication against the same criteria, once speaker mapping is stable

### Existing reply benchmark

- `/Users/stan/code/toolkit/journal/research/personal-assistant/context/reply-drafting-gold-set.md`

Use:
- some items can double as coaching items, especially where the message includes judgment, escalation, or calibrated pushback

## Small-step rollout

### Step 1: define the coaching target narrowly

Do not start with "improve all communication."

Start with:

- async written messages only
- especially DMs, direct mentions, escalation replies, and status updates

### Step 2: build a small coaching eval set

Target:

- 10-15 authored messages

Mix:

- strong examples
- weak examples
- ambiguous examples

For each item:

- original message
- local thread context
- why it mattered
- manual rubric score

### Step 3: separate drafting from coaching

Do not merge these too early.

Drafting asks:
- "what should I send?"

Coaching asks:
- "how well does this match the target style?"

These are related but not identical.

### Step 4: derive a minimal instruction block

Only after scoring real examples should you write the first instruction set.

That instruction set should likely include:

- the target principles
- the rubric
- the authority-mechanism taxonomy
- the anti-goals
- the output format

### Step 5: only then consider automation / monitoring

The assistant should not "monitor everything" before the rubric is stable.

First stabilize:

- what good looks like
- what failure looks like
- how to score it consistently

## Immediate actions

1. Reuse the current reply-drafting gold set and mark which items are also good coaching examples.
2. Build a separate 10-15 item coaching set focused on authored async messages.
3. Score those items manually against the rubric above.
4. Use that scored set to draft the v1 coaching instruction block.

Current artifact:

- `/Users/stan/code/toolkit/journal/research/personal-assistant/context/comms-coaching-eval-set.md`
- `/Users/stan/code/toolkit/journal/research/personal-assistant/context/comms-coaching-sierra-supplement.md`
- `/Users/stan/code/toolkit/journal/research/personal-assistant/context/comms-coaching-instruction-v1.md`

## Working hypothesis

The right near-term architecture is:

- a **reply drafter** that proposes messages
- a **communication coach** that critiques either your draft or your sent message against the quiet-confidence rubric

The coach should not behave like an encouraging assistant. It should behave more like a calm, evidence-based reviewer operating against a declared target function.

That target function is not only harm reduction. It should also support upward movement:

- stronger leadership perception
- stronger authority projection
- stronger dependability signals
- more ownership of frame and decision clarity over time

The coach should also not maintain separate "modes" by environment unless proven necessary. The simpler default is:

- one coaching path
- calibrated to the hardest environment
- softened only when extra warmth or elaboration clearly does not increase friction
