# Playlist Design: Evidence Base and Detailed Rationale

Read this file when generating playlists from any researched preset, or when the user asks about the evidence behind playlist constraints.

## Evidence Summary

- **Lyrics reliably impair reading** (d ~ -0.3 for comprehension). Instrumental conditions are near-null.
- **Fast + loud instrumental disrupts reading** relative to silence; slower/softer does not.
- **Background music meta-analysis**: overall effects average near-null because positive and negative cancel out by task/music/context. But text understanding has a reliably negative association (weighted r ~ -0.11).
- **"Work flow" music** (steady rhythm, simple tonality, broad spectral energy <6 kHz, moderate dynamism, no lyrics/hooks) produced significant improvements in mood and processing speed vs. "deep focus" music, pop hits, or office noise.
- **ADHD**: effects are individual-difference-driven. Beta-range amplitude modulations benefit higher-ADHD-symptom participants. Music reduces errors in children with and without ADHD (moderate effect). Safest approach: make ADHD adaptations optional, conservative, feedback-driven.

## Audio Feature Definitions

Ranges are 0.0-1.0 unless noted. Based on Spotify's audio-features schema:

- **Energy**: perceptual intensity/activity. Contributing factors: dynamic range, loudness, timbre, onset rate, entropy.
- **Instrumentalness**: likelihood of no vocals. >0.5 intended as instrumental.
- **Speechiness**: spoken-word presence. >0.66 mostly speech; 0.33-0.66 mixed; <0.33 mostly music.
- **Valence**: musical positiveness. Higher = happier/cheerful.
- **Tempo**: estimated BPM.

## Detailed Subtype Specifications

### Work Concentration

**Objective weights** (sum to 1.0):
- Relevance 0.35 (taste fit + "workable" genre neighbourhoods)
- Coherence 0.25 (smooth transitions)
- Novelty 0.15 (avoid staleness)
- Salience control 0.25 (avoid attention capture)

**Audio targets**:
- Energy: 0.35-0.65 (moderate activation without "fast & loud")
- Tempo: 90-130 BPM (steady pacing compatible with "work flow" groove)
- Valence: 0.40-0.70 (neutral-to-positive)
- Instrumentalness: >=0.60 preferred; down to 0.40 only if speechiness stays low
- Speechiness: <0.15 (hard cap 0.20)
- Complexity: low-to-medium event/tonal complexity. Prefer repetitive/minimal harmony. Avoid concentrated high-frequency energy, highly articulated attacks.

**Sequencing**:
- Energy curve: mostly flat with slight ramp in first 15-25% (settling -> flow), then stable plateau
- Tempo curve: avoid saw-toothing; cluster adjacent BPM tightly
- Max adjacent deltas: dTempo <=10 BPM, dEnergy <=0.12, dValence <=0.20
- Bridge rule: when switching subgenre neighbourhoods, insert 1-2 bridge tracks sharing rhythm density or timbral palette with both sides

**Lyrics**: default none. If allowed, confine to late playlist segments (lower-stakes tasks), require low speechiness and "submerged" vocals. Tag any vocal-forward track as salience-risk.

**Sourcing**: two-lane approach:
1. Anchors lane (taste-fit): user's known "I can work to this" tracks
2. Work-flow lane (function-fit): instrumental music matching the tested profile (strong rhythm, simple tonality, broad spectral energy <6 kHz, moderate dynamism, no lyrics/hooks)

**User knobs**: default vocal tolerance, preferred tempo band, preferred energy band, groove preference (low/med/high), complexity tolerance (low/med/high), max salience events, exploration rate (10-25%), max repeats policy

### Evening Reading

**Objective weights**:
- Relevance 0.25 (pleasant, non-irritating)
- Coherence 0.30 (very smooth; minimise context switching)
- Novelty 0.05 (stability > discovery)
- Salience control 0.40 (primary goal: reduce interference)

**Audio targets**:
- Energy: 0.15-0.40 (low arousal)
- Tempo: 55-90 BPM preferred; allow up to 100 if low energy and low dynamism
- Valence: 0.35-0.65 (neutral/comforting)
- Instrumentalness: >=0.80 (highly instrumental)
- Speechiness: <0.08 (hard cap 0.12)
- Complexity: very low. Prefer ambient, minimal, slow-evolving textures. Avoid high event density and abrupt structural changes.

**Sequencing**:
- Energy curve: gentle taper downward (evening wind-down)
- Tempo curve: flat or slowly decreasing
- Max adjacent deltas: dTempo <=6 BPM, dEnergy <=0.08, dValence <=0.15
- Bridge rule: for instrumentation shifts (piano -> ambient pads), use intermediate tracks (piano + pads, reverb-heavy)

