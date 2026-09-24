"""Stand-in for run.py: status working for $STANDIN_SECONDS, then done (failed when the step is in $STANDIN_FAIL,
stopped on SIGTERM), one ledger entry of $0.02; strategy and context record a stand-in step commit. No model, no card."""
import os, signal, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import standin, ledger, paths

(agent, n, step), o = standin.args(sys.argv[1:])
pages = o['--pages']
path = paths.status(paths.agent(pages, agent), n, step)
st = {'step': step, 'state': 'working', 'started': standin.now(), 'ended': None, 'seconds': None, 'commit': 'standin', 'model': o.get('--model'),
      'effort': o.get('--effort'), 'pid': os.getpid(), 'usage': None, 'live': None, 'error': None}
standin.write(path, st)
runs = paths.runs(paths.agent(pages, agent), n, step)
os.makedirs(runs, exist_ok=True)
open(os.path.join(runs, 'system.md'), 'w').write('Stand-in system prompt for ' + step)
open(os.path.join(runs, 'prompt.md'), 'w').write('Stand-in prompt for ' + step + ' of ' + n)
standin.log('run.py', step=step, n=n, agent=agent, cwd=os.getcwd(), feedback=o.get('--feedback'))


def end(state, error=None):
    if state == 'done' and step in ('strategy', 'context'):
        st['step_commit'] = {'hash': 'f' * 40, 'short': 'fffffff', 'subject': f'stand-in {step} for {n}', 'files': []}
    st.update(state=state, error=error, ended=standin.now(), seconds=1, usage={'in': 10, 'cached': 0, 'out': 5, 'reasoning': 0, 'commands': 1, 'cost': 0.02})
    standin.write(path, st)
    ledger.add(pages, agent, n, ledger.entry(st['ended'], step, st, st['usage']))
    sys.exit(0 if state == 'done' else 1)


signal.signal(signal.SIGTERM, lambda *a: end('failed', 'stopped from the page'))
time.sleep(float(os.environ.get('STANDIN_SECONDS') or 0.5))
end('failed', 'stand-in failure') if step in (os.environ.get('STANDIN_FAIL') or '').split(',') else end('done')
