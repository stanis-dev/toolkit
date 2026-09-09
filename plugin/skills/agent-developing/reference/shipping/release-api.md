# Snapshot and release API

Read when creating a main-workspace snapshot or releasing it through GraphQL. [Lifecycle](lifecycle.md) controls the gates, the release authorization, the target scope, verification, cleanup, and monitoring. Before an authenticated call, read [API authentication](../session/api-auth.md).

Neither mutation has a `pnpm sierra` command today. Check `pnpm sierra --help` before assuming that is still true, and prefer a supported tool or CLI operation when one exists. If no authorized interface is available, hand the exact artifact and the remaining step to the user.

## Endpoint and schema

POST JSON with `query` and `variables` to `https://<subdomain>.sierra.ai/-/api/graphql`. The `/-/api` prefix is required: `/graphql` answers with a misleading `403 Missing CSRF`. Introspection is disabled and the schema files live in the unreachable monorepo. Ground each argument and response shape with `ask_sierra_assistant`, and treat validation errors as the schema oracle, one named field at a time. Never guess a mutation shape.

## Mutations

- `mergeWorkspaceIntoMain` creates the main-workspace snapshot. Omit the merge-check override. Its description becomes the release name, so put the substance there per [authoring](../writing/authoring.md), and verify the resulting snapshot identity and name with a fresh read.
- `workspaceReleaseCreate` releases one target per call. The production Default target's name is the empty string and serves live customer traffic; it is not an unspecified target. Omitting `scheduledGoliveTime` ships immediately. A server-generated summary replaces the description you pass, so inspect the resulting description.

The schema accepts either `workspaceVersionId` or `arms`, not both. A single arm serves 100% of traffic; several arms split it. Never introduce a traffic split implicitly. Leave the simulation and outdated-version overrides unset; a release request does not authorize bypassing those gates.

Check both the HTTP status and the GraphQL `errors`. A timeout or an ambiguous response is not proof of failure: read the snapshot or target state before retrying a mutation. Stop on an authorization denial. After success, do the fresh-read verification in [lifecycle](lifecycle.md); an accepted mutation alone is not deployment evidence.
