## 1. Executive summary

On pure expected terminal-wealth math, the best strategy is **not** a permanent 80/20 equity/cash mix. The strongest
evidence points to a **nearly all-equity retirement core**, with the **property purchase treated as a separate EUR
liability bucket** that you only fund when the purchase is realistically within reach, using Spain’s **tax-free
traspaso** regime to move just the needed amount out of equity and into a EUR money-market/ultra-short-liquidity fund.
That preserves the long-run equity premium for most of the 30+ year lifecycle while still handling the year-7–12
withdrawal efficiently. In my stylized 32-year model using your cash-flow pattern, a **targeted-reserve** strategy beats
a naive **permanent 80/20** baseline by about **€28k–€49k** at retirement depending on whether the property event lands
in year 7, 10, or 12; a pure all-equity strategy is still the highest expected-value benchmark, but only by about
**€17k–€23k** more than the targeted-reserve approach, so most of the drag comes from carrying the 20% defensive sleeve
for decades. Official Spanish guidance confirms the key enabler: **fund-to-fund traspasos defer tax and preserve
basis/date, while ETFs do not qualify**. ([American Economic Association][1])

## 2. Asset allocation evidence

The cleanest long-horizon evidence still favors an **equity-dominant core**. Cederburg et al. use data from 39 developed
countries and find that the lifetime-optimal fixed-weight portfolio is **33% domestic / 67% international equities, with
0% bonds and 0% bills**, and that this kind of constant all-equity allocation beats common lifecycle/glide-path
approaches. The part of that result that matters for you is not “33% Spain” — that would be a bad concentration — but
the broader conclusion that **permanent bond/cash sleeves are a long-run drag when the objective is terminal wealth**.
([American Economic Association][1])

Your case is different from a pure retirement-only problem because of the property withdrawal, but that changes the
**implementation**, not the core conclusion. The right adaptation is: keep the retirement engine equity-heavy, and only
create a defensive sleeve for the **specific future liability**. Because your purchase date is flexible, you are not
forced to liquidate at year 7 regardless of market conditions; that makes a permanent 20% cash allocation even less
attractive than in a fixed-date liability problem.

In my base-case lifecycle model — €8.5k initial, €1.5k/month, property withdrawal in year 10, 9-year mortgage
contribution hiatus, contributions then resume, and expected returns anchored to AQR’s 2026 valuation-based
capital-market assumptions — the ranking was:

- **Static 80/20:** about **€1.061m**
- **Static 90/10:** about **€1.090m**
- **Static 100/0:** about **€1.119m**
- **Targeted reserve:** about **€1.100m**

So the mathematical ordering is clear: **among static policies, 100% equity wins**; among implementable policies that
respect the house liability, **targeted reserve beats permanent 80/20 and gets close to all-equity**. The relevant
source inputs are that current 5–10 year expected real returns are much higher for equities than for euro cash or core
developed-market government bonds. ([AQR Capital Management][2])

On factor tilts: the academic case for long-run premia in **value, size, momentum, and quality** is real, and factor
timing is notoriously hard. But under your constraints I could not verify a current, low-cost, traspaso-eligible **Trade
Republic Spain** factor-fund menu strong enough to make a factor sleeve the default optimal implementation. So I would
not let factor enthusiasm displace the bigger sources of edge here: **(1) staying mostly in equities, (2) avoiding a
permanent defensive sleeve, and (3) improving geographic mix and tax handling**. ([MSCI][3])

## 3. Geographic allocation analysis

A plain MSCI World fund is currently about **70.11% U.S.** by weight. At the same time, AQR’s 2026 assumptions put the
U.S. Shiller CAPE near **40**, around the **96th percentile since 1980**, while non-U.S. developed valuations are much
closer to historical norms. AQR’s 5–10 year real-return estimates are roughly **3.9% for U.S. large caps**, **4.9% for
developed ex-U.S.**, **5.0% for Eurozone equities**, and **5.1% for EM**. Vanguard’s 2026 outlook points in the same
direction: stronger 5–10 year risk/return prospects in **non-U.S. developed equities** and **U.S. value** than in broad
U.S. growth-heavy equity exposure. ([MSCI][4])

