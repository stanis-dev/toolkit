#!/usr/bin/env python3
"""Builds test/fixture/ from the live pages dir, read only: a handful of issues per agent with their cards, step
answers, status files, stage and run logs, one recorded resolution log, cost ledgers, sequences and batches. Status
files are made safe on the way: no pid, no working state, worktrees under @REPO@ (the test's own fake repo).

  make_fixture.py [--live <pages dir>]"""
import json, os, re, shutil, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'plugin', 'skills', 'sierra', 'scripts'))
import paths  # noqa: E402

LIVE = sys.argv[sys.argv.index('--live') + 1] if '--live' in sys.argv else os.path.expanduser('~/.claude/bbva-issues')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixture')
PICK = {'hipotecarios': ['296', '297', '300', '301', '302', '303', '304'], 'cobranzas': ['321', '366', '446', '447', '448'],
        'openpay': ['199', '206', '209', '213', '223']}
EXTRA_ISSUES = {'hipotecarios': ['240', '241', '242', '243', '244'], 'cobranzas': [], 'openpay': []}


def safe(obj):
    if isinstance(obj, dict):
        if obj.get('state') == 'working':
            obj.update(state='failed', error=obj.get('error') or 'process gone')
        for k in ('pid', 'pi'):
            if k in obj:
                obj[k] = 0
        for k in ('worktree',):
            if isinstance(obj.get(k), str):
                obj[k] = re.sub(r'^.*?/\.claude/worktrees/', '@REPO@/.claude/worktrees/', obj[k])
        for v in obj.values():
            safe(v)
    elif isinstance(obj, list):
        for v in obj:
            safe(v)
    return obj


def copy(src, dst, json_safe=False):
    if not os.path.exists(src):
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if json_safe:
        json.dump(safe(json.load(open(src, encoding='utf-8'))), open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    else:
        shutil.copy(src, dst)


shutil.rmtree(OUT, ignore_errors=True)
for agent, nums in PICK.items():
    s, d = paths.agent(LIVE, agent), paths.agent(OUT, agent)
    os.makedirs(os.path.join(d, 'issues'), exist_ok=True)
    for n in nums + EXTRA_ISSUES[agent]:
        copy(paths.issue(s, n), paths.issue(d, n))
        copy(paths.card(s, n), paths.card(d, n))
        for step in ('analysis', 'strategy', 'context', 'resolve', 'setup'):
            for ext in ('json', 'md', 'stage.json', 'runs.json'):
                copy(paths.step_file(s, n, step, ext), paths.step_file(d, n, step, ext))
            copy(paths.status(s, n, step), paths.status(d, n, step), json_safe=True)
        copy(paths.cost(s, n), paths.cost(d, n))
        copy(paths.chain(s, n), paths.chain(d, n), json_safe=True)
    for f in ('batches.json', 'sync.status.json'):
        copy(f'{s}/{f}', f'{d}/{f}', json_safe=True)
    for b in paths.batch_ids(s):
        copy(paths.batch_file(s, b, 'status.json'), paths.batch_file(d, b, 'status.json'), json_safe=True)
h = paths.agent(LIVE, 'hipotecarios')
copy(os.path.join(paths.runs(h, '304', 'resolve'), 'out.jsonl'), os.path.join(paths.runs(paths.agent(OUT, 'hipotecarios'), '304', 'resolve'), 'out.jsonl'))
for f in ('exclude.json',):
    copy(os.path.join(LIVE, f), os.path.join(OUT, f))
print('fixture in', OUT, sum(len(fs) for _, _, fs in os.walk(OUT)), 'files')
