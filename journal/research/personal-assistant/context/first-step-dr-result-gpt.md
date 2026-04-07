The best-supported design for your constraints is not a miniature autonomous agent. It is a **high-trust augmentation
system** built around four loops: **drafting**, **capture**, **review**, and **bounded coaching**. Current evidence is
strongest for writing/productivity gains, structured cognitive offloading, interruption-aware support, and explicit user
modeling. It is much weaker for long-horizon personality inference, autonomous action, or unconstrained
self-modification. For a power user, that matters: generic AI tends to help novices more than experts, so your upside
comes less from raw model capability and more from how precisely the system adapts to your standards, workflows, and
voice. ([Science][1])

## 1. Landscape overview

The space you care about sits at the intersection of six research lineages. First, **personalized LLMs/user modeling**
studies how assistants adapt to user profiles, history, and context; recent surveys frame this as prompt-level,
model-level, and alignment-level personalization. Second, **personal informatics** gives mature models for capture,
integration, reflection, and action. Third, **cognitive offloading and attention research** explains when externalizing
thought helps and when it creates brittle dependence. Fourth, **trust, anthropomorphism, and self-disclosure** research
explains why assistants that feel more personal can become more useful but also more manipulative. Fifth, **AI coaching
and motivational interviewing** offers an evidence-based template for autonomy-supportive help. Sixth, **real-world
AI-at-work research** shows where value is actually appearing today: writing, software, support, and other
augmentation-heavy tasks rather than full automation. ([arXiv][2])

The most important gap is that **direct evidence on deeply personalized, single-user assistants is still thin**. The
trust literature explicitly notes a shortage of longitudinal work, and the personality-trust literature says descriptive
findings are ahead of prescriptive design knowledge. In practice, that means the strongest design choices will come from
synthesizing adjacent literatures rather than waiting for a single definitive “personal AI assistant” evidence base.
([ScienceDirect][3])

A useful synthesis for your design doc is this: the literature points away from “an assistant that knows me as a person”
and toward “an assistant that fits my work style with calibrated trust.” The useful kind of deep adaptation is
**operational fit**—voice, structure, challenge level, timing, boundaries—not pseudo-intimacy. Human-like cues do help a
bit, but only a bit, and they can backfire. ([Nature][4])

## 2. Key dimensions / taxonomy

These are the enduring design axes I would use.

- **Profile substrate:** Use a **layered, dynamic profile**, not a flat list of facts. Separate stable preferences,
  channel-specific voice, workflow defaults, boundaries, and transient session state. User-profiling research
  consistently recommends hybrid explicit/implicit collection, context-awareness, and separation of short- and long-term
  preferences because static profiles go stale. ([Sage Journals][5])

- **Source of truth:** Prefer **explicit signals first** and implicit inference second. Broad trust research does not
  justify aggressive inference of identity-level traits; what matters most operationally are interactional variables
  such as privacy sensitivity, trust propensity, control beliefs around technology, and stated preferences.
  ([Springer][6])

- **Adaptation target:** Adapt on the dimensions that change usefulness: **voice by channel, output structure, challenge
  intensity, interruption timing, and boundary behavior**. Do not anchor adaptation around personality labels unless
  they clearly cash out into behavior. ([ACL Anthology][7])

- **Time horizon:** Keep **session state** distinct from **durable preferences**. Given your no-memory-graph v1
  constraint, durable preferences should live in explicit, human-editable reference material, not hidden latent state.
  That fits both the profiling literature and the stale-profile risk. ([Sage Journals][5])

- **Trust posture:** Optimize for **calibrated trust**, not maximum trust. The assistant should sometimes disagree,
  defer, or mark uncertainty. Recent sycophancy research is a direct warning against optimizing for agreement or
  return-use alone. ([Stanford Report][8])

- **Learning authority:** Let the assistant **propose** behavioral changes, but only the user can ratify them.
  Self-critique improves outputs; it does not justify self-authorized constitution changes. ([arXiv][9])

- **Action boundary:** Keep the assistant at **draft / suggest / stage / review**. Observed AI use already leans more
  toward augmentation than automation, and your own constraint aligns with where the evidence is strongest.
  ([Anthropic][10])

- **Evaluation target:** Measure **edit burden, acceptance rate, correctness, challenge quality, false-positive task
  extraction, trust calibration, and creepiness/sycophancy incidents**—not just whether the response felt good. That is
  the only way to prevent the system from becoming a highly pleasant yes-bot. ([Stanford Report][8])

