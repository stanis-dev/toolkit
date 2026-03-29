## 1. Executive summary

The capital-maximizing answer is **not** a permanent 80/20. The evidence points to a **nearly all-equity lifecycle
portfolio for almost the entire 30+ years**, implemented with Spanish **traspaso-eligible mutual funds**, and a
**temporary EUR house bucket only when the property purchase is realistically 12–24 months away**. My best
evidence-based, implementable version is a diversified all-equity core tilted away from today’s very U.S.-heavy
market-cap mix, then a tax-deferred traspaso into a EUR money-market or very short-duration EUR government fund for only
the **gross** amount needed to net the house down payment after CGT. In a 30-year deterministic after-tax model using
Spain’s 2026 savings-tax schedule, FIFO/traspaso rules, and current 2026 capital-market assumptions, that approach beats
a naive permanent 80/20 global-equity/MMF baseline by about **€64.5k to €90.8k after tax at retirement** across the
7/9/12-year and €60k/€70k/€80k withdrawal cases, or roughly **+10.1% to +11.8%**. Even a simpler **100% World +
temporary house bucket** beats the permanent 80/20 baseline by about **€17.7k to €31.2k**. ([CNMV][1])

## 2. Asset allocation evidence

The long-horizon evidence does not support a permanent bond/cash sleeve for a pure wealth-maximization objective. In the
Cederburg/Anarkulova/O’Doherty dataset across 39 developed markets, pooled real monthly returns were about **0.44% for
international stocks, 0.37% for domestic stocks, 0.04% for government bonds, and -0.03% for bills**. Their base-case
optimal pre-retirement portfolio is **all equity**—**33% domestic, 67% international, 0% bonds, 0% bills**—and they
estimate target-date-fund investors would need substantially more savings to match that outcome. Since that paper
already gets to all-equity despite using expected utility rather than raw terminal wealth, your stricter objective of
“maximize money at 69” pushes in the same direction, not toward a permanent defensive sleeve. ([ICPM][2])

Your house purchase changes the problem, but only **locally**. It creates a **mid-horizon liquidity constraint**, not a
reason to hold 20% cash for three decades. The right structure is phase-based: keep the core portfolio all-equity while
the purchase is distant; once the purchase becomes likely within roughly **12–24 months**, use **traspasos** to move
only the required gross proceeds into a low-volatility EUR fund; after the purchase, move the retained portfolio back to
the all-equity core. Because your purchase date is flexible, you also have option value: you are not forced to liquidate
in a year-7 crash, which makes a permanent cash allocation even less compelling. Spain’s traspaso regime is exactly what
makes this phase shift efficient, because qualifying fund-to-fund switches defer tax and preserve basis/date.
([CNMV][1])

A useful way to see the drag is with 2026 expected returns. J.P. Morgan’s 2026 EUR nominal long-term assumptions are
roughly **6.4% for AC World equity**, **7.2% for euro-area large caps**, **7.2% for EM equity**, and about **3.9%–4.0%
for euro government/aggregate bonds**; current euro cash-like rates are about **2.0%** from the ECB/TR cash environment.
On those starting points, a permanent 80/20 global-equity/cash mix compounds about **1.2 percentage points a year
below** the recommended all-equity tilted core after fund costs. That is why, in my model, the simpler **100% World +
temporary house bucket** already beats permanent 80/20 in every tested scenario. ([am.jpmorgan.com][3])

## 3. Geographic allocation analysis

A 2026 starting point does **not** make the current market-cap-weighted ~70% U.S. mix look optimal. AQR’s 2026
assumptions put U.S. CAPE **near 40**, around the **96th percentile since 1980**, and estimate lower local real returns
for U.S. large caps (**3.9%**) than for the eurozone (**5.0%**) or emerging markets (**5.1%**). J.P. Morgan’s EUR
nominal 2026 CMAs are similar in direction: **6.1% U.S. large cap**, **7.2% euro-area large cap**, **7.2% EM**, versus
**6.4% AC World**. Vanguard’s 2026 outlook also says the strongest 5–10 year risk/return profiles are outside the
obvious U.S. growth trade, especially in **ex-U.S. developed equities** and **U.S. value** rather than expensive U.S.
growth. ([AQR Capital Management][4])

