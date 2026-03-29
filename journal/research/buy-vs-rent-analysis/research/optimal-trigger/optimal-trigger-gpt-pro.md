I’m modeling this as a full lifecycle optimization from age 36 to 69, jointly solving the purchase trigger and mortgage LTV under current Spanish/Valencian tax, mortgage, and IVF rules. Then I’ll sweep your scenario ranges month by month, compare after-tax retirement wealth in nominal euros, and turn the dominant trigger/LTV regions into a practical decision rule.

I’ve now locked the tax spine from official law: the 19/21/23/27/30 savings scale is usable, FIFO applies, and traspasos keep basis and acquisition date so only the sold slice is taxed. One correction already matters for the IVF branch: the 2026 scheme is effectively a guarantee up to 95% of purchase price, not true 100% LTV, so it mostly affects very early high-LTV cases.

With the legal inputs settled, I’m moving into the actual month-by-month simulation and stress-testing the trigger/LTV grid. The key check now is whether the earlier 40–50% LTV result still survives for a younger, smaller portfolio.

The first scenario results are in: 100% coverage is rarely the exact optimum, and with a younger portfolio the wealth-maximizing solution often leans to higher LTVs than 40–50%, especially around 70% coverage. The split now looks like this: earlier buying dominates when house-price growth and post-year-8 rent are high, while later buying survives mainly where portfolio returns stay comfortably above mortgage costs; I’m finishing the IVF-before-45 and fragility cuts to turn that into the practical rule.

Thought for 86m 17s
1. Executive summary

I built a monthly nominal-euro lifecycle model from age 36 to 69 using your €7,000 lump sum, €1,500/month DCA, 80/20 world-equity/MMF split, your stated 10% acquisition-cost assumption, and a 2.0% MMF proxy for the cash sleeve. Tax is modeled with Spain’s current savings-rate ladder at 19/21/23/27/30, FIFO on homogeneous fund units, and traspasos that preserve basis/date instead of triggering tax. I treated the world fund and the MMF as separate homogeneous pools, so the purchase liquidation sells the lower-gain MMF sleeve first and then equity FIFO; that sequencing is an inference from the homogeneous-values rule. I also gave the mortgage no current IRPF deduction because the habitual-residence deduction was abolished for post-2012 acquisitions except the transitional regime. Baseline financing caps LTV at 80%; the IVF variant allows up to 100% of the property price while you are still 45. I did not include owner running costs such as IBI, comunidad, maintenance, or insurance, so the model is somewhat pro-buy and pro-leverage.

The core result is not “always buy earlier than 100% coverage.” It is: the optimal trigger is dominated by the spread between expected portfolio return and expected property appreciation. On your requested 50%-120% trigger grid, buying at exactly 100% coverage is never the maximizing grid point. The optimizer picks a trigger below 100% in 54 of 162 scenarios, at or above 100% in 108 of 162, and it hits the top boundary of 120% in 106 of 162. Relative to buying exactly at 100% coverage, the optimized trigger improves retirement wealth by a median €15.9k and an average €23.3k, with gains ranging from €1.1k to €126.7k.

The regime split is sharp. When the portfolio and the property both grow at 4%, the optimum is 50% coverage in all 18 scenario cells. When portfolio return is 4% and property growth 2.5%, the optimum is 65%-90% with a median of 75%. When portfolio return is 5% and property growth 4%, the optimum is 60%-85% with a median of 72.5%. But once the portfolio outruns the property by about 2 percentage points or more, the optimum usually moves to 120%, which means 100% coverage is too early, not too late.

For your baseline-ish middle case — €175k property, 5% portfolio return, 2.5% property growth, rent €500 for 8 years then €700, mortgage 3.5% — the best trigger within the 50%-120% band is 120% coverage, at about age 48.2, with an 80% LTV mortgage. That beats a 100% trigger by about €10.9k and beats never buying by about €32.7k. So under your middle assumptions, the answer is no: waiting until 100% coverage is not too late. If anything, it is a bit early.

A second big finding is that once you co-optimize trigger and LTV, your old “40%-50% LTV” result does not survive this younger-portfolio setup. Under a pure wealth objective, the best conventional choice is the 80% cap in 150 of 162 scenarios. In other words: within this model, lower LTV looks more like a comfort/risk choice than a wealth-maximizing one.

2. Cost-of-waiting analysis

The cleanest way to think about “one more year of waiting” is that it adds four direct drags and one main offset. The drags are: another year of rent, a higher purchase price, more CGT at the purchase liquidation, and usually a somewhat larger lifetime mortgage-interest bill because the same LTV is applied to a more expensive flat. The offset is a larger retained portfolio at the buy date, which then compounds for the rest of the horizon.

