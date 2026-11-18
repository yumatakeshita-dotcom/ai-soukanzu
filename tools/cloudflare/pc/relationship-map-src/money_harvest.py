"""相関図(深掘りした会社の図)の、出資・資金の線を、構造化して取り出す。 出力: money_flow.json
行: {src, dst, kind(出資|出資(双方向)|買収), label, year, note(図の出どころ説明)}"""
import glob, importlib, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import newco_data9 as nd
REC = []
orig = nd.deep
def cap(ticker, name, minyear, note, items, edges, center_desc):
    REC.append((ticker, name, note, items, edges))
    return orig(ticker, name, minyear, note, items, edges, center_desc)
nd.deep = cap
for f in sorted(glob.glob('newco_data*.py')):
    m = os.path.basename(f)[:-3]
    if m in ('newco_data', 'newco_data9'):
        continue
    try:
        importlib.import_module(m)
    except Exception as e:
        print('skip', m, str(e)[:80])
rows = []
for ticker, name, note, items, edges in REC:
    byid = {n['id']: n for n, _ in items}
    for n, _ in items:
        if n['kind'] == 'i':
            rows.append({'src': n['name'], 'dst': name, 'kind': '出資', 'label': n.get('role') or '', 'year': n.get('from'), 'desc': n.get('desc', ''), 'note': note})
    for e in edges:
        if len(e) >= 3 and e[2] in ('invest2', 'invest'):
            a, b = e[0], e[1]
            an = name if a == 'co' else byid.get(a, {}).get('name', a)
            bn = name if b == 'co' else byid.get(b, {}).get('name', b)
            d = byid.get(b if a == 'co' else a, {})
            rows.append({'src': an, 'dst': bn, 'kind': '出資', 'label': (e[3] if len(e) > 3 else '') or d.get('role', ''), 'year': (e[4] if len(e) > 4 else None) or d.get('from'), 'desc': d.get('desc', ''), 'note': note})
seen, out = set(), []
for r in rows:
    k = (r['src'], r['dst'])
    if k in seen:
        continue
    seen.add(k); out.append(r)
json.dump(out, open('money_flow.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('会社', len(REC), '出資の線', len(out))
for r in out[:12]: print(r['src'], '→', r['dst'], r['year'], r['label'], r['desc'][:50])
