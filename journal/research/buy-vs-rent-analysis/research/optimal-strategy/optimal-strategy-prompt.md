# Deep Research: Capital-Optimal Investment Strategy for a 30-Year Retirement Horizon with a Major Liquidity Event at Year 7–12

---

## What this is

A first-principles investigation into the mathematically optimal investment strategy for capital maximization over a
7–12 year horizon, ending in a partial liquidation event. This is not a review of an existing plan — it is a clean-slate
search for what the evidence says is the best approach given the hard constraints below.

## Hard constraints (non-negotiable)

- **Tax jurisdiction:** Spain. CGT on savings at 19/21/23/27/30% progressive brackets. FIFO cost basis. Fondos de
  inversión with traspaso (tax-free transfers between qualifying funds, preserving cost basis). ETFs do not qualify for
  traspaso.
- **Initial lump sum:** €7,000–€10,000
- **Monthly contribution:** €1,500
- **Investment horizon:** 30+ years to retirement. NOT a 7–12 year strategy.
- **Major liquidity event at year 7–12:** withdrawal of €60,000–€80,000 (net of tax) to fund a property down payment and
  acquisition costs. The timing is flexible (not a fixed date). Post-withdrawal, the €1,500/mo capacity is redirected to
  mortgage repayment for approximately 8–10 years (no new portfolio contributions during this period). After mortgage
  payoff, €1,500/mo resumes as portfolio contributions for the remaining ~10–15 years to retirement. The retained
  portfolio receives no contributions during the mortgage phase but continues compounding on its existing base. Note:
  there is an open question of whether the ~€500–650/mo difference between the mortgage minimum payment and €1,500/mo is
  better directed to mortgage overpayment or portfolio contributions — this should be evaluated as part of the strategy.
- **The optimization target is total wealth at retirement (age ~69)**, not portfolio value at year 7–12. The strategy
  must be optimal across the full lifecycle, not just the accumulation phase. However, the year 7–12 liquidity event
  creates a constraint that a pure retirement-only strategy would not have.
- **FIFO applies per-ISIN**
- **No leverage during accumulation** (no margin, no lombard credit)
- **Platform:** Trade Republic (Spanish IBAN, fondos de inversión with traspaso support). Fund selection is constrained
  to what is available on TR's fondo catalogue. **Critical data quality warning:** TR's Spanish fondos offering launched
  in June 2025 and has evolved rapidly. Any information about TR's fund catalogue, features, or capabilities that is not
  from a verifiable 2026 source should be treated as likely inaccurate. The older the data, the higher the probability
  it is wrong. If current fund availability cannot be verified, state that explicitly rather than assuming

## What I want

The most capital-efficient strategy to maximize total wealth at retirement (~age 69), given a partial liquidation event
at year 7–12. The strategy must work across the full 30+ year horizon, not just optimize for the intermediate
withdrawal.

**Challenge everything.** Do not assume global equity index funds are the answer. If a different asset class,
combination of asset classes, or non-equity-dominant strategy produces higher expected terminal wealth under these
constraints, recommend that instead. If 80/20 equity/cash is suboptimal, say so. If 100% equity is suboptimal, say so.
If equity itself is suboptimal for part or all of the horizon, say so. The only thing that matters is the number at
age 69.

## Research focus

### 1. Asset allocation: what maximizes retirement wealth given a mid-horizon withdrawal?

The true horizon is 30+ years, but with a 25–40% partial withdrawal at year 7–12. This is neither a standard 10-year
problem nor a standard 30-year problem. Cederburg et al. ("Beyond the Status Quo") argue 100% equity outperforms
lifecycle strategies even through retirement. Does this hold when there's a large intermediate liquidity event?

Investigate: optimal equity allocation for the FULL lifecycle (not just the first 7–12 years). Should allocation shift
before the withdrawal, then shift back after? Or is a single static allocation optimal across the whole horizon? Account
for the flexible withdrawal date (if markets crash at year 7, you wait). Does factor tilting (value, small-cap,
momentum, quality) improve expected returns over 30 years with a mid-horizon withdrawal?

### 2. Geographic allocation: how much US, how much international?

MSCI World is ~70% US. Cederburg's research recommends 33% domestic / 67% international. Current US valuations (CAPE 38,
96th percentile) are historically elevated while ex-US is cheaper. For a EUR-denominated investor with a EUR-denominated
endpoint (property purchase):

