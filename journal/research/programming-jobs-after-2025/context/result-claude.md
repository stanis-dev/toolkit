# Programming jobs are bifurcating, not disappearing

**The bottom line:** Between January 2025 and April 2026, the software engineering labor market split along a fault line
of seniority. Junior developer hiring collapsed by **20–73%** depending on the measure, while senior and staff
engineering roles held steady or grew. Job postings for software engineers remain **36–49% below pre-pandemic levels**,
salaries are rising modestly at mid-to-senior tiers but **declining at entry level**, and teams are compressing from
6–10 people to 3–4. Yet the causal story is messier than headlines suggest: the Federal Reserve found
"precisely-estimated null effects" linking firm-level AI adoption to reduced job postings, nearly half the decline in
tech postings **predated ChatGPT**, and the most rigorous randomized trial available showed experienced developers were
**19% slower** with AI tools — while believing they were 20% faster. What's emerging is not a simple story of AI eating
programming jobs but a structural reorganization where companies hire fewer people at the bottom, expect dramatically
more from people in the middle, and compete fiercely for people at the top — all while using AI as both a genuine
productivity lever and a convenient narrative for post-ZIRP belt-tightening.

---

## 1. Executive summary: three structural shifts backed by hard data

Three measurable changes define this period. First, the entry-level pipeline has constricted severely. Stanford's
Digital Economy Lab, analyzing ADP payroll records covering millions of workers, found employment for software
developers aged 22–25 declined **nearly 20%** from its late-2022 peak, while workers aged 30+ grew **6–12%** at the same
firms. A separate Harvard study tracking **62 million workers** across 285,000 companies found junior employment at
AI-adopting firms fell **9–10%** within six quarters of adoption, with senior employment virtually unchanged. Indeed's
August 2025 data showed only **2% of software development postings** carried junior titles versus **30.7% senior** — and
Ravio's compensation platform reported P1/P2 (entry-level) engineering hiring rates declined **73.4%** year-over-year.
The mechanism is primarily reduced hiring, not layoffs: companies simply stopped posting junior positions.

Second, engineering teams are physically shrinking. At a 500-person Pragmatic Engineer summit in February 2026,
engineering leaders confirmed the shift from "two-pizza teams" of 6–10 people to "one-pizza teams" of **3–4 people**.
Just Eat Takeaway.com restructured teams into one product manager plus one developer plus AI agent swarms.
Engineer-to-manager ratios are expanding from **1:5–6 to 1:8–12**, and SignalFire's decade-long analysis of the 100
largest tech companies shows a "slow, steady, and consistent trimming of management layers."

Third, the composition of what companies want from engineers is shifting. Dice reported that **53% of U.S. tech job
postings** in November 2025 required AI/ML skills, up from 29% a year earlier. More than **half of all open roles**
tracked by TrueUp are now positioned above senior level. Pragmatic Engineer's survey of nearly 1,000 engineers found
**95% weekly AI tool usage**, with **65–72% of code now AI-generated** inside IDE-based tools. The role of a software
engineer is moving from code generation toward system design, AI output validation, and architectural governance — a
shift that favors experience over fresh training.

---

## 2. Role-by-role landscape

### Junior and entry-level engineers face a structural hiring crisis

This is the most empirically robust finding in the dataset. **Every high-quality data source points the same
direction.** BLS data shows "computer programmer" employment fell **27.5% between 2023 and 2025** (though the broader
"software developer" category declined only 0.3%). CS graduate unemployment reached **6.1%** versus 3.6% overall;
computer engineering graduates faced **7.5%**. Entry-level tech hiring at the 15 biggest tech firms fell **25% from 2023
to 2024** (SignalFire). Handshake reported a **30% decline** in tech-specific internship postings since 2023. Big Tech's
share of new-grad hires dropped from roughly **15% to 7%** of total hires between 2019 and 2025. A Boston
University/Lightcast study analyzing the near-universe of online job vacancies found the ratio of senior-to-junior
software development postings sharply increased following ChatGPT's release and has not recovered — the interaction term
was "large, negative, and significant." A 2025 LeadDev survey found **54% of engineering leaders** plan to hire fewer
juniors as AI copilots enable seniors to handle more work.

