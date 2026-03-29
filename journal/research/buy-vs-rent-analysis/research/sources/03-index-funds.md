# Rent-and-invest in Spain with global equity index funds and ETFs

## Scope, definitions, and how to read the numbers

This report focuses on **global equity index investing** from the perspective of a **Spanish tax resident** making monthly contributions (€1,000–€1,500) over a **30‑year** horizon starting “now” (March 2026). It emphasises (i) what long-run equity outcomes have historically looked like, (ii) how fees compound, and (iii) what Spanish taxation implies for implementation choices (ETF vs *fondo de inversión*).

**Key definitions (important for comparing “index” vs “fund” results).**  
Total return means **price changes plus dividends**, assuming dividends are reinvested. The S&P 500 annual series cited explicitly states it includes “re-invested dividends”. citeturn57view0  
For MSCI, the factsheet explicitly reports **NET RETURNS** (EUR) and includes performance and risk metrics (including max drawdown). citeturn52view0  
For Vanguard’s VWCE product factsheet, the “benchmark” line is the **FTSE All‑World Index** and the factsheet reports **ongoing charges** and **annualised returns** (including a 10‑year figure for the benchmark). citeturn55view0  

**Currency caveat (EUR investor reality).**  
Even when you buy an ETF in EUR, if it holds global equities, the **economic exposure** is to the underlying currencies (USD, JPY, etc.). MSCI therefore publishes index returns directly in EUR, which is ideal for your modelling. citeturn52view0  

**Data limitations and transparency (especially for rolling-period and drawdown requests).**  
Some index providers publish detailed risk statistics (MSCI does, including maximum drawdown and the drawdown period). citeturn52view0 Others publish less in public factsheets. Where rolling-period and drawdown metrics cannot be obtained consistently from primary providers across all indices, I (a) use what the provider publishes, and (b) for S&P 500 rolling returns compute directly from the full annual total-return series. citeturn57view0  

## Historical performance of global equity indices and representative products

### FTSE All-World Index and Vanguard VWCE/VWRL

**What it is.**  
FTSE All‑World is a **developed + emerging** large/mid-cap global index (similar “shape” to MSCI ACWI). Vanguard’s **VWCE** (accumulating) is a UCITS ETF designed to track the FTSE All‑World Index; Vanguard’s own product page confirms this benchmark relationship. citeturn54view0turn55view0  

**VWCE ongoing charge / TER (critical input for long-horizon modelling).**  
Vanguard’s VWCE factsheet (31 Jan 2026) states the **ongoing charges figure is 0.19%**. citeturn55view0  
A Financial Times report also notes Vanguard cut the fee on its flagship FTSE All‑World UCITS ETF from **0.22% to 0.19%**. citeturn51news45  

**Annualised total returns (index vs fund).**  
Vanguard’s VWCE factsheet reports both fund returns (“Fonds (Na kosten)”) and benchmark returns. As at **31 Jan 2026**, benchmark annualised returns in **USD** are: **3‑year 19.03%**, **5‑year 11.97%**, **10‑year 12.73%**; “since inception” is also shown (12.75%), but note that refers to the benchmark over the period used by the factsheet—not index inception in 2000. citeturn55view0  

**What we can and cannot infer for your requested windows.**  
* Last 10 years: the FTSE All‑World benchmark figure (USD, total return) is available as **12.73% annualised** (as reported in Vanguard’s factsheet). citeturn55view0  
* Last 20 / 30 years and rolling 10/20-year ranges: the Vanguard factsheet does not provide 20‑ or 30‑year benchmark results. citeturn55view0  
* EUR equivalents: the cited VWCE factsheet performance table is in **USD**, so EUR return conversion would require either FTSE EUR total-return data or an FX-linked reconstruction. The publicly accessible sources captured here do not provide a like‑for‑like 20–30 year EUR total-return series for FTSE All‑World.

