---
name: sierra-wrap-up-issue
description: Wrap up completed Sierra issue work by generating client report, creating/updating PR, and documenting changes. Use when Sierra issue implementation is complete and ready for review.
---

# Sierra Issue Wrap-Up

Finalizes completed work on a Sierra issue with client-facing report and PR.

## Required Input

User provides a file containing work summary information.

## Pre-requisites (always perform)

- Fetch and evaluate code changes vs main to understand solution
- Fetch workspace diff via `sierras` tool to understand solution
- Read relevant spec from `~/code/pronet/context-docs/specs/`

## Output

Append all results to the relevant spec doc in `~/code/pronet/context-docs/specs/`

---

## 1. Client Report

Generate a Slack-compatible report. **Critical formatting rules:**

- **No tables** (Slack doesn't render them)
- All issue numbers must be hyperlinked
- All simulations must link to latest release (if exists) or current workspace; tag new sims as `[new]`
- Test links must use format from `TESTING_GUIDE.md`
- All links: `[text](URL)` format
- **No implementation details** (irrelevant to client)
- Include 2-3 word test user selection rationale when relevant
- For sims not directly testing the exact solution: add 2-5 word description of how it helps verification

### Example Format

```
• [#63](https://linear.app/issue/aaaf4b12-e50f-4a93-bbef-379c71409fd8) — Payment promise date should be limited to 3 days
    ◦ Live Scenario: complete verification → decline all payment options → give date 5 days out → agent requests closer date
      • [05559990001](https://eu.sierra.chat/agent/.../chat?voice=1&feedback=1&variable=PHONE_NUMBER:05559990001) - Can Öztürk — card fails, full payment promise flow
      • [05559876543](https://eu.sierra.chat/agent/.../chat?voice=1&feedback=1&variable=PHONE_NUMBER:05559876543) - Ayşe Demir — no card, bank transfer + promise flow
    ◦ Related Simulations
      • [Payment Promise Properly Recorded](https://pronet.sierra.ai/studio/workspaces/.../simulations/...)
      • [Payment via Bank Transfer/EFT with Promise](https://pronet.sierra.ai/studio/workspaces/.../simulations/...)
      • [Payment Failed - Insufficient Limit, Payment Promise Taken](https://pronet.sierra.ai/studio/workspaces/.../simulations/...)
      • [Payment Promise Reminder - Unfulfilled Promise from Last 30 Days](https://pronet.sierra.ai/studio/workspaces/.../simulations/...)
```

---

## 2. Pull Request

1. Check if PR exists against main; create if not
2. Add brief description of changes
3. Populate workspace diff block using `sierras` powertool

### PR Description Format

```md
- <Change summary 1>
- <Change summary 2>
- <Change summary 3>

```diff
# Diff: workspace vs #<issue> - <description>
# Generated: <timestamp>

## Journey
(changes or "No changes")

## Tools
(changes or "No changes")

## Simulations
+ <New simulation name>
+   Group: <group>
+   Device: <device>
+   Message: <user instruction>
+   Outcome: <expected outcome 1>
+   Outcome: <expected outcome 2>
+   Expected tag: <tag>
```
```
