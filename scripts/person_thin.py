#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""人物の「経歴の薄さ」の一覧。2026/11/24追加。足すだけ(日付つきの新しいファイルを作る。サイトは変えない)。

本体の相関図の人物(kind=p)ごとに、次を数える。
  説明文の長さ / 経歴の行数(CAREER) / 人物カードの行数(PERSONAL) / 出典の数 / Wikidata(PAUTO)の有無
  知名度 … 出てくる会社の図の数・つながりの線の数・ニュース見出しに出る数・肩書き(CEO・創業者など)
「薄い」= 説明文が短い・経歴が0〜2行・出典がない、のどれかが重なるもの。
知名度の高い順に、薄い人物の上位を inbox/people_thin/日付.json と日付.md に書く(latest も更新)。
毎日の人物追加(inbox/people_thin/latest.json の「上位」)が、ここから埋める人を選ぶ。
  埋めたら本体に足したあと、もう一度これを動かすと、その人は薄くない扱いになる。
  確かめられなかった人は inbox/people_thin/skip.json(名前→理由・日付)に足すと、次回から飛ばす(消さない)。
使い方: python3 scripts/person_thin.py [--top 30] [--dump /tmp/dump.json]
  --dump を省くと、scripts/nblm_dump.js を動かして作る(playwright が要る。読むだけ)。