**Risk/drawdown notes.**  
The VWCE factsheet highlights that “exchange-rate fluctuations can have a negative impact” on returns (relevant for EUR-based investors in global equities). citeturn55view0  
For deep drawdown metrics, MSCI publishes max drawdown statistics in its factsheets; for FTSE All‑World, the publicly accessible Vanguard factsheet excerpt does not publish an equivalent max-drawdown table. citeturn55view0turn52view0  

### MSCI World Index and common UCITS trackers

**What it is and history.**  
MSCI World represents large/mid-cap equities across **23 developed markets**; MSCI notes the index was launched **31 Mar 1986** and earlier data is back-tested. citeturn52view0  

**Annualised total returns in EUR (net total return).**  
MSCI publishes a full EUR net-return factsheet with multiple horizons:

* **10-year annualised (net, EUR): 12.34%**  
* **Since 29 Dec 2000 annualised (net, EUR): 6.32%** citeturn52view0  

This “since 2000” window is particularly useful as it spans multiple regimes (dot-com crash aftermath, GFC, Euro crisis, COVID shock, high inflation/fast rates period).

**Calendar-year returns (useful for understanding dispersion).**  
MSCI also lists annual performance (EUR, net) for recent calendar years—e.g., **2021: 31.07%**, **2022: −12.78%**, **2023: 19.60%**, **2024: 26.60%**, **2025: 6.77%**. citeturn52view0  

**Worst drawdown and when it happened (provider-published).**  
MSCI reports **maximum drawdown since 29 Dec 2000 of 53.60%**, with the stated drawdown period **2001‑05‑24 to 2009‑03‑09**. citeturn52view0  
This is exceptionally valuable for planning because it gives you a provider-defined “worst observed peak-to-trough” in EUR terms for the full multi-decade period they publish.

**Rolling best/worst 10- and 20-year outcomes.**  
MSCI’s publicly accessible factsheet provides max drawdown and annualised returns but does **not** provide best/worst rolling 10‑year / 20‑year tables. citeturn52view0  
To compute rolling-period extremes robustly, you need a full time series of index levels (total return) in EUR. Within the sources captured here, that full series is not available in-machine-readable form.

### S&P 500 total return

**Why it matters for your modelling.**  
The S&P 500 is US-only, but it is often used as a long-history comparator and as a “best-case” developed equity market outcome. SlickCharts provides a long-run total-return series by year with dividends reinvested. citeturn57view0  

**Annual total returns by year (dividends reinvested).**  
SlickCharts lists annual total returns back to 1926, explicitly noting dividends are reinvested and explaining the pre-1957 index predecessor context. citeturn57view0  

**Annualised returns over your requested windows (computed from the annual total-return series).**  
Using the SlickCharts annual total-return series through **2025** (last full calendar year shown), the implied annualised nominal returns in USD are approximately:

* **Last 10 years (2016–2025): ~13.5% annualised** citeturn57view0  
* **Last 20 years (2006–2025): ~10.2% annualised** citeturn57view0  
* **Last 30 years (1996–2025): ~9.6% annualised** citeturn57view0  
* **Since 1926 (1926–2025): ~10.4% annualised** citeturn57view0  

These are *not* inflation-adjusted.

**Rolling best and worst 10-year and 20-year periods (computed from annual total returns).**  
Based on rolling compounded returns from the same annual series:

* Best rolling **10-year** (calendar-year windows) occurred around **1990–1999**, about **~18.6% annualised**; the worst over the full history was around **1928–1937**, about **~−3.5% annualised**. citeturn57view0  
* Best rolling **20-year** window occurred around **1979–1998**, about **~16.8% annualised**; the worst over the full history occurred around **1928–1947**, about **~2.8% annualised**. citeturn57view0  

Because many investors care more about “modern era” relevance, it’s also informative that the worst rolling **10-year** period since roughly the modern S&P 500 era (post‑1957) is around **1999–2008**, approximately **~−1.4% annualised**. citeturn57view0  

