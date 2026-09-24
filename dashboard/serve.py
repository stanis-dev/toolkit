#!/usr/bin/env python3
"""Server for the issues pages: http://127.0.0.1:8489/  (no caching, so a plain reload shows current files).
GET serves the directory. POST /golden/<agent>/<n>.json writes that file: refine.html saves Stan's rewrites through it.
POST /drafts/<agent>/<n>.json the same: refine.html drops a dismissed draft cell through it.
POST /sync/<agent> starts the skill's sync.py, which refreshes the agent's issues and calls from the tracker.
POST /batch/<agent>/<n> with {"batch": "MMDD"} or {"batch": ""} sets or removes the card's batch comment.
POST /batchnew/<agent> with {"batch": "MMDD", "base": "<branch>"} and POST /batchbase/<agent>/<MMDD> with {"base": "<branch>"}
start the skill's batch.py create: the batch's own worktree on that existing branch and its own Studio workspace, both
named after the branch; on success agents/<agent>/batches.json holds {"MMDD": {"base", "workspace", "worktree"}}, and a
changed branch drops the old pair. POST /batchdel/<agent>/<MMDD> starts batch.py delete: workspace and worktree gone, the
batch's cards to no batch. Status in agents/<agent>/batches/<MMDD>.status.json. GET /branches lists the repository's local
branches, each with the worktree that has it checked out. Setup forks the issue's worktree from the batch's branch and
refuses without it.
POST /setup/<agent>/<n> starts the skill's setup.py: the issue's own worktree under <repo>/.claude/worktrees/ and its own Studio
workspace, both named <prefix>-<n>; status in agents/<agent>/cards/<n>/setup/status.json. Every step below runs in that worktree and
refuses (409) until it is there.
POST /reset/<agent>/<n> archives every step's answer (analysis, strategy, context, resolve), the strategy's before-the-fix
run files (guard-red, regressions) and the card to the steps'
history/ folders with the sidebar's stage history, drops the step status files and leaves the card with its state comments
only, and records it in the card's history (cardlog.py), which stays; it stops a live resolution session and moves the worktree's uncommitted tracked changes to a git stash, while the
branch and workspace stay. Refused (409) while analysis, strategy, context or a sequence of that issue is running.
POST /kill/<agent>/<n>/<step> sends SIGTERM to the run that status file names; run.py marks it failed («stopped from the page»),
which /steps reports as stopped, as it does a resolution session ended with /stop or whose host is gone.
POST /chain/<agent>/<n> {steps, model, effort} runs several of setup, analysis, strategy, context and resolve for one
issue, one after another in that order, each once the one before is done; the first that fails or is stopped ends it,
and POST /chain/<agent>/<n>/stop ends it after the current step. Both routes and /run take {from}: resolver, engineer or
ruling, whose the feedback is (run.py --from).
The batch driver: POST /driver/<agent>/<batch>/start {model, effort, resume}, send, abort, stop, and GET
/driver/<agent>/<batch>/events and state, as /chat for a resolution session, hosted by session.py --kind driver under
agents/<agent>/driver/; GET /driver/<agent>/<batch>/check is the batch card's data (batch_check).
POST /rule/<agent>/<n> {for: resolver|step, gap} is the engineer's ruling on an open disagreement (review contested):
for the resolver the step reruns with the ruling, for the step the resolution session is told the answer stands;
steps.rule records review ruled and a skill gap in agents/<agent>/skill-gaps.json. The sequence runs in chain.py, a process of its own;
state in agents/<agent>/chain/<n>.json, and in /steps as "chains".
POST /run/<agent>/<n>/<step> (analysis, strategy or context) starts the sierra skill's run.py for that issue and step, detached,
in the issue's worktree; the card's button calls it and then polls agents/<agent>/cards/<n>/<step>/status.json. A runner's own
stdout and stderr land in serve.log next to this file (setup.py's in its run.log, which it fills on purpose).
A step is refused (409, the reason) while another of the three runs for that issue; steps leave git alone, the card's
work stays uncommitted until merge. Both routes take {feedback}: /run with it starts a one-step sequence, /chain gives it
to the first step; when such a sequence ends and the issue's resolution session is live, the session is told which
steps reran, where their new answers are, and to review them again.

The resolution step is interactive: pi in RPC mode, one per issue, hosted by session.py in a process of its own, so
sessions and sequences outlive this server. POST /chat/<agent>/<n>/start {model, effort, ask?, resume?} starts the host
in the checkout with the step's brief (brief.py --step resolve) as the first prompt, the issue's state to talk about
(with ask, the skill text follows the brief in that same prompt: the sidebar's batch run starts the resolution at
once); with resume it starts pi on the last session's file instead. Its events go to
agents/<agent>/resolve/runs/<n>/out.jsonl. POST /chat/<agent>/<n>/ask sends the issue-resolution skill text, the
resolution itself, once; the status file's "asked" says whether it went. The other chat POSTs go to the host over
its socket, runs/<n>/sock.
GET /steps/<agent> is {"sig": <hash of the issue and card files' names, sizes and mtimes>, "steps": {"<n>": {"setup": "done",
"analysis": "working", …}}, "batches": {…}, "cost": {"<n>": {cost, runs, steps}} (the ticket's ledger, agents/<agent>/cost/<n>.json), "resolve": {"<n>": {stage, bar, rates, turn, live}},
"stale": {"<n>": {"<step>": why}} (answers whose input answer is newer)}: the page polls it once
every 2 s and re-renders on a change. "resolve" is the sidebar's row state: the last stage.py entry and the last state per
stage (cards/<n>/resolve/stage.json), the last three pass counts per stage (cards/<n>/resolve/runs.json, which the session's reader
appends when a `sierra … test` command ends), whose turn it is and since when a sim run is in flight. States come from the status files
(a working state whose pid is gone is written back as failed) and from the answers where no status file is left.
GET /request/<agent>/<n>/<conversation>[/<turn>] is the compiled request the agent model saw at that turn of the card's
conversation (the first agent turn without one), from the cached trace: system parts, tools, messages, and the
conversation's agent turns to step through. GET /call/<agent>/<n>/<conversation> is the whole conversation as card.py
reads it (turns, tool calls, cut-off rests, tags) for the page's transcript drawer, so the card and the drawer come from
one parse. GET /sources/<agent> is {n: source} for every issue and every card of another source, as source.py gives them.
GET /files/<agent>/<n> is every file of the card, [{group, path, size, t}] with paths under agents/<agent>/, as
paths.card_files lists them, for the page's files drawer.
GET /chat/<agent>/<n>/events is that log as server-sent events: the log so far, then live; each event's id is its
end offset in the file, so a stream that reconnects (Last-Event-ID) carries on where it broke off.
POST /chat/<agent>/<n>/send {message, mode?} forwards a prompt; while the agent runs it is queued as a steer unless
mode says follow_up; while it is idle, any mode starts a turn. POST /chat/<agent>/<n>/abort interrupts the current turn; /stop ends the process;
/ui {id, ...} answers an extension's confirm/select/input request; GET …/state is {running, streaming, resumable,
status}. Status: agents/<agent>/cards/<n>/resolve/status.json.

The server re-executes itself when one of its own modules changes (serve.py, steps.py, and the scripts it imports),
once the new code imports cleanly and no request is in flight; open event streams reconnect. `serve.py --check`
imports everything and exits."""
import hashlib, json, os, re, shutil, signal, socket, subprocess, sys, threading, time
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())
import steps
from steps import (ORDER, STEPS, SCRIPTS, REPO, alive, now, write_json, load_json, settle, card_batch, batches_path, load_batches,
                   batch_base, repo_of, spawn_proc, start_step, status_path)
