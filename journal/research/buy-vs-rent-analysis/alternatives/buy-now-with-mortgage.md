# Buy Now with Mortgage — Scenario Analysis

> This document contains the mortgage-purchase scenario analysis, extracted from the
> full comparison analysis. It covers upfront costs, mortgage terms, ongoing ownership
> costs, amortisation schedules, forced-sale risk, owner cost inflation, and property
> crash scenarios.
>
> For the complete three-way comparison (buy now vs rent forever vs invest-then-buy),
> see [full-comparison-analysis.md](full-comparison-analysis.md).

---

## Part 2 — Mortgage & Payment Scheme

**Goal:** Understand the full cost of buying — not just the mortgage, but everything around it.

### 2A — Upfront Costs

#### Down payment (via IVF guarantee)

- €250K flat → **€12,500** down payment, **€237,500** mortgage
- €200K flat → **€10,000** down payment, **€190,000** mortgage

#### Purchase tax

**Second-hand (resale):** ITP (Transmisiones Patrimoniales Onerosas)

- Current rate in Comunitat Valenciana: **10%**
- Drops to **9% from 1 June 2026** (Ley 5/2025, BOE)
- Tax base is the higher of declared price or Catastro "valor de referencia" (RDL 1/1993)

**New build:** IVA (10% national) + AJD (1.5% in CV, dropping to 1.4% from June 2026)

#### Fees (mid-case estimates)

| Item                   | €250K flat | €200K flat | Notes                                     |
| ---------------------- | ---------- | ---------- | ----------------------------------------- |
| Notary (purchase deed) | ~€850      | ~€800      | Regulated tariff (arancel)                |
| Land Registry          | ~€550      | ~€500      | Regulated tariff                          |
| Gestoría               | ~€400      | ~€400      | Administrative handling                   |
| Appraisal (tasación)   | ~€400      | ~€400      | Buyer-paid per Ley 5/2019                 |
| Agency fee             | €0         | €0         | Typically seller pays; contract-dependent |

#### Total cash needed at purchase (second-hand, mid-case)

| Item         | €250K flat (ITP 10%) | €250K flat (ITP 9%) | €200K flat (ITP 10%) | €200K flat (ITP 9%) |
| ------------ | -------------------- | ------------------- | -------------------- | ------------------- |
| Down payment | €12,500              | €12,500             | €10,000              | €10,000             |
| ITP          | €25,000              | €22,500             | €20,000              | €18,000             |
| Notary       | €850                 | €850                | €800                 | €800                |
| Registry     | €550                 | €550                | €500                 | €500                |
| Gestoría     | €400                 | €400                | €400                 | €400                |
| Appraisal    | €400                 | €400                | €400                 | €400                |
| **Total**    | **~€39,700**         | **~€37,200**        | **~€32,100**         | **~€30,100**        |

Plausible range: ±€1,500–€2,000 depending on fee variability and whether the Catastro reference value exceeds the
purchase price.

#### Still to be checked for specific flats

Initial renovation/furnishing budget (personal estimate needed), and whether the Catastro
"valor de referencia" exceeds the target purchase price.

### 2B — Mortgage Terms

#### Rate landscape (early 2026)

30-year fixed at **80% LTV** (standard, no IVF):

- CaixaBank CasaFácil: 2.85% TIN (bonified) / 3.85% TIN (non-bonified)
- Banco Sabadell Hipoteca Fija: 2.75% TIN (bonified) / 3.75% TIN (non-bonified)
- INE average on new housing mortgages (all types): 2.87% in Dec 2025 — useful anchor, not a 30yr fixed quote

30-year fixed at **95% LTV** (via IVF guarantee):

- IVF reduces lender risk on the above-80% tranche, but rate is still bank-set
- Higher LTV typically means less aggressive pricing unless borrower profile is very strong

| 95% LTV scenario        | Rate range    | Notes                                      |
| ----------------------- | ------------- | ------------------------------------------ |
| Best case               | ~3.5–3.9% TIN | Strong borrower, heavy bundling, best bank |
| Average                 | ~4.0–4.4% TIN | Realistic for most borrowers               |
| Prudent (for modelling) | **~4.5% TIN** | Buffers against pricing shifts             |

