# Guide for diagnosing Simulations Replays and Conversation

Your goal is find the earliest turn where agent went off script and identify the potential cause. All context edits are validated with me first and applied on my OK. Only offer followups if those are critical and justify taxing my attention. If the fix requires multiple steps - we'll focus on ony thing at a time. Once this gets fixed, we'll talk about next steps.

1. Use `sierra ghostwriter --sync-simulations --run-id` to fetch simulation replays. Make sure the replay with transcript and debug info are ready. If for any reason you cannot acess them, stop here and let me know.
2. Identify the turn that fails judge condition, or is being reported in the issue or I that I asked you to check.
3. If debugging a simulation - verify the simulation itself is correct (see /sierra-sims) and also makes sense from common sense before attempting to debug agent behaviour. If there's reasonable doubt - stop here and report your findings.
4. Evaluate whether that turn was the origin of the failure or was a consequence of a previous deviation. Move backwards until you find the earliest turn to fail.
  1. Start by finding the context that is meant to guide agent for the case at hand. See if it was agent's own inference, or something like tool-driven instructions. If it doesn't exist - propose draft to add it. If it exists:
    1. make sure it was present on that turn (e.g. not gated by a condition of a block or journey, tool took wrong branch).
    2. If it was present, understand why it did not have the desired effect - was it overpowered by another piece of context? poorly worded? under/over-specified?
5. Present to me the report in diff format. Don't mention ghostwriter files - those are meant for you only and the references will only create noise for me. Don't add any information I'd already know - I wrote this skill, I know exactly how it works and its parts.
  1. Sim/Issue - ✅ / ⚠️ / 🔴
  2. What agent said vs what it should've said (diff format).
  3. Responsible context. Current vs Suggested (diff format). Have the reason behind the suggestion clear and ready, but don't provide unless I ask you for it.
  4. (Ignore if debugging a simulation) Sims - adjust existing or add a new one, or both?

## Known failure modes

- An unintended condition triggered, revealing context/tool that were not intended to be present. Potential solutions:
  - Predicate/s should be reworded
- Agent did have the expected context and the instruction was present and clearly worded, in alignment with /good-prompting criteria:
  - A different case overpowered the expected point. Find the part of context responsible for it and present it to me. Then consider the potential edit for the overpowering context.
- Agent calls a tool too loosly/eagerly. 
  - See that tool's description is of high quality
  - See that apart from the description, prompt actually teaches agent how/when to use the tool within its workflows.

