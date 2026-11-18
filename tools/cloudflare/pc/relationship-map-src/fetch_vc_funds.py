"""日本のVC等が公表した「ファンド組成・クローズ」の発表(PR TIMES)から、運用会社・ファンド名・規模・公表されたLP(出資者)を集める。
LP(出資者)の内訳は、公表されたものだけ。公表のない部分は、空欄のまま(推測しない)。出力: vc_funds.json
使い方: python -u fetch_vc_funds.py [ページ数]"""
import html, json, os, re, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 3
KW = ['ファンド組成 ベンチャーキャピタル', 'ファンド 1stクローズ', 'ファンド ファイナルクローズ', 'ファンド 設立 LP出資', 'VC ファンド 組成 億円', 'ベンチャーファンド 募集 完了', 'CVCファンド 設立', 'ファンド 有限責任組合員 出資', '投資事業有限責任組合 組成 スタートアップ']
CACHE = os.path.join(S, 'vc_funds_cache.json')
cache = json.load(open(CACHE, encoding='utf-8')) if os.path.exists(CACHE) else {}


def g(u):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode('utf-8', 'replace')
        except Exception:
            time.sleep(2 * (i + 1))
    return ''


items = {}
for kw in KW:
    for pg in range(1, PAGES + 1):
        h = g('https://prtimes.jp/main/action.php?run=html&page=searchkey&search_word=%s&search_pattern=1&pagenum=%d' % (urllib.parse.quote(kw), pg))
        for m in re.finditer(r'href="(/main/html/rd/p/[0-9.]+\.html)"[^>]*>(.*?)</a>', h, flags=re.S):
            t = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
            d = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', t)
            t = re.sub(r'\d{4}年\d{1,2}月\d{1,2}日.*$', '', t).strip()
            if re.search(r'ファンド', t) and re.search(r'組成|クローズ|設立|募集|総額|規模|億円', t) and not re.search(r'セミナー|ウェビナー|キャンペーン|採用|開催|調査|ETF|投資信託|不動産|REIT|NISA|FX|暗号', t) and m.group(1) not in items:
                items[m.group(1)] = (t, '%04d-%02d-%02d' % tuple(map(int, d.groups())) if d else '')
        time.sleep(0.7)
print('対象の発表', len(items), flush=True)
rows, tot = [], 0
for u, (t, d) in items.items():
    if u not in cache:
        p = g('https://prtimes.jp' + u)
        txt = re.sub(r'<script.*?</script>|<style.*?</style>', '', p, flags=re.S)
        txt = re.sub(r'<br\s*/?>|</p>|</li>|</tr>|</div>|</h\d>|</td>', '\n', txt)
        txt = html.unescape(re.sub(r'<[^>]+>', '', txt))
        cache[u] = re.sub(r'[ \t　]+', ' ', txt)[:30000]
        time.sleep(0.6); tot += 1
        if tot % 20 == 0:
            json.dump(cache, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
    body = cache[u]
    size = re.search(r'(?:総額|規模|組成額|運用総額|ファンド総額|最終|合計)[^。\n]{0,20}?(約?[0-9,.，]+(?:億|万)?円(?:規模)?)', body) or re.search(r'(約?[0-9,.，]+億円)', t)
    name = re.search(r'[「『]([^」』]{3,40}ファンド[^」』]{0,10})[」』]', t) or re.search(r'([^\s、「」]{2,30}ファンド[0-9０-９一二三四五]*号?)', t)
    mgr = re.search(r'^([^、「」\s]{2,24}?)(?:、|が|は|，)', t)
    lps = []
    for line in body.split('\n'):
        line = line.strip()
        m = re.match(r'^(?:[■●◆・\-\s]*)?(?:LP(?:投資家)?|有限責任組合員|出資者|出資企業|主なLP|LP出資者|参画LP|主要LP|引受先|投資家)\s*[：:]\s*(.+)$', line)
        if m and len(line) < 600:
            for p in re.split(r'[、,，・／/]|および|及び', re.sub(r'[「」『』【】]', '', m.group(1))):
                p = re.sub(r'^株式会社\s*|\s*株式会社$|\s*(?:\(|（).*$|\s*(?:等|など|ほか)$', '', p.strip(' 　'))
                if 2 <= len(p) <= 30 and not re.search(r'[0-9]+社|名$|非公開|未公表|代表|取締役|個人|その他', p):
                    lps.append(p)
    if name or size:
        rows.append({'mgr': mgr.group(1) if mgr else '', 'fund': name.group(1) if name else '', 'size': size.group(1) if size else '', 'd': d, 'lps': list(dict.fromkeys(lps))[:20], 'url': 'https://prtimes.jp' + u, 'title': t[:140]})
json.dump(cache, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
json.dump(rows, open(os.path.join(S, 'vc_funds.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('ファンド', len(rows), '件 / LPの名前つき', sum(1 for r in rows if r['lps']), flush=True)
