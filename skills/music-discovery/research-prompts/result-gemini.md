Temporal Taste Modeling and Heuristic Sequencing for Personal Music Playlists

1. The Unified Temporal Affinity Framework The fundamental challenge in modeling personal music taste within a
   constrained, single-user environment is the absence of large-scale collaborative filtering data and real-time session
   feedback. Traditional music recommendation systems deployed by major streaming platforms rely heavily on matrix
   factorization, deep neural networks, and massive user-item interaction matrices to predict affinity.1 These systems
   leverage the listening habits of millions to solve the cold-start problem and infer the context of individual track
   skips. However, in a localized infrastructure managing approximately 2,000 tracks via PostgreSQL and an LLM-based
   agent, such machine learning architectures are neither feasible nor strictly necessary.2 Furthermore, the
   architectural constraints of this specific implementation dictate that all affinity scoring, temporal decay, and
   staleness prevention mechanisms must be entirely deterministic. The logic must be expressible through advanced SQL
   queries and heuristic rules processed periodically, rather than through continuously trained models evaluating
   mid-session telemetry. Adding to this algorithmic complexity is the psychological profile of the target listener. The
   presence of ADHD introduces unique cognitive variables regarding auditory stimulation, novelty-seeking, and rapid
   satiety. Individuals with ADHD frequently exhibit cycles of musical hyper-fixation—listening to a single track or
   specific auditory profile repeatedly to regulate dopamine and maintain executive focus—followed by abrupt, profound
   burnout. A standard recommendation algorithm that merely pushes highly-rated, frequently-played tracks to the top of
   the queue will inevitably induce auditory fatigue. Conversely, a purely randomized algorithm will fail to provide the
   structural consistency required for state-dependent contexts like deep work or exercise. To resolve these
   intersecting constraints, the analysis proposes the Unified Temporal Affinity Score (UTAS). The UTAS serves as the
   definitive, continuous metric for candidate generation, representing the probability that a specific track will
   provide optimal stimulation and satisfaction in the precise moment of playlist generation. The UTAS synthesizes
   static preferences, dynamic behavioral signals, cognitive memory decay, and contextual alignment into a single
   calculable value. The mathematical formulation of the UTAS is defined as a composite function:

The components of this model are defined as follows: (Time-Decayed Explicit Rating): The conscious, user-assigned rating
(1-10), subjected to an asymmetric exponential decay function that slowly regresses aging preferences toward a library
mean. (Behavioral Affinity): The subconscious preference signal derived from a Bayesian smoothed ratio of historical
play counts against aggregate skip counts. (Staleness and Satiety Modifier): A dynamic penalty or boost based on
recency, modeled via a bounded logistic curve to enforce cooldowns and reward exploration. (ACT-R Reintroduction
Probability): A cognitive memory model modifier that identifies tracks which have been forgotten and gently boosts them
back into the candidate pool. (Contextual Alignment): A heuristic penalty applied to tracks that violate the audio
feature centroids or categorical tags of the target playlist context. and (Weights): The proportional balance between
explicit conscious ratings and implicit behavioral signals. The subsequent sections of this report will deconstruct each
of these variables, providing the psychological justification, mathematical derivation, and concrete SQL implementation
required to deploy this architecture within the specified technological stack. 2. Signal Weighting: Reconciling Ratings,
Plays, and Skips Recommendation algorithms must weigh explicit feedback (conscious ratings) against implicit feedback
(subconscious behavior like plays and skips).4 Explicit ratings represent an intellectual judgment of a track's
objective quality or aesthetic value. However, behavioral signals often contradict these ratings. A listener might rate
a complex jazz composition as a 9/10 due to its artistic merit but only play it twice a year. Conversely, a highly
stimulating electronic track might be rated a 5/10 but played fifty times during gym sessions. For an ADHD profile,
implicit behavioral signals are often superior indicators of a track's immediate utility for regulating attention and
arousal.6 2.1 The Bayesian Smoothed Engagement Ratio The most direct measure of behavioral affinity is the relationship
between how often a track is played to completion versus how often it is skipped. However, utilizing a naive skip ratio
() introduces severe volatility for tracks with low interaction volumes.7 If a newly added track is played once and
skipped once, the naive ratio implies a 50% rejection rate, which lacks statistical confidence. To counteract this
volatility in a small library, the system must utilize Laplace smoothing, effectively establishing a Bayesian prior.
This pulls the engagement ratio of unplayed or rarely-played tracks toward a safe, assumed baseline until sufficient
user interaction data accumulates to override it. The smoothed behavioral engagement ratio is calculated as follows:

The parameters (Prior Plays) and (Prior Skips) define the baseline assumption for a track with zero history. Setting
assumes a baseline of two successful plays. Setting assumes a baseline of one skip. For a completely unplayed track,
this yields an engagement ratio of or . This is an optimistic prior, ensuring that new additions to the library are
treated favorably and are given the opportunity to surface in generated playlists. As actual plays and skips accumulate,
the impact of the and constants diminishes, and the ratio asymptotically approaches the true behavioral average. To
integrate this ratio seamlessly with the explicit rating system, it must be scaled to a continuous modifier bounding
between -1.0 and 1.0. This allows heavy skipping to actively subtract from a track's baseline score, while heavy playing
adds to it.

Under this scaling, a track with an engagement ratio of 0.80 yields a behavioral affinity of +0.60, while a track with
an engagement ratio of 0.30 yields a behavioral affinity of -0.40. 2.2 Time-Weighting Historical Plays Not all plays
carry equal predictive weight. Streaming platforms like Spotify segment user listening history into multiple distinct
timescales (typically 7 days, 28 days, and 6-12 months) to capture both immediate hyper-fixations and long-term
foundational taste.5 Because the localized PostgreSQL database aggregates total plays into a single integer (play_count)
and only stores the most recent playback timestamp (last_played_at), the system cannot perfectly reconstruct a 28-day
rolling play count. However, the system can approximate this temporal weighting by modulating the total play_count based
on recency. If a track has 100 plays but has not been listened to in four years, treating those 100 plays with the same
mathematical weight as 100 plays accumulated over the last month will severely distort the recommendation generation. To
resolve this, the system applies a logarithmic temporal discount to the play_count variable before it enters the
engagement ratio formula.

Where represents the days since the track was last played. This formula preserves the full value of the play count for
30 days. After 30 days of inactivity, the value of the historical plays begins to logarithmically compress. A track
unplayed for 365 days will have its effective play count reduced by approximately 60%, preventing ancient obsessions
from permanently dominating the behavioral affinity score. 2.3 Balancing Explicit and Implicit Signals The base affinity
score, before any situational or staleness modifiers are applied, is the weighted sum of the decayed explicit rating and
the behavioral affinity. Assuming the 1-10 rating is normalized to a 0.0-1.0 scale:

The determination of the weights (Rating Weight) and (Behavioral Weight) must reflect the user's interaction paradigm.
If the user meticulously rates tracks and updates those ratings frequently, should be dominant. However, given the
constraints of the ADHD profile and the tendency for behavior to outpace database curation, a recommended balance is:
(Rating Weight): (Behavioral Weight): This configuration ensures that conscious ratings establish the architectural
foundation of the track's value, while the behavioral affinity acts as a powerful gravitational pull, dynamically
adjusting the score based on actual listening habits without entirely overriding the user's explicit curation.4 3.
Rating Decay Functions and Preference Drift Human musical preferences are subject to continual evolution. The phenomenon
of preference drift dictates that a rating applied to a track several years ago possesses significantly less predictive
validity than a rating applied recently.10 In recommendation systems, this is typically addressed through temporal decay
functions that down-weight older data.11 3.1 Selecting the Decay Architecture Research into temporal dynamics in
recommender systems evaluates three primary mathematical architectures for decay: step functions, linear decay, and
exponential decay.13 Step Functions: This approach applies rigid cutoffs (e.g., dropping the weight of a rating by 50%
exactly one year after creation). Step functions are computationally simple but psychologically invalid, as human memory
and preference do not degrade in sudden, sheer cliffs. Linear Decay: This approach subtracts a fixed amount of value for
every passing day. Linear decay is highly destructive over long time horizons; eventually, all ratings will decay into
negative numbers unless artificially bounded, failing to capture the durable nature of core musical tastes. Exponential
Decay: Exponential decay curves mirror biological and cognitive degradation, where the rate of decay is proportional to
the current value. The score drops rapidly at first, then forms a long, stable tail.11 This is the most evidence-based
approach for modeling subjective affinity over time. While standard exponential decay forces values toward zero, a music
recommendation system must account for the cyclical nature of nostalgia. A track rated 10/10 three years ago should not
decay to a 0/10; rather, the certainty of that 10/10 rating diminishes, and the system should assume the track has
regressed slightly toward the library's average quality baseline. Therefore, the system employs a Bounded Exponential
Decay Model:

