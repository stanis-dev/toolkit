# Cruising Upward with Quiet Confidence as a Forward‑Deployed Contractor at Sierra

## Your operating environment in plain terms
Your situation is not “generic senior engineer in a normal org”. It is a high-contact, boundary-crossing role: **forward‑deployed engineering** in a fast startup, while being employed via a consultancy. Forward‑deployed engineers are typically described as a hybrid role that bridges product capability and real customer adoption, working closely with customers and internal teams to scope, implement, unblock, and iterate quickly. citeturn1search0turn1search2

Sierra’s own description of **Agent Engineers** is unusually aligned with the forward‑deployed pattern: Sierra describes agent engineers as people who **work with customers to design, build, and ship agents** using Sierra’s platform (“Agent OS”), and stresses that shipping agents at scale is materially harder than building demos. citeturn8view0 Sierra also positions Agent Engineering as a blend of software engineering, modern AI stack, and deep customer/domain understanding, including use of Sierra’s Agent SDK as part of the orchestration and control-flow layer. citeturn8view0

For the “Agent Strategist” (what you called “Agent Strategist / Agent Engineer / PM” triangle), public role descriptions show a function oriented around **delivery orchestration and customer advisory**: the Agent Development Strategist partners with Agent PMs and Agent Engineers to scope, build, and ship agents; combines product strategy, conversational design, and customer insight; and is accountable for clear communication across stakeholders while driving complex, high-visibility delivery. citeturn10view0 This matters because it tells you what your internal Sierra counterparts are optimised for: they are not “just support”; they are meant to be “trusted advisor + delivery driver” under pressure. citeturn10view0

You also flagged a cultural factor that strongly shapes communication norms: Sierra publicly describes an **in‑person, in‑office culture**, emphasising that working side by side helps them move faster and build stronger relationships. citeturn12view0 Separately, Sierra’s published values (in at least one job listing) highlight “Trust”, “Customer Obsession”, “Craftsmanship”, and—crucially—“Intensity” (explicitly framing urgency, fixing what isn’t right, and learning without blame). citeturn10view0 When you’re remote from Spain working with the London office, you’re effectively operating with a built-in “visibility tax” in a culture that self-identifies as in-office and “intensity” oriented. citeturn12view0turn10view0

Finally, your tooling constraints (“no source access”, “no logs”, “debug info must go through Sierra employees”) are not just organisational friction; they’re consistent with a standard security posture where access is constrained by **least privilege**—granting only the minimum authorisations needed to do the job. citeturn7search0 Whether this is driven by compliance, incident risk, or customer data obligations, it changes your day-to-day reality: you are forced into a *request-and-response debugging loop* rather than direct inspection, which makes communication skill and trust-building even more central than in a typical IC role. citeturn7search0turn8view0

## What from the original report still holds and what changes in your constraints
A lot of the original report still stands, but the “why” becomes sharper—and a few parts need to be reframed around **employment status boundaries** and **remote visibility**.

The “still true” core: sustained progression (your “cruise upward”) is strongly tied to being reliably useful and reducing uncertainty for others, not to being heroic. Research linking proactivity and extra-role contribution (OCB) to career success broadly supports the idea that consistent, visible helpfulness can contribute to positive career outcomes. citeturn0search0 In your context, however, the form of “helpfulness” must be *low-drama and low-overhead* for Sierra employees who are already operating in high intensity. citeturn10view0

Where the original report was too generic is that it didn’t fully account for the **outsider dynamics** you’re describing. There is direct research evidence that when internal employees and external consultants work together, knowledge sharing often follows in‑group/out‑group lines: employees tend to share knowledge with employees, while external consultants share more with other external consultants, and category‑specific trust predicts knowledge sharing across those boundaries. citeturn4view0 That finding is basically a research-backed version of what you’re noticing: being “the contractor” can make information flow more fragile even if nobody is being malicious. citeturn4view0

