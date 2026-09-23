#!/usr/bin/env python3
"""Host of one resolution session: pi in RPC mode for one issue, in a process of its own, so the pages server can
restart without ending it.

  session.py <agent> <n> [--model <id>] [--effort <level>] [--ask] [--resume] [--pages <dir>] [--repo <dir>]

Starts pi in the issue's worktree with the step's brief (brief.py --step resolve) as the first prompt; with --ask the
issue-resolution skill text follows the brief in that prompt. --resume starts pi on the session file of the last
session instead (--continue in its session dir), with no new prompt. Writes, under agents/<agent>/resolve/:
runs/<n>/out.jsonl (pi's events, results capped, the server streams it to the page), <n>.status.json (state, pid of
this process, usage, whose turn it is as "turn", an in-flight sim run as "simrun"), <n>.runs.json (pass counts of every
`sierra … test` the session ran) and, when pi ends, the ticket's ledger entry. Listens on the Unix socket runs/<n>/sock
for one JSON line per connection: {"cmd": "send", "message", "mode"?}, {"cmd": "abort"}, {"cmd": "ui", "id", …},
{"cmd": "ask"}, {"cmd": "stop"}, {"cmd": "state"}; replies with one JSON line, {"error": …} when refused. A start that
fails before pi runs leaves its reason in runs/<n>/start.err and exits 2."""
import json, os, re, shutil, signal, socket, subprocess, sys, threading
from datetime import datetime, timezone

import steps
from steps import now, write_json, load_json, add_usage, usage_of_log, run_counts, SIM_RUN, USAGE

PI = os.environ.get('SIERRA_PI') or shutil.which('pi') or '/opt/homebrew/bin/pi'
PROVIDER = os.environ.get('SIERRA_RUN_PROVIDER') or 'openai-codex'
SYSTEM = ('You work one issue of a Sierra voice agent with an engineer. The first message is the issue\'s brief: '
          'where things live, the issue and the step answers so far. Until a message brings the resolution '
          'instructions, answer the engineer from the brief and the files and change nothing.')


class Refused(Exception):
    pass


