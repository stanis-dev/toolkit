# Invest Now, Buy Later: Financial Plan

---

## 1. Decision and Strategy Overview

Three strategies were evaluated for building long-term wealth and eventually owning a coastal
flat in Castellón province (Spain):

1. **Buy now with mortgage** — purchase immediately using a 95% LTV mortgage via the IVF
   guarantee programme
2. **Rent forever and invest** — stay in a modest rental, invest the difference in a global
   index fund for 30+ years
3. **Invest now, buy later without mortgage** — invest from day 1, then buy outright once
   the portfolio reaches the flat price. No mortgage, no interest, no forced-sale risk.

After extensive analysis (documented in
[alternatives/full-comparison-analysis.md](alternatives/full-comparison-analysis.md)), the
third strategy was chosen. The comparison found:

- Buying now with a mortgage wins in only 1 out of 9 scenario combinations at the €500/mo
  rent baseline. It requires property to appreciate at 4%+ while investments return only 4%
  — Castellón outperforming its historical average while global equities underperform theirs.
- The buy-now path at €250K / €1K monthly capacity is barely viable — housing costs exceed
  the budget by mortgage year 12, eroding the safety buffer.
- The invest-now-buy-later strategy combines the compounding advantage of early investing
  with eventual mortgage-free ownership and zero forced-sale risk.

For the full mortgage analysis, see
[alternatives/buy-now-with-mortgage.md](alternatives/buy-now-with-mortgage.md).

---

## 2. Starting Position and Parameters

- **Age:** 36
- **Location:** Spain, Comunitat Valenciana, Castellón coast
- **Current savings:** €15,000
- **Emergency buffer (kept in bank):** €8,000
- **Initial lump sum to invest at month 0:** €7,000 (€15K − €8K buffer)
- **Monthly DCA capacity:** €1,000 or €1,500 (after rent and living costs)
- **Current rent:** €500/mo (validated: ~50–60m² at Castellón coast rates)
- **Rent inflation:** 3.0% baseline (blended: modest in-contract indexation + periodic
  market resets). Range: 1.5% (low) to 6.0% (high).
- **Target flat:** coastal Castellón, €200,000–€250,000
- **Purchase method:** outright cash (no mortgage) once portfolio reaches target
- **Investment vehicle:** fondo de inversión (Spanish mutual fund) — preferred over ETF for
  traspaso tax deferral advantage
- **Return scenarios (nominal EUR):** 4% pessimistic / 6% baseline / 8% optimistic
  - Anchored to MSCI World (EUR, net) since 2000: 6.32% annualised
  - All figures nominal. To approximate real returns, subtract ~2–2.5% for inflation.
- **Property appreciation scenarios:** 1% pessimistic / 2.5% baseline / 4% optimistic
  - Anchored to Castellón's 10yr CAGR of 2.5%

---

## 3. Investment Plan

### Vehicle choice: fondos de inversión + traspaso

The most important Spain-specific implementation decision. Fondos de inversión allow
tax-free transfers between eligible funds (_traspasos_), meaning you can rebalance, switch
providers, or de-risk into bonds without triggering capital gains tax. Tax is paid only at
final redemption (or when selling to buy the flat).

ETFs have lower fees (VWCE at 0.19% TER vs fondos at 0.10–0.59%) but every sale is a
taxable event. Over a 10–15 year accumulation phase with likely rebalancing and eventual
de-risking, **fondos are structurally better** for a Spanish tax resident.

**Platforms evaluated:**

| Feature | Trade Republic | MyInvestor | Indexa (roboadvisor) |
| ------- | :---: | :---: | :---: |
| Fondos de inversión | Yes (since June 2025) | Yes (mature) | Yes (managed) |
| Traspasos (internal) | Free | Free | Free |
| Traspasos (external) | Supported but operationally immature | Mature, well-tested | Supported |
| Auto DCA (savings plan) | Free | Free | Automatic |
| Manual purchases | €1/operation | Free | N/A (managed) |
| Global equity index fondo | Fidelity MSCI World, 0.12% TER | iShares Developed World, 0.10% TER | Diversified mix |
| All-in cost | ~0.12% (fund TER only) | ~0.10% (fund TER only) | ~0.53% (management + funds) |
| Cash interest | ~2% on all cash, tracks ECB (no limit) | ~2% (varies) | N/A |
| Auto tax retention/reporting | Yes (new) | Yes | Yes |
| Customer service quality | Poor (AI chatbot, slow) | Adequate | Good |

