## 1. Executive summary

Here is the map first: since January 1, 2025, the clearest structural change in programming jobs has not been a clean
collapse of software work. It has been **compression and rebundling**. Openings for software-development roles in major
advanced economies remained weak into early 2026, but the remaining openings tilted toward more senior, broader-scope,
and more explicitly AI-fluent work. As of March 27, 2026, Indeed’s software-development postings index, benchmarked to
February 1, 2020 = 100, stood at 72.44 in the U.S., 79.43 in Canada, 62.94 in the U.K., 56.05 in Germany, and 56.37 in
France. ([FRED][1])

That weakness in openings is **not the same thing as an immediate collapse in existing programmer employment**. In the
U.S., employment in “computer systems design and related services” was still 2.368 million in March 2026, and Indeed’s
own tech analyses in both the U.S. and Canada explicitly note that hiring freezes have so far hit job seekers harder
than incumbent employment. The right read is: fewer openings, slower churn, harder entry, and more selective hiring—not
“software jobs vanished.” ([FRED][2])

The strongest role-level pattern is **seniority polarization**. Indeed found U.S. senior/manager tech postings down 19%
from early-2020 levels versus standard/junior postings down 34%; in August 2025, software development postings were
30.7% senior-title but only 2% junior-title. In Canada, senior/higher-level tech postings were still up 5% from early
2020 while standard/junior titles were down 25%, and senior-level software engineer postings were roughly unchanged
while lower-level software engineer postings plunged. ([Indeed Hiring Lab][3])

AI is showing up inside mainstream programming jobs less as a separate new job family than as a **new baseline skill and
workflow expectation**. By December 2025, software-development postings in the U.S. mentioned AI 20% or more of the
time, while total tech postings were still 34% below pre-pandemic levels; in the U.K., AI-mentioning postings were 127%
above pre-pandemic levels by February 2026 even as overall postings were 27% below baseline. That is a real labor-market
signal: employers are hiring less overall, but when they do hire, they increasingly want programmers who can work
effectively with AI tools. ([Indeed Hiring Lab][4])

The day-to-day job is also shifting. The best direct evidence says code generation is getting cheaper, but requirements,
system design, debugging, testing, review, and validation are becoming more important bottlenecks. Marc Brooker at AWS
describes the bottleneck moving toward requirements, design, testing, and validation; Anthropic’s internal study found
engineers primarily using Claude for debugging and code understanding, with low-context and easily verifiable tasks the
most delegable; lower-weight hiring surveys point in the same direction, with system design, debugging, and real-world
simulations gaining importance while “writing new code” loses relative weight. ([se-radio.net][5])

The highest-confidence forward view after April 14, 2026 is this: **mainstream programming jobs are not disappearing,
but the market is becoming structurally tougher for junior and generic application-development roles, and structurally
better for senior/staff engineers, broad full-stack/backend owners, and platform/reliability/infrastructure roles that
constrain or operationalize AI-generated output.** Compensation data are thinner than postings data, but they point to
cooling and stabilization rather than broad wage collapse: European software-engineer pay mostly rose only 1%–2% in
2025, UK senior software engineer pay was nearly flat, and Dice’s 2025 U.S. survey showed entry-level tech pay down
while mid-career workers gained. ([Ravio][6])

Highest weight in this synthesis goes to public labor-market data and company disclosures: FRED/Indeed posting indices,
BLS employment data, and concrete company statements from Amazon, Shopify, Anthropic, and confirmed hiring-policy
changes at Meta. I use recruiter/vendor surveys such as CoderPad, Karat, Dice, and Ravio only where direct role-level
data is missing, and I treat them as directional rather than dispositive.

## 2. Role-by-role landscape

Included here: junior/early-career engineers, mainstream app-development roles, senior/staff ICs, tech leads/EMs,
QA/SDET, and DevOps/SRE/platform/infrastructure. I am excluding AI-specialist roles as a standalone category except
where they pull demand or reshape mainstream programming work.

### Junior / early-career engineers

