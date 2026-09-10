# Customer Reporting

Release notes and other customer-facing summaries of what a merge changed. The reader files
issues in Agent Studio and shares the spec with us, so the note says only what changed for them.

## Rules

- Report only what is done. Nothing pending, partial, blocked or removed appears in the note.
- Neutral Spanish. No voseo, no Argentine idiom: the writer is not Argentine and the reader
  knows it.
- Every line leads with the issue number(s), then one sentence on the customer-facing change.
- Issue numbers link to Studio, `https://bbva.sierra.ai/agents/<agent-id>/issues/<number>`,
  never to GitHub.
- Describe the behaviour the customer hears or sees. No mechanism, no block or tool names, no
  pattern lists, no run ids, no pass counts.
- One flat list under «Novedades de esta versión». No grouping.
- An issue whose fix landed only as a guard simulation, with no behaviour change, gets no line.
  Say so to me outside the note so I can decide.
- An issue verified as a control (unchanged behaviour confirmed) rides the line of the issue it
  protects: «#370 confirma que …».
- No em dashes. No status words the tracker already shows.

## Sources

Build the list from the merged PR's commits and body, then confirm each issue number and title
with `get_issue_details`. Drop anything the PR body lists as a known blocker or as removed.

## Shape

**Novedades de esta versión**

- [#NNN](…/issues/NNN): <what the agent now does>.
- [#NNN](…/issues/NNN), [#MMM](…/issues/MMM): <one change that closes both>.