**Recommendation: Trade Republic as primary, MyInvestor as backup.** Trade Republic is
already in use, offers competitive fondos with traspaso support, free automatic DCA, and
~2% cash interest (tracks ECB) on the emergency buffer. The Fidelity MSCI World Index Fund
(IE00BYX5NX33, 0.12% TER, accumulating) is the core equity fund. The Vanguard Global Bond
Index Fund EUR Hedged Acc (IE00B18GC888, 0.15% TER, accumulating) is the bond fund.

However, Trade Republic's fondos offering has been live only since June 2025 and users
report occasional issues with external traspasos. Having a MyInvestor account ready means
you can transfer funds out via traspaso if TR's service doesn't meet expectations — without
any tax consequence.

### Allocation: two-phase lifecycle

**Phase 1 — Accumulation to purchase (years 0 to ~12–15):**

- **80–90% global equities (accumulating fondo)**
- **10–20% EUR-hedged global bonds (accumulating fondo)**

Higher equity allocation during this phase because: (a) the horizon is long enough to
recover from drawdowns, (b) the purchase date is flexible (if markets crash, you wait),
and (c) every extra percentage of return shortens the time to purchase.

**Phase 2 — Post-purchase retirement accumulation (from purchase to ~age 67–69):**

- Shift toward **70–80% equities / 20–30% bonds** via traspasos (tax-free)
- Continue shifting to **~60% equities** by the last 5–10 years before retirement
- Hold 1–3 years of planned withdrawals in very low-risk assets as retirement approaches

All allocation shifts executed via **traspasos** — no taxable events until final withdrawal.

### Historical return evidence

| Index / benchmark | Period | Annualised return | Notes |
| ----------------- | ------ | ----------------: | ----- |
| MSCI World (EUR, net) | 10yr | 12.34% | Recent decade, strong |
| MSCI World (EUR, net) | Since 2000 | 6.32% | Spans dot-com, GFC, Euro crisis, COVID |
| MSCI World (EUR, net) | Max drawdown | −53.60% | May 2001 to March 2009 |
| S&P 500 (USD, total) | 30yr | ~9.6% | Long-history comparator |
| S&P 500 (USD, total) | Worst rolling 20yr | ~2.8% | 1928–1947 |

Return scenarios for modelling:

| Scenario    | Annual return | Rationale |
| ----------- | ------------- | --------- |
| Pessimistic | **4%**        | Below MSCI World EUR since 2000. Accounts for weak decades, valuation headwinds. |
| Baseline    | **6%**        | Consistent with MSCI World EUR since 2000. Leaves room for fees. |
| Optimistic  | **8%**        | Below recent 10yr but above multi-decade average. Historically plausible. |

An independent investment strategy research (80/20 equity/bond Monte Carlo model) produced
a median 30-year nominal outcome of ~€1,272K for €1K/mo DCA — consistent with our 6%
baseline. The 10th percentile outcome (~€716K nominal) closely matches our 4% pessimistic
scenario. The probability of underperforming a savings account over 30 years is ~7%.

### Portfolio projections

#### €1,000/mo DCA (€7,000 lump at month 0)

| Return | Year 10 | Year 20 | Year 32.1 | Year 32.6 |
| ------ | ------: | ------: | --------: | --------: |
| 4%     | €157,058 (AT €150,866) | €379,180 (AT €349,898) | €794,259 (AT €691,701) | €816,038 (AT €708,747) |
| 6%     | €175,009 (AT €165,047) | €475,889 (AT €423,209) | €1,172,202 (AT €956,262) | €1,212,930 (AT €986,571) |
| 8%     | €195,237 (AT €180,662) | €601,626 (AT €513,358) | €1,763,221 (AT €1,369,975) | €1,838,491 (AT €1,424,463) |

#### €1,500/mo DCA (€7,000 lump at month 0)

| Return | Year 10 | Year 20 | Year 31.4 | Year 31.8 |
| ------ | ------: | ------: | --------: | --------: |
| 4%     | €230,406 (AT €221,410) | €561,100 (AT €517,577) | €1,136,815 (AT €985,641) | €1,157,805 (AT €1,002,133) |
| 6%     | €256,246 (AT €241,439) | €702,608 (AT €620,046) | €1,657,737 (AT €1,350,286) | €1,696,294 (AT €1,379,076) |
| 8%     | €285,299 (AT €263,810) | €886,125 (AT €748,508) | €2,461,619 (AT €1,913,003) | €2,531,643 (AT €1,963,820) |