sys.path.insert(0, SCRIPTS)
import cardlog, ledger, paths, source

A = '(openpay|cobranzas|hipotecarios)'
GOLDEN = re.compile(r'^/(golden|drafts)/' + A + r'/(\d+)\.json$')
RUN = re.compile(r'^/run/' + A + r'/(\d+)/(analysis|strategy|context)$')
BATCH = re.compile(r'^/batch/' + A + r'/(\d+)$')
KILL = re.compile(r'^/kill/' + A + r'/(\d+)/(analysis|strategy|context|setup)$')
SETUP = re.compile(r'^/setup/' + A + r'/(\d+)$')
RESET = re.compile(r'^/reset/' + A + r'/(\d+)$')
STEPSTATE = re.compile(r'^/steps/' + A + '$')
REQUEST = re.compile(r'^/request/' + A + r'/(\d+)/([\w-]+)(?:/([\w-]+))?$')
CALL = re.compile(r'^/call/' + A + r'/(\d+)/([\w-]+)$')
SOURCES = re.compile(r'^/sources/' + A + r'$')
FILES = re.compile(r'^/files/' + A + r'/(\d+)$')
BATCHBASE = re.compile(r'^/batchbase/' + A + r'/(\d{4}(?:-\d)?)$')
BATCHNEW = re.compile(r'^/batchnew/' + A + '$')
BATCHDEL = re.compile(r'^/batchdel/' + A + r'/(\d{4}(?:-\d)?)$')
SYNC = re.compile(r'^/sync/' + A + '$')
CHAIN = re.compile(r'^/chain/' + A + r'/(\d+)(/stop)?$')
RULE = re.compile(r'^/rule/' + A + r'/(\d+)$')
DRIVER = re.compile(r'^/driver/' + A + r'/(\d{4}(?:-\d)?)/(start|events|send|abort|stop|state|check)$')
CHAT = re.compile(r'^/chat/' + A + r'/(\d+)/(start|ask|events|send|abort|stop|ui|state)$')
BOOT = f'{time.time():.3f}'


