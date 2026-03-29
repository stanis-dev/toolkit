# Executive Summary

**ChatGPT Deep Research** (OpenAI) excels at thorough multi-source synthesis with strong reasoning. It uses a GPT-5.x “Thinking” model (as of Mar 2026, GPT-5.4 Thinking)【30†L135-L143】, runs agentically through web search and user-provided sources, and produces detailed reports with citations. **Gemini Deep Research** (Google) shines with real-time access to Google Search and Workspace; its agent uses Gemini 3.1 Pro, can browse *“hundreds of websites”* in parallel【37†L42-L48】 and integrate Gmail/Drive/Chat data. **Claude Research** (Anthropic) handles extremely large contexts (up to ~200k tokens) and multi-agent parallel search: lead agent uses Claude Opus 4.6 (with Sonnet 4 subagents)【21†L69-L77】, yielding very deep analysis. **Perplexity Deep Research** pairs a powerful model (Anthropic-based “Opus 4.5” as of early 2026【28†L49-L53】) with its own search engine to deliver focused, citation-rich reports. 

In brief, ChatGPT is best for balanced multi-source research with smooth UI; Gemini is unmatched for up-to-date, expansive web and personal data integration; Claude is best for projects with *very* long context and complex multi-step analysis; and Perplexity is best for researchers prioritizing accuracy and efficiency on benchmarked research tasks. The single biggest differentiator is each tool’s architecture: ChatGPT and Perplexity use (mostly) single-agent RAG-like pipelines, while Gemini and Claude use true multi-step agentic workflows to autonomously plan, search, and synthesize across many sub-tasks【21†L105-L113】【37†L42-L48】.

# ChatGPT Deep Research (OpenAI)

## 1. Model and Architecture

- **Model:** By Mar 2026, ChatGPT Deep Research uses OpenAI’s latest “Thinking” models (e.g. GPT-5.4 Thinking)【30†L135-L143】【30†L145-L152】. These frontier models are optimized for reasoning, coding, and tool use, and explicitly improve deep web research tasks.  
- **Architecture:** It functions as a single “research” agent augmented with web search and tools. The user defines a research goal, then ChatGPT generates a plan and iteratively executes it. The model searches the web, ingests uploaded files or connected-app data, reasons, and composes the final report【3†L28-L35】. Users can intervene mid-run to refine focus. This is an agentic, multi-turn pipeline (not a one-pass RAG).  
- **Process:** Workflow is user-driven planning: *User prompt → model proposes a structured plan → user reviews/edits plan → ChatGPT executes searches and reads content (guided by the plan) → synthesizes findings → final report with citations and sources.* The report is displayed in a full-screen view with table-of-contents, source list, and editable results【3†L112-L120】【3†L120-L127】.  
- **Session Duration:** Research tasks typically take **several minutes** (often 5–30 min) per query【39†L177-L184】【32†L677-L680】. Complex, comprehensive tasks (e.g. detailed academic surveys) can take longer (users report hours for very deep dives).  
- **Sources Consulted:** ChatGPT can incorporate many references. Official descriptions and user tests note that Deep Research “autonomously brows[es] the web”【39†L177-L184】. In practice it may visit *tens of sources* (and could be dozens) during a session, though exact counts vary. (By comparison, Gemini boasts “up to hundreds” of pages【37†L42-L48】.)  

## 2. Input Capabilities & Constraints

- **Max prompt size:** Very large. In GPT-5.4 Thinking mode ChatGPT supports a ~256K-token context window (128K tokens input, 128K output)【1†L248-L252】. Deep Research queries should fit within ~128K input tokens.  
- **File uploads:** Yes. Users can attach up to 20 files (e.g. PDFs, docs, spreadsheets, text, code) per message【1†L283-L290】. Supported formats include text files (.txt, .csv, .json, .md, code languages), common office docs (.docx, .xlsx, .pptx), and PDFs, among others【1†L283-L290】. (Maximum file sizes are determined by the 20-file limit and overall token budget.)  
- **Source control:** Users can restrict or prioritize sites. Deep Research lets you specify particular URLs or domains to focus on, or mark certain sites as “trusted”【3†L96-L100】. You can also exclude sources by prompt or use the UI to “restrict research to these sites only.”  
- **Workspace integration:** ChatGPT can connect to user data via “connected apps.” This includes Google Drive, Google Docs, Slack, OneDrive/SharePoint, and specialized databases (e.g. FactSet, PitchBook, Scholar Gateway)【3†L79-L87】. With permission, Deep Research can fetch the user’s emails, calendars, documents, etc., integrating internal info into the analysis.  
- **Conversation context:** The research task is part of the ongoing chat. Context from earlier messages in the same thread is retained and can be leveraged. (Deep Research outputs are added to the chat history and can be referenced in follow-up prompts.) There is no persistent cross-session memory beyond normal ChatGPT features.

## 3. Output Capabilities

- **Max output length:** Very long. Output reports can approach the model’s output limit (~128K tokens, on the order of ~100,000 words). In practice, ChatGPT formats the answer as a multi-section report (often with hundreds or thousands of words, depending on query complexity).  
- **Citations:** ChatGPT includes citations to sources. All reports end with a list of references or footnotes (“sources used”) so the content can be verified【3†L120-L127】. Citations appear as URLs or footnote markers in the text. The UI shows a “Sources used” panel linking back to web pages. (However, accuracy of links is subject to normal LLM risks, so users should check originals.)  
- **Export formats:** After completion, the report can be downloaded as Markdown, Microsoft Word, or PDF【3†L124-L127】. The UI provides share/export functions in those formats.  
- **Structured output:** Yes. Deep Research produces fully structured reports: it generates a table of contents, headings, numbered lists, etc., as needed. Outputs are typically broken into sections with headings, bullet points, tables or code blocks as appropriate. (Users can prompt for specific structure too.)  
- **Follow-up:** Strong. Users can refine or extend the research within the same session. The Deep Research interface allows interrupting the run to change the plan or add queries【3†L30-L34】. After a report is returned, you can ask ChatGPT to dig deeper on a subtopic, revise the report, or start a new research task, continuing the multi-step process without losing prior results.

## 4. Web Search & Sources

