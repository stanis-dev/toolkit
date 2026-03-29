# Buy vs Rent & Invest: Analysis

---

## Parameters

- **Location:** Spain, Comunitat Valenciana, Castellón — coastal flats
- **Target flat prices:** €250,000 and €200,000
- **Buyer age:** 36 (age ~38–39 at purchase after saving period, age **68–69** at end of mortgage)
- **Down payment:** 5% of flat value via **IVF guarantee programme** (95% LTV mortgage)
  - Scheme: Institut Valencià de Finances "Programa de Garantías para la compra de vivienda"
  - IVF provides a guarantee on the tranche above 80% LTV, enabling banks to lend up to 95–100%
  - Eligibility: age ≤45, 2yr continuous residency in Comunitat Valenciana, first home, habitual/permanent residence,
    purchase price ≤€311,000 (excl. taxes). No cost to buyer.
  - 14 collaborating banks confirmed. Major nationals: **CaixaBank, Santander, Cajamar, Abanca**. Plus 10 regional
    Valencian entities (Caixa Ontinyent, Caixa Popular, Caixa Rural Benicarló, Caixa Rural de l'Alcúdia, Caixa Rural
    d'Algemesí, and others). List open for new entrants.
  - No standard IVF rate — each bank sets its own pricing. Guarantee is free to borrower.
- **Mortgage type:** Fixed rate
- **Mortgage term:** 30 years (25-year term not viable)
- **Modelling rates (95% LTV, 30yr fixed):** 4.0% TIN (baseline) / 4.5% TIN (prudent)
- **Evaluation horizon:** ~31–33 years total (saving period + 30yr mortgage). See Part 4 for exact timelines per
  scenario.
- **Investment vehicle (rent scenario):** Global equity index — fondo de inversión preferred over ETF for Spanish tax
  residents (traspaso advantage). VWCE/MSCI World as performance benchmark.
- **Return scenarios (nominal EUR):** 4% pessimistic / 6% baseline / 8% optimistic
  - Anchored to MSCI World (EUR, net) since 2000: 6.32% annualised
  - All figures nominal. To approximate real returns, subtract ~2–2.5% for inflation.
- **Monthly rent (rent scenario):** €500/month starting point (validated: ~50–60m² at Castellón coast rates)
- **Rent inflation scenarios:** 1.5% low / 3.0% baseline / 6.0% high (average annual over 30yr)
  - HICP actual rents in Spain roughly doubled over 30 years (1996–2025), ~2.5%/yr compound. Baseline 3% accounts for
    periodic market resets on top of in-contract indexation.
- **Monthly investment (rent scenario):** €1,000/month and €1,500/month (two sub-scenarios)

---

## Part 1 — Property Price Projections (Castellón Coast)

**Goal:** Establish a reasonable expectation of how flat prices in this area might evolve over ~30–33 years.

### Historical price data (researched)

#### Official appraisal €/m² backbone (1995 Q1 – 2025 Q4)

| Period                | Spain €/m²       | Comunitat Valenciana €/m² | Castellón province €/m² |
| --------------------- | ---------------- | ------------------------- | ----------------------- |
| 1995 Q1               | ~642             | ~562                      | ~448                    |
| 2005 Q4 (late-bubble) | ~1,817           | ~1,523                    | ~1,554                  |
| Bubble peak           | ~2,101 (2008 Q1) | ~1,698 (2008 Q2)          | ~1,761 (2007 Q3)        |
| Post-crash trough     | ~1,456 (2014 Q3) | ~1,115 (2014 Q1)          | ~1,022 (2015 Q1)        |
| 2019 Q4 (pre-COVID)   | ~1,653           | ~1,232                    | ~1,067                  |
| 2025 Q4 (latest)      | ~2,230           | ~1,806                    | ~1,367                  |

Castellón's bubble peak came earlier (2007 Q3), crash was **deeper (-42%)** and **longer (7.5 years)** than Spain
overall (-31%, 6.5 yrs). Current price still below peak in this series.

#### Compound annual growth rates (official appraisal €/m²)

| Geography            | 10yr CAGR | 20yr CAGR  | Trough → 2025 Q4 | Full 1995–2025 |
| -------------------- | --------- | ---------- | ---------------- | -------------- |
| Spain                | ~4.1%     | ~1.0%      | ~3.9%            | ~4.0%          |
| Comunitat Valenciana | ~4.6%     | ~1.0%      | ~4.2%            | ~4.4%          |
| **Castellón**        | **~2.5%** | **~−0.6%** | **~2.7%**        | ~3.7%          |

The 20-year CAGR is **negative** for Castellón because the window starts mid-bubble (2005) and the province still hasn't
fully recovered. Multi-year stagnation is not hypothetical here.

#### Coastal municipality asking prices (idealista, Feb 2026)

| Town             | Asking €/m² | 10yr CAGR (asking) | Notes                |
| ---------------- | ----------- | ------------------ | -------------------- |
| Benicàssim       | €2,796      | ~4.9%              | Premium coastal town |
| Peñíscola        | €2,204      | ~4.1%              |                      |
| Oropesa del Mar  | €2,004      | ~3.2%              |                      |
| Vinaròs          | €1,683      | ~3.2%              |                      |
| Province average | €1,526      | ~3.6%              |                      |

Caveats: asking prices (not transactions), idealista methodology change since March 2023, some small-market gaps in
early years. Prime coastal towns outpace provincial average.

#### Demand drivers and structural context

- **Domestic-heavy demand:** Castellón coastal tourism is far more domestic than Alicante (Costa Blanca). In 2023
  tourist-apartment stays: Castellón had 424K non-resident nights vs Alicante's 5.9M. Lower prices, but less dependence
  on single-source foreign demand shocks.
- **Foreign buyers:** ~21% of purchases in Castellón (2024 notarial data). Broad European mix (Romania, France
  prominent), not dominated by UK/Nordic buyers like Costa Blanca.
- **Infrastructure:** AP-7 toll removal (Jan 2020) improved coastal accessibility significantly. Castellón airport
  reached ~304K passengers in 2025 with expanding routes.
- **Supply:** Banco de España names Madrid, Barcelona, Valencia, Alicante, Málaga as supply- bottleneck provinces —
  **Castellón is not on that list.** Macro environment is supportive but assumptions should be more conservative than
  for the hotspot provinces.

### Scenarios (nominal annual appreciation)

| Scenario    | Rate     | Rationale                                                          |
| ----------- | -------- | ------------------------------------------------------------------ |
| Pessimistic | **1.0%** | Long stagnations historically plausible in Castellón. The 20yr     |
|             |          | CAGR was negative. Accounts for demand softness, demographic       |
|             |          | headwinds, or climate/regulatory risk repricing.                   |
| Baseline    | **2.5%** | Matches Castellón's official last-decade CAGR exactly. Consistent  |
|             |          | with trough-to-now recovery rate (~2.7%).                          |
| Optimistic  | **4.0%** | Close to Spain's long-run CAGR (~4.0%). Assumes supply constraints |
|             |          | persist, accessibility improvements compound (AP-7, airport), and  |
|             |          | coastal lifestyle demand stays strong.                             |

**Reality check:** at ~2% inflation, 2.5% nominal is only **~0.5% real appreciation per year**. The baseline is modest —
not a growth story, more of a "roughly keeps pace with inflation plus a bit."

### Projected flat values (pure price appreciation, no costs/income)

| Scenario         | Starting price | Year 10  | Year 20  | Year 30  |
| ---------------- | -------------- | -------- | -------- | -------- |
| Pessimistic (1%) | €250,000       | €276,156 | €305,048 | €336,962 |
| Pessimistic (1%) | €200,000       | €220,924 | €244,038 | €269,570 |
| Baseline (2.5%)  | €250,000       | €320,021 | €409,654 | €524,392 |
| Baseline (2.5%)  | €200,000       | €256,017 | €327,723 | €419,514 |
| Optimistic (4%)  | €250,000       | €370,061 | €547,781 | €810,849 |
| Optimistic (4%)  | €200,000       | €296,049 | €438,225 | €648,680 |

### Risk factors that could materially shift these projections

**Castellón's crash history:** The last crash was **-42% over 7.5 years** (2007 Q3 to 2015 Q1). This was deeper and
longer than Spain overall. A repeat of any similar magnitude during the mortgage period would devastate the buy
scenario, especially in the early years when equity is minimal. Connects directly to the 2D forced-sale risk.

**Tourist rental regulation (VUT):** Decree-law 9/2024 tightened rules for viviendas de uso turístico in the Valencian
Community, with stronger municipal powers to limit use and active registry enforcement/cancellations. If VUT income is
part of any coastal flat's value proposition, this reduces the "investor bid" portion of demand and could flatten
prices.

**Climate and flood risk:** The Valencian Community maintains PATRICOVA flood-risk mapping. IPCC AR6 projects
Mediterranean sea level rise of ~0.3–1.1m by 2100 depending on emissions pathway. For a coastal flat with a 30-year
horizon, this means potential increases in insurance costs, building maintenance, and eventual market repricing of
flood-exposed locations. **Any specific property should be checked against PATRICOVA and SNCZI flood mapping.**

**Supply not constrained in Castellón:** Banco de España's 2024 report names Madrid, Barcelona, Valencia, Alicante, and
Málaga as the supply-bottleneck provinces. Castellón is not on this list. The macro environment supports prices, but
this province should not be modelled with the same supply-scarcity premium as the named hotspots.

**Demand composition:** Castellón's coastal demand is more domestic than Costa Blanca. This stabilises prices (less
exposure to single-country foreign demand shifts) but may cap upside compared to internationally popular coasts where
global demand competes.

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