In the central case (5% portfolio, 2.5% property, €175k, €700 reset, 3.5% mortgage), waiting is still beneficial for quite a while, but the benefit decays steadily:

Central case: waiting one more year	Retirement-wealth effect
Age 39 → 40	+€17.6k
Age 43 → 44	+€12.2k
Age 44 → 45 (after rent reset)	+€8.5k
Age 49 → 50	+€3.0k
Age 52 → 53	+€44
Age 53 → 54	-€851

The direct breakdown at the 44 → 45 decision in that central case is useful. Waiting adds about €8.4k of rent, €5.3k to the purchase price, about €0.2k of extra purchase tax, and about €2.2k of extra lifetime mortgage interest. But it also gives you about €26.1k more retained portfolio at the buy date. Net result: still +€8.5k of retirement wealth. By 52 → 53, the same sort of direct waiting costs still exist, but the remaining compounding horizon is short enough that the net gain has collapsed to essentially zero.

Three representative cases make the shape clear:

Scenario	Wait 44 → 45	Read
House-hot: 4% portfolio / 4% property / €200k / €900 reset / 3.5% mortgage	-€12.2k	Waiting is already destructive by the rent-reset window.
Central: 5% / 2.5% / €175k / €700 / 3.5%	+€8.5k	Reset matters, but it does not force the buy date by itself.
Market-hot: 6% / 1% / €200k / €700 / 2.5%	+€33.1k	Waiting is still very valuable even after the reset.

So the answer to “when does the cost of waiting exceed the benefit?” is: early in house-hot regimes, around age 53 in the middle case, and not within your 120% band in market-hot regimes.

3. Optimal trigger table

For a compact scenario matrix, here is the €175k / €700 reset / 3.5% mortgage slice. Each cell shows:

trigger / best LTV / buy age

Portfolio return ↓ vs property growth →	1%	2.5%	4%
4%	120% / 80% / 47.0	75% / 80% / 43.9	50% / 80% / 41.6
5%	120% / 80% / 46.4	120% / 80% / 48.2	75% / 80% / 44.6
6%	120% / 80% / 45.9	120% / 80% / 47.4	120% / 80% / 49.7

That table is the whole story in miniature. Early triggers are concentrated where the flat is keeping up with, or nearly keeping up with, the portfolio. Once the portfolio’s expected return is meaningfully higher than house-price growth, the optimum pushes to the top of your tested band.

The secondary sensitivities are much smaller than that return-vs-house-growth spread:

Raising the rent reset from €700 to €900 moves the trigger earlier by 0 to 10 percentage points, with a median shift of zero.

Moving mortgage rates from 2.5% to 4.5% shifts the trigger by -15 to +5 points, again with a median shift of zero.

Moving the starting price from €150k to €200k barely changes the trigger in most cells, but it delays the buy age by a median 2.7 years because you simply reach the same coverage later.

The “never-buy boundary” is real. In 46 of 162 scenarios, even the best buy trigger in the 50%-120% band loses to continuing to rent and invest. Those 46 are concentrated in exactly the intuitively dangerous places: all 18 of the 6% portfolio / 1% property cells, 13 of 18 of the 6% / 2.5% cells, and 12 of 18 of the 5% / 1% cells.

A useful boundary diagnostic, even though it is outside your requested 120% cap: in the central case, extending the grid beyond 120% shows the wealth peak around 165% coverage. In a 6% / 1% market-hot case, wealth was still improving at 200% coverage and still lost to never-buy. In a 4% / 4% house-hot case, wealth peaked at 50% and then fell almost monotonically. So when the 120% ceiling is hit, it usually means one of two things: either “wait even longer” or “don’t force the purchase at all.”

4. Mortgage size sensitivity

This is where the co-optimization result is strongest: within a conventional 80% cap, the model almost always wants the cap. Out of 162 scenarios, the best LTV is 80% in 150. The few exceptions are all in the same corner: 4.5% mortgage, 4% portfolio return, where the optimum drops into the 50%-70% range.

There is also no evidence of the cliff you were worried about — the idea that a young portfolio makes mortgage CGT savings too small to justify the interest. In the central case, at a 70% trigger (buy age about 43.1), retirement wealth is roughly:

€1.036m at 80% LTV

€1.053m at 90% LTV

€1.062m at 95% LTV

€1.056m at 100% LTV

At a 120% trigger (buy age about 48.2), it is roughly:

€1.075m at 80% LTV

€1.085m at 90% LTV

€1.068m at 100% LTV

So the curve is smooth, and the “too much mortgage” point is near 95%-100%, not 50%-60%. That is true even though the portfolio is older at the later trigger. The maturity effect exists — the optimum nudges down from 95% toward 90% as the portfolio ages — but it is modest.

