# Conversation and simulation result access

Read before fetching a transcript, a result record, or a raw LLM call. Use only an environment and a tool authorized for the data. A missing wrapper is different from a permission denial; a direct API read needs its own permitted access.

Identifiers differ by object. Real conversations use the `audit-` prefix. Simulation results use `replaytestresult-` and `replaytestmeta-`, and a run uses `replaytestrunset-`. Confirm the tool's schema before prefixing; do not prepend a prefix to an already-qualified identifier.

## Downloaded artifacts

The default route is the CLI download per [ghostwriter files](../session/ghostwriter-files.md), with the command forms in `.composer/docs/agent-traces-reference.md`. Each lands under `.composer/simulations/` or `.composer/conversations/` with `result.json` or `summary.json`, `debug.log`, and `traces/`. Read `result.json` for status, tags, and per-assertion results, `debug.log` for the chronological event flow, and a `traces/*.trace` file only when one task needs the raw LLM request and response. The canonical `debug-simulations` and `debug-conversations` skills and `.composer/docs/agent-traces-reference.md` carry the file format. In this repo the `field-notes` skill carries a reader for downloaded runs; use it before writing a parser. `get_conversation_details` adds the rendered content the download lacks, in a payload small enough to call directly.

## MCP route

When the MCP subset carries them, `get_test_results` with verbose output returns the transcript and events of a run and a `resultId`. Pass that value as `testResultId`, together with `testId`, to `get_llm_call` for a raw prompt and response. Preserve returned IDs exactly rather than deriving one identifier from another. Request only the necessary detail, and run large reads in a subagent that saves the payload to a file and returns a summary.

## Direct GET

When neither route reaches a draft-workspace result:

```text
GET https://<subdomain>.sierra.ai/-/api/sdk/composer/simulations?workspace-id=<workspace-id>&run-id=<run-id>
```

Before that request, read [API authentication](../session/api-auth.md) for the session file, the Bearer token, the session and CSRF cookies, and the matching CSRF header. Do not print credentials, bypass a required permission flow, or change accounts after a denial.

## Reading a result

Check the status and the complete structured result. Diagnose from the per-assertion records, the emitted tags, the transcript turns, and the relevant raw call. Judge prose is a claim to compare with the transcript, not independent evidence. Report a failure by its failing assertion and the turn that broke it, and bind the data to the actual run and workspace. An unavailable required transcript stays an evidence gap.
