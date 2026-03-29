# Residential property price trends and long‑range projections for coastal flats in Castellón province

## Scope, data choices and how to read the numbers

This report focuses on **coastal flats (apartments) in Castellón province** (Comunitat Valenciana, Spain), with practical attention to the main coastal markets you cited: **Benicàssim, Oropesa del Mar, Peñíscola and Vinaròs**, plus province‑level context for when coastal‑specific data is incomplete.

Long-range projections (10–30 years) are inherently uncertain, so the goal here is a **historically grounded baseline** plus a **defensible scenario range**, not a single “correct” forecast.

Key point: “house prices” is not one dataset. For Spain you will encounter three common price concepts:

**Appraisal/valuation €/m² (tasación / valor tasado)**: based on valuations carried out by appraisal companies. It is often smoother than transactions and can cover long histories. Here we use the official **“Estadística de Valor Tasado de Vivienda”** for long-run provincial €/m² (quarterly, back to 1995). citeturn30search1turn30search2turn21view0  

**Transaction price indices**: quality-adjusted indices based on observed sale prices (e.g., INE’s Housing Price Index, IPV/HPI). These give reliable **growth rates** and cycle timing, but are indices rather than €/m² levels (and are at autonomous-community resolution, not municipality/province). citeturn51search2turn50view0  

**Asking prices (listing €/m²)**: commonly from portals (e.g., idealista). These are **not** final sale prices; they reflect seller expectations and can be sensitive to sample mix. They *do* provide useful municipality-level time series and up-to-date “market temperature”, but must be treated as a complementary view. Also note idealista explicitly flags a **methodology change from March 2023**, which can introduce a structural break in comparisons. citeturn38view0turn39view0turn41view0turn42view0turn43view0  

In short:  
- Use **official appraisal €/m²** for the *30-year backbone*.  
- Use **INE IPV** for *cycle confirmation* and macro comparability.  
- Use **idealista municipalities** to understand *coastal dispersion and relative momentum*, with suitable caveats.

## Historical price evidence for Castellón and coastal municipalities

### Province-level €/m² back to 1995 with the 2008 crash, recovery, COVID and post‑2020 surge

The official appraisal series (“valor tasado medio €/m² de vivienda libre”) provides a quarterly €/m² history from **1995 Q1 to 2025 Q4** for Spain, autonomous communities and provinces. citeturn30search1turn21view0turn30search2  

Selected reference points from that official series (€/m²; vivienda libre; total):

| Period (official appraisal series) | Spain €/m² | Comunitat Valenciana €/m² | Castellón province €/m² |
|---|---:|---:|---:|
| 1995 Q1 | ~642 | ~562 | ~448 |
| 2005 Q4 (late-bubble build-up) | ~1,817 | ~1,523 | ~1,554 |
| Bubble peak (Spain peak 2008 Q1; Castellón peak earlier) | ~2,101 (2008 Q1) | ~1,698 (2008 Q2) | ~1,761 (2007 Q3) |
| Post-crash trough | ~1,456 (2014 Q3) | ~1,115 (2014 Q1) | ~1,022 (2015 Q1) |
| 2019 Q4 (pre-COVID) | ~1,653 | ~1,232 | ~1,067 |
| 2020 Q4 (COVID year-end) | ~1,622 | ~1,218 | ~1,051 |
| 2025 Q4 (latest) | ~2,230 | ~1,806 | ~1,367 |

All values above come from the official appraisal €/m² series described in the government dataset documentation and delivered via the ISTAC open-data cube for Spain/CCAA/provinces. citeturn30search1turn21view0turn30search2  

What these points show in plain English:

- **Castellón’s bubble peak (2007 Q3) and subsequent correction were sharper and longer than Spain overall** (details and rates in later sections). citeturn30search1turn21view0  
- **COVID produced a mild year-end dip** in this appraisal series (2019 Q4 → 2020 Q4): about **‑1.5%** for Castellón, similar magnitude to Spain. citeturn30search1turn21view0  
- The **post‑2020 phase is a strong upswing**: by 2025 Q4 Spain and Comunitat Valenciana are at new highs in this series, and Castellón is rising fast—though still structurally cheaper than the national and regional averages. citeturn30search1turn21view0  

### Municipality and coastal specificity: what we can (and cannot) do

Official long-run **province €/m²** is strong. Official long-run **coastal-municipality €/m²** is much thinner in public sources.

