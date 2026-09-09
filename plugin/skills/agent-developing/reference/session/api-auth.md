# Existing-session API authentication

Read before an authorized direct API request that reuses the CLI session, or when diagnosing its cookie, CSRF, token, or User-Agent handling. This page describes the mechanics. It does not authorize a read, a mutation, a new account, or another route after a denial. Normal MCP reads never need it.

The credential is the whole of `~/.sierra/<host>.session`, where the host has no port. It is either `<subdomain>:<token>` or a bare token. Follow the CLI parser: strip a subdomain prefix when present, but keep `org-...:secret` admin API tokens intact. Do not split every credential at a colon. Never print the credential, a cookie, or an authorization header. Disable shell tracing and keep secrets out of command arguments, saved examples, logs, and artifacts.

Resolve the cookie subdomain from the credential prefix, otherwise from the configured org. The request carries:

```text
Content-Type: application/json
Cookie: <subdomain>_session=<token>; csrf=<fresh-uuid>
X-Sierra-CSRF-Token: <same-fresh-uuid>
Authorization: Bearer <token>
User-Agent: <client identifier>
X-Sierra-Subdomain: <subdomain>
```

Generate the CSRF value locally and use the same value in the cookie and the header. The CLI identifies itself as `sierra-cli/<version> (...)`. Older recipes used `pinecone/1.0` for the release mutations and a `claude-code/<version>` family for simulation reads. These are client identifiers, not authorization. Align `X-Sierra-Subdomain` with the intended org, never with another org to cross an access boundary.

A wrong path or a mismatched CSRF pair explains an error. A permission denial is not permission to broaden credentials or bypass the access flow: stop and report it.
