#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重要度ランキング(会社・人物)。2026/11/21追加。足すだけ(日付つきの新しいファイルを作る)。

閲覧数の計測はサイトに無いので、リポジトリの中のデータだけで「重要度」を計算する(外のサービスは使わない)。
  つながり   … 相関図(site/lab/graph.json)でつながっている相手の数(対数)           重み 0.40
  直近の動き … 直近90日の調査データ(inbox/moves・inbox/money)に名前が出る回数       重み 0.35
  ニュース   … ニュースの見出し(site/data の NEWS・RELNEWS・VCNEWS・YNEWS)に出る数  重み 0.25
各指標を 0〜1 にそろえて(1+件数の対数 ÷ 最大値の対数)、重みをかけて足す。
出力: inbox/ranking/日付.json と latest.json と latest.md。調べる順番(research_queue.py build)が latest.json を使う。
使い方: python3 scripts/importance_rank.py [--top 50]
"""
import jst
import argparse, datetime, glob, json, math, os, re, unicodedata
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'inbox', 'ranking')
W = {'links': 0.40, 'recent': 0.35, 'news': 0.25}
RECENT_DAYS = 90
KINDS = {'c': '会社', 'i': '投資家', 'p': '人物'}


def norm(s):
    s = unicodedata.normalize('NFKC', str(s or '')).lower()
    return re.sub(r'[\s・,、.()「」\-_/&]+', '', s)


# 株主名簿の名義(信託口・カストディ)や、持ち株が広く薄く並ぶだけの運用会社は、重要度が高く見えてしまうので外す
SKIP = re.compile(r'信託口|信託銀行|カストディ|BANK AND TRUST|BANK 5|BANK 3|NOMINEE|^BlackRock|^Vanguard|^State Street|^JP ?MORGAN CHASE BANK|^Found$|^Light$', re.I)
# 普通の英単語と同じ名前の会社は、見出しの数え間違いが多いので、ニュースは数えない
COMMON = {'found', 'light', 'line', 'open', 'scale', 'mercury', 'ramp', 'brex', 'base', 'figure', 'sprout', 'notion', 'linear'}


def usable(nm):
    if SKIP.search(str(nm)):
        return False
    k = norm(nm)
    return len(k) >= (4 if re.fullmatch(r'[a-z0-9]+', k) else 3)


def spaced(s):
    """単語の区切りを残した形(英数字は空白で区切る)。英語の名前を単語として数えるため"""
    s = unicodedata.normalize('NFKC', str(s or '')).lower()
    return ' ' + re.sub(r'\s+', ' ', re.sub(r'[^\w]+|_', ' ', s)) + ' '


def count(name, spaced_blob, plain_blob):
    k = norm(name)
    if re.fullmatch(r'[a-z0-9]+', k):
        return spaced_blob.count(spaced(name))
    return plain_blob.count(k)


def lg(x, mx):
    return math.log1p(x) / math.log1p(mx) if mx > 0 else 0.0


def en_names():
    """人物の日本語名 → 英語名。本体(index.html)の各図の人物と英語名の対応、実験ページの人物カード、人の移籍の調査データから集める(2026/11/21追加)"""
    import bisect
    m = {}
    h = open(os.path.join(ROOT, 'site', 'index.html'), encoding='utf-8').read()
    ns = [(x.start(), x.group(1)) for x in re.finditer(r'const N = (\[.*?\]);\n', h)]
    pos = [p for p, _ in ns]
    for x in re.finditer(r'const EN=(\{.*?\});', h):
        i = bisect.bisect_left(pos, x.start()) - 1
        if i < 0 or x.start() - pos[i] > 400000:
            continue
        try:
            N, E = json.loads(ns[i][1]), json.loads(x.group(1))
        except ValueError:
            continue
        for n in N:
            if n.get('kind') == 'p' and E.get(n['id']):
                m[norm(n['name'])] = E[n['id']]
    try:
        for c in json.load(open(os.path.join(ROOT, 'src', 'lab', 'cards.json'), encoding='utf-8')):
            if c.get('n') and c.get('en'):
                m[norm(c['n'])] = c['en']
        for c in json.load(open(os.path.join(ROOT, 'src', 'lab', 'flows.json'), encoding='utf-8')):
            if c.get('p') and c.get('en'):
                m[norm(c['p'])] = c['en']
    except (OSError, ValueError):
        pass
    for f in glob.glob(os.path.join(ROOT, 'inbox', 'moves', '20*.json')):
        try:
            for it in json.load(open(f, encoding='utf-8')).get('items', []):
                if it.get('name_ja') and it.get('name_en'):
                    m.setdefault(norm(it['name_ja']), it['name_en'])
        except (ValueError, OSError, AttributeError):
            pass
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--top', type=int, default=50)
    a = ap.parse_args()
    g = json.load(open(os.path.join(ROOT, 'site', 'lab', 'graph.json'), encoding='utf-8'))
    nodes = g['n']
    nb = [set() for _ in nodes]
    for e in g['e']:
        nb[e[0]].add(e[1]); nb[e[1]].add(e[0])
    cand = [i for i, n in enumerate(nodes) if n[1] in KINDS and usable(n[0])
            and not (n[1] == 'p' and re.fullmatch(r'[A-Za-z]+', n[0]))]   # 人物で英単語1語だけのものは、人名ではないことが多いので外す
    keys = {i: norm(nodes[i][0]) for i in cand}
    # 直近の動き
    now = jst.today()
    recent_txt = []
    for f in glob.glob(os.path.join(ROOT, 'inbox', '*', '20*.json')):
        if os.path.basename(os.path.dirname(f)) not in ('moves', 'money'):
            continue
        try:
            for it in json.load(open(f, encoding='utf-8')).get('items', []):
                d = str(it.get('date') or '')[:10]
                try:
                    if (now - datetime.date.fromisoformat(d)).days > RECENT_DAYS:
                        continue
                except ValueError:
                    pass
                recent_txt.append((' '.join(str(it.get(k, '')) for k in ('name_en', 'name_ja', 'from', 'to'))))
        except (json.JSONDecodeError, OSError, AttributeError):
            pass
    titles = []
    for fn in ('news', 'relnews', 'vcnews', 'ynews'):
        p = os.path.join(ROOT, 'site', 'data', fn + '.js')
        if os.path.exists(p):
            titles += [t for t in re.findall(r'"t":\s*"((?:[^"\\]|\\.)*)"', open(p, encoding='utf-8').read())]
    rec_s, news_s = '\x00'.join(spaced(t) for t in recent_txt), '\x00'.join(spaced(t) for t in titles)
    rec_p, news_p = '\x00'.join(norm(t) for t in recent_txt), '\x00'.join(norm(t) for t in titles)
    rows = []
    en = en_names()
    for i in cand:
        nm = nodes[i][0]
        names = [nm] + ([en[keys[i]]] if nodes[i][1] == 'p' and keys[i] in en else [])   # 人物は英語名でも数える
        r = {'name': nm, 'kind': KINDS[nodes[i][1]], 'links': len(nb[i]),
             'recent': sum(count(x, rec_s, rec_p) for x in names),
             'news': 0 if norm(nm) in COMMON else sum(count(x, news_s, news_p) for x in names)}
        if len(names) > 1:
            r['en'] = names[1]
        rows.append(r)
    mx = {m: max(r[m] for r in rows) for m in W}
    for r in rows:
        r['score'] = round(100 * sum(W[m] * lg(r[m], mx[m]) for m in W), 1)
    rows.sort(key=lambda r: -r['score'])
    for n, r in enumerate(rows, 1):
        r['rank'] = n
    today = now.isoformat()
    os.makedirs(OUT, exist_ok=True)
    out = {'date': today, 'method': '重要度=つながり40%+直近90日の動き35%+ニュース見出し25%(各指標は対数で0〜1にそろえる)',
           'weights': W, 'total': len(rows), 'top': rows[:max(a.top, 200)]}
    for fn in (today + '.json', 'latest.json'):
        json.dump(out, open(os.path.join(OUT, fn), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    md = [f'# 重要度ランキング({today})', '', out['method'], '',
          '閲覧数の計測が無いため、相関図の中のデータだけで計算。調べる順番(inbox/queue.json)に使う。', '']
    for title, kinds in (('会社・投資家 上位', ('会社', '投資家')), ('人物 上位', ('人物',))):
        md += [f'## {title}', '', '| 順位 | 名前 | 種類 | 点 | つながり | 直近の動き | ニュース |', '|---|---|---|---|---|---|---|']
        for r in [r for r in rows if r['kind'] in kinds][:a.top]:
            md.append(f"| {r['rank']} | {r['name']} | {r['kind']} | {r['score']} | {r['links']} | {r['recent']} | {r['news']} |")
        md.append('')
    open(os.path.join(OUT, 'latest.md'), 'w', encoding='utf-8').write('\n'.join(md))
    print(f'{len(rows)}件を計算。上位: ' + '、'.join(f"{r['name']}({r['score']})" for r in rows[:10]))


if __name__ == '__main__':
    main()
