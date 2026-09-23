"""Checks of the staging run.py and stepgit.py, the real scripts, on a made-up issue 900 in a throwaway git worktree,
with the stand-in pi (json mode), a stand-in sierra CLI, the stand-in brief and a card.py that renders nothing:
steps leaving git alone, a rerun on the tree as it is, context refused on a wrong binding, main's changes a pull brings
committed as base, --feedback continuing the kept session or running fresh, the schema retry on both paths, the context brief's
lane section, and the card's history: each run, stage entry and pull as an event whose files stay, the briefs' index. python3 -m unittest test_steps (from test/), or run.sh."""
import json, os, shutil, subprocess, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab

AG, N, WS = 'hipotecarios', '900', 'https://studio.example.invalid/workspace/hip-900'
SCRIPTS = lab.TOOLKIT
BLOCK = 'agents/hipotecarios/.composer/blocks/b.json'
LOCK = 'agents/hipotecarios/.composer/pnpm-lock.yaml'
SIM = 'agents/hipotecarios/simulations/s.tests.ts'
SIERRA = '''#!/usr/bin/env python3
import json, os, sys, time
open(os.environ['STANDIN_LOG'], 'a').write(json.dumps({'who': 'sierra', 'args': sys.argv[1:], 't': time.time()}) + '\\n')
if sys.argv[-1] == 'pull':  # a pull brings the workspace's content over the tree; the sequence restores it after
    open(os.path.join(sys.argv[2], '.composer', 'blocks', 'b.json'), 'w').write('{"from": "the workspace"}')
if os.environ.get('STANDIN_SIERRA_FAIL') == sys.argv[-1]:
    sys.exit('stand-in ' + sys.argv[-1] + ' failed')
'''


