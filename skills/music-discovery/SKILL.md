---
name: music-discovery
description:
    Use when the user wants music recommendations, wants to discover new artists, or asks to download music - combines
    Plex listening history, AI music knowledge, and SoulSync for search and download
---

# Music Discovery & Download

## Overview

Discover music based on Plex listening history, recommend new artists, and trigger downloads via SoulSync. Bridges two
machines: Mac Mini (Plex) and homelab (SoulSync + slskd).

**REQUIRED:** `mini-ssh` skill for Plex API access, `homelab-ssh` skill for SoulSync/slskd access.

SoulSync API key: "sk_C_eRfTvsUFlQzKqLd0sNVaZUpL-YRrAkhOHikb9_UyY"

## Workflow

```
1. Gather (Plex)  →  2. Recommend (Claude)  →  3. Act (SoulSync)
   ssh mini            analysis                  192.168.0.2:8008
```

### Step 1: Gather Listening Context

```bash
# Get Plex token
TOKEN=$(ssh mini 'defaults read com.plexapp.plexmediaserver PlexOnlineToken')

# Recent music plays
ssh mini "curl -s 'http://localhost:32400/status/sessions/history/all?librarySectionID=3&X-Plex-Token=$TOKEN' -H 'Accept: application/json'" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data.get('MediaContainer', {}).get('Metadata', [])[:20]:
    print(f\"{item.get('grandparentTitle','')} - {item.get('parentTitle','')} - {item.get('title','')}\")
"

# Current library artists
ssh mini "curl -s 'http://localhost:32400/library/sections/3/all?X-Plex-Token=$TOKEN' -H 'Accept: application/json'" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data.get('MediaContainer', {}).get('Metadata', []):
    print(item.get('title',''))
"

# User-rated tracks (strongest taste signal)
ssh mini "curl -s 'http://localhost:32400/library/sections/3/all?type=10&sort=userRating:desc&X-Plex-Token=$TOKEN' -H 'Accept: application/json'" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data.get('MediaContainer', {}).get('Metadata', []):
    rating = item.get('userRating')
    if rating:
        print(f\"{item.get('grandparentTitle','')} - {item.get('title','')} | {rating}/10\")
"
```

#### Sync Taste Data

The `taste` table in PostgreSQL is the durable store for ratings, play counts, context tags, and dislikes. It survives
Plex file deletions. Run this sync when the user requests it, or before generating recommendations if `MAX(synced_at)`
is older than 7 days.

```bash
TOKEN=$(ssh mini 'defaults read com.plexapp.plexmediaserver PlexOnlineToken')

# Copy and run the sync script on homelab
scp ~/.cursor/skills/music-discovery/scripts/sync_taste.py homelab:/tmp/
ssh homelab "python3 /tmp/sync_taste.py --plex-token $TOKEN"

# Check last sync time
PSQL='sudo docker exec postgres psql -U postgres -d music -t -A'
ssh homelab "$PSQL -c \"SELECT COUNT(*), MAX(synced_at) FROM taste;\""
```

Add `--dry-run` to preview the SQL without executing. The script fetches all rated tracks and play history from Plex,
enriches with MusicBrainz IDs from SoulSync, and upserts into the `taste` table. On each sync, rolling memory counters
(`play_mem_7/30/180`, `skip_mem_30/180`) are updated using exponential half-life decay applied to the delta since the
previous sync. The `playlist_exposures` table is also created if it doesn't exist.

### Step 2: Recommend

Act as a personal music recommendation engine and playlist curator. Treat every request as a recommendation + sequencing
problem, not just a list-making task. Use Plex data from Step 1 and metadata from the sources below as the primary
signals.

#### Operating Principles

1. **Two-stage pipeline (track-centric):**
    - **A) Candidate generation (broad):** Gather 60-200 plausible **tracks** from multiple neighbourhoods using
      `track.getSimilar` as the backbone, supplemented by artist expansion, MusicBrainz relationships, SoulSync's
      discovery pool, and web research.
    - **B) Filtering + re-ranking (strict):** Narrow to the final set by scoring each **track** on intent fit, taste
      fit, novelty, diversity, and sequence coherence. Use Last.fm tags where available; fall back to neighbour overlap
      when tags are absent. Use SoulSync DB to exclude already-owned tracks.

2. **Beyond-accuracy objectives:**
    - Always explicitly manage diversity, novelty, and serendipity (relevant but unexpected).
    - Include an "exploration rate" knob (0-100%) that controls how adventurous recommendations are.

3. **Explainability:**
    - For each final recommendation, give a short "why it fits" justification tied to the intent + user preferences.

4. **Interaction -- engagement levels:**

    The user controls how much back-and-forth they want. All modes produce a plan the user reviews
    before execution. Use structured questions (clickable options, multiple-choice) wherever possible.

    - **Quick** ("just do it"): Create the plan immediately. Include brief notes on anything notable
      (skip patterns, dropped tracks) but do not ask questions. Default mode.
    - **Review** ("let me see it first"): Create a draft plan and surface a small set of structured
      questions about patterns noticed. The user clicks through options quickly.
    - **Deep dive** ("let's really work on this"): Lead with a structured questionnaire (mood,
      what's working, what's not, tracks to include/exclude). Build the plan from the answers.

    If the user doesn't specify, assume **quick mode**. Never turn a routine refresh into a survey.

