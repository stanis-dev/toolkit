# Simulation Guidelines

Favour TDD approach — implement simulation first, validate with user before proceeding with a solution.

## User Instructions

### System Prompt Context

Sierra wraps your `instructions` in a system prompt. Your instructions are injected into the `# SCENARIO` section.
Everything else is Sierra-controlled — do not duplicate or contradict it.

```
# INSTRUCTIONS
* You are a customer interacting with a customer service agent for {company}.
* You are given a SCENARIO that describes your reason for contacting customer service.
* The SCENARIO may also include pertinent account information or personality traits.
* You are also given the full transcript of the conversation so far.
* Your goal is to generate the next message in the conversation, aligned with the SCENARIO.

## RULES
* You are interacting with the customer service agent via *voice call*, so you can only communicate via transcribed messages.
* Just generate one message at a time to simulate the user's next message in the conversation.
* Follow the agent's instructions and don't volunteer information unless specifically asked.
* Do not hallucinate any information that is not provided in the SCENARIO. For example, if the agent asks for the order ID but it is not mentioned in the SCENARIO, do not make up an order ID, just say you do not remember or have it.
* Do not repeat the exact SCENARIO in the conversation. Instead, use your own words to convey the same information.
* If the SCENARIO's reason for contacting customer service is satisfied, indicate that the conversation is over by adding ###STOP### to your last message.
* Do not repeatedly thank the agent; end the conversation by responding with ###STOP### by itself as your response.
* If the agent repeats themself, if you have to repeat yourself, or if there is no progress towards a resolution, get frustrated and asked to be transferred.
* If you are not transferred and the conversation is stuck, end the conversation with a final message, adding ###STOP### to indicate that the conversation is over.

# SCENARIO
You are given the following scenario.

<--- YOUR INSTRUCTIONS INJECTED HERE --->

## WRITING STYLE
* Do not misspell words since they're used as transcribed text.
* When possible, you use short phrases instead of full sentences, e.g. "unsubscribe me" instead of "Can you unsubscribe me from your newsletter?".
* Your first message focuses mainly on the action, and not on the additional information needed. e.g. "downgrade subscription" instead of "I want to downgrade my subscription to the basic plan."

## LANGUAGE REQUIREMENT
You MUST respond in the assistant's preferred language, which is identified by the IETF language tag "{locale}".

## RESPONSE FORMAT
* Respond with only the message text.
* DO NOT include any additional formatting or explanations.
```

### Writing Principles

The system prompt already handles terseness, voice modality, language, response format, brevity, and ###STOP### logic.
Do not restate any of these in your instructions.

What the system prompt does NOT handle well in practice:

- Despite "don't volunteer information unless specifically asked," the user LLM still tends to front-load information.
  For guided conversation flow, use explicit sequencing: "do NOT mention X until Y," "wait for agent to ask before
  providing Z"
- The WRITING STYLE section pushes for brevity in first messages but doesn't prevent information dumping in later turns
- Instructions must target specific journey intents to avoid hallucinations

### Structured Format

Use bold labels to structure instructions. This separates concerns and makes the scenario easier to validate.

Use bold labels (not markdown headings) to avoid hierarchy conflicts with Sierra's surrounding `##` sections.

```
**Identity**: You are [name], a [persona context].

**Objective**: You are calling to [goal].

**Knowledge**:
- You know: [facts the user has]
- You do NOT know: [facts the user lacks]
- You believe: [possibly incorrect beliefs]

**Behavior**:
- [scenario-specific behavioral constraints]

**Conditionals**:
- If [agent action] → [user response]

**Resolution**: The conversation is resolved when [explicit criteria].
```

**Section rationale:**

- **Identity** — persona anchor; maps to the system prompt's "personality traits" expectation
- **Objective** — singular and clear; maps to "reason for contacting customer service"
- **Knowledge** — separates known facts, unknown facts, and incorrect beliefs; helps the system-level no-hallucination
  rule work better since the user LLM can distinguish "I know this" from "I don't have this"
- **Behavior** — scenario-specific sequencing that complements (not duplicates) system-level terseness rules
- **Conditionals** — reactive if/then behavior; the system prompt has no branching concept beyond "get frustrated if
  stuck"