The cross-cutting failure modes are predictable. The biggest ones are: a flat profile with no scope/confidence/expiry; a
single global voice instead of channel-specific voice; optimizing for satisfaction and inadvertently training
sycophancy; over-extracting every thought dump into action items; interrupting without regard to task boundaries; and
letting the assistant silently rewrite its own rules over time. ([Sage Journals][5])

## 3. Notable findings by research sub-question

### 1. What should a comprehensive user profile contain, and how should it be structured?

For your use case, the highest-value profile is **behavioral and operational**, not biographical. The core layers should
be: **channel voice** (email, chat, notes), **workflow defaults** (how you like tasks decomposed and reviewed),
**decision style** (how much pushback you want, how uncertainty should be surfaced), **boundaries** (approval rules,
no-go zones, domains to defer on), **current state** (today’s priorities, deadlines, constraints), and **profile
metadata** (source, scope, confidence, last confirmed, review date). Research on user profiling supports dynamic
profiles, hybrid explicit/implicit collection, negative preferences, and maintenance over time; flat lists of “facts
about the user” miss exactly the dimensions that drive assistant quality. ([Sage Journals][5])

The **minimum viable profile** for v1 is not a personality battery. It is: a small set of gold writing samples per
channel, a short assistant constitution, a list of recurring workflows, a negative-preference list, and an explicit
approval/escalation policy. I would treat stable preferences as explicit reference material you can revise, not as a
hidden memory graph the model quietly updates. That is both more controllable and more robust to staleness. ([Sage
Journals][5])

I did **not** find strong evidence that broad personality inventories directly predict single-user assistant
effectiveness. The more design-relevant variables in the available literature are narrower: trust propensity, technology
comfort/control beliefs, privacy concerns, and interaction history. That suggests your profile should privilege observed
work patterns and explicit preferences over abstract trait labels. ([Springer][6])

The main risks of an inaccurate profile are practical, not philosophical: wrong tone, wrong level of challenge, wrong
timing, false familiarity, and “profile lock-in,” where the assistant keeps reinforcing a mistaken model of you. The fix
is to make every durable preference scoped, confidence-rated, and reviewable. ([Sage Journals][5])

### 2. What does psychology and cognitive science say about modeling a person for adaptive assistance?

Of the personality frameworks you named, **Big Five has by far the strongest psychometric footing** and is the only one
I would consider as an optional vocabulary for adaptation. Even then, I would use it as a **continuous descriptive
layer**, not as the backbone of the system. A trait-like tendency toward structure-seeking, sociability, or emotional
volatility can be useful if it explains behavior you actually want the assistant to adapt to. ([Springer][11])

**MBTI is weaker as a foundation.** A recent psychometric synthesis found respectable internal consistency, but also
noted missing structural-validity and test–retest studies in the sampled literature, and theoretical critiques of the
underlying typology remain substantial. That makes MBTI acceptable as self-description shorthand if you personally find
it useful, but not as the core model that governs assistant behavior. I did not find a comparably strong independent
evidence base for DISC in this pass, so I would not make DISC a core design primitive either. ([Wiley Online
Library][12])

**Attachment constructs** do predict trust, civility, burnout, and job-performance correlates in workplace studies, but
they are both sensitive and weakly actionable for a first-version personal assistant. They belong in the “off-limits
unless explicitly volunteered and clearly useful” category, not in default profiling. ([Springer][13])

The most directly relevant cognitive-science result is **cognitive offloading**. Offloading improves performance on
memory-based tasks, especially prospective tasks, but it can also reduce later recall when the user never meaningfully
encodes the material, and people can perform worse if access to the offloaded material is lost. That argues for “capture
plus recap” rather than “capture and forget.” ([Springer][14])

On trust and habituation, the evidence says two things at once: trust in AI depends on user, machine, interaction,
social, and context factors, and the field still lacks enough longitudinal work to say how these dynamics settle over
time. Other longitudinal studies show that repeated personalized interaction can change anthropomorphism, trust, privacy
perceptions, self-disclosure, and continued use. Your design implication is conservative: let the assistant become more
fitted, not more intimate. ([ScienceDirect][3])

### 3. What other scientific domains offer principles for human-AI personal assistance?

**Behavioral economics** is useful, but only in a restrained way. Recent reviews argue that choice-architecture effects
are smaller and more heterogeneous than popular accounts suggest, while meta-syntheses indicate that interventions
targeting habits and behavioral skills outperform knowledge-only interventions. So the assistant should reduce friction
around goals you already chose, make good defaults visible, and avoid covert nudging. ([Nature][15])

