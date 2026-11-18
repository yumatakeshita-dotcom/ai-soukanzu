"""お金の流れ(出資・資金調達)を、houjin.sqlite の money_flow に入れ、--push で D1 に送る(差分は数百行)。
入力: money_flow.json(money_harvest.py) / funding_news.json(出資者つきの資金調達の報道)
使い方: python -u money_apply.py [--push]"""
import json, os, re, sqlite3, subprocess, sys
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')
db = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite'))
db.execute('DROP TABLE IF EXISTS money_flow')
db.execute('CREATE TABLE money_flow (src TEXT, dst TEXT, kind TEXT, label TEXT, year TEXT, amount TEXT, note TEXT, url TEXT, media TEXT, d TEXT)')
INDEX = {'Vanguard', 'BlackRock', 'State Street', 'Vanguard Portfolio Mgmt', 'Capital Group', 'Fidelity', 'JPMorgan Asset Mgmt', 'Royal Trust Corporation of Canada', 'BMO Bank NA'}
n = 0
for r in json.load(open(os.path.join(S, 'money_flow.json'), encoding='utf-8')):
    kind = '大株主' if r['src'] in INDEX or '株主' in (r['label'] or '') else '出資'
    db.execute('INSERT INTO money_flow VALUES (?,?,?,?,?,?,?,?,?,?)', (r['src'], r['dst'], kind, r['label'], str(r['year'] or ''), '', (r['desc'] or '')[:200], '', '', ''))
    n += 1
m = 0
for x in json.load(open(os.path.join(S, 'funding_news.json'), encoding='utf-8')):
    if not x.get('inv') or not x.get('cn'):
        continue
    for inv in x['inv']:
        db.execute('INSERT INTO money_flow VALUES (?,?,?,?,?,?,?,?,?,?)', (inv, x['cn'], '資金調達', x.get('rd') or '', (x.get('d') or '')[:4], x.get('a') or '', (x.get('t') or '')[:160], x.get('u') or '', x.get('s') or '', x.get('d') or ''))
        m += 1
jp = os.path.join(S, 'jp_funding.json')
seen = set()
if os.path.exists(jp):
    for x in json.load(open(jp, encoding='utf-8')):
        src = re.sub(r'株式会社', '', x['src']).strip()
        k = (src, x['dst'], x['url'])
        if k in seen:
            continue
        seen.add(k)
        db.execute('INSERT INTO money_flow VALUES (?,?,?,?,?,?,?,?,?,?)', (src, x['dst'], '資金調達', x.get('label') or '', (x.get('d') or '')[:4], x.get('amount') or '', x.get('note') or '', x['url'], 'PR TIMES', x.get('d') or ''))
        m += 1
wpc = os.path.join(S, 'money_wp_clean.json')
if os.path.exists(wpc):
    for x in json.load(open(wpc, encoding='utf-8')):
        db.execute('INSERT INTO money_flow VALUES (?,?,?,?,?,?,?,?,?,?)', (x['src'], x['dst'], '出資', x.get('label') or '', '', '', x.get('note') or '', x.get('url') or '', x.get('media') or '', ''))
tbp = os.path.join(S, 'thebridge_funding.json')
if os.path.exists(tbp):
    seen2 = set()
    for x in json.load(open(tbp, encoding='utf-8')):
        k = (x['src'], x['dst'], x['url'])
        if k in seen2:
            continue
        seen2.add(k)
        db.execute('INSERT INTO money_flow VALUES (?,?,?,?,?,?,?,?,?,?)', (x['src'], x['dst'], '資金調達', x.get('label') or '', x.get('year') or '', x.get('amount') or '', x.get('note') or '', x['url'], 'THE BRIDGE', x.get('d') or ''))
        m += 1
for offp in (os.path.join(S, 'money_official.json'), os.path.join(S, 'money_official_jp.json')):
  if os.path.exists(offp):
    for x in json.load(open(offp, encoding='utf-8')):
        db.execute('INSERT INTO money_flow VALUES (?,?,?,?,?,?,?,?,?,?)', (x['src'], x['dst'], '出資', x.get('label') or '', x.get('year') or '', '', x.get('note') or '', x.get('url') or '', x.get('media') or '', ''))
        m += 1
jv = os.path.join(S, 'jpvc_portfolio.json')
if os.path.exists(jv):
    for x in json.load(open(jv, encoding='utf-8')):
        db.execute('INSERT INTO money_flow VALUES (?,?,?,?,?,?,?,?,?,?)', (x['src'], x['dst'], '出資', x.get('label') or '', '', '', x.get('note') or '', x.get('url') or '', x.get('media') or '', ''))
