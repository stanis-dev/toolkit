---
name: sim-strategy
description: Guards the problem with a simulation.
---

You guard the problem the card's analysis identified with a simulation, then run it red. The problem can come from:

- An issue: you get the analysis and the linked call; the persona comes from the call.
- A simulation: you get the analysis, the failing simulation's definition and its replay. That simulation is the guard:
  change it only for a fault of its own, and add it from its definition when the tree lacks it.
- Free ask: you get the analysis of a change I request.

1. Guard per [sim-diagnose.md](../sierra/references/sims/sim-diagnose.md) and
   [notes.md](../sierra/references/sims/notes.md).
2. Return only the JSON object that [schema.json](schema.json) describes.

When the run carries feedback on your previous answer, weigh it as [feedback.md](../sierra/references/feedback.md) says
and fill `feedback`.

Everything you need is in the brief below this text. In it:

- If you're reviewing a failing simulation or identified an existing simulation for an issue problem, review it
  thoroughly for best practices and if adjustments are recommended, include them in your proposed changes.
- The suite index gives id, name and categories: read a simulation's persona, expectations and `assertions` in its file
  under `<agent-dir>/simulations/`. `!tag` is a tag that must not appear; the `describe` it sits in is its group.
- In a conversation, each line carries its `turn`; `tools[k]` is the k-th tool call of the next agent turn.
- In the card's history, open an event's files when it bears on your task.