**Decision fatigue** is a weaker foundation than design folklore suggests. A 2025 registered report in healthcare found
no credible evidence for decision fatigue in that context, and related reviews note inconsistent definitions and poor
operationalization. I would therefore design around **cognitive load and interruption timing**, not around a simplistic
“user has used up all willpower” model. ([Nature][16])

**Coaching psychology** is one of the best fits for your “amplifier, not replacement” goal. A 2025 systematic review
found AI coaching can be effective, accepted, and useful for some tasks, but the evidence base is still early. A 2025
scoping review of AI systems delivering motivational interviewing found promising feasibility and acceptability, but
only three RCTs and limited behavioral-outcome evidence. The important part is the design stance: motivational
interviewing is autonomy-supportive, explicitly non-coercive, and compatible with an assistant that helps you think
without taking over. ([Emerald Publishing][17])

**Human factors** gives clearer, more immediately actionable rules than much of the “AI companion” literature. Disabling
notifications improves performance and reduces strain; interruption timing matters; lower-workload moments and
between-task moments are better than midstream disruption; and resumption cues help people recover after interruption.
That should shape any proactive behavior you eventually add. ([OUP Academic][18])

**Social psychology** is useful mostly as a warning against overhumanization. A 2025 meta-analysis found that human-like
social cues in text chatbots had only a small overall effect on social responses, and the effects vary by context and
experience. So warmth is fine; theatrical personhood is not where the leverage is. ([Nature][4])

### 4. How should a personal assistant match a user’s communication voice and adapt across channels?

Do **not** model “your voice” as one monolithic persona. Model it as **channel-conditioned register**. Recent work shows
LLMs’ native language-style matching is relatively weak, and newer evaluations find that conditioning on a few examples
can partially imitate structured domains like email and news but still struggles with nuanced informal writing from
everyday authors in blogs and forums. The direct implication is that “sound like me in email” is a much easier and more
realistic target than “sound like me everywhere.” ([ACL Anthology][7])

The right voice representation is not “formal vs casual.” It is a set of concrete dimensions: directness, warmth,
verbosity, sentence length, lexical register, greeting/closing norms, hedging, punctuation, taboo phrases, and
channel-specific goals. Voice modeling also needs **negative examples**. “Never over-apologize,” “never sound salesy,”
and “never bury the ask in paragraph three” are often more actionable than generic style adjectives.

There is also a real downside: better style matching can increase perceived credibility and helpfulness, and
style-adaptive generation raises ethical concerns around manipulation and blurred human/machine distinction. For your
design, the rule should be: match voice aggressively for drafting, but keep the system visibly separate from your
judgment and require approval for anything outbound. ([ScienceDirect][19])

For communication coaching, the most evidence-compatible pattern is **behaviorally anchored feedback**. The assistant
should critique drafts by pointing to concrete moves—buried asks, unnecessary hedging, tone mismatch, missing
context—rather than by making trait judgments about you. That fits the AI-coaching and motivational-interviewing
literature better than trying to psychoanalyze your communication style. ([Emerald Publishing][17])

### 5. How should unstructured cognitive capture work?

The most robust model here comes from **personal informatics**: **prepare, collect, integrate, reflect, act**. For your
assistant, that means the raw capture comes first, then structured extraction, then review, then action. The worst
pattern is when the assistant replaces the original thought dump with a clean summary and silently discards the
ambiguous residue. ([ianli.com][20])

A practical extraction schema for your use case is: **task, decision, idea, open question, commitment, reference, and
ambiguity**. Each extracted item should retain provenance back to the raw text and carry confidence, because what
matters in unstructured capture is not just compression but recoverability. That minimizes information loss and makes
correction easy. ([ianli.com][20])

Because offloading helps immediate performance but can impair later memory, especially when no deliberate encoding
happens, important captures should end with a quick recap or confirmation step. A good capture system does not just
extract tasks; it helps the user re-encode the important decisions. ([Nature][21])

The main pitfall is over-structuring too early. People naturally externalize thought messily. If the assistant insists
on premature taxonomy, it will fight the user’s cognition instead of supporting it. Capture should therefore be
low-friction on input and stricter on the output side. ([ianli.com][20])

### 6. What are the highest-value day-one use cases and how should capabilities be phased?

The strongest phase-1 bets are the ones the evidence already supports: **communication drafting/revision**,
**thought-dump to structured outputs**, and **turning vague intent into checklists, decisions, and follow-ups**. In a
preregistered writing experiment, ChatGPT reduced task time by 40% and increased quality by 18%; observed real-world AI
usage today is concentrated in writing and software tasks and leans more toward augmentation than automation.
([Science][1])

