# Agent Studio Issues

Step 1 of the issue workflow is the `issue-analysis` skill (`plugin/skills/issue-analysis/SKILL.md`), run on `<agent> <n>`.
It reads the issue and its linked call from the pages-dir cache ([tooling.md](./tooling.md)) and returns JSON: the
verdict, the failing turn as a `turn` with its bad spans, the good turn with its consequences, and the Studio
items involved. When the issue file or a linked call is not cached, refresh the cache first, then run it.

## The card

Render the Issue Analysis part ([info.md](./info.md), template `sections/issue-analysis.html`) from the JSON and the
cache, nothing else:

- Header: `type`. Verdict cell: `verdict`, unchanged.
- Conversation: the reported line from the source's `conversations[].marked[]`, omitted when it is the failure turn;
  the customer turn before the failure and the failure turn from the conversation at `failure.turn`, the `bad`
  spans struck; the good turn from `good.text`, its additions marked by diff against the failure turn; one row in gap style per
  clause of `good.then`; the resultado/motivo row from `metadata.tags`.