- **Search mechanism:** ChatGPT Deep Research uses a live web search tool (effectively Microsoft/Bing search under the hood). It dynamically queries for up-to-date info beyond its training cutoff. (GPT-5.4’s knowledge cutoff was Aug 31, 2025【5†L653-L656】, but the search tool provides current data.)  
- **Search depth:** The model explores multiple pages per query. Official sources say it “autonomously browses the web”【39†L177-L184】. In testing, it appears to parse many search results iteratively. Exact counts aren’t published, but user experiences suggest it may follow dozens of links.  
- **Recency:** Access is effectively current. The integrated search fetches latest content from the live web. There is no fixed lag (unlike knowledge cutoffs). ChatGPT Deep Research can cite news or papers published days before.  
- **Source diversity:** ChatGPT generally prioritizes high-quality sources (academic, news, technical docs) but may also sample broader sites. It will cite whatever it deems credible based on its reasoning. Users have noted it sometimes overuses Wikipedia or top-100 results; specifying sources can mitigate this.  
- **Paywalled content:** By default, ChatGPT cannot bypass paywalls. It can only see snippets indexed by search or known via open caches. It will not natively pull from subscription services or academic paywalled journals unless that content is mirrored or summarized elsewhere. (No indication Deep Research has special access to proprietary databases.)  

## 5. Accuracy and Reliability

- **Benchmarks:** OpenAI has not published formal benchmarks for Deep Research mode. However, an (outdated) report noted GPT-5.1-based Deep Research scoring 26.6% on the “Humanity’s Last Exam” benchmark【39†L185-L192】. OpenAI’s own internal evaluations (e.g. BrowseComp) suggest multi-agent browsing boosts performance dramatically【21†L69-L77】, but these are internal data. Independent commentary praises the credibility of ChatGPT’s cited answers, though notes occasional errors.  
- **Hallucination risk:** Like all LLM-based research tools, ChatGPT Deep Research can hallucinate facts or citations. OpenAI acknowledges it “occasionally” makes factual errors【39†L193-L196】. In practice, users report mostly accurate summaries, but fabricated or inaccurate claims and sources do occur. Verification by checking the cited URLs is advised.  
- **Self-correction:** ChatGPT will often hedge uncertainty (“sources say X” vs definitive statements). If inconsistencies appear, the user can have it re-check. The interface lets users interrupt and ask clarifying questions mid-run. GPT-5.4’s “Thinking” model also plans its reasoning and allows course correction (the UI plan-edit feature【30†L145-L152】). However, ChatGPT Deep Research does not autonomously fact-check all outputs (it trusts its retrieval chain); user guidance remains important.  

## 6. Prompting Recommendations

- **Ideal prompt structure:** Use a clear, objective tone. Explicitly state the research question, desired output format, and any constraints. For example: “*Research X topic and produce a detailed report with citations, covering A, B, C.*” Begin with context and goals (“I need an overview of...”, “Compare these two products...” etc.). According to OpenAI, best prompts *“describe the question, desired outcome, and any constraints”*【3†L22-L26】.  
- **Planning:** ChatGPT will propose a plan, but you can also ask it to outline steps before running (e.g. “First make a plan”). Review or adjust the plan if needed. Including bullet-point sub-questions in the prompt can guide thoroughness.  
- **Context handling:** If you have extensive background (articles, notes), attach them as files instead of pasting text. ChatGPT will retrieve relevant excerpts via RAG rather than ingesting entire uploads. Explicitly refer to uploaded sources in your prompt (e.g. “Based on the attached whitepaper, summarize…”).  
- **Clarity and scope:** Be precise. Vague or overly broad questions can confuse the agent. Break up very large tasks into sub-questions if needed. Avoid asking rhetorical or hypothetical queries that don’t map to factual searching.  
- **Source instructions:** If you need certain types of references, say so (“prefer peer-reviewed articles,” “focus on educational sources,” etc.). ChatGPT will attempt to follow but double-check it did not stray.  
- **What to avoid:** Don’t expect true multi-lingual or multimedia research unless specified. Avoid lengthy epilogues or tangential chat in the prompt. Don’t trust it to find extremely obscure or private data (e.g. unpublished proprietary info). Prompting to “hallucinate fewer sources” or explicitly “show your work” can sometimes reduce fabrication.  
- **Explicit instructions:** You generally do **not** need to tell ChatGPT to “search the web” – it does so automatically in Deep Research mode. However, you should prompt it to *cite sources* (it does by default, but reminders like “please include references” can help). You can also instruct the model to “prioritize XYZ sites” or “exclude XYZ sources” to control scope.  

# Gemini Deep Research (Google)

## 1. Model and Architecture

- **Model:** Gemini Deep Research runs on Google’s Gemini 3 series. Official docs state it is *“powered by Gemini 3.1 Pro”*【12†L195-L198】. (The user-facing “Gemini Advanced” product uses the same backend model.)  
- **Architecture:** A true multi-agent system. Gemini’s Deep Research uses an “agentic” workflow with planning and parallel search threads. It autonomously decomposes the query into sub-tasks, uses Google Search and an internal “url_context” browser tool, and spawns sub-agents to research different angles simultaneously【21†L105-L113】【21†L113-L122】. All tools (web search, browsing, file search) are run under Gemini’s control. After collecting data, the main agent synthesizes the findings into a report.  
- **Process:** Users initiate a Deep Research task (via the app or API). The system then outlines a plan and simultaneously launches searches. Google’s infrastructure lets it *“automatically browse up to hundreds of websites”* in parallel【37†L42-L48】, analyzing results in real time. The sub-agents return raw facts to the lead agent, which consolidates them and ensures coverage of all subtasks. A final “CitationAgent” then finds where to cite sources in the text【21†L127-L136】.  
- **Session Duration:** Typically on the order of **minutes**. Google notes that Deep Research tasks can take “several minutes” to run【12†L199-L204】. In practice, simple topics might finish under 1–2 min, whereas deeply complex ones may run longer (though usually under ~10 min).  
- **Sources Consulted:** Extensive. Gemini explicitly says it can scan *hundreds* of pages【11†L39-L43】. Each sub-agent may search dozens of results, and parallelism means total sources could reach into the low hundreds for a broad topic. The agents also search Google’s billions of indexed pages, so source diversity is extremely high.

## 2. Input Capabilities & Constraints

