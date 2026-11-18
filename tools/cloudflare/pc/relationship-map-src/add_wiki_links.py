"""各社の相関図の人物に、Wikipediaへのリンク(出典)を足す。英語名がWikipediaの記事と一致する人だけ(houjin.sqliteの person 表)。
すでにリンクがある人は、そのまま。何度実行しても同じ結果になる。
使い方: python -I add_wiki_links.py [ページのファイル]   (既定: output\\relationship-maps.html)"""
import json, os, sqlite3, sys, urllib.parse
P = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\yumat\.claude\output\relationship-maps.html'
db = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite'))
names = {}
dup = set()
for en, w, t in db.execute("select en,w,t from person where en<>'' and w<>'' and t<>''"):
    k = en.strip().lower()
    if k in names:
        dup.add(k)
    names[k] = (w, t)
for k in dup:
    names.pop(k, None)
lines = open(P, encoding='utf-8').read().split('\n')
added = total = 0
for i, ln in enumerate(lines):
    if not ln.startswith('const WIKI={'):
        continue
    j = next((k for k in range(i + 1, i + 4) if lines[k].startswith('const EN={')), None)
    if j is None:
        continue
    try:
        W = json.loads(ln[len('const WIKI='):].rstrip(';'))
        EN = json.loads(lines[j][len('const EN='):].rstrip(';'))
    except Exception:
        continue
    n0 = len(W)
    for pid, en in EN.items():
        if pid in W:
            continue
        hit = names.get((en or '').strip().lower())
        if hit:
            W[pid] = 'https://%s.wikipedia.org/wiki/%s' % (hit[0], urllib.parse.quote(hit[1].replace(' ', '_'), safe="_(),'!.-"))
    if len(W) > n0:
        lines[i] = 'const WIKI=' + json.dumps(W, ensure_ascii=False) + ';'
        added += len(W) - n0
    total += len(EN)
open(P, 'w', encoding='utf-8').write('\n'.join(lines))
print('Wikipediaへのリンクを足した人物', added, '/ 英語名のある人物', total)
