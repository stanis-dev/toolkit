#!/usr/bin/env python3
"""Render index.html from state.json + data/*.json. Edit state.json, rerun; never hand-edit index.html.
runs[]: role = baseline (fixed reference: the 10/09 suite + its follow-ups) | now (latest suite + follow-ups) | history (kept, not shown).
A sim's pill in each role is its LATEST run in that role (run ids are ULIDs, so max(id) = most recent) - runs are never accumulated (Stan, 11/09).
`suite: true` marks the full run in each role; the `now` suite defines which sims exist. `results` = runset.py --failed list for replay links. `fix` is informational.
Buckets in state.json hold only sims that are red now; a sim at 100 % now lands in Resolved (if it was ever red or annotated) or Green."""
import json, re, html, pathlib
D = pathlib.Path(__file__).parent
S = json.load(open(D/'state.json'))
for r in S['runs']: r['data'] = json.load(open(D/'data'/r['file'])); r['by'] = {t['name']: t for t in r['data']['tests']}
def role(x): return [r for r in S['runs'] if r.get('role') == x]
base, now = role('baseline'), role('now')
now_suite = next(r for r in now if r.get('suite')); base_suite = next(r for r in base if r.get('suite'))
groups = json.load(open(D/'data/groups.json'))
lst = {t['name']: t for t in json.load(open(D/'data/list.json'))}
AG = 'https://bbva.sierra.ai/agents/01KT4M480V7W2KHXRE6REPRVDC/simulations/runs/'
replays = {}
for r in S['runs']:
    if not r.get('results'): continue
    meta2name = {t['testId']: t['name'] for t in r['data']['tests']}; m = {}
    for line in open(D/'data'/r['results']):
        p = line.split()
        if len(p) >= 3 and p[0] == 'FAILED': m.setdefault(meta2name.get(p[1]), p[2].replace('replaytestresult-', ''))
    replays[r['id']] = m
esc = lambda s: html.escape(str(s or ''))
def latest(runs, n):
    rs = [r for r in runs if n in r['by']]
    return max(rs, key=lambda r: r['id']) if rs else None
def score(runs, n):
    r = latest(runs, n)
    if not r: return 0, 0, [], ''
    t = r['by'][n]
    return t['passed'], t['total'], list(t['statusDetails']), r['label']
def cls(p, n): return 'ok' if n and p == n else 'ko' if p == 0 else 'flaky'
def pill(lab, p, n, run=''): return f'<span class="pill {lab} {cls(p, n)}" title="{esc(lab)} · {esc(run)}">{p} / {n}</span>' if n else f'<span class="pill {lab} none" title="{lab}">—</span>'
RESOLVED, GREEN, UNATTR = 'Resolved', 'Green', 'Red now, not yet attributed'
rows = []
names = list(now_suite['by']) + [n for n, st in S['sims'].items() if st.get('removed') and n not in now_suite['by']]
for n in names:
    st = S['sims'].get(n, {})
    bp, bn, bj, brun = score(base, n); np_, nn, nj, nrun = score(now, n)
    if st.get('removed'): b = RESOLVED
    elif np_ == nn: b = RESOLVED if (st or bp < bn) else GREEN
    else: b = st.get('bucket', UNATTR)
    links = [(r['label'], r['id'], replays[r['id']][n]) for r in now + base if r['id'] in replays and replays[r['id']].get(n)] + [(r['label'], r['id'], None) for r in (latest(now, n), latest(base, n)) if r and not replays.get(r['id'], {}).get(n)]
    rows.append(dict(name=n, id=lst.get(n, {}).get('id', ''), group=groups.get(lst.get(n, {}).get('id', ''), '—'), bucket=b, bp=bp, bn=bn, np=np_, nn=nn, brun=brun, nrun=nrun,
                     removed=st.get('removed', False), cause=st.get('cause', ''), action=st.get('action', ''), judge=list(dict.fromkeys(nj + bj)), links=links))
