---
name: fix-issue
description:
    Investigate and fix a Sierra issue end-to-end. Invoke this skill when the user references an
    issue by number, link, or shorthand like ISSUE-123, or when you need to reproduce a behavioral
    bug from production conversations and apply a targeted fix.
---

# Fixing Issues

Issues identify behavioral problems in production conversations. This skill walks through the full
loop: understanding the issue, reproducing it in a simulation, diagnosing root cause, applying a
fix, and verifying the fix passes.

Prefer the Sierra MCP tools available in the current Ghostwriter session over asking the user to
gather information manually. Use issue lookup and simulation execution tools such as
`get_issue_details`, `run_test`, and `get_test_results` when they are exposed. Author reproduction
simulations as JSON under `.composer/simulations/tests/`. When you need workspace state, sync
locally and inspect the synced `.composer/` config.

---

## Phase 1: Understand the issue

Parse the issue number from the user request or surrounding context. Also capture any explicit
conversation ID or Agent Studio conversation URL the user already provided, then call
`get_issue_details`.

Read the issue description, linked conversations, and examples. Decide what to investigate next
based on this context.

**Exit criteria:** You know what the reported problem is and which conversations demonstrate it.

---

## Phase 2: Investigate linked conversations

If the user already gave you a conversation ID or conversation URL, include that conversation in
your investigation immediately instead of waiting for issue-linked examples alone. Normalize any
URL-derived conversation ID as needed by following `/debug-conversations`.

Sync the relevant conversation IDs locally with
`pnpm sierra ghostwriter --sync-conversations --ids <comma-separated-ids>`, then follow the
`/debug-conversations` skill to analyze the synced artifacts. This set should include both the
issue-linked conversations from `get_issue_details` and any explicit conversation ID the user gave
you.

**Exit criteria:** You understand the specific agent behavior that went wrong and have a hypothesis
about the root cause -- something missing (a policy gap, a wrong tool response, an incorrect
condition) or something present (competing instructions, a stale policy, an over-specific rule left
by a previous fix).

---

## Phase 3: Reproduce with a simulation

Follow the `/add-simulation-test` skill to build a reproduction simulation that captures the
problematic scenario.

Keep in mind that an issue may already be fixed by the time you investigate it, especially if it was
filed more than a week ago. If your best reproduction simulation now passes and you are reasonably
confident the behavior is working, say that clearly to the user instead of making an unnecessary
edit.

**Exit criteria:** You have a simulation that either reproduces the bug (confirming the issue is
still present) or passes (suggesting the issue is already resolved).

---

## Phase 4: Fix

Run `git gw-pull`, inspect the relevant synced workspace config, and edit the workspace files
directly to fix the relevant journeys, tools, policies, or conditions. Treat `.composer/blocks/` as
the source of truth for top-level block layout and identity.

If the behavior is wired through a code-defined `tool_ref`, keep the `tool_ref` block and adjust
only the surrounding no-code config here. If the registered tool implementation itself needs to
change, tell the user that fix has to happen in the SDK/runtime layer.

Apply the smallest change that addresses the root cause: correct the block or tool that produced the
bad behavior instead of adding a policy to patch over it. Before writing anything, name the kind of
change the diagnosis calls for -- a deletion, an edit, or an addition. Do not let "fix" silently
mean "add": when the root cause is something present rather than something missing, the fix is to
delete or rewrite it, and the definition gets smaller. The editing rules in "Start lean: context is
precious" (workspace instructions) bind hardest here; after the fix, remove or merge anything the
fix made redundant.

**Exit criteria:** The relevant blocks have been updated or removed to address the root cause.

---

## Phase 5: Verify

Rerun the reproduction simulation. Only claim the issue is fixed once the repro passes or the
remaining gap is clearly explained.

If the simulation still fails, sync the run locally with
`pnpm sierra ghostwriter --sync-simulations --run-id <simulationRunId>` and follow the
`/debug-simulations` skill to diagnose. Then return to Phase 4.

**Exit criteria:** The reproduction simulation passes, or you have a clear explanation of what
remains unresolved and why.

---

## Quality checklist

| #   | Check                                                                                                       |
| --- | ----------------------------------------------------------------------------------------------------------- |
| 1   | Called `get_issue_details` before investigating                                                             |
| 2   | Synced and analyzed the relevant conversations via `/debug-conversations`                                   |
| 3   | Built reproduction simulation via `/add-simulation-test`                                                    |
| 4   | Checked whether the issue is already fixed before making changes                                            |
| 5   | Fix addresses root cause, not symptoms                                                                      |
| 6   | Named the fix as a deletion, edit, or addition before writing; nothing added that restates existing context |
| 7   | Reproduction simulation passes after the fix                                                                |