#### Taste Profile

**User preferences:** Always read [user-preferences.md](user-preferences.md) first. This file contains the user's
self-described tastes, anti-preferences, and reference points. Never edit it -- only the user updates this file.

Build from user preferences + **seed tracks** -- their rated and most-played individual tracks, not only artists.

**Seed collection:** Query the `taste` table for seed tracks. This is the primary source -- it persists across Plex file
deletions and includes context tags.

```bash
PSQL='sudo docker exec postgres psql -U postgres -d music -t -A'

# Top rated tracks (strongest taste signal)
ssh homelab "$PSQL -c \"SELECT artist, track, album, user_rating, play_count FROM taste WHERE user_rating IS NOT NULL ORDER BY user_rating DESC, play_count DESC LIMIT 20;\""

# Most played tracks (behavioral signal)
ssh homelab "$PSQL -c \"SELECT artist, track, album, play_count, user_rating FROM taste WHERE play_count > 0 ORDER BY play_count DESC LIMIT 20;\""

# Tracks tagged for a specific context (when a preset is active)
ssh homelab "$PSQL -c \"SELECT artist, track, album, user_rating FROM taste WHERE 'gym' = ANY(context_tags) ORDER BY user_rating DESC NULLS LAST;\""

# Excluded tracks
ssh homelab "$PSQL -c \"SELECT artist, track, album FROM taste WHERE disliked = TRUE OR anti_tags != '{}';\""

# Join with audio_features for full picture
ssh homelab "$PSQL -c \"SELECT t.artist, t.track, t.user_rating, af.energy, af.valence, af.instrumentalness, af.speechiness FROM taste t JOIN audio_features af ON t.file_path = af.file_path WHERE t.user_rating >= 8 ORDER BY t.user_rating DESC;\""
```

Take the top 10-20 tracks from the taste table as taste anchors.

**Candidate ranking pool:** Use this query to generate a starting pool of ~100 candidates for a
given context. Fill in the preset's audio thresholds and context tag. The agent reviews and refines
this pool -- it is a starting point, not a final decision.

```bash
PSQL='sudo docker exec postgres psql -U postgres -d music -t -A'

# Candidate pool for a context (fill in preset values for energy/speechiness/instrumentalness)
ssh homelab "$PSQL -c \"
  SELECT t.artist, t.track, t.album,
    COALESCE(t.user_rating, 0) / 10.0 AS affinity,
    t.play_count, t.skip_count,
    t.play_mem_7, t.play_mem_30, t.play_mem_180,
    t.skip_mem_30, t.skip_mem_180,
    t.last_played_at, t.context_tags,
    af.energy, af.instrumentalness, af.speechiness,
    CASE
      WHEN t.last_played_at IS NULL THEN 1.00
      WHEN EXTRACT(EPOCH FROM NOW() - t.last_played_at) / 86400 < 1  THEN 0.05
      WHEN EXTRACT(EPOCH FROM NOW() - t.last_played_at) / 86400 < 3  THEN 0.25
      WHEN EXTRACT(EPOCH FROM NOW() - t.last_played_at) / 86400 < 7  THEN 0.60
      WHEN EXTRACT(EPOCH FROM NOW() - t.last_played_at) / 86400 < 14 THEN 0.85
      ELSE 1.00
    END AS cooldown
  FROM taste t
  JOIN audio_features af ON t.file_path = af.file_path
  WHERE t.disliked = FALSE
    AND NOT 'CONTEXT' = ANY(t.anti_tags)
    AND af.energy BETWEEN 0.35 AND 0.65
    AND af.speechiness < 0.15
    AND af.instrumentalness >= 0.60
  ORDER BY (COALESCE(t.user_rating, 0) / 10.0) *
    CASE
      WHEN t.last_played_at IS NULL THEN 1.00
      WHEN EXTRACT(EPOCH FROM NOW() - t.last_played_at) / 86400 < 1  THEN 0.05
      WHEN EXTRACT(EPOCH FROM NOW() - t.last_played_at) / 86400 < 3  THEN 0.25
      WHEN EXTRACT(EPOCH FROM NOW() - t.last_played_at) / 86400 < 7  THEN 0.60
      WHEN EXTRACT(EPOCH FROM NOW() - t.last_played_at) / 86400 < 14 THEN 0.85
      ELSE 1.00
    END DESC
  LIMIT 100;
\""
```

Adjust the audio feature thresholds, cooldown day values, and `CONTEXT` tag per preset.
Plex stores star ratings as 2/4/6/8/10 internally, so `/10.0` normalizes to 0-1.

**Tag fingerprinting:** For each seed, call Last.fm `track.getTopTags`. Aggregate tag frequencies across all seeds to
find recurring descriptors (e.g. "user's seeds cluster around: psychedelic soul, synthpop, chill hip-hop, neo-soul").
~50% of tracks return no tags -- for those, call `track.getSimilar` and infer character from the neighbours' tags
instead.

**Dimensions to track:**

