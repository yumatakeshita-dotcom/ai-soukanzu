"""手元の houjin.sqlite から消えた人物データ(GAFAM・VCの人・関係者などを、あとから足した分)を、公開側(D1)から取り戻す。
理由: build_site_assets.py などが、手元の person / img / person_role ... を作り直すと、あとから足した行が消える。
その状態で sync_people.py を動かすと、D1 からも消えてしまうため、sync_people.py の前に、このスクリプトを必ず動かす。
使い方: python -u restore_from_d1.py        (D1を読むだけ。D1は変更しない)"""
import json, os, sqlite3, subprocess, sys
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')
db = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite'))
TABLES = ['person', 'img', 'person_role', 'person_social', 'person_quote', 'person_feed']


def d1(sql):
    p = subprocess.run('npx wrangler d1 execute houjin --remote --json --command "%s"' % sql, cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    t = p.stdout
    i = t.find('[')
    return json.loads(t[i:])[0]['results']


for t in TABLES:
    cols = [c[1] for c in db.execute('PRAGMA table_info(%s)' % t)]
    rows = d1('SELECT * FROM %s' % t)
    have = set(tuple(str(x) if x is not None else '' for x in r) for r in db.execute('SELECT %s FROM %s' % (','.join(cols), t)))
    add = 0
    for r in rows:
        tup = tuple(r.get(c) for c in cols)
        key = tuple(str(x) if x is not None else '' for x in tup)
        if key not in have:
            db.execute('INSERT OR REPLACE INTO %s (%s) VALUES (%s)' % (t, ','.join(cols), ','.join('?' * len(cols))), tup)
            have.add(key)
            add += 1
    db.commit()
    print(t, 'D1', len(rows), '行 / 手元に足した', add, flush=True)