**We model at 4.0% (baseline) and 4.5% (prudent).**

#### Productos vinculados (bundled products for rate bonification)

Banks typically require some combination of:

- Payroll domiciliation + bank account + card usage
- Home (damage) insurance — **mandatory** regardless (buyer can choose insurer)
- Life insurance — not legally required, but strongly incentivised via rate discounts
- Sometimes: payment protection, pension plan, alarm service

#### Monthly payments (principal + interest only)

| Rate (TIN) | €237,500 mortgage (95% of €250K) | €190,000 mortgage (95% of €200K) |
| ---------- | -------------------------------- | -------------------------------- |
| 3.5%       | ~€1,066/mo                       | ~€853/mo                         |
| **4.0%**   | **~€1,134/mo**                   | **~€907/mo**                     |
| **4.5%**   | **~€1,203/mo**                   | **~€963/mo**                     |

These are pure amortisation payments. They **exclude** insurance, IBI, community fees, and maintenance — see ongoing
costs section below.

### 2B.1 — Age-Related Considerations

Buyer is 36. After a ~1.5–2.7 year saving period, purchase happens at age ~38–39. A 30-year mortgage from that point
means finishing at age **68–69**.

#### Bank age limits — confirmed safe

No single legal maximum in Spain; banks set their own policies:

- **CaixaBank:** age + term must not exceed **80** (~39 + 30 = 69 — well within limit)
- **Bankinter:** general limit around **75**
- At 68–69, age is **not a complication** for underwriting — still within all stated bank limits

#### Insurance costs (annual)

| Insurance      | Estimated range       | Notes                                                     |
| -------------- | --------------------- | --------------------------------------------------------- |
| Life insurance | ~€300–€600/year       | Anchored to bank examples at age 30; adjusted up for 36.  |
|                |                       | Premium may be level or decrease with mortgage balance.   |
|                |                       | Not legally required, but strongly incentivised for rate. |
| Home (damage)  | ~€200–€400/year       | **Mandatory.** Buyer can choose insurer.                  |
| **Combined**   | **~€500–€1,000/year** | Prudent planning envelope (~€42–€83/month)                |

CaixaBank example: life ~€266/yr at age 30, home ~€317/yr. Sabadell example: life ~€254/yr at age 30, home ~€156/yr.
Both from representative disclosure scenarios.

#### Income trajectory and retirement (qualitative — not research-answerable)

- At 36, likely still in career growth years. Peak earning capacity probably extends to ~50–55.
- The last 10 years of the mortgage (age ~59–69) coincide with a phase where earning power may plateau or decline. This
  is a solvency consideration that connects to 2D forced-sale risk.
- **The positive flip:** at ~68–69, the mortgage is done. The buyer owns the flat outright around retirement age —
  housing cost drops to ongoing only (~€500+/mo by then).
- **Rent scenario contrast:** at ~68–69, the renter is still paying rent (€1,300+/mo at 3% inflation) from pension +
  portfolio withdrawals. But the renter has had ~32–33 years of compounding. See 6.6 for the quantified retirement
  model.

### 2B.2 — Ongoing Ownership Costs (researched)

The mortgage payment and insurance are not the full picture. These recurring costs significantly affect total cost of
ownership and the buy-vs-rent comparison.

#### IBI (Impuesto sobre Bienes Inmuebles)

Municipal property tax. Rate set by each town; tax base is the valor catastral (typically ~50% of market value per the
RM=0.5 coefficient, though older revisions can drift lower).

| Municipality          | Urban IBI rate | IBI if VC=€100K | IBI if VC=€125K |
| --------------------- | -------------- | --------------- | --------------- |
| Benicàssim            | 0.58%          | ~€580           | ~€725           |
| Oropesa del Mar       | 0.670%         | ~€670           | ~€838           |
| Peñíscola             | 0.80%          | ~€800           | ~€1,000         |
| Vinaròs               | 0.772%         | ~€772           | ~€965           |
| Castellón de la Plana | 0.6492%        | ~€649           | ~€812           |