For municipalities, **idealista’s listing €/m²** provides consistent, accessible historical tables (monthly) for Castellón province and for coastal municipalities including Benicàssim, Oropesa del Mar, Peñíscola and Vinaròs. citeturn38view0turn39view0turn41view0turn42view0turn43view0  

Limitations you should be aware of:

- **Small-market “n.d.” gaps**: some municipalities have missing early years (e.g., Benicàssim shows many “n.d.” entries in 2006–2008). citeturn39view0turn40view2  
- **Listing prices, not closing prices**: the level is typically above transaction prices and can be influenced by listing mix. citeturn39view0turn41view0turn42view0turn43view0  
- **Methodology change since March 2023**: treat pre/post comparisons with caution, especially for precise CAGR calculations. citeturn38view0turn39view0turn41view0  

Despite that, municipal listing series are still valuable for **relative coastal vs non-coastal dispersion**, and for cross-town comparisons.

### Current coastal price levels and recent-cycle context (asking €/m²; idealista)

Latest available month in the captured pages is **February 2026**:

- **Castellón province:** **€1,526/m²** (asking; Feb 2026). citeturn38view0  
- **Benicàssim:** **€2,796/m²** (asking; Feb 2026). citeturn39view0  
- **Oropesa del Mar:** **€2,004/m²** (asking; Feb 2026). citeturn41view0  
- **Peñíscola:** **€2,204/m²** (asking; Feb 2026). citeturn42view0  
- **Vinaròs:** **€1,683/m²** (asking; Feb 2026). citeturn43view0  

This already quantifies a key structural fact: **prime coastal towns (Benicàssim, Peñíscola) price far above the Castellón provincial average**, consistent with tourism/second home dynamics.

## What has driven prices in coastal Castellón, and what makes it structurally different

### Demand composition: domestic tourism and second homes matter more than in Alicante/Málaga-style “international coast” models

A practical way to see the tourism mix difference within the Comunitat Valenciana is the **tourist apartment overnight stays** (pernoctaciones) by province.

In **2023 tourist-apartment pernoctaciones**, the Generalitat Valenciana statistical portal shows:

- **Alicante:** 8,745,097  
- **Castellón:** 1,868,348  
- **Valencia (province):** 1,749,583  

And crucially, in 2023 **non-resident** tourist-apartment pernoctaciones were vastly different:

- **Alicante:** 5,859,558  
- **Castellón:** 423,544  
- **Valencia:** 764,255 citeturn57search0  

Interpretation: **Castellón’s coastal demand has historically been more domestic-heavy** than Alicante’s (Costa Blanca), which is a classic foreign-tourism and foreign-buyer magnet. This tends to correlate with (i) lower prices than the “globalised” coasts, but also (ii) potentially less sensitivity to single-source foreign demand shocks.

### Foreign buyers: meaningful, but with a different profile than the stereotypical UK-focused Costa Blanca story

Notarial statistics for Castellón province show foreigners are a **significant share of purchases**:

From the notarial “Compraventa de Inmuebles de la provincia de Castellón” table, annual totals (2018–2024) imply foreigners were roughly **18%–23% of purchases** (depending on year), with **2024 around 21%** (3,161 foreign vs 11,727 Spanish) and **2025 H1 around 21%** (1,713 foreign vs 6,543 Spanish). citeturn34view0  

At municipality level (foreign purchases **up to Q2 2025**), the notarial “Detalle por municipios” tables show foreign purchase counts and nationalities in key coastal towns:

- **Oropesa del Mar:** **188** foreign purchases (to Q2 2025) citeturn34view3  
- **Peñíscola:** **111** citeturn34view3  
- **Vinaròs:** **98** citeturn34view3  
- **Benicàssim:** **28** citeturn35view1  

The same tables highlight nationalities with notable presence (e.g., Romania and France appear frequently across several municipalities). citeturn34view3turn35view0turn35view1  

Takeaway: foreign demand exists, but **coastal Castellón may have a broader European mix** and (based on the tourism data above) a weaker dependence on large-scale non-resident tourism than Alicante.

### Accessibility and infrastructure: gradual but important improvements

Two infrastructure-related developments are especially relevant for long horizon housing demand:

The **AP‑7 toll removal** (Tarragona–Alicante corridor, which runs through Castellón’s coastal axis) became a major accessibility shift. The Spanish government confirmed the AP‑7 between Tarragona and Alicante would be toll-free from **1 January 2020** when the concession ended. citeturn58search6  