@unittest.skipUnless(lab.RERUNS, 'the scripts have no stepgit.py')
class Steps(unittest.TestCase):
    def setUp(self):
        self.run_dir = os.path.join(HERE, 'run-steps')
        shutil.rmtree(self.run_dir, ignore_errors=True)
        self.env = lab.make(self.run_dir)
        scripts = os.path.join(self.run_dir, 'real-scripts')
        shutil.copytree(SCRIPTS, scripts, ignore=shutil.ignore_patterns('__pycache__'))
        os.rename(os.path.join(scripts, 'brief.py'), os.path.join(scripts, 'brief_real.py'))
        for f in ('brief.py', 'standin.py'):
            shutil.copy(os.path.join(HERE, 'standins', 'scripts', f), os.path.join(scripts, f))
        open(os.path.join(scripts, 'card.py'), 'w').write('import sys\nif __name__ == "__main__":\n    sys.exit(0)\n')
        self.scripts = scripts
        self.wt = os.path.join(self.run_dir, 'repo', '.claude', 'worktrees', 'hip-' + N)
        fork = lab.git_repo(self.wt, {BLOCK: '{"v": 1}\n', LOCK: 'lock 1\n', SIM: 'sim 1\n', '.gitignore': 'node_modules/\n.composer/build/\n'})
        self.fork = fork
        agent_dir = os.path.join(self.wt, 'agents', 'hipotecarios')
        os.makedirs(os.path.join(agent_dir, 'node_modules', '.bin'))
        sierra = os.path.join(agent_dir, 'node_modules', '.bin', 'sierra')
        open(sierra, 'w').write(SIERRA)
        os.chmod(sierra, 0o755)
        self.bind(WS)
        base = os.path.join(self.run_dir, 'agents', AG)
        json.dump({'issue': {'number': int(N), 'name': 'Made-up issue', 'status': 'OPEN'}, 'linkedLogs': []}, open(os.path.join(base, 'issues', N + '.json'), 'w'))
        os.makedirs(os.path.join(base, 'analysis'), exist_ok=True)
        json.dump({'ok': True}, open(os.path.join(base, 'analysis', N + '.json'), 'w'))
        json.dump({'state': 'done', 'worktree': self.wt, 'workspace': WS, 'name': 'hip-' + N, 'commit': fork},
                  open(os.path.join(base, 'setup', N + '.status.json'), 'w'))

    def tearDown(self):
        shutil.rmtree(self.run_dir, ignore_errors=True)

    def bind(self, url):
        d = os.path.join(self.wt, 'agents', 'hipotecarios', '.composer', 'build')
        os.makedirs(d, exist_ok=True)
        json.dump({'targetUrl': url}, open(os.path.join(d, 'workspace-meta.json'), 'w'))

    def run_step(self, step, edits=(), replies=None, feedback=None, **env):
        e = dict(self.env, STANDIN_EDITS=json.dumps(list(edits)), **env)
        if replies:
            e['STANDIN_REPLIES'] = json.dumps(replies)
        argv = [sys.executable, os.path.join(self.scripts, 'run.py'), AG, N, step, '--pages', self.run_dir, '--repo', self.wt]
        subprocess.run(argv + (['--feedback', feedback] if feedback else []), env=e, cwd=self.wt, capture_output=True, timeout=60)
        return self.status(step)

    def status(self, step):
        return json.load(open(os.path.join(self.run_dir, 'agents', AG, step, N + '.status.json')))

    def git(self, *a):
        return subprocess.run(['git', '-C', self.wt] + list(a), capture_output=True, text=True, env=self.env).stdout.strip()

    def log(self, who):
        try:
            rows = [json.loads(l) for l in open(self.env['STANDIN_LOG'])]
        except OSError:
            return []
        return [r for r in rows if r.get('who') == who]

    def pi_calls(self):
        return [r for r in self.log('pi') if r.get('mode') == 'json']

    def changes(self):
        return sorted(l.strip() for l in self.git('status', '--porcelain').splitlines() if '/build/' not in l)

    def test_steps_leave_git_alone(self):
        self.assertEqual(self.run_step('analysis')['state'], 'done')
        st = self.run_step('strategy', [[SIM, 'sim 2\n'], ['agents/hipotecarios/simulations/new.tests.ts', 'guard\n']])
        self.assertEqual(st['state'], 'done', st.get('error'))
        st = self.run_step('context', [[BLOCK, '{"v": 2}\n']])
        self.assertEqual(st['state'], 'done', st.get('error'))
        self.assertEqual(self.git('rev-parse', '--short', 'HEAD'), self.fork)
        self.assertEqual(self.changes(), ['?? agents/hipotecarios/simulations/new.tests.ts', 'M ' + BLOCK, 'M ' + SIM])
        self.assertNotIn('step_commit', st)
        self.assertEqual(self.log('sierra'), [])

    def test_rerun_works_on_the_tree_as_it_is(self):
        self.run_step('strategy', [[SIM, 'sim 2\n']])
        self.run_step('context', [[BLOCK, '{"v": 2}\n']])
        st = self.run_step('strategy', [[SIM, 'sim 3\n']])
        self.assertEqual(st['state'], 'done', st.get('error'))
        self.assertEqual(open(os.path.join(self.wt, BLOCK)).read(), '{"v": 2}\n')
        self.assertEqual(open(os.path.join(self.wt, SIM)).read(), 'sim 3\n')
        self.assertEqual(self.git('rev-parse', '--short', 'HEAD'), self.fork)

    def test_context_needs_the_issue_binding(self):
        self.bind('https://studio.example.invalid/workspace/batch-0922')
        st = self.run_step('context')
        self.assertEqual(st['state'], 'failed')
        self.assertIn('not the issue workspace ' + WS, st['error'])
        self.assertEqual(self.run_step('strategy')['state'], 'done')

    def test_pull_takes_main_as_base(self):
        self.git('checkout', '-q', '-b', 'side')
        open(os.path.join(self.wt, BLOCK), 'w').write('{"v": 5}\n')
        self.git('commit', '-q', '-am', 'Main moved')
        self.git('update-ref', 'refs/remotes/origin/main', 'HEAD')
        self.git('checkout', '-q', '-')
        open(os.path.join(self.wt, BLOCK), 'w').write('{"v": 5}\n')
        open(os.path.join(self.wt, 'agents/hipotecarios/.composer/blocks/c.json'), 'w').write('{"card": 1}\n')
        open(os.path.join(self.wt, SIM), 'w').write('sim 2\n')
        out = subprocess.run([sys.executable, '-c', 'import sys, stepgit; print(stepgit.absorb_main(sys.argv[1], sys.argv[2]))',
                              self.wt, 'agents/hipotecarios/.composer'], cwd=self.scripts, env=self.env, capture_output=True, text=True)
        self.assertEqual(out.stdout.strip(), repr([BLOCK]), out.stderr)
        self.assertEqual(self.git('log', '-1', '--format=%s'), "Main's changes that reached the workspace")
        self.assertEqual(self.changes(), ['?? agents/hipotecarios/.composer/blocks/c.json', 'M ' + SIM])

    def test_feedback_continues_the_session(self):
        self.run_step('strategy', [[SIM, 'sim 2\n']])
        st = self.run_step('strategy', [[SIM, 'sim 3\n']], feedback='The guard misses the second question.')
        self.assertEqual((st['state'], st['continued'], st['feedback']), ('done', True, True), st.get('error'))
        call = self.pi_calls()[-1]
        self.assertTrue(call['cont'])
        self.assertIn('The guard misses the second question.', call['stdin'])
        self.assertIn("holds the card's work so far, uncommitted", call['stdin'])
        runs = os.path.join(self.run_dir, 'agents', AG, 'strategy', 'runs', N)
        self.assertEqual(open(os.path.join(runs, 'feedback.md')).read(), 'The guard misses the second question.\n')
        self.assertTrue(open(os.path.join(runs, 'prompt.md')).read().startswith('Feedback from the engineer'))
        self.assertTrue(os.path.exists(os.path.join(runs, 'system.md')))
        self.assertEqual([d for d in os.listdir(runs) if d.startswith('session')], ['session'])

    def test_feedback_without_a_session_runs_fresh(self):
        st = self.run_step('strategy', feedback='Name the second question.')
        self.assertEqual((st['state'], st['continued']), ('done', False))
        call = self.pi_calls()[-1]
        self.assertFalse(call['cont'])
        self.assertIn('Stand-in sim-strategy instructions.', call['stdin'])
        self.assertIn('# Feedback from the engineer on the previous run\n\nName the second question.', call['stdin'])

    def test_fresh_run_moves_the_session_aside(self):
        self.run_step('strategy')
        self.run_step('strategy')
        runs = os.path.join(self.run_dir, 'agents', AG, 'strategy', 'runs', N)
        kept = sorted(d for d in os.listdir(runs) if d.startswith('session'))
        self.assertEqual(len(kept), 2)
        self.assertEqual(kept[0], 'session')
        self.assertFalse(any(c['cont'] for c in self.pi_calls()))

    def test_schema_retry_on_both_paths(self):
        st = self.run_step('strategy', replies=['not json', '{"ok": true}'])
        self.assertEqual(st['state'], 'done', st.get('error'))
        self.assertEqual([c['cont'] for c in self.pi_calls()], [False, True])
        self.assertIn('Your reply was not the JSON object', self.pi_calls()[1]['message'])
        st = self.run_step('strategy', replies=['{"ok": "no"}', '{"ok": true}'], feedback='Again.')
        self.assertEqual((st['state'], st['continued']), ('done', True), st.get('error'))
        calls = self.pi_calls()[2:]
        self.assertEqual([c['cont'] for c in calls], [True, True])
        self.assertIn('$.ok: expected boolean', calls[1]['message'])

    def history(self):
        return [json.loads(l) for l in open(os.path.join(self.run_dir, 'agents', AG, 'log', N + '.jsonl'))]

    def test_each_run_is_an_event_with_its_own_files(self):
        self.run_step('strategy', replies=['{"ok": true, "n": 1}'])
        self.run_step('strategy', replies=['{"ok": true, "n": 2}'], feedback='The guard misses the second question.')
        self.bind('https://studio.example.invalid/workspace/batch-0922')
        self.run_step('context')
        ev = self.history()
        self.assertEqual([e['who'] for e in ev], ['strategy', 'strategy', 'context'])
        self.assertIn("rerun on the engineer's feedback («The guard misses the second question.»)", ev[1]['what'])
        self.assertTrue(ev[2]['what'].startswith('failed: '), ev[2]['what'])
        base = os.path.join(self.run_dir, 'agents', AG)
        answers = [json.load(open(os.path.join(base, next(r for r in e['refs'] if r.endswith('answer.json'))))) for e in ev[:2]]
        self.assertEqual([a['n'] for a in answers], [1, 2])
        self.assertTrue(any(r.endswith('feedback.md') for r in ev[1]['refs']))
        self.assertFalse(any(r.endswith('feedback.md') for r in ev[0]['refs']))
        for r in sum((e['refs'] for e in ev), []):
            self.assertTrue(os.path.exists(os.path.join(base, r)), r)
        sys.path.insert(0, self.scripts)
        import cardlog
        lines = cardlog.index(self.run_dir, AG, N).splitlines()
        self.assertIn('superseded', lines[-3])
        self.assertNotIn('superseded', lines[-2])

    def test_stage_and_pull_are_events(self):
        stage = [sys.executable, os.path.join(self.scripts, 'stage.py'), AG, N]
        subprocess.run(stage + ['review', 'wrong', '--step', 'strategy', '--note', 'guard misses it', '--by', 'engineer', '--pages', self.run_dir], check=True, capture_output=True)
        self.git('checkout', '-q', '-b', 'side')
        open(os.path.join(self.wt, BLOCK), 'w').write('{"from": "the workspace"}')
        self.git('commit', '-q', '-am', 'Main moved')
        self.git('update-ref', 'refs/remotes/origin/main', 'HEAD')
        self.git('checkout', '-q', '-')
        out = subprocess.run([sys.executable, os.path.join(self.scripts, 'pull.py'), AG, self.wt], capture_output=True, text=True,
                             env=dict(self.env, BBVA_ISSUES_DIR=self.run_dir))
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        ev = self.history()
        self.assertEqual([(e['who'], e['what']) for e in ev], [('engineer', 'review wrong (strategy): guard misses it'),
                                                             ('pull', "took main's changes as base: b.json")])
        self.assertEqual(ev[1]['refs'], ['git:' + self.git('rev-parse', '--short', 'HEAD')])
        stages = json.load(open(os.path.join(self.run_dir, 'agents', AG, 'resolve', N + '.stage.json')))
        self.assertEqual(stages[-1]['t'], ev[0]['t'])

    def test_briefs_end_with_the_history(self):
        sys.path.insert(0, self.scripts)
        import cardlog
        for k in range(35):
            cardlog.add(self.run_dir, AG, N, 'engineer' if k % 2 else 'strategy', f'event {k}', [f'strategy/runs/{N}/x{k}/answer.json'])
        os.makedirs(os.path.join(self.wt, 'agents', 'hipotecarios', '.composer', 'blocks'), exist_ok=True)
        out = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'brief.py'), AG, N, '--step', 'context', '--pages', self.run_dir, '--repo', self.wt],
                             capture_output=True, text=True, env=self.env)
        self.assertEqual(out.returncode, 0, out.stderr)
        hist = out.stdout[out.stdout.index('# Card history · hipotecarios 900'):].splitlines()
        self.assertTrue(hist[4].startswith('earlier: strategy ×3, engineer ×2'), hist[4])
        self.assertEqual(len([l for l in hist if ' event ' in l and not l.startswith('earlier')]), 30)
        self.assertTrue(hist[-1].endswith(f'event 34 → strategy/runs/{N}/x34/answer.json'), hist[-1])

    def test_context_brief_carries_the_lane(self):
        os.makedirs(os.path.join(self.wt, 'agents', 'hipotecarios', '.composer', 'blocks'), exist_ok=True)
        out = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'brief.py'), AG, N, '--step', 'context', '--pages', self.run_dir, '--repo', self.wt],
                             capture_output=True, text=True, env=self.env)
        self.assertEqual(out.returncode, 0, out.stderr)
        lane = out.stdout[out.stdout.index('# Lane · hipotecarios 900'):]
        self.assertIn(f'- `<runs>`: `{os.path.join(self.run_dir, "agents", AG, "context", "runs", N)}`', lane)
        self.assertIn('- `<workspace>`: `hip-900`', lane)
        self.assertIn(f'- `<checkout>`: `{self.wt}`', lane)