## Part 3 — Rent & Invest Scenario

**Goal:** Model the alternative — keep renting, invest the difference, and see where we land at the end of the total
timeline (~31–33 years, matching the buyer's saving + mortgage period).

### Assumptions

- Monthly rent: **€500** starting point — validated against Feb 2026 asking rents:
  - Castellón coast asking rents (€/m²/month): Vinaròs €8.4, Oropesa €9.3, Benicàssim €10.5
  - €500/month corresponds to **~50–60m²** at these rates — consistent with a modest 1–2 bed flat
  - Castellón is the **cheapest of the three Valencian provinces** in asking rents (vs Alicante €12.3/m², Valencia
    €14.0/m²), supporting its use as a lower-cost rent baseline
  - **Risk flag:** current asking rents are rising fast — 8–13% YoY across Castellón coast municipalities (Feb 2026).
    This is asking-price inflation, not in-contract increases.
- Monthly investment into a global index fund
- Investment is **monthly DCA** (dollar-cost averaging), not a lump sum
- This means earlier contributions compound longer, later contributions compound less
- **Initial lump sum:** the cash that would have been spent on the purchase is instead invested from day one. This is
  the upfront cash from Part 2A:
  - If comparing against the €250K flat: **~€39,700** lump sum at month 0
  - If comparing against the €200K flat: **~€32,100** lump sum at month 0
  - This lump sum compounds for the full 30 years and is a significant contributor to the rent scenario's final
    portfolio value

### Rent evolution — LAU protections and real dynamics (researched)

Spanish rental law (LAU) creates two distinct rent dynamics that must not be conflated:

#### Within a contract (in-contract updates)

- Rent can only be updated **once per year**, on the anniversary, and **only if the contract explicitly provides for
  it**. If there is no update clause, **no update applies** (Art. 18 LAU).
- When updates are allowed, they are now limited by a new **INE reference index** designed to prevent "disproportionate"
  increases (mandated by the 2023 Housing Law, to be defined by end-2024). Previous emergency caps (2022–2024) limited
  updates to 2–3% during the CPI spike.
- In practice, in-contract rent evolution is **modest and index-like**, not market-like.

#### Between contracts (market resets)

- When a contract ends and you must sign a new one (or move), rent resets to **market rate**.
- "Stressed area" (zona tensionada) caps from the 2023 Housing Law **do not apply in Castellón** — no Valencian
  Community municipalities have been declared as stressed zones (as of BOE reporting through early 2026). Market resets
  can therefore be significant.

#### Contract stability under LAU

| Landlord type          | Mandatory minimum | Tacit renewal | Total potential stay |
| ---------------------- | ----------------- | ------------- | -------------------- |
| Individual person      | **5 years**       | + up to 3yr   | **~8 years**         |
| Legal entity (company) | **7 years**       | + up to 3yr   | **~10 years**        |

- Landlord must give **4 months' notice** to not renew; tenant must give **2 months'**.
- **Sale of the property** does not break the lease during the protected period — the buyer is subrogated into the
  landlord's rights for the first 5/7 years (Art. 14 LAU).
- After protected periods, practical risk is expiry/non-renewal rather than immediate eviction.

#### Coastal-specific risk

On the Castellón coast, landlords may prefer **seasonal contracts** (_arrendamientos por temporada_), which LAU
classifies as "use other than housing" — these do **not** carry the same multi-year stability protections. Securing a
true _vivienda habitual_ lease is critical.

#### How rent actually evolves over 30 years

Rent doesn't rise smoothly. The realistic pattern is a **step function**:

- **Years 1–5/8:** stable or near-stable (in-contract, index-linked increases only)
- **Reset event:** contract ends → new contract at market rate (potentially large jump)
- **Years 6–13:** stable again from the new base
- **Repeat** at each contract boundary

The long-run average depends on how often you face reset events and how hot the market is when they happen. HICP actual
rents in Spain doubled over 30 years (~2.5%/yr compound), but current asking rents in Castellón coast are rising 8–13%
YoY — resets during hot markets hurt.

### Rent inflation scenarios (30-year projections from €500/month)

| Scenario            | Avg annual increase |  Year 10 |  Year 20 |    Year 30 | Rationale                                        |
| ------------------- | ------------------: | -------: | -------: | ---------: | ------------------------------------------------ |
| Low (1.5%)          |                1.5% |     €580 |     €673 |       €782 | Long stays, minimal repricing, tenant-favourable |
| **Baseline (3.0%)** |            **3.0%** | **€672** | **€903** | **€1,214** | Blended: modest indexation + periodic resets     |
| High (6.0%)         |                6.0% |     €895 |   €1,604 |     €2,872 | Tight supply, frequent forced moves              |

At the baseline, rent roughly **doubles** every ~23 years. At the high scenario, it quintuples.

### Sub-scenarios

| Scenario | Monthly investment | Monthly rent | Total monthly outflow |
| -------- | ------------------ | ------------ | --------------------- |
| A        | €1,000             | €500         | €1,500                |
| B        | €1,500             | €500         | €2,000                |

### Historical returns (researched)

#### FTSE All-World / Vanguard VWCE

- 10yr annualised (USD, total return): **12.73%** (Vanguard factsheet, Jan 2026)
- No 20yr or 30yr EUR data available from the provider
- VWCE tracks the FTSE All-World Index (developed + emerging, large/mid-cap)

#### MSCI World (EUR, net total return) — best EUR anchor

- 10yr annualised: **12.34%**
- Since 29 Dec 2000 annualised: **6.32%** (spans dot-com crash, GFC, Euro crisis, COVID, rate hikes)
- Max drawdown since 2000: **53.60%** (May 2001 to March 2009)
- Calendar year dispersion: 2021 +31%, 2022 −12.8%, 2023 +19.6%, 2024 +26.6%, 2025 +6.8%

#### S&P 500 (USD, total return with dividends reinvested) — long-history comparator

- 10yr: ~13.5%, 20yr: ~10.2%, 30yr: ~9.6%, since 1926: ~10.4%
- Rolling best/worst 10yr: best ~18.6% (1990s), worst ~−1.4% (1999–2008, modern era)
- Rolling best/worst 20yr: best ~16.8% (1979–98), worst ~2.8% (1928–47)

#### Return scenarios for modelling (nominal EUR)

| Scenario    | Annual return | Rationale                                                  |
| ----------- | ------------- | ---------------------------------------------------------- |
| Pessimistic | **4%**        | Below MSCI World EUR since 2000 (6.32%). Accounts for weak |
|             |               | decades, valuation headwinds, EUR/USD uncertainty.         |
| Baseline    | **6%**        | Consistent with MSCI World EUR since 2000. Leaves room for |
|             |               | tracking difference and product costs.                     |
| Optimistic  | **8%**        | Below recent 10yr (12.34%) but above multi-decade average. |
|             |               | Historically plausible, not guaranteed.                    |

#### Fees and their 30-year impact

- **VWCE TER:** 0.19% (cut from 0.22% — Vanguard, FT report)
- **MyInvestor fondos indexados:** max 0.59% TER overall; some as low as 0.10% (iShares Developed World via BlackRock
  partnership)
- **Openbank:** no custody, subscription, redemption, or transfer fees for funds
- **Fee drag over 30 years** (at 7% gross, €1K/mo):
  - 0.22% TER → ~€1.12M final value
  - 0.50% TER → ~€1.07M final value
  - **Difference: ~€56K** — fees compound against an ever-growing base
  - At €1.5K/mo the gap widens to ~€84K

### Vehicle decision: ETF vs fondo de inversión

The most important Spain-specific implementation decision. Both track the same indices, but they are taxed very
differently.

**Fondos de inversión (mutual funds):**

- Transfers between qualifying fondos (_traspasos_) are **tax-deferred** — no capital gains event when switching
  providers, rebalancing, or de-risking. Tax is paid only at final redemption.
- Higher TER than the cheapest ETFs (MyInvestor: max 0.59%, some at 0.10%)
- Best platforms: MyInvestor (no custody/transfer fees, Vanguard/iShares/Fidelity/Amundi funds), Openbank (no
  custody/subscription/redemption fees)

**ETFs (e.g., VWCE):**

- Lower TER (VWCE at 0.19%)
- But every sale is a **taxable event** — no traspaso. Switching providers, rebalancing between regions, or de-risking
  to bonds all trigger capital gains tax.
- FIFO cost basis means oldest (most appreciated) lots are sold first

**Practical guidance:**

- For pure buy-and-hold of a single global fund over 30 years, the difference during accumulation is small (ETF wins
  slightly on fees, fondo wins on flexibility)
- For any rebalancing, de-risking, or provider switching over 30 years — which is likely over such a long horizon —
  **fondos are structurally better** for a Spanish tax resident
- **Accumulating** vehicles preferred over distributing (dividends reinvested internally, tax deferred until sale)

### Spanish tax framework (for the rent-and-invest scenario)

#### Capital gains tax (rendimientos del ahorro) — 2025+ rates

| Gain bracket      | Combined rate (state + autonomous) |
| ----------------- | ---------------------------------- |
| First €6,000      | 19%                                |
| €6,000–€50,000    | 21%                                |
| €50,000–€200,000  | 23%                                |
| €200,000–€300,000 | 27%                                |
| Above €300,000    | 30%                                |

Updated via Ley 7/2024. Top bracket increased to 30% from 1 January 2025.

#### Cost basis and FIFO

Spain uses **FIFO** (first in, first out) for homogeneous securities. In a DCA portfolio, this means when you sell, the
**oldest, most appreciated lots are sold first** — maximising the taxable gain per euro sold. Planning implication:
**spread sales across multiple tax years** to keep more gains in lower brackets.

#### Wealth tax (Impuesto sobre el Patrimonio) — Valencian Community

- **Mínimo exento:** €1,000,000 (net taxable wealth exempt)
- Progressive rates from **0.25%** to **3.5%** (above ~€10.7M)
- Becomes relevant if portfolio + other assets exceed €1M — plausible at the optimistic return scenario over 30 years

#### Solidarity tax (Impuesto de Solidaridad)

- State-level complementary wealth tax (Ley 38/2022)
- First **€3,000,000** at 0%. Then 1.7% / 2.1% / 3.5% progressive
- Deducts wealth tax already paid — avoids double taxation
- Only relevant at very high net worth levels

#### Exit scenario: selling after 30 years

If liquidating the full portfolio:

- Gain = market value − total contributions (cost basis)
- Apply progressive brackets above to the total gain
- Effective rate depends on gain size — a ~€600K gain would average ~24–25% effective rate
- **Key lever:** spreading sales across 3–5 tax years significantly reduces the effective rate

### Inflation context

- **ECB target:** 2% symmetric (medium-term, 2021 strategy review)
- **Spain long-run:** ~2–3% working range for planning
- **All return scenarios above are NOMINAL.** To approximate real returns, subtract ~2–2.5%.
  - 4% nominal → ~1.5–2% real (pessimistic)
  - 6% nominal → ~3.5–4% real (baseline)
  - 8% nominal → ~5.5–6% real (optimistic)

### Output — Investment portfolio projections

#### Invest path

- Current savings: **€15,000**
- Emergency buffer kept in bank: **€8,000**
- Initial lump sum invested at month 0: **€7,000** (€15K − €8K)
- Monthly DCA from month 1: **€1,000** or **€1,500** (after rent)
- Monthly rent: €500 (inflating 3%/yr)
- Total monthly outflow: €1,500 (at €1K DCA) or €2,000 (at €1.5K DCA)

#### €1,000/mo DCA (€7,000 lump at month 0)

| Return |                Year 10 |                Year 20 |                  Year 32.1 |                  Year 32.6 |
| ------ | ---------------------: | ---------------------: | -------------------------: | -------------------------: |
| 4%     | €157,058 (AT €150,866) | €379,180 (AT €349,898) |     €794,259 (AT €691,701) |     €816,038 (AT €708,747) |
| 6%     | €175,009 (AT €165,047) | €475,889 (AT €423,209) |   €1,172,202 (AT €956,262) |   €1,212,930 (AT €986,571) |
| 8%     | €195,237 (AT €180,662) | €601,626 (AT €513,358) | €1,763,221 (AT €1,369,975) | €1,838,491 (AT €1,424,463) |

Year 32.1 = endpoint when comparing vs €200K flat. Year 32.6 = vs €250K flat. AT = after Spanish CGT.

**After-tax detail — vs €250K flat (32.6yr):**

| Return |  Portfolio | Contributions |       Gain |      Tax | Eff. rate |      After-tax |
| ------ | ---------: | ------------: | ---------: | -------: | --------: | -------------: |
| 4%     |   €816,038 |      €398,000 |   €418,038 | €107,291 |     25.7% |   **€708,747** |
| 6%     | €1,212,930 |      €398,000 |   €814,930 | €226,359 |     27.8% |   **€986,571** |
| 8%     | €1,838,491 |      €398,000 | €1,440,491 | €414,027 |     28.7% | **€1,424,463** |

**After-tax detail — vs €200K flat (32.1yr):**

| Return |  Portfolio | Contributions |       Gain |      Tax | Eff. rate |      After-tax |
| ------ | ---------: | ------------: | ---------: | -------: | --------: | -------------: |
| 4%     |   €794,259 |      €392,000 |   €402,259 | €102,558 |     25.5% |   **€691,701** |
| 6%     | €1,172,202 |      €392,000 |   €780,202 | €215,941 |     27.7% |   **€956,262** |
| 8%     | €1,763,221 |      €392,000 | €1,371,221 | €393,246 |     28.7% | **€1,369,975** |

#### €1,500/mo DCA (€7,000 lump at month 0)

| Return |                Year 10 |                Year 20 |                  Year 31.4 |                  Year 31.8 |
| ------ | ---------------------: | ---------------------: | -------------------------: | -------------------------: |
| 4%     | €230,406 (AT €221,410) | €561,100 (AT €517,577) |   €1,136,815 (AT €985,641) | €1,157,805 (AT €1,002,133) |
| 6%     | €256,246 (AT €241,439) | €702,608 (AT €620,046) | €1,657,737 (AT €1,350,286) | €1,696,294 (AT €1,379,076) |
| 8%     | €285,299 (AT €263,810) | €886,125 (AT €748,508) | €2,461,619 (AT €1,913,003) | €2,531,643 (AT €1,963,820) |

Year 31.4 = endpoint when comparing vs €200K flat. Year 31.8 = vs €250K flat.

**After-tax detail — vs €250K flat (31.8yr):**

| Return |  Portfolio | Contributions |       Gain |      Tax | Eff. rate |      After-tax |
| ------ | ---------: | ------------: | ---------: | -------: | --------: | -------------: |
| 4%     | €1,157,805 |      €578,500 |   €579,305 | €155,671 |     26.9% | **€1,002,133** |
| 6%     | €1,696,294 |      €578,500 | €1,117,794 | €317,218 |     28.4% | **€1,379,076** |
| 8%     | €2,531,643 |      €578,500 | €1,953,143 | €567,823 |     29.1% | **€1,963,820** |

**After-tax detail — vs €200K flat (31.4yr):**

| Return |  Portfolio | Contributions |       Gain |      Tax | Eff. rate |      After-tax |
| ------ | ---------: | ------------: | ---------: | -------: | --------: | -------------: |
| 4%     | €1,136,815 |      €572,500 |   €564,315 | €151,175 |     26.8% |   **€985,641** |
| 6%     | €1,657,737 |      €572,500 | €1,085,237 | €307,451 |     28.3% | **€1,350,286** |
| 8%     | €2,461,619 |      €572,500 | €1,889,119 | €548,616 |     29.0% | **€1,913,003** |

Tax ranges from ~26% to ~29% effective rate at full liquidation. At the baseline 6% return with €1K/mo DCA, tax is
**€226K** at the €250K endpoint — roughly 19% of portfolio value. Spreading sales over 3–5 tax years would reduce the
effective rate significantly.

---

## Part 4 — Side-by-Side Comparison

### Scenario definition

Both paths start from the same position, operate on the same total monthly budget, and are measured over the **same
total duration** from today.

**Shared starting position:**

- Current savings: **€15,000**
- Monthly capacity after rent: **€1,000** or **€1,500**
- Current rent: **€500/mo** (inflating 3%/yr)
- Total monthly outflow: **€1,500** or **€2,000**

**Comparison timeline:** Both paths run from month 0 (today) to the month the buyer's mortgage is fully paid off. The
buyer's total timeline = saving period + 30 years of mortgage. The investor gets the **same total duration** of
compounding, including the extra months the buyer spent saving.

| Scenario          | Saving period | + Mortgage | = Total from today |
| ----------------- | :-----------: | :--------: | :----------------: |
| €250K at €1K/mo   |  ~32 months   |  30 years  |  **~32.7 years**   |
| €250K at €1.5K/mo |  ~21 months   |  30 years  |  **~31.75 years**  |
| €200K at €1K/mo   |  ~25 months   |  30 years  |  **~32.1 years**   |
| €200K at €1.5K/mo |  ~17 months   |  30 years  |  **~31.4 years**   |

Intermediate checkpoints at year 10 and 20 (from today) also reflect this: the buyer is that many years into their
combined saving + mortgage timeline, NOT that many years into the mortgage itself.

#### Invest path

- Month 0: invest **€7,000** (€15K − €8K emergency buffer) into global index fund
- Month 1+: pay €500 rent + DCA €1K or €1.5K/mo into index fund
- Ongoing: rent inflates 3%/yr, monthly DCA stays fixed
- Runs for the **full total duration** (31.4–32.7 years depending on scenario)

#### Buy path (three sequential phases)

**Phase 1 — Save for purchase (both paths have identical outflow during this phase):**

- Save €1K or €1.5K/mo at **2%/yr in bank** (risk-free), continue paying €500/mo rent
- Target: flat upfront costs + **€10K safety buffer** retained at purchase
  - €250K flat (ITP 9%): €37,200 + €10,000 = **€47,200 total to save**
  - €200K flat (ITP 9%): €30,100 + €10,000 = **€40,100 total to save**
- During this phase the investor's money is compounding in the market while the buyer's earns 2% in the bank — this is
  where the investor's head start builds

**Phase 2 — Purchase + rebuild buffer:**

- All savings above €10K go to down payment + costs. Mortgage begins. Rent stops.
- Spare capacity = total budget − mortgage − ongoing costs (inflating 2%/yr)
- Spare goes to **rebuilding emergency buffer to €20K** at 2% in bank — NOT market
- Already have €10K at purchase, need €10K more

**Phase 3 — Parallel market investing (if/when reached):**

- Once buffer hits €20K, spare capacity goes to index fund
- Monthly investable = total budget − housing cost (shrinks as costs inflate at 2%/yr)

#### Cashflow model and known asymmetry

The invest path assumes a **fixed nominal DCA** (€1K or €1.5K/mo) for the full duration,
with rent paid separately and rising at 3%/yr. This means the investor's total outflow rises
over time — implicitly assuming income grows enough to cover increasing rent while
maintaining the same investment commitment.

The buy path assumes a **fixed nominal budget** (€1.5K or €2K/mo) from which mortgage +
costs are paid. As ongoing costs inflate at 2%/yr, spare capacity shrinks (and eventually
turns negative in the €250K/€1K scenario).

This creates an asymmetry: the investor implicitly has rising income capacity; the buyer
does not. Two considerations make this acceptable as a modelling choice:

1. **Over 30+ years, nominal income growth is realistic.** If inflation averages 2–3%,
   nominal salaries typically rise — a fixed nominal DCA of €1K is progressively easier to
   maintain. The investor's total outflow rises at roughly the rate of rent inflation (~3%),
   which is within plausible wage growth.
2. **The buyer's fixed mortgage is itself an inflation hedge.** The €1,134/mo payment becomes
   lighter in real terms every year. This is a genuine structural advantage of buying that
   partially offsets the investor's rising capacity — the model captures this by keeping the
   mortgage payment fixed while inflating everything else.

Neither approach is perfectly symmetric. An alternative model (equal-outflow, where DCA
decreases as rent rises) is explored in section 6.3 for the "same flat" framing and produces
different win counts. The fixed-DCA model used here is appropriate for the "same person"
framing, where the question is "should I keep my current cheap rent and invest, or upgrade
to buying?"

### Computed: Buy path timelines

| Scenario           | Save target |       Phase 1 | Purchase age |         Phase 2 |      Phase 3 start |  Total timeline | End age |
| ------------------ | ----------: | ------------: | -----------: | --------------: | -----------------: | --------------: | ------: |
| €250K at €1,000/mo |     €47,200 | 31 mo (2.6yr) |         38.6 | 166 mo (13.8yr) | month 197 (16.4yr) | 391 mo (32.6yr) |    68.6 |
| €250K at €1,500/mo |     €47,200 | 21 mo (1.8yr) |         37.8 |   17 mo (1.4yr) |   month 38 (3.2yr) | 381 mo (31.8yr) |    67.8 |
| €200K at €1,000/mo |     €40,100 | 25 mo (2.1yr) |         38.1 |   28 mo (2.3yr) |   month 53 (4.4yr) | 385 mo (32.1yr) |    68.1 |
| €200K at €1,500/mo |     €40,100 | 17 mo (1.4yr) |         37.4 |   11 mo (0.9yr) |   month 28 (2.3yr) | 377 mo (31.4yr) |    67.4 |

The €250K/€1K scenario is extremely tight: initial spare is only €75/mo, Phase 2 takes **13.8 years**, and by mortgage
year 15 the buyer faces a housing cost deficit (costs exceed budget). Phase 3 barely starts and contributes almost
nothing to parallel investing.

The €250K/€1.5K and €200K scenarios are more workable: Phase 2 completes in 1–2 years, leaving 28+ years for Phase 3
parallel investing with €340–800/mo of declining spare.

#### Spare capacity trajectory (budget − housing cost)

| Mortgage year | €250K/€1K | €250K/€1.5K | €200K/€1K | €200K/€1.5K |
| ------------: | --------: | ----------: | --------: | ----------: |
|             1 |       €69 |        €569 |      €296 |        €796 |
|             5 |       €45 |        €545 |      €272 |        €772 |
|            10 |       €11 |        €511 |      €238 |        €738 |
|            15 |  **−€26** |        €474 |      €201 |        €701 |
|            20 |  **−€66** |        €434 |      €161 |        €661 |
|            25 | **−€111** |        €389 |      €116 |        €616 |
|            30 | **−€161** |        €339 |       €66 |        €566 |

The €250K/€1K buyer enters deficit by year 12–13 of the mortgage — housing costs exceed the €1,500 budget. From that
point, the deficit drains the buffer. By year 30 the buffer has shrunk from ~€20K to ~€9K and the parallel portfolio is
effectively €0. This scenario is barely viable financially.

### Computed: End-of-timeline comparison (after-tax)

Buyer net worth = flat equity + buffer + parallel portfolio (after-tax). Investor net worth = portfolio (after-tax).
Both at the same total timeline endpoint.

#### €250K flat at 4.0%, €1,000/mo capacity — End (32.6yr)

Buyer: mortgage done, but parallel portfolio ≈ €0 (Phase 3 started too late, then deficit). Buffer eroded to ~€9K. Buyer
net worth = flat value + ~€9K.

|                      | Inv 4% (€709K AT) | Inv 6% (€987K AT) | Inv 8% (€1,424K AT) |
| -------------------- | ----------------- | ----------------- | ------------------- |
| **Buy 1.0%** (€337K) | RENT +€363K       | RENT +€641K       | RENT +€1,079K       |
| **Buy 2.5%** (€524K) | RENT +€175K       | RENT +€453K       | RENT +€891K         |
| **Buy 4.0%** (€811K) | **BUY +€111K**    | RENT +€167K       | RENT +€605K         |

**Buy wins: 1/9.** The €250K/€1K buyer has almost zero parallel portfolio to offset the renter's advantage. Only the
optimistic-property/pessimistic-investment corner wins.

#### €250K flat at 4.0%, €1,500/mo capacity — End (31.8yr)

Buyer: parallel portfolio ~€371K (AT, at 6%). Buffer ~€35K. Much healthier position.

|                      | Inv 4% (€1,002K AT) | Inv 6% (€1,379K AT) | Inv 8% (€1,964K AT) |
| -------------------- | ------------------- | ------------------- | ------------------- |
| **Buy 1.0%** (€337K) | RENT +€356K         | RENT +€636K         | RENT +€1,085K       |
| **Buy 2.5%** (€524K) | RENT +€168K         | RENT +€448K         | RENT +€898K         |
| **Buy 4.0%** (€811K) | **BUY +€118K**      | RENT +€162K         | RENT +€611K         |

**Buy wins: 1/9.** Despite the buyer's much larger parallel portfolio, the investor's higher DCA over the full period
still dominates. Same pattern: only the extreme corner wins.

#### €200K flat at 4.0%, €1,000/mo capacity — End (32.1yr)

Buyer: parallel portfolio ~€152K (AT, at 6%). Buffer ~€35K.

|                      | Inv 4% (€692K AT) | Inv 6% (€956K AT) | Inv 8% (€1,370K AT) |
| -------------------- | ----------------- | ----------------- | ------------------- |
| **Buy 1.0%** (€270K) | RENT +€277K       | RENT +€500K       | RENT +€853K         |
| **Buy 2.5%** (€420K) | RENT +€127K       | RENT +€350K       | RENT +€703K         |
| **Buy 4.0%** (€649K) | **BUY +€102K**    | RENT +€121K       | RENT +€474K         |

**Buy wins: 1/9.**

#### €200K flat at 4.0%, €1,500/mo capacity — End (31.4yr)

Buyer: parallel portfolio ~€553K (AT, at 6%). Buffer ~€36K. Strongest buy case.

|                      | Inv 4% (€986K AT) | Inv 6% (€1,350K AT) | Inv 8% (€1,913K AT) |
| -------------------- | ----------------- | ------------------- | ------------------- |
| **Buy 1.0%** (€270K) | RENT +€267K       | RENT +€492K         | RENT +€849K         |
| **Buy 2.5%** (€420K) | RENT +€117K       | RENT +€342K         | RENT +€699K         |
| **Buy 4.0%** (€649K) | **BUY +€112K**    | RENT +€113K         | RENT +€470K         |

**Buy wins: 1/9.**

#### Summary — buy wins across all configurations (end of timeline)

| Configuration      | Buy wins |
| ------------------ | :------: |
| €250K at €1,000/mo | **1/9**  |
| €250K at €1,500/mo | **1/9**  |
| €200K at €1,000/mo | **1/9**  |
| €200K at €1,500/mo | **1/9**  |

Buying wins only at optimistic property growth (4%) + pessimistic investment return (4%) across all four configurations.
This is consistent with the old theoretical model but now computed from the actual financial position.

### Computed: Year 10 and Year 20 intermediate comparisons

#### Year 10 from today — all four scenarios

At year 10, the buyer is 7–8 years into the mortgage. In the €250K/€1K scenario the buyer is still in Phase 2 (buffer
rebuild) with zero parallel portfolio.

| Scenario              | Buy 1%     | Buy 2.5%   | Buy 4%     | Notes                           |
| --------------------- | ---------- | ---------- | ---------- | ------------------------------- |
| €250K/€1K vs Inv 6%   | RENT +€81K | RENT +€50K | RENT +€16K | Buyer has €0 parallel portfolio |
| €250K/€1.5K vs Inv 6% | RENT +€91K | RENT +€56K | RENT +€17K | Buyer has ~€54K parallel (AT)   |
| €200K/€1K vs Inv 6%   | RENT +€65K | RENT +€38K | RENT +€9K  | Buyer has ~€21K parallel (AT)   |
| €200K/€1.5K vs Inv 6% | RENT +€71K | RENT +€41K | RENT +€8K  | Buyer has ~€86K parallel (AT)   |

**Renting wins in all scenarios at year 10** (at baseline 6% return). Only at 4% investment + 4% property does buying
break even. This is expected — early years heavily favour renting due to interest-heavy mortgage payments and
transaction cost sunk.

#### Year 20 from today — all four scenarios (at 6% investment return)

| Scenario    | Buy 1%      | Buy 2.5%    | Buy 4%     |
| ----------- | ----------- | ----------- | ---------- |
| €250K/€1K   | RENT +€240K | RENT +€153K | RENT +€42K |
| €250K/€1.5K | RENT +€257K | RENT +€164K | RENT +€45K |
| €200K/€1K   | RENT +€193K | RENT +€121K | RENT +€28K |
| €200K/€1.5K | RENT +€200K | RENT +€124K | RENT +€26K |

At year 20 with baseline investment returns, renting still wins in every cell. Buying comes closest at optimistic
property growth (gap ~€26–45K).

### Computed: Break-even analysis (end of timeline)

"What annual property growth is needed for buying to match renting + investing?"

| Scenario          | At Inv 4% | At Inv 6% | At Inv 8% |
| ----------------- | --------: | --------: | --------: |
| €250K at €1K/mo   |  **3.5%** |  **4.7%** |  **5.9%** |
| €250K at €1.5K/mo |  **3.5%** |  **4.6%** |  **6.0%** |
| €200K at €1K/mo   |  **3.4%** |  **4.6%** |  **5.9%** |
| €200K at €1.5K/mo |  **3.3%** |  **4.6%** |  **5.9%** |

At the baseline 6% investment return, buying needs **~4.6–4.7%/yr property growth** to break even — above Castellón's
10yr CAGR (2.5%) and above Spain's 30yr CAGR (~4.0%). At the pessimistic 4% investment return, buying needs
**~3.3–3.5%** — within the plausible range but still above Castellón's historical average.

### When does each strategy win?

**Buying wins when** all three of these are true simultaneously:

1. Property appreciates at the **optimistic** end (~4%/yr) — above Castellón's track record
2. Investment returns are at the **pessimistic** end (~4%/yr nominal) — below the MSCI World multi-decade average
3. You hold for the **full 30 years** without being forced to sell early

**Renting + investing wins when** any of these are true:

1. You can achieve baseline investment returns (~6%) — the MSCI World EUR average since 2000
2. Property appreciation is at baseline (~2.5%) or below — Castellón's actual historical rate
3. There is any chance you might need to exit the property in the first 10 years (2D risk)

**The single most important variable remains investment return.** At 6%+ nominal, renting dominates in 8/9 cells. At 4%
investment return, buying becomes competitive if property hits 3.5%+ growth — plausible but above Castellón's average.

The €250K/€1K configuration is barely viable — the buyer runs into budget deficits by year 12
and has essentially zero parallel investment capacity. The €1.5K capacity is necessary for
the buy path to function at the €250K price point.

### Qualitative factors

- **Liquidity:** Renter portfolio is liquid and accessible. Buyer equity is illiquid.
- **Risk concentration:** Buyer holds one flat in one province. Renter holds global index.
- **Forced-sale asymmetry:** Crisis hits buyer hard in first 10 years (2D). Renter has options.
- **Retirement asymmetry:** Quantified in 6.6. Renter portfolio survives 20yr drawdown.
- **Income instability:** Strongly favours renting/investing. See note after 6.8.
- **Lifestyle:** Owning = stability, roots. Renting = flexibility, mobility.

## Part 5 — Sensitivity & What-Ifs

> **Note:** Sensitivity figures use a simplified 30-year model. Directional patterns are consistent with the
> real-scenario results in Part 4; exact figures differ slightly due to the saving period and cost inflation.

### Computed: Rent inflation sensitivity (highest-impact variable for the renter)

The Part 4 baseline uses 3% rent inflation. How does the outcome shift at 1.5% and 6%?

**€250K flat at 4.0%, Year 30 comparison:**

| Rent inflation      | Buy wins (out of 9) | Key shift                                                                |
| ------------------- | ------------------- | ------------------------------------------------------------------------ |
| **1.5%**            | **1/9**             | Renter invests more per month → portfolios larger.                       |
|                     |                     | Same outcome as baseline — only extreme corner wins.                     |
| **3.0%** (baseline) | **1/9**             | As computed in Part 4.                                                   |
| **6.0%**            | **3/9**             | Rent eats deeply into surplus → smaller portfolios.                      |
|                     |                     | Buying now wins at optimistic property + pessimistic _and baseline_ inv. |

At 6% rent inflation, the renter's year-30 portfolio drops sharply:

| Rent inflation | Renter at Inv 4% | Renter at Inv 6% | Renter at Inv 8% |
| -------------- | ---------------- | ---------------- | ---------------- |
| 1.5%           | €701,656         | €1,076,541       | €1,693,028       |
| 3.0%           | €608,250         | €959,290         | €1,542,596       |
| 6.0%           | €433,444         | €729,846         | €1,236,424       |

**Interpretation:** Rent inflation matters, but not enough to flip the conclusion. Even at 6% rent inflation (aggressive
— rents quintupling over 30 years), buying still only wins in 3/9 cells. The reason: even as rent eats into the surplus,
the lump sum + early-year DCA have already been compounding for decades. The rent scenario is front-loaded in its
advantage.

### Computed: Property stagnation (0% for 10 years, then 2.5% for 20 years)

This models a repeat of Castellón's post-2008 experience: a decade of flat or declining prices, followed by a gradual
recovery.

| Year | Flat value (stagnation) | Flat value (baseline 2.5%) | Buyer equity (stagnation) |
| ---- | ----------------------- | -------------------------- | ------------------------- |
| 10   | €250,000                | €320,021                   | €62,888                   |
| 20   | €320,021                | €409,654                   | €208,029                  |
| 30   | €409,654                | €524,392                   | €409,654                  |

At year 30, stagnation equity (€410K) is **€115K less** than the baseline (€524K). Compared to the renter at baseline 3%
rent inflation:

| Stagnation buyer equity (€410K) vs... | Result               |
| ------------------------------------- | -------------------- |
| Renter at Inv 4% (€608K)              | RENT wins by €199K   |
| Renter at Inv 6% (€959K)              | RENT wins by €550K   |
| Renter at Inv 8% (€1,543K)            | RENT wins by €1,133K |

**Interpretation:** A decade of stagnation destroys the buy case entirely. The buyer ends up with the same flat value at
year 30 as the baseline buyer had at year 20. Renting wins in every single cell, even at the pessimistic 4% investment
return.

### Computed: Stepped rent model (realistic contract-cycle pattern)

Instead of smooth 3%/yr, model the actual LAU contract dynamics:

- Years 1–5: €500/mo (no increase — no clause in contract)
- Year 6: +20% market reset → €600/mo
- Years 6–12: 2%/yr indexation → €688/mo by year 12
- Year 13: +15% market reset → €807/mo
- Years 13–20: 2%/yr → €927/mo by year 20
- Year 21: +15% market reset → €1,088/mo
- Years 21–30: 2%/yr → €1,300/mo by year 30

**Comparison with smooth 3%/yr at year 30 (€250K flat, buyer outflow €1,425/mo):**

| Model          | Total rent paid | Portfolio at Inv 6% | Difference vs smooth |
| -------------- | --------------- | ------------------- | -------------------- |
| Smooth 3%/yr   | ~€290,070       | €959,290            | —                    |
| Stepped resets | ~€308,001       | €937,122            | −€22,168             |

**Interpretation:** The stepped model produces ~€22K less portfolio than smooth 3% — a modest difference. The renter
pays ~€18K more in total rent, but the timing matters: rent is lower in the early years (when compounding helps most)
and higher in the later years (when it hurts less). The stepped model is slightly worse for the renter, but the impact
is small (~2.3% of portfolio value). The Part 4 conclusions hold under realistic contract-cycle dynamics.

### Qualitative: Seasonal contract risk

If you cannot secure a _vivienda habitual_ lease on the Castellón coast and end up in seasonal contracts
(_arrendamientos por temporada_), you lose the LAU stability protections (5–8 year minimum, sale subrogation, limited
updates). This means annual repricing at market rates, moving costs every 1–2 years (deposits, agency, lost time), and
no protection against landlord decisions. The effective rent inflation could approach the 6% scenario above — which
still doesn't flip the overall conclusion but significantly erodes the rent advantage. The mitigation is clear: **only
sign vivienda habitual contracts**, even if the selection is smaller.

### Qualitative: Regulatory change risk

Spain's rent update regime has changed four times in recent years (2019 LAU reform, 2022 emergency caps, 2023 Housing
Law, new INE reference index). Over 30 years, further changes are certain. If regulations become more tenant-protective
(e.g., stressed-area declarations in Valencia, permanent reset caps), the renter benefits — lower rent inflation,
stronger stability. If they become more landlord-favourable (deregulation, easier eviction), renting becomes riskier.
The direction is unpredictable, but the recent trend in Spain has been toward more protection. This is a wash for
planning purposes — model both extremes via the 1.5% and 6% rent scenarios.

