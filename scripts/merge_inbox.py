# -*- coding: utf-8 -*-
"""調査タスクの結果(inbox/*/*.json)を、サイトの「調査の新着」(site/data/finds.js)に足す。

- 足すだけ。finds.js にすでにある項目は消さない・書き換えない
- 同じ内容(種類+主な名前+出典URL)は2回足さない
- 出典(src)の無い項目は足さない
- 2行目の FINDLINKS(相関図に足すつながり)は scripts/finds_map.py が inbox/ から毎回作る
- 3行目の EXECTL_AUTO(幹部の年表に自動で足すもの)は scripts/exectl_auto.py が inbox/moves/ から毎回作る
使い方: python3 scripts/merge_inbox.py   (足した件数を表示する)
"""
import json, os, re, sys, glob, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import finds_map
import exectl_auto
import fun_merge
import quality_hold

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'site', 'data', 'finds.js')
KINDS = ['moves', 'money', 'vc', 'world', 'deep']
HEAD = ('// 調査タスク(引き抜き・お金の流れ・LP/VC・世界企業・深堀り)が見つけた候補。'
        'scripts/merge_inbox.py が inbox/ から毎日足す。足すだけで消さない\n')


def load_existing():
    if not os.path.exists(OUT):
        return []
    s = open(OUT, encoding='utf-8').read()
    for line in s.splitlines():
        if line.startswith('const FINDS='):
            return json.loads(line[len('const FINDS='):].rstrip().rstrip(';'))
    return []


def norm(x):
    return re.sub(r'[\s　・,、()()]+', '', str(x or '')).lower()


def main_fields(kind, it):
    if kind == 'moves':
        return [it.get('name_en') or it.get('name_ja'), it.get('to')]
    if kind == 'money':
        return [it.get('from'), it.get('to'), it.get('kind')]
    if kind == 'vc':
        return [it.get('fund') or it.get('startup'), it.get('gp')]
    if kind == 'world':
        return [it.get('country'), it.get('title')]
    if kind == 'deep':
        return [it.get('company_en') or it.get('company_ja')]
    return [json.dumps(it, ensure_ascii=False)[:80]]


def src_list(it):
    out = []
    for s in it.get('src') or []:
        if isinstance(s, (list, tuple)) and len(s) >= 2 and str(s[1]).startswith('http'):
            out.append([str(s[0]), str(s[1])])
        elif isinstance(s, str) and s.startswith('http'):
            out.append([s, s])
    return out


def key_of(kind, it):
    srcs = src_list(it)
    return kind + '|' + '|'.join(norm(f) for f in main_fields(kind, it)) + '|' + (srcs[0][1] if srcs else '')


def title_of(kind, it):
    g = lambda k: (it.get(k) or '').strip() if isinstance(it.get(k), str) else ''
    if kind == 'moves':
        nm = g('name_ja') or g('name_en')
        if g('name_ja') and g('name_en') and g('name_ja') != g('name_en'):
            nm = f"{g('name_ja')}({g('name_en')})"
        role = f"({g('role')})" if g('role') else ''
        return f"{nm}: {g('from')} → {g('to')}{role}"
    if kind == 'money':
        amt = f" {g('amount')}" if g('amount') else ''
        return f"{g('from')} → {g('to')}({g('kind')}{amt})"
    if kind == 'vc':
        parts = [g('gp'), g('fund')]
        t = ' / '.join(p for p in parts if p)
        if g('size'):
            t += f"({g('size')})"
        if g('lp'):
            t += f" LP: {g('lp')}"
        return t
    if kind == 'world':
        return f"[{g('country')}] {g('title')}"
    if kind == 'deep':
        nm = g('company_ja') or g('company_en')
        if g('company_ja') and g('company_en') and g('company_ja') != g('company_en'):
            nm = f"{g('company_ja')}({g('company_en')})"
        return f"{nm}: {g('what')}"
    return ''


def detail_of(kind, it):
    note = it.get('note') or it.get('detail') or ''
    if kind == 'deep':
        bits = []
        if it.get('founded'):
            bits.append(f"設立 {it['founded']}")
        if it.get('hq'):
            bits.append(f"本社 {it['hq']}")
        ppl = [p.get('name', '') + (f"({p['role']})" if p.get('role') else '') for p in it.get('people') or [] if isinstance(p, dict)]
        inv = [p.get('name', '') + (f" {p['amount']}" if p.get('amount') else '') for p in it.get('investors') or [] if isinstance(p, dict)]
        par = [p.get('name', '') for p in it.get('partners') or [] if isinstance(p, dict)]
        if ppl:
            bits.append('人: ' + '、'.join(ppl[:6]))
        if inv:
            bits.append('出資: ' + '、'.join(inv[:6]))
        if par:
            bits.append('取引: ' + '、'.join(par[:6]))
        note = (note + ' / ' if note else '') + ' / '.join(bits)
    return note


