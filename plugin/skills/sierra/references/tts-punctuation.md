# TTS punctuation & typography reference (grounded via ask_sierra_assistant, 2026-06)

How OpenAI tts-1 renders typographic elements in voice agents (German de-DE focus; general behavior
similar). Use when crafting synthesisRewriteRules replacements or verbatim voice copy.

## Pause ladder (short → long)

| Element                    | Spoken?                  | Pause       |
| -------------------------- | ------------------------ | ----------- |
| Joined letters `DE`        | word/acronym             | none        |
| Hyphen `D-E`               | letter names, dash silent| slight      |
| Spaced letters `D E`       | letter names             | ~150–300ms  |
| Comma                      | silent                   | ~200–400ms  |
| Colon                      | silent                   | ~200–400ms  |
| Semicolon                  | silent                   | ~300–500ms (varies) |
| En/em dash ` – `           | never spoken             | ~300–500ms  |
| Period / newline           | silent                   | ~500–800ms  |
| Ellipsis `...`             | silent                   | ~700–1200ms, trailing intonation |

## Spoken-aloud behavior

- `&` → "und" / "and"; `%` → "Prozent" / "percent" — reliable.
- `24/7` → "vierundzwanzig sieben"; slash silent (except explicit spelling contexts → "Schrägstrich").
- Quotation marks, parentheses: silent; slight intonation shift / pause around the content.
- Periods in abbreviations don't pause: "z.B." → "zett beh", "Dr." → "Doktor".
- Decimal "3.5" → "drei Komma fünf" / "three point five"; period silent.
- `?` rising intonation, `!` emphasis — no extra pause.
- `D.E.` (letters with periods): letters with short pauses; "Punkt"/"dot" sometimes spoken — avoid.

## Stability

- **Stable across providers/updates**: comma, period, newline, `?`/`!`, `&`, `%`, spaced letters,
  joined acronyms, abbreviations, decimal numbers.
- **Variable**: hyphen (tts-1: silent pause; ElevenLabs may speak "Bindestrich" in German), ellipsis
  pause length, semicolon pause length, slash in spelling contexts.
- Letter-spelling escalation path if a rendering sounds wrong by ear: hyphen `D-E` (quick cadence on
  tts-1) → spaced `D E` (stable but longer pauses) → phonetic spelling ("deh eh", least standard).
- Provider switch (e.g. to ElevenLabs) invalidates hyphen-based spellings — re-verify by ear.