### Qualitative: Voluntary early sale

Different from the 2D forced sale (crisis-driven), a voluntary early sale (e.g., moving cities, life change) still
incurs the same transaction costs, early repayment fees, and equity erosion. The Part 2D tables apply directly — even at
year 10 under optimistic 4% price growth, selling results in a net loss of ~€50K. Voluntary exit is _less_ bad than
forced (you can time it better, likely get market price), but the structural friction is the same. Every early exit
degrades the buy case; the rent scenario has no equivalent exit cost.

### Qualitative: Mortgage refinancing

If rates drop significantly below 4.0–4.5%, refinancing could reduce monthly payments and total interest. At 3.0%, the
€237,500 mortgage payment drops from €1,134 to ~€1,001 (~€133/mo saving). Over 20 remaining years, that's ~€32K saved.
However: refinancing costs money (new appraisal, possible notary/registry fees), the early repayment fee on the old
mortgage (up to 2% of outstanding balance) eats into the benefit, and you'd need rates to drop by at least 1 full
percentage point for the economics to work. This is a positive optionality for the buyer that the model doesn't capture
— but it's conditional on rate movements that are unpredictable.

### Qualitative: Below-average investment returns

What if the next 30 years produce only 2–3% nominal returns? This is below the pessimistic 4% scenario and would
represent an unprecedented multi-decade equity underperformance. At 2% nominal, the renter's portfolio (equal-outflow,
3% rent inflation, €250K flat comparison) would be roughly €400–450K — below the buyer's baseline 2.5% equity of €524K.
In this world, buying wins at baseline or optimistic property growth. The key question: is persistent sub-4% global
equity return plausible? The worst rolling 20-year S&P 500 return was ~2.8% (nominal, USD). It has happened — but
rarely, and only in the aftermath of the most extreme bubbles.

