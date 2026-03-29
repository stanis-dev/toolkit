# Deep Research: Cross-Tool Evaluation — Meta-Analysis Results Comparison

---

## What this is

I submitted an identical financial research prompt (a pre-execution assumption audit for an "invest now, buy later" strategy) to five different AI research tools/modes simultaneously. I am attaching all five results alongside this evaluation prompt.

The original prompt asked each tool to stress-test the assumptions behind a specific financial strategy: investing in a global equity index fund (fondo de inversión) via Trade Republic in Spain, then buying a coastal flat outright in Castellón province once the portfolio reaches target. The prompt requested adversarial analysis, current data verification, quantified impact assessment, and a pre-execution checklist.

## The five results being evaluated

1. **GPT-5.4 Heavy Thinking** (`result-gpt-5.4-heavy-thinking.md`) — Extended reasoning mode, no web search
2. **GPT-5.4 Pro Extended** (`result-gpt-5.4-pro-extended.md`) — Pro mode with extended output, no web search
3. **GPT Deep Research** (`result-gpt-deep-research.md`) — Agentic deep research with Bing web search
4. **Gemini Deep Research** (`result-gemini-deep-research.md`) — Agentic deep research with Google Search
5. **Claude Opus 4.6 Extended Deep Research** (`result-claude-opus-4.6-extended-deep-research.md`) — Extended research with Brave Search

## What I want

A rigorous cross-comparison of all five results to (a) determine which tool performed best for this specific task, (b) synthesize the strongest findings across all tools into a single consolidated assessment, and (c) identify where tools contradict each other and determine who is correct.

## Evaluation criteria

### 1. Factual accuracy and data freshness

For each tool: did it provide verifiable, current data? Did it cite sources? Were any claims factually wrong? Did it actually verify assumptions against current data (as instructed), or did it rely on training data / the prompt's own context?

Score each tool and flag specific errors.

### 2. Adversarial rigour

The prompt explicitly asked for adversarial analysis ("find what is wrong, what is fragile, what could break the strategy"). Which tools genuinely challenged the assumptions vs. which defaulted to mild validation? Did any tool identify risks or weaknesses that no other tool found?

### 3. Spain-specific accuracy

This strategy depends on Spanish tax law, the IVF guarantee programme, LAU rental protections, Castellón coast property dynamics, and Trade Republic's Spain-specific fondos offering. Which tools demonstrated genuine knowledge of these specifics vs. which gave generic European/global financial advice?

Flag any Spain-specific claims that are wrong or outdated across any of the five results.

### 4. Quantification and actionability

The prompt asked for quantified impact ("this assumption is off by X%, which shifts the timeline by Y years"). Which tools delivered specific numbers, and which stayed at the qualitative level? Were the quantified estimates plausible?

### 5. Instruction adherence

Did the tool follow the requested output format (7 sections)? Did it avoid the listed anti-patterns (generic advice, reassurance, repetition of existing findings)? Did it stay focused on the implementation audit rather than re-debating the strategy choice?

### 6. Novel insights

Which tools surfaced genuinely new information, risks, or perspectives that the existing research project (summarised in the prompt) had not already covered? Rank by novelty value.

## Cross-comparison analysis

### Consensus findings

Where do 3+ tools agree on a specific conclusion, risk assessment, or recommendation? These are the highest-confidence findings. List them with the supporting tools.

### Disagreements and resolution

Where do tools contradict each other on specific facts, assessments, or recommendations? For each disagreement: state the positions, evaluate which is correct (with evidence), and explain why the others got it wrong.

### Unique contributions

For each tool, identify 1–3 insights that were unique to that tool (no other tool mentioned them). Assess whether each unique contribution is genuinely valuable or noise.

## Output format

1. **Tool ranking** (table: tool name, overall score /10, factual accuracy, adversarial rigour, Spain-specifics, quantification, novel insights — one sentence summary per tool)
2. **Consensus findings** (the highest-confidence conclusions that emerge from cross-referencing all five results, organised by the original prompt's 7 sub-questions)
3. **Disagreements resolved** (each contradiction, the correct answer, and which tool(s) got it wrong)
4. **Best unique contributions by tool** (findings worth keeping that only one tool surfaced)
5. **Synthesized pre-execution checklist** (merged from all five results, deduplicated, in priority order — the single best checklist drawing from all tools)
6. **Synthesized monitoring triggers** (merged from all five results — the best set of thresholds and review triggers)
7. **Tool selection guidance** (which tool/mode to use for future financial research tasks of this type, and why)

## What I do NOT want

- Equal praise for all tools — rank them honestly, even if the differences are stark
- Evaluation based on writing style or length — judge on substance, accuracy, and usefulness
- Ignoring factual errors because the overall analysis was "good enough"
- Treating training-data-based reasoning as equivalent to web-verified current data
