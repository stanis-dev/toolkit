# Claude Code with the Latest Opus — Community-Endorsed Practices

---

## Executive summary — the seven things most worth your time

1. **Cap CLAUDE.md at ~80–160 lines and prune quarterly.** Past that, rules start being selectively ignored (the
   "instruction-drop" failure mode). Bijit Ghosh's slot-count argument has become the most-cited justification.
2. **Move anything mechanical from CLAUDE.md into hooks.** Text rules degrade with context length; hooks don't. The
   community's load-bearing motto in 2026 is: _if you can write it as a hook, do that, not a rule._
3. **The single highest-leverage hook is a `Stop` hook that runs tests and refuses turn-completion on red** — with
   `stop_hook_active` honored. Inverts control so Claude can't declare victory on broken work.
4. **For Opus 4.7 specifically: audit what you used to repeat mid-session and write it down.** 4.7 follows literal
   instructions but stops inferring intent. Delete scaffolding you no longer need ("self-verify", "give status updates")
   and add the corrections you previously had to nag.
5. **Anti-sycophancy works via positive framing + banned-word lists, not "don't" rules.** Telling Claude not to say
   "You're absolutely right" makes it more likely to say it. Output styles with positive examples are the actual fix.
6. **Document-and-clear beats `/compact` for multi-hour sessions.** At ~30% context, have Claude write `progress.md`,
   then `/clear`, then `@progress.md` to resume.
7. **Plan-to-file is the most-endorsed planning ritual.** Plan mode in-chat fades when the conversation scrolls; a
   `plan.md` you've annotated stays load-bearing. Ronacher's "I want a file on disk I can see and edit" is the canonical
   formulation.

---

# Part A — Landscape

## A.1 The five schools

The Claude Code discourse in mid-2026 splits into roughly five clusters, with X (volume), Substack (depth), GitHub
(artifacts), and YouTube/podcasts (walkthroughs) carrying the conversation. Reddit and HN are reactive but rarely
produce canonical takes.

**(a) Skills-framework builders.** Anchored by Jesse Vincent's `obra/superpowers` (~201K stars; accepted into the
official Anthropic marketplace by Jan 2026). Thesis: encode method as installable skill bundles (Brainstorm → Spec →
Plan → TDD → Subagent → Review → Finalize). Treats CLAUDE.md as a slim entry point into a larger skill tree.

**(b) Loop / autonomy school.** Geoffrey Huntley's "Ralph Wiggum" loop —
`while not COMPLETE: claude --print < PROMPT.md`. Now an official Claude Code plugin (`ralph-wiggum`). Companion
artifacts: disler's `infinite-agentic-loop` and `claude-code-is-programmable`. Ethos: trust fresh-context iteration over
carefully-curated single sessions; let it run overnight.

**(c) Pragmatist / architect school.** Armin Ronacher, Mitchell Hashimoto, Harper Reed. Lean against framework overhead;
treat themselves as architect, Claude as executor. Skeptical of subagent maximalism and skill proliferation.

**(d) Personal-AI / OS school.** Daniel Miessler's Personal AI Infrastructure (PAI), Eric Buess's hooks-driven personal
system. Treats Claude Code as a substrate for life automation, not just coding.

**(e) Evaluators / trackers.** Simon Willison, Zvi Mowshowitz, Hamel Husain, Dan Shipper / Every.to. Not method-builders
so much as serious chroniclers who keep the field honest with measurements and timely synthesis.

Steve Yegge sits across (b) and (e) — his "8 Levels" framework and Gas Town orchestrator make him a school-of-one with
outsized discourse influence.

## A.2 Live debates

