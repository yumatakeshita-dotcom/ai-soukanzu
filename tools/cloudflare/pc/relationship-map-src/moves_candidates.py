"""ウォッチ(watch.sqlite)に貯まった「人材移籍」の出来事を、まだ見ていないものだけ、確認用の一覧(docs/moves_candidates.md)に書き出す。
 人が(私が)出典を確かめてから、moves_extra.json に足し、build_move_lab.py → embed_move_lab.py で公開ページに反映する。
 使い方: python moves_candidates.py"""
import json, os, sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
S = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(os.path.expanduser('~'), '.claude', 'data', 'watch.sqlite')
STATE = os.path.join(S, 'moves_candidates_seen.json')
OUT = os.path.join(os.path.dirname(os.path.dirname(S)), 'moves_candidates.md')
seen = set(json.load(open(STATE, encoding='utf-8'))) if os.path.exists(STATE) else set()
db = sqlite3.connect(W)
rows = db.execute("select id,ts,src,title,url from events where kind='人材移籍' order by ts desc limit 400").fetchall()
new = [r for r in rows if r[0] not in seen]
lines = ['# 人材移籍の候補(自動で拾ったもの。出典を確かめてから、移籍マップに足す)', '']
for id_, ts, src, title, url in new:
    lines.append('- %s [%s] %s — %s' % (ts[:10], src, title, url))
open(OUT, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
json.dump(sorted(seen | {r[0] for r in new}), open(STATE, 'w', encoding='utf-8'))
print('新しい候補', len(new), '件 →', OUT)
