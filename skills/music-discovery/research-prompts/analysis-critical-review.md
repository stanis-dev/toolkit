# Critical Comparative Analysis: Temporal Taste Research Results

Three models (Claude, Gemini, GPT) responded to the same research prompt on temporal taste
modeling for a personal ~2000-track library with Plex + PostgreSQL + LLM agent. This document
critically compares their proposals across all 7 research areas, separating what the literature
genuinely supports from what is dressed-up speculation.

---

## 1. Signal Weighting: Combining Rating, Plays, Skips

### What they propose

**Claude** -- multiplicative confidence model:
```
base_affinity = (rating/10) × (1 + 0.5 × LN(1 + play_count)) / (1 + skip_penalty)
```
Rating is the seed. Play count multiplies confidence (log-dampened). Skip penalty divides.
Cites Hu-Koren-Volinsky (2008) for the log confidence function.

**Gemini** -- weighted additive of two components:
```
base = 0.55 × R_decay + 0.45 × H_affinity
```
Where H_affinity is a Bayesian-smoothed engagement ratio scaled to [-1, 1]. Explicit rating
and implicit behavior are separate additive terms with fixed weights.

**GPT** -- additive around a neutral center:
```
base_affinity = Clamp01(0.50 + 0.40×R + 0.20×P - 0.30×S)
```
Each signal type has its own weight. Starts at 0.50 (neutral) and adjusts up/down.

### Where they genuinely agree

- Explicit rating should carry the most weight among individual signals.
- Raw play_count should be log-dampened to prevent heavy-repeat tracks from dominating.
- Skip signal needs confidence gating (not raw count).

### Where they diverge and why it matters

The three architectures produce fundamentally different scoring dynamics:

- **Claude's multiplicative form** means a track with zero plays gets base_affinity from rating
  alone (the confidence multiplier is 1.0). But a track with many plays and a mediocre rating gets
  amplified, which may overvalue guilty pleasures.
- **Gemini's additive form** lets behavioral affinity actively *subtract* from the score (range is
  [-1, 1]). A heavily-skipped track can drag the score below what the rating alone would produce.
  The 55/45 split gives rating a slight edge but behavior nearly equal say.
- **GPT's centered form** caps at [0, 1] with the center at 0.50. The asymmetry in weights
  (rating 0.40 vs play 0.20 vs skip -0.30) means skips are weighted 1.5x as heavily as plays,
  which is a deliberate design choice reflecting that negative signals are more informative per
  event.

### Evidence quality

- Claude adapts HKV's α=40 down to α=0.5 -- an 80x reduction. HKV studied a multi-user system
  with millions of interactions. The adaptation to single-user is reasonable in direction but the
  specific value of 0.5 is a guess, not a derivation.
- Gemini's 55/45 rating-vs-behavior split is presented as a recommendation but has no citation.
  The reasoning (ADHD → behavior outpaces curation) is plausible but the specific numbers are
  invented.
- GPT's weights (0.40/0.20/0.30) are the most transparent about being starting defaults, not
  literature constants.

### What's genuinely new

GPT's multi-timescale play memories (`play_mem_7/30/180`) change the *input* to signal weighting,
not just the formula. Instead of asking "how should we weight aggregate play_count," GPT asks "what
if we had temporally-decomposed play data?" This reframes the problem. Claude and Gemini both build
elaborate math to compensate for data they don't have; GPT says collect better data first.

### Risks

The weight ratio between rating and behavior is the single highest-sensitivity parameter in Area 1.
A shift from 55/45 to 70/30 would dramatically change which tracks surface. None of the three
provide empirical guidance for calibrating this -- it requires listening to generated playlists and
tuning by ear.

---

## 2. Rating Decay Functions

### What they propose

**Claude** -- power-law decay toward zero:
```
rating_decay = 1.0 / (1.0 + (days/half_life)^0.5)
```
Half-lives: 545 / 365 / 180 days (high/mid/low). The rating's *weight* diminishes over time.
A 9/10 from 3 years ago contributes almost nothing.