**Planning band: ~€500–€1,000/year** for a €200–250K flat. IBI is not fixed — rates and cadastral values can be revised
over time. Assume upward pressure over decades.

#### Community fees (gastos de comunidad)

Monthly charges to the community of owners for building upkeep. The biggest variable in ongoing costs — driven by
amenities, building age, and maintenance history.

| Scenario                               | Monthly range   | What it covers                            |
| -------------------------------------- | --------------- | ----------------------------------------- |
| Low (basic building, modest amenities) | €40–€70/mo      | Lift, basic common areas, limited extras  |
| **Mid (typical coastal, lift + pool)** | **€80–€150/mo** | Lift, pool, garden, common lighting       |
| High (amenity-heavy or ageing)         | €150–€250+/mo   | Multiple lifts, extensive grounds, ageing |

Community fees tend to rise over time with labour, energy, and contract costs. **Mid-range (~€100/mo) is the most
realistic planning case for a coastal flat with a pool.**

#### Derramas (special assessments)

Extraordinary charges for major works not covered by ordinary fees or the reserve fund.

| Work type              | Typical cost range           | Per-flat estimate (20-unit building) |
| ---------------------- | ---------------------------- | ------------------------------------ |
| Facade rehabilitation  | €30–€120/m² of facade        | ~€900–€3,600 per flat                |
| Roof waterproofing     | ~€21–€25/m²                  | Shared across top-floor + community  |
| Lift replacement/major | Material — building-specific | Can be significant; check minutes    |

Budget a **non-zero annual reserve** for derramas even if the building looks well maintained. Due diligence: review the
community's last annual accounts, minutes, reserve fund balance, and planned works before purchasing.

#### Basura / waste collection tax

Separate municipal charge. Varies enormously:

- Benicàssim: €120–€150/yr (linked to valor catastral)
- Oropesa del Mar: €28.88/yr (flat rate)
- Vinaròs: €68.39/yr
- Spain average 2025: ~€116/yr

**Planning estimate: ~€70–€130/year** for most coastal Castellón municipalities.

#### Consolidated annual ongoing costs (excluding mortgage and insurance)

| Scenario | IBI     | Community fees | Derramas (avg) | Waste | **Total/year** | **Total/month** |
| -------- | ------- | -------------- | -------------- | ----- | -------------- | --------------- |
| Low      | ~€500   | ~€720/yr       | ~€200          | ~€30  | **~€1,300**    | **~€108**       |
| **Mid**  | ~€750   | ~€1,320/yr     | ~€600          | ~€100 | **~€2,770**    | **~€231**       |
| High     | ~€1,000 | ~€2,400/yr     | ~€1,500        | ~€150 | **~€5,050**    | **~€421**       |

Community fees + derramas dominate the variability. IBI is more stable and predictable. **The mid-case (~€231/month) is
the planning figure for the Part 4 comparison.**

### 2C — Amortisation Timeline (computed)

All figures rounded to nearest euro. French amortisation (constant monthly payment).

#### €250K flat — €237,500 mortgage at 4.0% TIN (monthly: €1,134)

| Year | Interest/yr | Principal/yr | Cum. paid | Cum. interest | Cum. principal | Balance  |
| ---: | ----------- | ------------ | --------- | ------------- | -------------- | -------- |
|    1 | €9,424      | €4,182       | €13,606   | €9,424        | €4,182         | €233,318 |
|    2 | €9,253      | €4,353       | €27,213   | €18,677       | €8,535         | €228,965 |
|    3 | €9,076      | €4,530       | €40,819   | €27,753       | €13,066        | €224,434 |
|    5 | €8,699      | €4,907       | €68,032   | €45,345       | €22,687        | €214,813 |
|    7 | €8,292      | €5,315       | €95,244   | €62,136       | €33,109        | €204,391 |
|   10 | €7,615      | €5,991       | €136,063  | €85,675       | €50,388        | €187,112 |
|   15 | €6,291      | €7,315       | €204,095  | €119,884      | €84,211        | €153,289 |
|   20 | €4,674      | €8,932       | €272,127  | €146,618      | €125,508       | €111,992 |
|   25 | €2,700      | €10,906      | €340,158  | €164,226      | €175,932       | €61,568  |
|   30 | €290        | €13,316      | €408,190  | €170,690      | €237,500       | €0       |

