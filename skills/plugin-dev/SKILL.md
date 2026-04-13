---

## name: plugin-dev
description: >-
  How to modify, extend, and propagate changes to Stan's personal toolkit plugin. Use when
  asked to add/edit/remove skills, agents, hooks, or any plugin configuration.

# Toolkit Plugin Development

Source: `~/code/toolkit` (git repo: `stanis-dev/toolkit`) Installed as: `toolkit@stan-marketplace` (user scope)

## Directory Layout

```
~/code/toolkit/
├── .claude-plugin/
│   ├── plugin.json            # Plugin identity and version
│   └── marketplace.json       # Single-plugin marketplace manifest
├── skills/<skill-name>/
│   ├── SKILL.md               # Instructions + frontmatter
│   └── (supporting files)     # Templates, scripts, references
├── agents/<agent-name>.md     # Subagent definitions with frontmatter
└── hooks/
    ├── hooks.json             # Hook event configuration
    └── session-start.sh       # Session orientation (lists all skills/agents)
```

## Critical: Keep session-start.sh in Sync

When adding or removing any skill or agent, update the `CONTEXT` string in `hooks/session-start.sh`. This is what tells
Claude about available skills at session start.

## Propagating Changes

After editing any file:

```bash
cd ~/code/toolkit

# 1. Bump version in BOTH files (must match):
#    .claude-plugin/plugin.json      -> "version": "X.Y.Z"
#    .claude-plugin/marketplace.json -> "version": "X.Y.Z"

# 2. Commit and push
git add -A && git commit -m "<describe change>" && git push

# 3. Update marketplace then plugin
claude plugin marketplace update stan-marketplace
claude plugin update toolkit@stan-marketplace
```

Version bump is required — Claude Code uses the version to detect updates. Without it, `claude plugin update` won't pull
changes.

Changes take effect on next session. Mid-session reload is unreliable (`/reload-plugins` has known bugs with skills).

## Rapid Iteration (No Commit)

For testing changes without committing:

```bash
claude --plugin-dir ~/code/toolkit
```

Loads plugin directly from disk. Edits take effect on next `--plugin-dir` session (not mid-session).