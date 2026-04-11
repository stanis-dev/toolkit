---

## name: work-radar

description: >-
  Answer targeted operational-awareness questions from Slack, Teams, and meeting notes. Use for
  "find my to-dos for today", "am I behind on something?", or "look at my chat with X" when the
  user explicitly asks. Not for general chat, drafting replies, or communication coaching.

# Work Radar

Explicit operational-awareness lookup.

## Operating Principle

This skill is **not** a background memory system.
It is a manual tool for targeted questions over work signals.

Use it when the user explicitly asks things like:

- "find my to-dos for today"
- "am I behind on something?"
- "what's up today?"
- "look at my chat with Seb"
- "what did Tom ask me recently?"

Do not activate it for general conversation.
Do not use it for drafting replies.
Do not use it for communication coaching.

## Constraints

- Only use when the user explicitly asks an operational-awareness question.
- Do not inject or summarize the full Slack / Teams / meeting corpus unless the user explicitly asks.
- Default to the smallest relevant context slice.
- Prefer recent, high-signal sources over broad historical search.
- Always distinguish between:
  - explicit asks
  - likely commitments
  - inferred follow-ups
- If confidence is low, say so plainly instead of pretending certainty.
- Do not draft replies unless the user explicitly asks for one.
- Do not evaluate communication style; that belongs to `communication-copilot`.
- Do not answer broad "what am I behind on?" questions from a single thread if the wider source set has not been checked.

## Workflow

### 1. Classify the Question

Identify which type of question this is:

- **today / status** — `what's up today?`, `find my to-dos for today`
- **behind / stale** — `am I behind on something?`, `what follow-ups are stale?`
- **thread-specific** — `look at my chat with Seb`
- **person-specific** — `what did Tom ask me recently?`
- **project-specific** — `what's pending on Pronet?`

Done when:

- the query type is explicit

### 2. Scope the Search

Default scope rules:

- For **thread-specific** questions:
  - search only the named thread / DM / channel first
- For **person-specific** questions:
  - search the recent messages involving that person
- For **today / status** and **behind / stale** questions:
  - search recent high-signal sources only first
  - recent Slack DMs / direct mentions
  - recent Teams chats / meeting threads
  - recent meeting summaries

Only widen scope if the first pass is insufficient.

Done when:

- the minimum viable source set is selected

### 3. Extract Operational Signals

Look for:

- tasks assigned to the user
- tasks the user volunteered for
- blockers the user raised
- waiting items
- unanswered asks
- follow-ups lacking closure
- meetings with explicit action items

Prefer explicit signals like:

- "I will"
- "I'll"
- "can you"
- "please"
- "follow up"
- "ready for review"
- "will release"
- "waiting on"
- "blocked on"

Done when:

- candidate operational items are extracted

### 4. Rank and Filter

Rank higher if the item is:

- recent
- clearly assigned to the user
- still open or unresolved
- blocking other work
- tied to a named person, thread, or project

Rank lower if it is:

- old and clearly resolved
- ambient discussion without ownership
- only weakly inferred from context

If you found task-like items and cannot determine their status from chat/meeting data alone, note them as "unverified — may be resolved in PRs or commits." If the user asks for verification, or if more than half of the items have unclear status, check:

- `gh pr list --repo sierra-agents/sky --state all --search "KEYWORD"`
- `gh pr list --repo sierra-agents/pronet --state all --search "KEYWORD"`

Done when:

- only the most relevant items remain, each with a clear status or an "unverified" tag

### 5. Return a Compact Answer

Default output:

```md
Answer: {one-line summary}

What looks active:
- {item}
- {item}

What may need follow-up:
- {item}

Sources checked:
- {file / thread / summary}

Confidence:
- {high / medium / low}
```

For thread-specific questions, use:

```md
Thread summary:
- {what the thread is about}
- {what is still open}
- {what you likely need to do next}

Sources checked:
- {thread path}

Confidence:
- {high / medium / low}
```

Done when:

- the user can immediately act on the answer

## GOOD / BAD

### GOOD — Narrow Thread Review

User:
`look at my chat with Seb`

Assistant behavior:

- finds the Seb thread
- reads the recent slice
- answers what is open, what is waiting, and what the next likely action is

Reasoning:

- targeted
- low-noise
- useful immediately

### BAD — Full Corpus Dump

User:
`look at my chat with Seb`

Assistant behavior:

- scans all Slack, Teams, and meetings
- returns a giant mixed summary of everything

Reasoning:

- high-noise
- unnecessary context pollution
- fails the actual ask

### GOOD — Honest Uncertainty

`I found two likely open follow-ups, but only one is explicit. The second is inferred from the thread and may already be resolved elsewhere.`

Reasoning:

- distinguishes fact from inference
- keeps trust high

### BAD — Fake Certainty

`You are definitely behind on X, Y, and Z`

when the source evidence is weak.

Reasoning:

- overstates confidence
- creates false operational pressure

## Anti-Patterns


| Temptation                                    | Reality                                                           |
| --------------------------------------------- | ----------------------------------------------------------------- |
| Search everything immediately                 | Broad corpus search creates noise and slows simple questions down |
| Treat any mention as a task                   | Not every message is an actionable commitment                     |
| Answer "behind on something?" from one thread | This requires at least a small cross-source check                 |
| Blend facts and inferences together           | The user needs to know what is explicit vs guessed                |
| Turn this into a reply-drafting skill         | Drafting belongs elsewhere                                        |
| Dump raw chat excerpts                        | The value is operational synthesis, not transcript spillage       |


## Interaction Rules

- If the user explicitly names a person, thread, or project, scope tightly to that first.
- If the user asks a broad operational question, start with recent high-signal sources only.
- If the evidence is mixed, say `likely`, `appears`, or `may`.
- If the user wants raw thread detail after the summary, provide it.
- If the user wants a reply draft after the operational answer, switch to `communication-copilot` behavior only if explicitly asked.

## Optional Deeper Grounding

Only use these when needed:

- `../../journal/research/personal-assistant/context/operational-awareness-integration.md`
- `../../journal/research/personal-assistant/research.md`

## Sources

All paths under `brain/data` (relative to the toolkit repo root).

- **Slack:** `slack/{workspace}/readable/*.md` — DMs start with `# DM: Person Name`, channels with `# #channel-name`. Two workspaces: `sierra-ai`, `wizeline`. To find a person's DM: `grep -rl "DM: Seb" slack/*/readable/`
- **Teams:** `teams/sierra/readable/*.md` — descriptive filenames like `Pronet___Sierra_Standup.md`
- **Meetings:** `rec-DATE-TITLE.summary.md` at the data root
- **Todo:** `assistant-todo.md` at the data root

Always search `readable/` first. Only fall back to raw JSON (`channels/*.json`) if you need reaction metadata or data not in the rendered markdown.

Do not load all sources unless the question genuinely requires it.