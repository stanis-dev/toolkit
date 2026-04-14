# sierras CLI — Feedback from Agent-Assisted Workflows

This document summarizes remaining tool-level issues discovered during a review of 26
agent-assisted Sierra development sessions across 2 projects (Pronet, Sky). Items that
have already been addressed (wrong-org via `--bot` auto-resolution, bot-id discovery,
workspace delete confirmation, `--async` flag addition, and per-command "Use when" /
"Don't use when" help text) have been removed.

---

## 1. `--no-cache` on individual replays in loops

**Current state:** `replay-all` no longer exposes `--no-cache` (good). But agents
still write loops calling `sim replay <name> --no-cache` for each sim individually,
bypassing the cache and turning a 2-second bulk export into a 5-minute crawl.

**User impact:**

> "Why the fuck did you add no cache flag? This is slowing everything down to a fucking crawl."

**Why it matters:** The agent reaches for `sim replay` in a loop because it knows the
command. Adding `--no-cache` seems like "getting fresh data." Nothing warns that this
pattern is 100x slower than `replay-all`.

**Suggested improvement:** When `sim replay --no-cache` is called more than 3 times in
quick succession, print a hint: "For bulk replay export, use `sim replay-all` (cached,
parallel, ~2s)." Alternatively, consider a `--no-cache` flag on `replay-all` that
handles cache-busting efficiently in bulk (parallel re-fetches with progress).

---

## 2. `sim run-all` hitting the 1200-run platform limit

**Current state:** `sim run-all` now has `--category`, `--group`, `--tag` filters for
subsetting. But when a full-suite run (e.g., 1516 sims x 5 = 7,580 runs) exceeds the
platform limit, the failure mode is unclear.

**User impact:** One session was abandoned after the agent couldn't work around the limit:

> "Even running with --count 1 won't work since I have 1516 sims total, which is
> already over the 1200 limit."

**Why it matters:** `sim bench start` handles chunking automatically. `sim run-all`
is what agents reach for first. When it hits the limit, there's no error message
pointing to `sim bench start` as the alternative.

**Suggested improvement:** When the computed run count exceeds the platform limit,
print: "N runs exceeds the 1200 platform limit. Use `sim bench start` for automatic
chunking, or filter with `--group`/`--category` to reduce the set."

---

## 3. Sim tag expectations not clearly surfaced

**Current state:** `sim list --json` returns "test definitions" — this may include tag
expectations, but it's not clear from the help text or field naming whether
`expectedTags` and full pass/fail criteria are part of the output.

**User impact:**

> "There is a very specific field with a very specific declaration of which tags each
> simulation expects to be present or not... Not inference but definition of the
> simulation."

**Why it matters:** Tag expectations are the primary pass/fail criteria. Agents that
can't find them via CLI resort to inferring from conversation patterns, which produces
wrong results. If `sim list --json` already includes this data, making it more
discoverable (e.g., documenting the JSON schema or adding a `sim show <name>` command)
would help.

**Suggested improvement:** If `sim list --json` already includes tag expectations,
document the schema. If not, add a `sim show <name> --json` command that returns the
full sim definition including `expectedTags`, `expectedOutcomes`, and `config`.

---

## 4. Sim name encoding sensitivity

**What happens:** Sim names containing em dashes, non-ASCII characters, or special
Unicode cause lookup failures when copied from output or Studio UI to the command line.

**User impact:** An agent repeatedly failed to find a sim by name due to encoding
mismatch. Not a showstopper but adds friction in every session involving sims with
special characters.

**Suggested improvement:** Normalize Unicode in sim name lookups (treat em dash and
hyphen as equivalent). Or support lookup by sim ID as a primary alternative. A fuzzy
match with "did you mean?" for close matches would also help.

---

## 5. `sim run-all` doesn't mention `sim bench start` as alternative

**Current state:** Both commands have "Use when" / "Don't use when" help text (great).
But `sim run-all`'s "Don't use when" says "to wait for completion (sierras sim
wait-all)" — it doesn't mention `sim bench start`, which is the correct choice for
evaluation workflows that need polling, collection, and recovery.

**User impact:** In 4 of 24 evaluation conversations, agents used `sim run-all` or
custom bash loops instead of `sim bench start`, leading to missing results and no
recovery on interruption.

**Why it matters:** The "Don't use when" guidance is the exact place an agent reads
before deciding which command to use. Adding bench there would close the loop.

**Suggested improvement:** Update `sim run-all --help` "Don't use when" to include:
"...or to run an evaluation with automatic polling, collection, and recovery
(`sim bench start`)."

---

## Context

These findings come from a structured review of 26 Cursor agent conversations spanning
Pronet and Sky projects, covering February–April 2026. The review covered simulation
evaluation, conversation analysis, issue investigation, and feature development.

Several items from the original review have already been addressed in the CLI:

- `--bot <name>` auto-resolves org, workspace, and bot-id from `.targets/`
- `workspace delete` now has interactive confirmation (requires `--force` for agents)
- `sim run --async` flag now exists
- All commands have "Use when" / "Don't use when" guidance in `--help`