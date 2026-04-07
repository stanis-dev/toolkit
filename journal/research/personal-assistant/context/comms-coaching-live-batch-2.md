# Communication Coaching Live Batch 2

Second recent-message pass, using the **current default coaching format** end-to-end:

- collapse risk
- primary authority mechanism
- authority gain opportunity

## Scope

This pass reviews **12 recent Sierra-facing authored messages** from March 13 to April 2, 2026.

Selection rule:

- recent real messages
- not benchmark-picked
- biased toward substantive status updates, asks, clarifications, and coordination

Primary sources:

- `/Users/stan/code/rec/data/slack/sierra-ai/channels/D0A576YED50.json`
- `/Users/stan/code/rec/data/slack/sierra-ai/readable/pronet-working-group.md`

Note:

- `D0A576YED50.json` is a Sierra Slack DM whose counterpart is unresolved in the export as `U08U80JMWBU`. That does not affect the communication analysis materially.

## Distribution

- **Strong:** 8
- **Ambiguous:** 4
- **Weak:** 0

Collapse risk distribution:

- **Low:** 8
- **Medium:** 4
- **High:** 0

## Item reviews

### LB2-01 — Recent Sierra DM: options for sim generation `[Strong]`
- Timestamp: `2026-04-01 12:21 UTC`
- Message:
  - `hey - following up on the sim gen script. I have two options: 1. You provide the API token to match your setup 2. I run it through Codex CLI with 5.4-mini with lowest reasoning. no token needed, but higher model + agent mode means temp isn't explicitly controlled, so results may vary from your runs Which do you prefer?`
- Verdict:
  - strong decision-framing message
- What worked:
  - presents explicit options
  - names the tradeoff between the two
  - ends with a direct decision ask
- What weakened the message:
  - the tradeoff sentence is slightly dense for chat
- Collapse risk:
  - `Low` — no self-undermining, no unnecessary softening
- Primary authority mechanism:
  - `Decision framing`
- Authority gain opportunity:
  - tighten the tradeoff explanation into one shorter sentence
- Tighter version:
  - `hey — following up on the sim-gen script. Two options: 1) you provide the API token so I match your setup exactly, or 2) I run it through Codex CLI with 5.4-mini. Option 2 needs no token, but results may vary slightly from your runs. Which do you prefer?`
- Evidence:
  - `I have two options`
  - `Which do you prefer?`
- Confidence:
  - `high`

### LB2-02 — Recent Sierra DM: choosing the agent route and naming a dependency `[Ambiguous]`
- Timestamp: `2026-04-01 13:27 UTC`
- Message:
  - `I'll just use the agent, codex is subscription based anyway. i will need the transcripts, though`
- Verdict:
  - operationally fine, but weaker than it could be
- What worked:
  - makes a decision
  - names the dependency immediately
- What weakened the message:
  - `codex is subscription based anyway` reads as extra justification that the decision does not need
- Collapse risk:
  - `Medium` — not collapse exactly, but mild self-justifying softness
- Primary authority mechanism:
  - `Ownership signal`
- Authority gain opportunity:
  - state the choice and the required dependency without explaining the rationale unless asked
- Tighter version:
  - `I'll use the agent route. I will need the transcripts, though`
- Evidence:
  - `I'll just use the agent`
  - `i will need the transcripts`
- Confidence:
  - `high`

### LB2-03 — Recent Sierra DM: catching unexpected transfer behavior `[Strong]`
- Timestamp: `2026-04-01 14:51 UTC`
- Message:
  - `Hey, there seems to be a large number of intents that are transferring immediately and didn't used to. Is that expected?`
- Verdict:
  - strong clarity anchor
- What worked:
  - quickly identifies the observed behavior change
  - asks the exact validation question
- What weakened the message:
  - nothing important
- Collapse risk:
  - `Low`
- Primary authority mechanism:
  - `Clarity anchor`
