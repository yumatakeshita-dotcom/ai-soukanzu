"""英語圏の技術ニュース(WordPressの公開API: techcrunch.com / siliconangle.com)の記事のうち、資金調達を報じたものから、会社・金額・ラウンド・出資者の名前を取り出す。
  出典=記事のリンク。見出し・金額・出資者の名前だけを記録し、本文は転載しない。 出力: wpen_<host>.json
使い方: python -u fetch_wp_funding_en.py <ホスト(techcrunch.com)> <終わりのページ> [始めのページ]"""
import html, json, os, re, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
S = os.path.dirname(os.path.abspath(__file__))
HOST = sys.argv[1]
END = int(sys.argv[2]) if len(sys.argv) > 2 else 20
START = int(sys.argv[3]) if len(sys.argv) > 3 else 1
H = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
VERB = r'(?:raises|secures|lands|closes|bags|nabs|snags|gets|scores|pulls in|picks up|banks|collects|racks up|announces|completes|unveils|reels in|brings in|attracts|lines up)'
TITLE = re.compile(r'^(.{2,90}?)\s+' + VERB + r'\b', re.I)
LAT = re.compile(r"\b(?:[A-Z][A-Za-z0-9&.\-']+|a16z|[0-9]{2,}[A-Za-z]+)(?:\s(?:[A-Z][A-Za-z0-9&.\-']+|&|of|for|Capital|Ventures))*")
STOP = set('AI CEO CTO COO CFO Series Seed Round Inc Corp Ltd LLC USD US UK EU API SaaS B2B B2C IoT VC CVC ARR GPU LLM App The A B C D E F G H Pre Google News TechCrunch Bloomberg Reuters Forbes Twitter X I We It In On At As To For And Or But With By From This That These Those He She They Its Our Their His Her Why How What When Where Who Also However Meanwhile Funding Total Existing New Other Additional Previous Early Later First Second Last Now Today Wednesday Tuesday Monday Thursday Friday Saturday Sunday January February March April May June July August September October November December'.split())
GENERIC = {'Capital', 'Systems', 'Ventures', 'Partners', 'Fund', 'Investments', 'Technology', 'Technologies', 'Holdings', 'Group', 'Labs', 'Growth', 'Venture', 'Equity'}
ORGWORD = re.compile(r'Capital|Ventures?|Partners|Fund|Invest|Holdings|Group|Labs|Equity|Angels?|Bank|Foundation|Asset|Management|Growth|Futures|Studio|Accelerator|Combinator|Catalyst|Sequoia|Khosla|Benchmark|Accel|Greylock|Lightspeed|Bessemer|Index|Insight|Thrive|Coatue|Tiger|SoftBank|Andreessen|a16z|Kleiner|Redpoint|Battery|IVP|GV|NEA|DST|ICONIQ|Menlo|Founders|Lux|Spark|Atomico|Balderton|Northzone|Creandum|Seedcamp|HV|Hedosophia|Ribbit|Elad|Sands|Fidelity|BlackRock|Temasek|GIC|Mubadala|QIA|CPPIB|Goldman|Morgan|JPMorgan|Nvidia|NVIDIA|Microsoft|Google|Amazon|Salesforce|Intel|Samsung|Qualcomm|Cisco|Oracle|SAP|Shopify|Stripe|OpenAI|Anthropic', re.I)
NORM = {'Sequoia': 'Sequoia Capital', 'Lightspeed': 'Lightspeed Venture Partners', 'Bessemer': 'Bessemer Venture Partners', 'Redpoint': 'Redpoint Ventures', 'USV': 'Union Square Ventures', 'NEA': 'New Enterprise Associates', 'Greylock': 'Greylock Partners', 'a16z': 'Andreessen Horowitz', 'a16z Perennial': 'Andreessen Horowitz', 'Kleiner': 'Kleiner Perkins', 'YC': 'Y Combinator', 'Softbank': 'SoftBank', 'GV': 'GV', 'Founders Fund': 'Founders Fund', 'Y Combinator': 'Y Combinator'}
SENT = re.compile(r'[^.!?\n]*(?:led by|co-led|participation from|participated|backed by|investors include|investment from|joined by|with support from|from existing investors|round included|including|new investors?)[^.!?\n]*', re.I)


def get(u):
    for i in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read())
        except Exception as e:
            time.sleep(20 if '429' in str(e) else 3 * (i + 1))


def clean(n):
    n = re.sub(r"[.,'\-]+$", '', n.strip())
    n = re.sub(r'\s+(?:and|of|for|&)$', '', n)
    n = re.sub(r"'s$", '', n)
    return n.strip()


rows, seen, posts = [], set(), 0
OUTF = os.path.join(S, 'wpen_%s.json' % HOST.split('.')[0])
if START > 1 and os.path.exists(OUTF):
    rows = json.load(open(OUTF, encoding='utf-8'))
    seen = {(r['src'], r['dst'], r['url']) for r in rows}
for pg in range(START, END + 1):
    j = get('https://%s/wp-json/wp/v2/posts?per_page=100&page=%d&search=%s&orderby=date&order=desc&_fields=link,date,title,content' % (HOST, pg, urllib.parse.quote('raises')))
    if not j:
        break
    for p in j:
        posts += 1
        t = html.unescape(re.sub(r'<[^>]+>', '', p['title']['rendered']))
        m = TITLE.search(t)
        if not m:
            continue
        left = m.group(1)
        cm = re.search(r"((?:[A-Z][\w.&'\-]*|[0-9][\w\-]*)(?:\s(?:[A-Z][\w.&'\-]*|[0-9][\w\-]*)){0,2})$", left)
        comp = clean(cm.group(1)) if cm else ''
        if not comp or comp in STOP or len(comp) < 2:
            continue
        am = re.search(r'\$\s?([0-9][0-9.,]*)\s?(M|B|K|million|billion|m|b)?\b', t)
        rd = re.search(r'(Pre-?[Ss]eed|Seed|Series [A-H]|Pre-Series [A-C])', t + ' ' + html.unescape(re.sub(r'<[^>]+>', ' ', p['content']['rendered']))[:600])
        body = html.unescape(re.sub(r'<[^>]+>', '\n', p['content']['rendered']))
        inv = []
        for s in SENT.findall(body[:5000]):
            for mm in LAT.finditer(s):
                n = clean(mm.group(0))
                if '-based' in n or re.search(r'(?:and|or)', n) or n in STOP or n in GENERIC or n == comp or comp in n or n in comp or len(n) < 3:
                    continue
                if n.split(' ')[0] in STOP and n not in NORM:
                    continue
                if not ORGWORD.search(n):
                    continue
                inv.append(NORM.get(n, n))
        for n in list(dict.fromkeys(inv))[:8]:
            k = (n, comp, p['link'])
            if k in seen:
                continue
            seen.add(k)
            rows.append({'src': n, 'dst': comp, 'kind': '資金調達', 'label': rd.group(1) if rd else '', 'amount': ('$' + am.group(1) + (am.group(2) or '')) if am else '', 'year': p['date'][:4], 'd': p['date'][:10], 'url': p['link'], 'media': HOST.split('.')[0].capitalize() if HOST != 'techcrunch.com' else 'TechCrunch', 'note': t[:160]})
    print('ページ', pg, '記事', posts, '線', len(rows), flush=True)
    json.dump(rows, open(OUTF, 'w', encoding='utf-8'), ensure_ascii=False)
    time.sleep(1)
print('合計', len(rows), '件 / 記事', len({r['url'] for r in rows}))
