# Cruising Upward as a Staff-Level Engineer in a Fast Startup and Consultancy

## Context and definition of “cruising upward”
You’re describing a very specific senior-IC reality: you sit at a comparatively senior level *inside your consultancy*, while being an “elite foot soldier” inside a fast-moving client startup. That combination creates two parallel expectations and two parallel reputations, which means your *actual* job is “deliver outcomes + manage context + preserve trust across two organisations”, not “write code”. This is common in staff-plus roles: the further you move beyond Senior, the more the role shifts from purely implementing to defining direction, unblocking, aligning, and maintaining credibility across people who are not in your reporting line. citeturn2view0turn19view0turn3view0

A useful way to define **cruising upward** (in your situation) is:

**Cruising upward = increasing your scope and trust *gradually* while keeping your effort sustainable and your risk profile low.**

It is not “being a star” or “doing hero hours”; it’s the opposite: becoming *predictably valuable* and *making the right things easy for other people*. Many org ladders and staff-engineering guides emphasise that after you reach Senior, you’re often no longer “required” to chase the next promotion, and promotions beyond Senior become “exceptional rather than expected”—so upward motion past that point tends to come from selective, high-leverage behaviour rather than more raw work. citeturn2view0turn4view0

In other words, your baseline target is: **become hard to replace because you reduce uncertainty**, not because you outwork everyone.

## What research says drives “upward” outcomes for non-managers
Even when you’re not on a management track, there’s substantial evidence that career outcomes (pay, promotion, perceived success) correlate with a few broad behavioural clusters: being proactive, building social capital, and navigating workplace dynamics with “political skill” (in the academic sense of social effectiveness, not cynicism).

**Proactivity and extra-role behaviour compound career success.** A large meta-analysis using meta-analytic structural equation modelling (sampled across 100k+ employees) found proactive personality relates to career success indicators (salary, promotion, subjective career success) through mediators including task performance and organisational citizenship behaviour (OCB—helping, contributing beyond formal requirements). Importantly, the mechanisms differ by outcome (e.g., salary links were mediated by both task performance and OCB; promotions showed stronger OCB-related pathways). citeturn11view0

**Political skill predicts performance and reputation beyond raw ability signals.** A major meta-analysis (Munyon et al.) defines political skill as the ability to understand others at work and use that knowledge to influence actions that enhance personal and/or organisational objectives. It also finds political skill predicts task performance above and beyond standard predictors like Big Five personality traits and general mental ability, and relates strongly to personal reputation and career success indicators. citeturn10view0turn10view1  
For a senior IC, the pragmatic translation is: *how you create alignment, reduce friction, and communicate uncertainty* becomes part of performance—not “nice to have”.

**Networking measurably affects objective outcomes over time.** A longitudinal study in the *Journal of Applied Psychology* found networking (building, maintaining, using relationships) is related to concurrent salary and—crucially—salary growth rate over time. citeturn13view0  
This matters in your setup because you effectively need two networks: one inside the consultancy (for internal growth, staffing influence, candidate evaluation credibility) and one inside the startup (for delivery and day-to-day impact).

**Engineering ladders operationalise “impact” as scope × execution quality over time.** Dropbox’s published engineering framework makes this explicit: impact is anchored on business results, and described as a function of *scope of impact* and *how you execute*. It also foregrounds **consistency** (sustained delivery over time), not just one-off wins. citeturn18view0  
This is an unusually helpful anchor for “cruising”: it legitimises doing *fewer*, higher-quality, higher-leverage things—reliably.

**The staff-plus shape: choose your archetype deliberately.** StaffEng’s taxonomy highlights four common staff-plus archetypes—Tech Lead, Architect, Solver, Right Hand—each with different interaction patterns and recognition risks. (“Solver” roles often bounce from hotspot to hotspot; Tech Leads carry team context and cross-functional relationships.) citeturn3view0  
Given your description (“agent design/maintenance”, dynamic environment, sometimes deep dives), you likely oscillate between **Solver** (knotty problems, execution risk) and **Tech Lead** (coordination, scoping, unblocking). Knowing which mode you’re in helps you pick the right communication and time-management tactics.

## Communication architecture that enables “cruising”  
Your question explicitly calls out communication as the hardest part—especially with ADHD and a tendency to deep-dive. The goal is to make communication do three jobs simultaneously:

