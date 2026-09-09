# Release monitoring

Before reading conversation evidence, read [result access](../gates/simulation-results.md). For release identity, target scope, and the authorized release operations, read [lifecycle](lifecycle.md). When handing an unresolved finding to another session, read [handoff](../writing/handoff.md).

Watch a new release until two questions carry evidence: is the agent
broadly healthy on it, and does the changed behavior work on live
traffic? Escalate only on evidence.

Anchor on the release record first (`query_releases`). The new hash is
the join key for every query. The previous hash for the target is both
the baseline and the rollback reference. The build's git commit proves
the release contains your change. Confirm it before you attribute any
behavior.

Conversations pin their release at start, and a cut does not migrate
in-flight ones, so traffic is mixed afterward. Filter by release hash.
Adoption is itself a health signal: no
new-hash conversations within minutes on a busy agent means the
release may not be serving.

A tag or metric is only a regression relative to baseline. Before
escalating any finding, run the same filter against the previous hash
bounded to a comparable window. Alarming-looking tags are often the
normal path for much of traffic, and this false-positive trap is the
most common way monitoring goes wrong. Start from the org's saved
reports for trend signals, containment and transfer rate above all.
Reports are scoped by time and target, not hash, so attribute with
hash-filtered conversation queries. A search count equal to the query
limit is a floor, not a total.

Containment and transfer measure only how conversations end, so watch
the start too. Baseline the rate of no-user-message conversations. A
spike means the greeting or channel wiring drove customers away before
they spoke. Confirm new-hash conversations open with the intended
greeting.

Overall health does not prove the change works. Derive the delta from
the git log between the two builds' commits, collect the touched
surfaces and the tags they emit, and read at least one full transcript
per surface: a conversation can carry the right tags while the agent
says the wrong thing. Low-traffic surfaces can take an hour or more to
be exercised. Report "not yet exercised in production" and hold the
final checkpoint until a real conversation confirms.

Checkpoints beat continuous polling. Space checkpoints by traffic: enough
new-hash conversations per checkpoint to read. The final one lands
once the changed surface is exercised. Thresholds are each rate's
normal band across comparable baseline windows. Report each checkpoint
as deltas only: one figure per signal against baseline. Agree the
escalation channel up front. Escalate when a rate leaves its band, on
adoption collapse, or when the changed surface misbehaves in a
transcript. The escalation carries the release hash and URL, the
evidence against baseline with conversation links, and the previous
hash as the rollback reference. Rolling back is the user's decision.
Anything below that bar is a status update, not an escalation. Both
follow the writing style in [authoring](../writing/authoring.md). After
the final checkpoint confirms the change, report and close out.
