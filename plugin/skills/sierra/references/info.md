# Information Formatting

You must maximise the ease with which I absorb the information.

## Renderer selection

Choose by the capability exposed in the current client, not by the model name:

- When `mcp__visualize__show_widget` is available, use the Claude Code renderer below.
- When Codex exposes its `visualize` skill and inline visualization content references, read
  [codex-widgets.md](./codex-widgets.md) and use the Codex renderer.
- When neither inline renderer is available, use the text fallback below.

The renderer changes only the delivery mechanics. The selected widget variation and its HTML
template define the required structure, order, rows, and data. Preserve them exactly. Replace
placeholders with evidence; do not redesign the layout, add diagnostic sections, or substitute a
different artifact type.

## Shared widget rules

- The widget holds only what the selected variation requires. Explanations and caveats stay
  outside unless that variation explicitly includes them.
- Content remains verbatim in its source language; chrome is English.
- Use no emoji and only font weights 400 and 500.
- Use one widget per answer.
- When revising a widget, render the complete widget again with a new version suffix.
- Optional sections are omitted unless their documented condition is met.

## Claude Code renderer

When `mcp__visualize__show_widget` is available:

- Call its `read_me` once before the first widget in the session.
- Start from the selected template under `widgets/`.
- Replace its placeholders without changing the template's structure.
- Use the preloaded Tabler icons and Claude theme tokens.
- Keep the template's edge-to-edge document reset and post-render padding adjustment.
- Render immediately with a versioned widget title.

## Widget variations

### Studio Context

When to use: I ask which part of the context teaches, allows or causes some behaviour; step 4
of agent-diagnose (the responsible context); the current state of a block before proposing an
edit to it. Reference: [widgets/studio-context.html](./widgets/studio-context.html).
Sources: the block files under `.composer/blocks/` and tool descriptions in code. When the
conversation being diagnosed saw a different version than the files hold, render what the
model saw and say so in the message.

Layout, top to bottom:

1. Optional summary row, when the answer is a pattern across places (e.g. one trigger worded
   four ways). Two columns, one per role, each a short list keyed `A1… / B1…`; the same keys
   appear as superscripts on the highlighted spans below. One muted closing line for the
   single fact that the reader would otherwise have to work out.
2. One section per place, in the order the model reads them.
   - The header is the breadcrumb: icon plus display name for each ancestor in
     `--text-secondary`, the current block last in `--text-primary` at weight 500, `›`
     separators. No sibling ordinals, no type words once an icon carries the type, no predicate
     icons on the path. Code tools carry `path/file.ts:line` in mono on the right.
   - Icons: `ti-folder` section, `ti-route` journey, `ti-file-text` custom, `ti-list-check`
     rules, `ti-git-branch` condition, `ti-book` glossary, `ti-gavel` policies,
     `ti-message-language` response phrasing, `ti-puzzle` component, `ti-tool` code tool,
     `ti-eye` observation predicate, `ti-database` rootStore predicate. A supervised rule inside a condition is one path segment
     with `ti-shield` in `--text-danger`; the shield replaces the branch and list-check icons and
     repeats on the store predicate row inside.
   - Body rows mirror the rendered context: a 64px right-aligned mono gutter pinned to the first
     line of the row, holding `-` for every list item and the number only when the item's own
     text starts with `1.`; a tool description or a gate row carries no marker. Sublist items
     are rows of class `sub`, whose gutter is 24px wider so the text indents like the render.
   - Conditions are one compact panel: 2px left rule, mono 11.5px, line-height 1.35, one
     predicate per line with an inline icon and `if` / `or` / `and` key, muted because it is
     machine-evaluated and not prose the model reads.
   - Neighbouring items in `--text-muted`, the items that matter in `--text-primary`. Long
     irrelevant middles become `(…)` with the full text in a `title` tooltip. Runs of skipped
     items become one italic muted row saying how many and what they are about.
   - Highlights by role, two ramps at most: `--bg-warning`/`--text-warning` and
     `--bg-accent`/`--text-accent`. Tool names inside prose in mono.

### Issue Analysis

When to use: step 1 of the workflow. What each part holds is in [issues.md](./issues.md);
this section is how it is drawn. Reference:
[widgets/issue-analysis.html](./widgets/issue-analysis.html).

Layout, top to bottom:

1. Header on `--surface-1`: issue number in mono, the type icon (`ti-bug` bug in
   `--text-danger`, `ti-arrow-up-circle` improvement, `ti-message-2` naturalness,
   `ti-text-recognition` update wording, `ti-volume` TTS, `ti-ear` STT) with the type word at
   weight 500, then the title. Right side in muted mono: `reporter · N calls · DD/MM`. Every
   header item is a 20px flex row so number, icon and text share one axis.
2. Two cells split by a hairline. Left: the reporter's words in `--text-muted` italics, the
   meaning below in body text. Right, headed "Closes it": one line, icon plus name
   (`ti-webhook` post-conversation hook, the block's own icon from Studio Context for a Studio
   block, `ti-tool` a tool, `ti-settings` a config record).
