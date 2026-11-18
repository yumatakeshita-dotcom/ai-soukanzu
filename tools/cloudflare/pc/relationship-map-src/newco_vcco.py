"""VCの投資先の会社・ニュースで資金調達が報じられた小さな会社の図(自動作成)。
元データ: vc_inv.json / vc_official.py / vc_yc.json(VCの投資先) と funding_news.json(ニュースの会社名・ラウンド・投資家)。
作る条件: 2つ以上のVCの投資先に載っている会社、またはニュースで投資家が分かった会社。既存の図と同名のものは作らない。"""
import json, os, re

from newco_data import mk, std
from newco_uni import n2

S = os.path.dirname(os.path.abspath(__file__))
MAXMAPS = 1200       # ページが大きくなりすぎないための上限(出力HTMLは16MBまで)
NOTE = ('この会社は、VCの投資先(英語版・日本語版Wikipedia、各VCの公式サイトの投資先ページをAIで読み取ったもの)や、資金調達のニュースの見出しから自動で作った図です(2026年11月)。'
        '投資の時期・金額は、ニュースの見出しにあるものだけです。人物(創業者・経営陣)は、まだ調べていません。')


def _ld(n, d):
    f = os.path.join(S, n)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else d


def build(existing):
    disp = {}
    for ln in open(os.path.join(S, 'vc_names.txt'), encoding='utf-8'):
        a = (ln.rstrip('\n').split('|') + [''] * 7)[:7]
        disp[a[0]] = a[6] or re.sub(r'\s*\(.*?\)', '', a[3] or a[4])
    comp = {}      # n2(名前) -> {'name','jp','vcs':{表示名: 出どころ}}
    def add(name, jp, vn, src):
        x = n2(name)
        if len(x) < 3:
            return
        d = comp.setdefault(x, {'name': name, 'jp': jp or '', 'vcs': {}, 'news': []})
        d['vcs'].setdefault(vn, src)
        if jp and not d['jp']:
            d['jp'] = jp
    for k, v in _ld('vc_inv.json', {}).items():
        vn = v.get('jp') or v['en']
        for p in v.get('p', []):
            add(p[0], p[1], vn, 'Wikipedia')
    for kid, v in _ld('vc_big.json', {}).items():      # Wikipediaのカテゴリとリンク元から集めた大量のVC・投資先
        vn = v.get('jp') or v['en']
        for p in v.get('p', []):
            add(p[0], p[1], vn, 'Wikipedia')
    try:
        from vc_official import OFFICIAL
        items = dict(OFFICIAL)
        yf = os.path.join(S, 'vc_yc.json')
        if os.path.exists(yf):
            items['yc'] = ('', ', '.join(json.load(open(yf, encoding='utf-8'))))
        for k, (_u, names) in items.items():
            for nm in [x.strip() for x in names.split(', ') if x.strip()]:
                add(nm, '', disp.get(k, k), '公式サイト')
    except ImportError:
        pass
    for h in _ld('funding_news.json', []):
        cn = h.get('cn')
        if not cn:
            continue
        x = n2(cn)
        if len(x) < 3:
            continue
        d = comp.setdefault(x, {'name': cn, 'jp': '', 'vcs': {}, 'news': []})
        d['news'].append(h)
        for iv in h.get('inv', []):
            d['vcs'].setdefault(iv, 'ニュース')
    co, lst, used = {}, [], set()
    cand = [(x, d) for x, d in comp.items() if x not in existing and (len(d['vcs']) >= 2 or (d['news'] and d['vcs']))]
    cand.sort(key=lambda t: (-len(t[1]['vcs']), -len(t[1]['news'])))
    for x, d in cand[:MAXMAPS]:
        news = sorted(d['news'], key=lambda h: h.get('d', ''), reverse=True)
        year = 2025
        if news and re.match(r'\d{4}', news[0].get('d', '')):
            year = int(news[0]['d'][:4])
        desc = '%s(VCの投資先・資金調達ニュースの記録にある会社)。' % d['name']
        if d['jp']:
            desc += '日本語名: %s。' % d['jp']
        for h in news[:3]:
            bits = [b for b in (h.get('rd'), h.get('a')) if b]
            desc += '%s %s(%s)。' % (h.get('d', ''), ' '.join(bits) or '資金調達', h.get('s', ''))
        N = [{'id': 'co', 'name': d['name'], 'kind': 'c', 'from': year, 'desc': desc}]
        for i, (vn, src) in enumerate(list(d['vcs'].items())[:10], 1):
            N.append({'id': 'v%d' % i, 'name': vn, 'kind': 'i', 'from': year,
                      'desc': 'この会社の出資者・投資家として、%sの記録にあります(投資の時期・金額は未確認)。' % src, 'role': 'VC・投資家(%s)' % src})
        key = 'vc_' + (re.sub(r'[^a-z0-9]', '', x)[:20] or 'x')
        while key in used:
            key += 'x'
        used.add(key)
        co[key] = mk(N, std('co'), {}, {}, {}, {}, {}, {}, 'co')
        lst.append({'key': key, 'name': d['name'], 'min': year, 'note': NOTE})
    return co, lst