**Lyrics**: none (hard constraint). Flag any track with intelligible lyrics as non-compliant. Only non-lexical vocals (vocalise/choir pads) if any.

**Sourcing**: prioritise instrumental-only catalogues: ambient, minimalist classical, slow post-classical, drone, soft instrumental jazz, soundtracks. Exclude borderline tracks with sampled speech. Keep tempo and loudness conservative.

**User knobs**: absolute lyrics ban (default yes), preferred sleepiness level (low/med), max BPM (default 90), preferred instrumentation, darkness tolerance (valence floor), dynamic-range tolerance, exploration rate (0-10%)

### Upbeat Concentration

**Objective weights**:
- Relevance 0.30 (must feel good; avoid irritation/fatigue)
- Coherence 0.20 (flow, but more movement allowed than reading)
- Novelty 0.10 (some freshness, carefully)
- Salience control 0.40 (despite upbeat, focus still fails with frequent salience spikes)

**Audio targets**:
- Energy: 0.55-0.75 (higher activation)
- Tempo: 110-140 BPM (groove-forward)
- Valence: 0.60-0.85 (positive; mood lift)
- Instrumentalness: >=0.55 preferred (or >=0.40 if speechiness stays very low)
- Speechiness: <0.12 (hard cap 0.18)
- Complexity: low structural complexity despite higher energy. Prefer strong steady rhythm + simple tonality. Avoid hooks, drops, dramatic breakdowns.

**Sequencing**:
- Energy curve: quick ramp to target by track 2-3, then stable with small oscillations (micro-variation reduces boredom)
- Tempo curve: tight cluster, especially first half
- Max adjacent deltas: dTempo <=8 BPM, dEnergy <=0.10
- If inserting a higher-energy "booster", bracket it with bridge tracks (one before, one after)
- Bridge rule: when changing rhythmic palette (four-on-the-floor <-> breaky <-> syncopated), insert a hybrid track sharing both rhythmic markers

**Lyrics**: default none. If allowed, only in final 15-20% and tagged "focus-risk".

**Sourcing**: use work-flow template as primary filter (strong rhythm, simple tonality, moderate dynamism, broad spectral energy <6 kHz, no lyrics/hooks). Maintain fatigue control: rotate substyles within the same rhythm family.

**User knobs**: energy ceiling, tempo comfort band, groove intensity (low/med/high), hook intolerance, vocal intolerance, boosters policy (0/1/2 per hour), exploration rate (10-20%), fatigue protection (max same drum palette in a row, max per artist)

## ADHD Considerations

Effects are individual-difference-driven, not one-size-fits-all. All adaptations should be optional, conservative, and feedback-driven.

**What to try (controlled)**:
1. Lyric-free music as default (lyrics are a predictable interference source)
2. "Stimulation dosing" rather than "more energetic = better" (high-arousing music can increase perceived effort)
3. Structured, predictable rhythm and simple tonality for focus tasks
4. Optionally trial purpose-designed amplitude-modulated music for sustained-attention blocks (beta-range modulation showed differential benefit for higher ADHD symptoms)
5. Lightweight A/B self-experimentation (same task, similar time of day, compare silence vs playlists)

**What to avoid**:
- Lyrics during reading or text-heavy work
- Fast + loud instrumental for reading
- Frequent novelty shocks (abrupt style/tempo changes)

**Adjustable parameters** (instead of binary "ADHD mode"):
- Stimulation dial (low/medium/high): raises/lowers energy+tempo targets and groove density
- Salience guardrail strictness (normal/strict/very strict): tightens speechiness/vocal thresholds and adjacent deltas
- Structure bias (moderate/high): increases preference for simple tonality and predictable rhythms

### Driving

**Evidence summary:**
- Loud music increases mental effort irrespective of traffic context, even when driving performance is not impaired (cognitive-compensatory strategy).
- As music tempo increases, driving speed and speed estimates increase; traffic violations are most frequent with fast-paced music.
- Medium-tempo music performs best overall for reducing fatigue and maintaining attention on long highway drives. Slow tempo may worsen fatigue after long exposure; fast tempo may relieve fatigue but harm attention after extended time.
- Self-selected music improves objective fatigue measures acutely, but the effect is transient (~15-25 minutes). Higher intensity/tempo and less instrumental tracks tended to be more effective against fatigue.
- Positive background music delays fatigue when introduced before onset and alleviates it after onset.
- Driver-preferred music from home increased severity of risky driving events in novice drivers, whereas alternative in-car music reduced event severity.
- High/medium volume tends to increase average speed; low volume can decrease it.

**Objective weights** (sum to 1.0):
- Relevance 0.33 (taste fit improves comfort/engagement, but highly preferred tracks can become attention-capturing)
- Coherence 0.27 (abrupt shifts create salience spikes competing with driving demands)
- Novelty 0.15 (freshness combats monotony, but too much surprise raises distraction)
- Salience control 0.25 (tempo/intensity and personal salience can increase speed/risk)

