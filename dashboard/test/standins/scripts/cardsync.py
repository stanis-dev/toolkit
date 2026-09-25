"""Stand-in for cardsync.py: logs the ask, fast-forwards the worktree to the batch branch, status done."""
import json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import standin

(agent, n), o = standin.args(sys.argv[1:])
card = os.path.join(o['--pages'], 'agents', agent, 'cards', n)
path = os.path.join(card, 'sync', 'status.json')
standin.write(path, {'state': 'working', 'pid': os.getpid(), 'started': standin.now()})
standin.log('cardsync.py', agent=agent, n=n)
time.sleep(float(os.environ.get('STANDIN_SECONDS') or 0))
wt = json.load(open(os.path.join(card, 'setup', 'status.json')))['worktree']
branch = json.load(open(os.path.join(o['--pages'], 'agents', agent, 'batches.json')))['0922']['base']
ok = subprocess.run(['git', '-C', wt, 'merge', '-q', '--ff-only', branch]).returncode == 0
standin.write(path, {'state': 'done' if ok else 'failed', 'pid': os.getpid(), 'started': standin.now(), 'ended': standin.now(), 'merged': ok,
                     'what': 'took batch 0922 in', **({} if ok else {'error': 'the stand-in could not fast-forward'})})