- Core descriptive tags across seeds (genre, mood, style, production)
- Core anti-preferences (things to avoid)
- Vocal tolerance by context: {work: **, reading: none, upbeat focus: **}
- Preferred era(s), languages, explicit-content policy
- Tempo comfort bands: {work: **-** BPM, reading: **-**, upbeat focus: **-**}
- Energy comfort bands: {work: **-**, reading: **-**, upbeat focus: **-**}
- Top staleness triggers (e.g. "vocal-forward", "too melancholic", "big drops", "same drum palette repeatedly")
- Comfort tracks (safe anchors) vs. overplayed tracks (avoid for now)
- Default exploration rate + max tracks per artist + repeat policy

#### Intent Sheet

Before generating recommendations, produce an Intent Sheet. If the request matches a researched preset, apply its
constraints automatically and note any overrides.

- **Playlist type:** work_concentration | evening_reading | upbeat_concentration | driving | sensual_bedroom |
  gym_strength | discovery | custom
- **Scenario:** where/when/what the user is doing + desired mental state
- **Target affect:** valence x arousal described in plain language
- **Energy & pacing:** desired intensity + whether it changes over time (curve)
- **Lyrics policy:** none | minimal | moderate | free
- **Exploration rate:** % new-to-me vs familiar anchors
- **Diversity constraints:** max tracks per artist; genre breadth; era breadth; geography breadth
- **Coherence constraints:** how smooth should transitions be?
- **Hard constraints:** must include / must exclude
- **Soft preferences:** nice-to-haves
- **ADHD dials** (optional): stimulation (low/med/high), salience guardrail (normal/strict/very strict), structure bias
  (moderate/high)

#### Playlist Presets

These presets are evidence-backed (see [playlist-design.md](playlist-design.md) for full rationale and sources). When a
preset applies, use its constraints as defaults -- the user can override any value.

|                            | work_concentration           | evening_reading         | upbeat_concentration    | driving                      | sensual_bedroom                          | gym_strength                           |
| -------------------------- | ---------------------------- | ----------------------- | ----------------------- | ---------------------------- | ---------------------------------------- | -------------------------------------- |
| **Obj. weights** (R/C/N/S) | 0.35/0.25/0.15/0.25          | 0.25/0.30/0.05/0.40     | 0.30/0.20/0.10/0.40     | 0.33/0.27/0.15/0.25          | 0.30/0.35/0.07/0.28                      | 0.45/0.15/0.30/0.10                    |
| **Energy**                 | 0.35-0.65                    | 0.15-0.40               | 0.55-0.75               | 0.45-0.75                    | 0.25-0.55                                | 0.75-0.95                              |
| **Tempo**                  | 90-130 BPM                   | 55-90 BPM               | 110-140 BPM             | 90-128 BPM                   | 65-105 BPM                               | 120-175 BPM                            |
| **Valence**                | 0.40-0.70                    | 0.35-0.65               | 0.60-0.85               | 0.45-0.80                    | 0.35-0.75                                | 0.25-0.75                              |
| **Instrumentalness**       | >=0.60                       | >=0.80                  | >=0.55                  | 0.20-0.70                    | 0.15-0.65                                | 0.05-0.55                              |
| **Speechiness**            | <0.15 (cap 0.20)             | <0.08 (cap 0.12)        | <0.12 (cap 0.18)        | <0.18 (cap 0.25)             | <0.12 (cap 0.18)                         | <0.25 (cap 0.35)                       |
| **Complexity**             | low-med; steady rhythm       | very low; slow-evolving | low despite high energy | low-med; steady groove       | low-med; warm groove, medium syncopation | medium; strong downbeats               |
| **Lyrics**                 | none (default)               | none (hard)             | none (default)          | moderate                     | moderate                                 | free                                   |
| **dTempo max**             | 10 BPM                       | 6 BPM                   | 8 BPM                   | 8 BPM                        | 6 BPM                                    | 15 BPM                                 |
| **dEnergy max**            | 0.12                         | 0.08                    | 0.10                    | 0.10                         | 0.08                                     | 0.15                                   |
| **Energy curve**           | flat + slight ramp first 20% | gentle taper down       | quick ramp then stable  | ramp + plateau + micro-waves | slow ramp + warm wave + soft taper       | ramp + high plateau with 3-track waves |
| **Exploration**            | 10-25%                       | 0-10%                   | 10-20%                  | 15-30%                       | 5-15%                                    | 25-40%                                 |

R = Relevance, C = Coherence, N = Novelty, S = Salience control.

#### Candidate Generation

All candidates are **specific tracks**, not artists. Source from multiple neighbourhoods:

1. **`track.getSimilar`** (primary) - Run on each seed track. 100% coverage, ~5-10 results per seed = 50-200 candidates.
   This is the backbone.
2. **`artist.getSimilar`** (expand to tracks) - Find similar artists, then select their best individual tracks via
   Last.fm `artist.getTopTracks` or SoulSync DB. Never recommend "anything by Artist X" -- always pick specific tracks.
3. **MusicBrainz relationships** - Collaborations, member-of-band, same-label, "influenced by" via artist relationship
   graph. Expand discovered artists to specific tracks as above.
4. **SoulSync discovery pool** - 1400+ pre-generated track-level candidates with genres and popularity.
5. **Web research** - For culturally specific prompts, scene-relevant options, or niche genres where API data is thin.
   Always resolve to specific tracks.

Use multiple independent sources. If uncertain about existence/availability of a track, flag it.

#### Filtering & Ranking