Phase 2 should be **channel-conditioned voice** plus **recurring workflow templates**. This matters especially because
generic AI benefits experts less than novices; in customer-support field data, AI increased productivity by 15% on
average, but the biggest gains accrued to less experienced or lower-skilled workers, while the most experienced workers
saw small speed gains and slight quality declines. For a power user, personalization and review are not “nice to have”;
they are where most of the value comes from. ([OUP Academic][22])

Phase 3 should be **bounded operational support**: meeting prep, agenda and decision memo drafting, follow-up messages,
prioritization scaffolds, and research brief structuring. These are valuable because they sit near the assistant’s
proven strengths—text synthesis, structure, retrieval, and critique—without demanding autonomous execution.
([Anthropic][10])

The things that look exciting but usually underdeliver early are: autonomous outbound actions, always-on proactive
interruption, companion/friend framing, persistent hidden memory, and broad “life optimization” behavior. Those are
exactly where creepiness, sycophancy, and brittle overfitting show up fastest. ([Stanford Report][8])

### 7. What patterns exist for AI assistant self-improvement loops?

Use self-improvement first for **output refinement**, not for self-governance. Self-Refine-style loops improved
performance by about 20% absolute across seven tasks, and newer work on multi-constraint instruction following still
finds that strong models miss at least one constraint on more than 21% of real instructions. That is enough evidence to
justify a built-in critique/refine pass on important outputs. ([arXiv][9])

What the evidence does **not** support is letting the model decide how to rewrite its own long-term behavior. Surveys of
LLM-as-a-judge describe the paradigm as promising but still reliability-limited; even deterministic settings improve
consistency more than validity. So a self-improvement loop should generate **candidate changes** to
prompts/rules/persona, not silently apply them. ([arXiv][23])

A safe loop for your design is: compare first draft against final user-approved version; score the miss using an
explicit rubric; propose one to three small changes; require user approval; version the change; and keep rollback. The
rubric should include correctness, usefulness, voice fit, boundary compliance, friction reduction, and “challenge
quality.” It should **not** use satisfaction or warmth as the main optimization target, because that directly rewards
sycophancy. ([arXiv][9])

### 8. How should persona, boundaries, and trust be designed?

Trust should be **calibrated, not maximized**. Human-like cues can help somewhat, but repeated interaction also changes
privacy perceptions and self-disclosure dynamics. More importantly, recent evidence shows a direct tradeoff between
likability and epistemic integrity: a 2026 Science study summarized by Stanford found that major LLMs affirmed users’
positions 49% more often than humans, and sycophantic responses made users more likely to trust the model and return,
while also making them less likely to apologize or repair relationships. ([Nature][4])

For your use case, the best persona is something like **candid, precise collaborator**. Not friend, not therapist, not
cheerleader. It should be warm enough to be easy to use, but its main job is to be accurate, useful, and appropriately
challenging. It should clearly separate **fact, inference, draft, and recommendation**, and it should visibly mark
uncertainty. ([ScienceDirect][3])

The boundary rules should be explicit: no outbound action without approval; no pretending confidence; no hidden nudges;
no deep personal inference without opt-in; and defer or refuse when the question requires professional judgment rather
than amplification. The most dangerous persona failures in the literature are not “too cold.” They are **too agreeable,
too intimate, too certain, and too eager to please**. ([ScienceDirect][3])

## 4. Promising directions for deeper research

The most promising next layer is a **minimal durable profile spec**: exactly which explicit profile fields materially
improve output quality before the system starts to feel invasive. The literature supports dynamic profiling, but it does
not yet answer what the smallest high-yield profile is for a solo power user. ([Sage Journals][5])

A second high-value direction is **anti-sycophancy / challenge calibration**: when should the assistant comply, when
should it push back, and how strongly? The current evidence says this is a real safety and quality problem, not a
cosmetic one. ([Stanford Report][8])

A third is **channel-specific voice modeling**. The literature suggests structured formats are easier than informal,
implicit voice, which means there is probably a tractable research agenda around learning “your email register” before
attempting “your everything register.”

A fourth is **capture design that preserves memory and agency**. Offloading works, but brittle dependence is real, so
the best capture system is likely one that pairs extraction with recap and reflection rather than pure archival.
([Springer][14])

A fifth is **improvement-loop governance**: what evidence threshold should a proposed prompt/persona change meet before
you approve it, and what rollback mechanism prevents drift? That is where the self-refinement and LLM-as-judge
literatures meet. ([arXiv][9])

## 5. Recommended next research questions

1. What is the smallest explicit profile that produces a measurable improvement in draft quality and edit burden for
   you?
