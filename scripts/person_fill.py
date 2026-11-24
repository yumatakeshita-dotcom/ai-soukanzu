#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""薄い人物の経歴を、本体(site/index.html)の相関図に足す。2026/11/24追加。足すだけ。

入力: inbox/people_thin/fills/*.json(出典のページを開いて確かめた人だけ書く)。形:
  {"date":"2026/11/24","items":[{"en":"Jack Ma","desc":"…","career":[["1999","アリババを共同創業"],…],
     "src":["英語版Wikipedia(2026/11/24確認)","https://en.wikipedia.org/wiki/Jack_Ma","r"]}]}
やること(各図の人物のうち、英語名が en と同じ人):
  説明文 … 新しい説明を先頭に、もとの説明を後ろに残して(もとの文が含まれていれば足さない)、出典と日付を添える
  経歴   … その図の CAREER に、その人の行がなければ足す(すでにあれば、同じ文言でない行だけを後ろに足す)
  出典   … DS に pf_(名前) を足し(/*PF_DS_START*/〜/*PF_DS_END*/ の間)、人物の src に付ける(確かさの印が付く)
消さない・上書きしない。何度動かしても同じ(2回目は変化なし)。数えるだけなら --dry-run。
使い方: python3 scripts/person_fill.py [--dry-run] [ファイル...]
"""
import argparse, glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, 'site', 'index.html')
FILLS = os.path.join(ROOT, 'inbox', 'people_thin', 'fills')
DSM = ('/*PF_DS_START*/', '/*PF_DS_END*/')


def slug(en):
    return 'pf_' + re.sub(r'[^a-z0-9]+', '', en.lower())


def dumps(o):
    return json.dumps(o, ensure_ascii=False)


def load_items(files):
    items = {}
    for f in files:
        for it in json.load(open(f, encoding='utf-8')).get('items', []):
            d = json.load(open(f, encoding='utf-8')).get('date', '')
            it.setdefault('date', d)
            items[it['en']] = it
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('files', nargs='*')
    a = ap.parse_args()
    files = a.files or sorted(glob.glob(os.path.join(FILLS, '*.json')))
    items = load_items(files)
    h = open(HTML, encoding='utf-8').read()
    blocks = [m for m in re.finditer(r'const N = (\[.*?\]);\n', h)]
    edits = []   # (start, end, newtext)
    stat = {k: {'nodes': 0, 'desc': 0, 'career': 0} for k in items}
    skipped = 0
    for bi, m in enumerate(blocks):
        end_limit = blocks[bi + 1].start() if bi + 1 < len(blocks) else len(h)
        seg = h[m.end():end_limit]
        me = re.search(r'const EN=(\{.*?\});', seg)
        mc = re.search(r'const CAREER=(\{.*?\});', seg)
        if not me or not mc:
            continue
        try:
            N, EN, CAR = json.loads(m.group(1)), json.loads(me.group(1)), json.loads(mc.group(1))
        except ValueError:
            skipped += 1
            continue
        if dumps(N) != m.group(1) or dumps(EN) != me.group(1) or dumps(CAR) != mc.group(1):
            skipped += 1
            continue
        chg_n = chg_c = False
        for n in N:
            if n.get('kind') != 'p':
                continue
            en = EN.get(n['id'])
            it = items.get(en)
            if not it:
                continue
            stat[en]['nodes'] += 1
            tag = '(%s 経歴を足した。出典:%s)' % (it['date'], it['src'][0])
            if tag not in (n.get('desc') or ''):
                old = n.get('desc') or ''
                new = it['desc'] + ((' ' + old) if old and old not in it['desc'] else '') + tag
                n['desc'] = new
                n['src'] = list(n.get('src') or [])
                if slug(en) not in n['src']:
                    n['src'].append(slug(en))
                chg_n = True
                stat[en]['desc'] += 1
            rows = CAR.get(n['id'], [])
            have = {tuple(r) for r in rows}
            add = [r for r in it.get('career', []) if tuple(r) not in have]
            if add:
                CAR[n['id']] = rows + add
                chg_c = True
                stat[en]['career'] += 1
        if chg_n:
            edits.append((m.start(1), m.end(1), dumps(N)))
        if chg_c:
            edits.append((m.end() + mc.start(1), m.end() + mc.end(1), dumps(CAR)))
    # 出典(DS)
    i0, i1 = h.find(DSM[0]), h.find(DSM[1])
    if i0 < 0 or i1 < 0:
        sys.exit('index.html に %s がありません(先にひな形を足してください)' % DSM[0])
    cur = h[i0 + len(DSM[0]):i1]
    add = ''
    for en, it in items.items():
        k = slug(en)
        if k + ':' not in cur and stat[en]['nodes']:
            add += ' %s:[%s,%s,%s],\n' % (k, json.dumps(it['src'][0] + '(' + en + ')', ensure_ascii=False), json.dumps(it['src'][1]), json.dumps(it['src'][2] if len(it['src']) > 2 else 'r'))
    if add:
        edits.append((i1, i1, add))
    for s, e, t in sorted(edits, reverse=True):
        h = h[:s] + t + h[e:]
    for en, st in stat.items():
        print('%-24s 図の人物 %d件 / 説明を足した %d / 経歴を足した %d' % (en, st['nodes'], st['desc'], st['career']))
    print('JSONで読めず飛ばした図:', skipped)
    if a.dry_run:
        print('(--dry-run: 書き込みなし)')
        return
    open(HTML, 'w', encoding='utf-8').write(h)


if __name__ == '__main__':
    main()
