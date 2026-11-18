"""資金調達のニュース(見出し・抜粋)から『どのVCが、どの会社に投資したか』を見つける。Claude不要。
funding_news.json / relation_news.json の見出しから、「…raises $X led by ○○ and △△」「…が資金調達。引受先はグロービス・キャピタル…」の形を拾う。
出力: vc_news.json  [{c:会社, v:[投資家...], t:見出し, u:URL, d:日付, s:出どころ}] (履歴は積み上げ、90日で古いものを落とす)"""
import datetime as dt, json, os, re, sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))


def ld(n, d):
    f = os.path.join(S, n)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else d


news = ld('funding_news.json', []) + ld('relation_news.json', []) + ld('vc_news_raw.json', [])
JP_INV = re.compile(r'(?:リード(?:投資家|インベスター|VC|投資家は)?(?:は|を|に|:|：)|引受先(?:は|として|:|：)|出資(?:者|先)?(?:は|:|：)|(?:が|を)リード(?:投資家)?(?:として|に))\s*([^。\n]{2,60})')
vcs = ld('vc_inv.json', {})
known = {}
for k, v in vcs.items():
    for nm in (v['en'], v['jp']):
        if nm and len(nm) >= 3:
            known[re.sub(r'\s*\(.*?\)', '', nm).strip().lower()] = v['jp'] or v['en']
JPVC = ['ジャフコ', 'グロービス・キャピタル', 'インキュベイトファンド', 'WiL', 'DCM', 'ANRI', 'UTEC', 'Coral Capital', 'ZVC', 'East Ventures', 'ベンチャーキャピタル', 'ベンチャーズ', 'キャピタル', 'ファンド']
INV = re.compile(r'(Capital|Ventures?|Partners|Fund|Investments?|Equity|Holdings|Labs|Management|Group)$')
EN_PAT = re.compile(r'^(?P<c>.{2,45}?)\s+(?:raises?|raised|secures?|lands?|closes?|nabs?|bags?|scores?|gets?|banks?|snags?|announces?)\b.*?\b(?:led by|co-led by|backed by|from|with participation from)\s+(?P<v>[^.;|]+)', re.I)
JP_PAT = re.compile(r'^(?P<c>[^、。「」【】\s]{2,24}?)(?:が|は|、).*?(?:資金調達|調達|出資|増資)')
out = ld('vc_news.json', [])
seen = {x['u'] for x in out}
today = dt.date.today()
new = 0
for h in news:
    u = h.get('u')
    if not u or u in seen:
        continue
    t = h.get('t', '')
    blob = t + ' ' + (h.get('x') or '')
    inv, comp = [], ''
    m = EN_PAT.match(t)
    if m:
        comp = m.group('c').strip(' ,:-–')
        parts = re.split(r',\s*|\s+and\s+|\s*&\s*|\s+with\s+', re.sub(r'\b(?:and|with)\s+(?:participation|others|existing).*$', '', m.group('v')))
        for p in parts:
            p = re.sub(r'\s*[-–|].*$', '', p).strip(' .')
            if 3 <= len(p) <= 40 and (p.lower() in known or INV.search(p)) and not re.search(r'\d', p):
                inv.append(known.get(p.lower(), p))
    elif h.get('r') == 'j' or re.search(r'[ぁ-ん]', t):
        mj = JP_PAT.match(t)
        if mj and re.search(r'資金調達|調達|出資|増資', t):
            for k, v in known.items():
                if re.search(r'[ぁ-んァ-ヶ一-龥]', v) and v in blob:
                    inv.append(v)
            mi = JP_INV.search(blob)
            if mi:      # 「リードは○○、△△」の形から、投資家らしい名前(キャピタル・ベンチャーズ・ファンドなど)を拾う
                for p in re.split(r'[、,・/]|および|及び|と|、', mi.group(1)):
                    p = re.sub(r'(?:など|ほか|他).*$', '', p).strip(' 「」『』()（）')
                    if 2 <= len(p) <= 30 and re.search(r'キャピタル|ベンチャーズ?|ファンド|パートナーズ|Capital|Ventures|Partners|Fund|インベストメント', p):
                        inv.append(p)
            comp = mj.group('c')
    if comp and inv:
        out.append({'c': comp, 'v': sorted(set(inv)), 't': t[:140], 'u': u, 'd': h.get('d', ''), 's': h.get('s', '')})
        seen.add(u)
        new += 1
cut = (today - dt.timedelta(days=90)).isoformat()
out = [x for x in out if x['d'] >= cut]
json.dump(out, open(os.path.join(S, 'vc_news.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('VCのニュース: 新規', new, '件 / 履歴', len(out), '件')
for x in out[:6]:
    print(' ', x['c'], '<-', x['v'], '|', x['t'][:60])