- **Max prompt size:** The user query is a standard text prompt (no large-context consumption by the model itself). Gemini doesn’t advertise a fixed token limit for the initial question, but it’s generally similar to other chat interfaces (a few thousand tokens max). The heavy lifting is done by agents with separate contexts.  
- **File upload:** Yes (in supported interfaces). Gemini Deep Research can ingest user files via Google Drive integration or direct upload. The “File Search” tool lets it read PDFs, docs, spreadsheets, etc., from the user’s Drive or shared links【12†L283-L288】. File size limits are not public, but presumably large (few hundred MB) since Google processes big documents.  
- **Source control:** Limited UI control. Unlike ChatGPT, Gemini does not offer an explicit “restrict to these domains” toggle. You can indirectly influence sources by how you phrase the query (e.g. “according to New York Times…”), but no built-in source restrictions are documented.  
- **Workspace integration:** Strong. Gemini can access the user’s Google Workspace data (Gmail, Drive, Google Docs, Google Chat) if the user has connected those accounts【11†L39-L43】【19†L57-L64】. In effect, it can incorporate your personal or company documents alongside web content. This is *native* to Gemini; no extra setup beyond granting permission.  
- **Conversation context:** Each Deep Research run is separate and starts fresh (it uses the prompt only). It doesn’t carry over previous sessions, though users can copy results into new queries. Within one research task, the agent keeps internal memory of its plan, but there is no long-term memory beyond that.  

## 3. Output Capabilities

- **Max output length:** Gemini outputs appear as multi-page reports. In the UI, the final answer can be dozens of paragraphs long. The precise token limit isn’t published, but likely on the order of tens of thousands of tokens (similar to other Gemini outputs). In practice, reports can be quite lengthy and are scrollable.  
- **Citations:** Yes. Gemini Deep Research generates cited output. The lead agent’s workflow ensures each factual claim is traced back to a source. The interface shows footnotes or link references for each claim. Google emphasizes “citations” throughout its docs (e.g. the Deep Research page promises *“detailed, cited reports”*【12†L195-L198】). These citations include direct URLs. Because Gemini uses live search, the links point to real pages.  
- **Export formats:** Currently, output is primarily viewed in the Gemini app. There is no native “export to Word/PDF” button in standard Gemini (as of Mar 2026). However, you can copy text out, or in Google Workspace-connected environments, send results to a Google Doc. No official PDF/Markdown download is offered yet.  
- **Structured output:** Gemini reports are highly structured with headings, bullet lists, tables, etc. The interface itself provides navigation and sometimes interactive elements (e.g. graphs or “notebook” widgets). The output is organized into clear sections reflecting the research plan.  
- **Follow-up capability:** Once a research run starts, the user cannot inject new queries until it finishes (unlike Perplexity’s live follow-ups). But after getting the report, you can refine by asking a new question or starting another Deep Research task. Gemini also offers an “editing” sidebar (NotebookLM integration) where you can annotate and iterate on results after the fact.

## 4. Web Search & Sources

- **Search mechanism:** Gemini Deep Research uses Google Search. The agent calls an internal Google Search API (“google_search” tool) to retrieve relevant pages, then “url_context” tools to fetch and read them【12†L283-L288】. This is Google’s own web index, so recall is extremely broad.  
- **Search depth:** Very deep. Google explicitly says it can browse “hundreds of websites” in a single session【11†L39-L43】. Each sub-agent queries Google and reads many results. There is no formal limit published; the agents typically cascade (e.g. if one search is too broad, sub-agents refine and fetch more). The result is extremely thorough coverage of the topic.  
- **Recency:** Real-time. Because it uses live Google Search, Gemini has up-to-the-minute data. It can find information posted within minutes or hours of the query. There is effectively no lag beyond search index update times.  
- **Source diversity:** Very broad. Google’s index includes news, research, blogs, forums, and more. In practice, Gemini often cites news articles, Wikipedia, academic sites, and niche blogs alike. Its agents explore multiple angles, so it tends to consult many source types rather than relying on a single site. There is no known bias toward any specific domain, aside from Google’s general ranking.  
- **Paywalled content:** No special access. It will not enter paywalled sites behind login. However, Google Search sometimes shows abstracts for subscription content; Gemini can use those if available. But it can’t directly fetch paywalled text. In general, it is limited to open or indexed content.

## 5. Accuracy and Reliability

- **Benchmarks:** Google has not published formal public benchmarks for Gemini Deep Research. However, marketing claims (as of 2025) promise state-of-the-art results. Independent testing by journalists suggests Gemini 3 holds up well against GPT-4/GPT-5 in accuracy. On internal tasks (BrowseComp-style), multi-agent systems like Gemini’s typically outperform single-agent baselines【21†L69-L77】.  
- **Hallucination risk:** Lower than ordinary chat. Because Gemini systematically references actual pages, it rarely invents facts without a source. Still, hallucinations can occur (e.g. misinterpreting content or mis-citing). Google’s agents do “interleaved thinking” to check consistency, but no published error rates exist. Users have found Gemini very reliable for factual info, though not flawless.  
- **Self-correction:** High. Gemini’s multi-agent loop inherently self-corrects by having sub-agents double-check information. The lead agent can spawn additional searches if something seems missing【21†L133-L142】. In the UI, you can also click on citations to verify the original. If the answer seems wrong, you can restart with clarifications, and Gemini’s agents will revise accordingly. However, it does not explicitly mark uncertainty the way some models do (it generally assumes found facts are correct if consistent).

## 6. Prompting Recommendations

