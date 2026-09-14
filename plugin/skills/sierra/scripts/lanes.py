#!/usr/bin/env python3
"""Spawn one pinned Claude desktop session per issue, each in its own worktree.

The desktop app has no session-creation API, so this drives it through Orca computer-use
(accessibility tree). Per issue: create the lane worktree off the batch branch (the repo's
post-checkout hook provisions the Studio workspace named after it), open the composer bound to
that folder through the claude://code/new deep link, set permission mode, model and effort, type
the opening prompt, send, and pin. Titles come out app-generated («Openpay issue #199»); rename
them afterwards with the ccd_session_mgmt set_session_title tool, one call per JSON line printed.

Example (the 11/09 Openpay batch):
  python3 lanes.py --repo /Users/stan/code/BBVA --branch stan/openpay-issues-0911 \
      --prefix opp --agent-dir agents/openpay \
      --prompt '/sierra start work on openpay issue #{n}' 199 206 209

Requires: orca CLI with computer-use permissions, the Claude desktop app running in the
foreground, and no other input while it runs. The slash prompt cannot travel in the deep link's
q= parameter (the app rejects prompts starting with /), hence the UI typing.
"""
import argparse, json, os, re, subprocess, sys, time

APP = 'com.anthropic.claudefordesktop'
t = ''