Where: : The global average rating of the entire 2,000-track library (typically around 0.50 or 0.60 on a normalized
scale). : The specific track's normalized 0.0-1.0 rating. : The time elapsed in days since last_rated_at. : The decay
constant, derived from the targeted half-life parameter () via the equation . 3.2 Asymmetric Half-Life Parameterization
The half-life parameter () dictates how many days must pass before the difference between the original rating and the
library mean is cut in half. Empirical research in multimedia recommendation systems often utilizes half-lives ranging
from 40 to 150 days.11 However, music consumption differs drastically from movie or e-commerce consumption because music
is inherently designed for repetition.10 Furthermore, cognitive retention and preference drift operate asymmetrically.
High-arousal positive associations (tracks that deeply resonate with core identity) degrade much slower than mild
negative associations (tracks that were irritating in a specific mood but might be tolerable later).14 A track rated
9/10 three years ago is highly likely to still be considered "good" today. Conversely, a track rated 3/10 three years
ago may have been judged unfairly during a period of over-exposure and is ripe for a second chance. To accurately model
this psychological reality, the half-life parameter must dynamically adjust based on the initial explicit rating. Rating
Bracket Original Score Recommended Half-Life (T1/2​) Derived λ Constant Psychological Rationale High 8 - 10 730 Days (2
Years)

Strong positive preferences form durable neural pathways. Decay should be minimal, acting only to slightly soften older
favorites compared to new obsessions. Medium 5 - 7 180 Days (~6 Months)

Moderate ratings are highly susceptible to taste drift and contextual shifts. They should decay toward the mean
relatively quickly to encourage re-evaluation. Low 1 - 4 90 Days (~3 Months)

Negative ratings often stem from transient over-exposure or acute mood mismatch. Rapid decay allows these tracks to be
softly reintroduced sooner.

By implementing this asymmetric decay structure, the algorithm organically facilitates the eventual reintroduction of
previously disliked tracks. Over the span of a year, a track rated 3/10 will have its negative penalty heavily decayed,
allowing its score to drift upward toward the 5/10 library average, where random exploration mechanics can occasionally
pull it into a playlist for re-evaluation. 4. Heuristic Disambiguation of Skip Signals Interpreting skip behavior is one
of the most complex challenges in music recommendation, particularly when restricted to aggregate metrics. Without
precise session telemetry—such as the exact second a track was skipped, or the tracks that played immediately before and
after it—the database's skip_count integer represents an ambiguous accumulation of user dissatisfaction.8 Research into
user behavior on streaming platforms categorizes skips into three primary cognitive intents 7: Active Dislike: A genuine
aesthetic rejection of the track's auditory profile. Satiety (Saturation): The user enjoys the track but has experienced
dopamine depletion regarding this specific stimulus due to recent over-exposure. Context Mismatch: The track is
inherently enjoyable but entirely inappropriate for the current physiological or environmental state (e.g., an
aggressive metal track surfacing during a focused reading session). To build an actionable heuristic, the system must
triangulate the ambiguous skip_count against the play_count, the last_played_at timestamp, and the context_tags. 4.1 The
Skip Intent Disambiguation Matrix By evaluating the ratios and recencies of interactions, the LLM agent can utilize
deterministic SQL conditions to classify the probable intent behind the skips and apply the appropriate penalization.17
Matrix Condition Inferred User Intent Action / Algorithmic Penalty skip_count > 2 AND play_count = 0 Active Dislike
Apply maximum penalty to . Track is effectively blacklisted from generation until long-term rating decay intervenes.
skip_count > play_count AND last_played_at > 90 days Stale Dislike Historic rejection. The penalty remains active but
allows for the ACT-R memory model (Section 6) to eventually trigger a reintroduction. play_count skip_count AND
last_played_at < 7 days Satiety / Burnout The user loves the track but is currently fatigued. Do not heavily penalize
the core affinity; instead, rely on the freshness cooldown multiplier to suppress it temporarily. play_count skip_count
AND audio features mismatch preset Context Mismatch Track is highly situational. Skips are likely driven by poor
sequencing. Utilize anti_tags to isolate the track from this specific context rather than destroying its global score.