class Disputes(unittest.TestCase):
    """A rerun step weighing feedback: run.py's check on its answer, the rerun note with the disputed points, the open
    disagreement and the engineer's ruling recorded."""
    def setUp(self):
        self.old, self.dir = os.getcwd(), os.path.join(HERE, 'run-disputes')
        shutil.rmtree(self.dir, ignore_errors=True)
        for d in ('resolve', 'strategy'):
            os.makedirs(os.path.join(self.dir, 'agents', AG, d))
        os.chdir(self.dir)
        sys.path.insert(0, os.path.dirname(HERE))
        import steps
        self.steps = steps
        self.fb = {'verdict': 'partly', 'points': [
            {'claim': 'Move the edit to item 2.', 'verdict': 'accepted', 'why': 'It decides the turn.', 'basis': None},
            {'claim': 'Re-ask the seller question.', 'verdict': 'disputed', 'why': 'She had answered it.', 'basis': '«retomá la pregunta pendiente»'}]}
        json.dump({'ok': True, 'feedback': self.fb}, open(os.path.join('agents', AG, 'strategy', N + '.json'), 'w'))

    def tearDown(self):
        os.chdir(self.old)
        shutil.rmtree(self.dir, ignore_errors=True)

    def stage(self, *entries):
        json.dump([dict(t='2026-09-23T10:0%dZ' % k, stage='review', step='strategy', **e) for k, e in enumerate(entries)],
                  open(os.path.join('agents', AG, 'resolve', N + '.stage.json'), 'w'))

    def test_run_checks_the_feedback_field(self):
        sys.path.insert(0, SCRIPTS)
        import run
        self.assertTrue(run.feedback_errors({'feedback': None}, 'Fix it.', 'resolver'))
        self.assertTrue(run.feedback_errors({'feedback': self.fb}, '', None))
        self.assertTrue(run.feedback_errors({'feedback': self.fb}, 'Fix it.', 'ruling'))
        self.assertEqual(run.feedback_errors({'feedback': self.fb}, 'Fix it.', 'resolver'), [])

    def test_rerun_note_lists_the_disputed_points(self):
        note = self.steps.rerun_note(AG, N, ['strategy'])
        self.assertIn('strategy answered the feedback: partly.', note)
        self.assertIn('disputed · Re-ask the seller question.', note)
        self.assertIn('basis: «retomá la pregunta pendiente»', note)
        self.assertIn('concede it, or hold it with review contested', note)

    def test_ruling_closes_the_disagreement(self):
        self.stage(dict(state='wrong', note='Re-ask it.'))
        self.assertEqual(self.steps.contest(AG, N), {})
        self.assertEqual(self.steps.rule(AG, N, 'step'), (None, 'no open disagreement'))
        self.stage(dict(state='wrong', note='Re-ask it.'), dict(state='contested', note='She never answered: turn 41.'))
        c = self.steps.contest(AG, N)
        self.assertEqual((c['step'], c['held'], [p['claim'] for p in c['disputed']]),
                         ('strategy', 'She never answered: turn 41.', ['Re-ask the seller question.']))
        out, err = self.steps.rule(AG, N, 'step', gap=True)
        self.assertIsNone(err)
        log = json.load(open(os.path.join('agents', AG, 'resolve', N + '.stage.json')))
        self.assertEqual((log[-1]['state'], log[-1]['step'], log[-1]['note']), ('ruled', 'strategy', 'for strategy; skill gap'))
        gaps = json.load(open(os.path.join('agents', AG, 'skill-gaps.json')))
        self.assertEqual((gaps[0]['n'], gaps[0]['for']), (N, 'step'))
        self.assertEqual(self.steps.contest(AG, N), {})


if __name__ == '__main__':
    unittest.main()
