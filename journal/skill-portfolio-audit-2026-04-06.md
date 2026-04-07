# Skill Portfolio Audit

Date: 2026-04-06

## Scope

- Reviewed all current plugin skills under `/Users/stan/code/toolkit/skills/*/SKILL.md`.
- Loaded the `skill-engineer` review rubric plus `references/principles.md`, `references/taxonomy.md`, and `references/root-causes.md`.
- Validated factual claims with current local CLIs, current remote host state (`homelab`, `mini`), real Cursor transcript samples, and official public docs where relevant.
- Collected transcript-usage discovery counts, but did not deep-read all matching conversations in this pass. Raw skill-name hits across Cursor transcripts total well over 200, which is large enough to justify a dedicated behavior-analysis pass.

## Method

I cross-referenced each skill against the 11 `skill-engineer` dimensions, but I did not force false precision on skills where some dimensions are legitimately less relevant. Reference and personal machine skills are strongest on tool guidance and domain accuracy; interactive skills are strongest on question design and output structure; procedural skills need explicit completion gates, anti-patterns, and exact tool sequences.

## Portfolio Dashboard

| Skill | Type | Verdict | Priority | Main reason |
| --- | --- | --- | --- | --- |
| `codex-proxy` | Reference / procedural | KEEP + IMPROVE | Medium | Accurate enough to use, but structurally thin: no anti-patterns, examples, or interaction rules. |
| `cursor-chat-history` | Reference | KEEP + IMPROVE | Medium | Good discovery surface and working scripts; needs explicit constraints, anti-patterns, and completion criteria. |
| `deep-eval` | Procedural | KEEP + IMPROVE | Medium | Strong anti-shortcut design, but over-length frontmatter and missing GOOD/BAD examples weaken activation and reuse. |
| `deep-research-prompt` | Interactive | KEEP + IMPROVE | Medium | Good workflow and template reference, but frontmatter is too long and constraint density is low. |
| `homelab-ssh` | Personal / reference | KEEP + IMPROVE | Medium | Valuable machine reference, but several operational facts have drifted from the live stack. |
| `mini-ssh` | Personal / reference | KEEP + IMPROVE | Medium | Still useful, but volatile machine facts are stale and should not be hardcoded. |
| `music-discovery` | Personal / procedural / interactive | DECOMPOSE | Critical | Oversized, mixed-concern skill with hardcoded secrets and stale install-path assumptions. |
| `plugin-dev` | Procedural / reference | KEEP + IMPROVE | Low | Mostly accurate, but missing constraints, examples, and done conditions. |
| `question-crystallization` | Interactive | KEEP + IMPROVE | Medium | Strong interaction design and output template, but discovery text is far too long and example coverage is missing. |
| `sierra-best-practices` | Procedural / reference | KEEP | Low | Best-structured Sierra skill in the set: constraints, examples, anti-patterns, and clear interaction rules. |
| `sierra-bootstrap` | Procedural | KEEP + IMPROVE | High | Good intent, but weak gates, stale paths, and incomplete workflow rigor. |
| `sierra-phrasing-eval` | Procedural | KEEP + IMPROVE | Medium | Solid methodology and output template; needs stronger anti-pattern coverage and clearer completion gates. |
| `sierra-powertool` | Reference | KEEP + IMPROVE | Medium | Strongest CLI reference after `sierra-best-practices`, but there is mild drift in commands and frontmatter length. |
| `sierra-triage` | Procedural | KEEP + IMPROVE | High | Under-specified to the point of being risky: no workflow, no template, and almost no tool guidance. |
| `sierra-wrap-up-issue` | Procedural | KEEP + IMPROVE | High | Useful terminal artifact, but current paths are wrong and completion criteria are underspecified. |
| `skill-engineer` | Interactive / review | KEEP + IMPROVE | High | Strong rubric and review logic, but it now contradicts current Cursor transcript reality and exceeds its own progressive-disclosure target. |

## Strongest Skills

### 1. `sierra-best-practices`

Why it stands out:

