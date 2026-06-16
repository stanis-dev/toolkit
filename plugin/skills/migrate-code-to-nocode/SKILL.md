---
name: migrate-code-to-nocode
description:
    Migrate an uploaded or otherwise provided code-defined agent into Agent Studio as a no-code or
    hybrid Sierra agent. Use when the user wants to migrate an existing code agent, uploaded zip, or
    Sierra Agent SDK TSX agent into Agent Studio; do not use for ordinary Ghostwriter edits, new
    journey or tool work, debugging, or general questions about SDK code.
---

# Migrating Code To No-Code

Migrate uploaded SDK agent code into Agent Studio without changing the agent's scope or inventing
new behavior.

---

## Phase 1: Define the migration boundary

Start with the uploaded files and determine exactly what is in scope for migration.

- Find the agent entry point, usually `main.tsx` or `agent.tsx`, and follow it to the rendered
  `<GoalAgent>`.
- Read the `GoalAgent` children together with the files (goals, tools, helpers, etc) they depend on.
- If the agent is large or has multiple journeys, prefer migrating one journey at a time rather than
  the whole agent in a single pass.
- Treat `<GoalAgent>` as the structural boundary: SDK constructs inside it are candidates for Agent
  Studio; everything outside it stays code-backed.
- Keep tools or helpers that still need code-side context or dependencies in code.
- If a tool is already registered in code with `tools.registerTool({ noCodeId: "..." })`, treat it
  as a registered tool and prefer reusing it through `tool_ref` rather than rebuilding it.
- Keep hook-based runtime logic that relies on SDK state, effects, or context in code unless that
  behavior is being replaced by an Agent Studio block.
- Use `sdk-to-blocks-mapping.md` as a high-level reference for likely block and tool conversions.
- Treat this as a structural boundary, not a prop-by-prop conversion exercise.

---

## Phase 2: Present the migration plan

Before editing, ask clarifying questions with `AskUserQuestion`.

Common examples:

- Which journey should migrate first if the agent is large or has multiple journeys?
- Should this pass preserve the current behavior, or also improve the journeys during migration?
- Should this migration slice end fully no-code or stay hybrid for now?

Then use `/plan-changes` and any required supporting skills such as `/add-journey`, `/add-tool`, and
`/add-integration` to shape the migration. Inspect the workspace yourself and be explicit in the
plan about what will remain code-backed, including any integrations, knowledge sources, or
registered tools that the migration will continue to rely on, then present a markdown proposal using
Agent Studio concepts and concrete behavior rather than files.

Structure it with sections such as:

- `What moves into Agent Studio`
- `What stays code-backed`
- `Target shape`
- `Cutover and verification`

---

## Phase 3: Build the Agent Studio representation

- Build the approved migration plan.
- If a tool is already registered in code, prefer `tool_ref` instead of rebuilding it as a new
  no-code tool.
- Default to parity. Preserve the existing scope, behavior, and journey granularity unless the
  developer explicitly asks to change them.

---

## Phase 4: Tell the developer what to do with the code

End with one of these outcomes:

- **Fully no-code**: Nothing meaningful remains outside `GoalAgent`. The code repo can be retired
  after verification.
- **Hybrid**: Code remains outside `GoalAgent`. Keep the remaining code, render the no-code journeys
  through `NoCodeJourneysTyped`, and remove or disable duplicate SDK journey content after parity is
  confirmed.
- **Hybrid with code-backed tools**: Some tools still need code-side context. Explain registered
  tools and `tool_ref` blocks before telling the developer what must stay in the repo.

Then, if code and no-code will coexist temporarily, choose one rollout path and explain it clearly.
Be explicit about what is temporary, what becomes the long-term source of truth, and what should be
disabled or removed at cutover.

1. **Cutover path**: Make the migrated no-code journey the new source of truth. Keep only the shared
   code that still belongs outside `GoalAgent`, plus any code-backed tools the no-code journey still
   needs. After parity is verified, remove or disable the old code-defined journey.
2. **Experiment path**: If you need a live comparison, route traffic with a code-side SDK
   `Experiment` so only one path is active per conversation. Use the control variant for the legacy
   code journey and the treatment variant for `NoCodeJourneysTyped` or the migrated no-code path.
   Use the experiment to confirm parity and check for regressions, then complete the cutover and
   retire the legacy code-defined journey.

Example cutover path:

```tsx
const LookupOrder = tools.registerTool({ noCodeId: "lookup-order", ... });

createAgent({
    useTools: () => [LookupOrder],
});

function Agent() {
    return (
        <GoalAgent>
            <SharedAuthRules />
            <EscalationConditions />
            <NoCodeJourneysTyped />
        </GoalAgent>
    );
}
```

```json
{ "type": "tool_ref", "noCodeId": "lookup-order" }
```

After parity, remove the old code-defined journey. Keep only the shared code context and any
registered tools the no-code journey still needs.

Example experiment path:

```tsx
<Experiment name="Returns migration" id="returns-migration" assignmentKey={customerId}>
    <Variant control percentage={0.5} id="code">
        <LegacyReturnsJourney />
    </Variant>
    <Variant percentage={0.5} id="no-code">
        <NoCodeJourneysTyped />
    </Variant>
</Experiment>
```

---

## Phase 5: Offer verification

Only offer verification after the migration is complete enough to have a concrete setup path from
Phase 4. First finish the target state and cutover approach, then propose a parity check between the
original code path and the Agent Studio version.

- Run existing simulations first if they already cover the migrated behavior.
- If coverage is missing, use `/add-simulation-test` to add a small representative set of parity
  scenarios, and use `/debug-simulations` for nontrivial failures.
- Be explicit about whether parity was checked, not checked, or only partially checked.
