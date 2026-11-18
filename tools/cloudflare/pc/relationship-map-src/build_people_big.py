"""people_big.jsonl(Wikidataから集めた人物)を、名前の先頭で振り分けた小さなファイル(pb/NNN.json)に分ける。検索したときに必要な1ファイルだけ読み込めるようにするため。
各ファイル: [[Q番号(数字), 英語名, 日本語名, 職業, 言語版の数], ...]  言語版の数が多い順。
使い方: python build_people_big.py"""
import json, os, re, sys, unicodedata
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
N = 100


def fold(s):
    s = unicodedata.normalize('NFKD', s or '').lower()
    return ''.join(c for c in s if not unicodedata.combining(c))


def toks(s):
    return [t for t in re.split(r'[^\w]+', fold(s)) if t and t != '_']


def key(t):
    cp = list(t)
    return ''.join(cp[:3]) if re.match(r'[a-z0-9]', t) else ''.join(cp[:2])


def h(k):
    v = 0
    b = k.encode('utf-16-le')
    for i in range(0, len(b), 2):
        v = (v * 31 + (b[i] | (b[i + 1] << 8))) & 0xFFFFFFFF
    return v % N


rows = {}
for ln in open(os.path.join(S, 'people_big.jsonl'), encoding='utf-8'):
    try:
        e = json.loads(ln)
    except Exception:
        continue
    q = e['q']
    old = rows.get(q)
    if old is None or e['sl'] > old[4]:
        rows[q] = [q, e['en'], e['ja'], e['o'], e['sl']]
print('人物', len(rows), flush=True)
sh = [[] for _ in range(N)]
for r in rows.values():
    ks = set()
    for t in toks(r[1]) + toks(r[2]):
        if len(t) >= 2 or not re.match(r'[a-z0-9]', t):
            ks.add(h(key(t)))
    for k in ks:
        sh[k].append(r)
tot = 0
META = json.dumps({'n': len(rows)})
for outdir in (os.path.join(S, 'web', 'pb'), os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(S))), 'output', 'pb')):
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, 'meta.json'), 'w').write(META)
    for i, rs in enumerate(sh):
        rs.sort(key=lambda r: -r[4])
        data = json.dumps(rs, ensure_ascii=False, separators=(',', ':'))
        open(os.path.join(outdir, '%03d.json' % i), 'w', encoding='utf-8').write(data)
        if outdir.endswith(os.path.join('web', 'pb')):
            tot += len(data.encode('utf-8'))
print('ファイル', N, '合計MB', round(tot / 1e6, 1), '最大KB', round(max(len(json.dumps(r, ensure_ascii=False)) for r in sh) / 1e3))
