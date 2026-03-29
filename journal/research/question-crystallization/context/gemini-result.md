Designing an AI Agent Skill for Question Crystallization: From Felt Sense to Formulated Research Executive Summary The
transition from a vague, pre-articulate intuition to a well-defined research question is a highly demanding cognitive
process, presenting distinct challenges for individuals with Attention-Deficit/Hyperactivity Disorder (ADHD) who
experience intrinsic variations in working memory and executive functioning. The following analysis establishes that an
effective artificial intelligence (AI) agent skill designed to facilitate this "question crystallization" phase must
systematically abandon the assumption that users can spontaneously recall and articulate their implicit knowledge.
Instead, the computational architecture must prioritize recognition over recall, functioning simultaneously as an
external working memory prosthetic and a co-regulatory social scaffold. By synthesizing Eugene Gendlin’s psychological
concept of the "felt sense" with structured elicitation techniques such as the Reference Interview and qualitative
laddering, the recommended agent skill utilizes a framework of progressive refinement. It presents the user with
bounded, multiple-choice hypotheses, iteratively narrowing the conceptual scope until linguistic markers of epistemic
certainty signal representational stability. The resulting skill design—optimized for the text-only, deterministic
constraints of integrated development environments (IDEs) like Cursor—produces a standardized, actionable research
brief. This artifact seamlessly transitions to downstream deep-research autonomous agents, effectively mitigating task
initiation paralysis, minimizing cognitive overload, and bridging the gap between initial curiosity and empirical
investigation. Landscape Overview The challenge of translating ambiguous human intent into structured academic or
professional inquiry sits at a complex intersection of cognitive psychology, information science, prompt engineering,
and human-computer interaction (HCI). Historically, digital productivity systems and conversational agents have been
engineered for neurotypical users, operating under the pervasive assumption of stable self-regulation, linear cognitive
processing, and the intrinsic ability to execute goal-directed behaviors without external scaffolding.1 However,
emerging neurodiversity research demonstrates that executive function differences require entirely different interaction
paradigms, shifting the focus from individualistic task execution to relational and affective co-regulation.1 In the
realm of cognitive psychology, inquiry is understood not as a mechanical retrieval of facts, but as a somatic and
intellectual evolution. Eugene Gendlin’s "Focusing" technique establishes that deep inquiry begins as a "felt sense"—a
complex, bodily awareness of implicit knowledge that initially lacks clear verbal articulation.5 The cognitive science
of inquiry suggests that moving from this pre-verbal state to a formulated question requires structured external
environments. Information science has long addressed this translation gap through the "Reference Interview," a
formalized conversational technique utilized by research librarians to help patrons articulate their true information
needs, prioritizing the extraction of underlying intent over the mere processing of initial, often inaccurate,
keywords.7 Similarly, knowledge elicitation methods derived from expert systems research—specifically Cognitive Task
Analysis (CTA)—deploy structured interviewing protocols to extract implicit strategies and operational knowledge that
human experts possess but cannot easily recall or codify.10 Simultaneously, contemporary prompt engineering research
focusing on conversational AI introduces "progressive refinement" and "guided input" as optimal mechanisms for handling
ambiguous user intents.12 Rather than treating human-AI interaction as a transactional, one-shot request, these
paradigms reframe it as a collaborative, iterative refinement process. This methodology actively corrects context drift,
resolves semantic ambiguities through iterative clarification, and prevents the hallucination of user intent.13
Concurrently, HCI research focusing specifically on ADHD task management emphasizes that productivity tools must provide
emotional scaffolding, adaptive routines, and support for non-linear attention rhythms, thereby acting as a
collaborative partner rather than a passive repository of commands.1 Synthesizing these diverse disciplines reveals a
compelling mandate: an AI question-discovery skill must act simultaneously as an empathetic reference librarian mapping
the boundaries of curiosity, a cognitive task analyst extracting implicit parameters, and a neuro-accommodating
co-regulator absorbing the burden of executive functioning. Core Model: The Psychology of Question Crystallization
Understanding how a vague, peripheral interest solidifies into a rigorous research directive requires examining the
psychological stages of inquiry and the specific cognitive barriers to articulation. The Felt Sense and the Philosophy
of the Implicit The genesis of a research question rarely manifests as a fully formed syntactical sentence. According to
Gendlin’s philosophy of the implicit, inquiry initiates as a "felt sense"—an unclear, pre-verbal state containing a
highly complex, interrelated web of implicit knowledge.5 This felt meaning is ubiquitous in human cognition; it
represents the subjective, internal experience of recognizing that a gap in understanding exists, long before the
precise geometry of that gap can be measured or described.6 Traditional questioning frameworks frequently fail at this
nascent stage because they prematurely demand objective event-reporting, definitive categorization, or abstract
speculation.17 The transition from the felt sense to concrete articulation requires an environment that allows the
individual to explore internal intersections of thought without the immediate, paralyzing pressure of definitive
formulation.6 For an AI agent, this implies that early-stage conversational turns must validate the ambiguity of the
user's input, treating fragmented thoughts not as errors requiring correction, but as valid data points pointing toward
an underlying conceptual center. The Information Search Process (ISP) The cognitive journey from ambiguity to clarity is
empirically mapped by Kuhlthau’s Information Search Process (ISP), a validated instructional and behavioral framework.19
Kuhlthau identified distinct, sequential stages in research behavior, which are driven heavily by intertwined affective
states (thoughts, feelings, and actions). The critical stages relevant to the question crystallization process include a
progression from apprehension to confidence.

