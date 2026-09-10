# Information Formatting

You must maximise the ease with which I absorb the information.

## The issues page

Everything you show me about an issue goes to one page, not to the chat. The page is a static
site at `http://127.0.0.1:8489/`, served from `~/.claude/bbva-issues/`; start it with
`~/.claude/bbva-issues/serve.sh` if the link does not answer. It shows, per Sierra agent, the
open tracker issues in a sidebar grouped in buckets, and one card for the selected issue,
`http://127.0.0.1:8489/#a=<agent>&i=<n>`.

If the card is not open in app browser, open it for me.

The agents are `openpay` (repo `agents/openpay`, MCP `sierra`) and `cobranzas` (repo
`agents/base`, MCP `sierra-base`). Everything below lives under `agents/<agent>/`.

- The sidebar and the "Issue as reported" fold under every card are built from `issues/<n>.json`
  ([tooling.md](./tooling.md)); an issue no card names sits under "No bucket yet".
- The card, `cards/<n>.html`: one file per issue, the only thing you write for me, and only for
  the issue you are working. Nobody else writes it.

A card is a bucket line, then state lines while there is state to show, then sections, one per
workflow step, in workflow order:

    <!-- bucket: Pedido de humano -->
    <!-- pr: draft https://github.com/<org>/<repo>/pull/NNN -->
    <!-- ws: default -->
    …section HTML, exactly as its template under sections/ renders it…

`pr` is `draft`, `ready` or `merged`, then the link. `ws` is the Studio workspace that holds the
edit, `default` once it is there, `released` once it is in a release. Update both the moment they
change.

## Card rules

- Don't change a section's structure unless asked explicitly.
- The card is the whole answer. Outside it, only a blocker or a question, one line each. I will
  ask for details myself if I need them.
- Only the top section has its own header.
- A step that re-measures an object already on the card refreshes that object's part where it
  stands: e.g. Expectations and the Replay of the simulation chosen in steps 2 and 3 update in
  place, not repeated.
- Expectations and Replay are `<details>` parts, closed by default. The Expectations summary
  carries the pass count of the run it reports; the Replay summary carries the heading with the
  result link.
- An expectation row states the observable only: the turn, what it must contain or omit, and
  the phrasings that do not meet it when the judge has passed one.
- Each step edits the card file in place: its section appended, or the part it refreshes
  replaced.

## Card sections

### Studio Context

When to use:

- I ask which part of the context teaches, allows or causes some behaviour;
- step 4 of agent-diagnose (the responsible context);
- the current state of a block before proposing an edit to it.

Sources:

- block files under `.composer/blocks/` and tool descriptions in code.

When the conversation being diagnosed saw a different version than the files hold, render what
the model saw. The template
[sections/studio-context.html](./sections/studio-context.html) holds the summary row, a block
entry per block kind and a row per item kind; copy the row, replace its text. What the template
cannot hold:

- The summary row exists for one case: layer 1 holds a conflict. One part of the context asks
  for the behaviour the turn needed, another overpowers it at that turn. Role A is the part that
  asks, role B the part that wins. Each column lists its spans as they read below. The note, in
  column B only, is one sentence: what wins and what it makes the agent do. A section without
  that conflict has no summary row.
- One block entry per place, in the order the model reads them. The breadcrumb carries display
  names only: no sibling ordinals, no type words once an icon carries the type, no predicate
  icons on the path.
- Block icons beyond the ones in the template: `ti-list-check` rules, `ti-git-branch`
  condition, `ti-book` glossary, `ti-gavel` policies, `ti-message-language` response phrasing,
  `ti-puzzle` component.
- Highlights carry role A or role B; the role's key is the superscript on the span and the list
  key in the summary row.
- Layer 1 of the relevant context ([agent-diagnose.md](./agent/agent-diagnose.md)) by default;
  layers 2 and 3 only when I ask for them.

### Issue Analysis (Workflow, Step 1)

What each part holds is in [issues.md](./issues.md). The template is [sections/issue-analysis.html](./sections/issue-analysis.html).

- Type: `ti-bug` in `--text-danger` for bug, `ti-arrow-up-circle` for improvement, then the
  change type.
- The failure row takes the gutter icon of the row kind whose value changed: `ti-robot` for a
  spoken line, `ti-tool` for a tool call or its result, `ti-webhook` for a post-call tag.

### Sim Strategy (Workflow, Step 1)

Template: [sections/sim-changes.html](./sections/sim-changes.html).

- Only affected simulations.
- A modification shows only the lines that change. A group move goes on the crumb the way the
  rename goes on the name.
- All simulation runs must update pass rate for sims.
- Replay shows the replay that with the most relevant failure scenario.
- Deletion's fold holds one short sentence about the reason it gets deleted.
- A regression is a simulation the edit did not touch whose pass count fell between the run before
  the edit and the run after it, same workspace, same replicas. Its row comes after the changed
  ones and carries no change mark: the count after in the gutter, then the count before, dimmed,
  linking to the run before. The Expectations mark the one that fails now with the judge's words,
  the Replay is one failing run. A count that recovers updates in place.

### Simulation Replay

When to use: step 3 of the workflow, showing one simulation result so that I can judge whether
the simulation is trustworthy before anything is said about the agent, inside that simulation's
row of Sim Strategy; on its own for the failing replay in a diagnosis. Source:
`runset.py <run-id> --failed` and `--transcript` on the synced run. The template
[sections/sim-replay.html](./sections/sim-replay.html) holds a row per turn kind; copy the row,
replace its text. What the template cannot hold:

- Only the breaking turn, the turn before it and the turn after it; everything else collapses
  into gap rows, in order, none dimmed. A turn is one speaker's consecutive messages: its first
  row carries the turn number, later rows of the same turn and the tool calls inside it carry
  none. One tool call per row, its arguments from the trace, never inferred from the transcript.
- The breaking turn is coloured and its text marked as the offending span; when the offence is
  an omission, the whole turn is the span. Nothing else is coloured. The pass count takes `ok`
  only when every run passed.
- The Replay heading links to the result,
  `https://bbva.sierra.ai/agents/<agent>/simulations/runs/<run>?resultId=<result>`, ids without
  their `replaytestrunset-` and `replaytestresult-` prefixes.

### Simulation Iteration

When to use: while iterating on one failing simulation, each time a run finishes after an edit
was tried. One simulation, one run, one edit per section; rounds do not accumulate, each attempt
re-renders the whole section with its own edit and its own replay. The template
[sections/sim-iteration.html](./sections/sim-iteration.html) is Simulation Replay with the
"Edit" part. What the template cannot hold:

- The header count is the run this section reports, not a total across attempts.
- The run before any edit is a plain Simulation Replay; the "Edit" part exists only once
  something was tried.

### Studio Context Edit

When to use: steps 4 and 5 of the workflow, proposing a wording change to a Studio block, and
again when reporting the change as applied. The template
[sections/studio-context-edit.html](./sections/studio-context-edit.html) is one Studio Context
block entry with the diff written into the edited item. What the template cannot hold:

- One block entry per block that changes, its neighbours dimmed and elided as in Studio Context.
- The block entry's status label reads `proposed`, and `applied` once pushed.