buckets = S['buckets'] + [{'name': UNATTR, 'status': 'to attribute', 'kind': 'armed'}, {'name': RESOLVED, 'status': 'no longer red', 'kind': 'done'}, {'name': GREEN, 'status': '', 'kind': 'ok'}]
by = {b['name']: [] for b in buckets}
for r in rows: by[r['bucket']].append(r)
for b in by: by[b].sort(key=lambda r: (r['nn'] and r['np'] / r['nn'], r['name']))
live = [r for r in rows if r['nn']]; red = sum(1 for r in live if r['np'] < r['nn']); green = len(live) - red
base_live = [n for n in base_suite['by']]; base_red = sum(1 for n in base_live if score(base, n)[0] < score(base, n)[1])
def by_id(b): return re.sub(r'[^a-z0-9]+', '-', b['name'].lower()).strip('-')
def row_html(r):
    pills = pill('baseline', r['bp'], r['bn'], r['brun']) + ('<span class="pill now rm" title="now">removed</span>' if r['removed'] else pill('now', r['np'], r['nn'], r['nrun']))
    head = (f'<div class="rw" id="s-{esc(r["id"])}"><div class="scs">{pills}</div><div class="nm">{esc(r["name"])}<span class="crumb"><i class="ti ti-folder"></i>{esc(r["group"])}</span></div>'
            f'<div class="cause">{esc(r["cause"])}</div></div>')
    links = ''.join(f'<a href="{AG}{rid}?resultId={res}">Replay · {esc(lab)}</a>' if res else f'<a href="{AG}{rid}">Run · {esc(lab)}</a>' for lab, rid, res in r['links']) + f'<a href="{AG}{now_suite["id"]}">Suite run</a>'
    judge = ''.join(f'<li>{esc(j)}</li>' for j in r['judge'][:6])
    act = f'<div class="act"><span class="k">next</span>{esc(r["action"])}</div>' if r['action'] else ''
    return f'<details class="sim"><summary>{head}</summary><div class="det">{act}<div class="k">judge</div><ul>{judge}</ul><div class="links">{links}</div></div></details>'
def bucket_html(b):
    rs = by[b['name']]
    if not rs: return ''
    lab = f'<span class="lab {b["kind"]}">{esc(b["status"])}</span>' if b['status'] else ''
    if b['kind'] in ('ok', 'done'):
        hint = 'never red · click to list' if b['kind'] == 'ok' else 'fixed or aligned since the baseline · click to list'
        inner = ''.join(row_html(r) for r in rs) if b['kind'] == 'done' else '<div class="glist">' + ''.join(f'<div class="g"><span class="sc ok">{r["np"]} / {r["nn"]}</span><span>{esc(r["name"])}</span><span class="crumb"><i class="ti ti-folder"></i>{esc(r["group"])}</span></div>' for r in sorted(rs, key=lambda r: (r['group'], r['name']))) + '</div>'
        return f'<section class="card fold" id="b-{by_id(b)}"><details class="greens"><summary><h3>{esc(b["name"])}<span class="cnt">{len(rs)}</span>{lab}</h3><span class="hint">{hint}</span></summary>{inner}</details></section>'
    return f'<section class="card" id="b-{by_id(b)}"><h3>{esc(b["name"])}<span class="cnt">{len(rs)}</span>{lab}</h3>' + ''.join(row_html(r) for r in rs) + '</section>'
side = ''.join(
    f'<div class="grp{" open" if b["kind"] not in ("ok", "done") else ""}" data-g="{by_id(b)}"><div class="row"><i class="ti ti-chevron-right"></i><span class="nm">{esc(b["name"])}</span><span class="cnt">{len(by[b["name"]])}</span></div>'
    + '<div class="items">' + ''.join(f'<a class="it" href="#s-{esc(r["id"])}"><span class="num {"rm" if r["removed"] else cls(r["np"], r["nn"])}">{"—" if r["removed"] else f"{r["np"]}/{r["nn"]}"}</span><span>{esc(r["name"])}</span></a>' for r in by[b['name']]) + '</div></div>'
    for b in buckets if by[b['name']])