This is reinforced by research on **perceived insider status (PIS)** among outsourced workers. One study reports that outsourced employees tend to be lower in perceived insider status and, indirectly, lower in job performance compared to standard employees, and that the “gap” can be especially strong when the outsourced worker is in a core-status, high-value role. citeturn15search11turn6view0 The implication for you is not “try harder”; it’s that *status signals and belonging cues become functional tools* for keeping information and responsiveness flowing.

Your “contractor is a dirty word” observation is also aligned with contract-work research on perceived status. A paper explicitly framing contract workers as “second-class citizens” examines a triangular relationship (worker–employer–client) and defines perceived “employment status similarity” as whether a contract worker feels valued comparable to standard employees at the client; that perceived similarity predicts commitment and relates to intent to quit. citeturn16view0 Even if you personally don’t mind, **others’ categorisation behaviour** can still alter responsiveness, warmth, and cooperation. citeturn4view0turn16view0

The second big “modifier” relative to the original report is your remote position in an in-office leaning culture. “Proximity bias” is widely discussed as managers favouring people who are physically closer (more visible) even when performance is comparable, and it is explicitly tied to visibility concerns in hybrid/remote contexts. citeturn3search1 You are not only remote; you are also status‑boundary (“contractor”) and tooling‑boundary (restricted access). So your version of “visibility” must be engineered through crisp outputs, written artefacts, and predictable communication patterns. citeturn3search1turn12view0turn4view0

Finally, the “feedback vacuum” you described is not just annoying; it creates chronic uncertainty. The feedback-seeking literature distinguishes two broad strategies: **monitoring** (reading cues) and **inquiry** (asking). citeturn2search3turn2search11 Your current approach is being forced into “monitoring” (“interpreting grunts”). The research-informed upgrade is to introduce *very low-cost inquiry* that doesn’t feel like a performance review request—because, per feedback-seeking models, people weigh the value of feedback against the social/effort costs of seeking it. citeturn2search7turn2search11

## A communication system designed for scarce replies, high pace, and low access
Given your constraints, your communication system has to do three things at once: reduce load for Sierra employees, create “status similarity” cues (quiet confidence), and keep you moving when answers are slow.

Start with a core principle: **every message must make it easy to respond**. In a high-intensity culture that values responsiveness and “dropping everything” when a customer has an issue, high-friction messages (long context dumps, multiple asks, uncertain ownership) are silently deprioritised. citeturn10view0turn3search3 This is amplified by communication overload dynamics: research on e-mail overload frames overload as a combination of information volume, frequency, and cognitive inability to process the flow, with a “culture of urgency” being one observed negative effect. citeturn3search3

A practical template that fits your situation is a four-line “constraint-to-plan” format:

**Context → Constraint (fact) → Plan (what I’ll do) → Ask (one thing, with a deadline)**

Example (internal Sierra thread):
- **Context:** “Customer reports: refund workflow failing for UK users since yesterday.”
- **Constraint (neutral):** “I don’t currently have direct access to production logs for this integration.”
- **Plan:** “I’ve reproduced via staging + narrowed it to step ‘X’ failing after tool call ‘Y’. Next I’ll validate prompt/tool schema mismatch hypotheses.”
- **Ask:** “Could you paste the last 20 lines of the relevant trace for conversation ID ___ (or run query ___) by 14:00? If not you, who’s the right owner?”

This works because it respects least-privilege access boundaries without debating them, and it reduces the cognitive work required to help you. citeturn7search0turn3search3

Since your access constraints force you into “proxy debugging”, treat each request like an API call: specify inputs and expected outputs. The security principle underlying least privilege is explicitly “grant the minimum authorisations needed to perform the function”; it is normal for organisations to restrict contractor or non-core access under that logic. citeturn7search0 Your quiet-confidence behaviour is to act like this is a known system design, not a personal injustice.

When you’re being ignored, you need an escalation ladder that is **firm but non-emotional**. The knowledge sharing research suggests out-group sharing is weaker and trust matters; escalation that reads as irritation can make the trust part worse. citeturn4view0 Use a timed ladder, not repeated “sorry to bother you” pings:

