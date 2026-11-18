"""VCごとに、ニュースサイトの検索(Google News)で『そのVCが出資・主導した会社』の記事を探し、投資先(会社名)を見つける。Claude不要。
  検索: 「VC名」+ 出資/資金調達/引受先/投資(日本語)、「VC name」+ led/backed/invests/raises(英語)。見出しにVC名がある記事だけを使う。
  会社名: fetch_sources.parse_funding(見出しから会社名・ラウンド・投資家)+「VCが○○に出資」の形。
出力: vc_pairs.json  {VC名: [{c:会社, d:日付, u:URL, t:見出し, s:出どころ, rd:ラウンド}, ...]}(積み上げ。1年)
使い方: python vc_name_news.py [上限(VCの数)]"""
import datetime as dt, html, json, os, re, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import fetch_sources as FS

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 400
JP = re.compile(r'[ぁ-んァ-ヶ一-龥]')


def ld(n, d):
    f = os.path.join(S, n)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else d


# 対象のVC: 投資先の多い順 + 日本のVCは全部
vcs = ld('vc_inv.json', {})
names = {}
for k, v in vcs.items():
    names[v.get('jp') or v['en']] = (len(v.get('p', [])), v['en'], v.get('jp', ''))
for k, v in ld('vc_big.json', {}).items():
    names.setdefault(v.get('jp') or v['en'], (len(v.get('p', [])), v['en'], v.get('jp', '')))
try:
    from vc_extra import EXTRA
    for key, en, jp, ctry, kind, desc, ports in EXTRA:
        names[jp or en] = (999, en, jp)
except ImportError:
    pass
try:
    from vc_official import OFFICIAL
    for k, (u, ns) in OFFICIAL.items():
        pass
except ImportError:
    pass
order = sorted(names.items(), key=lambda kv: -kv[1][0])[:LIMIT]
pairs = ld('vc_pairs.json', {})
today = dt.date.today()
cut = (today - dt.timedelta(days=365)).isoformat()
INV_JP = re.compile(r'(?:が|は|、)(?P<c>[^、。「」【】]{2,22}?)(?:に|へ)(?:出資|投資|参画)')
GN = 'https://news.google.com/rss/search?q=%s&hl=%s&gl=%s&ceid=%s'
n_new = 0
for vn, (cnt, en, jp) in order:
    qs = []
    if jp and JP.search(jp):
        qs.append((GN % (urllib.parse.quote('"%s" 出資 OR 資金調達 OR 引受先 OR 投資' % jp), 'ja', 'JP', 'JP:ja'), jp, 'j'))
    if en and re.match(r'^[\x00-\x7f]+$', en):
        qs.append((GN % (urllib.parse.quote('"%s" led OR backed OR invests OR raises OR funding' % re.sub(r'\s*\(.*?\)', '', en)), 'en-US', 'US', 'US:en'), re.sub(r'\s*\(.*?\)', '', en), 'w'))
    got = pairs.setdefault(vn, [])
    seen = {x['u'] for x in got}
    for url, key, region in qs:
        b = FS.get(url)
        if not b:
            continue
        try:
            root = ET.fromstring(b)
        except ET.ParseError:
            continue
        for it in root.iter():
            if not it.tag.endswith('item'):
                continue
            g = lambda t: next((c.text for c in it if c.tag.endswith(t) and c.text), '')
            title, link = html.unescape(g('title')).strip(), (g('link') or '').strip()
            src = 'Google News'
            m = re.search(r'\s[-–|]\s([^-–|]{2,40})$', title)
            if m:
                src, title = m.group(1).strip(), title[:m.start()]
            if not title or not link or link in seen or key.lower() not in title.lower():
                continue
            d = FS.parse_date(g('pubDate'))
            if d < cut:
                continue
            pf = FS.parse_funding(title, region)
            comp = pf['cn']
            if not comp and region == 'j':
                mm = INV_JP.search(title)
                if mm:
                    comp = mm.group('c').strip()
            if not comp or key.lower() in comp.lower() or len(comp) < 2:
                continue
            got.append({'c': comp, 'd': d, 'u': link, 't': title[:120], 's': src, 'rd': pf['rd']})
            seen.add(link)
            n_new += 1
        time.sleep(0.8)
    got[:] = [x for x in got if x['d'] >= cut][:80]
    if len(pairs) % 25 == 0:
        FS.save('vc_pairs.json', pairs)
FS.save('vc_pairs.json', {k: v for k, v in pairs.items() if v})
print('VC', len(order), '/ 新しく見つけた投資の記事', n_new, '/ 記録のあるVC', sum(1 for v in pairs.values() if v), '/ 会社の延べ数', sum(len(v) for v in pairs.values()))