**Drawdowns and recovery time: what we can say with citations.**  
SlickCharts provides a “current drawdown” page and explains its “intra-year drawdown by year” concept, but the captured output does not provide a full historical drawdown table from which to cite “worst drawdown and recovery time” in a consistent peak‑to‑trough sense. citeturn58view0  
A conservative planning approach is therefore to treat the **Great Depression** and **Global Financial Crisis** as the key historical drawdown regimes, while recognising that long-period drawdowns depend on whether you measure intraday, month-end, or year-end, and whether you use price or total return.

## Reasonable return assumptions for a 30‑year EUR model

This section proposes three **nominal EUR** return scenarios for a globally diversified equity index allocation (e.g., MSCI World / FTSE All‑World-style exposure). The intent is to pick numbers that are (a) defensible, (b) internally consistent with long-run evidence, and (c) easy to model.

### Anchors from the evidence above

The best “EUR anchor” in the sourced materials is **MSCI World (EUR) net returns**, which reports:

* **10-year annualised: 12.34% (EUR, net)** citeturn52view0  
* **Since 29 Dec 2000 annualised: 6.32% (EUR, net)** citeturn52view0  
* **Maximum drawdown since 2000: 53.60%**, with drawdown dated **2001‑05‑24 to 2009‑03‑09** citeturn52view0  

This suggests two planning realities:
1. A “recent decade” can be very strong, but  
2. A multi-decade period that includes major crises can look closer to mid-single digits in EUR.

Also, for a **US-only** comparator, the S&P 500 total-return history shows that even long windows can vary meaningfully; rolling 20-year outcomes have historically ranged from low single digits to mid/high teens depending on the era. citeturn57view0  

### Proposed nominal EUR scenarios

**Pessimistic (defensible lower bound): 4% nominal EUR per year**  
Rationale: even though MSCI World (EUR) since 2000 shows 6.32% annualised, that period contained strong US-led equity performance and substantial tailwinds at times; a lower bound for a 30‑year forward-looking plan can prudently haircut historical outcomes for valuation starting points, potential lower dividend yields, and uncertain EUR/USD effects for a EUR investor. The existence of very weak decade outcomes in US history (including negative 10‑year windows) supports keeping a “below-average but not catastrophic” scenario in the low single digits. citeturn52view0turn57view0  

**Baseline (historically grounded expectation): 6% nominal EUR per year**  
Rationale: this is broadly consistent with MSCI World (EUR) since 2000 at 6.32% annualised (net), while leaving room for tracking difference, product costs, and the possibility that the next 30 years are not as favourable as the strongest decades in the record. citeturn52view0  

**Optimistic (above-average but historically plausible): 8% nominal EUR per year**  
Rationale: this is below the strongest recent 10‑year MSCI World (EUR) outcome (12.34%) but above the 2000‑to‑present multi-decade outcome. It also sits comfortably below the best long historical S&P 500 rolling windows. citeturn52view0turn57view0  

### What these scenarios imply for monthly investing over 30 years

Ignoring taxes during accumulation and assuming constant net returns (after product fees and tracking difference), the future value of contributions is roughly:

*At 4% nominal:* ~€685k (at €1,000/month) to ~€1.03m (at €1,500/month)  
*At 6% nominal:* ~€975k to ~€1.46m  
*At 8% nominal:* ~€1.41m to ~€2.11m  

These figures are purely mechanical compounding illustrations to help you frame “rent and invest” affordability and risk capacity; real sequences will vary materially (as implied by the drawdowns and rolling-return dispersion above). citeturn52view0turn57view0  

## Fees and platform costs that matter over 30 years

### TER/OCF for VWCE and comparable equity-index exposure

**VWCE (Vanguard FTSE All‑World UCITS ETF, accumulating).**  
Vanguard’s VWCE factsheet (31 Jan 2026) lists **ongoing charges: 0.19%**. citeturn55view0  

**“Was it 0.22%?”**  
A Financial Times report describes Vanguard cutting the fee from **0.22% to 0.19%** for its flagship FTSE All‑World UCITS ETF. citeturn51news45  
Practical implication: when modelling over 30 years, you should treat TER/OCF as **subject to change** and re-check before implementation.

