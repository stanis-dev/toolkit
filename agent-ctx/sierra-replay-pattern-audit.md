# Sierra Replay Pattern Audit -- Cross-Referenced Findings

**Corpus**: 162 transcripts across Cursor (4 workspaces), Codex CLI, Claude Code, OpenCode
**Sierra-relevant**: ~83 transcripts analyzed in depth
**Method**: 4 independent sub-agents, deep-eval protocol, cross-referenced

---

## Tier 1: Independently Found by 3+ Agents (Highest Confidence)

### 1. Analysis-to-Implementation Boundary Violation

**Found by**: All 4 agents | **Frustration**: EXTREME | **Current coverage**: One buried sentence

The single highest-impact gap. Every evaluation session opens with "analysis only" but agents routinely cross into implementation. Triggered the most explosive correction in the entire corpus:

> "Do not apply the fucking fixes. I wanted to fucking report on the failures on the failing triage simulations." -- `de6dc65b`

Other evidence: "revert changes. i don't want to do anything yet" (`d543720f`), "I don't really want to create, I don't want to have any action" (`7f5609ca`), analysis-only scope stated in 15/22 Sky transcripts, 18+/32 newer Pronet transcripts.

**Current skill text** (`sierra-powertool` Interaction Rules): *"If the user asks for a report, analysis, or investigation, deliver that. Do NOT start implementing fixes unless the user explicitly asks."* -- This exists but is ineffective; agents ignore it.

**Recommendation**: Promote to top-level HARD CONSTRAINT in `sierra-best-practices`. Add a three-phase model with explicit transition signals:

```
Phase 1 (Analyze): "help me understand", "I want to explore", "just analysis"
Phase 2 (Review): User reviews findings, asks questions
Phase 3 (Implement): "let's implement", "go ahead", "let's fix this", "let's do it"
```

---

### 2. Sim User LLM Verification Before Evaluating Pass/Fail

**Found by**: Agents 1, 2, 3 | **Frustration**: VERY HIGH | **Current coverage**: None

The user's most frustrated corrections stem from agents treating sim results as meaningful without first verifying the sim user LLM behaves correctly:

> "we are focusing way too much on passes and fails. before we even begin to consider that we must absolutely ensure that the actual conversations are following the exact scenario" -- `79e587f8`

> "i don't like that customer asked themselves for that. we want customer llm to represent a real customer behaviour" -- `33160d08`

> "do not adapt anything in sims to meet agent capabilities pre-planned implementation" -- `1b72b8ec`

The existing skill says "Simulation TDD" but never describes what happens between "sim created" and "start evaluating." The missing step: verify sim user behavior independently over 3+ runs.

**Recommendation**: Expand `sierra-best-practices` Simulation TDD section with mandatory verification step.

---

### 3. Standard Evaluation Protocol (Repeated Verbatim Every Session)

**Found by**: Agents 1, 2, 3 | **Frustration**: Low per-instance, HIGH cumulative | **Current coverage**: None

The same scope -> run -> wait -> fetch -> analyze -> track sequence appears in 30+ transcripts across both workspaces. The user re-explains it every session because skills document individual commands but not the end-to-end workflow:

> "grab all the simulations that are related to tags or names, as requirements... run five runs per each simulation, fetch their replays and provide me an overview on per condition basis" -- `77f031d0`

Defaults that should be codified: 5x per sim (evaluation), 10x per sim (regression), per-condition breakdown, tracker in `agent-ctx/`, emoji for pass/fail.

**Recommendation**: New "Evaluation Protocol" section in `sierra-powertool` with the full sequence and defaults.

---

### 4. Workspace Management and Cleanup

**Found by**: Agents 1, 2, 3 | **Frustration**: MEDIUM-HIGH | **Current coverage**: Partially (one sentence)

"Delete all workspaces except default" appears in 11/32 Pronet transcripts alone. Wrong org/bot targeting wasted entire sessions:

> "Oh my god, yeah, we just wasted a ton of time because you did the analysis on the wrong project" -- `77f031d0`

> "Also ignore all other workspaces. We only want to work against the default and what is in the default." -- `33160d08`

**Recommendation**: Dedicated workspace lifecycle section in `sierra-best-practices`.

---

### 5. Output and Tracking Conventions

**Found by**: Agents 1, 2, 3 | **Frustration**: Low | **Current coverage**: None

Consistent across all workspaces: analysis artifacts go to `agent-ctx/`, markdown tables with emoji pass/fail, summary stats at top, per-condition details below. File naming: `transcripts-<topic>-<date-range>.md`, `<descriptive-name>.md`.

