"""手元にあって、公開側(D1)に無い行だけを、D1へ足す(INSERT OR REPLACE のみ。他の行は消さない)。
他のセッションの sync_people.py が、D1の人物表を手元の版で丸ごと入れ替えて、あとから足した人物が消えたときの復旧用。
先に restore_from_d1.py で、手元を整えてから使う。 使い方: python -u push_missing_to_d1.py [--dry]"""
import json, os, re, sqlite3, subprocess, sys
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')
db = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite'))
TABLES = ['person', 'img', 'person_role', 'person_social']
q1 = lambda v: 'NULL' if v is None else "'" + str(v).replace("'", "''") + "'"


def d1(sql):
    p = subprocess.run('npx wrangler d1 execute houjin --remote --json --command "%s"' % sql, cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    t = p.stdout
    m = re.search(r'\[\s*\{\s*"results"', t)
    return json.loads(t[m.start():])[0]['results']


L = []
for t in TABLES:
    cols = [c[1] for c in db.execute('PRAGMA table_info(%s)' % t)]
    rows = d1('SELECT * FROM %s' % t)
    pk = 'key' if t == 'img' else 'q'
    remote = set(str(r.get(pk)) for r in rows)      # 主キー(q / key)が、D1に無い行だけを足す(D1側で直された行は、上書きしない)
    n = 0
    for r in db.execute('SELECT %s FROM %s' % (','.join(cols), t)):
        if str(r[cols.index(pk)]) not in remote:
            L.append('INSERT OR REPLACE INTO %s (%s) VALUES (%s);' % (t, ','.join(cols), ','.join(q1(x) for x in r)))
            n += 1
    print(t, 'D1', len(rows), '行 / D1に足す', n, flush=True)
if '--dry' in sys.argv or not L:
    sys.exit(0)
sql = os.path.join(SITE, 'push_missing.sql')
open(sql, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
p = subprocess.run('npx wrangler d1 execute houjin --remote --yes --file="' + sql.replace(chr(92), '/') + '"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
o = (p.stdout or '') + (p.stderr or '')
print('D1', 'OK' if p.returncode == 0 and 'ERROR' not in o else 'NG ' + o[-300:], len(L), '文', flush=True)
