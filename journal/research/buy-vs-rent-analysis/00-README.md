# Buy vs Rent & Invest Analysis — Documentation Index

## What this is

A structured financial analysis evaluating whether to **buy a coastal flat in Castellón
province (Spain)** or **rent and invest the difference** in a global equity index fund,
over a 30-year horizon. The analysis was conducted in March 2026.

The buyer profile: 36-year-old Spanish tax resident, first home purchase, habitual residence,
targeting a €200,000–€250,000 flat on the Castellón coast, eligible for the IVF (Institut
Valencià de Finances) 5% down-payment guarantee programme.

## How this analysis was built

### Phase 1: Plan the research (human-driven)

The main analysis document (`01-main-analysis.md`) was created as a skeleton outlining every
scenario and calculation to be performed. The structure was designed iteratively through
conversation, with each section's research needs explicitly defined before any data was gathered.

### Phase 2: Deep research (ChatGPT Deep Research, 5 separate sessions)

Five focused research prompts were crafted and run through ChatGPT Deep Research, each
targeting a specific part of the analysis. The prompts were designed to be narrow and specific
to avoid vague or unfocused results. Each research output was reviewed for soundness before
integration.

One additional early research session (06-initial-exploration.md) was conducted from an
unfocused prompt and was explicitly NOT used for conclusions — only for identifying structural
blind spots in the research plan.

### Phase 3: Integration and computation (AI-assisted, human-reviewed)

Each research output was reviewed for quality and consistency, then integrated into the main
document section-by-section. All numerical computations (amortisation schedules, DCA
projections, forced-sale scenarios, break-even analysis, sensitivity runs) were performed
programmatically in Python and verified against research inputs.

### Phase 4: Sensitivity testing

The Part 4 conclusions were stress-tested against 10 sensitivity scenarios (3 computed,
7 qualitatively assessed) to check robustness.

### Phase 5: First peer review + real-scenario rewrite

The complete analysis (Parts 1–5) was submitted to a GPT-5 Pro peer review session. The
review confirmed the arithmetic but identified 6 material gaps (after-tax portfolios, owner
cost inflation, rent-to-buy equivalence, crash scenarios, equity stress test, retirement
cashflow). These were addressed in Part 6 (sections 6.1–6.8).

The buyer then identified that the comparison used a theoretical "instant purchase with lump
sum" model that didn't match their actual financial position. This led to a full rewrite of
Parts 3–4 using a **real-scenario framework**: actual starting savings (€15K), saving period
before purchase, safety buffer, post-purchase buffer rebuild, and three-phase buy path. All
Part 6 sections were recomputed with the real-scenario numbers.

### Phase 6: Real-scenario computation

All outstanding computations were run programmatically in Python:
- Buy-path timelines for 4 scenarios (2 flat prices × 2 monthly capacities)
- Investor portfolios at matching endpoints (after Spanish CGT)
- 3×3 comparison matrices (property growth × investment return)
- Break-even analysis
- Retirement drawdown survival analysis (20-year post-mortgage)
- Final updated comparison (section 6.9)

---

## File inventory and provenance

### Main analysis

| File | Description |
|------|-------------|
| `01-main-analysis.md` | The complete analysis document (~1,660 lines). Contains all parameters, research findings, computations (including real-scenario framework), comparisons, extended analysis (Part 6), and conclusions. This is the primary artifact. |

### Research sources (in `research/sources/`)

| File | Original name | Source | Used for | What was extracted |
|------|--------------|--------|----------|-------------------|
| `01-property-prices.md` | "price report.md" | ChatGPT Deep Research | **Part 1** — Property price projections | Historical €/m² data (1995–2025), CAGRs for Castellón/Spain/CV, coastal municipality asking prices, demand drivers, scenario rates (1%/2.5%/4%), 30yr projections, risk factors (crash history, VUT, climate, supply) |
| `02-buying-costs.md` | "buying home costs.md" | ChatGPT Deep Research | **Part 2** — Mortgage & payment scheme | IVF guarantee mechanism + eligibility, upfront costs (ITP, notary, registry, gestoría, appraisal), fixed mortgage rates (95% LTV range), monthly payment calculations, age/insurance considerations, selling costs for 2D |
| `03-index-funds.md` | "idx funds research.md" | ChatGPT Deep Research | **Part 3** — Investment returns & tax | Historical returns (FTSE All-World, MSCI World EUR, S&P 500), return scenarios (4%/6%/8%), fee analysis (VWCE 0.19%), ETF vs fondo traspaso advantage, Spanish CGT brackets, wealth tax, FIFO, exit planning, inflation context |
| `04-ongoing-costs.md` | "coastal flat ownershi.md" | ChatGPT Deep Research | **Part 2B.2** — Ongoing ownership costs | Municipality-specific IBI rates, community fee ranges, derrama estimates, waste tax, consolidated annual cost (Low €1,300/Mid €2,770/High €5,050). Also: IVF collaborating bank list (14 entities) |
| `05-rent-market.md` | "rent market.md" | ChatGPT Deep Research | **Part 3 rent** + **Part 5** | Current Castellón coast rental prices (€/m²), €500 starting rent validation, HICP 30yr rent inflation (~2.5%/yr), LAU tenant protections (Art. 14/18, contract stability 5–8yr), IRAV mechanism, stressed-area status, rent scenarios (1.5%/3%/6%), seasonal contract risk |
| `06-initial-exploration.md` | "first research.md" | ChatGPT Deep Research (early, unfocused prompt) | **Blind-spot analysis only** | NOT used for any data or conclusions. Reviewed for structural patterns that informed 5 additions to the research plan: equal-outflow methodology, upfront cash as lump sum, break-even framing, IRAV mechanism, income stress test. |

