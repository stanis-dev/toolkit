# Personal AI Assistant as Force Multiplier

## Summary

Designing a personal AI assistant as a high-trust augmentation system across communication, cognitive capture, and daily operations, with deep user adaptation focused on operational fit rather than pseudo-intimacy.

## Key findings

- The best-supported shape is augmentation, not autonomy: draft, capture, review, and bounded coaching are stronger than independent action.
- Deep adaptation should prioritize channel-specific voice, workflow defaults, challenge level, timing, and explicit boundaries over personality labels.
- The main risks are sycophancy, cognitive delegation, stale-profile lock-in, premature structuring of thought, and hidden self-modification.
- The strongest near-term use cases are communication drafting/revision, meeting synthesis and follow-up, thought-dump to structured tasks/decisions, and bounded coaching.

## Research status

- **Phase:** First-pass landscape synthesis complete
- **Base materials:** `context/deep-research-prompt.md`, `context/first-step-dr-result-gpt.md`, `context/first-step-dr-result-claude.md`, `context/first-step-dr-result-gemini.md`
- **Working benchmark:** `context/reply-drafting-gold-set.md` contains the first 22 draft DM / direct-mention eval cases
- **Coaching integration:** `context/comms-coaching-integration.md` maps the comms research onto a second assistant job: criterion-based communication coaching
- **Coaching benchmark:** `context/comms-coaching-eval-set.md` contains the first 12 scored authored-message coaching cases
- **Sierra supplement:** `context/comms-coaching-sierra-supplement.md` is source evidence used to harden the default coaching standard, with extra attention to collapse-pattern review
- **Pass 1:** `context/comms-coaching-pass-1.md` synthesizes the first larger 30-message coaching pass
- **Live batch 1:** `context/comms-coaching-live-batch-1.md` reviews a recent non-curated batch of Sierra-facing messages using the default instruction block
- **Live batch 2:** `context/comms-coaching-live-batch-2.md` is the first recent-message pass using the fully updated authority-growth review format
- **Skill smoke test:** `context/communication-copilot-smoke-test-1.md` manually tests the new communication-copilot skill on three realistic prompts
- **Best synthesis base:** GPT is the best base for the design document; Claude adds sharper risk and measurement frames; Gemini is more useful for implementation brainstorming than for scoping the research itself.
- **Core question:** What are the best practices, proven patterns, and common pitfalls for designing a personal AI assistant with deep user adaptation at its core?
- **Next research question:** What is the minimum viable explicit user profile, evaluation rubric, and dissent policy that measurably lowers edit burden without increasing sycophancy?
- **First concrete assistant job:** Monitor direct mentions and DMs, research likely context from Slack, Teams, and meetings, and propose reply drafts in your voice for approval
- **Second concrete assistant job:** Review authored communication against the quiet-confidence target and identify concrete improvement moves without flattery or pseudo-therapy

## Local data sources already available

### 1. Brain meeting corpus (`/Users/stan/code/rec/data`)

- 12 WAV recordings
- 9 transcript JSON files
- 17 plain transcript TXT files
- 8 polished transcript TXT files
- 5 summary markdown files
- 7 reasoning traces (`.jsonl`)
- Example meetings include `Pronet--Sierra-Standup`, `Alex-Baas-AI---Client-Validation`, `UK-Agent-Reviews`, and `Maundy-Thursday`
- Best use: meeting summarization, to-do extraction, follow-up drafting, identifying spoken communication patterns, and comparing raw transcript -> polished summary output

### 2. Slack exports (`/Users/stan/code/rec/data/slack`)

- **Sierra workspace:** 31 channel/DM JSON exports, 31 readable markdown views, 995 downloaded image attachments
- **Wizeline workspace:** 41 channel/DM JSON exports, 41 readable markdown views
- Readable views already exist under each workspace's `readable/` directory
- Best use: channel-specific written voice, collaborator-specific norms, recurring workflows, async prioritization patterns, and drafting benchmarks

### 3. Teams exports (`/Users/stan/code/rec/data/teams/sierra`)

- 2 channel exports
- 5 chat/meeting exports
- 7 readable markdown views
- Includes standups, working-group threads, and cross-org coordination
- Best use: meeting coordination patterns, decision continuity between meetings and chat, and follow-up/alignment language

## Continuous update implications

- These sources are not a one-time corpus; they are live context streams that will keep changing
- Slack and Teams exports already support incremental sync via workspace `state.json` files keyed by `last_ts` / `last_dt`
- This implies the assistant needs two distinct layers:
  - A **durable preference/profile layer** for stable patterns such as voice by channel, review preferences, and boundaries
  - A **fresh context layer** for new messages, recent meetings, open threads, and unresolved decisions