- Authority gain opportunity:
  - optionally name one example or scope if the issue becomes contentious
- Tighter version:
  - no rewrite needed
- Evidence:
  - `didn't used to`
  - `Is that expected?`
- Confidence:
  - `high`

### LB2-04 — Recent Sierra DM: brief consequence update after breakage `[Ambiguous]`
- Timestamp: `2026-04-01 14:58 UTC`
- Message:
  - `it broke a few transcript sims and some loop/post-hook. no worries`
- Verdict:
  - useful, but under-specified
- What worked:
  - reports the impact quickly
  - keeps emotional tone low
- What weakened the message:
  - no next step or ownership is stated
  - `no worries` closes off information where more operational detail would help
- Collapse risk:
  - `Medium` — the softener slightly substitutes for clarity
- Primary authority mechanism:
  - `Ownership signal`
- Authority gain opportunity:
  - add what you are doing next or what decision is needed
- Tighter version:
  - `it broke a few transcript sims and some loop/post-hook. I'm checking whether this is expected fallout from the requirement changes or a separate regression`
- Evidence:
  - `it broke a few transcript sims`
  - `no worries`
- Confidence:
  - `medium`

### LB2-05 — Recent Sierra DM: current sims state + sync request `[Strong]`
- Timestamp: `2026-04-02 07:54 UTC`
- Message excerpt:
  - `Morning. Sure • sims are now generally solid, with exception of the following 3 groups: requirements and red team (expected) and some triage ... i first wanted to sync about this`
- Verdict:
  - strong status report with a clear reason to sync
- What worked:
  - starts with overall state
  - distinguishes expected from unexpected failures
  - does not pretend the remaining issue is settled
- What weakened the message:
  - still slightly dense for chat formatting
- Collapse risk:
  - `Low`
- Primary authority mechanism:
  - `Strategic visibility`
- Authority gain opportunity:
  - convert the exceptions into a numbered list if repeated often
- Tighter version:
  - `Morning. Sure — sims are generally solid. Remaining groups: 1) requirements, 2) red team (both expected), and 3) some triage. I solved most of the triage issues, but want to sync on one remaining pattern before I push further`
- Evidence:
  - `sims are now generally solid`
  - `with exception of the following 3 groups`
- Confidence:
  - `high`

### LB2-06 — Recent Sierra DM: ack on holding new requirements `[Strong]`
- Timestamp: `2026-03-31 17:08 UTC`
- Message excerpt:
  - `hey. yeah, was taking a look at the doc since it provides great context for me. ack on holding new reqs off ...`
- Verdict:
  - strong low-friction alignment response
- What worked:
  - acknowledges the instruction immediately
  - explains the useful reason briefly
  - pivots cleanly to the new direction
- What weakened the message:
  - little to nothing
- Collapse risk:
  - `Low`
- Primary authority mechanism:
  - `Authority maintenance`
- Authority gain opportunity:
  - if useful, add one-line restatement of the current priority after the ack
- Tighter version:
  - `got it — I was reviewing the doc because it gives good context, but I’m aligned on holding new reqs off. I’ll stay focused on triage/transcript sims`
- Evidence:
  - `ack on holding new reqs off`
- Confidence:
  - `high`

### LB2-07 — Recent Sierra DM: offer of immediate availability plus work options `[Strong]`
- Timestamp: `2026-03-31 15:04 UTC`
- Message:
  - `hey, Seb. I'm finishing with finding the example for Chris and can jump on whatever. Can keep working on sim pass rate, sim dedup and new reqs in the meanwhile`
- Verdict:
  - strong ownership signal
- What worked:
  - clearly states current state
  - offers immediate capacity
  - names concrete next work options
- What weakened the message:
  - `can jump on whatever` is slightly vague compared to the stronger second sentence
- Collapse risk:
  - `Low`
- Primary authority mechanism:
  - `Ownership signal`