**Observed since January 1, 2025:** This is the most obviously constrained layer of the market. Indeed says the
environment for entry-level and early-career tech job seekers became more challenging; software development had just 2%
junior-title postings in August 2025; and remaining tech postings skewed toward more experience, with the share asking
for at least five years rising from 37% to 42% between Q2 2022 and Q2 2025. Entry-level openness did not fully
disappear—18% of tech postings that listed experience were still open to one year or less—but that was inside a much
smaller market. Pay evidence is directionally similar: Dice’s 2025 U.S. survey found entry-level tech compensation down
1.4%. ([Indeed Hiring Lab][3])

**Most plausible interpretation:** The best reading is not “AI killed junior jobs overnight.” Indeed explicitly argues
the squeeze on new entrants mirrors a broader market decline, not a unique junior collapse. But AI likely makes the
situation worse by eating some of the low-context starter tasks that used to justify apprenticeship hiring. Anthropic’s
internal evidence fits that mechanism: the easiest tasks to delegate are low-context and easy to verify—the exact kind
of work many juniors historically cut their teeth on. ([Indeed Hiring Lab][7])

**Expected trajectory after April 14, 2026:** Over the next 12 months, junior hiring likely stays selective and
increasingly concentrated in formal pipelines, high-trust teams, and organizations willing to train. Over 36 months, I
expect a bifurcated market: fewer ad hoc junior reqs, but continued hiring where firms want long-term talent pipelines
or where AI-native juniors can contribute quickly. Confidence is high on the 12-month squeeze and medium on the 36-month
bifurcation. The leading indicators to watch are the junior-title share of software postings, the share of postings open
to <=1 year of experience, and entry-level compensation. ([Indeed Hiring Lab][3])

**Evidence quality:** High on openings and seniority mix; medium on causal attribution to AI; low-to-medium on
compensation.

### Mid-level back-end / full-stack engineers

**Observed since January 1, 2025:** Direct public data for back-end and full-stack, specifically, are thinner than for
“software engineer” overall. What the strongest evidence does show is that generic software-engineer demand remained
weak, while lower-weight 2026 hiring surveys still ranked full-stack and back-end as the most sought-after mainstream
engineering roles among active hiring plans. At the same time, assessment formats are shifting toward system design,
multi-file debugging, working in existing codebases, and real-world scenarios instead of toy problems. ([Indeed Hiring
Lab][8])

**Most plausible interpretation:** In a weak market, employers appear to prefer engineers who can own broader slices of
delivery—specification, implementation, debugging, integration, and production follow-through—rather than narrowly
bounded coders. This does not look like explosive demand growth for back-end/full-stack so much as **share gain inside a
shrunken market**. Brooker’s description of the bottleneck moving away from raw code generation toward requirements and
validation points the same way. ([CoderPad][9])

**Expected trajectory after April 14, 2026:** In the next 12 months, this is the healthiest mainstream
application-development pocket. In the next 36 months, the role stays durable if paired with domain context, system
ownership, and strong judgment about AI-generated output. The downside case is that generic “full-stack” becomes too
commoditized unless tied to real product or systems responsibility. Confidence is medium because the role-level postings
evidence is weaker than for junior/senior splits. ([CoderPad][9])

**Evidence quality:** Medium.

### Front-end, mobile, and specialized application roles

**Observed since January 1, 2025:** This is where the clearest role-level compression shows up. Indeed’s U.S. analysis
found software engineer postings down 49% versus early 2020, and several specialized developer titles—Android, Java,
.NET, iOS, and web developers—down more than 60%. Indeed’s cross-country analysis also found that the same categories
weak in the U.S. were not especially strong in emerging markets, which argues against a simple “this all just moved
offshore” explanation. ([Indeed Hiring Lab][8])

**Most plausible interpretation:** Routine application-layer work is getting squeezed from several directions at once:
post-boom correction, mature frameworks, more platform standardization, some cross-platform substitution, and AI making
scaffolding and incremental maintenance cheaper. This looks more structural than purely cyclical because the weakness
clusters in the same families of narrower developer roles across regions. ([Indeed Hiring Lab][8])

