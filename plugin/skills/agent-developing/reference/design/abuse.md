# Abuse detection and guardrails

Before changing a config override, read [agent config](agent-config.md). For a custom defend instruction, read [tool results](tool-results.md) and [authoring](../writing/authoring.md). For threshold state across turns, read [runtime and state](runtime-state.md). Before verifying a change, read [testing](../gates/testing.md), [assertions](../gates/simulation-assertions.md), and [correctness review](../gates/verification.md). For transcript or raw-call diagnosis, read [result access](../gates/simulation-results.md). The Studio-side record is owned by the canonical `update-config` skill.

One classifier serves several wrappers. On the input side, the base agent
wires in `DetectAbuse`, the customer layer, configured from Agent Studio
plus code overrides. The runtime also injects `DetectAbuseCore`, the Sierra
layer for system safety and org backdoors. It is not yours to configure. On
the output side, `DetectAgentAbuse` classifies the agent's own messages. It
is opt-in agent code with its own injected core sibling. The wrappers live
in the monorepo (`journeys/sdk/skills/guardrails/`, classifier task in
`journeys/sdk/tasks/detect-abuse/`), unreachable in this environment. The
local SDK bundle ships only their types.

## Configuration

Agent Studio's Guardrails system package writes the guardrails config
record. In the materialized workspace it is `config/base/*sdk-abuse*.json`
with `entry_name` `sdk:abuse` and type `CoreAbuseConfig`; upstream docs
call the content entry `sdk:detectAbuse`. Legacy agents still read the
`errors` entry, and a migration marker decides which one the base agent
and the backend read. After migration the global mode is defend-only:
terminate or transfer. Core categories stay in defend mode and cannot be
disabled. Non-core categories can be disabled, observed, or given
thresholds and refocus messages. Reserve observe mode for trusted traffic.
A backend policy enforces the core-category rule even against direct CMS
writes. The category list and its core flags live in the content schema
and beside the wrappers. The standard list varies by `agentSafetyVersion`.

Code overrides go through `useCustomAbuseDetectionProps` on `createAgent`.
Merge semantics depend on `agentSafetyVersion`: old versions replace the
resolved base props wholesale, and newer versions deep-merge. The version
branch lives in the monorepo's `journeys/sdk/base/main.tsx`, unreachable
here: before assuming a Studio default survives a code override, confirm
the merge behavior for the agent's safety version with
`ask_sierra_assistant` or a trace. On the replace path,
`~abuse-overridden-key:*` tags mark the base keys that were dropped.

Return a custom defend action as a message instruction. A JSX component
such as `<Respond>` clears agent state and breaks the threshold count.

`DetectAgentAbuse` is configured only in code: categories, deterministic
checks, and rewriters. LLM categories disable streaming for the agent.
Deterministic checks and rewriters keep it. On voice,
`enableOnUserMessageType` limits the latency cost: output checks stay off
until a user message matches a listed behavior.

`AbuseAsyncPermissions` controls what the agent can do while classification
is pending: progress indicators, action tools, and mutations. A non-GET
Sierra `fetch` is a mutation even inside an allowed action tool. Before
you move a tool call or mutation earlier in the turn, read it.

## Behavior and debugging

A detection can refocus, transfer, terminate, and redact the flagged user
message. A refocus preserves agent state, so the per-category threshold
keeps counting. On voice, when every defend-mode detection looks like a
mistranscription, defend is suppressed.

Verify the resolved config, not the intended one. The `detect_abuse_init`
event captures the effective mode and categories. Traces name the layer:
`detect_abuse` is the customer layer and `detect_abuse_core` is the Sierra
layer. Debugging the wrong layer is the common dead end.

The `sierra-inc/sierra` monorepo is unreachable in this environment. When
the wrappers and the local SDK bundle leave a mechanism unresolved, ground
it with `ask_sierra_assistant`. The docs site covers the customer-facing
surface in the "Agent safety" guide, the Guardrails section of the
configuration guide, and the safety reference pages (DetectAbuse,
DetectAgentAbuse, AbuseAsyncPermissions). The reference pages carry the
current and deprecated category lists and the defend-action examples.

The gates apply in full to an abuse change. Drive each changed category
in a simulation and assert on its tag and the resulting action.
