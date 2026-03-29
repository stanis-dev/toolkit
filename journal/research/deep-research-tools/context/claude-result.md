# AI deep research tools: a head-to-head evaluation for prompt engineers

**The four leading AI deep research tools — ChatGPT Deep Research, Gemini Deep Research, Claude Research, and Perplexity Deep Research — have converged on similar agentic architectures but diverge sharply in input capacity, output length, citation reliability, and speed.** For a prompt engineer building optimized research prompts, these differences are decisive: Gemini accepts the most context (**1M tokens**), ChatGPT produces the longest reports (**100K output tokens**), Perplexity delivers the fastest results and most reliable citations, and Claude has the lowest hallucination rate by refusing to guess when uncertain. Every tool now uses an agentic multi-step loop — plan, search, read, iterate, synthesize — but the underlying models, search infrastructure, workspace integrations, and pricing structures differ in ways that directly affect how prompts should be constructed for each.

---

## ChatGPT Deep Research: the enterprise integration leader

### Model and architecture

ChatGPT Deep Research is powered by **GPT-5.2** in the consumer ChatGPT app since February 10, 2026. The API retains separate model identifiers: `o3-deep-research` and `o4-mini-deep-research`. The system was trained via end-to-end reinforcement learning on hard browsing and reasoning tasks, learning to plan multi-step trajectories, backtrack, and react to real-time information.

The internal workflow follows three stages: an intermediate model (gpt-4.1) **clarifies user intent and rewrites the prompt** into a detailed expanded version, then hands off to the deep research model for autonomous browsing, analysis, and synthesis. The model uses browser capabilities (searching, clicking, scrolling, interpreting files) alongside a Python code interpreter. A second custom-prompted o3-mini model summarizes chains of thought. Sessions typically take **5–30 minutes** and consume **~1–1.6 million tokens** of browsed content, synthesizing from what OpenAI describes as "hundreds of online sources."

### Input capabilities

The o3-deep-research model has a **200,000-token context window**. Users can attach **PDFs, spreadsheets, and images** for additional context, though exact per-file size limits are not publicly documented for the ChatGPT UI.

**Source control** is a standout feature added in February 2026. Via "Sites → Manage sites" in the prompt window, users can restrict research to specified domains or prioritize them while allowing broader search. This is critical for prompt engineers who need authoritative sources.

**Workspace integration** is the most extensive of any tool evaluated. ChatGPT Deep Research connects to Google Drive, SharePoint, Dropbox, Box, OneDrive, Gmail, GitHub, and authenticated industry sources like **FactSet, PitchBook, and Scholar Gateway**. It also supports any MCP (Model Context Protocol) server for private data. All connections are read-only.

Conversation context persists within a session. ChatGPT's memory feature works across sessions, though its direct influence on deep research execution is unconfirmed.

### Output capabilities

The maximum output is **100,000 tokens** (per the official API model page), theoretically supporting reports of ~75,000 words. In practice, reports span thousands of words with structured sections. Since February 2026, a **fullscreen document viewer** displays a table of contents, citations panel, and embedded graphs.

Citations appear **inline with clickable source links** and include URL, title, and character position annotations. Export options include **Markdown, Word (.docx), and PDF**. Users can interrupt research in progress, refine scope, and continue refining output in the same session.

### Search and source quality

ChatGPT uses **Microsoft Bing's search index** as its search infrastructure. The model performs multiple search queries, opens pages, scrolls, clicks, and uses find-in-page actions. It accesses live web data in real time, though the underlying model's knowledge cutoff is June 1, 2024. For paywalled content, access requires authenticated connectors (FactSet, Scholar Gateway); standard paywalled sites are not accessible otherwise.

### Accuracy and benchmarks

Published benchmarks (from the o3-based model at February 2025 launch):