**Create clarity, create trust, and create a record.**

### Trust and psychological safety as performance multipliers
Research on team learning identifies **psychological safety** as a shared belief that the team is safe for interpersonal risk-taking; Edmondson’s field study links psychological safety to team learning behaviour and shows learning behaviour mediates the relationship between psychological safety and team performance. citeturn15view1  
Google’s Project Aristotle write-up (re:Work) similarly reports that what mattered most was less “who is on the team” and more “how the team works together”, listing psychological safety as the top dynamic, alongside dependability and structure/clarity. citeturn16view0

For you as a senior IC (not the boss), the “cruise upward” play is to **model psychologically-safe behaviours without turning into a therapist**:
- ask clarifying questions early (normalise not knowing),
- surface risks quickly (normalise uncertainty),
- admit mistakes with a fix-forward plan (normalise learning),
- treat other people’s mistakes as system signals, not personal failures.

These behaviours increase *team throughput* and also increase your reputational capital as someone who is safe to work with. citeturn15view1turn16view0turn19view0

### Communicate at the right altitude
Staff-level expectations often explicitly call out “message to audience” and “right altitude”. Dropbox’s staff SWE expectations include tailoring the message, presenting clearly and concisely, and writing crisp narratives that enable decision-making. citeturn19view0  
Stripe’s public guide includes an interviewer rubric that penalises communication that becomes unclear or “rambling for a long time”, and rewards high-level points backed by concrete examples; while it’s written for interviews, it’s revealing because it reflects what high-performing engineering orgs *select for*. citeturn33view0

A practical cognitive model that works well for ADHD brains is to treat “altitude” as a *deliberate constraint*:

- **30,000 ft (strategy):** what outcome matters, what trade-offs, what risk, what’s next.
- **10,000 ft (plan):** milestones, interfaces, owners, dependencies, timeline.
- **Ground level (details):** implementation notes, edge cases, logs.

Cruising upward means: default to 30,000/10,000 in group settings; keep ground-level detail available *on demand* (doc, thread, PR description), not as an unprompted verbal download. This aligns with both staff expectations and the “don’t lose people in the conversation” failure mode. citeturn19view0turn33view0

### “Never surprise your manager” becomes “never surprise your stakeholders”
StaffEng’s guidance on staying aligned with authority is blunt: **surprises destroy trust**, and many staff-plus roles succeed by feeding context upward and using regular updates so leaders are not blindsided. citeturn5view0  
In your case, you likely have *at least three manager-equivalents*:
- consultancy people leadership / account leadership,
- the startup’s day-to-day product/engineering leadership,
- and sometimes “shadow stakeholders” (security, infra, PMs) who can block work.

So redefine the rule as:  
**Never surprise the person who will be blamed.**  
If a miss, risk, or ambiguity would roll uphill to them, tell them early with a proposed mitigation.

## Behaviour patterns that let you grow without becoming a “hero”
This is the “framework” part: actionable behaviours for recurring scenarios in a fast startup + consultancy context. The intention is not perfection; it’s a consistent, low-drama operating style that compounds trust and scope.

### Start every piece of work by turning ambiguity into agreements
Your deep-dive tendency is not inherently bad—Solvers are valuable precisely because they can go deep. The risk is *unbounded exploration* (high effort, unclear payoff). The fix is to always begin with a short alignment artefact:

**The Alignment Trifecta (send as a 6–10 line message or short doc):**
- **Outcome:** “We’re trying to achieve X for user/business Y.”
- **Constraints:** “We must not break Z; deadline/latency/cost bounds are A/B/C.”
- **Decision point:** “I propose option 1/2; I need a decision by <time>.”

This pattern maps directly onto “structure and clarity” as a driver of team effectiveness (Google), and it reduces the probability that you’ll later be penalised for being “right” but building the wrong thing. citeturn16view0turn18view0

### Timebox depth and make the timebox visible
StaffEng warns against “snacking” (easy, low-impact work) and also against “preening” (low-impact, high-visibility work), but it also makes the core point: time is finite, and pacing is essential for sustained success. citeturn4view0  
In your world, the failure mode is often the mirror image: **high-effort depth that is not proportionate to the task**.

Use a visible timebox that forces a checkpoint:
- “I’ll spend 90 minutes investigating. By then I’ll return with: (a) recommendation, (b) risks, (c) what I need from you.”
This is not bureaucratic—this is risk management and expectation management.

