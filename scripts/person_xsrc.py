#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本人のXの自己紹介で確かめた人物に、「本人」の出典を足す。2026/11/25追加。足すだけ。

入力: inbox/people_thin/xsrc/*.json  {"date":"2026/11/25","items":[{"en":"Helen Toner","handle":"hlntnr","bio":"…","career":[[年,文]…]}]}
  bio は python3 scripts/x_check.py @handle で実際に見た自己紹介の原文。自己紹介が、説明文の中心(いまの肩書き・創業など)と合う人だけ書く。
やること: 各図のその人物の src に pfx_(名前) を足し、DS(/*PF_DS_START*/〜/*PF_DS_END*/)に 's'(本人)で出典を足し、career の足りない行を足す。
  説明文は書き換えない(説明文の事実の出どころは person_fill.py の出典のまま)。何度動かしても同じ。
使い方: python3 scripts/person_xsrc.py [--dry-run]
"""
import argparse, glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, 'site', 'index.html')


def key(en):
    return 'pfx_' + re.sub(r'[^a-z0-9]+', '', en.lower())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dry-run', action='store_true'); a = ap.parse_args()
    items = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'inbox', 'people_thin', 'xsrc', '*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        for it in d['items']:
            it.setdefault('date', d.get('date', '')); items[it['en']] = it
    h = open(HTML, encoding='utf-8').read()
    blocks = list(re.finditer(r'const N = (\[.*?\]);\n', h, re.S))
    edits = []; hit = {k: 0 for k in items}
    for bi, m in enumerate(blocks):
        seg = h[m.end():(blocks[bi + 1].start() if bi + 1 < len(blocks) else len(h))]
        me = re.search(r'const EN=(\{.*?\});', seg); mc = re.search(r'const CAREER=(\{.*?\});', seg)
        if not me or not mc:
            continue
        try:
            EN, CAR = json.loads(me.group(1)), json.loads(mc.group(1))
        except ValueError:
            continue
        try:
            N = json.loads(m.group(1))
        except ValueError:
            N = None
        chg_n = chg_c = False
        if N is not None:
            for n in N:
                it = items.get(EN.get(n['id'])) if n.get('kind') == 'p' else None
                if not it:
                    continue
                hit[it['en']] += 1
                k = key(it['en']); s = list(n.get('src') or [])
                if k not in s:
                    n['src'] = s + [k]; chg_n = True
        else:
            def fix(lm):
                nonlocal chg_n
                line = lm.group(0); it = items.get(EN.get(lm.group(1)))
                if not it or "kind:'p'" not in line:
                    return line
                hit[it['en']] += 1; k = key(it['en'])
                if k in line:
                    return line
                chg_n = True
                if "src:['" in line:
                    return re.sub(r"src:\[([^\]]*)\]", lambda x: "src:[%s,'%s']" % (x.group(1), k), line, count=1)
                return line.replace("desc:'", "src:['%s'],desc:'" % k, 1)
            nt = re.sub(r"^ *\{id:'([^']+)'[^\n]*", fix, m.group(1), flags=re.M)
            if nt != m.group(1):
                edits.append((m.start(1), m.end(1), nt))
        for nid, en in EN.items():
            it = items.get(en)
            if not it:
                continue
            rows = CAR.get(nid, []); have = {tuple(r) for r in rows}
            add = [r for r in it.get('career', []) if tuple(r) not in have]
            if add and (N is None or any(n['id'] == nid and n.get('kind') == 'p' for n in N)):
                CAR[nid] = rows + add; chg_c = True
        if N is not None and chg_n:
            edits.append((m.start(1), m.end(1), json.dumps(N, ensure_ascii=False)))
        if chg_c:
            edits.append((m.end() + mc.start(1), m.end() + mc.end(1), json.dumps(CAR, ensure_ascii=False)))
    i0, i1 = h.find('/*PF_DS_START*/'), h.find('/*PF_DS_END*/')
    if i0 < 0:
        sys.exit('PF_DS の印がありません')
    cur = h[i0:i1]; add = ''
    for en, it in items.items():
        if hit[en] and key(en) + ':' not in cur:
            lab = '%s本人のXの自己紹介(%s確認。「%s」)' % (en, it['date'], it['bio'].replace('\n', ' ')[:80])
            add += ' %s:[%s,%s,\'s\'],\n' % (key(en), json.dumps(lab, ensure_ascii=False), json.dumps('https://x.com/' + it['handle']))
    if add:
        edits.append((i1, i1, add))
    for s, e, t in sorted(edits, reverse=True):
        h = h[:s] + t + h[e:]
    for en, n in hit.items():
        print('%-22s 図の人物 %d件' % (en, n))
    if not a.dry_run:
        open(HTML, 'w', encoding='utf-8').write(h)


if __name__ == '__main__':
    main()