#### €250K flat — €237,500 mortgage at 4.5% TIN (monthly: €1,203)

| Year | Interest/yr | Principal/yr | Cum. paid | Cum. interest | Cum. principal | Balance  |
| ---: | ----------- | ------------ | --------- | ------------- | -------------- | -------- |
|    1 | €10,609     | €3,831       | €14,441   | €10,609       | €3,831         | €233,669 |
|    2 | €10,433     | €4,007       | €28,881   | €21,042       | €7,839         | €229,661 |
|    3 | €10,249     | €4,192       | €43,322   | €31,291       | €12,030        | €225,470 |
|    5 | €9,855      | €4,585       | €72,203   | €51,203       | €21,000        | €216,500 |
|    7 | €9,424      | €5,016       | €101,084  | €70,271       | €30,813        | €206,687 |
|   10 | €8,700      | €5,740       | €144,405  | €97,118       | €47,288        | €190,212 |
|   15 | €7,255      | €7,185       | €216,608  | €136,414      | €80,194        | €157,306 |
|   20 | €5,446      | €8,995       | €288,811  | €167,424      | €121,387       | €116,113 |
|   25 | €3,181      | €11,260      | €361,013  | €188,062      | €172,952       | €64,548  |
|   30 | €346        | €14,095      | €433,216  | €195,716      | €237,500       | €0       |

#### €200K flat — €190,000 mortgage at 4.0% TIN (monthly: €907)

| Year | Interest/yr | Principal/yr | Cum. paid | Cum. interest | Cum. principal | Balance  |
| ---: | ----------- | ------------ | --------- | ------------- | -------------- | -------- |
|    1 | €7,539      | €3,346       | €10,885   | €7,539        | €3,346         | €186,654 |
|    2 | €7,403      | €3,482       | €21,770   | €14,942       | €6,828         | €183,172 |
|    3 | €7,261      | €3,624       | €32,655   | €22,203       | €10,452        | €179,548 |
|    5 | €6,960      | €3,925       | €54,425   | €36,276       | €18,150        | €171,850 |
|    7 | €6,633      | €4,252       | €76,195   | €49,708       | €26,487        | €163,513 |
|   10 | €6,092      | €4,793       | €108,851  | €68,540       | €40,310        | €149,690 |
|   15 | €5,033      | €5,852       | €163,276  | €95,907       | €67,369        | €122,631 |
|   20 | €3,739      | €7,146       | €217,701  | €117,295      | €100,407       | €89,593  |
|   25 | €2,160      | €8,725       | €272,127  | €131,381      | €140,746       | €49,254  |
|   30 | €232        | €10,653      | €326,552  | €136,552      | €190,000       | €0       |

#### €200K flat — €190,000 mortgage at 4.5% TIN (monthly: €963)

| Year | Interest/yr | Principal/yr | Cum. paid | Cum. interest | Cum. principal | Balance  |
| ---: | ----------- | ------------ | --------- | ------------- | -------------- | -------- |
|    1 | €8,487      | €3,065       | €11,552   | €8,487        | €3,065         | €186,935 |
|    2 | €8,346      | €3,206       | €23,105   | €16,834       | €6,271         | €183,729 |
|    3 | €8,199      | €3,353       | €34,657   | €25,033       | €9,624         | €180,376 |
|    5 | €7,884      | €3,668       | €57,762   | €40,962       | €16,800        | €173,200 |
|    7 | €7,539      | €4,013       | €80,867   | €56,217       | €24,650        | €165,350 |
|   10 | €6,960      | €4,592       | €115,524  | €77,694       | €37,830        | €152,170 |
|   15 | €5,804      | €5,748       | €173,286  | €109,131      | €64,155        | €125,845 |
|   20 | €4,357      | €7,196       | €231,049  | €133,939      | €97,110        | €92,890  |
|   25 | €2,545      | €9,008       | €288,811  | €150,449      | €138,361       | €51,639  |
|   30 | €277        | €11,276      | €346,573  | €156,573      | €190,000       | €0       |

