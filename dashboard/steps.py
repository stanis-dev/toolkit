"""What the pages server, the session host (session.py) and the sequence runner (chain.py) share: status files, the
issue's worktree and batch, and starting one step of one issue. Paths are relative to the pages dir, the caller's cwd."""
import json, os, re, socket, subprocess, sys, threading, time
from datetime import datetime, timezone

SCRIPTS = os.environ.get('SIERRA_SCRIPTS') or os.path.expanduser('~/code/toolkit/plugin/skills/sierra/scripts')
REPO = os.environ.get('BBVA_REPO') or os.path.expanduser('~/code/BBVA')
HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ('setup', 'analysis', 'strategy', 'context', 'resolve')
STEPS = ORDER[1:]
SIM_RUN = re.compile(r'sierra\S*\s+(?:-C\s+\S+\s+)?test\b')
USAGE = ('in', 'cached', 'out', 'reasoning', 'commands', 'cost')


def now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def alive(pid):
    """Whether the process runs; a child of this process that has ended is reaped here, so it never reads alive."""
    if pid <= 0:
        return False
    try:
        if os.waitpid(pid, os.WNOHANG)[0] == pid:
            return False
    except ChildProcessError:
        pass
    except OSError:
        return False
    try:
        os.kill(pid, 0); return True
    except Exception:
        return False


def write_json(path, obj):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path + '.tmp', 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(path + '.tmp', path)


def load_json(path, default):
    try:
        return json.load(open(path, encoding='utf-8'))
    except Exception:
        return default


def settle(path):
    """The status file's content; a working state whose process is gone is written back as failed, so every reader
    agrees. {} when there is no file."""
    try:
        st = json.load(open(path))
    except Exception:
        return {}
    if st.get('state') == 'working' and not alive(int(st.get('pid') or 0)):
        st.update(state='failed', ended=st.get('ended') or now(), error=st.get('error') or 'process gone')
        write_json(path, st)
    return st


def status_path(agent, n, step):
    return os.path.join('agents', agent, step, n + '.status.json')


def card_batch(agent, n):
    try:
        m = re.match(r'\s*<!--\s*batch:\s*(\d{4}(?:-\d)?)\s*-->', open(os.path.join('agents', agent, 'cards', n + '.html'), encoding='utf-8').read(400))
        return m.group(1) if m else ''
    except OSError:
        return ''


def batches_path(agent):
    return os.path.join('agents', agent, 'batches.json')


def load_batches(agent):
    return load_json(batches_path(agent), {})


def batch_base(agent, batch):
    return (load_batches(agent).get(batch) or {}).get('base') or ''


def repo_of(agent, n):
    """The issue's worktree, once setup.py has finished it; None before that."""
    st = load_json(os.path.join('agents', agent, 'setup', n + '.status.json'), {})
    wt = st.get('worktree')
    if st.get('state') == 'done' and wt and os.path.isdir(wt):
        return wt
    return None


def session_dir(agent, n, kind='resolve'):
    return os.path.join('agents', agent, kind, 'runs', n, 'session')


def batch_worktree(agent, batch):
    """The batch's worktree from batches.json, None when it has none on disk."""
    wt = (load_batches(agent).get(batch) or {}).get('worktree')
    return wt if wt and os.path.isdir(wt) else None


def resumable(agent, n, kind='resolve'):
    """A session (resolution, or with kind driver the batch driver's) that ended without finishing (stopped, crashed,
    host gone) and left pi's session file."""
    st = settle(status_path(agent, n, kind))
    d = session_dir(agent, n, kind)
    return st.get('state') == 'failed' and os.path.isdir(d) and any(f.endswith('.jsonl') for f in os.listdir(d))


RUNNING = {}  # status path -> Popen of the runner this process started, so two starts cannot race on one status file
RUNNING_LOCK = threading.Lock()