- Authority gain opportunity:
  - replace `whatever` with a more explicit “priority you want next”
- Tighter version:
  - `hey Seb — I’m finishing the example for Chris and then can pick up the next priority. In the meantime I can keep moving on sim pass rate, sim dedup, or new reqs`
- Evidence:
  - `can jump on whatever`
  - `Can keep working on sim pass rate, sim dedup and new reqs`
- Confidence:
  - `high`

### LB2-08 — Recent Sierra DM: request for `--sync-journeys` feature `[Ambiguous]`
- Timestamp: `2026-03-31 08:08 UTC`
- Message:
  - `btw, Daniel was able to turn on a feature for Pronet to use watch with --sync-journeys . if you could do this for sky as well it'd be super helpful`
- Verdict:
  - good ask, slightly over-softened
- What worked:
  - names the precedent
  - asks for a concrete enablement change
- What weakened the message:
  - `it'd be super helpful` is softer than necessary
- Collapse risk:
  - `Medium`
- Primary authority mechanism:
  - `Bounded ask`
- Authority gain opportunity:
  - tighten the ask into a direct enablement request
- Tighter version:
  - `btw, Daniel enabled watch with --sync-journeys for Pronet. Could you enable the same for Sky?`
- Evidence:
  - `if you could do this for sky as well`
- Confidence:
  - `high`

### LB2-09 — Recent Sierra DM: asking for context on PII expiration `[Ambiguous]`
- Timestamp: `2026-03-31 08:05 UTC`
- Message:
  - `morning! yeah, already have a session working on it :wink: could you give me a bit of context on the PII expiration? just so that i don't provide other non-useful examples, especially since agent has been sleeping for about 2 weeks now`
- Verdict:
  - reasonable, but over-explains the reason for the ask
- What worked:
  - states current progress
  - asks for the missing context directly
- What weakened the message:
  - too much explanation around why the context is needed
- Collapse risk:
  - `Medium`
- Primary authority mechanism:
  - `Bounded ask`
- Authority gain opportunity:
  - ask for the context directly and let the need stand on its own
- Tighter version:
  - `morning! already working on it. Could you give me a bit more context on the PII expiration so I use the right examples?`
- Evidence:
  - `just so that i don't provide other non-useful examples`
  - `especially since agent has been sleeping`
- Confidence:
  - `high`

### LB2-10 — Recent Sierra DM: simple pass-rate update `[Strong]`
- Timestamp: `2026-03-30 16:19 UTC`
- Message:
  - `full sim run update - 93% pass rate vs 88%`
- Verdict:
  - excellent compact status signal
- What worked:
  - pure delta
  - no noise
  - highly legible
- What weakened the message:
  - nothing
- Collapse risk:
  - `Low`
- Primary authority mechanism:
  - `Strategic visibility`
- Authority gain opportunity:
  - none needed for this format
- Tighter version:
  - no rewrite needed
- Evidence:
  - `93% pass rate vs 88%`
- Confidence:
  - `high`

### LB2-11 — Recent Sierra DM: full sim run WIP `[Strong]`
- Timestamp: `2026-03-30 15:28 UTC`
- Message:
  - `full sim run wip and might take a while. will let you know if any surprises`
- Verdict:
  - strong low-friction visibility
- What worked:
  - makes the work state legible
  - precommits to the next useful update
- What weakened the message:
  - `wip` is shorthand, but acceptable in this context
- Collapse risk:
  - `Low`
- Primary authority mechanism:
  - `Strategic visibility`
- Authority gain opportunity:
  - if needed, add an ETA once you have one
- Tighter version:
  - `full sim run in progress and may take a while. I’ll let you know if anything surprising shows up`
- Evidence:
  - `will let you know if any surprises`
- Confidence:
  - `high`

