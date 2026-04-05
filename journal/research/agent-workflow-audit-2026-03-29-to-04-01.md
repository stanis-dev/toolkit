# Agent Workflow Efficiency Audit

**Period**: Sunday March 29 - Tuesday April 1, 2026
**Scope**: 22 correction-bearing sessions across 4 projects (rec, toolkit, Sky, Pronet), ~1,840 JSONL lines, ~390 user messages, ~90 subagent transcripts spot-checked.

---

## Executive Summary

Across 22 sessions with substantive back-and-forth, I identified **~70 user corrections** (18 major, 22 medium, 30 minor) and **6 recurring correction patterns**. The most damaging patterns are (1) subagent research hallucinations and (2) declaring work "done" without end-to-end testing. Existing skills are effective when used but have specific blind spots -- particularly the sierra-powertool missing tag expectation fields and replay caching behavior. The `global.md` context file (created during this period) is still empty, representing the biggest immediate leverage point.

**Workflow Efficiency Assessment**: The current setup is approximately **60-65% efficient**. About a third of user corrections address gaps that could be eliminated by skill/context improvements. The remaining corrections involve judgment calls and novel situations where agent error is harder to prevent structurally.

---

## Part 1: Correction Patterns

### Pattern 1: "Trust but Don't Verify" (18 instances across 8 sessions)

The single most frequent correction pattern. The agent declares fixes, implementations, or research complete without verifying the result actually works.

| Session | Evidence |
|---------|----------|
| 823486e9 (Granite swap) | Two implementations declared "All done" -- both failed on first use. Agent ran linter checks but never tested transcription. |
| 2199e309 (Music playlist) | Blamed SoulSync for a "bug" without checking own pipeline. User: "thousands of people use it and I find it strange that we ran into something this obvious." |
| 67e4b88f (Transcription) | Declared PATH fix would work ("Rebuild the app and the transcribe button should work") -- it didn't. LogsTabView shipped causing app to crawl. |
| 9f4f3b0f (Meeting detect) | Fixed notification action handler when notifications never appeared at all. |
| 1c624c8a (VibeVoice) | Reported "no swap issues" using `ps aux` RSS which doesn't capture MPS allocations. User: "Another error in your judgment is yes there was swap happening." |
| 60e8d024 (Sky transfer) | Edited `personality.md` which has zero runtime effect -- never verified it's loaded. |
| 2f00b689 (Sky analyzer) | Inferred tag failures by comparing runs instead of reading actual TAG_EXPECTED fields. User: "Everything else is made up." |
| 77f031d0 (Sky analysis) | Ran entire analysis on wrong project (Pronet vs Sky) without noticing sim names didn't match. |

**Addressable?** Partially. A global rule could mandate "test before declaring done" and "verify org/workspace before starting," but this is fundamentally a judgment/diligence issue.

### Pattern 2: Subagent Research Hallucinations (14 instances across 3 sessions)

Subagents fabricated or misrepresented capabilities, benchmarks, and limitations.

| Session | Evidence |
|---------|----------|
| 67e4b88f | Fabricated WER numbers for Qwen3-ASR (5.76 WER invented). Claimed VibeVoice can't handle long audio when model card says "60-minute Single-Pass Processing." User: "we need to review with strong skepticism the entire research of the subagent." |
| 67e4b88f | Classified fairseq2 as "CPU only" on macOS from `/cpu` in a package URL. User: "where exactly did we get the idea that it will be CPU only?" |
| c90f854c | Presented inference as fact: called a code pattern a "deliberate design choice" with no evidence. Had to retract. |
| 4b99224e | Subagents did text-level verification only, not context-appropriate. User: "did the subagents eval text only, or did they also make sure to verify that through the context?" |

**Addressable?** Yes -- a "Model Research Protocol" skill could mandate: read the actual model card, check standardized leaderboards, never claim numbers without a URL, and always distinguish inference from evidence.

### Pattern 3: Over-Planning / Theorizing Before Doing (8 instances across 5 sessions)

Agent produces extensive analysis or planning when the user wants empirical exploration first.

| Session | Evidence |
|---------|----------|
| fd5b5a15 (Slack) | 6 consecutive assistant messages theorizing before user forced empirical exploration. User: "before planning anything, let's see what actual data we can grab." |
| 1c624c8a (VibeVoice) | 10 consecutive assistant exploration messages before user's second interaction. "Very clear picture" claimed 5 times without convergence. |
| 823486e9 (Granite) | Massive walls of stream-of-consciousness reasoning dumped to user. |
| faa5a230 (Transcript) | Response interrupted from excessive deliberation before output. |
| 42798829 (Assistant tab) | Response interrupted from excessive thinking. |