def spawn_proc(status, log_path, argv, cwd=None):
    """Start a runner detached, one per status file: the dict catches a second start before the runner has written
    its status, the file catches a runner from before this process started. Output goes to log_path, or to this
    process's own log when None. (None, Popen) when started, else (why not, None)."""
    with RUNNING_LOCK:
        p = RUNNING.get(status)
        if (p is not None and p.poll() is None) or settle(status).get('state') == 'working':
            return 'already running', None
        log = None
        if log_path:
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            log = open(log_path, 'ab')
        p = RUNNING[status] = subprocess.Popen([sys.executable] + argv, stdout=log, stderr=log, stdin=subprocess.DEVNULL,
                                               start_new_session=True, cwd=cwd or REPO)
        if log:
            log.close()
    return None, p


def start_session(agent, n, model, effort, repo, ask=False, resume=False, wait=60, kind='resolve'):
    """Start session.py, the resolution's own host process (with kind driver, the batch driver's, n the batch), and
    wait until it holds the session or gives up: None when it runs, else its reason (the brief failed, nothing to
    resume)."""
    runs = os.path.join('agents', agent, kind, 'runs', n)
    os.makedirs(runs, exist_ok=True)
    err_path = os.path.join(runs, 'start.err')
    if os.path.exists(err_path):
        os.remove(err_path)
    argv = [os.path.join(HERE, 'session.py'), agent, n, '--model', model, '--effort', effort, '--pages', os.getcwd(), '--repo', repo,
            '--kind', kind]
    err, p = spawn_proc(status_path(agent, n, kind), os.path.join(runs, 'host.log'), argv + (['--ask'] if ask else []) + (['--resume'] if resume else []), cwd=os.getcwd())
    if err:
        return err
    t0 = time.time()
    while time.time() - t0 < wait:
        st = load_json(status_path(agent, n, kind), {})
        if st.get('pid') == p.pid and (st.get('state') == 'working' or (p.poll() is not None and not os.path.exists(err_path))):
            return None
        if p.poll() is not None:
            try:
                return open(err_path, encoding='utf-8').read().strip() or f'session host exit {p.returncode}'
            except OSError:
                return f'session host exit {p.returncode}'
        time.sleep(0.1)
    return 'the session host did not start in time'


def start_driver(agent, batch, model=None, effort=None, resume=False):
    """Start the batch driver's session for one batch: None when it runs, else why not."""
    model, effort = str(model or 'gpt-5.6-terra'), str(effort or 'high')
    if not re.fullmatch(r'[\w.-]+', model) or not re.fullmatch(r'[\w-]+', effort):
        return 'bad model or effort'
    wt = batch_worktree(agent, batch)
    if not wt:
        return 'batch ' + batch + ' has no worktree: set it up first'
    if settle(status_path(agent, batch, 'driver')).get('state') == 'working':
        return 'the driver is already running'
    if resume and not resumable(agent, batch, 'driver'):
        return 'nothing to resume: no stopped driver with a session file'
    return start_session(agent, batch, model, effort, wt, ask=not resume, resume=resume, kind='driver')


def stepgit():
    """The scripts' stepgit module, or None with scripts that predate it."""
    if SCRIPTS not in sys.path:
        sys.path.insert(0, SCRIPTS)
    try:
        import stepgit as m
    except ImportError:
        return None
    return m


NO_RERUNS = 'reruns with feedback need the toolkit scripts with stepgit.py; run the step without feedback'


PREP = ('analysis', 'strategy', 'context')


def prep_refusal(agent, n, step, repo):
    """Why step cannot start now: another of the three answers is running in the same tree. None when it can."""
    for other in PREP:
        if other != step and settle(status_path(agent, n, other)).get('state') == 'working':
            return other + ' is running: wait for it or stop it'
    return None


