# Calibration set

Hand-curated comparison points. Each entry is one candidate the interview process has processed, with the specific trait that makes them a useful reference. Use these as named anchors in the script's post-conversation section — during a new interview, noting "this candidate is doing the Carlos thing" is a compact way to tag a pattern.

Keep entries short. Three sentences each. When a new candidate reveals a reusable pattern, add them. When an entry stops earning its place (no one ever invokes it), delete it.

## Current set

### Alex Baas · 2026-03-27 · 6.5/10 · *technically competent, comms concern*
Led by Seb, Stan shadowing. Strong on RAG architecture and agent design. Failed on comms structure (unengaging delivery, didn't smile) and on treating "build first, clarify later" as his only mode. The reference point for *technical strength that may not survive client exposure*.
Source: `rec-2026-03-27-140153-Alex-Baas-AI---Client-Validation.polished.txt` + `rec-2026-03-27-143722-...summary.md`.

### Carlos Ortiz · 2026-03-27 · *shallow on own work*
Led by Stan. Claimed a RAG plugin project but couldn't recall his own embedding strategy when asked. Gave generic advice ("be realistic, be honest") when pressed for a specific past stressful conversation. Reference point for *CV depth that doesn't hold under the follow-up ladder* — the failure mode to watch for in phase 2.
Source: `rec-2026-03-27-130311-Carlos-Ortiz-...polished.txt`.

### Senthil Nagan Vijay Raja · 2026-04-01 · *strong backend, limited TS/React*
Led by Stan. 14+ years, bioinformatics backend, solid on stakeholder experience and evaluation practices (RAGAS, LLM Guard, dual-LLM verification). Clear TS/React gap. Reference point for *strong fundamentals with a known gap* — the React/TS bar being the lowest-weighted technical dimension matters for this shape.
Source: `rec-2026-04-01-130222-Interview-Slot.summary.md`.

### OpenBank candidate · 2026-04-17 · *honest about learning curve*
Led by Stan. Front-end developer at OpenBank, self-teaching AI since Jan 2026. Built a Playwright + LangChain crawler and a LangGraph email classifier as side projects. Was transparent with Stan and with recruiter Rebecca about being early in AI engineering. Reference point for *low-experience but high-signal enthusiasm* — contrasts with Carlos's overclaim pattern.
Source: `rec-2026-04-17-130203-Interview-Slot.summary.md`.

### Manuel Martinez · 2026-04-22 · *Sierra reject, bench positive · substantive depth, wrong shape for forward-deployed*
Led by Stan. Substantive verification-design work (critic bank with deterministic + semantic verifiers, 10–12 critics at end-of-development, cited theory). Real customer-facing track record at GDS Modellica/Ittera including Santander, 24/7 support, international travel. But: architecture-vs-capabilities confusion under probe (Carlos-adjacent, recovered faster than Carlos did), instinctive resistance to ambiguity ("not the ideal for any professional to work in, in a rush" — recovered after Stan reframed), and admitted at line 102 that Cognipar is home-use-only with no professional AI experience. Reference point for *senior depth that belongs on a different client, not on Sierra forward-deployed.*
Source: `rec-2026-04-22-130053-Interview-Slot.txt`.

## Format for new entries

```
### {Candidate name} · {YYYY-MM-DD} · {Sierra verdict, optionally with bench note} · *{one-phrase trait}*
{2–3 sentences naming what makes this candidate a useful reference.}
Source: {recording filename}.
```

Where a candidate is not a Sierra fit but could still serve Wizeline on another engagement, note both outcomes explicitly (`Sierra reject, bench positive`). The distinction matters: Sierra forward-deployed rewards speed, ambiguity-tolerance, and customer-facing agility, whereas other engagements may reward depth, reliability, or domain fluency — some of the strongest bench candidates are weak Sierra fits.
