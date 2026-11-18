"""相関図の全会社(日本語名も英語名も)の、人物・ニュース・買収を、独自サイト用の表(mapco*)として houjin.sqlite に作る。
日本語名の会社は、EDINETの提出者と名前が一致すれば、法人番号(num)を付ける(取り違え防止のため、確実に一致したものだけ)。
使い方: python -I build_mapco.py <houjin.sqlite のパス>"""
import json, os, re, sqlite3, sys
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
from adds import apply_adds
dbp = sys.argv[1]
CO_ALL = {**__import__('newco_data').CO, **__import__('newco_data2').CO2, **__import__('newco_data3').CO3, **__import__('newco_data4').CO4, **__import__('newco_data5').CO5,
          **__import__('newco_data6').CO6, **__import__('newco_data7').CO7, **__import__('newco_data7b').CO7B, **__import__('newco_data8').CO8}
apply_adds(CO_ALL)
# Instagramは、VCの投資先の空の項目(vc_instagram)を、人物・出資者つきの図で置き換える
CO_ALL['vc_instagram'] = __import__('newco_data7c').CO7C['instagram']
CO_ALL.update(__import__('newco_data7d').CO7D)
CO_ALL.update(__import__('newco_data7e').CO7E)
CO_ALL.update(__import__('newco_data7f').CO7F)
page = open(os.path.join(S, '..', '..', '..', 'output', 'relationship-maps.html'), encoding='utf-8').read()
i = page.find('const ACQ=')
j = page.find(';\n', i)
ACQ = json.loads(page[i + len('const ACQ='):j]) if i > 0 else {}


def norm(s):
    s = re.sub(r'株式会社|\(株\)|（株）|㈱|Inc\.?|Corp\.?|Co\.,?\s*Ltd\.?|Ltd\.?|Holdings?', '', s or '')
    return re.sub(r'[\s　]', '', s).lower()


def clean(s):
    return re.sub(r'&nbsp;', ' ', str(s or '')).strip()


db = sqlite3.connect(dbp)
ed = {}
for name, num, listed in db.execute("select name, num, listed from edinet where num<>''"):
    ed.setdefault(norm(name), []).append((listed != '上場', num))
news = {}
for fn in ('news_cos.json', 'yahoo_cos.json'):
    p = os.path.join(S, fn)
    if os.path.exists(p):
        for name, rows in json.load(open(p, encoding='utf-8')).items():
            cap = 4 if fn == 'news_cos.json' else 3
            news.setdefault(name, []).extend(rows[:cap])
for t in ('mapco', 'mapco_people', 'mapco_news', 'mapco_acq'):
    db.execute('DROP TABLE IF EXISTS ' + t)
db.execute('CREATE TABLE mapco (slug TEXT PRIMARY KEY, name TEXT, en TEXT, note TEXT, num TEXT, people INTEGER, acq INTEGER)')
db.execute('CREATE TABLE mapco_people (slug TEXT, name TEXT, en TEXT, role TEXT, since TEXT, until TEXT, note TEXT, q TEXT)')
db.execute('CREATE TABLE mapco_news (slug TEXT, d TEXT, title TEXT, url TEXT, media TEXT)')
db.execute('CREATE TABLE mapco_acq (slug TEXT, year TEXT, target TEXT, amount TEXT, note TEXT)')
nco = npe = nne = nac = 0
for slug, c in CO_ALL.items():
    center = next((x for x in c['N'] if x['id'] == c.get('center')), None)
    name = center['name'] if center else slug
    num = ''
    if re.search(r'[ぁ-ヶ一-龥]', name) and norm(name) in ed:
        num = sorted(ed[norm(name)])[0][1]
    en = c.get('EN', {})
    people = [x for x in c['N'] if x.get('kind') == 'p']
    for x in people:
        db.execute('INSERT INTO mapco_people (slug,name,en,role,since,until,note) VALUES (?,?,?,?,?,?,?)', (slug, x['name'], en.get(x['id'], ''), x.get('role', '') or '', str(x.get('from', '') or ''), str(x.get('to', '') or ''), (x.get('desc', '') or '')[:200]))
    npe += len(people)
    seen = set()
    for d, t, u, m in news.get(name, []):
        if u in seen:
            continue
        seen.add(u)
        db.execute('INSERT INTO mapco_news VALUES (?,?,?,?,?)', (slug, d, t, u, m))
        nne += 1
    acq = ACQ.get(slug, [])
    for r in acq:
        db.execute('INSERT INTO mapco_acq VALUES (?,?,?,?,?)', (slug, str(r[1] or ''), clean(r[0]), clean(r[2]), clean(r[3])[:200]))
    nac += len(acq)
    db.execute('INSERT INTO mapco VALUES (?,?,?,?,?,?,?)', (slug, name, '', (center or {}).get('desc', '')[:300] if center else '', num, len(people), len(acq)))
    nco += 1

# ---- 相関図の外から足す会社: ① 東証の上場企業(中小を含む) ② 日本のスタートアップ ③ 米国の取引所に上場している日本企業 ----
def slugify(t):
    return re.sub(r'[^a-z0-9]+', '-', (t or '').lower()).strip('-')[:50]


have_names = set()
have_codes = set()
for k, c in CO_ALL.items():
    cen = next((x for x in c['N'] if x['id'] == c.get('center')), None)
    if cen:
        have_names.add(norm(cen['name']))
    m = re.match(r'jp_(\d{4})', k)
    if m:
        have_codes.add(m.group(1))