### Build “dependability” as a personal brand
Google re:Work lists **dependability** as a key dynamic: reliably completing quality work on time. citeturn16view0  
Dropbox’s career framework explicitly values **consistency** over time. citeturn18view0

For cruising upward, dependability beats brilliance. Concretely:
- Under-promise, over-deliver on timelines.
- If you suspect a slip, communicate before the slip occurs (risk-first updates).
- Close loops: “done” means shipped, documented, and handover/monitoring agreed—consistent with “we only get value from finishing projects” emphasis in staff-level guidance. citeturn4view0turn18view0

### Do “glue work”, but don’t drown in it
Tanya Reilly’s “glue work” framing is especially important for someone in consulting + startup execution: glue work includes noticing blockers, addressing inconsistencies, onboarding, writing docs, improving processes, and generally doing the coordination that makes projects succeed. She explicitly warns that doing glue work too early can become career-limiting, because it may not be rewarded even if it makes the team better. citeturn17view0

Cruising upward requires a controlled approach:
- Do glue that **unblocks revenue/critical path** or prevents **repeat incidents**, not glue that substitutes for missing management indefinitely.
- Make glue work legible: convert it into artefacts (“playbook”, “runbook”, “design memo”, “onboarding checklist”), not invisible labour. citeturn17view0turn18view0

### Treat relationships as an explicit deliverable
This is where the research on networking, political skill, and OCB becomes very practical:
- Networking correlates with salary growth over time. citeturn13view0
- Political skill predicts performance and reputation, not just “likability”. citeturn10view0turn10view1
- OCB can help mediate longer-term career success pathways. citeturn11view0

A non-cringey translation is: **be easy to work with at scale**.
- When you meet someone relevant, follow up with something useful (a doc, a decision summary, a link to a PR).
- Credit others publicly; escalate issues privately.
- When you disagree, keep the disagreement about trade-offs and outcomes, not competence.

If you want a *single* relationship model that also matches consulting realities, the “trust equation” commonly attributed to *The Trusted Advisor* frames trust as a function of credibility, reliability, and intimacy divided by self-orientation (self-focus). citeturn32view0  
Even without buying into the maths, the behavioural guidance is gold for consulting-like environments: show competence (credibility), be predictable (reliability), create safety (intimacy), and reduce signals that you’re optimising for ego/credit (low self-orientation). citeturn32view0turn16view0

## ADHD-informed tactics for communication, scope, and attention
I’ll avoid medical advice, but it’s important to be evidence-aligned about what ADHD tends to disrupt at work: attention regulation, organisation/time management, and impulse control in communication are explicitly listed in mainstream clinical sources. The NHS notes that adults with ADHD may be easily distracted/forgetful, find it hard to organise time, have difficulty following instructions/finishing tasks, and may be very talkative or interrupt conversations. citeturn20view0  
Research also links adult ADHD to executive-function difficulties (e.g., inhibition, working memory, plan/organise), and these areas relate to real-world functional impairments. citeturn21view0  
Medication can improve cognition/executive function measures over longer-term treatment, but it is not positioned as erasing the need for behavioural strategies. citeturn22view0turn20view0

### The core strategy: externalise working memory and “definition of done”
Because working memory and plan/organise functions are common pain points, treat your system as if your brain is not a reliable storage device. citeturn21view0turn22view0

Practical pattern:
- Every task gets a **one-screen “contract”**: outcome, constraints, next milestone, and how you’ll report progress.
- Every meeting ends with a **written decision + owner + next step** (even if it’s just a short message).
This directly supports the “structure and clarity” and “dependability” drivers highlighted by Google’s effectiveness research. citeturn16view0

### Use “guardrails” to prevent unbounded deep dives
Deep dives become harmful when they are misaligned, not when they are deep. So you don’t want to stop going deep; you want to make depth conditional on signal.

Three guardrails that work well in fast startups:
- **Timebox + checkpoint** (“90 minutes, then update with recommendation”).  
- **Two-path plan** (“Path A: ship something robust by Friday; Path B: deeper redesign next sprint”).  
- **Escalation threshold** (“If I hit uncertainty X or dependency Y, I’ll ask for a decision instead of continuing solo.”)