def start_step(agent, n, step, model=None, effort=None, ask=False, resume=False, feedback=None, source=None):
    """Start one step of one issue: setup.py, run.py for the three answers, or the resolution's host. None when
    started, else why not."""
    model, effort = str(model or 'gpt-5.6-terra'), str(effort or 'high')
    if not re.fullmatch(r'[\w.-]+', model) or not re.fullmatch(r'[\w-]+', effort):
        return 'bad model or effort'
    if step == 'setup':
        batch = card_batch(agent, n)
        if not batch:
            return 'no batch: put the card in a batch first'
        base = batch_base(agent, batch)
        if not base:
            return 'batch ' + batch + ' has no base branch: set it in the sidebar'
        return spawn_proc(status_path(agent, n, 'setup'), os.path.join('agents', agent, 'setup', 'runs', n, 'run.log'),
                          [os.path.join(SCRIPTS, 'setup.py'), agent, n, '--pages', os.getcwd(), '--repo', REPO, '--base', base, '--batch', batch])[0]
    repo = repo_of(agent, n)
    if not repo:
        return 'no worktree: set the issue up first'
    if step == 'resolve':
        if resume and not resumable(agent, n):
            return 'nothing to resume: no stopped session with a session file'
        return start_session(agent, n, model, effort, repo, ask=ask and not resume, resume=resume)
    why = prep_refusal(agent, n, step, repo)
    if why:
        return why
    return spawn_proc(status_path(agent, n, step), None,
                      [os.path.join(SCRIPTS, 'run.py'), agent, n, step, '--pages', os.getcwd(), '--repo', repo, '--model', model, '--effort', effort]
                      + (['--feedback', feedback] if feedback else []) + (['--from', source] if feedback and source else []), cwd=repo)[0]


def host_call(agent, n, req, timeout=15, kind='resolve'):
    """One command to the issue's session host (with kind driver, the batch driver's) over its socket: its reply, or
    {"error"} when no host listens."""
    path = os.path.join('agents', agent, kind, 'runs', n, 'sock')
    if settle(status_path(agent, n, kind)).get('state') != 'working' or not os.path.exists(path):
        return {'error': 'no session: start it first' if req.get('cmd') == 'ask' else 'not running'}
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect(path)
        s.sendall((json.dumps(req, ensure_ascii=False) + '\n').encode())
        buf = b''
        while not buf.endswith(b'\n'):
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
        return json.loads(buf or b'{"error": "no reply"}')
    except (OSError, ValueError) as ex:
        return {'error': 'session host: ' + str(ex)}
    finally:
        s.close()


SOURCES = ('resolver', 'engineer', 'ruling')


def feedback_lines(agent, n, step):
    """How a rerun step weighed its feedback, from its answer's `feedback`: the verdict, then each point."""
    fb = load_json(os.path.join('agents', agent, step, n + '.json'), {}).get('feedback') or {}
    if not fb.get('verdict'):
        return []
    out = [f"{step} answered the feedback: {fb['verdict']}."]
    for p in fb.get('points') or []:
        out.append(f"  {p.get('verdict')} · {p.get('claim')}")
        if p.get('verdict') == 'disputed':
            out.append(f"      why: {p.get('why')}")
            if p.get('basis'):
                out.append(f"      basis: {p['basis']}")
    return out


def contest(agent, n):
    """The open disagreement: the latest review contested entry when no ruling came after it, with the rerun step's
    disputed points. {} when none."""
    log = load_json(os.path.join('agents', agent, 'resolve', n + '.stage.json'), [])
    last = next((e for e in reversed(log) if e.get('stage') == 'review' and e.get('state') in ('contested', 'ruled')), None)
    if not last or last['state'] != 'contested' or last.get('step') not in PREP:
        return {}
    fb = load_json(os.path.join('agents', agent, last['step'], n + '.json'), {}).get('feedback') or {}
    return {'step': last['step'], 'held': last.get('note'), 't': last.get('t'),
            'disputed': [p for p in fb.get('points') or [] if p.get('verdict') == 'disputed']}