### Qualitative: Inflation impact

All scenarios use nominal figures. If inflation is higher than assumed (~2%), then:

- **Property prices** tend to track or exceed inflation (real assets), so nominal appreciation may be higher — but real
  appreciation (what matters for purchasing power) stays modest.
- **Rent** rises with or above inflation, eroding the renter's surplus faster.
- **Investment returns** in nominal terms may be higher, but real returns matter for purchasing power. At 3% inflation,
  a 6% nominal return is only 3% real.
- **Mortgage payments are fixed** — this is the buyer's single biggest inflation advantage. Inflation erodes the real
  value of the mortgage payment over time. By year 20, €1,134/mo feels much lighter in real terms.

Net effect: higher inflation modestly favours the buyer (fixed payments become cheaper in real terms) but also pushes
rents up faster (hurts the renter). At moderate inflation (2–3%), the impact is roughly neutral. At sustained high
inflation (5%+), buying gains a meaningful edge.

### Qualitative: Changing investment capacity

If your income grows over time, both scenarios benefit — but the renter benefits more (can invest more). If income
stagnates or falls, the buyer is locked into fixed mortgage payments while the renter can reduce investment
contributions. The buyer's payment is rigid; the renter's investment is flexible. This asymmetry is already captured in
the 2D income stress test — the buyer needs at least €4,071/mo net to stay below 35% housing ratio, while the renter
simply adjusts contributions downward.

