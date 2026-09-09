# Workspace diffs, conflicts, and release targets

Read this only when a workspace diff or merge reports a conflict or an
object that is not yours. It extends the post-merge flow in
[lifecycle](lifecycle.md), which controls authorization and verification.
For an authorized GraphQL operation, read [release API](release-api.md)
for the endpoint, the authentication prerequisites, and the schema checks.
For reconciling materialized no-code files, read [ghostwriter](../session/ghostwriter.md).

## Two diffs

One diff cannot separate drift from ride-along, and the remedies are
opposite.

- Diff against the live release version: what the release will carry.
  Anything not yours is a ride-along and needs a shipping decision.
- Diff against the workspace base: what you changed. Anything unexpected
  is drift. Reconcile it.

If your fork base equals the live version, there is no ride-along.
Cross-check `changes` against `changeSummary` on the same arguments. When
they agree with each other, trust them over the release description,
which is generated prose and not evidence of content or absence. When
they disagree with each other, chase it. Hand-diffing exported objects
means you skipped this step, and a stale local copy manufactures phantom
drift: query the workspace version.

## Conflicts

An `UNRESOLVED` conflict blocks the merge. `UPDATED_UPDATED` does not
prove divergence: when `conflictTheirsID` equals the base version, only
bookkeeping moved. Before accepting your side of a code object, prove
yours contains theirs with
`git merge-base --is-ancestor <their-build-commit> <your-build-commit>`.
On false, stop: you would discard their work.

Resolve per object, passing the theirs ID as `upToObjectVersionID`. Your
own ID silently leaves the object conflicted and the merge fails later.
Prefer per-object resolution over `overrideConflicts: true`, which skips
the merge checks.

## Ride-alongs

Block first, characterize while blocked, and hold until the owner
decides. Characterizing makes the block short. It does not replace it.
Give the owner the kind of change (authored edit or mechanical refresh),
the blast radius, who owns the content, and the cost of holding. Only the
owner's decision clears it. Interpreting an
instruction the owner already gave is yours. Verify a relayed ruling at
the source. For a code ride-along, report any SDK version bump and claim
behavior-free only after diffing. If the live build's commit is
unfetchable, say so instead of asserting safety.

## Release targets

Check each target's release history before choosing. A target absent
from recent releases, on a stale version, or built from a personal
branch is someone's working environment: leave it out. Match the
agent's established cadence instead of inventing a soak window. The
platform prefixes the release name with the version number, so leave
it out of your description.
