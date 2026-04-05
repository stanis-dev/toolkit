# Behavioral Signal Taxonomy

Evaluation rubric for ANALYZE mode. Each signal describes what to look for when reading a
conversation transcript alongside the skill that was supposed to guide the agent.

Data source: Cursor agent transcripts (JSONL). Each line is
`{"role":"user|assistant","message":{"content":[...]}}`. Only `type: "text"` blocks are stored.
Tool calls and their results are NOT captured. If the agent says "reading the file" or "I found
X," treat that as evidence the action happened — the tool_use block itself won't appear.

**How to use this rubric:** Don't run through every signal mechanically. Read the conversation
with the skill text in context, then use these categories as lenses to understand what happened.
Report all substantive findings. Highlight the most important one, but do not omit the others.

---

## Category 1: Activation

### 1.1 Correct Activation
- **What to look for**: The user's opening request matches what this skill is designed for, and
  the agent references or follows the skill. This is the baseline — note it and move on.
- **Polarity**: Positive
- **Remediation**: N/A

### 1.2 Missed Activation
- **What to look for**: Read the user's opening request. Does it describe a task this skill is
  designed for? If so, scan the entire conversation — did the agent ever reference, read, or
  follow this skill? If not, the skill's description may not match how users naturally phrase
  this type of request. Compare the user's exact wording to the skill's `description` field.
- **Polarity**: Negative
- **Remediation**: Rewrite description to include the trigger phrases users actually use

### 1.3 False Activation
- **What to look for**: The agent reads or references the skill, but the user's request doesn't
  actually call for it. Signs: the agent starts following the skill's workflow but quickly
  abandons it, or the skill's steps don't map to what the user asked for. Also check: did the
  skill's description overlap with a different, more appropriate skill?
- **Polarity**: Negative
- **Remediation**: Narrow description. Add explicit "Do NOT use when..." guidance.

### 1.4 User-Forced Activation
- **What to look for**: The user explicitly tells the agent to use the skill ("use the /X skill",
  "follow the X skill", "read the skill for Y"). This means the agent should have activated on
  its own but didn't. Compare what the user said before forcing it — that's the natural language
  the skill's description should have matched.
- **Polarity**: Negative
- **Remediation**: Add the user's natural phrasing to the skill description

---

## Category 2: Step Sequence

