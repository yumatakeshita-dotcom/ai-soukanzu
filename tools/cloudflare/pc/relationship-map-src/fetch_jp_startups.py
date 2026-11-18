"""日本のスタートアップの一覧を作る。Claude不要。途中から再開できる。
  ① 東証グロース市場の上場企業(JPXの『東証上場銘柄一覧』) = 上場スタートアップ(約590社)
     各社の設立・本社・代表者・資本金・従業員・HPは、日経の会社概要(誰でも読める部分)から取る
  ② 未上場: 日本のVC(UTEC・Coral・インキュベイトファンド・ビヨンドネクストなど)の投資先、日本語の資金調達ニュースに出た会社、日本のユニコーン
出力: jp_startups.json  [{n:名前, code, mkt, ind, est, hq, rep, cap, emp, url, vcs:[...], src:[...]}, ...]
使い方: python fetch_jp_startups.py"""
import json, os, re, sys, time, unicodedata, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
UA = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
JPX_PAGE = 'https://www.jpx.co.jp/markets/statistics-equities/misc/01.html'


def http(url, timeout=60):
    for i in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
        except Exception:
            time.sleep(3 * (i + 1))
    return None


def ld(n, d):
    f = os.path.join(S, n)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else d


def sv(n, o):
    json.dump(o, open(os.path.join(S, n + '.tmp'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    os.replace(os.path.join(S, n + '.tmp'), os.path.join(S, n))


# ---- ① JPX: グロース市場 ----
xl = os.path.join(S, 'jpx_list.xlsx')
page = http(JPX_PAGE)
if page:
    m = re.search(r'href="([^"]*data_j\.xlsx)"', page.decode('utf-8', 'replace'))
    if m:
        raw = http('https://www.jpx.co.jp' + m.group(1))
        if raw and raw[:2] == b'PK':
            open(xl, 'wb').write(raw)
import openpyxl
ws = openpyxl.load_workbook(xl, read_only=True).active
growth = []
for r in list(ws.iter_rows(values_only=True))[1:]:
    if r[3] and 'グロース' in str(r[3]):
        growth.append({'code': str(r[1]), 'n': unicodedata.normalize('NFKC', str(r[2])).strip(), 'mkt': '東証グロース', 'ind': str(r[5] or '')})
print('東証グロース', len(growth), flush=True)

# ---- 日経の会社概要 ----
cache = ld('jp_growth.json', {})
for g in growth:
    c = g['code']
    if c in cache:
        continue
    raw = http('https://www.nikkei.com/nkd/company/gaiyo/?scode=' + c)
    if not raw:
        continue
    t = raw.decode('utf-8', 'replace')
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    t = re.sub(r'<[^>]+>', '|', t)
    t = re.sub(r'[\s|]+', '|', t).replace('&nbsp;', ' ')

    def f(a, b):
        mm = re.search(a + r'\|(.*?)\|' + b, t)
        return mm.group(1) if mm else ''
    jn = lambda s: (' ' if re.search(r'[A-Za-z]{3}', s) else '').join(s.split('|')).strip()
    cache[c] = {'full': re.sub(r'[（(]株[）)]|株式会社', '', f('正式社名', 'URL')).strip(), 'url': f('URL', '英文社名'), 'est': f('設立年月日', '日経業種分類').split('|')[0],
                'rep': jn(f('代表者氏名', '資本金')), 'cap': (re.search(r'資本金\|([\d,]+\([^)]*\))', t) or [0, ''])[1],
                'emp': (re.search(r'従業員数\|([\d,]+)', t) or [0, ''])[1], 'hq': f('本社住所', '地図').replace('|', ' ')}
    sv('jp_growth.json', cache)
    time.sleep(1.2)
    if len(cache) % 50 == 0:
        print('日経の概要', len(cache), flush=True)
print('日経の概要', len(cache), flush=True)

out = {}
nz = lambda s: re.sub(r'[\s・･·.\-_,]', '', re.sub(r'株式会社|\(株\)|㈱', '', unicodedata.normalize('NFKC', str(s))).lower())
for g in growth:
    c = cache.get(g['code'], {})
    m = re.search(r'(\d{4})年', c.get('est', ''))
    out[nz(g['n'])] = {'n': g['n'], 'code': g['code'], 'mkt': g['mkt'], 'ind': g['ind'], 'est': int(m.group(1)) if m else 0,
                                         'hq': c.get('hq', ''), 'rep': c.get('rep', ''), 'cap': c.get('cap', ''), 'emp': c.get('emp', ''), 'url': c.get('url', ''), 'vcs': [], 'src': ['JPX東証グロース']}

# ---- ② 未上場 ----
JP = re.compile(r'[ぁ-んァ-ヶ一-龥]')
vcs = ld('vc_inv.json', {})
names = {}      # 名前 -> [VC名]
try:
    from vc_official import OFFICIAL
    disp = {}
    for ln in open(os.path.join(S, 'vc_names.txt'), encoding='utf-8'):
        a = (ln.rstrip('\n').split('|') + [''] * 7)[:7]
        disp[a[0]] = (a[6] or a[3], a[1])
    SKIPVC = {'softbankinv', 'visionfund', 'sonyfund', 'dcm', 'coral', 'utec', 'mizuhocap', 'mufgcapital', 'smbcvc', 'jic', 'sbi'}   # 日本の会社だけの一覧ではないVCは、日本語の社名だけ使う
    JPONLY = {'incubatefund', 'beyondnext', 'anri', 'wil'}   # 日本の会社が中心のVC: 英語表記の社名も使う(JAFCOなどはWikipediaに海外の会社も多いので日本語名だけ)
    for k, (_u, ns) in OFFICIAL.items():
        vn, reg = disp.get(k, (k, ''))
        if reg != '日本' or k in ('softbankinv', 'visionfund'):
            continue
        for nm in [x.strip() for x in ns.split(', ') if x.strip()]:
            if JP.search(nm) or k in JPONLY:
                names.setdefault(nm, []).append(vn)
except ImportError:
    pass
for k, v in vcs.items():
    if v.get('region') == '日本' and k not in ('softbankinv', 'visionfund'):
        for p in v.get('p', []):
            nm = p[1] or p[0]
            if JP.search(nm) or (k in ('incubatefund', 'beyondnext', 'anri', 'wil') and re.search(r'[A-Za-z]', nm)):
                names.setdefault(nm, []).append(v.get('jp') or v['en'])
for h in ld('funding_news.json', []):
    if h.get('r') == 'j' and h.get('cn') and (JP.search(h['cn']) or ('円' in h['t'] and JP.search(h['t']))):   # 日本語の記事で円建ての調達=日本の会社
        names.setdefault(h['cn'], []).extend(h.get('inv', []))
for u in ld('unicorns.json', []):
    if 'Japan' in (u.get('c') or []):
        names.setdefault(u['n'], [])
n_unl = 0
for nm, vs in names.items():
    k = nz(nm)
    if not k or len(k) < 2:
        continue
    if k in out:                  # 上場済みの会社は、VCの記録を足すだけ
        out[k]['vcs'] = sorted(set(out[k]['vcs'] + vs))
        out[k]['src'].append('VC・ニュース')
        continue
    out[k] = {'n': re.sub(r'^株式会社|株式会社$', '', nm).strip(), 'code': '', 'mkt': '未上場', 'ind': '', 'est': 0, 'hq': '', 'rep': '', 'cap': '', 'emp': '', 'url': '', 'vcs': sorted(set(vs)), 'src': ['VC・ニュース・ユニコーン']}
    n_unl += 1
rows = sorted(out.values(), key=lambda r: (r['mkt'] != '未上場', -(r['est'] or 0), r['n']))
sv('jp_startups.json', rows)
print('日本のスタートアップ', len(rows), '社(上場', sum(1 for r in rows if r['code']), '/ 未上場', sum(1 for r in rows if not r['code']), ')')