AT = after Spanish CGT at full liquidation (19–30% progressive brackets). Effective tax
rates range from ~26% to ~29%.

### Fees and their impact

- **VWCE TER:** 0.19%
- **MyInvestor fondos indexados:** 0.10–0.59% TER
- **Fee drag over 30 years** (at 7% gross, €1K/mo): 0.22% vs 0.50% TER → ~€56K difference
- Prefer the lowest-cost accumulating global equity fondo available on your platform

---

## 4. Property Market Context

### Target area: Castellón coast

| Scenario    | Rate     | Rationale |
| ----------- | -------- | --------- |
| Pessimistic | **1.0%** | Long stagnations historically plausible. 20yr CAGR was negative. |
| Baseline    | **2.5%** | Matches Castellón's official last-decade CAGR exactly. |
| Optimistic  | **4.0%** | Close to Spain's long-run CAGR (~4.0%). |

At ~2% inflation, 2.5% nominal is only ~0.5% real appreciation per year.

### Current asking prices (Feb 2026)

| Town | Asking €/m² | 10yr CAGR (asking) |
| ---- | ----------- | ------------------ |
| Benicàssim | €2,796 | ~4.9% |
| Peñíscola | €2,204 | ~4.1% |
| Oropesa del Mar | €2,004 | ~3.2% |
| Vinaròs | €1,683 | ~3.2% |
| Province average | €1,526 | ~3.6% |

### Projected flat values

| Scenario | Starting price | Year 10 | Year 15 | Year 20 |
| -------- | -------------- | ------- | ------- | ------- |
| 1% | €200,000 | €220,924 | €232,310 | €244,038 |
| 2.5% | €200,000 | €256,017 | €289,666 | €327,723 |
| 4% | €200,000 | €296,049 | €360,189 | €438,225 |
| 1% | €250,000 | €276,156 | €290,388 | €305,048 |
| 2.5% | €250,000 | €320,021 | €362,082 | €409,654 |
| 4% | €250,000 | €370,061 | €450,237 | €547,781 |

### Key risk factors

- **Castellón's crash history:** -42% over 7.5 years (2007–2015). Deeper and longer than
  Spain overall. For the buy-later strategy, a crash is actually *helpful* — it makes the
  target cheaper. This is a structural advantage over buying now with a mortgage.
- **Tourist rental regulation (VUT):** Tightened rules may reduce the "investor bid" portion
  of coastal demand, potentially flattening prices — again helpful for buy-later.
- **Climate and flood risk:** Any specific property should be checked against PATRICOVA and
  SNCZI flood mapping. Insurance and maintenance costs may increase.
- **Supply not constrained:** Castellón is not on Banco de España's supply-bottleneck list.

---

## 5. Purchase Timeline

The target is a moving one: the flat price appreciates while you invest. The tables below
show when the after-tax portfolio reaches the appreciated flat price + 10% for ITP and fees.

### When can you buy outright? (after tax + appreciation + purchase costs)

**€1,000/mo DCA:**

| Return | €200K @ 1% | €200K @ 2.5% | €200K @ 4% | €250K @ 1% | €250K @ 2.5% | €250K @ 4% |
| ------ | ---------: | -----------: | ---------: | ---------: | -----------: | ---------: |
| 4%     | 15.8yr (52) | 20.8yr (57) | 50+ yr | 19.3yr (55) | 27.2yr (63) | 50+ yr |
| 6%     | 14.0yr (50) | 17.2yr (53) | 24.0yr (60) | 16.8yr (53) | 21.2yr (57) | 32.7yr (69) |
| 8%     | 12.8yr (49) | 14.9yr (51) | 18.8yr (55) | 15.0yr (51) | 18.0yr (54) | 23.6yr (60) |

**€1,500/mo DCA:**

| Return | €200K @ 1% | €200K @ 2.5% | €200K @ 4% | €250K @ 1% | €250K @ 2.5% | €250K @ 4% |
| ------ | ---------: | -----------: | ---------: | ---------: | -----------: | ---------: |
| 4%     | 11.0yr (47) | 13.2yr (49) | 17.8yr (54) | 13.6yr (50) | 17.1yr (53) | 27.8yr (64) |
| 6%     | 10.1yr (46) | 11.8yr (48) | 14.4yr (50) | 12.2yr (48) | 14.7yr (51) | 19.2yr (55) |
| 8%     | 9.4yr (45) | 10.7yr (47) | 12.6yr (49) | 11.2yr (47) | 13.0yr (49) | 15.9yr (52) |

