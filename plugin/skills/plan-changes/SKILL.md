---
name: plan-changes
description: >-
    Structured planning for non-trivial changes. Use when the work spans multiple journeys,
    rearchitects the tool set, connects new integrations, involves nuanced design tradeoffs, or
    materially changes how the agent behaves. Skip for straightforward changes where the design is
    obvious: single-tool additions, policy tweaks, simulation fixes, or direct follow-ups to a
    confirmed direction.
---

# Structured planning

Planning is exploratory and iterative. Collect information, resolve ambiguity, and maximize clarity
before making changes. Present a proposal, get feedback, refine -- the user may push back, adjust
scope, or raise constraints you didn't know about. If the request is ambiguous, contradicts what
exists in the workspace, or has a design fork that materially changes the approach, ask before
researching further.

## Principles

1. **Understand the problem, not just the request.** Users often frame requests as solutions ("add a
   returns journey") rather than problems ("customers can't process returns"). Before planning what
   to build, understand why it's needed. The right plan might be a trigger tweak on an existing
   journey, not a new one.
2. **Outcomes over inputs.** Describe what the agent will be able to do, not what blocks to add.
   "The agent will resolve return requests end-to-end" rather than "add a ReturnOrder journey with
   three tools."
3. **Scope discipline.** Clearly separate what was requested from what you're additionally
   recommending. Don't expand scope without flagging it -- the user should explicitly opt in to work
   beyond what they asked for.
4. **Proportional planning.** Match the weight of the proposal to the complexity. A two-journey
   change needs a few bullets, not a detailed spec.
5. **Plan for verification.** Every plan should include how you'll know the changes work. Which
   simulation scenarios will you run? What conversations should be tested? A plan without a
   verification strategy is incomplete.
6. **Promise discipline.** Only commit to work you will do now. Everything else is optional next
   steps. Never end with only a plan unless the user explicitly asked for one -- the deliverable is
   a working agent, not a proposal.

## Grounding in current state

If you haven't already established context for the relevant parts of the agent earlier in the
conversation, do so before proposing changes:

- Review existing journeys, tools, conditions, and policies in `.composer/blocks/` and the relevant
  tool/component definition files.
- Refresh from Agent Studio with `git gw-pull` when local state may be stale.
- Check `docs/available-integrations.md` if the change involves external API tools.
- Run `list_knowledge_sources` if the change involves knowledge tools.
- Read any user-uploaded documents (SOPs, policy docs, screenshots) -- these are primary source
  material for what the agent should do.

Don't re-inspect what you already understand -- but don't propose changes against an incomplete
mental model either.

## Asking questions

Getting clarity is important -- be persistent. Go 1-2 questions at a time, re-evaluate after each
answer, and ask follow-ups as new gaps emerge. Don't front-load a wall of questions. If the request
is too broad to plan concretely -- e.g., "build me a customer service agent" -- ask which intents or
scenarios to start with before drafting a full proposal.

Use `request_user_input` when structured input (choices, confirmations) would help; use natural text
for open-ended questions. Format questions clearly under an **Action required** heading at the end
of your message so the user knows what's blocking progress.

## What a good proposal covers

Not every proposal needs every section -- scale to the complexity. These are the dimensions to
consider, not a form to fill out:

- **Current behavior** -- How the agent handles the relevant scenarios today.
- **Desired behavior** -- What the agent will be able to do, framed as conversational outcomes.
- **Recommended changes** -- Which journeys, tools, conditions, policies, knowledge tools, or
  simulations to add, modify, or remove. Be concrete: "Add a GetOrderStatus tool that takes an order
  ID and returns status, items, and tracking" -- not "add an order lookup tool." Flag anything
  beyond what was explicitly requested. Use tables when recommending multiple changes with shared
  dimensions (e.g., several tools each with a name, purpose, and journey).
- **Tradeoffs, impact, and unknowns** -- Why this approach, what existing behavior changes as a side
  effect, and any assumptions that could change the approach. Surface these alongside the
  recommendation, not as separate sections.
- **Verification** -- Which simulations or test scenarios will validate the changes.

Keep the proposal scannable and actionable -- each recommended change should be specific enough to
implement directly. Once the user confirms, invoke the relevant task-specific skills
(`/add-journey`, `/add-tool`, `/add-integration`, etc.) -- don't skip skill invocation just because
you have a plan.

## Finishing up

Before declaring the planned work complete, reconcile every intention from the proposal: done,
blocked (with reason and question), or cancelled (with reason). Do not end with unaddressed items.