That does **not** mean “go 100% Europe” or “go 100% Japan because one forecast is highest.” If you treated one manager’s
point estimates as literal truth, the mathematical maximum would be a highly concentrated single-region bet; I regard
that as overfitting, not robust evidence. The evidence-backed move is a **moderate ex-U.S. overweight**, not a
one-country concentration. My preferred implementation is **55% World / 25% Europe / 20% EM**, which leaves your
effective U.S. weight around **39%** while preserving a broad developed-market core. It captures the current
valuation/expected-return gap without pretending we can forecast the single best country for 30 years. If your TR app
lacks a suitable EM mutual fund, the fallback is **75% World / 25% Europe**. ([AQR Capital Management][4])

For currency, I would **not** broadly EUR-hedge the equity sleeve. Vanguard’s position is that investors should
generally accept currency risk in international equities because it can lower correlations and hedge domestic inflation
risk, while currency risk in international fixed income should usually be hedged because otherwise the bond sleeve can
take on equity-like volatility. Campbell/Serfaty-de Medeiros/Viceira reach a similar conclusion: the case for **full
hedging is strong in bonds**, much weaker in equities. Hedging “cost” itself is not a fixed fee; it largely reflects
rate differentials plus implementation/roll costs, so it can be a cost in one direction and a benefit in the other. My
rule is simple: **equities unhedged, defensive sleeve hedged to EUR**. ([Vanguard][5])

## 4. Defensive sleeve verdict

The permanent defensive sleeve verdict is: **zero**. Not 20%, not 10%, just **none** in the default state. The only
defensible reason to hold a low-return sleeve here is to immunize the specific euros needed for the house once the
purchase becomes near-term. Holding that sleeve permanently is insuring a temporary liability for decades with a large
long-run return penalty. On current assumptions, euro cash-like rates are around **2.0%**, far below the expected return
on equities, and even euro government bonds sit well below the equity CMAs. ([European Central Bank][6])

For the house bucket itself, the instrument ranking is: **(1) EUR money-market mutual fund** if purchase is within about
a year; **(2) EUR-hedged short-duration euro-government fund** if purchase is 12–24 months away and you are willing to
tolerate small mark-to-market noise for a bit of extra carry. Do **not** use ETFs for this sleeve because Spanish ETFs
do not qualify for traspaso; do **not** use unhedged foreign bonds because that adds FX risk to the bucket whose job is
to be stable in EUR. After the purchase, with roughly 15–20 years still left, the retained portfolio should go back to
the all-equity core. ([CNMV][1])

## 5. Fund selection for Spain

Public verification of Trade Republic Spain’s exact mutual-fund shelf is still imperfect. Trade Republic’s official June
2025 Spain launch note confirms a broad local mutual-fund offering, index funds from major managers, traspasos, and
investing from **€1**; TR’s public ES mutual-fund browse page exists, but the live catalogue is JS-only and only
partially visible in search snippets. A recent 2026 TR-focused Spanish catalogue from Rankia confirms that Vanguard,
BlackRock, Fidelity and similar index funds are in the TR Spain offer, and that periodic plans can be automated. So I
treat exact 2026 ISIN availability as **partially verified** and would re-check the final ISINs in-app before sending
cash. ([Trade Republic][7])

Within the funds I could verify as real, low-cost, traspaso-eligible building blocks for a Spanish investor, these are
the best candidates:

- **Fidelity MSCI World Index Fund P-ACC-EUR (IE00BYX5NX33)** — MSCI World, **0.12% ongoing charges**; Fidelity’s docs
  show Spain registration, and FT lists it as available for sale in Spain. This is the cheapest broad developed/global
  core I could verify. ([PRIIPs Documents][8])
- **Vanguard Global Stock Index Fund EUR Acc (IE00B03HD191)** — MSCI World, **0.18% OCF**. Good fund, but more expensive
  than the Fidelity World core. ([Vanguard][9])
- **iShares Europe Index Fund (IE) D Acc EUR (IE00BDRK7L36)** — MSCI Europe, **0.10% ongoing charge** on BlackRock’s
  current facts page. This is the clean Europe tilt I would pair with the World core. ([BlackRock][10])
- **Fidelity MSCI Emerging Markets Index Fund P-ACC-EUR (IE00BYX5M476)** — MSCI EM, **0.20% ongoing charges**;
  Fidelity’s docs show Spain registration. Use this if it is actually present in your TR catalogue when you check.
  ([Fidelity International][11])

I could **not** independently verify a specific EUR money-market mutual fund in TR’s current public pages, so for the
house bucket I would choose the **cheapest EUR money-market mutual fund** visible in the app, or failing that the
cheapest **EUR-hedged short-duration euro-government** mutual fund. That is the one place where product selection has to
remain conditional on what you see live in TR. ([Trade Republic][7])

