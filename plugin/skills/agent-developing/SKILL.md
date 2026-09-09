---
name: agent-developing
description: End-to-end workflow for developing Sierra agents, from wiring the agent-dev environment and editing the code and no-code halves via ghostwriter, through the simulation and correctness-review gates, to shipping via PRs, snapshots, and releases. Use for any change to a Sierra agent, whether code, journeys, blocks, knowledge, tests, or release work.
---

# Developing Sierra agents

A Sierra agent has two halves. The code half lives in a repo's `agents/{agent}` folder, and one repo can host several agents. The no-code half lives in Agent Studio: journeys, blocks, knowledge, tests, issues. A build deep-merges the code with the workspace's no-code version into one deploy artifact, so code and no-code changes ship atomically within the same workspace. Reason about the merged result only. Edit the no-code half locally with the ghostwriter CLI. Use the Sierra MCP for conversations, LLM calls, knowledge, and reports.

Memorized flags, block schemas, tag meanings, and code shapes drift. Discover commands with `--help` at use time. The `sierra-inc/sierra` monorepo and `sudo_search_docs` are unreachable in this environment. The materialized `.composer/docs` and `.composer/.claude/skills` bundle is the grounding for agent-building concepts, and `ask_sierra_assistant` fills what the bundle leaves open.

## Procedure

1. Identify the requested outcome, the agent, and the scope. For an assessment, answer without provisioning, editing, or shipping. For a delegated review, review only.
2. Check the current environment, permissions, and loaded tools. Reuse a verified thread workspace. Configure a missing capability only when the task needs it (reference/session/setup.md).
3. Read the references for the affected areas. Before an agent edit, load the matching canonical skills from the materialized bundle (reference/session/canonical-guidance.md). If required guidance is unavailable, report that before the affected edit.
4. Locate the behavior across both halves. For a production defect, verify the mechanism in a real conversation before designing the fix. Without that evidence, label the mechanism unverified and keep its verification outstanding.
5. Make the smallest complete change within scope. Touch only the code and blocks the behavior requires. Report unrelated findings separately. Split a change too large for one reviewable PR at scoping time (reference/shipping/lifecycle.md).
6. Clear both gates against the final change, in parallel: the simulation gate, every affected path asserted and five consecutive passing runs, and the correctness review. Where this skill says "the gate", read both. An unresolved defect, missing required evidence, or a 4-of-5 result blocks completion. Only the user can waive a gate, explicitly and per change; a waiver never carries over.
7. For implementation work, follow reference/shipping/lifecycle.md through the authorized completion point. State what changed, what was verified, what remains blocked, and who owns the next action. A PR, a snapshot, and a release are three distinct outcomes.

## Boundaries

- Skill text grants no permission. Follow the active system and tool instructions for authorization, data access, repository actions, and session management. When a conflict blocks work, name the conflicting instruction and continue the independent permitted work.
- Keep customer conversation data inside its approved environment. A summary, an identifier, or a paraphrase can still be sensitive. Read reference/writing/handoff.md before moving evidence between sessions.
- Verify before you assert. Behavior cites code at file:line. Conversation events cite the transcript or turn trace. Tag meaning cites emission logic. Frequency and impact cite a query. Simulation runs cite their JSON output, not the judge's summary. Mark unchecked claims unverified.
- Do not repeat a successful verification without a changed artifact, a failure, or a concrete unresolved risk. Do not expand a test run to the whole suite for general confidence. Any later behavior-affecting edit invalidates the affected gate results.
- Refactors, renames, and drive-by cleanup are separate steps after the gates are green.
- Write direct prose. Lead with the result and preserve uncertainty where evidence is incomplete. Load reference/writing/authoring.md for authored prompts, tags, or documents, not for every routine reply.
- After a context summary or a handoff, restore the scope, the artifact identity, the decisions, the unresolved checks, and the authorized next action. Reread the references no longer in context. A summary is not evidence that a gate passed.

## Required reference loading