#### 30-year total cost summary

| Mortgage              | Rate | Monthly | Total paid   | Total interest | Interest as % of principal |
| --------------------- | ---- | ------- | ------------ | -------------- | -------------------------- |
| €237,500 (€250K flat) | 4.0% | €1,134  | **€408,190** | **€170,690**   | 71.9%                      |
| €237,500 (€250K flat) | 4.5% | €1,203  | **€433,216** | **€195,716**   | 82.4%                      |
| €190,000 (€200K flat) | 4.0% | €907    | **€326,552** | **€136,552**   | 71.9%                      |
| €190,000 (€200K flat) | 4.5% | €963    | **€346,573** | **€156,573**   | 82.4%                      |

At 4.0%, you pay **72% of the principal again in interest** over 30 years. At 4.5%, it's **82%**. The 0.5% rate
difference costs an extra ~€25K on the €250K flat and ~€20K on the €200K flat.

Key observations for the 2D forced-sale analysis:

- At year 5, only ~€22K of principal is paid on the €250K flat at 4.0% — out of €68K total paid. The other €45K went to
  interest. Equity is minimal relative to money sunk.
- At year 10, ~€50K principal paid on €237.5K — still only 21% of the mortgage. Balance remaining: €187K. Early years
  are heavily interest-weighted.

### 2D — Forced Sale / Insolvency Risk

The world is unstable. There is a real possibility that at some point during the mortgage, something unpredictable
happens — job loss, economic crisis, health, geopolitical disruption — and I simply cannot continue paying. This is not
a "what if I want to sell" scenario. This is: **what does my financial position look like if I _have_ to sell because I
can't pay?**

This matters because:

- A forced sale means selling on someone else's timeline, likely at a bad moment (personal crisis often coincides with
  market downturns — recessions hit employment and property values at the same time)
- Selling costs eat into whatever equity exists
- Early in the mortgage, most payments went to interest — equity may be minimal
- If the flat has depreciated, I could owe more than it's worth (negative equity)

#### Selling costs in Spain (researched)

| Cost                         | Amount / rate                         | Notes                                                  |
| ---------------------------- | ------------------------------------- | ------------------------------------------------------ |
| Agency commission            | 3–5% of sale price + IVA (21%)        | Typically seller pays, but contract-dependent          |
| Plusvalía municipal (IIVTNU) | Varies — needs cadastral land value   | Reformed post-RDL 26/2021: two methods (objective      |
|                              |                                       | vs real), taxpayer picks the more favourable one.      |
|                              |                                       | No tax if no gain. Needs municipal coefficients.       |
| Capital gains tax (IRPF)     | Progressive: 19/21/23/27/30%          | On "base del ahorro." Gain = sale price − purchase     |
|                              |                                       | price (adjusted for acquisition costs + improvements). |
|                              |                                       | 30% top bracket (>€300K) confirmed via Ley 7/2024.     |
| Early mortgage repayment     | Max 2% of repaid capital (first 10yr) | Ley 5/2019 caps. Max 1.5% after year 10.               |
| Registry cancellation        | A few hundred euros                   | Notary deed + registry inscription of cancellation     |

#### Income stress test — what triggers a forced sale?

The 2D scenario models the _outcome_ of a forced sale, but the _trigger_ is an income drop that makes the mortgage
unsustainable. The commonly cited danger threshold is housing costs exceeding **~35–40% of net income**.

Total monthly housing outflow (mortgage + insurance + ongoing costs):

Insurance mid-case: ~€60/mo (€500–€1,000/yr from 2B.1). Ongoing costs mid-case: ~€231/mo (€2,770/yr from 2B.2).
**Non-mortgage total: ~€291/mo.**

