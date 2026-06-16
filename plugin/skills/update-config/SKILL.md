---
name: update-config
description:
    REQUIRED before editing config/base or config/integrations JSON. Use for voice, agent/persona,
    base SDK, connected integration, or package config changes. Covers ownership, scope,
    schema/default checks, and safe publish.
---

<!-- Copyright Sierra -->

# Updating Configuration

Configuration files are projected workspace config records. The useful mental model is: each file
has identity metadata plus an editable `value`; reference docs, schema refs, and the current JSON
shape explain which record owns a behavior and what scopes exist.

## Layout and Schema

| Path                                               | Meaning                                                                                                                                        |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `.composer/config/base/*.json`                     | Base SDK config records: voice, agent config, persona config, and other platform defaults.                                                     |
| `.composer/config/integrations/*.json`             | Editable config values for integration/package instances already connected to this workspace.                                                  |
| `.composer/config/integrations/refs/*.schema.json` | Read-only raw schemas for connected integration/package values. Use them to understand required/optional fields, defaults, secrets, and shape. |
| `.composer/docs/base-config-reference.md`          | Reference for base SDK config ownership, value shapes, enums, defaults, and runtime meaning.                                                   |

Every config record has identity metadata (`id`, `entry_name`, `type_name`, `entry_type`, `key`,
`$id`, `$key`, `$version`). Preserve it on existing records; add a new list instance without an
`id`, and the server returns the assigned id on the next pull. Editable configuration usually lives
under `value`.

Before changing a value, identify the owner (`entry_name`/record), scope (global/default, locale,
environment, resource, or connected instance), and schema shape. Missing values may mean
"inherit/default", not "empty". Required companion fields are meaningful; when adding a scoped
object, copy the current effective value for that scope or its documented parent rather than
inventing one.

For `config/integrations`, read the matching schema ref before adding, deleting, or reshaping
fields. Match by `entry_name`, `module_name`, or obvious file stem. Secret placeholders such as
`{"$type":"secret","name":"..."}` identify existing secret material; preserve them. Never ask the
user to paste secret values into chat. If a required secret is absent or must change, tell the user
which integration field needs a secret and ask them to set it in the Agent Studio integrations tab.
For required non-secret fields, help the user set a valid value; missing required config usually
means the connected integration will not work in production.

For `config/base`, read `.composer/docs/base-config-reference.md` before changing ownership, adding
fields, or adding scoped overrides. It describes the projected Base SDK records and the runtime
meaning of their fields.

Connected integration/package files are existing connection records. Edit the requested instance's
`value`; environment-scoped settings use raw config `per_environment` wrappers. Changing package
code or integration metadata happens outside Ghostwriter.

Review config diffs semantically before pushing: identity unchanged, requested owner/scope changed,
unrelated scopes untouched. If validation fails, use the schema and current effective values to fix
the shape rather than adding fields only to satisfy the error text.