class Host:
    def __init__(self, agent, n, repo, model, effort):
        self.agent, self.n, self.repo, self.model, self.effort = agent, n, repo, model, effort
        self.base = os.path.join(os.getcwd(), 'agents', agent, 'resolve')
        self.runs = os.path.join(self.base, 'runs', n)
        self.status_path = os.path.join(self.base, n + '.status.json')
        self.log_path = os.path.join(self.runs, 'out.jsonl')
        self.sock_path = os.path.join(self.runs, 'sock')
        self.session_dir = os.path.join(self.runs, 'session')
        self.lock, self.wlock, self.llock = threading.Lock(), threading.Lock(), threading.Lock()
        self.streaming = self.stopping = self.ended = False
        self.live = None
        self.proc = None

    def skill(self):
        """The issue-resolution skill text without its frontmatter, kept in ask.md."""
        skill = open(os.path.join(steps.SCRIPTS, '..', '..', 'issue-resolution', 'SKILL.md'), encoding='utf-8').read()
        skill = re.sub(r'\A---\n.*?\n---\n', '', skill, flags=re.S)
        open(os.path.join(self.runs, 'ask.md'), 'w', encoding='utf-8').write(skill)
        return skill

    def prepare(self, ask, resume):
        """Everything before pi starts; Refused when the session cannot start."""
        os.makedirs(self.runs, exist_ok=True)
        if len(self.sock_path) > 100:
            raise Refused('socket path too long: ' + self.sock_path)
        self.previous = load_json(self.status_path, {})
        if resume:
            if not (os.path.isdir(self.session_dir) and any(f.endswith('.jsonl') for f in os.listdir(self.session_dir))):
                raise Refused('nothing to resume: no session file in ' + self.session_dir)
            self.opening = None
        else:
            brief = subprocess.run([sys.executable, os.path.join(steps.SCRIPTS, 'brief.py'), self.agent, self.n, '--step', 'resolve',
                                    '--pages', os.getcwd(), '--repo', self.repo], capture_output=True, text=True)
            if brief.returncode != 0:
                raise Refused('brief: ' + brief.stderr.strip()[-600:])
            self.opening = brief.stdout + ('\n\n' + self.skill() if ask else '')
            open(os.path.join(self.runs, 'brief.md'), 'w', encoding='utf-8').write(self.opening)
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
            if os.path.isdir(self.session_dir) and os.listdir(self.session_dir):
                os.replace(self.session_dir, self.session_dir + '.' + stamp)
            shutil.rmtree(self.session_dir, ignore_errors=True)
            os.makedirs(self.session_dir)
            if os.path.exists(self.log_path) and os.path.getsize(self.log_path):  # the session before keeps its log
                os.replace(self.log_path, os.path.join(self.runs, 'out.' + stamp + '.jsonl'))
        before = [usage_of_log(os.path.join(self.runs, f)) for f in sorted(os.listdir(self.runs)) if re.fullmatch(r'out\.\d{8}T\d{6}Z\.jsonl', f)]
        if resume and os.path.exists(self.log_path):
            before.append(usage_of_log(self.log_path))
        self.usage = {k: 0 for k in USAGE}
        self.usage['cost'] = 0.0
        self.before = {k: sum(b[k] for b in before) for k in USAGE} if before else None
        if os.path.exists(self.sock_path):
            os.remove(self.sock_path)
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(self.sock_path)
        self.server.listen(16)
        self.ask_at = now() if ask and not resume else (self.previous.get('asked') or False) if resume else False

    def total(self):
        """This session's usage plus every earlier session's of this issue, whose logs sit next to it."""
        if not self.before:
            return None
        return {k: round(self.before[k] + self.usage[k], 6) if k == 'cost' else self.before[k] + self.usage[k] for k in USAGE}

    def write_status(self, **kw):
        with self.lock:
            self.status.update(kw)
            write_json(self.status_path, self.status)

    def start(self, resume):
        commit = subprocess.run(['git', '-C', self.repo, 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()
        cmd = [PI, '--mode', 'rpc', '--no-skills', '--no-extensions', '--no-context-files', '--no-prompt-templates',
               '--system-prompt', SYSTEM, '--session-dir', self.session_dir, '--thinking', self.effort, '--model', f'{PROVIDER}/{self.model}']
        if resume:
            cmd.append('--continue')
        open(os.path.join(self.runs, 'system.md'), 'w', encoding='utf-8').write(SYSTEM)
        self.log = open(self.log_path, 'a', encoding='utf-8')
        self.err = open(os.path.join(self.runs, 'err.log'), 'a' if resume else 'w')
        self.proc = subprocess.Popen(cmd, cwd=self.repo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.err,
                                     text=True, encoding='utf-8', errors='replace', bufsize=1)
        self.status = {'step': 'resolve', 'state': 'working', 'started': now(), 'ended': None, 'seconds': None, 'commit': commit,
                       'model': self.model, 'effort': self.effort, 'pid': os.getpid(), 'pi': self.proc.pid, 'thread': None,
                       'usage': dict(self.usage), 'usage_all': self.total(), 'live': None, 'error': None, 'asked': self.ask_at,
                       'turn': 'you', 'simrun': None, 'resumed': now() if resume else None}
        write_json(self.status_path, self.status)
        threading.Thread(target=self.reader, daemon=True).start()
        if resume:
            self.emit({'type': 'resumed'})
        else:
            self.send({'type': 'prompt', 'message': self.opening})

    def emit(self, ev):
        ev['t'] = now()
        with self.llock:
            self.log.write(json.dumps(ev, ensure_ascii=False) + '\n'); self.log.flush()

    def reader(self):
        for raw in self.proc.stdout:
            raw = raw.rstrip('\r\n')
            if not raw:
                continue
            try:
                ev = json.loads(raw)
            except ValueError:
                ev = {'type': 'stderr', 'text': raw}
            t = ev.get('type')
            if add_usage(self.usage, ev):
                self.write_status(usage=dict(self.usage), usage_all=self.total())
            if t in ('tool_execution_start', 'tool_execution_end') and ev.get('toolName') == 'bash':
                self.track_run(t, ev)
            if t == 'agent_start':
                self.streaming = True; self.write_status(turn='agent')
            elif t == 'agent_settled':
                self.streaming = False; self.write_status(turn='you')
            if t == 'tool_execution_end':  # cap what the log keeps of one result
                res = ev.get('result')
                if isinstance(res, dict):
                    text = '\n'.join(c.get('text', '') for c in res.get('content') or [] if isinstance(c, dict))
                    ev['result'] = {'text': text[:20000] + (f'\n… {len(text) - 20000} more chars' if len(text) > 20000 else '')}
            elif t in ('message_start', 'message_end') and (ev.get('message') or {}).get('role') == 'user':
                m = ev['message']; k = sum(len(c.get('text') or '') for c in m.get('content') or [] if isinstance(c, dict))
                ev['message'] = {'role': 'user', 'chars': k, 'timestamp': m.get('timestamp')}
            elif t == 'message_update':
                ev = {'type': t, 'assistantMessageEvent': ev.get('assistantMessageEvent')}
            elif t == 'turn_end':
                ev = {'type': t}
            self.emit(ev)
        rc = self.proc.wait()
        self.streaming = False
        started = datetime.strptime(self.status['started'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        self.write_status(usage=dict(self.usage), usage_all=self.total(), turn=None, simrun=None,
                          state='done' if rc == 0 else 'failed', ended=now(),
                          error=None if rc == 0 else 'stopped from the page' if self.stopping else f'pi exit {rc}',
                          seconds=round((datetime.now(timezone.utc) - started).total_seconds()))
        sys.path.insert(0, steps.SCRIPTS)
        import ledger
        ledger.add(os.getcwd(), self.agent, self.n, ledger.entry(self.status['ended'], 'resolve', self.status, self.usage))
        self.emit({'type': 'exit', 'code': rc})
        self.ended = True
        try:
            socket.socket(socket.AF_UNIX, socket.SOCK_STREAM).connect(self.sock_path)  # wakes the accept loop
        except OSError:
            pass

    def track_run(self, t, ev):
        """A `sierra … test` launch: in flight between its start and end events; at the end the file it wrote is read
        and its pass counts appended to resolve/<n>.runs.json under the stage current then."""
        if t == 'tool_execution_start':
            cmd = str((ev.get('args') or {}).get('command') or '')
            if SIM_RUN.search(cmd) and '--list' not in cmd:
                out = re.search(r'>\s*(\S+\.json)', cmd)
                self.live = {'id': ev.get('toolCallId'), 't': now(), 'out': out.group(1) if out else None}
                self.write_status(simrun={'t': self.live['t']})
            return
        live = self.live
        if not live or live['id'] != ev.get('toolCallId'):
            return
        self.live = None
        self.write_status(simrun=None)
        counts = run_counts(os.path.join(self.repo, live['out'])) if live['out'] else None
        if counts:
            stages = load_json(os.path.join(self.base, self.n + '.stage.json'), [])
            counts.update(t=now(), stage=stages[-1]['stage'] if stages else None, file=live['out'])
            path = os.path.join(self.base, self.n + '.runs.json')
            write_json(path, load_json(path, []) + [counts])

    def send(self, cmd):
        if self.proc is None or self.proc.poll() is not None:
            raise Refused('not running')
        with self.wlock:
            self.proc.stdin.write(json.dumps(cmd, ensure_ascii=False) + '\n'); self.proc.stdin.flush()
        if cmd.get('type') in ('prompt', 'steer', 'follow_up'):
            self.emit({'type': 'sent', 'mode': cmd['type'], 'text': cmd.get('message', '')})
        elif cmd.get('type') == 'extension_ui_response':
            self.emit({'type': 'ui_answer', 'id': cmd.get('id'), 'answer': {k: v for k, v in cmd.items() if k not in ('type', 'id')}})

    def stop(self):
        if self.proc is not None and self.proc.poll() is None:
            self.stopping = True
            self.proc.terminate()

    def command(self, req):
        what = req.get('cmd')
        if what == 'state':
            return {'running': not self.ended, 'streaming': self.streaming}
        if what == 'send':
            text = str(req.get('message') or '')
            if not text.strip():
                raise Refused('empty message')
            mode = req.get('mode') or ('steer' if self.streaming else 'prompt')
            if mode not in ('prompt', 'steer', 'follow_up'):
                raise Refused('bad mode')
            self.send({'type': mode, 'message': text})
            return {'mode': mode}
        if what == 'abort':
            self.send({'type': 'abort'}); return {}
        if what == 'ui':
            if not req.get('id'):
                raise Refused('no id')
            self.send(dict({k: v for k, v in req.items() if k != 'cmd'}, type='extension_ui_response')); return {}
        if what == 'ask':
            if self.status.get('asked'):
                raise Refused('resolution already sent')
            self.send({'type': 'follow_up' if self.streaming else 'prompt', 'message': self.skill()})
            self.write_status(asked=now()); return {}
        if what == 'stop':
            self.stop(); return {}
        raise Refused('unknown command')

    def client(self, conn):
        with conn:
            try:
                conn.settimeout(10)
                buf = b''
                while not buf.endswith(b'\n'):
                    chunk = conn.recv(65536)
                    if not chunk:
                        break
                    buf += chunk
                if not buf.strip():
                    return
                try:
                    out = self.command(json.loads(buf))
                except Refused as ex:
                    out = {'error': str(ex)}
                except ValueError:
                    out = {'error': 'not JSON'}
                conn.sendall((json.dumps(out, ensure_ascii=False) + '\n').encode())
            except OSError:
                pass

    def serve(self):
        while not self.ended:
            try:
                conn, _ = self.server.accept()
            except OSError:
                break
            if self.ended:
                conn.close(); break
            threading.Thread(target=self.client, args=(conn,), daemon=True).start()
        self.server.close()
        try:
            os.remove(self.sock_path)
        except OSError:
            pass


def main(argv):
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith('--') and argv[k] not in ('--ask', '--resume')}
    flags = {a for a in argv if a in ('--ask', '--resume')}
    args = [a for k, a in enumerate(argv) if not a.startswith('--') and not (k and argv[k - 1] in opts)]
    if len(args) != 2:
        sys.exit(__doc__)
    agent, n = args
    os.chdir(os.path.abspath(opts.get('--pages') or os.path.dirname(os.path.abspath(__file__))))
    repo = opts.get('--repo') or steps.repo_of(agent, n)
    host = Host(agent, n, repo, opts.get('--model') or 'gpt-5.6-terra', opts.get('--effort') or 'high')
    try:
        if not repo:
            raise Refused('no worktree: set the issue up first')
        host.prepare('--ask' in flags, '--resume' in flags)
        host.start('--resume' in flags)
    except (Refused, OSError) as ex:
        os.makedirs(host.runs, exist_ok=True)
        open(os.path.join(host.runs, 'start.err'), 'w', encoding='utf-8').write(str(ex))
        sys.exit(2)
    signal.signal(signal.SIGTERM, lambda *a: host.stop())
    host.serve()


if __name__ == '__main__':
    main(sys.argv[1:])