- The assistant should treat recency as a first-class signal, especially for reply drafting and triage
- Overlapping evidence across meetings, Slack, and Teams means retrieval needs deduplication and source-aware ranking rather than naive global search
- Constantly updating sources also imply explicit freshness and provenance in outputs: what was pulled from which thread/meeting and how recent it is
- The assistant should not "watch everything" equally in v1; attention should be scoped to direct mentions and DMs first

## Source classification for the next pass

### Voice/profile evidence

- Your authored Slack and Teams messages
- Your spoken turns from meeting transcripts
- Best suited for deriving channel-specific voice preferences, workflow defaults, negative preferences, and challenge/dissent preferences
- Operational readiness: Slack and Teams raw exports already expose author identity, and meeting transcripts already have speaker-level segmentation; `speakers.json` includes named speaker anchors such as `Stan`, `Tom`, `Bilgue`, and `Esan`

### Workflow/evaluation evidence

- Meeting transcripts paired with polished summaries and reasoning traces
- Slack and Teams threads where decisions, clarifications, and follow-ups are visible
- Best suited for measuring summary faithfulness, action extraction quality, and follow-up usefulness
- Also suited for coaching eval once the target rubric is fixed

### Context/retrieval evidence

- Full Slack and Teams thread history
- Downloaded Slack image attachments in the Sierra workspace
- Best suited for meeting prep, retrieval, continuity, and project-context support

### Data to treat carefully

- Mixed-author threads should not be used as direct proxies for your voice without author filtering
- Meeting transcripts need speaker attribution and `Stan`-only extraction before profile inference
- Bot/system messages are useful for context and workflow reconstruction, not for user modeling
- Sierra Slack may need a one-time mapping pass for your user IDs where `users.json` is incomplete

## Implications for the next research question

### Minimum viable explicit profile

- Derive it from observed behavior, not personality tests
- Likely high-yield fields: per-channel voice preferences, review/dissent preference, workflow defaults, approval boundaries, and negative preferences

### Evaluation rubric

- Edit burden
- Voice fit by channel
- Summary faithfulness
- Task/decision extraction precision
- Boundary compliance
- Non-sycophancy / challenge quality
- Retrieval usefulness for reply drafting
- Recency correctness and source grounding
- For communication coaching, the parallel rubric should be uncertainty reduction, response friction, composure, warmth-competence balance, communication altitude, constraint framing, and participation calibration

### Dissent policy

- Needs explicit testing on real work artifacts, especially drafts, summaries, and ambiguous decisions
- Should optimize for calibrated trust rather than agreement or warmth

## First concrete assistant job: direct-message and mention drafting

- Trigger condition: Slack DMs, Teams chats directed at you, and explicit @mentions in shared channels
- Expected behavior:
  - detect the incoming message
  - retrieve the most relevant context from the current thread, adjacent Slack/Teams conversations, and recent meetings
  - propose a concise draft reply in the right channel-specific voice
  - show the supporting context it used
  - require your approval before anything is sent
- This use case fits the current research well:
  - it is augmentation, not autonomy
  - it uses channel-conditioned voice rather than a single global persona
  - it benefits directly from calibrated retrieval over overlapping sources
  - it creates measurable outputs for profile and rubric design

### What this implies for assistant design

- The assistant needs an **attention policy**, not just a retrieval system
- It should prioritize direct asks over ambient channel noise
- It should distinguish between:
  - messages needing immediate response
  - messages needing research before response
  - messages needing no response
- For research-backed draft replies, the retrieval order should likely be:
  - current thread and recent messages from the sender
  - related Slack/Teams discussions on the same project
  - recent meeting transcripts and summaries
  - only then broader historical context
- Drafts should cite why they were generated: direct question, blocker, follow-up request, status ask, or coordination request
- The drafting surface should expose uncertainty and let you inspect the evidence used

## Planned next steps

1. Build an authored-only corpus from Slack, Teams, and meeting transcripts.
2. Build a small inbox-style gold set of direct mentions, DMs, and reply-worthy coordination messages.
3. For each item, attach the real supporting context from thread history, overlapping Slack/Teams threads, and recent meetings.
4. Evaluate draft replies on edit burden, voice fit, retrieval usefulness, recency correctness, and non-sycophantic judgment.
5. Build a separate small coaching eval set of authored messages and score them against the quiet-confidence rubric.
6. Use those results to draft a v1 explicit profile spec, attention policy, and dissent policy for reply drafting, plus a separate v1 instruction block for communication coaching.

## Scope

- **In:** Design patterns, behavioral science foundations, use case prioritization, evaluation design, profile design, source inventory
- **Out:** Multi-user patterns, implementation stack, persistent memory architecture in v1, autonomous actions without approval
