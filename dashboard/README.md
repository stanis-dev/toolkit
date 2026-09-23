# BBVA issues page

One page listing the open tracker issues of each Sierra voice agent, grouped per batch, with a card per issue that
has been worked on. The card's buttons run the workflow steps (setup, Issue Analysis, Sim Strategy, Studio Context
Edit, the interactive resolution) through the server; the sierra skill's `scripts/` do the work and write the card.

The code lives in the toolkit repo, `dashboard/`; the pages dir, `~/.claude/bbva-issues`, holds symlinks to it next to
the data (agents/, golden/, drafts/, reviews/, serve.log), which stays out of git.

    ~/.claude/bbva-issues/serve.sh              start the server if needed (idempotent; output in serve.log)
    http://127.0.0.1:8489/#a=<agent>&i=<n>      link to one issue

Agents (the `<select>` in index.html): `openpay` = repo `agents/openpay`, MCP `sierra`; `cobranzas` = repo
`agents/base`, MCP `sierra-base`; `hipotecarios` = repo `agents/hipotecarios`.

## Server

`serve.py` serves the files and runs the scripts. `serve.sh` starts it with `nohup`, appending stdout and stderr to
`serve.log`: every non-GET request, every error and whatever a runner prints. Routes:

    GET  /steps/<agent>                 {"sig": hash of the issue and card files, "steps": {<step>: {<n>: status}},
                                        "batches": {<MMDD>: batch.py status}, "resolve": {<n>: {stage, bar, rates,
                                        turn, live}}}: the sidebar rows' state
                                        the page polls it once per 2 s; a moved sig reloads the files, a changed
                                        status updates only the rows, bars and chips that show it
    GET  /call/<agent>/<audit-id>       the linked call as transcript rows for the card's drawer
    GET  /request/<agent>/<audit-id>/…  the compiled request of one turn
    GET  /branches                      local branches, newest first, each with the worktree that has it checked out
    POST /sync /setup /batch /run /kill /reset/<agent>/<n>
    POST /batchnew/<agent>, /batchbase/<agent>/<MMDD>, /batchdel/<agent>/<MMDD>   batch.py create or delete
    POST /chat/<agent>/<n>/(start|ask|send|abort|stop|ui)   the resolution session; start takes {"resume": true}
    GET  /chat/<agent>/<n>/state        {running, streaming, resumable, status}
    GET  /chat/<agent>/<n>/events       out.jsonl as SSE; each id is a byte offset, so a reconnect with
                                        Last-Event-ID resumes where it stopped
    POST /chain/<agent>/<n> {steps}, /chain/<agent>/<n>/stop   a sequence of steps; stop ends it after the current one

A run is refused with 409 while the same step of the same issue is working; the card's chip shows the server's text.
A status file whose pid is gone is written back as failed on read.

Nothing the server starts lives in the server. A resolution session is `session.py`, its own process: it holds pi
over RPC and listens on `resolve/runs/<n>/sock`, one JSON line per command; the server forwards the chat routes to it.
A sequence is `chain.py`, also detached. Steps run as `run.py`/`setup.py` children as before. The shared code (status
files, spawning, ledger totals, sequences) is `steps.py`.

The server restarts itself when serve.py, steps.py or a script it imports changes: it first imports the new code
(`serve.py --check`) and stays as it is when that fails (serve.log says why), then stops accepting, lets the requests
in flight finish and re-executes in place on the same listening socket, so no connection is refused. Sessions and
sequences keep running; open event streams reconnect. Editing serve.py is enough, no restart by hand.

