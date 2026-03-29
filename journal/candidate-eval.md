# Sierra Candidate Eval

**Main takeaway: ** Candidates are evaluated through the same rubric shared with us by Seb, the same One used for Sierra
Employees. New engineers are expected to land confortably at levels 3 and 4 across the board by 5-6 weeks, otherwise it
doesn't "work out". Cadidates are selected by how likely they are perceived to successfully do so

## Speed

Impossible to evaluate in a candidate, so evaluated though the rest of the rubric. It is assumed that a candidate with
great technical competence and communication is most likely to perform best in terms of delivery speed.

Rubrik success criteria:

- Delivery always at least on time, preferably consistently ahead of schedule
- Confortable to adjust to change, preferably actively anticipates downstream work
- Speed under ambiguity, with good quality balance

Seb mentions:

- Engineer is expected to adapt to project pace: prioritise speed when it is required, catch up on quality on a slowdown
- Explained wizeline's candidate was rejected because was perceived to prefer a standard industry flow: "give me a well
  defined ticket and I'll execute it"

Stan's notes: Increases pressure on the rest of skills

## Technical Competence

### 1. React and TS

The least important, especially with Sierra agressively moving toward Studio driven development and self-service

### Agent Architecture

Decent understanding is MUST HAVE.

- Prompt Engineering best practices:
  - Candidate must be able to articulate what is an agent, its challenges and possible solutions (at least
    theoretically)
  - Clear understanding of basic building blocks such as Persona, Rules, Context and Task
- Clear understanding of what a LLM is and how it works
- Familiarity with OpenAI API format
- Tools and Best Practices: when/why use a tool vs llm reasoning, their place in agent/api context
- Good awareness of Agent pitfalls: under/over-specification, context rot, user mirroring, sycofancy
- RAG: what it is, when to use it, pros and cons.
- LLM as a Judge evaluations
- Production Experience is desired, theoretical knowledge must compensate otherwise
- Be very confortable with AI coding agents
- Decent understanding of how the Agent building blocks fit together, not just individually
- Response latency awareness, especially STT/TTS
- Safeguards, Guardrails

Seb examples:

- Red flag: after 4-5 weeks keep finding non-trivial issues in PRs
- Less red but still a flag: PRs are not robust, with frequent details that need to be pointed out
- Good: a neatpick here and there, no feeling person's PRs need babysitting
- Great: engineer proactively delivers more-than-expected robust PRs, will implements updated best practices unprompted

## Communication

- Candidate is expected to work directly with customers, handle ambiguous requirements from customers not intimately
  aware of LLM/Agent capabilities and limitations
- Priority clarification to reduce ambiguity
- Candidate must be capable of clearly explaining technical agent-related aspects to non-technical audience
- Able to handle confusion and miscommunication
- Can present pros and cons of a solution clearly. When uncertain, clearly state so and be capable of narrating their
  thinking real-time in a way that would allow others to follow
- Good: clarity in candidate's communication; Great: improves clarity for everybody in conversation

Seb examples:

- Proactively framing a conversation in a way that allows for audience to follow with ease
- Best engineers are known to post at least weekly updates on agent progress, others can easily follow project progress
  through those
- Comfortable at high-pace, high-value conversations
- English language level can play a role

Stan's notes:

- Strongly related to "Initiative"
- Probably the most brutal part

## Ownership

- Doesn't need to be told that Agent is their responsibility, it is assumed
- Outcomes over implementations (my intepretation: quality of results over tickets/PR throughput)
- Owns those outcomes
- Is intimately familiar with agent and is quickly aware of impact radius of changes or bugs

Stan's notes:

- candidate is likely expected to handle either a simple agent or a significant part of a complex project/account on
  their own in under two months

## Initiative

- Strong independence is expected
- Proactively searches for ways of improving agent quality
- Regularly proposes high-impact improvements
- Balances technical, product and user trade-offs
- Uses good judgement of when to ask vs push an initiative

Stan's notes:

- Hand holding of any kind is not tolerated
- Waiting around to be given something to do is a mortal sin
