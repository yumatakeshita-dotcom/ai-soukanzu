"""日本のVC(Coral Capital・インキュベイトファンド・Beyond Next Ventures)の、公式の『投資先』ページから、投資先の会社名を集める。
 robots.txt で禁止されていない公式ページだけ。会社名だけを記録し、出典は、そのVCの公式ページ。 出力: jpvc_portfolio.json
使い方: python -u fetch_jpvc_portfolio.py"""
import html, json, os, re, sys, urllib.request
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
S = os.path.dirname(os.path.abspath(__file__))
H = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
def g(u):
    try:
        return urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40).read().decode('utf-8', 'replace')
    except Exception:
        return ''
def clean(n):
    n = html.unescape(n).strip()
    n = re.sub(r'株式会社|\(株\)|（株）|Inc\.?$|Co\.,? ?Ltd\.?$', '', n).strip(' 　,.')
    return n
JUNK = re.compile(r'^(AREA|CATEGORY|STATUS|FUND|JA|EN|STORY LIST|General Partner|領域／ジャンル|ステータス|twitter|facebook|Linked ?in|メール|email|logo|menu|search|close|more)', re.I)
SRC = [('Coral Capital', 'https://coralcap.co/portfolio/', 'alt'), ('インキュベイトファンド', 'https://www.incubatefund.com/portfolio', 'alt'), ('Beyond Next Ventures', 'https://beyondnextventures.com/portfolio/', 'title')]
rows = []
for vc, url, mode in SRC:
    h = g(url)
    if mode == 'alt':
        names = re.findall(r'<img[^>]*alt="([^"]{2,40})"', h)
    else:
        names = [re.sub(r'<[^>]+>', '', a) for a in re.findall(r'<(?:h[2-5]|p|span|div)[^>]*class="[^"]*(?:name|title|company)[^"]*"[^>]*>(.{2,60}?)</', h, flags=re.S)]
    seen = set()
    for n in names:
        n = clean(n)
        if not n or JUNK.search(n) or n.lower() in seen or len(n) < 2 or n.lower() == vc.lower() or 'ファンド' in n and len(n) > 10:
            continue
        seen.add(n.lower())
        rows.append({'src': vc, 'dst': n, 'kind': '出資', 'label': '公式の投資先ページ', 'year': '', 'amount': '', 'note': '%sの公式の投資先ページの記載' % vc, 'url': url, 'media': vc + '(公式)', 'd': ''})
    print(vc, len(seen), flush=True)
json.dump(rows, open(os.path.join(S, 'jpvc_portfolio.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('合計', len(rows))
