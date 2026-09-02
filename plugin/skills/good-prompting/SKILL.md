---
name: good-prompting
description: Guidance for writing and refining agent prompts. Critical to use any time you're modifying agent instructions.
---
# Good prompting

With agent prompts, your goal is to create a consistent and resilient behaviour pattern.

## Guidance

- Always think of the full context in mind because because modifications will interact with every part of the prompt. Modifications will have ripple effects throughout the prompt and may give more force to other sections of the prompt or  deprecate  context. Good prompting empowers words, produces maximum steering through minimum context.
- Good prompt defines the task and subtasks clearly: what, how and definition of done. A task needs no further explanation if it is well defined.
- Prompt phrasing will bias the agent towards those words and structures. Always make sure that you're biasing the agent correctly towards the register, vocabulary, and any other context requirements.
- Any time you add any content:
  - verify whether the new steering can be done through a better adjective, adverb or paraphrasing.
  - check whether what you want to add is a known information to the model.
- Phrasing must use instruction style phrasing, i.e. "Do X", "If Y, do Z" with sub bullet points for structure, ideally each mapped to the potential agent turns. 
- Your training strongly biases you towards "teasing" content farm writing style. You must prune it from all your written prompt text.
- When diagnosing model behaviour:
  - check if existing context over/under-loads something in task definition.
- Iterate on phrasing multiple times. Try different alternative phrasing options, verify through simulations.
- Prune ambiguity and contradictions ruthlessly.
- Agent's phrasing is best addressed through a clear definition of the communication context and its role in it. "Say
this, not that" is almost always a symptom of poor definition of that.
- Agent must have a clear and centralised definition of what its register must be. 
  - Smell: separate items instructing agent how to say the content.
- Negative instructions are usually bad smell. Can be caused by conflicting instructions, over/under-specification.
- Agent works with turns as its scope. Instruction must be clear about any turn-specific logic.
- (GPT5.4 specific) - model is known to be very aggressive calling tools. Two mechanisms help remediate it 
  - place tool inside a condition so that it's only revealed when needed. Good for session variable dependant tools or those that have clear context pre-requisites.
  - add a param to the actual tool for agent to evaluate that conditions for calling the tool are indeed, correct. Description should avoid explicitly stating it evaluates agent correctness in calling the tool.



## General Structure

Agent must always be provided with clear context for the situation: it must know what's going on, what's its role in it, what is the personality it has to adopt, what it's communication context is and clear set of goals it needs to achieve. If any of this is missing, underside behaviour will spawn from ambiguity and contradiction.

You know it's good when you could teleport an adult human into a room by surprise, hand them the instructions and they'd know what to do. That weren't born yesterday: they know stuff and don't have to be explained things like a "pen" is. If you do, they will interpret that it must be a critical point and that they should ignore what they already know and take your definition to the extreme - with all its over and under specifications, which will just create confusion. Similarly to the example of a human being teleported by complete surprise, every agent’s turn begins in that exact way. They are teleported into that context with only the history of what we showed them. Whenever we’re trying to understand a specific turn, we should always look at it from that perspective.  

Coherence is critical, because it needs to be understood within the complete prompt that ends up being rendered. The context we place in the builder or code, will be reordered. If we batch certain blocks in a conditional block, for example, it does not mean those pieces will be rendered together. You need to understand exactly where each of those pieces will show up. e.g, rules will get appended to the one single big list, same thing applies to policies. And the agent will not be aware of that intrinsic message we would infer by looking at the grouping. Always make sure you understand—and search the docs if you need to—how a given piece of context is rendered once it is rendered and evaluated. The coherency and consistency of the story depend on that specific item being in the place where you know it will appear. You can always verify by looking at the traces of any sim.

## Bad Smells

- Negative instructions.
- Instruction with a set of example cases - it can bias agent towards them. It's often a signal that better definition is needed.
- Empty instructions. Bits that have no actual meaning.



## Conditional blocks

That analogy of somebody appearing out of nowhere without any preparation somewhere else and needing to do stuff - applies here heavily. Conditional blocks embed everything within them once the conditions are met, and they do so permanently. When we look at the transcript and the logs, we see that a certain condition triggered, and we understand that something happened. The agent will not have that, it will only have new context appear, and because of the way it is done, the agent will believe that the context has always been there throughout the entire conversation. That is important to understand for the coherency and cohesiveness of the story when a certain condition block is revealed.

Context that lives within a condition must always be scoped to that situation. If at any point you attempt to add a comment that alludes to something already inside a conditional, there are two things that can be happening:

1. Agent should know that before the conditions are met - it may be a good idea to pull that information from within the conditional block into a higher scope.
2. You may be overspecifying - agent may be okay without this information. Once the block is revealed, the agent will know that and does not need this hint.

Conditional blocks work is a way that can be easy to mis interpret.

- The mechanism that triggers the actual condition and decides that an observation matches the situation is external to
agent memory. This means that the gated context will appear as is and that context must account for that.
- The observation conditions are inferred with an llm call that gets only the glossary and the transcript. That system
will not have access to journey context, make sure condition wording accounts for that.
- Observation conditions are meant for observations about the conversation, do not confuse them with agent decisions.
- Once context is revealed, it will remain for the rest of the conversation. Plan for how it will interact with
everything else.



## Rules

Rules are meant to correct unwanted agent behaviour that survives even the good scenario and persona definition.

- Before considering using a rule, see that agent's situational context provides the necessary information for agent to properly understand what is happening and what is expected if him. If the context is missing or ambiguous, do not use the rule - fix the context instead.
- Negative rules are especially suspect and very frequently wrong - use them only when the context clearly indicates they should be applied.
- A rule connects to a step only when both use the same words for the action. A rule about "giving the channels" does not apply to a step that says "give the phone line". To the model those are two different actions



## Failure modes

- Include information model already has - either from its training or other parts of agent context.
- Attempt to fix undesirable behaviour by adding "don't"s instead of refining task definition.
- Adding to the task definition instructions specific to a specific behaviour failure mode, instead of refining task
definition.
- Providing agent example words for non-english languages.
- Using emphasis in phrasing, words in caps. Never use without observing behaviour fail without it. If behaviour does
fail without those, find which part of agent context is fighting it. Make them work together
- Tangentially related parts of context silently fighting each other.



## Cookbook

- Agent will ask questions with and without offering options which can create prompt leaks.  Potential solution:
  - Declare Phrasing Instruction of type: "When instructed to ask a question, offer response options only when the instruction clearly asks/permits to do so and provides allowed options"
  - Review all instructions for agent asking questions and make sure those observe the above rule.
- 

 