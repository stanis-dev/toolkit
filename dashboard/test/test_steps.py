"""Checks of the staging run.py and stepgit.py, the real scripts, on a made-up issue 900 in a throwaway git worktree,
with the stand-in pi (json mode), a stand-in sierra CLI, the stand-in brief and a card.py that renders nothing:
the commit per step, the rewind per step and its refusals, the workspace push only when Studio content changed,
--feedback continuing the kept session or running fresh, the schema retry on both paths, and the context brief's
lane section. python3 -m unittest test_steps (from test/), or run.sh."""
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

    def subjects(self):
        return self.git('log', '--format=%s|%(trailers:key=Step,valueonly,separator=)', '--reverse', self.fork + '..HEAD').splitlines()

    def test_commit_per_step(self):
        self.assertEqual(self.run_step('analysis')['state'], 'done')
        st = self.run_step('strategy', [[SIM, 'sim 2\n'], ['agents/hipotecarios/simulations/new.tests.ts', 'guard\n'], [LOCK, 'lock 2\n']])
        self.assertEqual(st['state'], 'done', st.get('error'))
        self.assertEqual(sorted(st['step_commit']['files']), ['agents/hipotecarios/simulations/new.tests.ts', SIM])
        self.assertEqual(self.git('status', '--porcelain', '--untracked-files=no'), 'M ' + LOCK)
        st = self.run_step('context', [[BLOCK, '{"v": 2}\n']])
        self.assertEqual(st['step_commit']['files'], [BLOCK])
        self.assertEqual(self.subjects(), ['Sim strategy for hip-900|strategy 900', 'Context edit for hip-900|context 900'])
        self.assertNotIn('Co-Authored', self.git('log', '-2', '--format=%B'))
        self.assertIsNone(self.status('analysis')['step_commit'])

    def test_no_change_no_commit(self):
        st = self.run_step('strategy')
        self.assertEqual((st['state'], st['step_commit']), ('done', None))
        self.assertEqual(self.subjects(), [])

    def test_rewind_per_step(self):
        self.run_step('strategy', [[SIM, 'sim 2\n']])
        self.run_step('context', [[BLOCK, '{"v": 2}\n']])
        open(os.path.join(self.wt, 'fix.txt'), 'w').write('resolution work\n')
        self.git('add', 'fix.txt'); self.git('commit', '-q', '-m', 'Resolution fix')
        st = self.run_step('context', [[BLOCK, '{"v": 3}\n']])
        self.assertEqual([d['subject'] for d in st['rewind']['dropped']], ['Resolution fix', 'Context edit for hip-900'])
        self.assertTrue(st['rewind']['pushed'])
        self.assertEqual(self.subjects(), ['Sim strategy for hip-900|strategy 900', 'Context edit for hip-900|context 900'])
        self.assertFalse(os.path.exists(os.path.join(self.wt, 'fix.txt')))
        before = len(self.log('sierra'))
        st = self.run_step('strategy', [[SIM, 'sim 3\n']])
        self.assertEqual([d['step'] for d in st['rewind']['dropped']], ['context', 'strategy'])
        self.assertEqual(self.subjects(), ['Sim strategy for hip-900|strategy 900'])
        self.assertEqual([r['args'][-1] for r in self.log('sierra')[before:]], ['pull', 'lint', 'push', 'pull'])
        self.assertEqual(open(os.path.join(self.wt, BLOCK)).read(), '{"v": 1}\n')
        self.assertEqual(self.git('status', '--porcelain', '--untracked-files=no'), '')
        st = self.run_step('analysis')
        self.assertEqual([d['step'] for d in st['rewind']['dropped']], ['strategy'])
        self.assertEqual(self.git('rev-parse', '--short', 'HEAD'), self.fork)
        self.assertIsNone(self.run_step('analysis')['rewind'])

    def test_push_only_when_studio_content_changed(self):
        self.run_step('strategy', [[SIM, 'sim 2\n']])
        st = self.run_step('strategy', [[SIM, 'sim 3\n']])
        self.assertEqual((len(st['rewind']['dropped']), st['rewind']['push'], st['rewind']['pushed']), (1, False, False))
        self.assertEqual(self.log('sierra'), [])
        self.run_step('strategy', [[SIM, 'sim 4\n'], [BLOCK, '{"v": 9}\n']])
        st = self.run_step('strategy')
        self.assertTrue(st['rewind']['pushed'])
        self.assertEqual(len(self.log('sierra')), 4)

    def test_refusals(self):
        self.run_step('strategy', [[SIM, 'sim 2\n']])
        head = self.git('rev-parse', 'HEAD')
        open(os.path.join(self.wt, SIM), 'w').write('work in progress\n')
        st = self.run_step('strategy')
        self.assertEqual(st['state'], 'failed')
        self.assertIn('uncommitted changes: ' + SIM, st['error'])
        self.assertEqual(self.git('rev-parse', 'HEAD'), head)
        self.git('checkout', '--', SIM)
        open(os.path.join(self.wt, LOCK), 'w').write('lock 3\n')
        self.run_step('context', [[BLOCK, '{"v": 2}\n']])
        self.bind('https://studio.example.invalid/workspace/batch-0922')
        head = self.git('rev-parse', 'HEAD')
        st = self.run_step('context')
        self.assertEqual(st['state'], 'failed')
        self.assertIn('not the issue workspace ' + WS, st['error'])
        self.assertEqual(self.git('rev-parse', 'HEAD'), head)
        self.bind(WS)
        st = self.run_step('context', STANDIN_SIERRA_FAIL='lint')
        self.assertIn('rewound, but the workspace push failed: ghostwriter lint failed', st['error'])

    def test_feedback_continues_the_session(self):
        self.run_step('strategy', [[SIM, 'sim 2\n']])
        st = self.run_step('strategy', [[SIM, 'sim 3\n']], feedback='The guard misses the second question.')
        self.assertEqual((st['state'], st['continued'], st['feedback']), ('done', True, True), st.get('error'))
        call = self.pi_calls()[-1]
        self.assertTrue(call['cont'])
        self.assertIn('The guard misses the second question.', call['stdin'])
        self.assertIn('rewound to where this step started: ', call['stdin'])
        self.assertIn('Sim strategy for hip-900 dropped', call['stdin'])
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
        self.assertIn('# Feedback on the previous run\n\nName the second question.', call['stdin'])

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

    def test_context_brief_carries_the_lane(self):
        os.makedirs(os.path.join(self.wt, 'agents', 'hipotecarios', '.composer', 'blocks'), exist_ok=True)
        out = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'brief.py'), AG, N, '--step', 'context', '--pages', self.run_dir, '--repo', self.wt],
                             capture_output=True, text=True, env=self.env)
        self.assertEqual(out.returncode, 0, out.stderr)
        lane = out.stdout[out.stdout.index('# Lane · hipotecarios 900'):]
        self.assertIn(f'- `<runs>`: `{os.path.join(self.run_dir, "agents", AG, "context", "runs", N)}`', lane)
        self.assertIn('- `<workspace>`: `hip-900`', lane)
        self.assertIn(f'- `<checkout>`: `{self.wt}`', lane)


if __name__ == '__main__':
    unittest.main()