**Evidence quality: HIGH** — multiple independent, large-sample, methodologically rigorous sources converge. The
Stanford/ADP payroll study alone covers millions of actual workers, not self-reports.

### Mid-level engineers are squeezed from both ends

Mark Zuckerberg explicitly stated Meta is developing AI "capable of performing as a mid-level coder." Pragmatic Engineer
reports that engineering leaders privately discuss mid-career engineers being "left behind" — new graduates adapt faster
to AI tools, while seniors bring irreplaceable architectural judgment. At one Big Tech firm investigated by Fast
Company, tasks once handled by juniors were absorbed by mid-level and senior staff under the assumption AI would
compensate, resulting in senior burnout. JPMorgan Chase reported its AI coding assistant increased engineer efficiency
by **10–20%**, shifting mid-level time toward higher-value projects. The mid-level role isn't disappearing but is being
compressed: less pure coding, more integration work, customer insight, and cross-functional collaboration.

**Evidence quality: MEDIUM** — credible practitioner reporting and some company disclosures, but less systematic
quantitative data than for junior roles.

### Senior and staff engineers are in greater demand than ever

Staff+ engineers have become the organizational glue for AI adoption. LeadDev reports they now write specifications for
AI agents rather than code, with the new SDLC described as "agentic and parallel." New job titles are emerging — "Staff
Systems Engineer, AI Enablement" and "Senior Staff Software Engineer, AI Enablement Lead" — requiring expertise in
Claude Code, AI governance, and multi-agent orchestration. Pragmatic Engineer's survey found staff+ engineers are the
**heaviest AI agent users** at 63.5%, more than regular engineers (49.7%) or directors/VPs (51.9%). Andrew Ng reports
some teams now have **twice as many product managers as engineers** because AI makes rapid prototyping so fast, further
elevating the architects who keep systems coherent.

**Evidence quality: HIGH** — practitioner reports with specific examples corroborated by actual job postings and company
disclosures.

### QA, DevOps, and specialized roles are transforming, not vanishing

The World Quality Report 2025 found **89% of organizations** piloting or deploying generative AI in quality engineering,
though only **15%** have achieved enterprise-wide deployment. QA is shifting from test execution to test strategy and AI
supervision — exemplified by job postings like Secure Privacy's QA Engineer role explicitly requiring "experience with
AI coding tools, particularly Claude Code, Cursor, and GitHub Copilot" and "comfort with non-deterministic outputs." In
DevOps, **76% of teams** integrated AI into CI/CD pipelines in 2025, and a new product category of "AI SRE agents" has
emerged from AWS, Microsoft, and startups. Yet despite AI tooling, **operational toil increased for 43%** of
organizations, per the 2025 SRE Report. Platform engineering is the net beneficiary, with Google's DORA 2025 Report
showing organizations that invest in platform teams "experience significantly better outcomes when introducing AI
tools."

Frontend development is blurring into full-stack work. A State of Frontend survey of **6,028 developers** found 75% use
AI daily. Figma asserts that "a single experienced developer using the right AI-driven framework will run a team of
agents with the same efficiency and output as a team of 4–5 engineers." Roughly **45% of engineering roles** now expect
proficiency across multiple domains.

**Evidence quality: MEDIUM-HIGH** for QA and DevOps (industry surveys, actual job postings); **MEDIUM** for
frontend/full-stack (survey data, vendor reports that may overstate impact).

---

## 3. Five mechanisms are driving changes simultaneously

The reshaping of programming work is not driven by a single force. Five distinct mechanisms interact, and separating
them matters for predicting what happens next.

**Substitution** is the most discussed but perhaps least prevalent mechanism in practice. AI directly replaces tasks
that junior engineers performed — boilerplate CRUD code, simple test writing, routine bug fixes. The Stanford/ADP data
showing age-stratified employment divergence is the strongest evidence. But the Federal Reserve's finding of
"precisely-estimated null effects" at the firm level suggests substitution is operating more through industry-wide
expectation-setting than through measured deployment at individual companies.

**Complementarity and leverage** explain more of what's observable in practice. Senior engineers with AI tools produce
dramatically more output — Amazon reported a project originally estimated at 30 developers over 18 months was completed
by **6 developers in 76 days** using its Kiro AI tool. Block reported production code shipped per engineer rose **over
40%** since September 2025. This isn't replacement; it's amplification. But amplification still reduces the number of
bodies needed for a fixed scope of work.

