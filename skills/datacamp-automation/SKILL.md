---
name: datacamp-automation
description: >-
  Reuse and extend tested Playwright automation sequences for DataCamp course pages. Use
  for navigating lessons, interacting with widgets, and recording verified UI patterns.
  Not for stealth or detection evasion.
---

# DataCamp Automation

Reusable playbook for DataCamp course pages in the user's existing logged-in browser session.

Verified live against `campus.datacamp.com` on `2026-04-07`.

## Operating Principle

- Work from the user's already-open DataCamp tab when possible.
- Use ordinary browser automation only. Never optimize for stealth, evasion, or disguising automation.
- Prefer verified live sequences over generic helper APIs.
- Treat this skill as a living catalog. When a new widget is solved reliably, update this skill with the selectors, exact action sequence, verification method, and failure notes.

## Constraints

- Do not sign the user out, close their tab, or navigate away from the active DataCamp flow unless asked.
- Do not submit answers during sequence discovery unless the user explicitly asks.
- After exploratory tests, use `Reset` if the page exposes it so the user is left in a clean state.
- Prefer `playwright.execute` for DataCamp widgets. Use `browsermcp` only for simple navigation or inspection.
- For drag-and-drop widgets, trust DOM reads over accessibility snapshots.
- If a sequence is not yet proven, run a small live probe first and label the pattern unverified until it repeats.

## Workflow

### 1. Attach to the live course tab

- Use `context.pages().find((p) => /datacamp/i.test(p.url()))`.
- If no matching tab exists, ask the user to open the target course page.

Done when:
- `state.page.url()` is an active DataCamp course URL.

### 2. Observe and classify the screen

- Print the current URL.
- Use `snapshot({ page: state.page, showDiffSinceLastCall: false })` for page-level controls and labels.
- Use `getCleanHTML({ locator: state.page.locator('main'), showDiffSinceLastCall: false })` for exercise content and state.
- Name the current exercise type before automating it.

Done when:
- you can identify the current widget type and the controls you plan to use.

### 3. Probe one primitive at a time

- Change one interaction variable per attempt.
- Verify DOM state after each attempt before trying a new variant.
- If a test changes the exercise state, reset it before the next experiment unless the user wants to continue.

Done when:
- either a reliable sequence is found
- or the failure mode is specific enough to guide the next probe.

### 4. Record the pattern

- Capture the selectors that worked.
- Capture the exact action sequence, including pauses if they matter.
- Capture the verification method that proves success.
- Capture known failures so future sessions avoid the same dead ends.

Done when:
- a future session could repeat the interaction without rediscovery.

## Observed Stable Controls

Observed on the live course page and safe to reuse when present:

- Previous exercise: `[data-cy="header-previous"]`
- Next exercise: `[data-cy="header-next"]`
- Course outline: `[data-cy="header-outline"]`
- Slides: `[data-cy="header-slides"]`
- Video: `[data-cy="header-video"]`
- Hint: `[data-cy="exercise-show-hint"]`
- Reset: `[data-cy="reset-button"]`
- Submit: `[data-cy="submit-button"]`

Treat these as observed selectors, not a guarantee that the control is safe to click in every context.

## Verified Pattern: Classification Drag And Drop

### Applicability

Use this pattern when the exercise contains:

- one current card in the top source area
- multiple category buckets below
- `data-cy="draggable-item"`
- `data-cy="droppable-container"`
- `data-cy="reset-button"`

This matched the `Dimensions of responsible data` classification exercise on `2026-04-07`.

### Reliable Selectors

- Current source card:
  - `state.page.locator('[data-cy="droppable-container"]').first().locator('[data-cy="draggable-item"]').first()`
- Target bucket:
  - `state.page.locator('[data-cy="droppable-container"]').filter({ hasText: '<bucket title>' }).locator('[data-cy="droppable-area"]')`
- Reset button:
  - `state.page.locator('[data-cy="reset-button"]')`

### Reliable Action Sequence