**Audio targets:**
- Energy: 0.45-0.75 (moderate-to-moderately-high supports alertness; capped because higher arousal linked to faster driving/more violations)
- Tempo: 90-128 BPM (medium tempo best for long-distance attention/fatigue; >130 zone repeatedly implicated in speed/risk escalation)
- Valence: 0.45-0.80 (positive affect helps fatigue strategies; avoid very dark/angry material that may push arousal/risk)
- Instrumentalness: 0.20-0.70 (vocals help engagement during monotony and may be more effective against fatigue; maintain instrumental band to reduce semantic distraction)
- Speechiness: <0.18 (hard cap 0.25; driving already consumes cognitive resources)
- Complexity: low-med. Steady pulse, predictable phrasing, limited abrupt structural surprises.

**Sequencing:**
- Energy curve: quick ramp (first 10-15%) → long plateau with gentle waves → micro-boost every ~15-25 min → avoid end taper unless "arrival wind-down" enabled
- Tempo curve: mostly stable (95-120 core) with brief "wake-up crests" (120-128); avoid sustained >128 blocks
- Max adjacent deltas: dTempo <=8 BPM, dEnergy <=0.10
- Bridge rule: insert 1 bridge when changing genre family or when needed tempo jump exceeds delta cap. Bridges sit within ±4 BPM of both neighbours, keep energy within ±0.07, and prefer hybrid-genre or instrumental/OST to reduce semantic salience.

**Lyrics:** default moderate. Acceptable when familiarity is moderate and density is not story-heavy. Reduce when driving conditions are complex or user reports distraction. Hard cap: speechiness 0.25.

**Sourcing:** mid-tempo groove-stable material: synthwave/outrun, melodic rock, groove-forward metal (mid-tempo, less chaotic), rhythmic cinematic OST, Americana/country road-trip with restrained vocal density. Avoid high-salience novelty bombs, skit-heavy hip-hop, reggaeton.

**User knobs:** alertness level (Energy ±0.08, Tempo ±6 BPM), wake-up pulse frequency (default every 18-22 min), vocal density, safety strictness (tightens deltas/lowers energy ceiling), novelty (default 20%), darkness tolerance (valence floor to 0.35 if enabled)

### Sensual / Bedroom

**Evidence summary:**
- Music interventions show reliable stress-reduction effects: physiological d≈0.38, psychological d≈0.545 in broad meta-analysis of 104 RCTs.
- For acute stress recovery in healthy individuals, effects are more mixed (g=0.15, non-significant) with substantial heterogeneity.
- In everyday life, music listening is associated with lower subjective stress (p=0.010), with largest effects when listening for relaxation (cortisol p≤0.001).
- Music can operate as a dyadic co-regulation cue: women showed lower cortisol after listening; stronger cortisol linkage when partners' preferences were more similar.
- Groove research: medium syncopation produces greatest wanting-to-move and pleasure (inverted-U).
- Medium complexity rhythms elicit higher pleasure/wanting-to-move and engage reward-linked basal ganglia regions.
- Slow tempo (~60-80 BPM) is often associated with down-regulating heart rate; instrumental can be less activating but lyrics can be comforting (context-dependent).

**Objective weights** (sum to 1.0):
- Relevance 0.30 (shared preferences shape dyadic physiology)
- Coherence 0.35 (highest: intimacy benefits from continuous, non-jarring environment)
- Novelty 0.07 (surprises risk rupturing mood)
- Salience control 0.28 (activation spikes push away from relaxed-aroused balance)

**Audio targets:**
- Energy: 0.25-0.55 (low-to-moderate supports relaxation without sleepiness)
- Tempo: 65-105 BPM (slow-moderate supports relaxation effects; raised lower bound to preserve sensual groove)
- Valence: 0.35-0.75 (warmth/tenderness; allow sensual minor-key mood)
- Instrumentalness: 0.15-0.65 (vocals support emotional connection; excessive lyrics pull attention into semantic tracking)
- Speechiness: <0.12 (hard cap 0.18; protect immersion)
- Complexity: low-med. Steady pocket/groove, moderate syncopation, minimal abrupt structural turns.

**Sequencing:**
- Energy curve: slow ramp (first 20%) → warm plateau → gentle wave (1-2 soft peaks) → taper last 15% if "wind-down" enabled
- Tempo curve: start 65-80 → drift to 80-100 (groove phase) → optional return to 70-85
- Max adjacent deltas: dTempo <=6 BPM, dEnergy <=0.08
- Bridge rule: insert bridges when shifting vocal style or genre family. Bridges should be texturally smooth (pads, reverb tails) and keep speechiness <0.10.

