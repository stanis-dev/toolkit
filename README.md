# toolkit

Personal toolkit — AI agent skills, research, and tools for day-to-day workflows.

## Structure

```
skills/          # SKILL.md files loadable by Claude Code / Cursor agents
agents/          # Subagent definitions (read-only, scoped roles)
hooks/           # Session lifecycle hooks (e.g. inject context on start)
context/         # Global context injected into every session via hook
journal/         # Personal notes, journaling, and long-running deep research
knowledge-wiki/  # Review-gated canonical knowledge system for durable personal knowledge
brain/           # Meeting recorder, transcriber, and data export pipeline (macOS app)
.claude-plugin/  # Plugin manifest for Claude Code marketplace
```

## Skills

**Sierra workflows** — agent development on the Sierra platform:

| Skill                   | Purpose                                          |
| ----------------------- | ------------------------------------------------ |
| `sierra-powertool`      | Full `sierras` CLI reference                     |
| `sierra-best-practices` | Dev guidelines, debug workflows                  |
| `sierra-bootstrap`      | Kickstart issue work (branch, workspace, sims)   |
| `sierra-triage`         | Classify Agent Studio issues                     |
| `sierra-phrasing-eval`  | Manual phrasing evaluation workflow              |
| `sierra-wrap-up-issue`  | Generate report, PR, docs for completed work     |
| `deep-eval`             | Thoroughness override for deep evaluation passes |

**Personal tools:**

| Skill                      | Purpose                                            |
| -------------------------- | -------------------------------------------------- |
| `deep-research-prompt`     | Generate context-enriched research prompts         |
| `question-crystallization` | Move from vague intuitions to clear questions      |
| `communication-copilot`    | Tighten pasted drafts with compact coaching + rewrite |
| `reply-drafter`            | Draft grounded replies for DMs, mentions, and direct asks |
| `personal-assistant`       | Route awareness, coaching, and reply-drafting requests |
| `work-radar`               | Answer targeted "what's up / am I behind / look at this thread" questions |
| `wiki-editorial`           | Propose, publish, and lint gated knowledge-wiki updates |
| `wiki-smoke`               | Run the subagent-based smoke battery for `wiki-editorial` |
| `music-discovery`          | Recommendations via Plex history + SoulSync        |
| `homelab-ssh`              | Homelab server reference (SSH, Docker, storage)    |
| `mini-ssh`                 | Mac Mini / Plex server reference                   |
| `cursor-chat-history`      | Find and reconstruct Cursor agent chat histories   |
| `plugin-dev`               | How to modify and propagate changes to this plugin |

## Agents

- **phrasing-eval** — evaluates Turkish call-center agent transcripts against phrasing guardrails
- **replay-analyzer** — evidence-based reviewer of Sierra simulation replays
- **wiki-smoke-worker** — isolated scenario executor for the knowledge-wiki smoke battery

## Setup

Install as a Claude Code plugin:

```sh
claude plugin add /path/to/toolkit
```

On session start, the hook in `hooks/session-start.sh` injects `context/global.md` and a summary of all available skills into context.

## Brain

`brain/` is a personal macOS app for recording meetings, transcribing them with speaker attribution (Whisper Large-v3 on Apple Silicon), and exporting Slack/Teams chat history. It produces the data that skills like `work-radar` and `personal-assistant` consume.

```
brain/src/         # Swift source — recording, playback, meeting detection, assistant UI
brain/scripts/     # Python — transcription, Slack export, Teams export, polishing
brain/resources/   # Info.plist, AppIcon.icns, entitlements
brain/data/        # gitignored — recordings, transcripts, Slack/Teams exports
brain/models/      # gitignored — Whisper GGML model (~3GB)
```

Build and install: `cd brain && ./build.sh`

## Knowledge Wiki

`knowledge-wiki/` is a separate editorial system inside this repo. It is not the same thing as `journal/`.

- `journal/` remains a scratch/research workspace.
- `knowledge-wiki/` stores only review-approved durable knowledge.
- Canonical content is retrieved on demand and is never injected wholesale at startup.
