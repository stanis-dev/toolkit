Below I’m treating temporal modeling as a reranking layer on top of your existing preset/audio/candidate/sequencing stack, not as a replacement for it.

The key design choice is to **split temporal taste into two memories** instead of forcing everything into one counter:
**enduring preference memory** (“I like this track / artist / sound”) and **short-term state memory** (“I liked it, but not again right now”). That split matches public Spotify research on slow- vs fast-moving interests and multi-timescale user representations, as well as repeat-consumption work showing that recency is a dominant predictor of relistening while overexposure creates boredom/satiation. Context also matters: same-context sessions cluster together, and better user-session context match is associated with lower skip rates. ([Spotify Research][1])

## 1. Core model

Use your current context fit as the outer gate, then apply a temporal reranker:

```text
final_score_ctx = existing_context_score_ctx * temporal_affinity_ctx
```

For normal candidates:

```text
temporal_affinity_ctx = Clamp01(base_affinity_ctx * freshness_modifier_ctx)
```

For soft-negative tracks, do **not** let them compete directly with normal candidates. Put them through a separate **rehab lane** with a small quota:

```text
rehab_gate_ctx = p_reintro_ctx
```

That architecture is better than one monolithic score because the literature points to three distinct mechanisms you need to represent separately: enduring taste, recent intent/fatigue, and context-sensitive skip ambiguity. Public sources also do not provide production constants like “1 skip = 2.7 plays,” so a confidence-weighted, two-lane design is safer than a single fixed conversion. ([Spotify Research][1])

## 2. Components

### Rating

Treat explicit rating as the strongest **global prior**, but let rating age modulate confidence rather than erase meaning. Time-aware recommender literature commonly uses exponential half-life decay or windows for timestamped ratings, and one half-life-decay paper explicitly warns against simply converting an old 4-star rating into the semantic equivalent of a 2-star rating. Their better-performing variant keeps a stable component plus a time-weighted component. ([MDPI][2])

For your use case, I would decay **low ratings faster than high ratings**. That asymmetry is an inference, not a published music-industry constant, but it fits your constraint set: in personal music use, strong likes often remain valid for a long time, while dislikes are more likely to have been context-specific, mood-specific, or saturation-specific.

### Plays

Use plays as positive evidence of affinity, but not as a raw count. Music replay research and ACT-R/BLL-style models consistently show that **frequency + recency** matter together, often with a **power-law** pattern for relistening / temporal drift, while Spotify publicly describes three practical timescales: about **1 week, 1 month, 6 months**. ([arXiv][3])

So: long-term play history should help a track, but very recent play history should also feed a separate fatigue term so favorites do not dominate every playlist.

### Skips

Treat skip_count as **negative evidence with ambiguity**, not as a direct dislike meter. Public work shows skipped tracks add useful signal, but skip behavior varies by session type, time of day, and playlist type, and uncertainty-aware weighting beats naive weighting. In other words: skips matter, but aggregate skips are not self-explanatory. ([Rishabh Mehrotra][4])

For your system, the right question is not “how many skips?” but “how confident are we that these skips mean dislike rather than saturation or wrong context?”

### Recency / staleness

Recent play should contribute in **two opposite directions**:

* positive: evidence the track belongs in your taste space
* negative: evidence the track may feel stale right now

That is not contradictory; it is the actual repeat-consumption pattern. Recency strongly predicts reconsumption, but repeated exposure also follows a boredom / satiation curve, and overexposure can reduce appeal. Discovery/freshness work in music recommendation similarly argues that over-optimizing for familiarity creates staleness. ([cs.toronto.edu][5])

### Context

Yes, compute temporal affinity **per context**, but only at **coarse granularity**. Same-context sessions are more similar than random, and better context match lowers skip rate. With one user and ~2,000 tracks, I would use a small set of durable contexts such as work-focus, gym, driving, reading/evening, wind-down, rather than every micro-preset. ([Rishabh Mehrotra][4])

## 3. Formulas

### 3.1 Temporal decay primitive

For SQL-friendly implementation, use an exponential half-life primitive:

```text
D(age_days, half_life_days) = power(0.5, age_days / half_life_days)
```