Investigate: is the market-cap-weighted ~70% US allocation optimal, or would overweighting ex-US (Europe, emerging
markets) improve risk-adjusted returns from current starting valuations? What does the evidence say about currency
exposure for a EUR investor — should part of the portfolio be EUR-hedged? What is the historical cost of hedging and
does it pay off at 7–12yr horizons?

### 3. The defensive sleeve: cash, bonds, or nothing?

The current plan uses a 20% allocation to a EUR money market fund (AAA-rated, ~2% yield). Alternatives include: 0%
defensive (100% equity), short-term EUR government bonds, inflation-linked bonds, or a dynamic allocation that shifts
based on market conditions.

Investigate: over 30+ years with a partial withdrawal at year 7–12, does a permanent defensive sleeve improve retirement
wealth or just drag returns? Should the defensive allocation be zero during accumulation and only activated 1–2 years
before the withdrawal (using traspasos to shift tax-free)? Is 20% too much given that only 25–40% of the portfolio will
be liquidated? Does the answer change for the post-withdrawal phase (remaining 15–20 years to retirement)?

### 4. Fund selection and cost optimization in the Spanish market

The constraint of needing traspaso-eligible fondos limits the universe. Within that universe:

Investigate: what are the lowest-cost global equity fondos available to Spanish retail investors in 2026? Are there
specific fund families or share classes that offer meaningful cost advantages? Is a single global fund (MSCI World or
FTSE All-World) optimal, or does combining 2–3 regional funds (US + Europe + EM) offer lower costs or better tax
positioning (multiple ISINs for FIFO optimization)?

### 5. Contribution strategy: flat DCA vs dynamic approaches

The plan uses flat €1,500/mo DCA regardless of market conditions. Alternatives include: value averaging (invest more
when prices are low, less when high), momentum-based adjustment, or front-loading contributions.

Investigate: does any contribution strategy systematically outperform flat DCA for a €1,500/mo contributor over 7–12
years? What does the evidence say about value averaging vs DCA? Is there a benefit to front-loading (e.g., investing the
lump sum + first months more aggressively)?

### 6. Tax-aware strategies specific to the Spanish traspaso regime

The traspaso regime allows tax-free fund switching, creating unique optimization opportunities not available in most tax
jurisdictions.

Investigate: are there tax-loss harvesting equivalents within the traspaso framework? Can traspasos be used
strategically (e.g., switching between funds tracking the same index to create multiple FIFO queues)? One proposed
optimization is holding multiple funds tracking the same index to create FIFO optionality at partial liquidation —
evaluate whether this produces meaningful tax savings or is marginal given the added complexity and potential cost
differences between funds. Is there an optimal number of ISINs to hold? Any other Spain-specific tax-aware strategies
that the international literature wouldn't cover?

### 7. What does the optimal portfolio actually look like?

Synthesize the findings from questions 1–6 into a concrete, implementable portfolio. Specify: exact allocation
percentages, specific fund types (or names if identifiable), contribution strategy, and any conditional rules. Compare
the expected terminal value of this optimal portfolio against a naive 80/20 single-global-fund baseline over the 7–12
year horizon.

## What I do NOT want

- Advice calibrated to risk tolerance, behavioral factors, or personal comfort
- "It depends on your goals" hedging — the goal is stated: maximize capital
- US-centric advice that ignores Spanish tax mechanics
- Recommendations for products not available through Spanish fondos de inversión
- Qualitative arguments without quantified expected impact

## Output format

1. **Executive summary** (the optimal strategy in one paragraph, with expected outperformance vs an 80/20 single-fund
   baseline)
2. **Asset allocation evidence** (what the data says, by horizon, with citations)
3. **Geographic allocation analysis** (US vs international vs emerging, with valuation-adjusted forward estimates)
4. **Defensive sleeve verdict** (how much, what instrument, or none — with evidence)
5. **Fund selection for Spain** (specific lowest-cost options within the traspaso universe)
6. **Contribution strategy analysis** (DCA vs alternatives, quantified)
7. **Spanish tax optimization techniques** (traspaso-based strategies)
8. **The optimal portfolio** (concrete specification with expected wealth at retirement, including the mid-horizon
   withdrawal impact. Compare against the 80/20 single-fund baseline over the full 30+ year lifecycle, not just the
   first 7–12 years)