**Addressable?** Yes -- a global rule: "When debugging or exploring, prefer empirical testing over extended analysis. Do not produce more than 2 messages of planning without taking concrete action."

### Pattern 4: macOS App Development Gotchas (9 instances across 5 sessions)

Recurring gaps in macOS-specific development knowledge.

| Issue | Sessions | Recurrence |
|-------|----------|------------|
| PATH not inherited by GUI-spawned processes | 67e4b88f, 823486e9 | Identical issue hit twice |
| Python stdout buffering in non-TTY | 67e4b88f | Multiple instances in same session |
| SwiftUI performance with large content | 67e4b88f | LogsTabView loaded 190KB every 2s |
| MPS/Metal memory not in RSS | 1c624c8a | Used wrong monitoring tool |
| Cross-feature interaction blind spots | 9f4f3b0f | Dictation triggered meeting detector |

**Addressable?** Yes -- a "macOS App Development" skill or a CLAUDE.md entry in the rec project.

### Pattern 5: Pendulum Overcorrection (4 instances across 3 sessions)

When user provides a strategic redirect, agent swings too far in the new direction.

| Session | Evidence |
|---------|----------|
| f415676a | User said "use the agent" → agent wrote "lean heavily on agent judgment." User had to correct: "I would much rather try to use a deterministic system." Required 2 correction rounds. |
| 67e4b88f | Agent evaluated reliability when user cared about quality. Full re-evaluation required. User: "let's ignore the reliability... I only care about the quality." |
| 823486e9 | All major pivots driven by user -- lazy-load architecture, parakeet-mlx package, lighter alternative. Agent was purely reactive. |

**Addressable?** Partially. A global rule: "When the user provides a strategic correction, state back your understanding of the tension before committing to a direction."

### Pattern 6: Wrong Metric / Audience Optimization (6 instances across 4 sessions)

Agent optimizes for the wrong dimension of quality, or targets the wrong audience.

| Session | Evidence |
|---------|----------|
| 67e4b88f | Evaluated reliability over quality. Presented % stats when user wanted qualitative analysis. |
| f415676a | Plan mode workflow misunderstanding -- thought only deep-dive mode needed a plan. |
| c90f854c | Wrote briefing for non-technical audience when user is the developer. User: "eliminate context and text and data that would be addressed at somebody who didn't already know what simulations are." |
| 32852cd3 | Said Cursor doesn't support hooks (stale knowledge). |

**Addressable?** The audience issue is addressable via global.md ("I am a senior developer; always assume technical depth").

---

## Part 2: Skill Gap Analysis

### Skills Effectively Used (no gaps)

| Skill | Sessions | Notes |
|-------|----------|-------|
| deep-eval | efa1529d, 7d573cec, 832d7dab, 4b99224e, 67e4b88f | Protocol followed rigorously when invoked. Batch checkpointing, evidence requirements, and subagent management all worked. |
| plugin-dev | 129f6d66 | Used correctly for version bumping and plugin refresh. Was trimmed during the session to remove obvious content. |
| cursor-chat-history | f415676a | Read and followed correctly for transcript search. |
| music-discovery | f415676a, 2199e309 | Scripts updated, deep research prompt generated. Sync script gaps (skip_count, last_rated_at) were identified and fixed during sessions. |
| deep-research-prompt | f415676a | Template used correctly to generate the temporal taste algorithm research prompt. |

### Skills With Specific Gaps (need amendment)

#### 1. sierra-powertool

**Current state**: 370-line comprehensive CLI reference.

**Gaps identified across sessions**:

| Gap | Session(s) | Impact |
|-----|-----------|--------|
| No mention of `TAG_EXPECTED[met/missing]`, `TAG_FORBIDDEN[present]` in text replay output | 2f00b689 | Agent inferred tag failures instead of reading explicit fields. MAJOR correction required. |
| No documentation of `replay-all` bypassing build-hash filters while `replay --list --json` doesn't | 2f00b689, 832d7dab | 12+ turns of confusion across 2 sessions. |
| No warning about `wait-all` tracking ALL sims in workspace, not just recently triggered | 60e8d024 | Agent waited on 1443 untriggered sims. |
| `--org` default is `pronet` but skill doesn't warn about verifying org matches project context | 77f031d0 | MAJOR: entire analysis on wrong project. |
| No mention of replay caching after code changes (stale data until `--no-cache` or `replay-all`) | 31cace56, 832d7dab | False alarm that fix didn't work; 12-turn caching loop. |

