---
name: add-integration
description:
    REQUIRED before connecting or using an integration. Covers inventory, connected vs. connectable
    modules, ctx.apis handles, connected-instance config, required fields, secrets, and missing
    integration fallback.
---

# Connecting and Using Integrations

Integrations are code-defined packages that expose external systems and platform capabilities to an
agent. They may provide runtime API functions, packaged tools, Agent Studio connection UI, and
editable connected-instance settings. Ghostwriter works from the current workspace projection; it
does not create integration modules or connect new package instances by itself.

Most integrations are configured in Agent Studio through a structured form. The same configuration
is also projected into the workspace for already-connected instances. Config commonly includes
credentials, endpoint/base URL fields, routing rules, support hours, provider behavior toggles,
locale/environment branches, and package-specific settings. Required fields should be set before
production use; missing required fields usually mean the integration will not work at runtime.
Ghostwriter can edit ordinary config values, while required secret fields must be completed by the
user in Agent Studio.

Read `.composer/docs/integrations-reference.md` for the tool API model, config model, and Future
pattern.

## Surfaces

| Surface                                            | What it tells you                                                                                                      |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `.composer/docs/available-integrations.md`         | Runtime inventory: connected handles, function signatures, packaged tools, connectable modules, and Agent Studio URLs. |
| `.composer/config/integrations/*.json`             | Editable config values for package/integration instances already connected to this workspace.                          |
| `.composer/config/integrations/refs/*.schema.json` | Read-only raw schemas for integration settings: required/optional fields, defaults, scopes, secrets, and nested shape. |

Only entries under **Connected integrations** have live `ctx.apis.<handle>` APIs. Entries under
**Connectable modules** exist in the workspace build but have no connected instance yet, so they are
not callable. You can usually connect one by writing a record (see "Connecting a connectable module"
below); some need an interactive Agent Studio setup instead. Do not invent handles from module
names.

Connected-instance configuration is separate from runtime use. If the user asks to change Shopify
credentials, support hours, package toggles, routing settings, or similar values for an already
connected instance, invoke `/update-config` and read the matching value file plus schema ref. Use
the schema to tell the user what is required, what is optional, what default/inherited values mean,
and which fields are environment- or locale-scoped. If the same package can be connected more than
once, distinguish instances by the connected handle, title, connection URL, and record identity
rather than service name alone.

Secret values are different from ordinary config. Preserve existing secret placeholders and never
ask the user to paste API keys, tokens, passwords, or OAuth secrets into chat. If a secret is
missing or must change, tell the user which secret-backed field needs attention and ask them to set
it directly in the Agent Studio integrations tab. After they do, refresh the workspace before using
or validating the integration.

## Working Loop

1. Read `.composer/docs/available-integrations.md` and classify the capability as connected,
   connectable, or missing.
2. If connected, use the exact handle and signatures shown there. Prefer `ctx.apis.<handle>` over
   raw HTTP when the integration covers the job. If configuration matters, inspect the connected
   config value and schema ref before assuming the integration is ready for production behavior.
3. If connectable, connect it directly by writing a connection record under
   `.composer/config/integrations/`, then push and pull. See "Connecting a connectable module"
   below.
4. If missing, gather the operations and response shapes the agent needs. You can continue designing
   tools with mocks, but the Sierra team must add the integration/package before runtime use.

The integration handles authentication, transport, provider errors, retries, and response
normalization. Tools interpret those results for agent behavior: policy decisions, root-store
updates, `controls.result(...)`, `controls.instruct()`, and user-safe error handling.

## Using a Connected API

Consult `available-integrations.md` for the exact handle, function signatures, parameter types, and
return types. Use the typed API surface directly:

```typescript
// .composer/tools/LookupOrder/implementation.ts
type ToolFunc<P = {}> = import("../../build/types/tool-types").ToolFunc<P>;

const func: ToolFunc<{ order_number: string }> = (sierra, ctx, params, controls, mock) => {
    try {
        return ctx.apis.shopify.lookupOrder({ orderNumber: params.order_number }).get();
    } catch (err: any) {
        return controls.error(
            `Could not look up order ${params.order_number}.`,
            "Ask the customer to double-check their order number."
        );
    }
};
```

Integration functions may return `Future<T>` -- call `.get()` to block and retrieve the result. See
`.composer/docs/integrations-reference.md` for the full Future pattern reference.

## Connecting a connectable module

Connecting reuses the config-record model used for editing -- a file under
`.composer/config/integrations/` with identity metadata and an editable `value` (see
`/update-config` and `integrations-reference.md`). A fresh connection differs only in the points
below.

Create a new file under `.composer/config/integrations/`, filling each field from the schema ref and
omitting the identity fields -- the server assigns them on push. Leave `secret`-typed fields out for
the user to enter in Agent Studio. Set `value.$meta.handle` to the runtime handle
`ctx.apis.<handle>` resolves to: a short, stable slug derived from the integration name.

## Requesting a new integration

If no suitable integration exists in either the connected or connectable sections of the inventory,
a new integration needs to be built and added to the platform.

Tell the user:

> The integration you need is not currently available in your workspace. New integrations are built
> by the Sierra team. Please reach out to your Sierra contact or the Sierra support team to request
> that this integration be added. Include the external service name, the API operations you need
> (e.g., "lookup order", "process refund"), and any relevant API documentation.

In the meantime, gather as much context as possible so agent building can continue:

1. Ask the user what API operations they expect to be available (e.g., "lookup order by order
   number", "get customer by email", "initiate return").
2. Ask for the expected shapes of API responses -- field names, types, example payloads. If the user
   has API documentation, request it.
3. Use this information to design tools with realistic mock data that reflects the expected API
   surface. The `/add-tool` skill covers how to build tools with mocks.

This lets you build and test the full agent behavior (journeys, policies, conditions) while the
integration is being built. Once the integration is available and connected, swap the mocks for real
`ctx.apis.<handle>` calls.

Do not attempt to build a custom integration locally. The ghostwriter workflow does not currently
support uploading custom integrations.