| Flat  | Rate | Mortgage | Insurance + ongoing (~€291/mo) | **Total**   |
| ----- | ---- | -------- | ------------------------------ | ----------- |
| €250K | 4.0% | €1,134   | ~€291                          | **~€1,425** |
| €250K | 4.5% | €1,203   | ~€291                          | **~€1,494** |
| €200K | 4.0% | €907     | ~€291                          | **~€1,198** |
| €200K | 4.5% | €963     | ~€291                          | **~€1,254** |

At what net monthly income does this become unsustainable?

| Flat  | Rate | Total outflow | Min income (35%) | Min income (40%) |
| ----- | ---- | ------------- | ---------------- | ---------------- |
| €250K | 4.0% | ~€1,425       | **~€4,071**      | ~€3,563          |
| €250K | 4.5% | ~€1,494       | **~€4,269**      | ~€3,735          |
| €200K | 4.0% | ~€1,198       | **~€3,423**      | ~€2,995          |
| €200K | 4.5% | ~€1,254       | **~€3,583**      | ~€3,135          |

For the €250K flat at 4.0%, you need at least **~€4,071/mo net income** to stay below 35%. If income drops below
~€3,563, you're above 40% — the danger zone.

Not yet assessed: plausible income-drop scenarios over 30 years and their connection to
forced-sale triggers.

#### Forced-sale net position (computed)

Assumptions: 5% selling costs (agency + frictions), 2% early repayment fee on outstanding balance (first 10 years, per
Ley 5/2019). Insurance €60/mo + ongoing costs €231/mo included in "total sunk." These are **not** distressed-price
discounts — actual forced sales could be worse.

##### €250K flat — €237,500 mortgage at 4.0%

| Year | Price scenario | Flat value | Balance  | Sell costs | Repay fee | **Net proceeds** | Total sunk | **Net loss**  |
| ---: | -------------- | ---------- | -------- | ---------- | --------- | ---------------- | ---------- | ------------- |
|    2 | 1% pessimistic | €255,025   | €228,965 | €12,751    | €4,579    | **€8,730**       | €73,897    | **−€65,167**  |
|    2 | 2.5% baseline  | €262,656   | €228,965 | €13,133    | €4,579    | **€15,979**      | €73,897    | **−€57,917**  |
|    2 | 4% optimistic  | €270,400   | €228,965 | €13,520    | €4,579    | **€23,336**      | €73,897    | **−€50,561**  |
|    3 | 1% pessimistic | €257,575   | €224,434 | €12,879    | €4,489    | **€15,773**      | €90,995    | **−€75,222**  |
|    3 | 2.5% baseline  | €269,223   | €224,434 | €13,461    | €4,489    | **€26,838**      | €90,995    | **−€64,157**  |
|    3 | 4% optimistic  | €281,216   | €224,434 | €14,061    | €4,489    | **€38,232**      | €90,995    | **−€52,763**  |
|    5 | 1% pessimistic | €262,753   | €214,813 | €13,138    | €4,296    | **€30,506**      | €125,192   | **−€94,686**  |
|    5 | 2.5% baseline  | €282,852   | €214,813 | €14,143    | €4,296    | **€49,600**      | €125,192   | **−€75,591**  |
|    5 | 4% optimistic  | €304,163   | €214,813 | €15,208    | €4,296    | **€69,846**      | €125,192   | **−€55,346**  |
|    7 | 1% pessimistic | €268,034   | €204,391 | €13,402    | €4,088    | **€46,153**      | €159,388   | **−€113,235** |
|    7 | 2.5% baseline  | €297,171   | €204,391 | €14,859    | €4,088    | **€73,834**      | €159,388   | **−€85,555**  |
|    7 | 4% optimistic  | €328,983   | €204,391 | €16,449    | €4,088    | **€104,055**     | €159,388   | **−€55,334**  |
|   10 | 1% pessimistic | €276,156   | €187,112 | €13,808    | €3,742    | **€71,494**      | €210,683   | **−€139,190** |
|   10 | 2.5% baseline  | €320,021   | €187,112 | €16,001    | €3,742    | **€113,166**     | €210,683   | **−€97,517**  |
|   10 | 4% optimistic  | €370,061   | €187,112 | €18,503    | €3,742    | **€160,704**     | €210,683   | **−€49,979**  |