def orca(*args):
    r = subprocess.run(['orca', 'computer', *args, '--app', APP, '--no-screenshot', '--json'],
                       capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {'ok': False, 'raw': (r.stdout + r.stderr)[-400:]}

def tree():
    d = orca('get-app-state')
    return d['result']['snapshot']['treeText'] if d.get('ok') else ''

def find(tree_text, pat, last=False):
    ms = [m.group(1) for m in re.finditer(r'^\s*(\d+) ' + pat + r'.*$', tree_text, re.M)]
    if not ms:
        return None
    return ms[-1] if last else ms[0]

def click(i):
    return bool(orca('click', '--element-index', str(i)).get('ok'))

def log(*a):
    print(time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)

def settle(max_s=12):
    """Dismiss the «Trust this workspace?» and «Bypass all permissions?» modals, return the tree."""
    global t
    end = time.time() + max_s
    while True:
        t = tree()
        i = find(t, 'button Trust workspace') or (
            find(t, 'heading Bypass all permissions') and find(t, 'button Bypass permissions'))
        if i:
            click(i); time.sleep(1.5); continue
        if time.time() > end or find(t, r'text entry area \(settable\) Prompt') or find(t, 'rename session'):
            return t
        time.sleep(1)

def pick(button_pat, item_pat, tries=4):
    """Open a pop-up button and click a menu item, re-reading the tree between steps."""
    global t
    for _ in range(tries):
        t = tree(); i = find(t, button_pat)
        if not i or not click(i):
            time.sleep(1); continue
        time.sleep(1.2); t = tree(); j = find(t, item_pat)
        if j and click(j):
            time.sleep(1.5); t = tree(); return True
        orca('press-key', '--key', 'Escape'); time.sleep(0.8)
    return False

def ensure_worktree(a, n):
    name = f'{a.prefix}-{n}'
    wt = os.path.join(a.repo, a.worktrees, name)
    if not os.path.isdir(wt):
        r = subprocess.run(['git', '-C', a.repo, 'worktree', 'add', '-b', f'{a.owner}/{name}', wt, a.branch],
                           capture_output=True, text=True)
        if r.returncode:
            return None, 'git worktree add failed: ' + r.stderr.strip()[-300:]
    ready = os.path.join(wt, a.agent_dir, '.targets', name) if a.agent_dir else wt
    deadline = time.time() + a.ready_timeout
    while not os.path.exists(ready):
        if time.time() > deadline:
            return None, f'workspace target not provisioned: {ready}'
        time.sleep(5)
    return wt, None

def spawn(a, n):
    global t
    wt, err = ensure_worktree(a, n)
    if err:
        return {'issue': n, 'ok': False, 'error': err}
    log(n, 'worktree ready', wt)
    subprocess.run(['open', f'claude://code/new?folder={wt}&source=desktop_action'])
    time.sleep(3); t = settle()
    for _ in range(4):
        if find(t, r'text entry area \(settable\) Prompt Describe'):
            break
        i = find(t, 'button New$')
        if i:
            click(i); time.sleep(2); t = settle()
    else:
        return {'issue': n, 'ok': False, 'error': 'composer not shown'}
    name = f'{a.prefix}-{n}'
    if not find(t, f'pop-up button {re.escape(name)}$'):
        return {'issue': n, 'ok': False, 'error': f'composer bound to another folder, wanted {name}'}
    if not find(t, f'pop-up button {re.escape(a.permission)}$'):
        if not pick(r'pop-up button (?:Auto|Manual|Accept edits|Plan|Bypass permissions)$',
                    f'menu item {re.escape(a.permission)}'):
            return {'issue': n, 'ok': False, 'error': 'permission menu'}
        t = settle()
        if not find(t, f'pop-up button {re.escape(a.permission)}$'):
            return {'issue': n, 'ok': False, 'error': 'permission not applied'}
    if not find(t, f'pop-up button Model: {re.escape(a.model)}$'):
        if not pick('pop-up button Model:', f'menu item {re.escape(a.model)}'):
            return {'issue': n, 'ok': False, 'error': 'model not ' + a.model}
    if not find(t, f'pop-up button Effort: {re.escape(a.effort)}$'):
        i = find(t, 'pop-up button Effort'); click(i); time.sleep(1); t = tree()
        order = ['Low', 'Medium', 'High', 'Extra', 'Max']
        for _ in range(6):
            if find(t, rf'pop-up button (?:\(expanded\) )?Effort: {re.escape(a.effort)}$'):
                break
            m = re.search(r'pop-up button \(expanded\) Effort: (\w+)', t)
            cur = order.index(m.group(1)) if m and m.group(1) in order else 3
            s = find(t, r'slider \(settable\) Effort')
            orca('perform-secondary-action', '--element-index', s, '--action',
                 'decrement' if cur > order.index(a.effort) else 'increment')
            time.sleep(1); t = tree()
        orca('press-key', '--key', 'Escape'); time.sleep(1); t = tree()
        if not find(t, f'pop-up button Effort: {re.escape(a.effort)}$'):
            return {'issue': n, 'ok': False, 'error': 'effort not ' + a.effort}
    prompt = a.prompt.format(n=n)
    p = find(t, r'text entry area \(settable\) Prompt')
    orca('set-value', '--element-index', p, '--value', prompt); time.sleep(1); t = tree()
    if prompt not in t:
        return {'issue': n, 'ok': False, 'error': 'prompt not set'}
    s = find(t, 'button Send$')
    if not (s and click(s)):
        time.sleep(1); t = tree(); s = find(t, 'button Send$')
        if not (s and click(s)):
            return {'issue': n, 'ok': False, 'error': 'send'}
    log(n, 'sent'); time.sleep(6); t = settle()
    m = re.search(r'button (.+?), rename session', t)
    title = m.group(1) if m else None
    if not title or f'#{n}' not in title:
        return {'issue': n, 'ok': False, 'error': 'session header not found: ' + str(title)}
    pinned = False if a.no_pin else pick(r'pop-up button More options for ' + re.escape(title), 'menu item Pin$')
    return {'issue': n, 'ok': True, 'title': title, 'cwd': wt, 'pinned': pinned}

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('issues', nargs='+', help='issue numbers')
    ap.add_argument('--repo', required=True, help='main checkout, e.g. /Users/stan/code/BBVA')
    ap.add_argument('--branch', required=True, help='batch branch the lane branches fork from')
    ap.add_argument('--prefix', default='opp', help='lane name prefix: worktree, branch suffix and workspace are <prefix>-<n>')
    ap.add_argument('--owner', default='stan', help='branch namespace: <owner>/<prefix>-<n>')
    ap.add_argument('--worktrees', default='.claude/worktrees', help='worktree dir relative to --repo')
    ap.add_argument('--agent-dir', default='agents/openpay', help='agent dir whose .targets/<name> marks the hook done; empty to skip the wait')
    ap.add_argument('--prompt', default='/sierra start work on openpay issue #{n}', help='opening prompt, {n} = issue number')
    ap.add_argument('--model', default='Fable 5.1', help='label as the composer shows it')
    ap.add_argument('--effort', default='High', choices=['Low', 'Medium', 'High', 'Extra', 'Max'])
    ap.add_argument('--permission', default='Bypass permissions', help='menu item label: Manual, Accept edits, Plan, Auto, Bypass permissions')
    ap.add_argument('--no-pin', action='store_true')
    ap.add_argument('--ready-timeout', type=int, default=600, help='seconds to wait for the hook per lane')
    a = ap.parse_args()
    for n in a.issues:
        print(json.dumps(spawn(a, n)), flush=True)

if __name__ == '__main__':
    main()
