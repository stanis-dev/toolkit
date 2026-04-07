# Operational Awareness Integration

## Purpose

Define how the personal assistant should support:

- morning briefs
- "what's up today?"
- "am I behind on something?"
- "what are my to-dos?"
- quick questions like "take a look at my chat with Seb"

using Slack, Teams, and meeting transcripts **without** polluting the assistant with raw context by default.

## Core idea

The assistant should not carry the full message corpus in working memory all the time.

Instead, it should operate through **two layers**:

1. **Raw source layer**
- Slack exports
- Teams exports
- meeting transcripts / summaries

2. **Derived operational layer**
- commitments
- blockers
- follow-ups
- unanswered asks
- recent important threads

The assistant should be aware of the source roots, but daily use should primarily query the **derived layer** and only fall back to raw retrieval when needed.

## Why this matters

If the assistant always loads raw Slack / Teams / meetings:

- context gets noisy fast
- stale material competes with fresh material
- "what matters today?" becomes hard to answer
- simple questions become expensive retrieval problems

If the assistant only uses a derived operational layer:

- morning brief stays compact
- "behind on something?" becomes tractable
- to-dos and follow-ups become queryable
- raw context is still available for drill-down

## Third concrete assistant job

### Operational awareness

The assistant should maintain an operational view of:

- tasks you said you would do
- tasks others asked you to do
- blockers you raised
- follow-ups you are waiting on
- threads that still need response or closure
- meetings that produced actionable commitments

This is a different job from:

- reply drafting
- communication coaching

It is closer to a lightweight chief-of-staff / commitments tracker for your personal work.

## Recommended system boundary

### What belongs in scope

- Slack messages where you are:
  - directly tagged
  - in a DM
  - the apparent owner of a follow-up

- Teams chats / meeting threads where:
  - you are asked for something
  - you commit to something
  - a blocker or dependency is named

- Meeting summaries / transcripts where:
  - there are explicit action items
  - you are assigned work
  - you volunteer to do something
  - there is an unresolved dependency that affects you

### What should stay mostly out of scope

- ambient channel noise
- historical messages with no open action
- broad conversational memory with no operational value
- everything that is merely interesting but not action-relevant

## Derived artifacts the assistant likely needs

### 1. Commitments ledger

A structured list of:

- `item`
- `type`: todo / follow-up / blocker / waiting / decision
- `owner`
- `source`
- `source_path`
- `source_time`
- `project`
- `status`: open / waiting / done / stale / unclear
- `due_hint`: today / this week / none / explicit date
- `confidence`

This becomes the default source for:

- "find my to-dos for today"
- "am I behind on anything?"
- "what am I waiting on?"

### 2. Recent thread index

A lightweight index of high-signal threads:

- participant
- channel
- project
- last activity
- whether there is an unanswered ask
- whether there is an open action

This becomes the routing layer for:

- "take a look at my chat with Seb"
- "what did Tom ask me recently?"

### 3. Morning brief artifact

A compact generated summary for the day:

- today's likely priorities
- open commitments
- waiting items
- likely messages needing response
- recent meetings that changed the picture

This should be derived from the commitments ledger + recent thread index, not from the raw corpus directly.

## Query patterns

### Pattern A: broad morning question

Example:
- "what's up today?"
- "find my to-dos for today"
- "am I behind on something?"

Behavior:

- query the commitments ledger first
- rank by recency + ownership + explicitness + risk
- pull in raw context only for the top few uncertain items

### Pattern B: thread-specific question

Example:
- "take a look at my chat with Seb"
- "what did Daniel ask me?"

Behavior:

- use the recent thread index to find the right thread
- read the recent slice of the raw thread
- answer from that slice
- if relevant, connect to the commitments ledger

### Pattern C: status / drift question

Example:
- "did I drop anything?"
- "what follow-ups are stale?"

Behavior:

- compare open commitments against recent source activity
- surface items where:
  - you committed but there is no closing signal
  - someone asked you something and there is no reply
  - a blocker is still unresolved

## Anti-pollution rules

- Do not inject whole Slack / Teams histories into the assistant by default.
- Do not treat every message as a memory candidate.
- Default to derived state, not raw state.
- Raw retrieval should be targeted by:
  - participant
  - thread
  - project
  - recent time window
- Prefer "open commitments" over "interesting historical context."

## Practical architecture recommendation

### Best near-term approach

Keep the existing source roots:

- `/Users/stan/code/rec/data/slack`
- `/Users/stan/code/rec/data/teams`
- `/Users/stan/code/rec/data/rec-*`

But add a new derived artifact, likely under the personal-assistant research or a future app-specific data path:

- `commitments.jsonl` or `commitments.md`
- `recent-threads.json`
- `morning-brief.md`

The personal assistant should answer daily awareness questions from those first.

### Avoid for now

- full autonomous background reading of all corpora on every turn
- implicit "memory graph" behavior
- trying to answer daily-awareness questions from raw retrieval only

## Immediate steps

1. Define the commitments ledger schema.
2. Build a tiny gold set of real commitment examples from Slack / Teams / meetings.
3. Test whether those examples can be normalized into the ledger reliably.
4. Once that works, define the morning-brief output.
5. Only then decide whether this should become a skill, an automation, or an app-level feature.

## Working hypothesis

The personal assistant should gain operational awareness through **derived artifacts**, not through omniscient raw-memory behavior.

That keeps the system:

- personal in scope
- useful in day-to-day work
- resistant to context pollution
- compatible with "brief question" interactions like:
  - "what's up today?"
  - "am I behind on anything?"
  - "look at my chat with Seb"
