---
name: good-prompting
description: Guidance for writing and refining minimal, high-steering agent prompts. Use when modifying agents.
---

# Good prompting

Good prompting empowers words, produces maximum steering through minimum context.

Good prompt will define the task: what, how and definition of done. A task needs no further explanation if it is well
defined.

Example case: I am working on something that is not clearly defined in my head - I may lack expertise in domain, be
unsure as to my goal, want to experiment, etc... So I want a prompt for agent to ask me questions and through those help
me narrow down my ideas. A can have a wall of text to explain which type of questions to ask, what cases I may want to
explore, how to ask those questions, give examples and a lot more. The genius solution would be a one-liner: "Ask me
questions relentlessly until we reach alignment". That phrase alone creates a behaviour that defines everything agent
needs to know.

## Guidance

- Whatever you are modifying, always think of the full context in mind. Understand how other parts of the prompt
  interact with it. Additions will affect and be affected by other sections of the prompt. Modifications will have
  ripple effects throughout the prompt. Deletions may give more force to other sections of the prompt or may deprecate
  existing content.
- Any time you add any content:
    - verify whether the new steering can be done through a better adjective, adverb or paraphrasing.
    - check whether what you want to add is a known information to the model.
- Any time you delete anything, check if some loaded word/phrase can become simpler.
- When diagnosing model behaviour:
    - check if existing context over/underloads something in task definition.
- Iterate on phrasing multiple times. Try different alternative phrasing options, verify through simulations.
- Always think of a given behaviour with agent's full context in mind.
- Prune ambiguity and contradictions ruthlessly.

## Conditional

Conditional blocks work is a way that can be easy to mis interpret.

- The mechanism that triggers the actual condition and decides that an observation matches the situation is external to
  agent memory. This means that the gated context will appear as is and that context must account for that.
- The observation conditions are inferred with an llm call that gets only the glossary and the transcript. That system
  will not have access to journey context, make sure condition wording accounts for that.
- Observation conditions are meant for observations about the conversation, do not confuse them with agent decisions.
- Once context is revealed, it will remain for the rest of the conversation. Plan for how it will interact with
  everything else.

## Failure modes

- Include information model already has - either from its training or other parts of agent context.
- Attempt to fix undesirable behaviour by adding "don't"s instead of refining task definition.
- Adding to the task definition instructions specific to a specific behaviour failure mode, instead of refining task
  definition.
- Providing agent example words for non-english languages.
- Using emphasis in phrasing, words in caps. Never use without observing behaviour fail without it. If behaviour does
  fail without those, find which part of agent context is fighting it. Make them work together
- Tangentially related parts of context silently fighting each other.
