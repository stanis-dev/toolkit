# Prompt & Skill Engineering Principles

Reference for the skill-engineer skill. Distilled from Claude Code CLI source analysis
and 2025-2026 research.

---

## Core Axioms

1. **Constraints drive quality.** Research on production prompt frameworks found constraints
  are the single largest driver of output quality (~40%), with format second (~25%). Allocate
   50% of token budget to constraints + format, 40% to context + data, 10% to persona + task.
2. **The description is the discovery surface.** Only `name`, `description`, and `when_to_use`
  enter the model's context for skill selection. The body loads only after activation. If the
   skill never activates, perfect instructions are worthless. Write the description first.
3. **250-character cap on the listing entry.** Combined `description + when_to_use` is truncated
  at 250 characters in the skill listing. Write dense, trigger-rich text within this budget.
4. **Binary criteria outperform subjective scales.** For automated improvement loops, strict
  yes/no criteria reduce probability noise vs 1-5 Likert scales. Every step in a skill should
   have a testable done condition.
5. **Numeric anchors beat qualitative instructions.** "Keep text to 25 words" produces 1.2% better
  compliance than "be concise." Use specific numbers for length, counts, and formats. Reserve
   qualitative language for tone and judgment.
6. **Examples over adjectives.** One good example beats five adjectives describing desired behavior.
  Anthropic's official guidance: 3-5 examples for best results.
7. **Instruction position matters.** Models exhibit primacy and recency effects. Place the most
  critical instructions at the beginning and end of the skill. Avoid burying important
   constraints in the middle.
8. **The instruction ceiling.** Model compliance degrades as instruction count increases. As a
  practical heuristic, treat ~150 distinct instructions as a soft ceiling. Exact threshold
   varies by model and instruction complexity. Prioritize ruthlessly.
9. **Skills can be net-negative.** A 138-repo study found LLM-generated context files reduced
  agent success rates by 20%. More instructions does not equal better outcomes. Every token
   in a skill must justify its existence.

---

## Structural Patterns

### The Canonical Skill Structure

```
---
name: skill-name
description: >-
  Dense trigger-rich description under 250 chars. Includes WHAT it does and WHEN to use it.
---

# Title

One-line summary.

## Workflow
1. Phase/step with binary done condition
2. ...

## Constraints
- Specific, testable prohibitions (40-50% of content)

## Examples
### GOOD
...
### BAD (with reasoning for WHY it's bad)
...

## Anti-Patterns
| Temptation | Reality |
| --- | --- |

## Interaction Rules
- When to ask vs when to act

## Output Template (if applicable)
```

### Defense in Depth

Never rely on instructions alone for critical constraints. Enforce through multiple layers:

- **Layer 1**: Instructional text says "don't do X"
- **Layer 2**: Structural mechanisms prevent X (verification gates, tool restrictions)
- **Layer 3**: Recurring micro-reminders reinforce "you cannot do X"

### Anti-Pattern Inoculation

Name the model's failure modes and rationalizations explicitly before they occur.
Structure: "You will feel the urge to [specific shortcut]. The exact excuse you reach for
is [verbatim rationalization]. Do the opposite."

This is metacognitive inoculation — the model can't deploy a rationalization it just read
is a documented failure pattern.

### Bidirectional Calibration

Every constraint should fight BOTH the error AND its overcorrection:

- "Don't claim tests pass when they fail" paired with "Don't hedge confirmed results
with unnecessary disclaimers"
- Frame the calibrated target: "The goal is an accurate report, not a defensive one."

### GOOD/BAD Example Pairs

The most effective teaching format. Structure:

```
### GOOD — {label}
{example}
Reasoning: {why this works}

### BAD — {label}
{example}
Reasoning: {why this fails — name the SPECIFIC failure, not just "this is wrong"}
```

### Sparse/Full Reminder Pattern

For multi-turn skills, send full behavioral instructions once, then use abbreviated
"reminder" versions on subsequent turns. The sparse version references the full version:
"See full instructions earlier. Key invariants: [list]."

This cuts token cost by ~90% on intermediate turns while maintaining behavioral consistency.

---

## Skill Frontmatter Fields