Enrich the top ~30 candidates with `track.getTopTags`. When tags are absent (~50% of tracks), use **neighbour overlap**
as a proxy: if a candidate's `getSimilar` results overlap with the user's seed tracks' `getSimilar` results, it likely
fits.

When a preset applies, use its objective weights (R/C/N/S) to weight scoring. Score each candidate track on:

1. **Relevance** - Track tags vs user's taste fingerprint. No tags? Check if the candidate appears in multiple seeds'
   similar-track lists.
2. **Coherence** - How well the track fits adjacent to its neighbours. BPM data from SoulSync DB where available. Check
   preset dTempo/dEnergy limits.
3. **Novelty** - SoulSync DB to check what's already owned. Prefer tracks the user doesn't have. Respect preset
   exploration rate.
4. **Salience control** - Enforce preset speechiness/instrumentalness thresholds. Check for attention hooks: lyrics,
   sharp attacks, dramatic drops. Tag violations as "salience-risk" rather than auto-excluding (user may override).

Remove tracks that violate hard constraints.

#### Sequencing

- Order matters. Create a listening path.
- When a preset applies, enforce its max adjacent deltas (dTempo, dEnergy) and energy curve shape from the presets
  table.
- Use "bridges" (1-2 intermediate tracks) when switching subgenre neighbourhoods or rhythmic palettes. Bridges should
  share characteristics with both sides.
- For work_concentration: flat energy with slight ramp first 20%.
- For evening_reading: gentle taper downward; feel like a single stable sound field.
- For upbeat_concentration: quick ramp to target by track 2-3, then stable. Bracket any "booster" track with bridges.
- For driving: quick ramp → long plateau with gentle waves; insert micro-boosts every ~18-22 min to counter transient
  fatigue effects. Avoid sustained >128 BPM blocks.
- For sensual_bedroom: slow ramp (first 20%) → warm plateau → gentle wave → optional taper last 15%. Stay within a
  coherent rhythmic pocket; use texturally smooth bridges (pads, reverb tails).
- For gym_strength: ramp hard (first 15%) → high plateau with 3-track waves (2 high + 1 "rest groove" dip). Wider delta
  tolerance (15 BPM, 0.15 energy) allows sharper genre switches.

#### Output

- Provide the final **track list** in order. Every recommendation is a specific track, not an artist.
- For each track include:
    - **Why it fits** (1-2 sentences) referencing the track's tags or similar-track neighbours, not just the artist's
      reputation.
    - **Source signal** -- what data drove this pick (tag match, similar-track chain from seed X, MusicBrainz
      relationship, discovery pool, web research).
    - **Risk note** if it might not match taste.
- Summarise the playlist's intended arc in 2-4 sentences.
- Ask for feedback:
    - Rate overall fit (1-10)
    - Best 3 tracks + why
    - Worst 3 tracks + why (what specifically failed: vocals, tempo, mood, production style, etc.)
    - Adjust knobs: exploration rate, lyrics policy, energy curve, genre breadth

### Step 3: Download, Playlist, Verify

After the user confirms the track list from Step 2, materialise the playlist. The script uses SoulSync's mirrored
playlist pipeline which handles the full lifecycle: metadata discovery (iTunes), library dedup, Soulseek search with
quality ranking, concurrent downloading (3 workers), metadata tagging, album art, file organization, and Plex playlist
creation.

#### 3a. Download tracks and create Plex playlist

Build a JSON track list from the Step 2 output and run [sync_playlist.py](scripts/sync_playlist.py). The script creates
a mirrored playlist in SoulSync, runs metadata discovery to resolve each track to real iTunes metadata, then syncs
(matches against library, downloads missing tracks via Soulseek, creates the Plex playlist).

```bash
TRACKS='[{"artist":"Mac Miller","track":"Surf","album":"Swimming"},{"artist":"Kiasmos","track":"Looped","album":"Kiasmos"}]'

scp ~/.cursor/skills/music-discovery/scripts/sync_playlist.py homelab:/tmp/
ssh homelab "python3 /tmp/sync_playlist.py --playlist-name 'Evening Vibes' --tracks '$TRACKS'"
```

For large track lists, write the JSON to a file to avoid shell quoting issues:

```bash
cat << 'EOF' > /tmp/tracks.json
[{"artist":"Erykah Badu","track":"Otherside of the Game","album":"Baduizm"},
 {"artist":"Maxwell","track":"Fortunate","album":""}]
EOF
scp /tmp/tracks.json homelab:/tmp/
scp ~/.cursor/skills/music-discovery/scripts/sync_playlist.py homelab:/tmp/
ssh homelab "python3 /tmp/sync_playlist.py --playlist-name 'Neo Soul Essentials' --tracks-file /tmp/tracks.json --timeout 1800"
```

The script runs 4 stages and outputs JSON to stdout (progress on stderr):

1. **Mirror** -- stores the track list in SoulSync
2. **Discover** -- resolves each track to real iTunes metadata (IDs, duration, album art, release date). ~10 seconds for
   20 tracks.
3. **Sync** -- matches discovered tracks against Plex library, creates/updates the Plex playlist with matched tracks,
   adds missing tracks to the wishlist with rich metadata
4. **Download** -- triggers wishlist download for missing tracks, polls until complete