**Gemini** -- bounded exponential decay toward library mean:
```
R_decay = μ + (R - μ) × exp(-λ × days)
```
Half-lives: 730 / 180 / 90 days (high/mid/low). The rating *regresses toward ~5/10*.
A 9/10 from 3 years ago becomes approximately a 5.5/10.

**GPT** -- stable floor plus temporal component:
```
R = r × (0.65 + 0.35 × D(age, H_r))
```
Half-lives: 540 / 270 / 180 days. 65% of the rating is permanent. Only 35% decays.
A 9/10 from 3 years ago retains roughly 65-70% of its original value.

### Concrete impact: a 9/10 rated 3 years ago

- Claude: weight drops to ~0.15 → the rating barely matters
- Gemini: regresses to ~5.5/10 → treated as an average track
- GPT: retains ~6.5/10 → still clearly above average

This is not a minor parametric difference. These three approaches produce *categorically different*
outcomes for old favorites. The choice here determines whether a beloved-but-not-recently-played
track still surfaces or gets buried.

### Where they genuinely agree

- Asymmetric decay (high ratings decay slower than low ratings) is a reasonable heuristic.
- Pure linear decay is destructive and should not be used.
- Some form of decay is appropriate for a single-user system.

### Evidence quality

**This is the weakest area across all three responses.** Critical findings:

- Claude cites Koren (2009) who found "prediction quality improves as we moderate that time decay,
  reaching best quality when there is no decay at all" -- then argues this doesn't apply to
  single-user systems. That argument is plausible but unvalidated.
- Gemini cites similar half-life literature (Ardagelou & Arampatzis 2017: ~150 days for movies)
  then extrapolates to music with no music-specific evidence.
- GPT explicitly warns against converting old ratings to different values, citing a half-life paper
  that found the "stable + temporal" variant outperforms pure decay.
- **No published research directly tests asymmetric decay rates for high vs. low ratings.**
  All three acknowledge this. The idea is a plausible heuristic that all three independently
  converged on, which suggests it's reasonable in direction, but the specific half-life values
  are all made up.
- The half-life spread is enormous: for high ratings, Claude says 545 days, Gemini says 730 days
  (34% longer). For low ratings, Claude says 180 days, Gemini says 90 days (2x shorter). GPT falls
  between. None can justify their specific values with evidence.

### What's genuinely new

GPT's "stable + temporal" formulation is the most important insight. It operationalizes Koren's
finding: if no decay at all produces the best predictions, then heavy decay is worse than light
decay, and keeping a permanent floor is safer than letting old ratings vanish. This is the one
approach with indirect empirical support (Koren 2009 + the half-life paper GPT cites).

### Risks

Rating decay interacts with reintroduction (Area 5). Gemini's decay-toward-mean naturally
resurfaces old low-rated tracks without any explicit reintroduction mechanism -- a 3/10 from
2 years ago is already a 4.5/10. Claude's decay-toward-zero makes old negative ratings
disappear entirely, requiring a separate reintroduction system. GPT's stable floor keeps old
negatives *permanently negative* unless explicitly overridden, putting more weight on the
reintroduction mechanism.

---

## 3. Skip Signal Interpretation

### What they propose

**Claude** -- Bayesian penalty subtracted from score:
```
skip_penalty = smoothed_rate × confidence × never_played_boost
```
Priors: 2 skips + 5 plays (29% baseline). Confidence grows with interactions. Calibrates
against the user's personal baseline (σ thresholds). Cross-context detection: if skipped in
one context but played in others, infer context mismatch.

**Gemini** -- skips integrated into behavioral affinity ratio:
```
H_affinity = ((P+2) / (P + S×w_skip + 3) × 2) - 1
w_skip = 1 - 0.5×exp(-days_since_play/7)
```
Priors: 2 plays + 1 skip (optimistic). Recent skips carry half weight if track was recently
played (the "satiety index"). Provides a 4-category disambiguation matrix (active dislike /
stale dislike / satiety / context mismatch).

