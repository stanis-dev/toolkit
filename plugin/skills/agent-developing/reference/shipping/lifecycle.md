# Shipping

Use this procedure for implementation work, not for an assessment or a delegated review. Keep the distinction between an open PR, a main-workspace snapshot, and a release to a target: they are three outcomes.

Before judging readiness, read [testing](../gates/testing.md) and [correctness review](../gates/verification.md). Before a code upload or a workspace deletion, read [workspace CLI](../session/workspace-cli.md). Before a no-code operation, read [ghostwriter](../session/ghostwriter.md). Before assigning another session a slice or a blocked step, read [handoff](../writing/handoff.md).

## Cleanup and checks

After both gates pass, inspect the changed footprint for unnecessary code. Simplify only when it improves the requested change, and keep unrelated cleanup separate. Touch the code half only: leave block rules, journey goals, `custom` blocks, `response_phrasing`, tool descriptions, and knowledge alone, and report any prompt cleanup you notice for the user to decide.

Guard each simplification with the plain unit tests, run before and after. Test success does not prove behavioral equivalence. Any later behavior-affecting edit invalidates the affected review and simulation results; reclear them before declaring the final artifact ready.

Read the current agent-check warnings with `get_agent_checks_warnings`; it also reports whether checks are still pending. Resolve warnings your change caused. Silence with `update_agent_checks_warning_status` only a warning you own and accept, with a reason. Record pre-existing warnings you do not own in the PR body and leave them active.

## Pull requests

Read [PR descriptions](pr-descriptions.md) for the title and body. Before creating a PR, check the current branch and search for an existing PR covering the same workstream. Reuse a match, and change its title or description only when asked or when the workflow requires it. Return the PR link and separate completed checks from outstanding ones. A test-only PR still follows the repository's protections and merge authorization.

## Scope and ownership

Keep a behavioral fix and the tests establishing it reviewable together. Split independent work when a single PR becomes hard to review. Prefer disjoint slices that each branch from and target main. Stack only when a slice cannot build or be reviewed without its parent, as with a prefactor plus its behavior change.

When separate sessions are authorized, give each slice one owner, explicit write boundaries, and its own completion criterion. One owner controls no-code writes to the thread workspace. The coordinator owns the combined verification and the post-merge tail.

## Post-merge snapshot

Merging the agent-repo PR does not ship the change. The change ships as a snapshot committed to the main workspace in Agent Studio, the analog of git's main branch.

1. Preserve local work, then check out and pull the merged main. Main can contain other merges since the branch was cut, and the snapshot must reflect all of it. Compare it with the tested revision, identify changed assumptions or paths, and reverify the affected ones.
2. Upload the merged main to the thread workspace, both halves: ghostwriter for the no-code half, `pnpm sierra upload` for the code half. Do not run a watcher on main. Confirm the upload picked up no stray uncommitted files.
3. If the upload regenerates tracked artifacts that differ from main, land them through the normal PR workflow, then repeat from step 1. A clean snapshot requires the upload to match main exactly.
4. Compare the thread workspace with its base. Confirm it carries only your objects and no unresolved conflicts. Read [conflicts](conflicts.md) when either check fails.
5. Create the snapshot with `mergeWorkspaceIntoMain`, merge-check override omitted, through [release API](release-api.md). Give it a substantive description: it becomes the release name. Verify the resulting workspace version and build identity with a fresh read.

Create the snapshot once the PR merges, without an extra prompt, when the user asked for the implementation to ship. Hold the release until the user asks.

## Release

Release only on a user request, and only to the targets the user names. A request with no named targets means the non-production targets. Include production only when the user names it or says all. Leave personal `dev:*` targets unchanged. The production Default target's name is the empty string; never read that as a harmless omitted target.

A release carries every change between the live snapshot and the new one, not only yours. Before asking for confirmation, compare each target's current version with the intended snapshot, report what else would ride along, and confirm the snapshot's build commit contains your merge commit and is clean. Then release one target per `workspaceReleaseCreate` call.

Treat a reported release as shipped only after a fresh read of the bot's release targets shows the build commit contains your merge commit. The mutation response is not evidence, the index can lag hours, and non-default targets can miss the default query. Then query the released code and no-code bundles: confirm the change behaves as intended and the bundles carry no unintended changes and no duplicated records or blocks. Confirm the targets you did not release to are unchanged.

Read [monitoring](monitoring.md) and arrange its first checkpoint. Annotate the release on affected reports, restart experiment windows at the boundary, and record any pre-release trend up front.

## Cleanup and waiting

Delete only a thread workspace this session created, with `pnpm sierra delete-workspace`, after the PR merged and the snapshot was verified. Deleting earlier destroys state the snapshot process or a reviewer can still need. A reused workspace needs its owner's cleanup decision. Snapshot creation, not release, unlocks cleanup. The Studio release flow sometimes removes the workspace on its own; confirmed server-side absence is completion, not an error.

If a PR closes without merging, preserve the unmerged workspace changes unless the user authorizes their disposal.

Merge and snapshot can land days after the session's active work. Use existing monitoring for the events it covers. For an uncovered post-merge or release check, use a scheduled wakeup when the client supports one, and otherwise state the outstanding action and its resume condition. Do not create an indefinite loop because a future release is possible.