The discovery step is critical: it ensures SoulSync's download engine has real metadata (duration, album name, real IDs)
for generating Soulseek search queries. Without it, search queries fail for ~50% of tracks.

Options:

- `--playlist-name` (required): Name for the Plex playlist
- `--timeout`: Max seconds to wait (default 1200)
- `--keep-mirrored`: Don't delete the temporary mirrored playlist after completion

After downloads complete, trigger a Plex library scan so newly downloaded tracks appear:

```bash
TOKEN=$(ssh mini 'defaults read com.plexapp.plexmediaserver PlexOnlineToken')
ssh mini "curl -s -X POST 'http://localhost:32400/library/sections/3/refresh?X-Plex-Token=$TOKEN'"
```

Wait ~60 seconds for the scan to complete before proceeding.

#### 3b. Analyze new tracks with VibeNet (required)

**Always run VibeNet after downloads complete.** This keeps the `audio_features` table current so future recommendation
runs have energy/valence/instrumentalness/speechiness data for all library tracks.

```bash
ssh homelab 'sudo docker run --rm --add-host=host.docker.internal:host-gateway -v "/mnt/storage/media/music:/music:ro" -v "/home/stan/docker/config/soulsync:/scripts:ro" vibenet /scripts/vibenet-analyze.py'
```

For preset-based playlists, also verify the new tracks against preset thresholds:

```bash
PSQL='sudo docker exec postgres psql -U postgres -d music -t -A'
ssh homelab "$PSQL -c \"SELECT file_path, energy, valence, instrumentalness, speechiness,
  CASE WHEN energy NOT BETWEEN 0.35 AND 0.65 THEN 'energy_out_of_range'
       WHEN speechiness >= 0.15 THEN 'too_much_speech'
       WHEN instrumentalness < 0.60 THEN 'low_instrumentalness'
       ELSE 'PASS' END AS status
FROM audio_features
WHERE analyzed_at > NOW() - INTERVAL '1 hour'
ORDER BY status, file_path;\""
```

Report any tracks that fail verification. The user can decide to keep them (override), swap them out, or adjust the
preset thresholds.

## Temporal Taste & Playlist Refresh

The taste table now includes rolling memory counters (`play_mem_7/30/180`, `skip_mem_30/180`) that
track temporally-decomposed activity at three timescales. These are updated on each sync via
exponential half-life decay. Use these instead of raw play_count/skip_count when judging recent
activity patterns.

### Playlist Refresh

The primary use case is refreshing an existing recurring playlist, not generating from scratch.

- **Compare against previous version:** query `playlist_exposures` to see what was in the last
  version(s). Check which tracks were played (positive signal) vs. skipped (rotation candidate).
- **Rotation:** "familiar" = tracks with `play_count > 0`, not just tracks on disk. Keep ~40-60%
  familiar tracks that are performing well, rotate in ~30-40% fresh candidates from the ranking
  pool, reserve ~10-20% for discovery (tracks with low play counts or new additions).
- **Record the result:** after materializing, insert rows into `playlist_exposures`.

```bash
PSQL='sudo docker exec postgres psql -U postgres -d music -t -A'

# What was in the last version of a playlist
ssh homelab "$PSQL -c \"SELECT track_artist, track_name, position FROM playlist_exposures WHERE context = 'work_concentration' ORDER BY generated_at DESC, position LIMIT 30;\""

# Tracks appearing in the last 3 generations of a context
ssh homelab "$PSQL -c \"
  WITH recent AS (
    SELECT DISTINCT generated_at FROM playlist_exposures
    WHERE context = 'work_concentration' ORDER BY generated_at DESC LIMIT 3
  )
  SELECT pe.track_artist, pe.track_name, COUNT(*) AS appearances
  FROM playlist_exposures pe JOIN recent r ON pe.generated_at = r.generated_at
  WHERE pe.context = 'work_concentration'
  GROUP BY pe.track_artist, pe.track_name
  ORDER BY appearances DESC;
\""

# Record a new playlist generation
ssh homelab "$PSQL -c \"
  INSERT INTO playlist_exposures (playlist_name, context, track_artist, track_name, track_album, position)
  VALUES
    ('Work Focus v12', 'work_concentration', 'Kiasmos', 'Looped', 'Kiasmos', 1),
    ('Work Focus v12', 'work_concentration', 'Bonobo', 'Kerala', 'Migration', 2);
\""
```

### Skip Interpretation

Use rolling skip memories to spot patterns. The agent acts based on engagement level:

- **Quick mode:** if `skip_mem_30 >= 3`, drop the track from the candidate pool. Explicitly
  mention what was dropped and why in the output so the user can correct.
- **Review mode:** surface as a note: "Dropped Track X (3 skips in the last month). Flag if wrong."
- **Deep dive mode:** ask: "Track X has been skipped a few times recently. Wrong context, burned
  out, or don't like it?" Record: wrong context → add anti_tag, burned out → no action (cooldown
  handles it), don't like → update rating or set disliked.

```bash
# Tracks with notable recent skip activity
ssh homelab "$PSQL -c \"SELECT artist, track, skip_mem_30, skip_mem_180, play_mem_30 FROM taste WHERE skip_mem_30 >= 2 ORDER BY skip_mem_30 DESC;\""
```

### Periodic Taste Review