- **Ideal prompt structure:** Keep it broad but well-scoped, as Gemini will break it down itself. For example, “*Investigate [topic] and prepare a detailed report covering A, B, C, with sources.*” Avoid too-narrow phrasing that could limit the agent’s autonomous planning. You can also supply “side questions” or sub-topics in the prompt to guide exploration.  
- **Clarifying questions:** Gemini often asks its own clarifications if the initial query is vague. To benefit from this, make your question complex enough to require multiple steps. You don’t need to ask “search the web” — just state your research goal. Gemini will automatically plan and ask you if needed.  
- **Context handling:** Large context beyond the initial prompt is not provided directly in text. If you have background documents, you can upload them to Google Drive and then mention them (e.g. “using the attached report on [file] and web data, analyze…”). Gemini can pull those files via Drive integration during the session.  
- **What to include:** Key elements are topic, scope, and any focus areas. Because Gemini is agentic, it can take open queries and decompose them, but giving bullet points or sub-questions can yield a more targeted report. E.g., “Report on Topic X including (1) historical context, (2) current status, (3) key players.”  
- **What to avoid:** Avoid extremely narrow yes/no questions or tasks that cannot be solved by factual research. Gemini is not for private or creative tasks. Also, don’t start with trivial queries (it’s meant for complex tasks). It’s usually best *not* to have all answers in mind; let the agent explore.  
- **Tool-specific notes:** You do *not* need to say “search web” — Gemini Research always searches. If you want it to use your own data, make sure your Google accounts are connected. For the Chrome/UI version, simply clicking “Deep Research” is enough. No special syntax is required.

# Claude Research (Anthropic)

## 1. Model and Architecture

- **Model:** Claude’s research is powered by its latest high-capacity models. In practice (as of early 2026) Claude Research uses a combination of **Claude 4.6 (Opus)** as the lead reasoning model and **Claude 4.x (Sonnet)** as subagents【21†L69-L77】.  (On Claude’s consumer service, Pro/Team users typically use Sonnet 3.5 for simple tasks and Opus 4.6 for hard ones; Research mode unleashes the Opus-class agents.)  
- **Architecture:** Claude Research is explicitly a multi-agent system. When you ask a question in Research mode, one Claude agent (the LeadResearcher) devises a plan, then spawns multiple parallel subagents each searching different aspects (via web search or connected tools). Each subagent fetches info and returns summaries to the lead, which synthesizes them. Finally, a citation-pass ensures all claims have sources【21†L127-L136】. This orchestrated “orchestrator-worker” design lets Claude pursue many threads concurrently.  
- **Process:** Similar to Google’s, Claude’s Research pipeline is: *Analyze query → plan strategy (saved to memory) → create subagents with specific search tasks → each subagent uses web search tools and internal chains-of-thought → aggregate findings → optionally spawn more subagents if needed → finalize report → CitationAgent tags facts to URLs for footnotes.* This loop continues until the system judges the answer complete【21†L125-L134】【21†L135-L142】.  
- **Session Duration:** Many minutes. Claude’s Research is thorough and computationally heavy. Although no official timing is published, users and Anthropic describe answers arriving “in minutes” rather than seconds【19†L39-L45】. Given the multi-agent nature, expect typical reports to take ~5–10 minutes or more on complex topics.  
- **Sources Consulted:** High. Claude’s multi-agent system is reported to examine on the order of **50–100 sources** per task (user reports suggest around 50–100 distinct pages)【42†L144-L148】. The subagents cast a wide net, so coverage is deep. The final answer includes multiple citations (often dozens) spanning news, scholarly articles, and more, systematically aggregated.

## 2. Input Capabilities & Constraints

- **Max prompt size:** Very large. Claude Opus 4.6 supports up to ~200,000 tokens of context【21†L129-L136】. In research mode, user prompts can include substantial context. Unlike ChatGPT, Claude will actually read attached documents start-to-finish (retrieval isn’t used for uploads)【17†L120-L128】. So you can paste or upload very long texts (200k tokens ≈ 150K–160K words) for it to process in-line.  
- **File upload:** Yes. Claude supports uploading documents in the chat interface (via the Claude.ai web or Cowork desktop). It can ingest PDFs, text files, spreadsheets, etc. Large files up to hundreds of pages are supported because Claude’s long context can accommodate them wholly【17†L120-L124】. When you upload, Claude reads the entire document.  
- **Source control:** You can steer Claude Research via prompts. For example, asking “please use only these websites: …” may help, though no GUI for site selection is provided. More effectively, use Claude’s feature flags: make sure “web search” is enabled (per [19†L47-L54]). There is no explicit site whitelist UI, but Claude tends to follow prompt instructions about source preferences.  
- **Workspace integration:** Via Google integrations. If you enable Google Workspace in Claude settings, Research mode will search your Gmail, Calendar, Docs, etc. as part of the query【19†L57-L64】. This lets Claude incorporate your private data. However, there is no direct “file upload to Claude Drive” aside from the standard uploads above. For local files, Anthropic’s “Claude Cowork” desktop tool can access your machine via the Model Context Protocol (MCP)【17†L87-L96】, but that is separate from the web interface.  
- **Conversation context:** As with other Claude chats, context persists within the session (Claude has no user memory beyond the chat thread). Within a Research chat, you can recall earlier messages. There is no automatic memory across separate research tasks unless manually copied.

## 3. Output Capabilities

- **Max output length:** Very large (since Claude can output a lot within the same context). Officially, Opus 4.6 allows up to 200k tokens total, including prompt and answer【21†L129-L136】. In practice, answers can be tens of thousands of words long. The final report can span multiple “documents” or screens in the interface.  
- **Citations:** Yes. Claude’s Research includes citations. Its automated pipeline ensures every key statement is footnoted. The format is usually numbered endnotes with URLs. Citations link to the original source. Because of the citation agent, hallucinated references are rare – most come directly from browsed content.  
- **Export formats:** The Claude UI lets you copy text. There is no built-in “download PDF/Word” button (as of Mar 2026). However, one can highlight/copy the formatted report or use the API to retrieve the text. In a Claude Cowork project, outputs can be exported as HTML/MD. (No proprietary format is needed.)  
- **Structured output:** Yes. Claude’s output is highly structured with sections, bullets, and tables as needed. The research report often starts with an outline or summary, then sections for each subtask. Claude also shows an interactive “Artifacts” panel where content is formatted side-by-side.  
- **Follow-up capability:** Similar to Gemini, once a research run begins it runs to completion uninterrupted. However, after the report is done, you can immediately ask Claude to refine or continue in the same conversation. For example, “Can you expand section 2?” or “Now compare X and Y.” Claude’s extended context (200k tokens) easily incorporates follow-up within the same thread. 

## 4. Web Search & Sources

