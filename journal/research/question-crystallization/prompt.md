# Deep Research: Designing a Question Crystallization Skill -- From Vague Intuition to Well-Defined Research Questions

---

## Who this is for

- Software engineer who uses AI agent tools (Cursor, Claude) extensively for research and knowledge work
- I have ADHD, which affects working memory, energy regulation, and my ability to hold abstract questions in mind without external scaffolding
- I build AI agent skills (structured instruction files) that guide AI assistants through complex workflows
- I already have a deep-research-prompt skill that works well when I arrive with a rough question -- this new skill handles the messier upstream stage where I can't yet articulate what I want to know
- My research projects span diverse domains (financial analysis, professional communication, tool evaluation) -- the skill needs to be domain-agnostic

## Context and constraints

- **Target platform**: Cursor IDE agent skills (SKILL.md format) -- text-only interaction, no visual aids, no audio/tone reading
- **Interaction model**: AI agent asks questions, user responds in text. The agent must do the heavy lifting of structuring, tracking state, and proposing directions
- **ADHD design constraints**: Externalize all state (the user cannot be expected to hold the thread). Keep question loops short. Minimize cognitive load per interaction. Make progress visible
- **Upstream positioning**: This skill sits before the deep-research-prompt skill in the workflow. Its output should be a refined research question/brief that can feed directly into the deep-research-prompt skill or be used standalone
- **Existing prior art to build on**:
  - Deep-research-prompt skill: handles Phase 2 (question refinement) with a fixed sequence of questions (research question → output type → anti-patterns → constraints). Works well when you arrive with a question, but assumes you have one
  - Brainstorming skill (superpowers): one-question-at-a-time, multiple-choice-preferred, incremental validation. Good UX patterns but designed for implementation design, not question discovery

## Starting point

This is the first research session on this topic. There is no prior research to build on. Start from first principles.

**What I already know (informal):**
- The Socratic method is probably relevant -- using questions to surface implicit knowledge and assumptions
- There's likely psychology research on how people move from "felt sense" (vague awareness) to articulated understanding
- Prompt engineering has converging best practices around structured elicitation, but most of it assumes the user already knows what they want
- The brainstorming skill's "one question at a time" and "multiple choice preferred" patterns feel right for reducing cognitive load
- I suspect the skill needs distinct phases (explore → narrow → crystallize) rather than a linear question sequence
- The hardest part is probably the very beginning -- how to help someone who says "I'm interested in X but I don't know what specifically"

## Instructions

1. **Do not repeat what is already covered** above. Build on it, extend it, or challenge it -- but do not re-derive it.
2. **Be specific to my situation.** This is about an AI text agent guiding a human with ADHD through question refinement, not generic research methodology.
3. **Keep output pragmatic and actionable.** Specific frameworks, concrete phase structures, evidence-grounded design principles. The output needs to translate into a SKILL.md file.
4. **Search the web for current data.** Cite all sources with URLs. If specific research is unavailable, state that rather than estimating. If data is insufficient to answer confidently, say so rather than speculating.
5. **Structure output for consolidation.** Results will be distilled into the skill design. Separate timeless principles from implementation-specific recommendations.
6. **Map the landscape first.** Before diving deep, provide an overview of the key disciplines, frameworks, and design principles relevant to this space.

## Research focus

The core question: **What is the most effective structure for an AI agent skill that guides a user from a vague, pre-articulate sense of interest to a well-defined research question -- grounded in psychology, prompt engineering, and interaction design research?**

### 1. Psychology of question formulation: How do people move from vague intuition to articulated questions?

Investigate: Gendlin's "felt sense" and Focusing technique, Socratic method research, cognitive science of inquiry and curiosity, the role of recognition vs. recall in question formation. What does the literature say about the cognitive stages between "I sense something interesting here" and "here is my specific question"? Are there validated phase models?

### 2. Elicitation techniques: What works for extracting knowledge people don't know they have?

Investigate: Knowledge elicitation methods from expert systems research, cognitive task analysis, motivational interviewing techniques (adapted for intellectual exploration rather than behavior change), requirements elicitation from software engineering. Which techniques work in text-only, asynchronous-ish interaction?

### 3. Prompt engineering for progressive refinement: How should an AI agent structure a multi-turn question discovery conversation?

Investigate: Research on chain-of-thought prompting for user-facing interactions, conversational AI design patterns for ambiguous user intents, the "funnel" pattern in UX research interviews. What does current prompt engineering research say about guiding users through structured exploration vs. open-ended conversation?

### 4. ADHD-informed interaction design: How should the skill account for executive function differences?

Investigate: ADHD research on working memory limitations, decision fatigue, choice overload, and "analysis paralysis." What interaction patterns reduce cognitive load while maintaining exploration depth? How do you prevent the skill from becoming another source of overwhelm?

### 5. Phase structure and transitions: What should the skill's internal architecture look like?

Investigate: How many phases? What signals that the user has moved from one phase to the next? How does the agent detect when a question has crystallized vs. when the user is still exploring? Look at analogies from design thinking (diverge/converge), requirements engineering, and therapeutic conversation structures.

### 6. Existing tools and frameworks: What already exists in this space?

Investigate: Are there existing AI tools, research assistants, or conversation frameworks designed specifically for question refinement? How do research librarians approach reference interviews (the process of helping someone figure out what they're actually looking for)? What can we learn from how experienced research supervisors help PhD students refine their research questions?

### 7. Output design: What should the skill produce?

Investigate: What's the optimal format for the skill's output -- a single refined question, a question + sub-questions, a research brief, or something else? How should it signal "readiness" to the user? Should it produce something that feeds directly into the deep-research-prompt skill, or should the handoff be more flexible?

## What I do NOT want

- Generic advice about asking open-ended questions -- I need specific, structured techniques with evidence
- Overly academic taxonomy that doesn't translate to a practical skill workflow
- Therapy/coaching frameworks that assume a human facilitator and can't be adapted for an AI text agent
- Generic "explore more" without concrete mechanisms
- Reassurance -- honest assessment of what the research supports vs. what's speculative
- Assumptions about access to visual tools, real-time audio, or in-person interaction
- Repetition of what's already in the Starting Point section above

## Output format

Hybrid of Framework/model and Actionable strategy:

1. **Executive summary** (1 paragraph: the core insight and recommended approach)
2. **Landscape overview** (what disciplines and frameworks are relevant, how they connect)
3. **Core model** (the psychological/cognitive model of question crystallization -- how it actually works, with evidence)
4. **Design principles** (research-grounded principles for the skill, each with supporting evidence)
5. **Recommended skill architecture** (concrete phase structure, transition signals, interaction patterns -- specific enough to implement)
6. **ADHD-specific adaptations** (what changes for executive function differences)
7. **Handoff design** (how the skill's output connects to downstream tools like deep-research-prompt)
8. **Open questions and limitations** (what the research doesn't cover, what needs testing)