---

## Part 6 — Extended Analysis

This section extends the core analysis (Parts 1–5) with additional computations addressing
cost inflation, taxation, rent equivalence, crash scenarios, equity stress testing, retirement
cashflow, timing effects, and an alternative strategy. Each subsection is self-contained.

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

### 6.2 — After-tax portfolio outcomes

Spanish CGT brackets (19/21/23/27/30%) applied to portfolio gains at liquidation. The
renter's cost basis is total contributions (lump sum + all monthly DCA). Effective tax rates
range from ~23% to ~29% depending on gain size — taxation is not a rounding error.

The after-tax comparison matrices in Part 4 incorporate these rates. Key observation:
spreading sales over 3–5 tax years would reduce the effective rate (more gains stay in lower
brackets), benefiting the renter regardless of scenario.

### 6.3 — Rent-to-buy equivalence

Is €500/mo the market rent for the same flat you'd buy at €200–250K? The existing research
data answers this.

#### Implied rental yields from existing research

| Municipality    | Asking €/m² (sale) | Asking rent €/m²/mo | Gross yield |
| --------------- | ------------------ | ------------------: | ----------: |
| Benicàssim      | €2,796             |               €10.5 |        4.5% |
| Oropesa del Mar | €2,004             |                €9.3 |        5.6% |
| Vinaròs         | €1,683             |                €8.4 |        6.0% |
| Province avg    | €1,526             |                €9.1 |        7.2% |

