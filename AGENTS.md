# Toolkit Repo Instructions

- If you edit any `skills/*/SKILL.md` or `agents/*.md`, run `python3 scripts/validate_skills.py` before finishing.
- Treat validator failures as blocking. Fix the file instead of leaving broken frontmatter for a later pass.
- When creating a new skill or agent, copy the frontmatter shape from a nearby valid file instead of improvising it.
- When adding or removing a skill or agent, update `hooks/session-start.sh` so startup context stays accurate.
