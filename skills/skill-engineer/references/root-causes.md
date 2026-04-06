# Root Cause → Fix Reference

When proposing improvements in any mode, use this as a starting point — the right fix depends
on understanding WHY the failure happened:

| Root cause | Typical fix |
| --- | --- |
| Agent skips a step because it seems optional | Add explicit gate: "Do NOT proceed until X is done" |
| Agent uses wrong tool for a task | Add "ALWAYS use X for this. NEVER use Y — it lacks Z." |
| Agent acts without gathering required info | Add "STOP and ask the user before proceeding" at that step |
| Agent produces output in wrong format | Move the template closer to where the agent generates output |
| Agent claims completion prematurely | Add a verification checklist as the final step |
| User has to repeat themselves | The skill is ambiguous about that topic — add explicit guidance |
| Agent retries the same failing approach | Add "If X fails, try Y instead. Do not retry more than once." |
| Agent follows steps but misunderstands intent | Rewrite the step with a concrete example of correct execution |
| Skill instruction contradicts another | Resolve the conflict with explicit priority ordering |