### Baseline expectation

At 6% return and 2.5% property appreciation:

| DCA | Flat | Years to buy | Purchase age | Flat appreciated to | Total needed |
| --- | ---- | :----------: | :----------: | ------------------: | -----------: |
| €1,000 | €200K | 17.2 | **53** | ~€306K | ~€336K |
| €1,000 | €250K | 21.2 | **57** | ~€422K | ~€465K |
| €1,500 | €200K | 11.8 | **48** | ~€267K | ~€294K |
| €1,500 | €250K | 14.7 | **51** | ~€359K | ~€395K |

These are median estimates. Based on the investment research's Monte Carlo analysis, the
actual purchase date has a probabilistic range of roughly +/−5 years depending on market
performance. At p10 (bad luck), the timeline extends; at p90 (good luck), it shortens.

### Post-purchase outlook

At the point of purchase, nearly the entire portfolio goes to the flat — remaining balance
is ~€0–2K. From that point forward, you own outright and invest the full monthly capacity
into a retirement portfolio.

Example (baseline 2.5% appreciation, €1.5K/mo at 6%): buy €200K flat at age 48, then
invest €1.5K/mo for the remaining ~21 years to age ~69 → portfolio at age 69: **~€680K+**
(pure retirement savings, no housing cost, no mortgage).

### The trade-off

The cost of this strategy is **renting for 10–21 years longer** than if you bought now.
At €500/mo with 3% inflation, total rent over 12 years is ~€82K; over 17 years: ~€132K.
This is the "price" of avoiding €171–196K in mortgage interest and eliminating forced-sale
risk.

At baseline assumptions, the rent cost during the investment phase roughly offsets the
mortgage interest saved. The net financial benefit is smaller than it first appears, but the
strategy retains full liquidity and zero forced-sale risk throughout.

### Two-phase lifecycle

```
Years 0–12: Rent cheap. Invest aggressively (80–90% equity).
            Portfolio grows toward flat purchase target.
            Full liquidity. Flexible timing. No obligations.

Year ~12:   Buy flat outright. Pay CGT on gains. Own free and clear.
            No mortgage. No interest. No bank.

Years 12–33: Own flat. Invest €1.5K/mo into retirement portfolio.
             Shift allocation toward 60/40 via traspasos.
             At age ~69: flat owned + ~€680K+ liquid retirement savings.
```

---

## 6. Rental Stability During Investment Phase

Securing stable, affordable housing for ~10–15 years is critical. Spanish rental law (LAU)
provides strong protections for _vivienda habitual_ leases.

### Contract stability under LAU

| Landlord type | Mandatory minimum | Tacit renewal | Total potential stay |
| ------------- | ----------------- | ------------- | -------------------- |
| Individual | **5 years** | + up to 3yr | **~8 years** |
| Legal entity | **7 years** | + up to 3yr | **~10 years** |

- Landlord must give **4 months' notice** to not renew; tenant gives **2 months'**
- Sale of the property does not break the lease during the protected period (Art. 14 LAU)

### In-contract rent updates

- Only once per year, only if the contract has an update clause (Art. 18 LAU)
- Limited by the INE reference index (2023 Housing Law)
- In practice: modest, index-like increases (~2–3%/yr)

### Market resets between contracts

- When a contract ends, rent resets to market rate
- "Stressed area" caps do not apply in Castellón (no municipalities declared)
- This is the main rent risk: periodic jumps of 15–20% at contract boundaries

### Rent inflation scenarios

| Scenario | Avg annual | Year 10 | Year 15 | Year 20 |
| -------- | ---------: | ------: | ------: | ------: |
| Low (1.5%) | 1.5% | €580 | €619 | €673 |
| **Baseline (3%)** | **3%** | **€672** | **€779** | **€903** |
| High (6%) | 6% | €895 | €1,198 | €1,604 |

### Coastal-specific risk

On the Castellón coast, landlords may prefer **seasonal contracts** (_arrendamientos por
temporada_), which do not carry LAU stability protections. **Only sign _vivienda habitual_
contracts**, even if the selection is smaller.

---

## 7. Risk Assessment

### Equity market crashes