That is the standard decay family in time-aware recommendation work, and it maps cleanly to PostgreSQL. For **explicit ratings**, I recommend this exponential form. For **play-event histories**, power-law/BLL is more faithful to music relistening research; if you later add event logs, use that for the play component. ([MDPI][2])

### 3.2 Minimal rolling memories from sync-time aggregates

Because you only sync periodically, the best upgrade is a small persistent state table with decayed counters. That lets you approximate Spotify-style 1w/1m/6m histories **without** real-time instrumentation:

```text
delta_play = greatest(play_count - prev_play_count, 0)
delta_skip = greatest(skip_count - prev_skip_count, 0)
delta_days = days_since_prev_sync

play_mem_7   = play_mem_7   * D(delta_days, 7)   + delta_play
play_mem_30  = play_mem_30  * D(delta_days, 30)  + delta_play
play_mem_180 = play_mem_180 * D(delta_days, 180) + delta_play

skip_mem_30  = skip_mem_30  * D(delta_days, 30)  + delta_skip
skip_mem_180 = skip_mem_180 * D(delta_days, 180) + delta_skip
```

That is the single highest-value schema addition for your setup. It reproduces the practical benefit of multi-timescale interaction histories using only sync deltas. Spotify’s public representation work explicitly uses ~1 week, 1 month, and 6 months as distinct windows for fresh intent, mid-term shifts, and core taste. ([Spotify Research][6])

If you later keep a real play-event log, replace the positive play signal with a BLL/ACT-R form:

```text
play_bll = sum_j (age_play_event_j_days + 1)^(-d)
```

with `d ≈ 0.86` as a strong starting value for music relistening. That comes from ACT-R-based relistening evaluation and aligns with the power-law patterns reported for music preference drift. ([arXiv][3])

### 3.3 Normalization helper

Use percentile-based log normalization so a few heavy-repeat tracks do not swamp the library:

```text
N(x, q95) = least(1.0, ln(1.0 + x) / ln(1.0 + q95))
```

Compute `q95` over the current eligible pool or over the library-wide temporal-state distribution.

### 3.4 Base affinity score

#### Rating signal

```text
r = CASE
      WHEN user_rating IS NULL THEN 0.0
      ELSE (user_rating - 5.5) / 4.5
    END
```

```text
H_r = CASE
        WHEN user_rating >= 8 THEN 540   -- slow decay for strong likes
        WHEN user_rating <= 4 THEN 180   -- faster decay for dislikes
        ELSE 270
      END
```

```text
R = r * (0.65 + 0.35 * D(age_rating_days, H_r))
```

Use `last_rated_at`; if it is null, treat `age_rating_days` as a medium age such as 270 days.

#### Play signal

```text
P_raw = 0.40 * play_mem_180
      + 0.35 * play_mem_30
      + 0.25 * play_mem_7
```

```text
P = N(P_raw, p95(P_raw))
```

#### Skip penalty

```text
skip_ratio_d = skip_mem_180 / greatest(skip_mem_180 + play_mem_180, 1.0)

evidence = 1 - exp(-(skip_mem_180 + play_mem_180) / 4.0)
```

```text
neg_conf = Clamp01(
    0.15
  + 0.55 * skip_ratio_d
  + 0.20 * CASE WHEN play_count = 0 THEN 1 ELSE 0 END
  + 0.10 * CASE WHEN user_rating <= 4 THEN 1 ELSE 0 END
  - 0.15 * CASE WHEN play_count >= 3 THEN 1 ELSE 0 END
  - 0.10 * CASE WHEN user_rating >= 7 THEN 1 ELSE 0 END
  - 0.10 * CASE WHEN age_play_days <= 7 THEN 1 ELSE 0 END
)
```

```text
S_raw = (0.60 * skip_mem_30 + 0.40 * skip_mem_180) * evidence * neg_conf
S = N(S_raw, p95(S_raw))
```

This formula makes skips hurt more when they are recent, high-ratio, and uncorroborated by successful plays, and hurt less when the track has strong positive evidence or was just played recently (a saturation case). That is the closest SQL-friendly answer to your “skip relative to play_count” problem. The sources I reviewed do **not** provide a universal skip:play exchange rate; they instead support contextual and uncertainty-aware treatment. ([Rishabh Mehrotra][4])