**Lyrics:** default moderate. Acceptable when romantic/sensual themes with low narrative density. Minimise when user wants meditative embodied presence. Hard cap: speechiness 0.18.

**Sourcing:** neo-soul, downtempo R&B, trip-hop, atmospheric pop, smooth jazz-adjacent, warm electronic, sensual film/TV OST. Highlight soothing female vocalists (Sade-adjacent, Sabrina Claudio-like). Use groove-centred tracks with medium rhythmic complexity. Avoid comedy skits, harsh vocals, aggressive EDM drops, reggaeton. Explicit content user-controlled.

**User knobs:** warmth/heat (Energy ±0.10, Valence ±0.10), groove vs float (Tempo centre 75 vs 90, Complexity very-low vs low-med), vocals ratio (default 60% vocal), lyric intimacy (filters speechiness + tags), novelty (default 10%), wind-down end (optional taper)

### Gym (Strength Training)

**Evidence summary:**
- Meta-analytic review: small-to-moderate ergogenic/psychophysical benefits: affective valence g=0.48, physical performance g=0.31, RPE reduction g=0.22; performance benefits moderated by tempo (fast > slow-to-medium).
- Preferred vs non-preferred vs no music: significant advantages for preferred music on strength endurance (SMD=0.72), maximal strength (SMD=0.53), power output (SMD=0.47), plus higher motivation and lower RPE.
- Music had no benefit to explosive power at 30% 1RM, but increased repetitions-to-failure at low/moderate intensities; self-selected and metal conditions especially favourable.
- In women at 75% 1RM back-squat: music increased reps-to-failure by ~18.5% (ES=0.507), motivation (ES=0.704), and reduced RPE (ES=0.456).
- Preferred vs non-preferred during Wingate sprints: no power advantage but motivation strongly increased (ES=1.520) and RPE decreased (ES=0.540).
- Pre-task music meta-analysis: significant benefits for relative peak power (SMD=0.53) and mean power (SMD=0.38) but no RPE change, suggesting "psych-up" effects.
- Null results exist at moderate loads (50% 1RM): no effect of preferred music during rest intervals on power/HR, underscoring need for intensity/timing tailoring.

**Objective weights** (sum to 1.0):
- Relevance 0.45 (highest: preferred music has strongest/most consistent benefits)
- Coherence 0.15 (hard training tolerates sharper transitions)
- Novelty 0.30 (elevated to reduce habituation and keep psych-up potency)
- Salience control 0.10 (lowest: gym can benefit from arousal and attention capture)

**Audio targets:**
- Energy: 0.75-0.95 (high energy for psychophysiological activation; slight ceiling below 1.0 for fatigue/irritation control)
- Tempo: 120-175 BPM (fast tempo explicitly linked to larger performance benefits; covers metal/industrial/synthwave/DnB)
- Valence: 0.25-0.75 (allow "dark hype" aggression; mid-valence supports motivation/enjoyment)
- Instrumentalness: 0.05-0.55 (allow vocals: preferred music effects are strong, many motivational genres include vocals)
- Speechiness: <0.25 (hard cap 0.35; permit rap/trap-metal, cap to avoid skits)
- Complexity: medium (med-high allowed at peaks). Strong rhythmic drive, clear downbeats, higher density permitted.

**Sequencing:**
- Energy curve: ramp hard (first 15%) → high plateau with 3-track waves (2 high + 1 slightly lower "rest groove") → optional 10% taper for cooldown
- Tempo curve: warm-up 110-130 → working phase 135-175 with dips to 125-140 → optional cooldown <120
- Max adjacent deltas: dTempo <=15 BPM, dEnergy <=0.15
- Bridge rule: use bridges when switching high-contrast genre textures (e.g., doom-industrial → metalcore → synthwave). Bridges keep tempo within ±8 BPM and share timbral elements.

**Lyrics:** default free (with guardrails). Acceptable when motivational/aggressive and not skit-heavy. Reduce when user wants technique focus (heavy singles, complex lifts). Hard cap: speechiness 0.35.

**Sourcing:** metalcore/alt-metal (Sleep Token/BMTH-adjacent), groove metal, industrial rock, aggressive synthwave, hard rock, dark cinematic OST (Doom/Tenet/Dune). Self-selected and metal conditions are especially supportive for reps/effort outcomes. Avoid reggaeton and long ambient interludes unless deliberate "rest groove."

**User knobs:** psych-up intensity (Energy ±0.10, Tempo ±10 BPM), aggression priming (Valence floor to 0.15, distortion sourcing), rest-dip depth (wave amplitude), vocals vs instrumentals, novelty (default 30%), technique mode (tightens dTempo to 10, raises instrumentalness floor to 0.25), scream tolerance (default on)