**Comparable global equity UCITS ETFs.**  
I did not pull a complete comparable-ETF list with verified OCFs from primary KIDs in the remaining tool budget. In practice, the common “global equity” ETF set in Europe includes FTSE All‑World and MSCI ACWI / MSCI World trackers from Vanguard, iShares, SPDR, Amundi, Xtrackers, etc.; you should model (and choose) based on **OCF + tracking difference + trading costs + tax implementation fit**.

### Index funds (*fondos indexados*) offered in Spain: fee structure signals

**MyInvestor (platform-level statement).**  
MyInvestor’s “Fondos indexados” landing page (as captured in the snippet) states: **no custody fees**, “only 0.30% management fee”, and a **maximum total cost (TER) of 0.59% per year** for its offering of index funds from Vanguard, iShares, Fidelity, Amundi, and NN. citeturn51search5  

This is crucial for Spain because *fondos de inversión* can carry the **“traspaso” tax deferral** (discussed below), which can matter more than a few basis points of TER depending on how often you rebalance or de-risk.

**MyInvestor / BlackRock (iShares) partnership (fee datapoints).**  
A CincoDías report on MyInvestor’s BlackRock alliance (as summarised in the snippet) cites examples like an **iShares Developed World Index fund with TER 0.10%** (class C), and reiterates the “no trading / transfer / custody fees” positioning for these funds. citeturn51news46  

### How much a TER difference costs over 30 years with €1,000–€1,500/month

Small annual fee differences compound into meaningful money because they apply to an ever-growing asset base.

Assuming the underlying market delivers **7% nominal per year before product fees**, and fees reduce returns one-for-one (a simplification, but directionally useful), the difference between **0.19–0.22% vs 0.50%** is material.

Illustrative comparison (7% gross, 30 years, monthly investing):

* €1,000/month:  
  * ~€1.12m with 0.22% TER vs ~€1.07m with 0.50% TER → **~€56k** difference  
* €1,500/month:  
  * ~€1.68m with 0.22% TER vs ~€1.60m with 0.50% TER → **~€84k** difference  

The exact figures vary with market returns; for gross 5% the gap is smaller (~€37k on €1,000/month), and for gross 9% it is larger (~€84k on €1,000/month). These figures are modelling illustrations to quantify “fee drag” over long horizons. (Fee levels for VWCE itself are sourced above.) citeturn55view0turn51news45  

### Broker/platform costs in Spain: what could be verified here

**Openbank (platform-level statement).**  
Openbank’s investments page claims for funds: “No transfer, subscription, redemption or custody fees” and also advertises access to “over 1,000 ETFs”. citeturn51search2  

**Degiro / Interactive Brokers:**  
Within the remaining source budget, I could not pull and verify up-to-date 2026 fee schedules for Degiro Spain and Interactive Brokers and therefore will not assert specific numbers. The practical guidance is to separate:
- One-off costs: trading commissions, FX conversion costs, exchange connectivity fees  
- Ongoing costs: custody, inactivity, data subscriptions  
…and model them conservatively as a small annual drag (or choose platforms where they are near-zero for your use case).

## Spanish tax treatment for a Spanish tax resident investing in equities

This section focuses on **IRPF savings income**, the **fondo “traspaso” regime**, dividend taxation, and wealth/solidarity taxes relevant to the Valencian Community.

### Capital gains and savings-income tax rates in 2025/2026

**Savings income brackets (rendimientos del ahorro / base liquidable del ahorro).**  
From **1 January 2025**, Spain increased the *top marginal* rate applicable to savings income. Multiple professional summaries tie this change to **Ley 7/2024** and describe an increase of the last bracket to **30%** for savings income above **€300,000**. citeturn41search0turn41search2turn41search6  

A commonly used consolidated “combined scale” (state + regional) for savings income from 2025 onward is:

- Up to **€6,000**: **19%**  
- **€6,000–€50,000**: **21%**  
- **€50,000–€200,000**: **23%**  
- **€200,000–€300,000**: **27%**  
- Over **€300,000**: **30%** citeturn50search7turn41search2  