def batch_check(agent, batch):
    """The batch card's data: the driver's stage history, each check run file under batches/<batch>/check/ with its
    per-simulation counts, newest last, the batch's cards with their guard counts and reopenings, and the driver's main
    workspace (mainws.py's status)."""
    d = os.path.join(paths.batch_dir(paths.agent('', agent), batch), 'check')
    runs = []
    for f in sorted(os.listdir(d), key=lambda f: os.path.getmtime(os.path.join(d, f))) if os.path.isdir(d) else []:
        j = load_json(os.path.join(d, f), None) if f.endswith('.json') else None
        if isinstance(j, dict) and j.get('tests'):
            runs.append({'file': f, 'run': j.get('simulationRunId'), 't': datetime.fromtimestamp(os.path.getmtime(os.path.join(d, f)), timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                         'sims': [{'name': x.get('name'), 'passed': x.get('passed') or 0, 'total': x.get('total') or 0} for x in j['tests']]})
    cards = []
    for n in paths.cards(paths.agent('', agent)):
        if steps.card_batch(agent, n) != batch:
            continue
        red = paths.guard_red(paths.agent('', agent), n)
        stage = load_json(paths.step_file(paths.agent('', agent), n, 'resolve', 'stage.json'), [])
        cards.append({'n': n, 'stage': stage[-1] if stage else None, 'repro': [red['passed'], red['total']] if red else None,
                      'reopened': load_json(paths.step_file(paths.agent('', agent), n, 'resolve', 'reopen.json'), [])})
    return {'stage': load_json(paths.step_file(paths.agent('', agent), batch, 'driver', 'stage.json'), []), 'runs': runs, 'cards': cards,
            'entry': load_batches(agent).get(batch) or {}, 'main': load_json(paths.step_file(paths.agent('', agent), batch, 'driver', 'main.json'), None)}


def step_states(agent):
    """{n: {step: state}} for setup and the four steps, from status files and answers."""
    out, base = {}, paths.agent('', agent)
    for step in ('setup',) + STEPS:
        for n in paths.numbers(base, step):
            st = settle(paths.status(base, n, step))
            state, err = st.get('state') or '', st.get('error') or ''
            if state == 'failed' and (err.startswith('stopped') or (step == 'resolve' and err == 'process gone')):
                state = 'stopped'
            if state:
                out.setdefault(n, {})[step] = state
        if step != 'setup':
            for n in set(paths.numbers(base, step, 'json')) | set(paths.numbers(base, step, 'md')):
                out.setdefault(n, {}).setdefault(step, 'done')
    return out


def files_sig(agent):
    """One hash over the names, sizes and mtimes of the agent's issue and card files: the page's change signal."""
    h, base = hashlib.md5(), paths.agent('', agent)
    for p in [paths.issue(base, n) for n in paths.issues(base)] + [paths.card(base, n) for n in paths.cards(base)]:
        try:
            st = os.stat(p)
        except OSError:
            continue
        h.update(f'{paths.rel(base, p)}:{st.st_size}:{st.st_mtime_ns}\n'.encode())
    return h.hexdigest()


def batch_states(agent):
    """{MMDD: status} for every batch with a batch.py status file."""
    base = paths.agent('', agent)
    return {b: settle(paths.batch_file(base, b, 'status.json')) for b in paths.batch_ids(base)}


def branches():
    """[{name, at}] for the repository's local branches, newest commit first; at is the worktree that has it checked out."""
    at, path = {}, None
    for line in subprocess.run(['git', '-C', REPO, 'worktree', 'list', '--porcelain'], capture_output=True, text=True).stdout.splitlines():
        if line.startswith('worktree '):
            path = line[9:]
        elif line.startswith('branch refs/heads/'):
            at[line[18:]] = path
    names = subprocess.run(['git', '-C', REPO, 'for-each-ref', '--sort=-committerdate', '--format=%(refname:short)', 'refs/heads/'],
                           capture_output=True, text=True).stdout.split()
    return [{'name': b, 'at': at.get(b)} for b in names]


def live_sessions(agent):
    """{n: status} of the resolution sessions whose host runs."""
    out, base = {}, paths.agent('', agent)
    for n in paths.numbers(base, 'resolve'):
        st = settle(paths.status(base, n, 'resolve'))
        if st.get('state') == 'working':
            out[n] = st
    return out


def resolve_view(agent, live):
    """{n: {stage, bar, turn, live, rates, ended}} for the sidebar: the latest stage.py entry, the latest state per stage,
    whose turn it is while a session runs, when an in-flight sim run started, the last three runs per stage, and when
    each prep step last finished."""
    out, base = {}, paths.agent('', agent)
    for n in set(paths.numbers(base, 'resolve', 'stage.json')) | set(paths.numbers(base, 'resolve', 'runs.json')):
        stages = load_json(paths.step_file(base, n, 'resolve', 'stage.json'), [])
        runs = load_json(paths.step_file(base, n, 'resolve', 'runs.json'), [])
        v = out.setdefault(n, {})
        v['stage'] = stages[-1] if stages else None
        v['bar'] = {e['stage']: e['state'] for e in stages}
        rates = {}
        for r in runs:
            rates.setdefault(r.get('stage') or '', []).append({k: r.get(k) for k in ('passed', 'total', 'green', 'sims')})
        v['rates'] = {k: x[-3:] for k, x in rates.items()}
        v['ended'] = {}
        for step in ('analysis', 'strategy', 'context'):
            st = load_json(paths.status(paths.agent('', agent), n, step), {})
            if st.get('state') == 'done' and st.get('ended'):
                v['ended'][step] = st['ended']
    for n, st in live.items():
        v = out.setdefault(n, {})
        v['turn'] = st.get('turn') or 'you'
        v['live'] = (st.get('simrun') or {}).get('t')
    return out


def cost_states(agent, live):
    """{n: {cost, runs, steps}} per ticket from its ledger, a live resolution session's spend so far included."""
    out = {}
    for n in paths.numbers(paths.agent('', agent), 'cost', 'json'):
        out[n] = ledger.total(ledger.load(os.getcwd(), agent, n))
    for n, st in live.items():
        spent = (st.get('usage') or {}).get('cost') or 0
        if spent:
            t = out.setdefault(n, {'cost': 0, 'runs': 0, 'steps': {}})
            t['cost'] = round(t['cost'] + spent, 6); t['runs'] += 1
            t['steps']['resolve'] = round(t['steps'].get('resolve', 0) + spent, 6)
    return out


def chain_states(agent):
    """{n: chain state} from agents/<agent>/chain/; a working one whose chain.py is gone reads failed."""
    return {n: steps.chain_state(agent, n) for n in paths.numbers(paths.agent('', agent), 'chain', 'json')}


def steps_view(agent):
    live = live_sessions(agent)
    return {'sig': files_sig(agent), 'steps': step_states(agent), 'batches': batch_states(agent), 'resolve': resolve_view(agent, live),
            'chains': chain_states(agent), 'cost': cost_states(agent, live), 'stale': steps.stale_states(agent)}


host_call = steps.host_call


# Self-restart: the modules this server runs, their mtimes at start, and the requests in flight.
GATE = threading.Condition()
INFLIGHT = [0]
CLOSING = [False]
SRV = []


def own_modules():
    roots = (os.getcwd(), os.path.abspath(SCRIPTS))
    files = {os.path.abspath(__file__)}
    for m in list(sys.modules.values()):
        f = getattr(m, '__file__', None)
        if f and f.endswith('.py') and os.path.abspath(f).startswith(roots):
            files.add(os.path.abspath(f))
    return files


def mtimes(files):
    out = {}
    for f in files:
        try:
            out[f] = os.stat(f).st_mtime_ns
        except OSError:
            out[f] = None
    return out


def watch_self():
    """Every second: when a module changed and the new code imports cleanly, stop accepting (new connections wait in
    the listen queue, which the next process inherits), answer what arrives on open connections with Connection:
    close, and once nothing is in flight re-execute in place. Children (runners, hosts, sequences) are not this
    process's to lose."""
    seen = mtimes(own_modules())
    while True:
        time.sleep(1)
        cur = mtimes(own_modules() | set(seen))
        if cur == seen:
            continue
        changed, seen = sorted(os.path.basename(f) for f in cur if cur[f] != seen.get(f)), cur
        check = subprocess.run([sys.executable, os.path.abspath(__file__), '--check'], capture_output=True, text=True, timeout=60)
        if check.returncode != 0:
            sys.stderr.write(now() + ' not restarting, the new code fails: ' + (check.stderr or check.stdout).strip()[-800:] + '\n'); sys.stderr.flush()
            continue
        with GATE:
            CLOSING[0] = True
        SRV[0].shutdown()
        with GATE:
            GATE.wait_for(lambda: INFLIGHT[0] == 0, timeout=120)
            sys.stderr.write(now() + ' restarting: ' + ', '.join(changed) + ' changed\n'); sys.stderr.flush()
            fd = SRV[0].socket.fileno()
            os.set_inheritable(fd, True)
            os.environ['SERVE_FD'] = str(fd)
            os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:])


