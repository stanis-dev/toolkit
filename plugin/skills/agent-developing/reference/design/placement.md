# Placement across the halves

Rules for allocating behavior between the code half and the no-code half.
Only rules the canonical skills cannot carry live here. Load the matching
canonical skill first through [canonical guidance](../session/canonical-guidance.md).

## Which half

Default to the no-code half. It is reviewable in Agent Studio and ships
without a repo deploy.

Before choosing the code half or writing any instruction text, enumerate
the no-code candidates from the materialized workspace. Read the quick index in
`.composer/docs/block-reference.md`, the workspace's connected packages
and their schema refs under `.composer/config/integrations/`, and
`.composer/docs/platform-capabilities.md` for what stays outside
ghostwriter. The materialized copies match the released bundle. When those
references leave a capability unresolved, ground it with
`ask_sierra_assistant` instead of assuming. A behavior a block, package,
or deterministic setting covers stays no-code.

Use the code half when any line applies.

- The behavior needs an SDK-only construct: hooks, monitors, experiments,
  PromptContext.
- The behavior serves more than one agent in the repo.
- The tool meets the tool_ref criteria in
  `.composer/docs/tool-block-reference.md`.
- The behavior is a natural extension of existing code, such as a new
  branch or field in a code tool that already carries the logic.

When the agent lives in one half today, prefer that half. The first file
in the other half is a step change in complexity.

Then check ownership: place the behavior in the half whose owner changes
it. To move existing code, follow
`.composer/.claude/skills/migrate-code-to-nocode/SKILL.md`.

## Which surface carries an instruction

Before writing an instruction, prefer a mechanism that removes it. In
order: fold a fixed call sequence into one implementation, use the
deterministic tool settings, gate context behind root-store conditions,
compute the guidance in the tool return, and write static text last.

Then test ownership: move the tool to another journey. If the instruction
still holds, it is tool-intrinsic and lives on the tool surface. The tool
surface is the only text present wherever a `tool_ref` activates the
tool. Otherwise the instruction lives in a block. Call protocols are
always tool-intrinsic: call order, one call per item, cursors, a token
one call produces and the next consumes. Split a protocol: the
description carries the static summary, and the return computes the next
step from the protocol's current state. Read [tool results](tool-results.md)
before designing that return, [prompt lifetime](prompt-lifetime.md) when
the guidance expires, and [authoring](../writing/authoring.md) before
writing the instruction. For a no-code edit, read [ghostwriter](../session/ghostwriter.md).

## Boundary sweep

Run the review-agent-context checks across both halves together.
Cross-half drift has no owner: the halves have different authors.
Two checks are boundary-specific.

- A code tool's description must stand alone. Its author cannot assume
  any journey text renders beside it.
- After a code deploy changes a tool's protocol, re-read every block that
  names the tool. No lint catches stale protocol text in the other half.

Before judging the cross-half change complete, apply [correctness review](../gates/verification.md).
