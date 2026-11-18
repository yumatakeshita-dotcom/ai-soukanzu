"""VCの公式サイトの出資先ページ(サーバー側で作られた一覧)から、出資先の会社名を集める。 出典=そのVC公式の出資先ページ。
対象: Accel / Greylock / General Catalyst / Index Ventures / Union Square Ventures (リンクの文字か、アドレスの末尾から会社名を取る)
出力: money_official.json    使い方: python -u fetch_vc_official.py"""
import html, json, os, re, sys, urllib.request
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
S = os.path.dirname(os.path.abspath(__file__))
H = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
T = [('Accel', 'https://www.accel.com/relationships', r'/companies/([a-z0-9\-]+)'),
     ('Greylock Partners', 'https://greylock.com/portfolio/', r'/portfolio/([a-z0-9\-]+)'),
     ('General Catalyst', 'https://www.generalcatalyst.com/portfolio', r'/companies/([a-z0-9\-]+)'),
     ('Index Ventures', 'https://www.indexventures.com/companies/', r'/companies/([a-z0-9\-]+)'),
     ('Union Square Ventures', 'https://www.usv.com/companies/', r'/portfolio/company/([a-z0-9\-]+)')]
BADSLUG = {'backed', 'portfolio', 'all', 'companies', 'categories', 'category', 'filter', 'search', 'new', 'exits', 'index'}
rows = []
for vc, url, pat in T:
    h = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60).read().decode('utf-8', 'replace')
    got = {}
    for m in re.finditer(r'<a\b[^>]*href="[^"]*' + pat + r'/?"[^>]*>(.*?)</a>', h, flags=re.S):
        slug = m.group(1)
        if slug in BADSLUG or slug in got:
            continue
        txt = html.unescape(re.sub(r'<[^>]+>', ' ', m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(0)))
        txt = re.sub(r'\s+', ' ', txt).strip()
        im = re.search(r'alt="([^"]{2,40})"', m.group(0))
        name = (im.group(1) if im and len(txt) > 40 else txt) if txt else (im.group(1) if im else '')
        lab = ''
        if vc.startswith('Union Square') and re.match(r'^(Seed|Series|Pre|Growth|Early|Late)', name):
            lab = re.sub(r'\s+(NASDAQ|NYSE).*$', '', name)
            name = slug.replace('-', ' ').title()
        if not name or len(name) > 40:
            name = slug.replace('-', ' ').title()
        name = re.sub(r'\s+logo$', '', name, flags=re.I)
        name = re.sub(r'\s+(?:NASDAQ|NYSE|AMS|LSE|TSE|EPA|ETR|SIX|TYO|HKG|NYSE American|TSX|ASX|KRX|STO|BIT).*$', '', name).strip()
        got[slug] = (name, lab)
    print(vc, len(got), [v[0] for v in list(got.values())[:12]], flush=True)
    for slug, (name, lab) in got.items():
        ym = re.search(r'(20\d\d|19\d\d)', lab)
        rows.append({'src': vc, 'dst': name, 'kind': '出資', 'label': ('公式の出資先ページ ' + lab).strip(), 'year': ym.group(1) if ym else '', 'amount': '', 'note': '%s公式の出資先ページに掲載' % vc, 'url': url, 'media': vc + ' 公式', 'd': ''})
json.dump(rows, open(os.path.join(S, 'money_official.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('合計', len(rows))
