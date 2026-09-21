# Agent Studio Issues

Read the issue that was filed for Sierra Voice Agent and the conversation attached to it, then intepret what the
reporter is asking of me. Your conclusion will be used for designing the fix.

## Deliverable

I know the agent and its context; I read the two lines to decide what the agent must learn, before I open the call. Read
the issue file, every comment (the latest one states the ask) and the linked call, then report per the Issue Analysis
section in [info.md](./info.md) and nothing else.

### 1. Verdict.

One short English sentence with the agent as subject: the one thing a trained representative would have understood here
that the agent did not, a pattern - not just this specific situation. Write it at the altitude of the fix, as an
instruction the agent's context could carry unchanged: name the agent and what it must grasp, with the customer's
circumstances removed. If the line still needs the product, the bank, the amount or the relationship to make sense, go
one level up.

- When the issue is a wrong tag, write «Conversation was misclassified. wanted: `x`, actual: `y`»
- When the cause is transcription or synthesis, write «STT failure» or «TTS failure on <what>».

### 2. Closes It.

«-» by default. When #1 leaves open what the agent does instead, state that move: a sequence as `on "<trigger>":` with
one agent move per line, taken from the SOP row when one covers the case; a judgement as one sentence, what the agent
recognises and what it does. Write the behaviour that replaces the failure.

Done when the two lines name the lesson and the move, and everything that shows them is in the Conversation part.

- Reporters are frequently unfamiliar with even the basics of agent development and are business minded. Their
  interpretation is frequently unreliable and requires translating to agent development.

### 3. Linked Conversation Diagnosis.

First, highlight the turn that reporter selected from the conversation for the issue.

Then, you must find the earliest turn where agent behaviour would have to change in order to achieve the desired change.

- Reporters may have identified a turn that represents only the symptom. You must traverse the conversation backwards
  until you identify the source.
- Highlight the part of that turn which represents the failing behaviour.
- Based on previous hypothesys, reimagine what a "good" turn looks like.
    - consider what a trained human professional would say in given situation. do so with the whole conversation in
      mind.
    - changing agent turn can lead to different customer responses. make sure that the "good" proposition accounts for
      all the effects until the end of the conversation.
    - pay attention not only to "what" agent would say, but also to "how".

## Recipies

- Issue already fixed: stop workflow, gather proof and report to me.
- Transcription: unless mis-transcribed word/expression is very common and critical, stop analysis and just let me know.
- Multi-turn effects: the ask will potentially affect several agent turns or transform one-turn behaviour into
  multi-turn. Let me know asap, multiturn changes are especially complicated.