**Important nuance (state vs autonomous components).**  
AEAT’s INFORMA note indicates, for example, that from 2025 the *autonomous* component’s last bracket increased (e.g., “del 14 al 15 por ciento”), which is consistent with reaching a 30% combined top marginal rate when paired with the state component. citeturn41search6turn50search1  

### How gains are calculated and cost-basis method

For **homogeneous securities**, Spain applies a **FIFO** rule (first acquired = first deemed sold). Article-level summaries of Ley 35/2006 explain that when there are “valores homogéneos” (homogeneous units), the transmitted/redeemed units are deemed those acquired first. citeturn50search4  

Practical consequence for your monthly DCA plan:  
If you sell part of an ETF position after decades, FIFO typically means you sell your **oldest, most-appreciated lots first**, realising a relatively high gain per euro sold—unless you manage sales across multiple funds/ISINs.

### ETFs vs *fondos de inversión*: the “traspaso” advantage and why it matters

**Core concept: tax deferral on fund-to-fund switches.**  
Spain has a well-known regime where transfers between qualifying collective investment schemes (*IIC*, typically mutual funds / *fondos de inversión*) can be done as a **“traspaso”** without crystallising a capital gain at the time of the switch, allowing tax to be deferred until final redemption.

**Why ETFs are treated differently.**  
AEAT explicitly highlights that Ley 11/2021 modified **Article 94** of the IRPF law “to homogenise” the treatment of investments in certain *instituciones de inversión colectiva* known as **ETFs**, regardless of whether they are listed on Spanish or foreign markets. citeturn50search2  
This is the administrative underpinning of the practical rule most Spanish investors live by: **selling an ETF is a taxable event**, and “switching” from one ETF to another is not a tax-neutral *traspaso*.

**Does this make *fondos* strictly better than ETFs for long-term DCA?**  
Not strictly, but often **structurally advantageous** in Spain—because what matters is not only the long-run gross return, but how much tax you pay *en route* when you:
- rebalance between regions (e.g., World vs EM),
- switch providers,
- reduce risk near retirement (equities → bonds),
- or change strategy.

With **ETFs**, these changes typically require sales and create **tax leakage** at each change. With **qualifying mutual funds**, you can often make these transitions without immediate tax. citeturn50search2  

**When ETFs can still be fine (even in Spain).**  
If your plan is “buy one global accumulating ETF and hold for 30 years, then gradually sell”, the *traspaso* advantage is less critical during the accumulation phase. It becomes more important if you expect to do major switches.

### Tax on dividends and the (usually) better Spanish tax profile of accumulating vehicles

**Dividends are savings income.**  
Dividends and capital gains are both generally part of the savings income base that is taxed at the progressive savings rates shown above. citeturn50search7turn41search2  

**Accumulating vs distributing: Spanish personal-tax timing.**
- A **distributing** ETF/fund pays dividends to you; you generally recognise taxable savings income when paid.
- An **accumulating** ETF/fund reinvests internally, which typically means you are taxed primarily when you sell (via capital gains).

Therefore, for a Spanish tax resident building wealth, **accumulating share classes usually improve tax deferral**, even though you still bear any withholding taxes at source inside the fund structure.

### Wealth tax in the Valencian Community and the solidarity tax

#### Impuesto sobre el Patrimonio in the Valencian Community

Valencian-specific rules are set in **Ley 13/1997** (articles 8 and 9), and recent changes were enacted via **Ley 5/2025** (Valencian measures law). citeturn48view0turn44view0turn45view1  

**Minimum exempt threshold (mínimo exento) in Valencia.**  
The BOE text shows that for taxpayers resident in the Valencian Community under “obligación personal”, the base is reduced by **€1,000,000** as the mínimo exento. citeturn49view3turn45view1  
Ley 5/2025 specifies this applies for events/devengo from **31 December 2025** (i.e., affecting the filing in 2026 for wealth held at 31 Dec 2025). citeturn45view3turn44view0  

**Valencian wealth-tax rate schedule.**  
Ley 13/1997 provides the progressive scale, starting at **0.25%** and reaching **3.5%** above €10,695,996.06 (as shown in the scale). citeturn49view1turn49view3  

