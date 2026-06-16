---
name: add-tool
description:
    REQUIRED before designing or implementing any tool. Covers tool naming, parameters,
    descriptions, mock output, MCP shapes, and wiring a TypeScript implementation.
---

# Adding a Tool

Tools are the primary behavior layer. They look up information, take actions, perform deterministic
computation, and read or write conversation state. This skill covers designing a tool and wiring it
to a TypeScript implementation. A custom implementation lives at
`.composer/tools/{ToolName}/implementation.ts`.

Work through the phases below in order.

---

## Phase 1: Design the tool

Before writing any code, design the tool around the job the agent needs done.

### Naming and description

The tool name, description, and parameter names are all visible to the LLM at inference time. They
are also visible in Agent Studio where non-technical users review the agent. Write them from the
perspective of the customer problem the agent solves, not the system that fulfills it.

A tool named `GetOrderStatus` in a retail agent is self-evident -- the agent knows it sells products
and ships orders. A tool named `QueryShopifyOrdersAPI` exposes an implementation detail that neither
the agent nor the user benefits from knowing. The agent's identity and the company context already
establish what systems are involved.

Descriptions should tell the agent _when_ to call the tool, _what_ it returns, and _how_ the results
connect to other tools. They should not explain API mechanics or internal routing.

### Parameter design

Parameters are where the LLM's reasoning ability does real work. Every parameter is a decision the
model makes -- choosing an enum value is classification, filling a structured field is extraction.
Design parameters to take advantage of this.

**Enums over free-text.** When a parameter has a known set of values, use `enum`. The LLM classifies
the customer's intent into the right bucket -- that is inference, not string matching. A
`return_reason` enum of `["damaged", "wrong_item", "changed_mind", "defective", "other"]` lets the
model reason about what the customer said. A free-text `reason` field that downstream code greps for
keywords throws away the model's reasoning and replaces it with brittle pattern matching.

**Extract, don't echo.** Parameters should capture structured facts the model extracts from
conversation -- an order number, a product category, a date. They should not ask the model to
summarize or rephrase what the customer said into a description string for downstream code to parse.

**Omit implementation details.** Parameter descriptions are part of the agent's prompt context.
Describe what the parameter means in the domain, not how it maps to an API field.
`"The order number the customer is asking about"` is useful.
`"Maps to the order_id field in the Shopify GraphQL API"` is noise that consumes context and may
leak into conversation.

### Tools provide context, not directives

A well-designed tool gives the agent data and context to reason from. The anti-pattern is a tool
whose sole purpose is to return step-by-step instructions telling the agent what to say next -- this
produces scripted agents that break on unexpected situations. Tools that return _data_ let the agent
adapt; tools that return _scripts_ make the agent rigid.

When a tool does need to guide the agent's next response (edge cases, policy-specific outcomes),
that guidance belongs in `instructions` within `controls.result({ data, instructions })` or in
`mock_output`. Keep it to the specific situation the tool just resolved, not a general playbook.

### Simulation check

Before finalizing the design, walk through a realistic conversation turn-by-turn. At each step the
agent would call this tool, ask: What params would the model fill? Is the information available in
the conversation at that point? Would the model pick the right enum value? Would any param name or
description text sound odd if the agent mentioned it to the customer? If a param requires
information the customer hasn't provided, the agent will have to ask for it -- is that the right
experience?

---

## Phase 2: Delegate the implementation

Check `.composer/docs/available-integrations.md` to see whether a connected integration covers the
API the tool needs. If the tool is `tool_type: "mcp"`, decide whether it should be a no-code
pass-through or needs a custom wrapper; preserve `integration_id` and `mcp_tool_name` either way.

For no-code MCP tools, no implementation is needed -- skip ahead to wiring.

Otherwise, hand the implementation to `ghostwriter_tool_engineer`. You author the tool block (the
contract); the engineer writes only its `implementation.ts`. Send the contract:

- Tool name and path (`.composer/tools/{ToolName}/`).
- Params shape and types.
- Expected happy-path return shape, matching the `mock_output` field names and structure.
- Integration handle the implementation should call, if any.
- MCP identity (`integration_id`, `mcp_tool_name`) when wrapping an MCP tool.
- Any agent-facing instructions the implementation should attach via
  `controls.result({ instructions })` for specific edge cases.

**Exit criteria:** The engineer reports the implementation file is in place, or has surfaced a
blocker.

---

## Phase 3: Wire the implementation to the block

After the engineer reports back, set `implementation_file` on the tool block in the top-level block
file:

```json
{
    "type": "tool",
    "name": "GetOrder",
    "implementation_file": "tools/GetOrder/implementation.ts",
    ...
}
```

For no-code MCP tools, the correct wiring is the opposite: preserve `tool_type: "mcp"`,
`integration_id`, and `mcp_tool_name`, and omit `implementation_file`.

**Exit criteria:** Implemented tools reference the implementation file; no-code MCP tools do not.

---

## Phase 4: Update simulator state

If the engineer's reply surfaced a simulation contract (integration calls and required account
facts), update `systemsSimulationOptions.accountState` (free-form prose) in every existing sim test
that exercises this tool, so the simulator has the records and branch values the new calls will
query. Skip this phase if the engineer reported no `ctx.apis` calls.

**Exit criteria:** Every existing sim that can reach this tool has `accountState` consistent with
the engineer's surfaced facts.

---

## Phase 5: Verification

1. Run `pnpm sierra ghostwriter --lint` -- must pass with no errors.
2. Run existing simulation tests -- they must still pass. In the test environment, the system
   simulator intercepts `ctx.apis.<handle>` calls and returns responses consistent with each test's
   `accountState` instead of hitting the real integration.

**Exit criteria:** Lint passes, all existing tests pass.

---

## Quality checklist

| #   | Criterion                               | Check                                                                                                                                                 |
| --- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Name and description are domain-level   | No API names, internal system references, or implementation details exposed                                                                           |
| 2   | Params use enums where possible         | Known-set values are enums, not free-text fields parsed downstream                                                                                    |
| 3   | Params capture extracted facts          | Model extracts structured data from conversation, not echoing text for grep                                                                           |
| 4   | Tool returns data, not directives       | Agent reasons from results; `instructions` reserved for edge-case guidance                                                                            |
| 5   | `mock_output` is shaped for the agent   | Every field is one the agent will surface or branch on; no internal IDs, duplicate aliases, producer-prefixed timestamps, or pagination on singletons |
| 6   | Happy-path return follows `mock_output` | Same field names and nesting for the fields that apply; alternate branches may diverge                                                                |
| 7   | Custom implementation wired             | Implemented tools reference their .ts file via `implementation_file`                                                                                  |
| 8   | MCP identity preserved                  | MCP tools keep `integration_id` and `mcp_tool_name`; no-code MCP has no file                                                                          |
| 9   | Lint and tests pass                     | `pnpm sierra ghostwriter --lint` clean, no regressions                                                                                                |