**GPT** -- confidence-gated penalty using rolling memories:
```
S_raw = (0.60 × skip_mem_30 + 0.40 × skip_mem_180) × evidence × neg_conf
```
Where neg_conf is a multi-factor calculation (skip ratio, never-played, rating, corroborating
plays, recency). Evidence gating: `1 - exp(-interactions/4)`. Below ~3-4 interactions, skip
signal is suppressed almost entirely.

### Where they genuinely agree

- Raw skip rate is unreliable for low-interaction tracks. All three use some form of Bayesian
  smoothing or confidence gating.
- Skips on tracks that have never been fully played are the strongest negative signal.
- Context-mismatched skips should not destroy global affinity.
- More interactions = more confidence in the skip signal.

### Where they diverge and why it matters

- **Structure**: Claude and GPT treat skips as a *penalty* (subtracted or reducing the score).
  Gemini integrates skips into the *base score itself* (the engagement ratio). This means in
  Gemini's model, you cannot separate "how good is this track" from "how often was it skipped."
  Claude and GPT can tune skip sensitivity independently.
- **Recency weighting**: Gemini's satiety index reduces skip damage when the track was recently
  played -- the reasoning is that recent skips after recent plays are saturation, not dislike.
  Claude and GPT don't model this directly (GPT captures it implicitly through rolling memories).
- **Disambiguation**: Gemini provides an explicit matrix of 4 skip categories. Claude provides
  cross-context consistency checking. GPT uses confidence gating where low-evidence skips are
  simply suppressed. All three are heuristics -- none can truly disambiguate with aggregate data.

### Evidence quality

GPT states the critical finding plainly: **"The sources I reviewed do not provide a universal
skip:play exchange rate."** This is honest and important. Claude cites Lamere's Spotify finding
(~50% of songs never fully listened to) and Deezer's Beta distribution priors. Gemini cites
similar skip behavior research. But none of the specific ratios (2:5, 2:1, or the multi-factor
weights) come from the literature. They are all educated guesses.

The one firmly evidence-backed claim: skip behavior is contextual and session-dependent (Mehrotra
et al., Brost et al. MSSD dataset, Meggetto et al. CIKM 2021). All three cite this literature
and reach the same conclusion: aggregate skips are fundamentally ambiguous.

### What's genuinely new

Gemini's recency-weighted skip satiety is a creative idea specific to this problem. If a track
was played yesterday and skipped today, that skip probably means "I just heard this" not "I
dislike this." The formula `w_skip = 1 - 0.5×exp(-days/7)` is not from any paper, but the
reasoning is sound for an ADHD listener who may hyper-fixate then abruptly burn out.

GPT's rolling memories eliminate the need for elaborate recency heuristics -- if you track
`skip_mem_30` vs. `skip_mem_180`, you can see whether skips are recent or historical without
any special formula.

### Risks

Skip handling has the highest potential for unintended harm. An overly aggressive skip penalty
permanently buries tracks that were skipped for contextual reasons. An overly lenient one lets
genuinely disliked tracks keep surfacing. The safe starting position is GPT's approach:
confidence-gate heavily and require corroboration before acting on skips.

---

## 4. Staleness Prevention and Cooldowns

### What they propose

**Claude** -- exponential recovery + count freshness + exploration bonus:
```
time_freshness = 1 - exp(-hours / 72)           -- 72-hour cooldown
count_freshness = 1 / (1 + LN(1 + plays/30))    -- saturation at 30
exploration = 0.1 × SQRT(LN(total_plays) / GREATEST(plays, 1))  -- UCB1-inspired
```
Recovery is monotonic -- once the cooldown passes, the track is fully available.

**Gemini** -- logistic curve with exploration bonus and dynamic hyper-fixation:
```
M_freshness = LEAST(1.25, (days/(days+7)) × 1.35)   -- 7-day cooldown
```
Exploration bonus pushes past 1.0 (up to 1.25x) for long-forgotten tracks. If a track is in
the top 5% of recent plays AND play_count > 20, cooldown extends to 21 days ("dopamine detox").