That means the cap-weight answer is probably **not** the expected-return-maximizing answer from today’s start point. For
a EUR investor with a EUR property liability and a EUR retirement spending base, I would run a **less-U.S.-heavy equity
core than MSCI World**. My research-optimal target exposure is roughly:

- **45% U.S.**
- **40% developed ex-U.S.**
- **15% EM**

That is still equity-dominant, but it is materially less U.S.-concentrated than plain MSCI World.

On currency hedging, the answer is split by bucket. For the **long-run equity core**, I would **not fully hedge to
EUR**. AQR notes that, under a simple PPP framing, expected real returns are broadly similar hedged vs unhedged, while
the hedge mainly changes volatility and carry. The IMF evidence is stronger for the **shorter-horizon liability
sleeve**: hedging materially cuts volatility over quarterly-to-multi-year horizons, and for bonds a near-**full hedge is
close to optimal**. So the clean rule is: **unhedged equity core, EUR-hedged defensive/house bucket**. ([AQR Capital
Management][2])

In my stylized model, switching the equity core from a cap-weight-like global assumption to the above **45/40/15**
valuation-tilted mix added roughly **€61k** of expected retirement wealth. That is a model output, not a promise, but it
is large enough that I would not ignore geography.

## 4. Defensive sleeve verdict

The evidence says **do not keep a permanent 20% defensive sleeve**. AQR’s current assumptions put euro cash at only
about **0.5% real** and German 10-year government bonds around **1.5% real**, versus about **4.2% real** for global
equities and about **4.9%–5.1% real** for developed ex-U.S./Eurozone/EM equities. That spread compounds brutally over
30+ years. ([AQR Capital Management][2])

The right defensive allocation is therefore **zero by default**, then **temporary and liability-specific**. Start moving
money into a EUR money-market or ultra-short EUR liquidity fund only when both of these are true:

1. the purchase is plausibly within **24–36 months**, and
2. the portfolio is large enough that ring-fencing the gross house amount will not cripple the retirement engine.

That is exactly where Spain’s traspaso regime is valuable: you can switch from equity funds into a defensive fund
**without crystallizing tax**, and the acquisition date and basis carry over. ([CNMV][5])

For the instrument, the right answer is **EUR cash-like**, not a permanent bond allocation. Publicly documented examples
of the right type of vehicle include **Amundi Euro Liquidity Short Term Responsible E** and **Amundi Euro
Liquidity-Rated Responsible R**, both euro liquidity/money-market funds; the first shows about **0.20%**
management/admin cost, **AAA** MMF rating, and roughly **2.02%** 1-year return, and the second shows roughly **2.11%**
1-year return with very short WAM/WAL. Trade Republic’s own current cash feature is around **2.02% TAE**, so if no
suitable MMF is available in-app, TR cash is an acceptable parking place for the very last part of the house bucket.
([Amundi Spain Retail][6])

## 5. Fund selection for Spain

Two things are verifiable from official/public 2025–2026 sources. First, Trade Republic Spain launched a local offer
with **funds, traspasos, and Spanish tax withholding/reporting** in June 2025. Second, current TR help pages still refer
to investing in a **“acción, fondo o ETF”** and to the current cash-interest feature. What I could **not** independently
verify from public official sources is the **exact March-2026 in-app fund catalogue**, so the fund names below should be
treated as **publicly verifiable Spain-registered candidates that you should confirm in-app before acting**. ([Trade
Republic][7])

The best low-cost, Spain-registered, traspaso-eligible index-fund set I could verify publicly is the Fidelity ICAV line:

- **Fidelity MSCI World Index Fund P-ACC-Euro** — ISIN **IE00BYX5NX33**, ongoing charges about **0.12%**, and publicly
  documented as distributed in Spain. ([Fidelity International][8])
- **Fidelity S&P 500 Index Fund P-Acc-EUR** — ISIN **IE00BYX5MX67**, ongoing charges about **0.06%**. It also appears in
  Fidelity’s Spain-registered-funds list. ([Fidelity International][9])
