# Guide for diagnosing Simulations Replays and Conversation

Your goal is find the earliest turn where agent went off script and identify the potential cause. Only offer followups if those are critical and justify taxing my attention. If the fix requires multiple steps - we'll focus on only thing at a time. Once this gets fixed, we'll talk about next steps.

1. Download the simulation run the way `.composer/docs/agent-traces-reference.md` describes, with the target qualifier from the sierra skill's tooling.md. Make sure the replay with transcript and debug info are ready. If for any reason you cannot access them, stop here and let me know.
2. Identify the turn that fails judge condition, or is being reported in the issue or I that I asked you to check.
3. If debugging a simulation, verify the simulation itself against
   [sim design](../sims/sim-design.md) and also check that it makes sense before attempting to
   debug agent behaviour. If there's reasonable doubt, stop here and report your findings.
4. Evaluate whether that turn was the origin of the failure or was a consequence of a previous deviation. Move backwards until you find the earliest turn to fail.
  1. Start by finding the context that is meant to guide agent for the case at hand, layer 1 of the relevant context below. See if it was agent's own inference, or something like tool-driven instructions. If it doesn't exist - propose draft to add it. If it exists:
    1. make sure it was present on that turn (e.g. not gated by a condition of a block or journey, tool took wrong branch).
    2. If it was present, understand why it did not have the desired effect - was it overpowered by another piece of context? poorly worded? under/over-specified?
5. Show it to me on the card: the failing replay (Simulation Replay), the responsible context
   with the edit (Studio Context Edit) and, unless debugging a simulation, the simulation
   changes (Sim Strategy). Don't mention ghostwriter files: those are meant for you only and
   the references only create noise for me. Don't add any information I'd already know: I wrote
   this skill. Have the reason behind the suggestion ready, but don't give it unless I ask.

## Relevant context

The context relevant to a turn comes in three layers, by how directly it reaches the turn:

1. Direct: what tells the agent what to do at this turn, «do X» or «when X, do Y» with X true
   at the turn, together with what puts it in front of the model: the gate of its block, the
   tool result that carries it. Anything that contradicts one of these head-on is in this layer
   too, wherever it sits.
2. Scenario: what talks about the part of the journey the conversation is in at this turn
   without telling the agent what to do at it: the mission of the journey, the rules for the
   other turns of the same offer, the definitions of the variant.
3. General: what shapes the agent's behaviour at every turn and so at this one: tone, register,
   phrasing, guardrails. «Always show empathy» is layer 3 to «Ask the customer what they think
   of…».

## Known failure modes

- An unintended condition triggered, revealing context/tool that were not intended to be present. Potential solutions:
  - Predicate/s should be reworded
- Agent did have the expected context and the instruction was present and clearly worded, in
  alignment with [agent design](agent-design.md):
  - A different case overpowered the expected point. Find the part of context responsible for it and present it to me. Then consider the potential edit for the overpowering context.
- Agent calls a tool too loosly/eagerly. 
  - See that tool's description is of high quality
  - See that apart from the description, prompt actually teaches agent how/when to use the tool within its workflows.
- Agent must take a decision on a concept that was never defined to him clearly. It may be tangentially referenced throughout the prompt, but not as an explicit bullet point. Often results in agent flakiness. 
  - Solution: centralise the concept.
- A known trap: attempting to gate agent behaviour through a supervised rule. The supervised behaviour will be enforced once through a fake tool return, but all future turns will have the rule present as a standard one. Supervised rules are good for one-time guardrails, e.g. customer requesting to be transferred to human agent where agent logic dictates to do so and end the call. This is often used as a lazy solution.
- Known trap: progress indicator content participates in agent's steering and can induce unwanted behaviour. e.g. PI comes out as "let me check what other offers I can find for you" and agent even despite having been instructed to not provide the next offer will fail and do so because of the PI. If identified, confirm with a quick test - disable PI for all tools and set latency PI to 10s, then verify. If without PI behaviour fails and with them regressed again - this case is confirmed. A solution is to add to the PI custom instructions a point that PIs must never announce an action itself, but only win time for the actual decision.
