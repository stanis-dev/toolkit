---
name: sierra-debug
description: Critical guidance for Sierra agent debugging. Use every time you need to find why an agent failed.
---

# Guide for diagnosing Simulations Replays and Conversation

Your goal is find the earliest turn where agent went off script and identify the potential cause.

- Use `sierra ghostwriter --sync-simulations --run-id` to fetch simulation replays.

1. Make sure the replay with transcript and debug info are ready. If for any reason you cannot acess them, stop here and let me know.
2. Identify the turn that fails judge condition, or is being reported in the issue or I that I asked you to check.
3. Evaluate whether that turn was the origin of the failure or was a consequence of a previous deviation. Move backwards until you find the earliest turn to fail.
4. Present to me the report in diff format. Don't mention ghostwriter files - those are meant for you only and the references will only create noise for me. Don't add any information I'd already know - I wrote this skill, I know exactly how it works and its parts.
  1. What agent said vs what it should've said.
  2. Responsible context. Current vs Suggested. Have the reason behind the suggestion clear and ready, but don't provide unless I ask you for it.
  3. (Ignore if debugging a simulation) Sims - adjust existing or add a new one, or both?
5. All context edits are validated with me first and applied on my OK. Only offer followups if those are critical and justify taxing my attention. If the fix requires multiple steps - we'll focus on ony thing at a time. Once this gets fixed, we'll talk about next steps.

## Known failure modes

- An unintended condition triggered, revealing context/tool that were not intended to be present. Potential solutions:
  - Predicate/s should be reworded
- Agent did have the expected context and the instruction was present and clearly worded, in alignment with /good-prompting criteria:
  - A different case overpowered the expected point. Find the part of context responsible for it and present it to me. Then consider the potential edit for the overpowering context.

