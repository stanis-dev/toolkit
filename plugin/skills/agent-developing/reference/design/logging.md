# SDK logging

Read before editing a log call or interpreting its visibility and alerting. Before the edit, load the matching canonical skill per [canonical guidance](../session/canonical-guidance.md). A logging edit alone needs no transcript. When the diagnosis needs conversation or simulation events, read [result access](../gates/simulation-results.md).

Log with the functions exported from `@sierra/agent`. Read the function surface in the installed SDK at use time. Visibility is baked into the function name and is independent of severity. The narrowest tier is the default, and widening is deliberate. The error-level variants emit a Slack error event that can trigger alerting, so reserve them for failures worth investigating. A `*Details` trailing object renders as an expandable modal in the inspector.

Log an error with `warnDetails` and put the error inside the details object, reduced to a serializable field:

```ts
warnDetails("message", {
    error: err instanceof Error ? err.message : String(err),
    ...context,
});
```

A plain object spliced into the message string prints `[object Object]`. A bare `Error` serializes to `{}` because its `message` and `stack` are non-enumerable. Include only the diagnostic context the reader needs, never credentials or customer data the log does not need.