- The frontmatter is concise and correctly includes an anti-trigger at [`skills/sierra-best-practices/SKILL.md:3`](/Users/stan/code/toolkit/skills/sierra-best-practices/SKILL.md:3).
- Constraint density is high and testable at [`skills/sierra-best-practices/SKILL.md:12`](/Users/stan/code/toolkit/skills/sierra-best-practices/SKILL.md:12).
- It includes both a Temptation/Reality table and GOOD/BAD example pair at [`skills/sierra-best-practices/SKILL.md:40`](/Users/stan/code/toolkit/skills/sierra-best-practices/SKILL.md:40) and [`skills/sierra-best-practices/SKILL.md:48`](/Users/stan/code/toolkit/skills/sierra-best-practices/SKILL.md:48).
- Domain-accuracy claims were mostly confirmed: local Sierra docs exist, `sierras fetch-docs` exists, and `--workspace-name` is valid.

### 2. `sierra-powertool`

Why it is still net-positive:

- It gives the clearest task-to-command mapping in the portfolio at [`skills/sierra-powertool/SKILL.md:20`](/Users/stan/code/toolkit/skills/sierra-powertool/SKILL.md:20), [`skills/sierra-powertool/SKILL.md:113`](/Users/stan/code/toolkit/skills/sierra-powertool/SKILL.md:113), and [`skills/sierra-powertool/SKILL.md:250`](/Users/stan/code/toolkit/skills/sierra-powertool/SKILL.md:250).
- Current CLI help confirms most of the documented structure: `sim bench`, `conv`, `workspace`, `diff`, `issues`, and `fetch-docs` are all real commands.
- It already includes some interaction rules and limitation-reporting behavior, which is rare elsewhere.

Main weaknesses:

- The description is 252 chars and misses the 250-char discovery target.
- Error recovery still says `sierra login` at [`skills/sierra-powertool/SKILL.md:275`](/Users/stan/code/toolkit/skills/sierra-powertool/SKILL.md:275), but the actual CLI is `sierras`.
- The bench reference omits the now-available `resume` subcommand.

## Highest-Risk Skills

### 1. `music-discovery`

This is the clearest decomposition candidate.

Problems:

- It is 731 lines long, which breaks the progressive-disclosure target outright.
- It combines at least four different skill types in one file:
  - personal taste modeling
  - recommendation methodology
  - playlist materialization ops
  - database and metadata administration
- It hardcodes live secrets:
  - SoulSync API key at [`skills/music-discovery/SKILL.md:17`](/Users/stan/code/toolkit/skills/music-discovery/SKILL.md:17)
  - Last.fm API key at [`skills/music-discovery/SKILL.md:672`](/Users/stan/code/toolkit/skills/music-discovery/SKILL.md:672)
- It references nonexistent install paths on this machine at [`skills/music-discovery/SKILL.md:69`](/Users/stan/code/toolkit/skills/music-discovery/SKILL.md:69), [`skills/music-discovery/SKILL.md:339`](/Users/stan/code/toolkit/skills/music-discovery/SKILL.md:339), and [`skills/music-discovery/SKILL.md:351`](/Users/stan/code/toolkit/skills/music-discovery/SKILL.md:351): `~/.cursor/skills/music-discovery/...` does not exist.
- It does have real backing infrastructure:
  - `postgres`, `soulsync`, and `vibenet:latest` are present on `homelab`
  - `taste`, `audio_features`, and `playlist_exposures` tables exist
  - SoulSync DB columns like `bpm`, `lastfm_tags`, and `genres` do exist

Recommended split:

1. `music-discovery-core`
   - intent sheet
   - recommendation logic
   - user interaction modes
2. `music-playlist-sync`
   - `sync_playlist.py`
   - download / Plex refresh / VibeNet verification
3. `music-taste-ops`
   - taste-table sync
   - anti-tags / dislikes / playlist exposures
4. Keep `playlist-design.md` as a reference, not inline instructions.

### 2. `sierra-triage`

At 30 lines, it is not a working skill so much as a note.

Problems:

- No workflow phases or completion criteria at [`skills/sierra-triage/SKILL.md:6`](/Users/stan/code/toolkit/skills/sierra-triage/SKILL.md:6).
- No output template despite explicitly instructing the agent to write a result at [`skills/sierra-triage/SKILL.md:8`](/Users/stan/code/toolkit/skills/sierra-triage/SKILL.md:8).
- No exact tool sequence (`sierras issues`, `sierras conv show`, etc.).
- No anti-pattern section, examples, or interaction rules.

This should not be retired, but it should be rebuilt almost from scratch.

### 3. `skill-engineer`

The review framework is strong, but it now contains a domain-accuracy contradiction that will mislead transcript analysis.

Current contradiction:

