// The page in a headless Chrome against a lab server (test/lab.py up): sidebar rows and marks, card switch keeping
// folds, scroll and the open drawer, keys, a sequence started and stopped from the card, the recorded session of
// hipotecarios 304 and its Prompt fold, nothing rebuilt on poll, and a server restart under the open page with a live
// stand-in session. Usage: node smoke.mjs <base url> <lab dir>
import { launch } from './cdp.mjs';
import { utimesSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const [BASE, RUN] = process.argv.slice(2);
const A = 'hipotecarios';
const RERUNS = existsSync(join(RUN, 'skills', 'sierra', 'scripts', 'stepgit.py'));  // scripts with rewinds and --feedback
const sleep = ms => new Promise(r => setTimeout(r, ms));
let passed = 0, failed = 0;
const { page, close } = await launch();
const P = page;

async function check(name, fn) {
  const t0 = Date.now();
  try { await fn(); passed++; console.log(`ok    ${name} (${((Date.now() - t0) / 1000).toFixed(1)} s)`); }
  catch (e) { failed++; console.log(`FAIL  ${name}\n      ${String(e.message).split('\n').join('\n      ')}`); }
}
function eq(a, b, what) { if (JSON.stringify(a) !== JSON.stringify(b)) throw new Error(`${what}: got ${JSON.stringify(a)}, want ${JSON.stringify(b)}`); }
function ok(v, what) { if (!v) throw new Error(what); }
const js = x => JSON.stringify(x);
// The run strip of one step in the card on screen: its play, resume, stop and session buttons.
const strip = label => `document.querySelector('#cardv button[aria-label="Run ${label}"]').closest('.run')`;
const card = n => P.waitFor(`document.querySelector('#tree a.it.active')?.dataset.n==='${n}'&&document.querySelector('#cardv .card')&&document.querySelectorAll('#cardv .runbar .run').length>0`, 8000, 'card #' + n);
const folds = () => P.eval(`[...document.querySelectorAll('#view details.part, #view details.secw')].map(d=>d.open)`);

try {
  await P.goto(`${BASE}/index.html#a=${A}&i=304`);
  await card(304);
  await P.eval(`window.__smoke=1`);

  await check('sidebar: rows, groups, marks, strip', async () => {
    const s = await P.eval(`(${function () {
      const rows = [...document.querySelectorAll('#tree a.it')];
      return {
        rows: rows.length, groups: [...document.querySelectorAll('#tree .grp')].map(g => g.dataset.g + (g.classList.contains('open') ? ' open' : '')),
        marks: rows.map(a => a.dataset.n + ':' + a.querySelectorAll('.bar i').length).join(' '),
        merged: document.querySelectorAll('#tree a.it[data-n="304"] .bar i.merged').length, you: rows.filter(a => a.classList.contains('you')).map(a => a.dataset.n),
        label301: document.querySelector('#tree a.it[data-n="301"] .stg').textContent, active: document.querySelector('#tree a.it.active').dataset.n,
        strip: document.getElementById('strip').textContent, branch: document.querySelector('.grp[data-g="0922"] .bnm')?.textContent || '', cost: document.querySelector('.grp[data-g="0922"] .bcost')?.textContent || '',
      };
    }})()`);
    eq(s.rows, 12, 'rows'); eq(s.groups, ['0923', '0922 open', 'No batch yet'], 'groups'); eq(s.active, '304', 'active row');
    ok(/304:5 301:5 300:5/.test(s.marks) && /303:4 302:4/.test(s.marks), 'resolution rows carry five marks, prep rows four: ' + s.marks);
    eq(s.merged, 1, 'merged mark on 304'); eq(s.you, ['301'], 'your-turn rows'); eq(s.label301, 'Ready to merge', '301 label');
    eq(s.strip, '1 ready', 'strip'); ok(s.branch, 'batch branch shown'); ok(/^\$/.test(s.cost), 'batch cost shown: ' + s.cost);
  });

  await check('session panel: recorded out.jsonl of 304 and its Prompt fold', async () => {
    await P.eval(`${strip('resolution')}.querySelector('.sbtn2').click()`);
    await P.waitFor(`document.querySelectorAll('aside.sess .tl > *').length>20`, 8000, 'timeline rows');
    const s = await P.eval(`({rows:document.querySelectorAll('aside.sess .tl > *').length,state:document.querySelector('aside.sess header .st').textContent,chat:document.querySelector('aside.sess').classList.contains('chat'),ttl:document.querySelector('aside.sess .ttl').textContent})`);
    ok(s.rows > 20, 'timeline rows: ' + s.rows); eq(s.ttl, '#304 · resolution', 'title'); eq(s.state, 'failed', 'state chip');
    await P.waitFor(`document.querySelector('aside.sess details.prm .pp .pl')`, 5000, 'prompt fold filled');
    const prm = await P.eval(`[...document.querySelectorAll('aside.sess details.prm .pl')].map(x=>x.textContent)`);
    eq(prm, ['System prompt · not recorded', 'First message · not recorded'], 'prompt fold parts');
  });

  await check('card switch keeps folds, scroll and the open drawer', async () => {
    await P.eval(`(function(){var l=[...document.querySelectorAll('#view details.part, #view details.secw')];l[0].open=!l[0].open;l[l.length-1].open=true})()`);
    await P.eval(`document.querySelector('aside.sess details.prm').open=true`);
    await P.eval(`window.scrollTo({top:300})`); await sleep(400);
    const before = { f: await folds(), y: await P.eval(`window.scrollY`) };
    ok(before.y > 0, 'page scrolls');
    await P.eval(`document.activeElement.blur()`);
    await P.key('L'); await card(301);
    eq(await P.eval(`!!document.querySelector('aside.sess')`), false, 'drawer closed on the other card');
    await P.key('H'); await card(304);
    await P.waitFor(`document.querySelector('aside.sess .ttl')?.textContent==='#304 · resolution'`, 5000, 'session drawer back');
    eq(await folds(), before.f, 'folds'); eq(await P.eval(`window.scrollY`), before.y, 'scroll');
  });

  await check('keys: j/k, zj/za, ? and Esc', async () => {
    await P.eval(`document.querySelector('aside.sess header button[aria-label="Close"]').click()`);
    await P.eval(`window.scrollTo({top:0})`);
    await P.key('j'); await sleep(100); eq(await P.eval(`window.scrollY`), 60, 'j scrolls 60');
    await P.key('k'); await sleep(100); eq(await P.eval(`window.scrollY`), 0, 'k scrolls back');
    await P.keys(['z', 'j']); const f = await P.eval(`[...document.querySelectorAll('#view details.kf')].length`); eq(f, 1, 'zj focuses one section');
    const was = await P.eval(`document.querySelector('#view details.kf').open`);
    await P.keys(['z', 'a']); eq(await P.eval(`document.querySelector('#view details.kf').open`), !was, 'za toggles it');
    await P.keys(['z', 'a']);
    await P.key('?'); ok(await P.eval(`!!document.getElementById('keyhelp')`), '? opens the key list');
    await P.key('Escape'); ok(await P.eval(`!document.getElementById('keyhelp')`), 'Esc closes it');
    await P.keys([']', 'b']); await card(301); await P.keys(['[', 'b']); await card(304);
    await P.key('n'); await sleep(200); await card(304);
    await P.goto(`${BASE}/index.html#a=${A}&i=304`); await card(304); await P.eval(`window.__smoke=1`);
  });

  await check('sequence from the card: start, progress, stop; nothing rebuilt on poll', async () => {
    await P.eval(`document.querySelector('#cardv .card').__mark=1; document.querySelector('#tree a.it[data-n="304"]').__mark=1; document.querySelector('#tree').__mark=1`);
    await P.eval(`localStorage.setItem('chainSteps','analysis,strategy,context')`);
    await P.click('#cardv .run.chain .cho');
    await P.waitFor(`!document.querySelector('#cardv .run.chain .chpop').hidden`, 3000, 'step popover');
    eq(await P.eval(`[...document.querySelectorAll('#cardv .run.chain .stp.on')].map(b=>b.dataset.s)`), ['analysis', 'strategy', 'context'], 'chosen steps');
    await P.click('#cardv .run.chain .cgo');
    await P.waitFor(`/1\\/3 · analysis/.test(document.querySelector('#cardv .run.chain .chip').textContent)`, 8000, 'chip 1/3 · analysis');
    await P.waitFor(`document.querySelector('#tree a.it[data-n="304"] .who .spin')`, 5000, 'row spinner');
    await P.waitFor(`${strip('issue analysis')}.querySelector('.chip').classList.contains('working')`, 5000, 'analysis chip working');
    await P.click('#cardv .run.chain .kbtn');
    await P.waitFor(`/sequence stopped/.test(document.querySelector('#cardv .run.chain .chip').textContent)`, 12000, 'sequence stopped');
    await P.waitFor(`!document.querySelector('#tree a.it[data-n="304"] .who .spin')`, 5000, 'row spinner gone');
    const k = await P.eval(`({analysis:${strip('issue analysis')}.querySelector('.chip').textContent,strategy:${strip('sim strategy')}.querySelector('.chip').className})`);
    ok(/done|\d/.test(k.analysis), 'analysis ran: ' + k.analysis);
    await P.eval(`${strip('issue analysis')}.querySelector('.sbtn2').click()`);
    await P.waitFor(`document.querySelector('aside.sess .ttl')?.textContent==='#304 · issue analysis'&&document.querySelectorAll('aside.sess details.prm .pl').length>=2`, 5000, 'analysis session drawer with its prompt');
    eq(await P.eval(`[...document.querySelectorAll('aside.sess details.prm .pl')].map(x=>x.textContent.replace(/\\d+/,'N'))`), ['System prompt · N chars', 'Message · N chars'], 'analysis prompt fold');
    ok(await P.eval(`/Stand-in system prompt for analysis/.test(document.querySelector('aside.sess details.prm .pp').textContent)`), 'system.md text shown');
    await P.eval(`document.querySelector('aside.sess header button[aria-label="Close"]').click()`);
    await sleep(2500);
    const m = await P.eval(`[document.querySelector('#cardv .card').__mark,document.querySelector('#tree a.it[data-n="304"]').__mark,document.querySelector('#tree').__mark,window.__smoke]`);
    eq(m, [1, 1, 1, 1], 'card, row, tree and page kept across polls');
  });

  await check('stale marks in the card and the sidebar; the card\'s rerun popover', async () => {
    const t = new Date(Date.now() + 5000); utimesSync(join(RUN, 'agents', A, 'analysis', '304.json'), t, t);
    await P.waitFor(`document.querySelector('#tree a.it[data-n="304"] .stl')`, 6000, 'stale mark on the sidebar row');
    eq(await P.eval(`document.querySelector('#tree a.it[data-n="304"] .stl').title`), 'Stale: Sim strategy (analysis is newer), Context edit (analysis is newer)', 'row mark title');
    await P.waitFor(`${strip('sim strategy')}.querySelector('.chip.stale')`, 4000, 'stale chip on the strategy strip');
    eq(await P.eval(`[${strip('issue analysis')}.querySelector('.chip.stale'),${strip('context edit')}.querySelector('.chip.stale')?.title]`), [null, 'Out of date: analysis is newer'], 'stale chips');
    const f0 = await folds();
    await P.eval(`${strip('sim strategy')}.querySelector('.rrb1').click()`);
    await P.waitFor(`document.querySelector('.flt .rrn .rrf')`, 3000, 'rerun popover');
    eq(await P.eval(`document.querySelector('.flt .rrh').textContent`), 'Rerun sim strategy', 'popover title');
    await P.eval(`document.querySelector('.flt .rrf').focus()`);
    await P.keys([' ', 'j', 'k']);
    eq(await P.eval(`document.querySelector('.flt .rrf').value`), ' jk', 'typing goes to the feedback box');
    eq(await folds(), f0, 'folds untouched by typing');
    await P.key('Escape');
    ok(await P.eval(`!document.querySelector('.flt')`), 'Esc closes the popover');
  });

  await check('server restart under the open page with a live stand-in session', async () => {
    await P.goto(`${BASE}/index.html#a=${A}&i=296`); await card(296); await P.eval(`window.__smoke=2`);
    await P.eval(`${strip('resolution')}.querySelector('button[aria-label="Run resolution"]').click()`);
    await P.waitFor(`document.querySelector('aside.sess.chat .ttl')?.textContent==='#296 · resolution'`, 10000, 'session drawer opens');
    await P.waitFor(`document.querySelector('aside.sess header .st').textContent==='working'`, 10000, 'session working');
    await P.waitFor(`/stand-in/i.test(document.querySelector('aside.sess .tl').textContent)`, 10000, 'stand-in reply in the timeline');
    await P.waitFor(`document.querySelectorAll('aside.sess details.prm .pl').length>=2`, 5000, 'prompt fold');
    const prm = await P.eval(`[...document.querySelectorAll('aside.sess details.prm .pl')].map(x=>x.textContent)`);
    ok(/^System prompt · \d+ chars$/.test(prm[0]) && /^First message · \d+ chars$/.test(prm[1]), 'prompt fold of the live session: ' + js(prm));
    const st0 = await P.eval(`fetch('chat/${A}/296/state').then(r=>r.json())`);
    ok(st0.running && st0.status.pid, 'session running');
    const boot0 = await P.eval(`fetch('index.html',{cache:'no-store'}).then(r=>r.headers.get('X-Server-Boot'))`);
    await P.eval(`document.querySelector('aside.sess').__mark=1; document.querySelector('aside.sess details.prm').open=true`);
    const t = new Date(); utimesSync(join(RUN, 'steps.py'), t, t);
    await P.waitFor(`fetch('index.html',{cache:'no-store'}).then(r=>r.headers.get('X-Server-Boot')).catch(()=>null).then(b=>b&&b!==${js(boot0)})`, 15000, 'new server boot');
    const st1 = await P.eval(`fetch('chat/${A}/296/state').then(r=>r.json())`);
    eq([st1.running, st1.status.pid], [true, st0.status.pid], 'same session host after the restart');
    await P.eval(`(function(){var t=document.querySelector('aside.sess form.comp textarea');t.value='after the restart';document.querySelector('aside.sess form.comp .send').click()})()`);
    await P.waitFor(`/after the restart/.test(document.querySelector('aside.sess .tl').textContent)`, 10000, 'message after the restart in the timeline');
    eq(await P.eval(`[window.__smoke,document.querySelector('aside.sess').__mark,document.querySelector('aside.sess details.prm').open]`), [2, 1, true], 'page, drawer and open Prompt fold kept');
    await P.eval(`${strip('resolution')}.querySelector('.kbtn').click()`);
    await P.waitFor(`/^(done|failed)$/.test(document.querySelector('aside.sess header .st').textContent)`, 10000, 'session ended after stop');
    eq(await P.eval(`fetch('chat/${A}/296/state').then(r=>r.json()).then(j=>j.running)`), false, 'host gone');
  });

  if (RERUNS) await check('rerun from the resolution panel: prefill, the live session told', async () => {
    const stage = join(RUN, 'agents', A, 'resolve', '297.stage.json');
    writeFileSync(stage, JSON.stringify(JSON.parse(readFileSync(stage, 'utf8')).concat([{ t: new Date().toISOString(), stage: 'fix', state: 'misguided', step: 'context', note: 'The edit is too broad.' }])));
    await P.goto(`${BASE}/index.html#a=${A}&i=297`); await card(297);
    await P.eval(`${strip('resolution')}.querySelector('button[aria-label="Run resolution"]').click()`);
    await P.waitFor(`document.querySelector('aside.sess.chat header .st')?.textContent==='working'`, 10000, 'session working');
    await P.waitFor(`document.querySelector('aside.sess details.rrw[open] .rrs')?.value==='context'`, 5000, 'rerun block open, context chosen');
    eq(await P.eval(`[document.querySelector('aside.sess .rrw .rrf').value,document.querySelector('aside.sess .rrw>summary').textContent,!!document.querySelector('aside.sess .rrw + form.comp')]`),
      ['The edit is too broad.', 'Rerun step · context edit blamed', true], 'prefill, title, above the message box');
    await P.eval(`document.querySelector('aside.sess .rrw .rrgo').click()`);
    await P.waitFor(`document.querySelector('aside.sess .rrw .rrm.done')`, 5000, 'rerun started');
    await P.waitFor(`/The engineer reran context with feedback/.test(document.querySelector('aside.sess .tl').textContent)`, 15000, 'the session is told');
    ok(await P.eval(`/new commit fffffff stand-in context for 297/.test(document.querySelector('aside.sess .tl').textContent)`), 'with the new commit');
    const log = readFileSync(join(RUN, 'standin.log'), 'utf8').trim().split('\n').map(JSON.parse).filter(r => r.who === 'run.py' && r.n === '297');
    eq(log.map(r => [r.step, r.feedback]), [['context', 'The edit is too broad.']], 'run.py got the feedback');
    await P.eval(`${strip('resolution')}.querySelector('.kbtn').click()`);
    await P.waitFor(`/^(done|failed)$/.test(document.querySelector('aside.sess header .st').textContent)`, 10000, 'session ended');
  });

  await check('no page errors', async () => {
    const errs = P.errors.filter(e => !/status of 404/.test(e) && !/status of 409 .*\/run\/hipotecarios\/297\/context$/.test(e));
    eq(errs, [], 'console errors');
  });
} finally {
  await close();
  console.log(`${passed} passed, ${failed} failed`);
  process.exitCode = failed ? 1 : 0;
}