| Field                      | Required | Effect                                                                       |
| -------------------------- | -------- | ---------------------------------------------------------------------------- |
| `name`                     | yes      | Slash-command name (directory name if omitted)                               |
| `description`              | yes      | Discovery text — the ONLY thing the model sees before activation             |
| `when_to_use`              | no       | Appended to description in listing. High-ROI for auto-activation.            |
| `allowed-tools`            | no       | Tool permission patterns auto-granted during execution                       |
| `arguments`                | no       | Named args for `$name` substitution in body                                  |
| `argument-hint`            | no       | Shown in autocomplete: `/skill [hint]`                                       |
| `model`                    | no       | Override model (haiku, sonnet, opus). `inherit` = no override.               |
| `user-invocable`           | no       | Whether user can type `/skill-name` (default: true)                          |
| `disable-model-invocation` | no       | If true, model cannot auto-invoke (default: false)                           |
| `context`                  | no       | `inline` (interactive, default) or `fork` (isolated subagent)                |
| `agent`                    | no       | Agent type when forked                                                       |
| `effort`                   | no       | `low`/`medium`/`high`/`max` — controls thinking depth                        |
| `paths`                    | no       | Gitignore-style globs — skill activates only when matching files are touched |
| `hooks`                    | no       | PreToolUse/PostToolUse/Stop handlers (triggers permission prompt)            |
| `shell`                    | no       | `bash` or `powershell` for `!` blocks                                        |


### Description Writing Guide

The description field is the highest-leverage text in any skill. It must include:

- **WHAT** the skill does (capability)
- **WHEN** to use it (trigger conditions, example phrases)
- **WHEN NOT** to use it (anti-triggers — equally important for reducing false activations)

Format: third person, present tense. "Creates X when Y. Use for Z. Not for W."

---

## Anti-Pattern Catalog

Common skill design failures with fixes.


| Anti-pattern                                | Why it fails                                                           | Fix                                                                             |
| ------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Prose paragraphs without commands           | Agents read them, represent them as vague preferences, and ignore them | Use imperative commands with specific tools/actions                             |
| Ambiguous directives ("be careful")         | "Careful" isn't a constraint. No verification mechanism.               | Replace with testable condition: "If X, then STOP and ask"                      |
| Contradictory priorities without resolution | Agents skip verification entirely when instructions conflict           | Add explicit priority ordering: "When X conflicts with Y, prefer X"             |
| Style guides without enforcement            | "Follow Google style" gives no mechanism to verify compliance          | Add enforcement command: "Run `ruff check --select D`"                          |
| Instructions exceeding 500 lines            | Context saturation, instruction dropping                               | Split into SKILL.md + references/. Front-load critical instructions.            |
| Description that just restates the name     | Zero discovery signal — model can't match user intent to skill         | Write trigger phrases: "Use when user asks to deploy, push to staging, or test" |
| "CRITICAL: MUST" everywhere                 | Claude 4.6 overtriggers on aggressive language. Causes overcorrection. | Use measured natural language. Save emphasis for true invariants.               |
| Constraints only say what TO do             | Missing the "when NOT" clause. Causes false activations.               | Add explicit anti-triggers and prohibited behaviors.                            |


---

## Platform Differences


| Feature                | Claude Code                            | Cursor                  | Codex                   |
| ---------------------- | -------------------------------------- | ----------------------- | ----------------------- |
| Skill format           | `SKILL.md` in directory                | `SKILL.md` in directory | `SKILL.md` in directory |
| Instruction file       | `CLAUDE.md`                            | `.cursor/rules/*.mdc`   | `AGENTS.md`             |
| Skill location         | `~/.claude/skills/`, `.claude/skills/` | `~/.cursor/skills/`     | `~/.codex/skills/`      |
| Plugin system          | marketplace plugins                    | built-in + marketplace  | marketplace plugins     |
| Subagents              | built-in typed agents                  | Task tool with types    | cloud-based             |
| Shell in skills        | `!` backtick syntax                    | not supported           | `scripts/` directory    |
| Conditional activation | `paths` frontmatter                    | glob patterns in `.mdc` | not supported           |


When designing cross-platform skills, avoid:

- `!` shell commands (Claude Code only)
- `${CLAUDE_SKILL_DIR}` variable (Claude Code only)
- `allowed-tools` frontmatter (Claude Code only)
- `hooks` frontmatter (Claude Code only)