- `cursor-chat-history` says Cursor transcripts can contain `tool_use` blocks at [`skills/cursor-chat-history/SKILL.md:22`](/Users/stan/code/toolkit/skills/cursor-chat-history/SKILL.md:22).
- Actual Cursor transcripts on this machine do contain `tool_use` blocks.
- `skill-engineer` taxonomy still says only `type: "text"` is stored at [`skills/skill-engineer/references/taxonomy.md:6`](/Users/stan/code/toolkit/skills/skill-engineer/references/taxonomy.md:6).

Other issues:

- The skill is 556 lines long.
- For multi-skill review, it hardcodes subagent parallelization at [`skills/skill-engineer/SKILL.md:218`](/Users/stan/code/toolkit/skills/skill-engineer/SKILL.md:218) rather than making it conditional on platform capabilities and current policy.

## Cross-Skill Findings

### 1. Discovery-surface drift is widespread

Skills over the 250-char frontmatter discovery budget:

- `deep-eval`
- `deep-research-prompt`
- `question-crystallization`
- `sierra-powertool`

This matters because `skill-engineer` correctly identifies description text as the discovery surface. Overlong descriptions are likely being truncated before they can help activation.

### 2. Only a small minority of skills have real constraints

The skills that meaningfully encode constraints and anti-shortcut behavior are:

- `sierra-best-practices`
- `deep-eval`
- `skill-engineer`

Most others are still closer to notes/reference docs than enforceable skills. That means they depend too heavily on base model behavior and user correction.

### 3. GOOD/BAD example coverage is nearly absent

Only `sierra-best-practices` has an actual GOOD/BAD pair in the main skill body. The rest of the portfolio is largely asking the model to infer behavior from prose alone.

### 4. Binary completion gates are missing almost everywhere

The portfolio strongly prefers workflows and checklists, but most skills still do not say what constitutes “done” for each phase. That is especially risky in:

- `sierra-bootstrap`
- `sierra-wrap-up-issue`
- `sierra-triage`
- `plugin-dev`
- `deep-research-prompt`

### 5. Path drift is a recurring accuracy problem

Verified path mismatches or likely stale paths:

- `music-discovery`: stale `~/.cursor/skills/...` script paths
- `sierra-bootstrap`: `~/code/agent-ctx/customer-docs/` is not present
- `sierra-wrap-up-issue`: `~/code/pronet/context-docs/specs/` is not present
- `sierra-best-practices`: `./context-docs/specs` is ambiguous against the current repo layout

### 6. The personal machine skills should not hardcode volatile numbers

These skills are useful as live environment references, but volatile facts go stale fast:

- `mini-ssh` says macOS `26.3` at [`skills/mini-ssh/SKILL.md:16`](/Users/stan/code/toolkit/skills/mini-ssh/SKILL.md:16), but the host is on `26.4`
- `mini-ssh` says disk `14% used` at [`skills/mini-ssh/SKILL.md:17`](/Users/stan/code/toolkit/skills/mini-ssh/SKILL.md:17), but the current host is at `17%`
- `homelab-ssh` lists services like `lidarr` and `soularr` at [`skills/homelab-ssh/SKILL.md:64`](/Users/stan/code/toolkit/skills/homelab-ssh/SKILL.md:64), but the current compose services do not include them

### 7. There is one especially important internal contradiction

`skill-engineer` depends on transcript semantics for ANALYZE mode, but its transcript assumptions are now contradicted by:

- real Cursor transcript data
- `cursor-chat-history`

This is the most important cross-skill inconsistency in the portfolio because it undermines the audit methodology itself.

## Usage Signal

Raw Cursor transcript hit counts by skill name:

- `sierra-powertool`: 62
- `sierra-best-practices`: 52
- `music-discovery`: 22
- `deep-eval`: 21
- `homelab-ssh`: 16
- `mini-ssh`: 16
- `cursor-chat-history`: 11
- `sierra-bootstrap`: 11
- `deep-research-prompt`: 9
- `plugin-dev`: 8
- `question-crystallization`: 8
- `sierra-triage`: 8
- `sierra-phrasing-eval`: 7
- `sierra-wrap-up-issue`: 6
- `skill-engineer`: 4
- `codex-proxy`: 2

This is not a quality score, but it does help prioritize where fixes have the highest payoff. By that measure, `sierra-powertool`, `sierra-best-practices`, `music-discovery`, and `deep-eval` deserve the most attention first.

## Per-Skill Fix Queue

### `codex-proxy`

- Add anti-triggers to the frontmatter: not for tool use, browsing, or file-editing tasks.
- Add one GOOD/BAD example pair.
- Label token-overhead numbers as a point-in-time measurement rather than a stable invariant.

