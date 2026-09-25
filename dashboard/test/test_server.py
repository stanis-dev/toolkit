"""Checks of the server, the session host and the sequence runner over a lab copy of a few issues, with stand-ins for
run.py, setup.py and pi. python3 -m unittest test_server (from test/), or run.sh for these and the browser checks."""
import importlib.util, json, os, socket, subprocess, sys, threading, time, unittest, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab
sys.path.insert(0, lab.TOOLKIT)
import paths  # noqa: E402

PORT = 8491
BASE = f'http://127.0.0.1:{PORT}'
AG = 'hipotecarios'
B = paths.agent('', AG)


def get(path, headers=None):
    r = urllib.request.urlopen(urllib.request.Request(BASE + path, headers=headers or {}), timeout=10)
    return json.loads(r.read() or b'null')


def post(path, body=None):
    req = urllib.request.Request(BASE + path, data=json.dumps(body or {}).encode(), headers={'Content-Type': 'application/json'}, method='POST')
    try:
        r = urllib.request.urlopen(req, timeout=70)
        data = r.read()
        return r.status, json.loads(data) if data else None
    except urllib.error.HTTPError as ex:
        text = ex.read().decode()
        try:
            return ex.code, json.loads(text)
        except ValueError:
            return ex.code, {'error': text}


def until(fn, timeout=10, step=0.1):
    t0 = time.time()
    while time.time() - t0 < timeout:
        v = fn()
        if v:
            return v
        time.sleep(step)
    raise AssertionError('timed out waiting')