**Organizational redesign** is happening independent of measured productivity gains. Shopify's April 2025 memo requiring
teams to "demonstrate why they cannot get what they want done using AI" before requesting headcount became a template
across the industry. Fiverr's CEO issued a similar directive. Duolingo made AI usage part of performance reviews. These
are structural policy changes — new default assumptions about team composition — that persist even if AI productivity
gains prove modest.

**Budget pressure and post-ZIRP correction** is the elephant in the room. Pragmatic Engineer extensively documented that
Meta grew from 45,000 to 86,000 employees during the zero-interest-rate era; Alphabet surged from 119,000 to 190,000.
The correction was inevitable and explains a large fraction of the hiring decline. Indeed's data showing nearly half the
decline in tech postings predated ChatGPT's release supports this. A Resume.org survey found **59% of companies** admit
emphasizing AI's role in layoffs because "it plays better with stakeholders than citing financial constraints."

**Narrative contagion and CEO signaling** functions as a distinct mechanism. When Salesforce's Marc Benioff announced
"no new software engineers in 2025" and Shopify's Tobi Lütke posted his AI-first memo, these became coordination signals
across the industry. Engineering leaders at the Pragmatic Engineer summit confirmed that these public statements
directly influenced their own hiring plans, regardless of whether their own AI deployments delivered measurable gains.

---

## 4. Forward trajectories by role category

### 12-month outlook (through April 2027)

The junior hiring crisis will likely persist. The structural factors — AI tools enabling task consolidation upward,
corporate policy defaults against new headcount, and CEO signaling — show no signs of reversing. **Confidence: HIGH.**
Citadel Securities' finding of an 11% year-over-year rebound in software engineer postings in early 2026 offers a faint
recovery signal, but it applies to aggregate postings, not junior-specific ones. The BLS "computer programmer" category
will likely continue declining while "software developer" holds roughly steady.

Mid-level roles will stabilize but narrow in scope. The pure "implementation engineer" who translates specs into working
code faces the most pressure, while mid-level engineers who combine coding with domain expertise, customer interaction,
or system integration will retain value. Expect continued growth in "product engineer" titles that collapse frontend,
backend, and product thinking into a single role. **Confidence: MEDIUM.**

Senior/staff demand will remain strong to growing. Every company that reduces juniors needs more senior judgment to
validate AI output, maintain architectural coherence, and manage the **1.75x increase in correctness errors** and **45%
security vulnerability rate** that Veracode and CodeRabbit found in AI-generated code. Gartner's prediction that
AI-driven prompt-to-app approaches will increase software defects by **2500% by 2028** would, if even directionally
correct, massively increase demand for experienced engineers. **Confidence: HIGH.**

QA will continue consolidating into development roles. Dedicated manual QA teams will shrink further as AI test
generation matures. The surviving QA roles will be highly technical, focused on test architecture, AI output validation,
and security testing. **Confidence: MEDIUM-HIGH.**

DevOps/SRE will evolve toward platform engineering. The operational toil paradox — AI creates new complexity even as it
solves old complexity — will sustain demand for experienced infrastructure engineers, but under new titles and with
broader scope. **Confidence: MEDIUM.**

### 36-month outlook (through April 2029)

This is where uncertainty dominates. The forecasts diverge sharply:

- The World Economic Forum projects software developer jobs growing **57% through 2030**.
- The BLS projects **15% growth through 2034**.
- Gartner predicts **80% of organizations** will have smaller, AI-augmented engineering teams by 2030.
- Goldman Sachs expects **6–7% of U.S. workers** displaced over ~10 years, with computer programmers among the
  highest-risk occupations.

These cannot all be simultaneously true without significant definitional gymnastics. The most likely reconciliation:
total spending on software creation will increase (WEF/BLS are right about demand), but each unit of software will
require fewer traditional "programmer" hours (Gartner is right about team compression). The result is probably **modest
net growth in software engineering headcount** combined with **dramatic internal restructuring** — fewer juniors, more
seniors, smaller teams, broader individual scope, and significantly higher output per person. **Confidence in this
synthesis: MEDIUM.** The Jevons Paradox argument — that cheaper software creation will expand total software demand
enough to increase total employment — is historically well-supported but untested at current AI capability levels.