- **Search mechanism:** Claude uses Google Custom Search (or its own web crawler) as the search tool in Research mode. (Anthropic documentation states Claude’s Research agents use a “web search tool” to fetch information from the internet【21†L123-L132】.) It’s not publicly documented whether this is Bing or Google, but functionally it behaves like a standard search engine.  
- **Search depth:** High. The multi-agent design means Claude performs many parallel searches. Internal descriptions say subagents use “interleaved thinking” to iteratively call the search tool【21†L133-L142】. There’s no published limit, but users report Claude routinely fetching ~50–100 sources【42†L144-L148】. Claude will issue additional searches if needed (e.g. if a subagent finds a new avenue).  
- **Recency:** Real-time. Claude’s search tool queries the live web, so it can find very recent info. It has no fixed data lag (beyond the underlying search index). Like Gemini, it should be current to within days or less.  
- **Source diversity:** Broad. Claude agents appear to draw from news sites, academic publications, official stats, Wikipedia, etc. The multi-agent approach explicitly explores “different angles” simultaneously【21†L46-L54】, so the sources are varied. Anthropic has not reported any tendency to over-rely on one site (and indeed their design tries to avoid single-thread bias).  
- **Paywalled content:** No special access. Claude Research uses public web search and cannot read paywalled content behind login. It may glean limited info from meta descriptions, but otherwise is blocked by paywalls like anyone else. (However, Claude Cowork could theoretically open local copies of articles if you provided them.)

## 5. Accuracy and Reliability

- **Benchmarks:** Anthropic has published internal research benchmarks indicating multi-agent Research excels at certain tasks. For example, a team evaluation found Claude’s multi-agent Research scored ~90% better on a BrowseComp-like task than a single agent【21†L69-L77】. There are no public third-party scores for Claude Research specifically. Anecdotally, users find Claude very accurate and systematic.  
- **Hallucination risk:** Claude’s design heavily minimizes hallucinations. The citation agent especially ensures facts are source-backed. That said, hallucinations can still occur if a chain-of-thought misinterprets info. Claude’s published research acknowledges LLMs can hallucinate, and suggests multi-agent search “drastically” reduces it. In practice, Claude reports tend to be factual with clear source grounding.  
- **Self-correction:** Built-in. The lead agent can redirect subagents if it detects a gap. Claude also supports user steering: if the assistant misses something, you can say “Double-check claim X” or “look for more recent data on Y.” Internally, its agents persist their plan in memory (to avoid losing context)【21†L129-L136】, which helps maintain consistency. Claude also offers “undo” or plan-edit features so you can refine the direction mid-run.

## 6. Prompting Recommendations

- **Ideal prompt structure:** Enable Research mode (toggle “Research” blue). Then simply pose your question clearly. E.g. “*Research the impact of [policy] on [industry] and compile an evidence-backed report covering A, B, and C.*” Because Claude is agentic, you don’t need detailed instructions — it will autonomously make a plan. However, including key subtopics in your prompt helps guide the plan.  
- **Clarify usage:** If Claude isn’t automatically using research (e.g. if button isn’t on), you can say explicitly: “Claude, please use your research tool to…”【19†L69-L72】. If needed, ask it to use specific internal sources: “Pull relevant context from my Google Docs.” This steers it to incorporate your connected data【19†L76-L80】.  
- **Context handling:** You can paste or upload very large context. Claude will read it all (up to ~200k tokens)【17†L120-L128】. For very long docs, a single upload is usually enough; no need to summarize first. If including prior conversation or data, you can just mention it or paste it — Claude will consume it.  
- **What to include:** As with any query, include the main question and goals. If you have assumptions or prior findings, state them. For example: “Given [fact from my data], what are the implications for [X]?” Claude can incorporate that context.  
- **What to avoid:** Don’t give Claude Research trivial prompts; it expects multi-step tasks. Also avoid overly conversational or off-topic comments. Remember to stay in research mode — questions like “what do you think?” may shift it out of planning.  
- **Tool-specific instructions:** By default, Claude Research uses web search, so no need to say “search online.” However, ensure you have “Research” toggled on【19†L49-L54】. Explicitly request citations or say “list sources,” and Claude will include them. If it’s not searching enough, prompt: “Claude, use your web search to find references.” But typically, once Research mode is enabled, the agentic pipeline runs automatically.

# Perplexity Deep Research

## 1. Model and Architecture

- **Model:** Perplexity Deep Research uses Perplexity’s top-tier LLMs. As of early 2026, Perplexity runs research tasks on “Opus 4.5” (an Anthropic Opus-equivalent model) for both Pro and Max users【28†L49-L53】. (They mention upgrading to “4.6” soon.) This is a large, agentic-capable model akin to Claude. Lower-tier Pro users may use “Opus 4.6 Thinking” when available【24†L68-L74】.  
- **Architecture:** Perplexity uses a mainly single-agent retrieval pipeline, not an explicit multi-agent system. It couples its proprietary search engine (“Sonar”) with the LLM. The model iteratively queries the search engine, retrieves and summarizes relevant chunks, and repeats as needed. The “Thinking” variant enables advanced chain-of-thought. The architecture is thus more RAG-like than Claude/Gemini, but enhanced for deep search and analysis. Perplexity did not announce a separate multi-agent mechanism.  
- **Process:** When you submit a Deep Research query, Perplexity runs multiple search queries (often guided by LLM reasoning) and collects information in real time. It cross-references facts across sources. The exact loop is opaque, but the output is one comprehensive answer. Perplexity’s interface also shows key findings and stream of thinking as it goes. New Deep Research adds features like clarifying questions, follow-ups, and a progress view【24†L79-L88】, suggesting an interactive retrieval process.  
- **Session Duration:** Faster than ChatGPT or Claude in many cases. Perplexity markets Deep Research as more efficient. Typical runs likely take 1–5 minutes. There’s no official timing, but its focus on speed and key-findings suggests shorter waits. (The UI’s progress indicators suggest users rarely wait more than a few minutes.)  
- **Sources Consulted:** Perplexity Deep Research explicitly increases “searches more sources”【24†L45-L52】. While it likely visits dozens of pages, it may use fewer sources than fully agentic systems. The number varies by plan: “Pro Search” mode gives 3× normal sources【26†L48-L56】, and Research mode likely uses many. Published claims say it “outperforms” others on benchmarks, implying thorough sourcing. In practice, users see dozens of references.  

## 2. Input Capabilities & Constraints

