# Role bars for the Wizeline→Sierra track

Explicit hiring bars surface in `#sierra-validations` (Slack channel ID `C096PSTHJTH` in `brain/data/slack/wizeline/readable/slack_C096PSTHJTH.md`) and in post-interview debriefs (`brain/data/rec-*-Client-Validation.summary.md`). They drift — refresh before each interview.

## How to extract

**Every bar in the script must trace to a dated message or debrief.** If you can't cite the source, don't write the bar.

1. Open `brain/data/slack/wizeline/readable/slack_C096PSTHJTH.md`. Scan messages from the last 2–4 weeks for guidance from Benja Gil Mendoza, Santi Morillo Segovia, Jorge Muñiz Moran, or other Sierra-side reviewers. They post instructions like "for this role we need X" — these become bars.
2. Open the most recent 1–3 `brain/data/rec-*-Client-Validation.summary.md` files. Post-debriefs reveal failure modes the team has seen — turn those into watch-cues.
3. Cross-check against `journal/candidate-eval.md` — the rubric's "MUST HAVE" items are permanent bars and do not need to be re-sourced per interview.

## Permanent bars (from `journal/candidate-eval.md`)

These are rubric-level and rarely shift:

- **Agent Architecture** — MUST HAVE. Prompt engineering fundamentals, agent components (persona, rules, context, task), LLM mechanics, tool-vs-reasoning decisions, RAG, LLM-as-judge, agent pitfalls (context rot, user mirroring, sycophancy), latency awareness, guardrails. Production experience preferred, theoretical knowledge acceptable if strong.
- **Communication** — customer-facing, handles ambiguous requirements, priority clarification over premature execution, can narrate technical thinking real-time.
- **Ownership & Initiative** — assumed, not negotiated. Hand-holding is not tolerated.
- **Speed** — evaluated indirectly via the other dimensions.
- **React & TypeScript** — the *least* important technical dimension (Sierra moving toward Studio-driven / self-service). Gap-probe it but do not overweight in scoring.

## Seed dated bars (current as of 2026-04-22)

Refresh these by re-scanning the channel before each new interview. Format: `YYYY-MM-DD · who · bar · where to find it`.

- **2025-07-30 · Santi Morillo Segovia · AI copilot fluency in agent mode is required, not just autocomplete.** "MUY importante que estén muy cómodos con el copiloto (cursor, copilot, roo, claude code). No solo autocomplete, copilotos en modo agente. Incluso creo que debería hacer parte del prescreening el heavy use the AI para desarrollo." *(slack_C096PSTHJTH.md, section 2025-07-30.)*
- **2025-08-18 · Benja Gil Mendoza · English must be validated strictly at senior level.** "Para este rol necesito validemos inglés mucho más estricto. Al candidato que entrevisté hoy me pareció demasiado básico su inglés. Especialmente para un rol tan senior." *(slack_C096PSTHJTH.md, section 2025-08-18.)*
- **2026-03-27 · Seb (via Alex Baas debrief) · Engagement matters for client-facing work.** Alex was technically strong but "didn't smile once" during the interview; Seb flagged this as a concern for some clients. Build-first-as-*only*-mode was similarly flagged. *(rec-2026-03-27-143722-Alex-Baas-AI---Client-Validation.summary.md.)*

When a new bar appears in the channel, add a line here with the date and source. When a bar ages out (>6 months without reinforcement and not showing up in debriefs), delete it.
