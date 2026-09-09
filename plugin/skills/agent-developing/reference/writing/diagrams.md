# ASCII diagrams

These rules govern every ASCII diagram this skill produces: PR schematics, code comments, chat replies, and report figures. The rules distill the AGG corpus (https://asciidiagrams.github.io/agg.json), 2,156 curated diagrams mined from Linux, Chromium, LLVM, and TensorFlow comments. Corpus practice is conservative: 98.7% pure ASCII, and width holds at 80 columns at the 90th percentile.

Before writing the surrounding prose, captions, or labels, read reference/writing/authoring.md. For a PR schematic, read reference/shipping/pr-descriptions.md for placement and evidence requirements.

## When a diagram earns its place

Draw a diagram when the payload is spatial or relational. The jobs, ranked by corpus frequency:

1. Position, width, and adjacency of packed data: memory, registers, wire formats.
2. Naming a topology (nodes, fields, regions) so prose and tests can reference its parts.
3. The before and after of a transformation. Only paired pictures show which edges moved.
4. The full cross-product of two or more inputs, where a missing case shows as a hole.
5. Concurrency and ordering across actors.
6. 2-D layout of regions, windows, or pins.
7. A complete state-transition relation with cycles.

When no job applies, write prose or a list. A diagram is spatial encoding, not decorated text.

## Core rules

- Use pure ASCII: `+ - | / \ ^ v < >`. Use Unicode box drawing only when the whole render path is monospace UTF-8. Even then, use it only when the extra glyphs encode a second semantic level.
- Keep every line within 80 columns, including the comment prefix.
- Indent and align with spaces only. One tab breaks the diagram at any other tab stop.
- Define every non-obvious glyph in a legend directly beside the diagram. Hold one meaning per glyph per document.
- Label nodes, edges, and fields with the code's real identifiers, so the diagram greps back to code.
- Print the numbers: bit rulers, byte offsets at boundaries, coordinates, axis ticks. Where rival conventions exist (bit numbering, address growth, time direction), state yours in words.
- Sandwich the diagram in prose. One sentence before states what it shows. Semantics and caveats follow it.
- Keep labels terse. Hang detail on `(*)` footnotes or `<-- note` callouts outside the drawn structure.
- Elide repetition explicitly (`...`, `/\/\`, `~`) and keep the total or final offset visible. Declare simplifications, for example "not to scale".
- Land every arrow on an explicit endpoint. Use `+` for junctions and route around crossings, so a plain `|` crossing a `-` means no connection.
- Show a transformation as before and after diagrams with identical geometry, joined by `Before:`/`After:` or `=>`. Reserve `=>` for "becomes".
- Show dynamics as a storyboard of small complete snapshots.
- Pair the diagram with an oracle: a worked example with real values, or an expected-result table.
- Keep one canonical copy of a diagram and reference it: corpus copies measurably diverged.
- After any edit, re-verify the parallel rows: rulers, border walls, leader lines. Each is an unchecked copy of the data one line away.
- Respect the density ceilings: about 10 nodes, 3 nesting levels, 3 edge crossings. Past a ceiling, split the diagram, storyboard it, or switch to a table.
- Mark unknowns honestly with `?` and a note. Honest gaps beat confident wrongness.

## Genre recipes

- Bit and memory layouts: draw RFC style. One `-+` per bit, so cell width is field width. Add a two-row bit ruler, byte offsets in a margin gutter, and a field legend below. Split a 64-bit word into two 32-bit rows. Label narrow flags with leader lines below the box.
- Tables: title what maps to what. Scale ruling to cell complexity: whitespace between atomic cells, `|` between phrases, full `+--+` grids only around wrapping cells. Fill an empty cell with one explicit "none" mark, held constant across sibling tables.
- Trees: root at top with `/ | \` when shape or child slot matters. Root at left with tree(1) indentation for deep or long-labeled trees. Put edge labels in parentheses and node state in a one-glyph suffix with a legend.
- Graphs and dataflow: omit arrowheads for acyclic top-down flow. Add `v` or `^` only for cycles or upward flow. Prefer duplicating a node, with an alias note, over crossing edges. Leave renamable identifiers unboxed: a rename bursts the border.
- Sequences and concurrency: one column per named actor, time strictly downward. Put verbatim message names on arrows and local state in parentheses on the lifeline. For a race, draw both the broken and the fixed interleaving.
- State machines: label every edge with its trigger or guard. Mark the initial and terminal states explicitly.
- Formulas: draw fraction bars as `-----` rows. Write exponents inline as `^` or `**`, because raised superscript rows rot fastest in the corpus. Number equations, then bind each symbol to a code identifier in a "where:" list.

## Habitat traps

- In `//` comments, a diagram line ending in `\` splices the next source line. Append a `.` sentinel or reshape the line.
- Guard the diagram from formatters (`// clang-format off` and equivalents). Re-check the raw text even when a renderer shows it fine.
- In Markdown, always fence the diagram.
- Keep diagram lines ASCII even when the surrounding prose is not. Full-width CJK glyphs and typographic quotes shear columns.
