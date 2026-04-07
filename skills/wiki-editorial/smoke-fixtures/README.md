# Wiki Smoke Fixtures

Declarative smoke battery inputs for `wiki-editorial`.

## Layout

- `catalog.json` defines batches, scenarios, setup steps, commands, and assertions.
- `common/` stores shared external source files and reusable markdown snippets.
- `seeds/` stores prebuilt wiki roots for publish and full-lint scenarios.

## Conventions

- Seed directories are copied into an isolated temp wiki root before a scenario runs.
- Scenario `setup_steps` may further modify the temp workspace after the seed is copied.
- No scenario mutates the real `/Users/stan/code/toolkit/knowledge-wiki` tree.
- Proposal ids in seeded publish scenarios are fixed to `manual-proposal` to keep publish cases deterministic.