**GPT** -- hard cooldown steps + soft fatigue + bell-curve freshness:
```
cooldown_mod: 0.05 / 0.25 / 0.60 / 0.85 / 1.00 at 1/3/7/14+ days
fatigue = 1 - exp(-(0.70×play_mem_7 + 0.30×play_mem_30) / 3.0)
freshness = (1 - exp(-age/30)) × exp(-age/365)   -- rises then FALLS
```
Context-dependent: work/reading uses 1/3/7/14-day schedule; gym/driving compresses to 1/2/5/10.

### Where they genuinely agree

- A track just played should be heavily suppressed.
- Some form of diminishing returns on total play count is needed.
- Exploration bonuses for neglected tracks help prevent playlist stagnation.

### Where they diverge and why it matters

**Cooldown duration**: Claude says 72 hours. Gemini says 7 days. GPT says it depends on context.
This is the most listener-visible parameter -- if you generate a playlist daily, the 72-hour
cooldown means a favorite can appear in every third playlist. The 7-day cooldown means once a week.
For ADHD-driven hyper-fixation cycling, the right answer probably varies per person and per phase.

**Recovery shape**: Claude and Gemini both use monotonic recovery -- the longer since last play,
the higher the freshness. GPT uniquely uses a bell curve: freshness rises after a gap, peaks around
2-3 months, then *falls again* for tracks that have gone completely cold. The reasoning: a track
not heard in 2 years is not "maximally fresh" -- it may have been forgotten for good reason. This
is a defensible design choice, though no paper directly supports this specific shape.

**ADHD-specific**: Gemini's "dopamine detox" protocol (extending cooldown to 21 days for
hyper-fixated tracks) is the only proposal directly targeting the ADHD cycling pattern described
in the research prompt. It requires detecting hyper-fixation, which is hard with aggregate data.

### Evidence quality

The research supports the general shape (inverted-U / Berlyne curve, confirmed by Chmiel &
Schubert meta-analysis and Deezer Ex2Vec), and the specific finding that preference peaks around
~10 exposures before declining. But specific cooldown durations, saturation points, and exploration
weights are all invented. Claude's citation of radio programming (2-6 hour cooldowns) is
interesting but those are for passive broadcast audiences, not active personal listening.

### What's genuinely new

GPT's context-dependent cooldowns are the most practically useful idea. Work/reading playlists
need more variety than gym playlists -- this is intuitive and aligns with the activity-context
research (Gong et al.: energy differences up to t=49.48 between running and relaxing). Applying
the same cooldown everywhere is a blunt instrument.

### Risks

Cooldown is the parameter most likely to produce immediate user frustration. Too short: "why is
this track in every playlist?" Too long: "where did my favorite track go?" The safest approach
is GPT's: start with a conservative step function, make it context-dependent, and tune from there.

---

## 5. Soft Reintroduction of Rejected Tracks

### What they propose

**Claude** -- multi-factor probability model:
```
reintro_probability = memory_decay × taste_drift × (1 - rejection_strength)
```
Memory decay: ACT-R power-law with 180-day inflection. Taste drift: checks if recent
ratings in the same genre trended upward. Rejection strength: tiered 0.3-0.9. Placement-
dependent thresholds (0.25/0.40/0.60). Tracks with `disliked=true` never auto-reintroduced.

**Gemini** -- simple binary trigger:
```
WHEN R < 0.5 AND ACT_R_Activation < -2.5 THEN 1.20x boost ELSE 1.0
```
If a low-rated track has been forgotten long enough (ACT-R activation below -2.5), apply
a flat 1.20x multiplier. No escalation. If skipped again, deep hibernation.

**GPT** -- separate rehab lane with hard quotas:
```
p_reintro = cap_ctx × time_recovery × (0.5 + 0.5×uncertainty) × (0.5 + 0.5×drift) × context_fit
```
Hard reject rules prevent auto-reintroduction of strong negatives. Per-context caps (0.05-0.15).
Quota: max 1 rehab track per 20 normal tracks for work, 2/25 for gym. Only soft negatives and
uncertain tracks are eligible.

### Where they genuinely agree

- Tracks explicitly marked as disliked should not be automatically reintroduced.
- Time should erode negative impressions (all cite ACT-R memory decay).
- Context matters for reintroduction (a track rejected in one context might work in another).

### Where they diverge and why it matters