def rule(agent, n, side, gap=False):
    """The engineer's ruling on the open disagreement. For the resolver: the step reruns with the ruling, which it
    applies. For the step: the live resolution session is told the answer stands on those points. Either way stage.py
    records review ruled, and a skill gap is appended to agents/<agent>/skill-gaps.json. (state, None) or (None, why not)."""
    c = contest(agent, n)
    if not c:
        return None, 'no open disagreement'
    if side not in ('resolver', 'step'):
        return None, 'rule for resolver or step'
    step, points = c['step'], '\n'.join('- ' + (p.get('claim') or '') for p in c['disputed'])
    if side == 'resolver':
        st = settle(status_path(agent, n, step))
        feedback = (f"On the points you disputed, the resolution agent is right:\n{points}\n\n"
                    f"The resolution agent's reply to your dispute: {c.get('held') or ''}")
        out, err = start_chain(agent, n, [step], st.get('model'), st.get('effort'), feedback=feedback, source='ruling')
        if err:
            return None, err
    else:
        msg = (f"The engineer ruled for {step} on:\n{points}\n"
               "The answer stands on those points. Do not raise them again; review the rest as usual.")
        live = host_call(agent, n, {'cmd': 'state'})
        out = host_call(agent, n, {'cmd': 'send', 'message': msg, 'mode': 'follow_up' if live.get('streaming') else 'prompt'}) if 'error' not in live else live
    note = 'for ' + ('the resolution agent' if side == 'resolver' else step) + ('; skill gap' if gap else '')
    subprocess.run([sys.executable, os.path.join(SCRIPTS, 'stage.py'), agent, n, 'review', 'ruled', '--step', step,
                    '--note', note, '--pages', os.getcwd()], capture_output=True)
    if gap:
        path = os.path.join('agents', agent, 'skill-gaps.json')
        gaps = load_json(path, [])
        gaps.append({'t': now(), 'n': n, 'step': step, 'disputed': c['disputed'], 'held': c.get('held'), 'for': side})
        write_json(path, gaps)
    return out, None


def rerun_note(agent, n, ran):
    """What the resolution session is told when steps it blamed were rerun: each step's outcome, its new answer, and to
    review them again."""
    lines = ['The engineer reran ' + ', '.join(ran) + ' with feedback.']
    for step in ran:
        st = settle(status_path(agent, n, step))
        if st.get('state') != 'done':
            lines.append(f"{step}: {st.get('state') or 'not run'}" + (f" ({st['error']})" if st.get('error') else '') + '.')
        else:
            lines.append(f"{step}: done, new answer in {os.path.join('agents', agent, step, n + '.json')}.")
        lines += feedback_lines(agent, n, step)
    disputed = any('disputed' in l.split(' · ')[0] for step in ran for l in feedback_lines(agent, n, step)[1:])
    lines.append('Weigh each disputed point: concede it, or hold it with review contested, as your skill says; then review them again.'
                 if disputed else 'Review them again.')
    return '\n'.join(lines)


def notify_rerun(agent, n, ran):
    """Send rerun_note to the issue's live resolution session, after its current turn when it is working. The reply,
    or {"error"} when none is live."""
    st = host_call(agent, n, {'cmd': 'state'})
    if 'error' in st:
        return st
    return host_call(agent, n, {'cmd': 'send', 'message': rerun_note(agent, n, ran), 'mode': 'follow_up' if st.get('streaming') else 'prompt'})


def stale_states(agent):
    """{n: {step: why}} for answers an earlier step's newer answer has overtaken."""
    out = {}
    base = os.path.join('agents', agent)
    for f in os.listdir(os.path.join(base, 'setup')) if os.path.isdir(os.path.join(base, 'setup')) else []:
        m = re.fullmatch(r'(\d+)\.status\.json', f)
        if not m:
            continue
        n = m.group(1)
        times = {}
        for step in PREP:
            try:
                times[step] = os.stat(os.path.join(base, step, n + '.json')).st_mtime
            except OSError:
                pass
        for k, step in enumerate(PREP):
            st = load_json(status_path(agent, n, step), {})
            if step not in times or st.get('state') == 'working':
                continue
            newer = [e for e in PREP[:k] if times.get(e, 0) > times[step]]
            if newer:
                out.setdefault(n, {})[step] = newer[-1] + ' is newer'
    return out


