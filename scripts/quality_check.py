#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""品質チェック係(2026/11/21追加): 取り込み(merge_inbox.py)の前に、まだサイトに入っていない候補を一括で確かめる。

見るもの(まだ finds.js に入っていない項目だけ。inbox/ は読むだけで、書き換えない):
  - 出典切れ: 出典(src)が無い・URLが http で始まらない(この項目は取り込まれない)。--urls を付けると、URLを実際に開いて確かめる(上限あり)
  - 日付のずれ: 日付が書式どおりでない・今日より先・5年より前(さかのぼりの項目を除く)・項目の日付がファイルの日付より先
  - 確かさ(confidence)が決まった言葉でない・無い
  - 重複: 別のファイルに同じ内容(種類+名前+最初の出典URL)がある。同じ名前の組で、すでに finds.js にあるもの(別の出典)は「情報」として出す
結果は inbox/quality/日付.md と .json に足す(同じ日は -2)。取り込み(9:13)は止めない・壊さない: これは知らせるだけ。
使い方:
  python3 scripts/quality_check.py            # 確かめて inbox/quality/ に足す
  python3 scripts/quality_check.py --no-write # 表示だけ
  python3 scripts/quality_check.py --urls 30  # 出典URLを最大30件、実際に開く(開けない=クラウドの許可外のこともあるので「注意」)
