// A headless Chrome over the DevTools protocol, with nothing to install: Node's own WebSocket and the Playwright
// cache's chrome-headless-shell (or Google Chrome when that is missing).
import { spawn } from 'node:child_process';
import { existsSync, mkdtempSync, readdirSync, rmSync } from 'node:fs';
import { tmpdir, homedir } from 'node:os';
import { join } from 'node:path';

function chromePath() {
  const cache = join(homedir(), 'Library/Caches/ms-playwright');
  if (existsSync(cache)) for (const d of readdirSync(cache).filter(x => x.startsWith('chromium_headless_shell-')).sort().reverse())
    for (const sub of readdirSync(join(cache, d))) { const p = join(cache, d, sub, 'chrome-headless-shell'); if (existsSync(p)) return p; }
  const app = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  if (existsSync(app)) return app;
  throw new Error('no Chrome found');
}

export async function launch() {
  const dir = mkdtempSync(join(tmpdir(), 'smoke-chrome-'));
  const proc = spawn(chromePath(), ['--headless', '--remote-debugging-port=0', `--user-data-dir=${dir}`, '--no-first-run', '--no-default-browser-check',
    '--window-size=1400,900', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
  process.on('exit', () => { try { proc.kill('SIGKILL'); rmSync(dir, { recursive: true, force: true }); } catch {} });
  const url = await new Promise((ok, bad) => {
    let buf = ''; const t = setTimeout(() => bad(new Error('Chrome did not start')), 15000);
    proc.stderr.on('data', d => { buf += d; const m = /DevTools listening on (ws:\S+)/.exec(buf); if (m) { clearTimeout(t); ok(m[1]); } });
    proc.on('exit', c => bad(new Error('Chrome exited ' + c)));
  });
  const ws = new WebSocket(url);
  await new Promise((ok, bad) => { ws.onopen = ok; ws.onerror = bad; });
  let id = 0; const wait = new Map(), handlers = [];
  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if (m.id && wait.has(m.id)) { const w = wait.get(m.id); wait.delete(m.id); m.error ? w.bad(new Error(m.error.message)) : w.ok(m.result); }
    else handlers.forEach(h => h(m));
  };
  const send = (method, params = {}, sessionId) => new Promise((ok, bad) => { const k = ++id; wait.set(k, { ok, bad }); ws.send(JSON.stringify({ id: k, method, params, sessionId })); });
  const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const s = (m, p) => send(m, p, sessionId);
  const errors = [], events = [];
  handlers.push(m => {
    if (m.sessionId !== sessionId) return;
    if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text);
    if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push(m.params.args.map(a => a.value ?? a.description).join(' '));
    if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error' && !/favicon/.test(m.params.entry.url || '')) errors.push(m.params.entry.text + ' ' + (m.params.entry.url || ''));
    events.push(m);
  });
  await s('Runtime.enable'); await s('Page.enable'); await s('Log.enable');
  const page = {
    errors,
    async goto(u) { await s('Page.navigate', { url: u }); },
    async eval(expr) {
      const r = await s('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
      if (r.exceptionDetails) throw new Error((r.exceptionDetails.exception?.description || r.exceptionDetails.text) + '\n  in: ' + expr.slice(0, 200));
      return r.result.value;
    },
    async waitFor(expr, ms = 8000, what) {
      const t0 = Date.now(); let last;
      while (Date.now() - t0 < ms) { try { last = await page.eval(expr); if (last) return last; } catch (e) { last = e.message; } await new Promise(r => setTimeout(r, 50)); }
      throw new Error('timed out waiting for ' + (what || expr) + (last ? ' (last: ' + last + ')' : ''));
    },
    async key(key, opts = {}) {
      const code = key.length === 1 ? (/[a-z]/i.test(key) ? 'Key' + key.toUpperCase() : key === ' ' ? 'Space' : '') : key;
      const mods = (opts.ctrl ? 2 : 0) | (opts.shift || (key.length === 1 && key !== key.toLowerCase()) ? 8 : 0);
      await s('Input.dispatchKeyEvent', { type: 'keyDown', key, code, text: key.length === 1 && !opts.ctrl ? key : undefined, modifiers: mods, windowsVirtualKeyCode: key.length === 1 ? key.toUpperCase().charCodeAt(0) : key === 'Escape' ? 27 : 0 });
      await s('Input.dispatchKeyEvent', { type: 'keyUp', key, code, modifiers: mods });
    },
    async shot() { return (await s('Page.captureScreenshot', { format: 'png' })).data; },
    async keys(seq) { for (const k of seq) await page.key(k); },
    async click(sel) {
      const ok = await page.eval(`(function(){var e=document.querySelector(${JSON.stringify(sel)});if(!e)return false;e.scrollIntoView({block:'center'});e.click();return true})()`);
      if (!ok) throw new Error('nothing to click at ' + sel);
    },
  };
  const close = async () => { try { ws.close(); } catch {} proc.kill('SIGKILL'); await new Promise(r => setTimeout(r, 100)); try { rmSync(dir, { recursive: true, force: true }); } catch {} };
  return { page, close };
}
