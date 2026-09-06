---
name: sierra
description: Critical guidance for Sierra agent development. Must always be loaded when working with Sierra agents.
---
# Sierra Agent Development Guidance

Sierra Agents are developed with a custom SDK based on React, with components rendering agent context instead of UI. The
final context is compiled from the combination of the following items and all of them must be tracked to avoid having
only partial understanding of agent context:

- Studio Journey definition: synced to `.composer/` by `pnpm sierra ghostwriter --sync`
- Studio Configuration
- Knowledge Base
- Codebase context. Changes require `pnpm sierra upload/watch` to take effect.

You will use these tools for development process. All must be available and accessible. If any of these are not fully
functional - stop immediately and inform the user:

- sierra mcp
- sierra cli

## My workflow

1. (If issue) Understand what has to be done (read [issues.md](./references/issues.md))
2. Decide on sim strategy (read [sim-strategy.md](./references/sims/sim-strategy.md))
3. Ensure there's a sim/s I can trust (read [sim-design.md](./references/sims/sim-design.md))
4. Understand what changes are needed for the agent (read [agent-design.md](./references/agent/agent-design.md))
5. Implement and verify (read [agent-design.md](./references/agent/agent-design.md))
6. Draft a PR (read [pr.md](./references/pr.md))
7. Draft reporting (read [reporting.md](./references/reporting.md))



## My preferences

- Refer to Studio block by their display name and type to help me follow.

