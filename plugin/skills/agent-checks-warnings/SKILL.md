---
name: agent-checks-warnings
description:
    Triage and address Agent Checks warnings. Invoke only when the user explicitly asks to look at,
    address, fix, or silence one or more Agent Checks warnings. Do not invoke proactively.
---

# Agent Checks warnings

Agent Checks warnings are expert-graded potential issues in an agent definition, such as missing
tools, conflicting instructions, or undefined terminology. They appear in Agent Studio's "Checks"
feature in the UI. You can also access and manipulate the warnings through MCP tools.

## Relevant MCP tools

Use these two MCP tools; rely on their MCP documentation for usage details:

- get_agent_checks_warnings
- update_agent_checks_warning_status

## Addressing warnings

### Keep it short

- If the user request is about a particular warning (specified by a warning ID), then only fix that
  particular warning.
- If the user request is about addressing warnings in general, then start with the first active
  warning returned by `get_agent_checks_warnings`. Include nearby warnings only when they are in the
  same block or clearly need the same fix.

In either case, make the smallest change that achieves the desired goal. After edits, call
`get_agent_checks_warnings` until `hasPendingChecks` is false; fixed warnings should be absent from
active results. Then return to the user.

### Possible actions

For each warning, choose one of the four actions:

- **`fix`**:
    - Default to this action whenever editing a no-code block can resolve the issue, even if the
      warning also references code-defined content.
    - Prefer editing the flagged block over adding new blocks or tools. When a warning suggests
      something is missing, first check whether an existing block or tool should be extended or
      corrected; only add a new one when nothing existing covers the behavior. Never resolve a
      warning by restating context that already exists elsewhere in the workspace (see "How the
      runtime assembles the prompt" in the workspace instructions).
- **`ask`**:
    - The warning is probably fixable in no-code blocks, but the correct fix depends on
      customer-specific context that you don't have. In that case, you should ask the user for the
      necessary context. For example:
        - If the warning flags undefined terminology, do not invent a glossary definition; ask the
          user what the term means before editing.
        - If a tool reference is dangling and the correct behavior is not obvious, explain whether
          it looks like a misspelling, an unexposed tool, or a genuinely missing tool, then ask the
          user to confirm the right fix.
    - When in doubt, ask the user instead of making a speculative fix.
- **`silence`**:
    - Use only when one of the following holds and you can explain why:
        - The warning is a clear false positive; the rule misread the agent's intent.
        - The flagged content is intentional, and the trade-off has been explicitly weighed against
          the rule's guidance.
    - Before silencing the warning, present your reasoning for this action to the user and ask for
      their confirmation.
- **`skip`**:
    - Use when one of the following holds:
        - Resolving the warning requires editing code-defined content, such as when all relevant
          flagged blocks are code-defined, i.e., they have no `blockLink`.
        - Required customer-specific context is still missing after you asked the user for it, and
          the user cannot provide it now or asks you to defer that warning.