def add_usage(u, ev):
    """Adds one event's tokens and cost to u: an assistant message_end brings its usage, a tool_execution_end counts
    one command, and context is the latest call's whole input. The same sums run.py keeps for the three answers."""
    if ev.get('type') == 'message_end' and (ev.get('message') or {}).get('role') == 'assistant':
        x = ev['message'].get('usage') or {}
        for k, f in (('in', 'input'), ('cached', 'cacheRead'), ('out', 'output'), ('reasoning', 'reasoning')):
            u[k] = u.get(k, 0) + (x.get(f) or 0)
        u['cost'] = round(u.get('cost', 0) + ((x.get('cost') or {}).get('total') or 0), 6)
        u['context'] = (x.get('input') or 0) + (x.get('cacheRead') or 0)
        return True
    if ev.get('type') == 'tool_execution_end':
        u['commands'] = u.get('commands', 0) + 1
    return False


def usage_of_log(path):
    u = {'in': 0, 'cached': 0, 'out': 0, 'reasoning': 0, 'commands': 0, 'cost': 0.0}
    for line in open(path, encoding='utf-8') if os.path.exists(path) else []:
        try:
            add_usage(u, json.loads(line))
        except ValueError:
            pass
    return u


def run_counts(path):
    """{run, passed, total, green, sims} from a `sierra test --json` file: runs passed of runs, sims all-green of sims."""
    d = load_json(path, None)
    if not isinstance(d, dict) or not d.get('tests'):
        return None
    tests = d['tests']
    return {'run': d.get('simulationRunId'), 'passed': sum(x.get('passed') or 0 for x in tests),
            'total': sum(x.get('total') or 0 for x in tests), 'sims': len(tests),
            'green': sum(1 for x in tests if x.get('total') and x.get('passed') == x.get('total'))}


def chain_path(agent, n):
    return os.path.join('agents', agent, 'chain', n + '.json')


def chain_state(agent, n):
    """The sequence's state file; a working one whose chain.py is gone is written back as failed."""
    path = chain_path(agent, n)
    st = load_json(path, {})
    if st.get('state') == 'working' and not alive(int(st.get('pid') or 0)):
        st.update(state='failed', error=st.get('error') or 'the sequence process ended', ended=st.get('ended') or now())
        write_json(path, st)
    return st


def start_chain(agent, n, steps, model, effort, wait=10, feedback=None, source=None):
    """Start chain.py for one issue and wait until it has written its state: (state, None) or (None, why not). The
    first step is checked here as run.py would refuse it; feedback goes to that step."""
    if chain_state(agent, n).get('state') == 'working':
        return None, 'a sequence is already running'
    if feedback and not stepgit():
        return None, NO_RERUNS
    first = next((x for x in ORDER if x in steps), None)
    repo = repo_of(agent, n)
    if first in PREP and repo:
        why = prep_refusal(agent, n, first, repo)
        if why:
            return None, why
    stop = chain_path(agent, n)[:-5] + '.stop'
    if os.path.exists(stop):
        os.remove(stop)
    argv = [os.path.join(HERE, 'chain.py'), agent, n, '--steps', ','.join(steps), '--pages', os.getcwd()]
    if model:
        argv += ['--model', str(model)]
    if effort:
        argv += ['--effort', str(effort)]
    if feedback:
        argv += ['--feedback', str(feedback)]
        if source in SOURCES:
            argv += ['--from', source]
    err, p = spawn_proc(chain_path(agent, n), os.path.join('agents', agent, 'chain', 'runs', n + '.log'), argv, cwd=os.getcwd())
    if err:
        return None, 'a sequence is already running'
    t0 = time.time()
    while time.time() - t0 < wait:
        st = load_json(chain_path(agent, n), {})
        if st.get('pid') == p.pid:
            return st, None
        if p.poll() is not None:
            return None, f'chain.py exit {p.returncode}'
        time.sleep(0.05)
    return None, 'the sequence did not start in time'
