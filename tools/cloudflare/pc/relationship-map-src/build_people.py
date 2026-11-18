"""Wikidataの人物(people_wd.jsonl)を、人ごとにまとめて people.json にする。行の形: [Q番号, 英語名, 日本語名, [[会社名, 役割], ...]]
出力: web/people.json と ../../../output/people.json (公開は Artifact の files で people.json として添付)"""
import json, os, sys
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
by = {}
f = os.path.join(S, 'people_wd.jsonl')
if os.path.exists(f):
    for ln in open(f, encoding='utf-8'):
        try:
            e = json.loads(ln)
        except Exception:
            continue
        p = by.setdefault(e['p'], {'en': e['en'], 'ja': e.get('ja', ''), 'sl': e.get('sl', 0), 'c': []})
        if [e['c'], e['role']] not in p['c'] and len(p['c']) < 8:
            p['c'].append([e['c'], e['role']])
intro = {}
_fi = os.path.join(S, 'people_intro.json')
if os.path.exists(_fi):
    intro = json.load(open(_fi, encoding='utf-8'))
rows = []
for q, v in sorted(by.items(), key=lambda kv: -kv[1]['sl']):
    it = intro.get(q, {})
    rows.append([q, v['en'], v['ja'], v['c'], it.get('d', ''), it.get('x', ''), it.get('w', ''), it.get('t', '')])
out = {'built': __import__('datetime').date.today().isoformat(), 'rows': rows}
for d in (os.path.join(S, 'web'), os.path.join(S, '..', '..', '..', 'output')):
    os.makedirs(d, exist_ok=True)
    json.dump(out, open(os.path.join(d, 'people.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('人物', len(rows))
