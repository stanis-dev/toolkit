# Codex Inline Widget Renderer

Use this renderer only when the current Codex client exposes the `visualize` skill and supports
inline visualization content references.

## Render

1. Read the complete `visualize` skill before creating or revising a widget.
2. Select the widget variation in [info.md](./info.md) and read its template under `widgets/`.
3. Treat the template's DOM structure, part order, row kinds, and placeholders as normative.
   Replace placeholders with evidence; add, remove, merge, or reinterpret parts only where
   `info.md` marks a part optional.
4. Save the adapted HTML fragment in the thread-scoped visualization directory supplied by
   Codex. Use a versioned ASCII filename and a unique root ID.
5. Read the fragment back and compare its structure with the source template.
6. Emit the Codex visualization content reference in the same response:

   ```text
   visualize{"path":"<absolute-path>/<variation>-vN.html","title":"<variation>_vN"}
   ```

## Adapt The Host, Not The Widget

The source templates use Claude's host bindings. For Codex, make only these mechanical changes:

- Keep an HTML fragment: no doctype, `html`, `head`, or `body` elements.
- Remove the template's `html,body` reset and its document-padding adjustment script.
- Scope every CSS selector to the fragment's unique root ID.
- Preserve every element beneath the template root in the same order.
- Resolve the theme tokens through the Codex fallbacks already present in the templates.
- Use the Lucide name in each icon's `data-lucide` attribute; do not load another icon library.
- Replace a template's `title` tooltip attribute with Codex's `data-tooltip`, preserving its text.
- Follow every other constraint in the loaded `visualize` skill, including its network, layout,
  accessibility, and response requirements.

## Theme Mapping

The templates use their Claude token first and the Codex token as a fallback:

| Template token | Codex fallback |
| --- | --- |
| `--font-sans` | inherited host font |
| `--font-mono` | system monospace stack |
| `--text-primary` | `--foreground` |
| `--text-secondary` | `--muted-foreground` |
| `--text-muted` | `--muted-foreground` |
| `--text-danger` | `--destructive` |
| `--text-success` | `--green` |
| `--text-warning` | `--orange` |
| `--text-accent` | `--accent-foreground` |
| `--surface-1` | `--muted` |
| `--border` | `--border` |
| `--border-strong` | `--border` |
| `--border-success` | `--green` |
| `--border-danger` | `--destructive` |
| `--bg-danger` | low-opacity `--destructive` mix |
| `--bg-success` | low-opacity `--green` mix |
| `--bg-warning` | low-opacity `--yellow` mix |
| `--bg-accent` | `--accent` |

## Icon Mapping

Keep the template's Tabler class for Claude and set its Codex equivalent in `data-lucide`:

| Tabler class | Lucide name |
| --- | --- |
| `ti-folder` | `folder` |
| `ti-route` | `route` |
| `ti-file-text` | `file-text` |
| `ti-list-check` | `list-checks` |
| `ti-git-branch` | `git-branch` |
| `ti-book` | `book-open` |
| `ti-gavel` | `gavel` |
| `ti-message-language` | `languages` |
| `ti-puzzle` | `puzzle` |
| `ti-tool` | `wrench` |
| `ti-eye` | `eye` |
| `ti-database` | `database` |
| `ti-shield` | `shield` |
| `ti-bug` | `bug` |
| `ti-arrow-up-circle` | `circle-arrow-up` |
| `ti-message-2` | `message-circle` |
| `ti-text-recognition` | `scan-text` |
| `ti-volume` | `volume-2` |
| `ti-ear` | `ear` |
| `ti-webhook` | `webhook` |
| `ti-settings` | `settings` |
| `ti-robot` | `bot` |
| `ti-user` | `user` |
| `ti-phone-off` | `phone-off` |
| `ti-check` | `check` |
| `ti-x` | `x` |
| `ti-chevron-right` | `chevron-right` |

## Completion Criterion

The widget is complete only when its fragment contains exactly the parts and data required by its
`info.md` variation, in the template's order, and the response includes its inline visualization
content reference.
