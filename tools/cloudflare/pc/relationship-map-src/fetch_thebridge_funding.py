"""THE BRIDGE(thebridge.jp)の記事のうち、資金調達を報じたものから、会社・金額・ラウンド・出資者の名前を取り出す(出典は記事のリンク)。
  WordPressの公開API(/wp-json/wp/v2/posts)で、見出しと本文を読む。出資者は『リード』『出資』『参加』を含む文から、組織名らしい固有名詞だけを拾う。
  見出し・金額・出資者の名前だけを記録し、本文は転載しない。 出力: thebridge_funding.json
使い方: python -u fetch_thebridge_funding.py [ページ数(1ページ100記事, 既定6)]"""
import html, json, os, re, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
S = os.path.dirname(os.path.abspath(__file__))
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 6
START = int(sys.argv[2]) if len(sys.argv) > 2 else 1
H = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
ORG_JP = re.compile(r'(?:キャピタル|ベンチャーズ?|ファンド|パートナーズ|インベストメント|ホールディングス|銀行|証券|ベンチャー|ラボ|インキュベート)$')
STOP = set('AI CEO CTO COO CFO Series Seed Round Inc Corp Ltd LLC USD US UK EU API SaaS B2B B2C IoT VC CVC ARR GPU LLM App The A B C D E F G H Pre Google News TechCrunch Bloomberg Reuters Forbes THE BRIDGE Twitter X Meta Microsoft Amazon Apple Facebook'.split())
KEEP_BIG = {'Google', 'Microsoft', 'Amazon', 'Apple', 'Meta', 'Nvidia', 'NVIDIA', 'Salesforce', 'Intel', 'Samsung', 'Cisco', 'Qualcomm'}
GENERIC = {'Capital', 'Systems', 'Ventures', 'Partners', 'Fund', 'Investments', 'Technology', 'Technologies', 'Holdings', 'Group', 'Labs', 'Neo', 'Liquid', 'Spice', 'Combinator'}
SHORT_OK = {'USV', 'JIC', 'NEA', 'SBI', 'DCM', 'BNP', 'GV', 'a16z', 'CVC'}
SENT = re.compile(r'[^。\n]*(?:リード|出資|参加|投資家|調達)[^。\n]*')
LAT = re.compile(r"[A-Z][A-Za-z0-9&.\-']{1,}(?: (?:[A-Z][A-Za-z0-9&.\-']+|&|of|for|and)){0,4}")


def get(u):
    for i in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read())
        except Exception:
            time.sleep(3 * (i + 1))


def clean(n):
    n = n.strip(" .,'-")
    n = re.sub(r'\s+(?:Inc|Corp|Ltd|LLC|Co)\.?$', '', n)
    return n


NORM = {'Sequoia': 'Sequoia Capital', 'Lightspeed': 'Lightspeed Venture Partners', 'Bessemer': 'Bessemer Venture Partners', 'Redpoint': 'Redpoint Ventures', 'USV': 'Union Square Ventures', 'NEA': 'New Enterprise Associates', 'Greylock': 'Greylock Partners', 'a16z': 'Andreessen Horowitz', 'ANRI6': 'ANRI', 'LinkCapital1': 'Link Capital', 'Venture Capital': '', 'Kleiner': 'Kleiner Perkins'}
PEOPLEWORD = re.compile(r'CEO|CIO|CTO|COO|CFO|Founder|founder')
rows, seen, posts = [], set(), 0
OUTF = os.path.join(S, 'thebridge_funding.json')
if START > 1 and os.path.exists(OUTF):
    rows = json.load(open(OUTF, encoding='utf-8'))
    seen = {(r['src'], r['dst'], r['url']) for r in rows}
for pg in range(START, PAGES + 1):
    j = get('https://thebridge.jp/wp-json/wp/v2/posts?per_page=100&page=%d&search=%s&orderby=date&order=desc&_fields=link,date,title,content' % (pg, urllib.parse.quote('調達')))
    if not j:
        break
    for p in j:
        posts += 1
        t = html.unescape(re.sub(r'<[^>]+>', '', p['title']['rendered']))
        if not re.search(r'調達|出資|資金', t):
            continue
        body = html.unescape(re.sub(r'<[^>]+>', '\n', p['content']['rendered']))
        # 会社名: 見出しの最初のラテン文字の固有名詞
        head = t.split('、')[0] if '、' in t else ''
        mm = re.search(r"([A-Za-z0-9][A-Za-z0-9&.\-' ]*[A-Za-z0-9])$", head) or re.search(r'([ァ-ヶー・]{3,})$', head)
        comp = clean(mm.group(1)) if mm else ''
        comp = re.sub(r'^(?:and|the)\s+', '', comp)
        if not comp or comp in STOP:
            continue
        am = re.search(r'([0-9０-９][0-9,.０-９]*(?:億|万)?(?:ドル|円|ユーロ|ポンド)|[0-9][0-9,.]*\s?(?:million|billion))', t)
        rd = re.search(r'(プレシリーズ ?[A-Z]|シリーズ ?[A-Z]|シード|プレシード|Series [A-Z]|Seed)', t)
        inv = []
        for s in SENT.findall(body[:6000]):
            if re.search(r'[がを]?(?:リード|出資|参加)', s) is None:
                continue
            for m in LAT.finditer(s):
                n = clean(m.group(0))
                if n in STOP or n == comp or comp in n or n in comp or len(n) < 3 or n.split(' ')[0] in STOP and n not in KEEP_BIG:
                    continue
                if n == 'YCombinator':
                    n = 'Y Combinator'
                if n in GENERIC or (len(n) < 4 and n not in SHORT_OK):
                    continue
                n = NORM.get(n, n)
                if not n or PEOPLEWORD.search(n):
                    continue
                inv.append(n)
        inv = list(dict.fromkeys(inv))[:8]
        for n in inv:
            k = (n, comp, p['link'])
            if k in seen:
                continue
            seen.add(k)
            rows.append({'src': n, 'dst': comp, 'kind': '資金調達', 'label': rd.group(1) if rd else '', 'amount': am.group(1) if am else '', 'year': p['date'][:4], 'd': p['date'][:10], 'url': p['link'], 'media': 'THE BRIDGE', 'note': t[:160]})
    print('ページ', pg, '記事', posts, '線', len(rows), flush=True)
    time.sleep(1)
json.dump(rows, open(os.path.join(S, 'thebridge_funding.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('合計', len(rows), '件 / 記事', len({r['url'] for r in rows}))
