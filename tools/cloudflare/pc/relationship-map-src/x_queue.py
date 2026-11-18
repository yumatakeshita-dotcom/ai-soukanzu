"""有名度(Wikipediaの言語版の数)の高い順に、まだXを読んでいない人の一覧 x_queue.json を作る。読んだ印は watch.sqlite の発信(X)と x_checked.json(0件・古い投稿だった人も含む)。"""
import json, os, sqlite3
S = os.path.dirname(os.path.abspath(__file__))
fame = json.load(open(os.path.join(S, 'people_fame.json'), encoding='utf8'))
soc = json.load(open(os.path.join(S, 'people_social.json'), encoding='utf8'))
chk = set(json.load(open(os.path.join(S, 'x_checked.json'), encoding='utf8'))) if os.path.exists(os.path.join(S, 'x_checked.json')) else set()
w = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'watch.sqlite'))
have = {r[0].split('(@')[1][:-1].lower() for r in w.execute("select src from events where kind='発信(X)'") if '(@' in r[0]}
done = {x['h'].lower() for x in json.load(open(os.path.join(S, 'x_targets.json'), encoding='utf8'))}
h = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite'))
out = []
for q, v in soc.items():
    x = v.get('x')
    if not x or x.lower() in have | done | chk: continue
    r = h.execute('select en,ja from person where q=?', (q.lstrip('Q'),)).fetchone()
    out.append({'q': q, 'h': x, 'name': (r[0] or r[1]) if r else '', 'fame': fame.get(q, 0)})
out.sort(key=lambda o: -o['fame'])
json.dump(out, open(os.path.join(S, 'x_queue.json'), 'w', encoding='utf8'), ensure_ascii=False)
print(len(out)); print(' / '.join('%s(%s,%d)' % (o['h'], o['name'], o['fame']) for o in out[:60]))