These guardrails also operationalise “never surprise your manager/stakeholders” because you’re creating planned points for surfacing risk. citeturn5view0turn16view0

### Communication scripts that reduce “rambling risk”
If your risk is verbal over-explaining, use scripted constraints that mirror what strong orgs rate as clarity: high-level point + specific example, with responsiveness to prompts. citeturn33view0turn19view0

Try these two scripts:

**The one-breath opener (forces altitude):**  
“**Recommendation:** X. **Because:** Y. **Risk:** Z. **Need from you:** decision/approval on A.”

**If asked for detail:**  
“I can go deeper—do you want implementation details, edge cases, or risk trade-offs?”

This preserves your ability to be thorough while signalling social calibration (political skill as social effectiveness). citeturn10view0turn33view0

### Reasonable adjustments as performance tooling, not weakness
Independent of whether you disclose, it’s useful to know that UK employment guidance treats neurodivergence as often amounting to a disability under the Equality Act, and Acas provides concrete examples of adjustments for concentration, written communication, organisation/time management (check-ins, visual planners, extra reminders, breaking work into smaller tasks). citeturn23view0turn20view0  
This can be framed internally as “I’m optimising my throughput and reducing risk”, not as “special treatment”.

## A curated reading list and research agenda tailored to your niche
You asked for literature that is not “manager-only”, and more relevant to a staff-level IC who needs to communicate and behave effectively without being on a formal manager track. Here’s a focused set, organised by the problems you’re solving.

### Staff-level IC craft, scope, and “what to work on”
Will Larson’s *Staff Engineer* material is unusually aligned with your situation because it treats staff as a distinct job (not “senior with more years”), includes archetypes, and covers how to choose work and stay aligned with authority. citeturn2view0turn3view0turn5view0turn4view0  
Combine it with a published career framework like Dropbox’s, which concretely defines impact, consistency, and staff expectations including communication behaviours. citeturn18view0turn19view0

**Research agenda:** map your current responsibilities against one staff archetype (Solver vs Tech Lead), then run a monthly review: “Did my work increase scope/impact, or just activity?” citeturn3view0turn18view0turn4view0

### Communication, team dynamics, and psychological safety
Amy Edmondson’s 1999 paper is a foundational empirical anchor: psychological safety → learning behaviour → performance. citeturn15view1  
Google’s re:Work write-up is a practitioner-friendly translation that also names dependability and structure/clarity—useful because it converts “soft skills” into observable behaviours. citeturn16view0

**Research agenda:** treat “psych safety moments” as technical incidents: when a misunderstanding happened, ask “what signal did I miss, and what system would prevent recurrence?”

### Consulting-style trust and stakeholder management for engineers
If you work inside a client startup as a consultant, “trusted advisor” dynamics matter even when you’re hands-on. The trust equation model (credibility + reliability + intimacy, divided by self-orientation) is one compact way to audit how you come across. citeturn32view0  
Even if you never use the formula explicitly, it pairs well with the research-backed emphasis on psychological safety and dependability. citeturn16view0turn32view0

**Research agenda:** after key interactions (tense incident, disagreement, scope negotiation), ask which variable you strengthened: credibility, reliability, intimacy, or reduced self-orientation.

### ADHD at work: evidence-aligned self-management and accommodations
For baseline correctness and UK relevance, use NHS and NICE as your stable starting points for symptoms and management options. citeturn20view0turn7search0  
Use Acas for workplace adjustment ideas that are framed in employer/employee terms, not social media terms. citeturn23view0  
For cognition/executive function evidence, the KCL summary of a systematic review/meta-analysis is a readable bridge into the research literature, and reinforces that cognition impacts occupational performance. citeturn22view0

**Research agenda:** run small experiments (two-week sprints) with one adjustment at a time (daily check-in, written instructions, timeboxing rule). Track whether dependability improves (missed deadlines, surprise slips) rather than tracking “hours worked”. citeturn23view0turn18view0turn16view0

---

If you boil this entire report into a single operating principle, it’s this: **cruising upward is the art of converting your technical ability into organisational dependability and decision clarity—without consuming your life.** The literature converges on that from multiple angles: career success research (proactivity, political skill, networking), staff engineer guidance (work on what matters, stay aligned), and team performance research (psych safety, dependability, clarity). citeturn11view0turn10view0turn13view0turn4view0turn5view0turn16view0