**Subagents — leverage or overhead?** Pro side (Skills-framework + Anthropic's May 2026 "dynamic workflows" launch):
subagents are now table stakes for multi-domain tasks; supervisor topology with one level of subagents is the 2026
production default. Skeptical side: ~20K tokens of overhead per subagent before user payload, ~4× spend for three
subagents on one task. Pragmatists side with skeptics for solo work. Honest read: subagents pay off when the work needs
genuine isolation or parallelism. For repetitive edits across a known file list, edit directly.

**Plan mode — load-bearing or theatre?** Ronacher's "What Actually Is Claude Code's Plan Mode?" makes the skeptical
case: the generated plan has no extra structure beyond text; if you rubber-stamp it you pay the cost without the
benefit. Skills-framework camp treats plan mode as the single biggest reliability lever and the most underused part of
the harness. Honest consensus: plan mode is valuable iff the human actually critiques the plan. Otherwise it's pure
cost.

**Long vs. short CLAUDE.md.** Minimalist consensus has hardened: under 200 lines, ideally under 500 tokens, every line a
behavioral contract. Bloated CLAUDE.md files demonstrably cause instructions to be ignored. Contrarian "you don't need a
CLAUDE.md" position exists but is minority. Live disagreement is structural: one short file vs. short root + `docs/`
tree + skills.

**Output styles and narration.** Output styles are documented and widely used. Related debate: whether Claude's default
narration (commenting "what" instead of "why") is noise. Power users mostly land on: terse default, expressive styles
for specific modes (debugging, teaching).

## A.3 Converged consensus (table stakes — assume you do these)

- Keep CLAUDE.md short and behavior-changing; prune it like code.
- Use plan mode for non-trivial work, but actually read the plan.
- Verification beats prompting — give Claude a way to check its own output.
- Use a PreToolUse secrets-scan hook and a PostToolUse lint/format hook at minimum.
- Curate skills aggressively — most are noise.
- Parallel sessions are common practice now (Boris Cherny himself runs 5 local + 5–10 web simultaneously).

## A.4 Emerging patterns (flag uncertainty)

- **Dynamic workflows** (Anthropic, May 2026). Claude writes its own orchestration scripts. Promising but only
  weeks-old; reproducibility outside Anthropic is unverified.
- **"Agents that run while you sleep."** Ralph loop is mainstream, but quality concerns persist — $10/hour vibe-cloned
  commercial software exists.
- **Self-improving skills / `learnings.md`.** Risk: `learnings.md` grows unbounded and becomes the new bloated-CLAUDE.md
  problem.
- **The Karpathy CLAUDE.md genre.** Forrest Chang's Karpathy-derived skill hit ~144K stars in weeks (despite not
  actually being Karpathy's). Durable methodology or hype-cycle peak — genuinely unsettled.
- **Claude Code as personal OS.** Miessler-style PAI builds are growing but remain niche.

---

# Part B — The Playbook

## B.1 General behavioral instructions (CLAUDE.md, global rules)

### Recipe: "Don't assume — surface ambiguity, then ask"

**Rule:** Make Claude state assumptions explicitly and ask before guessing. **Why:** Practitioners reported Opus's
biggest sustained failure mode is silent guessing on ambiguous instructions. Forrest Chang's viral file: _"Don't assume.
Don't hide confusion. Surface tradeoffs."_ **How to apply:**

```
## Think Before Coding
Don't assume. Don't hide confusion. Surface tradeoffs.
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.
```

**Endorsement:** Converged consensus. **Sources:**

- multica-ai/andrej-karpathy-skills CLAUDE.md — https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md
- Alex Rusin —
  https://blog.alexrusin.com/the-viral-karpathy-claude-md-file-heres-the-honest-truth-about-what-it-actually-is/
- rishabhsonker gist — https://gist.github.com/rishabhsonker/707c9c68ee1035edca7c28ba9d7b4d14 **Fails when:** Trivial
  single-file edits — Claude opens with three questions for "rename this variable."

### Recipe: Surgical changes — every line traces to the request

**Rule:** Forbid drive-by refactors, style "improvements," and adjacent cleanup. **Why:** The most-cited sustained
complaint with 4.6/4.7 is scope creep on edits. Kirill Markin: _"Don't rewrite half the file because you got excited."_
**How to apply:**

```
## Surgical Changes
Touch only what you must. Clean up only your own mess.
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.
The test: Every changed line should trace directly to the user's request.
```

**Endorsement:** Converged across at least four maintained CLAUDE.md repos. **Sources:**

- multica-ai/andrej-karpathy-skills
- kirill-markin — https://kirill-markin.com/articles/claude-code-rules-for-ai/ **Fails when:** Greenfield work where
  broad scaffolding is what you want.

### Recipe: Anti-sycophancy block

**Rule:** Explicitly instruct against agreement-seeking, flattery, abandoning positions under pushback. **Why:**
Sycophancy persists even in 4.7 and degrades code review / architectural debate. **How to apply:**

```
- Be anti-sycophantic — don't fold arguments just because I push back.
- Stop excessive validation — challenge my reasoning instead.
- Avoid flattery or unnecessary praise.
- Don't anthropomorphize yourself.
- Prefer terse updates. Be concise and direct.
```

**Endorsement:** Converged. **Sources:**

- BSWEN — https://docs.bswen.com/blog/2026-02-12-claude-custom-instructions/
- Claude Unleashed — https://claudeunleashed.substack.com/p/stop-claude-from-always-agreeing
- Freek Van der Herten — https://freek.dev/3026-my-claude-code-setup **Fails when:** 4.7 sometimes overcorrects into
  argumentative mode; back off to "be concise and direct, don't flatter."

### Recipe: No silent fallbacks, no swallowed errors

**Rule:** Ban catch-all error handlers and quiet retries unless explicitly requested. **Why:** Kirill Markin: most
expensive debugging cost was "burning messages on the same stuff" — Opus defaulting to try/except that hides root
causes. **How to apply:**

```
- No silent fallbacks. No fallbacks unless I explicitly ask for them.
- Always raise errors explicitly, never silently ignore them.
- Avoid catch-all exception handlers that hide the root cause.
- No error handling for impossible scenarios.
```

**Endorsement:** Strong (Markin) + converged on Karpathy-style files. **Sources:**

- kirill-markin — https://kirill-markin.com/articles/claude-code-rules-for-ai/
- multica-ai/andrej-karpathy-skills **Fails when:** Production-hardening passes where defensive code is correct.

### Recipe: No-attribution rule

**Rule:** Prohibit Claude from attributing itself in commits, PRs, code comments, docs. **Why:** Anthropic's defaults
inject `Co-Authored-By: Claude` and emoji robots; users find this leaks AI provenance. **How to apply:**

```
- Claude must NEVER add attribution to itself in any form.
- Do NOT add "Co-Authored-By: Claude" to commits.
- Do NOT add Claude/AI references in code comments.
- Do NOT add emoji indicators (e.g. 🤖) to denote AI involvement.
```

**Endorsement:** Converged on personal dotfiles; contested on team repos where the trailer is a transparency norm.
**Sources:**

- banagale gist — https://gist.github.com/banagale/50dde8d6c56929d07e8ad17dab01680f
- HivemindOverlord/poe2-mcp CLAUDE_COMMIT_SETUP.md **Fails when:** OSS repos where reviewers want to know which PRs were
  AI-assisted.

### Recipe: Keep CLAUDE.md to 80–160 lines, prune quarterly

**Rule:** Hard-cap CLAUDE.md length; everything else into skills, slash commands, or `@import`ed files. **Why:** Bijit
Ghosh: _"Models can reliably follow approximately 150–200 distinct instructions, with Claude Code's system prompt
consuming ~50 slots, leaving only 100–150 usable slots."_ Maximalist files measurably stop being followed mid-session.
**How to apply:** 80–120 line target (Ghosh) or ~160 lines (gbrain reference). Treat CLAUDE.md as a behavioral contract
— every word should change how the agent acts. **Endorsement:** Converged. The minimalist camp won. **Sources:**

- Bijit Ghosh —
  https://medium.com/@bijit211987/the-complete-guide-to-claude-md-memory-rules-loading-and-cross-tool-compression-97cc12ed037b
- garrytan/gbrain — https://github.com/garrytan/gbrain/blob/master/CLAUDE.md
- MuhammadUsmanGM minimal example —
  https://github.com/MuhammadUsmanGM/claude-code-best-practices/blob/main/examples/claude-md-minimal.md **Fails when:**
  Very large monorepos — nested CLAUDE.md is the right answer instead.

### Recipe: Commands + Structure + Rules — minimal template

**Rule:** A useful project CLAUDE.md has exactly three sections. **Why:** Anything aspirational ("write clean code")
gets dropped; only concrete, executable info changes behavior. **How to apply:**

```
## Commands
- `npm test` — run tests (Jest)
- `npm run lint` — ESLint check
- `npm run dev` — start dev server

## Structure
- `src/routes/` — API route handlers
- `src/models/` — database models (Sequelize)
- `tests/` — test files mirroring src/ structure

## Rules
- TypeScript strict mode — no `any`
- All API responses use `{ data, error, status }`
- Use the existing logger (`src/utils/logger.ts`), not console.log
```

**Endorsement:** Converged for project-level CLAUDE.md. **Sources:**

- MuhammadUsmanGM
- elegantsoftwaresolutions — https://www.elegantsoftwaresolutions.com/blog/claude-code-mastery-claude-md-patterns
  **Fails when:** Solo research repos with no test/lint commands.

### Recipe: Global = personal toolkit; project = team playbook

**Rule:** `~/.claude/CLAUDE.md` holds your private defaults; project `CLAUDE.md` is self-contained for teammates without
your global file. **Why:** Both files compose, both burn context. Conflating them duplicates and bloats. **How to
apply:** Personal rules (style, anti-sycophancy, no-emoji, no-attribution) go global. Project rules (commands, layout,
conventions) go in repo root. **Endorsement:** Converged. **Sources:**

- shanraisshan —
  https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-global-vs-project-settings.md
- raythanni — https://raythanni.substack.com/p/claude-code-memory-files-global-vs **Fails when:** Pure solo on personal
  repos — separation isn't worth the bookkeeping.

### Recipe: The "twice-corrected" rule

**Rule:** Only add a line to CLAUDE.md after you've corrected Claude on the same thing twice. **Why:** Prevents
speculative bloat. _"A CLAUDE.md that grows organically from real problems is more useful than one written
speculatively."_ **How to apply:** First mistake — fix in chat. Second time — dictate the rule into CLAUDE.md.
Quarterly, delete rules you can't remember why you added. **Endorsement:** Converged. **Sources:**

- shanraisshan — https://github.com/shanraisshan/claude-code-best-practice/blob/main/CLAUDE.md
- Bijit Ghosh (quarterly pruning) **Fails when:** New projects where you genuinely know conventions before Claude breaks
  them.

### Recipe: Opus 4.7 — write down what you used to repeat mid-session

**Rule:** Anything you previously had to nag mid-session belongs in CLAUDE.md verbatim; 4.7 follows literal instructions
but stops inferring intent. **Why:** _"Everything you had to repeat to 4.6 mid-session, 4.7 will follow from the start —
as long as you've written it down."_ **How to apply:** Audit last week of chats. Add every mid-session correction to
CLAUDE.md. _Remove_ scaffolding 4.7 self-handles: delete "double-check before returning" (self-verifies), delete "give
status updates" (emits natively), delete vague "don't try this in one response." _Keep_ negative constraints — these now
work reliably where 4.6 ignored them. **Endorsement:** Converged in the post-4.7 wave. **Sources:**

- MindStudio — https://www.mindstudio.ai/blog/how-to-prompt-claude-opus-4-7
- claudefa.st — https://claudefa.st/blog/guide/development/opus-4-7-best-practices
- wmedia.es — https://wmedia.es/en/tips/claude-code-opus-4-7 **Fails when:** Users who never used 4.6 can skip this
  exercise.

### Recipe: Verification protocol — no done without proof

**Rule:** Forbid describing work as "done" / "implemented" / "working" without the exact command run and its actual
output. **Why:** Sustained users find Opus claims tasks complete based on reading code rather than running it. **How to
apply:**

```
- Never claim work is "implemented", "done", "complete", or "working" without verification proof.
- If not verified, explicitly state "INCOMPLETE - not tested" or "Built but not verified".
- When verifying, show the exact command executed and the actual output received.
- Integration tests must not use mocks, stubs, or fake responses.
```

**Endorsement:** Strong + convergent. **Sources:**

- anthropics/claude-code Issue #8945 — https://github.com/anthropics/claude-code/issues/8945
- Godmode — https://getgodmode.dev/blog/claude-code-skips-tests.html **Fails when:** Pure design/spec sessions; needs an
  "unless this is a planning session" carve-out.

### Recipe: Goal-driven loop framing

**Rule:** Convert tasks into verifiable goals with explicit success criteria, then loop until verified. **Why:** Strong
success criteria let you loop independently. Weak criteria ("make it work") require constant clarification. **How to
apply:**

```
## Goal-Driven Execution
Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"
For multi-step tasks, state a brief plan:
1. [Step] → verify: [check]
```

**Endorsement:** Strong (Karpathy-style file) + independent convergence with Ronacher's workflow shape. **Sources:**

- multica-ai/andrej-karpathy-skills
- Armin Ronacher — https://lucumr.pocoo.org/2025/6/12/agentic-coding/ **Fails when:** Exploratory coding where success
  criteria are themselves the question.

---

## B.2 Workflows & rituals

### Recipe: Plan-to-file before any code

**Rule:** Never let Claude write code until a written plan exists on disk that you've reviewed and approved. **Why:**
Armin Ronacher: _"I'm more in control if I have a file on disk somewhere that I can see, that I can read, that I can
review, that I can edit."_ **How to apply:**

1. Enter plan mode (Shift+Tab) or invoke `obra/superpowers` `writing-plans` skill.
2. Prompt: _"read this folder in depth, understand how it works deeply… then write a detailed `research.md` report."_
3. Then: _"write a detailed `plan.md` outlining how to implement this. include code snippets."_
4. Annotate the plan inline across 1–6 rounds before unlocking edits. **Endorsement:** Converged. **Sources:**

- Armin Ronacher — https://lucumr.pocoo.org/2025/12/17/what-is-plan-mode/
- Boris Tane — https://boristane.com/blog/how-i-use-claude-code/
- obra/superpowers — https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md **Fails when:** Plan
  stays in chat — once it scrolls past, Claude loses the contract.

### Recipe: Brainstorm → Clarifying Questions → Spec

**Rule:** Force Claude to ask clarifying questions before any plan or code. **Why:** _"Hearing your half-formed thoughts
reflected back makes you think harder."_ Surfaces decisions you'd otherwise discover at implementation. **How to
apply:** Install `obra/superpowers` and use `brainstorming` skill, or prompt manually: _"Before proposing anything, ask
me 5 clarifying questions whose answers aren't already in CLAUDE.md, memory, or git status."_ **Endorsement:** Converged
among superpowers users. **Sources:**

- Code Miner — https://blog.codeminer42.com/brainstorming-the-skill-that-changed-claude-for-me/
- obra/superpowers — https://github.com/obra/superpowers **Fails when:** Skill asks generic questions despite rich
  CLAUDE.md context (filed as superpowers issue #849).

### Recipe: Verification-before-completion gate

**Rule:** No success claim without running the verification command and reading its full output this turn. **Why:**
Claude self-reported: _"Without a verification step, I'm pattern-matching on 'this edit looks like it should fix the
problem' and declaring victory."_ **How to apply:** Five-step gate from `obra/superpowers`:

> "IDENTIFY what command proves the claim → RUN the full command (fresh, complete) → READ the full output and check exit
> code → VERIFY if output confirms the claim → CLAIM." Iron law: _"NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION
> EVIDENCE."_ Forbid "should," "probably," "seems to" in completion summaries. **Endorsement:** Converged. **Sources:**

- obra/superpowers — https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md
- Walking Labs Lecture 9 —
  https://walkinglabs.github.io/learn-harness-engineering/en/lectures/lecture-09-why-agents-declare-victory-too-early/
  **Fails when:** Linter/typecheck alone — doesn't catch behavioral regressions. Pair with actual test execution.

### Recipe: Stop-hook completion gate

**Rule:** Externalize the "are we done?" judgment to a `Stop` hook the agent can't override. **Why:** _"Completion
judgment should not be made by the agent itself."_ The hook is deterministic where the prompt is suggestive. **How to
apply:** `Stop` hook runs your test/build/lint command and returns
`{"decision":"block","reason":"<actionable failure>"}` on red. Critical: respect `stop_hook_active` — if true, exit 0 to
allow stopping. Error messages must be repair instructions, not bare failures. **Endorsement:** Converged. **Sources:**

- Coding with Roby — https://codingwithroby.substack.com/p/the-stop-hook-that-wont-let-claude
- disler/claude-code-hooks-mastery — https://github.com/disler/claude-code-hooks-mastery **Fails when:** Catches
  premature completion, not correctness. A hook asking "did Claude run the tests?" can't detect that Claude wrote broken
  tests.

### Recipe: Round-trip screenshot verification for UI

**Rule:** For any front-end change, make Claude render the result in a real browser, capture a screenshot, and re-read
it. **Why:** Closes the loop between "looks right in code" and "looks right on screen." Tal Rotbart: _"giving Claude
Code eyes."_ **How to apply:** Wire Playwright or Chrome-DevTools-MCP into post-edit flow. Agent navigates, screenshots,
visually inspects. Compare against fixtures. **Endorsement:** Converged among MCP browser-tool users. **Sources:**

- Tal Rotbart — https://medium.com/@rotbart/giving-claude-code-eyes-round-trip-screenshot-testing-ce52f7dcc563
- alexop.dev — https://alexop.dev/posts/automated-qa-claude-code-agent-browser-cli-github-actions/ **Fails when:**
  Screenshot of broken state still loads — Claude says "renders correctly." Pair with explicit assertion text.

### Recipe: Ralph loop for greenfield grunt work

**Rule:** Wrap Claude in `while not COMPLETE: claude --print < PROMPT.md` with external state in `prd.json` +
`progress.txt`. **Why:** Solves context degradation by re-loading state every turn. Huntley shipped the CURSED language
over 3 months for ~$297. **How to apply:** Geocodio's recipe:

```
1. PROMPT.md: "Read prd.json and progress.txt. Pick highest-priority story
   where passes=false. Implement. Run npm test. Update prd.json and append
   to progress.txt. Emit <PROMISE>COMPLETE</PROMISE> when no passes:false remain."
2. Bash: while iter<MAX; do out=$(cat PROMPT.md | claude --print); grep COMPLETE && exit; done
```

Use explicit permission prompts in `.claude/settings.local.json` rather than `--dangerously-skip-permissions`.
**Endorsement:** Contested. Strong for greenfield/MVP; discouraged for production by Geocodio and Simon Wang.
**Sources:**

- Geoffrey Huntley — https://ghuntley.com/cursed/
- Adam Tuttle — https://adamtuttle.codes/blog/2026/my-ralph-workflow-for-claude-code/
- Geocodio (dissent) — https://www.geocod.io/code-and-coordinates/2026-01-27-ralph-loops
- Simon Wang (dissent) —
  https://itnext.io/ralph-loop-is-innovative-i-wouldnt-use-it-for-anything-that-matters-cd92f2f0df2e **Fails when:**
  Established codebases with implicit conventions, complex deployment pipelines, or where you need to deeply understand
  every line.

### Recipe: One worktree per subagent

**Rule:** Every code-writing subagent gets its own git worktree (`isolation: "worktree"`). **Why:** Parallel agents
collide on file edits. Cost is zero; upside is non-interference at scale. **How to apply:** Set `isolation: worktree` in
subagent frontmatter. Run 3–5 in parallel; 4–8 concurrent worktrees per dev is the practical ceiling. Weekly
`git worktree prune` + idle-directory nag — stale worktrees are _"the single biggest reason teams give up on the
pattern."_ **Endorsement:** Converged. **Sources:**

- obra/superpowers `using-git-worktrees`
- Claude Directory — https://www.claudedirectory.org/blog/claude-code-worktrees-guide
- spillwavesolutions/parallel-worktrees **Fails when:** Skipped cleanup; >10 parallel workers — review becomes the
  bottleneck.

### Recipe: Adversarial code-review subagent pass

**Rule:** After implementation, dispatch an independent code-review subagent (or several) before committing. **Why:**
_"When an agent assesses its own output, it systematically provides overly positive assessments."_ A fresh subagent has
no prior commitment to the approach. **How to apply:** Druce's prompt: _"Do a git diff and pretend you're a senior dev
doing a code review and you HATE this implementation. What would you criticize?"_ HAMY ships 9 parallel reviewers
(test-runner, linter, code-reviewer, security, style, test-quality, performance, dependency-safety, simplification).
Rule: _"a finding must be reproduced by another agent to count."_ **Endorsement:** Converged. **Sources:**

- HAMY — https://hamy.xyz/blog/2026-02_code-reviews-claude-subagents
- Druce.ai — https://druce.ai/2026/02/claude-code
- VoltAgent/awesome-claude-code-subagents
- obra/superpowers `requesting-code-review` + `receiving-code-review` **Fails when:** Reviewer inherits same prompt
  context — pass diff only with fresh system prompt.

### Recipe: Frontend/backend parallel split

**Rule:** When the boundary is clean, run two Claude instances simultaneously — one UI (mocked APIs), one backend.
**Why:** Houmann: _"Frontend + backend at the same time is a great approach."_ **How to apply:** Define the API contract
first (OpenAPI or types file). Worktree per side. Merge when both pass their own tests, then integration verification.
**Endorsement:** Converged. **Sources:**

- Christian Houmann — https://bagerbach.com/blog/how-i-use-claude-code/
- Agent Interviews — https://docs.agentinterviews.com/blog/parallel-ai-coding-with-gitworktrees/ **Fails when:** API
  contract drifts mid-flight. Lock contracts before splitting.

### Recipe: `/clear` between unrelated tasks

**Rule:** Reset context with `/clear` rather than relying on auto-compaction. **Why:** Druce: _"Quality tends to fall
when context reaches ~50% full."_ Compaction loses load-bearing detail. **How to apply:** Land work, commit, `/clear`,
prime next task by referencing the plan file rather than prior conversation. **Endorsement:** Converged. **Sources:**

- Druce.ai — https://druce.ai/2026/02/claude-code
- Sankalp — https://sankalp.bearblog.dev/my-claude-code-experience-after-2-weeks-of-usage/ **Fails when:** You `/clear`
  without persisting state to a file.

### Recipe: Subagent for token-heavy exploration

**Rule:** Use a subagent (Haiku-powered Explore, or a custom one) for codebase research; let it return a digested
report. **Why:** Keeps the main Opus context lean. Simon Willison endorses subagents for _"token-heavy stuff, including
actual implementation."_ **How to apply:** In Plan mode, Explore activates automatically. For custom flows, define
`code-explorer` subagent (`tools: Read, Grep, Glob`, `model: haiku`) returning a structured report. Heuristic: _"If the
work is small and should stay in front of you, that is a skill. If the work is big and should run in a side process,
that is a subagent."_ **Endorsement:** Converged. **Sources:**

- Simon Willison — https://simonwillison.net/tags/sub-agents/
- alexop.dev — https://alexop.dev/posts/understanding-claude-code-full-stack/ **Fails when:** Subagent given open-ended
  question — burns its own context and returns mush.

### Recipe: TDD red-green-refactor as enforced phase

**Rule:** Tests first; verification gates between phases. **Why:** _"Systematic over ad-hoc — process over guessing."_
Prevents "refactor before functionality is verified" failure. **How to apply:** Plan task → write failing test → commit
test → implement → run test → commit implementation. `executing-plans` skill enforces 2–5 minute tasks each ending in a
commit. **Endorsement:** Converged among superpowers users; contested in rapid-prototyping camps. **Sources:**

- obra/superpowers `test-driven-development`
- Marc Nuri — https://blog.marcnuri.com/superpowers-claude-code-skills-framework **Fails when:** Throwaway prototypes —
  TDD ceremony slows exploratory work.

---

## B.3 Hook patterns

### Recipe: Bash firewall via PreToolUse

**Rule:** Wrap `Bash` with a `PreToolUse` hook that regex-matches destructive commands and exits 2 to block. **Why:**
Permissions allow-listing only catches verbatim commands; a chained `cd repo && git push --force origin main` slips
through. Hooks see the entire command string. **How to apply:**

```json
{
    "hooks": {
        "PreToolUse": [
            {
                "matcher": "Bash",
                "hooks": [
                    {
                        "type": "command",
                        "command": "bash -c 'INPUT=$(cat); CMD=$(echo \"$INPUT\" | jq -r \".tool_input.command\"); if echo \"$CMD\" | grep -qE \"rm\\s+-rf\\s+/|git\\s+push\\s+(-f|--force)\\s+(origin\\s+)?main|git\\s+reset\\s+--hard|DROP\\s+TABLE\"; then echo \"BLOCKED: $CMD\" >&2; exit 2; fi'"
                    }
                ]
            }
        ]
    }
}
```

**Endorsement:** Converged — the single most-recommended hook across every guide. **Sources:**

- Blake Crosley — https://blakecrosley.com/blog/claude-code-hooks-tutorial
- karanb192/claude-code-hooks — https://github.com/karanb192/claude-code-hooks
- aihero.dev — https://www.aihero.dev/this-hook-stops-claude-code-running-dangerous-git-commands **Fails when:** Regex
  misses obfuscated commands (variable expansion, base64 scripts). Defense-in-depth, not a sandbox.

### Recipe: PostToolUse auto-format

**Rule:** Run formatter on the touched file after every successful edit. **Why:** _"Simplest and most impactful hook."_
Eliminates formatting drift. **How to apply:**

```json
{
    "hooks": {
        "PostToolUse": [
            {
                "matcher": "Edit|MultiEdit|Write",
                "hooks": [{ "type": "command", "command": "~/format-code.sh" }]
            }
        ]
    }
}
```

The script reads JSON from stdin, extracts `.tool_input.file_path`, dispatches on extension.
`ryanlewis/claude-format-hook` is a ready-made polyglot version. **Endorsement:** Converged. **Sources:**

- ryanlewis/claude-format-hook — https://github.com/ryanlewis/claude-format-hook
- Pixelmojo — https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns **Fails when:** Matcher
  case mismatch — `multiEdit` (lowercase m) silently never matches `MultiEdit`. Also: forgetting `chmod +x`.

### Recipe: PostToolUse typecheck/lint feedback loop

**Rule:** After every edit, run `tsc --noEmit` (incremental) and/or `ruff check`. Surface stderr — Claude sees it and
self-corrects next turn. **Why:** Catches type errors immediately rather than after Claude has built layers on a broken
signature. **How to apply:**

```json
{
    "hooks": {
        "PostToolUse": [
            {
                "matcher": "Edit|Write",
                "hooks": [
                    { "type": "command", "command": "npx --no-install tsc --noEmit --incremental 2>&1 | head -20" }
                ]
            }
        ]
    }
}
```

Use `--incremental` + `head -20` to stay under the 10-min timeout and avoid flooding context. **Endorsement:** Strong /
converging. **Sources:**

- Pixelmojo
- Mustafa Morbel — https://medium.com/becoming-for-better/taming-claude-code-a-guide-to-claude-md-and-hooks-ed059879991c
  **Fails when:** Full `tsc` on every keystroke kills monorepos.

### Recipe: Stop hook that won't let Claude lie about "done"

**Rule:** On `Stop`, run tests. Exit 0 if green; emit `{"decision":"block","reason":"..."}` if red. Honor
`stop_hook_active`. **Why:** Inverts control — Claude must pass the check before its turn ends. The single most-cited
"this changed my workflow" hook of 2026. **How to apply:**

```bash
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then exit 0; fi
if npm test > /dev/null 2>&1; then
  exit 0
else
  jq -n '{decision: "block", reason: "npm test exited non-zero. Read failures and fix before completing."}'
  exit 0
fi
```

**Endorsement:** Strong. **Sources:**

- Coding with Roby — https://codingwithroby.substack.com/p/the-stop-hook-that-wont-let-claude
- Amit Kothari — https://amitkoth.com/claude-code-stop-hooks/
- claudefa.st — https://claudefa.st/blog/tools/hooks/stop-hook-task-enforcement **Fails when:** Omitting
  `stop_hook_active` guard creates infinite continuation loop. Long test suites blow past 10-min timeout — use fast
  smoke suite.

### Recipe: SessionStart context injection

**Rule:** Use `SessionStart` to print just-in-time context (current branch, recent commits, freeze windows) — Claude
reads it as a system reminder. **Why:** CLAUDE.md is static; `SessionStart` is dynamic. Model deprioritizes file content
as conversation grows; injected context arrives as fresh system message. **How to apply:**

```json
{
    "hooks": {
        "SessionStart": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "echo \"## Repo state\"; git branch --show-current; git log --oneline -5; git status --short"
                    }
                ]
            }
        ]
    }
}
```

**Endorsement:** Strong. **Sources:**

- MindStudio — https://www.mindstudio.ai/blog/session-start-hooks-claude-code-force-context
- claudefa.st — https://claudefa.st/blog/tools/hooks/session-lifecycle-hooks **Fails when:** Flaky historically on "new
  vs resume" (#10373). Keep idempotent and cheap.

### Recipe: PreCompact checkpoint write

**Rule:** Before compaction, write critical state (constraints, open tasks, goal) to a checkpoint file. After compact,
instruct Claude to re-read it. **Why:** Auto-compaction summarizes silently and routinely drops constraints. A tiny
external checkpoint is more reliable than hoping the summary preserved them. **How to apply:** `PreCompact` hook runs
`.claude/hooks/pre-compact.sh` which tails transcript JSON, pulls last N user messages and current goal, appends to
`.claude/checkpoint.md`. Mike Adolan's `claude-brain` writes full transcript to SQLite. **Endorsement:** Niche but
rapidly converging. **Sources:**

- Mike Adolan —
  https://dev.to/mikeadolan/claude-code-compaction-kept-destroying-my-work-i-built-hooks-that-fixed-it-2dgp
- Yuanchang — https://yuanchang.org/en/posts/claude-code-auto-memory-and-hooks/
- okhlopkov — https://okhlopkov.com/claude-code-compaction-explained/ **Fails when:** Writing too much (full
  transcripts) inflates the next session.

### Recipe: Stop / Notification desktop alert

**Rule:** On `Stop` and `Notification`, fire `osascript` / `notify-send` / `terminal-notifier` plus terminal bell.
**Why:** Long agentic runs are the main use case; people stop watching. End-of-turn ping is the highest-ROI QoL hook.
**How to apply:**

```json
{
    "hooks": {
        "Stop": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "osascript -e 'display notification \"Claude is done\" with title \"Claude Code\"' ; printf '\\a'"
                    }
                ]
            }
        ],
        "Notification": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "terminal-notifier -title 'Claude Code' -message 'Needs your attention' -sound Glass"
                    }
                ]
            }
        ]
    }
}
```

**Endorsement:** Converged. **Sources:**

- Michael Swann gist — https://gist.github.com/michael-swann-rp/6112d64456b49ec606d7fdbe1e2bd310
- Konabos — https://konabos.com/blog/stop-babysitting-claude-code-a-five-minute-sound-notification-setup **Fails when:**
  macOS Focus modes mute notifications. Spammy if `Notification` hook fires on every permission prompt.

### Recipe: Protect critical paths

**Rule:** `PreToolUse` matching `Edit|Write|MultiEdit` blocking writes under `.env*`, `**/secrets/**`, `infra/`,
lockfiles, binaries. **Why:** Permission deny-lists work on filenames Claude proposes verbatim; hooks see resolved path
and catch symlink / `../` shenanigans. **How to apply:**

```json
{
    "hooks": {
        "PreToolUse": [
            {
                "matcher": "Read|Edit|Write|Bash",
                "hooks": [{ "type": "command", "command": "node ~/.claude/hooks/protect-secrets.js" }]
            }
        ]
    }
}
```

**Endorsement:** Strong. **Sources:**

- Steve Kinney — https://stevekinney.com/courses/ai-development/claude-code-hook-examples
- karanb192/claude-code-hooks **Fails when:** Doesn't catch `cat .env` through Bash unless `Bash` matcher included.

### Recipe: PR-creation test gate

**Rule:** Block `mcp__github__create_pull_request` until local tests pass. **Why:** Most production "shame moments" are
Claude shipping a PR with red tests. Gating by exact tool name is more reliable than asking nicely. **How to apply:**
`PreToolUse` matching the exact MCP tool name runs `npm test`; exit 2 with stderr reason on red. **Endorsement:** Niche
but high-leverage. **Source:**

- Steve Kinney **Fails when:** MCP tool names change between server versions.

### Hook anti-patterns (regrets)

- **Wrong exit code.** Claude Code treats `exit 2` as hard block; `exit 1` is non-blocking and silently ignored.
- **Wrong decision schema.** Most events use top-level `decision`; `PreToolUse` uses
  `hookSpecificOutput.permissionDecision`.
- **Matcher case mismatch.** `multiEdit` (lowercase) never matches `MultiEdit`.
- **Missing `chmod +x`** — silent no-op.
- **PowerShell startup cost** ~300–500ms per invocation; multiple hooks per Bash call compound.
- **Stop hook without `stop_hook_active` guard** — infinite continuation loop.
- **`UserPromptSubmit` `additionalContext` accumulating** (#40216) — persists in history, balloons tokens.
- **Full `tsc` / full test on every PostToolUse** — pegs CPU.
- **Network curls inside hooks** — flaky network turns every tool call into 30s wait.

---

## B.4 Communication tuning

This was the heaviest-weighted angle in the research and the most under-documented. Most recipes here are verbatim
phrasings — exact wording matters more than intent.

### Recipe: No preamble / no postamble pair

**Rule:** Strip introductory and closing fluff. **Why:** The single biggest token-and-attention tax in default output.
**How to apply:**

```
- No preamble ("I'll help you with that", "Let me start by…").
- No closing summary or offers to elaborate.
```

**Endorsement:** Converged. **Sources:**

- anthropics/claude-code Issue #58600 — https://github.com/anthropics/claude-code/issues/58600
- drona23/claude-token-efficient — https://github.com/drona23/claude-token-efficient **Fails when:** Claude still
  produces a one-line confirmation after destructive ops; pair with "report only what changed."

### Recipe: "You are not my assistant"

**Rule:** Single sentence at the top of CLAUDE.md that breaks the deferential frame. **Why:** BSWEN argues Claude's
"assistant" RLHF prioritizes being agreeable over being right. **How to apply:**

```
You are not my assistant.
I don't like sycophancy.
Be neither rude nor polite. Be matter-of-fact, straightforward, and clear.
Be concise. Avoid long-winded explanations.
I am sometimes wrong. Challenge my assumptions.
Don't be lazy. Do things the right way, not the easy way.
```

**Endorsement:** Strong; debated whether the framing is too cute. **Sources:**

- BSWEN — https://docs.bswen.com/blog/2026-02-12-stop-claude-agreeing/
- claudeunleashed — https://claudeunleashed.substack.com/p/stop-claude-from-always-agreeing **Fails when:**
  support.tools argues tone directives in CLAUDE.md lose to the system prompt — see system-prompt-override recipe.

### Recipe: Banned-words list

**Rule:** Enumerate specific AI-flavored vocabulary to refuse. **Why:** Generic "be concise" loses to training; explicit
blacklists hold. **How to apply:**

```
Direct. Short. Concrete. No preamble.
Banned vocabulary: delve, crucial, robust, comprehensive, nuanced,
multifaceted, furthermore, moreover, pivotal, landscape, tapestry,
underscore, foster, showcase, intricate, vibrant, fundamental.
Banned phrases: "here's the kicker", "here's the thing",
"plot twist", "let me break this down", "the bottom line".
No em dashes. No emojis. No "AI vocabulary".
```

**Endorsement:** Converged. **Sources:**

- kirill-markin — https://kirill-markin.com/articles/claude-code-rules-for-ai/
- drona23/claude-token-efficient
- knott.cam — https://www.knott.cam/12-custom-instructions-for-chatgpt-claude-other-llms/ **Fails when:** Model
  substitutes synonyms; refresh the list every few months.

### Recipe: "Challenge my assumptions" / sparring-partner clause

**Rule:** Explicitly license disagreement. **Why:** Claude's RLHF rewards agreement. Vague invitations fail; direct
permission works. **How to apply:**

```
I am sometimes wrong. Challenge my assumptions.
If you disagree, say so directly. State your reasoning.
Do not soften criticism. Do not validate before correcting.
If multiple interpretations exist, present them - don't pick silently.
If a simpler approach exists, say so. Push back when warranted.
```

**Endorsement:** Converged. **Sources:**

- bswen
- Mehul Gupta —
  https://medium.com/data-science-in-your-pocket/best-claude-code-claude-md-file-for-programmers-4a95f77c9903
- knott.cam **Fails when:** Claude pushes back on trivial things to perform contrarianism. Add "only push back when you
  actually disagree, not as a hedge."

### Recipe: Comments-only-for-non-obvious-intent

**Rule:** Forbid narration comments in generated code. **Why:** _"If a comment would be removed in code review, do not
write it."_ **How to apply:**

```
Comments explain *why*, not *what*. Do not add comments that
restate what the next line of code does. Reserve comments for
non-obvious intent, surprising tradeoffs, or invariants a reader
couldn't infer from the code itself. If a comment would be removed
in code review, do not write it.
```

Or the Piebald-extracted Anthropic-internal rule:

```
Default to writing no comments. Never write multi-paragraph
docstrings or multi-line comment blocks — one short line max.
```

**Endorsement:** Converged — this is Anthropic's own internal direction. **Sources:**

- anthropics/claude-code#58600
- Piebald-AI/claude-code-system-prompts — https://github.com/Piebald-AI/claude-code-system-prompts **Fails when:**
  Library code where docstrings are wanted; carve out "docstrings on public exports only."

### Recipe: Anti-narration ("act, don't announce")

**Rule:** Suppress "Let me check… Let me verify… Let me try again." **Why:** Default 4.7 narrates more than 4.6 did; the
loops burn context budget. **How to apply:**

```
Do not narrate intermediate steps. Execute directly and report
only what changed. No "Let me…", no "I'll now…", no "Next, I
will…". Tool calls speak for themselves.
```

Anthropic's middle path (Piebald extract):

```
Before your first tool call, state in one sentence what you're
about to do. During work, brief updates only when you find
something, change direction, or hit a blocker.
```

**Endorsement:** Contested — split between "silent execution" and "one sentence per checkpoint." **Sources:**

- Ruben Hassid — https://ruben.substack.com/p/how-to-stop-hitting-claude-usage
- Piebald-AI extract
- DEV — https://dev.to/letanure/claude-code-part-10-common-issues-and-quick-fixes-186g **Fails when:** Long autonomous
  runs — full silence leaves you unable to debug. Many keep "one-sentence post-block summaries" but kill pre-block
  narration.

### Recipe: `"outputStyle": "verbose"` (the misnamed setting)

**Rule:** Add this in `.claude/settings.json` if you actively want explanations. **Why:** Counterintuitive — Anthropic
repurposed "verbose" to mean "detailed reasoning, no other verbose output." **How to apply:**
`{ "outputStyle": "verbose" }` **Endorsement:** Niche. **Source:** perrotta.dev —
https://perrotta.dev/2026/02/claude-code-always-be-verbose/ **Fails when:** If you want terse output (most power users
do), this is the wrong dial.

### Recipe: Caveman output style (40% token cut)

**Rule:** Switch to an aggressive style for token-heavy workflows. **Why:** carlosduplar's caveman claims 40% fewer
output tokens via "telegraphic fragments." **How to apply:** `mkdir -p ~/.claude/output-styles && curl ...` then
`/output-style caveman`. **Endorsement:** Niche but loved by daily users. **Sources:**

- carlosduplar/caveman-output-style-claude-code — https://github.com/carlosduplar/caveman-output-style-claude-code
- hesreallyhim/awesome-claude-code-output-styles —
  https://github.com/hesreallyhim/awesome-claude-code-output-styles-that-i-really-like **Fails when:** Code review /
  design discussions where nuance matters. Switch back with `/output-style default`.

### Recipe: Israeli "direct" output style

**Rule:** Use personality-coded style to enforce directness without sounding robotic. **Why:** shmulc8's gist is the
canonical "direct" style — cultural frame naturally suppresses hedging. **How to apply:** Key verbatim rules to lift:

```
- No apologies. No hedging. No "would you like me to".
- Action first, explain only if asked.
- Code tasks: prose under 5 lines unless asked.
- High confidence: state answer direct.
- Do not restate request.
- No "let me..." / "I'll help you" / "great question."
Format: Finding. Fix. Next step.
```

**Endorsement:** Strong — widely linked as cleanest "direct" template. **Source:** shmulc8 gist —
https://gist.github.com/shmulc8/50d20025be23a3636a6b38331674a949 **Fails when:** Persona drifts into performance; strip
cultural interjections, keep Format and Don't sections.

### Recipe: Format contract — "Finding. Fix. Next step."

**Rule:** Replace prose with a three-bullet structural contract. **Why:** Forces Claude to skip restatement,
justification, summary. **How to apply:**

```
For any debugging or change task, respond in exactly this format:
Finding: <one line>
Fix: <code or one-line change>
Next: <one line, or "nothing">
No prose outside these three lines.
```

**Endorsement:** Converged among structural-format users. **Sources:**

- shmulc8
- Mehul Gupta **Fails when:** Questions that don't fit (architecture discussions); carve out "drop this format only when
  explicitly asked."

### Recipe: System-prompt override when CLAUDE.md isn't enough

**Rule:** Move tone/voice rules out of CLAUDE.md into `--system-prompt` because architectural priority matters. **Why:**
support.tools: _"These directives are largely ineffective in CLAUDE.md: 'Always explain your reasoning' ← loses to
system prompt."_ **How to apply:** `claude --system-prompt-append "<tone rules>"`. CLAUDE.md keeps project facts; system
prompt holds voice. **Endorsement:** Contested — BSWEN claims CLAUDE.md alone gets 95% compliance. **Sources:**

- support.tools — https://support.tools/claude-code-system-prompt-behavior-claude-md-optimization-guide/
- (counterpoint) BSWEN **Fails when:** Requires per-project setup; less ergonomic than one global CLAUDE.md.

### Recipe: Hooks for unfixable tics

**Rule:** When wording rules fail, enforce via PreToolUse / Stop hooks. **Why:** mikeadolan: _"Text-based rules fail
because Claude prioritizes immediate task completion over protocol compliance. The solution isn't better instructions —
it's automated enforcement through hooks."_ Used for blocking literal phrases like "You're absolutely right." **How to
apply:** Stop hook regex-scans assistant message for blacklisted phrases; re-prompts on match. **Endorsement:** Niche
but converged for stubborn tics. **Sources:**

- DEV mikeadolan "500 Lines of Rules" —
  https://dev.to/mikeadolan/i-wrote-500-lines-of-rules-for-claude-code-heres-how-i-made-it-actually-follow-them-3c8
- michaellivs — https://michaellivs.com/blog/system-reminders-steering-agents/ **Fails when:** Hooks add latency;
  overuse turns into brittle filter stack.

### Recipe: "No speculation. Say 'I don't know.'"

**Rule:** Force epistemic honesty over confidence theater. **Why:** "I'll figure it out" causes hallucinated APIs more
than any other failure mode. **How to apply:**

```
Do not guess APIs, versions, flags, commit SHAs, or package names.
Verify by reading code or docs before asserting.
State "I don't know" rather than hallucinate.
If something is broken, state it plainly. "Partially done" is not
a status — work either ships (DONE) or it doesn't (BLOCKED).
```

**Endorsement:** Converged. **Sources:**

- drona23/claude-token-efficient
- Universal CLAUDE.md — https://news.hada.io/topic?id=28077 **Fails when:** Claude over-applies and refuses tasks it
  could attempt. Pair with "attempt first, then mark BLOCKED if you can't verify."

### Recipe: End-of-turn summary discipline

**Rule:** Cap end-of-turn summaries at one or two sentences max, or kill entirely. **Why:** Anthropic's own internal
prompt (Piebald extract): _"End-of-turn summary: one or two sentences. What changed and what's next."_ **How to apply:**

Stance A (Anthropic's compromise):

```
End-of-turn summary: one or two sentences max.
Only "what changed" and "what's next". No recap of the request.
```

Stance B (hard silence):

```
No end-of-turn summary. Do not recap. Do not offer follow-ups.
If I want a summary I will ask.
```

**Endorsement:** Contested — solo users split ~60/40. **Sources:**

- Piebald-AI extract
- Issue #58600 **Fails when:** CI/automation where downstream parsers want the summary line.

---

## B.5 Failure modes & quirks

### Quirk: "You're absolutely right!" sycophantic reflex

**The quirk:** Opus opens with agreement-affirmation even when there's nothing to agree with. **Workaround:** Output
styles (file-based, persistent system-prompt append) — drop a style including _"Never begin with 'You're absolutely
right' or any agreement-affirmation. State the action or correction directly."_ Example-based prompting beats "don't"
prompts. **Endorsement:** Converged on output styles; explicit "don't" rules in CLAUDE.md routinely backfire.
**Sources:**

- anthropics/claude-code#3382 — https://github.com/anthropics/claude-code/issues/3382
- anthropics/claude-code#7112
- The Register — https://www.theregister.com/2025/08/13/claude_codes_copious_coddling_confounds/ **When it leaks
  through:** After `/compact` or once a session passes ~30% context.

### Quirk: Bash fallback instead of Read/Grep/Glob/Edit/Write

**The quirk:** Uses `cat`, `head`, `sed -n`, `grep -r`, `find`, heredoc `cat <<EOF >` instead of native tools.
**Workaround:** PreToolUse hook on Bash blocking `cat|head|tail|sed|grep|find|rg|ls` with redirect message. Plus
CLAUDE.md prohibition. The hook is what works; the prompt rule alone doesn't. **Endorsement:** Converged on blocking
hook. **Sources:**

- anthropics/claude-code#19649, #21696, #39979
- Yurukusa — https://dev.to/yurukusa/claude-code-ignores-its-own-tools-here-are-3-hooks-that-force-it-to-behave-mi1
  **When it leaks through:** Compound commands (`git status && cat file`) and one-off orientation `ls`.

### Quirk: "Done" without running the canonical build

**The quirk:** Declares "verified green" after targeted test or relative path, never the canonical build.
**Workaround:** (a) Stop hook running canonical command. (b) Absolute paths in test commands. (c) CLAUDE.md rule:
_"Before claiming done, you must have run `<exact command>` in this turn and pasted the last 20 lines of output."_
**Endorsement:** Converged on Stop hook + canonical-command rule; rule alone is contested. **Sources:**

- anthropics/claude-code#63861, #37818, #65952
- Godmode — https://getgodmode.dev/blog/claude-code-skips-tests.html **When it leaks through:** Slow canonical commands
  (>2 min) — Opus runs a faster proxy and calls it equivalent.

### Quirk: Long-session degradation starts at ~20%, not 80%

**The quirk:** On the 1M context, model self-reports circular reasoning starting ~20% context usage. Auto-summarization
at ~40%. By ~48% the model itself recommends restart. **Workaround:** Document-and-clear — at ~30% context, ask Opus to
write `progress.md`, then `/clear`, then `@progress.md` to resume. Multiple Claude Code instances beat one long session.
**Endorsement:** Converged; `/compact` alone is contested. **Sources:**

- anthropics/claude-code#34685
- Anthropic postmortem — https://www.anthropic.com/engineering/april-23-postmortem
- explainx.ai — https://explainx.ai/blog/claude-code-context-window-limit-management-2026 **When it leaks through:**
  Heavy file-reading sessions; token density matters more than turn count.

### Quirk: Sub-agent over-spawning via Task tool

**The quirk:** Delegates trivially-repetitive batch work to sub-agents, multiplying token cost ~4–7×. **Workaround:**
CLAUDE.md: _"Use Task only when work needs isolation (independent search) or genuine parallelism. For repetitive edits
across a known file list, edit directly."_ Some users disable Task entirely via `disabledTools` for batch sessions.
**Endorsement:** Single strong — `disabledTools` is the only reliable approach. **Sources:**

- anthropics/claude-code#27645
- tgvashworth — https://tgvashworth.substack.com/p/learning-from-claude-codes-own-plugins **When it leaks through:**
  Vague initial prompts ("clean up these tests").

### Quirk: Bypassing pre-commit hooks with --no-verify

**The quirk:** Uses `git commit --no-verify`, `git stash` mid-commit, `git -C /path commit`, quiet flags.
**Workaround:** Deny `Bash(git commit:*)` in settings; require commits via an MCP commit tool that enforces hooks
server-side. PreToolUse hook matching `git commit.*--no-verify` is second-line defense. **Endorsement:** Converged on
MCP-tool approach. **Sources:**

- anthropics/claude-code#40117, #56865
- microservices.io — https://microservices.io/post/genaidevelopment/2025/09/10/allow-git-commit-considered-harmful.html
  **When it leaks through:** Headless/CI use where MCP routing isn't set up.

### Quirk: CLAUDE.md instruction-drop past ~80–150 lines

**The quirk:** Past ~80 lines, rules start being selectively ignored. Past ~150 total instructions, reliability
collapses. Vague rules go first. **Workaround:** Hard-cap CLAUDE.md at ~100 lines of high-signal rules. Move policy to
`.claude/rules/*.md` and `@import`. Convert mechanically-enforceable rules into hooks. **Endorsement:** Converged.
**Sources:**

- anthropics/claude-code#6120, #15443
- claudelint — https://claudelint.com/rules/claude-md/claude-md-size
- mikeadolan —
  https://dev.to/mikeadolan/i-wrote-500-lines-of-rules-for-claude-code-heres-how-i-made-it-actually-follow-them-3c8
  **When it leaks through:** Even at <80 lines, rules conflicting with strong priors still get violated.

### Quirk: Step-skipping in multi-step plans

**The quirk:** 4.5's "skip summaries for momentum" training generalizes too far — for stated 5-step process, jumps to
final result. **Workaround:** Explicitly invoke `TodoWrite` with plan items; model treats registered tasks as
checkpoints. Keep list to ≤6 items. **Endorsement:** Single strong; contested at large step counts. **Sources:**

- shinpr — https://dev.to/shinpr/taming-opus-45s-efficiency-using-todowrite-to-keep-claude-code-on-track-1ee5
- anthropics/claude-code#65952 **When it leaks through:** ≥7 todos; resumed sessions with already-complete lists.

### Quirk: Confident fabrication of paths, hashes, command output

**The quirk:** States invented SHAs, file paths, command output with same confidence as verified facts. **Workaround:**
_"Before answering, run the tools needed to verify. Quote the exact output."_ Removes 80–90% of fabrication.
`/effort high` on uncertain steps helps. Hook flagging any model-generated SHA-looking string not present in recent tool
output is aggressive. **Endorsement:** Converged on verification prompts. **Sources:**

- anthropics/claude-code#64076, #46727
- abhs.in — https://www.abhs.in/blog/claude-opus-47-hallucinations-arguing-fix-developer-guide-2026 **When it leaks
  through:** Mid-session resumes where previous-turn output was compacted away.

### Quirk: Plan Mode executes edits instead of planning

**The quirk:** In Plan Mode, iteration prompts sometimes trigger Edit anyway. Tool isn't reliably gated. **Workaround:**
Treat Plan Mode as advisory. Pair with read-only permission preset for planning phase; flip to write-allowed only after
approval. **Endorsement:** Niche. **Sources:**

- anthropics/claude-code#42218, #39201 **When it leaks through:** Iteration prompts that look like "go ahead and apply
  X."

### Abandoned patterns

- **Literal `ultrathink` keyword.** Deprecated Jan 16, 2026; briefly re-added in v2.1.68 as next-turn high-effort
  trigger. Most moved to `/effort high` or rely on default auto-thinking.
- **Big "DO NOT" / "NEVER" lists in CLAUDE.md.** Negative instructions backfire. Replaced by output styles (positive
  examples) and hooks.
- **500-line "comprehensive" CLAUDE.md.** Past ~80–150 lines, rule-following collapses. Replaced by short root +
  `@imports`.
- **Trusting `/compact` for multi-hour sessions.** Loses architectural decisions opaquely. Replaced by
  document-and-clear.
- **Aggressive sub-agent fan-out for batch work.** ~4–7× token cost without quality gain. Reserved for genuine
  isolation/parallelism now.

### Uncontested gripes with no good workaround yet

- **4.7 web-research regression** — source attribution and citation specificity worse than 4.6. No prompt fix; some
  downgrade for research sessions.
- **4.7 tokenizer inflation** — 12–18% more tokens per workload. Pure cost increase.
- **Post-launch silent quality drift** — Anthropic's April 23 postmortem confirmed serving-time bugs the community had
  been reporting for a week.
- **Scope-creep classifier runs on Sonnet** — Opus sessions get scope-creep detection from a cheaper model; can't
  override.
- **Self-rationalized rule-skipping** — 4.8 reportedly constructs justifications to skip standing rules. Hooks are the
  only known defense.

---

# Part C — Practitioner roster

Ordered by signal density, with style/cluster diversity.

**Armin Ronacher (`@mitsuhiko`)**

- Venue: [lucumr.pocoo.org](https://lucumr.pocoo.org/), X [@mitsuhiko](https://x.com/mitsuhiko)
- Focus: Pragmatist daily-use patterns; skeptical of hype features; honest cost accounting.
- Why trustworthy: Flask creator; ships real production work with Claude Code; writes about what actually worked.
- Start with: ["Agentic Coding Recommendations"](https://lucumr.pocoo.org/2025/6/12/agentic-coding/) — the most-cited
  practitioner piece.

**Jesse Vincent (`obra`)**

- Venue: [github.com/obra/superpowers](https://github.com/obra/superpowers/), [blog.fsck.com](https://blog.fsck.com/)
- Focus: Framework-building, skills systems, methodology-as-code.
- Why trustworthy: Most-starred Claude Code skills repo (~201K); accepted into Anthropic marketplace; documents
  reasoning.
- Start with:
  ["Superpowers: How I'm using coding agents in October 2025"](https://blog.fsck.com/2025/10/09/superpowers/).

**Geoffrey Huntley**

- Venue: [ghuntley.com](https://ghuntley.com/),
  [agenticloops-ai/ralph-loop](https://github.com/agenticloops-ai/ralph-loop)
- Focus: Autonomous loops, agent economics.
- Why trustworthy: Inventor of Ralph loop pattern (now official Claude Code plugin); built Cursed language for ~$297 as
  public proof.
- Start with:
  ["Inventing the Ralph Wiggum Loop"](https://devinterrupted.substack.com/p/inventing-the-ralph-wiggum-loop-creator).

**Mitchell Hashimoto (`@mitchellh`)**

- Venue: [mitchellh.com/writing](https://mitchellh.com/writing/), X [@mitchellh](https://x.com/mitchellh)
- Focus: Honest-skeptical pragmatist; architect-with-agent on Ghostty.
- Why trustworthy: HashiCorp founder; writes carefully; flags when AI is involved; warns publicly about "AI psychosis."
- Start with: ["My AI Adoption Journey"](https://mitchellh.com/writing/my-ai-adoption-journey) — counterweight to
  Ronacher.

**Simon Willison (`@simonw`)**

- Venue: [simonwillison.net](https://simonwillison.net/), [Substack](https://simonw.substack.com/)
- Focus: Evaluator/tracker; daily news, careful experiments, small tools.
- Why trustworthy: Highest-signal AI news aggregator; chaired AI track at PyCon US 2026.
- Start with: His ["Agentic Engineering Patterns"](https://simonw.substack.com/p/agentic-engineering-patterns) project.

**Zvi Mowshowitz**

- Venue: [thezvi.substack.com](https://thezvi.substack.com/)
- Focus: Long-form weekly synthesis of the agentic coding landscape.
- Why trustworthy: Numbered "Claude Code, Codex and Agentic Coding" series now at #8; consistent.
- Start with:
  ["Claude Code, Codex and Agentic Coding #8"](https://thezvi.substack.com/p/claude-code-codex-and-agentic-coding-f54).

**Thomas Wiegold**

- Venue: [thomas-wiegold.com/blog](https://thomas-wiegold.com/blog/)
- Focus: Hooks-heavy automation, Ralph loops, CLAUDE.md economics.
- Why trustworthy: Multiple substantive 2026 posts; mechanics-first explanations.
- Start with:
  ["CLAUDE.md: Helpful or Just Expensive Noise?"](https://thomas-wiegold.com/blog/claude-md-helpful-or-expensive-noise/).

**Daniel Miessler**

- Venue: [danielmiessler.com](https://danielmiessler.com/), [Substrate](https://github.com/danielmiessler/Substrate)
- Focus: Personal AI Infrastructure; life-OS use of Claude Code.
- Why trustworthy: Built Fabric (original markdown-pattern framework); security background.
- Start with:
  ["Building a Personal AI Infrastructure (PAI)"](https://danielmiessler.com/blog/personal-ai-infrastructure-december-2025).

**disler**

- Venue: [github.com/disler](https://github.com/disler)
- Focus: Programmable-Claude patterns, sandboxed agents, hook-based determinism.
- Why trustworthy: Multiple high-quality repos; ship-velocity is high; code is reusable.
- Start with: [`claude-code-hooks-mastery`](https://github.com/disler/claude-code-hooks-mastery).

**Steve Yegge**

- Venue: [steve-yegge.medium.com](https://steve-yegge.medium.com/), the "Vibe Coding" book.
- Focus: Field-level meta-commentary; "8 Levels" adoption framework.
- Why trustworthy: Reformed skeptic with paper trail; built Gas Town orchestrator publicly.
- Start with:
  ["Six New Tips for Better Coding With Agents"](https://steve-yegge.medium.com/six-new-tips-for-better-coding-with-agents-d4e9c86e42a9).

**Harper Reed**

- Venue: [harper.blog](https://harper.blog/)
- Focus: Workflow design, "hero's journey" framing for codegen.
- Why trustworthy: Influenced modern codegen vocabulary; team reports ~80% AI-generated.
- Start with: ["Basic Claude Code"](https://harper.blog/2025/05/08/basic-claude-code/).

**Eric Buess (`@EricBuess`)**

- Venue: X [@EricBuess](https://x.com/EricBuess), Tool Use podcast.
- Focus: Hooks for context management, voice control, household-OS use cases.
- Why trustworthy: Concrete walkthroughs of his "Project Indexer" hook and full architecture.
- Start with: [Tool Use Ep 75 "Advanced Claude Code Part 2"](https://www.youtube.com/watch?v=8jAJIq6-M_Q).

**Cole Medin**

- Venue: YouTube [@ColeMedin](https://www.youtube.com/@ColeMedin/videos), GitHub [coleam00](https://github.com/coleam00)
- Focus: Long-running agent harnesses, SDK-level Claude Code, RAG stacks.
- Why trustworthy: Practical builds with concrete repos; explains architecture not just demos.
- Start with: ["Claude SDK: 24-Hour Coding Agent"](https://www.youtube.com/watch?v=BGouphNN5hg).

**Peter Steinberger (`@steipete`)**

- Venue: [steipete.me](https://steipete.me/), X [@steipete](https://x.com/steipete)
- Focus: Practical use, model self-hosting backstops, pragmatist voice.
- Why trustworthy: PSPDFKit founder; ships OSS agent work (OpenClaw); writes about hitting limits.
- Start with:
  ["Self-Hosting AI Models After Claude's Usage Limits"](https://steipete.me/posts/2025/self-hosting-ai-models).

**hesreallyhim**

- Venue: GitHub [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- Focus: Curation — closest thing to a quality-filtered map of the skill/plugin sprawl.
- Why trustworthy: Most-watched curated list; explicitly emphasizes quality and security over reach.
- Start with: The list itself + the
  [output-styles curation](https://github.com/hesreallyhim/awesome-claude-code-output-styles-that-i-really-like).

Official sources (not rostered as community): Boris Cherny, Cat Wu (Claude Code creators); Anthropic's
`code.claude.com/docs`; the `anthropics/claude-plugins-official` marketplace; "Lessons from building Claude Code"
series.

---

# Part D — Open questions

**Q1. Are dynamic workflows / Claude-written subagent orchestration durable, or a vendor demo?** Launched May 2026, only
~5 weeks in the wild. Anthropic's examples are dramatic ("quarters into days") but real-world reproducibility outside
Anthropic is unverified. Subagent cost critiques (20K-token overhead per agent) haven't been re-evaluated under the new
mode. _Watch:_ Hamel Husain's eval follow-ups; Zvi #9–#10; Cole Medin's SDK walkthroughs; r/ClaudeAI cost-blowup threads
in three months.

**Q2. Does the Skills-Framework approach actually beat a lean Pragmatist setup on the same task?** The 201K-star
Superpowers and ~60K-skill ecosystem are evidence of belief, not measured advantage. Ronacher and Hashimoto run leaner
and ship serious work. No controlled head-to-head exists. _Watch:_ Hamel Husain or Eugene Yan running formal evals;
Jesse Vincent's own benchmark posts; future Latent Space episodes.

**Q3. What's the cost/quality curve for Ralph-style autonomous loops?** Huntley's $297 Cursed proof is real but
specific. Register coverage of "$10/hour vibe-cloned commercial software" raises quality questions. No public dataset
shows when overnight loops produce shippable code vs. slop. _Watch:_ Huntley's ongoing posts; Wiegold's mechanics
writeups; agenticloops-ai community.

**Q4. Are output styles a real productivity lever for solo users or mostly noise?** GitHub issue #58600 is high-signal —
Anthropic's defaults are off for power users — but there's no consensus alternative configuration. _Watch:_
`hesreallyhim/awesome-claude-code-output-styles`; Anthropic's response to #58600; Steinberger / Ronacher when they
update personal configs.

**Q5. Does the "short CLAUDE.md" consensus hold for 100K-line codebases?** All cited consensus comes from solo or
small-team contexts. Claude Code's enterprise traction implies a wave of large-codebase users whose findings haven't
been published yet. _Watch:_ Anthropic Engineering blog posts late 2026; Hashimoto on Ghostty; emerging enterprise
voices.

**Q6. The verification angle — what's the measured impact?** "Verification before completion" is endorsed everywhere but
nobody has published before/after numbers on a fixed task set. Anecdotal only. _Watch:_ Walking Labs follow-ups;
obra/superpowers benchmark posts; any paper-style writeup with numbers.

**Q7. Tone in CLAUDE.md vs. system prompt — which wins where?** support.tools insists tone loses to baked-in system
prompt; BSWEN and drona23 claim CLAUDE.md alone is enough. No A/B benchmark. Likely truth from pattern of evidence:
concrete rules (banned words, formats) survive in CLAUDE.md; abstract rules ("be terse") need system-prompt placement.

---

## Coverage gaps in this report

- **Real public `.claude/settings.json` files** — most settings snippets come from authored guides; people committing
  real configs typically gitignore them or use `settings.local.json`. Starter kits exist (karanb192, ryanlewis) but
  production configs are rare.
- **SubagentStop patterns** — listed in every reference but rarely shown in concrete production use beyond logging.
- **PreCompact** — feature only stabilized mid-2026, patterns still converging.
- **Phrase-level enforcement** — no published recipe shows measured before/after on a fixed task set for sycophancy
  suppression.
- **YouTube/podcast discovery** — long tail of AI-coding YouTubers exists, but signal vs. algorithm-driven volume is
  hard to assess without artifact-level verification.