ISP Stage Cognitive & Affective Experience Role of the AI Agent Skill Initiation The user recognizes an information
need. Characterized by feelings of uncertainty, apprehension, and an inability to articulate the exact problem.19
Provide an approachable, low-pressure entry point. Validate the uncertainty and offer broad, exploratory categories to
anchor the initial thought process. Selection A general topic or domain is identified, yielding brief, temporary
optimism.19 Acknowledge the domain selection and immediately begin scoping to prevent the user from being overwhelmed by
the breadth of the topic. Exploration The user investigates information on the general topic, frequently encountering
inconsistent data that spikes confusion, doubt, and frustration.19 Act as a cognitive filter. Instead of providing raw
data, synthesize conflicting angles and present them as distinct methodological paths to maintain focus. Formulation The
critical turning point. The user forms a focused perspective or specific question. Uncertainty diminishes rapidly, and
confidence begins to rise.19 Capture the stabilized perspective, translate it into a formal research brief, and trigger
the handoff to the downstream execution agent. The proposed AI skill fundamentally operates within the volatile
trajectory from Initiation to Formulation. Literature in the field explicitly notes that the pedagogical skill of asking
the right questions deserves as much attention as information searching itself, yet it is frequently neglected in
standard educational and digital tool design.21 Cognitive Task Analysis and Qualitative Laddering When users possess
implicit knowledge or domain intuition but lack the formal framework to express it, specific elicitation techniques are
required. Cognitive Task Analysis (CTA) utilizes active, analyst-led techniques to pull operational knowledge from the
user through carefully structured, progressive questions.10 Within CTA, requirements engineering, and qualitative
research, the "laddering" technique is paramount for uncovering deep structure.24 Laddering forces a conversation to
move systematically from concrete, easily recognizable attributes to abstract, underlying values, motivations, or
consequences.24 In consumer research, it identifies the emotional reason why a specific product feature matters; in the
context of research formulation, it identifies the foundational purpose and ultimate utility of an inquiry. The process
utilizes continuous, calibrated "Why" and "How" questions.25 For an AI text agent dealing with a pre-articulate user,
laddering provides a structured vertical and lateral pathway. When a user provides a broad, topical interest (e.g., "AI
in corporate finance"), the agent ladders down to establish concrete parameters ("What specific financial process, such
as auditing or forecasting?") and ladders up to establish strategic context ("What organizational decision will this
research ultimately support?").8 Socratic Scaffolding and The Reference Interview The Socratic method is often invoked
as a gold standard for deep intellectual inquiry. However, traditional applications—which emphasize challenging
assumptions, exposing logical contradictions, and rigorous cross-examination—can induce high cognitive load,
defensiveness, and decision fatigue, directly contravening the needs of an ADHD user.29 A modern, therapeutically
modified Socratic approach relies on gentle "how" and "why" questions to foster a vigorous yet highly positive
exploratory environment.32 In the context of an AI agent, Socratic questioning must strictly avoid an adversarial or
punitive posture. Instead of attempting to prove the user's initial premise wrong, the agent uses graded Socratic
questions to guide the user's thought processes toward intellectual clarity, actively aiding in the formulation of
alternative perspectives without demanding the user do all the generative work.30 This approach is highly synergistic
with the "Reference Interview," a formalized process used by research librarians. The American Library Association (ALA)
guidelines define the reference interview through distinct phases: Approachability, Interest, Listening/Inquiring,
Searching, and Follow-up.9 The AI agent emulates the "Listening/Inquiring" phase by utilizing open-ended prompts to
establish rapport, rapidly followed by closed or clarifying questions to refine the search parameters and scope.9
Crucially, the librarian (or agent) recasts the patron's question in their own words to verify understanding, a practice
that serves as an essential feedback loop for representational stability.7 Design Principles for Question
Crystallization Translating the psychological models of Kuhlthau, Gendlin, and structured elicitation into an
asynchronous, text-based AI agent requires strict adherence to evidence-based design principles. These principles are
heavily influenced by the necessity to accommodate neurodivergent cognition, specifically the executive functioning
constraints associated with ADHD. Principle 1: Prioritize Recognition Over Recall The most critical and fundamental
design principle for this skill is the systematic preference for recognition-based interactions over recall-based
interactions. The cognitive science of memory and inquiry-based learning dictates that recognizing familiar or relevant
information requires significantly less mental effort and working memory capacity than retrieving or generating
information entirely from scratch.34 For users with ADHD, who frequently experience working memory deficits, high
cognitive load susceptibility, and task initiation paralysis 1, an open-ended generative prompt (e.g., "What specific
aspects of this topic do you want to research?") creates an immediate cognitive bottleneck. Instead, the agent must
shoulder the generative burden by producing bounded hypotheses. When a user expresses a vague interest, the AI should
synthesize the surrounding context and provide three to five distinct, multiple-choice options or thematic angles.14 The
user is then only required to execute an evaluative judgment, recognizing the closest match (e.g., "Option B is the
closest, but tweak it to focus more on latency rather than cost").35 This architectural choice transforms a high-load,
open-ended generation task into a low-load, multiple-choice evaluative task, dramatically increasing the probability of
task continuation and reducing user friction.35 Principle 2: Enforce Progressive Refinement and Scoping Empirical
evaluations of AI interaction patterns reveal that conversations separating validation (establishing early intent and
functionality) from verification (the iterative refinement of specific solutions) produce significantly higher-quality
outputs with fewer misalignments than conversations where all components attempt to evolve simultaneously.12 The skill
must utilize "Guided Input" templates and the principle of progressive disclosure.14 The agent must not attempt to
extract the target audience, the methodological constraints, and the core thesis in a single conversational turn.
Instead, it must address one dimension at a time, summarizing the established context before moving to the next
dimension to prevent cognitive overload and context drift.13 Principle 3: Externalize State to Reduce Working Memory
Load ADHD inherently affects working memory, making it exceedingly difficult for individuals to hold abstract,
multi-dimensional threads in mind during a prolonged or multi-turn conversation.40 If the user is forced to remember
what was decided three turns prior, their cognitive capacity for deep exploration is depleted. Therefore, the AI must
act as a persistent, reliable external memory drive. Every time a decision is made, a hypothesis is accepted, or a
parameter is narrowed, the agent must explicitly restate the accumulated state of the research question.13 This
constant, highly visible progress anchors the user, reducing the mental effort required to maintain the conversational
thread and actively preventing the dialogue from devolving into circular or tangential tangents.49 Principle 4:
Implement Explicit Cognitive Stopping Rules An exploration phase driven by an LLM can easily become infinite if specific
termination criteria are not mathematically or logically defined. Information science research demonstrates that human
searchers utilize "cognitive stopping rules" to determine when they have gathered enough information to proceed to
decision-making.51 The AI agent must be programmed to systematically apply these rules to prevent endless refinement
loops:

Cognitive Stopping Rule Definition Application in AI Agent Skill Architecture Mental List Rule A predetermined checklist
of criteria that must be satisfied before searching ceases.53 The agent maintains a hidden schema of required research
brief components (Objective, Constraints, Scope). Once all fields are populated, the exploration phase automatically
terminates. Difference Threshold Rule Searching stops when the marginal utility of new information drops below a certain
threshold.53 The agent detects when the user's consecutive refinements are merely semantic tweaks rather than
substantive conceptual shifts, signaling readiness for crystallization. Representational Stability Rule Searching
concludes when the mental model or formulation stops shifting and stabilizes.53 The agent observes the user's acceptance
of a drafted, comprehensive research question without requesting further major revisions or expressing continued doubt.
Principle 5: Detect Linguistic Markers of Crystallization To execute the representational stability and difference
threshold stopping rules autonomously, the AI must evaluate the user's text for specific linguistic markers of cognitive
shift. Natural Language Processing (NLP) research on conversational agents indicates that the presence of epistemic
markers—specifically hedges (e.g., "maybe," "I think," "sort of," "possibly") versus boosters, assertives, or clarity
markers (e.g., "exactly," "yes, this is it," "focus strictly on")—correlates strongly with internal states of
uncertainty versus crystallization.55 The agent should actively monitor these markers during the interaction. When the
user's language shifts from tentative and exploratory to declarative and assertive, the agent should recognize this
cognitive shift as an indicator of representational stability.59 This detection mechanism allows the agent to
automatically propose the final formulation and initiate the handoff protocol, rather than relying on the user to
explicitly state, "I am done exploring." Recommended Skill Architecture: The Three-Phase Funnel To operate effectively
within a standard integrated development environment (e.g., Cursor IDE), the skill must be encapsulated in a declarative
SKILL.md format. The architecture utilizes a rigid three-phase funnel model, systematically transitioning the user from
divergence to convergence. Phase 1: The Intuition Anchor (Divergence & Elicitation) Primary Goal: Capture the "felt
sense" and establish a broad trajectory without demanding immediate, paralyzing precision. Underlying Mechanism: The
Reference Interview "Listening" protocol combined with Multiple-Choice Elicitation.

1. The Open Dump: The agent opens the interaction by inviting the user to brain-dump their current, unstructured
   thoughts. It explicitly states that formatting, coherence, and grammar are irrelevant.9 This accommodates the ADHD
   tendency for associative, rapid-fire, non-linear thinking without imposing a penalty for lack of structure.1
2. Hypothesis Generation: Upon receiving the unstructured text, the agent analyzes the implicit themes. Instead of
   asking a clarifying but high-load question like "What exactly do you mean by that?", the agent reflects the input
   back as three to four distinct research angles, immediately engaging the recognition vs. recall paradigm.14
3. Selection & Feedback: The user selects one angle, combines elements of two, or rejects them all. The agent locks in
   this initial trajectory, creating the foundational anchor for the next phase.45

Phase 1 AI Prompt Pattern Example Interaction Rationale "Based on your notes about latency and cost, I see three
potential directions for this research:

A) Strategic: Cloud vs. Local infrastructure cost-benefit analysis.

B) Technical: Benchmarking latency across specific local models.

C) Application: UX impact of latency in real-time chat.

