---
name: deep-research-prompt
description: >-
    Generate context-enriched deep research prompts by ingesting existing research and interactively refining the
    research question. Use when the user wants to create a research prompt, expand a research topic, start a new
    research project, or prepare a prompt for deep research tools like ChatGPT, Claude, or Gemini.
---

# Deep Research Prompt Generator

Generate tool-agnostic research prompts enriched with existing context. Produces prompts optimised for deep research on
ChatGPT, Gemini, or Claude.

## Workflow

```
1. Gather context  →  2. Refine question  →  3. Generate prompt  →  4. Deliver
```

### Phase 1: Gather existing context

Context can come from any combination of sources. Use whatever is available:

- **Files on disk** -- if the user references files/directories, or the conversation implies a research project exists
  in the workspace, read those files
- **Current session** -- if the user has been discussing a topic, extract relevant context from the conversation history
- **User-provided** -- the user may paste or describe what they already know
- **None** -- if there is no prior context, skip to Phase 2

When context exists, build a **context summary** containing:

1. **Topics already covered** -- major areas from the research
2. **Key frameworks or models** referenced
3. **Key findings or conclusions** reached
4. **Open questions** -- areas flagged for future research
5. **Source quality notes** -- any caveats

Keep the summary dense but complete. This becomes the "What has already been researched" section of the prompt.

### Phase 2: Refine the research question

Walk the user through sharpening their question. Ask questions liberally.

**Ask in sequence (skip what's already clear from context):**

1. **Research question** -- "What specific question or area do you want to research next?" (open-ended)
2. **Output type** -- What kind of output do you need?

```
Options:
- Evidence review (what does the research say about X?)
- Comparison / decision support (A vs B, evaluated on criteria)
- Framework / model (build me a mental model for X)
- Actionable strategy (give me a plan for X)
- Exploratory (map the landscape of X)
- Other
```

3. **Anti-patterns** -- "Anything you specifically do NOT want?" (open-ended, optional)
4. **Constraints** -- "Any specific constraints the research should respect?" (geography, time horizon, budget, etc.)

After gathering answers, **summarise the refined research brief back to the user** in 3-5 sentences and ask for
confirmation before generating.

### Phase 3: Generate the prompt

Use the template from [prompt-template.md](prompt-template.md). Fill each section:

| Section            | Source                                                                                               |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| Title              | Research question + topic                                                                            |
| Personal context   | Extracted from prior research, prompts, or conversation ("Who I am" sections); ask user if not found |
| Constraints        | From Phase 2 + any found in existing context                                                         |
| Already researched | Context summary from Phase 1 (omit section entirely if no prior context)                             |
| Instructions       | Standard set (see template)                                                                          |
| Research focus     | Refined question from Phase 2, broken into numbered sub-questions                                    |
| Anti-patterns      | From Phase 2 + standard set                                                                          |
| Output format      | Matched to output type from Phase 2                                                                  |

## Rules

- **Never fabricate context** -- only summarise what actually exists
- **Preserve the user's voice** -- if existing context uses first person, maintain that style
- When a "Who I am" section exists in prior context, reuse it unless the user says otherwise
- If there is no existing research, omit the "What has already been researched" section entirely and generate a
  first-exploration prompt instead