- **Max prompt size:** Standard. The query prompt length is similar to other chatbots (a few thousand tokens max). There’s no special extended context window for user prompts. Perplexity’s strength is in subsequent searching, not huge prompt ingestion.  
- **File upload:** Yes. The new Deep Research can “process and work with uploaded documents directly”【24†L56-L63】. Users can attach PDFs and documents, which the system will parse and analyze. The specifics of file limits aren’t documented, but likely moderate (e.g. a few MB or ~500 pages).  
- **Source control:** Not explicitly user-controlled. There is no documented way to lock to specific domains. If you need to focus on a site, mention it in the prompt, but there’s no official toggle.  
- **Workspace integration:** None. Perplexity cannot connect to personal apps like Google Drive or Gmail. All research is over the public internet and any uploaded files.  
- **Conversation context:** Within one session, the assistant remembers previous messages, so you can build a research thread. However, there is no persistent memory or project save beyond the chat. Each Deep Research is a separate process. After a report is generated, you can ask follow-up questions in the same chat.

## 3. Output Capabilities

- **Max output length:** Moderate. Perplexity’s UI streams answers, and reports can be quite long (several thousand words). The exact token cap isn’t public, but likely on the order of 50K tokens or less. The interface shows a scrolled final answer and a complete report.  
- **Citations:** Yes. Every answer (including Deep Research reports) includes numbered citations linking to URLs. As Perplexity markets, these are usually real links to the cited sources. The citations appear inline as footnotes. The “Advanced Deep Research” page emphasizes comprehensive citations【24†L45-L52】.  
- **Export formats:** Currently, results can be copied or saved, but there’s no direct export to Word/PDF in the UI. The help says “research reports stream directly into a file, where you can edit and share”【24†L101-L105】, implying perhaps a built-in editor. (The UI does let you edit and highlight as you go.) There is no explicit download button, though you can copy text or use Print-to-PDF.  
- **Structured output:** Yes. Perplexity’s reports use headings, bullet lists, and sections. The new UI shows “Key findings” as they come, suggesting structure. Users can expect a report outline or Q&A format. The model can generate tables or code blocks if asked.  
- **Follow-up capability:** Unique. Users can *add follow-up questions while research is still running*【24†L86-L94】. The interface lets you type a new question mid-stream, which the agent will incorporate into the ongoing session. This is a powerful feature: you can steer or expand the research on-the-fly without waiting for the final report.

## 4. Web Search & Sources

- **Search mechanism:** Perplexity uses its own search technology. The “Sonar” model is paired with a proprietary search index (and possibly Google/Bing backend). The Help notes “Perplexity’s proprietary search engine”【28†L49-L53】. The interface is closely integrated: it shows search results in a sidebar, and the model queries them programmatically.  
- **Search depth:** High. Perplexity explicitly “searches more sources” in Deep Research mode【24†L45-L52】. While not quantified, it likely runs many queries and follows up on multiple leads. It may not parallelize as heavily as Claude/Gemini, but it is thorough and iterative.  
- **Recency:** Real-time. Perplexity uses live internet search, so it can access the latest information. It advertises “real-time answers” on its site. There is no known lag beyond search indexing, so it’s up-to-date.  
- **Source diversity:** Broad. Perplexity blends multiple models and search modes. It is known to include results from web, news, Wikipedia, and other trusted sites. The default “best” mode auto-selects among LLMs like GPT-5.2, Claude 4.6, etc.【26†L68-L77】, which diversifies responses. The help claims deep research *“searches more sources, cross-references information”*【24†L45-L52】, so it should not rely on a single site.  
- **Paywalled content:** Likely not. There is no special access. It will use search results as any user would. If a source is paywalled, it might cite the snippet Google provides or skip it. There’s no indication of subscription access to journals or archives.

## 5. Accuracy and Reliability

- **Benchmarks:** Perplexity explicitly cites benchmarks. Their LinkedIn post claims “state-of-the-art performance on all leading external benchmarks” for Deep Research, and mentions scores (e.g. 93.9% on OpenAI’s SimpleQA)【28†L46-L53】. Their help page likewise says it “matches or outperforms competitors on fact-finding, product comparisons, academic research, due diligence”【24†L45-L52】. While internal, these boast that Perplexity leads in accuracy compared to other research AI.  
- **Hallucination risk:** Lower than typical chat. The emphasis on many sources and cross-checking reduces fabrications. Perplexity’s updates explicitly tout improved accuracy and robustness【28†L46-L53】. However, no tool is perfect; Perplexity may still hallucinate if sources conflict. Users say it “can produce false positives if sources are ambiguous,” but the multi-source approach mitigates blatant fabrications.  
- **Self-correction:** Built-in through interface. The clarifying-questions feature means it can ask for context before answering, reducing mistakes【24†L81-L84】. And crucially, the live follow-up mechanism lets users immediately refine queries. This interactive loop helps catch and fix errors on-the-fly. The “thinking” mode and high-end models also mean the system internally chains reasoning, which aids consistency, but it does not explicitly flag uncertainty except by being vague.

## 6. Prompting Recommendations

- **Ideal prompt structure:** Be explicit about scope. For example: “*Conduct an in-depth analysis of [topic], including sections on A, B, and C. Provide detailed reasoning and cite sources.*” Since Deep Research asks clarifying questions upfront【24†L81-L84】, you can start with a broad question and let it refine. Specify any format (report, bullet points, etc.) if needed.  
- **Context handling:** You can upload documents; mention them in the prompt. For large context or data tables, use the file upload feature. If you have particular data (e.g. a CSV), say “analyze the attached file.” Perplexity will parse attachments directly into the session.  
- **Key prompt elements:** Emphasize depth (“in-depth analysis”), include subtopics, and ask for citations. Use actionable phrasing like “analyze,” “compare,” “summarize.” Because the system now asks clarifying questions, you can leave some leeway; it will say “should I focus on X or Y?” if the query is broad.  
- **What to avoid:** Avoid overly narrow or single-sentence queries — deep research mode expects complexity. Don’t ask for opinions or tasks outside factual research. Also, avoid extremely open-ended questions with no direction (“Tell me something interesting about X”).  
- **Tool-specific instructions:** You don’t have to say “use Deep Research” — select the mode in the UI instead. You should **explicitly ask for citations** if you want them (though it usually provides them anyway). There’s no need to say “search the web” — just ask the question. You *can* interject during the run with follow-ups (e.g. “Also look for Y”), and the system will incorporate them in real time【24†L86-L94】.

