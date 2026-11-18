"""x_queue_biz.json(企業家・スタートアップ関係)から、まだ読んでいない人の先頭 n 件のアカウントを出す。使い方: python x_next.py [n]"""
import json, os, sqlite3, sys
S = os.path.dirname(os.path.abspath(__file__))
n = int(sys.argv[1]) if len(sys.argv) > 1 else 9
w = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'watch.sqlite'))
have = {r[0].split('(@')[1][:-1].lower() for r in w.execute("select src from events where kind='発信(X)'") if '(@' in r[0]}
chk = {h.lower() for h in json.load(open(os.path.join(S, 'x_checked.json')))}
q = [o for o in json.load(open(os.path.join(S, 'x_queue_biz.json'), encoding='utf8')) if o['h'].lower() not in have | chk]
print(len(q)); print(' '.join(o['h'] for o in q[:n]))
