"""取得済みの人の最新投稿を読み直す順番を決める。
  python x_refresh.py next [n]     … 読み直す人を n 人(既定9。ブラウザの1バッチの上限)。最後に読んだ日が古い順、同じなら有名度が高い順
  python x_refresh.py mark h1 h2.. … 読んだ人に今日の日付を付ける(0件・古い投稿だった人も)
  python x_refresh.py status       … 読み直しの状況(何人・いちばん古い確認日)
対象は watch.sqlite に発信(X)がある人(=過去に新しい投稿が取れた人)と、x_checked.json にある人。状態は x_state.json。"""
import datetime as dt, json, os, sqlite3, sys
S = os.path.dirname(os.path.abspath(__file__))
ST = os.path.join(S, 'x_state.json')
state = json.load(open(ST, encoding='utf8')) if os.path.exists(ST) else {}
w = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'watch.sqlite'))
today = dt.date.today().isoformat()
hs = {}
for (src,) in w.execute("select distinct src from events where kind='発信(X)'"):
    if '(@' in src: hs[src.split('(@')[1][:-1]] = 1
last = {}
for src, ts in w.execute("select src, max(ts) from events where kind='発信(X)' group by src"):
    if '(@' in src: last[src.split('(@')[1][:-1].lower()] = ts[:10]
soc = json.load(open(os.path.join(S, 'people_social.json'), encoding='utf8'))
fame = json.load(open(os.path.join(S, 'people_fame.json'), encoding='utf8'))
hf = {v['x'].lower(): fame.get(q, 0) for q, v in soc.items() if v.get('x')}
for x in json.load(open(os.path.join(S, 'x_targets.json'), encoding='utf8')): hf.setdefault(x['h'].lower(), 99)
cmd = sys.argv[1] if len(sys.argv) > 1 else 'next'
if cmd == 'mark':
    for h in sys.argv[2:]: state[h.lower()] = today
    json.dump(state, open(ST, 'w', encoding='utf8'))
    print('記録', len(sys.argv) - 2, '人')
else:
    # 発信(X)に出てくる人だけが対象(投稿が古い・0件の人は、月1回程度の確認で足りるので別枠 stale)
    rows = sorted(hs, key=lambda h: (state.get(h.lower(), '0000'), -hf.get(h.lower(), 0)))
    if cmd == 'status':
        old = [state.get(h.lower(), '未確認') for h in rows]
        print('対象', len(rows), '人 / 未確認', sum(1 for o in old if o == '未確認'), '人 / いちばん古い確認日', min(old))
    else:
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 9
        print(' '.join(rows[:n]))
