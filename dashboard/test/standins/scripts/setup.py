"""Stand-in for setup.py: the issue's worktree is a new git repo with one commit under --repo; status done."""
import os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import standin, paths

(agent, n), o = standin.args(sys.argv[1:])
prefix = {'cobranzas': 'cob', 'openpay': 'opp', 'hipotecarios': 'hip'}[agent]
wt = os.path.join(o['--repo'], '.claude', 'worktrees', f'{prefix}-{n}')
path = paths.status(paths.agent(o['--pages'], agent), n, 'setup')
st = {'state': 'working', 'pid': os.getpid(), 'started': standin.now(), 'name': f'{prefix}-{n}', 'worktree': wt, 'branch': f'stan/{prefix}-{n}',
      'batch': o.get('--batch'), 'base': o.get('--base'), 'steps': [], 'step': 'worktree'}
standin.write(path, st)
standin.log('setup.py', n=n, agent=agent, base=o.get('--base'))
time.sleep(float(os.environ.get('STANDIN_SECONDS') or 0.5))
os.makedirs(wt, exist_ok=True)
if not os.path.exists(os.path.join(wt, '.git')):
    open(os.path.join(wt, 'README'), 'w').write('lab\n')
    for cmd in (['init', '-q', '-b', f'stan/{prefix}-{n}'], ['add', '-A'], ['commit', '-q', '-m', 'fork point']):
        subprocess.run(['git', '-C', wt] + cmd, check=True, capture_output=True)
commit = subprocess.run(['git', '-C', wt, 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()
st.pop('step'); st.update(state='done', ended=standin.now(), seconds=0, steps=['worktree'], commit=commit, workspace='standin-' + n)
standin.write(path, st)