| Benchmark | Score | Notes |
|---|---|---|
| Humanity's Last Exam (HLE) | **26.6%** | Text-only subset; 3× previous best at time of release |
| GAIA | **New SOTA** | Topped external leaderboard |
| DRACO (Perplexity's benchmark, Feb 2026) | **52.1%** | Third behind Perplexity (70.5%) and Gemini (59.0%) |

No published benchmarks exist specifically for the GPT-5.2 upgrade. OpenAI explicitly acknowledges the model "occasionally makes factual hallucinations" and "may reference rumors." The iterative backtracking architecture provides some self-correction, but independent verification of citations remains essential.

---

## Gemini Deep Research: the largest context window and strongest benchmarks

### Model and architecture

Gemini Deep Research is powered by **Gemini 3.1 Pro** (released February 19, 2026), succeeding Gemini 3 Pro (December 2025), 2.5 Pro, and 2.0 Flash Thinking in earlier iterations. The API agent identifier is `deep-research-pro-preview-12-2025`.

The architecture uses a **novel asynchronous task manager** that maintains shared state between planner and task models, enabling graceful error recovery without restarting. The workflow: **Plan → Search → Read → Iterate → Output**. The model formulates a research plan (user-reviewable and editable before execution), determines which sub-tasks can run simultaneously versus sequentially, reasons over gathered information to identify gaps, then searches again. This loop repeats across multiple iterations before synthesizing a final report.

Sessions have a **60-minute hard limit** and typically complete within **20 minutes**. A standard task involves ~80 search queries and ~250K input tokens; complex tasks can reach **~160 search queries** and **~900K input tokens**. Google states the system can browse "up to hundreds of websites" per task — one user reported 622 websites in a single session.

### Input capabilities

Gemini's defining advantage is its **1-million-token input context window**, equivalent to ~1,500 pages of text. This is **5× larger** than ChatGPT's and Claude's standard windows. Users can upload **PDFs, CSVs, Docs, and images** (audio is not supported).

Source control works through the editable research plan and verbal instructions — users can tell the system what sites to prioritize or ignore, and select source types via a dropdown (web, Gmail, Drive, Chat).

**Google Workspace integration** is native and deep. Gemini can access **Gmail, Google Drive** (Docs, Slides, Sheets, PDFs), and **Google Chat**, inheriting the Workspace permission graph — if the user can open a file, the model can read it. One caveat: visual reports are unavailable when Gmail/Drive sources are used in the same run.

### Output capabilities

The underlying model supports up to **65,536 output tokens** (~49,000 words). Complex tasks generate **60–80K output tokens** per the official API docs, though the default `maxOutputTokens` in the API is only 8,192 and must be explicitly increased.

Reports include **inline citations with links** and a "Sites browsed" panel. Export options include **Google Docs** (native one-click), **Canvas** (interactive editing), **Audio Overview** (podcast-style conversion), and **JSON** via the API. Follow-up questions are fully supported within a session via `previous_interaction_id`.

### Search and source quality

Gemini uses **Google Search** natively — the most comprehensive web index available. This gives it a structural advantage in source coverage and recency. However, it **cannot access paywalled content** — this is explicitly confirmed across multiple sources. Google's own guidance suggests asking the model to use publicly available summaries and note the limitation.

### Accuracy and benchmarks

Google published these scores for the Gemini 3 Pro-based Deep Research agent (December 11, 2025):

| Benchmark | Score | Context |
|---|---|---|
| Humanity's Last Exam (HLE) | **46.4%** | SOTA at time of release; raw Gemini 3 Pro scored 37.5% |
| DeepSearchQA | **66.1%** | Google's own 900-task benchmark across 17 fields |
| BrowseComp | **59.2%** | OpenAI's web browsing benchmark; raw model scored 49.4% |
| DRACO (Perplexity's benchmark) | **59.0%** | Second behind Perplexity (70.5%) |

These represent the **highest published third-party benchmark scores** among the four tools. Google describes Gemini 3 Pro as its "most factual model yet," specifically trained to reduce hallucinations, though no quantitative hallucination rate is published. The iterative research loop includes built-in gap identification and re-searching.

---

## Claude Research: lowest hallucination risk, no dedicated research model

### Model and architecture

Claude Research is fundamentally different from the other three tools. **Anthropic does not offer a dedicated "research mode" model** — there is no specialized research-trained variant. Instead, Claude Research combines standard Claude models (primarily **Claude Opus 4.6**, released February 5, 2026) with web search, extended thinking, and code execution tools in an agentic workflow. The DRACO benchmark paper explicitly notes: "Claude Opus 4.5 and 4.6 are standard models as Anthropic does not offer research mode as a dedicated API."

The process is agentic and multi-step: Claude develops a research plan, executes **multiple iterative web searches** that build on each other, reads full web pages (not just snippets), cross-references information, resolves contradictions, and synthesizes findings with inline citations. Extended thinking is automatically enabled alongside Research. Sessions typically take **5–45 minutes** and consult **10+ sources**, scaling to hundreds for complex queries.

### Input capabilities

Claude's context window is **200,000 tokens standard**, with a **1-million-token context window now GA** as of March 13, 2026, for Opus 4.6 and Sonnet 4.6 at standard pricing — no multiplier or beta header required. This matches Gemini's capacity.

File uploads support up to **30MB per file** and **20 files per conversation**, with formats including PDF, DOCX, TXT, CSV, HTML, RTF, EPUB, JSON, ODT, and XLSX (with code execution enabled). PDFs under 100 pages receive full multimodal analysis including charts and images; 100–1,000 pages are text-only. The Files API (developer beta) allows up to **500MB per file**.

The web search API supports **`allowed_domains` and `blocked_domains`** parameters for source restriction. In the claude.ai UI, source steering is done through verbal instructions rather than a dedicated UI.

**Workspace integration** spans Google Workspace (Gmail, Calendar, Docs), Microsoft connectors (SharePoint, OneDrive, Outlook, Teams), and **MCP** for extensible connections to Notion, Slack, Databricks, Snowflake, and others. Enterprise users get Google Docs cataloging for improved retrieval.

**Cross-session memory** became available for all users (including free) as of early 2026, enabling Claude to build on previous conversations.

### Output capabilities

Claude Opus 4.6 supports up to **128,000 output tokens** — the longest maximum output of any tool evaluated, though practical Research reports are shorter. Citations are **inline with source URLs**, and the API provides `cited_text` with exact quoted passages. The Research feature launched in beta for Max, Team, and Enterprise plans (April 2025) and has since expanded to **Pro plans** in select regions.

Export is primarily **Markdown** in the chat interface. Artifacts can generate interactive content, and Claude can now produce inline **charts, diagrams, and visualizations** (announced March 12, 2026). There is no native PDF or Word export — users must copy and convert.

### Search and source quality

Claude uses **Brave Search** as its primary web search backend, with **Bing powering image search**. Independent testing found **86.7% overlap** between Claude's cited results and Brave's top organic results. Brave's index covers ~30 billion pages — significantly smaller than Google's. This means Claude may underperform on queries requiring deep or niche web coverage compared to Gemini (Google Search) or Perplexity (hybrid approach). **Paywalled content is inaccessible.**

### Accuracy and benchmarks

Claude's hallucination profile is structurally distinct. Anthropic's models are **calibrated to refuse rather than guess**, yielding the lowest hallucination rates on knowledge benchmarks but sometimes lower raw accuracy. Key metrics:

| Benchmark | Model | Score |
|---|---|---|
| BullshitBench v2 (BS detection) | Sonnet 4.6 (High Reasoning) | **91.0% Green Rate, 3.0% Red Rate** (best overall) |
| Vectara HHEM hallucination rate | Claude 3.7 Sonnet | **4.4%** |
| MMLU-Pro | Opus 4.5 | **90%** (tied best) |
| Terminal-Bench Hard | Opus 4.5 | **44%** (highest of any model) |

No Research-specific benchmarks have been published by Anthropic. The DRACO paper evaluated Claude Opus 4.5/4.6 as standard models (not research agents) and found them competitive but behind the purpose-built research systems from Perplexity and Google.

---

## Perplexity Deep Research: fastest results, best citation quality

### Model and architecture

Perplexity Deep Research launched in February 2025 on a custom version of **DeepSeek R1** with proprietary test-time compute. As of March 2026, it runs on **Claude Opus 4.6** for Max subscribers and **Claude Opus 4.5** (gradually rolling out to Pro). The system is explicitly **model-agnostic** — Perplexity upgrades to top reasoning models as they become available and uses **4–6 LLMs simultaneously** including in-house Sonar models, with Cerebras infrastructure for speed.

The architecture is agentic multi-step: iterative search, read, and reason loops, followed by report writing and export. A key differentiator is **speed** — typical sessions complete in **2–4 minutes**, with the DRACO benchmark average at **7.7 minutes** versus 9.9 minutes for Gemini and 30+ minutes for ChatGPT. Recent UX improvements (March 2026) include clarifying questions for broad queries, the ability to add follow-up questions while research is still running, and streaming reports into editable files.

### Input capabilities

The Sonar Deep Research API has a **128,000-token context window**. Direct pasted input in the app supports ~8,000 tokens per query, with longer text auto-converted to file attachments.

File uploads support a wide range of formats — **PDF, DOCX, PPTX, XLSX, CSV, RTF, ODT, MD, JSON, TXT, images, and audio/video** — with a **40–50MB size limit** and up to 10 files per prompt (Pro). Enterprise users can upload up to 30 files per thread and maintain repositories of up to 5,000 files.

**Focus modes** are Perplexity's distinctive source control mechanism: **Academic** limits to peer-reviewed journals, arXiv, Semantic Scholar, and PubMed; **Web** provides broad search; **Social** focuses on Reddit and social media. Users can also focus on specific domains.

Workspace integration includes **Spaces** (custom knowledge hubs) and Enterprise connectors for Google Drive, SharePoint, OneDrive, Box, and Dropbox. **Cross-session memory** works across all models and search modes, with claimed **95% recall accuracy** as of the February 2026 upgrade.

### Output capabilities

This is Perplexity's notable weakness. Default reports are approximately **1,000–2,600 words** — substantially shorter than competitors. The February 2026 update promises "longer, more comprehensive reports," but exact maximum token limits remain unpublished. For users needing lengthy reports, a section-by-section multi-turn approach is recommended.

Where Perplexity excels is **citation quality**. Every claim includes **inline numbered citations with clickable source URLs** — this is foundational to the product, not an afterthought. Independent testing found **85% of citations were accurate and traceable**, described as "significantly higher than any competitor." Export options include **PDF, Document, Perplexity Page** (shareable web page), and editable files.

### Search and source quality

Perplexity uses a **hybrid search approach**: third-party APIs from both **Google and Bing**, its own crawler (PerplexityBot), and a proprietary index. In February 2026, it released state-of-the-art embedding models (pplx-embed-v1) surpassing Google and Alibaba on public benchmarks. This multi-source approach provides strong source diversity.

The system accesses real-time web data and can pull articles published within the past 30 minutes. For paywalled content, the standard interface cannot access it, though the Comet browser (Max product) has a revenue-sharing scheme with partner publishers (CNN, Fortune, etc.) that enables some paywall access.

### Accuracy and benchmarks

| Benchmark | Score | Date | Notes |
|---|---|---|---|
| SimpleQA | **93.9%** | Feb 2025 | OpenAI's factuality benchmark |
| HLE | **21.1%** | Feb 2025 | Below OpenAI DR (26.6%) |
| DRACO (self-created) | **70.5%** (Opus 4.6) | Feb 2026 | Beat Gemini (59.0%) and OpenAI (52.1%) |
| DRACO Law domain | **89.4%** | Feb 2026 | Highest domain score |

The **DRACO benchmark** deserves scrutiny: it was created by Perplexity from its own production queries. While open-sourced, validated across judge models (GPT-5.2 and Sonnet-4.5), and covered by Harvard's D³ Institute, the provenance creates potential home-field advantage. Rankings were consistent across different judge models, lending some credibility.

Perplexity does not independently fact-check sources — it relies on source credibility. If top search results contain biased or outdated information, that bias propagates into the output.

---

## Head-to-head comparison across critical dimensions

| Dimension | ChatGPT Deep Research | Gemini Deep Research | Claude Research | Perplexity Deep Research |
|---|---|---|---|---|
| **Model (Mar 2026)** | GPT-5.2 | Gemini 3.1 Pro | Opus 4.6 / Sonnet 4.6 (standard) | Opus 4.6 (Max) / 4.5 (Pro) + Sonar |
| **Input context** | 200K tokens | **1M tokens** | 200K (1M GA for Opus/Sonnet 4.6) | 128K tokens |
| **Max output** | **100K tokens** | 65K tokens | 128K tokens (model limit) | ~1,000–2,600 words typical |
| **Session speed** | 5–30 min | 2–20 min (max 60) | 5–45 min | **2–4 min typical** |
| **Search engine** | Bing | **Google Search** | Brave Search | Google + Bing + own index |
| **Source control UI** | ✅ Sites → Manage sites | ✅ Via plan + verbal | ⚠️ API only (allowed/blocked domains) | ✅ Focus modes + domains |
| **Workspace integration** | **Best** (Drive, SharePoint, Box, Gmail, GitHub, MCP, FactSet) | Google Workspace (Gmail, Drive, Chat) | Google + Microsoft + MCP | Spaces + Enterprise connectors |
| **Paywalled access** | Via authenticated connectors | ❌ No | ❌ No | ❌ (Comet/partners for Max) |
| **Citation style** | Inline + clickable URLs | Inline + clickable URLs | Inline + clickable URLs + cited_text | **Inline numbered + URLs (highest accuracy)** |
| **Export formats** | Markdown, Word, PDF | Google Docs, Canvas, Audio | Markdown (copy only) | PDF, Document, Perplexity Page |
| **File uploads** | PDF, spreadsheets, images | PDF, CSV, Docs, images | PDF, DOCX, TXT, CSV + 15 more | PDF, DOCX, PPTX, XLSX + audio/video |
| **Hallucination approach** | Acknowledges risk; backtracking | "Most factual model yet" (unquantified) | **Refuses rather than guesses** (lowest rate) | Relies on source credibility |

### Best-in-class by use case

| Use Case | Best Tool | Why |
|---|---|---|
| **Deep, multi-source research** | **Gemini** | Strongest benchmarks (HLE 46.4%, BrowseComp 59.2%), Google Search, longest research sessions |
| **Very long context input** | **Gemini** (or Claude with 1M GA) | 1M tokens native; Claude now matches at 1M GA |
| **Current/real-time data** | **Perplexity** | Hybrid search with sub-30-min article retrieval; fastest turnaround |
| **User's own files/data** | **ChatGPT** | Most connectors: Drive, SharePoint, Box, Gmail, GitHub, MCP, FactSet, PitchBook |
| **Strict citation requirements** | **Perplexity** | 85% citation accuracy in independent testing; citations are foundational to the product |
| **Token-efficient output** | **Perplexity** | Fastest results (2–4 min), lowest API cost (~$0.41/query); shorter but dense |
| **Lowest hallucination risk** | **Claude** | Calibrated to refuse rather than fabricate; 4.4% hallucination rate (Vectara HHEM); 91% BS detection rate |

---

## Pricing and access tiers

| Tool | Free | Mid-tier | Premium | API cost per query |
|---|---|---|---|---|
| **ChatGPT** | 5 lightweight queries | **Plus $20/mo**: 25 queries (15 lightweight) | **Pro $200/mo**: 250 queries (half lightweight) | ~$2–5 (o3-DR: $10/$40/M tokens) |
| **Gemini** | "A few times/month" | **AI Plus $7.99/mo**: Enhanced access | **AI Pro $19.99/mo**: Higher access · **AI Ultra $249.99/mo**: Highest + visual reports | ~$2–3 estimated (Gemini 3 Pro: $2/$12/M tokens) |
| **Claude** | ❌ No Research access | **Pro $20/mo**: Research included | **Max $100–200/mo**: Higher limits · **Team $25–30/seat/mo** | Web search: $10/1K queries + model tokens |
| **Perplexity** | 3–5 queries/day | **Pro $20/mo**: 20/month (reduced from 50) | **Max $200/mo**: Unlimited + Opus 4.6 | ~$0.41/query (Sonar DR: $2/$8/M tokens) |

Key pricing notes: ChatGPT Plus offers the best **queries-per-dollar ratio** at the mid tier (25 for $20). Gemini's **AI Plus at $7.99** is the cheapest paid entry point with Deep Research access. Perplexity Pro's limit reduction from 50 to **20 queries/month** in early 2026 (unannounced) generated significant user backlash. Claude requires a Pro plan minimum ($20/month) with no free Research access.

---

## Prompting recommendations: a practical reference card

### ChatGPT Deep Research

**Do:**
- Front-load specificity: include objectives, scope, time frame, geography, industry, and desired output format
- Use the **"Sites → Manage sites"** feature to restrict to authoritative domains before starting
- Connect relevant data sources (FactSet, PitchBook, Google Drive) before initiating research
- Review and edit the research plan ChatGPT proposes before execution
- Request tables explicitly when comparisons would help
- Specify "prioritize official/primary sources over aggregators"

**Don't:**
- Submit vague prompts — the system benefits enormously from upfront specificity
- Restart queries mid-session (each counts against quota)
- Trust output verbatim without checking citations — OpenAI acknowledges hallucination risk
- Expect write actions — Deep Research is read-only across all integrations

**Tool-specific:** Select "Deep research" from the tool menu or type `/deep research`. The intermediate model will rewrite your prompt automatically — you don't need to optimize for the research model's format, just for clarity of intent.

### Gemini Deep Research

**Do:**
- Start simple, then refine — Google's own PM advises against overthinking the initial prompt
- Include extensive background context directly in the prompt (the 1M context window supports it)
- Place **critical instructions at both the beginning and end** of long prompts — the model can lose track of mid-prompt instructions
- Explicitly instruct how to handle missing data: "If specific figures are unavailable, state they are unavailable rather than estimating"
- Edit the research plan before execution — this is your primary lever for quality
- Use follow-ups to deepen specific sections after the initial report

**Don't:**
- Expect access to paywalled content — plan around this limitation
- Assume the default output length is sufficient — explicitly set `maxOutputTokens` in the API (default is only 8,192)
- Forget to specify format requirements (headers, tables, tone)

**Tool-specific:** Use the source dropdown to select Gmail, Drive, or Chat when you want Workspace data included. Note that visual reports become unavailable when Workspace sources are used in the same run.

### Claude Research

**Do:**
- Provide purpose context: "I'm writing a board presentation" versus "I'm choosing a vendor" steers depth and format
- Use structured prompts with **XML tags** for clear sections (INSTRUCTIONS / CONTEXT / TASK / OUTPUT FORMAT)
- Explicitly request citations: "Cite all claims with source URLs"
- Give permission to express uncertainty: "If the data is insufficient, say so rather than speculating"
- Leverage the 1M context window (now GA) for extensive background documents
- Set large output token budgets: 64K+ tokens at medium or high reasoning effort
- Use the `allowed_domains` and `blocked_domains` API parameters for source control

**Don't:**
- Over-prompt — tools that under-triggered in previous Claude models now trigger appropriately
- Expect a dedicated research API — Claude Research uses standard models with tools, not a specialized research model
- Assume broad web coverage — Brave Search's index is smaller than Google's; for niche topics, steer toward known sources
- Skip citation verification — Claude can occasionally cite sources that don't fully support claims

**Tool-specific:** Research automatically enables extended thinking. If Research doesn't engage on its own, explicitly say "Please use the Research tool to investigate..." You can steer mid-research with follow-up prompts that build on already-gathered findings.

### Perplexity Deep Research

**Do:**
- Use **natural language** — no role-play prompts, no few-shot examples, no system block markers
- Apply the **3-Layer Research Chain**: Layer 1 (landscape query for broad overview) → Layer 2 (focused deep-dive) → Layer 3 (verification of key claims)
- Use **Focus modes** strategically: Academic for peer-reviewed sources, Social for community sentiment, default for breadth
- Use Spaces for project-based research with custom instructions and file uploads
- Plan for shorter output — use multi-turn follow-ups for comprehensive coverage

**Don't:**
- Use role-play prompts ("Act as a McKinsey consultant") — this triggers irrelevant web searches
- Include few-shot examples — these trigger searches for example content rather than the actual query
- Try to pack everything into one query — the output length is limited; iterate instead
- Assume Pro tier has generous limits — the current cap is **20 Deep Research queries per month**

**Tool-specific:** Perplexity's citation quality is its core strength, so you rarely need to request citations explicitly — they're built in. Focus your prompting energy on scope definition and source type selection rather than output formatting.

---

## Conclusion: matching tool to task

The most important insight for prompt engineers is that **these tools are not interchangeable** despite similar architectures. Each has a structural advantage that shapes optimal prompting strategy.

**Gemini owns the benchmark leaderboard** and brings Google Search's unmatched web index, making it the default choice for comprehensive research requiring broad source coverage. Its 1M context window also makes it ideal for prompts that include extensive background documents. **ChatGPT leads in enterprise data integration** — if the research needs to synthesize internal documents alongside web sources, no competitor matches its connector ecosystem. Its 100K output token limit also makes it the only realistic option for prompts requesting truly exhaustive reports.

**Claude's "refuse rather than guess" calibration** makes it structurally the safest choice for high-stakes research where a fabricated fact is worse than a gap — legal, medical, and compliance work. But it lacks a dedicated research model and has the weakest search infrastructure (Brave vs. Google/Bing). **Perplexity is the speed and citation champion** — for iterative research workflows where the user plans to verify and refine across multiple quick rounds, its 2–4 minute turnaround and 85% citation accuracy are unmatched. Its output brevity is a real constraint that prompts must account for through multi-turn strategies.

The single most actionable finding: **prompt structure should vary fundamentally by tool.** Gemini benefits from extensive inline context and editable plans. ChatGPT benefits from specificity upfront and source restriction configuration. Claude benefits from structured XML prompts with explicit uncertainty permissions. Perplexity benefits from natural language with iterative follow-ups. A universal prompt template across all four tools will underperform a tool-specific one by a significant margin.