4.2 The Recency-Weighted Skip Satiety Index To translate the matrix above into a seamless mathematical function for the
database, the impact of a skip on the engagement ratio must be dynamically weighted based on recency. If a track
possesses 50 historical plays, and the user skips it twice this week, treating those skips as a permanent degradation of
the track's quality is a false assumption; they are symptoms of transient satiety. We define a dynamic skip weight ()
that reduces the destructive power of a skip if the track was played successfully in the very recent past.

If (days since last play) is close to zero, drops to . This means recent skips only carry half the negative weight in
the calculation, protecting the long-term score of a beloved track from a temporary bout of ADHD-driven auditory
burnout. As the days since the last play increase, returns to 1.0, ensuring that skips on tracks that haven't been heard
in months are treated as genuine aesthetic rejections. 5. Staleness Prevention and Satiety Cooldowns Preventing
staleness is arguably the most critical requirement for an ADHD-oriented music system. The neurological mechanics of
ADHD involve chronic dopamine dysregulation, leading to a behavioral pattern of intense novelty-seeking. When an ADHD
listener discovers a stimulating track, they will frequently hyper-fixate, playing it relentlessly until the
neurological reward is entirely depleted. If the recommendation algorithm stubbornly relies on the highest Base Affinity
Score, a small cluster of top-rated, frequently-played songs will utterly dominate every generated playlist,
accelerating this burnout cycle and rendering the playlists monotonous.18 To counter this, the system must implement
aggressive diminishing returns formulas and mandatory cooldown periods.20 5.1 The Logistic Freshness Modifier Each
consecutive play of a track yields diminishing cognitive returns. Therefore, the probability of a track being selected
by the LLM agent must decrease logarithmically with recent play frequency, and recover exponentially as time elapses.14
Rather than utilizing a rigid, binary rule (e.g., WHERE last_played_at < NOW() - INTERVAL '3 days'), a continuous
fractional cooldown provides superior, organic rotation. The Freshness Modifier () is mathematically modeled using an
S-curve (Logistic function). This curve ensures that a track is heavily penalized immediately after playback, slowly
recovers its probability over a designated cooldown window, and eventually receives an "exploration bonus" if it remains
unplayed for a prolonged duration. To ensure computational efficiency when querying across thousands of rows in
PostgreSQL, the standard logistic function is approximated using a bounded algebraic fraction:

Where: : The elapsed time in days since last_played_at. If null (unplayed), this resolves to infinity, making the
fraction equal to 1.0. : The cooldown parameter representing the exact number of days required for the track to reach
50% of its normal selection probability. : The maximum allowable exploration bonus (e.g., 1.25). If a track has a of 7
days, and it was played exactly 7 days ago, its is . This cuts its effective UTAS in half, allowing older, slightly
lower-rated tracks to surpass it in the playlist generation queue. If the track remains unplayed for 60 days, the
fraction resolves to . To actively encourage the surfacing of neglected tracks, the formula is adjusted to push past 1.0
into the territory for long-forgotten tracks:

Under this adjusted formula, a track unplayed for months will receive up to a 25% artificial boost to its UTAS, granting
it a temporary competitive advantage against newer favorites. Once it is selected and played, resets to zero, plummets
to zero, and the track is instantly rotated out of the active daily rotation. 5.2 Dynamic Cooldowns for Hyper-Fixation
The parameter dictates the severity of the staleness prevention. For standard listening habits, a 5-to-7 day recovery
half-life is sufficient. However, to explicitly address ADHD hyper-fixation, the system can utilize a dynamic cooldown
parameter. While the database does not store session arrays, the relationship between total play_count and
last_played_at provides clues. If the agent detects an unusually high play_count relative to the track's age in the
library (if added_at is tracked), or if a secondary lightweight table tracks "plays in the last 7 days," the system can
trigger a "dopamine detox" protocol. Standard Rotation: days. Burnout Guardrail: If play_count > 20 and the track is in
the top 5% of recent plays, dynamically extends to 21 days. This effectively buries the hyper-fixated track for three
weeks, forcing the listener to pivot to new stimuli and preserving the long-term utility of the track. 6. ACT-R Memory
Modeling for Track Reintroduction A robust personal music system must not merely rotate favorites; it must also possess
a mechanism for the soft reintroduction of previously rejected tracks. When a track is low-rated or frequently skipped,
it sinks to the bottom of the candidate pool. However, taste evolves, and a track skipped in 2023 might be highly
appealing in 2026. Determining when a track feels "fresh" enough to try again requires a psychological model of human
memory. The cognitive architecture ACT-R (Adaptive Control of Thought-Rational) provides a highly validated framework
for predicting memory retrieval and music relistening behavior.21 ACT-R utilizes a declarative memory module where the
"activation" of a memory (or a song preference) depends on its base-level learning equation, which integrates both the
frequency of past exposure and the recency of that exposure.24 6.1 Approximating the ACT-R Activation Equation The pure
ACT-R base-level activation formula requires the exact timestamp of every historical interaction () a user has ever had
with an item:

Where is the cognitive memory decay parameter. Research specific to music relistening identifies as a standard cognitive
default, while is highly optimized for modeling week-over-week relistening fatigue and memory decay.21 Because the local
PostgreSQL database only stores the aggregate play_count and the single last_played_at timestamp, the pure ACT-R
equation cannot be executed natively. It must be heuristically approximated.24 The approximation assumes that the total
play_count () represents the frequency asymptote, while the days since last_played_at () drives the recency decay.
SQL-Compatible ACT-R Approximation ():

Using , this formula accurately tracks the psychological "availability" of a song in the user's working memory. A
recently played track will yield a positive activation score. A track unplayed for hundreds of days will yield a heavily
negative activation score, signifying that it has been functionally forgotten by the active auditory memory.25 6.2 The
Reintroduction Trigger and Probability Bonus The system utilizes the intersection of the Rating Decay (Section 3) and
the ACT-R Activation to trigger soft reintroductions. Consider a track that was rated 3/10 two years ago. Over those two
years: The Asymmetric Rating Decay has slowly pulled the 3/10 rating back upward, neutralizing the severe numerical
penalty and returning it to the library average. The ACT-R Activation () has dropped significantly into negative values
(e.g., ) due to the massive . The system isolates tracks where the explicit rating or historical engagement was low, but
the has fallen below a critical "forgotten" threshold (empirically, ). When this condition is met, the system applies a
Reintroduction Probability Bonus () to the UTAS. This acts as a mild multiplier (e.g., 1.20x) that subtly pushes the
forgotten, previously-disliked track into the mid-tier of the candidate pool. If the track is sequenced by the LLM agent
and the user plays it without skipping: The last_played_at timestamp updates to today. The instantly shoots back into
positive territory. The condition for is broken, the bonus vanishes, and the new, positive behavioral signals govern its
future placement. If the user skips it again: The skip_count increases, driving the behavioral affinity further
negative. The last_played_at timestamp updates, resetting the ACT-R memory. The track is plunged back into a deep
algorithmic hibernation, requiring another multi-year wait before its memory activation drops low enough to trigger
another reintroduction. 7. Context-Specific Signal Interpretation In a tightly curated library of 2000 tracks, global
scoring is inherently flawed because music taste is fundamentally contextual. A high-bpm electronic track may possess a
stellar global UTAS due to heavy play counts during gym sessions, but sequencing that track into an evening reading
playlist would derail the user's cognitive state.26 While the existing system utilizes audio feature thresholds (energy,
valence, instrumentalness, speechiness) to filter candidate tracks for specific presets, relying purely on binary
thresholding creates rigid, predictable boundaries. To bridge this gap, the global UTAS must be modulated by a
continuous Context Alignment Score (). 7.1 Continuous Audio Feature Alignment When the Claude LLM agent initiates a
playlist generation sequence for a specific context (e.g., deep_work), it should not just apply hard SQL WHERE clauses
(e.g., WHERE energy BETWEEN 0.35 AND 0.65). Instead, it defines the ideal centroid for that context. For deep_work, the
ideal centroids might be: Energy: 0.45 Speechiness: 0.05 Instrumentalness: 0.90 The modifier is calculated as a function
of the Euclidean distance between the track's actual audio features and the context's ideal centroids. Tracks that sit
exactly on the centroid receive a multiplier of . As a track drifts further from the centroid—even if it technically
remains within the acceptable bounds—its drops toward , penalizing its overall UTAS for that specific playlist request.
This ensures that the most contextually perfect tracks naturally float to the top of the selection pool, while edge-case
tracks are only selected if their freshness and affinity scores are overwhelmingly high. 7.2 Managing Context-Blind
Skips via Anti-Tags The most significant vulnerability of an aggregate local database is managing context-blind skips.
If a user skips a track during a reading session because it was too energetic, the database simply registers skip_count
= skip_count + 1. This indiscriminately damages the track's global Behavioral Affinity (), eventually ruining its
placement in the gym playlists where it actually belongs. Because Plex and PostgreSQL cannot natively segment skips by
the session context in which they occurred, the system must rely on user-curated metadata guardrails: context_tags and
anti_tags. Positive Tags (context_tags): If a track is tagged with "gym", and the LLM is generating a gym playlist, a
flat multiplier is applied to the score, overriding minor audio-feature deviations. Negative Tags (anti_tags): If a
track possesses the anti-tag "reading", its for any reading-related preset is hard-coded to , making it mathematically
impossible for the LLM to select it. The implementation constraint requires the user to actively curate these tags. When
a jarring track interrupts a focused session, the user should not merely skip it; they should apply an anti-tag for that
context. This simple heuristic protects the integrity of the global UTAS while permanently solving the contextual
sequencing error. 8. Practical SQL Implementation Formulas To render this theoretical framework actionable within the
specified constraints, the mathematical models must be translated into PostgreSQL compatible syntax. The Claude agent
will execute these calculations via Common Table Expressions (CTEs) to rank the 2000-track library and draw the optimal
sequence. 8.1 Variable Definitions and Bounds Assume a table tracks containing the columns: user_rating (1-10),
play_count, skip_count, last_played_at, last_rated_at, energy, speechiness, instrumentalness. The base metrics must be
extracted and bounded to prevent null errors or divide-by-zero faults:

