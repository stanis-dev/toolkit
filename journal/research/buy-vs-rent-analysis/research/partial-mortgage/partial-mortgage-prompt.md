# Deep Research: Optimal Partial-Mortgage Strategy at Property Purchase — Balancing CGT, Interest Cost, and Continued Compounding

---

## Who this is for

- Spanish tax resident (Comunitat Valenciana) planning to buy a coastal flat outright using a portfolio accumulated over 10–15 years in fondos de inversión
- The portfolio will contain significant embedded capital gains at the point of purchase, subject to Spain's progressive CGT brackets (19–30%)
- The investor holds funds in a traspaso-eligible vehicle, meaning unrealized portions can be rebalanced or de-risked tax-free
- The purchase will happen at age ~48–55 depending on market conditions, with continued investment capacity post-purchase

## Context and constraints

**Tax (certain):**
- Spain — CGT on savings income (rendimientos del ahorro) at 19/21/23/27/30% progressive brackets (Ley 7/2024). FIFO cost basis applies
- Fondos de inversión with traspaso (tax-free transfers between qualifying funds). Tax is triggered only at redemption
- Fund redemptions withheld at 19% by the intermediary; actual progressive liability may be higher, creating a top-up at the next Renta declaration
- ITP on resale property in Comunitat Valenciana: 9% (from June 2026, Ley 5/2025)

**Portfolio structure (certain):**
- Single equity fund: Fidelity MSCI World Index Fund P-Acc-EUR (IE00BYX5NX33, 0.12% TER, accumulating)
- Cash sleeve: Fidelity Institutional Liquidity EUR A Acc (IE0003323494, 0.10% TER, money market)
- Allocation: 80% equity / 20% money market
- Built via monthly DCA over 10–15 years, meaning under FIFO the earliest (most appreciated) units are sold first — the gain ratio on the oldest lots will be very high

**Purchase parameters (near-certain):**
- Property price range: €150,000–€250,000 (target municipalities are Moncofa, Xilxes, Nules — cheaper than premium coastal towns)
- Total acquisition costs: ~10% of purchase price (9% ITP + ~1% notary/registry/gestoría)
- Purchase age: ~48–55, meaning maximum mortgage term is ~15–20 years (Spanish bank age limits of ~75)
- IVF guarantee programme (Comunitat Valenciana) allows up to 100% LTV for first-home buyers under 45, property ≤€311,000 — available as fallback only if purchase happens before age 45

**Post-purchase (near-certain):**
- Monthly DCA capacity of ~€1,500 continues after purchase (same as accumulation phase, since no rent to pay)
- This capacity is available to service any mortgage taken and/or rebuild the investment portfolio for retirement
- Retirement accumulation horizon: ~15–20 more years after purchase

## Starting point

This is the first research session on this topic. There is no prior research to build on. Start from first principles.

**What I already know (informal):**
- Full portfolio liquidation at purchase triggers a single large taxable event that pushes gains into the 27–30% brackets
- A partial mortgage would allow liquidating only part of the portfolio, keeping the rest compounding tax-deferred
- The retained portfolio can be de-risked via traspaso (tax-free) without triggering gains
- Mortgage interest is a direct cost that works against this advantage
- There should be a crossover point where the CGT saved equals the mortgage interest paid — but I don't know where that is or how sensitive it is to assumptions
- Phased redemptions over multiple tax years could also reduce CGT without a mortgage, but this requires timing the purchase differently

## Instructions

1. **Do not assume a specific portfolio size, return rate, or mortgage rate.** Instead, solve the problem parametrically — show how the optimal LTV changes as these variables move. Use ranges, not point estimates.
2. **Be specific to Spanish tax law.** The progressive CGT brackets, FIFO rules, withholding mechanics, and traspaso regime are essential to the analysis. Generic tax advice is not useful.
3. **Consider all viable alternatives**, not just "full liquidation" vs "partial mortgage." Include: phased liquidation over multiple tax years before purchase, partial liquidation + partial mortgage, retaining the entire portfolio and taking a full mortgage, or hybrid approaches.
4. **Search the web for current data.** Cite sources. Include current Spanish mortgage rates for relevant LTV ranges, and verify the CGT bracket structure.
5. **Quantify everything.** The output should include worked examples across a range of portfolio sizes (€180K–€350K), embedded gain ratios (40–70% of portfolio), mortgage rates (2.5–5%), mortgage terms (10–20yr), and LTV levels (0–60%).
6. **Structure output for decision-making.** The result should produce a clear decision rule: "given your portfolio size, gain ratio, and available mortgage rate, the optimal LTV is approximately X%."