##### €200K flat — €190,000 mortgage at 4.0%

| Year | Price scenario | Flat value | Balance  | Sell costs | Repay fee | **Net proceeds** | Total sunk | **Net loss**  |
| ---: | -------------- | ---------- | -------- | ---------- | --------- | ---------------- | ---------- | ------------- |
|    2 | 1% pessimistic | €204,020   | €183,172 | €10,201    | €3,663    | **€6,984**       | €60,854    | **−€53,870**  |
|    2 | 2.5% baseline  | €210,125   | €183,172 | €10,506    | €3,663    | **€12,784**      | €60,854    | **−€48,071**  |
|    2 | 4% optimistic  | €216,320   | €183,172 | €10,816    | €3,663    | **€18,669**      | €60,854    | **−€42,185**  |
|    3 | 1% pessimistic | €206,060   | €179,548 | €10,303    | €3,591    | **€12,619**      | €75,231    | **−€62,613**  |
|    3 | 2.5% baseline  | €215,378   | €179,548 | €10,769    | €3,591    | **€21,471**      | €75,231    | **−€53,761**  |
|    3 | 4% optimistic  | €224,973   | €179,548 | €11,249    | €3,591    | **€30,586**      | €75,231    | **−€44,646**  |
|    5 | 1% pessimistic | €210,202   | €171,850 | €10,510    | €3,437    | **€24,405**      | €103,985   | **−€79,581**  |
|    5 | 2.5% baseline  | €226,282   | €171,850 | €11,314    | €3,437    | **€39,680**      | €103,985   | **−€64,305**  |
|    5 | 4% optimistic  | €243,331   | €171,850 | €12,167    | €3,437    | **€55,877**      | €103,985   | **−€48,109**  |
|    7 | 1% pessimistic | €214,427   | €163,513 | €10,721    | €3,270    | **€36,922**      | €132,739   | **−€95,817**  |
|    7 | 2.5% baseline  | €237,737   | €163,513 | €11,887    | €3,270    | **€59,067**      | €132,739   | **−€73,672**  |
|    7 | 4% optimistic  | €263,186   | €163,513 | €13,159    | €3,270    | **€83,244**      | €132,739   | **−€49,496**  |
|   10 | 1% pessimistic | €220,924   | €149,690 | €11,046    | €2,994    | **€57,195**      | €175,871   | **−€118,676** |
|   10 | 2.5% baseline  | €256,017   | €149,690 | €12,801    | €2,994    | **€90,533**      | €175,871   | **−€85,338**  |
|   10 | 4% optimistic  | €296,049   | €149,690 | €14,802    | €2,994    | **€128,563**     | €175,871   | **−€47,308**  |

##### Key takeaways

**A forced sale is always a net loss in the first 10 years.** Even under the optimistic price scenario (4%/yr), selling
at year 10 means losing ~€48–50K on either flat. Under the pessimistic scenario, losses exceed **€100K** by year 10.

The loss comes from three compounding sources:

1. **Transaction costs** (upfront + selling) are enormous relative to early equity
2. **Interest-heavy early payments** mean most of what you've paid is gone, not stored as equity
3. **Ongoing costs** (€291/mo) accumulate — by year 10, that's ~€35K in insurance + IBI/community/waste

This is why the 2D forced-sale risk is not hypothetical — it's the single biggest asymmetric downside of buying versus
renting. A renter facing the same crisis walks away with their liquid portfolio (possibly down, but not structurally
destroyed by transaction costs).

#### Contrast with rent scenario under the same crisis

This is a key asymmetry. If the same crisis hits while renting:

- I stop paying rent — I lose the flat, but I owe nothing
- My investment portfolio is **liquid** — I can withdraw partially or fully
- The portfolio may also be down in a crisis, but I'm not forced to realise the full loss
- I have options: reduce contributions, pause, withdraw only what's needed

This contrast should feed directly into the Part 4 comparison.


---

### 6.1 — Owner cost inflation

Ongoing ownership costs inflate at **2%/yr** (conservative — below rent inflation). This
affects the buyer's total monthly outflow and spare capacity over the mortgage term.

