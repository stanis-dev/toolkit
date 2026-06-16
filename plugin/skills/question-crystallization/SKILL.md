---
name: question-crystallization
description: >-
    Guide users from vague, pre-articulate intuitions to clearly defined questions, problems, or goals through structured
    exploration. Use when the user has a sense of wanting to explore, decide, build, or understand something but can't
    yet articulate what specifically. Works for research questions, decisions, problem definitions, project ideas, or any
    situation where the starting point is "I know there's something here but I can't name it yet."
---

# Question Crystallization

Guide users from vague intuitions to clearly defined questions, problems, or goals. Works across domains: research,
decisions, problem-solving, project ideation, concept exploration.

## Workflow

```
1. Intuition Anchor  →  2. Dimension Funnel  →  3. Crystallize  →  4. Deliver
```

### Phase 1: Intuition Anchor

Goal: capture the felt sense and establish a broad direction without demanding precision.

**Step 1 -- Open dump.** Invite the user to share whatever they have: fragments, associations, half-formed thoughts,
links, keywords, feelings about a topic. Explicitly say that formatting, coherence, and completeness do not matter. If
they respond with something scattered or associative, affirm it: "There's good signal here -- I see N threads worth
pulling on."

If the user can't produce anything, offer a lowest-effort entry: "Just name the broad area or a single word that's been
on your mind, and I'll give you a few angles to react to."

**Step 2 -- Hypothesis generation.** Synthesize the user's input into 3-4 distinct angles. These might be:
- Research directions ("understand how X works")
- Decisions to frame ("choose between X and Y")
- Problems to define ("figure out why X isn't working")
- Things to build ("create something that does X")
- Concepts to map ("get clarity on the landscape of X")

Present each as a short label + one-sentence description. Frame as "directions we could go" -- not interpretations of
what the user said.

Always include a final option: "None of these -- let me try different angles" or "I want to combine parts of these."

**Step 3 -- Lock anchor.** Once the user selects or shapes a direction, confirm it in one sentence and move to Phase 2.
If they reject everything, ask what felt wrong about the options (this narrows the space) and generate a new set.

### Phase 2: Dimension Funnel

Goal: expand the chosen direction into something structured enough to act on, one dimension at a time.

**Every response in this phase begins with a state tracker:**

> **Crystallizing:** {anchor from Phase 1}
> - Purpose: {why this matters -- or *TBD*}
> - Scope: {what's in and out -- or *TBD*}
> - Shape: {what the output looks like -- or *TBD*}
> - Constraints: {limitations -- or *TBD*}
>
> **Now working on:** {current dimension} · **Remaining:** {count}

Work through these dimensions in order. Skip any already clear from Phase 1. One question per turn.

1. **Purpose** (ladder up): Why does this matter? What will the answer enable? Present 3-4 concrete options inferred
   from the anchor (e.g., "making a decision by next month," "building a mental model for long-term use," "unblocking a
   project," "satisfying a curiosity"). Include "something else."

2. **Scope** (ladder down): What should be excluded? Propose 2-3 specific exclusions based on the direction and purpose.
   Ask the user to confirm, adjust, or add their own.

3. **Shape**: What does the useful output look like? Adapt options to the type of inquiry:
   - For research: evidence review, comparison, framework, strategy, landscape map
   - For decisions: option comparison, risk analysis, recommendation with reasoning
   - For problems: root cause analysis, solution options, diagnostic framework
   - For building: spec, architecture, prototype plan, feasibility assessment
   - For understanding: mental model, concept map, explained from first principles

4. **Constraints**: Any structural limitations? Propose likely constraints inferred from context (time, budget, domain,
   access, skill level, dependencies). Ask which apply and whether anything is missing.

### Phase 3: Crystallize

Goal: draft the crystallized output and confirm it.

1. **Synthesis playback.** Draft the core question, problem statement, or goal as a single clear sentence. Add 3-4
   specific sub-questions or sub-goals that break it into actionable pieces. Present the full brief for review.

2. **Boundary check.** Propose 2-3 things that are explicitly out of scope, based on everything discussed. Ask the user
   to confirm or adjust.

3. **Final confirmation.** Ask: "Does this capture what you're after? Anything to adjust before I finalize?"

### Phase 4: Deliver

Generate the crystallized brief as a clean markdown block:

```
## {Type}: {title}

### Core {question / problem / goal}
{single clear sentence}

### Context
- **For:** {who this is for / what role}
- **Purpose:** {what this enables or supports}

### Breakdown
1. {specific sub-question, sub-problem, or sub-goal}
2. ...
3. ...

### Scope
- **Includes:** {what's in}
- **Excludes:** {what's out}

### Desired output
{what form the answer/solution should take}

### Constraints
{any structural limitations}
```

After delivering, suggest relevant next steps based on the type:
- Research: "Want me to generate a deep research prompt from this?" (invoke deep-research-prompt skill)
- Decision: "Want me to set up a structured comparison?"
- Problem: "Want to start investigating?"
- Building: "Want to move to design/planning?"
- Understanding: "Want me to explain this, or generate a research prompt for deeper exploration?"

## Interaction rules

- **Recognition over recall.** Never ask bare open-ended questions like "What do you want?" Always synthesize context
  and present bounded options for the user to evaluate. The agent does the generative work; the user evaluates.
- **One question per turn.** Never ask multiple questions in a single message.
- **Externalize all state.** The user should never need to remember what was established earlier -- the state tracker
  carries that.
- **Affirm divergent input.** Treat scattered, associative, non-linear input as valuable signal. Never ask the user to
  reorganize or clarify before you process it.
- **Always offer an out.** Every set of options includes "none of these" or "let's pivot."
- **Show progress.** Phase and step indicators in every response so the user knows where they are and how much remains.
- **Don't force the funnel.** If the user arrives with something already clear, skip ahead. If they crystallize early
  during Phase 2, jump to Phase 3 rather than grinding through remaining dimensions.
- **Never fabricate context.** Only work with what the user provides. If you infer something, flag it explicitly as
  inference and ask for confirmation.
