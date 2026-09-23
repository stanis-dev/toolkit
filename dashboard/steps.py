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
        m = re.match(r'\s*<!--\s*batch:\s*(\d{4})\s*-->', open(os.path.join('agents', agent, 'cards', n + '.html'), encoding='utf-8').read(400))
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


def session_dir(agent, n):
    return os.path.join('agents', agent, 'resolve', 'runs', n, 'session')


def resumable(agent, n):
    """A resolution session that ended without finishing (stopped, crashed, host gone) and left pi's session file."""
    st = settle(status_path(agent, n, 'resolve'))
    d = session_dir(agent, n)
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


def start_session(agent, n, model, effort, repo, ask=False, resume=False, wait=60):
    """Start session.py, the resolution's own host process, and wait until it holds the session or gives up: None
    when it runs, else its reason (the brief failed, nothing to resume)."""
    runs = os.path.join('agents', agent, 'resolve', 'runs', n)
    os.makedirs(runs, exist_ok=True)
    err_path = os.path.join(runs, 'start.err')
    if os.path.exists(err_path):
        os.remove(err_path)
    argv = [os.path.join(HERE, 'session.py'), agent, n, '--model', model, '--effort', effort, '--pages', os.getcwd(), '--repo', repo]
    err, p = spawn_proc(status_path(agent, n, 'resolve'), os.path.join(runs, 'host.log'), argv + (['--ask'] if ask else []) + (['--resume'] if resume else []), cwd=os.getcwd())
    if err:
        return err
    t0 = time.time()
    while time.time() - t0 < wait:
        st = load_json(status_path(agent, n, 'resolve'), {})
        if st.get('pid') == p.pid and (st.get('state') == 'working' or (p.poll() is not None and not os.path.exists(err_path))):
            return None
        if p.poll() is not None:
            try:
                return open(err_path, encoding='utf-8').read().strip() or f'session host exit {p.returncode}'
            except OSError:
                return f'session host exit {p.returncode}'
        time.sleep(0.1)
    return 'the session host did not start in time'


def stepgit():
    """The scripts' stepgit module, or None with scripts that predate step commits and rewinds."""
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
    """Why step cannot start now: another of the three answers is running (the rewind would pull the tree from under
    it), or the worktree has uncommitted changes. None when it can."""
    for other in PREP:
        if other != step and settle(status_path(agent, n, other)).get('state') == 'working':
            return other + ' is running: wait for it or stop it'
    try:
        return stepgit() and stepgit().refusal(repo)
    except RuntimeError as ex:
        return str(ex)


def start_step(agent, n, step, model=None, effort=None, ask=False, resume=False, feedback=None):
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
                      + (['--feedback', feedback] if feedback else []), cwd=repo)[0]


def host_call(agent, n, req, timeout=15):
    """One command to the issue's session host over its socket: its reply, or {"error"} when no host listens."""
    path = os.path.join('agents', agent, 'resolve', 'runs', n, 'sock')
    if settle(status_path(agent, n, 'resolve')).get('state') != 'working' or not os.path.exists(path):
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


def rerun_note(agent, n, ran):
    """What the resolution session is told when steps it blamed were rerun: each step's outcome and new commit, what
    the rewind dropped, and to review them again."""
    lines = ['The engineer reran ' + ', '.join(ran) + ' with feedback.']
    for k, step in enumerate(ran):
        st = settle(status_path(agent, n, step))
        rw = st.get('rewind') or {}
        if k == 0 and rw.get('dropped'):
            lines.append('The branch was rewound first, dropping ' + '; '.join(d['short'] + ' ' + d['subject'] for d in rw['dropped'])
                         + ('; the issue workspace was pushed to match.' if rw.get('pushed') else '.'))
        c = st.get('step_commit')
        if st.get('state') != 'done':
            lines.append(f"{step}: {st.get('state') or 'not run'}" + (f" ({st['error']})" if st.get('error') else '') + '.')
        elif c:
            lines.append(f"{step}: new commit {c['short']} {c['subject']}.")
        else:
            lines.append(f"{step}: done, no files changed" + ('' if step == 'analysis' else ', no commit') + '.')
    lines.append('Review them again.')
    return '\n'.join(lines)


def notify_rerun(agent, n, ran):
    """Send rerun_note to the issue's live resolution session, after its current turn when it is working. The reply,
    or {"error"} when none is live."""
    st = host_call(agent, n, {'cmd': 'state'})
    if 'error' in st:
        return st
    return host_call(agent, n, {'cmd': 'send', 'message': rerun_note(agent, n, ran), 'mode': 'follow_up' if st.get('streaming') else 'prompt'})


HEADS = {}  # (worktree, commit) -> (reflog stamp, on the branch)


def head_stamp(wt):
    """The mtime of the worktree's HEAD reflog: it moves with every commit, reset and checkout."""
    g = os.path.join(wt, '.git')
    try:
        if os.path.isfile(g):
            g = open(g).read().split('gitdir:', 1)[1].strip()
        return os.stat(os.path.join(g, 'logs', 'HEAD')).st_mtime_ns
    except (OSError, IndexError):
        return None


def on_branch(wt, commit):
    key, stamp = (wt, commit), head_stamp(wt)
    hit = HEADS.get(key)
    if hit and hit[0] == stamp and stamp is not None:
        return hit[1]
    r = subprocess.run(['git', '-C', wt, 'merge-base', '--is-ancestor', commit, 'HEAD'], capture_output=True)
    HEADS[key] = (stamp, r.returncode == 0)
    return r.returncode == 0


def stale_states(agent):
    """{n: {step: why}} for answers that no longer match the branch: their step commit was dropped (a rewind, or the
    branch moved), or an earlier step's answer is newer than theirs."""
    out = {}
    base = os.path.join('agents', agent)
    for f in os.listdir(os.path.join(base, 'setup')) if os.path.isdir(os.path.join(base, 'setup')) else []:
        m = re.fullmatch(r'(\d+)\.status\.json', f)
        if not m:
            continue
        n = m.group(1)
        wt = repo_of(agent, n)
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
            c = (st.get('step_commit') or {}).get('hash')
            newer = [e for e in PREP[:k] if times.get(e, 0) > times[step]]
            if c and wt and not on_branch(wt, c):
                out.setdefault(n, {})[step] = 'its commit ' + c[:9] + ' is no longer on the branch'
            elif newer:
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


def start_chain(agent, n, steps, model, effort, wait=10, feedback=None):
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
