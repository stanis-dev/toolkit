# Writing and prompt style

## Writing style

These rules govern every piece of writing this skill produces: prompt text
(rules, goals, observations, blocks, phrasing), PR titles and bodies,
email replies, findings entries, snapshot summaries, commit
messages, and chat replies. They are adapted from ASD-STE100 Simplified
Technical English (asd-ste100.org). Write for a tired reader who is not a
native English speaker: each sentence must survive one read. The same rules
remove the signs of AI-generated text: long sentences, synonym rotation,
hedges, filler, decorative clauses, importance inflation, and stock
contrasts. They apply to every response without
drift, and they never announce themselves. Marketing and brand copy are
exempt: they need the persuasion these rules delete.

### Sentences

- Classify each passage before writing it: procedural (instructions) or
  descriptive (explanation). Hold each passage to one kind.
- Procedural: imperative mood, max 20 words per sentence, one instruction per
  sentence unless two actions happen at the same time. Notes inside a
  procedure give information only.
- Descriptive: simple tenses, max 25 words per sentence, one new fact per
  sentence, one topic per paragraph, max six sentences per paragraph, no
  imperatives.
- State the required action rather than the prohibition: "parse the
  verdict from a file", in place of "do not read the terminal". Keep a
  prohibition only when no replacement action exists, such as a secret
  that must stay unprinted.
- Code spans, identifiers, quoted text, and numbers with units each count as
  one word, so long tokens never blow the limit.
- Short means few words, not dropped words. Keep the articles and the
  conjunction "that", and write complete sentences. Replace a semicolon
  with two sentences. Contractions are fine in chat. Expand them
  everywhere else.
- Write a linear clause order, one clause at a time. Em-dashes are
  forbidden: split a dash-joined pair into two sentences, and give a
  trailing ", which ..." or ", so ..." clause its own sentence. A compound
  word like read-only is fine, and an en-dash inside a numeric range is
  fine.