SQL

WITH base_metrics AS ( SELECT track_id, COALESCE(user_rating, 5.0) / 10.0 AS R, -- Normalize 1-10 to 0.0-1.0
COALESCE(play_count, 0) AS P, COALESCE(skip_count, 0) AS S, GREATEST(EXTRACT(DAY FROM NOW() - last_played_at), 0.1) AS
days_since_play, GREATEST(EXTRACT(DAY FROM NOW() - last_rated_at), 0.1) AS days_since_rate, energy, speechiness,
instrumentalness FROM tracks ),

8.2 Calculating Components (Decay, Affinity, Freshness) The subsequent CTE calculates the psychological and temporal
components using the asymmetric half-lives and the bounded logistic freshness curve:

SQL

component_calculations AS ( SELECT track_id, R, P, S, days_since_play,

        -- 1. Asymmetric Rating Decay (Targeting Library Mean of 0.5)
        CASE
            WHEN R >= 0.8 THEN 0.5 + (R - 0.5) * EXP(-0.00095 * days_since_rate)  -- 730 day half-life
            WHEN R >= 0.5 THEN 0.5 + (R - 0.5) * EXP(-0.00385 * days_since_rate)  -- 180 day half-life
            ELSE 0.5 + (R - 0.5) * EXP(-0.00770 * days_since_rate)                -- 90 day half-life
        END AS R_decay,

        -- 2. Bayesian Smoothed Behavioral Affinity (Alpha=2, Beta=1)
        -- Includes Recency-Weighted Skip Satiety
        (
            (P + 2.0) /
            (P + (S * (1.0 - (0.5 * EXP(-days_since_play / 7.0)))) + 3.0)
            * 2.0
        ) - 1.0 AS H_affinity,

        -- 3. Logistic Freshness Modifier (7-day cooldown, 1.25x exploration max)
        -- Forces score to 0 if track has zero plays but multiple skips
        CASE
            WHEN P = 0 AND S > 2 THEN 0.0
            ELSE LEAST(1.25, (days_since_play / (days_since_play + 7.0)) * 1.35)
        END AS M_freshness,

        -- 4. ACT-R Memory Activation Approximation (d=0.86)
        LN(P + 1.0) - (0.86 * LN(days_since_play + 1.0)) AS ACT_R_Activation

    FROM base_metrics

),

8.3 The Final UTAS Assembly The final query synthesizes these components into the UTAS. The LLM agent injects the
contextual centroids (in this example, targeting energy=0.45, speechiness=0.05, instrumentalness=0.90).

SQL