## Research focus

The core question: **When buying a property using accumulated investment funds, what is the optimal split between portfolio liquidation and mortgage financing to minimize total cost (CGT + mortgage interest) while maximizing retained wealth, under Spanish tax law?**

### 1. The CGT cost curve: how does the tax bill change with partial vs full liquidation?

Model the Spanish progressive CGT brackets applied to different redemption amounts under FIFO. For a portfolio with €150K in embedded gains, what is the total tax at full liquidation vs liquidating 75%, 50%, 25%? How does the marginal rate change as you reduce the redemption? At what point do you drop below the 27% bracket entirely?

### 2. The mortgage cost curve: what does partial financing actually cost?

For a €150K–€250K property, model the total interest cost of a 10–20yr fixed mortgage at various LTV levels (20%, 30%, 40%, 50%) and rate assumptions (2.5%, 3.5%, 4.5%). Include upfront costs that come with a mortgage (appraisal, notary, AJD if applicable, life/home insurance if required for rate bonification). Note that €1,500/mo post-purchase capacity is available for accelerated repayment. At what LTV and rate does the mortgage interest exceed the CGT saved?

### 3. The retained-portfolio compounding benefit

If you keep €50K–€150K invested instead of liquidating it (in a single-fund DCA portfolio where the oldest lots have the highest embedded gains under FIFO), what is the expected additional wealth over 10–20 years at various return assumptions? How does the traspaso advantage (tax-free rebalancing of the retained portion into the money market fund for de-risking) affect this? What is the breakeven return rate — below which keeping money invested while paying mortgage interest destroys value?

### 4. Phased liquidation as an alternative to mortgage

Instead of a mortgage, could you liquidate the portfolio over 2–4 tax years before purchase (parking proceeds in a money market fund via traspaso, then redeeming in tranches)? How much CGT does this save compared to single-year liquidation? What are the practical constraints (you need the full amount on notary day)?

### 5. The interaction of all three: total cost optimization

Combine CGT, mortgage interest, and retained compounding into a single total-cost model. For a given property price, portfolio size, embedded gain ratio, mortgage rate, and expected return: what LTV minimizes total cost? How sensitive is the optimum to each variable? Is there a robust "rule of thumb" that holds across plausible parameter ranges?

### 6. Spanish-specific mechanics that affect the analysis

Does mortgage interest provide any tax deduction in Spain (it did historically for pre-2013 purchases — does any deduction survive for new purchases)? How does the IVF guarantee programme interact with this strategy (can you get a low-LTV mortgage through IVF even after accumulating a large portfolio)? Are there specific Spanish mortgage products designed for asset-rich borrowers (e.g., pledge/lombardkredit against the portfolio)?

## What I do NOT want

- Generic "pay off your mortgage vs invest" advice that ignores Spanish tax specifics
- Analysis that assumes a single set of parameters — I need the sensitivity across ranges
- Assumptions about my specific portfolio size or return rate — keep it parametric
- Oversimplified comparisons that ignore FIFO, progressive brackets, or traspaso mechanics
- Recommendations without quantification

## Output format

1. **Executive summary** (the core insight: when does a partial mortgage win, and by how much?)
2. **CGT analysis** (tax bill by redemption level, marginal rate breakpoints, FIFO impact)
3. **Mortgage cost analysis** (interest cost by LTV and rate, including upfront fees)
4. **Retained compounding analysis** (breakeven return, expected benefit ranges)
5. **Phased liquidation analysis** (multi-year redemption as an alternative, practical constraints)
6. **Total cost optimization** (combined model, sensitivity tables or charts, optimal LTV by scenario)
7. **Decision rule** (a simple heuristic: "if your embedded gain ratio is above X% and mortgage rates are below Y%, take a Z% LTV mortgage")
8. **Spanish-specific considerations** (deductions, IVF interaction, portfolio-backed lending)
