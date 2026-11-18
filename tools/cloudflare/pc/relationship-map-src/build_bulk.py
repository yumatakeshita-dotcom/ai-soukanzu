"""全企業リスト(bulk.json)を作る。SEC(米国上場)・東証(上場全社)・Wikidata(英語版Wikipediaに記事のある会社)を、名前と国で重複を除いて1つにまとめる。
出力: web/bulk.json と ../../../output/bulk.json (公開は Artifact の files で bulk.json として添付)
行の形: [英語名または社名, 日本語名, 国, 業種, 設立年, 出どころ(S/J/W), 識別子]"""
import json, os, re, sys, openpyxl
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
rows, seen = [], set()
nz = lambda t: re.sub(r'[^a-z0-9ぁ-んァ-ヶ一-龥]', '', re.sub(r'\b(inc|corp|corporation|ltd|limited|co|company|plc|llc|sa|ag|nv|se|group|holdings?)\b', '', (t or '').lower()))


def add(en, ja, c, ind, inc, src, ident):
    key = (nz(en or ja), c)
    if not nz(en or ja) or key in seen:
        return False
    seen.add(key)
    rows.append([en, ja, c, ind, inc, src, ident])
    return True


n = {'S': 0, 'J': 0, 'W': 0}
f = os.path.join(S, 'sec_tickers.json')
if os.path.exists(f):
    for cik, name, tk, ex in json.load(open(f, encoding='utf-8'))['data']:
        if add(name.title() if name.isupper() else name, '', '米国', ex or '', 0, 'S', '%s|%s' % (cik, tk)):
            n['S'] += 1
f = os.path.join(S, 'jpx_list.xlsx')
if os.path.exists(f):
    ws = openpyxl.load_workbook(f, read_only=True).active
    for r in list(ws.iter_rows(values_only=True))[1:]:
        mk = str(r[3] or '')
        if '内国株式' in mk and r[2]:
            if add('', str(r[2]), '日本', str(r[5] or ''), 0, 'J', '%s|%s' % (r[1], mk.split('（')[0])):
                n['J'] += 1
f = os.path.join(S, 'wd_bulk.jsonl')
if os.path.exists(f):
    for ln in open(f, encoding='utf-8'):
        try:
            e = json.loads(ln)
        except Exception:
            continue
        if add(e['en'], e.get('ja', ''), e['c'], e.get('ind', ''), e.get('inc', 0), 'W', e['q']):
            n['W'] += 1
out = {'built': __import__('datetime').date.today().isoformat(), 'src': {
    'S': ['SEC(米国証券取引委員会)の上場企業一覧', 'https://www.sec.gov/files/company_tickers_exchange.json'],
    'J': ['日本取引所グループ(JPX)の東証上場銘柄一覧', 'https://www.jpx.co.jp/markets/statistics-equities/misc/01.html'],
    'W': ['Wikidata(英語版Wikipediaに記事のある会社)', 'https://www.wikidata.org/']}, 'rows': rows}
for d in (os.path.join(S, 'web'), os.path.join(S, '..', '..', '..', 'output')):
    os.makedirs(d, exist_ok=True)
    json.dump(out, open(os.path.join(d, 'bulk.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('全企業', len(rows), n, 'MB', round(os.path.getsize(os.path.join(S, 'web', 'bulk.json')) / 1e6, 2))