**Expected trajectory after April 14, 2026:** Over 12 months, I expect this to remain one of the weakest mainstream
programming segments outside heavily regulated or product-core niches. Over 36 months, the durable subset will be
engineers with performance, accessibility, design-system, graphics, device-native, or domain-specific constraints that
generic AI-assisted development does not handle cleanly. Confidence is medium-high on near-term weakness and medium on
the long-run shape. ([Indeed Hiring Lab][8])

**Evidence quality:** High on current weakness; medium on forward structure.

### Senior / staff / principal individual contributors

**Observed since January 1, 2025:** Senior layers are holding up much better. Indeed found U.S. senior/manager titles
much closer to pre-pandemic levels than standard/junior titles; Canada found senior/higher-level tech postings still up
5% from early 2020 while standard/junior tech titles were down 25%, with senior software-engineer postings roughly
unchanged. Public-company anecdotes are unusually concrete here: Amazon described six highly skilled engineers, working
with its agentic coding service, shipping a Bedrock engine rebuild in 76 days that normally might have taken a 40-person
team about a year. ([Indeed Hiring Lab][3])

**Most plausible interpretation:** AI is complementing and amplifying strong senior engineers more than replacing them.
Someone still has to decide what to build, decompose the work, review it, test it, integrate it, and own the
consequences. Anthropic’s internal study reinforces that: employees report heavy AI use, but most fully delegable work
remains low-context and low-stakes. The premium is moving toward judgment, architecture, and ownership.
([Anthropic][10])

**Expected trajectory after April 14, 2026:** In the next 12 months, this is the strongest IC tier. In the next 36
months, I expect staff-level leverage to rise further even if total headcount layers stay lean. The base case is not
“more titles everywhere,” but “more of the value and compensation pool accrues to people who can supervise larger flows
of machine-produced code.” Confidence is high. ([Indeed Hiring Lab][3])

**Evidence quality:** High.

### Tech leads / engineering managers

**Observed since January 1, 2025:** Direct role-count data for leads and EMs are thinner than for IC seniority, but
senior/manager roles clearly held up better than junior/standard roles. At the same time, company evidence points to a
changing job, not a disappearing one: Amazon said it flattened its organization over the last year for faster
decision-making; Anthropic openly says it uses Claude for job descriptions, interview questions, candidate
communications, sourcing, interview transcription, and hiring-metrics analysis; Meta began trialing AI-assisted coding
interviews to better match real developer workflows. ([Indeed Hiring Lab][3])

**Most plausible interpretation:** The role is shifting from coordination and process management toward **workflow
design, hiring-bar setting, AI governance, and technical judgment about leverage**. Coordination-only layers look more
fragile; technical leadership layers look more valuable. Amazon’s explicit flattening language is important here because
it points to fewer layers but not less need for decision-making. ([Amazon News][11])

**Expected trajectory after April 14, 2026:** Over 12 months, technical leads and strong EMs look stable to slightly
better than the market, while “manager as status layer” looks pressured. Over 36 months, I expect leaner org charts,
larger spans, and more emphasis on leaders who can redesign hiring, toolchains, and team structure around AI-assisted
delivery. Confidence is medium. ([Indeed Hiring Lab][3])

**Evidence quality:** Medium.

### QA / SDET / test engineering

**Observed since January 1, 2025:** This is one of the thinnest public-data categories. I did not find good 2025–2026
labor-market panels isolating QA/SDET demand across major regions. The strongest direct evidence instead comes from
workflow change: Anthropic’s engineers most commonly use Claude for debugging and code understanding; Brooker says
faster code generation makes testing and validation more central bottlenecks; and lower-weight hiring survey data show
real-world scenarios, code review, and debugging exercises gaining ground in assessments. ([Anthropic][10])

**Most plausible interpretation:** The manual, repetitive edge of QA is under pressure, but the quality function itself
is not becoming less important. It is being redefined upward: toward test automation, release validation, regression
detection, observability, safety/security checking, and evaluation of AI-generated changes. This looks like role
redesign, not simple elimination. ([Anthropic][10])

