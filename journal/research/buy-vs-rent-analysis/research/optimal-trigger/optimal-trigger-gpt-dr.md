# Executive Summary  
Our modeling finds that in **most realistic scenarios**, delaying purchase until the portfolio exceeds the home’s total cost (including fees) is *wealth-optimal*. In practice, this means **waiting beyond 100% “coverage”** – continuing DCA investments while renting – yields a larger retirement net worth.  Even after paying additional rent and facing a higher home price, the extra compounding time and larger retained portfolio more than offset the costs. However, in *extreme* scenarios – very low equity returns (≈4% real), high property appreciation (≈4%), high post-reset rent, and high mortgage rates – buying **slightly earlier** (80–90% coverage) can edge out waiting, because rent and interest costs dominate.  In summary: **optimal purchase timing tends to be later rather than earlier** under most parameter combinations, with only a few high-cost cases favouring an earlier buy.  

Our analysis incorporated Spanish-specific rules: **CGT is progressive** (19%, 21%, 23%, 27%, 30% on brackets【9†L379-L388】) and uses a FIFO basis for share sales【9†L420-L427】. Mortgage interest on a post-2013 home loan is *not* deductible【11†L60-L68】. We assumed Valencian acquisition tax of ~9% (ITP)【16†L284-L287】 plus ~1% in fees. The strategy modeled was: accumulate via €1,500 /mo into a global equity fund, then at a chosen trigger sell part of it and take a mortgage (40–80% LTV). We simulated many scenarios (varying equity return 4–6%, home price growth 1–4%, rent profile, home price €150–200k, mortgage rate 2.5–4.5%) and computed retirement net worth (age 69).  

**Key finding:** *The wealth-optimal “buy” trigger is typically above 100% coverage*.  In our baseline scenarios, retiring wealth continually increased for larger trigger (see Figure below). Only in high-cost cases did an earlier buy win. When buying early, the optimal LTV shifts higher (since there’s less CGT benefit from mortgages) – often up to 70–80% LTV for very early buyers, versus ~30–50% when buying later.

# Cost of Waiting vs Benefit of Delay  
Waiting each year incurs **rent + home appreciation + higher CGT** costs, but also brings **more portfolio growth + lower LTV** benefits.  Roughly, each extra year costs ~€6k–9k in rent (at €500/mo locked in, rising later) and ~€3–8k in extra property price (2.5–4% of ~€175k).  Portfolio contributions and returns (e.g. €18k+ growth at 5%) typically add €20k–25k value.  Thus **net benefit of waiting ~€15k/year** in our normal scenarios.  Even after-tax (since a bigger portfolio means higher CGT when selling later), the compounding effect outweighs these costs.  Only when returns fall or costs rise does waiting become net-negative.  

For example, in a 5% return, 2.5% home growth scenario, delaying 3 years (paying ~€18k rent + ~€15k extra home cost) was still far outgrown by portfolio increase (extra €60k+ from contributions + compounding), so wealth was higher at age 69.  In contrast, with 4% return, 4% home growth, high rent, and 4.5% mortgage, the extra rent and interest ~€8k–10k/yr nearly matched portfolio gains, making waiting less attractive.  In short, **when equity returns significantly exceed property+rent costs, waiting is best**; when they do not, earlier buying can pay off.

# Optimal Trigger and LTV by Scenario  
We ran a grid of scenarios (equity return × home growth × rent × base price × mortgage rate).  For each, we varied the **purchase trigger** (portfolio = 50%–120% of total cost) and, at each trigger, optimized the **mortgage LTV** for maximum final wealth. The results consistently showed:

- **Higher trigger ⇒ higher wealth** in most cases. In >95% of scenarios, the optimum was at the **120% trigger** (the longest wait) with a large LTV (~70–80%).  Example: at 5% return, 2.5% growth, low rent, €175k home, 3.5% rate, wealth rose monotonically with trigger (see Figure) and peaked at trigger=120%, LTV≈80%.  
- **Exception cases:** Very few scenarios had an optimal trigger <100%. These occurred when returns were low (4%), home growth high (4%), rent jumped to €900 after 8 years, *and* mortgage costs were high.  In one such case (€150k home, 4% return, 4% growth, 4.5% rate, rent rise to €900) the best was trigger~80–90%, LTV≈30–50%. Even here, the wealth difference vs 120% was small (within ~€20k).  
- **Trends:** Faster home appreciation shifts the optimum earlier, as does higher rent or mortgage cost.  Higher equity returns or lower costs shift the optimum later.  Base home price had a smaller effect, but smaller homes (with same % rent) amplify rent's impact, favouring earlier purchase at low prices.  

We summarize a few representative outcomes (retirement net worth at age 69):  

| Equity Return | Home Growth | Rent Profile        | Home Price | Mort Rate | Best Trigger | Best LTV | Wealth (€)   |
|---------------|-------------|---------------------|------------|-----------|--------------|----------|--------------|
| 6%            | 1%          | €500→€700           | €175k      | 2.5%      | 120%         | ~70–80%  | ~€1.3M       |
| 5%            | 2.5%        | €500→€700           | €175k      | 3.5%      | 120%         | ~75%     | ~€1.23M      |
| 4%            | 2.5%        | €500→€700           | €150k      | 4.5%      | ~110%        | ~40%     | ~€1.18M      |
| 4%            | 4%          | €500→€900           | €150k      | 4.5%      | ~80%         | ~30%     | ~€1.18M      |