The wild card is AI capability trajectory. Stanford HAI reports SWE-bench scores jumped from ~60% in 2024 to nearly
**100% in 2025**, and inference costs dropped **280-fold** in two years. If agentic AI systems achieve reliable
autonomous software development on production-scale codebases within 36 months, all bets are off. But the METR study's
finding that experienced developers were slower on large, mature codebases with AI suggests a significant gap between
benchmark performance and real-world production reliability. **Confidence that benchmarks overstate near-term impact:
MEDIUM-HIGH.**

---

## 5. Separating signal from noise requires acknowledging what we don't know

The strongest signals — changes most likely to represent durable structural shifts rather than cyclical noise or
narrative hype — are:

- **The junior hiring collapse is real and multi-sourced.** Stanford payroll data, Harvard employer data, Indeed
  postings data, BLS employment data, and academic labor economics research all converge. This is not a single anecdote
  or survey; it's a robust empirical finding from independent methodologies. However, the _causal attribution_ to AI
  specifically (versus post-ZIRP correction, Section 174 tax code changes, or general macro tightening) remains
  contested. The most careful reading of the evidence suggests both AI and macro factors are operating simultaneously,
  with AI preventing a recovery that might otherwise have occurred.

- **Team compression is happening at named companies with specific numbers.** Just Eat Takeaway.com's restructuring,
  Amazon's 30-to-6 developer project, Block's 40% headcount reduction with 40%+ increase in code shipped per engineer —
  these are concrete, verifiable organizational changes, not projections.

- **CEO and policy signals have independent causal force.** Even where measured AI productivity gains are modest, the
  _expectation_ of AI capability is reshaping hiring defaults. Shopify's memo, Salesforce's hiring freeze, and
  Duolingo's AI-first policy create industry-wide coordination effects.

The noisiest signals — claims most likely to be overstated, premature, or self-serving — deserve explicit
identification:

- **"X% of code is AI-generated" metrics are poorly defined and unreliable.** When Nadella says "maybe 20%, 30%" and
  Pichai says "more than 30%," these figures conflate autocomplete suggestions, AI-assisted refactoring, and genuinely
  autonomous code generation. LessWrong analysis of Amodei's "90% of code" claim found it didn't survive conventional
  measurement. These numbers serve marketing purposes more than analytical ones.

- **Vendor-sponsored productivity studies systematically overstate gains.** GitHub's finding that Copilot users complete
  coding tasks **56% faster** (cited by McKinsey) contrasts sharply with METR's randomized controlled trial showing
  experienced developers **19% slower**, and DX's analysis of 121,000 developers finding productivity gains stuck at
  **~10%** despite 92.6% tool adoption. The independent studies are more credible. The 2024 Microsoft/MIT/Harvard field
  study of 4,867 developers found **26% more tasks completed** — but gains concentrated among junior/newer developers,
  with senior developers showing "little or no measurable speed-up."

- **"AI washing" of layoffs is documented and widespread.** Challenger, Gray & Christmas tracked 1.2 million layoffs in
  2025; Forrester estimates fewer than 100,000 were primarily attributable to AI. The AEI and multiple analysts have
  noted that AI provides a more palatable narrative for investors than "we overhired during ZIRP." The NBER found **nine
  in ten executives** reporting no impact of AI on employment or productivity over the past three years.

- **Klarna is a cautionary tale, not a template.** The company's 40% headcount reduction was accompanied by a public
  reversal when quality suffered, growing financial losses ($99M in Q1 2025, double the prior year), and an IPO pause.
  CEO Siemiatkowski admitted "cost unfortunately seems to have been a too predominant evaluation factor" and began
  rehiring humans. Several engineers were reportedly reassigned to customer service.

The critical evidence gap is between benchmark capability and production reliability. AI scores near-perfect on
SWE-bench but generates code with **1.75x more correctness errors**, **1.64x more maintainability issues**, and **45%
security vulnerability rates** in real-world deployments. Until this gap closes — or until companies develop reliable
processes for managing AI-generated technical debt — the displacement timeline will be slower than AI capability curves
suggest.

---

## 6. Open questions that data could resolve