#### Base affinity

```text
base_affinity = Clamp01(
    0.50
  + 0.40 * R
  + 0.20 * P
  - 0.30 * S
)
```

Interpretation:

* rating is strongest because it is explicit
* play memory is supporting positive evidence
* skip penalty is strong but confidence-gated

### 3.5 Staleness / freshness modifier

Use both a **hard cooldown** and a **soft freshness curve**.

#### Hard cooldown

For high-repetition-sensitive contexts like work concentration / reading:

```text
cooldown_mod = CASE
  WHEN last_played_at IS NULL THEN 1.00
  WHEN age_play_days < 1  THEN 0.05
  WHEN age_play_days < 3  THEN 0.25
  WHEN age_play_days < 7  THEN 0.60
  WHEN age_play_days < 14 THEN 0.85
  ELSE 1.00
END
```

#### Soft fatigue

```text
fatigue = 1 - exp(-(0.70 * play_mem_7 + 0.30 * play_mem_30) / 3.0)
```

#### Freshness bonus

```text
freshness = CASE
  WHEN last_played_at IS NULL THEN 0.10
  ELSE (1 - exp(-age_play_days / 30.0)) * exp(-age_play_days / 365.0)
END
```

That freshness curve is deliberate: it is near zero when a track was just heard, rises after a gap, then slowly falls again for tracks that have gone completely cold. That shape is a practical approximation of the “recently stale / pleasantly fresh again / eventually irrelevant” pattern that piecewise-decay and repeat-consumption work suggest. ([arXiv][7])

#### Combined freshness modifier

```text
freshness_modifier = greatest(
  0.05,
  least(
    1.15,
    cooldown_mod * (1 - 0.50 * fatigue + 0.25 * freshness)
  )
)
```

#### Main temporal affinity

```text
temporal_affinity = Clamp01(base_affinity * freshness_modifier)
```

### 3.6 Reintroduction probability

Use reintroduction only for **soft negatives**, never as a universal “maybe everything should come back” rule.

#### Hard reject rule

```text
hard_reject =
     disliked
  OR user_rating <= 2
  OR (play_count = 0 AND skip_count >= 3)
  OR (user_rating <= 4 AND skip_ratio_d >= 0.80 AND (play_count + skip_count) >= 5)
```

These should stay out unless manually overridden.

#### Negative strength

```text
neg_strength = Clamp01(
    0.60 * greatest((5.0 - coalesce(user_rating, 5.5)) / 4.0, 0.0)
  + 0.40 * skip_ratio_d
)
```

#### Recovery half-life

```text
H_reintro = CASE
  WHEN neg_strength < 0.35 THEN  60
  WHEN neg_strength < 0.65 THEN 180
  ELSE 365
END
```

#### Time recovery + uncertainty

```text
time_recovery = 1 - D(age_play_days, H_reintro)

uncertainty = exp(-(play_mem_180 + skip_mem_180) / 4.0)
```

#### Taste-drift term

If you can compute a recent context centroid from your existing audio features, use:

```text
sim(track, centroid) =
  1 - (
        sqrt(
          power(energy - c_energy, 2) +
          power(valence - c_valence, 2) +
          power(instrumentalness - c_instr, 2) +
          power(speechiness - c_speech, 2)
        ) / 2.0
      )
```

```text
drift = Clamp01(0.50 + (sim_recent_ctx - sim_longterm_ctx) / 0.20)
```

If you do not want centroid math yet, use a simpler proxy:

* `drift = 1.0` if current context is in `context_tags`
* `drift = 0.5` if context unknown
* `drift = 0.0` if current context is in `anti_tags`

#### Reintroduction probability

```text
p_reintro = CASE
  WHEN hard_reject THEN 0.0
  ELSE cap_ctx
       * time_recovery
       * (0.50 + 0.50 * uncertainty)
       * (0.50 + 0.50 * drift)
       * context_fit
END
```

Use `cap_ctx` as:

* `0.05` for work / reading
* `0.10` for driving
* `0.15` for gym

Then enforce a **rehab quota**:

* at most **1 rehab track per 20 tracks** for work / reading
* at most **2 rehab tracks per 25 tracks** for gym / driving

