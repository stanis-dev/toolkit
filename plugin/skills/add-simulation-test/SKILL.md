---
name: add-simulation-test
description:
    REQUIRED before writing or running simulation tests. Invoke this skill when you need to author
    test scenarios, run simulations, check expected outcomes, or validate tool and integration
    behavior. Covers file-authored simulation JSON, the user simulator, system simulator, judge,
    accountState, initialMemory, running tests, assertion strategies, and instruction writing.
---

# Adding Simulation Tests

Simulation tests verify the real agent against a simulated customer, simulated integration data, and
a judge. In Ghostwriter, authored tests are workspace files: create, edit, and delete JSON under
`.composer/simulations/tests/`, then commit and `git gw-push` before running. MCP simulation tools
are for execution and result inspection.

Read `.composer/docs/simulation-test-reference.md` when you need the full file shape. Read
`.composer/docs/tool-block-reference.md` when a test depends on tool result shape (`mock_output`,
`mock_calls`); read `.composer/docs/tool-code-implementation.md` when it depends on
`controls.result(...)`, `controls.instruct()`, `controls.error()`, or simulator interception.

---

## 1. Gather Context

Read the relevant `.composer/blocks/` files and nearby tests before authoring. Existing files under
`.composer/simulations/tests/` show editable authored tests; files under
`.composer/simulations/test_refs/` are read-only references for code-defined or system tests.

Decide what layer the test should exercise:

- journey routing or conditions
- tool parameter collection and result handling
- implementation behavior inside `func`
- integration behavior through `ctx.apis.<handle>`
- memory-dependent behavior

---

## 2. Author the Test File

Write JSON under `.composer/simulations/tests/`. Keep an existing file's `id` when editing it. Omit
`id` only for a new test. Delete the JSON file to delete that authored test.

Core fields:

```json
{
    "name": "Short scenario title",
    "groupDescription": "Journey or capability",
    "categories": ["scenario"],
    "messages": ["Customer simulator instructions, or exact opening turns plus instructions"],
    "origin": "UI_SIMULATION",
    "expectedOutcomes": ["Behavior the judge should verify"]
}
```

Use `messages` as the user-simulator setup. Most tests use one instruction string. When exact
opening customer turns matter, put those turns first and set `simulationStartIndex` to the index of
the first simulator-instruction entry.

Watch out for duplicate-looking tests. If you need multiple near-identical tests to cover one
behavior, the assertions are probably too weak or the scenario is not actually distinct.

Use `systemsSimulationOptions.accountState` when a tool calls `ctx.apis.<handle>`. The system
simulator stands in for integrations in the test runtime. It intercepts `ctx.apis.<handle>` calls
and returns responses consistent with the starting account snapshot you wrote. Tool functions still
exercise their real implementation: branching, `ctx.store` writes, `controls.result(...)`,
`controls.instruct()`, and `controls.error()`.

The simulator only activates when `accountState` is set. Without it, a simulation that reaches
`ctx.apis.<handle>` can hit the real integration backend. `sierra.fetch` is not intercepted; route
calls through an integration when a simulated response matters.