utas_ranking AS ( SELECT c.track_id,

        -- Base Score: 55% Rating, 45% Behavior
        ((c.R_decay * 0.55) + (c.H_affinity * 0.45)) AS Base_Score,

        -- Reintroduction Probability Boost (1.20x if forgotten & previously disliked)
        CASE
            WHEN c.R < 0.5 AND c.ACT_R_Activation < -2.5 THEN 1.20
            ELSE 1.0
        END AS P_reintro,

        -- Context Alignment Penalty (Euclidean Distance from LLM-provided Centroids)
        -- Scaled to output between 0.5 (poor match) and 1.0 (perfect match)
        GREATEST(0.5, 1.0 - SQRT(
            POWER(b.energy - 0.45, 2) +
            POWER(b.speechiness - 0.05, 2) +
            POWER(b.instrumentalness - 0.90, 2)
        )) AS P_context

    FROM component_calculations c
    JOIN base_metrics b ON c.track_id = b.track_id

)

SELECT track_id, (Base_Score _ M_freshness _ P_reintro \* P_context) AS UTAS FROM utas_ranking ORDER BY UTAS DESC LIMIT
100;

The LLM agent pulls this ranked list of 100 top-UTAS candidates. Because the UTAS organically rotates tracks based on
the freshness cooldowns, this candidate list will look fundamentally different from week to week, preventing playlist
staleness. The agent then applies the previously researched sequencing logic (energy curves, transition bridges, artist
diversity limits) to map these raw candidates into the final playlist geometry. 9. Edge Cases and System Limitations
While the UTAS framework robustly manages temporal dynamics within a constrained infrastructure, specific edge cases
necessitate explicit guardrails to prevent algorithmic collapse. 9.1 The Cold Start Problem for Local Additions When new
albums are added to the library, they possess zero plays, zero skips, and typically lack an explicit rating. Without
intervention, these tracks fall into a mathematical void.2 Under the provided SQL formulas, a completely blank track is
gracefully handled: The unrated R coalesces to (the mean). The smoothed evaluates to . The base score initializes to a
modest . However, because days_since_play defaults to infinity, the yields the maximum exploration bonus of . This
ensures new tracks are competitive, but they will not overpower established favorites. To guarantee that newly imported
tracks are actually heard, the LLM agent must enforce a distinct rule during the final playlist assembly: A minimum of
10% and a maximum of 20% of the playlist volume must be allocated to tracks where play_count = 0. This hardcoded
diversity metric forces exploration without overwhelming the user's ADHD requirement for structural familiarity. 9.2 The
Limitations of Aggregate Telemetry The most significant limitation of this architecture is the reliance on Plex's
aggregate sync data. Because Plex cannot provide the timestamp of an individual skip, the algorithm cannot differentiate
between a skip occurring at 5 seconds (an immediate aesthetic rejection) and a skip occurring at 4 minutes and 30
seconds (skipping a long, silent outro).27 Both interactions increase skip_count by . Over time, tracks with prolonged
fade-outs will accrue massive skip counts simply because the user becomes impatient as the song ends, inadvertently
destroying the track's behavioral affinity score. This is a structural limitation of the technology stack that
mathematics cannot solve. It requires human-in-the-loop curation. The user must manually edit the audio files to trim
extensive fade-outs or create a custom outro_skip_safe tag in the database. The SQL logic can then be amended to halve
the negative impact of skip_count for any track bearing this tag, preserving the UTAS for tracks that are genuinely
beloved but structurally prone to late-stage skipping. 9.3 Conclusion By synthesizing cognitive memory models, bounded
decay functions, and Bayesian behavioral smoothing, the Unified Temporal Affinity Score transforms a static, localized
PostgreSQL database into a dynamic, context-aware recommendation engine. It mathematically satisfies the dopamine
regulation requirements of an ADHD listener through aggressive staleness cooldowns, ensures the periodic re-evaluation
of rejected music, and achieves organic playlist rotation without the prohibitive infrastructure costs of real-time
machine learning architectures. Works cited Exploiting Music Play Sequence for Music Recommendation - IJCAI, accessed
March 29, 2026, https://www.ijcai.org/proceedings/2017/0511.pdf Deep content-based music recommendation, accessed March
29, 2026, http://papers.neurips.cc/paper/5004-deep-content-based-music-recommendation.pdf "Context Aware Music
Recommendation and Playlist Generation" by Elias Mann, accessed March 29, 2026,
https://scholar.smu.edu/jour/vol8/iss2/2/ Spotify's Music Recommendation Algorithm: The Complete Guide - Beats To Rap
On, accessed March 29, 2026, https://beatstorapon.com/blog/ultimate-guide-to-spotify-music-algorithm/ How to Get Your
Music Recommended by Streaming Algorithms? - Soundcharts, accessed March 29, 2026,
https://soundcharts.com/en/blog/how-to-get-recommended-by-streaming-algorithms (PDF) Music Recommendations -
ResearchGate, accessed March 29, 2026, https://www.researchgate.net/publication/339301409_Music_Recommendations (PDF)
Sequential skip prediction using deep learning and ensembles - ResearchGate, accessed March 29, 2026,
https://www.researchgate.net/publication/331206584_Sequential_skip_prediction_using_deep_learning_and_ensembles The
skipping behavior of users of music streaming services and its relation to musical structure - PMC, accessed March 29,
2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC7526936/ Spotify Popularity Score guide: what it is and when and why it
matters for artists - SubmitHub, accessed March 29, 2026, https://www.submithub.com/story/spotify-popularity-score-guide
Time-Aware Music Recommender Systems: Modeling the Evolution of Implicit User Preferences and User Listening Habits in A
Collaborative Filtering Approach - MDPI, accessed March 29, 2026, https://www.mdpi.com/2076-3417/10/15/5324 A Half-Life
Decaying Model for Recommender Systems with Matrix Factorization, accessed March 29, 2026,
https://www.researchgate.net/publication/320223308_A_Half-Life_Decaying_Model_for_Recommender_Systems_with_Matrix_Factorization
Exponential Decay Function-Based Time-Aware Recommender System for E-Commerce Applications - The Science and Information
(SAI) Organization, accessed March 29, 2026,
https://thesai.org/Downloads/Volume13No10/Paper_71-Exponential_Decay_Function_Based_Time_Aware_Recommender_System.pdf
Half-life - Wikipedia, accessed March 29, 2026, https://en.wikipedia.org/wiki/Half-life Dynamic Forgetting and
Spatio-Temporal Periodic Interest Modeling for Local-Life Service Recommendation - arXiv, accessed March 29, 2026,
https://arxiv.org/html/2508.02451v1 Analyzing user behavior and sentiment in music streaming services - Diva-portal.org,
accessed March 29, 2026, https://www.diva-portal.org/smash/get/diva2:927614/FULLTEXT01.pdf On Skipping Behaviour Types
in Music Streaming Sessions | Request PDF - ResearchGate, accessed March 29, 2026,
https://www.researchgate.net/publication/355784422_On_Skipping_Behaviour_Types_in_Music_Streaming_Sessions Analyzing and
Predicting Spotify Skip Behaviour | TDS Archive - Medium, accessed March 29, 2026,
https://medium.com/data-science/to-skip-or-not-to-skip-that-is-the-question-a0c76925737e Running Playlist BPM: 5
Science-Backed Rules for Better Runs - Runners Connect, accessed March 29, 2026,
https://runnersconnect.net/running-with-music/ To Skip, or Not to Skip? That Is The Question - Towards Data Science,
accessed March 29, 2026, https://towardsdatascience.com/to-skip-or-not-to-skip-that-is-the-question-a0c76925737e/
Diminishing Returns in Music: Learn How to Overcome Practice Plateaus, accessed March 29, 2026,
https://lakehighlandsmusic.com/diminishing-returns-in-music-learn-how-to-overcome-practice-plateaus/ Predicting Music
Relistening Behavior Using the ACT-R Framework - Humans and Recommender Systems, accessed March 29, 2026,
https://humrec.github.io/publication/reiter-haas-recsys-2021/reiter-haas-recsys-2021.pdf Predicting Music Relistening
Behavior Using the ACT-R Framework - arXiv, accessed March 29, 2026, https://arxiv.org/html/2108.02138v2 Integrating the
ACT-R Framework with Collaborative Filtering for Explainable Sequential Music Recommendation - HCAI MMS Group JKU,
accessed March 29, 2026, https://hcai.at/assets/pdf/2023_recsys_actr.pdf Applying Mathematical Optimization Methods to
an ACT-R Instance-Based Learning Model, accessed March 29, 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC4936697/
[2108.02138] Predicting Music Relistening Behavior Using the ACT-R Framework - arXiv, accessed March 29, 2026,
https://arxiv.org/abs/2108.02138 Contextual Personalized Re-Ranking of Music Recommendations through Audio Features -
arXiv, accessed March 29, 2026, https://arxiv.org/pdf/2009.02782 The skipping behavior of users of music streaming
services and its relation to musical structure | Spotify Research, accessed March 29, 2026,
https://research.atspotify.com/publications/the-skipping-behavior-of-users-of-music-streaming-services-and-its-relation-to-musical-structure