def write_hold(held, today):
    """保留にしたものを inbox/quality/hold-日付.json・.md に足す(足すだけ・同じ項目は2回書かない)。失敗しても取り込みは止めない"""
    if not held:
        return
    try:
        d = os.path.join(ROOT, 'inbox', 'quality')
        os.makedirs(d, exist_ok=True)
        jp = os.path.join(d, f'hold-{today}.json')
        old = json.load(open(jp, encoding='utf-8')) if os.path.exists(jp) else []
        seen = {(r['file'], r['key'], r['reason']) for r in old}
        new = [h for h in held if (h['file'], h['key'], h['reason']) not in seen]
        rows = old + new
        if not new:
            print(f'保留: {len(held)}件(記録ずみ)')
            return
        json.dump(rows, open(jp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        L = [f'# 取り込みで保留にした候補 {today}', '',
             '品質チェックの「問題」のある候補です。サイトには取り込んでいません(元のファイルは inbox/ にそのまま残っています)。',
             '直す(出典・日付)か、日付が来れば、次の取り込みで自動で入ります。', '',
             '| 種類 | ファイル | 項目 | 理由 |', '|---|---|---|---|']
        for r in rows:
            L.append('| ' + ' | '.join(str(r[k]).replace('|', '/') for k in ('kind', 'file', 'title', 'reason')) + ' |')
        open(os.path.join(d, f'hold-{today}.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
        print(f'保留にした件数: {len(new)}(取り込まず、inbox/quality/hold-{today}.md に理由を記録)')
    except Exception as e:
        print('保留の記録に失敗(取り込みは済んでいる):', e)


def main():
    have = load_existing()
    keys = {h['key'] for h in have}
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d')
    added = []
    held = []  # 品質チェックの「問題」で保留にしたもの(取り込まない。元ファイルはそのまま)
    today_d = quality_hold.today_jst()
    for kind in KINDS:
        for f in sorted(glob.glob(os.path.join(ROOT, 'inbox', kind, '*.json'))):
            try:
                d = json.load(open(f, encoding='utf-8'))
            except Exception as e:
                print('読めないファイル(とばす):', f, e, file=sys.stderr)
                continue
            for it in d.get('items') or []:
                if not isinstance(it, dict):
                    continue
                srcs = src_list(it)
                why = quality_hold.hold_reason(it, today_d)
                if why:
                    held.append({'kind': kind, 'file': os.path.relpath(f, ROOT).replace(os.sep, '/'),
                                 'title': title_of(kind, it)[:80], 'reason': why, 'key': key_of(kind, it)})
                    continue
                if not srcs:
                    continue
                k = key_of(kind, it)
                if k in keys:
                    continue
                keys.add(k)
                row = {
                    'key': k, 'k': kind,
                    'd': str(it.get('date') or d.get('date') or '')[:10],
                    't': title_of(kind, it)[:160],
                    'x': detail_of(kind, it)[:400],
                    'c': it.get('confidence') or '',
                    'src': srcs[:3],
                    'add': today,
                    'f': os.path.relpath(f, ROOT).replace(os.sep, '/'),
                }
                if it.get('backfill'):
                    row['b'] = 1
                if it.get('quote'):
                    row['q'] = str(it['quote'])[:200]
                added.append(row)
    allrows = have + added
    allrows.sort(key=lambda r: (r.get('add', ''), r.get('d', '')), reverse=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as w:
        w.write(HEAD + 'const FINDS=' + json.dumps(allrows, ensure_ascii=False, separators=(',', ':')) + ';\n')
        # 相関図に足すつながり(引き抜き・出資・買収・取引)。inbox/ から毎回作る。どの図に付けるかは index.html の applyFinds が決める
        w.write(finds_map.js_line())
        # 3行目: 幹部の年表に自動で足すもの(2026/11/19追加)。inbox/moves/ から毎回作る
        w.write(exectl_auto.js_line())
        # 4行目: おもしろ情報に自動で足すもの(2026/11/21追加)。inbox/fun/ から毎回作る
        w.write(fun_merge.js_line())
    assert len(allrows) >= len(have), '件数が減った(ありえない)'
    print(f'足した件数: {len(added)} / 合計: {len(allrows)}')
    for kind in KINDS:
        n = sum(1 for r in added if r['k'] == kind)
        if n:
            print(f'  {kind}: {n}')
    write_hold(held, today)
    exectl_auto.report(exectl_auto.build())
    fun_merge.report(*fun_merge.build())
    # ニュースの見出し(トップの「最近のニュース」)も毎回足す。2026/11/20追加(11/13から止まっていたため)
    try:
        import fetch_relnews
        fetch_relnews.main()
    except Exception as e:
        print('ニュースの取り込みに失敗(ほかの処理は済んでいる):', e)


if __name__ == '__main__':
    main()