Reruns: the prep steps (analysis, strategy, context) run on the issue's worktree, and strategy and context each leave
one commit there with the trailer `Step: <step> <n>`. Before a prep step runs, `scripts/stepgit.py` moves the issue
branch back to the commit before that step's commit and the later steps' commits, and pushes the tree's Studio content
to the issue workspace when a dropped commit touched `.composer/`. It refuses, and the run answers 409 naming them,
when tracked files are uncommitted (setup's `.composer/pnpm-lock.yaml` and `.composer/.gitignore` aside) or when
another prep step of the issue is running. `/run` and `/chain` take `feedback`: a rerun continues the step's pi
session with it, or runs fresh with it at the end of the prompt; in a sequence only the first step gets it. A `/run`
with feedback runs as a one-step sequence. When a sequence with feedback ends, `chain.py` tells the live resolution
session which steps reran and their new commits. `/steps` carries `stale`: {<n>: {<step>: why}} for answers whose
commit left the branch or that are older than an earlier step's; the card's chips and the sidebar dots mark them. The
resolution panel's «Rerun step» control is prefilled from the latest `review wrong` / `fix misguided` stage entry.

Resume: when a resolution session ended and its pi session file is still there, the card's resolution strip shows a
resume button; pi starts again with `--continue` on that session and the timeline carries on in the same out.jsonl.

## Files

    agents/<agent>/issues/<n>.json    get_issue_details response, default arguments, verbatim.
    agents/<agent>/conversations/<audit-id>/   a linked call: the ghostwriter download (debug.log, summary.json,
                                      traces/) plus details.json, the get_conversation_details response verbatim.
    agents/<agent>/cards/<n>.html     one file per issue, rendered by card.py from the step answers.
    agents/<agent>/<step>/<n>.json    the step's answer: analysis, strategy, context; resolve/<n>.md is the report.
    agents/<agent>/<step>/<n>.status.json   the run's state (working, done, failed), pid, times, cost.
    agents/<agent>/<step>/history/    previous answers and cards, stamped.
    agents/<agent>/<step>/runs/<n>/   system.md, prompt.md, out.jsonl (pi events), err.log; setup keeps run.log.
                                      prep steps also keep session/ (pi's session; older ones session.<stamp>/),
                                      feedback.md (a rerun's feedback) and rewind.log (the workspace push's output).
    agents/<agent>/resolve/runs/<n>/  the session: brief.md, ask.md, system.md, out.jsonl, session/ (pi's session file),
                                      sock (while it runs), host.log, start.err (why the last start failed).
    agents/<agent>/chain/<n>.json     the last sequence: steps, the one at, state, pid; <n>.stop asks it to stop.
    agents/<agent>/setup/<n>.status.json    the issue's worktree and Studio workspace once setup ran.
    agents/<agent>/batches.json       per batch: its branch (base), its Studio workspace and its worktree, both named after
                                      the branch with / as -; batch.py writes it when a create ends.
    agents/<agent>/batches/<MMDD>.status.json, runs/<MMDD>/run.log   the last batch.py create or delete.
    agents/<agent>/resolve/<n>.stage.json   the resolution's stages and verdicts, appended by the skill's stage.py.
    agents/<agent>/resolve/<n>.runs.json    pass counts of every `sierra test` the resolution session ran, with the stage
                                      current then; the server appends it when the command ends.
    agents/<agent>/strategy/runs/<n>/regressions.json   the Sim Strategy's regression list run 5×: the baseline.
    agents/<agent>/sop/sop.md         the agent's SOP when it has one; the analysis brief carries it.
    golden/<agent>/<n>.json           Stan's rewrites of card cells, written by refine.html. Nobody else writes it.
    drafts/<agent>/<n>.json           a session's proposed rewrites, same shape plus `like` (the golden file it mirrors) and `by`.
    exclude.json                      `out`: cards kept out of the refine set for now, as `agent/issue`. Hand-edited.
    index.html, refine.html, card.js, preact-htm.js, page.css, sections.css    the pages. Nothing to build.
    serve.py, steps.py, session.py, chain.py    the server, and the processes it starts.
    test/run.sh                       every check against a copy of a few issues with stand-ins for pi and the scripts.

`card.js` loads an agent's issues and cards, renders one card with the page's chrome and remembers folds; the card's
live parts (top bar, run strips, the Context, Transcript and Session drawers) are Preact components fed by one store
that the page's poll fills. `index.html`'s sidebar is one too. `preact-htm.js` is Preact with htm (htm@3.1.1
preact/standalone), kept as a file. `page.css` is the chrome's styles. Both pages use them.

`sections.css` holds the styles of every section template (`<sierra skill>/references/sections/`),
the rules for combining sections in one card, and the tracker report. Templates are markup only.

## A card

Line 1 names the batch, the `mmdd` of the batch branch; optional `pr` and `ws` lines follow, then section markup, one section
per workflow step, in order. A card may be the comment lines alone.

    <!-- batch: 0917 -->
    <!-- pr: draft https://github.com/<org>/<repo>/pull/NNN -->
    <!-- ws: default -->
    <div class="ia"> … </div>

`pr`: `draft`, `ready` or `merged`, then the link. `ws`: the Studio workspace the edit is on,
`default`, or `released`. The sidebar shows both as icons: grey at half opacity when the line is
absent, grey for a draft PR or another workspace, green for ready or default, purple for merged
or released. An item gets a faint green wash when its card's Sim Strategy carries run counts and
every count is full: the repro passes and no regression stands.

The page owns the chrome and rebuilds it on every render, whatever the card brings: the Issue
Analysis header (number, type kept from the card, title, reporter, call count, first call's date),
one fold per section titled from its class (`ss` Sim Strategy, `so` Simulation Replay, `si`
Simulation Iteration, `oc` Studio Context, or Studio Context Edit when it holds a diff or a state
label), a fold for every `.part` with a heading and every `.sec` block entry. Sections nested inside `.ia` or a
titled `.part` are hoisted to the card's top level in document order.

The page puts a card in again within 2 s of its file changing; no reload needed. A status change never rebuilds it:
open folds, drawers and scroll stay.

## Batches

A batch exists because a card names it or batches.json lists it. Batches sort newest first; issues no card names sit
under "No batch yet". The count on a batch row opens it in review mode, `#a=<agent>&b=<mmdd>`,
one card at a time with Previous and Next above it.

## The issue files

The page lists every `issues/<n>.json` present, whatever its status, so a closed issue disappears
only when its file is deleted. A card whose issue file is missing still shows, titled by its
number. The page reads `issue.{number,name,status,severity,description,createdTime,owner.name,
comments[].{creatorName,body,createdAt}}`.

## Refinement view

`http://127.0.0.1:8489/refine.html`: every card that has an Issue Analysis top part and a tracker issue (a card without
an issue file has no reporter and stays out), both agents in one list ordered by issue number. The editor holds the cell under refinement, Verdict, prefilled with the card's text;
below it the issue as reported, open, and the full card, folded until opened; both folds are remembered per issue.
Keys are modal, as in nvim; the footer names the mode and its keys. Normal: `j` `k` next and previous issue, `h` `l`
move the cursor between the cells, `i` edits the cell, `n` its note, `u` puts the card's text back, `s` cycles the card's state approved → draft → n/a, `↩` accepts what
stands as kept and moves on (with the pointer or focus on the sidebar, `↩` instead focuses the card's first cell), `za` folds the card, `gg` `G` first and last, `t` hides done issues. Insert: typing saves, `↩` breaks the
line, `esc` returns to normal, `⇥` moves to the next field, `⌘↩` accepts and moves on. `⌥↑` `⌥↓` move in either mode.
Opening the page lands on the first pending issue.

Saves go through `POST /golden/<agent>/<n>.json` in serve.py, one file per issue, only once something was said about it:

    {"agent": "cobranzas", "issue": 261, "state": "approved", "fields": {
      "ia/said":   {"card": "…", "golden": "…", "note": "", "status": "rewritten", "at": "…"},
      "ia/closes": {"card": "…", "golden": "…", "note": "", "status": "kept", "at": "…"}}}

`card` is the cell as the card read when the rewrite was made, `golden` what Stan wanted instead, `note` his optional why,
`status` `rewritten` or `kept`; a cell with no entry is pending. `state` is the card's: `approved`, `draft` or `n/a`, set from the
dropdown in the editor header or by `↩`, which approves; typing never changes it. Without one, the cells decide: both
filed reads approved, one reads draft, none reads pending. `n/a` leaves the count and hides with done; `t` hides approved
and n/a. When the live card no longer matches `card`, the editor
shows the text it was written against. Field keys are `<section>/<field>`; adding an entry to `FIELDS` in refine.html
brings a later stage's cell into the same files.

A cell nobody has said anything about yet may show a draft from `drafts/`, dashed and labelled `draft · like <golden>`,
with the card's own text under it. A draft is not Stan's: typing in it never files the other, untouched draft cell,
and only `↩` files what stands. `u` on a draft cell dismisses it, removing the field from the draft file.
