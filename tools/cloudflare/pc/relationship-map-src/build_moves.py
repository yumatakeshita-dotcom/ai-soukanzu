"""相関図(公開ページ内のデータ)の「出身(from)」「移籍先(moved)」の線から、人の移籍の一覧を作る。
 from: 人 a が、組織 b から center の会社へ来た   → b → center
 moved: 人 a が、center の会社から組織 b へ移った → center → b
年は、人のノードの from(入った年)/to(出た年)、線の since。わからないものは None。
使い方: python build_moves.py   (scratchpad の hub_edges.json を読み、moves.json を書く)"""
import json, os, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
SP = r'C:\Users\yumat\AppData\Local\Temp\claude\f0b3d5485105e630\ca60b507-9e00-4c2c-ba48-a67554d79e05\scratchpad'
d = json.load(open(os.path.join(SP, 'hub_edges.json'), encoding='utf-8'))['res']
names = {}
for k, v in d.items():
    for n in v.get('N', []):
        if n['kind'] in ('c', 'o', 'i'):
            names.setdefault(n['id'], n['name'])
SAME = {'Google Brain': 'Google DeepMind', 'DeepMind': 'Google DeepMind', 'Alphabet': 'Google DeepMind'}
def norm(n):
    return SAME.get(n, n)
out = []
errs = []
for k, v in d.items():
    if 'err' in v:
        errs.append((k, v['err'][:60])); continue
    N = {n['id']: n for n in v['N']}
    en = v.get('EN') or {}
    cn = names.get(v['center'], v['center'])
    for e in v['E']:
        p = N.get(e['a'])
        if not p or p['kind'] != 'p':
            continue
        o = N.get(e['b']); on = (o or {}).get('name') or names.get(e['b'])
        if not on:
            continue
        if e['k'] == 'from':
            a, b, y = on, cn, p.get('from')
        else:
            a, b, y = cn, on, p.get('to') or e.get('since') or (o or {}).get('from')
        a, b = norm(a), norm(b)
        if a == b:
            continue
        out.append({'p': p['name'], 'en': en.get(e['a']) or '', 'a': a, 'b': b, 'y': y, 'k': e['k'], 'src': k, 'role': p.get('role') or ''})
# 重複除去(人・元・先)
seen = {}
for m in out:
    key = (m['p'], m['a'], m['b'])
    if key not in seen or (not seen[key]['y'] and m['y']):
        seen[key] = m
res = list(seen.values())
json.dump(res, open(os.path.join(SP, 'moves.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('companies', len(d), 'errors', errs[:5], 'raw', len(out), 'unique', len(res), 'with year', sum(1 for m in res if m['y']))
print(collections.Counter(m['src'] for m in res).most_common(15))