That is where the repeated-exposure literature matters: repeated recommendations can rescue **novel / uncertain / mildly positive** items, and neutral initial responses can become favorable, but that does **not** justify repeatedly forcing known strong dislikes. Use rehab for soft negatives and uncertain items, not hard rejects. ([archives.ismir.net][8])

## 4. Parameter recommendations

The public sources give you **functional shapes and windows** more than exact deployed constants. I did not find public Spotify/Deezer numbers for skip weights, cooldown windows, or explicit music-rating half-lives, so the numbers below are starting defaults I would use for your setup, not literature constants. The strongest evidence is for multi-timescale histories, exponential half-life for timestamped ratings, and power-law replay dynamics. ([Spotify Research][6])

* **Time windows:** 7d / 30d / 180d rolling memories. This matches Spotify’s published multi-timescale pattern and is a good fit for a personal library where “fresh intent,” “current phase,” and “core taste” are all relevant. ([Spotify Research][6])
* **Rating half-lives:** `540d` for ratings ≥8, `270d` for 5–7, `180d` for ≤4. This follows the broader half-life literature and the “stable + temporal component” idea, while reflecting the fact that music likes usually persist longer than dislikes. ([CEUR Workshop Proceedings][9])
* **Skip-confidence saturation:** use `k = 4` in `evidence = 1 - exp(-interactions / 4)`. Below ~3–4 effective interactions, keep skip interpretations provisional; uncertainty-aware weighting is better than naive weighting. ([arXiv][10])
* **Hard negative thresholds:** hard-bury only with corroboration: disliked flag, or rating ≤2, or at least 3 skips with no successful play, or rating ≤4 plus skip ratio ≥0.8 with at least 5 total interactions. That avoids turning wrong-context or saturation skips into permanent rejection. ([University of Strathclyde][11])
* **Cooldowns:** for work/reading use the 1/3/7/14-day schedule above; for gym/driving compress it to roughly `1/2/5/10` days because repeat tolerance is higher. This is a design recommendation motivated by the general repeat-consumption / satiation findings, not a published platform constant. ([cs.toronto.edu][5])
* **Freshness peak:** the recommended freshness curve peaks around roughly 2–3 months, which is a good default for avoiding staleness without resurrecting long-dead tracks too aggressively. That shape is adapted from repeat-consumption and piecewise-decay patterns. ([arXiv][7])
* **Reintroduction half-lives:** `60d` mild negative, `180d` medium negative, `365d` strong negative. Stronger than that should be manual-only. The repeated-exposure literature supports second chances mainly for uncertain items, not entrenched dislikes. ([archives.ismir.net][8])
* **Context shrinkage prior:** `m = 6` interactions in `λ_ctx = n_ctx / (n_ctx + m)` is a good start for one-user data. That makes context matter quickly without letting one or two events override global taste.

## 5. Context-specific considerations

Yes: compute temporal affinity **per context** once you can, and shrink it toward global when context evidence is sparse:

```text
score_effective_ctx = λ_ctx * score_ctx + (1 - λ_ctx) * score_global
λ_ctx = n_ctx / (n_ctx + 6)
```

Where `n_ctx` is context-local evidence, e.g. decayed plays + decayed skips + explicit context rating weight.

Use **coarse contexts**, not every preset variant. With one user and ~2,000 tracks, per-preset temporal models will get noisy fast. Same-context sessions are measurably more similar than random, and higher user-session/context match is associated with lower skip; that supports context-local modeling, but not ultra-fine segmentation on sparse data. ([Rishabh Mehrotra][4])

For the data you already have:

* `context_tags` and `anti_tags` should act as **priors**, not as substitutes for context-local feedback.
* A global explicit rating should be interpreted as “overall prior,” not “never in every context.”
* A skip in one context should not globally poison the track unless other evidence agrees.

A practical way to get context-local signals without real-time feedback is to persist **playlist exposures**: `(playlist_id, context, track_id, generated_at)`. On the next sync, attribute play/skip deltas to the most recent single context that served the track in that interval; if multiple contexts served it, either split credit or mark it ambiguous and do not update the context-local counters. That is weak labeling, but it is enough to make context-local play/skip memories useful.

