# Feedback on a step's answer

Feedback on your answer is a claim about it, from the resolution agent or the engineer, not an order. The skill you run
and the evidence it names (the issue, the call, the Studio blocks, the runs) decide: the feedback is right where they
back it.

1. Split the feedback into its points, each one thing it says your answer got wrong or should say.
2. Weigh each point against the skill text and the evidence. Accept it when they back it. Dispute it when a passage or
   a turn contradicts it, or when it asks for something the skill does not.
3. Do the step again on the tree as it is: apply every accepted point, leave out what the disputed ones would change,
   and take in anything else the rerun shows. The answer is always your whole current answer.
4. Fill `feedback` as schema.json describes: per point, the claim in one line, your verdict, why, and for a dispute the
   passage or turn that decides it, quoted.

A ruling is not a claim: feedback headed as the engineer's ruling settles its points. Apply it; every point is accepted.