### LB2-12 — Recent Sierra DM: PR ready with flakiness caveat `[Strong]`
- Timestamp: `2026-03-30 15:24 UTC`
- Message excerpt:
  - `fyi - PR ready, 46/47 with some flakiness on 6 of those ... the only consistent failure is ...`
- Verdict:
  - strong authority-building status update
- What worked:
  - names readiness
  - quantifies the caveat
  - isolates the truly consistent failure
- What weakened the message:
  - slightly dense, but justified
- Collapse risk:
  - `Low`
- Primary authority mechanism:
  - `Strategic visibility`
- Authority gain opportunity:
  - put the consistent-failure sentence earlier if the audience is very time-constrained
- Tighter version:
  - `fyi — PR ready. Current state is 46/47, with flakiness on 6 cases. The only consistent failure is ...`
- Evidence:
  - `PR ready`
  - `the only consistent failure`
- Confidence:
  - `high`

### LB2-13 — Recent channel update: to-release-tomorrow + scope heads-up `[Strong]`
- Timestamp: `2026-03-25 17:20 UTC`
- Message excerpt:
  - `:pr:to release tomorrow ... Heads-up - at current agent scope, I'm likely to run out of clear work items soon ...`
- Verdict:
  - strong combined execution + capacity signal
- What worked:
  - lists concrete release items
  - raises staffing/utilization risk early
- What weakened the message:
  - none significant
- Collapse risk:
  - `Low`
- Primary authority mechanism:
  - `Strategic visibility`
- Authority gain opportunity:
  - none major; already good leadership-style signaling
- Tighter version:
  - no rewrite needed
- Evidence:
  - `to release tomorrow`
  - `I'm likely to run out of clear work items soon`
- Confidence:
  - `high`

### LB2-14 — Recent channel handoff before vacation `[Strong]`
- Timestamp: `2026-03-13 16:52 UTC`
- Message excerpt:
  - `hey team. since i'll be vacationing until Tuesday 24 - posting an update on state of things in :thread:`
- Verdict:
  - strong artifact-like communication
- What worked:
  - clear handoff posture
  - makes absence safe
  - shows organizational awareness
- What weakened the message:
  - a brief top-line summary could make scanning easier
- Collapse risk:
  - `Low`
- Primary authority mechanism:
  - `Strategic visibility`
- Authority gain opportunity:
  - lead with a one-line executive summary before the detailed thread
- Tighter version:
  - `hey team — I’ll be out until Tuesday 24, so posting a full state-of-play update in thread below`
- Evidence:
  - `posting an update on state of things`
- Confidence:
  - `high`

### LB2-15 — Recent mpdm skip note `[Strong]`
- Timestamp: `2026-04-01 14:02 UTC`
- Message:
  - `hey guys. i'll have to skip today's meeting`
- Verdict:
  - simple, efficient, and right-sized
- What worked:
  - direct
  - no drama
  - enough information for the context
- What weakened the message:
  - none
- Collapse risk:
  - `Low`
- Primary authority mechanism:
  - `Authority maintenance`
- Authority gain opportunity:
  - if the meeting requires handoff, add one line of substitute context; otherwise this is fine
- Tighter version:
  - no rewrite needed
- Evidence:
  - `i'll have to skip today's meeting`
- Confidence:
  - `high`

## Synthesis

### What this pass shows

The updated coaching standard holds up on current real communication.

The recent batch is notably strong. Most messages are already doing one of the authority-building jobs well:

- strategic visibility
- bounded ask
- ownership signaling
- clarity anchoring

### What still needs work

The remaining weakness is not broad collapse. It is **micro-softening**:

- extra justification around why you are asking
- slight urgency downrating
- over-explaining the social reason for the message

### Recommendation

No need to regenerate the live-batch corpus again right now.

The right next move is to keep using this current format and let the coach enforce two defaults:

1. `authority mechanism first`
2. `authority gain opportunity always present`

That will push the coaching system toward upward authority growth from the start, rather than only catching collapse after the fact.
