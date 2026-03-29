# Question Crystallization Skill Design

## Summary

Research into the optimal structure for an AI agent skill that guides users from vague, pre-articulate intuitions to well-defined research questions. Cross-references cognitive psychology, information science, prompt engineering, and ADHD-informed interaction design.

## Key findings

### Core insight

The skill must systematically abandon the assumption that users can spontaneously recall and articulate their implicit knowledge. Instead, it should function as an **external working memory prosthetic** and **co-regulatory scaffold**, prioritizing recognition over recall at every interaction point.

### Theoretical foundations

- **Gendlin's "felt sense"** -- inquiry begins as a pre-verbal, somatic awareness of a knowledge gap. Early-stage interactions must validate ambiguity rather than demand precision
- **Kuhlthau's Information Search Process (ISP)** -- validated phase model: Initiation (uncertainty) → Selection (brief optimism) → Exploration (confusion/doubt) → Formulation (clarity). The skill operates in the volatile Initiation→Formulation trajectory
- **Reference Interview** (library science) -- formalized process for helping people articulate information needs they can't yet express. Phases: Approachability, Interest, Listening/Inquiring, Searching, Follow-up
- **Cognitive Task Analysis + Laddering** -- structured techniques for extracting implicit knowledge. Laddering moves vertically (concrete→abstract and back) and laterally to map the conceptual space
- **Modified Socratic method** -- gentle "how"/"why" questions that guide without adversarial cross-examination. Traditional Socratic method induces too much cognitive load for ADHD users

### Design principles (evidence-grounded)

1. **Recognition over recall** -- never ask open-ended generative questions. Always synthesize context and present 3-4 bounded multiple-choice options. Transforms high-load generation into low-load evaluation
2. **Progressive refinement** -- address one dimension at a time. Separating validation (intent) from verification (specifics) produces higher-quality outputs with fewer misalignments
3. **Externalize state** -- every response must restate accumulated context. The agent is the working memory, not the user
4. **Cognitive stopping rules** -- three mechanisms to prevent infinite refinement:
   - Mental List Rule: predefined checklist of research brief components; exploration ends when all are populated
   - Difference Threshold Rule: detect when refinements are semantic tweaks rather than substantive shifts
   - Representational Stability Rule: the formulation has stopped shifting
5. **Linguistic marker detection** -- monitor hedges ("maybe," "sort of") vs. boosters ("exactly," "yes, this is it") as signals of exploration vs. crystallization. Caveat: neurodivergent users may hedge even when internally certain

### Recommended architecture: Three-Phase Funnel

**Phase 1: Intuition Anchor** (divergence)
- Open dump: invite unstructured brain-dump, explicitly state formatting/coherence doesn't matter
- Hypothesis generation: agent reflects input as 3-4 distinct research angles (recognition, not recall)
- Selection: user picks, combines, or rejects. Agent locks initial trajectory

**Phase 2: Dimension Funnel** (laddering & scoping)
- Work through research brief dimensions one at a time
- Ladder up (abstraction): "What decision will this support?"
- Ladder down (constraints): "Should we exclude X?"
- State tracker prepended to every response showing established parameters and what's missing

**Phase 3: Crystallization Check** (convergence)
- Synthesis playback: draft primary question + 3-4 sub-questions
- Anti-pattern check: propose explicit exclusions for boundary confirmation
- Final approval: user confirms, triggers handoff artifact generation

### ADHD-specific adaptations

- **Task initiation paralysis**: agent initiates cognitive heavy lifting. Default options, suggested starting points, "type 'help me explore' to start with a single question"
- **Co-regulation**: affirm divergent/associative input as valuable ("excellent associative depth here, synthesized into three themes"). Never demand reorganization before processing
- **Hyperfocus management**: architecture must handle massive unstructured text dumps without losing thread
- **Time blindness**: explicit progress indicators ("Step 2 of 4"), strictly one question per turn
- **Always include "none of the above, let's pivot"** to prevent passive acceptance of AI-generated options during low energy states

### Handoff design

Output is a standardized research brief with 5 components:
1. Primary research question (single unambiguous sentence)
2. Semantic core & entities (audience, intent, 3-5 core concepts)
3. Required sub-themes (specific dimensions to explore)
4. Exclusion criteria (explicit anti-patterns/guardrails)
5. Expected deliverable format

### Open questions

- **Hallucinated intent risk**: multiple-choice hypotheses may steer away from novel ideas the AI failed to generate. Mitigated by persistent "none of the above" option
- **Linguistic marker reliability**: neurodivergent users may hedge as social masking even with internal clarity. Must balance linguistic analysis with hard Mental List criteria
- **Context window limits**: massive brain dumps risk "lost in the middle" phenomenon. Requires continual summarization and chunked processing

## Source files

- `context/gemini-result.md` -- Gemini Deep Research output (primary source, 81 citations)