| Year | Monthly (flat) | Monthly (2% inflated) | Cum. flat | Cum. inflated | Extra cost |
| ---: | -------------: | --------------------: | --------: | ------------: | ---------: |
|    1 |           €291 |                  €291 |    €3,492 |        €3,492 |         €0 |
|    5 |           €291 |                  €315 |   €17,460 |       €18,173 |      +€713 |
|   10 |           €291 |                  €348 |   €34,920 |       €38,236 |    +€3,316 |
|   15 |           €291 |                  €384 |   €52,380 |       €60,389 |    +€8,009 |
|   20 |           €291 |                  €424 |   €69,840 |       €84,846 |   +€15,006 |
|   25 |           €291 |                  €468 |   €87,300 |      €111,850 |   +€24,550 |
|   30 |           €291 |                  €517 |  €104,760 |      €141,664 |   +€36,904 |

Over 30 years, inflating owner costs at 2% adds **~€37K** in extra ownership costs compared to the flat assumption. By
year 30, the buyer's monthly non-mortgage costs have risen from €291 to €517.

Buyer total monthly outflow now **increases over time** (mortgage stays fixed, costs rise):

| Year | €250K flat (mortgage + costs) | €200K flat (mortgage + costs) |
| ---: | ----------------------------: | ----------------------------: |
|    1 |                        €1,425 |                        €1,198 |
|   10 |                        €1,482 |                        €1,255 |
|   20 |                        €1,558 |                        €1,331 |
|   30 |                        €1,651 |                        €1,424 |

This is used in the updated equal-outflow comparison (Step 9). The renter's investable surplus now changes due to both
rising rent AND rising buyer outflow.

---

### 6.4 — Property crash in forced sale

The 2D tables in Part 2 assume prices grow at 1%+. Forced sales are most likely to happen
_during_ a downturn — exactly when prices are down. This section models that scenario.

#### Scenario: -20% price shock, no recovery (permanent)

€250K flat at 4.0%. Property drops to €200K and stays there. Total sunk consistent with
Part 2D (upfront + cumulative mortgage + insurance + ongoing at flat €291/mo).

| Year | Flat value | Balance  | Negative equity? | Net proceeds | Total sunk | **Net loss**  |
| ---: | ---------- | -------- | :--------------: | ------------ | ---------- | ------------- |
|    3 | €200,000   | €224,434 |     **YES**      | **−€38,923** | €90,995    | **−€129,918** |
|    5 | €200,000   | €214,813 |     **YES**      | **−€29,109** | €125,192   | **−€154,301** |
|    7 | €200,000   | €204,391 |     **YES**      | **−€18,479** | €159,388   | **−€177,867** |

**At year 3, you owe the bank €38,923 AFTER selling.** You've sunk €91K in total and walk
away owing money. At year 7, you still owe €18K after the sale and your net loss is €178K.

Negative equity at 95% LTV with a 20% price drop is not hypothetical — Castellón's last crash was -42%. At 95% LTV, you
only need a ~7% price decline to be underwater.

#### Scenario: -20% crash at year 3, linear recovery to original price by year 10

More realistic: crash, then gradual recovery (Castellón took ~7.5 years to trough).

| Year | Flat value | Balance  | Net proceeds | Total sunk | **Net loss** |
| ---: | ---------- | -------- | ------------ | ---------- | ------------ |
|    3 | €200,000   | €224,434 | −€38,923     | €90,995    | −€129,918    |
|    5 | €214,286   | €214,813 | −€15,538     | €125,192   | −€140,730    |
|    7 | €228,571   | €204,391 | €8,664       | €159,388   | −€150,724    |
|   10 | €250,000   | €187,112 | €46,646      | €210,683   | −€164,037    |

Even after full price recovery (year 10 = back to €250K), the net loss is **€164K** because
of all the sunk costs accumulated over the decade. Negative equity persists until year 6–7.

**This is the scenario the buyer must be comfortable surviving.** It's not a theoretical worst case — it happened in
Castellón from 2007 to 2015.