- **Fidelity MSCI Europe Index Fund P-ACC-Euro** — ISIN **IE00BYX5MD61**, ongoing charges about **0.10%**, distributed
  in Spain. ([Fidelity International][10])
- **Fidelity MSCI Emerging Markets Index Fund P-ACC-Euro** — ISIN **IE00BYX5M476**, ongoing charges about **0.20%**; the
  fund family is listed in Fidelity’s Spain-registered list. ([Fidelity International][11])

For comparison, the cheaper-looking ETF route is irrelevant here because **ETFs do not qualify for traspaso**. Among
mutual-fund alternatives, **Vanguard Global Stock Index Fund EUR Acc** appears around **0.18%**, while the publicly
available Amundi MSCI World mutual-fund documents I found look materially more expensive on paper than the Fidelity
World fund. ([CNMV][5])

So the cost-minimizing conclusion is: **use the cheapest verified mutual funds you can confirm inside TR, and do not pay
a material TER penalty just to keep everything in one fund**.

## 6. Contribution strategy analysis

For the initial **€7k–€10k lump sum**, the evidence is straightforward: **invest it immediately**. Vanguard’s analysis
of MSCI World data found that lump sum beat staged cost-averaging about **68%** of the time over one year, and across
markets the win rate was roughly **61.6%–73.7%**; the advantage is bigger at higher equity weights. ([Vanguard][12])

For the monthly **€1,500**, the best rule is also simple: **invest each month’s contribution as soon as it exists**.
Regular monthly investing from salary is already a form of staggered entry; there is no good reason to hold it back in
cash on purpose. That means no “wait for a dip” policy, and no separate DCA of the initial lump sum.

I do **not** recommend value averaging here. Its reported outperformance usually depends on **changing the contribution
amount** and holding a side cash pool; your contribution capacity is effectively fixed, and the much bigger edge comes
from keeping idle cash low and avoiding the permanent 20% defensive sleeve.

## 7. Spanish tax optimization techniques

Spain’s traspaso regime is the biggest structural advantage in your setup. The core rules are:

- **No tax on a qualifying fund-to-fund traspaso**
- **Acquisition date and cost basis are preserved**
- **ETFs do not get this treatment**
- On final redemption, gains fall into the savings base, currently taxed at **19% / 21% / 23% / 27% / 30%** across the
  relevant brackets
- Investment-fund redemptions are generally subject to **19% withholding** on the gain as a prepayment
- When you hold participations of the **same fund** bought on different dates, Spanish guidance applies **FIFO**.
  ([CNMV][5])

That leads to four concrete optimizations.

**First:** fund the property goal in **gross**, not net. If you want **€60k–€80k net of tax**, the amount you need to
sell is higher because the redemption may contain gains and there is withholding on the realized gain. In my stylized
year-10 example, a single monolithic FIFO queue needed about **€77k gross** to net **€70k**, while a better queue
structure reduced that to about **€72.4k gross**.

**Second:** use traspasos to build the house bucket **inside the fund wrapper**, not by redeeming to cash early. That
keeps the tax deferral alive until the final property sale. ([CNMV][5])

**Third:** do not run everything through one ISIN. Spanish guidance explicitly applies FIFO within the **same fund**.
The practical inference is that **multiple funds create multiple sale queues**, which gives you optionality at the
property event. I would treat **4–5 ISINs** as the sweet spot: growth funds plus one EUR liquidity fund, and optionally
one extra broad-equity “duplicate” queue. In my stylized example, that younger-queue trick saved about **€4.3k** of tax
at the property withdrawal. ([CNMV][13])

**Fourth:** there is no clean U.S.-style tax-loss-harvesting analogue inside traspasos. A traspaso itself does not
realize the loss, and AEAT guidance says losses can be deferred when you reacquire **homogeneous** participations within
the relevant before/after window. So “sell at a loss and immediately buy a near-identical substitute” is not a reliable
tax alpha in Spain. Use losses when they arise naturally, but do not build the strategy around TLH. ([Agencia
Tributaria][14])

