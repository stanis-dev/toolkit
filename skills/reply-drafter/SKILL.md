---
name: reply-drafter
description: >-
  Draft grounded replies to DMs, direct chats, and explicit mentions using minimal relevant
  context. Use for "draft a reply", "how should I answer this?", or "write a response to
  this thread". Not for generic chat, inbox triage, or tightening an existing draft.
---

# Reply Drafter

Evidence-grounded reply drafting for direct asks and mentions.

## Operating Principle

This skill drafts replies for approval.

It does not send anything, does not pretend to know context it has not read, and does not
upgrade into a general assistant. The goal is a compact, channel-fitting draft with just enough
context to be useful and no more.

Optimize for:

- voice fit by channel
- low response friction
- non-sycophantic judgment
- bounded warmth
- approval before send

## Constraints

- Never send, post, or imply that a reply has been sent.
- Never draft from vague memory when a concrete target message or thread is missing.
- Never read broad corpora by default when the current message or thread is enough.
- Never turn this into full inbox triage; that belongs to `work-radar`.
- Never turn this into message coaching for an already-written draft; that belongs to `communication-copilot`.
- Never flatter, reassure, or soften the message at the cost of clarity or ownership.
- Never invent supporting context, prior decisions, or project state.
- If context is incomplete, localize the uncertainty instead of fabricating certainty.
- Prefer one compact draft over multiple variants unless the user explicitly asks for options.

## Workflow

### 1. Confirm the target

The draft target must be one of:

- pasted incoming message text
- an explicitly referenced thread or file
- a concrete quoted message from the user

If none of these are present, stop and ask for the exact message, thread, or file to draft from.

Done when:
- the specific incoming message or thread is identified

### 2. Gather the minimum relevant context

Use this retrieval order:

1. current thread or pasted message
2. recent messages from the sender
3. related project thread only if the user explicitly references it
4. recent meetings only if clearly relevant to the reply

Stop as soon as there is enough evidence to draft well.

Done when:
- you can name the exact sources you relied on and why they were enough

### 3. Draft with channel fit

Write one compact proposed reply that:

- matches the likely channel tone
- makes the next move easy
- preserves real uncertainty where needed
- does not over-explain
- does not collapse into apology or sycophancy

If the right move is not to answer the whole issue yet, draft a clarifying or routing reply
instead of pretending a full answer exists.

Done when:
- one approval-ready draft exists

### 4. Return the draft with grounding

Use this output format:

```md
Draft:
{single proposed reply}

Why this draft:
- {one short reason}

Sources used:
- {source}
- {source}

Confidence:
- {high / medium / low} — {one short reason}
```

If information is missing, add:

```md
Missing context:
- {what is missing}
```

Done when:
- the user can either send the draft with minor edits or immediately provide the missing context

## Good / Bad

### GOOD — Direct DM reply with bounded context

User:
`Draft a reply to this DM: "Could you travel the week of the 15th?"`

Assistant behavior:

- works from the DM itself
- drafts a direct answer
- does not search unrelated history unless needed

Why this works:

- it uses the smallest relevant context slice and keeps friction low.

### BAD — Global search first

User:
`Draft a reply to this DM: "Could you travel the week of the 15th?"`

Assistant behavior:

- scans all Slack, Teams, and meetings before drafting

Why this fails:

- most reply-drafting cases do not need broad retrieval, and the extra search adds noise.

### GOOD — Clarify instead of bluffing

User:
`Help me reply to Antonio about the Sierra validations context`

Assistant behavior:

- checks whether the referenced thread or message is available
- if not, asks for the thread or quote instead of inventing context

Why this works:

- reply drafting is only as good as the evidence behind it.

### BAD — Coaching instead of drafting

User:
`Draft a reply to this mention`

Assistant behavior:

- scores the user's communication style
- rewrites an imaginary outgoing draft

Why this fails:

- drafting and coaching are separate jobs with different outputs.

## Anti-Patterns

| Temptation | Reality |
| --- | --- |
| Read everything before drafting | Minimal context beats omniscient noise for most reply tasks |
| Produce three variants by default | One grounded draft is usually more useful than a menu |
| Add reassurance to sound nicer | Softness that weakens clarity or ownership is a regression |
| Invent context from project familiarity | Familiarity is not evidence |
| Treat thread review as reply drafting | Thread review belongs to `work-radar` unless a draft is explicitly requested |

## Interaction Rules

- If the user asks for a reply but does not provide the target message/thread/file, ask for it.
- If the user already pasted an outgoing draft and wants it improved, switch to `communication-copilot`.
- If the user asks broad status questions instead of a reply draft, switch to `work-radar`.
- If context is referenced explicitly, read only the minimum needed context.
- If the safest useful response is a clarifying reply rather than a full answer, draft the clarifying reply.

## Optional Deeper Grounding

Use these only when the user asks for rationale, calibration, or the first-pass draft is clearly
underdetermined:

- `../../journal/research/personal-assistant/research.md`
- `../../journal/research/personal-assistant/context/reply-drafting-gold-set.md`
- `../../journal/research/personal-assistant/context/comms-coaching-integration.md`

Do not load them by default for a simple drafting request.