> "could you please substitute this status fail and pass for uh like I guess emoji so it's a little bit more visual?" -- `2f00b689`

> "put them into agent-ctx folder and keep them in a single dir to avoid creating noise in the root dir" -- `5f57fb8d`

**Recommendation**: New "Analysis Output Conventions" section in `sierra-best-practices`.

---

## Tier 2: Found by 2 Agents (High Confidence)

### 6. Tag-Based vs Judge LLM Evaluation Selection

**Found by**: Agents 1, 2 | **Frustration**: HIGH | **Current coverage**: None

The user consistently prefers tags for binary assertions and reserves judge LLM for subjective quality. Agent 2 found the pivotal moment: a judge LLM marked a sim as PASSED when the agent technically mentioned card first but semantically committed to bank transfer (`33160d08`).

**Recommendation**: Add evaluation-type selection guidance to `sierra-best-practices`.

---

### 7. Conversation Batch Analysis Workflow

**Found by**: Agents 2, 3, 4 | **Frustration**: MEDIUM-HIGH | **Current coverage**: None

The fetch -> save -> batch-classify -> extract workflow appears in 13+ transcripts but has zero documentation:

> "filtering issues by pattern matching is ineffective. reporters are highly inconsistent... we'll need to use llm eval per each issue" -- `d1a1ab42`

> "this is not evaluating each conversation as conversation, but attempts to find a shortcut" -- `1b72b8ec`

**Recommendation**: New "Conversation Analysis Workflow" section in `sierra-powertool`.

---

### 8. Plan-File Driven Workflow

**Found by**: Agents 3, 4 | **Frequency**: 23+ transcripts | **Current coverage**: None

Identical boilerplate in every implementation session:

> "Implement the plan as specified... Do NOT edit the plan file itself. To-do's from the plan have already been created. Do not create them again." -- appears verbatim in 23+ transcripts

This is cross-cutting (not Sierra-specific) but dominates Sierra sessions.

**Recommendation**: This belongs in a session-start hook or agent convention, not a Sierra skill.

---

### 9. Regression Protocol (10x, Baseline, Diff)

**Found by**: Agents 1, 2 | **Frustration**: MEDIUM | **Current coverage**: None

> "let's do a full regression run - all sims, 10x per sim vs the default workspace" -- `3ac10e24`

Standard: create baseline workspace, bench start on both with `--count 10`, `sim diff`, re-run flaky individually before declaring regression.

**Recommendation**: New "Regression Protocol" section in `sierra-powertool`.

---

## Tier 3: Unique to One Agent (Signal, Needs Validation)

### 10. --no-cache Flag Abuse (Agent 1)

5/22 Sky sessions, always HIGH frustration:

> "Why the fuck did you add no cash flag? This is slowing everything down to a fucking crawl." -- `2f00b689`

> "DO NOT USE --no-cache tag!!!" -- `67423aef`

**Recommendation**: Explicit guardrail in `sierra-powertool`.

### 11. Phrasing Propagation Architecture (Agent 3)

Journey phrasing, brand voice, progress indicators, and respond_paraphrase all have different propagation scopes. The user had to empirically discover this (`d4167b74`):

> "journey level phrasing instructions: propagate to main response [YES], propagate to ad-hoc Respond blocks [NO], propagate to latency fillers [NO]"

**Recommendation**: Add propagation matrix to `sierra-best-practices`.

### 12. Trace Data Awareness (Agent 3)

Agents don't know what's in traces until told. The sim user LLM system prompt is accessible via `--json` but the agent claimed it was "a black box" (`94d00578`).

**Recommendation**: Expand "What Traces Expose" in `sierra-powertool`.

### 13. Journey vs Code vs System Prompt Decision Framework (Agent 4)

Where to put behavior changes? Missing entirely:

> "there are some instructions in code or in journey that essentially are overlapping with probably some of the system prompting" -- `5694c1aa`

**Recommendation**: Decision framework in `sierra-best-practices`.

### 14. Pink Elephant Problem in Skill Writing (Agent 4)

> "let's avoid using negatives. i'd rather avoid those in order to avoid the 'pink elephant' problem" -- `a4d344b0`

**Recommendation**: Applies to `skill-engineer` skill, not Sierra skills directly.

### 15. Journey Rule Format: Bullet Points Over Prose (Agent 1)

> "the CRSDK and specifically the studio requires much more of a bullet point approach" -- `60e8d024`

