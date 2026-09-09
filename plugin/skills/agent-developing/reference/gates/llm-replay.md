# Replaying an observed LLM failure

Read when comparing an original LLM call with a changed prompt. [Correctness review](verification.md) owns the evidence standard; this page restores the replay route only.

The tool is `replay_llm_call`. It is not in every Sierra MCP subset, so check the loaded tool list before planning around it. When it is available, replay the original call under the changed prompt and compare the output against the observed failure, keeping the original model, inputs, and settings where the tool supports it. Older guidance asked for temperature 0 to reduce sampling variation. Confirm the model and the tool accept it, and do not read determinism into a zero temperature.

Obtain the original call through a permitted evidence route. For a simulation call, [result access](simulation-results.md) gives the `testResultId` and `testId` relationship. Record the changed settings and the remaining differences. A successful replay is one bounded observation. It does not replace the simulations or the correctness review.