Also add explicit user controls:

* `never_in_context`
* `snooze_until`
* `rehab_allowed`

That is worth doing because modern music products are moving toward more direct control beyond passive likes/dislikes/skips, and user studies on context control report higher perceived quality without extra cognitive load. ([Deezer Newsroom][12])

## 6. Edge cases

* **New track, no rating, no plays, no skips:** set `R=0`, `P=0`, `S=0`, `temporal_affinity≈0.50`. Let your existing exploration policy decide whether it enters the playlist.
* **Old 9/10 rating, not heard in years:** the stable rating component preserves it; the temporal component decays it. It remains eligible, but not dominant.
* **Track with many plays and many skips:** interpret via decayed `skip_ratio_d`, not raw totals. High recent play memory plus recent skips often means saturation, not rejection.
* **Only skips, no plays:** treat as provisional negative quickly; hard-bury only after corroboration.
* **Disliked flag:** bypass temporal scoring and exclude from automatic reintroduction.
* **Recently rerated downward:** let the rating term dominate for at least one rating half-life; do not allow historical play count to completely override a recent explicit rerating.

## 7. Limitations

* **Aggregate skip_count is fundamentally ambiguous.** Without skip timestamps or context-labeled skips, you cannot truly separate dislike, saturation, and wrong-context cases; the best you can do is confidence-weight them. ([University of Strathclyde][11])
* **Explicit music-rating decay is under-specified in the public literature.** Time-aware recommender work gives you decay families and half-life ideas, but I did not find a music-specific consensus half-life for explicit track ratings. ([MDPI][2])
* **Your current per-track aggregates are enough for a good first version, but not for the best version.** The decayed-memory table is the smallest change that materially improves temporal modeling.
* **Human overrides still matter.** Because music taste is highly contextual, direct controls like snooze / never-in-context / rehab-allowed are not just UX niceties; they correct what passive signals cannot reliably express. ([Deezer Newsroom][12])

Inline citations are clickable and point to the source URLs.

[1]: https://research.atspotify.com/2022/02/modeling-users-according-to-their-slow-and-fast-moving-interests "https://research.atspotify.com/2022/02/modeling-users-according-to-their-slow-and-fast-moving-interests"
[2]: https://www.mdpi.com/2076-3417/10/15/5324 "https://www.mdpi.com/2076-3417/10/15/5324"
[3]: https://arxiv.org/pdf/2108.02138v2 "https://arxiv.org/pdf/2108.02138v2"
[4]: https://rishabhmehrotra.com/papers/recsys2020-context.pdf "https://rishabhmehrotra.com/papers/recsys2020-context.pdf"
[5]: https://www.cs.toronto.edu/~ashton/pubs/repeat-consumption-www2014.pdf "https://www.cs.toronto.edu/~ashton/pubs/repeat-consumption-www2014.pdf"
[6]: https://research.atspotify.com/2025/9/generalized-user-representations-for-large-scale-recommendations "https://research.atspotify.com/2025/9/generalized-user-representations-for-large-scale-recommendations"
[7]: https://arxiv.org/pdf/1010.3988 "https://arxiv.org/pdf/1010.3988"
[8]: https://archives.ismir.net/ismir2020/paper/000013.pdf "https://archives.ismir.net/ismir2020/paper/000013.pdf"
[9]: https://ceur-ws.org/Vol-2038/paper1.pdf "https://ceur-ws.org/Vol-2038/paper1.pdf"
[10]: https://arxiv.org/pdf/2505.02492 "https://arxiv.org/pdf/2505.02492"
[11]: https://pure.strath.ac.uk/ws/portalfiles/portal/130450243/Meggetto_etal_CIKM2021_On_skipping_behaviour_types_in_music_streaming_sessions.pdf "https://pure.strath.ac.uk/ws/portalfiles/portal/130450243/Meggetto_etal_CIKM2021_On_skipping_behaviour_types_in_music_streaming_sessions.pdf"
[12]: https://newsroom-deezer.com/2026/02/deezer-launches-flow-tuner-personalized-recommendations/ "https://newsroom-deezer.com/2026/02/deezer-launches-flow-tuner-personalized-recommendations/"
