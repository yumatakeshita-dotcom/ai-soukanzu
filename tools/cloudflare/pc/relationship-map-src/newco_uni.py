"""ユニコーン一覧(英語版Wikipedia)の会社のうち、まだ図がない会社の図を自動で作る。
元データ: unicorns.json(創業者・評価額) と uni_cos.json(Wikidata: 創業者・CEO・会長・所有者・親会社)。人物の名前は英語表記のまま。"""
import json, os, re
from newco_data import mk, std

S = os.path.dirname(os.path.abspath(__file__))
COUNTRY = {'United States': 'アメリカ', 'China': '中国', 'India': 'インド', 'Israel': 'イスラエル', 'France': 'フランス', 'United Kingdom': 'イギリス', 'Germany': 'ドイツ',
           'Canada': 'カナダ', 'South Korea': '韓国', 'Brazil': 'ブラジル', 'Japan': '日本', 'Singapore': 'シンガポール', 'Sweden': 'スウェーデン', 'Switzerland': 'スイス',
           'Netherlands': 'オランダ', 'Australia': 'オーストラリア', 'Ireland': 'アイルランド', 'Spain': 'スペイン', 'Finland': 'フィンランド', 'Indonesia': 'インドネシア'}
NOTE = ('創業者・CEO・会長・株主は、英語版Wikipediaの「ユニコーン一覧」とWikidataの記録(2026年11月取得)に基づきます。評価額は資金調達時の報道ベースの推定値です。'
        '出資したVCなどの投資家は、この図には入っていません。人物の名前は英語表記のままです。記録のない人は載っていない場合があります。')
ROLE = {'founder': ('創業者', 'p'), 'ceo': ('CEO(Wikidata)', 'p'), 'chair': ('会長(Wikidata)', 'p'), 'owner': ('株主(個人・Wikidata)', 'i')}


def _n(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())


def n2(s):
    """既存の図と同じ会社かを調べるための名前(『AI』『Inc』などの語尾を除く)。Perplexity AI と Perplexity を同じ会社とみなす"""
    x = _n(s)
    for suf in ('technologies', 'technology', 'holdings', 'labs', 'inc', 'ai'):
        if x.endswith(suf) and len(x) > len(suf) + 3:
            x = x[:-len(suf)]
    return x


def _vc_index():
    f = os.path.join(S, 'vc_inv.json')
    idx = {}
    if os.path.exists(f):
        for k, v in json.load(open(f, encoding='utf-8')).items():
            vn = v.get('jp') or v['en']
            for p in v.get('p', []):
                for nm in (p[0], p[1]):
                    if nm:
                        idx.setdefault(n2(nm), [])
                        if vn not in idx[n2(nm)]:
                            idx[n2(nm)].append(vn)
    # 公式サイトの投資先ページ(vc_official.py)とYコンビネーターの一覧も加える
    try:
        from vc_official import OFFICIAL
        disp = {}
        for ln in open(os.path.join(S, 'vc_names.txt'), encoding='utf-8'):
            a = (ln.rstrip('\n').split('|') + [''] * 7)[:7]
            disp[a[0]] = a[6] or re.sub(r'\s*\(.*?\)', '', a[3] or a[4])
        items = dict(OFFICIAL)
        yf = os.path.join(S, 'vc_yc.json')
        if os.path.exists(yf):
            items['yc'] = ('', ', '.join(json.load(open(yf, encoding='utf-8'))))
        for k, (_u, names) in items.items():
            vn = disp.get(k, k)
            for nm in [x.strip() for x in names.split(', ') if x.strip()]:
                idx.setdefault(n2(nm), [])
                if vn not in idx[n2(nm)]:
                    idx[n2(nm)].append(vn)
    except ImportError:
        pass
    return idx


def build(existing):
    VCIDX = _vc_index()
    f = os.path.join(S, 'uni_cos.json')
    uc = json.load(open(f, encoding='utf-8')) if os.path.exists(f) else {}
    uni = json.load(open(os.path.join(S, 'unicorns.json'), encoding='utf-8'))
    co, lst, used = {}, [], set()
    for u in uni:
        nk = _n(u['n'])
        if not nk or n2(u['n']) in existing:
            continue
        c = uc.get(u['n'], {})
        N, EN, seen, i = [], {}, set(), 0
        try:
            year = int(re.match(r'(\d{4})', u.get('d') or '').group(1))
        except Exception:
            year = 2020
        cn = '・'.join(COUNTRY.get(x, x) for x in u.get('c', [])) or '国は未確認'
        v = u['v']
        vt = ('%.2f兆ドル' % (v / 1000)) if v >= 1000 else ('%s十億ドル' % v)
        N.append({'id': 'co', 'name': u['n'], 'kind': 'c', 'from': year, 'desc': '%s(ユニコーン。%s、分野: %s)。評価額は約%s(%s時点の記録、英語版Wikipediaの一覧・報道ベース)。' % (u['n'], cn, u.get('i') or '未確認', vt, u.get('d') or '?')})
        people = [{'en': x['t'] or x['n'], 'ja': '', 'role': 'founder', 'from': 0} for x in u.get('f', [])] + c.get('people', [])
        order = {'founder': 0, 'ceo': 1, 'chair': 2, 'owner': 3}
        for p in sorted(people, key=lambda x: order.get(x['role'], 9)):
            nm = p.get('en') or p.get('ja')
            if not nm or _n(nm) in seen:
                continue
            seen.add(_n(nm))
            role, kind = ROLE[p['role']]
            i += 1
            d = {'id': 'p%d' % i, 'name': nm, 'kind': kind, 'from': p.get('from') or year, 'desc': ('英語版Wikipediaのユニコーン一覧に創業者として載っています。' if p['role'] == 'founder' and not p.get('id') else 'Wikidataの記録(2026年11月取得)。'), 'role': role}
            if p['role'] == 'founder':
                d['founder'] = 1
                d['from'] = year
            N.append(d)
            if p.get('en') or nm:
                EN['p%d' % i] = p.get('en') or nm
        for o in c.get('orgs', []):
            nm = o.get('ja') or o.get('en')
            if not nm or _n(nm) in seen:
                continue
            seen.add(_n(nm))
            i += 1
            N.append({'id': 'o%d' % i, 'name': nm, 'kind': 'i', 'from': year, 'desc': 'Wikidataの「%s」の記録(2026年11月取得)。' % ('親会社' if o['role'] == 'parent' else '所有者'), 'role': '親会社・株主(Wikidata)'})
        for vn in VCIDX.get(n2(u['n']), [])[:8]:      # VCの投資先の記録(Wikipedia)に、この会社が載っていれば、出資者として加える
            if _n(vn) in seen:
                continue
            seen.add(_n(vn))
            i += 1
            N.append({'id': 'v%d' % i, 'name': vn, 'kind': 'i', 'from': year, 'desc': 'このVC・投資家の投資先として、Wikipediaに載っています(2026年11月取得。投資の時期・金額は未確認)。', 'role': 'VC・投資家(Wikipediaの投資先の記録)'})
        if len(N) < 2:
            continue      # 関係する人・組織の記録がない会社は、図を作らない
        key = 'un_' + (nk[:24] or 'x')
        while key in used:
            key += 'x'
        used.add(key)
        co[key] = mk(N, std('co'), EN, {}, {}, {}, {}, {}, 'co')
        lst.append({'key': key, 'name': u['n'], 'min': year, 'note': NOTE})
    return co, lst