**Recommendation**: Add to `sierra-best-practices`.

### 16. Sim User Instructions in English (Agent 2)

> "customer llm instructions are in turkish, but should be in english. llm will generate Turkish on its own thanks to the locale setting" -- `1eff163d`

**Recommendation**: Add to `sierra-best-practices` simulations section.

### 17. Turkish Conversation Translation (Agent 2)

> "save them all into a file and translate them so that i can understand" -- `2b2b5cf8`

Appears in 5/32 Pronet transcripts. Pronet conversations are in Turkish.

**Recommendation**: Pronet-specific; may not generalize. Add as a note.

---

## Skill Mapping: What Goes Where

### `sierra-best-practices` (workflow rules, anti-patterns, guidelines)


| #   | Section                                                  | Content                                                                                                                              | Priority |
| --- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | -------- |
| 1   | **Analysis-to-Implementation Protocol** (NEW, top-level) | Three-phase model, transition signals, HARD boundary                                                                                 | P0       |
| 2   | **Simulation TDD** (EXPAND existing)                     | Mandatory sim user verification step, 3+ run check                                                                                   | P0       |
| 3   | **Workspace Lifecycle** (NEW)                            | Cleanup ritual, baseline creation, experiment isolation                                                                              | P1       |
| 4   | **Analysis Output Conventions** (NEW)                    | agent-ctx/ directory, file naming, table format, emoji                                                                               | P1       |
| 5   | **Evaluation Type Selection** (NEW)                      | Tags for binary, judge LLM for subjective, when each                                                                                 | P1       |
| 6   | **Journey Rule Design** (NEW)                            | Bullet-point format, step-back methodology                                                                                           | P2       |
| 7   | **Instruction Deduplication** (NEW)                      | Check system prompt before adding journey rules                                                                                      | P2       |
| 8   | **Sim User Instructions** (add to Simulations ref)       | English instructions, locale handles language                                                                                        | P2       |
| 9   | Anti-patterns table (EXPAND)                             | Add: "Focus on pass/fail before verifying conversation", "Pattern matching for issue classification", "Adapt sims to avoid failures" | P1       |


### `sierra-powertool` (CLI reference, debugging, command sequences)


| #   | Section                                              | Content                                                             | Priority |
| --- | ---------------------------------------------------- | ------------------------------------------------------------------- | -------- |
| 1   | **Evaluation Protocol** (NEW)                        | Full scope->run->wait->fetch->analyze->track sequence with defaults | P0       |
| 2   | **Guardrails** (EXPAND)                              | --no-cache ban, run ownership (multi-agent coordination)            | P0       |
| 3   | **Sim Filtering** (NEW or expand)                    | --tag vs --group vs --category behavior differences                 | P1       |
| 4   | **Conversation Analysis Workflow** (NEW)             | conv list->show->save->batch-classify with LLM eval                 | P1       |
| 5   | **Regression Protocol** (NEW)                        | 10x, baseline workspace, sim diff, flaky re-run                     | P1       |
| 6   | **What Traces Expose** (NEW)                         | --trace vs --json, sim user prompt access, platform-level calls     | P2       |
| 7   | **Per-condition Analysis Fields** (expand Debugging) | outcomeEvalResults, tagExpectations, judge reasoning                | P2       |


### Not Sierra-specific (other skills)


| Finding                                | Target                                 |
| -------------------------------------- | -------------------------------------- |
| Plan-file driven workflow boilerplate  | Session-start hook or agent convention |
| Pink elephant problem in skill writing | `skill-engineer` skill                 |
| Zero-trust review subagent pattern     | General development convention         |
| Turkish conversation translation       | Pronet-specific local config           |


---

## Decision Point: New Skill vs. Extending Existing?

The evaluation-specific patterns (Evaluation Protocol, Regression Protocol, Tag Taxonomy, Per-Condition Analysis, Output Conventions) form a coherent workflow. Options:

**Option A: Keep in existing skills.** Add ~7 new sections across `sierra-best-practices` and `sierra-powertool`. Pro: fewer skills to trigger. Con: skills get long.

**Option B: Extract `sierra-eval-protocol` skill.** Move all evaluation/analysis workflow content there. Pro: clean separation of "how to develop" vs "how to evaluate." Con: one more skill to invoke.

Current `sierra-best-practices` is 77 lines. With the additions it would be ~200. Current `sierra-powertool` is 328 lines. With additions it would be ~450. Both are within reason for a skill file. Recommend **Option A** unless the skill sizes feel unwieldy after implementation.