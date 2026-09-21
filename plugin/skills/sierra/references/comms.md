# Communications with BBVA

Everything BBVA reads. Nothing is posted without my go.

- Use neutral, ES Spanish. No em dashes. No opening question mark (¿). Quote with " not «».
- The reader is aware of the context. Say only what changed for them or what they need to act on.
- Issue numbers, simulation mentions and PRs are links
   - issues: `https://bbva.sierra.ai/agents/<agent-id>/issues/<number>`
- Drafts are plain text for easy copy/paste.

## Project conversations

### Google Chat

- [Voicebot - Openpay](/Users/stan/code/toolkit/brain/data/google-chat/sierra/readable/google_chat_AAQAkdY0pQg.md)
- [VoiceBot- Cobranza](/Users/stan/code/toolkit/brain/data/google-chat/sierra/readable/google_chat_AAQAZ0v2SzU.md)

### Slack · Sierra

- [#bbva-working-group](/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/slack_C0ABSRJ3VSN.md)
- [Juan Ruiz Pozuelo — DM](/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/slack_D0BFDVCHXEV.md)
- [Álvaro Rausell Guiard — DM](/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/slack_D0AUHRG4AG2.md)
- [Shynggys Kassen — DM](/Users/stan/code/toolkit/brain/data/slack/sierra-ai/readable/slack_D0BMGE8DH35.md)

## Clarification Questions

- Each ask starts with issue number if it's coming from one.
- Name SOP row by its opening words and the resultado it registers, with SOP version e.g. (v2.0-07/09)
- Short bullet point per item.

## Release notes

What a merge changed, for the reader who files the issues. Report only what is done: nothing
pending, partial, blocked or removed appears.

- One flat list under «Novedades de esta versión», no grouping. Every line leads with the
  issue number(s) linked to Studio, `https://bbva.sierra.ai/agents/<agent-id>/issues/<number>`,
  never to GitHub, then one sentence on what the agent now does.
- An issue fixed only by a guard simulation, with no behaviour change, gets no line; say so to
  me outside the note.
- An issue verified as a control rides the line of the issue it protects: «#370 confirma que …».
- Build the list from the merged PR's commits and body, confirm each number and title with
  `get_issue_details`, drop anything the PR body lists as a blocker or as removed.

**Novedades de esta versión**

- [#NNN](…/issues/NNN): <what the agent now does>.
- [#NNN](…/issues/NNN), [#MMM](…/issues/MMM): <one change that closes both>.
