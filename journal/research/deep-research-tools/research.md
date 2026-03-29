# Deep Research Tool Capabilities (March 2026)

## Summary

Cross-referenced comparison of four deep research tools (ChatGPT, Gemini, Claude, Perplexity) conducted March 19, 2026 by submitting an identical research prompt to three tools simultaneously and synthesizing the results.

## Key findings

- All four tools now use agentic multi-step architectures (plan -> search -> read -> iterate -> synthesize)
- **ChatGPT** (GPT-5.4): Best for long autonomous synthesis sessions, strongest workspace integration (FactSet, PitchBook, MCP), Bing search backend
- **Gemini** (3.1 Pro): Largest effective context (1M-2M tokens), native Google Workspace, Google Search backend, highest SimpleQA Verified score (77.5%)
- **Claude** (Opus 4.6): 1M context GA, lowest hallucination risk (refuses rather than guesses), fastest raw aggregation (261 sources in ~6 min), uses Brave Search (~30B page index, smaller than Google)
- **Perplexity** (Opus 4.6 / 4.5 + Model Council): Fastest turnaround (2-4 min), best citation quality (10x density, 85% accuracy), shorter output (~1K-2.6K words)
- Prompt structure should vary fundamentally by tool -- a universal template underperforms tool-specific ones
- None bypass paywalls natively (ChatGPT can via authenticated connectors)

## Methodology

The same prompt was submitted to ChatGPT Deep Research, Claude Research, and Gemini Deep Research. Results were cross-referenced to identify consensus facts, resolve disagreements, and evaluate each tool's performance on the research task itself.

### Tool performance on this task

1. **Gemini**: Most thorough (62 cited URLs), most novel architectural insights, most granular pricing
2. **Claude**: Best organized comparison matrix, correctly identified Brave Search as Claude's backend
3. **ChatGPT**: Least reliable -- 5+ factual errors including wrong Claude search backend, missing 1M context, understated Perplexity input capacity

## Source files

- `context/gemini-result.md` -- Gemini Deep Research output (primary source, 62 URLs cited)
- `context/claude-result.md` -- Claude Research output (best organized, good DRACO analysis)
- `context/chatgpt-result.md` -- ChatGPT Deep Research output (least accurate, some useful architectural details)
