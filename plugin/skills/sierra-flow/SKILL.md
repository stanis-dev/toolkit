---
name: sierra-flow
description: Batch workflow for Sierra agent issues.
---

# Sierra issue batch flow

This skill is /sierra automation.

You are the overseer and own the orchestration of the batch through cross-session messages.
Expect to receive instructions about which issues to work on, otherwise the run is a no-go.

- Decisions the sierra skill reserves for me stay mine unless I explicitly delegated them to you.
- Unless an issue agent is done, make sure they are not idle.
- Once we agree that an issue is considered done - unpin the agent.

## 1. Session start

1. Create branch `stan/<agent>-issues-<mmdd>` with latest remote main or previous PR I worked on the agent.
2. Create one agent per issue and hand them their issue.

## Checkpoints (lane → you)

Issue Agents must report to you on these steps and you must review their progress according to /sierra best practices. If agents skip a checkpoint because research revealed further elements - that's fine.

1. Issue analysis completed: make sure agent understood what the issue is about and what the reported wants.
2. Sim Strategy defined and Repro Sim ready: see that agent created a simulation that is high quality and will reproduce/catch Sierra agent failure.
3. Solution Draft: see that agent identified the layer 1 relevant context correctly and proposed changes are high quality.
4. Repro passing and no regressions. Execute the final review with "beginner's mind" approach and if ok, instruct to execute the "done" step of the issue workflow.
5. Any blocker or issue early exit.
