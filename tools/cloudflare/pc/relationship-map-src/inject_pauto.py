import json, os, re, sys

S = os.path.dirname(os.path.abspath(__file__))
OUTHTML = r'C:\Users\yumat\.claude\output\relationship-maps.html'
wd = json.load(open(os.path.join(S, 'people_wd.json'), encoding='utf-8'))
people = {p['en']: p for p in json.load(open(os.path.join(S, 'people_all.json'), encoding='utf-8'))}
xf = os.path.join(S, 'people_wd_x.json')
if os.path.exists(xf):
    wd.update(json.load(open(xf, encoding='utf-8')))
    for p in json.load(open(os.path.join(S, 'people_all_x.json'), encoding='utf-8')):
        people.setdefault(p['en'], p)
uf = os.path.join(S, 'people_wd_u.json')
if os.path.exists(uf):
    for k, v in json.load(open(uf, encoding='utf-8')).items():
        wd.setdefault(k, v)
    for p in json.load(open(os.path.join(S, 'people_all_u.json'), encoding='utf-8')):
        people.setdefault(p['en'], p)
STOP ={'group', 'inc', 'corp', 'corporation', 'company', 'holdings', 'technologies', 'technology', 'international',
        'limited', 'capital', 'partners', 'global', 'systems', 'labs', 'research', 'the', 'and', 'bank', 'financial'}
OCC = re.compile(r'business|executive|entrepreneur|investor|engineer|scientist|researcher|computer|chief|ceo|founder|'
                 r'venture|banker|professor|financier|programmer|economist|software|inventor|technology|manager|'
                 r'billionaire|philanthrop|lawyer|politician|physicist|mathematician|chairman|director', re.I)


def year(t):
    m = re.match(r'^([+-]\d+)', t or '')
    return int(m.group(1)) if m else None


stat = {'ok': 0, 'maybe': 0, 'no': 0}
auto = {}
for en, r in wd.items():
    p = people.get(en)
    if not p or not r.get('q') or r.get('dis') or not r.get('human'):
        stat['no'] += 1
        continue
    text = ((r.get('ex') or '') + ' ' + (r.get('desc') or '')).lower()
    toks = set()
    for c in p['co']:
        for w in re.findall(r'[a-z0-9]+', c[1].lower()):
            if len(w) >= 4 and w not in STOP:
                toks.add(w)
    match = any(re.search(r'\b' + re.escape(t) + r'\b', text) for t in toks)
    occ = bool(OCC.search(text))
    dob = r.get('dob')
    ok_dob = True
    if dob:
        y = year(dob[0])
        froms = [c[3] for c in p['co'] if c[3] and c[5] == 'p']
        if y and froms and (min(froms) < y + 14 or y < 1900):
            ok_dob = False
        if y and (y > 2008 or y < 1930):
            ok_dob = False
    if not ok_dob:
        stat['no'] += 1
        continue
    if match:
        flag = 0
        stat['ok'] += 1
    elif occ:
        flag = 1
        stat['maybe'] += 1
    else:
        stat['no'] += 1
        continue
    pob = r.get('pob')
    auto[en] = [dob, pob, r.get('cit') or [], r.get('edu') or [], r.get('occ') or [], r.get('dod'),
                r.get('jaw'), r.get('enw') or r.get('title'), flag]
print(stat, len(auto))
s = open(OUTHTML, encoding='utf-8').read()
js = json.dumps(auto, ensure_ascii=False, separators=(',', ':'))
assert 'const PAUTO=/*PAUTO*/{};' in s
s = s.replace('const PAUTO=/*PAUTO*/{};', 'const PAUTO=' + js.replace('</', '<\\/') + ';')
uni = os.path.join(S, 'unicorns.json')
if os.path.exists(uni):
    assert 'const UNI=/*UNI*/[];' in s
    s = s.replace('const UNI=/*UNI*/[];', 'const UNI=' + open(uni, encoding='utf-8').read().replace('</', '<\\/') + ';')
for _ph, _fn, _empty in (('const SEC=/*SEC*/[];', 'sec_ipo.json', '[]'), ('const NEWS=/*NEWS*/[];', 'funding_news.json', '[]'), ('const RELNEWS=/*RELNEWS*/[];', 'relation_news.json', '[]'), ('const YNEWS=/*YNEWS*/{};', 'yahoo_cos.json', '{}'), ('const GNEWS=/*GNEWS*/{};', 'news_cos.json', '{}')):
    if _ph in s:
        _f = os.path.join(S, _fn)
        _js = open(_f, encoding='utf-8').read().replace('�', '') if os.path.exists(_f) else _empty
        if _fn in ('news_cos.json', 'yahoo_cos.json'):      # ページの大きさを抑えるため、1社あたりの件数を絞る
            _d = json.loads(_js)
            _cap = 4 if _fn == 'news_cos.json' else 3
            _js = json.dumps({k: v[:_cap] for k, v in _d.items()}, ensure_ascii=False, separators=(',', ':'))
        s = s.replace(_ph, _ph.split('=')[0] + '=' + _js.replace('</', '<\\/') + ';')
