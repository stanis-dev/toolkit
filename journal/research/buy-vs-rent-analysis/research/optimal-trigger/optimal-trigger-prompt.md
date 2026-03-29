# Deep Research: Optimal Purchase Trigger — When to Stop Accumulating and Buy

---

## Who this is for

- Spanish tax resident (Comunitat Valenciana) executing an "invest now, buy later" strategy
- Accumulating capital via monthly DCA into a global equity index fund (fondo de inversión)
- Will use a partial mortgage at purchase (40-50% LTV) rather than full portfolio liquidation, based on prior research showing this saves €25-100K in total wealth over 15 years through CGT avoidance and retained compounding

## Context and constraints

**The established strategy:**
- Monthly DCA: €1,500 into Fidelity MSCI World P-Acc-EUR (IE00BYX5NX33, 0.12% TER)
- 80/20 allocation: equity + Fidelity Institutional Liquidity EUR money market fund
- Starting position: €7,000 lump sum + €1,500/mo from age 36
- At purchase: partial liquidation + mortgage, then aggressive repayment at €1,500/mo. Prior research found 40-50% LTV optimal for a fully-accumulated portfolio, but this finding assumed high embedded gains from a mature DCA portfolio. For an earlier purchase with a smaller, younger portfolio, the optimal LTV may differ — this research should co-optimize the trigger AND the LTV simultaneously

**Property parameters:**
- Target municipalities: Moncofa, Xilxes, Nules (Castellón coast, Comunitat Valenciana)
- Current price range: €150,000-€200,000 for the target flat type
- Property appreciation scenarios: 1% pessimistic / 2.5% baseline / 4% optimistic
- Acquisition costs: ~10% of purchase price (9% ITP from June 2026 + ~1% fees)

**Costs of waiting (accumulation phase):**
- Rent: €500/mo currently locked with IPC increases for 5 years, then market reset to ~€650-750 at year 9 (LAU 5+3yr protection)
- Property appreciation: the target gets more expensive each year
- CGT grows: a larger portfolio at purchase means more embedded gains under FIFO, pushing more into higher brackets

**Benefits of waiting:**
- Portfolio grows: more compounding time means a larger base at purchase
- Smaller LTV needed: less mortgage interest paid
- More retained capital after partial liquidation: bigger retirement compounding base

**Tax mechanics (certain):**
- CGT: 19/21/23/27/30% progressive brackets (Ley 7/2024). FIFO applies per-ISIN
- At purchase: partial liquidation triggers CGT on sold portion only. Retained portion continues tax-deferred via traspaso
- Mortgage interest is NOT tax-deductible (post-2013 purchases)
- ITP: 9% in Comunitat Valenciana from June 2026

**Partial mortgage research findings (already established):**
- Optimal LTV at purchase: 40-50%
- Breakeven portfolio return: ~1-3% (well below any equity return assumption)
- With €1,500/mo accelerated repayment, a €80-100K mortgage is cleared in 5-7 years
- Total mortgage interest cost at 3.5%: ~€7-11K on an aggressively-repaid €80-100K loan

**Post-purchase:**
- €1,500/mo capacity continues: first directed to mortgage payoff (5-7yr), then to retirement portfolio
- Retirement accumulation horizon varies with purchase age: buy at 45 = 24yr to age 69, buy at 52 = 17yr

## Starting point

This is the first research session on this specific question. The prior research established that a partial mortgage at purchase is optimal, but assumed the portfolio had already reached full purchase coverage. This research asks: **does that assumption hold, or should the purchase be triggered earlier?**

**The intuition to test:**
Waiting until the portfolio covers 100% of purchase + costs may be suboptimal because:
- Every year of waiting costs rent (~€6K-9K/yr) and adds property appreciation (~€3.5-8K/yr on a €175K target)
- A larger mortgage (50-60% LTV instead of 40-50%) costs more interest but may be offset by lower property price, less rent paid, and more post-purchase compounding time
- The partial mortgage research showed CGT savings are proportionally large even at higher LTVs

## Instructions

1. **Model this as a total-wealth optimization across the full lifecycle** — from age 36 (start of DCA) through age 69 (retirement). The variable being optimized is total net worth at retirement, including: property equity + investment portfolio (after-tax) - all costs incurred.
2. **The key variable is the purchase trigger**: at what portfolio value (as a percentage of the total purchase cost including acquisition fees) should the investor stop accumulating and buy? Test triggers from 50% to 120% of total purchase cost.
3. **Do not assume a specific set of parameters is correct.** Solve parametrically across the ranges provided and show how the optimal trigger changes as assumptions shift.
4. **Account for all interacting costs:** rent during accumulation (with the step-function profile), property appreciation, CGT at partial liquidation under FIFO, mortgage interest with accelerated repayment, post-purchase retirement compounding, and the opportunity cost of capital directed to mortgage repayment vs investment.
5. **Be specific to Spanish tax law.** CGT brackets, FIFO, traspaso, and mortgage mechanics must be correctly modeled.
6. **Quantify the sensitivity.** How much does the optimal trigger shift with different property growth rates, portfolio returns, and rent trajectories?

