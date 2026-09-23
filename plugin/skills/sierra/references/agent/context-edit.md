# Studio Context and its Edit

Step 4 of the issue workflow is the `context-edit` skill (`plugin/skills/context-edit/SKILL.md`), run on `<agent> <n>` once
the Issue Analysis JSON is at `agents/<agent>/analysis/<n>.json`, and the Sim Strategy JSON when step 2 has run. It
reads the request the model saw at the failure turn, the Studio content and the agent code and returns JSON: the
cause, the responsible context with its roles, the edit as old and new text on a JSON pointer, alternatives, and
flags. Save it as `agents/<agent>/context/<n>.json` in the pages dir. It edits nothing: the edit is a proposal until I
approve it, then step 5 applies it against [agent-design.md](./agent-design.md).

## The card

Two parts, rendered from the JSON and the tree ([info.md](../info.md)), nothing else:

- Studio Context, template `sections/studio-context.html`: the glance lists from the `context` entries' `role` and
  `spans`, A left, B right, keyed A1, B1 in order; one section per entry with its `path` as the breadcrumb, its `gate`
  as the gate rows, the item text from the tree at `pointer` with the `spans` marked in the role's colour, the
  `neighbours` dimmed; a tool section from `tool` when it is not null. The summary row only when both roles exist.
- Studio Context Edit, template `sections/studio-context-edit.html`: one section at `edit.path`, state `proposed`, the
  item read once with the words that go struck and the words that replace them inserted, computed by diff of `old`
  against `new`; a new item shows as inserted after the item at `after`; neighbours dimmed. State becomes `applied`
  once step 5 pushes it.
- `alternatives` and `ripple` do not go on the card; they answer my questions when I ask.

## Flags

- `tree_moved`: tell me before anything is applied; the call may predate a fix.
- `code`: the change goes through a code PR, not Studio; the card still shows it as an edit.
- `sync`: stop; `pull --continue` or `pull --abort` is my call.
- `missing`: refresh the cache, run the agent again.