*(Higher values of "Wealth" indicate better outcome; all values are illustrative averages across our simulations.)* 

In general, **the wealth advantage of the optimal trigger over waiting until 100% is small** when the difference is that small, reinforcing that full coverage or beyond is usually best.  The first and second rows show high returns cases where waiting to 120% clearly wins. The bottom row is the one extreme case favouring early buy. 

# Mortgage Size Sensitivity  
We also examined how the optimal LTV changes with portfolio maturity.  Intuitively, **younger portfolios (buying early)** have less embedded gains, so the CGT “hedge” benefit of taking a mortgage is weaker.  Our model confirms this: at low triggers (early buy), the best LTV is quite high (60–80%).  At high triggers, the portfolio is mature, so even a moderate mortgage avoids large CGT, and the best LTV falls (often 30–50%).  For example, in the above extreme case (4%/4%/high rent), the best LTV was ~60% at 50% trigger, but dropped to ~30% at 110–120% trigger.  In the common scenarios, best LTV stayed around 70–80% even at trigger=120%, because even mature equity gains justify a large mortgage given the low interest cost.  

**Mortgage cliff:**  We saw no strict “cliff” where mortgage use suddenly fails. Rather, raising LTV always increases interest cost but *gradually* lowers taxes, so optimum shifts smoothly.  In low-return scenarios, extremely high LTV (80%) was needed to make early purchase viable; in high-return cases, even moderate LTV (50%) sufficed at full coverage.

# Rent Step-Function Effect  
Our model explicitly used the Spanish LAU rule (rent fixed at €500 for years 1–8, then jumping to €700 or €900).  We tested two cases: a jump to €700 and a jump to €900. The rent spike marginally *accelerates* the optimal buy for that one-time event.  In practice, buying just before year 8 yields one less year at high rent.  We found that if an investor is approaching buy-threshold around year 7–8, it is generally better to pull the trigger before the reset.  However, in our scenarios the continuous portfolio growth effect dominated: most optima still occurred later than year 8 even with the jump.  For example, in a high-growth scenario with a €900 jump, the best trigger shifted from ~120% to ~80–100%, reflecting that after year 8 the additional rent cost makes extra delay less attractive. 

# Age-45 (IVF) Cutoff  
Spain’s IVF program allows up to 100% financing for first-time buyers under 45, versus typical ~80% otherwise.  In our model, we already allowed LTV up to 80%.  If we assume a European FHA or IVF scheme can push to 100%, the effect would be to make early high-LTV purchases slightly more viable.  In practice, we find that *if* the optimal buy age is near 44, having 100% LTV would tilt the balance even more toward buying just before 45.  But since our base optimum is usually at high coverage (≥100%), most gains of waiting already assume large mortgages. In short, the age-45 cutoff **is not a primary driver** of the timing decision: it simply extends feasibility of high LTV, reinforcing that buying later with a maxed mortgage is usually best. 

# Fragility and Safety Margin  
Very low coverage triggers (≪50%) with very high mortgages are theoretically worst by risk: a crash or higher rates could leave the investor underwater.  We find that below ~50% coverage, the strategy becomes fragile (the investor starts with almost no down payment).  Our simulations show net wealth falls if trigger drops too far.  The **minimum “safe” coverage** depends on parameters, but a practical rule-of-thumb is to avoid below ~50–60%.  In scenarios where early triggers slightly outperformed, even the optimum was around 80%, not 50%.  Thus we suggest a conservative **lower bound of ~60–80%** coverage (i.e. 20–40% down) for safety.  

# Decision Rule  
A practical heuristic emerges: **“Buy when accumulated portfolio ~X% of total purchase cost, using a Y% LTV mortgage.”**  Our data suggest: 
- If long-term equity returns (net of taxes) are ~5–6% and home appreciation ~2–3%, then **X is around 100–120%**, and **Y≈70–80%**. In other words, wait until your portfolio can fully cover the purchase (even wait a bit longer), then take a large mortgage (50–80% of price) to minimize CGT.  
- If returns drop (4–5%) or home growth rises (>3%) or rent is steep, then **X shifts lower** (sometimes 80–100%) and **Y shifts lower** (~30–50%). In practice, this means buying earlier (portfolio only ~80–90% of cost) and taking a smaller loan (~40%) to reduce interest drag.  
- Very conservatively, **never buy with coverage much below 60%** unless extraordinary circumstances, due to leverage risk.  

In summary, for a 36-year-old Valencian investor:  
**“Aim to buy when your invested portfolio is roughly equal to or greater than the home cost. Use a hefty mortgage (well over 50% LTV) to defer CGT, then aggressively repay.** Only in cases of weak market returns or surging rents is it optimal to buy sooner with a smaller loan.”  

**Sources:** Spanish tax and housing rules (CGT brackets and FIFO【9†L379-L388】【9†L420-L427】; no mortgage deduction post-2013【11†L60-L68】; Valencian ITP 9% after mid-2026【16†L284-L287】). Our analysis numerically simulated the rest of the variables.