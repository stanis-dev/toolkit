# Deep Research: Temporal Taste Modeling for Personal Music Playlists

---

## Who this is for

- Building a personal music recommendation system that generates playlists for specific contexts (work concentration,
  gym, evening reading, driving, etc.)
- Have ~2000 tracks in local library with user ratings (1-10), play counts, skip counts, and last-played timestamps
- Using Last.fm, MusicBrainz, and local audio feature analysis (energy, valence, instrumentalness, speechiness)
- System runs on local infrastructure (Plex + PostgreSQL), not a streaming service
- ADHD — playlists need to balance stimulation without becoming repetitive or monotonous
- Already have researched and implemented: playlist presets with audio feature thresholds, candidate generation via
  track.getSimilar, coherence-based sequencing

## Context and constraints

- **Data available per track:** user_rating (1-10), play_count, skip_count, last_played_at, last_rated_at, duration,
  audio features (energy, valence, instrumentalness, speechiness), context_tags (e.g. "gym", "driving"), anti_tags,
  disliked flag
- **No real-time feedback:** unlike Spotify, I can't observe mid-session skips. Plex aggregates skip_count at sync time.
- **Small library:** ~2000 tracks, not millions. Solutions need to work at this scale without complex ML infrastructure.
- **Context-dependent taste:** a track rated 3 stars might be "bad for reading" but "perfect for gym." Current ratings
  are context-blind.
- **Personal use only:** no cold-start problem, no multi-user considerations
- **Implementation constraint:** algorithm runs as part of an LLM-based agent (Claude) generating playlists. Logic must
  be expressible as SQL queries + heuristic rules, not trained models.

## What has already been researched

- **Playlist preset constraints:** evidence-based audio feature ranges for each context (work_concentration: energy
  0.35-0.65, speechiness <0.15, instrumentalness >=0.60, etc.)
- **Candidate generation:** using Last.fm track.getSimilar as backbone, supplemented by artist expansion and MusicBrainz
  relationships
- **Sequencing logic:** energy curves, max adjacent deltas (dTempo, dEnergy), bridge tracks for genre transitions
- **Diversity controls:** exploration rate, max tracks per artist, novelty scoring against owned library
- **ADHD considerations:** stimulation dosing, salience guardrails, structure bias as adjustable parameters

**Not yet researched:**

- How to weight and combine play_count, skip_count, rating, and recency signals
- How to handle rating decay over time (a 3-star rating from 2 years ago vs. last week)
- When and how to reintroduce low-rated or frequently-skipped tracks
- How to interpret skip_count without context (skipped because heard recently vs. skipped because disliked)
- How to prevent staleness while maintaining coherence

## Instructions

1. **Do not repeat what is already covered** above. Build on it, extend it, or challenge it -- but do not re-derive it.
2. **Be specific to my situation.** Ground analysis in the constraints described above (small library, local-only,
   LLM-agent implementation).
3. **Keep output pragmatic and actionable.** Specific formulas, concrete heuristics, quantified thresholds where
   possible.
4. **Search the web for current data.** Cite all sources with URLs. If specific figures are unavailable, state they are
   unavailable rather than estimating.
5. **Structure output for consolidation.** Results will be integrated into the existing playlist-design.md and SKILL.md
   files.

## Research focus

How should I incorporate temporal signals (play history, skip behavior, rating age) into my playlist generation
algorithm to balance freshness, prevent staleness, account for evolving taste, and enable soft reintroduction of
previously rejected tracks?

### 1. Signal weighting: combining rating, play count, skip count, and recency

What are evidence-based approaches to combine these signals into a single "affinity score" for a track? Specifically:

- How should skip_count be weighted relative to play_count? (Research suggests skips are strong negative signals but
  context-dependent)
- How should recent plays be weighted vs. old plays? (Spotify uses 3 timescales: 6 months, 1 month, 1 week)
- What role should rating recency play? (A 5-star rating from 3 years ago vs. one from last month)

### 2. Rating decay functions

What decay functions are used in music recommendation systems to down-weight old ratings? Research:

- Exponential decay vs. linear decay vs. step functions
- Half-life parameters that make sense for music (unlike movies, music gets replayed)
- Whether decay should apply differently to high ratings vs. low ratings (a 9/10 from 2 years ago might still be valid;
  a 3/10 might have changed)

### 3. Skip signal interpretation

Skip_count is an aggregate number without context. How can I disambiguate:

- Skipped because disliked (strong negative signal)
- Skipped because recently heard (not negative, just saturation)
- Skipped because wrong context (not inherently bad, just misplaced)

What heuristics or secondary signals help distinguish these? For example:

- Skip ratio (skip_count / (play_count + skip_count))
- Time since last full play vs. time since last skip
- Whether the track has ever been played to completion

### 4. Staleness prevention

How do recommendation systems prevent the same highly-rated tracks from dominating every playlist? Research:

- Cooldown periods after a track is played
- Diminishing returns formulas (each consecutive play reduces next-play probability)
- "Exploration bonus" for tracks not played recently
- How Spotify/Deezer balance familiar vs. fresh in algorithmic playlists

### 5. Soft reintroduction of rejected tracks

For tracks that were low-rated or frequently skipped, when and how should they be re-surfaced? Research:

- Memory decay models (ACT-R) for predicting when a track might feel "fresh" again
- Reintroduction triggers (time elapsed, taste drift indicators, context change)
- Confidence thresholds (how certain must we be before reintroduction?)
- User control vs. automatic reintroduction

### 6. Context-specific signal interpretation

Should play/skip/rating signals be segmented by context? For example:

- A track played 50 times during "gym" sessions but skipped every time during "reading"
- If context_tags exist, should affinity scores be computed per-context rather than globally?
- What's the right granularity (per-preset, per-mood, or just global)?

### 7. Practical formulas for implementation

Given my constraints (SQL + heuristic rules), what are concrete formulas I can implement? Looking for:

- An affinity score formula combining the signals
- A freshness modifier based on last_played_at
- A reintroduction probability formula for low-rated tracks
- A skip penalty formula that accounts for ambiguity

## What I do NOT want

- Generic advice about "using machine learning" without specific formulas or heuristics
- Approaches that require real-time feedback loops (I sync data periodically, not per-session)
- Recommendations designed for streaming services with millions of users (I have one user, small library)
- Oversimplified "just use weighted average" without addressing the decay/reintroduction questions
- Assumptions about having labeled skip reasons (I only have aggregate skip_count)

## Output format

**Framework / model:**

1. **Core model** — a unified "temporal affinity" model showing how signals combine
2. **Components** — each signal type (rating, plays, skips, recency) with its role and evidence
3. **Formulas** — specific, implementable formulas for:
    - Base affinity score
    - Temporal decay modifier
    - Skip penalty
    - Staleness/freshness modifier
    - Reintroduction probability
4. **Parameter recommendations** — suggested values for half-lives, thresholds, weights (with reasoning)
5. **Context-specific considerations** — whether/how to segment by playlist context
6. **Edge cases** — how to handle new tracks, tracks with no plays, tracks with only skips
7. **Limitations** — what this approach can't handle, where human judgment is still needed