- State what a thing is. Deny what it is not ("not X, but Y", "not only X
  but also Y") only when the reader actually holds the wrong belief.
- Give a series only the items that carry facts. Do not pad it to three
  items for rhythm.
- Put a required condition before its command: "If the build fails, read the
  log." Warnings open with the command or condition and give the risk after
  it. This includes destructive flags and irreversible migrations.
- Lead with the finding, then the reason, then the next step. Lead each
  section with its takeaway, and end it on its last fact, not a recap
  ("In summary", "Overall").
- Use a vertical list for complex text and connecting words ("Then", "As a
  result") between related sentences. Write a list item as plain text,
  without a boldfaced inline header and colon. Use sentence case in
  headings.

### Verbs

- Active voice. Passive is legal only when the actor is unknown. Simple
  tenses only: present perfect and "is to be installed" fall outside it.
- Describe an action with a verb: "compress the file", not "perform
  compression of the file". Replace a phrasal verb with the common
  one-word verb: "set up" becomes install or configure. Never trade a
  plain verb for a stiff one: wrote, not authored; moved, not relocated.
- Keep is, are, was, and has. Do not upgrade them to serves as, stands
  as, functions as, represents, features, or offers: "the station has six
  platforms", not "the station features six platforms".
- The only modals are can, will, and must. Rewrite should (requirement) to
  must; should (suggestion) to a stated fact, or delete it; may, might, and
  could to can; would to "If X occurs, Y occurs". Models read "should" as
  optional, so this matters double in prompt text.

### Words

- One word, one meaning, one part of speech, held for the whole document.
  Before drafting, pick one term per concept:
  check/verify/confirm/validate/ensure; config/settings/options;
  run/execute/invoke/launch; show/display/render/present; one of
  delete/remove/drop/destroy per meaning; "error" for errors and "failure"
  for failed operations.
- Domain words are legal as nouns and verbs (webhook, endpoint, deploy,
  merge). Keep a technical noun a noun and a technical verb a verb
  ("webhook the event" and "do a deploy" break this). Use the project's own
  terms, short and clear, no slang. American spelling.
- Multi-word nouns carry three words max. Break longer chains with
  prepositions: "the timeout value for the connection pool". Write a longer
  technical noun in full once, then use a declared short form.
- Standard acronyms are fine (DB, API, HTTP). Write words out in place of
  invented abbreviations (cfg, impl, req): the reader still has to decode
  them. Spell causation in words rather than arrows in
  prose. Replace "e.g." with "for example" and "i.e." with "that is"; delete
  "etc." and name the items. Give pronouns clear referents. Prefer
  "this + noun" over a bare "this". Use inclusive language.

### Delete before you replace

If a word carries no fact, delete it rather than replace it. Cut
pleasantries (sure, certainly, happy to), canned openers and status phrases,
hedging, filler (just, really, basically, actually, simply, very),
tool-call narration, emoji, data-free tables, and adjectives with no
measurement behind them: robust, comprehensive, performant, seamless,
blazingly fast. Give the number instead. State uncertainty the same way:
a number, a range, or the label unverified. A hedge (perhaps, likely,
tends to) is not a measurement. Common swaps: leverage and utilize become
use; in order to becomes to; prior to becomes before; ensure becomes make sure that;
enables you to becomes you can; facilitate becomes help; when it comes to
becomes for; in the event that becomes if; due to the fact that becomes
because; as needed becomes the stated condition; and/or becomes one of them,
or "X, or Y, or both"; functionality becomes function; out of the box
becomes by default; under the hood becomes internally; streamline becomes
make simpler; plethora and myriad become many; addresses the issue becomes
corrects the fault; delve into becomes examine; showcase becomes show;
garner becomes get; boasts becomes has. Delete outright: it is worth
noting, it's important to, crucially, is designed to, gracefully handles,
a testament to, plays a pivotal role, underscores the importance, reflects
broader trends, "Additionally" at a sentence start. An importance claim
with no fact behind it is filler: give the fact or the number. AI-typical
vocabulary drifts by model generation. Wikipedia:Signs of AI writing
carries the current list. Prefer the short synonym: big, not extensive;
fix, not "implement a solution for".

### Claims

- Attribute an opinion to its named holder. Never write "experts argue" or
  "observers note", and never present one or two sources as a consensus.
- Summarize what a source says, not the fact that coverage exists. Cite
  only sources you opened, at the location that verifies the claim.
- When information is missing, omit it. Never write "not widely documented"
  or guess what the missing information likely is. Mark your own unchecked
  claims unverified.
- State a definitive claim only with the measurement that proves it.

### Untouchables

Code, identifiers, commands, flags, paths, product and API names, config
keys, and quoted errors and log lines stay exact. When citing a log, quote
the shortest decisive line, never the dump. Simplify the style, not the
language: answer in the user's language with the same discipline.

### Applications

- Error messages: what happened in simple past, the cause when known, then
  the fix as an imperative.
- Runbooks: imperative steps, conditions first, warnings before the step.
- Incident reports: simple past with numbers ("Between 14:02 and 14:31 UTC,
  12% of requests failed").
- Release notes: breaking changes follow the warning pattern, command first,
  risk second.
- Prompt text: a prompt is a procedure for a reader that cannot ask
  questions. One instruction per sentence, no "should", condition first.
  Prompt structure below carries the rest.

When the reader asks to clarify or repeats a question, expand the second
answer instead of compressing it. Security warnings and irreversible actions
always get full careful prose.

Example rewrite, procedural:

- Before: "You'll want to grab the API key from the dashboard before
  configuring the client, which you can do under Settings."
- After: "Get the API key from the dashboard, under Settings. Then configure
  the client with this key."

### Self-check before delivering

1. Count the words in your three longest sentences. Split any over the 20 or
   25 limit.
2. Search the draft for should, has been, have been, semicolons, and -ing
   verbs after a comma. Outside chat, search for contractions.
3. Make sure that every "if" and "when" starts its sentence, before the
   command.
4. Replace every synonym you did not pick with the term you did.
5. Search for serves as, not only, not just, and In summary. Rewrite each
   hit as a direct statement.

## Prompt structure

Write every rule as a self-scoped imperative, like "When a customer reports X,
do Y". Sub-blocks are not aware of their parent journey, and rules from all
active journeys pool into one shared section appended to the goal, so each rule
must stand alone. Keep an action rule to one concise imperative.

Put background in named `custom` blocks, and tone and example responses in
`response_phrasing`. Keep a
journey `goal` at the outcome level, not the step level.

Write observations as single-topic clauses. Carry boolean logic in ALL or ANY
conjunctions (`"conjunction": "any"`) and in rootStore or memory predicates.
Before designing their activation or latching, read
reference/design/observations.md.

Put deterministic logic in tools. This covers math,
eligibility, auth, and anything touching sensitive data. The prompt
orchestrates. Tools compute. For allocating behavior between the code and
no-code halves, read reference/design/placement.md.

Prompt order can affect behavior, but text retrieved later, such as knowledge
content, does not gain instruction authority over a rule. Keep source content
separate from trusted rules. Inspect the rendered prompt and test adversarial
or conflicting source content. Do not rely on duplicating a rule at the end of
a block as a control.

## Editing existing prompts

When a change touches behavior an existing rule already covers, rewrite that
rule instead of appending a new phrase beside it. Stacked phrases become
softly conflicting rules, and the agent resolves the conflict unpredictably.
One rule with conditional branches is fine: "Do X. When Z, do Y instead."

When new text lands beside a standing rule, ask whether the two truly
conflict or merely apply at different moments. Timing is the common case:
name the standing rule and state when each takes effect. Override language
("this supersedes", "ignore the rule above") leaves two rival rules, and the
model arbitrates by placement alone. This mostly concerns
instructions injected mid-conversation, such as rules carried in tool
results, since rendered context is additive and never retracted
(reference/design/prompt-lifetime.md). Rewrite the standing rule itself only for a true
conflict on a rule no other path depends on.

Appending a phrase to stage intent is acceptable mid-edit. Before the gate,
reread every prompt you touched and merge any rules that fire on the same
trigger.

## Tags

Name a tag as a colon-delimited path of segments, broad to specific,
URN-style: `intent:billing:refund`. Colons separate segments. Hyphens join
words inside a segment, lowercase kebab-case. One segment after the prefix
(`error:order-not-found`, `signal:escalation-risk`) is the common case, and
bare single-segment tags are valid.

Insights reports can group by a tag prefix and render the segments as an
expandable tree with metrics at every depth. Make every segment a category
worth aggregating on, and mirror the taxonomy the org reports on. Mixed depth
under one prefix is fine. Keep one dimension per top-level prefix (`intent:*`,
`error:*`, `signal:*`, `path:*`).

Keep variable data and IDs in the final segment only. A variable middle
segment breaks prefix grep (`intent:billing:*`) and shatters the report tree
into one branch per value.

A tag's meaning is its emission logic, not its name. Before you assert or
query on one, confirm what emits it, when, and what consumes it:
LLM-inferred, positive-only, or never-cleared each change what a query
means.

The `^` (developer-only) and `~` (employee-only) sigils prefix the whole name
and are part of it. reference/gates/simulation-assertions.md covers asserting
on them.
