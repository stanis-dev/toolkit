# Transcript Polish + Summary

You will be given:
- `INPUT_TRANSCRIPT`: path to a raw Whisper transcription of a meeting
- `POLISHED_OUTPUT`: path to write the corrected transcript
- `SUMMARY_OUTPUT`: path to write the structured summary
- `PROJECT_CONTEXT` (optional): notes about ongoing projects to help infer what topics relate to and which to-dos are relevant

Read `INPUT_TRANSCRIPT` and complete BOTH tasks below.

━━━ TASK 1: Correct the transcript ━━━

Output a corrected version of the ENTIRE transcript. Fix ONLY obvious transcription errors:
- Words that are clearly misheard (wrong homophones, nonsense words, garbled domain terms)
- Repeated gibberish fragments
- Clearly wrong punctuation that changes meaning

For single-word corrections where context strongly indicates the right word
(abbreviations: AA→AI, homophones: takes→tags, near-misses: depth→debt),
go ahead and make the fix. These are low-risk, high-clarity improvements.
Only hesitate on corrections that could change the speaker's intended meaning.

For passages that remain unintelligible even after considering context,
add an [unclear] or [inaudible] marker so readers know the text is unreliable.

Do NOT:
- Rephrase or improve anyone's speech
- Fix grammar (non-native speakers' grammar IS their speech)
- Remove filler words (um, uh, like)
- Add commentary or explanations
- Translate Spanish to English (or any language to any other language) — preserve the source language of every utterance exactly

Keep timestamps and the original structure exactly as-is.
NEVER change speaker labels. Speaker names were assigned by voice matching and must not be altered.
The filename may contain a calendar event name — this does NOT reliably indicate who is in the call.
Participants may have joined after the calendar event ended, or the call may be unrelated to the event.
For long speaker turns, insert paragraph breaks at natural topic shifts to improve readability.
Keep the speaker label and timestamp on the first paragraph only.
Write the corrected transcript to `POLISHED_OUTPUT`.

━━━ TASK 2: Generate a summary ━━━

After correcting the transcript, generate a structured summary for Stan (always a participant).

If the conversation content does not match the calendar event name in the filename,
add a first line: `## Title: <descriptive name for the actual conversation>`
Only add this line when the filename is misleading. Otherwise omit it.

## Summary
A concise 3-7 bullet point summary covering: key topics discussed, decisions made, and open questions.

## To-Dos
Extract actionable to-dos. For each:
- Include the timestamp [MM:SS] where it was discussed
- Brief description of the task
- Who is responsible (bold the name)

Default assumption: if a task was discussed but not explicitly assigned to someone else,
it is Stan's task. Stan works on Sierra agent projects and is responsible for technical
implementation and client-facing coordination.

Format each to-do as: `- [ ] [MM:SS] Description — **Name**`

If `PROJECT_CONTEXT` was provided, use it to make better inferences about what the
discussed topics relate to and which to-dos are relevant.

Write the summary to `SUMMARY_OUTPUT`.
