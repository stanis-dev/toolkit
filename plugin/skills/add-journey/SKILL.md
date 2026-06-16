---
name: add-journey
description:
    REQUIRED before creating or modifying journeys. Invoke this skill when you need to build a new
    journey, add a customer intent, create tools, add blocks to the materialized workspace, or set
    up a new workflow. Covers the phased workflow (understand state, design tools, write blocks,
    implement, test) and quality gates. Without it you will miss design considerations that produce
    high-quality agents.
---

# Adding a New Journey

The user owns requirements: what the agent should do, what policies exist, what behavior they
expect. You own the how: which block types to use, how to structure the prompt, where context lives,
what goes in tool response instructions vs. content blocks. Validate requirements and expected
behavior with the user; do not ask them to make prompting or context-management decisions.

When the user provides a step-by-step procedure or SOP, treat it as source material -- not the
target format. Extract the policies, constraints, and tool behaviors from the steps. The procedure
tells you what the agent needs to accomplish and what rules govern it; the block structure you build
is a separate design decision.

## Phase 1: Understand what exists

Read `.composer/blocks/`, `.composer/tools/`, `.composer/docs/available-integrations.md`, and
`.composer/docs/block-reference.md` before writing anything. Know what tools, integrations, and
knowledge sources are already available.

---

## Phase 2: Design tools

Tools come before blocks. For each tool, decide what deterministic work it does, what
result-specific guidance it may return in edge cases, and what state it writes to unlock conditions.
Keep enough standing context in the journey for common paths; use tool responses and conditions to
reveal additional context only when results make it relevant. This allocation determines the scope
of Phase 3.

Use enums for parameters with known value sets -- the LLM reasons about which value fits the
conversation, and the tool receives a constrained, deterministic input. Parameters should capture
structured facts the model extracts from conversation, not free-text summaries for downstream code
to parse. Prefer the existing naming convention in the current journey over the default PascalCase
verb-object pattern. When the user describes a domain, that tells you what tools to design and what
data shapes to expect -- not specific policies.

Verbalize the tool design and allocation decisions before writing blocks. Articulating what each
tool does, what guidance it returns, and what state it writes sharpens your own reasoning and
surfaces the right questions for the user.

Invoke `/add-tool` for the full design checklist and implementation details.

For transfers, check `docs/available-integrations.md` for a contact center integration and
`.composer/tools/` for existing transfer tools before creating one. See
[Transfers](docs/tool-block-reference.md#transfers) for the full pattern. Ask the user for specific
transfer criteria rather than guessing.

---

## Phase 3: Write blocks

Consult [Block Reference](docs/block-reference.md) for every block type's fields, valid values, and
"When to generate" guidance before writing any block. The reference is authoritative for schema and
field semantics.

Before adding any block, identify both its source and its job. If you cannot trace it to user input,
existing workspace definitions, or synced data, you are inventing. If you cannot explain how the
agent would use it in conversation, it likely does not belong.

Tools belong inside the journey as children, scoped to the intent. The orchestration layer already
handles shared company context like brand and greeting, so do not duplicate it.

### Writing block content

The agent's runtime prompt is assembled from multiple layers: the base prompt (tone, personality,
brand), tool definitions (names, descriptions, parameters, response instructions), conditions
(progressively unfurled context), and content blocks (rules, policies, workflows, glossary,
response_phrasing, custom). Content blocks are one input among many.

Before writing a content block, become the agent you are building. Mentally assemble what the agent
already sees from all other layers -- its tools, base prompt, brand config, and any conditions
already in scope. When roleplaying, count only the context the agent can currently see. Content
behind inactive conditions is unavailable until those conditions activate. Then ask: what is missing
for the agent to handle this journey's conversations coherently? Write only what fills that gap. The
goal is a coherent assembled prompt where every piece of context earns its place and no layer
restates what another already communicates. Apply the same perspective to the journey's goal: write
it from the customer's point of view as the outcome the agent should achieve for them, not the
internal operations it will perform.

Keep related guidance together in the narrowest scope that needs it. Do not split one behavior
across multiple blocks unless each layer adds distinct information.

When the same coherent behavior belongs in multiple journeys, extract it into a reusable component
instead of copying it. Define shared behavior once and include it wherever needed, but do not invent
speculative components for reuse you cannot yet see.

Do a subtraction pass before moving on: delete any line whose removal would not materially change
the agent's behavior. Prefer one precise, information-dense instruction over several overlapping
reminders.

**Exit criteria:** `pnpm sierra ghostwriter --lint` passes.

---

## Phase 4: Implement tools

Invoke `/add-tool` for each tool needing a TypeScript implementation. Invoke `/add-integration`
first when a tool needs an external API and no matching integration is connected.

---

## Phase 5: Test

Invoke `/add-simulation-test`. Prefer focused, diagnosable scenarios over one broad conversation,
and use a red/green loop.

---

## Quality checklist

All must pass before the journey is complete.

| #   | Check                                                                                                               |
| --- | ------------------------------------------------------------------------------------------------------------------- |
| 1   | Every policy, glossary term, and rule traces to user-provided information                                           |
| 2   | Every block materially changes behavior; if removing it would not, delete it                                        |
| 3   | No block restates what tools, base prompt, or other layers already communicate                                      |
| 4   | Shared behavior reused across journeys is factored into a coherent, non-speculative component instead of duplicated |
| 5   | Tools are children of the journey, not top-level                                                                    |
| 6   | Tool descriptions are well-specified and avoid internal system names                                                |
| 7   | Tools do real work (lookups/computation or actions); none exist solely to return instructions                       |
| 8   | Simulation tests pass                                                                                               |