def runs_html(rs): return ' · '.join(f'<a href="{AG}{r["id"]}">{esc(r["label"])}</a>' for r in rs)
page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(S["title"])}</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tabler-icons/3.31.0/tabler-icons.min.css">
<style>
:root{{color-scheme:light dark;--font-sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;--font-mono:ui-monospace,SFMono-Regular,Menlo,monospace;--radius:8px;
--text-primary:#1f1f1d;--text-secondary:#5f5e5a;--text-muted:#888780;--surface-0:#f5f4f0;--surface-1:#f1efe8;--surface-2:#ffffff;--border:rgba(0,0,0,.12);--border-strong:rgba(0,0,0,.22);
--text-danger:#a32d2d;--bg-danger:#fcebeb;--text-success:#3b6d11;--bg-success:#eaf3de;--text-warning:#854f0b;--bg-warning:#faeeda;--text-accent:#185fa5;--bg-accent:#e6f1fb}}
@media (prefers-color-scheme:dark){{:root{{--text-primary:#ecebe6;--text-secondary:#b4b2a9;--text-muted:#888780;--surface-0:#1c1c1a;--surface-1:#262624;--surface-2:#30302e;--border:rgba(255,255,255,.14);--border-strong:rgba(255,255,255,.26);
--text-danger:#f09595;--bg-danger:#501313;--text-success:#97c459;--bg-success:#173404;--text-warning:#fac775;--bg-warning:#412402;--text-accent:#85b7eb;--bg-accent:#0c447c}}}}
html,body{{margin:0;padding:0;background:var(--surface-0);color:var(--text-primary);font-family:var(--font-sans);font-size:14.5px;line-height:1.4}} a{{color:inherit}}
.app{{--side:300px;display:grid;grid-template-columns:var(--side) 16px minmax(0,1fr);padding:16px;max-width:1240px;margin:0 auto}}
nav.side{{position:sticky;top:16px;align-self:start;max-height:calc(100vh - 32px);overflow:auto}}
.side .hd{{padding:0 10px 8px}} .side .hd h1{{margin:0;font-size:11.5px;font-weight:500;letter-spacing:.02em;text-transform:uppercase;color:var(--text-muted)}}
.side .grp{{margin-bottom:4px}} .side .grp>.row{{display:grid;grid-template-columns:14px 1fr auto;gap:6px;align-items:center;padding:5px 10px;border-radius:var(--radius);cursor:pointer}}
.side .grp>.row:hover{{background:var(--surface-1)}} .side .grp>.row .ti{{font-size:13px;color:var(--text-muted);transition:transform .18s ease}} .side .grp.open>.row .ti{{transform:rotate(90deg)}}
.side .grp>.row .nm{{font-weight:500;font-size:13.5px}} .side .cnt{{font-family:var(--font-mono);font-size:12px;color:var(--text-secondary)}}
.side .items{{display:none;padding:2px 0 2px 14px}} .side .grp.open .items{{display:block}}
.side .it{{display:grid;grid-template-columns:44px 1fr;gap:6px;align-items:start;padding:4px 10px;border-radius:var(--radius);text-decoration:none;font-size:13px;line-height:1.35;color:var(--text-secondary)}}
.side .it:hover{{background:var(--surface-1)}} .side .it.active{{background:var(--surface-2);box-shadow:inset 0 0 0 1px var(--border);color:var(--text-primary)}}
.side .it .num{{font-family:var(--font-mono);font-size:12px}} .num.ko{{color:var(--text-danger)}} .num.ok{{color:var(--text-success)}} .num.flaky{{color:var(--text-warning)}} .num.rm{{color:var(--text-muted)}}
main{{min-width:0}} .card{{background:var(--surface-2);border:1px solid var(--border);border-radius:12px;overflow:hidden;padding:0 0 4px}} .card+.card{{margin-top:12px}} .card.fold{{opacity:.85}}
.card h3{{margin:0;padding:10px 14px 6px;font-size:13.5px;font-weight:500;display:flex;align-items:center;gap:8px}} .card h3 .cnt{{font-family:var(--font-mono);font-size:12px;color:var(--text-secondary)}}
.lab{{font-size:11px;font-weight:500;letter-spacing:.02em;text-transform:uppercase;padding:1px 7px;border-radius:10px;border:1px solid var(--border)}}
.lab.go{{color:var(--text-accent);background:var(--bg-accent);border-color:transparent}} .lab.armed{{color:var(--text-warning);background:var(--bg-warning);border-color:transparent}} .lab.decide{{color:var(--text-secondary);background:var(--surface-1)}} .lab.flaky{{color:var(--text-warning)}} .lab.done{{color:var(--text-success);background:var(--bg-success);border-color:transparent}}
.top{{display:flex;flex-wrap:wrap;gap:8px 22px;align-items:baseline;padding:12px 14px}} .top .big{{font-size:22px;font-weight:500;font-family:var(--font-mono)}} .top .big b{{color:var(--text-danger);font-weight:500}} .top .big .g{{color:var(--text-success)}} .top .meta{{color:var(--text-secondary);font-size:13px}} .top .meta a{{color:var(--text-accent)}} .top .runs{{flex-basis:100%;font-size:12px;color:var(--text-muted)}} .top .runs a{{color:var(--text-muted)}}
.rw{{display:grid;grid-template-columns:150px minmax(220px,1fr) minmax(0,1.6fr);gap:10px;align-items:start;padding:7px 14px;border-top:1px solid var(--border)}}
.scs{{display:flex;gap:6px;flex-wrap:wrap;padding-top:1px}}
.pill{{display:inline-flex;align-items:baseline;gap:5px;font-family:var(--font-mono);font-size:12.5px;padding:1px 8px;border-radius:10px;border:1px solid var(--border);white-space:nowrap}} .pill .pl{{font-family:var(--font-sans);font-size:10.5px;text-transform:uppercase;letter-spacing:.03em;color:var(--text-muted)}}
.pill.ok{{color:var(--text-success);background:var(--bg-success);border-color:transparent}} .pill.ko{{color:var(--text-danger);background:var(--bg-danger);border-color:transparent}} .pill.flaky{{color:var(--text-warning);background:var(--bg-warning);border-color:transparent}} .pill.none,.pill.rm{{color:var(--text-muted)}} .pill.baseline{{opacity:.4}}
.rw .nm{{font-weight:500;font-size:13.5px}} .crumb{{display:block;font-weight:400;font-size:12px;color:var(--text-muted);margin-top:1px}} .crumb .ti{{font-size:12px;margin-right:4px;vertical-align:-1px}}
.rw .cause{{font-size:13px;color:var(--text-secondary)}}
details.sim>summary{{list-style:none;cursor:pointer}} details.sim>summary::-webkit-details-marker{{display:none}} details.sim[open]>summary .rw,.rw.hl{{background:var(--surface-1)}}
.det{{padding:4px 14px 10px 174px;font-size:13px;color:var(--text-secondary)}} .det .k{{font-family:var(--font-mono);font-size:11px;text-transform:uppercase;letter-spacing:.03em;color:var(--text-muted);margin:6px 0 2px}}
.det .act{{color:var(--text-primary)}} .det .act .k{{display:inline-block;margin:0 8px 0 0}} .det ul{{margin:0;padding-left:18px}} .det li{{margin:2px 0}} .det .links a{{color:var(--text-accent);margin-right:12px}}
details.greens>summary{{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;padding-right:14px}} details.greens>summary::-webkit-details-marker{{display:none}} .hint{{font-size:12px;color:var(--text-muted)}}
.glist{{columns:2;column-gap:24px;padding:4px 14px 8px}} .glist .g{{break-inside:avoid;display:grid;grid-template-columns:44px 1fr;gap:8px;padding:3px 0;font-size:13px}} .glist .g .sc{{font-family:var(--font-mono);font-size:12px;color:var(--text-success)}} .glist .g .crumb{{grid-column:2;margin-top:-2px}}
@media (max-width:760px){{.app{{grid-template-columns:1fr;padding:10px}}nav.side{{position:static;max-height:none}}.rw{{grid-template-columns:1fr}}.det{{padding-left:14px}}.glist{{columns:1}}}}
</style></head><body>
<div class="app">
<nav class="side"><div class="hd"><h1>{esc(S["title"])}</h1></div>{side}</nav>
<div></div>
<main>
<section class="card"><div class="top"><span class="big"><b>{red}</b></span><span class="big"><span class="g">{round(100 * green / len(live))} %</span></span><span class="meta" title="{green} of {len(live)} simulations at 100 % in their latest run">pass rate · baseline {round(100 * (len(base_live) - base_red) / len(base_live))} %</span></div></section>
{''.join(bucket_html(b) for b in buckets)}
</main></div>
<script>
document.querySelectorAll('.side .grp>.row').forEach(function(r){{r.addEventListener('click',function(){{r.parentNode.classList.toggle('open')}})}});
function go(){{var id=location.hash.slice(1);if(!id)return;var el=document.getElementById(id);if(!el)return;var d=el.closest('details');while(d){{d.open=true;d=d.parentElement&&d.parentElement.closest('details')}}document.querySelectorAll('.rw.hl').forEach(function(x){{x.classList.remove('hl')}});el.classList.add('hl');document.querySelectorAll('.side .it').forEach(function(a){{a.classList.toggle('active',a.getAttribute('href')==='#'+id)}});el.scrollIntoView({{block:'center'}})}}
window.addEventListener('hashchange',go);go();
</script></body></html>'''
(D/'index.html').write_text(page)
print('rendered', len(rows), 'rows;', red, 'red now,', green, 'at 100 %;', {b: len(by[b]) for b in by if by[b]})