class Lab(unittest.TestCase):
    """One lab dir and one server per test class."""
    name, extra = 'unit', {}

    @classmethod
    def setUpClass(cls):
        cls.run_dir = os.path.join(HERE, 'run-' + cls.name)
        cls.env = dict(lab.make(cls.run_dir), **cls.extra)
        cls.server = lab.serve(cls.run_dir, cls.env, PORT)

    @classmethod
    def tearDownClass(cls):
        lab.stop_all(cls.run_dir)
        cls.server.wait()

    def path(self, *p):
        return os.path.join(self.run_dir, *p)

    def load(self, *p):
        with open(self.path(*p)) as f:
            return json.load(f)

    def standin_log(self, who=None):
        try:
            rows = [json.loads(l) for l in open(self.path('standin.log'))]
        except OSError:
            return []
        return [r for r in rows if not who or r['who'] == who]

    def write(self, rel, obj):
        p = self.path(rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w') as f:
            json.dump(obj, f)

    def module(self, name):
        spec = importlib.util.spec_from_file_location(name + '_under_test', self.path(name + '.py'))
        m = importlib.util.module_from_spec(spec)
        old, cwd = dict(os.environ), os.getcwd()
        os.environ.update(self.env)
        try:
            spec.loader.exec_module(m)
        finally:
            os.environ.clear(); os.environ.update(old)
        os.chdir(cwd)
        return m


class StepStates(Lab):
    name = 'states'

    def test_stopped_versus_failed(self):
        a = f'agents/{AG}'
        self.write(paths.step_file(a, '900', 'analysis', 'status.json'), {'state': 'failed', 'error': 'stopped from the page', 'pid': 0})
        self.write(paths.step_file(a, '900', 'strategy', 'status.json'), {'state': 'failed', 'error': 'pi exit 1', 'pid': 0})
        self.write(paths.step_file(a, '900', 'resolve', 'status.json'), {'state': 'failed', 'error': 'process gone', 'pid': 0})
        self.write(paths.step_file(a, '900', 'context', 'status.json'), {'state': 'working', 'pid': 999999})
        self.write(paths.step_file(a, '901', 'resolve', 'status.json'), {'state': 'working', 'pid': 999999})
        self.write(paths.step_file(a, '901', 'analysis', 'json'), {})
        s = get('/steps/' + AG)['steps']
        self.assertEqual(s['900'], {'analysis': 'stopped', 'strategy': 'failed', 'resolve': 'stopped', 'context': 'failed'})
        self.assertEqual(s['901'], {'resolve': 'stopped', 'analysis': 'done'})
        st = self.load(paths.step_file(a, '900', 'context', 'status.json'))
        self.assertEqual((st['state'], st['error']), ('failed', 'process gone'))
        self.assertEqual(s['304']['setup'], 'done')


class SimCards(Lab):
    """A card opened from one failing replay reads as an issue card does: listed with the issues, its replay served as
    a conversation, the request at one of its turns."""
    name = 'simcards'

    def test_replay_card(self):
        sims = self.path('sims', 'replaytestrunset-X', 'results', 'replaytestresult-X')
        os.makedirs(os.path.join(sims, 'traces'))
        with open(os.path.join(sims, 'debug.log'), 'w') as f:
            f.write('seq,timestamp,event_type,message\n1,t,AGENT_MSG,Hola.\n2,t,USER_MSG,No soy yo.\n'
                    '3,t,GOALSDK_RESPOND,Tool calls: EndCall\n4,t,AGENT_LOG,[INFO] Invoking tool: EndCall {}\n'
                    '5,t,AGENT_MSG,Disculpá la molestia.\n6,t,TOOL_CALL,EndCall\n')
        json.dump({'id': 'replaytestresult-X', 'replayTestId': 'replaytestmeta-Y', 'runSetId': 'replaytestrunset-X', 'status': 'FAILED',
                   'tags': ['tool:end-call'], 'tagExpectations': {'present': ['resultado:no-reconoce'], 'absent': []},
                   'outcomeEvalResults': [{'expectedOutcome': 'Se despide.', 'metExpectation': False, 'reasoning': 'No se despidió.'}]},
                  open(os.path.join(sims, 'result.json'), 'w'))
        json.dump({'traces': [{'llm_chat': {'raw_request': {'model': 'm', 'messages': [{'role': 'system', 'content': 'Sé breve.'}], 'tools': []}}}]},
                  open(os.path.join(sims, 'traces', '3.trace'), 'w'))
        with open(self.path('sims', 'test-names.json'), 'w') as f:
            json.dump({'replaytestmeta-Y': 'No reconoce al titular'}, f)
        out = subprocess.run([sys.executable, os.path.join(lab.TOOLKIT, 'simcard.py'), AG, sims, '--pages', self.run_dir],
                             capture_output=True, text=True, check=True).stdout.strip()
        self.assertEqual(out, '10001')
        src = get(f'/sources/{AG}')['10001']
        self.assertEqual((src['kind'], src['title'], src['conversations'][0]['id']), ('sim', 'No reconoce al titular', 'replaytestresult-X'))
        self.assertIn('Missing tags: resultado:no-reconoce', src['description'])
        rows = get(f'/call/{AG}/10001/replaytestresult-X')['rows']
        self.assertEqual([(r.get('turn'), r.get('text')) for r in rows if r.get('role')], [('1', 'Hola.'), ('2', 'No soy yo.'), ('5', 'Disculpá la molestia.')])
        self.assertEqual(rows[-1]['tools'], [{'name': 'EndCall', 'args': '{}'}])
        req = get(f'/request/{AG}/10001/replaytestresult-X/5')
        self.assertEqual((req['error'], req['turn'], req['trace'], req['system'][0]['text']), (None, '5', '3', 'Sé breve.'))
        files = [f['path'] for f in get(f'/files/{AG}/10001')]
        self.assertIn('cards/10001/conversations/replaytestresult-X/debug.log', files)


class Sequences(Lab):
    name = 'chain'
    extra = {'STANDIN_SECONDS': '0.6'}

    def chain(self, n):
        return get('/steps/' + AG)['chains'].get(n) or {}

    def wait_chain(self, n):
        return until(lambda: self.chain(n).get('state') != 'working' and self.chain(n), timeout=20)

    def test_order_and_resolution_last(self):
        code, st = post(f'/chain/{AG}/304', {'steps': ['context', 'resolve', 'analysis'], 'model': 'gpt-5.6-terra', 'effort': 'low'})
        self.assertEqual(code, 202)
        self.assertEqual(st['steps'], ['analysis', 'context', 'resolve'])
        self.assertEqual(post(f'/chain/{AG}/304', {'steps': ['analysis']})[0], 409)
        done = self.wait_chain('304')
        self.assertEqual((done['state'], done['at'], done['error']), ('done', 'resolve', None))
        self.assertEqual([r['step'] for r in self.standin_log('run.py') if r['n'] == '304'], ['analysis', 'context'])
        state = get(f'/chat/{AG}/304/state')
        self.assertTrue(state['running'])
        self.assertTrue(state['status']['asked'])
        self.assertIn('Stand-in resolution instructions', open(self.path(paths.runs(B, '304', 'resolve'), 'brief.md')).read())
        post(f'/chat/{AG}/304/stop')
        until(lambda: not get(f'/chat/{AG}/304/state')['running'])

    def test_refusals(self):
        self.assertEqual(post(f'/chain/{AG}/302/stop')[0], 409)
        self.assertEqual(post(f'/chain/{AG}/302', {'steps': []})[0], 400)
        post(f'/chain/{AG}/302', {'steps': ['setup', 'analysis']})
        self.assertEqual(self.wait_chain('302')['error'], 'setup: no batch: put the card in a batch first')
        self.assertEqual(post(f'/chain/{AG}/303', {'steps': ['analysis']}), (409, {'error': 'not set up yet: add setup to the steps'}))

    def test_keep_alive_after_a_body_the_route_ignores(self):
        import http.client
        c = http.client.HTTPConnection('127.0.0.1', PORT, timeout=10)
        c.request('POST', f'/chain/{AG}/302/stop', body=b'{"ignored": true}', headers={'Content-Type': 'application/json'})
        self.assertEqual(c.getresponse().read() and None, None)
        c.request('GET', f'/steps/{AG}')
        r = c.getresponse()
        self.assertEqual(r.status, 200)
        self.assertIn('steps', json.loads(r.read()))

    def test_setup_then_step(self):
        self.assertEqual(post(f'/batch/{AG}/302', {'batch': '0922'})[0], 204)
        post(f'/chain/{AG}/302', {'steps': ['analysis', 'setup']})
        done = until(lambda: self.chain('302').get('steps') == ['setup', 'analysis'] and self.chain('302').get('state') == 'done' and self.chain('302'), timeout=20)
        self.assertEqual(done['at'], 'analysis')
        self.assertEqual(get('/steps/' + AG)['steps']['302']['setup'], 'done')

    def test_stop_after_current_step(self):
        post(f'/chain/{AG}/301', {'steps': ['analysis', 'strategy', 'context']})
        until(lambda: self.chain('301').get('at') == 'analysis')
        self.assertEqual(post(f'/chain/{AG}/301/stop')[0], 202)
        done = self.wait_chain('301')
        self.assertEqual((done['state'], done['error']), ('stopped', 'stopped from the page'))
        self.assertEqual([r['step'] for r in self.standin_log('run.py') if r['n'] == '301'], ['analysis'])
        self.assertFalse(os.path.exists(self.path(paths.chain(B, '301', 'stop'))))

    def test_failed_step_ends_it(self):
        lab_env = dict(self.env, STANDIN_FAIL='strategy')
        subprocess.run([sys.executable, self.path('chain.py'), AG, '300', '--steps', 'analysis,strategy,context', '--pages', self.run_dir], env=lab_env, check=True, timeout=30)
        st = self.load(paths.chain(B, '300'))
        self.assertEqual((st['state'], st['error']), ('failed', 'strategy: stand-in failure'))


class Ledger(Lab):
    name = 'ledger'

    def test_totals(self):
        steps = self.module('steps')
        sys.path.insert(0, self.env['SIERRA_SCRIPTS'])
        import ledger
        pages = self.run_dir
        before = ledger.total(ledger.load(pages, AG, '302'))
        ledger.add(pages, AG, '302', ledger.entry('2026-09-23T00:00:00Z', 'analysis', {'model': 'm', 'state': 'done'}, {'cost': 0.25}))
        ledger.add(pages, AG, '302', ledger.entry('2026-09-23T00:00:01Z', 'resolve', {'model': 'm', 'state': 'done'}, {'cost': 1.5}))
        after = ledger.total(ledger.load(pages, AG, '302'))
        self.assertAlmostEqual(after['cost'] - before['cost'], 1.75, places=6)
        self.assertEqual(after['runs'], before['runs'] + 2)
        self.assertAlmostEqual(after['steps']['resolve'] - before['steps'].get('resolve', 0), 1.5, places=6)
        self.write(paths.step_file(B, '302', 'resolve', 'status.json'), {'state': 'working', 'pid': os.getpid(), 'usage': {'cost': 0.5}, 'turn': 'agent'})
        cost = get('/steps/' + AG)['cost']['302']
        self.assertAlmostEqual(cost['cost'], after['cost'] + 0.5, places=6)
        self.assertEqual(cost['runs'], after['runs'] + 1)
        self.assertEqual(get('/steps/' + AG)['resolve']['302']['turn'], 'agent')
        self.assertTrue(steps.alive(os.getpid()))

    def test_stage_step_check(self):
        stage = [sys.executable, os.path.join(self.env['SIERRA_SCRIPTS'], 'stage.py'), AG, '302']
        pages = ['--pages', self.run_dir]
        self.assertNotEqual(subprocess.run(stage + ['review', 'wrong'] + pages, capture_output=True).returncode, 0)
        self.assertNotEqual(subprocess.run(stage + ['review', 'holds', '--step', 'analysis'] + pages, capture_output=True).returncode, 0)
        self.assertNotEqual(subprocess.run(stage + ['fix', 'misguided', '--step', 'resolve'] + pages, capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(stage + ['review', 'wrong', '--step', 'analysis'] + pages, capture_output=True).returncode, 0)
        last = self.load(paths.step_file(B, '302', 'resolve', 'stage.json'))[-1]
        self.assertEqual((last['stage'], last['state'], last['step']), ('review', 'wrong', 'analysis'))
        self.assertEqual(get('/steps/' + AG)['resolve']['302']['stage']['step'], 'analysis')


class SessionHost(Lab):
    name = 'host'

    def events(self):
        return [json.loads(l) for l in open(self.path(paths.runs(B, '304', 'resolve'), 'out.jsonl'))]

    def test_send_abort_ui_ask_stop_resume(self):
        code, r = post(f'/chat/{AG}/304/start', {'model': 'gpt-5.6-terra', 'effort': 'low'})
        self.assertEqual(code, 202)
        st = get(f'/chat/{AG}/304/state')
        self.assertEqual((st['running'], st['status']['pid']), (True, r['pid']))
        self.assertEqual(post(f'/chat/{AG}/304/start', {})[0], 409)
        until(lambda: any(e['type'] == 'agent_settled' for e in self.events()))
        self.assertEqual(post(f'/chat/{AG}/304/send', {'message': 'SLOW ASKUI one'}), (202, {'mode': 'prompt'}))
        until(lambda: get(f'/chat/{AG}/304/state')['streaming'])
        self.assertEqual(get('/steps/' + AG)['resolve']['304']['turn'], 'agent')
        self.assertEqual(post(f'/chat/{AG}/304/send', {'message': 'two'}), (202, {'mode': 'steer'}))
        self.assertEqual(post(f'/chat/{AG}/304/send', {'message': 'three', 'mode': 'follow_up'}), (202, {'mode': 'follow_up'}))
        self.assertEqual(post(f'/chat/{AG}/304/send', {'message': ' '})[0], 400)
        self.assertEqual(post(f'/chat/{AG}/304/abort')[0], 202)
        self.assertEqual(post(f'/chat/{AG}/304/ui', {'id': 'ui1', 'confirmed': True})[0], 202)
        self.assertEqual(post(f'/chat/{AG}/304/ui', {})[0], 400)
        self.assertEqual(post(f'/chat/{AG}/304/ask')[0], 202)
        self.assertIn('resolution already sent', post(f'/chat/{AG}/304/ask')[1]['error'])
        until(lambda: any(e['type'] == 'extension_ui_request' for e in self.events()))
        pi = get(f'/chat/{AG}/304/state')['status']['pi']
        cmds = [r['cmd'] for r in self.standin_log('pi') if 'cmd' in r and r['pid'] == pi]
        self.assertEqual(cmds[:6], ['prompt', 'prompt', 'steer', 'follow_up', 'abort', 'extension_ui_response'])
        ev = self.events()
        self.assertIn({'type': 'ui_answer', 'id': 'ui1', 'answer': {'confirmed': True}}, [{k: v for k, v in e.items() if k != 't'} for e in ev])
        self.assertEqual([e['mode'] for e in ev if e['type'] == 'sent'][:4], ['prompt', 'prompt', 'steer', 'follow_up'])
        entries = len(json.load(open(self.path(paths.cost(B, '304')))))
        self.assertEqual(post(f'/chat/{AG}/304/stop')[0], 202)
        until(lambda: not get(f'/chat/{AG}/304/state')['running'])
        st = get(f'/chat/{AG}/304/state')
        self.assertEqual((st['status']['state'], st['status']['error']), ('failed', 'stopped from the page'))
        self.assertTrue(st['resumable'])
        self.assertEqual(get('/steps/' + AG)['steps']['304']['resolve'], 'stopped')
        self.assertEqual(len(json.load(open(self.path(paths.cost(B, '304'))))), entries + 1)
        self.assertEqual(self.events()[-1]['type'], 'exit')
        self.assertFalse(os.path.exists(self.path(paths.runs(B, '304', 'resolve'), 'sock')))
        self.assertEqual(post(f'/chat/{AG}/304/send', {'message': 'x'})[0], 409)
        n = len(self.events())
        self.assertEqual(post(f'/chat/{AG}/304/start', {'resume': True, 'model': 'gpt-5.6-terra', 'effort': 'low'})[0], 202)
        pi = get(f'/chat/{AG}/304/state')['status']['pi']
        self.assertIn('--continue', until(lambda: [r for r in self.standin_log('pi') if r['pid'] == pi and 'argv' in r])[0]['argv'])
        ev = self.events()
        self.assertEqual(ev[n]['type'], 'resumed')
        self.assertFalse([e for e in ev[n:] if e['type'] == 'sent'])
        self.assertTrue(get(f'/chat/{AG}/304/state')['status']['asked'])
        post(f'/chat/{AG}/304/stop')
        until(lambda: not get(f'/chat/{AG}/304/state')['running'])

    def test_sim_run_counts(self):
        post(f'/chat/{AG}/297/start', {'model': 'gpt-5.6-terra', 'effort': 'low'})
        runs = len(self.load(paths.step_file(B, '297', 'resolve', 'runs.json')))
        post(f'/chat/{AG}/297/send', {'message': 'SIM SLOW'})
        until(lambda: get('/steps/' + AG)['resolve']['297'].get('live'))
        until(lambda: len(self.load(paths.step_file(B, '297', 'resolve', 'runs.json'))) == runs + 1)
        last = self.load(paths.step_file(B, '297', 'resolve', 'runs.json'))[-1]
        self.assertEqual((last['passed'], last['total'], last['green'], last['sims'], last['file']), (8, 10, 1, 2, 'sim.json'))
        sims = [e for e in map(json.loads, open(self.path(paths.log(B, '297')))) if e['who'] == 'sims']
        self.assertTrue(sims[-1]['what'].startswith('sim.json: 8/10 runs passed, 1/2 sims green'), sims[-1]['what'])
        until(lambda: not get('/steps/' + AG)['resolve']['297'].get('live'))
        post(f'/chat/{AG}/297/stop')

    def test_direct_socket(self):
        post(f'/chat/{AG}/300/start', {'model': 'gpt-5.6-terra', 'effort': 'low'})
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        here = os.getcwd(); os.chdir(self.run_dir)  # a socket path is capped near 104 bytes: connect by the pages-relative one
        try:
            s.connect(os.path.join(paths.runs(B, '300', 'resolve'), 'sock'))
        finally:
            os.chdir(here)
        s.sendall(b'{"cmd": "state"}\n')
        self.assertEqual(json.loads(s.makefile().readline())['running'], True)
        s.close()
        post(f'/chat/{AG}/300/stop')
        until(lambda: not get(f'/chat/{AG}/300/state')['running'])

    def test_history_points_into_the_session_log(self):
        runs, log = self.path(paths.runs(B, '300', 'resolve')), self.path(paths.log(B, '300'))
        before = len(open(log).readlines()) if os.path.exists(log) else 0
        for rnd in range(2):
            post(f'/chat/{AG}/300/start', {'model': 'gpt-5.6-terra', 'effort': 'low'})
            until(lambda: get(f'/chat/{AG}/300/state')['running'])
            self.assertTrue(os.path.islink(os.path.join(runs, 'out.jsonl')))
            post(f'/chat/{AG}/300/send', {'message': f'round {rnd}\nmore'})
            post(f'/chat/{AG}/300/send', {'message': 'the steps reran', 'by': 'rerun'})
            post(f'/chat/{AG}/300/stop')
            until(lambda: not get(f'/chat/{AG}/300/state')['running'])
            time.sleep(1.1)  # the next session's log is named by its start second
        ev = [json.loads(l) for l in open(log)][before:]
        self.assertEqual([(e['who'], e['what']) for e in ev], [
            ('session', 'resolution session started, its brief as the first prompt'), ('engineer', 'message: «round 0» (more lines)'),
            ('session', 'resolution session started, its brief as the first prompt'), ('engineer', 'message: «round 1» (more lines)')])
        self.assertNotEqual(ev[1]['refs'][0].split('@')[0], ev[3]['refs'][0].split('@')[0])
        for e, text in zip(ev, ('', 'round 0\nmore', '', 'round 1\nmore')):
            path, line = e['refs'][0].split('@L')
            sent = json.loads(open(self.path('agents', AG, path)).read().splitlines()[int(line) - 1])
            self.assertEqual(sent['type'], 'sent')
            if text:
                self.assertEqual(sent['text'], text)

    def test_start_refused(self):
        steps = self.module('steps')
        cwd = os.getcwd()
        os.chdir(self.run_dir)
        old = dict(os.environ)
        os.environ.update(self.env, STANDIN_BRIEF_FAIL='1')
        try:
            err = steps.start_step(AG, '296', 'resolve', 'gpt-5.6-terra', 'low')
            self.assertEqual(err, 'brief: stand-in brief refused')
            self.assertEqual(steps.start_step(AG, '303', 'resolve'), 'no worktree: set the issue up first')
            self.assertEqual(steps.start_step(AG, '296', 'resolve', resume=True), 'nothing to resume: no stopped session with a session file')
        finally:
            os.environ.clear(); os.environ.update(old); os.chdir(cwd)
        self.assertNotEqual(get(f'/chat/{AG}/296/state')['status'].get('state'), 'working')


@unittest.skipUnless(lab.RERUNS, 'the scripts have no stepgit.py')
class Reruns(Lab):
    name = 'reruns'
    extra = {'STANDIN_SECONDS': '0.4'}

    def wt(self, n):
        return self.load(paths.step_file(B, n, 'setup', 'status.json'))['worktree']

    def git(self, n, *a):
        return subprocess.run(['git', '-C', self.wt(n)] + list(a), capture_output=True, text=True, env=self.env, check=True).stdout.strip()

    def test_refused_while_another_step_runs(self):
        self.write(paths.step_file(B, '301', 'analysis', 'status.json'), {'state': 'working', 'pid': os.getpid()})
        try:
            self.assertEqual(post(f'/run/{AG}/301/context', {}), (409, {'error': 'analysis is running: wait for it or stop it'}))
        finally:
            os.remove(self.path(paths.step_file(B, '301', 'analysis', 'status.json')))
        self.assertEqual(post(f'/run/{AG}/301/context', {})[0], 202)

    def test_feedback_reaches_the_first_step_and_the_live_session(self):
        self.assertEqual(post(f'/chat/{AG}/304/start', {'model': 'gpt-5.6-terra', 'effort': 'low'})[0], 202)
        code, st = post(f'/chain/{AG}/304', {'steps': ['context', 'strategy'], 'feedback': 'The guard misses the second question.'})
        self.assertEqual((code, st['steps']), (202, ['strategy', 'context']))
        done = until(lambda: (lambda c: c.get('state') == 'done' and 'notified' in c and c)(self.load(paths.chain(B, '304'))), timeout=20)
        self.assertTrue(done['notified'])
        runs = [r for r in self.standin_log('run.py') if r['n'] == '304']
        self.assertEqual([(r['step'], r['feedback']) for r in runs], [('strategy', 'The guard misses the second question.'), ('context', None)])
        out = self.path(paths.runs(B, '304', 'resolve'), 'out.jsonl')
        sent = until(lambda: [e for e in map(json.loads, open(out)) if e.get('type') == 'sent' and 'reran' in e['text']])
        self.assertEqual(sent[0]['text'], 'The engineer reran strategy, context with feedback.\n'
                         f'strategy: done, new answer in {paths.answer(B, "304", "strategy")}.\ncontext: done, new answer in {paths.answer(B, "304", "context")}.\nReview them again.')
        post(f'/chat/{AG}/304/stop')

    def test_run_with_feedback_is_a_one_step_sequence(self):
        code, st = post(f'/run/{AG}/297/analysis', {'feedback': 'Look at turn 12.'})
        self.assertEqual((code, st['steps']), (202, ['analysis']))
        done = until(lambda: (lambda c: c.get('state') == 'done' and 'notified' in c and c)(self.load(paths.chain(B, '297'))), timeout=20)
        self.assertFalse(done['notified'])
        self.assertEqual([r['feedback'] for r in self.standin_log('run.py') if r['n'] == '297'], ['Look at turn 12.'])

    def test_stale_answers(self):
        a = f'agents/{AG}'
        for step, age in (('analysis', 30), ('strategy', 20), ('context', 10)):
            p = self.path(paths.answer(a, '300', step))
            os.utime(p, (time.time() - age, time.time() - age))
        self.assertNotIn('300', get('/steps/' + AG)['stale'])
        os.utime(self.path(paths.answer(a, '300', 'analysis')))
        self.assertEqual(get('/steps/' + AG)['stale']['300'], {'strategy': 'analysis is newer', 'context': 'analysis is newer'})


@unittest.skipIf(lab.RERUNS, 'the scripts have stepgit.py')
class OlderScripts(Lab):
    name = 'older'

    def test_feedback_refused_plain_runs_as_before(self):
        wt = self.load(paths.step_file(B, '301', 'setup', 'status.json'))['worktree']
        open(os.path.join(wt, 'README'), 'a').write('work in progress\n')
        try:
            for path, body in ((f'/run/{AG}/301/strategy', {'feedback': 'x'}), (f'/chain/{AG}/301', {'steps': ['context'], 'feedback': 'x'})):
                self.assertEqual(post(path, body), (409, {'error': 'reruns with feedback need the toolkit scripts with stepgit.py; run the step without feedback'}))
            self.assertEqual(post(f'/run/{AG}/301/context', {})[0], 202)
        finally:
            subprocess.run(['git', '-C', wt, 'checkout', '--', 'README'], env=self.env, check=True)


class SelfRestart(Lab):
    name = 'restart'

    def boot(self):
        return urllib.request.urlopen(BASE + '/index.html', timeout=2).headers.get('X-Server-Boot')

    def test_restart_keeps_the_session(self):
        post(f'/chat/{AG}/304/start', {'model': 'gpt-5.6-terra', 'effort': 'low'})
        got, ids = [], []
        def follow(last=None):
            req = urllib.request.Request(BASE + f'/chat/{AG}/304/events', headers={'Last-Event-ID': last} if last else {})
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    for raw in r:
                        line = raw.decode().rstrip('\n')
                        if line.startswith('id: '):
                            ids.append(line[4:])
                        elif line.startswith('data: {"'):
                            got.append(json.loads(line[6:]))
            except Exception:
                pass
        t = threading.Thread(target=follow, daemon=True); t.start()
        until(lambda: any(e.get('type') == 'agent_settled' for e in got))
        boot, pid = self.boot(), self.server.pid
        refused, probing = [], [True]
        def probe():
            while probing[0]:
                try:
                    urllib.request.urlopen(BASE + '/index.html', timeout=10).read()
                except Exception as ex:
                    refused.append(repr(ex))
                time.sleep(0.02)
        p = threading.Thread(target=probe, daemon=True); p.start()
        os.utime(self.path('steps.py'))
        until(lambda: self._boot_changed(boot), timeout=15)
        probing[0] = False; p.join(5)
        self.assertEqual(refused, [])
        t.join(5)
        self.assertFalse(t.is_alive())
        self.assertEqual(int(open(self.path('server.pid')).read()), pid)
        self.assertTrue(lab.subprocess.run(['kill', '-0', str(pid)]).returncode == 0)
        self.assertTrue(get(f'/chat/{AG}/304/state')['running'])
        seen = len(got)
        t2 = threading.Thread(target=follow, args=(ids[-1],), daemon=True); t2.start()
        self.assertEqual(post(f'/chat/{AG}/304/send', {'message': 'after the restart'}), (202, {'mode': 'prompt'}))
        until(lambda: any(e.get('type') == 'sent' and e['text'] == 'after the restart' for e in got[seen:]))
        self.assertEqual(got[seen]['type'], 'sent')
        post(f'/chat/{AG}/304/stop')
        t2.join(10)
        self.assertEqual(got[-1]['type'], 'exit')

    def _boot_changed(self, boot):
        try:
            return self.boot() != boot
        except Exception:
            return False

    def test_broken_code_does_not_restart(self):
        boot = self.boot()
        p = self.path('steps.py')
        good = open(p).read()
        try:
            open(p, 'w').write(good + '\ndef broken(:\n')
            time.sleep(3)
            self.assertEqual(self.boot(), boot)
            self.assertIn('not restarting', open(self.path('serve.log')).read())
        finally:
            open(p, 'w').write(good)
        until(lambda: self._boot_changed(boot), timeout=15)


class BatchSync(Lab):
    """Card 301 (batch 0922, not merged) against a batch branch one commit ahead of its worktree."""
    name = 'batchsync'

    def setUp(self):
        self.wt = self.path('repo', '.claude', 'worktrees', 'hip-301')
        g = lambda *a: subprocess.run(['git', '-C', self.wt] + list(a), check=True, capture_output=True, env=self.env)
        g('checkout', '-q', '-B', 'stan/hip-issues-0922')
        open(os.path.join(self.wt, 'batch.txt'), 'w').write('another card\n')
        g('add', '-A'); g('commit', '-q', '-m', 'another card merged into the batch')
        g('checkout', '-q', 'stan/hip-301')
        g('reset', '-q', '--hard', 'stan/hip-issues-0922~1')

    def behind(self):
        return get('/steps/' + AG)['behind']

    def test_behind_route_and_refusal(self):
        v = self.behind()
        self.assertEqual(list(v), ['301'])
        self.assertEqual((v['301']['batch'], v['301']['branch'], v['301']['count']), ('0922', 'stan/hip-issues-0922', 1))
        a = f'agents/{AG}'
        self.write(paths.step_file(a, '301', 'strategy', 'status.json'), {'state': 'working', 'pid': os.getpid()})
        code, j = post('/cardsync/' + AG + '/301')
        self.assertEqual((code, j['error']), (409, 'strategy is running'))
        os.remove(self.path(paths.step_file(a, '301', 'strategy', 'status.json')))
        self.assertEqual(post('/cardsync/' + AG + '/301')[0], 202)
        until(lambda: not self.behind())
        self.assertEqual([r['n'] for r in self.standin_log('cardsync.py')], ['301'])


class BatchSyncLoop(BatchSync):
    """The server's own loop takes the batch in without being asked, once the card is idle."""
    name, extra = 'batchsyncloop', {'CARDSYNC_SECONDS': '0.3'}

    def test_behind_route_and_refusal(self):
        pass

    def test_loop_syncs_an_idle_card(self):
        until(lambda: not self.behind(), timeout=10)
        self.assertEqual([r['n'] for r in self.standin_log('cardsync.py')], ['301'])
        time.sleep(1)
        self.assertEqual(len(self.standin_log('cardsync.py')), 1)


class MergeButton(Lab):
    """POST /mergecard hands the go to the card's resolution session, starting one when none is live."""
    name = 'mergecard'

    def test_go_reaches_a_fresh_session(self):
        with open(self.path('skills', 'issue-resolution', 'SKILL.md'), 'a') as f:
            f.write('\n## 5. Ready to merge\n\nCommit, then batchmerge.\n\n## 6. After\n\nnot this\n')
        self.assertEqual(post(f'/mergecard/{AG}/296'), (409, {'error': 'already merged'}))
        self.assertEqual(post(f'/mergecard/{AG}/301', {'model': 'gpt-5.6-terra', 'effort': 'low'})[0], 202)
        out = self.path(paths.runs(B, '301', 'resolve'), 'out.jsonl')
        sent = until(lambda: [e for e in (json.loads(l) for l in open(out)) if e['type'] == 'sent'] if os.path.exists(out) else None)
        msg = sent[-1]['text']
        self.assertIn('go to merge this card into batch 0922', msg)
        self.assertIn('## 5. Ready to merge\n\nCommit, then batchmerge.', msg)
        self.assertNotIn('not this', msg)
        post(f'/chat/{AG}/301/stop')
        until(lambda: not get(f'/chat/{AG}/301/state')['running'])


if __name__ == '__main__':
    unittest.main()