First follow-up (same day): “Bumping—this blocks customer deploy. I can jump on a 5‑min call or you can just point me to the right owner.”

Second follow-up (next working day): “I’m going to escalate to <PM/AE> so we can unblock. If you’re the owner, a single ‘yes/no + ETA’ is enough.”

That second line matters because it signals you’re managing risk, not pleading for attention. It also fits the forward‑deployed ethic of keeping the customer-facing clock in mind. citeturn1search0turn1search2turn10view0

For customer-facing standups, the system should be similar but with “translation” built in: customers don’t care about internal access rules; they care about outcomes and timelines. Sierra’s own Agent Strategist role emphasises communicating complex technical information clearly to non-technical stakeholders and driving projects forward with clarity. citeturn10view0 So your standup posture becomes:

- What we shipped / verified
- What’s next and by when
- What is blocked (phrased as a dependency, not a complaint)
- What the customer can do (if anything) to help unblock

Avoid “we’re blocked because I’m a contractor” framing; it forces the customer to process your employment context. Instead use: “We’re waiting on an internal trace pull; I’ve already narrowed it to two hypotheses; next update at 16:00.” That is outcome-centred and confidence-coded.

## Quiet confidence in your specific pressure points
Quiet confidence is not a personality trait; it’s a set of observable behaviours that signal: (a) you’re in control of your work, (b) you respect other people’s time, (c) you are not emotionally outsourcing stress to others.

In your environment, “quiet confidence” has three concrete pillars.

First, **precision without theatre**. Forward‑deployed roles are increasingly recognised as demanding and not always considered glamorous, even though they’re high impact; that mismatch creates a temptation to over-explain to “prove” you’re valuable. citeturn1news45turn1search0 Quiet confidence is doing the opposite: state the recommendation first, then supply details on request.

Second, **status similarity signals without pretending you’re an employee**. Contract-work research highlights that contract workers compare their status to standard employees in the client organisation, and perceived similarity (“valued comparable to standard workers”) matters for attitudes and stability. citeturn16view0 You can’t force people to treat you like an insider, but you can make it easy for them to *experience you* as one: predictable delivery, crisp writing, ownership language (“I’ll take point on X”), and calm escalation.

A simple “contractor disclosure” script that avoids sheepishness is:
“I’m working with Sierra through <consultancy>, embedded on this deployment. My scope is <X>; for <Y> permissions I’ll route via <Sierra owner>. My goal is to reduce your load and keep delivery moving.”

This does not apologise, does not hide anything, and it puts the emphasis on outcome and collaboration.

Third, **constraint framing that never sounds like whining**. Your fear is valid: in an intensity culture, contractors who sound like they’re “complaining about access” can be dismissed as high-maintenance. Sierra’s stated “Intensity” value explicitly encourages fixing what isn’t right and learning without blame; it does not invite complaint, it invites action. citeturn10view0 So you should treat constraints like engineering realities:

Bad: “I can’t do this because I don’t have access and it’s a mess.”  
Good: “Given current access boundaries, the fastest path is: you pull X, I validate Y, we patch Z today.”

This is also psychologically protective for you: job insecurity (your “firings out of the blue” observation) is associated in large-scale meta-analytic evidence with a wide range of negative outcomes; jobs where feedback is scarce and uncertainty is high can intensify those effects. citeturn13search1 Quiet confidence is partly a *self-regulation strategy* to keep your stress from leaking into your comms.

## How to “cruise upward” when you’re 10/90 consulting and can’t rely on feedback
In your specific context, “cruising upward” is less about formal promotion and more about: **renewal safety, scope trust, and being the person people want on the deployment**. That is what produces stability and gradual role expansion in consultancy arrangements.

The research on outsourced workers’ perceived insider status gives you an important lens: outsourced workers can struggle to acquire insider markers, and lower perceived insider status is linked to lower performance; the gap can be especially pronounced among high-value (“core-status”) roles hired through outsourcing. citeturn15search11turn6view0 If you translate that into a practical strategy, it means you should aim to become a *team-level insider* even if you can’t become an organisational insider. This is consistent with broader research trends that treat “insiderness” as something that can exist at the local team/project level in contingent work contexts. citeturn15search3