sec2num = {}
for sec, num in db.execute("select sec, num from edinet where sec<>'' and num<>''"):
    sec2num.setdefault(sec[:4], num)
added = {'jpx': 0, 'startup': 0, 'usjp': 0}
new_slugs = []
# ① 東証(内国株式)
import openpyxl
jx = os.path.join(S, 'jpx_list.xlsx')
if os.path.exists(jx):
    ws = openpyxl.load_workbook(jx, read_only=True).active
    for r in list(ws.iter_rows(values_only=True))[1:]:
        mk = str(r[3] or '')
        code = str(r[1] or '').strip()
        if '内国株式' not in mk or not code or code in have_codes or norm(str(r[2])) in have_names:
            continue
        slug = 'jpx_' + code
        market = mk.split('（')[0]
        note = '東京証券取引所 %s。証券コード %s。業種: %s。' % (market, code, r[5] or '')
        db.execute('INSERT INTO mapco VALUES (?,?,?,?,?,?,?)', (slug, str(r[2]), '', note, sec2num.get(code, ''), 0, 0))
        added['jpx'] += 1
        new_slugs.append((slug, str(r[2])))
# ② 日本のスタートアップ(東証グロース上場・未上場)
jsu = os.path.join(S, 'jp_startups.json')
if os.path.exists(jsu):
    for r in json.load(open(jsu, encoding='utf-8')):
        n = (r.get('n') or '').strip()
        if not n or norm(n) in have_names:
            continue
        slug = 'su_' + (slugify(n) or ('x%d' % added['startup']))
        note = ' / '.join(x for x in [('市場: ' + r['mkt']) if r.get('mkt') else '', ('業種: ' + r['ind']) if r.get('ind') else '', ('設立: %s年' % r['est']) if r.get('est') else '', ('本社: ' + r['hq']) if r.get('hq') else '', ('出資: ' + '・'.join(r['vcs'][:6])) if r.get('vcs') else ''] if x)
        if db.execute('select 1 from mapco where slug=?', (slug,)).fetchone():
            slug += '-%d' % added['startup']
        db.execute('INSERT INTO mapco VALUES (?,?,?,?,?,?,?)', (slug, n, '', note[:300], '', 1 if r.get('rep') else 0, 0))
        if r.get('rep'):
            db.execute('INSERT INTO mapco_people (slug,name,en,role,since,until,note) VALUES (?,?,?,?,?,?,?)', (slug, r['rep'], '', '代表者', '', '', ''))
            npe += 1
        added['startup'] += 1
        new_slugs.append((slug, n))
        have_names.add(norm(n))
# ③ 米国の取引所に上場している日本企業(SEC EDGAR)
usj = os.path.join(S, 'us_japan_scan.json')
if os.path.exists(usj):
    for cik, r in json.load(open(usj, encoding='utf-8')).items():
        tk = (r.get('ticker') or (r.get('tickers') or [''])[0] or '').strip()
        nm = r.get('name') or ''
        if nm.isupper():
            nm = nm.title()
        nm = nm.rstrip('/ ').strip()
        if not nm or norm(nm) in have_names or ('us_' + tk.upper()) in CO_ALL:
            continue
        slug = 'usjp_' + (slugify(tk) or cik)
        ex = r.get('exchange') or ''
        note = '米国の市場(%s)に上場している日本企業。ティッカー: %s。本社: %s。業種(SIC): %s。' % (ex or '取引所不明', tk or '—', (r.get('city') or '日本').title(), r.get('sicDesc') or '—')
        if r.get('website'):
            note += ' 公式サイト: ' + r['website']
        if db.execute('select 1 from mapco where slug=?', (slug,)).fetchone():
            slug += '-' + cik
        db.execute('INSERT INTO mapco VALUES (?,?,?,?,?,?,?)', (slug, nm, nm, note[:300], '', 0, 0))
        added['usjp'] += 1
        new_slugs.append((slug, nm))
        have_names.add(norm(nm))
for _slug, _name in new_slugs:
    _seen = set()
    for _d, _t, _u, _m in news.get(_name, []):
        if _u in _seen:
            continue
        _seen.add(_u)
        db.execute('INSERT INTO mapco_news VALUES (?,?,?,?,?)', (_slug, _d, _t, _u, _m))
        nne += 1
nco += sum(added.values())
print('足した会社: 東証', added['jpx'], '/ スタートアップ', added['startup'], '/ 米国上場の日本企業', added['usjp'])
# 人物ページ(/p/<Wikidata番号>)へ移れるように、英語名がWikidataの人物と1対1で一致する人に、番号(q)を付ける
db.execute("UPDATE mapco_people SET q=(SELECT p.q FROM person p WHERE p.en<>'' AND lower(p.en)=lower(mapco_people.en) AND (SELECT count(*) FROM person p2 WHERE lower(p2.en)=lower(mapco_people.en))=1) WHERE en<>''")
for ix in ('CREATE INDEX i_mapco_name ON mapco(name)', 'CREATE INDEX i_mapco_num ON mapco(num)', 'CREATE INDEX i_mapco_p ON mapco_people(slug)', 'CREATE INDEX i_mapco_n ON mapco_news(slug, d)', 'CREATE INDEX i_mapco_a ON mapco_acq(slug)'):
    db.execute(ix)
db.commit()
nco = db.execute('select count(*) from mapco').fetchone()[0]
print('相関図の会社', nco, '/ 人物', npe, '/ ニュース', nne, '/ 買収・子会社', nac, '/ 法人番号つき', db.execute("select count(*) from mapco where num<>''").fetchone()[0])
