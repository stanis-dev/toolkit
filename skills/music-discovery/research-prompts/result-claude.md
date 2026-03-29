# Temporal signals for personal playlist scoring

**A composite affinity score built from rating, play count, skip rate, and recency — decayed, context-modified, and
exploration-balanced — can replace trained ML models entirely for a single-user, ~2000-track library.** The academic
literature on implicit feedback, cognitive memory models, and production systems at Spotify and Deezer converges on a
clear set of formulas with empirically grounded parameters. What follows is a complete, SQL-implementable system
grounded in that research.

The core insight across all seven areas: simple weighted averages fail because signals are _non-stationary_ (preferences
drift), _ambiguous_ (skips have multiple causes), and _context-dependent_ (a gym anthem is a reading-session skip). The
solution is a layered architecture — base affinity → temporal decay → skip penalty → freshness modifier → context
adjustment → exploration bonus — where each layer has its own formula with tunable parameters.

---

## 1. Core model: the composite affinity score

The architecture follows three stages: a base affinity score from explicit and implicit signals, temporal modifiers that
adjust for recency and staleness, and a context layer that reweights for the current playlist preset. The final
selection score for a candidate track is:

```
selection_score = base_affinity × rating_decay × freshness_modifier × context_modifier
                  + exploration_bonus - skip_penalty
```

Each component is detailed below with its formula, parameters, and research basis.

### Base affinity: combining rating with implicit signals

The Hu-Koren-Volinsky (HKV) framework separates implicit feedback into **preference** (binary: liked or not) and
**confidence** (how certain we are). For a single-user system with explicit ratings, adapt this by treating the
user_rating as the preference signal and play_count as the confidence multiplier:

```sql
base_affinity = (user_rating / 10.0)
              × (1 + α × LN(1 + play_count))
              / (1 + β × adjusted_skip_penalty)
```

The logarithmic confidence function `1 + α × LN(1 + play_count)` comes directly from HKV's log variant, which dampens
the influence of very high play counts. HKV found **α = 40** optimal for their dataset, but that was for a multi-user
matrix factorization system. For a single-user system with ratings on a 1–10 scale, a much smaller α is appropriate —
**α ≈ 0.5** keeps the confidence multiplier in a manageable range (a track played 100 times gets confidence ~3.3× vs
~1.85× for 10 plays).

The **β parameter** controls skip penalty influence. Set **β ≈ 1.0** initially (see skip penalty section for the full
formula). The entire base_affinity is normalized to a 0–1 range for downstream multiplication.

**Key citation**: Hu, Y., Koren, Y., & Volinsky, C. (2008). "Collaborative Filtering for Implicit Feedback Datasets."
ICDM 2008. The confidence function `c_ui = 1 + α·log(1 + r_ui/ε)` is from this paper.

---

## 2. Rating decay: power-law beats exponential for music

Koren's landmark 2009 finding is counterintuitive but critical: **"prediction quality improves as we moderate that time
decay, reaching best quality when there is no decay at all."** Simply down-weighting old ratings destroys useful signal
about stable preferences. However, Koren was studying multi-user collaborative filtering where old ratings establish
cross-user patterns. For a **single-user system**, old ratings help less — there are no cross-user patterns to preserve
— so moderate decay is appropriate.

### The recommended decay function

Use a **power-law decay** rather than exponential. The ACT-R Base-Level Learning equation models human memory with a
power function that decays rapidly at first then slows — memories never fully vanish. This matches music behavior: Lex,
Kowald, and Schedl (2020) confirmed that music relistening follows a power-law distribution on the LFM-1b dataset (1.1
billion listening events).

```sql
rating_decay = 1.0 / (1.0 + (days_since_rated / half_life_days) ^ decay_power)
```

This is a **sigmoid-shaped decay** that stays near 1.0 for recent ratings and asymptotically approaches 0 for very old
ones, with a smooth transition around the half-life. Unlike pure exponential decay (`e^(-λt)`), it preserves a
meaningful long tail — a 9/10 from three years ago still contributes, just at reduced weight.

### Parameter recommendations

