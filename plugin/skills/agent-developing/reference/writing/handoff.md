# Handoff reports

Transfer enough verified context to continue the named task. A handoff does not grant access or authorize additional work. For the wording, read [authoring](authoring.md). When reporting gate status or resuming verification, read [testing](../gates/testing.md) and [correctness review](../gates/verification.md). For a remaining snapshot or release step, read [lifecycle](../shipping/lifecycle.md).

## Data boundary

Check both environments' data permissions before preparing the report. Conversation IDs, issue details, paraphrases, and narrow aggregates can remain traceable customer data. Removing names or quoting nothing does not establish safety.

Keep restricted evidence and its identifiers in the approved environment. Transfer only material explicitly allowed for the destination. If the classification is unresolved, omit the material and state the missing verification capability. A human review is useful but does not override policy.

Do not switch a data-bearing session into a model or provider without permission to process that data. Use a synthetic reproducer only when it carries no customer-derived identifying detail and policy permits it.

## Contents

State the following facts directly. Omit irrelevant sections, but make unknown required facts explicit.

- The requested outcome, scope limits, allowed actions, and completion criterion.
- The repo, branch, exact code revision, no-code version, configuration, and permitted evidence references.
- Verified findings and their source locations. Separate hypotheses, rejected explanations, and missing evidence.
- Decisions already made, and unresolved decisions with their consequences.
- Named checks already run, their result references, and the artifact each result covers.
- Outstanding checks, the supported commands when known, the required capabilities, and the owner of each next action.
- Coordination identifiers only when permitted and needed for the handoff.

Tell the receiver to load `agent-developing`. Give a reviewer a bounded review assignment, not the full build procedure. If the skill or a required capability is missing there, the receiver does the permitted work and reports the blocked portion. Do not guess the missing rules.

## Delivery and resumption

Use a destination-approved message or artifact route. Verify that the receiver can access the referenced files. A local path does not imply a shared filesystem. Do not commit sensitive evidence or temporary reports merely to transport them.

The recipient verifies artifact identity before using prior results. After edits or relevant version drift, rerun the affected checks. A report's statement that a gate passed is not a replacement for its run evidence.

For compaction within a session, retain the same scope, artifact identities, decisions, missing checks, and authorized next action. Reread the references no longer present in context.
