# Communication Coaching Live Batch 1

First recent-message pass using the default instruction block from `/Users/stan/code/toolkit/journal/research/personal-assistant/context/comms-coaching-instruction-v1.md`.

## Scope

This pass reviews **18 recent Sierra-facing authored messages** from late February to early April 2026.

Selection rule:

- recent real messages
- not the hand-picked benchmark set
- biased toward substantive updates, asks, clarifications, and coordination

Sources:

- `/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/Seb_Tranæus.md`
- `/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/pronet-working-group.md`
- `/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/Daniel_Book.md`

## Distribution

- **Strong:** 11
- **Ambiguous:** 6
- **Weak:** 1

Collapse risk distribution:

- **Low:** 11
- **Medium:** 6
- **High:** 1

## Item reviews

### L01 — Capacity heads-up to Seb `[Strong | collapse risk: Low]`
- Context:
  - proactive update on availability
- Message:
  - `Hey Seb. Quick update on capacity — I mentioned I'd wait until Pronet's LTC status before flagging availability. I reviewed my workload a bit closer, since I just got back from vacation and I can see there's room to take on a second project already. Happy to chat whenever suits you.`
- What worked:
  - state first
  - clear operational implication
  - low-drama tone
- What weakened it:
  - `Happy to chat whenever suits you` is slightly softer than necessary, but low-cost here
- Verdict:
  - strong default behavior

### L02 — Seb asks what % is free `[Ambiguous | collapse risk: Medium]`
- Context:
  - follow-up to capacity update
- Message:
  - `if LTC comes through I'd expect to have about 40% free. if it doesn't - all of it :disappointed:`
- What worked:
  - direct answer
  - very low response friction
- What weakened it:
  - emotive tail adds color without adding useful information
- Verdict:
  - operationally strong, slightly over-exposed

### L03 — Claude access thanks `[Strong | collapse risk: Low]`
- Context:
  - Seb checked on Claude access
- Message:
  - `hey, thanks for taking the time to look into this! already submitted the request. that's great news`
- What worked:
  - appreciative without being deferential
  - closes the loop cleanly
- What weakened it:
  - nothing meaningful
- Verdict:
  - strong simple reply

### L04 — Early Sky progress ping `[Strong | collapse risk: Low]`
- Context:
  - Seb asks how Sky work is going
- Message:
  - `hey! managed to make some progress and will have the first PR up in a bit`
- What worked:
  - clear status
  - concrete next artifact
- What weakened it:
  - no numbers yet, but reasonable for the stage
- Verdict:
  - strong and appropriately concise

### L05 — Sims pass-rate summary `[Strong | collapse risk: Low]`
- Context:
  - Seb asks what is realistic to wrap up today
- Message:
  - `the tldr is PR gets sims to 1,373 of 1,504 passing(PR) VS 1,158 of 1,504 passing (main) + those sims that are still failing have more conditions passing. The focus was on issues that were affecting several cases at the same time + low hanging stuff`
- What worked:
  - starts with the delta
  - grounded in numbers
  - clear prioritization logic
- What weakened it:
  - a bit dense for chat, but still useful
- Verdict:
  - strong status reporting

### L06 — Requirement-sim answer `[Strong | collapse risk: Low]`
- Context:
  - Seb asks specifically about requirement sims
- Message:
  - `37vs24 out of 47. yeah, the focus was the 47 requirement sims, the total diff is more of a byproduct tbh`
- What worked:
  - direct answer first
  - clarifies what matters
- What weakened it:
  - `tbh` is unnecessary but harmless
- Verdict:
  - strong, low-friction clarification

### L07 — Draft PR already up `[Strong | collapse risk: Low]`
- Context:
  - Seb asks whether Stan can push what he has so far
- Message:
  - `yeah, there's a draft PR already ... i'm mostly working on the description to provide context to the changes`
- What worked:
  - answers the ask immediately
  - names the current bottleneck cleanly
- What weakened it:
  - nothing significant
- Verdict:
  - strong update

### L08 — “almost, yes” on Pronet capacity `[Strong | collapse risk: Low]`
- Context:
  - Seb asks if Stan is 100% free of Pronet
- Message:
  - `almost, yes. we're still doing standups for now to keep Pronet engaged and that spawns minor tasks occasionally`
- What worked:
  - concise
  - precise enough
  - no hedging beyond what is truly needed
- What weakened it:
  - nothing meaningful
- Verdict:
  - strong bounded answer

### L09 — Scope confirmation list `[Strong | collapse risk: Low]`
- Context:
  - Seb is assigning more Sky tasks
- Message:
  - `to make sure i understand the scope, before release date, in order of priority, we need: ... does this sound right?`
- What worked:
  - converts ambiguity into an ordered priority stack
  - very easy to respond to
- What weakened it:
  - none worth calling out
- Verdict:
  - one of the strongest messages in the batch

### L10 — Release + capacity heads-up in `pronet-working-group` `[Strong | collapse risk: Low]`
- Context:
  - channel update