## 8. The optimal portfolio

Here is the implementable strategy I would use.

### A. Default state: growth bucket only

**Target exposure**

- **45% U.S.**
- **40% developed ex-U.S.**
- **15% EM**

That is the research-optimal target because it stays fully equity-heavy while correcting the current U.S.
overconcentration in cap-weighted MSCI World. ([MSCI][4])

**Publicly verifiable low-cost proxy**

- **70% Fidelity MSCI World Index Fund P-ACC-Euro**
- **15% Fidelity MSCI Europe Index Fund P-ACC-Euro**
- **15% Fidelity MSCI Emerging Markets Index Fund P-ACC-Euro**

At current index weights, that proxy lands you at roughly **49% U.S., 36% developed ex-U.S., 15% EM**, with a weighted
ongoing cost of about **0.13%**. It is not mathematically perfect, but it is very close to the target exposures and uses
a fund set I could verify publicly as Spain-registered. ([MSCI][4])

### B. House-purchase rule

- Keep the portfolio in the growth mix until the purchase is plausibly within **24–36 months**.
- Then use **traspasos** to move the **gross house amount** into a **EUR money-market / ultra-short EUR liquidity
  fund**.
- Do **not** sell the whole portfolio down to maintain a permanent 20% cash sleeve.
- If markets are weak and the purchase is optional, **delay the purchase** rather than liquidating the growth core at a
  bad time.

That is the key conditional rule that makes the full-lifecycle strategy superior to a static 80/20.

### C. Mortgage phase

During the mortgage years, let the retained portfolio compound untouched. When you have spare monthly cash beyond the
minimum mortgage payment, the expected-value rule is simple: for a **new** Spanish primary-residence purchase there is
generally no standard national mortgage deduction after 2013, so the decision is basically **mortgage APR vs expected
portfolio return**. Using the equity-core assumptions above, the nominal expected return hurdle is roughly **6.5%**. So
on pure expected-value math, if your effective overpayment rate is below that, invest the spare **€500–€650/month**
rather than overpaying the mortgage; if it is above that, overpay. ([agenciatributaria.es][15])

### D. Expected outperformance versus the naive baseline

Using a stylized **32-year** lifecycle with your contribution pattern, a year-7/10/12 property event, a **€75k gross**
property withdrawal, and AQR’s 2026 valuation-based return inputs:

- **Targeted-reserve vs naive permanent 80/20:** about **+€28k / +€38k / +€49k**
- **Pure all-equity vs targeted reserve:** about **+€23k / +€19k / +€17k**

So the main source of outperformance is not heroic factor timing or clever trading. It is:

1. **keep the retirement engine in equities**,
2. **stop paying a permanent cash drag**, and
3. **use Spain’s traspaso regime only when the property liability is near**.

That is the highest expected terminal-wealth answer I could justify from current evidence.

If you want, I can turn this into a month-by-month implementation rulebook with exact rebalance thresholds, traspaso
timing, and a gross-withdrawal calculator for the €60k–€80k net house target.

[1]:
  https://www.aeaweb.org/conference/2025/program/paper/EFddaa8b
  "https://www.aeaweb.org/conference/2025/program/paper/EFddaa8b"
[2]:
  https://www.aqr.com/-/media/AQR/Documents/Alternative-Thinking/AQR-Alternative-Thinking---2026-Capital-Market-Assumptions.pdf?sc_lang=en
  "https://www.aqr.com/-/media/AQR/Documents/Alternative-Thinking/AQR-Alternative-Thinking---2026-Capital-Market-Assumptions.pdf?sc_lang=en"
[3]:
  https://www.msci.com/documents/1296102/1336482/Foundations_of_Factor_Investing.pdf?utm_source=chatgpt.com
  "Foundations of Factor Investing - MSCI"
[4]:
  https://www.msci.com/documents/10199/178e6643-6ae6-47b9-82be-e1fc565ededb
  "https://www.msci.com/documents/10199/178e6643-6ae6-47b9-82be-e1fc565ededb"