# Comparison Matrix

| **Aspect**                                 | **ChatGPT Deep Research**              | **Gemini Deep Research**            | **Claude Research**                    | **Perplexity Deep Research**         |
|--------------------------------------------|----------------------------------------|-------------------------------------|-----------------------------------------|--------------------------------------|
| **Model** (Mar 2026)                       | GPT-5.4 Thinking (OpenAI)【30†L135-L143】         | Gemini 3.1 Pro【12†L195-L198】           | Claude 4.6 Opus (lead) + Sonnet (sub)【21†L69-L77】 | Anthropic Opus 4.5 (paired model)【28†L49-L53】    |
| **Architecture**                           | Single-agent, plan-driven search & synth【3†L28-L35】 | Multi-agent, agentic (parallel subagents)【21†L105-L113】 | Multi-agent, orchestrator with subagents【21†L105-L113】 | Single-agent RAG-style with code-sandbox【24†L54-L63】 |
| **Search Tools**                           | Web search (Bing), integrated with GPT【39†L177-L184】 | Google Search (agent tool)【12†L283-L288】         | Web search tool (Google or similar)【21†L123-L132】      | Proprietary web search engine (Sonar)【28†L49-L53】    |
| **Speed**                                  | Several minutes (5–30min typical)【32†L677-L680】 | Minutes (often under ~10)【12†L199-L204】     | Several minutes per task【19†L39-L45】   | Few minutes (fastest; often 1–5 min)    |
| **Sources per session**                    | Dozens (user reports)【32†L677-L680】      | Hundreds (claims)【37†L42-L48】           | Dozens to ~100 (user reports)【42†L144-L148】    | Dozens (3× search results for Pro)【26†L48-L56】【49†L114-L118】 |
| **Web search recency**                     | Real-time Bing (no cutoff)              | Real-time Google (no cutoff)         | Real-time (uses live search)            | Real-time (uses live search)         |
| **Paywalled access**                       | No                                     | No                                  | No                                      | No                                    |
| **Maximum input size**                     | ~128K tokens (input)【1†L248-L252】         | Large (not explicitly capped; uses tools) | ~200K tokens (able to ingest very long docs)【21†L129-L136】 | Standard (~several thousand tokens)   |
| **File uploads**                           | Yes (up to 20 files; PDFs, docs, code)【1†L283-L290】 | Yes (via Drive and API tools)【12†L283-L288】   | Yes (large PDFs/docs; Claude Cowork for local) | Yes (supports document upload)【24†L58-L63】 |
| **Workspace integration**                  | Yes (Google Drive, Slack, Salesforce, etc.)【3†L79-L87】 | Yes (Gmail, Drive, Chat, Calendar)【11†L39-L43】 | Yes (Google Workspace: Gmail, Docs)【19†L57-L64】 | No (only public web and uploads)    |
| **Output length**                          | Very long (up to ~128K tokens)         | Very long (tens of thousands words)  | Very long (up to ~200K tokens)          | Long (likely up to tens of thousands of tokens) |
| **Citations**                              | Inline footnotes/links【3†L112-L120】         | Inline citations (footnotes)         | Inline citations (footnotes)            | Inline citations (footnotes)          |
| **Export formats**                         | Markdown, Word, PDF (built-in)【3†L124-L127】  | None built-in (text copy only)       | Copy text (HTML/MD via API)            | (No direct export; copy or print)   |
| **Follow-up**                              | Yes (can refine mid-run or new query)   | No live mid-run edits (start new if needed) | Yes (very long context allows continuous follow-ups) | Yes (can ask new Q mid-run)【24†L86-L94】 |
| **Best for Deep Research**                 | Balanced deep research with control and plan | Up-to-date/real-time data and Google integration | Extremely long context and thorough analysis | Highest factual accuracy and efficiency |
| **Best for Long Context**                  | ~128K tokens (thinking model)          | Moderate (Gemini context < 64K)      | ~200K tokens (reads end-to-end)【17†L120-L124】    | Moderate (likely ~few 10Ks tokens)   |
| **Best for Current Data**                  | Yes (Bing integration)                 | Yes (Google)                        | Yes (uses live web search)            | Yes (live search engine)            |
| **Best for User’s Files/Data**             | Yes (connected apps)                   | Yes (Drive/Gmail integration)       | Yes (Google Drive via integration or Cowork) | Partial (file upload only)          |
| **Best for Strict Citations**              | Good (user-editable refs)             | Good (structured citations)          | Good (automated citations)             | Good (footnotes, pro claims accuracy)|
| **Tokens efficiency** (output per input)   | Lower (many tokens used on plan/search) | Moderate (parallelism, but overhead) | Lower (multi-agent overhead)         | High (optimized search-driven outputs)|
| **Reliability (hallucination)**           | High risk of occasional errors【39†L193-L196】 | Lower (agentic checks)             | Low (multi-agent + citation agent)     | Low (benchmark claims)              |

# Pricing and Access

| **Tool**        | **Plan/Tier for Research**                    | **Usage Limits**                                    | **Cost**                         |
|-----------------|-----------------------------------------------|-----------------------------------------------------|----------------------------------|
| **ChatGPT**     | Research available on Free (limited) and paid tiers (Plus, Pro, Team, Enterprise)【19†L36-L44】【39†L219-L228】.  | Varies by plan: e.g. in early 2026 *Plus/Team/Ent* got ~10 full-research tasks/30d; *Pro* got ~250【39†L219-L228】; *Free* ~5 per month. (Limits change, check UI counter.)  | Free (with limited tasks); $20/mo for Plus (more tasks); higher for Team/Enterprise.  |
| **Gemini**      | Research included on Google AI **Free**, **Plus**, **Pro** plans【47†L53-L60】【47†L113-L117】. No separate add-on required.  | Free: 50 AI credits/day; Plus: 200 credits/month; Pro: 1000 credits/month【47†L69-L77】【47†L121-L129】. (Credits cover all Gemini usage.)  | Free plan: €0; Plus: €7.99/mo; Pro: €21.99/mo【47†L103-L112】【47†L159-L167】. (Prices in EUR) |
| **Claude**      | Research requires **paid** plan – Pro, Max, Team, or Enterprise【19†L36-L44】. (Free plan cannot use Research.)  | Same usage limits as standard chat on that plan【19†L82-L87】. Research queries consume tokens quickly but are counted under normal quotas.  | Pro ~ $20/mo; Max/Team ~ $136 CAD/mo (as of 2026, dependent on currency)【17†L113-L121】; Enterprise higher (custom pricing).  |
| **Perplexity**  | Deep Research requires **Perplexity Pro** or **Max**. (Not available on Free plan.)  | Pro plan: typically up to 20 Deep Research queries/month【49†L114-L122】; Max plan: higher (unspecified). Normal search queries have separate higher limits.  | Perplexity Pro: ~$25–30 USD/mo (depending on region); Perplexity Max: ~$100+ USD/mo (varies, often by promotion)【49†L114-L122】【52†L77-L85】.  |

