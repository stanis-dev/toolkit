#!/usr/bin/env python3
"""Spawn one Herdr lane per issue, each in its own worktree.

Per issue: create the lane worktree off the batch branch (the repo's post-checkout hook provisions
the Studio workspace named after it), optionally finish provisioning (Claude Code MCP config,
Ghostwriter bound to the lane workspace, tree pushed to it), open the worktree as a Herdr workspace
labelled «<PREFIX> #<n>», start claude in its root pane at the model, effort and permission mode the
flags name, and submit the opening prompt. Prints one JSON line per issue.

Example (the 16/09 Cobranzas batch):
  python3 lanes.py --repo /Users/stan/code/BBVA --branch stan/cobranzas-issues-0916 \
      --prefix cob --agent-dir agents/base --provision --mcp-server sierra-base \
      --prompt '/sierra start work on cobranzas issue #{n}' 442 443

Requires: herdr 0.9+ with its server running (`herdr status`) and the `claude` integration
installed (`herdr integration status`). Nothing needs the desktop app or the foreground. The first
bypass-permissions lane on a machine meets Claude's one-time acceptance dialog; the script answers
it. Lanes report to the overseer through cross-session messages; Herdr adds `herdr agent list`
(state per lane), `herdr agent read <name>` (its screen) and `herdr notification show`.
"""
import argparse, json, os, re, subprocess, sys, time


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)


def herdr(*args, timeout=120):
    """Run a herdr CLI command; JSON on stdout is the result, JSON on stderr is the error."""
    r = subprocess.run(['herdr', *args], capture_output=True, text=True, timeout=timeout)
    for stream in (r.stdout, r.stderr):
        try:
            d = json.loads(stream)
        except Exception:
            continue
        if 'error' in d:
            return {'ok': False, 'code': d['error'].get('code'), 'error': d['error'].get('message')}
        return {'ok': True, **d.get('result', {})}
    return {'ok': False, 'code': 'cli', 'error': (r.stdout + r.stderr).strip()[-300:]}


def sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def ensure_worktree(a, n):
    name = f'{a.prefix}-{n}'
    wt = os.path.join(a.repo, a.worktrees, name)
    if not os.path.isdir(wt):
        rc, out = sh(['git', '-C', a.repo, 'worktree', 'add', '-b', f'{a.owner}/{name}', wt, a.branch])
        if rc:
            return None, 'git worktree add failed: ' + out.strip()[-300:]
    ready = os.path.join(wt, a.agent_dir, '.targets', name) if a.agent_dir else wt
    deadline = time.time() + a.ready_timeout
    while not os.path.exists(ready):
        if time.time() > deadline:
            return None, f'workspace target not provisioned: {ready}'
        time.sleep(5)
    return wt, None


def provision(a, wt, n):
    """Bind the lane checkout to its Studio workspace: Claude Code MCP config, Ghostwriter target,
    tree pushed to the workspace. Skipped when .mcp.json already names the MCP server."""
    name = f'{a.prefix}-{n}'
    mcp = os.path.join(wt, '.mcp.json')
    try:
        if a.mcp_server in json.load(open(mcp))['mcpServers']:
            return None
    except Exception:
        pass
    agent = os.path.join(wt, a.agent_dir)
    sierra = os.path.join(agent, 'node_modules', '.bin', 'sierra')
    if not os.path.exists(sierra):
        return f'sierra CLI missing at {sierra}'
    src = os.path.join(a.repo, a.agent_dir, '.composer', '.gitignore')
    if os.path.exists(src):
        sh(['cp', src, os.path.join(agent, '.composer', '.gitignore')])
    steps = [
        ('setup-mcp', [sierra, 'setup-mcp', name, '--mcp-client', 'claude-code', '--mcp-server-name', a.mcp_server]),
        ('init', [sierra, 'ghostwriter', 'init', name]),
        ('pull', [sierra, 'ghostwriter', 'pull']),
        ('restore', ['git', '-C', wt, 'checkout', '--', os.path.join(a.agent_dir, '.composer')]),
        ('lint', [sierra, 'ghostwriter', 'lint']),
        ('push', [sierra, 'ghostwriter', 'push']),
        ('pull2', [sierra, 'ghostwriter', 'pull']),
        ('restore2', ['git', '-C', wt, 'checkout', '--', os.path.join(a.agent_dir, '.composer', 'root-store-schema.json')]),
    ]
    for title, cmd in steps:
        log(n, 'provision', title)
        rc, out = sh(cmd, cwd=agent)
        if rc:
            return f'provision {title} failed: ' + out.strip()[-300:]
    return None


def open_workspace(a, wt, n):
    """Open the worktree as a Herdr workspace (reuse it if already open); return (workspace_id, pane_id, err)."""
    label = f'{a.prefix.upper()} #{n}'
    lst = herdr('worktree', 'list')
    for w in lst.get('worktrees', []) if lst['ok'] else []:
        if w.get('path') == wt and w.get('open_workspace_id'):
            wid = w['open_workspace_id']
            panes = herdr('pane', 'list', '--workspace', wid)
            free = [p for p in panes.get('panes', []) if panes['ok'] and p.get('agent_status') in (None, 'unknown')]
            if not free:
                return wid, None, f'workspace {wid} already open with an agent in every pane'
            return wid, free[0]['pane_id'], None
    r = herdr('worktree', 'open', '--path', wt, '--label', label, '--no-focus')
    if not r['ok']:
        return None, None, 'worktree open failed: ' + str(r.get('error'))
    return r['workspace']['workspace_id'], r['root_pane']['pane_id'], None