**When does it become relevant for your plan?**  
Roughly speaking, it becomes relevant once your **net taxable wealth** (after exemptions, debts, etc., and after the mínimo exento) exceeds the threshold. Since your plan could plausibly reach ~€1–€2m over 30 years depending on returns, it is realistic that wealth tax could become a consideration—especially if you hold additional assets (home equity, other investments). The precise base depends on exemptions and valuation rules under the wealth tax law.

#### Impuesto Temporal de Solidaridad de las Grandes Fortunas

Spain introduced the “solidarity tax” as a **state-level complementary wealth tax**.

**Who it targets and starting point.**  
Ley 38/2022 describes it as a complementary tax aimed at **net wealth above €3,000,000**, with the first **€3,000,000** taxed at **0%**. citeturn61view0turn61view2  

**Rates (as set out in Ley 38/2022).**  
The law provides a progressive schedule:

- Up to €3,000,000: **0%**  
- €3,000,000 to €5,347,998.03: **1.7%**  
- €5,347,998.03 to €10,695,996.06: **2.1%**  
- Above €10,695,996.06: **3.5%** citeturn61view2turn61view3turn61view4  

**Interaction with wealth tax.**  
Ley 38/2022 explains its complementary nature and the mechanism of avoiding double taxation by **deducting wealth tax actually paid** against the solidarity tax. citeturn61view0turn61view2  

### Exit scenario framework after 30 years: estimating the tax bill

When you sell after 30 years, your tax bill depends on:

1. **Sale proceeds**  
2. **Tax cost basis** (sum of acquisition costs for the lots sold; FIFO for homogeneous securities) citeturn50search4  
3. **Total realised gain** = proceeds − basis  
4. Apply the **savings income tax scale** to the realised gain (plus any other savings income in that year) citeturn50search7turn41search2  

A simple rule-of-thumb to model:

- Let portfolio market value be **X**  
- Let total contributions (cost basis) be **C**  
- If selling everything (simplification): gain **G = X − C**  
- Approximate effective CGT rate **t(G)** using the progressive brackets

Then estimated tax ≈ **Tax(G)**.

Example bracket logic (2025+ combined rates): first €6k at 19%, next €44k at 21%, next €150k at 23%, next €100k at 27%, remainder at 30%. citeturn50search7turn41search2  

**Planning implication:** If you are likely to realise large gains, you can reduce the effective rate by **spreading sales across multiple tax years**, rather than liquidating everything at once.

## Inflation context for converting nominal to real

### Spain inflation history: what we can cite here

The ECB Data Portal offers a time series for Spain’s HICP inflation rate (timeline shown from **January 1996 to December 2025**). citeturn51search3  
Spain’s national statistics office (INE) also publishes CPI releases and current annual rates (e.g., flash estimate notes). citeturn51search11  

Within the constrained tool budget, I did not extract a full annual table to compute an exact 20–30 year average. Practically, for long-horizon personal modelling, many planners use **~2%–3%** as a reasonable “long-run inflation” working range for Spain/euro area, and then perform sensitivity analysis.

### ECB’s long-term inflation target

The ECB’s monetary policy strategy (2020–21 review, published July 2021) states it adopted a **symmetric 2% inflation target over the medium term**. citeturn56search2  

This target is often used as a planning benchmark for “expected inflation” in long-run real-return calculations in the euro area, with the caveat that realised inflation can deviate significantly for multi-year periods.

---

**Bottom line for a Spain-based “rent and invest” plan:**  
The deepest structural decision is not whether global equities have historically compounded—both MSCI and long-run US evidence show strong long-run nominal returns but with severe drawdowns. citeturn52view0turn57view0 The deepest Spain-specific decision is **implementation**: ETFs are cost-efficient (VWCE OCF ~0.19%), citeturn55view0turn51news45 but *fondos de inversión* can offer **tax-deferral via traspasos**, which can be highly valuable if you will rebalance or de-risk over time. citeturn50search2turn51news46