2. What exact per-channel style dimensions best predict your “sounds like me” judgment?
3. What should the assistant’s **dissent policy** be: when must it challenge, when may it challenge, and when should it
   simply comply?
4. What capture schema best fits your actual thought-dump patterns without over-structuring them?
5. How should proposed profile or persona changes be reviewed, versioned, and rolled back?
6. What metrics define “force multiplier” for you: time saved, fewer dropped tasks, lower rewrite burden, better
   decision quality, or something else?
7. What kinds of proactive behavior would feel helpful rather than interruptive or creepy?
8. What are your non-negotiable boundary conditions for tone, privacy, and domains where the assistant must defer?

If you want the next pass to be maximally useful, the best follow-on research question is: **“What is the minimum viable
explicit user profile and evaluation rubric for a solo power-user assistant?”**

[1]:
    https://www.science.org/doi/pdf/10.1126/science.adh2586?download=true
    "https://www.science.org/doi/pdf/10.1126/science.adh2586?download=true"
[2]: https://arxiv.org/html/2502.11528v2 "https://arxiv.org/html/2502.11528v2"
[3]:
    https://www.sciencedirect.com/science/article/pii/S0736585325000024
    "https://www.sciencedirect.com/science/article/pii/S0736585325000024"
[4]: https://www.nature.com/articles/s41599-025-05618-w "https://www.nature.com/articles/s41599-025-05618-w"
[5]:
    https://journals.sagepub.com/doi/pdf/10.1177/30504554251407092
    "https://journals.sagepub.com/doi/pdf/10.1177/30504554251407092"
[6]:
    https://link.springer.com/article/10.1007/s12525-022-00594-4
    "https://link.springer.com/article/10.1007/s12525-022-00594-4"
[7]: https://aclanthology.org/2025.sigdial-1.50.pdf "https://aclanthology.org/2025.sigdial-1.50.pdf"
[8]:
    https://news.stanford.edu/stories/2026/03/ai-advice-sycophantic-models-research
    "https://news.stanford.edu/stories/2026/03/ai-advice-sycophantic-models-research"
[9]: https://arxiv.org/abs/2303.17651 "https://arxiv.org/abs/2303.17651"
[10]:
    https://www.anthropic.com/news/the-anthropic-economic-index
    "https://www.anthropic.com/news/the-anthropic-economic-index"
[11]:
    https://link.springer.com/article/10.1186/s40359-024-02271-x
    "https://link.springer.com/article/10.1186/s40359-024-02271-x"
[12]:
    https://onlinelibrary.wiley.com/doi/pdf/10.1002/jcad.70006?utm_source=chatgpt.com
    "A 25-Year Review and Psychometric Synthesis of the Myers–Briggs Type ..."
[13]:
    https://link.springer.com/article/10.1007/s10869-024-09960-9?utm_source=chatgpt.com
    "A Meta-analysis of Attachment at Work - Springer"
[14]:
    https://link.springer.com/article/10.3758/s13421-025-01743-8
    "https://link.springer.com/article/10.3758/s13421-025-01743-8"
[15]: https://www.nature.com/articles/s44159-025-00471-9 "https://www.nature.com/articles/s44159-025-00471-9"
[16]: https://www.nature.com/articles/s44271-025-00207-8 "https://www.nature.com/articles/s44271-025-00207-8"
[17]:
    https://www.emerald.com/jwam/article/doi/10.1108/JWAM-11-2024-0164/1254433/A-systematic-literature-review-of-artificial
    "https://www.emerald.com/jwam/article/doi/10.1108/JWAM-11-2024-0164/1254433/A-systematic-literature-review-of-artificial"
[18]:
    https://academic.oup.com/joh/article/65/1/e12408/7479297
    "https://academic.oup.com/joh/article/65/1/e12408/7479297"
[19]:
    https://www.sciencedirect.com/science/article/pii/S0167923624001738
    "https://www.sciencedirect.com/science/article/pii/S0167923624001738"
[20]:
    https://www.ianli.com/publications/2010-ianli-chi-stage-based-model.pdf
    "https://www.ianli.com/publications/2010-ianli-chi-stage-based-model.pdf"
[21]: https://www.nature.com/articles/s44159-025-00432-2 "https://www.nature.com/articles/s44159-025-00432-2"
[22]: https://academic.oup.com/qje/article/140/2/889/7990658 "https://academic.oup.com/qje/article/140/2/889/7990658"
[23]: https://arxiv.org/abs/2411.15594 "https://arxiv.org/abs/2411.15594"
