"""A throwaway pages dir for the checks: the staging code, a fresh copy of the fixture, the stand-in scripts beside
copies of the real card.py, blocks.py, cardlog.py, ledger.py and stage.py, and a fake repo. Nothing in it reaches a model,
Studio, the tracker or the real repo."""
import json, os, shutil, signal, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
STAGING = os.path.dirname(HERE)
TOOLKIT = next(d for d in (os.environ.get('LAB_TOOLKIT'), os.path.join(STAGING, 'scripts'),  # the staging copy, else the live
                            os.path.expanduser('~/code/toolkit/plugin/skills/sierra/scripts')) if d and os.path.isdir(d))  # (read only)
RERUNS = os.path.exists(os.path.join(TOOLKIT, 'stepgit.py'))  # scripts with step commits, rewinds and --feedback
CODE = ('serve.py', 'steps.py', 'session.py', 'chain.py', 'index.html', 'card.js', 'page.css', 'sections.css', 'refine.html', 'preact-htm.js')


def make(run):
    """Builds the dir at run and returns the environment the server and scripts run with there."""
    if os.path.isdir(run):
        stop_all(run)
        shutil.rmtree(run)
    os.makedirs(run)
    for f in CODE:
        shutil.copy(os.path.join(STAGING, f), os.path.join(run, f))
    shutil.copytree(os.path.join(HERE, 'fixture'), run, dirs_exist_ok=True)
    repo = os.path.join(run, 'repo')
    for root, _, files in os.walk(os.path.join(run, 'agents')):
        for f in files:
            if f.endswith('.json'):
                p = os.path.join(root, f)
                t = open(p, encoding='utf-8').read()
                if '@REPO@' in t:
                    open(p, 'w', encoding='utf-8').write(t.replace('@REPO@', repo))
                    for wt in [v for v in [json.load(open(p)).get('worktree')] if isinstance(v, str)]:
                        git_repo(wt)
    scripts = os.path.join(run, 'skills', 'sierra', 'scripts')
    shutil.copytree(os.path.join(HERE, 'standins', 'scripts'), scripts)
    for f in ('card.py', 'blocks.py', 'cardlog.py', 'ledger.py', 'stage.py') + (('stepgit.py',) if RERUNS else ()):
        shutil.copy(os.path.join(TOOLKIT, f), os.path.join(scripts, f))
    shutil.copy(os.path.join(TOOLKIT, 'brief.py'), os.path.join(scripts, 'brief_real.py'))
    os.makedirs(os.path.join(run, 'skills', 'issue-resolution'))
    open(os.path.join(run, 'skills', 'issue-resolution', 'SKILL.md'), 'w').write('---\nname: issue-resolution\n---\nStand-in resolution instructions.\n')
    os.makedirs(os.path.join(repo, '.claude', 'worktrees'), exist_ok=True)
    for skill in ('issue-analysis', 'sim-strategy', 'context-edit'):  # what the real run.py reads: a stand-in skill and schema
        d = os.path.join(run, 'plugin', 'skills', skill)
        os.makedirs(d)
        open(os.path.join(d, 'SKILL.md'), 'w').write(f'Stand-in {skill} instructions.\n')
        json.dump({'type': 'object', 'required': ['ok'], 'properties': {'ok': {'type': 'boolean'}}}, open(os.path.join(d, 'schema.json'), 'w'))
    return dict(os.environ, SIERRA_SCRIPTS=scripts, BBVA_REPO=repo, SIERRA_PI=os.path.join(HERE, 'standins', 'pi'),
                STANDIN_LOG=os.path.join(run, 'standin.log'), CHAIN_POLL='0.2', GIT_CEILING_DIRECTORIES=run, PYTHONDONTWRITEBYTECODE='1',
                SIERRA_PLUGIN=os.path.join(run, 'plugin'), **GIT_ENV)


GIT_ENV = {'GIT_AUTHOR_NAME': 'lab', 'GIT_AUTHOR_EMAIL': 'lab@example.invalid', 'GIT_COMMITTER_NAME': 'lab',
           'GIT_COMMITTER_EMAIL': 'lab@example.invalid', 'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_NOSYSTEM': '1'}


def git_repo(wt, files=None):
    """A throwaway git repo at wt with one commit of files ({path: text}); its short hash."""
    os.makedirs(wt, exist_ok=True)
    env = dict(os.environ, **GIT_ENV)
    subprocess.run(['git', 'init', '-q', '-b', 'stan/' + os.path.basename(wt), wt], check=True, env=env)
    for rel, text in (files or {'README': 'lab\n'}).items():
        os.makedirs(os.path.dirname(os.path.join(wt, rel)), exist_ok=True)
        open(os.path.join(wt, rel), 'w').write(text)
    subprocess.run(['git', '-C', wt, 'add', '-A'], check=True, env=env)
    subprocess.run(['git', '-C', wt, 'commit', '-q', '-m', 'fork point'], check=True, env=env)
    return subprocess.run(['git', '-C', wt, 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True, env=env).stdout.strip()


def serve(run, env, port):
    """Starts the server of that dir on port and waits until it answers; the Popen."""
    with open(os.path.join(run, 'serve.log'), 'ab') as log:
        p = subprocess.Popen([sys.executable, os.path.join(run, 'serve.py'), str(port)], env=env, cwd=run,
                             stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    with open(os.path.join(run, 'server.pid'), 'w') as f:
        f.write(str(p.pid))
    wait_up(port)
    return p


def wait_up(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            return urllib.request.urlopen(f'http://127.0.0.1:{port}/index.html', timeout=1).headers.get('X-Server-Boot')
        except Exception:
            time.sleep(0.1)
    raise RuntimeError(f'no server on {port}')


def stop_all(run):
    """Ends every process this lab started under run: the server, session hosts, sequences, stand-ins."""
    out = subprocess.run(['ps', '-axo', 'pid=,command='], capture_output=True, text=True).stdout
    for line in out.splitlines():
        pid, _, cmd = line.strip().partition(' ')
        if run in cmd and int(pid) != os.getpid():
            try:
                os.kill(int(pid), signal.SIGKILL)
            except OSError:
                pass


if __name__ == '__main__':
    cmd, run = sys.argv[1], os.path.abspath(sys.argv[2])
    if cmd == 'up':
        serve(run, make(run), int(sys.argv[3]))
    elif cmd == 'down':
        stop_all(run)
