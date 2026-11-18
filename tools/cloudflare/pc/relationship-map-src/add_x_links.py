"""各社の相関図の人物に、Xの最近の発信(短い抜粋+元の投稿へのリンク)を足す。元: watch.sqlite の 発信(X)(Chromeで読んだ投稿)。
人物ごとに新しい順に最大2件。何度実行しても同じ結果になる。
使い方: python -I add_x_links.py [ページのファイル]   (既定: output\\relationship-maps.html)"""
import json, os, re, sqlite3, sys
P = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\yumat\.claude\output\relationship-maps.html'
w = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'watch.sqlite'))
ev = {}
for src, ts, title, url in w.execute("select src,ts,title,url from events where kind='発信(X)' and ts>='2026-08-01' order by ts desc"):
    m = re.match(r'X\(@(.+)\)', src or '')
    if not m:
        continue
    h = m.group(1).lower()
    tx = title.split(': ', 1)[1] if ': ' in title else title
    tx = re.sub(r'\s+', ' ', tx).strip()
    if len(ev.setdefault(h, [])) < 2 and tx:
        ev[h].append((ts[5:10], tx[:48] + ('…' if len(tx) > 48 else ''), url))
lines = open(P, encoding='utf-8').read().split('\n')
out = []
i = 0
added = blocks = 0
while i < len(lines):
    ln = lines[i]
    out.append(ln)
    if ln.startswith('const X={'):
        try:
            X = json.loads(ln[len('const X='):].rstrip(';'))
        except Exception:
            i += 1
            continue
        # この後の LINKS の文の終わりを探す
        j = next((k for k in range(i + 1, i + 10) if lines[k].startswith('const LINKS=')), None)
        if j is None:
            i += 1
            continue
        e = j
        if not lines[e].rstrip().endswith('};'):
            while not lines[e].rstrip().endswith('};'):
                e += 1
        items = []
        for pid, h in X.items():
            for d, tx, url in ev.get((h or '').lower(), []):
                items.append([pid, '最近の発信(X) %s: %s' % (d, tx), url])
        # 前回の追加行があれば除く
        nxt = e + 1
        old = lines[nxt].startswith('/*XQ*/')
        for k in range(i + 1, e + 1):
            out.append(lines[k])
        if items:
            out.append('/*XQ*/(function(){const q=%s;q.forEach(function(r){(LINKS[r[0]]=LINKS[r[0]]||[]).push([r[1],r[2]])})})();' % json.dumps(items, ensure_ascii=False))
            added += len(items)
            blocks += 1
        i = e + 2 if old else e + 1
        continue
    i += 1
open(P, 'w', encoding='utf-8').write('\n'.join(out))
print('Xの発信リンクを足した', added, '件(', blocks, '社の図)')
