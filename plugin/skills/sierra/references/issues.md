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

## Report

Report back per the Issue Analysis variation in [info.md](./info.md) and nothing else. I will
request details if I need to. What goes in each part:

- Header: the issue number, its type from the list above, its title, the reporter's name, how
  many calls are linked and the call date.
- Reporter's words: what they wrote, paraphrased short. If their words don't translate well to
  agent implementation - then under it write what that means in agent terms, one short paragraph.
- Closes it: 3-10 word tldr on agent change that'd close the issue.
- Conversation: only the turns that matter, with neighbours that give them sense. Mark 3 spans:
  1. the turn the reporter is pointing at.
  2. then two rows: what agent produced vs what it should have according to reported
- Observations: omitted by default. Only for insight that would make the report dangerously
  incomplete.