| Scenario | Impact on smooth portfolio | Notes |
| -------- | ------------------------- | ----- |
| -40% crash at year 2, recovery over 5yr | −11% to −18% of final value | Survivable: 10+ years of DCA buys cheap units |
| -40% crash at year 10 (near purchase) | Delays purchase by 2–4 years | Flexibility to wait is the key advantage |

An early crash during the accumulation phase is manageable — continued monthly contributions
buy more units at depressed prices. A crash *near* the intended purchase date means waiting
longer, not losing money (the portfolio recovers, you just delay).

### Property crash: helps the buy-later strategy

Unlike buying now with a mortgage (where a crash creates negative equity and forced-sale
catastrophe), a property crash during the investment phase makes the target **cheaper**. If
Castellón has another -20% to -40% crash, the buy-later investor can purchase sooner and at
a lower price. This is the strategy's most important structural advantage.

### Property appreciates faster than portfolio

The worst-case scenario for this strategy: property grows at 4%/yr while investment returns
are only 4%. At those assumptions, the €250K flat becomes unreachable (50+ years). This
requires sustained outperformance of Castellón property vs global equities — possible but
historically unlikely.

**Mitigation:** target a €200K flat (more achievable), increase DCA capacity, or accept a
longer timeline. The strategy remains viable for the €200K target even at pessimistic
investment returns if property appreciation is moderate.

### Income instability

A mortgage is a rigid 30-year legal obligation. This portfolio is a liquid asset with zero
ongoing obligation. If income is disrupted:

- **Buy-later investor:** pause DCA instantly, draw from portfolio if needed, move to a
  cheaper flat. A delay is just a delay — not a crisis.
- **Mortgage buyer:** owes ~€1,449/mo regardless of income, needs €4,071/mo net to stay
  below 35% housing ratio, faces €56–95K net losses if forced to sell.

For anyone with meaningful probability of income disruption in the 5+ year horizon (AI-driven
job market shifts, career transitions, reduced earnings), the buy-later strategy dominates.

---

## 8. Tax Optimization Roadmap

### Capital gains tax (rendimientos del ahorro) — 2025+ rates

| Gain bracket | Combined rate |
| ------------ | -----------: |
| First €6,000 | 19% |
| €6,000–€50,000 | 21% |
| €50,000–€200,000 | 23% |
| €200,000–€300,000 | 27% |
| Above €300,000 | 30% |

### Traspaso-based rebalancing

Execute all allocation shifts (equity → bonds, provider switches) via traspasos. No taxable
event until final sale. This is the single most important tax-efficiency lever.

### CGT at flat purchase

When selling the portfolio to buy the flat, the full gain is realised in one tax year. This
pushes a large fraction into the 27–30% brackets. Unlike retirement (where phased withdrawals
over 5+ years reduce the effective rate), the purchase event is a single liquidation.

At the baseline scenario (€1.5K/mo, 6%, buying at year ~12 with ~€267K gain):
- Tax: ~€60–65K
- Effective rate: ~24%
- After-tax portfolio: ~€294K (enough to cover the appreciated flat + 10% costs)

### Planes de pensiones (small supplement)

Contribute up to €1,500/year if your current marginal IRPF rate is meaningfully higher than
your expected retirement rate. The annual tax saving is modest (€90–200/yr depending on
marginal rate) but compounds over time. Accept the illiquidity: these funds are locked until
retirement (with a 10-year liquidity rule from 2025 for qualifying contributions).

### Wealth tax monitoring

Valencian mínimo exento: €1,000,000 net taxable wealth. Monitor as the portfolio grows.
Primary residence has a partial exemption (up to €300K) — once you buy the flat, this
shelters part of your wealth from the tax.

### FIFO management

Spain uses first-in-first-out for cost basis. The oldest (most appreciated) lots are sold
first. Keep records. When eventually selling to buy the flat, this is unavoidable — but
after purchase, new contributions start fresh cost bases.

---

## 9. Open Questions and Next Steps

- [ ] **Specific flat type and municipality to target.** Benicàssim, Oropesa, Peñíscola,
  Vinaròs — each has different price levels, rental yields, and lifestyle trade-offs.
- [ ] **Comparable rental data for the target flat type.** The GPT Pro peer review identified
  this as the single most decision-critical variable. If the equivalent rent for a €200K+
  flat is €700–800/mo (not €500), the comparison shifts materially.