jvn = os.path.join(S, 'money_jpvc_news.json')
if os.path.exists(jvn):
    for x in json.load(open(jvn, encoding='utf-8')):
        db.execute('INSERT INTO money_flow VALUES (?,?,?,?,?,?,?,?,?,?)', (x['src'], x['dst'], '資金調達', x.get('label') or '', x.get('year') or '', x.get('amount') or '', x.get('note') or '', x['url'], 'PR TIMES', x.get('d') or ''))
        m += 1
mm = os.path.join(S, 'muse_money_add.json')
if os.path.exists(mm):
    for x in json.load(open(mm, encoding='utf-8')):
        db.execute('INSERT INTO money_flow VALUES (?,?,?,?,?,?,?,?,?,?)', (x['src'], x['dst'], x['kind'], x.get('label') or '', x.get('year') or '', x.get('amount') or '', x.get('note') or '', x['url'], x.get('media') or '', x.get('d') or ''))
ex = os.path.join(S, 'money_extra.json')
e = 0
if os.path.exists(ex):
    for x in json.load(open(ex, encoding='utf-8')):
        db.execute('INSERT INTO money_flow VALUES (?,?,?,?,?,?,?,?,?,?)', (x['src'], x['dst'], x['kind'], x.get('label') or '', x.get('year') or '', x.get('amount') or '', x.get('note') or '', x.get('url') or '', x.get('media') or '', x.get('d') or ''))
        e += 1
NORMMAP = {'SBI Group': 'SBI', 'Sequoia': 'Sequoia Capital', 'Lightspeed': 'Lightspeed Venture Partners', 'Tiger Global': 'Tiger Global Management', 'Nvidia': 'NVIDIA', 'Salesforce': 'Salesforce Ventures', 'DNX Capital': 'DNX Ventures', 'XTech': 'XTech Ventures', 'DUAL BRIDGE CAPITAL': 'Dual Bridge Capital', 'Peak XV': 'Peak XV Partners', 'Spiral Regional Innovation': 'Spiral Regional Innovation Fund', 'Genesia Ventures': 'Genesia Venture Fund', 'Abies Ventures Fund': 'Abies Ventures', 'Fidelity Management and Research Company': 'Fidelity Management & Research Company', 'JIC VGI': 'JIC-VGI', 'Mayfield Fund': 'Mayfield', 'T. Rowe Price': 'T. Rowe Price Investment Management', 'Amplify Venture Partners': 'Amplify', 'Balderton': 'Balderton Capital', 'DST Global Partners': 'DST Global', 'Evantic Capital': 'Evantic', 'FirstMark Growth': 'FirstMark Capital', 'GENDA': 'GENDA Capital', 'Left Lane': 'Left Lane Capital', 'Nexus': 'Nexus Venture Partners', 'Point72 Ventures': 'Point72', 'Scribble VC': 'Scribble Ventures', 'Skyland Next': 'Skyland Next Fund', 'Taisu VC': 'Taisu Ventures', 'Mizuho Leaguer Investments': 'Mizuho Leaguer Investment', 'CrossLink Capital': 'Crosslink Capital', 'Glilot Capital Partners': 'Glilot Capital', 'Meritech': 'Meritech Capital', 'Top Tier': 'Top Tier Capital Partners', 'UNERI': 'UNERI Capital'}
for a, b in NORMMAP.items():
    db.execute('UPDATE money_flow SET src=? WHERE src=?', (b, a))
    db.execute('UPDATE money_flow SET dst=? WHERE dst=?', (b, a))
db.execute('DELETE FROM money_flow WHERE rowid NOT IN (SELECT min(rowid) FROM money_flow GROUP BY src, dst, kind, url)')
cl = os.path.join(S, 'money_cleanup.sql')
if os.path.exists(cl):
    db.executescript(open(cl, encoding='utf-8').read())
db.commit()
print('追加分(AIマネー・YC)', e)
print('相関図の線', n, '/ 資金調達の報道', m, flush=True)
if '--push' not in sys.argv:
    sys.exit(0)
q1 = lambda v: "'" + str('' if v is None else v).replace("'", "''") + "'"
L = ['DROP TABLE IF EXISTS money_flow;', 'CREATE TABLE money_flow (src TEXT, dst TEXT, kind TEXT, label TEXT, year TEXT, amount TEXT, note TEXT, url TEXT, media TEXT, d TEXT);', 'CREATE INDEX i_mf_d ON money_flow(dst);', 'CREATE INDEX i_mf_s ON money_flow(src);']
for r in db.execute('SELECT * FROM money_flow'):
    L.append('INSERT INTO money_flow VALUES (%s);' % ','.join(q1(x) for x in r))
sql = os.path.join(SITE, 'money.sql')
open(sql, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
p = subprocess.run('npx wrangler d1 execute houjin --remote --yes --file="' + sql.replace(chr(92), '/') + '"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
out = (p.stdout or '') + (p.stderr or '')
if p.returncode != 0 or 'ERROR' in out:
    print('失敗', out[-400:]); sys.exit(1)
print('D1に反映しました', len(L), '文', flush=True)