### `cursor-chat-history`

- Add an anti-pattern section covering “assume timestamps exist”, “assume tool results are stored”, and “guess the project slug”.
- Add a minimal output template for conversation discovery and transcript triage.

### `deep-eval`

- Shorten frontmatter to stay under 250 chars.
- Add a GOOD/BAD example pair for evidence quality.
- Make the batch checkpoint output a first-class template.

### `deep-research-prompt`

- Shorten the description.
- Add an anti-pattern table and a small GOOD/BAD example set.
- Tighten done conditions for each phase.

### `homelab-ssh`

- Refresh the live stack tables from current compose config.
- Replace volatile capacity numbers with “check with command X” guidance where possible.
- Add explicit anti-triggers for tasks that belong in `music-discovery`.

### `mini-ssh`

- Remove or soft-label volatile machine facts.
- Add anti-triggers for tasks that belong in `homelab-ssh` or `music-discovery`.

### `music-discovery`

- Remove secrets immediately.
- Replace hardcoded install paths with skill-relative paths or a “resolve skill dir first” instruction.
- Split the skill into smaller operational units.
- Move most research evidence to references and keep the skill body operational.

### `plugin-dev`

- Add explicit completion criteria for “propagated” and “verified”.
- Add one GOOD/BAD example around version bumping and session-start synchronization.
- Clarify that it is Claude-plugin-specific unless expanded to other platforms.

### `question-crystallization`

- Rewrite the frontmatter to fit the discovery budget.
- Add GOOD/BAD examples for bounded-option questioning.
- Add a short tool-guidance section and a crisp “done” gate for each phase.

### `sierra-best-practices`

- Keep structure mostly intact.
- Clarify the feature-spec path so it cannot drift between repos.

### `sierra-bootstrap`

- Fix numbering and phase rigor.
- Replace vague “ask whenever needed” language with concrete STOP/ASK gates.
- Repair or remove stale `customer-docs` and spec-path assumptions.

### `sierra-phrasing-eval`

- Add anti-pattern coverage and examples.
- Add explicit completion criteria for transcript collection and evaluation completeness.

### `sierra-powertool`

- Fix `sierra login` to `sierras`.
- Add `sim bench resume`.
- Shorten the description to fit the discovery budget.

### `sierra-triage`

- Add a real workflow with exact tool sequence.
- Add a deliverable template and completion criteria.
- Add anti-patterns for trusting issue reports at face value or skipping transcript review.

### `sierra-wrap-up-issue`

- Fix stale spec paths.
- Add a concrete step-by-step workflow with done gates.
- Add tool guidance for PR discovery/creation and diff collection.

### `skill-engineer`

- Update transcript assumptions in `references/taxonomy.md`.
- Make multi-skill subagent fan-out conditional rather than mandatory.
- Move more reference material out of the main body to get under 500 lines.

## Recommended Order

1. P0: fix `music-discovery` secrets and stale install paths.
2. P1: fix `skill-engineer` transcript taxonomy so the review workflow is trustworthy.
3. P1: rebuild `sierra-triage` and repair path drift in `sierra-bootstrap` and `sierra-wrap-up-issue`.
4. P2: shorten overlong frontmatter in `deep-eval`, `deep-research-prompt`, `question-crystallization`, and `sierra-powertool`.
5. P2: refresh `homelab-ssh` and `mini-ssh` live-state facts.

## Evidence Notes

- Current local CLI state:
  - `codex-cli 0.118.0`
  - `Claude Code 2.1.92`
  - `sierras` present; current help confirms `sim bench`, `conv`, `workspace`, `issues`, `fetch-docs`, `diff`
- Current remote state:
  - `homelab`: Ubuntu 24.04, Docker 28.4.0, Compose v2.39.1
  - `mini`: macOS 26.4, Plex `1.43.0.10492-121068a07`
- Cursor transcript sample plus `rg` across transcript files confirmed `tool_use` blocks are present in at least some transcripts.

## External Sources

- [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API)
- [Last.fm artist.getTopTags](https://www.last.fm/api/show/artist.getTopTags)
- [Last.fm track.getTopTags](https://www.last.fm/api/show/track.getTopTags)
- [Last.fm track.getSimilar](https://www.last.fm/api/show/track.getSimilar)
- [Last.fm artist.getSimilar](https://www.last.fm/api/show/artist.getSimilar)
