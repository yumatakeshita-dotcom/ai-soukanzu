"""各社の買収一覧を英語版Wikipediaの『List of mergers and acquisitions by ○○』から集める。Claude不要。
出力: acq.json  {図のキー: [[買収先, 年, 金額, 説明, Wikipedia記事名], ...]}  /  acq_log.txt(対象外の一覧)
使い方: python fetch_acquisitions.py"""
import json, os, re, sys, time, urllib.parse, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
WP = 'https://en.wikipedia.org/w/api.php'


def api(**p):
    url = WP + '?' + urllib.parse.urlencode(p)
    for i in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        except Exception as e:
            time.sleep(3 * (i + 1))
    return {}


# 図のキー → 英語の会社名(Wikipedia記事の表記)。日本語名の会社は手動
EN = {}
for ln in open(os.path.join(S, 'acq_names.txt'), encoding='utf-8'):
    ln = ln.strip()
    if '=' in ln:
        k, n = ln.split('=', 1)
        EN[k] = n
ALIAS = {'Alphabet': ['Alphabet', 'Google'], 'Meta': ['Meta Platforms', 'Facebook'], 'X (Twitter)': ['Twitter, Inc.', 'Twitter'],
         'ADP': ['Automatic Data Processing'], 'BNY': ['BNY Mellon'], 'Nvidia': ['Nvidia'], 'RTX': ['Raytheon Technologies', 'RTX Corporation'],
         'GE Aerospace': ['General Electric', 'GE Aerospace'], 'Walt Disney': ['The Walt Disney Company', 'Disney'],
         'AMD': ['Advanced Micro Devices', 'AMD'], 'Salesforce': ['Salesforce'], 'Cursor (Anysphere)': ['Anysphere'],
         '楽天グループ': ['Rakuten'], 'ソフトバンクグループ': ['SoftBank Group', 'SoftBank'], 'LINEヤフー': ['LY Corporation', 'Yahoo Japan'],
         'メルカリ': ['Mercari'], 'ソフトバンク': ['SoftBank Corp.'], 'Slack': ['Slack Technologies']}
PAT = ['List of mergers and acquisitions by {}', 'List of acquisitions by {}', 'List of {} acquisitions', 'List of {} mergers and acquisitions']

cand = {}  # title -> key
for k, en in EN.items():
    for nm in ALIAS.get(en, [en]):
        nm = re.sub(r'\s*\(.*?\)', '', nm).strip()
        if not re.match(r'^[\x00-\x7f]+$', nm):
            continue
        for p in PAT:
            cand.setdefault(p.format(nm), k)
titles = list(cand)
found = {}
for i in range(0, len(titles), 50):
    ch = titles[i:i + 50]
    d = api(action='query', format='json', titles='|'.join(ch), redirects=1, formatversion=2)
    q = d.get('query', {})
    norm = {x['from']: x['to'] for x in q.get('normalized', [])}
    red = {x['from']: x['to'] for x in q.get('redirects', [])}
    pages = {p['title']: p for p in q.get('pages', [])}
    for t in ch:
        n = norm.get(t, t)
        n = red.get(n, n)
        pg = pages.get(n)
        if pg and not pg.get('missing'):
            found.setdefault(cand[t], n)
    time.sleep(0.5)
print('見つかった一覧', len(found), flush=True)

REF = re.compile(r'<ref[^>/]*>.*?</ref>|<ref[^>]*/>|<!--.*?-->', re.S)


def clean(s):
    s = REF.sub('', s)
    for _ in range(4):
        s = re.sub(r'\{\{[^{}]*\}\}', '', s)
    s = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', s)
    s = re.sub(r"'''?", '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip(' ,;|')


def cells_of(row):
    out = []
    for ln in row.split('\n'):
        if not ln or ln[0] not in '|!':
            if out:
                out[-1] += '\n' + ln
            continue
        ln = ln[1:]
        for part in re.split(r'\|\||!!', ln):
            if re.match(r'^[^\[\]{}<>]*\|(?!\|)', part):
                part = part.split('|', 1)[1]
            out.append(part)
    return out


H_DATE = re.compile(r'date|year|announced|completed|acquired on|acquired in|when', re.I)
H_NAME = re.compile(r'company|acquired|acquiree|target|name|business acquired|subsidiary|acquisition|firm', re.I)
H_VAL = re.compile(r'value|price|cost|amount|deal|consideration|\$|acquired for|usd', re.I)
H_DESC = re.compile(r'business|description|notes?|industry|details|sector|derived|product', re.I)


def parse(wt):
    rows = []
    for tb in re.findall(r'\{\|(.*?)\n\|\}', wt, re.S):
        rs = re.split(r'\n\|-+[^\n]*', '\n' + tb)
        hdr = None
        for r in rs:
            cs = cells_of(r.strip('\n'))
            if not cs:
                continue
            if r.strip().startswith('!') and hdr is None:
                hdr = [clean(c) for c in cs]
                continue
            if hdr is None or len(cs) < 2:
                continue
            idx = {}
            for j, h in enumerate(hdr):
                for nm, rx in (('d', H_DATE), ('v', H_VAL), ('n', H_NAME), ('x', H_DESC)):  # 1列は1つの役割だけ
                    if rx.search(h):
                        idx.setdefault(nm, j)
                        break
            if 'n' not in idx:
                idx['n'] = 1 if 'd' in idx and idx['d'] == 0 else 0
            if len(cs) < len(hdr) - 2:
                continue
            g = lambda k: cs[idx[k]] if k in idx and idx[k] < len(cs) else ''
            m = re.search(r'\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]', REF.sub('', g('n')))
            name = clean(m.group(2) or m.group(1)) if m else clean(g('n'))
            wtitle = m.group(1).strip() if m else ''
            y = re.search(r'(?<!\d)(19[5-9]\d|20[0-3]\d)(?!\d)', g('d'))
            if not name or len(name) > 70 or not y:
                continue
            val = clean(g('v'))[:60] if 'v' in idx else ''
            desc = clean(g('x'))[:110] if 'x' in idx else ''
            rows.append([name, int(y.group(1)), val if re.search(r'\d', val) else '', desc, wtitle])
    return rows


res = {}
for k, title in found.items():
    d = api(action='parse', format='json', page=title, prop='wikitext', formatversion=2, redirects=1)
    wt = d.get('parse', {}).get('wikitext', '')
    rows = parse(wt)
    seen, out = set(), []
    for r in rows:
        key = (r[0].lower(), r[1])
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    out.sort(key=lambda r: r[1])
    print(k, title, len(out), flush=True)
    if out:
        res[k] = out
    time.sleep(0.7)
_old = {}
try:      # 取得に失敗した会社(回数制限など)で、前回までの記録が消えないように、前回の分を引き継ぐ
    _old = json.load(open(os.path.join(S, 'acq.json'), encoding='utf-8'))
except Exception:
    pass
for _k, _v in _old.items():
    if not res.get(_k):
        res[_k] = _v
json.dump(res, open(os.path.join(S, 'acq.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('会社数', len(res), '買収件数', sum(len(v) for v in res.values()))