A reference file's rules bind only while its text is in your context. Before the next read, edit, command, or diagnosis, scan the triggers below and read every matching reference not already in context. Match both the requested task and the mechanisms discovered in the code or the failure. A task can match several rows. Follow a leaf's explicit conditional prerequisites only when that condition applies; do not load a whole directory.

Recheck the triggers when the scope changes, a new failure appears, or context is compacted. Before claiming an action complete, confirm its matching references were read.

### Environment and no-code

- A fresh session, or changing workspace setup: [setup](reference/session/setup.md).
- Registering, watching, uploading, or deleting a CLI workspace: [workspace CLI](reference/session/workspace-cli.md).
- Connecting, reloading, or diagnosing a stale MCP target: [MCP connection](reference/session/mcp-connection.md).
- Before any code or no-code edit: [canonical guidance](reference/session/canonical-guidance.md).
- Editing or pushing no-code resources: [ghostwriter](reference/session/ghostwriter.md) and [ghostwriter files](reference/session/ghostwriter-files.md).
- Ghostwriter credential minting, a scope error, or a legacy `--sync`/`--upload` recipe: [ghostwriter credentials](reference/session/ghostwriter-auth.md).
- An authorized direct API request using the CLI session, or a cookie, CSRF, token, or User-Agent diagnosis: [API authentication](reference/session/api-auth.md). Normal MCP reads do not trigger it.
- Model selection or a model-specific failure: [models](reference/session/models.md).

### Agent mechanics

- Allocating behavior across code and prompts, or choosing which surface carries an instruction: [placement](reference/design/placement.md).
- Tool return values, `controls.result`, or instruction channels: [tool results](reference/design/tool-results.md).
- `createAgent`, config overrides, or compatibility dates: [agent config](reference/design/agent-config.md).
- Log calls, error serialization, visibility, or alerting: [logging](reference/design/logging.md).
- Cross-turn state, clocks, globals, JS features, or React-like SDK APIs: [runtime and state](reference/design/runtime-state.md).
- Conditional rules, transient guidance, or tool availability: [prompt lifetime](reference/design/prompt-lifetime.md).
- Observation Conditions, `OnActivation`, latching, or re-arming: [observations](reference/design/observations.md).
- `useAgentMonitors`, final replies, or Condition and monitor migration: [monitors](reference/design/monitors.md).
- Abuse detection and guardrails: [abuse](reference/design/abuse.md).

### Testing and evidence

- Simulation coverage, the pass bar, or gate diagnosis: [testing](reference/gates/testing.md).
- Running simulations, selecting names, or parsing the verdict: [simulation CLI](reference/gates/simulation-cli.md).
- Tag assertions, judge wording, markup, or fixture clocks: [assertions](reference/gates/simulation-assertions.md).
- Conversation or result IDs, transcripts, raw LLM calls, or result API access: [result access](reference/gates/simulation-results.md).
- Knowledge setup failures, network timeouts, or egress allowlists: [networking](reference/gates/simulation-network.md).
- Replaying an observed LLM failure under a changed prompt: [LLM replay](reference/gates/llm-replay.md).
- Correctness review and evidence freshness: [verification](reference/gates/verification.md).

### Shipping and output

- Cleanup, PR scope, snapshots, releases, or workspace deletion: [lifecycle](reference/shipping/lifecycle.md).
- Authenticated GraphQL snapshot or release calls: [release API](reference/shipping/release-api.md).
- PR titles or descriptions: [PR descriptions](reference/shipping/pr-descriptions.md).
- Workspace conflicts or foreign objects in a diff: [conflicts](reference/shipping/conflicts.md).
- A released change on live traffic: [monitoring](reference/shipping/monitoring.md).
- Prompt text, tags, or document style: [authoring](reference/writing/authoring.md).
- An ASCII diagram in any habitat: [diagrams](reference/writing/diagrams.md).
- Work transferred between sessions: [handoff](reference/writing/handoff.md).
- Changing this skill's workflow or model guidance: [evaluation](reference/maintenance/evaluation.md).
