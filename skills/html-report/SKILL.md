---
name: html-report
description: >-
    Single-page HTML deep-dive report with research-backed typography and structure, rendered in a
    browser tab. Use for multi-section long-form output with mixed content (prose, code, tables,
    callouts); skip factoid answers, logs, or pipeable output.
---

# html-report

Emit one self-contained `.html` file: inline CSS, optional ~40 lines of vanilla JS for TOC
active-state, Google Fonts link for type. No React, no Babel, no external JSX, no build step.

## Why this exists (one paragraph)

The user ingests many agent deep-dives per working day under cognitive load. Working-memory capacity
is ~4 live referents (Cowan), sustained-attention quality degrades within 15–30 minutes (Warm),
prefrontal executive control fails first under stress (Arnsten), and every domain-switch between
reports costs residual time (Monsell). The design below is tuned for that reader — not for a fresh,
calm, one-document reader.

## Console-vs-HTML decision rule

Run in order. Stop at the first match.

1. Output <300 words AND single shape (pure prose, pure table, pure log) → **console**.
2. Output is a log, stream, or pipeable byte sequence the user may chain → **console**.
3. Output has a table ≥3 columns × ≥5 rows AND surrounding prose → **HTML**.
4. Output has ≥2 hierarchy levels AND ≥2 distinct content types → **HTML**.
5. Output is ≥600 words of argument or exposition the user may re-enter or scan → **HTML**.
6. Factoid answer to a direct question → **console**.
7. Tiebreaker: <500 words → console; ≥500 words → HTML.

If HTML wins, continue. If console wins, respect the writing-discipline rules in `context/global.md`
and emit plain text or markdown.

## How to emit

1. Start from `template.html` in this skill directory. Copy it verbatim as the base.
2. Replace placeholders with the report content. Do not add colors, fonts, or CSS rules not in the
   template. Do not modify existing CSS values.
3. Decide whether to include the TOC: emit the `<nav class="toc">…</nav>` block only if the report
   is ≥3000 words or ≥6 sections. Otherwise delete the entire `<nav>` block; the content centers
   automatically.
4. Emit as a single file. Ask the user where to save it if not stated.
5. Do not open the file or screenshot it unless asked.

## Content-type vocabulary

Use only these. Anything that doesn't fit is recast as prose.

- **Paragraph** — `<p>` inside a section. Most of the report.
- **Subheading** — `<h3>`. One or two per section. Don't nest further.
- **Code block** — `<pre class="code"><span class="lang">sql</span>…</pre>`. Language label optional;
  no syntax highlighting.
- **Inline code** — `<code>` inside prose. Identifiers, paths, function names.
- **Callout** — `<aside class="callout"><span class="kind">caveat</span>…</aside>`. One-word kind
  label from {note, caveat, warning}. One paragraph of content.
- **Table** — `<table>`. Column alignment via `class="left|right|center"`. Delta columns: prefix
  every cell with `↑`, `↓`, or `·` — never color alone. Apply `.delta-pos` (regression) or
  `.delta-neg` (improvement) on the Δ cell only.
- **Definition list** — `<dl><div><dt>…</dt><dd>…</dd></div>…</dl>` for keyed items.
- **File list** — `<ul class="files"><li><code>path</code><span class="why">reason</span></li>…</ul>`.

Nothing else. No figures, no images, no embedded diagrams, no quotations, no collapsibles, no
tabs, no accordions, no carousels.

## Rules

### Structure

1. **BLUF first**, 150–250 words, immediately after the H1. No kicker line, no agent/model
   metadata, no hero image, no TOC above it.
2. **Keep ≤4 simultaneously-live referents per passage** (Cowan cap). If a paragraph introduces a
   fifth entity before the first four are discharged, split.
3. **Heading hierarchy: H1 + H2 + H3.** No H4 or deeper.
4. **Paragraphs 60–120 words typical; flag ≥180.** One-sentence paragraphs allowed for emphasis.
5. **Sentences mean ~20 words; flag ≥45.**
6. **Prose by default.** Lists only for genuinely enumerable, parallel, non-flowing content.
7. **Section summary.** Each section opens with a 1–2-line italic summary (≤140 chars). If the
   summary exceeds 140 chars, add `class="section-summary long"` — the CSS switches to roman.
8. **Landmark every 400–700 words of body prose** — heading, callout, or table.
9. **Section numbering** `01`, `02`, … beside each H2 as re-entry cue.
10. **TOC** only when ≥3000 words or ≥6 sections. Sticky left rail, active-section tracked.

### Typography (already set in template; do not override)

11. Body: Source Serif 4, 18.5px, line-height 1.62, oldstyle figures.
12. Measure: 660px content column.
13. H1 44px, H2 28px, H3 20px — all weight 500.
14. Table body Inter 14px with tabular-nums + lining-nums; headers Inter 11.5px uppercase.
15. UI chrome labels (BLUF kicker, callout kind, TOC label): Inter 10.5px, 0.14–0.18em tracking.

### Color (already set; do not override)

16. Bg `#FAF8F3`, body `#1E1B17`, accent `#1F4FD6`. Single accent, used only for BLUF label,
    callout border, active TOC, link color.
17. Muted text tiers: 0.78 / 0.62 / 0.45 / 0.35 opacity on fg.
18. Semantic Δ colors: improvement `#116149`, regression `#9A3412`. **Always paired with ↑/↓
    prefix** — never color alone.
19. No dark mode. No `prefers-color-scheme` branch. No theme variables.

### Separation

20. **Separator stack**: whitespace → hairline → left-border accent. No cards for routine paragraphs.
21. 72px between sections.
22. Code blocks: 2px left border + subtle tint (stacked; tint amplitude is below the "second cue"
    threshold).
23. Callouts: 3px left accent border only. No tint, no card, no icon.
24. Tables: hairline row dividers, thicker header underline. No outer border, no grid.

### Motion

25. No motion, no autoplay, no carousels, no popups, no scroll-jacking. Only interactive behavior:
    TOC active-section tracking + smooth scroll on TOC click. `prefers-reduced-motion: reduce`
    disables smooth scroll (template handles this).

## Anti-patterns — never emit

- Card-per-paragraph (bordered/rounded/shadowed containers around routine prose).
- Rainbow section colors (each H2 in a different hue).
- Decorative hero image or gradient banner above the BLUF.
- Dark mode as default, or claimed as a "comfort" feature.
- Dense arrival TOC above the BLUF.
- Ornamental dividers, fleurons, emoji section markers.
- Bionic-reading / prefix-bolding.
- OpenDyslexic, Dyslexie, or Sans Forgetica fonts.
- Ultra-thin body (weight ≤300).
- Pure `#000` on pure `#FFF`, or WCAG-4.5:1-grade contrast.
- Executive summary that restates the body. BLUF states the conclusion; it does not summarize the
  argument.
- Color-alone semantic encoding on Δ columns (missing ↑/↓ prefix is a bug).
- Read-time badges, autoplaying progress bars, "back to top" scroll-follower buttons.
- Popups, modals, tooltips hiding key data, auto-focus shifts.
- Collapsed/hidden primary content.
- Overriding user zoom or `prefers-reduced-motion`.

## Relation to `context/global.md`

Surface-agnostic rules (BLUF, Cowan cap, paragraph/sentence length, prose-over-lists, heading depth,
landmarks) live in `context/global.md` and apply to every output regardless of surface. This skill
adds the HTML-specific layer on top; it does not redefine the surface-agnostic rules.
