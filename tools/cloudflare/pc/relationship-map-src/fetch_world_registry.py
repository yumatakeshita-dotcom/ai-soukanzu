"""海外の政府が無料で公開している会社登記データを取得して、解凍せずに、現存する会社だけを SQLite(world.sqlite)に入れる。
  UK: Companies House「BasicCompanyData」(Open Government Licence)  FR: INSEE「Sirene StockUniteLegale」(Licence Ouverte)
使い方: python -I fetch_world_registry.py uk|fr   (保存先: C:/Users/yumat/.claude/data/world_raw と world.sqlite)"""
import csv, io, os, sqlite3, sys, time, urllib.request, zipfile
which = sys.argv[1]
D = os.path.join(os.path.expanduser('~'), '.claude', 'data')
RAW = os.path.join(D, 'world_raw')
os.makedirs(RAW, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (compatible; relationship-map-research/1.0)'}
SRC = {
    'uk': ('https://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2026-11-01.zip', 'uk_basic.zip'),
    'fr': ('https://static.data.gouv.fr/resources/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/20261103-091933/stock-stockunitelegale-csv.zip', 'fr_sirene_ul.zip'),
}
url, fn = SRC[which]
path = os.path.join(RAW, fn)
if not os.path.exists(path):
    t = time.time()
    part = path + '.part'
    total = int(urllib.request.urlopen(urllib.request.Request(url, headers=UA, method='HEAD'), timeout=60).headers.get('content-length', 0))
    for attempt in range(40):      # 途中で切れたら、続きから取り直す(全部そろうまで)
        have = os.path.getsize(part) if os.path.exists(part) else 0
        if total and have >= total:
            break
        try:
            req = urllib.request.Request(url, headers=dict(UA, Range='bytes=%d-' % have))
            r = urllib.request.urlopen(req, timeout=120)
            with open(part, 'ab' if r.status == 206 else 'wb') as f:
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    f.write(b)
            print('取得', os.path.getsize(part) >> 20, '/', total >> 20, 'MB', flush=True)
        except Exception as e:
            print('再試行', attempt, str(e)[:80], flush=True)
            time.sleep(5)
    if total and os.path.getsize(part) != total:
        sys.exit('取得が完了しませんでした')
    os.replace(part, path)
    print('取得完了', os.path.getsize(path) >> 20, 'MB', round(time.time() - t), '秒', flush=True)
db = sqlite3.connect(os.path.join(D, 'world.sqlite'))
db.execute('PRAGMA journal_mode=OFF')
db.execute('PRAGMA synchronous=OFF')
db.execute('CREATE TABLE IF NOT EXISTS wcorp (cc TEXT, id TEXT, name TEXT, kind TEXT, city TEXT, post TEXT, since TEXT, sic TEXT, PRIMARY KEY (cc, id))')
db.execute('DELETE FROM wcorp WHERE cc=?', (which.upper(),))
z = zipfile.ZipFile(path)
name = next(i.filename for i in z.infolist() if i.filename.lower().endswith('.csv'))
t = io.TextIOWrapper(z.open(name), encoding='utf-8-sig', errors='replace', newline='')
rd = csv.DictReader(t)
rows, n, keep = [], 0, 0
for r in rd:
    n += 1
    if which == 'uk':
        if (r.get(' CompanyStatus') or r.get('CompanyStatus') or '').strip() not in ('Active', 'Active - Proposal to Strike off'):
            continue
        g = lambda k: (r.get(k) or r.get(' ' + k) or '').strip()
        rows.append(('UK', g('CompanyNumber'), g('CompanyName'), g('CompanyCategory'), g('RegAddress.PostTown'), g('RegAddress.PostCode'), g('IncorporationDate'), g('SICCode.SicText_1')[:80]))
    else:
        if r.get('etatAdministratifUniteLegale') != 'A' or r.get('categorieJuridiqueUniteLegale') == '1000':      # 現存の法人だけ(個人事業主=1000は除く)
            continue
        nm = (r.get('denominationUniteLegale') or '').strip()
        if not nm:
            continue
        rows.append(('FR', r['siren'], nm, r.get('categorieJuridiqueUniteLegale', ''), '', '', r.get('dateCreationUniteLegale', ''), r.get('activitePrincipaleUniteLegale', '')))
    if len(rows) >= 50000:
        db.executemany('INSERT OR REPLACE INTO wcorp VALUES (?,?,?,?,?,?,?,?)', rows)
        keep += len(rows)
        rows = []
    if n % 1000000 == 0:
        print('読み込み', n, '現存', keep, flush=True)
if rows:
    db.executemany('INSERT OR REPLACE INTO wcorp VALUES (?,?,?,?,?,?,?,?)', rows)
    keep += len(rows)
db.commit()
print('完了', which.upper(), '全', n, '現存', keep, flush=True)
