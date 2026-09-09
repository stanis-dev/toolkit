# Simulation assertions and clocks

Read before writing a tag assertion, an `expectedOutcomes` entry, a markup expectation, or a time-sensitive fixture. The canonical assertion grammar is in `.composer/docs/simulation-test-reference.md`; confirm it there before relying on the forms below. For tag names and outcome wording, read [authoring](../writing/authoring.md). When the behavior under test consumes a clock or persisted state, read [runtime and state](../design/runtime-state.md).

| Syntax  | Meaning                                                              |
| ------- | -------------------------------------------------------------------- |
| `!foo`  | asserts the tag `foo` is absent; `!` is the only operator            |
| `^foo`  | asserts the developer tag `^foo` is present; `^` is part of the name |
| `~foo`  | employee-only tag; `~` is also part of the name                      |
| `!^foo` | prefixes compose with negation: asserts the dev tag is absent        |

Use `^` and `~` only when the emitting code actually creates such a tag. Prefer deterministic tag assertions. Reserve `expectedOutcomes` for behavior a tag cannot express. A simulation that reaches a path but asserts nothing about it does not cover it.

An LLM judge misreads markup: a `[label](url)` link reads as the domain appearing twice and fails correct output. Spell the markup semantics out in the outcome wording, in a shared fixture helper. Check the transcript before concluding the judge is wrong.

When a simulation asserts on live knowledge content, record the depended-on articles or content property beside the assertion. When it asserts a verbatim date from mock data, pin `testOnlyNowUtc` to the mock's capture timestamp. Confirm the key and its location in the installed fixture schema rather than applying a production clock override.

Diagnose a failed assertion through [result access](simulation-results.md) and interpret the gate through [testing](testing.md).
