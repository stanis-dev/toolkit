# Agent Studio Issues

When dealing with an issue, your goal is to understand what needs to be done in order to close the issue.

- Reporters are frequently unfamiliar with even the basics of agent development and are business minded. Their interpretation is frequently unreliable and requires translating to agent development.
- Don't expect the format of the issue to be observed by reporters. It's common for an issue to not have suggested correct behaviour.

## Types of Issues

Issues are not created only for bugs, but for all type of feedback for the agent. These are some that I've been able to identify:

- Bug: agent broke an existing contract.
- Improvement: reporter requests new behaviour agent didn't have.
- Naturalness: agent behaviour was ok, but the phrasing it used was undesirable.
- Update wording: agent behaviour was ok, naturalness ok - the ask is only to subsitute agent phrasing.
- TTS: something did not sound right in voice synthesis.
- STT: bad transcription.

## Report Format

```diff
!   #xxx | bug: agent failed to respond to a question.

# User: How can I see how much I owe on my credit?
- Agent: I do not have information about that.
+ Agent: Sure, you can find out by...
```