**Scope**: Gemini's model can reintroduce *any* low-rated track once memory fades enough. Claude
limits by rejection strength but has no hard quotas. GPT draws the sharpest line: hard rejects
(disliked, rating <= 2, 3+ skips with 0 plays) are permanently excluded from automatic
reintroduction. Only soft negatives (mild skip history, rating 3-4, uncertain tracks) enter rehab.

**Integration**: Gemini and Claude fold reintroduction into the main scoring formula (a multiplier
on the score). GPT puts reintroduction in a separate lane with its own quota. This means in GPT's
model, a rehab track never *outscores* a normal track -- it gets a reserved slot. In Claude/Gemini,
a sufficiently decayed old negative could theoretically outscore a mediocre current positive.

**Escalation**: Only GPT has escalating recovery half-lives (60/180/365 days based on negative
strength). If a track fails reintroduction (skipped again), Gemini says "deep hibernation" but
doesn't specify how deep. Claude's model would naturally increase rejection_strength after a
second skip, lengthening the wait. GPT's hard reject rules would likely catch repeat offenders
after enough corroborating skips.

### Evidence quality

The ACT-R basis is the most research-grounded element across all three. Lex, Kowald, and Schedl
(2020) validated the base-level learning equation against 1.1 billion Last.fm listening events.
Reiter-Haas et al. (RecSys 2021) fitted d values for music specifically. The *memory decay*
component is well-supported.

However, the *reintroduction trigger logic* is entirely heuristic in all three. The ISMIR 2020
paper GPT cites (repeated exposure rescuing uncertain items) supports reintroduction for
*uncertain* items but explicitly not for entrenched dislikes. This is the strongest evidence-based
constraint: **rehab should target ambiguity, not known rejection.**

### Risks

Reintroduction gone wrong is the most annoying possible failure mode -- having a disliked track
repeatedly resurface. GPT's approach is safest: hard rejects stay out, soft negatives get a
limited quota, and the user never hears more than 1 rehab track per 20 in a focus playlist.
Gemini's simple trigger is riskiest because the 1.20x boost is applied to *any* low-rated
forgotten track, including ones the user genuinely dislikes but hasn't flagged.

---

## 6. Context-Specific Signal Interpretation

### What they propose

**Claude** -- per-context Beta distribution:
```
context_weight = (context_plays + 1) / (context_plays + context_skips + 2)
```
Uniform prior. Minimum 5 observations to use per-context weights. Cross-context skip detection
(skipped here but played elsewhere → context mismatch, not dislike). Hierarchy: preset > 
time-of-day > mood.

**Gemini** -- Euclidean distance from context centroids:
```
P_context = GREATEST(0.5, 1.0 - SQRT(distance²))
```
Hardcoded centroid coordinates per context. context_tags give 1.0x boost. anti_tags give 0.0
(hard exclusion). No per-context learning from interaction data.

**GPT** -- shrinkage estimator blending local and global:
```
score = λ × context_score + (1-λ) × global_score
λ = n_ctx / (n_ctx + 6)
```
Coarse contexts only (5 categories, not fine presets). Proposes persisting playlist exposures
for weak context labeling. User controls: never_in_context, snooze_until, rehab_allowed.

### Where they genuinely agree

- Global scoring alone is insufficient; context matters measurably.
- With ~2000 tracks and one user, context granularity must be coarse to avoid data sparsity.
- anti_tags (hard exclusions) are a practical necessity for context-mismatched tracks.
- Audio feature alignment is a useful prior even before per-context behavioral data exists.

### Where they diverge and why it matters

**Data requirement**: Claude's per-context Beta needs per-context play/skip counts, which the
current database doesn't store. Gemini needs only audio features (already available) and tags
(partially available). GPT's shrinkage estimator also needs per-context data but degrades
gracefully (falls back to global when evidence is sparse).

**Granularity**: Gemini works at the preset level (deep_work, gym, reading). GPT explicitly warns
against this -- "per-preset temporal models will get noisy fast" -- and recommends 5 coarse
categories. Claude allows per-preset but includes a 5-observation minimum threshold.