Consider [What makes a good simulation test](#what-makes-a-good-simulation-test) for best practices.

---

## 3. Push Before Running

Simulation runs execute in Agent Studio's runtime against the server workspace. Local JSON edits are
not runnable until they are committed and pushed:

```bash
git add .composer/simulations/tests
git commit -m "Add simulation coverage"
git gw-push
```

If `git gw-push` fails because the workspace moved forward, run `git gw-pull`, resolve any rebase
conflicts, then retry the push.

---

## 4. Run and Inspect

Use MCP execution tools:

1. `run_test` with specific test names/IDs, or no filter for all tests. Start independent runs in
   parallel when useful.
2. `get_test_run_summary` with `simulationRunId` until relevant tests leave `runningTestIds`.
3. `get_test_results` for detailed output from one failed test.

If MCP simulation tools are unavailable, validation is blocked. Do not substitute package-manager
commands or direct API scripts for a simulation run.

For nontrivial failures, sync the run locally:

```bash
pnpm sierra ghostwriter --sync-simulations --run-id <simulationRunId>
```

Then read `result.json`, `debug.log`, and only the relevant `traces/*.trace` files.

---

## 5. Iterate

When a test fails, identify the layer before editing:

- wrong journey or condition activated
- tool arguments or result behavior were wrong
- implementation branch did not match the simulated integration state
- expected outcome assumes behavior the tool never communicates
- policy/config contradicts tool-driven behavior

Fix the source of truth for the behavior, re-push when local files changed, and re-run the failing
test plus nearby tests that exercise the same branch.

---

## What makes a good simulation test

### Writing `accountState`

Before writing `accountState`, become the system simulator. Mentally assemble only what it sees: the
integration method name, description, parameter schema, call arguments, test group/name, the account
state you wrote, and prior integration method calls. It does not see the tool definition, tool
implementation, or conversation. Read the tool implementation and ask: given only the simulator's
context and this incoming method call, would I return the exact fields and values this code branches
on?

Write `accountState` as account facts from the integration's point of view, not as named tool
instructions. Include identifiers the customer will mention, records the integrations will search
on, and exact branch values such as `status 'delivered'`, `eligibility 'eligible'`, or
`case_state 'open'`. The simulator treats this as the starting snapshot and evolves it across calls;
if a method creates a return or cancels an order, later calls should reflect that mutation.

Use `initialMemory` when a branch depends on preloaded memory. Pulled files do not contain secret
values; preserving a pulled file preserves existing encrypted secrets server-side.

Use `mockToolData` only when the normal simulator setup cannot express the scenario. If a tool has
an `implementation.ts` and an integration, prefer `accountState` so the real code path runs.

### Writing instructions for the user simulator

The user simulator responds better when the prompt gives it a concrete persona to play and a clear
structure for the conversation.

#### Default recipe for non-trivial tests

1. **Situation** -- who the customer is, why they are reaching out, and any emotional or practical
   context that makes the conversation feel organic.
2. **Action map** -- what facts to provide when the agent asks. This is the default pattern for any
   simulation that collects structured data.
3. **Resolution** -- when to accept, decline, transfer, or end.

#### Ground the customer's persona

Customer tone and emotional state are part of the scenario. A frustrated customer may respond
differently than a patient one, and the agent should handle that pressure well.

The simulated user sees the full conversation history on every turn, including initial messages
defined through `simulationStartIndex`. It pattern-matches on earlier messages, so the first message
can set the tone for the entire conversation.

#### Use action mappings

Prefer action-mapped conditionals in the "If ..., then ..." format over loose natural-language
summaries once the scenario has more than one or two facts. When facts are spread across individual
conditionals, the simulator reveals them one at a time in response to the agent's questions --
mimicking how real customers behave. When all facts are packed into a single block of text, the
simulator tends to volunteer everything in one message, skipping the multi-turn collection flow
you're trying to test.

**When action-mapping matters most:** Any test where the agent collects structured data. If the
agent has a multi-step collection flow, each step needs its own conditional gate.

**Watch out for conditional sprawl.** Too many conditionals create their own problems:

- **Dead branches** -- if the agent never asks a question you wrote a conditional for, that branch
  is untested dead weight. It clutters the instructions and can confuse the simulation user about
  what's important.
- **Ambiguous routing** -- overlapping conditionals like "If the agent asks about your policy..."
  and "If the agent asks about changes..." can both trigger on the same agent question, leading to
  unpredictable simulation user behavior.

#### Subtle nudges that reduce drift

These are useful when the test needs the simulator to stay on one valid branch without turning the
whole prompt into a script. Prefer to use explicit prompting to tighten the following:

- Prefer one valid branch: when the agent offers several options, tell the simulator which one to
  choose.
- Bound scope and initiative: keep the simulator on the task at hand, answering the agent directly
  rather than opening new threads.
- Constrain verbosity: ask for short replies unless the agent requests more detail.
- Avoid invented details: limit the simulator to the facts you provide, and have it express
  uncertainty when asked for anything else.

### Every simulation needs a clear stopping point

Without one, the simulation user keeps asking questions and the conversation loops or times out.
Give the simulator an explicit cue to acknowledge success and end the conversation. Make it clear
whether to accept a transfer or not when the agent offers one.

### Choosing `tagExpectations` vs `expectedOutcomes`

Be opinionated here: **new tests should lean harder on `tagExpectations` than on
`expectedOutcomes`.** If the behavior can be checked deterministically with a tag, do that first.

| You want to verify...                        | Use              | Why                                             |
| -------------------------------------------- | ---------------- | ----------------------------------------------- |
| An action was taken (refund, transfer, tool) | Tag              | Deterministic, won't flake                      |
| An action was NOT taken                      | Tag (`!`)        | Negative tags are reliable                      |
| Journey/ conditional activation              | Tag              | Binary -- it routed or it didn't                |
| What the agent _said_ to the user            | expectedOutcomes | Tags can't see message content                  |
| Tone, empathy, brand voice                   | expectedOutcomes | Inherently subjective, needs LLM eval           |
| A specific price or value was quoted         | expectedOutcomes | Message content, not just "quote was generated" |

- If the behavior is a definite binary outcome but there is no tag for it yet, treat that as a sign
  that the journey may need better tagging. Do not reflexively paper over missing tags with more
  `expectedOutcomes` when the behavior should really be asserted deterministically. At the same
  time, avoid adding new tags if they are logically equivalent to existing ones.

#### Working with tags

Tags originate from block definitions, tool implementations, and the platform runtime -- see
[Tag assertions](.composer/docs/simulation-test-reference.md#tag-assertions-tagexpectations) for
where each comes from. When writing assertions:

- Read the relevant `.composer/blocks/` files and tool implementations first to see which tags
  already exist before writing assertions.
- Use tool-implementation tags (`sierra.addAgentTags([...])`) for tool branches that should be
  asserted deterministically, such as not-found, ineligible, or success outcomes.
- Always assert `transfer` where relevant -- it is a terminal action, so check `transfer` when it
  should happen and `!transfer` when it must not.

Well-tagged outcomes make tests more reliable and also make the behavior easier to monitor and
analyze elsewhere.

#### expectedOutcomes

`expectedOutcomes` rely on an LLM judge, which can misinterpret context. Vague outcomes will flake.
Write them like contract clauses -- specific enough that a reviewer could unambiguously judge
pass/fail from the transcript.

Use them only for things tags **cannot** verify -- primarily the content of what the agent said, not
whether an action occurred. This includes both highly specific conditions, like the agent quoting a
particular value, and qualitative assertions, like tone or empathy -- but either way, pin them to
observable behavior.

If something can be asserted with a tag, **do not** duplicate it under `expectedOutcomes`.

#### Writing Good expectedOutcomes

- **Test decisions, not steps.** A strong outcome is specific enough to fail when the agent skips an
  important decision:
    - Good: assert that the agent confirms a key decision before acting on it.
    - Weak: assert a routine intermediate step the agent will almost always take anyway.
- **Don't test exact phrasing.** Test behavioral decisions, not wording:
    - Good: assert that the agent takes the right action for the situation.
    - Bad: assert that the agent says a specific sentence verbatim.
    - Exception: required wording like legal disclaimers or mandated transfer language, where the
      content itself is the behavior. `expectedOutcomes` can be used if there is no clean way to
      assert this with a tag.
- One thing per outcome -- compound outcomes (the agent does X and Y) are harder for the evaluator
  to judge and give ambiguous pass/fail signals
- Avoid jargon -- the LLM evaluator won't understand internal terminology.
- **Outcomes must be measurable.** A reviewer should be able to judge pass/fail unambiguously.
- For **factual outcomes** (agent took an action, shared specific info), be precise and unambiguous.
- For **qualitative outcomes** (tone, empathy, brand voice), some subjectivity is inherent and
  that's okay -- these are the outcomes where expectedOutcomes add value that tags can't.

---

## Quality Bar

| #   | Criterion                        | Check                                                                           |
| --- | -------------------------------- | ------------------------------------------------------------------------------- |
| 1   | Test setup is intentional        | The file targets one clear branch or behavior                                   |
| 2   | Common regressions are covered   | Core customer paths have simulation coverage                                    |
| 3   | Tricky branches are protected    | High-risk tool, integration, and condition branches are exercised               |
| 4   | Integration state is explicit    | `accountState` carries the facts the system simulator needs                     |
| 5   | Condition branches are clear     | `initialMemory` is used when state changes behavior                             |
| 6   | Assertions use the right surface | `tagExpectations` cover binary actions; `expectedOutcomes` cover judged content |
| 7   | Customer messages are realistic  | Simulator instructions brief a customer, not the agent                          |
| 8   | Tests are stable                 | New tests pass repeated runs, not just one green run                            |
| 9   | Results are verified             | Runs are checked with `run_test` and `get_test_run_summary`                     |