Ratings do not decay automatically. A 5-star rating stays 5 stars until the user says otherwise.
Instead, the agent surfaces stale ratings for human review at the right moment:

- **Never in quick mode.** Don't interrupt routine refreshes.
- **In review mode:** brief note: "15 tracks in your pool have ratings over a year old. Review?"
- **In deep dive mode:** surface stale ratings and walk through them.

```bash
# Tracks with old ratings still in active rotation
ssh homelab "$PSQL -c \"SELECT artist, track, user_rating, last_rated_at FROM taste WHERE user_rating IS NOT NULL AND last_rated_at < NOW() - INTERVAL '1 year' AND play_count > 0 ORDER BY last_rated_at LIMIT 20;\""
```

### Reintroduction

Tracks with low ratings or high skip history that haven't been played in 6+ months are candidates
for reintroduction. The agent proposes these, never forces them:

- **Quick mode:** may include 1 reintroduction in the discovery slot if it fits the context well.
- **Review mode:** flagged in draft: "Trying Track X again -- rated 2 stars a year ago, your taste
  shifted toward similar stuff. Remove it?"
- **Deep dive mode:** full proposal with reasoning.
- **Never auto-reintroduce** tracks with `disliked = TRUE`.
- **No hardcoded quotas.** The user decides how many reintroductions to include.
- **Record outcome:** if played → stays in rotation. If skipped → note "reintroduction failed."

```bash
# Reintroduction candidates (low-rated, not disliked, dormant 6+ months)
ssh homelab "$PSQL -c \"SELECT artist, track, user_rating, last_played_at, skip_count FROM taste WHERE disliked = FALSE AND (user_rating IS NOT NULL AND user_rating <= 6) AND (last_played_at IS NULL OR last_played_at < NOW() - INTERVAL '6 months') ORDER BY last_played_at NULLS FIRST LIMIT 15;\""
```

### Research Reasoning Principles

The agent should understand these patterns conceptually and apply them as judgment, not formulas:

- **Inverted-U exposure curve:** a track peaks in enjoyment around ~10 listens, then declines.
  Use this to judge when a favorite is getting overplayed.
- **Asymmetric skip signals:** skips on recently-played tracks (`play_mem_7 > 0` AND new skips)
  are likely saturation, not dislike. Skips on tracks not played recently are stronger negatives.
- **Multi-timescale taste:** `play_mem_7` captures weekly fixations, `play_mem_180` captures
  enduring preferences. A track with high 180-day memory but zero 7-day memory is a stable
  favorite that hasn't been heard recently (rotation candidate), not a forgotten track.
- **Context clustering:** similar activities produce similar preferences. When the user asks for
  a new context type, reason from the nearest existing preset.

## Managing Taste Data

The `taste` table in PostgreSQL (`music` database on homelab) is the single durable store for all preference signals.
The agent manages it via SQL through `docker exec psql`.

```bash
PSQL='sudo docker exec postgres psql -U postgres -d music -t -A'

# Tag a track for a specific context
ssh homelab "$PSQL -c \"UPDATE taste SET context_tags = array_append(context_tags, 'driving') WHERE artist = 'ARTIST' AND track = 'TRACK';\""

# Tag multiple tracks at once (e.g. all tracks by an artist for gym)
ssh homelab "$PSQL -c \"UPDATE taste SET context_tags = array_append(context_tags, 'gym') WHERE artist = 'ARTIST' AND NOT 'gym' = ANY(context_tags);\""

# Remove a context tag
ssh homelab "$PSQL -c \"UPDATE taste SET context_tags = array_remove(context_tags, 'driving') WHERE artist = 'ARTIST' AND track = 'TRACK';\""

# Add an anti-tag (track doesn't work for a context)
ssh homelab "$PSQL -c \"UPDATE taste SET anti_tags = array_append(anti_tags, 'too_vocal_for_reading') WHERE artist = 'ARTIST' AND track = 'TRACK';\""

# Mark a track as disliked (hard exclusion from all recommendations)
ssh homelab "$PSQL -c \"UPDATE taste SET disliked = TRUE WHERE artist = 'ARTIST' AND track = 'TRACK';\""

# Add a note
ssh homelab "$PSQL -c \"UPDATE taste SET notes = 'Great bridge track between metal and ambient' WHERE artist = 'ARTIST' AND track = 'TRACK';\""

# View all context tags in use
ssh homelab "$PSQL -c \"SELECT DISTINCT unnest(context_tags) AS tag, COUNT(*) FROM taste GROUP BY tag ORDER BY count DESC;\""

# Overview: ratings distribution
ssh homelab "$PSQL -c \"SELECT user_rating, COUNT(*) FROM taste WHERE user_rating IS NOT NULL GROUP BY user_rating ORDER BY user_rating DESC;\""
```

**Valid context tags** correspond to playlist preset types. Current presets: `work_concentration`, `evening_reading`,
`upbeat_concentration`. Additional tags can be any string (e.g., `driving`, `gym`, `sensual`, `cooking`, `party`).