The **Airport of Castellón** has moved from “limited utility” to a meaningful, growing regional airport. Reports indicate it reached about **304,493 passengers in 2025** and expanded route offerings (14 routes in 2025; more planned for 2026). citeturn55search3turn55search1  

Why this matters: better access can lift second-home and retirement demand and shorten the “psychological distance” for weekend and seasonal use—especially for coastal flats marketed as lifestyle assets.

### National-level structural driver: housing supply bottlenecks, but Castellón is not always the epicentre

At the Spain level, both the OECD and Banco de España emphasise **supply bottlenecks** as a structural reason for recent price pressure.

The OECD Economic Survey for Spain notes persistent **housing supply bottlenecks in high-demand areas** pushing prices up and highlights the need to expand supply (e.g., faster land development and more social housing). citeturn44search3  

Banco de España’s 2024 Annual Report (Box on recent housing dynamics) quantifies a **cumulative supply–demand gap of ~400k–450k housing units between 2022 and 2024**, and notes the mismatch is “particularly significant” in **Madrid, Barcelona, Valencia, Alicante and Málaga**. citeturn48view1turn48view4  

Implication for Castellón coast:  
- The macro environment is supportive of prices (tight supply),  
- but **Castellón is not explicitly named among the highest-pressure provinces**, which argues for **more conservative baseline appreciation assumptions** than Costa Blanca/Costa del Sol hotspots.

### Regulatory environment affecting coastal flats: tourist rentals tightening in the Valencian Community

For coastal flats, the ability to generate seasonal income can materially affect buy/hold decisions. The Valencian Community has materially tightened the framework for **viviendas de uso turístico (VUT)**.

Europa Press reports that **Decree‑law 9/2024** modified regulations on tourist-use housing, including stronger municipal powers to limit use, and added/clarified requirements (with a transition period mentioned for adaptation). citeturn59search2  

The Generalitat Valenciana’s tourism page documents a broad clean-up process for VUT registrations (e.g., cancellations when required identifying data such as cadastral reference/NIF/NIE are missing, with referenced resolutions and procedures). citeturn59search5  

This is a **non-trivial risk factor** for “buy to holiday-let” strategies in coastal towns, and it increases the value of doing due diligence on (i) urban compatibility, (ii) building/community rules, and (iii) registration compliance.

## Historical appreciation rates and slump durations

### Castellón province versus Spain and Comunitat Valenciana using the official appraisal €/m² backbone

Using the official appraisal €/m² series (quarterly; vivienda libre; total), here are **compound annual growth rates (CAGR)** for key windows:

| Geography | CAGR 10y (2015 Q4 → 2025 Q4) | CAGR 20y (2005 Q4 → 2025 Q4) | Post-crash trough | CAGR trough → 2025 Q4 | CAGR 1995 Q1 → 2025 Q4 |
|---|---:|---:|---|---:|---:|
| Spain | ~4.1%/yr | ~1.0%/yr | 2014 Q3 | ~3.9%/yr | ~4.0%/yr |
| Comunitat Valenciana | ~4.6%/yr | ~1.0%/yr | 2014 Q1 | ~4.2%/yr | ~4.4%/yr |
| Castellón province | **~2.5%/yr** | **~‑0.6%/yr** | 2015 Q1 | **~2.7%/yr** | ~3.7%/yr |

These are calculated from the official appraisal €/m² values for the indicated quarters. citeturn30search1turn21view0turn30search2  

Interpretation:

- Castellón’s **last decade CAGR (~2.5%)** is positive but **well below** Spain and the regional average in this appraisal series. citeturn30search1turn21view0  
- The **20-year window is negative** for Castellón because it starts in the late bubble (2005 Q4) and ends in a period that, while rising, still does not fully “beat” that bubble level in this series. This is a reminder that **multi‑year stagnation is not hypothetical**—it already happened. citeturn30search1turn21view0  

### How deep was the crash in Castellón, and how long did it last?

Peak-to-trough metrics (bubble peak defined as the maximum within 2000–2010; trough as the minimum after 2008 Q1) from the official appraisal series:

| Geography | Bubble peak | Peak €/m² | Post-crash trough | Trough €/m² | Peak → trough | Duration |
|---|---|---:|---|---:|---:|---:|
| Spain | 2008 Q1 | ~2,101 | 2014 Q3 | ~1,456 | ~‑31% | ~6.5 yrs |
| Comunitat Valenciana | 2008 Q2 | ~1,698 | 2014 Q1 | ~1,115 | ~‑34% | ~5.8 yrs |
| Castellón province | **2007 Q3** | ~1,761 | **2015 Q1** | ~1,022 | **~‑42%** | **~7.5 yrs** |

This highlights that **Castellón’s downturn was both deeper and longer** on this metric. citeturn30search1turn21view0  

### Coastal municipality momentum in the last decade using asking €/m²

Because robust 20–30 year *transaction* €/m² series at municipal level are not consistently available publicly, the following is an **asking-price** view using idealista monthly tables.

10-year CAGRs from **February 2016 to February 2026** (asking €/m²):

| Area (asking prices) | Feb 2016 €/m² | Feb 2026 €/m² | Approx. CAGR (10y) |
|---|---:|---:|---:|
| Benicàssim | 1,741 citeturn40view0 | 2,796 citeturn39view0 | ~4.9%/yr |
| Oropesa del Mar | 1,462 citeturn52view0 | 2,004 citeturn41view0 | ~3.2%/yr |
| Peñíscola | 1,473 citeturn52view2 | 2,204 citeturn42view0 | ~4.1%/yr |
| Vinaròs | 1,228 citeturn52view3 | 1,683 citeturn43view0 | ~3.2%/yr |
| Castellón province (asking) | 1,069 citeturn52view4 | 1,526 citeturn38view0 | ~3.6%/yr |

Important caveats: these are **listing prices**, and idealista flags a **methodology change since March 2023**, so treat the CAGRs as indicative rather than exact. citeturn38view0turn39view0  

Even with that caveat, the pattern is consistent with intuition: **prime coastal destinations (especially Benicàssim and Peñíscola) have outpaced the provincial average** in the last decade’s asking-price dynamics.

## Thirty-year scenario framework with projections for €250k and €200k flats

### Choosing defensible annual appreciation rates

It is useful to anchor long-run nominal appreciation to at least three reference lines:

Castellón official appraisal €/m²:  
- **~2.5%/yr** over the last decade (2015 Q4 → 2025 Q4). citeturn30search1turn21view0  
- **~2.7%/yr** from the post-crash trough (2015 Q1 → 2025 Q4). citeturn30search1turn21view0  
- **~3.7%/yr** across the full 1995–2025 history (note: includes a low starting base and different macro regimes). citeturn30search1turn21view0  

Macro reality check: Spain overall has had strong post-2014 real price growth and recent acceleration, with supply-demand mismatch a key factor per Banco de España and OECD. citeturn48view4turn44search3  

Given this, a reasonable scenario set for **nominal** annual appreciation might be:

Pessimistic **1.0%**: allows for long stagnations like “bubble hangover”, demand softness, demographic headwinds, or regulatory/climate risk repricing—consistent with the idea that 20-year windows can be flat/negative in Castellón depending on start point. citeturn30search1turn21view0  

Baseline **2.5%**: approximately aligned to Castellón’s official last‑decade CAGR. citeturn30search1turn21view0  

Optimistic **4.0%**: closer to long-run nominal growth (and not far from Spain’s long-run CAGR in the same official dataset), and could be justified if (i) supply constraints persist, (ii) accessibility improvements (AP‑7, airport) compound, and (iii) coastal lifestyle demand stays strong. citeturn30search1turn21view0turn58search6turn55search3turn48view4  

### Value projections under three scenarios

Assumptions: compound growth, no transaction costs, no taxes, no renovations, no rental income, and no vacancy—pure price appreciation only.

| Scenario (annual nominal) | Start | Year 10 | Year 20 | Year 30 |
|---|---:|---:|---:|---:|
| Pessimistic (1.0%) | €250,000 | €276,156 | €305,048 | €336,962 |
| Pessimistic (1.0%) | €200,000 | €220,924 | €244,038 | €269,570 |
| Baseline (2.5%) | €250,000 | €320,021 | €409,654 | €524,392 |
| Baseline (2.5%) | €200,000 | €256,017 | €327,723 | €419,514 |
| Optimistic (4.0%) | €250,000 | €370,061 | €547,781 | €810,849 |
| Optimistic (4.0%) | €200,000 | €296,049 | €438,225 | €648,680 |

