"""日本のVCの公式サイトの出資先ページから、出資先の会社名を集める。 出典=そのVC公式の出資先ページ。
対象: Coral Capital / インキュベイトファンド / SMBCベンチャーキャピタル / NTTドコモ・ベンチャーズ / UTEC / Genesia Ventures
出力: money_official_jp.json    使い方: python -u fetch_vc_jp_official.py"""
import html, json, os, re, sys, urllib.request
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
S = os.path.dirname(os.path.abspath(__file__))
H = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
GEN = re.compile(r'^(?:logo|icon|repeat-icon.*|menu|メニュー|閉じる|twitter|facebook|linked ?in|youtube|arrow.*|ロゴ|more|next|prev|top|close|search|.*(?:ベンチャーキャピタル|ベンチャーズ|Capital|ファンド|Fund)$)', re.I)


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read().decode('utf-8', 'replace')


def alts(h):
    return [html.unescape(a).strip() for a in re.findall(r'<img[^>]+alt="([^"]{2,50})"', h)]


def norm(n):
    n = re.sub(r'^(?:株式会社|\(株\)|㈱)\s*|\s*(?:株式会社|Inc\.?|Co\.,? ?Ltd\.?)$', '', n.strip())
    n = re.sub(r'[,.、。]+$', '', n.strip())
    n = re.sub(r'\s*(?:Pvt\.? ?Ltd\.?|S\.r\.l\.?|GmbH|Ltd\.?|LLC|B\.V\.?)$', '', n).strip()
    return n


def utec(h):
    out = []
    for m in re.finditer(r'<a\b[^>]*href="https://www\.ut-ec\.co\.jp/our_companies/([a-z0-9_\-]+)/?"[^>]*>(.*?)</a>', h, flags=re.S):
        t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', m.group(2)))).strip()
        a = re.search(r'alt="([^"]{2,40})"', m.group(0))
        out.append(t if t and len(t) < 40 else (a.group(1) if a else m.group(1).replace('_', ' ').replace('-', ' ').title()))
    return out


T = [('Coral Capital', 'https://coralcap.co/portfolio/', lambda h: alts(h)),
     ('インキュベイトファンド', 'https://incubatefund.com/portfolio/', lambda h: alts(h)),
     ('SMBCベンチャーキャピタル', 'https://www.smbc-vc.co.jp/portfolio/', lambda h: alts(h)),
     ('NTTドコモ・ベンチャーズ', 'https://www.nttdocomo-v.com/portfolio/', lambda h: alts(h)),
     ('UTEC', 'https://www.ut-ec.co.jp/portfolio/', utec),
     ('Genesia Ventures', 'https://genesiaventures.com/portfolio/', lambda h: alts(h))]
rows = []
for vc, url, fn in T:
    try:
        h = get(url)
    except Exception as e:
        print(vc, 'ERR', str(e)[:60]); continue
    names = []
    for n in fn(h):
        n = norm(n)
        if not n or GEN.match(n) or n in (vc, 'SMBC', 'SMBCグループ') or len(n) > 40 or n in names or re.search(r'READ MORE|MORE$', n):
            continue
        names.append(n)
    print(vc, len(names), names[:14], flush=True)
    for n in names:
        rows.append({'src': vc, 'dst': n, 'kind': '出資', 'label': '公式の出資先ページ', 'year': '', 'amount': '', 'note': '%s公式の出資先ページに掲載' % vc, 'url': url, 'media': vc + ' 公式', 'd': ''})
json.dump(rows, open(os.path.join(S, 'money_official_jp.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('合計', len(rows))