if 'const VENT=/*VENT*/{};' in s:
    vent = {}
    vf = os.path.join(S, 'ventures_wd.json')
    if os.path.exists(vf):
        for p, rows in json.load(open(vf, encoding='utf-8')).items():
            vent[p] = [[r[0], r[1], r[2], r[3], r[4], 'w', ''] for r in rows]
    mf = os.path.join(S, 'ventures_manual.json')
    if os.path.exists(mf):
        for p, rows in json.load(open(mf, encoding='utf-8')).items():
            have = {r[0].lower() for r in rows} | {r[4].lower() for r in rows}
            vent[p] = rows + [r for r in vent.get(p, []) if r[0].lower() not in have and (r[4] or '').lower() not in have]
    s = s.replace('const VENT=/*VENT*/{};', 'const VENT=' + json.dumps(vent, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';')
    print('VENT people', len(vent))
if 'const ACQ=/*ACQ*/{};' in s:
    acq = {}
    nrm = lambda t: re.sub(r'[\s・･·.\-_,]', '', (t or '').lower())
    af = os.path.join(S, 'acq.json')
    if os.path.exists(af):  # Wikipedia一覧: [名前,年,金額,説明,記事名]
        for k, rows in json.load(open(af, encoding='utf-8')).items():
            acq[k] = [[r[0], r[1], r[2], r[3], 'w', 0] for r in rows]
    wf = os.path.join(S, 'acq_wd.json')
    if os.path.exists(wf):  # Wikidata: [名前,年,種類,終了年,英語名]
        for k, rows in json.load(open(wf, encoding='utf-8')).items():
            have = {nrm(r[0]) for r in acq.get(k, [])}
            for r in rows:
                if nrm(r[0]) in have or (r[4] and nrm(r[4]) in have):
                    continue
                if re.search(r'patent', str(r[2]), re.I):      # 特許は会社ではないので載せない(IBMなどで数万件になる)
                    continue
                have.add(nrm(r[0]))
                acq.setdefault(k, []).append([r[0], r[1], '', r[2], 'd', r[3]])
    try:      # 手で調べた最近の買収(acq_manual.py)
        sys.path.insert(0, S)
        from acq_manual import ACQM
        from yen import yenify
        for k, rows in ACQM.items():
            have = {nrm(r[0]) for r in acq.get(k, [])}
            for r in rows:
                if nrm(r[0]) not in have:
                    r = list(r)
                    r[2], r[3] = yenify(r[2]), yenify(r[3])
                    acq.setdefault(k, []).append(r)
    except ImportError:
        pass
    s = s.replace('const ACQ=/*ACQ*/{};', 'const ACQ=' + json.dumps(acq, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';')
    print('ACQ companies', len(acq), 'rows', sum(len(v) for v in acq.values()))
if "const BUILT=/*BUILT*/'';" in s:
    import datetime
    s = s.replace("const BUILT=/*BUILT*/'';", "const BUILT='" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + "';")
if 'const VCS=/*VCS*/{};' in s:
    vf = os.path.join(S, 'vc_inv.json')
    vcs = {}
    if os.path.exists(vf):
        for k, v in json.load(open(vf, encoding='utf-8')).items():
            vcs[k] = {'en': v['en'], 'jp': v['jp'], 'region': v['region'], 'kind': v['kind'], 'desc': v.get('desc', ''), 'wiki': v.get('wiki', []), 'site': '',
                      'p': [[p[0], p[1], p[2]] for p in v.get('p', [])]}
    try:      # 公式サイトの投資先ページから読み取った会社名を足す(Wikipedia由来と重なるものは足さない)
        sys.path.insert(0, S)
        from vc_official import OFFICIAL
        yf = os.path.join(S, 'vc_yc.json')
        if os.path.exists(yf):      # Y Combinator: Wikipediaの『List of Y Combinator companies』
            OFFICIAL = dict(OFFICIAL)
            OFFICIAL['yc'] = ('https://www.ycombinator.com/companies', ', '.join(json.load(open(yf, encoding='utf-8'))))
        _n = lambda t: re.sub(r'[^a-z0-9ぁ-んァ-ヶ一-龥]', '', (t or '').lower())
        _base = {}
        for _ln in open(os.path.join(S, 'vc_names.txt'), encoding='utf-8'):
            _a = (_ln.rstrip('\n').split('|') + [''] * 7)[:7]
            _base[_a[0]] = {'en': re.sub(r'\s*\(.*?\)', '', _a[3] or _a[4]).strip(), 'jp': _a[6], 'region': _a[1], 'kind': _a[2], 'desc': '', 'wiki': [], 'p': []}
        for k, (url, names) in OFFICIAL.items():
            v = vcs.setdefault(k, _base.get(k) or {'en': k, 'jp': '', 'region': '世界', 'kind': 'VC', 'desc': '', 'wiki': [], 'p': []})
            have = {_n(p[0]) for p in v['p']} | {_n(p[1]) for p in v['p']}
            v['site'] = url
            for nm in [x.strip() for x in names.split(', ') if x.strip()]:
                if _n(nm) and _n(nm) not in have:
                    have.add(_n(nm))
                    v['p'].append([nm, '', 'o'])
    except ImportError:
        pass
    try:      # 本拠地の国(vc_country.py)。確認できていないものは空
        sys.path.insert(0, S)
        from vc_country import COUNTRY
        for k, v in vcs.items():
            v['country'] = COUNTRY.get(k, '')
    except ImportError:
        pass
    try:      # 手で追加したVC(vc_extra.py)。すでに同名があれば、投資先だけ足す
        sys.path.insert(0, S)
        from vc_extra import EXTRA
        _x = lambda t: re.sub(r'[^a-z0-9ぁ-んァ-ヶ一-龥]', '', (t or '').lower())
        _ix = {}
        for k, v in vcs.items():
            for nm in (v['en'], v['jp']):
                if _x(nm):
                    _ix[_x(nm)] = k
        for key, en, jp, ctry, kind, desc, ports in EXTRA:
            k = _ix.get(_x(en)) or _ix.get(_x(jp))
            if not k:
                k = key
                _old = vcs.get(k)      # 公式ページ由来の投資先(OFFICIAL)がすでに同じキーで入っていれば、上書きせず引き継ぐ
                vcs[k] = {'en': en, 'jp': jp, 'region': '日本', 'kind': kind, 'desc': desc, 'wiki': [], 'site': (_old or {}).get('site', ''), 'p': list((_old or {}).get('p', []))}
            v = vcs[k]
            v['country'] = v.get('country') or ctry
            if not v.get('desc'):
                v['desc'] = desc
            have = {_x(p[0]) for p in v['p']}
            for nm in ports:
                if _x(nm) not in have:
                    v['p'].append([nm, '', 'o'])
    except ImportError:
        pass
    xnews = []
    try:      # X(旧Twitter)の投稿で確認できた投資(vc_x.py)と、VCごとのニュース検索の結果(vc_pairs.json)
        sys.path.insert(0, S)
        from vc_x import PAIRS, NEW_VCS
        _y = lambda t: re.sub(r'[^a-z0-9ぁ-んァ-ヶ一-龥]', '', re.sub(r'\(.*?\)|（.*?）|株式会社', '', (t or '')).lower())
        _iy = {}
        for k, v in vcs.items():
            for nm in (v['en'], v['jp']):
                if _y(nm):
                    _iy[_y(nm)] = k
        for key, en, jp, ctry, kind in NEW_VCS:
            if _y(en) not in _iy and _y(jp) not in _iy:
                _o = vcs.get(key) or {}
                vcs[key] = {'en': en, 'jp': jp, 'region': ctry, 'kind': kind, 'desc': '', 'wiki': [], 'site': _o.get('site', ''), 'country': ctry, 'p': list(_o.get('p', []))}
                _iy[_y(en)] = key
                _iy[_y(jp)] = key
            else:      # 公式ページ由来で名前がキーのままのものは、正式な名前・国に直す
                _k = _iy.get(_y(en)) or _iy.get(_y(jp))
                _v = vcs.get(_k)
                if _v and _v.get('en') == _k:
                    _v.update({'en': en, 'jp': jp, 'region': ctry or _v.get('region', ''), 'kind': kind, 'country': _v.get('country') or ctry})
        for inv, comp, d, note, handle in PAIRS:
            k = _iy.get(_y(inv))
            if not k:
                continue
            v = vcs[k]
            if _y(comp) not in {_y(p[0]) for p in v['p']}:
                v['p'].append([comp, '', 'x'])
            xnews.append({'c': comp, 'v': [v['jp'] or v['en']], 't': (note or '出資') + '(Xの投稿' + ('・@' + handle if handle else '') + ')', 'u': ('https://x.com/' + handle) if handle else '', 'd': d, 's': 'X'})
    except ImportError:
        pass
    try:
        vp = os.path.join(S, 'vc_pairs.json')
        if os.path.exists(vp):
            _y2 = lambda t: re.sub(r'[^a-z0-9ぁ-んァ-ヶ一-龥]', '', re.sub(r'\(.*?\)|（.*?）|株式会社', '', (t or '')).lower())

            def _cn(c):      # 「Dellows News 株式会社トレポータル」「高専発…のプロッセルHD」→ 会社名だけに近づける
                c = re.sub(r'^\S+\s(?:News|ニュース)\s', '', c.strip())
                if len(c) > 14 and 'の' in c:
                    c = c.split('の')[-1]
                return c.replace('株式会社', '').strip(' 、,')
            _iy2 = {}
            for k, v in vcs.items():
                for nm in (v['en'], v['jp']):
                    if _y2(nm):
                        _iy2[_y2(nm)] = k
            for vn, items in json.load(open(vp, encoding='utf-8')).items():
                k = _iy2.get(_y2(vn))
                if not k:
                    continue
                v = vcs[k]
                have = {_y2(p[0]) for p in v['p']}
                for it in items:
                    it = dict(it, c=_cn(it['c']))
                    if len(it['c']) < 2:
                        continue
                    if _y2(it['c']) not in have:
                        have.add(_y2(it['c']))
                        v['p'].append([it['c'], '', 'n'])
                    xnews.append({'c': it['c'], 'v': [v['jp'] or v['en']], 't': it['t'], 'u': it['u'], 'd': it['d'], 's': it['s']})
    except Exception as _e:
        print('vc_pairs 失敗', _e)
    bf = os.path.join(S, 'vc_big.json')       # Wikipediaのカテゴリとリンク元から集めた大量のVC・投資先(fetch_vc_big.py)
    if os.path.exists(bf):
        _m = lambda t: re.sub(r'[^a-z0-9ぁ-んァ-ヶ一-龥]', '', (t or '').lower())
        idx = {}
        for k, v in vcs.items():
            for nm in (v['en'], v['jp']):
                if _m(nm):
                    idx[_m(nm)] = k
        added = merged = 0
        for kid, v in json.load(open(bf, encoding='utf-8')).items():
            k = idx.get(_m(v['en'])) or (idx.get(_m(v['jp'])) if v['jp'] else None)
            rows = [[p[0], p[1], 'w'] for p in v['p']]
            if k:
                cur = vcs[k]
                have = {_m(p[0]) for p in cur['p']} | {_m(p[1]) for p in cur['p'] if p[1]}
                for r in rows:
                    if _m(r[0]) not in have and not (r[1] and _m(r[1]) in have):
                        have.add(_m(r[0]))
                        cur['p'].append(r)
                if v.get('site'):
                    cur['home'] = v['site']
                if not cur.get('country') and v.get('country'):
                    cur['country'] = v['country']
                if not cur.get('desc') and v.get('desc'):
                    cur['desc'] = v['desc']
                merged += 1
            elif re.match(r'^(エンジェル投資家|クラウドファンディング.*|ベンチャーデット|ベンチャーキャピタル|創薬ベンチャー.*|GREEN FUNDING|ソーシャルレンディング)$', v['jp'] or v['en'] or ''):
                continue      # 一般名詞(概念)の記事
            elif not v.get('country') and not re.search(r'キャピタル|ベンチャー|ファンド|投資|capital|ventures|partners|fund|invest|equity|holdings|group|labs', (v['en'] or '') + ' ' + (v['jp'] or ''), re.I):
                continue      # 国も分からず、名前にVCらしい語もないもの(概念・人物・サービス名などの誤分類)は入れない
            else:
                vcs[kid] = {'en': v['en'], 'jp': v['jp'], 'region': '', 'kind': v.get('kind', 'VC'), 'desc': v.get('desc', ''), 'wiki': v.get('wiki', []), 'site': '', 'home': v.get('site', ''),
                            'country': v.get('country', ''), 'p': rows}
                idx[_m(v['en'])] = kid
                added += 1
        print('vc_big: 追加', added, '統合', merged)
    s = s.replace('const VCS=' + '/*VCS*/{};', 'const VCS='+ json.dumps(vcs, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';')
    nf = os.path.join(S, 'vc_news.json')
    nj = open(nf, encoding='utf-8').read() if os.path.exists(nf) else '[]'
    _vn = json.loads(nj) + xnews
    _vn.sort(key=lambda x: x['d'], reverse=True)
    nj = json.dumps(_vn, ensure_ascii=False, separators=(',', ':'))
    s = s.replace('const VCNEWS=/*VCNEWS*/[];', 'const VCNEWS=' + nj.replace('</', '<\\/') + ';')
    print('VCS', len(vcs), 'portfolio rows', sum(len(v['p']) for v in vcs.values()))
if 'const EXITS=/*EXITS*/{};' in s:
    ef = os.path.join(S, 'exits_wd.json')
    ej = open(ef, encoding='utf-8').read() if os.path.exists(ef) else '{}'
    _ex = json.loads(ej)
    try:      # Xの投稿で「上場」が確認できた投資先(vc_x.py)
        from vc_x import EXITS_X
        for nm, typ, yr_, det in EXITS_X:
            _ex[re.sub(r'[^a-z0-9ぁ-んァ-ヶ一-龥]', '', nm.lower())] = [typ, yr_, det]
    except ImportError:
        pass
    ej = json.dumps(_ex, ensure_ascii=False, separators=(',', ':'))
    s = s.replace('const EXITS=/*EXITS*/{};', 'const EXITS=' + ej.replace('</', '<\\/') + ';')
    print('EXITS', len(json.loads(ej)))
if 'const YCS=/*YCS*/[];' in s:
    yf = os.path.join(S, 'yc_startups.json')
    yj = open(yf, encoding='utf-8').read() if os.path.exists(yf) else '[]'
    s = s.replace('const YCS=/*YCS*/[];', 'const YCS=' + yj.replace('</', '<\\/') + ';')
    print('YCS', len(json.loads(yj)))
if 'const WORLD=/*WORLD*/{r:[],s:{}};' in s:      # 世界の企業(world_cos.py)
    sys.path.insert(0, S)
    import world_cos as _w
    _seen = {}
    for n, c, g, b, j, f, e, src, t in _w.R:
        k = re.sub(r'[^a-z0-9ぁ-んァ-ヶ一-龥]', '', n.lower())
        if k in _seen:
            continue
        from yen import yenify as _yf
        b, t = _yf(b), _yf(t)
        _seen[k] = {'n': n, 'c': c, 'g': g, 'b': b, 'j': j, 'f': f, 'e': e, 's': (src if isinstance(src, (list, tuple)) else re.findall(r'N\d*|[A-MO-Z]', src)), 't': t}
    _wj = json.dumps({'r': list(_seen.values()), 's': {k: list(v) for k, v in _w.SRC.items()}}, ensure_ascii=False, separators=(',', ':'))
    s = s.replace('const WORLD=/*WORLD*/{r:[],s:{}};', 'const WORLD=' + _wj.replace('</', '<\/') + ';')
    print('WORLD', len(_seen))
if 'const JPSU=/*JPSU*/[];' in s:
    jf = os.path.join(S, 'jp_startups.json')
    jj = open(jf, encoding='utf-8').read() if os.path.exists(jf) else '[]'
    s = s.replace('const JPSU=/*JPSU*/[];', 'const JPSU=' + jj.replace('</', '<\\/') + ';')
    print('JPSU', len(json.loads(jj)))
if 'const WEBSITES=/*WEBSITES*/{k:{},n:{}};' in s:
    wf = os.path.join(S, 'websites.json')
    wj = open(wf, encoding='utf-8').read() if os.path.exists(wf) else '{"k":{},"n":{}}'
    s = s.replace('const WEBSITES=/*WEBSITES*/{k:{},n:{}};', 'const WEBSITES=' + wj.replace('</', '<\\/') + ';')
    print('WEBSITES', len(json.loads(wj)['n']), json.loads(wj)['k'] and len(json.loads(wj)['k']))
jpf = os.path.join(S, 'ranking_jp.txt')
if 'const JPRANK=/*JPRANK*/[];' in s:
    jp = []
    if os.path.exists(jpf):
        for ln in open(jpf, encoding='utf-8'):
            a = ln.rstrip('\n').split('|')
            if len(a) >= 6:
                jp.append([int(a[0]), a[1], a[2], a[3], int(a[4]), a[5]])
    s = s.replace('const JPRANK=/*JPRANK*/[];', 'const JPRANK=' + json.dumps(jp, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';')
    print('JPRANK', len(jp))
import glob
pfs =sorted(glob.glob(os.path.join(S, 'profiles_deep*.js')))
if pfs:
    assert '/*PROFILES_EXTRA*/' in s
    s = s.replace('/*PROFILES_EXTRA*/', '\n'.join(open(p, encoding='utf-8').read() for p in pfs).replace('</', '<\\/'))
open(OUTHTML, 'w', encoding='utf-8').write(s)
print('injected', len(js))
