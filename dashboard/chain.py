#!/usr/bin/env python3
"""A sequence: several steps of one issue, one after another, in a process of its own.

  chain.py <agent> <n> --steps setup,analysis,strategy,context,resolve [--model <id>] [--effort <level>] [--pages <dir>]
           [--feedback <text>]

Steps run in the order setup, analysis, strategy, context, resolve, whatever order --steps names them in; each starts
when the one before is done, and a step that fails, is stopped or cannot start ends the sequence there. The
resolution, when chosen, is last and starts with the skill text: its session host outlives this process. State in
agents/<agent>/chain/<n>.json: steps, at, state (working, done, failed, stopped), error, pid. The file
agents/<agent>/chain/<n>.stop ends the sequence after the current step. --feedback goes to the first step; when a
sequence started with it ends, the issue's live resolution session, if any, is told which steps reran and their new
commits (steps.notify_rerun), "notified" in the state file."""
import os, sys, time

import steps
from steps import ORDER, now, write_json, settle, status_path


def main(argv):
    opts = {argv[k]: argv[k + 1] for k in range(len(argv) - 1) if argv[k].startswith('--')}
    args = [a for k, a in enumerate(argv) if not a.startswith('--') and not (k and argv[k - 1].startswith('--'))]
    if len(args) != 2 or not opts.get('--steps'):
        sys.exit(__doc__)
    agent, n = args
    os.chdir(os.path.abspath(opts.get('--pages') or os.path.dirname(os.path.abspath(__file__))))
    chosen = opts['--steps'].split(',')
    path, stop = steps.chain_path(agent, n), steps.chain_path(agent, n)[:-5] + '.stop'
    state = {'steps': [x for x in ORDER if x in chosen], 'at': None, 'state': 'working', 'started': now(), 'error': None, 'pid': os.getpid()}
    write_json(path, state)
    feedback, ran = opts.get('--feedback'), []
    for step in state['steps']:
        if os.path.exists(stop):
            state.update(state='stopped', error='stopped from the page'); break
        state['at'] = step; write_json(path, state)
        err = steps.start_step(agent, n, step, opts.get('--model'), opts.get('--effort'), ask=True, feedback=None if ran else feedback)
        if err:
            state.update(state='failed', error=step + ': ' + err); break
        ran.append(step)
        if step == 'resolve':
            continue
        sp = status_path(agent, n, step)
        while True:
            time.sleep(float(os.environ.get('CHAIN_POLL') or 3))
            p = steps.RUNNING.get(sp)
            if (p is None or p.poll() is not None) and settle(sp).get('state') != 'working':
                break
        st = settle(sp)
        if st.get('state') != 'done':
            stopped = (st.get('error') or '').startswith('stopped')
            state.update(state='stopped' if stopped else 'failed', error=step + ': ' + (st.get('error') or st.get('state') or 'no status')); break
    else:
        state['state'] = 'done'
    if os.path.exists(stop):
        os.remove(stop)
    prep = [x for x in ran if x in steps.PREP]
    if feedback and prep:
        state['notified'] = 'error' not in steps.notify_rerun(agent, n, prep)
    state.update(ended=now()); write_json(path, state)


if __name__ == '__main__':
    main(sys.argv[1:])
