# Agent configuration

Read before changing `createAgent`, a config override, the compatibility date, or environment-controlled behavior. Load the matching canonical skill per [canonical guidance](../session/canonical-guidance.md) before the edit. When the compatibility date or safety version is managed in Agent Studio, the canonical `manage-agent-versioning` skill and `pnpm sierra versioning` own both the read and the change.

Read `createAgent` and its props in the installed SDK and take every config key from that definition. The props layer as overrides onto the no-code base agent. The compatibility date gates whether `config` deep-merges into the base or replaces it wholesale. Confirm the merge behavior for the agent's date before touching `config`. The replace path tags the base keys it drops.

Config is not runtime-only. At upload the server runs the config entrypoint against the workspace's no-code version and persists the validated result on the build. Services read that extracted config, not the source file. Verify the resulting build config through the Sierra tools available in the session. When a field's downstream meaning is not in `.composer/docs/base-config-reference.md`, ask `ask_sierra_assistant` instead of inferring it from SDK comments.

Keep the toggle convention: an environment-variable override whose null value disables the behavior outright, so setting the override is the instant mitigation. For a time-sensitive decision or a persisted flag, read [runtime and state](runtime-state.md).
