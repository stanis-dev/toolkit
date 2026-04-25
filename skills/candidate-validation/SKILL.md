---
name: candidate-validation
description: Design a candidate-validation interview script from a reference interview, channel context, calibration, and CV.
when_to_use: Use for candidate-screen or client-validation interview prep when a reference transcript and CV exist. Not for panel design or debrief.
---

# candidate-validation

Given a reference interview, validation-channel context, a calibration set, and a candidate CV — produce an interview script. Draft, review, refine, emit. For Stan's live use during the call.

# Constraints

- Never invent a phase arc from scratch. Always extract from a real prior interview. Default anchor: Seb's Alex Baas validation (`rec-2026-03-27-140153-Alex-Baas-AI---Client-Validation.polished.txt`).
- Never fabricate role bars. Every bar in the script traces to a dated message in `#sierra-validations` or a specific post-interview debrief. Cite the source on first use.
- Never write generic probes. Every question is either (a) arc-standard from `references/script-arc.md` or (b) candidate-specific based on a concrete CV signal.
- Never use a scorecard dimension that isn't in `journal/candidate-eval.md`. The rubric is authoritative; don't invent new axes.
- Never overweight React/TypeScript. The rubric names it the *least* important technical dimension. Probe the gap, do not gate on it.
- Never modify `html-report`'s CSS or introduce custom classes. Use only the content-type vocabulary from `skills/html-report/SKILL.md`.
- Never emit before candidate slug, output path, and arc reference are explicit in the conversation.
- Never merge the during-call and post-conversation layers. In-moment cues (listen, drift, red flag) stay inline per phase; scorecard, verdict, and calibration stay in the final H2.
- Never use em dashes in prompts. Hyphen only. Never use semicolons — split or comma.
- Never paste bare URLs. Labelled links only.
- If the request is not about designing a candidate-validation interview script, stop and say so.

# Sources

All paths relative to the toolkit repo root.

- **Reference interview**: `brain/data/rec-*-Client-Validation.polished.txt` + matching `.summary.md`. Default arc anchor: Alex Baas (2026-03-27).
- **Validation channel**: `brain/data/slack/wizeline/readable/slack_C096PSTHJTH.md` (`#sierra-validations`). Source for dated role bars.
- **Rubric**: `journal/candidate-eval.md`. Authoritative scorecard dimensions.
- **Calibration set**: `references/calibration-set.md`. Named past candidates as comparison anchors.
- **Canonical arc**: `references/script-arc.md`. The reusable phase scaffold.
- **Current bars**: `references/role-bars.md`. Permanent + dated bars with extraction rules.
- **Output template**: `skills/html-report/template.html`. Do not modify.

# Workflow

## 1 · Scope the interview

Confirm four things before reading any source:

- Candidate name and CV path
- Role track (default: Wizeline→Sierra Staff AI / SWE5 AI unless the channel shows otherwise)
- Duration (default 60 min)
- Arc reference (default: Alex Baas; override if a newer Seb-led validation has a usable debrief)

Done when all four are fixed explicitly in conversation.

## 2 · Gather sources in parallel

Read in one round of parallel reads — don't serialise:

1. Reference interview polished transcript + its `.summary.md` debrief
2. Candidate CV (and LinkedIn profile PDF if provided)
3. Recent `#sierra-validations` activity (last 2–4 weeks) for current role bars
4. `references/calibration-set.md` for comparison points

Done when each source has at least one specific finding extracted — not a theme.

## 3 · Extract three things from the CV

One sentence each, specific:

- **Highest overclaim risk** — usually the most recent, solo-built, unverifiable claim. This becomes the phase-2 deep-probe target.
- **Gap against role bars** — where the CV is thin against the bars from `references/role-bars.md` and the rubric. This becomes phase 3.
- **Comfort-zone drift target** — the topic the candidate will pivot to under pressure. This becomes a drift-redirect callout in phase 2.

Done when each is a specific sentence naming a file/project/claim, not a category.

## 4 · Assemble the script

Walk the phase arc from `references/script-arc.md`. For every phase write:

- Italic phase-intent line (≤140 chars) — goes in `<p class="section-summary">`
- Opening prompt — italic paragraph, verbatim speech
- Follow-up ladder only for the deep-probe phase(s), as `<ol>` with a one-line "why" per rung
- In-moment cues as `<aside class="callout">` with kind in {note, caveat, warning}
- Scorecard in the post-conversation section, aligned with `journal/candidate-eval.md` dimensions

Done when every phase has at minimum a kicker (section number), intent line, and one prompt. Red flags and drift cues are added where the reference arc or the CV analysis demands them — not uniformly.

## 5 · Emit