### Additional research (in `research/` subdirectories)

| Directory | Contents | Date |
|-----------|----------|------|
| `investment-strategy/` | Investment strategy prompt, result, and step-by-step action plan | Mar 2026 |
| `partial-mortgage/` | Partial mortgage optimization — prompt + 3 tool results (Claude, Gemini, GPT DR) | Mar 2026 |
| `optimal-trigger/` | Purchase trigger optimization — prompt + 4 tool results (Claude, Gemini, GPT DR, GPT Pro) | Mar 2026 |
| `optimal-strategy/` | Capital-optimal investment strategy challenge — prompt + results (pending) | Mar 2026 |

### Meta-review (in `meta/`)

| File | Description |
|------|-------------|
| `eval-prompt.md` | Cross-tool evaluation prompt |
| `evaluation.md` | Full evaluation of all 5 meta-review results with cross-tool synthesis and action items |
| `result-*.md` | Individual tool results (GPT DR, Gemini, Claude, GPT-5.4 HT, GPT-5.4 Pro Extended) |

### What was NOT used and why

- `06-initial-exploration.md` conclusions were not trusted because the prompt was vague and
  the parameters didn't match our analysis (used €240K at 3%, not our €250K/€200K at 4.0–4.5%).
  Only the structural patterns were used to identify blind spots.
- `"flat purchase in castellon.md"` was identified as a duplicate of `02-buying-costs.md` and
  was excluded from this folder.

---

## Key assumptions

| Parameter | Value | Source / Rationale |
|-----------|-------|-------------------|
| Flat prices | €250,000 and €200,000 | User-defined |
| Down payment | 5% via IVF guarantee | IVF programme rules (02-buying-costs.md) |
| Mortgage rate | 4.0% TIN (baseline), 4.5% TIN (prudent) | 95% LTV range from bank product pages (02-buying-costs.md) |
| Mortgage term | 30 years fixed | User-defined, age 36 → purchase at ~37–39 → mortgage ends at ~68–69 |
| Property appreciation | 1% / 2.5% / 4% nominal | Castellón historical CAGRs (01-property-prices.md) |
| Investment return | 4% / 6% / 8% nominal EUR | MSCI World EUR since 2000: 6.32% (03-index-funds.md) |
| Starting rent | €500/month | Validated at ~50–60m² for Castellón coast (05-rent-market.md) |
| Rent inflation | 1.5% / 3.0% / 6.0% per year | HICP 30yr ~2.5% + market reset premium (05-rent-market.md) |
| Insurance | ~€60/month mid-case | Bank representative examples (02-buying-costs.md) |
| Ongoing costs | ~€231/month mid-case | IBI + community + derramas + waste (04-ongoing-costs.md) |
| Total buyer outflow | €1,425/mo (€250K) / €1,198/mo (€200K) | Mortgage + insurance + ongoing |

---

## Conclusion summary

> **Updated March 2026** with real-scenario computations (actual starting position, saving
> period, buffer rebuild, after-tax portfolios, inflated ownership costs). Supersedes the
> earlier theoretical model in `01-main-analysis.md`.

**At €500/mo rent ("same person" framing):** renting and investing wins in **8 out of 9
scenario combinations** (after-tax) at the end of the total timeline (~31–33 years), across
all four configurations (2 flat prices × 2 monthly capacities). Buying wins only when
property growth is optimistic (4%) AND investment returns are pessimistic (4%).

**At €700–800/mo rent ("same flat" framing):** buying becomes competitive or favourable,
winning 3–6 out of 9 scenarios depending on the flat price. The actual rent level is the
single most decision-critical variable.

The break-even analysis shows that at a 6% investment return, buying needs ~4.6–4.7%/yr
property growth to match rent+invest — above Castellón's 10yr CAGR of 2.5% and above
Spain's 30yr average (~4.0%).

The retirement analysis (6.6) confirms the renter's portfolio **survives 20 years of rent
drawdown** in every tested scenario (4%/6%/8% accumulation × 2%/4% drawdown returns).

The biggest risk of buying remains forced early exit (Part 2D): a sale in the first 10 years
results in a net loss of €48K–€139K. At 95% LTV, only ~7% price decline creates negative
equity. Castellón's last crash was -42%.

A third strategy — **buy later without mortgage** (6.8) — offers zero interest cost, zero
forced-sale risk, and full liquidity until purchase. At baseline 6% return with €1.5K/mo DCA,
a €200K flat can be bought outright at age ~45 (€250K at age ~47).

---

## Known limitations and caveats

1. **All projections are mechanical.** Constant growth rates, constant returns, no sequence-of-
   returns risk, no market crashes modelled mid-period (except the stagnation and crash
   sensitivities in Parts 5 and 6.4–6.5).
2. **After-tax portfolios are computed** in the real-scenario model (Spanish CGT 19–30%
   applied at full liquidation). Spreading sales over 3–5 tax years would reduce effective
   rates further — this benefits the renter.
3. **Rental income from the flat** (if not used as primary residence) is not modelled. The IVF
   guarantee requires habitual residence, so this is consistent — but it means no "buy and
   rent out" optionality is captured.
4. **Currency risk** is not modelled. If the buyer earns in a non-EUR currency, FX fluctuations
   affect mortgage affordability.
5. **Emotional and lifestyle value** of owning a home is acknowledged but not quantified.
6. **Research data is from early 2026.** Rates, prices, and regulations will change.
7. **The €250K/€1K scenario is barely viable.** Housing costs exceed the budget by mortgage
   year 12–13, eroding the buffer. This configuration is unsuitable for a €1K/mo capacity.