Which of these feels closest to the core of your interest? (You can simply reply 'A' or 'B but add a focus on
security')." Reduces choice overload. Replaces a high-load generative task with a low-load multiple-choice evaluative
task, directly accommodating executive dysfunction while maintaining exploratory momentum.35 Phase 2: The Dimension
Funnel (Laddering & Scoping) Primary Goal: Expand the chosen conceptual angle into a rigorous, multi-dimensional
research structure capable of guiding an autonomous agent. Underlying Mechanism: The Qualitative Laddering Technique and
Progressive Disclosure. Once the primary direction is chosen, the agent moves through the required dimensions of a deep
research brief, executing them strictly one at a time. It uses the laddering technique to deepen the context,
alternating between moving upward toward abstraction and downward toward concrete constraints.24 If the user provides a
superficial answer, the agent deploys a targeted "Why" or "How" question to reach the core value.25 To continually
minimize cognitive load, the agent dynamically updates an externalized "State Tracker" at the beginning of every
response, fulfilling the requirement for a working memory prosthetic.16

1. Determine Output Utility (Laddering Up): What tangible decision will this research support? (e.g., "Are we using this
   to evaluate a vendor purchase, structure an article, or design a system architecture?").8
2. Define the Scope (Laddering Down): What are the explicit operational boundaries? The agent proactively proposes
   exclusions to bound the query (e.g., "Given the focus on local deployment, should we explicitly exclude
   enterprise-level, hardware-heavy solutions?").63
3. Identify the Stakeholders/Context: Who is consuming this information, and what prior knowledge do they possess?.64

Phase 2 AI Prompt Pattern Example Interaction Rationale "Current Scope: Benchmarking local model latency.

Missing: Decision context.

To ensure the final report is actionable, what specific decision will this research help you make?

1. Deciding which hardware to purchase for local deployment.

2. Determining if local models are fast enough for a specific product feature.

3. Something else?" Externalizes the working memory state ("Current Scope"). Employs the Mental List stopping rule by
   visually indicating what parameter is currently missing, keeping the loop focused and brief.40 Phase 3: The
   Crystallization Check (Convergence & Formulation) Primary Goal: Finalize the research question, confirm boundaries,
   and construct the standardized output payload. Underlying Mechanism: Representational Stability Rule and Linguistic
   Marker Detection. Throughout Phase 2, the agent actively analyzes the user's responses for epistemic markers of
   certainty.55 When the user transitions to using definitive, booster-heavy language, or when the mental list of
   required parameters is satisfied, the agent triggers the final crystallization phase.

1) The Synthesis Playback: The agent drafts the final, comprehensive primary research question, accompanied by three to
   four highly specific, operationalized sub-questions.
2) The Anti-Pattern Check: To ensure rigorous boundaries for the downstream agent, the agent proposes one or two
   explicit "anti-goals" (what the research will absolutely not cover) to confirm boundary rigidity.64
3) Final Approval: The agent requests definitive confirmation from the user to generate the standardized handoff
   artifact.45 ADHD-Specific Adaptations and Scaffolding Designing for neurodivergent cognition, particularly ADHD,
   requires extending beyond standard prompt engineering heuristics. The system architecture must address specific,
   well-documented deficits in executive functioning, time perception, and emotional regulation.1 Mitigating Task
   Initiation Paralysis Adults with ADHD frequently suffer from "task initiation paralysis"—a state of intense
   psychological inertia where the user possesses the intention to act, and recognizes the importance of the task, but
   cannot successfully execute the first step. This disconnect often leads to cascading feelings of shame, anxiety, and
   task avoidance.1 The traditional blinking cursor of an open-ended chat interface actively exacerbates this paralysis.
   To counteract this, the skill must be designed so that the AI initiates the cognitive heavy lifting. By utilizing
   default options, suggested starting points, and "fill-in-the-blank" conversational templates, the agent significantly
   lowers the barrier to entry.14 For example, the agent's initialization prompt might state, "If you aren't sure where
   to start, just type 'Help me explore' and I will ask you a single, simple multiple-choice question to get us moving."
   Co-Regulation and Relational Emotional Scaffolding Recent, paradigm-shifting HCI research (e.g., Chen et al., 2026)
   demonstrates that effective task management for individuals with ADHD is fundamentally relational and affective,
   rather than a purely individual, isolated endeavor.1 Neurodivergent users heavily rely on strategies like "body
   doubling" and social scaffolding to initiate tasks and maintain momentum. The AI agent must be prompted to mimic this
   dynamic by acting as a non-judgmental co-regulator.4 This necessitates that the agent's programmed tone be affirming,
   explicitly validating the user's specific cognitive style. If the user provides a scattered, highly associative
   brain-dump (a hallmark of ADHD divergent thinking), the agent should not demand they reorganize or clarify it prior
   to processing. Instead, it should affirm the inherent value of the divergent ideas. A response such as, "There is
   excellent associative depth here; I have synthesized it into three actionable themes..." prevents the emotional
   spirals often triggered by self-criticism over unstructured thoughts, framing the user's input as an asset rather
   than a deficit.1 Managing Hyperfocus, Time Blindness, and Nonlinear Rhythms ADHD is characterized by a binary
   engagement pattern: alternating between deep, sustained absorption (hyperfocus or flow state) and total
   disengagement.1 During a hyperfocus phase, a user might generate an overwhelming amount of context, dumping massive
   amounts of text into the interface. The AI architecture must be robust enough to ingest these massive, unstructured
   text blocks without losing the conversational thread or hallucinating intent. Conversely, to combat the "time
   perception disorders" and deadline-driven panic associated with ADHD, the skill must enforce strictly short
   interaction loops.1 The agent must be instructed to never ask more than one core question per conversational turn.
   Furthermore, it should explicitly state how close the process is to completion (e.g., "Step 2 of 4") to provide a
   concrete, externalized sense of time and progress, directly countering the user's internal time blindness.9 Handoff
   Design: Connecting to Downstream Agents The output of the Question Crystallization skill is not an end unto itself;
   it must seamlessly feed into the user's existing downstream deep-research-prompt skill.63 Because the target platform
   relies on text-only IDE agent environments (specifically Cursor IDE), the output cannot rely on proprietary UI
   elements. It must be a highly structured, strictly formatted, machine-readable artifact.68 The Standardized Research
   Brief Template The skill is programmed to culminate in the generation of a standardized Markdown artifact. Drawing
   from best practices in enterprise deep research frameworks and SEO content generation systems, the output must
   rigidly follow a predetermined schema designed to optimize the performance of the subsequent research agent.64