**Expected trajectory after April 14, 2026:** Over 12 months, pure manual QA roles are the most vulnerable part of the
quality stack, while automation-heavy SDET and quality-engineering work should be steadier. Over 36 months, I expect
fewer standalone manual-testing seats and more embedded quality ownership plus specialized evaluation/reliability roles.
Confidence is medium-low because the direct demand data are weak. ([se-radio.net][5])

**Evidence quality:** Low-to-medium.

### DevOps / SRE / platform / infrastructure

**Observed since January 1, 2025:** Public role-specific demand data are again thinner than for software engineers, but
the available signals are notably better than for generic application development. Indeed Canada found elevated demand
for roles supporting AI infrastructure, including data and platform engineers and data-center technicians. Amazon is
simultaneously investing at huge scale in AI infrastructure and explicitly using small, high-skill teams plus AI tooling
to rebuild core systems faster. Lower-weight hiring surveys still show meaningful demand for DevOps, cloud, and systems
engineers. ([Indeed Hiring Lab][12])

**Most plausible interpretation:** As application code becomes cheaper to generate, the value of platform abstractions,
CI/CD, reliability, observability, security, and cost control rises. This is one of the clearest complementarity
stories: AI-assisted development tends to increase the need for good guardrails and operating systems around code, not
reduce it. ([Indeed Hiring Lab][12])

**Expected trajectory after April 14, 2026:** Over 12 months, this category looks resilient. Over 36 months, it is one
of the best bets among non-AI-specialist software roles, especially where platform teams can standardize and constrain
AI-heavy engineering workflows. Confidence is medium-high. ([Indeed Hiring Lab][12])

**Evidence quality:** Medium-high.

### Compensation across roles

The compensation picture is less dramatic than the openings picture. The cleanest signal is **cooling, not collapse**.
At the start of 2025, U.S. software-development posted wages were growing only 0.7% year over year. In Ravio’s European
benchmarks, 2025 software-engineer salaries rose modestly—1.6% in the U.K., 1.9% in Germany, 1.2% in France, 1.0% in
Spain—and U.K. senior software-engineer pay was nearly flat at +0.3%. Dice’s 2025 U.S. survey points in the same
direction on seniority mix: entry-level compensation fell, mid-career (3–5 years) rose nearly 6%, and the overall market
stayed sticky rather than crashing. ([Indeed Hiring Lab][13])

## 3. Key mechanisms

**1. A post-boom correction is still the base layer.** The strongest labor-market sources do **not** support a
simplistic “AI caused the whole crash” story. Indeed explicitly says there is no smoking gun linking the tech-postings
plunge to AI, and that a large share of the decline happened before consumer LLM adoption. Canada shows the same
pattern. AI is changing the rebound, but it did not single-handedly create the downturn. ([Indeed Hiring Lab][8])

**2. AI is mostly acting as leverage, not broad autonomous replacement.** Anthropic’s internal study is unusually
concrete: engineers reported using Claude in 60% of their work with a 50% self-reported productivity gain, but
low-context and easily verifiable tasks were the most delegable. It also found that 27% of Claude-assisted work was work
that otherwise would not have been done. That is a complementarity signal: AI expands throughput and task volume before
it cleanly substitutes whole jobs. Shopify’s official account of universal AI-code-editor adoption supports the same
“baseline tool” reading. ([Anthropic][10])

**3. The bottleneck is moving from coding to specification, review, and validation.** Brooker’s description is the best
direct statement of the mechanism: when code generation accelerates, requirements, design, testing, and validation
become the constraints. CoderPad’s lower-weight 2026 survey points the same direction: respondents ranked debugging and
fine-tuning, system design, and collaboration as more important over time, while “writing new code” ranked lower.
([se-radio.net][5])