## Research focus

The core question: **Given that a partial mortgage at purchase is the established endgame strategy, what is the optimal portfolio accumulation threshold to trigger the purchase — and how does buying earlier (with a larger mortgage, but a cheaper property and less rent) compare to buying later (with a smaller mortgage, but a more expensive property and more rent paid)?**

### 1. The total cost of waiting

For each year of continued accumulation beyond the earliest feasible purchase point, quantify the combined cost: rent paid + property appreciation + additional CGT from a larger portfolio. Compare this to the benefit: additional portfolio growth + lower LTV at purchase. At what point does the cost of waiting exceed the benefit?

### 2. The optimal purchase trigger by scenario (co-optimized with LTV)

Model total retirement wealth (age 69) for purchase triggers ranging from 50% to 120% of total purchase cost. **At each trigger point, also solve for the optimal LTV** — do not assume 40-50% holds at all trigger levels. A younger portfolio has lower embedded gains (shallower FIFO gradient), which reduces the CGT saving per euro of mortgage, potentially shifting the optimal LTV.

Test across:
- Portfolio return: 4%, 5%, 6%
- Property appreciation: 1%, 2.5%, 4%
- Rent trajectory: €500 for 8yr then €700 vs €500 for 8yr then €900
- Starting property price: €150K, €175K, €200K
- Mortgage rate: 2.5%, 3.5%, 4.5%

For each combination, identify both the trigger AND the LTV that maximize retirement wealth. Show how optimal LTV changes with the trigger — does it stay at 40-50% or shift toward 60-70% for early purchases?

### 3. The mortgage size trade-off at different portfolio maturities

Buying earlier means a larger mortgage (higher LTV) but also a younger portfolio with lower embedded gains. Model the interaction between:
- Higher mortgage interest cost (larger loan, longer to repay even at €1,500/mo)
- Lower property price at purchase (less appreciation)
- Less rent paid (fewer years renting)
- **Less CGT saving per euro of mortgage** (younger portfolio, shallower FIFO gradient, gains may not reach the 23%+ brackets yet)
- More post-purchase retirement compounding years
- But: less retained portfolio at purchase (lower starting base for retirement)

The key question: **at what portfolio age/size does the CGT saving from a mortgage become too small to justify the interest cost?** Is there a minimum portfolio maturity (e.g., 5 years of DCA) below which buying with a mortgage is worse than continuing to accumulate? Is there a clear LTV cliff, or is the relationship smooth?

### 4. The rent step-function impact

The rent profile is not smooth — it's stable at ~€500 for years 1-8 (LAU protection) then jumps to ~€650-750 at year 9. Does this create a natural purchase window? Is buying just before the rent reset (year 7-8) significantly better than buying after it (year 10-12)?

### 5. The IVF age-45 deadline interaction

The IVF guarantee programme allows up to 100% LTV for first-home buyers under 45. If the optimal trigger suggests buying at age 42-44 with a 50-60% LTV mortgage, does the IVF guarantee meaningfully improve the terms? Does the age-45 cutoff create a discontinuity in the optimization — is there a scenario where buying at 44 with IVF is significantly better than buying at 46 without it?

### 6. Sensitivity to the "never buy" boundary

At what combination of parameters does the early-purchase strategy become risky — where a large mortgage + small portfolio + market crash could create financial distress? What is the minimum portfolio coverage (as % of purchase cost) below which the strategy becomes fragile?

## What I do NOT want

- Analysis that assumes full cash purchase is the baseline — the partial mortgage is already established as superior
- Generic lifecycle investing advice unrelated to the specific purchase-trigger question
- Assumptions about my specific return rate or property growth — keep it parametric across the stated ranges
- Qualitative hand-waving — every claim should be backed by modeled numbers
- Ignoring the rent step-function or treating rent as smoothly increasing

## Output format

1. **Executive summary** (the core finding: should you buy earlier than "100% coverage"? By how much? What's the wealth impact?)
2. **Cost-of-waiting analysis** (annual cost breakdown: rent + appreciation + CGT growth vs portfolio growth benefit)
3. **Optimal trigger table** (purchase trigger × scenario matrix showing retirement wealth)
4. **Mortgage size sensitivity** (LTV vs total cost curve, identifying any cliffs)
5. **Rent step-function analysis** (does the year-8 reset create a natural purchase window?)
6. **IVF deadline analysis** (does the age-45 cutoff matter for the optimal trigger?)
7. **Fragility analysis** (minimum safe portfolio coverage, downside scenarios)
8. **Decision rule** (a simple heuristic: "buy when your portfolio reaches X% of purchase cost, with Y% LTV mortgage, provided mortgage rates are below Z%" — with X and Y co-varying by scenario)