class H(SimpleHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'  # keep-alive: the page's poll and the card's fetches reuse a few connections
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Server-Boot', BOOT)
        if CLOSING[0]:
            self.send_header('Connection', 'close')
        super().end_headers()
    def log_message(self, fmt, *a):  # serve.log: every POST and every error, never the GET traffic
        if self.command != 'GET' or not fmt.startswith('"'):
            sys.stderr.write(now() + ' ' + (fmt % a) + '\n'); sys.stderr.flush()
    def body(self):
        try:
            return json.loads(self.raw or b'{}')
        except ValueError:
            return None
    def reply(self, code, obj=None):
        data = json.dumps(obj).encode() if obj is not None else b''
        self.send_response(code)
        if obj is not None:
            self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers(); self.wfile.write(data)
    def counted(self, fn):
        with GATE:
            INFLIGHT[0] += 1
        self.counting = True
        try:
            fn()
        finally:
            self.uncount()
    def uncount(self):
        if getattr(self, 'counting', False):
            self.counting = False
            with GATE:
                INFLIGHT[0] -= 1
                GATE.notify_all()
    def do_GET(self):
        self.counted(self.get)
    def do_POST(self):
        self.raw = self.rfile.read(int(self.headers.get('Content-Length') or 0))  # read whatever the route: keep-alive
        self.counted(self.post)
    def get(self):
        path = self.path.split('?')[0]
        ss = STEPSTATE.match(path)
        if ss:
            self.reply(200, steps_view(ss.group(1))); return
        if path == '/branches':
            self.reply(200, branches()); return
        rq = REQUEST.match(path)
        if rq:
            agent, n, conv, turn = rq.groups()
            import brief
            try:
                self.reply(200, brief.compiled_request(os.path.join(os.getcwd(), 'agents', agent), n, conv, turn))
            except Exception as ex:
                self.reply(500, {'error': str(ex)[-400:]})
            return
        so = SOURCES.match(path)
        if so:
            self.reply(200, source.all_sources(paths.agent('', so.group(1)))); return
        fl = FILES.match(path)
        if fl:
            agent, n = fl.groups()
            base = paths.agent('', agent)
            out = []
            for group, p in paths.card_files(base, n):
                try:
                    st = os.stat(p)
                except OSError:
                    continue
                out.append({'group': group, 'path': paths.rel(base, p), 'size': st.st_size,
                            't': datetime.fromtimestamp(st.st_mtime, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')})
            self.reply(200, out); return
        cl = CALL.match(path)
        if cl:
            agent, n, conv = cl.groups()
            import card
            d = source.conv_dir(paths.agent(os.getcwd(), agent), n, conv)
            if not os.path.isdir(d):
                self.reply(404, {'error': 'conversation ' + conv + ' is not in the cache'}); return
            try:
                self.reply(200, card.call_rows(d))
            except Exception as ex:
                self.reply(500, {'error': str(ex)[-400:]})
            return
        c, kind = CHAT.match(path), 'resolve'
        if not c:
            c, kind = DRIVER.match(path), 'driver'
        if not c:
            return super().do_GET()
        agent, n, what = c.groups()
        if what == 'state':  # the status file is the record; a session whose host died reads failed there
            st = settle(status_path(agent, n, kind))
            running = st.get('state') == 'working'
            self.reply(200, {'running': running, 'streaming': running and st.get('turn') == 'agent', 'resumable': steps.resumable(agent, n, kind), 'status': st}); return
        if what == 'check' and kind == 'driver':
            self.reply(200, batch_check(agent, n)); return
        if what != 'events':
            self.send_error(405); return
        self.events(agent, n, kind)
    def events(self, agent, n, kind='resolve'):
        """out.jsonl as server-sent events from the offset the browser last saw, then followed until the session's exit
        event, or until a new session replaces the file."""
        log_path = os.path.join(paths.runs(paths.agent('', agent), n, kind), 'out.jsonl')
        status = status_path(agent, n, kind)
        try:
            pos = int(self.headers.get('Last-Event-ID') or 0)
        except ValueError:
            pos = 0
        self.close_connection = True
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Connection', 'keep-alive')
        self.end_headers()
        self.uncount()  # a stream stays open; it never holds a restart back
        def running():
            return settle(status).get('state') == 'working'
        try:
            f = open(log_path, 'rb') if os.path.exists(log_path) else None
            ino = os.fstat(f.fileno()).st_ino if f else None
            if f and pos > os.fstat(f.fileno()).st_size:
                pos = 0
            if f:
                f.seek(pos)
            buf, ended, ready, quiet = b'', False, False, 0.0
            self.wfile.write(b'retry: 1000\n\n')
            while True:
                chunk = f.read() if f else b''
                if chunk:
                    buf += chunk
                    lines = buf.split(b'\n')
                    buf = lines.pop()
                    out = []
                    for line in lines:
                        pos += len(line) + 1
                        if line.strip():
                            out.append(b'id: ' + str(pos).encode() + b'\ndata: ' + line + b'\n\n')
                            if line.startswith(b'{"type": "exit"'):
                                ended = True
                    self.wfile.write(b''.join(out)); self.wfile.flush(); quiet = 0.0
                    continue
                if not ready:
                    self.wfile.write(b'event: ready\ndata: {}\n\n'); self.wfile.flush(); ready = True
                if ended or not running():
                    if not ended and f:  # the host may have written its last lines while this looked
                        rest = f.read()
                        if rest:
                            buf += rest; continue
                    self.wfile.write(b'event: closed\ndata: {}\n\n'); self.wfile.flush(); return
                if f is None and os.path.exists(log_path) or f is not None and os.path.exists(log_path) and os.stat(log_path).st_ino != ino:
                    if f is not None:
                        self.wfile.write(b'event: closed\ndata: {}\n\n'); self.wfile.flush(); return
                    f = open(log_path, 'rb'); ino = os.fstat(f.fileno()).st_ino; pos = 0
                    continue
                time.sleep(0.2); quiet += 0.2
                if quiet >= 15:
                    self.wfile.write(b': ping\n\n'); self.wfile.flush(); quiet = 0.0
        except (BrokenPipeError, ConnectionResetError):
            pass
    def do_chat(self, agent, n, what, kind='resolve'):
        body = self.body()
        if body is None:
            self.send_error(400, 'body is not JSON'); return
        if what == 'start':
            if kind == 'driver':
                err = steps.start_driver(agent, n, body.get('model'), body.get('effort'), resume=bool(body.get('resume')))
            else:
                err = start_step(agent, n, 'resolve', model=body.get('model'), effort=body.get('effort'), ask=bool(body.get('ask')), resume=bool(body.get('resume')))
            if err:
                self.reply(409, {'error': err}); return
            self.reply(202, {'pid': settle(status_path(agent, n, kind)).get('pid')}); return
        if what in ('check', 'events', 'state'):
            self.send_error(405); return
        if what == 'send':
            if not str(body.get('message') or '').strip():
                self.send_error(400, 'empty message'); return
            if body.get('mode') and body['mode'] not in ('prompt', 'steer', 'follow_up'):
                self.send_error(400, 'bad mode'); return
        if what == 'ui' and not body.get('id'):
            self.send_error(400, 'no id'); return
        if what == 'stop' and settle(status_path(agent, n, kind)).get('state') != 'working':
            self.reply(202, {}); return
        out = host_call(agent, n, dict(body, cmd=what) if what in ('send', 'ui') else {'cmd': what}, kind=kind)
        if 'error' in out:
            self.send_error(409, out['error']); return
        self.reply(202, out)
    def spawn(self, status, log_path, argv, cwd=REPO):
        err = spawn_proc(status, log_path, argv, cwd)[0]
        if err:
            self.send_error(409, err); return
        self.reply(202)
    def batch_run(self, agent, batch, args):
        self.spawn(paths.batch_file(paths.agent('', agent), batch, 'status.json'), os.path.join(paths.batch_runs(paths.agent('', agent), batch), 'run.log'),
                   [os.path.join(SCRIPTS, 'batch.py')] + args + ['--pages', os.getcwd(), '--repo', REPO])
    def post(self):
        c = CHAT.match(self.path)
        if c:
            self.do_chat(*c.groups()); return
        dr = DRIVER.match(self.path)
        if dr:
            self.do_chat(*dr.groups(), kind='driver'); return
        ch = CHAIN.match(self.path)
        if ch:
            agent, n, stop = ch.groups()
            if stop:
                if steps.chain_state(agent, n).get('state') != 'working':
                    self.reply(409, {'error': 'no sequence running'}); return
                open(steps.chain_path(agent, n)[:-5] + '.stop', 'w').close()
                self.reply(202); return
            body = self.body() or {}
            chosen = [x for x in body.get('steps') or [] if x in ORDER]
            if not chosen:
                self.reply(400, {'error': 'no steps'}); return
            st, err = steps.start_chain(agent, n, chosen, body.get('model'), body.get('effort'), feedback=str(body.get('feedback') or '').strip() or None,
                                        source=body.get('from'))
            if err:
                self.reply(409, {'error': err}); return
            self.reply(202, st); return
        ru = RULE.match(self.path)
        if ru:
            body = self.body() or {}
            st, err = steps.rule(*ru.groups(), body.get('for'), bool(body.get('gap')))
            self.reply(409, {'error': err}) if err else self.reply(202, st if isinstance(st, dict) else {}); return
        y = SYNC.match(self.path)
        if y:
            agent = y.group(1)
            self.spawn(os.path.join('agents', agent, 'sync.status.json'), None,
                       [os.path.join(SCRIPTS, 'sync.py'), agent, '--pages', os.getcwd(), '--repo', REPO]); return
        su = SETUP.match(self.path)
        if su:
            err = start_step(*su.groups(), 'setup')
            self.reply(409, {'error': err}) if err else self.reply(202); return
        bb = BATCHBASE.match(self.path) or BATCHNEW.match(self.path)
        if bb:
            body = self.body()
            if body is None:
                self.send_error(400, 'body is not JSON'); return
            agent = bb.group(1)
            batch = bb.group(2) if bb.re is BATCHBASE else str(body.get('batch') or '')
            base = str(body.get('base') or '').strip()
            if not re.fullmatch(r'\d{4}(?:-\d)?', batch):
                self.reply(400, {'error': 'batch is MMDD or MMDD-2'}); return
            if not re.fullmatch(r'[\w][\w./-]*', base):
                self.reply(400, {'error': 'bad branch name'}); return
            if bb.re is BATCHNEW and batch in load_batches(agent):
                self.reply(409, {'error': 'batch ' + batch + ' exists'}); return
            self.batch_run(agent, batch, ['create', agent, batch, '--branch', base]); return
        bd = BATCHDEL.match(self.path)
        if bd:
            agent, batch = bd.groups()
            self.batch_run(agent, batch, ['delete', agent, batch]); return
        bm = BATCH.match(self.path)
        if bm:
            agent, n = bm.groups()
            body = self.body()
            if body is None:
                self.send_error(400, 'body is not JSON'); return
            batch = str(body.get('batch') or '')
            if batch and not re.fullmatch(r'\d{4}(?:-\d)?', batch):
                self.send_error(400, 'batch is MMDD'); return
            path = paths.card(paths.agent('', agent), n)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            text = re.sub(r'\A(\s*<!--\s*batch:[^>]*-->\s*\n?)', '', open(path, encoding='utf-8').read() if os.path.exists(path) else '')
            if batch:
                text = '<!-- batch: ' + batch + ' -->\n' + text
            with open(path + '.tmp', 'w', encoding='utf-8') as f:
                f.write(text)
            os.replace(path + '.tmp', path)
            source.link(paths.agent('', agent), n)
            self.reply(204); return
        rs = RESET.match(self.path)
        if rs:
            agent, n = rs.groups()
            base = paths.agent('', agent)
            for step in STEPS[:-1]:
                st = load_json(paths.status(base, n, step), {})
                if st.get('state') == 'working' and alive(int(st.get('pid') or 0)):
                    self.reply(409, {'error': step + ' is running: stop it first'}); return
            if settle(paths.chain(base, n)).get('state') == 'working':
                self.reply(409, {'error': 'a sequence is running: stop it first'}); return
            host = settle(status_path(agent, n, 'resolve'))
            if host.get('state') == 'working':
                host_call(agent, n, {'cmd': 'stop'})
                t0 = time.time()
                while alive(int(host.get('pid') or 0)) and time.time() - t0 < 10:
                    time.sleep(0.2)
                if alive(int(host.get('pid') or 0)):
                    self.reply(409, {'error': 'the resolution session did not stop'}); return
            stamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')
            archived, kept = [], []
            wt, sg = repo_of(agent, n), steps.stepgit()
            left = sg.dirty(wt) if wt and sg else []
            if left:
                sg.git(wt, 'stash', 'push', '-m', 'reset ' + n + ' ' + stamp, '--', *left)
                archived.append('uncommitted changes to git stash: ' + ', '.join(left))
            card = paths.card(base, n)
            if os.path.exists(card):
                text = open(card, encoding='utf-8').read()
                h = paths.history(base, n, 'analysis', stamp, 'card.html'); os.makedirs(os.path.dirname(h), exist_ok=True)
                shutil.copy(card, h); archived.append('card')
                kept.append(paths.rel(base, h))
                head = re.match(r'(?:\s*<!--.*?-->\n?)*', text, re.S).group(0)
                with open(card + '.tmp', 'w', encoding='utf-8') as f:
                    f.write(head)
                os.replace(card + '.tmp', card)
            for step in STEPS:
                for ext in ('json', 'md'):
                    p = paths.step_file(base, n, step, ext)
                    if os.path.exists(p):
                        when = datetime.fromtimestamp(os.path.getmtime(p), timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')
                        h = paths.history(base, n, step, when, ext); os.makedirs(os.path.dirname(h), exist_ok=True)
                        shutil.move(p, h); archived.append(step)
                        kept.append(paths.rel(base, h))
                p = paths.status(base, n, step)
                if os.path.exists(p):
                    os.remove(p)
            sruns = paths.runs(base, n, 'strategy')
            for f in sorted(os.listdir(sruns)) if os.path.isdir(sruns) else []:
                if re.fullmatch(r'(guard-red|regressions(-added-\d+)?)\.(json|id)', f):
                    h = paths.history(base, n, 'strategy', stamp, f); os.makedirs(os.path.dirname(h), exist_ok=True)
                    shutil.move(os.path.join(sruns, f), h); archived.append('strategy ' + f)
                    kept.append(paths.rel(base, h))
            for ext in ('stage.json', 'runs.json'):
                p = paths.step_file(base, n, 'resolve', ext)
                if os.path.exists(p):
                    h = paths.history(base, n, 'resolve', stamp, ext); os.makedirs(os.path.dirname(h), exist_ok=True)
                    shutil.move(p, h); archived.append('resolve ' + ext.split('.')[0])
                    kept.append(paths.rel(base, h))
            cardlog.add(os.getcwd(), agent, n, 'engineer', 'reset the card: ' + (', '.join(archived) or 'nothing to archive')
                        + '; answers so far are history', kept)
            self.reply(200, {'archived': archived}); return
        k = KILL.match(self.path)
        if k:
            agent, n, step = k.groups()
            st = load_json(paths.status(paths.agent('', agent), n, step), {})
            pid = int(st.get('pid') or 0)
            if st.get('state') != 'working' or not alive(pid):
                self.send_error(409, 'nothing running'); return
            os.kill(pid, signal.SIGTERM)
            self.reply(202); return
        r = RUN.match(self.path)
        if r:
            opts = self.body() or {}
            feedback = str(opts.get('feedback') or '').strip()
            if feedback:  # a one-step sequence, so its end reaches the live resolution session as any rerun's does
                agent, n, step = r.groups()
                st, err = steps.start_chain(agent, n, [step], opts.get('model'), opts.get('effort'), feedback=feedback, source=opts.get('from'))
                self.reply(409, {'error': err}) if err else self.reply(202, st); return
            err = start_step(*r.groups(), model=opts.get('model'), effort=opts.get('effort'))
            self.reply(409, {'error': err}) if err else self.reply(202); return
        m = GOLDEN.match(self.path)
        if not m:
            self.send_error(404); return
        body = self.raw
        try:
            json.loads(body)
        except ValueError:
            self.send_error(400, 'body is not JSON'); return
        path = os.path.join(m.group(1), m.group(2), m.group(3) + '.json')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path + '.tmp', 'wb') as f:
            f.write(body)
        os.replace(path + '.tmp', path)
        self.reply(204)


if __name__ == '__main__':
    if '--check' in sys.argv[1:]:
        import brief, card  # noqa: F401  the lazily imported ones must import too
        sys.exit(0)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8489
    fd = os.environ.pop('SERVE_FD', None)
    if fd:  # re-executed: keep listening on the same socket, so no connection is refused in between
        srv = ThreadingHTTPServer(('127.0.0.1', port), H, bind_and_activate=False)
        srv.socket = socket.socket(fileno=int(fd))
        os.set_inheritable(int(fd), False)
    else:
        srv = ThreadingHTTPServer(('127.0.0.1', port), H)
    SRV.append(srv)
    srv.daemon_threads = True
    threading.Thread(target=watch_self, daemon=True).start()
    sys.stderr.write(now() + f' serving on {port}\n'); sys.stderr.flush()
    srv.serve_forever()
    threading.Event().wait()  # stopped accepting for a restart: the watcher re-executes this process
