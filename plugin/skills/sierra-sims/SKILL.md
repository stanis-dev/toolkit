---
name: sierra-sims
description: Guidance for producing great agent simulations.
---

# Sierra Simulations

A good simulation must combine a well instructed customer LLM, complete set of evaluation criteria, accurate judge LLM
conditions and result in a realistic conversation between the agent and the customer.

## Customer LLM

Customer LLM's goal is to steer the agent into the exact scenario that is intended to be evaluated.

- It must dose per-turn information. Blurt a bit too much, just enough for agent to be comfortable or be terse enough to
  cause underspecification.
- It must never have information that a normal customer would not have/care about.
- It should have a personality that matches the scenario - calm and collaborative, annoyed/frustrated,
  anxious/concerned, etc...
- It should know whether to let itself be guided by agent or push a specific direction.
- It should communicate in a way that a real life customer would in a real conversation.
- It does not need to know the path the scenario is meant to take, so that agent failure happens as it would in a real
  conversation, where customer is not aware unless the scenario is meant to have a customer who is familiar with the
  system.

### Customer LLM Failure Modes

- Poorly paced information sharing not suited for failure mode being explored.
- Underspecified customer LLM improvisation steering conversation from the desired scenario, causing a simulation to
  fail due to that and not the agent's fault.
- Customer LLM hints agent towards the right path with implementation info a real customer would not have.
- Customer LLM parrots its instructions with same wording as the journey, instead of natural wording a real customer
  would most likely use.

## Evaluation Criteria

Tag expectations evaluate deterministic pathing of the agent. Observation conditions evaluate what tags cannot.

- Prefer tag expectations to observation conditions.
- When considering tags to apply, apply all tags that we'd expect the agent to apply in a correctly handled scenario.
- Negative tag expectations are useful to evaluate paths that agent could take even with positive tag expectations
  passing. If a positive tag expectation already excludes an undesired path - don't use the negative tag expectation.
- Tags can evaluate a path, but not always how that path was reached/executed - e.g. agent phrasing, whether agent asked
  redundant questions, etc... For those cases use observations.

## Agent Known Failure Modes

- A single turn provides information that it was meant to acquire over several turns.
- A turn provides information that agent did not expect.
- A turn provides information that skips steps of the workflow agent was taught.
- A turn provides only partial information of what agent would expect from a turn.
- A condition that was not meant to trigger does, and unwanted context confuses agent.
- A condition that had to trigger did not, necessary context never injects.

## Debugging Problems

- Always search for the earliest deviation from happy path. Actual damage may present on later turn, obscuring the
  source.