Average gross yield across available data: **~5.8%**.

#### What would a €250K / €200K flat rent for?

| Flat price | At Benicàssim yield (4.5%) | At Oropesa yield (5.6%) | At average yield (5.8%) |
| ---------- | -------------------------- | ----------------------- | ----------------------- |
| €250,000   | **€939/mo**                | €1,160/mo               | €1,209/mo               |
| €200,000   | **€751/mo**                | €928/mo                 | €968/mo                 |

Even at the lowest yield (Benicàssim, a premium market), a €250K flat would rent for ~€939/mo — nearly **double** our
€500 assumption. A €200K flat would rent for ~€751/mo.

#### What this means for the comparison

There are **two valid ways to frame the decision**, and they answer different questions:

**"Same flat" framing:** If you're asking "should I buy THIS flat or rent THIS flat and invest the difference?" then
starting rent should be the equivalent rent (~€750–€950). This dramatically favours buying.

**"Same person" framing:** If you're asking "I currently rent for €500 in a modest flat — should I upgrade to a €250K
flat or stay and invest?" then €500 is correct. This is the framing we've been using, and it favours renting because
you're comparing "buy expensive" vs "rent cheap + invest the difference."

Both are valid, but they answer fundamentally different questions.

#### Year 30 after-tax comparison at different starting rents (€250K flat)

> **Note:** This table uses an equal-outflow model where the renter's DCA varies with rent
> level (DCA = buyer outflow − rent). This is the appropriate model for the "same flat"
> framing, where higher rent directly reduces investable surplus. The Part 4 comparison uses
> a fixed-DCA model for the "same person" framing. Specific win counts may differ slightly
> between models; the directional pattern — higher rent shifts the comparison toward buying
> — is robust.

Buyer outflow with inflated costs (from 6.1). After-tax renter portfolios (CGT applied).