def screen(name, lines=40):
    r = herdr('agent', 'read', name, '--source', 'visible', '--lines', str(lines))
    return r.get('text') or r.get('content') or json.dumps(r)


def start_agent(a, name, pane_id):
    args = ['--model', a.model, '--effort', a.effort, '--permission-mode', a.permission, *a.claude_args]
    r = herdr('agent', 'start', name, '--kind', 'claude', '--pane', pane_id, '--timeout', '60000', '--', *args)
    if r['ok']:
        return None
    if r.get('code') != 'agent_not_ready':
        return 'agent start failed: ' + str(r.get('error'))
    # Claude's one-time «Bypass Permissions mode» acceptance: move to «Yes, I accept» and confirm.
    s = screen(name)
    if re.search(r'(?i)bypass permissions', s) and re.search(r'(?i)yes, i accept', s):
        herdr('agent', 'send-keys', name, 'down'); time.sleep(0.5)
        herdr('agent', 'send-keys', name, 'enter')
        w = herdr('agent', 'wait', name, '--until', 'idle', '--timeout', '30000')
        if w['ok']:
            return None
    return 'agent blocked at startup: ' + s.strip()[-300:]


def send_prompt(a, name, prompt):
    r = herdr('agent', 'prompt', name, prompt)
    if not r['ok']:
        return 'prompt failed: ' + str(r.get('error'))
    w = herdr('agent', 'wait', name, '--until', 'working', '--timeout', '20000')
    if w['ok']:
        return None
    # A slash prompt can stay in the input under the command menu; one more Enter submits it.
    if prompt.split()[0] in screen(name):
        herdr('agent', 'send-keys', name, 'enter')
        w = herdr('agent', 'wait', name, '--until', 'working', '--timeout', '20000')
        if w['ok']:
            return None
    return 'prompt not picked up: ' + screen(name).strip()[-300:]


def spawn(a, n):
    name = f'{a.prefix}-{n}'
    wt, err = ensure_worktree(a, n)
    if err:
        return {'issue': n, 'ok': False, 'error': err}
    log(n, 'worktree ready', wt)
    if a.provision:
        err = provision(a, wt, n)
        if err:
            return {'issue': n, 'ok': False, 'error': err}
    wid, pane, err = open_workspace(a, wt, n)
    if err:
        return {'issue': n, 'ok': False, 'workspace_id': wid, 'error': err}
    log(n, 'herdr workspace', wid, 'pane', pane)
    err = start_agent(a, name, pane)
    if err:
        return {'issue': n, 'ok': False, 'workspace_id': wid, 'pane_id': pane, 'error': err}
    err = send_prompt(a, name, a.prompt.format(n=n))
    if err:
        return {'issue': n, 'ok': False, 'workspace_id': wid, 'pane_id': pane, 'agent': name, 'error': err}
    log(n, 'working')
    return {'issue': n, 'ok': True, 'workspace_id': wid, 'pane_id': pane, 'agent': name, 'cwd': wt}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('issues', nargs='+', help='issue numbers')
    ap.add_argument('--repo', required=True, help='main checkout, e.g. /Users/stan/code/BBVA')
    ap.add_argument('--branch', required=True, help='batch branch the lane branches fork from')
    ap.add_argument('--prefix', default='opp', help='lane name prefix: worktree, branch suffix, Studio workspace and Herdr agent are <prefix>-<n>')
    ap.add_argument('--owner', default='stan', help='branch namespace: <owner>/<prefix>-<n>')
    ap.add_argument('--worktrees', default='.claude/worktrees', help='worktree dir relative to --repo')
    ap.add_argument('--agent-dir', default='agents/openpay', help='agent dir whose .targets/<name> marks the hook done; empty to skip the wait')
    ap.add_argument('--provision', action='store_true', help='also run setup-mcp and bind Ghostwriter to the lane workspace (Cobranzas)')
    ap.add_argument('--mcp-server', default='sierra-base', help='MCP server name setup-mcp writes for claude-code')
    ap.add_argument('--prompt', default='/sierra start work on openpay issue #{n}', help='opening prompt, {n} = issue number')
    ap.add_argument('--model', default='fable', help='claude --model value')
    ap.add_argument('--effort', default='high', choices=['low', 'medium', 'high', 'max'])
    ap.add_argument('--permission', default='bypassPermissions', help='claude --permission-mode value')
    ap.add_argument('--claude-args', nargs=argparse.REMAINDER, default=[], help='extra claude flags, after --claude-args')
    ap.add_argument('--ready-timeout', type=int, default=600, help='seconds to wait for the hook per lane')
    a = ap.parse_args()
    st = herdr('status', '--json')
    if not st['ok'] and 'running' not in json.dumps(st):
        sys.exit('herdr server not reachable: ' + str(st.get('error')))
    for n in a.issues:
        print(json.dumps(spawn(a, n)), flush=True)


if __name__ == '__main__':
    main()