- Message:
  - `:pr:to release tomorrow ... Heads-up - at current agent scope, I'm likely to run out of clear work items soon ... I've already flagged availability with Seb, but wanted to surface it here too`
- What worked:
  - execution state + staffing risk in one place
  - raises the issue before it becomes a problem
- What weakened it:
  - nothing major
- Verdict:
  - strong channel update

### L11 — “Apologies, Sky agent got me busy” `[Ambiguous | collapse risk: Medium]`
- Context:
  - Tom checks if you looked at a lighter analysis task
- Message:
  - `hey tom. apologies, sky agent got me a bit busy :melting_face:` followed by a substantive explanation
- What worked:
  - follow-up content is useful and concrete
- What weakened it:
  - opener apologizes for a normal prioritization tradeoff
- Verdict:
  - fine overall, but opener weakens the message

### L12 — Vacation handoff `[Strong | collapse risk: Low]`
- Context:
  - upcoming vacation
- Message:
  - long threaded update on state, pipeline, and pending alignment
- What worked:
  - strong handoff structure
  - clear separation between shipped state, pending work, and alignment needs
- What weakened it:
  - long, but length is justified
- Verdict:
  - strong artifact-like communication

### L13 — Proposal response to Tom on improvement strategy `[Ambiguous | collapse risk: Medium]`
- Context:
  - Tom asks for a write-up of improvement opportunities
- Message excerpt:
  - `I'd like to hear your thoughts on the strategy. For now, mine is keep bringing up specific issues on standups ... there's also a world where "good enough" is good enough ...`
- What worked:
  - strong strategic decomposition
  - names organizational friction honestly
- What weakened it:
  - closes by slightly down-rating the strategic push with `good enough`
- Verdict:
  - strategically strong, but slightly too self-dampening at the edges

### L14 — Internal alignment note on issue noise `[Strong | collapse risk: Low]`
- Context:
  - issue triage and reviewer alignment
- Message excerpt:
  - `I've been triaging issues and it's clear that we can benefit from explicit alignment ... Noise delays action on genuine critical issues`
- What worked:
  - systems framing
  - explicit consequences
  - no blame language
- What weakened it:
  - could use a one-line summary at the top, but already strong
- Verdict:
  - one of the best examples in the corpus

### L15 — InsertAI interface question `[Ambiguous | collapse risk: Medium]`
- Context:
  - Tom asks about passing a variant into `insertAiCall`
- Message:
  - `@Daniel Book i wan't present on conversations regarding insert ai call so not sure about the interface. any of these properties look like a good candidate ... Or should I sync with Pronet first?`
- What worked:
  - asks the right routing question
- What weakened it:
  - more self-qualification than needed
- Verdict:
  - good technical question, softened by self-positioning

### L16 — “would appreciate some feedback” on IBAN `[Ambiguous | collapse risk: Medium]`
- Context:
  - Stan wants guidance on IBAN readout approach
- Message excerpt:
  - `would appreciate some feedback on IBAN readout implementation idea ... wanted to hear your thoughts first on the approach itself`
- What worked:
  - seeks alignment before overcommitting
- What weakened it:
  - ask is softer and broader than necessary
- Verdict:
  - reasonable, but weaker than the default standard

### L17 — “I generally try to slightly over communicate” `[Weak | collapse risk: High]`
- Context:
  - Tom says he missed some prior context
- Message:
  - `absolutely no worries. i'm aware you're all working on several projects in parallel. i generally try to "slightly over communicate" specifically for that reason :wink:`
- What worked:
  - socially kind
- What weakened it:
  - explains your communication stance instead of just restoring context
  - lowers authority with unnecessary self-positioning
- Verdict:
  - clearest weak pattern in the live batch

### L18 — Action-item pass after standup `[Strong | collapse risk: Low]`
- Context:
  - Tom posts standup notes
- Message excerpt:
  - `Those are all actionable items i can see right now. let me know if there's something else.`
- What worked:
  - converts discussion to owned action
  - cleanly bounds current scope
- What weakened it:
  - little to nothing
- Verdict:
  - strong execution communication

## Synthesis

### What the live batch confirms

The default instruction block is mostly right.

The messages that perform best consistently do the following:

- answer the operational question quickly
- make the next move easy
- convert ambiguity into explicit priorities or states
- stay calm without over-explaining
- raise capacity or risk early, without melodrama

### What the live batch refines

The main failure mode is still **not warmth**.

It is:

- softening your own ask before the other person has even had a chance to react
- adding social or self-explanatory material where the work state is enough
- localizing uncertainty badly, by down-rating yourself instead of the specific unknown

### What seems stronger than expected

Your default in recent Sierra-facing communication is actually fairly strong.

The larger pattern is not "frequent collapse."
The larger pattern is "generally strong, with a recurring over-softening habit in a narrow class of messages."

## Practical takeaway

For live use, the coach should watch especially for three things:

1. Did the opener lower the priority of the message unnecessarily?
2. Did the message explain the work state, or explain *you*?
3. Did uncertainty stay scoped to the actual unknown, or spill into self-undermining language?

If those three checks pass, the rest of your default style is often already close to target.
