# Simulation Strategy

Step 2 of the issue workflow is the `sim-strategy` skill (`plugin/skills/sim-strategy/SKILL.md`), run on `<agent> <n>` once
the Issue Analysis JSON is at `agents/<agent>/cards/<n>/analysis/answer.json`. It reads that JSON, the linked call and the agent's
simulation files and returns JSON: the existing guard and its state, the simulations that change with their persona,
expectations and tags, the expected reds, and flags. Save it as `agents/<agent>/cards/<n>/strategy/answer.json` in the pages dir;
`scripts/run.py <agent> <n> strategy` does the run, the save and the card ([tooling.md](../tooling.md)).
It may launch one existing simulation, unedited, in the issue's own workspace, to see the shape its conversation takes;
the brief's last section carries the commands. Red before the fix and green after are step 3.

## The card

Render the Sim Strategy part ([info.md](../info.md), template `sections/sim-changes.html`) from the JSON, nothing
else:

- One entry per item of `sims`, in the JSON's order: `add`, `modify` and `delete` map onto the template's `add`, `mod`
  and `del` entries. Name and group from `name` and `group`, the old name struck when it changes.
- `gist` on an `add`, and on a `modify` only when it is not null.
- A Persona part when the answer says anything about the persona: `persona.why` first, then the full text of a new
  persona as inserted, a modification's `persona.changes` as struck and inserted text, the opening turns, the mock user.
- Expectations: `kept` plain, `reworded` as struck and inserted text, `added` inserted, `removed` struck. Tags:
  `kept` plain, `added` inserted, `removed` struck.
- A `delete` shows `covered_by` in its fold.
- `expected_reds` go under the changed entries as untouched simulations, no counts yet.
- The pass count of every entry stays empty until step 3 runs it; runs then refresh the count in place.

## Flags

- `no_tag`: tell me before the sim is written; the fix may need to add the tag first.
- `fixture`: tell me; adding persona data is a separate change.
- `multi_sim`: stop and tell me; one scenario per simulation is the rule, an exception is my call.
- `missing`: refresh the cache, run the agent again.