## 6. Contribution strategy analysis

For contribution timing, the optimal rule is simple. **Invest the initial lump sum immediately.** Vanguard’s work finds
lump-sum investing beats staged cost averaging about **two-thirds of the time** because time in the market matters. Then
invest each monthly **€1,500 as soon as it exists**. That is not “DCA alpha”; it is just minimizing idle cash.
([Vanguard][12])

I would **not** use value averaging, momentum-based contribution timing, or “wait for a better entry.” Hayley’s paper
shows value averaging’s headline IRR advantage is largely a **measurement bias**, not a true improvement in expected
terminal wealth, and it creates unstable cash-flow demands. More generally, DCA reduces variance only by accepting lower
expected return when cash is already available; once you exclude leverage, there is no legal/clean way to front-load
future salary beyond immediately investing the lump sum you already have. ([Bayes Business School][13])

## 7. Spanish tax optimization techniques

Spain-specific optimization starts with **vehicle choice**. Use mutual funds, not ETFs, in the core. CNMV’s 2026 guide
is clear that qualifying fund-to-fund **traspasos** defer tax and preserve the original acquisition date/value, while
ETFs do **not** get this regime. FIFO applies to homogeneous holdings, so in practice **separate ISINs create separate
queues**. ([CNMV][1])

The best use of that rule is **not** to own five clones of MSCI World. Because a traspaso preserves basis/date,
switching from one World fund to another does **not** reset your tax clock. You only gain real FIFO optionality when
separate ISINs have genuinely different purchase histories or different return paths. That is why I prefer **2–3
distinct equity sleeves plus a temporary house-bucket ISIN**. The tax value of holding many same-index clones is real
but second-order relative to allocation and house-bucket timing. ([CNMV][1])

There is also no true U.S.-style tax-loss-harvesting equivalent inside traspaso. To realize a loss you must actually
sell, and CNMV’s guide notes the **two-month anti-loss rule**: if you buy the same fund in the two months before or
after the sale, the loss is deferred rather than immediately usable. So the real Spanish edge here is **tax deferral via
traspaso**, not harvesting. ([CNMV][1])

## 8. The optimal portfolio

My recommended portfolio is:

- **Normal state (default):** **55% Fidelity MSCI World Index Fund P-ACC-EUR** **25% iShares Europe Index Fund (IE) D
  Acc EUR** **20% Fidelity MSCI Emerging Markets Index Fund P-ACC-EUR** _(if available in your TR app; otherwise use 75%
  World / 25% Europe)_. ([PRIIPs Documents][8])

- **When the house purchase becomes likely within 12–24 months:** Redirect **all new monthly contributions** to a **EUR
  money-market mutual fund**. Then use **traspasos** from the lowest embedded-gain sleeve(s) until the bucket equals the
  **gross** amount needed to net the down payment after CGT. If equities are in a deep drawdown and your timing is truly
  flexible, wait rather than forcing the sale. ([CNMV][1])

- **After the purchase:** Move the retained portfolio back to the same all-equity core. Do **not** keep a permanent
  defensive sleeve just because you once had a house purchase. The remaining horizon is still long. ([ICPM][2])

- **During the mortgage years:** If you truly have **€500–€650/month** above the required mortgage payment, the
  expected-value answer is to **invest it**, not overpay the mortgage, as long as your actual mortgage rate is below
  roughly **5.0%–5.5% nominal**. That threshold comes from comparing the guaranteed mortgage-rate “return” with the
  proposed portfolio’s after-tax equivalent CAGR over a 10–15 year horizon. Banco de España’s current 2026 reference
  housing-loan rate is around **2.8%**, so on today’s numbers the expected-wealth choice favors investing the spare
  cash. If your actual mortgage ends up materially above that threshold, flip the rule and overpay. ([Cliente
  Bancario][14])

Here is the base-case comparison from my model, using a midpoint **€8.5k** initial lump sum, **€1.5k/month**, a
**30-year horizon**, a **year-9 €70k net** house withdrawal, a **9-year mortgage contribution gap**, Spain’s 2026
CGT/FIFO rules, and annual net return assumptions anchored to current 2026 CMAs and verified fund costs:

| Strategy                                                   | After-tax wealth at year 30 |
| ---------------------------------------------------------- | --------------------------: |
| Permanent **80/20** World/MMF baseline                     |                 **€696.6k** |
| **100% World** + temporary 18-month house bucket           |                 **€718.9k** |
| Recommended **55/25/20** + temporary 18-month house bucket |                 **€771.4k** |