**Learning vs. rules**: Gemini is entirely rule-based (centroids + tags). Claude learns from
per-context interactions once data accumulates. GPT blends both: rules (tags as priors) plus
learned signals (shrinkage toward global when evidence is weak).

### Evidence quality

The research consensus is strong that context matters: Spotify CoSeRNN showed 10%+ improvement
from context-aware modeling, and activity-context research (Gong et al.) measured enormous
audio feature differences between activities. However, all that research was on streaming
platforms with rich per-session data. For a periodic-sync system with aggregate counts, the
transfer is indirect.

GPT's proposal to persist playlist exposures (`playlist_id, context, track_id, generated_at`)
and attribute play/skip deltas to the most recent context is the most practical bridge. It's
"weak labeling" -- imprecise but better than no context data at all.

### What's genuinely new

GPT's user controls (never_in_context, snooze_until, rehab_allowed) are a practical insight that
none of the pure algorithmic approaches address. Music taste is too personal and contextual for
algorithms alone. Providing explicit override mechanisms reduces the stakes of getting the
algorithm wrong.

### Risks

The main risk is over-segmenting: with 2000 tracks split across 5+ contexts, some context bins
will have very few tracks with meaningful interaction data. Noise in per-context scores would then
dominate signal. GPT's shrinkage estimator handles this best (blending toward global when evidence
is thin), while Claude's hard 5-observation threshold is a cruder but effective safeguard.

---

## 7. SQL Implementation and Practical Feasibility

### What they propose

**Claude** -- a single complete CTE query:
Three-stage CTE (params → user_stats → scored → final). Works with the existing `taste` table
schema. No infrastructure changes needed. Ready to run today.

**Gemini** -- a single complete CTE query:
Three-stage CTE (base_metrics → component_calculations → utas_ranking). Also works with existing
schema. Includes COALESCE/GREATEST for null safety. The LLM agent injects context centroids at
query time.

**GPT** -- schema change + simpler queries:
Requires adding rolling memory columns (`play_mem_7/30/180`, `skip_mem_30/180`, plus
`prev_play_count`, `prev_skip_count`, `prev_sync_at`). The `sync_taste.py` script must be
modified to compute decayed deltas at each sync. The ranking query itself becomes simpler because
temporal decomposition happens at sync time, not query time.

### Practical assessment

Claude and Gemini offer immediate gratification: paste the SQL, run it, get a ranked list.
But both are compensating for data limitations with formula complexity. GPT requires upfront
investment (modify sync_taste.py, add columns, run a migration) but the resulting system is
more honest about its signals and easier to debug.

The current `sync_taste.py` (339 lines) already handles Plex API → PostgreSQL sync. Adding
rolling memory counters means: (1) new columns on the taste table, (2) on each sync, compute
deltas since previous sync and apply exponential decay to the memory fields, (3) store
prev_play_count and prev_skip_count for delta computation.

### Edge cases

All three handle the basics (new tracks, unrated tracks, never-played tracks) reasonably. The
notable differences:

- **Unrated tracks**: Claude zeros out base_affinity. Gemini coalesces to 5/10. GPT sets R=0
  (neutral). GPT's approach means unrated tracks start at 0.50 (center) -- neither penalized
  nor boosted. Gemini's coalesce to 5 is similar. Claude's zero is harsh and would bury unrated
  tracks entirely.
- **Recently re-rated downward**: Only GPT addresses this: "let the rating term dominate for at
  least one rating half-life; do not allow historical play count to completely override a recent
  explicit rerating." Neither Claude nor Gemini handle this case.
- **Outro-skip problem**: Only Gemini addresses this: tracks with long fade-outs accumulate false
  skips. Proposes an `outro_skip_safe` tag to halve skip penalty. This is a real problem with
  Plex's aggregate data.

---

## Synthesis: What We Actually Know

### Firmly evidence-backed claims

1. **Multiple timescales matter.** Music preference has fast-moving (weekly fixations) and
   slow-moving (enduring taste) components. Validated by Spotify multi-timescale research,
   ACT-R relistening models, and the LFM-1b dataset analysis.

