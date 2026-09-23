"""Stand-in for batch.py create|delete: batches.json gains or loses the batch; status done."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import standin

(action, agent, batch), o = standin.args(sys.argv[1:])
base = os.path.join(o['--pages'], 'agents', agent)
standin.log('batch.py', action=action, batch=batch)
bj = os.path.join(base, 'batches.json')
data = json.load(open(bj)) if os.path.exists(bj) else {}
if action == 'create':
    data[batch] = {'base': o.get('--branch'), 'workspace': 'standin-' + batch, 'worktree': os.path.join(o['--repo'], '.claude', 'worktrees', batch)}
else:
    data.pop(batch, None)
standin.write(bj, data)
standin.write(os.path.join(base, 'batches', batch + '.status.json'), {'state': 'done', 'action': action, 'pid': os.getpid(), 'started': standin.now(), 'ended': standin.now()})
