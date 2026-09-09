# PR descriptions

Apply this reference to agent and persona repository PRs. Platform repositories use their own conventions. A PR body is Markdown.

Write only what the diff cannot explain: intent, relevant context, blast radius, decisions, verification, and risk. Scale detail with the reviewer's needs, not with the length of the conversation or the diff. Follow [authoring](../writing/authoring.md).

## Contents

Open with a concise description of the behavior change and its scope. Distinguish merge, snapshot, and release effects.

- Explain the motivation and the verified mechanism. Cite permitted sources and existing work items. Include rejected alternatives only when they explain a material decision.
- Describe the affected code and no-code surfaces. For a non-obvious flow or a cross-half change, add a schematic per [diagrams](../writing/diagrams.md). Do not invent a diagram for a trivial leaf edit.
- Report the final tested artifact, the named commands, the run references, the actual pass counts, and the correctness-review result. State missing checks and per-change waivers prominently. Simulations require five consecutive passing runs per [testing](../gates/testing.md).
- State rollback, deployment dependencies, and remaining risk. Include locale, observability, experiment, or latency effects when relevant. Verify reply-path timing from the implementation before making a latency claim.
- Record material decisions and deliberately excluded follow-ups. Include stack dependencies or a reading order only when useful.

Use short prose by default. Fold a long coverage map or supporting detail in a `<details>` block, with a blank line after the `</summary>` tag so the Markdown inside renders. Keep blockers, waivers, residual risk, and conclusions visible without opening a fold. Remove repeated explanations, not the evidence needed to judge readiness.

## Evidence and privacy

Include only evidence permitted in the repository and accessible to the intended reviewers. Audit IDs, simulation identifiers, and synthetic-looking transcripts are not automatically safe. Keep restricted customer content and identifiers in their approved environment. A link does not itself establish permission to publish its target's details.

Use the final valid run for the headline. Keep a concise account of material failures, judge corrections, and unresolved flakes with permitted references. Do not hide a failure history to imply a clean first attempt. An exemplar conversation supports a claim; it is not exhaustive proof.

Do not invent absent identifiers, issue links, or measurements.

## Title and updates

Write an imperative, sentence-case title describing the behavior change, with no trailing period and no ticket IDs. Prefix with the agent scope (`<agent>:`) when the repo hosts more than one agent.

This file governs content, not permission to create or edit a PR. Follow [lifecycle](lifecycle.md) and the repository's workflow. Update a title or body only when asked or when that workflow requires it, with current facts and recomputed figures.

If a gate is pending, report it as pending. An open draft is not ready for review or shipping. After both gates pass against the final artifact, report readiness without inventing a merge approval.

When a footer is appropriate, identify `agent-developing`.