| Starting rent | Buy wins (out of 9) | Key shift from €500 baseline                                                                |
| ------------- | ------------------: | ------------------------------------------------------------------------------------------- |
| **€500/mo**   |             **1/9** | Original — buyer surplus maximised                                                          |
| **€600/mo**   |             **3/9** | Buying competitive at 2.5% prop + 4% inv                                                    |
| **€700/mo**   |             **3/9** | Buying wins same cells but by wider margins                                                 |
| **€800/mo**   |             **6/9** | **Buying wins the majority.** Only loses at pessimistic property + high investment returns. |

At €800/mo starting rent (plausible for a €200K+ flat in non-premium coastal locations), **buying wins 6 out of 9
scenario cells** — a complete reversal from the €500 baseline.

The detailed after-tax matrices for each rent level:

**€500/mo:** BUY 1/9 — only at 4% prop + 4% inv **€600/mo:** BUY 3/9 — adds 2.5% prop + 4% inv and 4% prop + 6% inv
**€700/mo:** BUY 3/9 — same cells as €600 but wider buy margins **€800/mo:** BUY 6/9 — buying wins everything except 1%
property or 8% investment return

**This is the single most decision-critical variable.** The conclusion swings entirely on whether you're comparing "rent
the same flat" vs "rent cheap and invest the upgrade budget."

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

### 6.5 — Equity drawdown stress test

Part 2D stress-tests housing through forced sale. This section applies symmetric treatment
to equities by modelling two crash scenarios for the renter's portfolio.

#### "Bad decade first" — -40% crash at year 2, slow recovery over 5 years

| Base return | Smooth (after-tax) | With crash (after-tax) | Impact          |
| ----------- | ------------------ | ---------------------- | --------------- |
| 4%          | €574,710           | €510,120               | −11.2% (−€65K)  |
| 6%          | €831,440           | €709,526               | −14.7% (−€122K) |
| 8%          | €1,255,208         | €1,023,992             | −18.4% (−€231K) |

An early crash hurts by 11–18%. Significant, but the portfolio still recovers thanks to 28 years of continued DCA after
the crash. Early crashes are survivable because continued monthly contributions buy more units at depressed prices.

#### "Bad decade last" — -40% crash at year 28

| Base return | Smooth (after-tax) | With crash (after-tax) | Impact          |
| ----------- | ------------------ | ---------------------- | --------------- |
| 4%          | €574,710           | €367,939               | −36.0% (−€207K) |
| 6%          | €831,440           | €516,043               | −37.9% (−€315K) |
| 8%          | €1,255,208         | €739,121               | −41.1% (−€516K) |

**A late crash is devastating** — it wipes out 36–41% of the after-tax portfolio with no time to recover. At 6% base
return, the portfolio drops from €831K to €516K after tax. Compare this to the buyer's equity of €524K (at 2.5% property
growth) — the renter now **loses** to the buyer even at baseline assumptions.

#### What this means

The renter's strategy is **fragile to late-career market crashes**. The buyer's equity at year 30 is the flat value (not
exposed to equity market timing). If the renter reaches year 28 with a large portfolio and the market crashes 40%,
they're worse off than the buyer in most scenarios. The buyer's "forced savings in a real asset" provides crash
insurance at retirement that the renter's portfolio does not.

This is the symmetric counterpart to the buyer's forced-sale risk: the buyer is vulnerable to property crashes in the
early years, the renter is vulnerable to equity crashes in the late years. Neither strategy is risk-free.

### 6.6 — Post-mortgage retirement cashflow (recomputed with real scenario)

The mortgage ends at age ~68–69 depending on scenario. The retirement extension runs 20 years post-mortgage (to age
~87–89). Shown here for the two primary scenarios.

#### Starting positions — €250K flat, €1,500/mo (mortgage ends age ~68)

| Item                 | Owner (at 2.5% prop)                      | Renter (Inv 6%, AT)             |
| -------------------- | ----------------------------------------- | ------------------------------- |
| Housing asset        | Flat worth ~€524K                         | None                            |
| Liquid assets        | ~€406K (€35K buffer + €371K portfolio AT) | ~€1,379K                        |
| Monthly housing cost | ~€527 (ongoing, inflating 2%/yr)          | ~€1,278 (rent, inflating 3%/yr) |

Owner cumulative housing cost over 20yr retirement: ~€154K. Renter cumulative rent over 20yr retirement: ~€412K.

#### Starting positions — €200K flat, €1,000/mo (mortgage ends age ~68)

| Item                 | Owner (at 2.5% prop)                      | Renter (Inv 6%, AT)             |
| -------------------- | ----------------------------------------- | ------------------------------- |
| Housing asset        | Flat worth ~€420K                         | None                            |
| Liquid assets        | ~€187K (€35K buffer + €152K portfolio AT) | ~€956K                          |
| Monthly housing cost | ~€527 (ongoing, inflating 2%/yr)          | ~€1,291 (rent, inflating 3%/yr) |

#### Does the renter's portfolio survive 20 years of rent drawdown?

Portfolio continues earning returns during drawdown. Tested at 2% (conservative) and 4% (moderate) drawdown-phase
returns. Results for the €250K/€1.5K scenario:

| Starting portfolio (AT) | Drawdown return | Balance at age ~88 | Survives? |
| ----------------------: | :-------------: | -----------------: | :-------: |
|        €1,002K (Inv 4%) |       2%        |          **€994K** |    Yes    |
|        €1,002K (Inv 4%) |       4%        |        **€1,595K** |    Yes    |
|        €1,379K (Inv 6%) |       2%        |        **€1,554K** |    Yes    |
|        €1,379K (Inv 6%) |       4%        |        **€2,420K** |    Yes    |
|        €1,964K (Inv 8%) |       2%        |        **€2,423K** |    Yes    |
|        €1,964K (Inv 8%) |       4%        |        **€3,702K** |    Yes    |

Results for the €200K/€1K scenario:

| Starting portfolio (AT) | Drawdown return | Balance at age ~88 | Survives? |
| ----------------------: | :-------------: | -----------------: | :-------: |
|          €692K (Inv 4%) |       2%        |          **€527K** |    Yes    |
|          €692K (Inv 4%) |       4%        |          **€908K** |    Yes    |
|          €956K (Inv 6%) |       2%        |          **€921K** |    Yes    |
|          €956K (Inv 6%) |       4%        |        **€1,488K** |    Yes    |
|        €1,370K (Inv 8%) |       2%        |        **€1,535K** |    Yes    |
|        €1,370K (Inv 8%) |       4%        |        **€2,395K** |    Yes    |

**The renter's portfolio never runs out in any tested scenario.** Even at the most pessimistic combination (4%
accumulation, 2% drawdown), the portfolio survives 20 years of rent withdrawals and still has €527K–€994K remaining at
age ~88.

#### Why the retirement asymmetry is real but smaller than it appears

The owner at ~88: owns a flat worth ~€859K (appreciated from €524K over 20yr at 2.5%), paid ~€154K in ongoing costs. But
the wealth is **illiquid** (locked in the flat).

The renter at ~88 (baseline 6% accum, 4% drawdown): still has **€2,420K liquid portfolio** after paying ~€412K in rent
over 20 years. More money, fully liquid.

The retirement asymmetry favours buying **only if:**

- Investment returns during drawdown are very low (below 2%), OR
- The renter started with a smaller portfolio (e.g., higher equivalent rent from 6.3), OR
- The renter faces a late-career crash (6.5) that depletes the portfolio before retirement

For the €500/mo rent baseline, the renter comfortably outperforms in retirement. For the €700–800/mo equivalent-rent
scenario, the renter's starting portfolio is smaller and the retirement picture becomes tighter — but the portfolio
still survives in all tested scenarios.

### 6.7 — Cash position timing divergence

Current savings: €15,000. Emergency buffer: €8,000. The two paths diverge immediately.

#### Saving period before purchase

| Target flat     | Upfront needed | At €1K/mo saving      | At €1.5K/mo saving    |
| --------------- | -------------- | --------------------- | --------------------- |
| €200K (ITP 9%)  | €30,100        | 15 months (1.2yr)     | 10 months (0.8yr)     |
| €200K (ITP 10%) | €32,100        | 17 months (1.4yr)     | 12 months (1.0yr)     |
| €250K (ITP 9%)  | €37,200        | **22 months (1.8yr)** | **15 months (1.2yr)** |
| €250K (ITP 10%) | €39,700        | 24 months (2.0yr)     | 16 months (1.3yr)     |

The buyer must save at 2% in a bank account for 10–24 months before they can act.

#### What the investor has during that waiting period

The investor deploys €7K (€15K − €8K buffer) immediately and starts DCA from month 1. By the time the buyer reaches the
purchase threshold for the €250K flat (ITP 9%):

| Monthly capacity | Wait period | Investor portfolio at that point | Buyer position |
| ---------------- | ----------- | -------------------------------- | -------------- |
| €1,000/mo        | 22 months   | **€30–32K** (in the market)      | €0 liquid      |
| €1,500/mo        | 15 months   | **€30–31K** (in the market)      | €0 liquid      |