```bash
# Rolling memory snapshot (recent activity patterns)
ssh homelab "$PSQL -c \"SELECT artist, track, play_mem_7, play_mem_30, play_mem_180, skip_mem_30, skip_mem_180 FROM taste WHERE play_mem_7 > 0 OR skip_mem_30 > 0 ORDER BY play_mem_7 DESC LIMIT 20;\""

# Playlist history for a context
ssh homelab "$PSQL -c \"SELECT playlist_name, generated_at, COUNT(*) AS tracks FROM playlist_exposures WHERE context = 'work_concentration' GROUP BY playlist_name, generated_at ORDER BY generated_at DESC LIMIT 5;\""
```

**When to update taste data:**

- After playlist feedback: if the user reports tracks that didn't fit, add anti-tags or mark as disliked
- During recommendation: if the user says "this track is perfect for driving," add the context tag
- After materializing a playlist: insert rows into `playlist_exposures` to track what was placed where

## Metadata Sources

Do NOT query all sources for every track. Use each source at the pipeline stage where it adds value.

**Rate budget for a typical run:** 20 seed tracks x 2 calls each (tags + similar) = 40 calls, plus ~30 candidate
enrichment calls = ~70 total Last.fm calls at 5 req/sec = ~15 seconds. MusicBrainz at 1 req/sec is slower -- use
sparingly (5-10 calls for artist relationships). Batch by phase: gather all seed data first, then generate all
candidates, then enrich top candidates. Do not interleave.

### VibeNet + PostgreSQL (Layer 0 -- audio features + taste data, free, local)

The `music` database on homelab PostgreSQL has two tables:

- **`audio_features`**: energy, valence, instrumentalness, speechiness, danceability, acousticness, liveness (all 0-1
  scale) for every track in the library. Keyed by `file_path`.
- **`taste`**: user ratings (Plex 2-10 scale, i.e. 1-5 stars), play/skip counts, rolling memory
  counters (`play_mem_7/30/180`, `skip_mem_30/180`), context tags, anti-tags, dislikes. Keyed by
  `(artist, track, album)`. Joins with `audio_features` via `file_path`.
- **`playlist_exposures`**: tracks which tracks were placed in which playlists. Keyed by
  `(playlist_name, context, track_artist, track_name, generated_at)`. Used for rotation decisions.

```bash
PSQL='sudo docker exec postgres psql -U postgres -d music -t -A'

# Query features for specific tracks
ssh homelab "$PSQL -c \"SELECT file_path, energy, valence, instrumentalness, speechiness FROM audio_features WHERE file_path ILIKE '%SEARCH_TERM%';\""

# Filter tracks matching a playlist preset (e.g. work_concentration)
ssh homelab "$PSQL -c \"SELECT file_path, energy, valence, instrumentalness, speechiness FROM audio_features WHERE energy BETWEEN 0.35 AND 0.65 AND speechiness < 0.15 AND instrumentalness >= 0.60 ORDER BY energy;\""

# Analyze new tracks after download (incremental -- only processes files not already in postgres)
ssh homelab 'sudo docker run --rm --add-host=host.docker.internal:host-gateway -v "/mnt/storage/media/music:/music:ro" -v "/home/stan/docker/config/soulsync:/scripts:ro" vibenet /scripts/vibenet-analyze.py'
```

After any SoulSync download completes, run the incremental analyze command to keep features up to date.

### SoulSync DB (Layer 0 -- library awareness, free, local)

Database: `/app/data/music_library.db` in the `soulsync` container. Primary use: **deduplication** (what does the user
already own?) and cross-reference IDs (Spotify/MusicBrainz/Deezer).

```bash
# What the user owns (for dedup during candidate filtering)
ssh homelab 'sudo docker exec soulsync python3 -c "
import sqlite3; c = sqlite3.connect(\"/app/data/music_library.db\").cursor()
c.execute(\"SELECT a.name, al.title, COUNT(t.id) FROM artists a JOIN albums al ON al.artist_id=a.id JOIN tracks t ON t.album_id=al.id GROUP BY a.name, al.title\")
for r in c.fetchall(): print(f\"{r[0]} - {r[1]} ({r[2]} tracks)\")
"'

# BPM data for tempo-based preset filtering (available on ~30% of tracks)
ssh homelab 'sudo docker exec soulsync python3 -c "
import sqlite3; c = sqlite3.connect(\"/app/data/music_library.db\").cursor()
c.execute(\"SELECT a.name, t.title, t.bpm FROM tracks t JOIN artists a ON t.artist_id=a.id WHERE t.bpm IS NOT NULL AND t.bpm BETWEEN 90 AND 130 ORDER BY t.bpm\")
for r in c.fetchall(): print(f\"{r[0]} - {r[1]} | {r[2]:.0f} BPM\")
"'

# Recent listening history (what the user actually played, with timestamps)
ssh homelab 'sudo docker exec soulsync python3 -c "
import sqlite3; c = sqlite3.connect(\"/app/data/music_library.db\").cursor()
c.execute(\"SELECT artist, title, album, played_at FROM listening_history ORDER BY played_at DESC LIMIT 30\")
for r in c.fetchall(): print(f\"{r[0]} - {r[1]} ({r[2]}) | {r[3]}\")
"'

# Seasonal tracks as candidate source (pre-curated by SoulSync)
ssh homelab 'sudo docker exec soulsync python3 -c "
import sqlite3; c = sqlite3.connect(\"/app/data/music_library.db\").cursor()
c.execute(\"SELECT track_name, artist_name, album_name, popularity FROM seasonal_tracks ORDER BY popularity DESC LIMIT 20\")
for r in c.fetchall(): print(f\"{r[1]} - {r[0]} ({r[2]}) pop={r[3]}\")
"'
```

