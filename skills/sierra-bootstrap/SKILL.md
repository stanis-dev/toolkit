---
name: sierra-bootstrap
description: Bootstrap Sierra issue work by creating branch, workspace, fetching issue context, analyzing simulation coverage, and generating Linear ticket. Use when starting work on a Sierra issue with PRO-XX ticket and #NN issue number.
---

# Sierra Issue Bootstrap

Automates the setup required to start work on a Sierra issue.

## Required Input

User must provide:

-   **Linear ticket ID**: format `PRO-<number>` (e.g., PRO-123)
-   **Issue number**: format `#<number>` (e.g., #34)

If not provided, request both before proceeding. If user indicates that feature has no related issue, run a quick check
of outstanding issues in case some are affected in any way.

**CRITICAL** actively ask user for clarifications whenever needed

## Workflow

1. **Git setup**: Create new branch from main (ensure up-to-date with remote). Name: linear ticket ID
2. **Workspace creation**: `sierras` CLI to create workspace. Name: linear ticket ID
3. **Fetch issue content**: `sierras` CLI to get exact issue details, and the original conversation on which it was
   reported
4. **Fetch journey definition**: `sierras` CLI
5. **Check requirements**: Find related info in `~/code/agent-ctx/customer-docs/`
1. **Analyze codebase**: agent behavior is often product of code-based and Studio-based instructions
6. **Fetch workspace data**: Establish updated agent context
7. **Analyze simulation coverage** (see procedure below)
8. **SDK docs check**: Verify assumptions and best practices by using `/sierra-best-practices` skill
9. **Generate Linear ticket body** (see format below)
10. **Persist analysis** to `~/code/agent-ctx/specs/` as markdown

---

## Simulation Coverage Analysis

Determine: **"Can we evaluate this issue with existing sims, or do we need changes?"**

### Step 1: Survey simulations

List sims and scan for keywords from issue. Sim names describe customer behavior—search for user-facing terms (e.g., "payment", "card", "verification"), not implementation terms.

### Step 2: Investigate candidates (max 5)

Replay each candidate and check:
- Does `message` describe same user intent as issue?
- Does `expectedOutcome` test the broken behavior?
- Is mock user configured correctly for this scenario?
- If failing: is it failing for the reason we're investigating?

### Step 3: Decide

**A: Existing sim covers this** → If failing, that's the target. If passing, issue may be edge case or already fixed.

**B: Existing sim is close enough to extend** → Note what to modify (message, outcome, mock user).

**C: No sim covers this** → Only after confirming no existing sim can be extended. Propose new sim spec.

---

## Linear Ticket Body Format

```md
# [#<issue>] <Short behavior-focused title>

Fixes
[#<issue>](https://pronet.sierra.ai/agents/01K9WVVXBBMBS4V8VJYQVNJNN2/issues/<issue>?status=OPEN%2CNEEDS_CLARIFICATION%2CCONFIRMED)
[GitHub](https://github.com/sierra-agents/pronet/tree/<branch>),
[Workspace](https://pronet.sierra.ai/agents/01K9WVVXBBMBS4V8VJYQVNJNN2/journeys/01K9WVVYV5MM357XWAC9E35V32?workspaceId=<workspace-id>)
```

Requirements:

-   Link to the issue
-   Mention existing related simulations OR one-sentence description of new scenario(s)
-   Mention related requirements if they exist
-   Title: short, 100% behavior-focused, clear actionable item