- **Resolution** — makes "satisfied" explicit for the ###STOP### mechanism so the user LLM doesn't prematurely end or
  drag on

### Example

```
**Identity**: You are Bilge Göçen, a business customer with an overdue balance. You are
cooperative but firm about not paying by card today.

**Objective**: You are calling to arrange a payment promise for your outstanding debt.

**Knowledge**:
- Your name is Bilge Göçen
- You have an outstanding balance (you do NOT know the exact amount)
- You do NOT know which cards are on file
- You believe you can pay by bank transfer on Friday

**Behavior**:
- When asked your name, say 'Bilge Göçen'
- When offered card payment, decline without elaborating
- Do NOT mention Friday or bank transfer until you've declined the card option
- If agent asks about your address for verification, confirm it

**Conditionals**:
- If agent asks when you can pay → say Friday
- If agent asks how you will pay → say bank transfer
- If agent reads out bank/IBAN details → say you've noted them down
- If agent asks for confirmation of the promise → confirm

**Resolution**: The conversation is resolved when a payment promise for Friday is recorded
and you have confirmed it.
```

## Configuration

- **Device**: Agent is phone-based — all sims must have device configured accordingly
- **Locale**: Always set simulations to the project's configured locale
- **Naming**: Group and name simulations according to expected customer-facing behavior — never use ticket IDs or
  development-focused references
- **Granularity**: Reuse groups when possible. Avoid creating granular simulations — if behavior is already part of a
  tested scenario, adjust the evaluation rather than creating a new sim

## Validity

A simulation's tag assertions and outcome evaluations are meaningless unless the conversation actually reproduces the
scenario being tested. **Before considering any evaluation results, verify the conversation itself is valid.**

This checklist is mandatory after every sim create or update. A sim that passes all assertions but fails validity is not
a passing sim — it's a false positive. Do not consider a simulation ready until validity passes.

### Scenario Fidelity

Verify the user LLM followed the intended instructions:

- [ ] **Information sequencing**: If instructions specify "don't mention X until Y," confirm X was not revealed early
- [ ] **Conditional triggers fired correctly**: If instructions say "if agent offers X, decline" — verify the user
      actually declined (not agreed, ignored, or sidestepped)
- [ ] **Knowledge boundaries respected**: User did not provide information they weren't supposed to know
- [ ] **No hallucinated details**: User did not invent order numbers, dates, amounts, or other specifics not in the
      instructions

### Path Coverage

Verify the conversation traversed the path the sim was designed to test:

- [ ] **Critical interaction points occurred**: The specific decision moments that matter for evaluation were reached
- [ ] **Agent did not skip steps**: The agent went through the intended sequence, not a shortcut that happened to
      produce the right tags
- [ ] **The scenario's core tension was exercised**: The thing that makes this test meaningful actually happened in the
      conversation

### Conversation Health

- [ ] **No repeated requests**: Agent did not ask for the same information multiple times
- [ ] **No stuck loops**: Conversation progressed naturally without circular exchanges
- [ ] **Reasonable turn count**: Not suspiciously short (steps skipped) or long (stuck/confused)
- [ ] **User and agent stayed on topic**: Conversation didn't drift to unrelated subjects
- [ ] **No unexpected identity prompts**: If not evaluating identity verification, user was not asked for phone number
- [ ] **No phone in user message**: User phone number did not appear in the user LLM's messages unless specifically
      testing unidentified user behavior

### When Validity Fails

Do not trust the evaluation results. Instead:

1. Identify which check failed and why
2. Adjust the user instructions to fix the scenario fidelity issue, OR identify a journey/tool bug if the agent caused
   the path deviation
3. Re-run and re-validate

Iterate until validity passes before evaluating outcomes.

When user requests a **sim review**, run the validity checklist against the latest replay transcript for each specified
simulation (or all sims if none specified). Report findings per sim.

## Evaluation

After validity is confirmed:

- Favor **tag evaluation** over judge LLM evaluation when possible — judge LLM is prone to hallucinations
- Ensure mock user is properly configured and appropriate for the scenario being evaluated
- Verify failures are for expected reasons by reading the full replay

Flag patterns for journey/tool improvements.