**Status**: NOT corrected. All gaps still present in skill v1.3.0.

#### 2. sierra-best-practices

**Gaps identified**:

| Gap | Session | Impact |
|-----|---------|--------|
| No mention that `personality.md` is NOT loaded into the agent runtime | 60e8d024 | Agent edited a file with zero effect. |
| No guidance on journey phrasing instructions format (bullet-point for Studio compatibility) | 60e8d024 | Agent used markdown headers; user corrected to bullets. |

**Status**: NOT corrected.

### Skills That Don't Exist But Should

#### 1. macOS App Development (for rec project)

**Justification**: 9 corrections across 5 sessions involve macOS-specific gotchas that repeat.

**Content**: PATH inheritance for GUI-launched subprocesses, MPS/Metal memory monitoring (not `ps aux`), SwiftUI performance with streaming/large content, Python subprocess stdout buffering (`-u` flag), ScreenCaptureKit audio exclusion patterns, cross-feature interaction testing (own mic access triggering own listeners).

**Priority**: HIGH -- these exact issues recurred within the 4-day window.

#### 2. Model Research Protocol

**Justification**: 14 subagent hallucination instances across 3 sessions. User explicitly called this out as a pattern.

**Content**: Always read the actual model card (don't infer). Check standardized leaderboards (Open ASR, MMLU, etc.) rather than model card cherry-picks. Never cite a number without a verifiable URL. Distinguish "the code shows X" from "the team decided X." When comparing models, test empirically on the user's actual hardware before recommending.

**Priority**: HIGH -- subagent hallucinations were the most damaging pattern.

#### 3. Agent Interaction Heuristics (global context)

**Justification**: Patterns 1, 3, 5, and 6 are cross-project behavioral issues that a global rule could address.

**Content**: Test before declaring done. Empirical first, theory second. When user redirects strategy, state the tension before committing. Always assume technical audience. Don't use `security dump-keychain`. Don't add `--no-cache` flags without asking.

**Priority**: MEDIUM -- these are behavioral guidelines, harder to enforce than knowledge skills.

---

## Part 3: Specific Recommendations

### Immediate Actions (High Impact, Low Effort)

**1. Populate `context/global.md`** with cross-project behavioral rules:

```markdown
# Global Context

## Verification Requirements
- Never declare a fix or implementation complete without end-to-end testing on the actual use case.
- When subagents perform research, spot-check claims against primary sources. Never cite metrics
  without a verifiable URL.

## Interaction Style  
- I am a senior developer. Always assume technical depth. Don't explain what simulations are,
  what APIs do, or how tools work at a conceptual level.
- When debugging or exploring unknowns, prefer empirical testing over extended analysis. Do not
  produce more than 2 planning messages without taking concrete action.
- When I provide a strategic correction, state back your understanding of the tradeoff before
  committing to a direction. Don't swing to the opposite extreme.

## macOS Development
- macOS GUI apps do NOT inherit shell PATH. Always set PATH explicitly when spawning subprocesses
  (include /opt/homebrew/bin, /usr/local/bin).
- Python stdout is buffered in non-TTY contexts. Always use `python3 -u` or `PYTHONUNBUFFERED=1`.
- MPS/Metal memory usage does NOT appear in `ps aux` RSS. Use `memory_pressure` or Activity Monitor.
- SwiftUI: never put large (>10KB) text in a single Text view inside ScrollView.

## Safety
- Never run `security dump-keychain` -- it triggers system-wide permission dialogs.
- Never add `--no-cache` flags to API calls without asking first.
- Always save expensive computation results unconditionally before attempting to parse them.
```

**2. Amend sierra-powertool** with tag expectations and replay caching:

Add after the "Debugging Simulation Replays" section:
- Document `TAG_EXPECTED[met]`, `TAG_EXPECTED[missing]`, `TAG_FORBIDDEN[present]` fields in text replay output.
- Document replay caching behavior after code changes.
- Add warning: "When working in a non-pronet org, always verify `--org` flag matches the project before running commands."
- Document that `wait-all` monitors ALL sims in workspace, not just recently triggered ones.
- Document that `replay-all` bypasses build-hash filters.

**3. Amend sierra-best-practices**:
- Add: "`personality.md` is documentation only -- it is NOT loaded into the agent runtime. Use Rules or journey phrasing instructions for runtime behavioral guidance."
- Add: "Studio journey phrasing instructions require bullet-point format, not markdown headers."

**4. Add CLAUDE.md to rec project** with macOS gotchas:

The current rec/CLAUDE.md only has "Prefer hardcoding stuff." It should include the macOS development section from global.md, plus: "This is a SwiftUI + AppKit hybrid macOS app built with `swiftc`. When spawning Python subprocesses, always set PATH explicitly and use `-u` for unbuffered output."

### Medium-Term Actions

**5. Create "Model Research Protocol" skill**:
For any session involving model evaluation or recommendation. Mandate: read model card, check leaderboard, test on actual hardware, never fabricate metrics.

**6. Create "macOS App Development" skill** (or keep in rec CLAUDE.md if it's only for rec):
Codify the 9 recurring macOS gotchas as a checklist.

### Skills That Worked Well (Keep As-Is)

- **deep-eval**: The protocol is solid. Sessions where it was invoked (efa1529d, 7d573cec, 832d7dab, 4b99224e) ran with minimal corrections. The checkpointing and evidence requirements consistently produce thorough work.
- **plugin-dev**: After the trim in session 129f6d66, it's appropriately concise. No further changes needed.
- **music-discovery**: The sync script was updated during sessions to capture skip_count and other missing fields. The research prompt template worked well.

---

## Part 4: Workflow Metrics

### Session Outcome Distribution

| Outcome | Count | Sessions |
|---------|-------|----------|
| Smooth execution (0-1 corrections) | 6 | faa5a230, efa1529d, 5207bb0a, 42798829, 7d573cec, 24a95e92 |
| Moderate friction (2-4 corrections) | 9 | 129f6d66, 32852cd3, 2199e309, 9f4f3b0f, fd5b5a15, 8c380a96, 60e8d024, 31cace56, c90f854c |
| High friction (5+ corrections) | 7 | f415676a, 1c624c8a, 823486e9, 67e4b88f, 2f00b689, 77f031d0, 4b99224e |

### Correction Severity Distribution

| Severity | Count | % of Total |
|----------|-------|------------|
| Major | 18 | 26% |
| Medium | 22 | 31% |
| Minor | 30 | 43% |

### Corrections by Root Cause

| Root Cause | Count | Addressable by Skill/Rule? |
|------------|-------|---------------------------|
| Didn't verify result | 18 | Partially (global rule) |
| Subagent hallucination | 14 | Yes (research protocol skill) |
| Over-planning/theorizing | 8 | Yes (global rule) |
| macOS platform gap | 9 | Yes (skill or CLAUDE.md) |
| Sierra CLI knowledge gap | 8 | Yes (powertool amendment) |
| Wrong metric/audience | 6 | Partially (global.md) |
| Pendulum overcorrection | 4 | Partially (global rule) |
| Stale knowledge | 2 | No (inherent) |
| Invasive system command | 1 | Yes (global rule) |

**~47 of 70 corrections (67%)** are addressable through the recommendations above.

### Skill Invocation Rate

| Skill | Times Used | Adequacy |
|-------|-----------|----------|
| sierra-powertool | 9 sessions | Used but has specific gaps (tag expectations, caching, org verification) |
| sierra-best-practices | 8 sessions | Used but missing personality.md and Studio format guidance |
| deep-eval | 5 sessions | Effective when invoked, no changes needed |
| plugin-dev | 2 sessions | Trimmed during the period, now appropriate |
| music-discovery | 2 sessions | Updated during the period |
| deep-research-prompt | 1 session | Effective |
| cursor-chat-history | 1 session | Effective |
| sierra-bootstrap | 0 sessions | Not applicable (no new issue starts in the evaluated period) |

---

## Part 5: Already-Corrected Items

| Item | When Corrected | Session |
|------|---------------|---------|
| plugin-dev skill too basic | Mar 29 (session 129f6d66) | Trimmed to remove obvious "how to edit a file" content |
| music-discovery sync script missing skip_count, last_rated_at, duration | Mar 29 (session 129f6d66) | Added fields to sync_taste.py and DB schema |
| global.md mechanism created | Mar 29 (session 32852cd3) | Created context/global.md + updated session-start.sh hook |

**Not yet corrected**:
- sierra-powertool tag expectations (still missing)
- sierra-powertool replay caching documentation (still missing)
- sierra-powertool org verification warning (still missing)
- sierra-best-practices personality.md note (still missing)
- sierra-best-practices Studio format guidance (still missing)
- global.md content (still placeholder)
- rec CLAUDE.md macOS gotchas (still just "prefer hardcoding")
- Model Research Protocol skill (does not exist)
- macOS App Development skill (does not exist)