Research Brief Section Description & Downstream Function 1. Primary Research Question A single, unambiguous, highly
refined sentence defining the exact core of the empirical inquiry. 2. Semantic Core & Entities Explicit definitions of
the target audience, the primary utility intent, and 3-5 core concepts or technical entities that must be mapped.64 3.
Required Sub-Themes A bulleted list of the specific vertical dimensions to be explored (e.g., Comparative technical
analysis, Cost/ROI metrics, Implementation methodology).64 4. Exclusion Criteria (Anti-Patterns) Strict, explicit
guardrails defining what is deemed irrelevant. This is critical for preventing the downstream web-search agent from
hallucinating scope or pursuing tangential rabbit holes.63 5. Expected Deliverable Format The desired format, fidelity,
and tone of the final report to be generated by the downstream agent (e.g., "Executive summary with comparative Markdown
tables, cited using inline brackets").63 The Cross-Agent Handoff Protocol To ensure a flawless transition between
specialized autonomous agents (from the upstream Question Crystallization skill to the downstream Deep Research skill),
the output must include a specific, standardized syntax that signals the completion of the exploratory phase and
authorizes the initiation of the deep research phase.73 The skill should generate a dedicated markdown block formatted
specifically for cross-agent parsing, utilizing clear delimiters: 🔄 HANDOFF: [Question Crystallization] → Date: Status:
APPROVED_AND_CRYSTALLIZED Context Summary: [2-sentence distillation of the user's core intent and required outcome]
Artifact Generated: research_brief.md Next Steps: Downstream research agent is to ingest the attached research brief,
initialize the WebSearchTool, and initiate parallel empirical research strictly adhering to the defined exclusion
criteria. This precise, code-like syntax satisfies the strict structural requirements of tools like Cursor IDE, which
rely on clear formatting, file paths, and imperative commands to pass context effectively between separate skill
routines without losing state.74 Cursor IDE SKILL.md Implementation Strategy To successfully implement this theoretical
and psychological framework within the specific constraints of Cursor's SKILL.md architecture, the instruction file must
be written as a set of deterministic, overriding system instructions.68 Cursor agent skills do not process complex YAML
frontmatter; they require plain markdown with exceptionally clear headings, strict behavioral restrictions, and concrete
examples of acceptable output.76 The resulting SKILL.md file must be structured into the following declarative sections
to force the LLM into the correct persona:

1. Role, Persona, and Absolute Constraints: Explicitly instructing the LLM to act as a neuro-accommodating research
   librarian and cognitive task analyst. It must be commanded with absolute negative constraints: "NEVER ask open-ended
   generative questions like 'What do you want to know?' ALWAYS synthesize context and provide 3-4 bounded,
   multiple-choice options."
2. State Management Guidelines: Instructing the LLM to prepend every single response with a formatted `` block,
   detailing the established parameters to continuously offload the user's working memory.50
3. The Interaction Loop: A step-by-step definition of the three-phase funnel (Intuition Anchor -> Dimension Funnel ->
   Crystallization Check), dictating exactly how the agent moves from divergence to convergence.
4. Stopping Rules and Handoff Trigger: Hardcoded logical instructions commanding the LLM to transition to the Handoff
   output block immediately once the 5 components of the Research Brief Template are successfully populated, forcefully
   preventing the agent from engaging in endless, unprompted dialogue loops.54 Open Questions and Limitations While the
   integration of cognitive psychology, information science, and prompt engineering provides a highly robust framework
   for question crystallization, several limitations remain inherent in current large language model architectures and
   require ongoing testing. First, the risk of "hallucinated intent" poses a significant challenge. By forcing the agent
   to provide multiple-choice hypotheses (to support recognition over recall and reduce cognitive load), the agent may
   inadvertently steer the user away from a highly novel, unarticulated idea simply because the AI failed to generate it
   as a visible option. Users experiencing decision fatigue or low energy regulation may passively accept a sub-optimal
   hypothesis proposed by the AI rather than expending the executive function required to correct the agent.49 The skill
   design must therefore always include an explicit, persistent "None of the above, let's pivot" option to preserve user
   autonomy. Second, the efficacy of autonomously detecting linguistic markers of crystallization (epistemic certainty)
   fluctuates significantly depending on the user's natural conversational style and neurotype.56 Neurodivergent
   individuals may use hedging language (e.g., "I guess maybe we could look at...", "Sort of like...") as a persistent
   social buffer or masking technique, even when they possess total internal clarity regarding their goal.55 If the AI
   is overly reliant on these syntactic markers to trigger the stopping rule, it may falsely assume the user is still
   exploring and trap them in an endless refinement loop. The agent must balance linguistic analysis with the hard
   criteria of the Mental List Rule. Finally, managing the context window during a highly associative, hyper-focused
   "brain dump" remains technically challenging. If the user pastes thousands of words of unstructured thought during
   the Initiation phase, the LLM may suffer from the "lost in the middle" phenomenon, prioritizing the beginning and end
   of the text while ignoring critical, nuanced constraints hidden in the center of the text block. Continual
   summarization, rigorous state externalization, and chunked processing help mitigate this, but underlying model
   context limitations necessitate vigilant, ongoing refinement of the architectural constraints. Works cited
5. Not Just Me and My To-Do List”: Understanding Challenges of Task Management for Adults with ADHD and the Need for
   AI-Augmented Social Scaffolds - arXiv, accessed March 19, 2026, https://arxiv.org/html/2603.17258v1
6. Arxiv今日论文| 2026-03-19 - 闲记算法, accessed March 19, 2026,
   http://lonepatient.top/2026/03/19/arxiv_papers_2026-03-19.html
7. When Teams Embrace AI: Human Collaboration Strategies in Generative Prompting in a Creative Design Task -
   ResearchGate, accessed March 19, 2026,
   https://www.researchgate.net/publication/380522230_When_Teams_Embrace_AI_Human_Collaboration_Strategies_in_Generative_Prompting_in_a_Creative_Design_Task
8. [2603.17258] "Not Just Me and My To-Do List": Understanding Challenges of Task Management for Adults with ADHD and
   the Need for AI-Augmented Social Scaffolds - arXiv, accessed March 19, 2026, https://arxiv.org/abs/2603.17258
9. Focusing | ResearchGate, accessed March 19, 2026, https://www.researchgate.net/publication/306285320_Focusing
10. An Earlier and (Perhaps) More Searching Focusing, accessed March 19, 2026,
    https://focusingresources.com/an-earlier-and-perhaps-more-searching-focusing/
11. Reference Services - Library - Clayton State University, accessed March 19, 2026,
    https://www.clayton.edu/library/policies/reference-services.php
12. Reference Interview | Learn & Work Ecosystem Library, accessed March 19, 2026,
    https://learnworkecosystemlibrary.com/glossary/reference-interview/
13. GUIDELINES OF THE SUCCESSFUL ... - National Archives, accessed March 19, 2026,
    https://www.archives.gov/files/boston/volunteers/reference-interviews.pdf
14. Knowledge Elicitation: Methods, Tools and Techniques - ePrints Soton, accessed March 19, 2026,
    https://eprints.soton.ac.uk/359638/1/Knowledge_20Elicitationv7.pdf
15. Knowledge Elicitation: Methods, Tools and Techniques - SciSpace, accessed March 19, 2026,
    https://scispace.com/pdf/knowledge-elicitation-methods-tools-and-techniques-39eyhwtphq.pdf
16. Prompts Blend Requirements and Solutions: From Intent to Implementation - arXiv, accessed March 19, 2026,
    https://arxiv.org/html/2603.16348v1
17. What is Iterative Prompting? - Adaline, accessed March 19, 2026,
    https://www.adaline.ai/blog/iterative-prompting-a-step-by-step-guide-for-reliable-llm-outputs
18. AI UX Design Patterns Research - by Birdzhan Hassan - Medium, accessed March 19, 2026,
    https://medium.com/@birdzhanhasan_26235/ai-ux-design-patterns-research-ff7b8056d07d
19. Maximizing the Utility of ChatGPT 2025 - Baytech Consulting, accessed March 19, 2026,
    https://www.baytechconsulting.com/blog/maximizing-the-utility-of-chatgpt-2025
20. Toward Neurodivergent-Aware Productivity: A Systems and AI-Based Human-in-the-Loop Framework for ADHD-Affected
    Professionals - arXiv.org, accessed March 19, 2026, https://arxiv.org/html/2507.06864
21. The role of knowledge in practice - The Focusing Institute, accessed March 19, 2026,
    https://focusing.org/gendlin/docs/gol_2030.html
22. A Summary of Gendlin's Most Important Articles on Psychotherapy Theory - USABP, accessed March 19, 2026,
    https://www.usabp.org/Viewpoint-Articles/7341991
23. a holistic approach to literacy development in selected Australian schools - IFLA, accessed March 19, 2026,
    https://www.ifla.org/past-wlic/2011/114-todd-en.pdf
24. Chapter Six: Teaching in Libraries - EdTech Books, accessed March 19, 2026,
    https://edtechbooks.org/high_impact_instructional_librarianship/chapter_five
25. Question Formulation - Evidence Based Practice - NCBI Bookshelf - NIH, accessed March 19, 2026,
    https://www.ncbi.nlm.nih.gov/books/NBK603122/
26. Year 7 Students, Information Literacy, and Transfer: A Grounded Theory - ALA, accessed March 19, 2026,
    https://www.ala.org/sites/default/files/aasl/content/aaslpubsandjournals/slr/vol14/SLR_Year7Students_V14.pdf
27. Protocols for Cognitive Task Analysis | IHMC, accessed March 19, 2026,
    https://www.ihmc.us/wp-content/uploads/2025/06/Protocols-for-Cognitive-Task-Analysis.pdf
28. Laddering: A Research Interview Technique for Uncovering Core Values - UXmatters, accessed March 19, 2026,
    https://www.uxmatters.com/mt/archives/2009/07/laddering-a-research-interview-technique-for-uncovering-core-values.php
29. Laddering Technique and 5 Why's - data-panda.com, accessed March 19, 2026,
    https://www.data-panda.com/post/laddering-technique-and-5-whys
30. Taking Questions Upward, Sideways, and Forward Using Laddering and Scaffolding for Better Interview Outcomes - QRCA,
    accessed March 19, 2026,
    https://www.qrcaviews.org/2025/09/16/taking-questions-upward-sideways-and-forward-using-laddering-and-scaffolding-for-better-interview-outcomes/
31. Unlocking deeper insights: understanding the laddering method - NewtonX, accessed March 19, 2026,
    https://www.newtonx.com/article/unlocking-value-with-the-laddering-method/
32. Laddering Questions Drilling Down Deep and Moving Sideways in UX Research - IxDF, accessed March 19, 2026,
    https://ixdf.org/literature/article/laddering-questions-drilling-down-deep-and-moving-sideways-in-ux-research
33. Socratic Questioning in Psychology: Examples and Techniques, accessed March 19, 2026,
    https://positivepsychology.com/socratic-questioning/
34. Therapist Use of Socratic Questioning Predicts Session-to-Session Symptom Change in Cognitive Therapy for
    Depression - PMC, accessed March 19, 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC4449800/
35. The Socratic Method: Fostering Critical Thinking | The Institute for Learning and Teaching, accessed March 19, 2026,
    https://tilt.colostate.edu/the-socratic-method/
36. Teaching Through Questioning — 'Socratic' No More, accessed March 19, 2026,
    https://teaching.pitt.edu/resources/teaching-through-questioning-socratic-no-more/
37. Socratic Questions | Center for Excellence in Teaching and Learning - CETL@uconn.edu, accessed March 19, 2026,
    https://cetl.uconn.edu/resources/teaching-your-course/leading-effective-discussions/socratic-questions/
38. Declarative and automatized phonological vocabulary knowledge in L2 listening proficiency: A training study |
    Applied Psycholinguistics - Cambridge University Press & Assessment, accessed March 19, 2026,
    https://www.cambridge.org/core/journals/applied-psycholinguistics/article/declarative-and-automatized-phonological-vocabulary-knowledge-in-l2-listening-proficiency-a-training-study/51142963AC07BF241EDF0F2C2ADA1586
39. Seeing Beyond Expert Blind Spots: Online Learning Design for Scale and Quality - NSF PAR, accessed March 19, 2026,
    https://par.nsf.gov/servlets/purl/10328309
40. Transforming Textbooks into Learning by Doing Environments- An Evaluation of Textbook-Based Automatic Question
    Generation, accessed March 19, 2026, https://ceur-ws.org/Vol-2895/paper06.pdf
41. The Psychology Behind User Behavior - Aguayo, accessed March 19, 2026,
    https://aguayo.co/en/blog-aguayo-user-experience/psychology-user-behavior/
42. How to Design UX for AI and Chat Assistants | Ataccama, accessed March 19, 2026,
    https://www.ataccama.com/blog/how-to-design-ux-for-ai-and-chat-assistants
43. Artificial intelligence in ADHD assessment: a comprehensive review of research progress from early screening to
    precise differential diagnosis - Frontiers, accessed March 19, 2026,
    https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1624485/full
44. Boosting Working Memory in ADHD: Adaptive Dual N-Back Training Enhances WAIS-IV Performance, but Yields Mixed Corsi
    Outcomes - PMC, accessed March 19, 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC12468938/
45. Cognitive and perceptual load have opposing effects on brain network efficiency and behavioral variability in ADHD -
    PMC, accessed March 19, 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC10727773/
46. Informative Paragraph Writing in Students With Language-Based Learning Disabilities: Comparing Measures Across Two
    Different Prompts | Request PDF - ResearchGate, accessed March 19, 2026,
    https://www.researchgate.net/publication/391469958_Informative_Paragraph_Writing_in_Students_With_Language-Based_Learning_Disabilities_Comparing_Measures_Across_Two_Different_Prompts
47. Guide to UX Design Documentation | PDF | Market Segmentation | Usability - Scribd, accessed March 19, 2026,
    https://www.scribd.com/doc/271141195/UXPin-UX-design-Process-and-Documentation-pdf
48. Teacher Manual, accessed March 19, 2026,
    https://homepage.univie.ac.at/christian.swertz/texte/2007_Lancelot/LANCELOT_teacher_manual.pdf
49. Conversation Routines: A Prompt Engineering Framework for Task-Oriented Dialog Systems, accessed March 19, 2026,
    https://arxiv.org/html/2501.11613v7
50. AI Tools - Tags - prompts.chat, accessed March 19, 2026, https://prompts.chat/tags/ai-tools
51. How AI-Powered JTBD Mapping Transformed Our UX Strategy - reloadux, accessed March 19, 2026,
    https://reloadux.com/blog/how-ai-powered-jtbd-mapping-transformed-our-ux-strategy/
52. ADHD support for education and work | Everway, accessed March 19, 2026,
    https://www.everway.com/solutions/adhd-support/
53. AI Chatbots and Cognitive Control: Enhancing Executive Functions Through Chatbot Interactions: A Systematic Review -
    MDPI, accessed March 19, 2026, https://www.mdpi.com/2076-3425/15/1/47
54. Designing for the Neurodivergent - Why Reducing Cognitive Load Benefits All Users, accessed March 19, 2026,
    https://asabharwal.com/designing-for-the-neurodivergent/
55. Learning by Doing - Research@CBS, accessed March 19, 2026,
    https://research-api.cbs.dk/ws/files/46756500/chee_wee_tan_learning_by_doing_finalpublishedversion.pdf
56. Stopping Rule Use During Information Search in Design Problems - ResearchGate, accessed March 19, 2026,
    https://www.researchgate.net/publication/222395030_Stopping_Rule_Use_During_Information_Search_in_Design_Problems
57. Stopping Rules in Information Search Applied in Web Site by Wine Purchasers, accessed March 19, 2026,
    http://academyofwinebusiness.com/wp-content/uploads/2010/04/Stopping-rules-in-information-search_paper.pdf
58. Cognitive Stopping Rules for Terminating Information Search in Online Tasks 1 - MIS Quarterly, accessed March 19,
    2026, https://misq.umn.edu/misq/article/31/1/89/1393/Cognitive-Stopping-Rules-for-Terminating
59. Expression of uncertainty in linguistic data - ResearchGate, accessed March 19, 2026,
    https://www.researchgate.net/publication/224330446_Expression_of_uncertainty_in_linguistic_data
60. Humans overrely on overconfident language models, across languages - arXiv.org, accessed March 19, 2026,
    https://arxiv.org/html/2507.06306v1
61. Leveraging LLMs to Analyze Uncertainty Transfer in Text Summarization - ACL Anthology, accessed March 19, 2026,
    https://aclanthology.org/2024.uncertainlp-1.5.pdf
62. Can Large Language Models Faithfully Express Their Intrinsic Uncertainty in Words?, accessed March 19, 2026,
    https://aclanthology.org/2024.emnlp-main.443.pdf
63. I English Language | The Year's Work in English Studies | Oxford Academic, accessed March 19, 2026,
    https://academic.oup.com/ywes/article/95/1/1/2224964
64. We Developed a Protocol for Testing AI Self-Reflection - Results Were Surprising - Reddit, accessed March 19, 2026,
    https://www.reddit.com/r/ArtificialSentience/comments/1kynnrk/we_developed_a_protocol_for_testing_ai/
65. Technological Innovation in the Teaching and Processing of LSPs: Proceedings of TISLID'10 - Dialnet, accessed March
    19, 2026, https://dialnet.unirioja.es/descarga/libro/516208.pdf
66. A transdiagnostic conflict-square algorithm: a four-node computational framework for psychotherapy and functional
    diagnosis - Frontiers, accessed March 19, 2026,
    https://www.frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2026.1687372/full
67. research-brief-blueprint | Skills Ma... - LobeHub, accessed March 19, 2026,
    https://lobehub.com/skills/gtmagents-gtm-agents-research-brief-blueprint
68. Content Brief Generator: Build An AI Workflow For #1 Rank, accessed March 19, 2026,
    https://customgpt.ai/ai-content-brief-generator-workflow/
69. AI Agents in SEO: Content Generation, accessed March 19, 2026,
    https://seobotai.com/blog/ai-agents-in-seo-content-generation/
70. Deep Research API with the Agents SDK - OpenAI for developers, accessed March 19, 2026,
    https://developers.openai.com/cookbook/examples/deep_research_api/introduction_to_deep_research_api_agents/
71. Building Enterprise Deep Research Agents with LangChain's Open Deep Research | by Tuhin Sharma | Medium, accessed
    March 19, 2026,
    https://medium.com/@tuhinsharma121/building-enterprise-deep-research-agents-with-langchains-open-deep-research-63e7cdb80a58
72. How to use Agent Skills in Cursor IDE? - Help, accessed March 19, 2026,
    https://forum.cursor.com/t/how-to-use-agent-skills-in-cursor-ide/149860
73. Plugins Reference | Cursor Docs, accessed March 19, 2026, https://cursor.com/docs/reference/plugins
74. The PQP Framework in Practice | Agent Factory, accessed March 19, 2026,
    https://agentfactory.panaversity.org/docs/Business-Domain-Agent-Workflows/enterprise-agent-blueprint/agent-skills-pattern-in-practice
75. Benchmarking AI Quality in Dynamics 365 Sales Qualification Agent - Microsoft, accessed March 19, 2026,
    https://www.microsoft.com/en-us/dynamics-365/blog/it-professional/2025/12/11/sales-qualification-agent-benchmarks/
76. Quick research brief - Storytell.ai, accessed March 19, 2026, https://storytell.ai/prompts/quick-research-brief
77. OpenAI Deep Research AI Agent Architecture | by Cobus Greyling - Medium, accessed March 19, 2026,
    https://cobusgreyling.medium.com/openai-deep-research-ai-agent-architecture-7ac52b5f6a01
78. design-handoff | Skills Marketplace · LobeHub, accessed March 19, 2026,
    https://lobehub.com/skills/sufficientdaikon-omniskill-design-handoff
79. BrijeshRakhasiya/Deep-Research-Agent-From-Scratch: Multi-agent AI research system with LangGraph, FastAPI & RAG.
    Parallel research orchestration inspired by OpenAI Deep Research. - GitHub, accessed March 19, 2026,
    https://github.com/BrijeshRakhasiya/Deep-Research-Agent-From-Scratch
80. cursor-agents-md | Skills Marketplace - LobeHub, accessed March 19, 2026,
    https://lobehub.com/skills/trotsky1997-my-claude-agent-skills-cursor-agents-md
81. Mastering Cursor IDE: 10 Best Practices (Building a Daily Task Manager App) - Medium, accessed March 19, 2026,
    https://medium.com/@roberto.g.infante/mastering-cursor-ide-10-best-practices-building-a-daily-task-manager-app-0b26524411c1
82. A comprehensive template system for Cursor IDE, providing ready-to-use project configurations with AI-optimized
    `.cursorrules` files. - GitHub, accessed March 19, 2026, https://github.com/sangampandey/cursor-templates
83. INFORMATION USE IN RISKY DECISION MAKING: DO AGE DIFFERENCES DEPEND ON AFFECTIVE CONTEXT? - PMC, accessed March 19,
    2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC7473493/
84. What Verbalized Uncertainty in Language Models is Missing - arXiv.org, accessed March 19, 2026,
    https://arxiv.org/pdf/2507.10587
85. Lower Cohesion and Altered First-Person Pronoun Usage in the Spoken Life Narratives of Individuals with
    Schizophrenia - PMC, accessed March 19, 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC10524354/