**Enrichment columns on tracks/artists** (populated by SoulSync's background workers -- check availability before
relying on them):

- `tracks`: `bpm`, `lastfm_tags`, `lastfm_playcount`, `genius_lyrics`, `genius_description`, `isrc`, `play_count`,
  `last_played`
- `artists`: `lastfm_tags`, `lastfm_similar`, `lastfm_bio`, `genius_description`, `genres`

When these are populated, they can replace or supplement external API calls. See the enrichment cache note under Last.fm
below.

### Last.fm API (Layer 1 -- primary enrichment, 5 req/sec)

**Before calling Last.fm**, check if SoulSync already has the data cached locally. This saves rate budget and is
instant:

```bash
ssh homelab 'sudo docker exec soulsync python3 -c "
import sqlite3; c = sqlite3.connect(\"/app/data/music_library.db\").cursor()
# Check if artist has cached Last.fm tags and similar artists
c.execute(\"SELECT lastfm_tags, lastfm_similar, lastfm_bio FROM artists WHERE name = \\\"ARTIST\\\"\")
r = c.fetchone()
if r and r[0]: print(f\"tags: {r[0]}\")
if r and r[1]: print(f\"similar: {r[1]}\")
# Check if track has cached Last.fm tags
c.execute(\"SELECT t.lastfm_tags, t.lastfm_playcount FROM tracks t JOIN artists a ON t.artist_id=a.id WHERE a.name = \\\"ARTIST\\\" AND t.title = \\\"TRACK\\\"\")
r = c.fetchone()
if r and r[0]: print(f\"track tags: {r[0]}\")
"'
```

Only fall back to the Last.fm API when SoulSync's enrichment data is NULL for the entity you need.

**API key required.** Create one free at `https://www.last.fm/api/account/create`.

```bash
LASTFM_KEY="0b27fdd7aa84d1168c7bea667b316e4d"

# Per-track mood/style tags (the key enrichment Last.fm provides)
curl -s "http://ws.audioscrobbler.com/2.0/?method=track.getTopTags&artist=ARTIST&track=TRACK&api_key=$LASTFM_KEY&format=json" | python3 -c "
import sys, json
for tag in json.load(sys.stdin).get('toptags', {}).get('tag', [])[:10]:
    print(f\"{tag['name']} ({tag['count']})\")
"

# Similar tracks (sonic neighbours for candidate generation)
curl -s "http://ws.audioscrobbler.com/2.0/?method=track.getSimilar&artist=ARTIST&track=TRACK&api_key=$LASTFM_KEY&format=json&limit=20" | python3 -c "
import sys, json
for t in json.load(sys.stdin).get('similartracks', {}).get('track', []):
    print(f\"{t['artist']['name']} - {t['name']} | match={t.get('match','')}\")
"

# Similar artists
curl -s "http://ws.audioscrobbler.com/2.0/?method=artist.getSimilar&artist=ARTIST&api_key=$LASTFM_KEY&format=json&limit=20" | python3 -c "
import sys, json
for a in json.load(sys.stdin).get('similarartists', {}).get('artist', []):
    print(f\"{a['name']} | match={a.get('match','')}\")
"

# Artist tags (genre/style descriptors)
curl -s "http://ws.audioscrobbler.com/2.0/?method=artist.getTopTags&artist=ARTIST&api_key=$LASTFM_KEY&format=json" | python3 -c "
import sys, json
for tag in json.load(sys.stdin).get('toptags', {}).get('tag', [])[:10]:
    print(f\"{tag['name']} ({tag['count']})\")
"
```

### MusicBrainz API (Layer 2 -- relationship graph, 1 req/sec, no key needed)

Use MusicBrainz IDs from SoulSync DB (`musicbrainz_id` on artists, `musicbrainz_recording_id` on tracks) for direct
lookups.

```bash
UA="MusicDiscovery/1.0 (github.com/user)"

# Artist relationships (collaborations, member-of, side projects)
curl -s "https://musicbrainz.org/ws/2/artist/MBID?inc=artist-rels&fmt=json" -H "User-Agent: $UA" | python3 -c "
import sys, json
for rel in json.load(sys.stdin).get('relations', []):
    target = rel.get('artist', {}).get('name', '')
    print(f\"{rel.get('type','')} -> {target}\")
"

# Artist genre tags
curl -s "https://musicbrainz.org/ws/2/artist/MBID?inc=tags&fmt=json" -H "User-Agent: $UA" | python3 -c "
import sys, json
for tag in sorted(json.load(sys.stdin).get('tags', []), key=lambda x: x.get('count',0), reverse=True)[:10]:
    print(f\"{tag['name']} ({tag.get('count',0)})\")
"
```

### Spotify (Layer 3 -- via SoulSync's cached data)

Do not call the Spotify API directly. SoulSync already caches Spotify metadata (genres, popularity, IDs) in its
database. Use the SoulSync DB queries above -- the `discovery_pool` table contains Spotify-sourced popularity scores and
genre data for 1400+ candidates. Artist-level Spotify genres are in the `artists.genres` column.
