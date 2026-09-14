---
name: sierra
description: Critical guidance for Sierra agent development. Must always be loaded when working with Sierra agents.
---
# Sierra Agent Development Guidance

Sierra Agents are developed with a custom SDK based on React, with components rendering agent context instead of UI. The
final context is compiled from the combination of the following items and all of them must be tracked to avoid having
only partial understanding of agent context:

- Studio Journey definition: synced to `.composer/` by `pnpm sierra ghostwriter pull`
- Studio Configuration
- Knowledge Base
- Codebase context. Changes require `pnpm sierra upload/watch` to take effect.

You will use these tools for development process. All must be available and accessible. If any of these are not fully
functional - stop immediately and inform the user:

- sierra mcp
- sierra cli

- Fetching anything, an issue, a conversation, a simulation run or Studio content, follows
[tooling.md](./references/tooling.md).
- If i write "www" (where were we?) - it means I lost context and don't quite remember where we left off. Give me a tldr snapshot - short and sweet.
- If you are running simulations, let me know explicitly if those come back with fails that are unrelated to what we're working on.

## Non Negotiables

- All Studio context edits require my approval.
- All agent edits must observe [agent design](./references/agent/agent-design.md) practices. Add document emoji to all drafts where you explicitly observed it.
- Anything written for BBVA, an issue comment, a notas item, release notes, follows
  [comms.md](./references/comms.md); read it before drafting. Posting requires my approval.
- If you discover edits between your turns, those are my edits and are not to be reverted without my consent.
- Before editing ghostwriter blocks, always sync first.
- Before presenting an issue, context, simulation, or proposed edit, read
  [info.md](./references/info.md). It goes on the issue's card, in the section's template
  structure, nothing else.

## My workflow

When working on issues I have 1 agent be the overseer, and spawn separate agents for each issue which
execute the workflow below.

- Overseer creates and maintains the gh branch for current batch, keeps it aligned with main and maintains PR description.
- Overseer spawns the issue agents with `python3 <base>/scripts/lanes.py --repo <checkout> --branch <batch branch> <issue numbers…>`: one worktree `<prefix>-<n>` off the batch branch per issue, its Studio workspace from the post-checkout hook, and one pinned desktop session opened with `/sierra start work on … #<n>` at the model, effort and permission mode the flags name. It drives the desktop app through Orca computer-use, so the app must stay in front and untouched while it runs, about 25 seconds per issue. Titles come out app-generated; rename each to `OPP #<n>` with `set_session_title` from the JSON lines it prints.
- Issue agents iterate on their workflow untill their solution is ready. Once I confirm that we're done with the issue, they commit and push their changes to the draft PR for the current branch and migrate studio changes to the default workspace. Then notify the overseer.
- All agents maintain their worktrees and workspaces synced with the draft PR and default workspace.
- Once I declare to Overseer that the batch is ready, it performs regression test and present the results in browser.
- When PR is set "ready for review", Overseer must re-fetch issue cache and cleanup cards of all completed items.

### Issue Workflow

1. (If issue) Analyse the issue. (read [issues.md](./references/issues.md))
2. Decide on sim strategy (read [sim-strategy.md](./references/sims/sim-strategy.md))
3. Ensure there's a sim/s I can trust (read [sim-design.md](./references/sims/sim-design.md))
4. Understand what changes are needed for the agent (read [agent-design.md](./references/agent/agent-design.md))
5. Implement and verify (read [agent-design.md](./references/agent/agent-design.md))
6. Draft a PR (read [pr.md](./references/pr.md))
7. Draft communications (read [comms.md](./references/comms.md))



## My preferences

- Refer to Studio block by their display name and type.