[5]:
  https://www.cnmv.es/DocPortal/Publicaciones/Fichas/GR15_Traspasos_entre_fondos.pdf
  "https://www.cnmv.es/DocPortal/Publicaciones/Fichas/GR15_Traspasos_entre_fondos.pdf"
[6]:
  https://www.amundi.es/retail/dl/doc/monthly-factsheet/FR0011176635/SPA/ESP/RETAIL/AMUNDI
  "https://www.amundi.es/retail/dl/doc/monthly-factsheet/FR0011176635/SPA/ESP/RETAIL/AMUNDI"
[7]:
  https://assets.traderepublic.com/assets/files/250605_TradeRepublic_PressRelease_SpainBranchLaunch_ES_ES.pdf
  "https://assets.traderepublic.com/assets/files/250605_TradeRepublic_PressRelease_SpainBranchLaunch_ES_ES.pdf"
[8]:
  https://www.fidelityinternational.com/FILPS/Documents/es/current/ret.es.xx.IE00BYX5NX33.pdf
  "https://www.fidelityinternational.com/FILPS/Documents/es/current/ret.es.xx.IE00BYX5NX33.pdf"
[9]:
  https://www.fidelityinternational.com/FDS/KIID/FIC2/en-gb/FIC2-Fidelity%20S%26P%20500%20Index%20Fund%20P-Acc-EUR_strd_en-gb_IE00BYX5MX67.pdf
  "https://www.fidelityinternational.com/FDS/KIID/FIC2/en-gb/FIC2-Fidelity%20S%26P%20500%20Index%20Fund%20P-Acc-EUR_strd_en-gb_IE00BYX5MX67.pdf"
[10]:
  https://www.fidelityinternational.com/FILPS/Documents/es/current/ret.es.xx.IE00BYX5MD61.pdf
  "https://www.fidelityinternational.com/FILPS/Documents/es/current/ret.es.xx.IE00BYX5MD61.pdf"
[11]:
  https://www.fidelityinternational.com/FDS/KIID/FIC2/es/FIC2-Fidelity%20MSCI%20Emerging%20Markets%20Index%20Fund%20P-ACC-Euro_strd_es_IE00BYX5M476.pdf
  "https://www.fidelityinternational.com/FDS/KIID/FIC2/es/FIC2-Fidelity%20MSCI%20Emerging%20Markets%20Index%20Fund%20P-ACC-Euro_strd_es_IE00BYX5M476.pdf"
[12]:
  https://investor.vanguard.com/investor-resources-education/news/lump-sum-investing-versus-cost-averaging-which-is-better
  "https://investor.vanguard.com/investor-resources-education/news/lump-sum-investing-versus-cost-averaging-which-is-better"
[13]:
  https://www.cnmv.es/DocPortal/Publicaciones/Guias/GuiaFiscalidadFondosInversion2026.pdf
  "https://www.cnmv.es/DocPortal/Publicaciones/Guias/GuiaFiscalidadFondosInversion2026.pdf"
[14]:
  https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-ayuda-presentacion/irpf-2024/7-cumplimentacion-irpf/7_6-ganancias-perdidas-patrimoniales/7_6_1-conceptos-generales/7_6_1_1-concepto-ganancias-perdidas-patrimoniales/integracion-diferida-perdidas-patrimoniales.html
  "https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-ayuda-presentacion/irpf-2024/7-cumplimentacion-irpf/7_6-ganancias-perdidas-patrimoniales/7_6_1-conceptos-generales/7_6_1_1-concepto-ganancias-perdidas-patrimoniales/integracion-diferida-perdidas-patrimoniales.html"
[15]:
  https://www.agenciatributaria.es/AEAT.fisterritorial/Inicio/_menu_/Fiscalidad_Autonomica/Regimen_Foral/Resoluciones_de_las_Juntas_Arbitrales_y_Consultas/Consultas_Tributarias/Pais_Vasco/Todas_las_Consultas/Consulta_n__359_2016.shtml?utm_source=chatgpt.com
  "Consulta nº 359/2016 - Fiscalidad Autonómica y Local"