Across all tested **year-7/year-9/year-12** and **€60k/€70k/€80k** house-withdrawal scenarios, the recommended portfolio
beat the permanent 80/20 baseline by **€64.5k to €90.8k after tax**, while the simpler 100% World + temporary bucket
beat it by **€17.7k to €31.2k**. These are my expected-value model outputs, not guarantees, but they are directionally
consistent with the underlying research: **maximize equity exposure for almost the whole lifecycle, diversify away from
today’s U.S. concentration, and defend only the specific euros needed for the house only when the house becomes
near-term.** ([CNMV][1])

[1]:
  https://www.cnmv.es/DocPortal/Publicaciones/Guias/GuiaFiscalidadFondosInversion2026.pdf
  "https://www.cnmv.es/DocPortal/Publicaciones/Guias/GuiaFiscalidadFondosInversion2026.pdf"
[2]:
  https://www.icpmnetwork.com/wp-content/uploads/2025/09/1.Beyond-the-Status-Quo-A-Critical-Assessment-of-Lifecycle-Investment-Advice.pdf
  "https://www.icpmnetwork.com/wp-content/uploads/2025/09/1.Beyond-the-Status-Quo-A-Critical-Assessment-of-Lifecycle-Investment-Advice.pdf"
[3]:
  https://am.jpmorgan.com/content/dam/jpm-am-aem/americas/us/en/institutional/insights/portfolio-insights/ltcma-full-report.pdf
  "https://am.jpmorgan.com/content/dam/jpm-am-aem/americas/us/en/institutional/insights/portfolio-insights/ltcma-full-report.pdf"
[4]:
  https://www.aqr.com/-/media/AQR/Documents/Alternative-Thinking/AQR-Alternative-Thinking---2026-Capital-Market-Assumptions.pdf?sc_lang=en
  "https://www.aqr.com/-/media/AQR/Documents/Alternative-Thinking/AQR-Alternative-Thinking---2026-Capital-Market-Assumptions.pdf?sc_lang=en"
[5]:
  https://www.vanguard.co.uk/content/dam/intl/europe/documents/en/gbp-vemo-2024-eu-en-pro.pdf
  "https://www.vanguard.co.uk/content/dam/intl/europe/documents/en/gbp-vemo-2024-eu-en-pro.pdf"
[6]:
  https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html
  "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html"
[7]:
  https://assets.traderepublic.com/assets/files/250605_TradeRepublic_PressRelease_SpainBranchLaunch_ES_ES.pdf
  "https://assets.traderepublic.com/assets/files/250605_TradeRepublic_PressRelease_SpainBranchLaunch_ES_ES.pdf"
[8]:
  https://www.priipsdocuments.com/fidelity/docs/Fidelity%20MSCI%20World%20Index%20Fund%20P-ACC-Euro_STRD_en-gb_IE00BYX5NX33.pdf
  "https://www.priipsdocuments.com/fidelity/docs/Fidelity%20MSCI%20World%20Index%20Fund%20P-ACC-Euro_STRD_en-gb_IE00BYX5NX33.pdf"
[9]:
  https://www.vanguard.co.uk/professional/product/fund/equity/9837/global-stock-index-fund-eur-acc
  "https://www.vanguard.co.uk/professional/product/fund/equity/9837/global-stock-index-fund-eur-acc"
[10]:
  https://www.ishares.com/uk/individual/en/products/287906/ishares-europe-index-fund-ie-class-d-acc-eur
  "https://www.ishares.com/uk/individual/en/products/287906/ishares-europe-index-fund-ie-class-d-acc-eur"
[11]: https://www.fidelity.at/fonds/factsheet/IE00BYX5M476 "https://www.fidelity.at/fonds/factsheet/IE00BYX5M476"
[12]:
  https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf
  "https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf"
[13]:
  https://www.bayes.citystgeorges.ac.uk/__data/assets/pdf_file/0007/126736/Hayley.pdf
  "https://www.bayes.citystgeorges.ac.uk/__data/assets/pdf_file/0007/126736/Hayley.pdf"
[14]:
  https://clientebancario.bde.es/pcb/es/menu-horizontal/productosservici/relacionados/tiposinteres/guia-textual/tiposinteresrefe/tabla_tipos_referencia_oficiales_mercado_hipotecario.html
  "https://clientebancario.bde.es/pcb/es/menu-horizontal/productosservici/relacionados/tiposinteres/guia-textual/tiposinteresrefe/tabla_tipos_referencia_oficiales_mercado_hipotecario.html"
