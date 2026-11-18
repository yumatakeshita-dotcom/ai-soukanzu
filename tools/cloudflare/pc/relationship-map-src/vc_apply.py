"""VCのファンド規模・LPの表を houjin.sqlite に入れ、--push で D1 に送る(数十行)。 使い方: python -u vc_apply.py [--push]"""
import json, os, sqlite3, subprocess, sys
from vc_funds_curated import ROWS, LP_SIDE, LP_COMMIT, LP_COMMIT_URL
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')
db = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite'))
DDL = ['DROP TABLE IF EXISTS vc_fund', 'CREATE TABLE vc_fund (mgr TEXT, fund TEXT, size TEXT, usd_m REAL, whenx TEXT, status TEXT, lp TEXT, note TEXT, url TEXT, conf TEXT)',
       'DROP TABLE IF EXISTS lp_side', 'CREATE TABLE lp_side (lp TEXT, what TEXT, url TEXT)',
       'DROP TABLE IF EXISTS lp_commit', 'CREATE TABLE lp_commit (lp TEXT, fund TEXT, total_m INTEGER, commit_m INTEGER, year INTEGER, url TEXT)',
       'DROP TABLE IF EXISTS lp_fund', 'CREATE TABLE lp_fund (lp TEXT, mgr TEXT, fund TEXT, vintage INTEGER, committed_usd INTEGER, asof TEXT, url TEXT)']
for s in DDL:
    db.execute(s)
for r in ROWS:
    db.execute('INSERT INTO vc_fund VALUES (?,?,?,?,?,?,?,?,?,?)', (r['mgr'], r['fund'], r['size'], r['usd_m'], r['when'], r['status'], r['lp'], r['note'], r['url'], r['conf']))
for r in LP_SIDE:
    db.execute('INSERT INTO lp_side VALUES (?,?,?)', (r['lp'], r['what'], r['url']))
for f in LP_COMMIT:
    db.execute('INSERT INTO lp_commit VALUES (?,?,?,?,?,?)', ('中小機構(中小企業基盤整備機構)', f[0], f[1], f[2], f[3], LP_COMMIT_URL))
CS_URL = 'https://www.calstrs.com/files/76f90b08c/semi122025P+-+PE.pdf'
for f in json.load(open(os.path.join(S, 'calstrs_vc.json'), encoding='utf-8')):
    db.execute('INSERT INTO lp_fund VALUES (?,?,?,?,?,?,?)', ('CalSTRS', f['mgr'], f['fund'], f['vintage'], f['committed'], '2025-12-31', CS_URL))
WS_URL = 'https://www.sib.wa.gov/docs/reports/quarterly/ir033126.pdf'
for f in json.load(open(os.path.join(S, 'wsib_vc.json'), encoding='utf-8')):
    db.execute('INSERT INTO lp_fund VALUES (?,?,?,?,?,?,?)', ('WSIB', f['mgr'], f['fund'], f['vintage'], f['committed'], '2026-03-31', WS_URL))
CP_URL = 'https://www.calpers.ca.gov/investments/about-investment-office/investment-organization/pep-fund-performance'
for f in json.load(open(os.path.join(S, 'calpers_vc.json'), encoding='utf-8')):
    db.execute('INSERT INTO lp_fund VALUES (?,?,?,?,?,?,?)', ('CalPERS', f['mgr'], f['fund'], f['vintage'], f['committed'], '2026-03-31', CP_URL))
db.commit()
print('VCファンド', len(ROWS), '/ LP側', len(LP_SIDE), flush=True)
if '--push' not in sys.argv:
    sys.exit(0)
q1 = lambda v: 'NULL' if v is None else ("'" + str(v).replace("'", "''") + "'")
L = DDL + ['CREATE INDEX i_vc_u ON vc_fund(usd_m)']
for r in db.execute('SELECT * FROM vc_fund'):
    L.append('INSERT INTO vc_fund VALUES (%s);' % ','.join(q1(x) for x in r))
for r in db.execute('SELECT * FROM lp_side'):
    L.append('INSERT INTO lp_side VALUES (%s);' % ','.join(q1(x) for x in r))
for r in db.execute('SELECT * FROM lp_commit'):
    L.append('INSERT INTO lp_commit VALUES (%s);' % ','.join(q1(x) for x in r))
for r in db.execute('SELECT * FROM lp_fund'):
    L.append('INSERT INTO lp_fund VALUES (%s);' % ','.join(q1(x) for x in r))
sql = os.path.join(SITE, 'vc.sql')
open(sql, 'w', encoding='utf-8').write(';\n'.join(l.rstrip(';') for l in L) + ';\n')
p = subprocess.run('npx wrangler d1 execute houjin --remote --yes --file="' + sql.replace(chr(92), '/') + '"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
out = (p.stdout or '') + (p.stderr or '')
if p.returncode != 0 or 'ERROR' in out:
    print('失敗', out[-400:]); sys.exit(1)
print('D1に反映しました', flush=True)
