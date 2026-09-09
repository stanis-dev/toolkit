# Correctness review gate

This is an evidence-backed review over the paths the change can reach, not a proof over an unbounded input space. Older text that says "theoretical correctness gate" means this gate. Run it alongside the [simulation gate](testing.md); the two are independent.

For SDK evidence, load the canonical skill per [canonical guidance](../session/canonical-guidance.md) and select the affected mechanics through [SDK routing](../design/sdk.md) or [rendering routing](../design/rendering.md), not every design file. Before delegating a slice or transferring evidence, read [handoff](../writing/handoff.md).

1. Record the reviewed artifact: the code commit or working-copy identity, the no-code version, the relevant configuration, and the dependency assumptions.
2. Map the affected callers, journey branches, boundary values, store and memory states, tool failures, and render timing. Include null, empty, and overflow cases where relevant.
3. Inspect the implementation and the SDK evidence for each path. Cite the exact source at file:line and explain why the requirement holds or how it fails. Eliminate from read code, not recalled SDK behavior.
4. Challenge the map for missed branches and unsound assumptions with concrete counterexamples. A second perspective must test the argument, not vote on it.
5. Report supported paths, confirmed defects, and unresolved required evidence separately. Name the triggering input or the missing check for every blocking item.

A confirmed defect blocks the gate. Missing evidence needed to establish an affected path also blocks it, but is not itself a defect. Only an explicit per-change waiver from the user permits completion without the evidence. Record the waiver and its scope. Do not turn speculation into unrelated cleanup.

When production data covers a scenario, prefer the empirical check: a transcript, a query count, or a replay per [LLM replay](llm-replay.md).

## Review execution

The lead owns coverage and the final verdict. Review directly when the change fits one bounded pass. When independent risk areas exist, assign bounded slices to subagents and choose their number from the slices and the budget, not from a fixed quota.

Give each reviewer the diff, the artifact identity, the requirements, the relevant references, and the permitted evidence sources. Reviewers return findings and gaps only. They do not provision workspaces, edit, ship, or spawn more reviewers. The lead continues non-overlapping work while they run.

Recheck every finding against the code. Fix supported defects and rerun the affected checks. Stop when the map is supported and no blocking item remains. Do not repeat a clean review to raise the reviewer count.

## Evidence freshness

A verdict belongs to its artifact. A code edit, a no-code edit, a configuration change, a fixture change, or a relevant merge-base change invalidates the affected conclusions. Identify the impacted paths and rerun their review and simulations. An unchanged, unrelated path keeps its evidence with an explicit reason.

Report both gates together: the run references, the coverage map, the unresolved items, and the final tested artifact. A summary or an earlier session's confidence is not evidence.