- [x] **Platform selection.** Trade Republic (primary) + MyInvestor (backup).
- [x] **Fund selection — equity.** Fidelity MSCI World Index Fund P-Acc-EUR (IE00BYX5NX33,
  0.12% TER, accumulating). Confirmed on TR with savings plan support.
- [x] **Fund selection — bonds.** Vanguard Global Bond Index Fund EUR Hedged Acc
  (IE00B18GC888, 0.15% TER, accumulating). Confirmed on TR as mutual fund (traspaso eligible).
- [ ] **Career risk assessment.** Plausible income-drop scenarios over the next 10–15 years.
- [ ] **Renovation/furnishing budget.** Personal estimate needed for when purchase happens.
- [ ] **Start investing.** See Week 1 checklist below.

---

## Week 1 Action Checklist

### Confirmed portfolio

| Sleeve | Fund | ISIN | TER | Type |
| ------ | ---- | ---- | --: | ---- |
| Equity (80–90%) | Fidelity MSCI World P-Acc-EUR | IE00BYX5NX33 | 0.12% | Mutual fund (traspaso eligible) |
| Bonds (10–20%) | Vanguard Global Bond EUR Hedged Acc | IE00B18GC888 | 0.15% | Mutual fund (traspaso eligible) |
| Emergency buffer | Trade Republic cash account | — | ~2% (tracks ECB) | Bank deposit (€100K guarantee) |

### Steps (in order)

- [ ] **Confirm TR IBAN is Spanish.** If you still have a German IBAN, activate the Spanish
  one in app settings. Interest can be paused until you do.
- [ ] **Sell the FTSE All-World ETF position (~€167).** This is a small loss (~€4) which is
  tax-deductible against future gains. Redirect the cash to the equity fondo.
- [ ] **Ensure €8,000 is in TR cash as emergency buffer.** Verify interest is accruing
  (check monthly interest payment in transaction history).
- [ ] **Buy €7,000 of Fidelity MSCI World (IE00BYX5NX33).** One-off purchase. Expect
  forward NAV pricing (not instant like an ETF) — settlement is T+2 business days.
- [ ] **Set up monthly savings plan on IE00BYX5NX33.** Choose your DCA amount (€1,000 or
  €1,500). Set execution date a few days after salary arrives. Frequency: monthly.
- [ ] **Bond allocation — defer to month 2.** Start 100% equity. When ready, direct new
  contributions to IE00B18GC888 until you reach the 80/20 target, or use contribution
  rebalancing monthly.

### Month 2–3

- [ ] Begin directing ~20% of monthly contributions to Vanguard bond fund (IE00B18GC888)
- [ ] Verify first savings plan executed correctly (check transaction history)
- [ ] Set calendar reminder: quarterly allocation check (are you within 5pp of 80/20?)

### Ongoing rules

- **Check allocation quarterly.** If within 75–85% equity, do nothing.
- **If outside the band:** use contribution rebalancing first; traspaso only if drift
  persists after 2 months of directed contributions.
- **During a crash:** keep the savings plan running. Do not sell. If equity drops below 75%,
  traspaso from bonds to equity (buy low, mechanically).
- **Annual review:** verify fund TERs haven't changed, tax paperwork matches TR certificates,
  buffer still covers 4–6 months of expenses, rent contract status.

---

## 10. Alternative Strategies Considered

This plan was chosen after a comprehensive three-way comparison of buy now (mortgage),
rent forever (invest), and invest now (buy later). The full analysis — including mortgage
amortisation schedules, forced-sale risk tables, 3×3 comparison matrices across property
growth and investment return scenarios, sensitivity testing, equity/property crash stress
tests, and retirement cashflow modelling — is preserved in the reference documents below.

**Key finding from the comparison:** at a €500/mo rent baseline, renting + investing wins in
8/9 scenario combinations at the end of a ~32-year timeline. Buying now with a mortgage wins
only at optimistic property growth (4%) + pessimistic investment returns (4%). The buy-later
strategy captures the renter's compounding advantage while adding eventual mortgage-free
ownership.

**Reference documents:**

- [Full three-way comparison analysis](alternatives/full-comparison-analysis.md) — complete
  analysis with all computations, matrices, sensitivity runs, and peer review revisions
- [Buy now with mortgage — scenario analysis](alternatives/buy-now-with-mortgage.md) —
  mortgage terms, upfront costs, amortisation, ongoing costs, forced-sale risk, crash
  scenarios