2. **Bayesian smoothing is necessary for skip rates.** Small samples produce unreliable rates.
   Laplace smoothing / Beta priors are standard and well-justified.

3. **Power-law patterns govern music relistening.** ACT-R base-level learning, validated by
   Lex et al. (2020) on 1.1 billion events, fits music consumption better than exponential decay.

4. **Preference follows an inverted-U over exposures.** Berlyne's curve confirmed by Chmiel &
   Schubert meta-analysis (87.7% of 57 studies compatible) and Deezer Ex2Vec (peak ~10 listens).

5. **Activity context produces large, measurable preference differences.** Gong et al. measured
   t-values up to 49.48 for energy between running and relaxing. Context-aware models improve
   ranking by 10%+ (Spotify CoSeRNN).

6. **Aggregate skip_count is fundamentally ambiguous.** All three models, all cited research, and
   the original prompt agree. No formula can fully disambiguate skips without per-event timestamps.

7. **Reintroduction should target uncertainty, not confirmed dislike.** ISMIR 2020 repeated
   exposure study supports rescuing uncertain items, not entrenched negatives.

### Plausible but unvalidated heuristics

1. **Asymmetric decay rates** (high ratings decay slower). All three propose it, none cite direct
   evidence. Directionally sound but specific half-lives are invented.

2. **Recency-weighted skip attenuation** (recent skips after recent plays = saturation). Gemini
   proposes this; the logic is sound for ADHD patterns but no paper validates the specific formula.

3. **Dynamic hyper-fixation cooldowns.** Gemini's "dopamine detox" is intuitive for ADHD but the
   5% threshold and 21-day duration are arbitrary.

4. **Cross-context skip inference** (skipped in A, played in B → context mismatch). Claude
   proposes this; logically sound but depends on having per-context data that doesn't yet exist.

### Speculative claims presented as findings

1. **All specific parameter values** -- half-lives, weights, cooldown durations, exploration
   weights, saturation points, thresholds. None come from the literature. They are starting guesses
   that require empirical tuning.

2. **The skip:play exchange rate.** GPT says it directly: "sources do not provide a universal
   skip:play exchange rate." Claude and Gemini both propose specific ratios without acknowledging
   this limitation as clearly.

3. **Rating decay targets** (zero vs. mean vs. stable floor). No research directly compares these
   for music ratings. GPT's stable-floor approach has the most indirect support (Koren 2009 found
   no-decay outperforms decay in multi-user systems).

### Key architectural decisions to resolve before implementation

1. **Data model: rolling memories or raw aggregates?**
   GPT's rolling memory counters are the highest-value single change. They transform every
   subsequent formula from "guess about temporal distribution" to "use actual temporal data."
   Cost: modify sync_taste.py + add columns. Benefit: every other formula becomes simpler and
   more honest.

2. **Score architecture: single formula or two-lane?**
   GPT's two-lane approach (normal candidates + rehab lane with quotas) is safest for
   reintroduction. The main scoring formula stays focused on ranking good tracks; rehabilitation
   gets its own controlled path.

3. **Rating decay: what happens to old ratings?**
   GPT's stable-floor approach has the best indirect evidence and the lowest risk. Gemini's
   decay-toward-mean is elegant but makes strong assumptions about preference drift. Claude's
   decay-toward-zero is aggressive and essentially discards old ratings.

4. **Cooldown strategy: fixed or context-dependent?**
   Context-dependent (GPT) is more work but better aligned with research showing that activity
   contexts produce large differences in repeat tolerance.

5. **Context data: how to get it?**
   The existing system has context_tags/anti_tags (manual) and audio features (automatic).
   Per-context interaction data doesn't exist. GPT's playlist-exposure tracking is the minimum
   viable path to getting it. Without this, context handling remains rule-based only.

### Parameters that need empirical testing (not guessable from research)

- Rating vs. behavior weight ratio
- Cooldown duration per context type
- Saturation point (plays before diminishing returns kick in)
- Exploration bonus magnitude
- Rehab quota per context
- Skip confidence threshold (how many interactions before trusting skip signal)
- Asymmetric half-life ratios
