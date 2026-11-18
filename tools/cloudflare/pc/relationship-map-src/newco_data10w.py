import json, os
from newco_data9 import P, O

# Wikidata(2026年11月取得)の記録から作った、AI分野の会社の図。ai_wd_to_maps.py が ai_wd_maps.json を作る。
# 創業者・CEO・出資者・親会社は、Wikidataに記録があるものだけ。記録にないこと(金額・出資比率など)は書かない。
NOTE_W = 'Wikidataの記録(2026年11月取得)に基づきます。創業者・CEO・出資者・親会社は、Wikidataに記録があるものだけで、金額や持ち分は載せていません。記録が古い・足りない場合があります。顔写真がない人はイニシャル表示です。'


NOTE_Y = 'Y Combinator公式ディレクトリ(2026年11月)の記載に基づきます。出資者・金額は載せていません。'
AWDATA = {}  # {key: {N,E,EN,center}}  別ファイル(aw/NN.json)に書き出す。ページには入れない
AIWD = []   # [{key,name,min,note}]  タブには出さず、検索で開く


def load(st):
    import newco_data10 as _m
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_wd_maps.json')
    if not os.path.exists(p):
        return
    for c in json.load(open(p, encoding='utf-8')):
        items, edges = [], []
        en = lambda s: s if all(ord(ch) < 0x250 for ch in s) else None
        _seen = set()
        c['p'] = [r for r in sorted(c['p'], key=lambda r: r['rel'] != '創業者') if not (r['p'] in _seen or _seen.add(r['p']))]
        c['i'] = [r for r in c['i'] if r['p'] not in {x['p'] for x in c['p']}]
        c['o'] = [r for r in c['o'] if r['p'] not in {x['p'] for x in c['p']} | {x['p'] for x in c['i']}]
        for r in c['p']:
            role = '創業者' if r['rel'] == '創業者' else 'CEO'
            items.append(P('w' + r['p'], r['name'], en(r['name']), c['year'], 'Wikidataに、%sとして記録があります。' % role, role + '(Wikidata)', None, 1 if role == '創業者' else 0))
        for r in c['i']:
            items.append(O('w' + r['p'], r['name'], c['year'], 'Wikidataに、出資者(投資家)として記録があります。', '出資者(Wikidata)', 'i'))
        for r in c['o']:
            items.append(O('w' + r['p'], r['name'], c['year'], 'Wikidataに、親会社として記録があります。', '親会社(Wikidata)'))
            edges.append(('w' + r['p'], 'co', 'owns', '親会社'))
        desc = '%s年ごろに設立された、AI分野の会社(Wikidataの分野の記録による)。' % c['year'] if c['year'] != 2000 else 'AI分野の会社(Wikidataの分野の記録による)。設立年は確認できていません。'
        note = NOTE_W
        yc = c.get('yc')
        if yc:
            note = NOTE_Y
            desc = 'Y Combinator(%s)。%s%s' % (yc['b'], (yc['one'][:90] + '。') if yc['one'] else '', ('所在地: %s。' % yc['loc'].split(',')[0]) if yc['loc'] else '')
            items = []
            for r in c['p']:
                items.append(P('w' + r['p'], r['name'], en(r['name']), c['year'], '', (r.get('t') or '創業者'), None, 1))
            items.append(O('yc', 'Y Combinator', c['year'], '', yc['b'], 'i'))
            edges = []
        st('stw_' + c['q'], c['name'], c['year'], note, items, edges, desc)
        AIWD.append(_m.STARTUPS.pop())   # タブの一覧からは外す
        _cc = _m.CO10['stw_' + c['q']]
        _E = [{'a': n['id'], 'b': 'co', 'k': 'member'} for n in _cc['N'] if n.get('kind') == 'p'] + [{'a': n['id'], 'b': 'co', 'k': 'invest'} for n in _cc['N'] if n.get('kind') == 'i']
        for e_ in edges:
            _d = {'a': e_[0], 'b': e_[1], 'k': e_[2]}
            if len(e_) > 3 and e_[3]:
                _d['label'] = e_[3]
            _E.append(_d)
        AWDATA['stw_' + c['q']] = {'N': _cc['N'], 'E': _E, 'EN': _cc['EN'], 'center': 'co'}


def shard_of(k):
    h = 5381
    for ch in k:
        h = (((h * 33) & 0xFFFFFFFF) ^ ord(ch)) & 0xFFFFFFFF
    return h


def write_shards(outdir, per=40):
    """aw/NN.json に、図のデータを分けて書き出す。振り分けは、ページ側(awShardOf)と同じ計算。"""
    import math
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        if f.endswith('.json'):
            os.remove(os.path.join(outdir, f))
    n = max(1, math.ceil(len(AWDATA) / per))
    parts = [dict() for _ in range(n)]
    for k, v in AWDATA.items():
        parts[shard_of(k) % n][k] = v
    total = 0
    for i, d in enumerate(parts):
        if d:
            s = json.dumps(d, ensure_ascii=False, separators=(',', ':'))
            open(os.path.join(outdir, '%d.json' % i), 'w', encoding='utf-8').write(s)
            total += len(s.encode('utf-8'))
    return n, total