**Will the junior hiring recovery materialize?** The single most important data point to watch is whether the Citadel
Securities report of an 11% year-over-year rebound in software engineer postings extends to junior-specific roles.
Indeed Hiring Lab's quarterly breakdowns by seniority level, once updated through Q2 2026, will be definitive. If junior
postings remain at 2% of total while aggregate postings recover, the structural interpretation is confirmed.

**Is AI actually causing the hiring changes, or merely coinciding with them?** The Federal Reserve's
"precisely-estimated null effects" at the firm level directly conflicts with Stanford's finding of age-stratified
employment divergence. Resolving this requires firm-level panel data that tracks both AI tool adoption timing and hiring
changes for specific role levels — data that ADP, Revelio Labs, or LinkedIn Economic Graph could produce but haven't yet
published. The NBER study finding AI adoption in Denmark had "precisely zero effect on earnings or hours" needs
replication in U.S. tech sector data.

**What happens to code quality and maintenance costs at scale?** The Veracode, CodeRabbit, and DORA data on AI-generated
code quality are alarming but based on relatively small or early-stage samples. If the Gartner prediction of **2500%
defect increases by 2028** proves even directionally correct, companies will need to hire engineers to fix what AI
built. Longitudinal tracking of bug rates, security incidents, and technical debt at companies with high AI code
adoption would resolve this. The Arxiv study finding 484,606 AI-introduced issues across 3,841 repositories is a
promising start.

**Will Jevons Paradox hold?** If cheaper software development genuinely expands total software demand, we should see it
in increased startup formation rates, higher software project initiation at enterprises, and expansion of software into
previously non-software domains. GitHub new repository creation rates, venture funding for software startups, and
enterprise IT spending data would test this. Early YC data — companies reaching $10M revenue with fewer than 10 people —
suggests Jevons dynamics may operate at the _company formation_ level while still reducing employment per company.

**How will the talent pipeline crisis resolve?** If companies skip a generation of junior hiring, they face a
five-to-ten year gap before today's would-be juniors become tomorrow's needed seniors. No data yet exists on whether AI
can substitute for the experiential learning that junior roles historically provided, or whether alternative
apprenticeship models will emerge. AWS CEO Matt Garman's warning — calling the idea of replacing entry-level developers
with AI "one of the dumbest things I've ever heard" because "ten years in the future you have no one that has learned
anything" — captures the long-term risk. But acknowledging the problem and solving it are different things.

**What is the real productivity number?** The gap between vendor claims (~56% faster), independent measurement (~10%
gain or 19% slower for experienced developers), and executive claims (30% productivity gain at Salesforce, 4–5x at
Duolingo) is too large to ignore. A definitive, large-sample, longitudinal study tracking the same teams before and
after AI tool adoption — controlling for selection effects, task complexity, and downstream quality costs — would
resolve years of debate. The DX dataset of 121,000 developers across 450+ companies is closest to this standard, and its
finding of **~10% productivity gains despite 92.6% adoption** deserves more attention than it has received.

---

## Conclusion: the reorganization is real, the revolution is premature

The programming labor market is undergoing genuine structural change, not merely cyclical adjustment. The convergence of
independent, high-quality data sources on junior hiring decline, team compression, and role redefinition is too
consistent to dismiss. But the change is better described as **reorganization** than replacement. Companies are not
eliminating engineering functions; they are compressing them into fewer, more senior, broader-scoped roles while raising
the floor of expected AI tool fluency.

The most underappreciated dynamic is the emerging tension between **speed of code production** and **reliability of code
in production**. AI tools demonstrably accelerate initial code generation. They also demonstrably introduce more
defects, security vulnerabilities, and architectural problems. This tension will likely sustain demand for experienced
engineers — precisely the people who can evaluate, debug, and architect around AI-generated code — even as it reduces
demand for engineers whose primary value was generating that code in the first place.

For the next 12 months, expect continued junior hiring weakness, growing expectations of AI tool fluency as a baseline
skill, further team compression at companies that have already adopted AI workflows, and a widening gap between
companies that have genuinely reorganized around AI and those using AI narratives to justify unrelated cost-cutting. The
36-month picture is genuinely uncertain — AI capability curves are steep, but the gap between benchmark performance and
production reliability is wide, and historically, productivity tools have expanded rather than contracted the developer
workforce. The honest answer is that we are in the early innings of a structural transition whose endpoint no one can
yet see clearly, and anyone claiming certainty about the destination is selling something.
