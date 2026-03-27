---
name: plugin-dev
description: How to modify, extend, and propagate changes to Stan's personal toolkit plugin. Use when asked to add/edit/remove skills, agents, hooks, or any plugin configuration.
---

# Toolkit Plugin Development

Source: `~/code/toolkit` (git repo: `stanis-dev/toolkit`)
Installed as: `toolkit@stan-marketplace` (user scope)

## Directory Layout

```
~/code/toolkit/
├── .claude-plugin/
│   ├── plugin.json            # Plugin identity and version
│   └── marketplace.json       # Single-plugin marketplace manifest
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md           # Required: instructions + frontmatter
│       └── (supporting files) # Optional: templates, scripts, references
├── agents/
│   └── <agent-name>.md        # Subagent definitions with frontmatter
├── hooks/
│   ├── hooks.json             # Hook event configuration
│   └── session-start.sh       # Session orientation script
└── .gitignore
```

## Modifying a Skill

Edit `~/code/toolkit/skills/<name>/SKILL.md` directly. Supporting files (templates, reference docs, scripts) live alongside SKILL.md in the same directory.

## Adding a New Skill

1. Create `~/code/toolkit/skills/<name>/SKILL.md` with required frontmatter:

```yaml
---
name: <kebab-case-name>
description: <when to use this skill -- Claude uses this for auto-invocation>
---
```

2. Add supporting files in the same directory if needed.
3. Update `~/code/toolkit/hooks/session-start.sh` -- add the new skill to the appropriate section in the CONTEXT string.

## Adding or Modifying an Agent

Agents live at `~/code/toolkit/agents/<name>.md`. Required frontmatter:

```yaml
---
name: <agent-name>
description: <what this agent does and when to invoke it>
model: <model-name or "inherit">
disallowedTools: <comma-separated tool names>
---
```

After adding a new agent, update `session-start.sh` to list it.

## Modifying Hooks

- Event config: `~/code/toolkit/hooks/hooks.json`
- Session start script: `~/code/toolkit/hooks/session-start.sh`

When adding or removing any skill or agent, always update the CONTEXT string in `session-start.sh` to keep the session orientation accurate.

## Propagating Changes

After editing any file in `~/code/toolkit/`:

```bash
cd ~/code/toolkit
# Bump version in both files (must match):
#   .claude-plugin/plugin.json      -> "version": "X.Y.Z"
#   .claude-plugin/marketplace.json -> "version": "X.Y.Z"
git add -A && git commit -m "<describe change>" && git push
claude plugin marketplace update stan-marketplace
claude plugin update toolkit@stan-marketplace
```

The marketplace update fetches the latest repo state; the plugin update then detects the version change and pulls it into the local cache.

Changes take effect on the next Claude Code session. Mid-session skill reload is not reliable (`/reload-plugins` has a known bug with skills).

For rapid iteration without committing, start a session with:
```bash
claude --plugin-dir ~/code/toolkit
```
This loads the plugin directly from disk. Edits take effect on the next `--plugin-dir` session (not mid-session).

## Version Bumping

Both `plugin.json` and `marketplace.json` declare the version. They must match. Claude Code uses the version to detect updates -- if you change files without bumping the version, `claude plugin update` won't pull the changes.

Use semver: bump patch for small changes, minor for new skills/agents, major for breaking changes.