How to interpret: if long-run inflation averages ~2% (an order-of-magnitude reference consistent with many developed-economy targets), then **2.5% nominal is only ~0.5% real**. That is often a more realistic “anchoring” mindset for 30-year planning than focusing on nominal numbers alone. citeturn44search4  

## Caveats and risks that could make projections materially wrong

### Dataset and measurement risks

Mixing appraisal €/m², asking €/m², and index measures can lead to false precision. The official appraisal series is built from valuation-company tasations (not every sale), while idealista is listings and INE IPV is a quality-adjusted transaction index. You should not expect these to match in level or even in short-run dynamics. citeturn30search1turn38view0turn51search2  

Municipal thin‑market noise: several coastal towns show missing early years (“n.d.”) and can have volatile changes, suggesting sample-size sensitivity. citeturn39view0turn42view0turn43view0  

### Macro and financial-condition risks

Rates and credit: Spanish housing is sensitive to mortgage conditions. A prolonged period of high real interest rates (or reduced credit availability) would compress affordability and could flatten prices for years, as seen historically after 2008.

Supply response: Spain’s housing market is currently discussed in terms of supply bottlenecks, but if planning reforms, build-to-rent expansion, or a construction rebound occur, appreciation could slow. Banco de España highlights supply shortfalls and the difficulty of meeting demand in certain provinces; if that pressure diffuses, coastal Castellón’s “relative value” story could change in either direction. citeturn48view4turn44search3  

### Valencia-specific and coastal-specific regulatory risks

Tourist-rental regulation: tighter VUT rules and registry enforcement can reduce expected returns for coastal flats used as short-term rentals, lowering the “investor bid” portion of demand. The Decree‑law 9/2024 changes and the subsequent registry clean-up actions are directly relevant. citeturn59search2turn59search5turn59search1  

Community/building restrictions: even if regional law permits, building communities can impose constraints in some cases—this is due diligence rather than a data series issue, but it changes realised ROI.

### Climate, flood and coastal erosion risks

Flood risk mapping is not abstract in the Valencian Community. The Generalitat Valenciana maintains PATRICOVA cartography and documentation for flood risk prevention planning. citeturn60search2turn60search5  

At national level, MITECO’s **SNCZI** provides a cartographic flood-risk system intended to support spatial planning and citizen awareness (including an online map viewer). citeturn61search0  

Longer-term, the IPCC AR6 WG2 Mediterranean cross‑chapter synthesis projects **Mediterranean sea level rise continuing through coming decades and centuries** (e.g., indicative ranges around **0.3–0.6m by 2100 under lower-emissions pathways and 0.6–1.1m under high-emissions**, relative to 1995–2014) and states coastal flood risks will increase in low‑lying Mediterranean areas. citeturn61search5  

Why this matters for a coastal flat purchase with a 30-year view:
- Increased expected flood/erosion risk can affect **insurance cost/availability**, building maintenance, and eventually **market pricing of risk**.  
- The impact will not be uniform: micro-location (elevation, shoreline protection, drainage) and building characteristics dominate outcomes—so PATRICOVA/SNCZI checks are part of prudent comparables analysis, not a generic “climate discount” assumption. citeturn60search5turn61search0turn61search5  

### Demographic and demand-composition risks

Castellón’s coastal demand appears more domestically anchored than Alicante’s in tourism-apartment data, which can be stabilising—but it could also cap upside if international demand surges elsewhere. citeturn57search0  

Foreign demand can shift with exchange rates, geopolitics, visa/tax policy, and airline connectivity. The notarial municipal tables show foreign-buyer presence in key towns, but the profile (nationalities, volumes) can change over time. citeturn34view3turn35view1  

### A practical way to use this report for your own “realistic baseline” model

For a conservative long-horizon underwriting model for a coastal flat in Castellón province:

Use **2.5% nominal** as a baseline (historically consistent with Castellón’s official last-decade CAGR), and test sensitivity to **1%** and **4%**. citeturn30search1turn21view0  

Then explicitly stress-test:
- A 5–8 year stagnation segment (Castellón’s last cycle shows long stagnations are plausible). citeturn30search1turn21view0  
- A “tourist rental tightening” case (if VUT income is part of your thesis). citeturn59search2turn59search5  
- A “coastal risk repricing” case by checking the property against **PATRICOVA** and **SNCZI** flooding layers. citeturn60search5turn61search0  

These steps turn an uncertain 30-year outlook into a structured, testable range that is consistent with the region’s historical boom-bust experience and today’s regulatory and climate context.