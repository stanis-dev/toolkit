---
name: sierra-triage
description: Retrieve and classify Sierra Agent Studio issues into prioritized buckets. Use when triaging agent issues from Studio.
---

# Agent Issue Triage

Your goal is retrieve issues from Agent Studio and classify them into buckets. Write result in succint and clear format
in `~/code/agent-ctx` folder

## Default Criteria

If different instructions are provided below, those will take precedence. Otherwise follow these rules:

- "Needs Clarification" will go into a separate bucket, those have already been started and are awaiting alignment with
  Pronet
- Issues Related to TTS and STT are out of scope. Only those which can be fixed through synthesys rewrite can be
  considered.
- Understanding issues requires to fetch and read the conversations those are linked to.
- Issues are often filed by people who are not familiar with the development, we must be careful about taking those at
  face value

## Known problems

- Users can file issues from either listening to the recording or looking at the transcript. It is a platform feature
  that PII is redacted from audios and users unfamiliar with platform can think that some behaviour errors occured, such
  as "customer did not provide their full name and agent provided them with private information" because in the
  recording that is what they hear. Or that conversation is incomplete. When such concerns are brought up - verify
  whether debug and transcript data confirms the suspicion. If it doesn't - place those in lowest priority bucket for
  user to still be aware but not introduce noise to genuine issues.
