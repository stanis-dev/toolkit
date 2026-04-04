---
name: sierra-best-practices
description:
  Rules, best practices, and guidelines for Sierra agent development. Must be used for any Sierra agent work including
  journey development, simulation creation, workspace operations, and code review.
---

# Sierra Agent Development Guidelines

Must apply whenever working on Sierra Agent

## Sierra Documentation

For documentation reference and routing, always read [docs-routing.md](references/docs-routing.md) first.

## Debug Guidelines

- Sometimes when working with a feature workspace the `pnpm sierra watch` will not be running against target workspace.
  You can upload the code manually by using official sierra cli to complete the task at hand, but after finishing remind
  user to start the `watch` command to ensure change sync.

## Feature spec-based development

- All feature specs are located in `./context-docs/specs` with files named after the linear ticket id

## Workspace Discipline

- **Always use feature workspaces** for all workspace operations unless explicitly instructed otherwise. Prefer
  workspace-name flag for idiomatic invocations
- **Never use default workspace** for active development - it represents the baseline for comparison, simulation
  regression evaluation, and reference
- Fetch workspace diffs exclusively via `sierras` CLI tool

## Simulations

For simulation design and evaluation guidelines, read [simulations.md](references/simulations.md).