*Notes:* All four tools are subscription-based, not per-query. ChatGPT and Claude charge monthly; Gemini uses a credit system under Google AI subscriptions; Perplexity has monthly tiers. Deep research usage is limited by plan quotas (queries per month or AI credits). There is generally no additional “per query” fee. Features like advanced models, large context, or priority access are gated by the higher tiers (e.g. Claude Max, Gemini Pro, Perplexity Max). Always check the provider’s latest pricing page for exact fees and limits.

# Prompting Recommendations (by Tool)

**ChatGPT Deep Research:**  
- ✔ *Do:* Frame your query clearly and specifically. Include goals and constraints (e.g. “Provide a detailed report on X, focusing on A and B”). Let ChatGPT plan – review or edit the proposed research plan. Ask for citations explicitly (though it does this automatically). Attach relevant docs or data files. Use bullet points or numbered sub-questions if it helps break down the task.  
- ✘ *Avoid:* Vagueness or multiple unrelated questions in one prompt. Overly casual language or open-ended rhetorical questions. Relying on Deep Research for nonsensical or non-factual tasks. Expecting it to know closed or proprietary content.  
- *Tip:* Say e.g. “Outline your plan first” to check the agent’s approach. Use site directives (“Restrict to domain X”) if needed. Don’t forget to use the “Interrupt” button to refine mid-run【3†L30-L34】.

**Gemini Deep Research:**  
- ✔ *Do:* Use broad, research-style queries. Let Gemini ask clarifying questions (its new UI does this for open prompts). Provide subtopics or side questions to shape the search (as a Gemini “Gem” can do). If using Google Workspace, mention relevant files (it will pull them automatically).  
- ✘ *Avoid:* Trying to micromanage the agent (it plans itself). Very short prompts – it works best with complex queries. Assuming it can read files without them in Drive.  
- *Tip:* Use the NotebookLM canvas after output to annotate or push Gemini’s research further. You don’t have to write “search web” – just ask, and make sure “Deep Research” is active.

**Claude Research:**  
- ✔ *Do:* Enable the Research mode toggle. Pose your question with all relevant details; Claude will plan automatically. Explicitly say “please use your Research tool” if needed【19†L69-L72】. Provide long documents in full (Claude can handle up to ~200k tokens); it will read them linearly. Ask for citations or clarify needed confidence levels.  
- ✘ *Avoid:* Asking Claude to do creative or abstract tasks in research mode. Giving confusing or contradictory context. Disabling web search when you need it.  
- *Tip:* Feed Claude your exact data or project files via upload or Cowork – it can work on them directly. If it misses something, prompt “see if you find anything in my files on [topic]” – it can retrieve from connected data【19†L76-L80】.

**Perplexity Deep Research:**  
- ✔ *Do:* Start with a clear directive (“Perform deep research on X. Include sections on Y and Z.”). Take advantage of the clarifying prompts: if it asks a question first, answer it to focus the search. Attach any documents for context. Use follow-ups during the run: e.g. type “Also look for how A affects B” while it’s computing.  
- ✘ *Avoid:* Ignoring the follow-up feature – it is unique here. Don’t ask “why” questions that are speculative. Avoid too many nested clauses; be explicit.  
- *Tip:* The system has “Research mode” – use it (it auto-selects models). To maximize output, choose “Research” or “Reasoning” modes rather than default. Remember you have a cap (≈20 deep searches/month on Pro【49†L114-L122】) so plan queries accordingly.

# Sources

- OpenAI Help Center, “Deep research in ChatGPT” (February 2026)【3†L22-L30】【3†L120-L127】  
- OpenAI Release Notes (Feb–Mar 2026)【1†L248-L252】【30†L135-L143】【30†L145-L152】  
- TechRadar “I tried Deep Research on ChatGPT…” (Mar 2025)【32†L677-L680】  
- Wikipedia, “ChatGPT Deep Research” entry (as of Mar 2026)【39†L177-L184】  
- Google Gemini Deep Research Overview (Google AI documentation, including Polish version)【11†L39-L43】【12†L195-L198】  
- Medium by Sacha Storz, “O1, Gemini, and Perplexity Deep Research in Comparison” (Mar 2025)【37†L42-L48】  
- Gemini API Docs: “Gemini Deep Research Agent” (Google AI Dev)【12†L195-L203】【12†L283-L288】  
- Claude Help Center, “Using Research on Claude” (Mar 2026)【19†L39-L47】【19†L76-L80】  
- Anthropic Engineering Blog, “How we built our multi-agent research system” (Jun 2025)【21†L69-L77】【21†L127-L136】  
- Reddit (ClaudeAI), user comment on Claude Research sources【42†L144-L148】  
- Perplexity Help Center, “What’s New in Advanced Deep Research” (Mar 2026)【24†L45-L52】【24†L58-L63】  
- Perplexity Help Center, “What advanced AI models are included in my subscription?” (Mar 2026)【26†L68-L77】【26†L98-L104】  
- Perplexity LinkedIn post, “Deep Research Upgrade” (Feb 2026)【28†L49-L53】  
- Reddit (Perplexity), “Notes on new limits for Perplexity Pro” (Apr 2026)【49†L114-L122】  
- Google AI Subscriptions page (Gemini pricing)【47†L53-L60】【47†L113-L117】  
- Claude ecosystem commentary (Nicolle Weeks, Feb 2026)【17†L113-L121】  

