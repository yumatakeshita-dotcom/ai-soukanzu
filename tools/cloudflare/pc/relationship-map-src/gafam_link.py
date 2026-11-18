import json, os, sqlite3, subprocess, sys
for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(encoding='utf-8', errors='replace')
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')
db = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite'))
try:
    db.execute('ALTER TABLE mapco_people ADD COLUMN q TEXT')
except Exception:
    pass
if not db.execute("SELECT 1 FROM mapco_people WHERE slug='us_META' AND en='Adam Mosseri'").fetchone():
    db.execute("INSERT INTO mapco_people (slug,name,en,role,since,until,note) VALUES ('us_META','アダム・モセリ','Adam Mosseri','Instagram責任者','2018','','2018年にInstagramの責任者(CEO)に就任。')")
top = json.load(open(os.path.join(S, 'top100_data.json'), encoding='utf-8'))
by = {e['en'].lower(): e['q'].lstrip('Q') for e in top if e.get('q')}
gp = json.load(open(os.path.join(S, 'gafam_people.json'), encoding='utf-8'))
ALIAS = {'dina powell mccormick': 'Q3278769', 'daniel huttenlocher': 'Q1162007', 'andrew w. houston': 'Q5307199', 'john hennessy': 'Q92854', 'andrew ng': 'Q2846695', 'adam mosseri': 'Q56877012', 'robert m. kimmitt': 'Q822657', 'c.j. mahoney': 'Q38854983'}
for q, e in gp.items():
    by.setdefault(e['en'].lower(), q.lstrip('Q'))
for k, v in ALIAS.items():
    by[k] = v.lstrip('Q')
n = 0
rows = db.execute("SELECT rowid, slug, en FROM mapco_people WHERE slug IN ('us_META','msft','us_GOOGL','us_AMZN','us_AAPL')").fetchall()
L = []
for rid, slug, en in rows:
    q = by.get((en or '').lower())
    if q:
        db.execute('UPDATE mapco_people SET q=? WHERE rowid=?', (q, rid))
        L.append("UPDATE mapco_people SET q='%s' WHERE slug='%s' AND en='%s';" % (q, slug, (en or '').replace("'", "''")))
        n += 1
db.execute("UPDATE mapco SET people=(SELECT count(*) FROM mapco_people WHERE slug='us_META') WHERE slug='us_META'")
db.commit()
print('リンクした人', n, '/', len(rows), flush=True)
if '--push' in sys.argv:
    pre = ["INSERT INTO mapco_people (slug,name,en,role,since,until,note) SELECT 'us_META','アダム・モセリ','Adam Mosseri','Instagram責任者','2018','','2018年にInstagramの責任者(CEO)に就任。' WHERE NOT EXISTS (SELECT 1 FROM mapco_people WHERE slug='us_META' AND en='Adam Mosseri');",
           "UPDATE mapco SET people=(SELECT count(*) FROM mapco_people WHERE slug='us_META') WHERE slug='us_META';"]
    sql = os.path.join(SITE, 'gafam_link.sql')
    open(sql, 'w', encoding='utf-8').write('\n'.join(pre + L) + '\n')
    r = subprocess.run('npx wrangler d1 execute houjin --remote --yes --command "ALTER TABLE mapco_people ADD COLUMN q TEXT"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('ALTER', 'OK' if r.returncode == 0 else (r.stdout + r.stderr)[-200:], flush=True)
    p = subprocess.run('npx wrangler d1 execute houjin --remote --yes --file="' + sql.replace(chr(92), '/') + '"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    o = (p.stdout or '') + (p.stderr or '')
    print('D1', 'OK' if p.returncode == 0 and 'ERROR' not in o else 'NG ' + o[-300:], flush=True)