**4. The hiring bar is moving upward even when total hiring stays weak.** Indeed’s seniority data and
experience-requirement shift are the clearest proof. This is why the market feels harsher than a generic downturn:
employers are not just hiring less; they are asking for broader scope, more experience, and more immediate productivity.
That is why juniors and generic mid-level app roles feel squeezed even when overall employment has not fallen
proportionately. ([Indeed Hiring Lab][3])

**5. Organization design is changing alongside jobs.** Amazon said it flattened its organization for speed and gave a
concrete example of a very small, very skilled team using AI tooling to compress delivery time dramatically. Shopify
made reflexive AI use a baseline expectation and reported universal AI code-editor adoption. These are not labor-market
aggregates, but they are the strongest kind of anecdote: concrete statements tied to real workflow and org-design
changes inside large software organizations. ([Amazon News][11])

**6. Hiring criteria are changing for non-AI programming jobs.** Anthropic now explicitly wants candidates who can
collaborate well with AI, while still restricting live-interview AI use unless allowed. Meta is piloting AI-assisted
interviews because it sees them as more representative of real developer work and more robust to hidden AI use by
candidates. Lower-weight survey data say 44% of hiring leaders’ top 2026 goals include “AI-friendly processes,” but also
show that classic algorithms still remain in 43% of tests and degree requirements remain sticky in many job postings.
The implication is not “credentials disappeared.” It is “proof of leverage, judgment, and tool use is gaining, but old
filters still persist.” ([Anthropic][14])

**7. Geography matters, and the mix is shifting.** Indeed found tech postings in emerging markets still 47% above
pre-pandemic levels as of October 2025, and their share of tracked global tech postings rose from 16% in early 2020 to
28% by September 2025. But the same source also says outsourcing appears to be a subtle contributor rather than the main
driver, because the job titles weakest in the U.S. were also relatively weak in emerging markets. So there is some
redistribution, but the bigger story is common technological and macro pressure, not a pure offshore swap. ([Indeed
Hiring Lab][15])

## 4. Forward trajectories

The most defensible scenario frame is:

- **Base case:** slow recovery in openings, continued seniority polarization, broader role definitions, and AI-tool
  fluency becoming table stakes inside mainstream programming work. This is the highest-confidence path because it
  matches current postings, hiring-bar shifts, and company workflow evidence. ([FRED][16])
- **Upside case:** cheaper software creation expands the number of viable projects enough to reopen hiring below the
  senior tier. This would look like stronger postings recovery, rising junior share, and faster pay growth in generalist
  roles. Current evidence does not rule it out, but does not favor it yet. ([FRED][2])
- **Downside case:** firms use AI mostly as headcount discipline and keep output flat with smaller teams, pushing
  further compression into generic app-dev, junior layers, manual QA, and non-technical management. The evidence does
  not yet prove this, but it is a real risk signaled by weak openings, flat pay, and org flattening. ([FRED][16])

Role by role:

**Junior / early-career:** 12 months: still the toughest part of the market. 36 months: smaller but not dead; more
concentrated in structured pipelines and high-learning environments. Confidence: high on 12 months, medium on 36.
Leading indicators: junior-title share in software postings, <=1 year experience share, entry-level compensation, and
whether firms reopen apprenticeship-style reqs. ([Indeed Hiring Lab][3])

**Mid-level back-end / full-stack:** 12 months: best mainstream application-development pocket, but still a selective
market. 36 months: durable if coupled with ownership, systems thinking, and domain context; vulnerable if “full-stack”
means generic ticket execution only. Confidence: medium. Leading indicators: role mix in active hiring plans,
system-design/debugging emphasis in interviews, and whether broad “software engineer” postings recover materially.
([CoderPad][9])

**Front-end / mobile / specialized app roles:** 12 months: still weak. 36 months: niche but durable where complexity is
real—performance, graphics, accessibility, device constraints, high-end UX systems, regulated environments. Confidence:
medium-high on near-term weakness. Leading indicators: web/iOS/Android/.NET/Java posting trends, cross-platform tooling
adoption, and whether those titles recover faster than generic software-engineer demand. ([Indeed Hiring Lab][8])