終了コード: 問題があれば 1。Gemini は使わない。
"""
import argparse, datetime, glob, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import merge_inbox as mi  # noqa: E402

JST = datetime.timezone(datetime.timedelta(hours=9))
CONF = {'公式', '開示', '報道', '本人の発言', '推定', ''}  # ''は「無い」として別に数える
KINDS = mi.KINDS


def parse_date(s):
    try:
        return datetime.date.fromisoformat(str(s)[:10]) if re.match(r'^\d{4}-\d{2}-\d{2}', str(s)) else None
    except ValueError:
        return None


def pending_items():
    have = mi.load_existing()
    keys = {h['key'] for h in have}
    names = {}
    for h in have:
        names.setdefault(h['key'].rsplit('|', 1)[0], h['key'])
    out, seen_key = [], {}
    for kind in KINDS:
        for f in sorted(glob.glob(os.path.join(ROOT, 'inbox', kind, '*.json'))):
            try:
                d = json.load(open(f, encoding='utf-8'))
            except Exception:
                continue
            for i, it in enumerate(d.get('items') or []):
                if not isinstance(it, dict):
                    continue
                k = mi.key_of(kind, it)
                has_src = bool(mi.src_list(it))
                if has_src and k in keys:
                    continue  # すでにサイトにある
                out.append({'kind': kind, 'file': os.path.relpath(f, ROOT), 'i': i, 'item': it, 'key': k,
                            'file_date': str(d.get('date') or '')[:10],
                            'same_pair_have': names.get(k.rsplit('|', 1)[0])})
    return out


def check(today, url_limit):
    rows = []  # (判定, ファイル, 項目, ひとこと)
    P = pending_items()
    keymap = {}
    for p in P:
        keymap.setdefault(p['key'], []).append(p)
    urls_done = 0
    for p in P:
        it, f = p['item'], p['file']
        title = mi.title_of(p['kind'], it)[:60] or '(題なし)'
        srcs = mi.src_list(it)
        raw = it.get('src')
        if not srcs:
            rows.append(('問題', f, title, '出典(src)が無い、またはURLが http で始まらない(この項目は取り込まれない)' if raw is not None else '出典(src)の項目が無い(取り込まれない)'))
        elif url_limit and urls_done < url_limit and not p['kind'] == 'fun':
            urls_done += 1
            u = srcs[0][1]
            try:
                req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (quality-check)'})
                urllib.request.urlopen(req, timeout=12).close()
            except Exception as e:
                rows.append(('注意', f, title, f'出典URLが開けなかった({str(e)[:50]})。クラウドの許可外のこともある: {u[:80]}'))
        d = parse_date(it.get('date'))
        if it.get('date') in (None, ''):
            rows.append(('注意', f, title, '日付が無い'))
        elif d is None:
            rows.append(('問題', f, title, f'日付の書式が YYYY-MM-DD でない: {it.get("date")}'))
        else:
            if d > today + datetime.timedelta(days=1):
                rows.append(('問題', f, title, f'日付が先(未来): {d}'))
            elif (today - d).days > 365 * 5 and not it.get('backfill'):
                rows.append(('注意', f, title, f'日付が5年より前: {d}(さかのぼりなら backfill:true を付ける)'))
            fd = parse_date(p['file_date'])
            if fd and d > fd + datetime.timedelta(days=1):
                rows.append(('注意', f, title, f'項目の日付 {d} がファイルの日付 {fd} より先(日付のずれの可能性)'))
        c = it.get('confidence', '')
        if c not in CONF:
            rows.append(('注意', f, title, f'確かさ(confidence)が決まった言葉でない: {c}'))
        elif c == '':
            rows.append(('注意', f, title, '確かさ(confidence)が無い'))
        if p['same_pair_have'] and srcs:
            rows.append(('情報', f, title, 'すでにサイトにある内容(別の出典で入っている)。重複として足されないものも含む'))
    for k, lst in keymap.items():
        files = sorted({x['file'] for x in lst})
        if len(files) > 1 and lst[0]['item'].get('src'):
            seed = [x for x in files if '-seed-' in x]
            rows.append(('情報' if seed else '注意', files[0], mi.title_of(lst[0]['kind'], lst[0]['item'])[:60],
                         f'同じ内容が {len(files)} つのファイルにある' + ('(初回の拾い seed を含む。取り込みで1件にまとまる)' if seed else '(取り込みで1件にまとまる)') + ': ' + ', '.join(os.path.basename(x) for x in files[:3])))
    return len(P), rows


def to_md(now, n, rows):
    prob = [r for r in rows if r[0] == '問題']
    warn = [r for r in rows if r[0] == '注意']
    L = [f'# 品質チェックの記録 {now:%Y-%m-%d %H:%M}(日本時間)', '',
         f'**結果: ' + ('問題あり' if prob else ('注意あり' if warn else 'すべて順調')) + f'**(まだサイトに入っていない候補 {n} 件 / 問題 {len(prob)} / 注意 {len(warn)} / 情報 {sum(r[0]=="情報" for r in rows)})', '',
         '取り込み(9:13)は止めません。この記録は知らせるだけで、inbox/ のファイルは書き換えていません。', '']
    if rows:
        L += ['| 判定 | ファイル | 項目 | ひとこと |', '|---|---|---|---|']
        for r in sorted(rows, key=lambda r: ['問題', '注意', '情報'].index(r[0])):
            L.append('| ' + ' | '.join(str(x).replace('|', '/') for x in r) + ' |')
    return '\n'.join(L) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--no-write', action='store_true')
    ap.add_argument('--urls', type=int, default=0, help='出典URLを実際に開く件数の上限')
    a = ap.parse_args()
    now = datetime.datetime.now(JST)
    n, rows = check(now.date(), a.urls)
    md = to_md(now, n, rows)
    print(md)
    if not a.no_write:
        d = os.path.join(ROOT, 'inbox', 'quality')
        os.makedirs(d, exist_ok=True)
        base, i = os.path.join(d, f'{now:%Y-%m-%d}'), 2
        while os.path.exists(base + '.md'):
            base = os.path.join(d, f'{now:%Y-%m-%d}-{i}'); i += 1
        open(base + '.md', 'w', encoding='utf-8').write(md)
        json.dump({'at': now.isoformat(), 'pending': n, 'rows': rows}, open(base + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('保存:', os.path.relpath(base + '.md', ROOT))
    sys.exit(1 if any(r[0] == '問題' for r in rows) else 0)


if __name__ == '__main__':
    main()
