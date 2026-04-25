---
name: sierra
description: Guidance for Sierra agent development
---

# Sierra Agent Development Guidance

Sierra Agents are developed with a custom SDK based on React, with components rendering agent context instead of UI.

User will interact most frequently with:

- Studio Journey definition
- Studio Configuration
- Simulations
- Codebase context - interacts with Studio. Changes require `pnpm sierra upload/watch` to take effect.

At the beginning of each session check that `Sierra` MCP is available and functional, comprehend its tools. If
unavailable, stop immediately and notify user.

## Constraints

- **Sierra SDK is private.** You must ground your understanding with:
    - use `sierra` mcp tool: `ask_sierra_assistant`
    - sdk source files in `node_modules`

## Development Flow

### In all cases

- Always keep Studio context synced.

### New Feature

1. Create a failing simulation for the feature first.

### Bug Fix

1. Check whether there's an existing simulation that covers the failing behaviour.
    - if exists: check sim quality
    - if not: create one
