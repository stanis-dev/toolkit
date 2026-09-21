# Sims

- Sims get value-checked at two points: the issue card's sim-strategy step, and a sim review.

- When should a scenario be tested with different persona.
- good: pass criteria comparison will find same evaluations, but not necessarily same scenario.
- criteria - when is it tight enough, not lose nor overly strict.
- long e2e are great. which scenarios should have them, how to maintain them, how to signal the intent to other devs.
    - how do i name them?
    - how do i signal them?
- edges of happy path e2e. what's the most efficient way of having them not re-eval the whole scenario for 1 turn
  failure.
- what groups should exist and which sim should go into it.
- when should a criteria be added to an existing sim vs spawn a new one.
- what are the sources of flakiness?
    - which come from straight forward bad patterns?
    - which come from eval mechanism quirks?
- is there ever a reason for same criteria, different shape of scenario?
- what are eval mechanism quirks that matter even with good practices?
- phrasing sensibility for same scenario. doesn't feel sustainable. draw a principle? why exactly the different phrasing
  affects agent? what patterns can we derrive from it?
- common principles that agent should potentially observe in all interactions should go onto e2e group, those are the
  highest value sims.
- split by journey steps?
- is there any real value in grading persona as well as agent?

Review Smells:

- Condition re-states a tag.
- Expectation not aligned with journey.
- Condition requires specific wording journey doesn't observe.
- Condition pins observation on a very specific turn that would fail on a slow turn which would trigger a PI.
- Condition was added just to avoid leaving expectedOutcomes empty, even though it's perfectly fine.
- Condition provides reason for the condition (can cause flakiness if judge expects agent to provide that reason)

Eval runs efficiency:

- Can we identify hotspots and run sims hottest-to-coldest
- split by scenarios. regression runs would trigger the most specific ones first, generic later. or e2e to more
  specific.

Components:

- persona
- persona data
- eval:conditions
- eval:tags

Reasons to near duplicate a scenario:

- non-standard phrasing.
- same scenario, same persona, different customer data.
- same scenario tested for edges.
- different paths for the same scenario.

Good suite:

- no redundant sims.
- the most
- good naming.
- good grouping.
    - clear separation between e2e and narrow behaviour sim
    - abuse, guardrails, e2e?

Good sim:

- not outdated.
- good evaluation criteria.
    - tag/condition balance: tags eval deterministic checkpoints, conditions behaviour (including how tag checkpoints
      are treated when genuinely relevant)
    - helps identify what needs fixing right away.
    - doesn't cause false failures.
    - conditions allow to understand immediately what's being evaluated.
    - target the principle over specific behaviour example.
    - on catching failure (e.g. repro) - rather than evaluating the exact bad behaviour, adjusts the principle agent
      should've followed.
- good tags:
    - requires tags that are critical for the right path. doesn't require tags that are not critical, however common
      those seem to appear in good conversation samples.
    - forbids only tags which presence will always mean agent failure.
- right persona.
    - speaks the intended amount of information per-turn: just enough, slight/strong over/under share.
    - pushes back, guides agent, allows itself to be guided.
    - focused on the conversation, distracted.
    - represent behaviour that creates desired scenario (so long as agent doesn't derail, at which point it doesn't
      matter), i.e. doesn't derail before agent.
    - doesn't tap out pre-maturely.
- correctly sized.
- no flakiness.