1. Read the source and target bounding boxes.
2. Move the mouse to the source card center.
3. Call `mouse.down()`.
4. Wait about `150-200ms`.
5. Move about `15-20px` from the source center over `8-10` steps to enter drag state.
6. Move into the target bucket interior over about `25-30` steps.
7. Hover inside the target bucket for about `250-400ms`.
8. Make a small settle move inside the target bucket if needed.
9. Call `mouse.up()`.
10. Wait about `400ms` before verifying.

Done when:
- the target bucket contains the dragged card text in the DOM.

### Example Sequence

```js
const source = state.page
  .locator('[data-cy="droppable-container"]')
  .first()
  .locator('[data-cy="draggable-item"]')
  .first();

const target = state.page
  .locator('[data-cy="droppable-container"]')
  .filter({ hasText: bucketTitle })
  .locator('[data-cy="droppable-area"]');

const s = await source.boundingBox();
const t = await target.boundingBox();

await state.page.mouse.move(s.x + s.width / 2, s.y + s.height / 2);
await state.page.mouse.down();
await state.page.waitForTimeout(200);
await state.page.mouse.move(s.x + s.width / 2 + 20, s.y + s.height / 2 + 20, {
  steps: 10,
});
await state.page.mouse.move(t.x + t.width / 2, t.y + 120, { steps: 30 });
await state.page.waitForTimeout(400);
await state.page.mouse.move(t.x + t.width / 2 - 10, t.y + 140, { steps: 8 });
await state.page.waitForTimeout(250);
await state.page.mouse.up();
await state.page.waitForTimeout(400);
```

### Verification

Preferred verification:

- `getCleanHTML({ locator: state.page.locator('main'), showDiffSinceLastCall: false })`

Confirm all of the following when possible:

- the target bucket now contains the dragged card text
- the source area now shows the next card
- the `cards left` text changed as expected

Diagnostic-only verification:

- while the card is held, `getCleanHTML(..., includeStyles: true)` may show `is-dragging-over` on the active target bucket

### Known Failures

- `locator.dragTo()` was unreliable on this widget.
- Fast drag-and-release often hovered the correct target but did not commit the drop.
- `snapshot()` could look unchanged or ambiguous even when the DOM had changed.
- Click-based placement was inconsistent and should not be treated as a reliable primitive.

### Recovery

- If the drop fails, click `[data-cy="reset-button"]` to return to a known state.
- If the target shows `is-dragging-over` while held but the drop does not commit, increase the hover duration before `mouse.up()`.

## Known Gaps

These patterns have not yet been documented in this skill:

- multiple choice exercises
- free-response or fill-in widgets
- code editor exercises
- video or slide progression logic

Do not infer behavior for those exercise types from the drag-and-drop sequence alone.

## Good / Bad

### GOOD

- inspect with `snapshot()`
- verify widget state with `getCleanHTML()`
- test one primitive
- reset the exercise
- then document the exact working sequence

Why this works:

- it produces a reusable pattern instead of a one-off lucky interaction.

### BAD

- call `dragTo()` once
- trust the snapshot
- assume the move worked
- click `Submit`

Why this fails:

- this widget can show stale or misleading high-level state unless the DOM is checked directly.

## Anti-Patterns

| Temptation | Reality |
| --- | --- |
| Use `locator.dragTo()` because it is shorter | On the verified DataCamp classification widget it was not reliable enough; use low-level mouse drag |
| Trust the accessibility snapshot for bucket contents | DOM reads were more reliable for confirming the actual drop result |
| Discover sequences by submitting answers | Sequence discovery should stop before submit unless the user explicitly wants to progress |
| Leave exploratory state in place | Reset after probes so the user is not left mid-test |
| Generalize one accidental success into a pattern | Repeat the sequence until the success condition is deterministic, or keep it marked unverified |

## Interaction Rules

- If the user asks to work on a live DataCamp page, attach to the existing tab first.
- If the user wants a new exercise type automated, start with a small probe and record the result.
- If a sequence is already documented here, reuse it instead of improvising.
- When a new sequence is verified, update this skill so the next session starts with the playbook instead of rediscovery.
