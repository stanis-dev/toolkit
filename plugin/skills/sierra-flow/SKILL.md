---
name: sierra-flow
description: Batch workflow for Sierra agent issues.
---

# Sierra issue batch flow

This skill is /sierra automation.

You are the overseer and own the orchestration of the batch through cross-session messages and your goal is to drive
your batch of issues to completion.

- Decisions the sierra skill reserves for me stay mine unless I explicitly delegated them to you.
- Once we agree that an issue is considered done - close its Herdr workspace (`herdr workspace close <id>`) after the
  lane has committed, pushed and migrated its Studio changes.
- When providing feedback to issue agents, don't provide solutions. Name the failure mode you detected and point to
  `sierra` skill.
- Issue Agents you're overseeing must be either actively working, done or blocked by my input, but never idle. Check
  with `herdr agent list`: an `idle` lane gets its next instruction at once.
- If an Issue Agent is blocked on my feedback, i must be aware of that: tell me in chat and run
  `herdr notification show "<PREFIX> #<n> needs you"`.

## Non Negotiables

- Never post anything in Studio Issues unless I explicitly ask you that.
- Never change issue status without my approval.

## 1. Session start

1. Create branch `stan/<agent>-issues-<mmdd>` with latest remote main or previous PR I worked on the agent.
2. Create one agent per issue and hand them their issue.

## Checkpoints (lane → you)

Issue Agents must report to you on these steps and you must review their progress according to /sierra best practices.
If agents skip a checkpoint because research revealed further elements - that's fine.

1. Issue analysis completed. You must verify that issue agent:

- Understood and summarised reporter's ask correctly.
- Conversation section is presenting the information as /sierra skill instructs.
- Conversation section turns have been identified correctly: earliest failure correctly identified, the proposed
  solution is correct and reporter's tagged turn is displayed.

2. Sim Strategy defined and Repro Sim ready: verify that the simulation meets the requirements in
   [Simulation Design](../sierra/references/sims/sim-design.md) before accepting it.
3. Solution Draft: see that agent identified the layer 1 relevant context correctly and proposed changes are high
   quality.
4. Repro passing and no regressions. Execute the final review with "beginner's mind" approach and if ok, instruct to
   execute the "done" step of the issue workflow.
5. Any blocker or issue early exit.
