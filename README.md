# toolkit

Personal Claude Code plugin — a collection of skills, agents, and hooks for day-to-day development workflows.

## Structure

```
skills/          # SKILL.md files loadable by Claude Code / Cursor agents
agents/          # Subagent definitions (read-only, scoped roles)
hooks/           # Session lifecycle hooks (e.g. inject context on start)
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
| `music-discovery`          | Recommendations via Plex history + SoulSync        |
| `homelab-ssh`              | Homelab server reference (SSH, Docker, storage)    |
| `mini-ssh`                 | Mac Mini / Plex server reference                   |
| `cursor-chat-history`      | Find and reconstruct Cursor agent chat histories   |
| `plugin-dev`               | How to modify and propagate changes to this plugin |

## Agents

- **phrasing-eval** — evaluates Turkish call-center agent transcripts against phrasing guardrails
- **replay-analyzer** — evidence-based reviewer of Sierra simulation replays

## Setup

Install as a Claude Code plugin:

```sh
claude plugin add /path/to/toolkit
```

On session start, the hook in `hooks/session-start.sh` injects a summary of all available skills into context.
