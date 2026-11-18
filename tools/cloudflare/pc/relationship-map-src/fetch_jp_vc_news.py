"""日本のVCの名前で、PR TIMESの資金調達・出資の発表を探し、題名にそのVCの名前が出ているものを『VC → 会社』の出資として記録する。
出典=その発表のページ。題名の会社名は、読点の前から取る(取れないものは載せない)。 出力: money_jpvc_news.json
使い方: python -u fetch_jp_vc_news.py"""
import html, json, os, re, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
S = os.path.dirname(os.path.abspath(__file__))
H = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
VCS = {'ANRI': ['ANRI'], 'WiL': ['WiL'], 'ANOBAKA': ['ANOBAKA'], 'ジャフコ': ['ジャフコ', 'JAFCO'], 'Beyond Next Ventures': ['Beyond Next Ventures', 'BNV'], 'DNX Ventures': ['DNX Ventures', 'DNX'],
       'インキュベイトファンド': ['インキュベイトファンド'], 'Coral Capital': ['Coral Capital'], 'UTEC': ['UTEC', '東京大学エッジキャピタル'], 'Genesia Ventures': ['ジェネシア・ベンチャーズ', 'Genesia'],
       'グロービス・キャピタル・パートナーズ': ['グロービス・キャピタル・パートナーズ', 'グロービス'], 'XTech Ventures': ['XTech Ventures', 'Xtech Ventures'], 'Skyland Ventures': ['Skyland Ventures'], 'SBIインベストメント': ['SBIインベストメント'],
       '三菱UFJキャピタル': ['三菱UFJキャピタル'], 'みずほキャピタル': ['みずほキャピタル'], '日本ベンチャーキャピタル': ['日本ベンチャーキャピタル'], 'ニッセイ・キャピタル': ['ニッセイ・キャピタル'],
       'Archetype Ventures': ['Archetype Ventures'], 'Spiral Capital': ['Spiral Capital', 'スパイラル・キャピタル'], 'Z Venture Capital': ['Z Venture Capital', 'ZVC'], 'KDDI Open Innovation Fund': ['KDDI Open Innovation Fund', 'KOIF'],
       '東京大学協創プラットフォーム開発': ['東大IPC', '東京大学協創プラットフォーム開発'], 'Sozo Ventures': ['Sozo Ventures'], 'ソニーイノベーションファンド': ['ソニーイノベーションファンド', 'Sony Innovation Fund'],
       'MTGベンチャーズ': ['MTGベンチャーズ'], 'STRIVE': ['STRIVE', 'ストライブ'], 'East Ventures': ['East Ventures'], 'サイバーエージェント・キャピタル': ['サイバーエージェント・キャピタル'],
       'リアルテックファンド': ['リアルテックファンド', 'リアルテックホールディングス'], 'ものづくりベンチャーズ': ['Monozukuri Ventures', 'ものづくりベンチャーズ'], 'KVP': ['KVP', 'Kyoto University Venture Partners'], 'Light Street': ['Light Street'],
       'DCM': ['DCM Ventures', 'DCM'], 'B Dash Ventures': ['B Dash Ventures', 'ビーダッシュ'], 'ミクシィ': ['MIXI VENTURES', 'ミクシィ'], 'SMBCベンチャーキャピタル': ['SMBCベンチャーキャピタル'], 'NTTドコモ・ベンチャーズ': ['NTTドコモ・ベンチャーズ'],
       'ドーガン・ベータ': ['ドーガン', 'DOGAN'], 'Heart Beat Capital': ['Heart Beat Capital'], 'ミドリムシ': []}
BADTITLE = re.compile(r'調査|アンケート|セミナー|ウェビナー|キャンペーン|採用|開催|登壇|募集|ファンド組成|ファンド設立|募集開始|LP|キャピタルコール|新ファンド|ファイナルクローズ|ファーストクローズ|1stクローズ|1stクローズ|第\d+号|号ファンド')


def get(u):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40).read().decode('utf-8', 'replace')
        except Exception:
            time.sleep(2 * (i + 1))
    return ''


def company(t):
    head = re.split(r'[、,]|が資金|が出資|の資金調達|は、|は資金', t)[0]
    head = re.sub(r'^(?:【[^】]*】)+', '', head).strip()
    m = re.search(r'(?:を提供する|を展開する|を運営する|を開発する|を手がける|を手掛ける|のAI|向けの?)([^、]{2,20})$', head)
    if m:
        head = m.group(1)
    head = re.sub(r'^(?:株式会社)\s*|\s*株式会社$', '', head).strip()
    if not head or len(head) > 22 or re.search(r'[「」『』（）()]', head):
        return ''
    if re.search(r'(?:から|ほか|など|による|について)$', head):
        return ''
    return head


rows, seen = [], set()
for vc, names in VCS.items():
    got = 0
    for nm in names:
        for kw in (nm + ' 出資', nm + ' 資金調達'):
            h = get('https://prtimes.jp/main/action.php?run=html&page=searchkey&search_word=%s&search_pattern=1' % urllib.parse.quote(kw))
            for m in re.finditer(r'href="(/main/html/rd/p/[0-9.]+\.html)"[^>]*>(.*?)</a>', h, flags=re.S):
                t = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
                d = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', t)
                t = re.sub(r'\d{4}年\d{1,2}月\d{1,2}日.*$', '', t).strip()
                if not any(n in t for n in names) or not re.search(r'調達|出資|増資', t) or BADTITLE.search(t):
                    continue
                c = company(t)
                if not c or c in names or vc in c:
                    continue
                k = (vc, c)
                if k in seen:
                    continue
                seen.add(k)
                got += 1
                dd = '%04d-%02d-%02d' % tuple(map(int, d.groups())) if d else ''
                rows.append({'src': vc, 'dst': c, 'kind': '資金調達', 'label': '', 'year': dd[:4], 'amount': (re.search(r'([0-9,.]+(?:億|万)?円)', t) or [None, ''])[1] if re.search(r'([0-9,.]+(?:億|万)?円)', t) else '', 'd': dd, 'url': 'https://prtimes.jp' + m.group(1), 'media': 'PR TIMES', 'note': t[:160]})
            time.sleep(0.7)
    print(vc, got, flush=True)
json.dump(rows, open(os.path.join(S, 'money_jpvc_news.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('合計', len(rows))