3. "Call": rows on the 64px gutter grid. Speaker icons in the gutter: `ti-robot` agent,
   `ti-user` caller, `ti-tool` tool call, `ti-phone-off` hang-up with the delay in muted mono
   beside it. Neighbouring turns in `--text-muted`, the reporter's span in `--bg-warning`. The
   two value rows carry `-` / `+` in the gutter, `--bg-danger` and `--bg-success` on the value
   in mono. Their gutter icon is the icon of the row kind whose value changed, the same one the
   call rows use: `ti-robot` for a spoken line, `ti-tool` for a tool call or its resultado,
   `ti-webhook` for a post-call tag. Never the change-locus icon, that one lives in "Closes it".
4. "Observations": heading in `--text-warning`, one bullet per item at 13.5px. Absent unless
   issues.md says it is warranted.

### Simulation Changes

When to use: step 2 of the workflow, reporting which simulations change for the task at hand.
Reference: [widgets/sim-changes.html](./widgets/sim-changes.html).

Only simulations that change appear: additions, modifications, deletions. Simulations that
stay as they are, however close to the scenario, are not listed; if one of them is the reason
nothing changes, say so in the message.

Layout, top to bottom:

1. Header on `--surface-1`: issue number in mono and the issue title. Nothing else.
2. One row per changed simulation, hairline-separated, with a mono mark in the 64px gutter:
   `+` in `--text-success` for an addition, `~` in `--text-warning` for a modification, `-` in
   `--text-danger` for a deletion.
   - Name line: display name at weight 500 on the left; on the right the group and path as a
     crumb, `ti-folder` group name `›` `path:*` in muted mono. Both belong to the row, not the
     header, since one task can touch several groups. No character count, no position among
     siblings, no categories.
   - `gist` line: one sentence on what the persona does and what must come of it. Always on an
     addition; on a modification only when the persona's behaviour changes.
   - `assertions` line: the tag expectations as neutral mono chips, `!` for negatives. Colour on
     a chip means one thing only: `--bg-success` added, `--bg-danger` struck removed. A new
     simulation's chips carry no colour at all.
   - A modification shows only the fields that change. A rename or a group move is shown inline
     on that line, old value struck in `--bg-danger`, new value in `--bg-success`.
   - A deletion is the struck-through name in `--text-muted`, its crumb, and a muted note of
     where its coverage goes.

### Simulation Replay

When to use: step 3 of the workflow, showing one simulation result so that I can judge whether
the simulation is trustworthy before anything is said about the agent; also the failing replay
in a diagnosis. Reference: [widgets/sim-replay.html](./widgets/sim-replay.html).
Source: `runset.py <run-id> --failed` and `--transcript` on the synced run.

Layout, top to bottom:

1. Header on `--surface-1`: simulation display name at weight 500, then the pass count in mono
   (`0 / 5`, `--text-danger` when any run failed). Right: group and path crumb as in Simulation
   Changes.
2. "Expectations": one row per expected outcome with `ti-check` in `--text-success` or `ti-x` in
   `--text-danger` in the gutter; under a failed one, the judge's reasoning in muted 13px. Then
   one row of tag-assertion chips, neutral mono, the violated ones in `--bg-danger`.
3. "Replay": the turns in order, none dimmed. Speaking turns carry `ti-robot` or `ti-user` in
   the 64px gutter and full-colour text; the persona's scripted lines get no colour of their own.
   Non-speaking rows leave the gutter empty and start in the text column with their icon: tool
   calls as `Name(args)` in muted mono 12.5px, one call per row, arguments slightly fainter;
   activated observations with `ti-eye` in muted mono 11.5px, elided with `…`; skipped runs of
   turns as one italic muted row saying how many and what happened. Only the turn that broke an
   expectation is coloured: `--bg-danger` on the offending span and on the tool call, with its
   gutter or icon in `--text-danger`. Argument values must come from the trace, not be inferred
   from the transcript.

### Simulation Iteration

When to use: while iterating on one failing simulation, each time a run finishes after an edit
was tried. One simulation, one run, one edit per widget; rounds do not accumulate. Each new
attempt re-renders the whole widget with its own edit and its own replay. Reference:
[widgets/sim-iteration.html](./widgets/sim-iteration.html).

It is Simulation Replay with one part added between the header and "Expectations":

- "Edit", a native `details` element closed by default. Its summary carries a `ti-chevron-right`
  that turns when open, the word "Edit", and the crumb of the edited item (block icon, block
  name `›` item name) so the attempt is identifiable without opening it. Inside: the crumb again
  on its own row, then the item as in Studio Context Edit, `-` in the gutter, removed words
  struck in `--bg-danger`, inserted words in `--bg-success`.
- Header count is the run this widget reports (`4 / 5`), not a total across attempts. Splits
  across runs, earlier rounds and their counts belong in the message.
- The run before any edit is a plain Simulation Replay; the "Edit" part exists only once
  something was tried.

### Studio Context Edit

When to use: steps 4 and 5 of the workflow, proposing a wording change to a Studio block, and
again when reporting the change as applied. Reference:
[widgets/studio-context-edit.html](./widgets/studio-context-edit.html).

It is the Studio Context section with the change written into it: same breadcrumb header, same
gate panel when the block sits under a condition, neighbours dimmed and elided as there. The
edited item is in `--text-primary` and carries the diff inline, so the sentence is read once:
removed words struck through in `--bg-danger`, inserted words in `--bg-success`. One section
per block that changes. The reason for the edit goes in the message, and the edit itself waits
for my approval before any block is touched.

## Text fallback

When no inline renderer is available, preserve the same content contract using diff formatting.