"""
import argparse, collections, datetime, glob, json, math, os, re, subprocess, sys, unicodedata
import jst
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'inbox', 'people_thin')
LEAD = re.compile(r'CEO|CTO|COO|CFO|創業|創設|共同|社長|会長|代表|最高|Chief|Founder|頭取|総裁|議長|取締役', re.I)


def norm(s):
    return re.sub(r'[\s・,、.()「」\-_/&]+', '', unicodedata.normalize('NFKC', str(s or '')).lower())


def spaced(s):
    s = unicodedata.normalize('NFKC', str(s or '')).lower()
    return ' ' + re.sub(r'\s+', ' ', re.sub(r'[^\w]+|_', ' ', s)) + ' '


def load_dump(path):
    if not path:
        path = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'people_thin_dump.json')
        subprocess.run(['node', os.path.join(ROOT, 'scripts', 'nblm_dump.js'), path], check=True)
    return json.load(open(path, encoding='utf-8'))


def profile_keys():
    """人物ページの深掘りプロフィール(index.html の PROFILES)がある人の英語名。ある人は「薄い」から外す"""
    h = open(os.path.join(ROOT, 'site', 'index.html'), encoding='utf-8').read()
    return set(re.findall(r'\n"([^"\n]{3,40})":\{jp:', h))


def collect(d):
    L = d['lists']
    prof = profile_keys()
    P = {}
    for ck, m in d['maps'].items():
        deg = collections.Counter()
        for e in m['E']:
            deg[e['a']] += 1
            deg[e['b']] += 1
        for n in m['N']:
            if n['kind'] != 'p':
                continue
            key = n['en'] or n['name']
            p = P.setdefault(key, dict(name=n['name'], en=n['en'], cos=[], roles=[], desc=0, career=0, edges=0, src=0, ext=0))
            p['cos'].append(ck)
            if n['role']:
                p['roles'].append(n['role'])
            p['desc'] = max(p['desc'], len(n['desc'] or ''))
            p['career'] = max(p['career'], len(m['career'].get(n['id'], [])))
            p['edges'] += deg[n['id']]
            p['src'] += len(n['src'])
            p['ext'] += bool(n['wiki'] or n['x'] or n['web'])
    titles = []
    for k in ('NEWS', 'RELNEWS', 'VCNEWS', 'YNEWS'):
        titles += [str(x.get('t', '')) for x in L.get(k, []) if isinstance(x, dict)]
    blob_s = '\x00'.join(spaced(t) for t in titles)
    blob_p = '\x00'.join(norm(t) for t in titles)
    for key, p in P.items():
        p['personal'] = len(L['PERSONAL'].get(key, []))
        p['pauto'] = key in L['PAUTO']
        p['profile'] = key in prof
        nm = p['en'] or p['name']
        k = norm(nm)
        p['news'] = blob_s.count(spaced(nm)) if re.fullmatch(r'[a-z0-9]+', k) and ' ' in nm.strip() else (blob_p.count(k) if len(k) >= 3 and not re.fullmatch(r'[a-z0-9]+', k) else 0)
        p['cos'] = sorted(set(p['cos']))
    return P


def score(key, p):
    thin = 0
    why = []
    if p['desc'] < 60:
        thin += 2; why.append('説明文が短い(%d字)' % p['desc'])
    elif p['desc'] < 150:
        thin += 1; why.append('説明文がやや短い(%d字)' % p['desc'])
    if p['career'] == 0:
        thin += 2; why.append('経歴の行が0')
    elif p['career'] <= 2:
        thin += 1; why.append('経歴の行が%d' % p['career'])
    if p['src'] == 0 and not p['ext']:
        thin += 1; why.append('出典・外部リンクなし')
    main = sum(1 for c in p['cos'] if '_' not in c)   # us_・jp_・st_ などの接頭辞のない主要なAI・半導体の図
    fame = (main * 5 + (len(p['cos']) - main) * 1.5 + p['edges'] * 0.7 + min(p['news'], 30) * 2
            + (3 if any(LEAD.search(r) for r in p['roles']) else 0) + (2 if p['pauto'] else 0))
    return thin, why, round(fame, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--top', type=int, default=30)
    ap.add_argument('--dump')
    a = ap.parse_args()
    P = collect(load_dump(a.dump))
    skip = {}
    sp = os.path.join(OUT, 'skip.json')
    if os.path.exists(sp):
        skip = json.load(open(sp, encoding='utf-8'))
    rows = []
    for key, p in P.items():
        thin, why, fame = score(key, p)
        rows.append(dict(key=key, name=p['name'], en=p['en'], thin=thin, why=why, fame=fame, desc=p['desc'], career=p['career'],
                         personal=p['personal'], src=p['src'], news=p['news'], edges=p['edges'], companies=p['cos'][:6],
                         role=(p['roles'] or [''])[0], skipped=key in skip, profile=p['profile']))
    thin_rows = [r for r in rows if r['thin'] >= 3 and not r['profile']]
    thin_rows.sort(key=lambda r: -r['fame'])
    todo = [r for r in thin_rows if not r['skipped']]
    os.makedirs(OUT, exist_ok=True)
    today = jst.today().isoformat()
    res = dict(date=today, total=len(rows), thin=len(thin_rows),
               method='薄さ=説明文・経歴の行・出典の少なさ(3点以上)。知名度=主要なAI・半導体の図の数×5+その他の図×1.5+線の数×0.7+ニュース見出し(上限30)×2+肩書き3+Wikidata2',
               top=todo[:a.top], all_thin_count=len(thin_rows))
    for fn in (today + '.json', 'latest.json'):
        json.dump(res, open(os.path.join(OUT, fn), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    md = ['# 人物の経歴の薄さ(%s)' % today, '', '人物 %d人のうち、薄い人は %d人。知名度の高い順に上位 %d人。' % (len(rows), len(thin_rows), a.top), '',
          '| 順 | 人物 | 知名度 | 経歴行 | 説明文字数 | つながり | 肩書き・会社 | 薄い理由 |', '|--|--|--|--|--|--|--|--|']
    for i, r in enumerate(todo[:a.top], 1):
        md.append('| %d | %s%s | %s | %d | %d | %d | %s / %s | %s |' % (i, r['name'], ('(%s)' % r['en']) if r['en'] and r['en'] != r['name'] else '', r['fame'], r['career'], r['desc'], r['edges'], r['role'], ','.join(r['companies'][:3]), '、'.join(r['why'])))
    for fn in (today + '.md', 'latest.md'):
        open(os.path.join(OUT, fn), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    print('人物', len(rows), '薄い', len(thin_rows), '→', os.path.join(OUT, 'latest.md'))


if __name__ == '__main__':
    main()