Your “cruise upward” playbook in this environment is:

Maintain two reputations on purpose. Boswell et al. describe the triangular relationship: your experiences at the client can spill over into attitudes towards the employer, and contract workers hold both entities in mind. citeturn16view0 In practice, you should run a lightweight dual-update system: a weekly Sierra-facing delivery summary (customer outcomes, next risks) and a weekly consultancy-facing impact summary (what you delivered, where you unblocked, what risks you prevented). This protects you when explicit feedback is absent.

Engineer visibility because remote + in-office culture creates a known bias risk. Sierra explicitly states an in-person culture; remote workers in general face “visibility” concerns under proximity bias framings. citeturn12view0turn3search1 Your answer is not self-promotion; it is **high-quality written artefacts**: decision summaries, short design notes, incident postmortem notes, and “what changed” messages after you ship. These are “visibility that scales” and don’t require people to remember what you said on calls.

Replace “interpreting grunts” with micro-feedback requests that are cheap to answer. Feedback-seeking theory recognises both monitoring and inquiry strategies, and also notes there are costs to seeking feedback in organisations. citeturn2search7turn2search11 So you are optimising for *low-cost inquiry*:
“Quick calibration: for this week, what’s one thing I should keep doing, and one thing I should change?”
It’s a two-item prompt that is hard to ignore and doesn’t demand a formal review.

Avoid over-delivery spirals by choosing the right kind of “extra”. The knowledge sharing research suggests out-group sharing is weaker; one way to increase insider-like treatment is to produce artefacts that reduce other people’s workload (runbooks, “copy-paste” troubleshooting steps, reproducible minimal cases). citeturn4view0 This is “extra-role” behaviour that is legible and directly reduces team pressure—unlike deep research that stays in your head.

## ADHD-aware tactics that fit a high-intensity forward‑deployed role
You identified a genuine operational risk: ADHD can increase the likelihood of over-investing in deep dives or producing messages that are too dense, even when the work is good. Mainstream clinical sources on adult ADHD list common issues such as distractibility, difficulty organising time, and excessive talking/interrupting—symptoms that map directly onto your “communication takes a lot of mental energy” experience. citeturn0search0turn3search3turn3search6

In your environment, the “ADHD-friendly” approach is to make your process externally structured, not internally remembered.

Externalise scope with timeboxed investigation contracts. Every deep dive begins with: “I’ll spend 60–90 minutes; I will return with (1) a recommendation, (2) risks, (3) what I need.” This prevents disproportionate investment while still leveraging your ability to go deep when needed. It also aligns with the “intensity” culture because it keeps momentum and reporting cadence. citeturn10view0

Use one-message objectives to reduce rambling. Because digital communication overload is real (email overload is explicitly framed as information/communication/cognitive overload), your default should be one ask per message, one outcome per thread. citeturn3search3turn3search13 This is not just etiquette; it’s a strategy to stay responded-to.

Protect your energy by treating “keeping comms open” as work, not as a personal failing. Research on remote work and communication technology use links communication technology patterns with role clarity, coworker support, overload, and burnout pathways. citeturn3search6 In your case, you’re doing high-stakes “social maintenance” across an employment boundary; budgeting time for that is rational. Quiet confidence includes allowing yourself to schedule that work instead of trying to “just be naturally good at it”.

If you want a single sentence that captures the refined framework for your exact scenario, it is this: **act like an embedded Sierra delivery driver whose job is to reduce uncertainty and workload for overloaded insiders—by making your constraints neutral, your asks easy, your outputs legible, and your presence calm.** That combination directly targets the two forces that most distort your environment: out-group knowledge sharing dynamics across employment categories and visibility bias in an in-office leaning culture. citeturn4view0turn3search1turn12view0turn16view0