"""Stand-in for sync.py: status done, nothing fetched."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import standin

(agent,), o = standin.args(sys.argv[1:])
standin.log('sync.py', agent=agent)
standin.write(os.path.join(o['--pages'], 'agents', agent, 'sync.status.json'), {'state': 'done', 'pid': os.getpid(), 'started': standin.now(), 'ended': standin.now(), 'seconds': 0, 'issues': 0})