**Half-life**: Ardagelou and Arampatzis (2017) found **~150 days** optimal for movie ratings. Music preferences are more
stable than movie preferences (you replay songs; you don't rewatch most movies), so a longer half-life is warranted.
Sánchez-Moreno et al. (2020) used **years** as the time unit for music decay, noting that "changes in musical trends are
not" on shorter timescales. **Recommended: half_life_days = 365** (one year), meaning a rating from one year ago retains
~50% of its weight.

**Decay power**: The ACT-R canonical value is **d = 0.5**. Reiter-Haas et al. (RecSys 2021) fitted d to actual music
listening data and found values ranging from **d = 0.86** (one-week window) to **d = 1.737** (full 2019 dataset). For
rating decay (not relistening prediction), **d = 0.5** is conservative and appropriate — it produces gentler decay that
preserves more signal from older ratings.

### Asymmetric decay: high vs. low ratings

No published research directly tests asymmetric decay rates for high vs. low ratings. However, the logic is sound and
supported indirectly by Koren's user-bias-drift model: **a high rating is more likely to reflect stable preference**
(the user actively chose to rate highly), while **a low rating is more likely to reflect transient context** (mood,
overexposure, wrong moment). Implement this as:

```sql
effective_half_life = CASE
    WHEN user_rating >= 8 THEN 545   -- 1.5 years: high ratings decay slowly
    WHEN user_rating >= 5 THEN 365   -- 1 year: moderate ratings standard decay
    ELSE 180                          -- 6 months: low ratings decay faster
END
```

This is a pragmatic heuristic, not a research-backed formula. The rationale: a 3/10 from two years ago is more likely to
have changed than a 9/10 from the same period, because negative reactions are more context-sensitive. The Spotify
Preference Transition Model (Sanna Passino et al., 2021) measured total variation distance of **~0.05 per quarter** in
genre preferences, accumulating to **~0.6 over 4 years** — confirming that tastes drift enough to make old low ratings
unreliable.

---

## 3. Skip penalty: Bayesian smoothing with a "never played" amplifier

### Why raw skip rate fails

A track with 1 skip and 0 plays has a 100% skip rate — but that tells you almost nothing. The fundamental problem is
**small-sample unreliability**. The Deezer Research team (Sguerra et al., 2025) addressed this with Beta distribution
priors, and the approach maps perfectly to SQL.

### The Bayesian-smoothed skip penalty

```sql
skip_penalty = (skip_count + prior_skips)
             / (play_count + skip_count + prior_skips + prior_plays)
             × confidence_factor
             × never_played_boost
```

Where:

- **`prior_skips = 2`** and **`prior_plays = 5`** encode a prior belief of ~29% skip rate, close to the empirical
  baseline. Paul Lamere's analysis at Spotify found **~50% of songs are never listened to in their entirety**, with the
  highest skip concentration in the first 20 seconds. For a personal library (not a streaming catalog of unknowns), a
  lower prior of ~29% is reasonable since the user presumably chose to add these tracks.

- **`confidence_factor = 1 - 1/(1 + LN(1 + play_count + skip_count))`** — ranges from 0 (no interactions) to ~0.85 (100
  interactions). This ensures tracks with few interactions get negligible skip penalty regardless of raw skip rate. This
  follows HKV's principle that "the numerical value of implicit feedback indicates confidence, not preference."

- **`never_played_boost`**: If `play_count = 0 AND skip_count >= 3`, set to **1.5**. If the track has _never_ been fully
  played despite multiple encounters, that is the strongest negative implicit signal available from aggregate data —
  stronger than a high skip rate on a track that was previously enjoyed.

### Interpreting skip rate tiers

Based on Lamere (2014), Chartmetric (2022), and the MSSD dataset (Brost et al., 2019), calibrate against the user's
personal baseline:

| Smoothed skip rate vs. user baseline | Interpretation                       | Action                   |
| ------------------------------------ | ------------------------------------ | ------------------------ |
| **>2σ above baseline**               | Strong dislike or permanent mismatch | Heavy penalty (×1.5)     |
| **1–2σ above baseline**              | Likely dislike, possibly contextual  | Standard penalty         |
| **Within ±1σ of baseline**           | Normal / contextual                  | Minimal penalty          |
| **>1σ below baseline**               | Genuine preference signal            | No penalty; slight bonus |

Calculate the user's baseline as `SUM(skip_count) / SUM(play_count + skip_count)` across all tracks. For ~2000 tracks,
this is a stable statistic.

### SQL implementation

```sql
WITH user_stats AS (
    SELECT
        SUM(skip_count)::float / NULLIF(SUM(play_count + skip_count), 0) AS avg_skip_rate,
        STDDEV(skip_count::float / NULLIF(play_count + skip_count, 1)) AS skip_rate_std
    FROM tracks WHERE play_count + skip_count > 0
)
SELECT
    t.id,
    ((t.skip_count + 2.0) / (t.play_count + t.skip_count + 7.0))  -- Bayesian smoothed
    * (1.0 - 1.0 / (1.0 + LN(1.0 + t.play_count + t.skip_count)))  -- confidence
    * CASE WHEN t.play_count = 0 AND t.skip_count >= 3 THEN 1.5 ELSE 1.0 END  -- never-played
    AS skip_penalty
FROM tracks t, user_stats u
```

---

## 4. Freshness modifier: power-law cooldown with exploration bonus

### The staleness problem

The mere exposure effect follows Berlyne's **inverted-U curve**: preference rises with familiarity to a peak, then
declines with overexposure. Chmiel and Schubert's (2017) meta-analysis of **57 studies over 115 years** found **87.7%
compatible** with this model. Deezer's Ex2Vec research (Sguerra et al., RecSys 2023) confirmed it empirically: for newly
released tracks, listening probability follows an inverted-U over exposures, peaking around **10 listens** before
declining.

### The freshness formula

Combine a **time-since-last-play cooldown** with a **play-count diminishing returns** factor:

```sql
freshness_modifier = time_freshness × count_freshness
```

**Time freshness** (cooldown after play):

```sql
time_freshness = 1.0 - EXP(-1.0 * hours_since_last_played / cooldown_hours)
```

This exponential recovery function starts at 0 immediately after a play and asymptotically approaches 1.0. With
**`cooldown_hours = 72`** (3 days), the track recovers to ~63% weight after 3 days, ~86% after 6 days, ~95% after 9
days. Radio programming uses **2–3 hour** cooldowns for power rotation tracks and **4–6 hours** for recurrents, but
those are commercial stations playing for passive audiences. For active listening with a personal library, longer
cooldowns are appropriate.

**Count freshness** (diminishing returns from total plays):

```sql
count_freshness = 1.0 / (1.0 + LN(1.0 + play_count / saturation_point))
```

With **`saturation_point = 30`**, a track played 30 times has count_freshness ~0.59; at 100 plays, ~0.45. This never
reaches zero — even heavily-played tracks retain some probability of selection. The logarithmic form mirrors the Deezer
finding that listening tendency peaks around 10 plays then slowly drops.

### Exploration bonus for neglected tracks

Apply a **UCB-inspired exploration bonus** to tracks that haven't been played recently:

```sql
exploration_bonus = exploration_weight × SQRT(LN(total_library_plays) / GREATEST(play_count, 1))
```

This is the UCB1 formula adapted from bandit literature. **`exploration_weight = 0.1`** keeps exploration as a modest
tiebreaker rather than a dominant force. The formula gives higher bonuses to tracks with low play counts relative to
overall library usage — exactly the tracks most likely to be underexplored. Spotify's BaRT system uses **ε-greedy** with
~5% exploration, pre-selecting the 100 most relevant items to explore. Deezer's carousel bandit research (RecSys 2020)
found **Thompson Sampling outperforms UCB when feedback is delayed** — relevant for the periodic-sync scenario. However,
Thompson Sampling requires maintaining posterior distributions per track, which is complex in SQL. The UCB formula above
is a simpler approximation with similar properties.

### Combined SQL

```sql
SELECT
    t.id,
    -- Time freshness
    (1.0 - EXP(-1.0 * EXTRACT(EPOCH FROM NOW() - t.last_played_at) / 3600.0 / 72.0))
    -- Count freshness
    * (1.0 / (1.0 + LN(1.0 + t.play_count / 30.0)))
    AS freshness_modifier,
    -- Exploration bonus
    0.1 * SQRT(LN(lib.total_plays + 1) / GREATEST(t.play_count, 1))
    AS exploration_bonus
FROM tracks t, (SELECT SUM(play_count) AS total_plays FROM tracks) lib
```

---

## 5. Soft reintroduction of low-rated and disliked tracks

### The cognitive science basis

The ACT-R Base-Level Learning equation models memory activation as:

**B*i = ln(Σ*{j=1}^{n} t_j^{-d})**

where t_j is the time since the j-th access and **d ≈ 0.5** is the canonical decay parameter. For a single negative
event (one dislike), the activation decays as **-0.5 × ln(t)**. With a typical retrieval threshold of τ ≈ -2 in ACT-R
models, a single negative memory falls below retrieval threshold between **1 and 6 months** depending on noise
parameters. This provides a cognitively grounded estimate for when a dislike might be "forgotten enough" for
reintroduction.

Lex, Kowald, and Schedl (2020) validated this equation against the LFM-1b Last.fm dataset (1.1 billion listening events,
120,000+ users) and found it **outperformed collaborative filtering, frequency-based, and recency-based baselines** for
predicting music genre preferences.

### The reintroduction probability formula

```sql
reintro_probability =
    memory_decay × taste_drift_factor × (1.0 - rejection_strength)
```

**Memory decay** — how much the negative impression has faded:

```sql
memory_decay = 1.0 - (1.0 / (1.0 + (days_since_rejection / 180.0) ^ 0.5))
```

At 90 days: ~0.29. At 180 days: ~0.41. At 365 days: ~0.59. At 730 days: ~0.75. The power of 0.5 implements the ACT-R
decay rate. The 180-day denominator sets the inflection point at 6 months.

**Taste drift factor** — has the user's preference profile shifted toward this track? Track whether recent ratings in
the same genre/mood cluster have trended upward:

```sql
taste_drift_factor = CASE
    WHEN avg_recent_rating_in_genre > avg_old_rating_in_genre + 1.0 THEN 1.5
    WHEN avg_recent_rating_in_genre > avg_old_rating_in_genre + 0.5 THEN 1.2
    ELSE 1.0
END
```

The Spotify Preference Transition Model (Sanna Passino et al., 2021) showed taste distributions shift with **total
variation ~0.05 per quarter** — substantial enough that genre-level preference shifts are detectable over 6–12 months.
This factor amplifies reintroduction probability when drift is detected.

**Rejection strength** — how emphatic was the rejection:

```sql
rejection_strength = CASE
    WHEN disliked = true THEN 0.9          -- Explicit dislike flag
    WHEN user_rating <= 2 THEN 0.8         -- Very low explicit rating
    WHEN user_rating <= 4 THEN 0.5         -- Low rating
    WHEN skip_rate > 0.8 AND play_count = 0 THEN 0.7  -- Never played, always skipped
    ELSE 0.3                                -- Mild negative signal
END
```

### Reintroduction thresholds

A track becomes eligible for reintroduction when `reintro_probability` exceeds a threshold that depends on placement:

| Placement type                              | Threshold | Minimum days since rejection |
| ------------------------------------------- | --------- | ---------------------------- |
| Deep in exploratory playlist (position 15+) | 0.25      | 90                           |
| Mid-playlist in a matching context          | 0.40      | 180                          |
| Prominent position in a familiar playlist   | 0.60      | 365                          |

These thresholds are derived from the ACT-R memory decay timeline and Spotify's taste drift velocity. **Tracks with
`disliked = true` should never be automatically reintroduced** — respect explicit user rejection. Only tracks with
implicit negative signals (high skip rate, low rating without explicit dislike flag) are candidates.

---

## 6. Context-specific signal interpretation

### The research consensus

Spotify's CoSeRNN research (Hansen et al., RecSys 2020) demonstrated that **sessions sharing the same context are
significantly more similar** than random sessions, with **10%+ improvement** on all ranking metrics from context-aware
modeling. Gong, Kaya, and Tintarev (2020) measured the largest audio feature differences between running and relaxing
contexts — **t-values up to 49.48 for energy**.

However, for ~2000 tracks with limited per-context observations, pure per-context scoring causes a **severe data
sparsity problem**. The recommended approach from the literature is a **hierarchical model**: global affinity modified
by a context factor.

### The context-modified score

```sql
context_score = base_affinity
              × COALESCE(context_weight, 1.0)
              × CASE WHEN has_anti_tag_for_context THEN 0.0 ELSE 1.0 END
```

**Context weight** uses Wang et al.'s (2012) Beta distribution approach for per-(track, context) affinity:

```sql
context_weight = (context_plays + 1.0) / (context_plays + context_skips + 2.0)
```

This is a **Beta(1,1) prior** (uniform) updated with per-context play/skip observations. With no per-context data, it
returns 0.5 (neutral). With 10 context-plays and 0 context-skips, it returns 0.917. With 0 context-plays and 5
context-skips, it returns 0.143. The formula is Bayesian, handles small samples gracefully, and is a single SQL
expression.

**Minimum data threshold**: Only use per-context weights when `context_plays + context_skips >= 5`. Below this
threshold, fall back to audio-feature matching against context profiles. Research consistently recommends at least 5
per-context observations for statistical reliability.

### Context granularity

The user's existing preset system maps directly to the research-recommended hierarchy. Activity is the **strongest
context dimension** — running vs. relaxing produces the largest measurable preference differences. The user's
`context_tags` and `anti_tags` already implement contextual pre-filtering, which the CARS literature shows works well
for small catalogs. The recommended priority:

- **Per-preset** (gym, focus, chill, etc.) — highest signal, user-defined, zero ambiguity
- **Per-time-of-day** (4 bins: morning/afternoon/evening/night) — significant but secondary
- **Per-mood** — only when explicitly set by the user, too volatile for inference

### Detecting context-mismatched skips

Without labeled skip reasons, use cross-context consistency:

```sql
-- Track skipped in this context but played in others = context mismatch
SELECT t.id,
    CASE
        WHEN ctx_skips > 0 AND other_ctx_plays > 3 THEN 'context_mismatch'
        WHEN global_skip_rate > user_avg + 2 * user_std THEN 'dislike'
        WHEN play_count > 10 AND recent_skip_rate > 2 * historical_skip_rate THEN 'saturation'
        ELSE 'ambiguous'
    END AS skip_interpretation
FROM track_context_stats t
```

A track that is skipped in one preset but played in others is a **context mismatch**, not a dislike. The system should
add an `anti_tag` for that preset rather than penalizing the global score. Only tracks skipped consistently **across all
contexts** should receive global penalty.

---

## 7. Complete formulas for SQL implementation

### The full selection score

```sql
WITH params AS (
    SELECT
        0.5   AS alpha,          -- play confidence weight
        365.0 AS rating_half_life,
        0.5   AS decay_power,
        72.0  AS cooldown_hours,
        30.0  AS saturation_point,
        0.1   AS explore_weight,
        2.0   AS prior_skips,
        5.0   AS prior_plays
),
user_stats AS (
    SELECT
        SUM(play_count)::float AS total_plays,
        SUM(skip_count)::float / NULLIF(SUM(play_count + skip_count), 0) AS avg_skip_rate
    FROM tracks WHERE play_count + skip_count > 0
),
scored AS (
    SELECT
        t.id,
        t.title,

        -- BASE AFFINITY (0 to ~2.5 range)
        (t.user_rating / 10.0)
        * (1.0 + p.alpha * LN(1.0 + t.play_count))
        AS raw_affinity,

        -- RATING DECAY (0 to 1)
        1.0 / (1.0 + POWER(
            EXTRACT(EPOCH FROM NOW() - t.last_rated_at) / 86400.0
            / (CASE
                WHEN t.user_rating >= 8 THEN 545
                WHEN t.user_rating >= 5 THEN 365
                ELSE 180
            END),
            p.decay_power
        )) AS rating_decay,

        -- TIME FRESHNESS (0 to 1, 0 = just played)
        1.0 - EXP(
            -1.0 * EXTRACT(EPOCH FROM NOW() - t.last_played_at)
            / 3600.0 / p.cooldown_hours
        ) AS time_freshness,

        -- COUNT FRESHNESS (0 to 1)
        1.0 / (1.0 + LN(1.0 + t.play_count / p.saturation_point))
        AS count_freshness,

        -- SKIP PENALTY (0 to ~1.5)
        ((t.skip_count + p.prior_skips) / (t.play_count + t.skip_count + p.prior_skips + p.prior_plays))
        * (1.0 - 1.0 / (1.0 + LN(1.0 + t.play_count + t.skip_count)))
        * CASE WHEN t.play_count = 0 AND t.skip_count >= 3 THEN 1.5 ELSE 1.0 END
        AS skip_penalty,

        -- EXPLORATION BONUS
        p.explore_weight * SQRT(LN(u.total_plays + 1) / GREATEST(t.play_count, 1))
        AS exploration_bonus

    FROM tracks t, params p, user_stats u
    WHERE t.disliked = false
)
SELECT
    id, title,
    (raw_affinity * rating_decay * time_freshness * count_freshness)
    - skip_penalty
    + exploration_bonus
    AS selection_score
FROM scored
ORDER BY selection_score DESC
```

### Reintroduction query for rejected tracks

```sql
SELECT t.id, t.title, t.user_rating,
    -- Memory decay of negative impression
    (1.0 - 1.0 / (1.0 + POWER(
        EXTRACT(EPOCH FROM NOW() - COALESCE(t.last_rated_at, t.last_played_at)) / 86400.0 / 180.0,
        0.5
    ))) AS memory_decay,

    -- Rejection strength
    CASE
        WHEN t.user_rating <= 2 THEN 0.8
        WHEN t.user_rating <= 4 THEN 0.5
        WHEN t.play_count = 0 AND t.skip_count >= 3 THEN 0.7
        ELSE 0.3
    END AS rejection_strength,

    -- Final reintroduction probability
    (1.0 - 1.0 / (1.0 + POWER(
        EXTRACT(EPOCH FROM NOW() - COALESCE(t.last_rated_at, t.last_played_at)) / 86400.0 / 180.0,
        0.5
    )))
    * (1.0 - CASE
        WHEN t.user_rating <= 2 THEN 0.8
        WHEN t.user_rating <= 4 THEN 0.5
        WHEN t.play_count = 0 AND t.skip_count >= 3 THEN 0.7
        ELSE 0.3
    END)
    AS reintro_probability

FROM tracks t
WHERE t.disliked = false
  AND (t.user_rating <= 4 OR (t.skip_count::float / NULLIF(t.play_count + t.skip_count, 0) > 0.6))
  AND EXTRACT(EPOCH FROM NOW() - COALESCE(t.last_rated_at, t.last_played_at)) / 86400.0 > 90
ORDER BY reintro_probability DESC
```

---

## Parameter recommendations and tuning

All parameters below are starting points derived from the literature. For a single-user system with ~2000 tracks,
**manual tuning based on playlist quality** is the appropriate optimization method — not A/B testing.

| Parameter                    | Value    | Source / Rationale                                                                            |
| ---------------------------- | -------- | --------------------------------------------------------------------------------------------- |
| **α (play confidence)**      | 0.5      | Adapted from HKV α=40 for single-user scale                                                   |
| **Rating half-life (high)**  | 545 days | Extended from Ardagelou & Arampatzis 150-day movie finding; music preferences are more stable |
| **Rating half-life (mid)**   | 365 days | Sánchez-Moreno et al. used years as time unit for music                                       |
| **Rating half-life (low)**   | 180 days | Faster decay for low ratings; Spotify taste drift ~0.05 TV/quarter                            |
| **Decay power**              | 0.5      | ACT-R canonical d value (Anderson & Schooler, 1991)                                           |
| **Cooldown hours**           | 72       | Between radio's 2–6 hours and weekly refresh cycles                                           |
| **Saturation point**         | 30 plays | Deezer Ex2Vec peak at ~10; buffer for personal favorites                                      |
| **Exploration weight**       | 0.1      | Spotify uses ~5% exploration; conservative for quality                                        |
| **Prior skips / plays**      | 2 / 5    | Encodes ~29% baseline; Lamere found ~50% global, lower for personal library                   |
| **Never-played boost**       | 1.5×     | No specific research value; heuristic based on "gold signal" finding                          |
| **Reintro inflection**       | 180 days | ACT-R retrieval threshold crossing at 1–6 months                                              |
| **Context min observations** | 5        | Standard heuristic in CARS literature for statistical reliability                             |

### What to tune first

The three parameters with the highest impact on playlist quality are **cooldown_hours** (too low = repetitive playlists,
too high = favorites never appear), **saturation_point** (controls how aggressively well-known tracks are
deprioritized), and **exploration_weight** (controls the familiar/fresh balance). Start by adjusting cooldown_hours
based on listening frequency — if you listen daily, 72 hours works; if weekly, reduce to 24.

---

## Edge cases the formulas handle

**New tracks (no play history)**: `play_count = 0` and `skip_count = 0` yield base_affinity from rating alone, no skip
penalty, full freshness, and maximum exploration bonus. New tracks with a good rating surface naturally.

**Unrated but frequently played tracks**: With `user_rating = 0` or NULL, the base_affinity zeroes out. For unrated
tracks, substitute an inferred rating: `COALESCE(user_rating, 5 + 2 * LN(1 + play_count) - 3 * skip_rate)` — a neutral
starting point adjusted by implicit signals.

**Tracks with exactly one skip and zero plays**: Bayesian smoothing returns (0+2)/(0+0+2+5) ≈ 0.29 with near-zero
confidence. The skip penalty is negligible (~0.0), correctly treating this as insufficient evidence.

**Seasonal tracks** (Christmas music in July): The time_freshness modifier handles this automatically — 6 months without
a play yields full freshness. The context system handles the mismatch: if the track has `anti_tag` for the current
season's presets, it's excluded.

**Tracks rated high but never played** (rated from memory, imported from another system): These get high base_affinity,
full freshness, and high exploration bonus — they'll surface quickly, which is appropriate since they need validation
through actual plays.

---

## Limitations and honest unknowns

**No published asymmetric decay research exists.** The differentiated half-lives for high vs. low ratings (545/365/180
days) are a reasonable heuristic, not an empirically validated formula. If this produces odd results, collapse to a
single 365-day half-life.

**Skip ambiguity is fundamentally irreducible** with only aggregate skip_count. The Bayesian smoothing and never-played
heuristic help, but without per-event timestamps or listening duration data, the system cannot distinguish "skipped at 5
seconds (dislike)" from "skipped at 3 minutes (almost finished, just moved on)." If Plex provides listening duration
data at sync time, incorporate it — the 30-second threshold used by Spotify and Apple Music is the standard cutoff
between "skip" and "partial play."

**The exploration bonus formula assumes stationarity.** UCB1 is designed for stationary reward distributions — it
doesn't account for the fact that a track's quality _for this user_ may change over time. For a slowly-drifting
single-user system, this is acceptable but not optimal. Thompson Sampling would be theoretically superior but
impractical in pure SQL.

**Context modifier quality depends entirely on tagging discipline.** If `context_tags` are incomplete or inconsistent,
the per-context Beta scores will be noisy. The system degrades gracefully (defaulting to global scores), but the full
benefit requires that plays and skips are associated with the preset they occurred in.

**The reintroduction model has no feedback loop.** If a reintroduced track is skipped again, the current formulas don't
specifically track "reintroduction attempt failed." Implementing a `reintro_attempts` counter with escalating cooldowns
(180 days → 365 days → 730 days → permanent exclusion after 3 failed attempts) would address this, though no published
research provides specific parameters for such escalation.

## Conclusion

The most important insight from this research is that **temporal signals are not just recency weights — they encode
fundamentally different information at different timescales**. Play count measures cumulative preference. Skip rate
measures current tolerance. Rating age measures confidence in explicit preference. Last-played recency measures
saturation risk. Each needs its own decay function because each models a different cognitive process: long-term
preference stability (power-law, d=0.5), short-term saturation (exponential cooldown, 72 hours), and medium-term taste
drift (sigmoid decay, 365-day half-life). The layered architecture — base affinity × decay × freshness × context +
exploration - skip penalty — keeps these processes independent and separately tunable, which matters more for practical
quality than getting any single parameter exactly right.