The investor has **€30K+ compounding in the market** while the buyer has spent everything on the purchase and has zero
liquid savings. This head start compounds for the remaining 28+ years.

#### Impact on the full 30-year picture

The timing divergence has two effects:

1. The investor gets **22 extra months** of market exposure on early contributions
2. The buyer's mortgage runs shorter (~28.2 years instead of 30) but they start later

For the €250K flat at €1K/mo capacity, the investor's raw portfolio at year 30 (from today, not from purchase) is:
**€717K at 4%, €1,047K at 6%, €1,567K at 8%** — before any equal-outflow adjustment for rent vs buyer costs.

The timing effect is moderate but real: the ~22-month head start adds roughly **€15–25K** to the final portfolio
depending on return assumptions. Not decision-changing on its own, but it compounds the renter's existing structural
advantage.

### 6.8 — "Buy later without mortgage" third strategy

Instead of choosing between "buy now with mortgage" or "rent forever and invest," there's a third path: **invest from
day 1, then buy outright once the portfolio reaches the flat price.** No mortgage. No interest. No 95% LTV risk. No
forced-sale exposure.

The purchase cost includes the appreciated flat price + ~10% for ITP and fees (no
mortgage-related costs). CGT is paid on the portfolio gains when selling to buy.

The target is a moving one: the flat price appreciates while you save. The table below shows
when the after-tax portfolio reaches the appreciated flat price + 10% costs, across all three
property growth scenarios.

#### When can you buy outright? (after tax + appreciation + purchase costs)

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

At the baseline 6% return and 2.5% property appreciation with €1,500/mo: buy a €200K flat
outright at **age 48** (flat has appreciated to ~€267K) or a €250K flat at **age 51** (flat
has appreciated to ~€359K). With €1,000/mo: ages 53 and 57 respectively.

At pessimistic property growth (1%), the timelines are shorter — closer to the original
static-price estimates. At optimistic property growth (4%), the strategy becomes much slower
or impractical (the flat appreciates nearly as fast as the portfolio).

**Impact of accounting for appreciation (6% return, 2.5% property growth):**

| DCA    | Flat | Static price | With appreciation | Delay  |
| ------ | ---- | :----------: | :---------------: | :----: |
| €1,000 | €200K | 12.7yr (49) | 17.2yr (53) | +4.5yr |
| €1,000 | €250K | 14.9yr (51) | 21.2yr (57) | +6.3yr |
| €1,500 | €200K | 9.3yr (45)  | 11.8yr (48) | +2.4yr |
| €1,500 | €250K | 11.2yr (47) | 14.7yr (51) | +3.5yr |

Accounting for appreciation adds **2–6 years** to the buy-later timeline at baseline
assumptions. The delay is larger at lower DCA (smaller portfolio grows slower relative to
the rising target) and for the more expensive flat.

#### What makes this strategy attractive

1. **Zero interest cost.** The mortgage on a €250K flat costs €171–196K in interest over 30 years. This strategy pays €0
   in interest.
2. **Zero forced-sale risk.** No mortgage means no negative equity, no bank pressure, no early repayment fees. If prices
   crash, you just wait.
3. **Full liquidity until purchase.** Your money is in a diversified global index fund, not locked in a single property.
   You can adjust timing, change target, or abandon the plan.
4. **Flexibility on what you buy.** Property prices in 10–15 years may be very different — you can adapt to the market
   rather than being locked into a 2026 purchase decision.
5. **After purchase, you continue investing.** Once you own outright, the €1,000–1,500/mo that was going to DCA
   continues — now building a pure retirement portfolio with no housing cost drag.

#### Remaining portfolio after buying outright

At the point of purchase, nearly the entire portfolio goes to the flat — remaining balance
is ~€0–2K. But from that point forward, you own outright + invest the full monthly capacity.

Example (baseline 2.5% appreciation): buy €200K flat at age 48 (€1.5K/mo at 6%), then
invest €1.5K/mo for the remaining ~21 years to age ~69 → portfolio at age 69: **~€680K+**
(pure retirement savings, no housing cost, no mortgage). Compare to: "buy now" scenario at
age ~69 has flat equity + minimal parallel portfolio (constrained by buffer rebuild and cost
inflation).

#### The trade-off

The cost of this strategy is **renting for 10–21 years longer** than if you bought now
(depending on DCA, returns, and property appreciation). At €500/mo with 3% inflation, total
rent paid over 12 years is ~€82K; over 17 years: ~€132K. This is the "price" of avoiding
€171–196K in mortgage interest and eliminating forced-sale risk.

At baseline assumptions (6% return, 2.5% appreciation, €1.5K DCA), the rent cost during
the investment phase roughly offsets the mortgage interest saved — the net financial benefit
is smaller than the static-price estimate suggested, but the strategy retains full liquidity
and zero forced-sale risk throughout.

### Note: Income instability and AI disruption risk

If there is meaningful probability of income disruption in the 5+ year horizon (AI-driven job market shifts, career
transitions, periods of reduced earnings), this **strongly favours renting + investing** or the buy-later strategy over
buying now with a mortgage.

The core asymmetry: a mortgage is a rigid 30-year legal obligation. A portfolio is a liquid asset with zero ongoing
obligation. At year 5, the buyer owes ~€1,449/mo regardless of income, needs €4,071/mo net to stay below 35% housing
ratio, and faces €56–95K net losses if forced to sell (or owes the bank €29K in a -20% crash). The renter at year 5 pays
~€580/mo rent, can pause DCA instantly, can draw from a ~€80–100K liquid portfolio, and can move to a cheaper flat. The
buy-later strategy adds the advantage that a delay is just a delay — not a crisis — and the portfolio serves as an
emergency fund during any income gap.

### 6.9 — Consolidated comparison

All Part 4 computations use the buyer's actual financial position (€15K savings, €7K lump
for investor, three-phase buy path with saving period, buffer rebuild, and parallel
investing). All renter portfolios are after Spanish CGT. Owner costs inflate at 2%/yr.
Results incorporate sections 6.1–6.8.

#### Results summary

**Buy wins 1/9 in all four configurations** at the end of the total timeline. Only at
optimistic property (4%) + pessimistic investment (4%) does buying win.

Three structural features drive this:

1. **The investor gets a compounding head start.** The buyer saves at 2% bank rate for 17–31
   months while the investor deploys €7K + DCA at market rates from month 1. By purchase
   time, the investor has €30K+ in the market vs the buyer's €0 liquid.

2. **The buyer's parallel investment capacity is severely limited.** After purchase, spare =
   budget − housing costs. For the €250K/€1K scenario, spare starts at €75/mo and goes
   negative by year 12. Even the €250K/€1.5K scenario only generates €339–575/mo of
   declining spare.

3. **The €250K/€1K scenario is barely viable.** Housing costs exceed the €1,500 budget by
   mortgage year 12–13. The buyer's buffer erodes, and the final net worth consists almost
   entirely of flat equity.

#### Break-even: required property growth to match renting

| Scenario          | At Inv 4% | At Inv 6% | At Inv 8% |
| ----------------- | --------: | --------: | --------: |
| €250K at €1K/mo   |      3.5% |      4.7% |      5.9% |
| €250K at €1.5K/mo |      3.5% |      4.6% |      6.0% |
| €200K at €1K/mo   |      3.4% |      4.6% |      5.9% |
| €200K at €1.5K/mo |      3.3% |      4.6% |      5.9% |

At baseline 6% investment return, buying needs **~4.6–4.7% annual property growth** — above Castellón's 10yr CAGR (2.5%)
and Spain's 30yr CAGR (~4.0%). Only at pessimistic 4% investment does the required growth (~3.3–3.5%) enter the
plausible range.

#### Rent-level sensitivity (from 6.3) still applies

The 6.3 analysis (using an equal-outflow model appropriate for the "same flat" framing)
showed that at €800/mo starting rent, buying wins 6/9 scenarios. The specific win counts may
shift slightly under the fixed-DCA model used in Part 4, but the directional conclusion
holds: **the actual rent level is the single most decision-critical variable.**

#### Updated conclusion

**At €500/mo rent ("same person" framing):** Renting + investing wins in 8/9 scenario combinations at the end of the
total timeline, across all four configurations. The real scenario reinforces this finding and reveals that the €250K/€1K
buy path is financially precarious (budget deficit from year 12). Buying is only competitive if property appreciates at
4%+ while investments return only 4% — requiring Castellón to outperform its historical average while global equities
underperform theirs.

**At €700–800/mo rent ("same flat" framing):** Buying becomes competitive or favourable, as established in section 6.3.

**The third strategy — buy later without mortgage (6.8)** — remains the most robust path for a buyer with income
instability concerns. It combines the compounding advantage of early investing with eventual mortgage-free ownership and
zero forced-sale risk.