**Senior / staff / principal ICs:** 12 months: strongest mainstream category. 36 months: further leverage premium, more
value per engineer, likely higher compensation share even in flatter orgs. Confidence: high. Leading indicators:
senior-title share, staff/principal hiring at large firms, public examples of small elite teams shipping outsized
output, and persistence of higher experience requirements. ([Indeed Hiring Lab][3])

**Tech leads / EMs:** 12 months: stable for technical managers, weaker for coordination-only roles. 36 months: fewer
layers, wider spans, more emphasis on workflow design, hiring judgment, and technical credibility. Confidence: medium.
Leading indicators: manager-title mix, public flattening disclosures, and whether companies continue redesigning
interviews and recruiting around AI-assisted work. ([Amazon News][11])

**QA / SDET / test engineering:** 12 months: redesign, not clean disappearance. 36 months: fewer pure manual-test roles,
more automation, evaluation, release-quality, and reliability ownership. Confidence: medium-low. Leading indicators:
prevalence of debugging/code-review/test-eval exercises in hiring, public SDET/quality-engineering req mix, and any
direct role-level postings data that becomes available. ([se-radio.net][5])

**DevOps / SRE / platform / infrastructure:** 12 months: resilient. 36 months: likely one of the healthiest
non-AI-specialist categories because AI-heavy development needs better guardrails and operating systems. Confidence:
medium-high. Leading indicators: platform/data/cloud/system job demand, infrastructure capex, and whether public
companies keep emphasizing AI-enabled delivery on top of heavier platform investment. ([Indeed Hiring Lab][12])

## 5. Signal vs noise

**Well-supported claims:** Advanced-economy software-development openings remained depressed through early 2026; the
market favored senior/context-heavy roles over junior/generic ones; AI mentions rose inside mainstream programming
postings even while total hiring stayed weak; and the work itself shifted toward design, debugging, review, testing, and
validation. ([FRED][16])

**Weakly supported claims:** AI is already causing a broad net reduction in programmer employment; mainstream
software-engineer compensation is collapsing; contractor demand is replacing full-time demand at scale; or middle
management is collapsing everywhere. The public evidence base for those claims is thin, mixed, or too broad. Openings
are clearly down, but employment and pay are more stable than the loudest narratives imply. ([FRED][2])

**Likely hype:** “Most programmers will be replaced very soon,” “junior hiring is dead,” “coding skill no longer
matters,” and “AI has already made traditional hiring obsolete.” The real data show continuing technical interviews,
continuing system-design emphasis, continuing degree screens in many cases, and growing demand for engineers who can
verify and own AI-assisted work rather than merely prompt it. ([CoderPad][9])

**What would falsify the current narrative:** If software-development posting indices recover strongly across major
markets, the junior share rises materially, experience requirements relax, and generalist software wages re-accelerate,
then the “structural compression” reading is too strong and the last two years were more cyclical than structural. If,
instead, AI-mention rates keep rising but platform/reliability/quality roles do not strengthen and firms stop changing
hiring loops, then the “workflow redesign” thesis is overstated. Those are the cleanest falsifiers because they directly
test the indicators now showing the clearest signal. ([FRED][16])

## 6. Open questions

The biggest unanswered questions are not philosophical; they are data problems.

First, I did not find robust 2025–2026 public panels splitting **contractor versus full-time demand** for programming
roles. That matters because some “AI replacement” stories may actually be “less permanent hiring, more flexible
staffing.”

Second, role-level public data are still too weak for **QA/SDET, SRE, platform, front-end, and mobile** compared with
the much better evidence we now have for “software engineer” and seniority splits.

Third, we need matched company-level evidence linking **AI tool adoption to actual engineering headcount changes by
level**. Right now, the best company evidence is concrete but anecdotal: Amazon, Shopify, Anthropic, and Meta show
workflow and hiring-process change, but not enough public functional headcount data to quantify substitution cleanly.
([Amazon News][11])

Fourth, compensation needs better coverage. The best available signals show stabilization and seniority spread, but we
still lack comprehensive 2026 pay panels by role and level across regions. Ravio and Dice are useful, not definitive.
([Ravio][6])