### 2.1 Ordered Phase Execution
- **What to look for**: Map the agent's actions across the conversation to the skill's step list.
  Did the agent work through them in the prescribed order? Look for explicit phase markers
  (numbered steps, phase names) or implicit ordering (the agent does step 1's work, then step
  2's work, etc.).
- **Polarity**: Positive
- **Remediation**: N/A

### 2.2 Step Skipping
- **What to look for**: Identify each step in the skill. For each, find evidence that the agent
  performed it. If a step's work is absent from the transcript, it was skipped. But check
  whether the skip was justified — did the user's request already provide the information that
  step was supposed to gather? Did the skill itself say "skip if already clear"? The failure is
  when the agent skips a step AND the information wasn't available from context.
- **Polarity**: Negative (unless justified)
- **Remediation**: Make steps less optional, or add explicit skip conditions

### 2.3 Phase Regression
- **What to look for**: The agent returns to earlier phases after advancing past them. This
  looks like asking Phase 1 questions after already producing Phase 3 output. Distinguish from
  legitimate backtracking — did the user reject a direction and ask to start over?
- **Polarity**: Negative (unless user-initiated)
- **Remediation**: Add explicit "if user wants to revisit, do X" guidance

### 2.4 State Tracker Absence
- **What to look for**: If the skill requires a state tracker, progress indicator, or status
  block in every response, check whether the agent actually includes it. This is one of the few
  signals that is straightforward to verify — either the pattern appears or it doesn't.
- **Polarity**: Negative when absent
- **Remediation**: Make tracker template more prominent, move earlier in skill

---

## Category 3: Interaction

### 3.1 Appropriate Clarification
- **What to look for**: The skill says to ask clarifying questions at certain points. Did the
  agent ask questions that match those specified topics? Are the questions genuinely useful for
  narrowing scope, or are they generic ("What would you like me to do?") ?
- **Polarity**: Positive
- **Remediation**: N/A

### 3.2 Missing Clarification (Premature Execution)
- **What to look for**: Find the skill instructions that say to ask before acting. Then read the
  conversation flow — did the agent gather the required information before starting work?
  **Critical nuance:** The agent may have obtained the information implicitly (from attached
  files, earlier context, or the user's detailed request) rather than by asking. That's not a
  failure. The failure is when the agent proceeds without the information AND without it being
  available from context.
- **Polarity**: Negative
- **Remediation**: Add "STOP and ask" markers. Put required inputs in a prominent section.

### 3.3 Over-Questioning
- **What to look for**: The agent asks for information the user already provided. Read the user's
  earlier messages — does any of them contain the answer to what the agent is asking? Also:
  does the agent ask questions the skill doesn't specify, adding unnecessary friction?
- **Polarity**: Negative
- **Remediation**: Add "skip what's already clear from context" guidance

### 3.4 Question Batching Violation
- **What to look for**: If the skill says "one question per turn," check whether the agent asks
  multiple questions in a single message. But use judgment — a message that asks one primary
  question and adds a clarifying follow-up is different from a message that dumps four unrelated
  questions at once.
- **Polarity**: Negative
- **Remediation**: Move the rule to top of interaction rules section, add emphasis

### 3.5 User Correction
- **What to look for**: The user redirects the agent — "no, I meant X", "that's not what I
  asked for", "stop doing Y and do Z instead." This is the most important interaction signal.
  For each correction, determine: is this a skill failure (agent misunderstood the skill's
  instructions), a skill gap (the skill doesn't cover this situation), or a preference change
  (the user changed their mind, not the agent's fault)?
- **Polarity**: Negative (unless it's a preference change)
- **Remediation**: If the correction addresses a skill failure, clarify the ambiguous instruction

### 3.6 User Repetition
- **What to look for**: The user restates something they already said, phrasing it differently
  or with more emphasis. This means the agent didn't act on it the first time. Read both
  instances — is the user asking for the same thing, or has the context shifted?
- **Polarity**: Negative
- **Remediation**: The skill failed to guide the agent on that topic. Add explicit guidance.

---

## Category 4: Tool Usage

### 4.1 Prescribed Tool Usage
- **What to look for**: The skill names specific tools or commands. When the agent describes
  performing those actions, does it use the prescribed approach? Remember: you can't see
  tool_use blocks, only the agent's text describing what it did.
- **Polarity**: Positive
- **Remediation**: N/A

### 4.2 Wrong Tool Substitution
- **What to look for**: The skill says "use X for Y" but the agent describes using Z for Y.
  This is visible in the agent's text — "I'll use sed to edit the file" when the skill says
  to use the dedicated edit tool, for example.
- **Polarity**: Negative
- **Remediation**: Add "ALWAYS use X, NEVER use Y for this step" with reasoning

### 4.3 Tool Absence (Hallucination Risk)
- **What to look for**: The skill requires reading a file or running a command, but the agent
  produces the information without mentioning that it did so. This is a hallucination risk —
  the agent may be generating plausible-sounding content from training data instead of actually
  reading the source. Look for specificity: does the agent cite specific details that could
  only come from the actual file?
- **Polarity**: Negative
- **Remediation**: Add "Do NOT rely on pre-training knowledge. Read the actual file."

### 4.4 Excessive Retries
- **What to look for**: The agent describes retrying the same action multiple times — "trying
  again", "let me retry", or describing the same operation with no meaningful change in
  approach. This indicates the skill doesn't provide error-handling guidance.
- **Polarity**: Negative
- **Remediation**: Add "If X fails, try Y instead. Do not retry more than once."

### 4.5 Inappropriate Delegation
- **What to look for**: The agent delegates to subagents during a workflow that should be
  interactive (breaking the conversation flow), or does everything itself during a workflow
  where delegation would be more effective.
- **Polarity**: Context-dependent
- **Remediation**: Add explicit delegation guidance for each phase

---

## Category 5: Output Compliance

### 5.1 Template Conformance
- **What to look for**: If the skill defines an output template, compare the agent's final
  output against it. Does it have the right sections, headings, and structure? But also check
  substance — a template can be perfectly filled out with shallow or irrelevant content.
- **Polarity**: Positive when structure and content match
- **Remediation**: Move template closer to where agent generates output. Add "MUST use this format."

### 5.2 Template Section Omission
- **What to look for**: Which specific sections of the template are missing? Is there a pattern
  across conversations — does the agent consistently skip the same section? That section may be
  confusing, feel optional, or be positioned where the agent has already moved on mentally.
- **Polarity**: Negative
- **Remediation**: Make the section explicitly required or explicitly optional

### 5.3 Verbosity Mismatch
- **What to look for**: Does the agent's communication style match the skill's guidance? If the
  skill says "be concise" but the agent writes paragraphs, or the skill says "explain reasoning"
  but the agent gives terse answers. Also look for hedging ("I think", "probably", "might")
  and filler ("Let me go ahead and", "I'll now proceed to") that the skill's tone doesn't call
  for.
- **Polarity**: Negative
- **Remediation**: Add concrete word/sentence limits instead of qualitative style guidance

---

## Category 6: Error Recovery

### 6.1 Graceful Error Handling
- **What to look for**: Something goes wrong during execution. The agent diagnoses the problem,
  explains it, and adapts. This is healthy behavior — note it as a strength.
- **Polarity**: Positive
- **Remediation**: N/A, or add the error scenario to the skill as a known issue

### 6.2 Retry Loop
- **What to look for**: The agent describes the same action multiple times without changing
  approach. The text may contain "trying again", "retrying", or describe the same operation
  repeatedly. This usually means the skill doesn't tell the agent what to do when something fails.
- **Polarity**: Negative
- **Remediation**: Add "If X fails, do NOT retry. Try Y instead." Add max retry counts.

### 6.3 Apology-and-Restart
- **What to look for**: The agent apologizes ("I apologize", "Sorry about that", "Let me start
  over") and then repeats work it already did. This is a stronger failure signal than a retry
  loop — it means the agent lost confidence in its approach entirely.
- **Polarity**: Negative
- **Remediation**: Find what caused the loss of confidence. Clarify that instruction.

### 6.4 Silent Abandonment
- **What to look for**: The agent stops following the skill's workflow without acknowledging the
  change. Earlier in the conversation it referenced skill phases; later it just does its own
  thing. This is harder to spot than explicit failure — look for the point where skill-specific
  language stops appearing. Was the skill's workflow actually complete, or did the agent just
  give up on it?
- **Polarity**: Negative (unless the workflow was legitimately finished)
- **Remediation**: Add a "Completion" phase so the agent knows when the workflow is done

### 6.5 Hallucinated Capability
- **What to look for**: The agent claims to have done something it cannot do — "I've updated
  the database", "I sent the notification" — without any evidence the action was taken. The
  agent may be confusing what the skill describes with what it can actually execute.
- **Polarity**: Negative
- **Remediation**: Add scope boundaries: "This skill does NOT enable X."

---

## Category 7: Behavioral Shift

### 7.1 Detectable Style Shift
- **What to look for**: Compare how the agent communicates before and after the skill loads. Does
  the tone, structure, question frequency, or level of detail change in ways that align with the
  skill's guidance? If the skill says "be direct" but the agent stays verbose, the style guidance
  isn't landing.
- **Polarity**: Positive if shift aligns with skill guidance
- **Remediation**: If no shift detected, make style guidance more prominent and specific

### 7.2 No Observable Effect
- **What to look for**: The agent reads the skill but its behavior doesn't change at all. It
  continues doing what it was doing before. This could mean the skill is redundant (the agent
  already behaves this way) or the skill's instructions aren't directive enough to override
  default behavior.
- **Polarity**: Negative
- **Remediation**: Add unique, specific requirements that wouldn't occur without the skill

---

## Category 8: Edge Cases

### 8.1 Graceful Scope Extension
- **What to look for**: The user asks for something the skill doesn't explicitly cover. The
  agent acknowledges the gap and handles it reasonably, either by extending the skill's
  framework or by telling the user it's out of scope. This is good behavior — note what the
  gap was so the skill can be updated.
- **Polarity**: Positive
- **Remediation**: Add guidance for the commonly-encountered gap

### 8.2 Rigid Over-Compliance
- **What to look for**: The agent forces skill phases that don't apply to the situation. It
  fills template sections with "N/A" or placeholder content. It ignores user signals to skip
  ahead ("just do it", "skip that"). The skill is being followed mechanically without
  understanding its purpose.
- **Polarity**: Negative
- **Remediation**: Add "Don't force the funnel" guidance. Add conditions for skipping steps.

---

## Category 9: Conversation Outcome

### 9.1 Single-Pass Completion
- **What to look for**: The task completes without significant corrections or restarts. The user
  got what they needed in roughly the minimum number of turns the skill's workflow requires.
- **Polarity**: Positive
- **Remediation**: N/A

### 9.2 Conversation Abandonment
- **What to look for**: The conversation ends without the skill's workflow completing. No final
  output, no wrap-up. The user may have left out of frustration, or may have gotten what they
  needed early. Look at the last few user messages for tone cues.
- **Polarity**: Negative (usually)
- **Remediation**: Skill may be too long or rigid. Add early-exit paths.

### 9.3 User Satisfaction Proxy
- **What to look for**: Read the user's final messages. Positive signals: "perfect", "thanks",
  "great", "exactly what I needed", or immediately giving the agent a follow-on task.
  Negative signals: "nevermind", "I'll do it myself", "forget it", silence after a long
  exchange. Absence of positive signals in a long conversation is weakly negative.
- **Polarity**: Direct indicator
- **Remediation**: Correlate with specific failure signals to find root cause

---

## Category 10: Anti-Pattern Compliance

### 10.1 Explicit Prohibition Violation
- **What to look for**: Read the skill's explicit prohibitions ("never", "must not", "do NOT").
  Then read the transcript for evidence the agent violated them. This requires understanding
  the prohibition's intent, not just matching keywords. An agent that technically doesn't say
  the forbidden phrase but effectively does the forbidden thing is still violating the spirit.
- **Polarity**: Negative
- **Remediation**: Make the prohibition more prominent. Add an example of the violation.

### 10.2 Anti-Pattern Table Match
- **What to look for**: If the skill has an anti-pattern table (Temptation | Reality), read the
  agent's behavior looking for the described temptations. Did the agent take the shortcut the
  skill warned against? This is particularly relevant for thoroughness-oriented skills where
  the agent is tempted to skim, sample, or extrapolate instead of doing the full work.
- **Polarity**: Negative
- **Remediation**: Strengthen the mitigation. Add a mandatory checkpoint or evidence gate.

---

## Aggregation Guidance

After reviewing individual conversations, synthesize findings into overall patterns. Do not
compute numerical scores from a formula — that creates false precision from small samples.
Instead, answer these questions:

1. **Is the skill activating correctly?** Do users get it when they need it without forcing it?
2. **Are the core steps being followed?** Which ones are consistently skipped or misunderstood?
3. **Does the interaction pattern match the skill's design?** Are questions asked when they should be?
4. **Is the output useful?** Does it match the template in both structure and substance?
5. **How does the agent handle the unexpected?** Graceful adaptation or rigid failure?
6. **What's the overall trajectory?** Getting better, worse, or static?

The most important output of analysis is not a score — it's identifying the 1-3 specific skill
instructions that most need revision, with evidence from conversations showing why.
