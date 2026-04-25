# Canonical interview arc

Extracted from Seb's Alex Baas validation interview (`brain/data/rec-2026-03-27-140153-Alex-Baas-AI---Client-Validation.polished.txt`), cross-read against its post-debrief (`rec-2026-03-27-143722-Alex-Baas-AI---Client-Validation.summary.md`). This is the scaffold. Don't reinvent it per candidate — adapt the candidate-specific probes inside the fixed phase structure.

## Shape

Default 60 min. Sections are proportional, not absolute — shift time toward the deep-probe phase for higher-risk claims.

| # | Phase | Typical | Purpose |
|---|-------|---------|---------|
| 0 | Open | 30s | State the shape of the conversation |
| 1 | Intros & narrative | 5–7 min | Let the candidate set their own framing; observe engagement |
| 2 | Deep technical probe | 15–20 min | Stress-test the highest-risk claim on the CV |
| 3 | Gap probe | 3–5 min | Directly surface known gaps against role bars |
| 4 | Comms & ambiguity | 5–7 min | Specific past-situation prompts, not generics |
| 5 | AI copilot fluency | 3–5 min | Agent-mode tool use, not autocomplete |
| 6 | Motivation | 2–3 min | One pointed question; listen for lukewarm |
| 7 | Their questions | 5–10 min | Diagnostic — what they ask reveals how they think |
| 8 | Close | 30s | Next-steps script |

Phase 2 absorbs extra time when phases 5–6 run short, which is common.

## Phase-by-phase intent

### 0 · Open
Set expectations. Verbatim:
> "We've got an hour booked — doesn't have to fill. I'll start with quick intros, then ask about your recent work and dive deep on a project. We'll leave time for you to ask questions about Sierra and the role. Sound good?"

### 1 · Intros & narrative
You go first (~45s), then:
> "Would love to hear a bit more deeply what you've been up to — especially the last year or two."

Listen for: structure of answer; engagement; how they frame career gaps; whether they land on the relevant recent work naturally.

Red flags: flat intro, no smile, no reciprocal questions. This is the Alex Baas failure mode — the post-debrief explicitly named "didn't smile once" as a concern for client-facing work.

### 2 · Deep technical probe — the decisive phase
Pick the highest-overclaim-risk item on the CV: usually the most recent, solo-built, unverifiable claim. Open broad, then run the ladder.

Opening pattern:
> "Let's go deep on [specific claim]. Walk me through the architecture — what does it actually do, end to end?"

Follow-up ladder pattern (six rungs, progressively adversarial):
1. Ask them to name the concrete pieces. Vague vs specific.
2. Ask why this shape and not a simpler/alternative shape. Tests whether the design is reasoned or decorative.
3. Ask where it fails. Ask for the hardest thing they've debugged. No concrete failure = the system isn't used seriously.
4. Ask how they evaluate it. Golden dataset, regression, LLM-as-judge — or "I ran it and it worked"?
5. Ask what a specific tool/framework made easy vs hard. Tests real use vs name-drop.
6. Ask how this differs from something adjacent. Tests conceptual clarity.

Drift redirect: candidates will pivot to their comfort zone (old tech, a pet project, a different stack). Politely: "Let's stay on [topic] — we can come back to [their pivot] if time allows."

### 3 · Gap probe
Direct. The gap has been pre-identified in CV analysis (phase 3 of the skill workflow). Example format:
> "Sierra's SDK is TypeScript — [describe the specific shape of the stack]. Walk me through your most recent hands-on work in [this stack]. Not 'I've used it' — a specific thing you built."

Follow-up: "When did you last ship production [X]?" + "Comfortable if the outcome is: you write [X] every day from day one?"

Red flag: hedging, "I learn fast", "used it in the past" without recency. Honest-about-the-gap + plan to close it is workable. Overselling is not.

### 4 · Comms & ambiguity
Three prompts, each hitting a different facet.

**Client comms — demand specifics:**
> "Tell me about a time you had a stressful conversation with a client. What happened, what you did, what the outcome was."

Listen for: concrete situation, stakes, what they actually said. Push once if vague. Carlos Ortiz-style generic advice ("be honest, be clear") is a red flag.

**Ambiguity tolerance:**
> "At Sierra, things move fast. Specs aren't always perfect. A customer gives you a rough idea and it's on you to build, get feedback, iterate. How do you work — do you need strict requirements, or are you comfortable with that?"

**Critical follow-up — the Alex Baas gate:**
> "Is there ever a case where you'd push back and say 'I need to clarify first' instead of building? How do you decide?"

Red flag: build-first as *the* mode, not *a* mode. Alex got dinged specifically here — he named "cheaper to build and show than clarify" as a philosophy. Right answer names both modes and knows when each applies.

**Stakeholders:**
> "You'll be on near-daily calls with a client. Tell me about managing stakeholder communication in [specific past role from CV]."

### 5 · AI copilot fluency
Agent-mode bar (per Santi in `#sierra-validations`, 2025-07-30). Open:
> "What AI coding tools do you use day to day, and how do you leverage them?"

Follow-ups: tool choice + why; subagents or parallelization; handling drift when the agent goes off-track; MCPs in use.

Good signal: specific workflow, named plugins/MCPs, opinions on model choice, verification loops. Alex naming Ralph Loop was a strong signal.

### 6 · Motivation
One pointed question, calibrated to the candidate's trajectory. For a senior/founder candidate going via a staffing firm, the question is whether they're genuinely OK being IC again.

### 7 · Their questions
> "Happy to wrap earlier than the hour. But first — any questions about Sierra, the role, how we work?"

What they ask is diagnostic. Good: technical depth (SDK internals, eval practices, model versioning), team structure, ambiguity handling. Weak: only logistics (WFH, schedule), "what tech do you use" after you covered it, no questions.

### 8 · Close
> "Thanks for the time. The Wizeline team will get back to you on next steps once we've compared notes on the candidates this week."

## Post-conversation section

Below the main arc, emit a final H2 "Post-conversation" with:
- Scorecard table — dimensions from `journal/candidate-eval.md`, scored 1–5
- Verdict line — N/10 plus one-line rationale
- Calibration — `<dl>` keyed by past candidate name (from `references/calibration-set.md`)

Keep this physically separated in the output so during-call scrolling never lands on it by accident.