Fifth, the geography question is still open. Emerging markets clearly gained share, but Indeed’s own analysis says
offshoring is only a subtle part of the story. To resolve that, we would need company-by-company hiring footprints, not
just national posting aggregates. ([Indeed Hiring Lab][15])

My bottom line is simple: the strongest evidence does **not** say “programming is over.” It says the market has become
harder, more senior, more selective, more AI-mediated, and more focused on people who can turn cheap code generation
into reliable shipped systems. The labor-market damage since January 1, 2025 is real, but it is concentrated—above all
in junior and generic application-development layers—while senior, platform, and judgment-heavy work is strengthening
its relative position. ([FRED][16])

[1]:
    https://fred.stlouisfed.org/series/IHLIDXUSTPSOFTDEVE?utm_source=chatgpt.com
    "Software Development Job Postings on Indeed in the United States (IHLIDXUSTPSOFTDEVE) | FRED | St. Louis Fed"
[2]: https://fred.stlouisfed.org/series/CES6054150001 "https://fred.stlouisfed.org/series/CES6054150001"
[3]:
    https://www.hiringlab.org/2025/07/30/experience-requirements-have-tightened-amid-the-tech-hiring-freeze/
    "Experience Requirements Have Tightened Amid the Tech Hiring Freeze - Indeed Hiring Lab"
[4]:
    https://www.hiringlab.org/2026/01/22/january-labor-market-update-jobs-mentioning-ai-are-growing-amid-broader-hiring-weakness/
    "January 2026 US Labor Market Update: Jobs Mentioning AI Are Growing Amid Broader Hiring Weakness - Indeed Hiring Lab"
[5]:
    https://se-radio.net/2026/03/se-radio-710-marc-brooker-on-spec-driven-ai-dev/
    "SE Radio 710: Marc Brooker on Spec-Driven AI Dev – Software Engineering Radio"
[6]: https://ravio.com/blog/software-engineer-salary-trends "https://ravio.com/blog/software-engineer-salary-trends"
[7]:
    https://www.hiringlab.org/2025/09/25/september-labor-market-squeeze-on-new-entrants/
    "September 2025 Labor Market Update: The Squeeze on New Entrants Mirrors a Marketwide Decline - Indeed Hiring Lab"
[8]:
    https://www.hiringlab.org/2025/07/30/the-us-tech-hiring-freeze-continues/
    "The US Tech Hiring Freeze Continues - Indeed Hiring Lab"
[9]:
    https://coderpad.io/survey-reports/coderpad-state-of-tech-hiring-2026/
    "CoderPad State of Tech Hiring 2026 - CoderPad"
[10]:
    https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic
    "How AI Is Transforming Work at Anthropic \\ Anthropic"
[11]:
    https://www.aboutamazon.com/news/company-news/amazon-ceo-andy-jassy-2025-letter-to-shareholders
    "CEO Andy Jassy’s 2025 Letter to Shareholders"
[12]:
    https://www.hiringlab.org/en-ca/2025/08/26/canadian-tech-hiring-freeze-continues/
    "Canadian Tech Hiring Freeze Continues - Indeed Hiring Lab Canada"
[13]:
    https://www.hiringlab.org/2025/02/06/software-development-postings-remain-in-the-doldrums/
    "US Q4 2024 Business-to-Business Labor Market Update: Software Development Postings Remain in the Doldrums  - Indeed Hiring Lab"
[14]: https://www.anthropic.com/candidate-ai-guidance "Guidance on Candidates' AI Usage \\ Anthropic"
[15]:
    https://www.hiringlab.org/2025/10/15/emerging-economies-avoided-global-tech-hiring-freeze/
    "Emerging Economies Have Avoided (Most) of the Global Tech Hiring Freeze - Indeed Hiring Lab"
[16]: https://fred.stlouisfed.org/series/IHLIDXUSTPSOFTDEVE "https://fred.stlouisfed.org/series/IHLIDXUSTPSOFTDEVE"
