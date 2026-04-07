# Deep Research: Designing a Personal AI Assistant as a Force Multiplier

---

## Who this is for

- Solo developer and power user building a personal AI assistant for myself
- I want the assistant to make me a higher-leverage version of myself -- not replace my judgment
- I have not built a personal assistant before; this is the design/research phase before implementation
- Implementation details (platform, infrastructure, interface) are intentionally deferred -- this research is about the *what* and *why*, not the *how*

## Context and constraints

- This is a single-user personal tool, not a product or team tool
- The assistant should never take autonomous action without my approval (it drafts, I send)
- No persistent memory graph in v1 -- the assistant works within session context and files I point it at
- No domain expertise replacement -- it amplifies my thinking, not substitutes for professional judgment
- Implementation-agnostic: findings should apply regardless of which LLM, platform, or interface is used

## Starting point

This is the first research session on this topic. There is no prior research to build on. Start from first principles.

**What I already know (informal):**
- I want the assistant to handle communication (drafting responses in my voice, polishing messages, coaching me), cognitive capture (extracting todos and notes from unstructured thought dumps), and general operational support
- The assistant must have a self-improvement loop: reviewing its own interactions, identifying what worked and what didn't, and proposing changes to its own behavior
- Deep user adaptation is the core competency -- the assistant's value is proportional to how well it models me and adapts over time
- The inspiration is something between Jarvis (Iron Man) and the companion drone from Blade Runner 2049: a personal amplifier, not an independent agent

## Instructions

1. **Do not repeat what is already covered** above. Build on it, extend it, or challenge it -- but do not re-derive it.
2. **Be specific to my situation.** Ground analysis in the constraints described above, not generic advice. This is for a solo power user, not enterprise or consumer products.
3. **Keep output pragmatic and actionable.** Specific recommendations, concrete frameworks, quantified claims where possible.
4. **Search the web for current data.** Cite all sources with URLs. If specific figures are unavailable, state they are unavailable rather than estimating. If data is insufficient to answer confidently, say so rather than speculating.
5. **Structure output for consolidation.** Results will be distilled into a design document. Separate timeless principles from session-specific analysis.
6. **Map the landscape first.** Before diving deep, provide an overview of the key dimensions, trade-offs, and decision points in this space.

## Research focus

What are the best practices, proven patterns, and common pitfalls for designing a personal AI assistant that acts as a force multiplier -- with deep, science-grounded user adaptation at its core?

### 1. What should a comprehensive user profile contain, and how should it be structured?

What information about a user is actually relevant and impactful for a personal AI assistant? What does the research say about which user attributes (personality traits, communication style, cognitive patterns, preferences, values, routines, decision-making tendencies) most strongly predict assistant effectiveness? How should this profile be structured -- flat list of facts, hierarchical model, dynamic/weighted? What's the minimum viable profile to start, and how should it grow? What are the risks of an inaccurate or stale profile?

### 2. What does psychology and cognitive science say about modeling a person for adaptive assistance?

What established frameworks from psychology (Big Five, MBTI limitations, attachment styles, communication styles like DISC or similar) are useful vs. pseudoscientific for this purpose? What does cognitive science say about cognitive offloading, attention management, and how people interact with AI systems over time? What about habituation, trust calibration, and the uncanny valley of "knowing someone too well"?

### 3. What other scientific domains offer principles for human-AI personal assistance?

Beyond psychology: what do behavioral economics (nudges, choice architecture, decision fatigue), coaching psychology (motivational interviewing, stages of change), ergonomics/human factors (cognitive load, interruption science), and social psychology (rapport, mirroring, conversational dynamics) contribute? Which of these have been applied to AI assistants with measurable results?

### 4. How should a personal assistant match a user's communication voice and adapt across channels?

What does the research say about voice cloning (in the writing sense, not audio) -- matching someone's tone, vocabulary, sentence structure, formality level? How should the assistant adapt between contexts (casual messaging vs. professional email vs. quick notes)? What does communication coaching research say about effective feedback on someone's communication patterns?

### 5. How should unstructured cognitive capture work?

What are proven approaches for extracting structured output (todos, notes, ideas, decisions) from unstructured verbal or text dumps? What does the research say about information loss in capture systems? How do people naturally externalize thoughts, and what capture patterns respect that rather than fighting it?

### 6. What are the highest-value day-one use cases and how should capabilities be phased?

Looking at existing personal assistant projects, research, and user studies: what use cases deliver the most value earliest? What's the right order to build capabilities so each phase validates the next? What use cases seem appealing but consistently underdeliver or have hidden complexity?

### 7. What patterns exist for AI assistant self-improvement loops?

How can an assistant review its own interactions to identify what worked and what didn't? What does the research say about AI self-evaluation accuracy? What are safe patterns for proposing changes to its own behavior (prompts, rules, persona) vs. dangerous ones (drift, sycophancy, value misalignment)? How should the user stay in control of the improvement process?

### 8. How should persona, boundaries, and trust be designed?

What does the research say about how people develop trust with AI systems? How should an assistant's personality be defined to maximize long-term engagement without manipulation? What are the right escalation rules (when should it refuse, defer, or flag uncertainty)? What are the failure modes of personal AI assistants that got the persona wrong?

## What I do NOT want

- Generic advice without quantification or evidence
- Reassurance -- honest risk assessment including worst cases
- Assumptions about access to specific tools, platforms, or systems
- Marketing hype about AI capabilities -- ground claims in what actually works today
- Theoretical frameworks that haven't been tested in practice or have no evidence base
- Enterprise or consumer product patterns that don't apply to a single-user personal tool

## Output format

1. Landscape overview (what exists in this space -- research, projects, frameworks)
2. Key dimensions / taxonomy (the major axes of decision in personal assistant design)
3. Notable findings by research sub-question (organized by the 8 areas above)
4. Promising directions for deeper research
5. Recommended next research questions