1. Start from `skills/html-report/template.html` verbatim.
2. Apply the content mapping below. No new CSS, no custom classes.
3. Drop the TOC (`<nav class="toc">`) — the script is short and live-use; a sticky rail is noise.
4. Save to `~/Downloads/interview-{candidate-slug}.html`. Ask Stan to confirm the slug if it's not obvious from the CV.
5. Do not open the file unless asked.

# Content mapping onto html-report

| Interview element | html-report vocabulary |
|---|---|
| Interview title | `<h1>` |
| "Going in" strip — 2–3 things to remember before starting | `.bluf` with one `.lead` paragraph + at most one supporting paragraph |
| Phase section | `.section` with `.section-num` `01`–`08` + H2 title |
| Phase intent | `<p class="section-summary">` italic, ≤140 chars |
| Verbatim prompt | Italic paragraph: `<p><em>…</em></p>` |
| Follow-up ladder | `<ol>` with a one-line plain rationale per rung |
| Listen cue | `<aside class="callout"><span class="kind">note</span>…</aside>` |
| Drift redirect | `<aside class="callout"><span class="kind">caveat</span>…</aside>` |
| Red flag | `<aside class="callout"><span class="kind">warning</span>…</aside>` |
| Scorecard | `<table>` with columns: Dimension, 1–5, Hint |
| Verdict | `<dl>` with one `<dt>Verdict · /10</dt><dd>{blank slot}</dd>` |
| Calibration comparisons | `<dl>` keyed by past candidate name |

Post-conversation is a normal `.section` with num `09`. The 72px inter-section space plus the num shift is enough separation — no custom rule needed.

# Examples

### GOOD — arc anchored, CV-specific probes

Stan says "help me prep for the validation interview with Manuel Martinez, his CV is at /Users/stan/Downloads/CV_Manuel_Martinez.pdf". The skill confirms candidate slug (`manuel-martinez`), output path, and arc reference (Alex Baas). Reads CV + LinkedIn + Alex transcript + recent `#sierra-validations` + calibration set in parallel. Extracts: overclaim risk = "5 months solo on Claude Agent SDK work at Quasient"; gap = "no fresh TS/React, listed in skills not in recent projects"; drift target = "PAL, his JVM runtime". Emits a script where phase 2 stress-tests the Claude SDK claim with a six-rung ladder, phase 3 is a direct TS/React gap probe, and phase 2 includes a drift-redirect callout naming PAL specifically.

### BAD — generic probes, no CV grounding

Stan asks for a script. Skill emits a generic "tell me about your hardest project / how do you handle ambiguity / what tools do you use" script without reading the CV. Questions could apply to any candidate. No drift target named. No overclaim identified. Useless live.
Why this fails: the skill's value is candidate-specific probe design. A generic arc is already in `references/script-arc.md`; the output must add the candidate layer.

### GOOD — honest about source gaps

No recent Seb-led debrief exists beyond Alex Baas. The skill states this: "using Alex Baas (2026-03-27) as the arc anchor; no newer debrief available." Stan can decide whether that's fresh enough.

### BAD — fabricated bar

The skill writes "per Seb, engineers must have 5+ years Python experience" when no such message exists in `#sierra-validations` or in any debrief. Every bar must be citable.
Why this fails: fabricated bars leak into real interviews and damage credibility with candidates.

### GOOD — rubric-aligned scorecard

Scorecard dimensions: Speed (indirect), Agent Architecture, Communication, Ownership, Initiative, React/TS (low-weight). Matches `journal/candidate-eval.md` exactly.

### BAD — invented scorecard axes

Scorecard includes "Leadership potential", "Culture fit", "Growth mindset". None of these are in the rubric.
Why this fails: drifts from the hiring team's shared evaluation framework. Seb's rubric is what Sierra employees are evaluated on; candidates should be too.

# Anti-patterns

| Temptation | Reality |
|---|---|
| Copy the arc for every candidate | Arc is shared; probes are candidate-specific |
| Put every CV concern into the script | Three focused probes beat seven scattered ones |
| Style the HTML to match the last one Stan liked | html-report already owns the aesthetic; do not override |
| Merge during-call cues with synthesis | You'll read scorecard language mid-call and lose flow |
| Skip the channel read because "bars don't change much" | Benja's English bar and Santi's agent-mode bar both appeared mid-stream; refresh every time |
| Treat React/TS as a hard gate | Rubric says lowest-weight technical dimension; probe, don't disqualify |
| Open the file automatically | Stan may want to edit or review first |
| Write a TOC | Script is short and live; a sticky TOC rail fragments attention |

# Conversation flow

After emitting the script, Stan may ask to widen the column, split layers differently, or adjust a phase. Those are single-turn tweaks; don't re-run phases 1–4. If Stan asks for a post-interview debrief or scorecard synthesis, that's outside this skill — stop and say so.