My read is that your earlier 40%-50% LTV result was probably being driven by assumptions that are not in this objective function: explicit safety buffers, rate-risk aversion, underwriting constraints, or owner-cost assumptions. In a stripped-down after-tax wealth maximization, the optimizer wants to preserve invested capital.

5. Rent step-function analysis

The rent reset is real, but it is a second-order accelerator, not the primary driver.

Across all scenarios:

Waiting from month 84 to month 96 adds an average €13.3k of retirement wealth.

Waiting from month 96 to month 108 adds an average €9.4k when the reset is to €700, and €7.0k when the reset is to €900.

So the reset chops about €2.4k off the value of that first post-reset year of waiting.

The sign still depends on the return-vs-house-growth regime:

In all 18 cells where portfolio return is 6% and property growth 1%, waiting from 96 → 108 is still positive.

In all 18 cells where portfolio return is 4% and property growth 4%, waiting from 96 → 108 is negative.

That means there is not a universal “buy just before year 8” rule. There is a natural pre-reset purchase window if you believe the Castellón coast flat is compounding at something like 4% nominal and your portfolio is only a 4%-5% nominal engine. But if you believe property growth is more like 1%-2.5% and the portfolio can compound at 5%-6%, the reset alone is not strong enough to overturn the benefit of waiting.

6. IVF deadline analysis

As of 24 February 2026, the Generalitat’s IVF guarantee can cover up to 20% of the purchase price, which lets participating mortgages reach 100% of value. The normal age window is 18 to 45, and the price cap is €311,000, comfortably above your €150k-€200k target range.

In the model, IVF matters only through that extra leverage before your 46th birthday. It improves the optimum in 122 of 162 scenarios. The gain is +€9.2k median across all scenarios, and the maximum is +€56.9k.

The biggest gains are in hot-property regimes where IVF lets you move the purchase into the 42-45 window with 95%-100% LTV. In the strongest example I found — €200k price, 5% portfolio return, 4% property growth, €900 rent reset, 2.5% mortgage — IVF shifts the optimum from 65% trigger / 80% LTV / age 44.5 to 60% trigger / 100% LTV / age 43.75, adding about €56.9k of retirement wealth.

In the central case, IVF matters much less. It improves the optimum by only about €1.3k, moving you from 120% trigger / 80% LTV / age 48.2 to roughly 95% trigger / 90% LTV / age 45.7. So the deadline is economically meaningful only if your subjective scenario is house-hot enough that high pre-45 leverage is actually valuable.

7. Fragility analysis

I stress-tested each trigger by applying an immediate -35% equity shock right after purchase, leaving the MMF sleeve unchanged, and then measuring the retained portfolio as months of €1,500 outflow coverage.

That test says your wealth optimum is too aggressive below about 70% coverage. Specifically:

At 50%-65% triggers, there are 8 fragile rows where the shocked retained portfolio covers less than 12 months.

At 70% and above, no scenario breaches the 12-month rule.

All 8 fragile cases are the same cluster: €200k property, 4% portfolio return, 4% property growth, 4.5% mortgage, with runway between 4.1 and 11.4 months. That is exactly the combination where buying early is tempting but financing is expensive and the retained cushion is thin.

So my practical conclusion is:

70% coverage is the minimum safe trigger floor.

Below that, the strategy only works if you are deliberately taking a hot-property bet and you have extra liquidity outside the model. Because I omitted owner running costs, that floor is, if anything, slightly generous.

8. Decision rule

Use this as the operational heuristic:

If expected portfolio return is within about 1 point of property appreciation, buy early, at roughly 50%-75% of total purchase cost, and use the highest LTV available that still fits your risk tolerance. Under normal financing that usually means 80% LTV. If IVF is available before you turn 46, it often means 95%-100%.

If the portfolio beats property by about 1.5 points, buy around 70%-90% coverage. The rent reset nudges you earlier, but it is not the main driver.

If the portfolio beats property by 2 points or more, then 100% coverage is usually too early, not too late. Inside your requested grid, the answer is often 115%-120%, and in many cells the true optimum is likely above 120%.

Do not trigger below 70% coverage unless you also hold a separate cash buffer and are intentionally leaning into a strong house-price view.

Default LTV rule: if mortgage rates are not above your expected portfolio return, the wealth optimizer usually wants the max conventional mortgage. If rates are around 4.5% and your portfolio assumption is only 4%, cut LTV down toward 50%-70%.

So the plain-English rule is:

Buy at 70%-80% coverage only when you think the flat will appreciate almost as fast as the portfolio. Otherwise, 100% coverage is not late. In your middle case, wait beyond 100% — roughly 120% in the tested grid — and still use the maximum conventional mortgage.