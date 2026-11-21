#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""毎朝の自動作業が止まっていないかを、リポジトリに残った記録だけから確かめる見張り役(2026/11/20追加)。

使い方:
  python3 scripts/watchdog.py              # 今日(日本時間)と前日を確かめ、inbox/watchdog/日付.md に足す
  python3 scripts/watchdog.py --no-write   # 表示だけ
  python3 scripts/watchdog.py --now 2026-11-20T10:30   # 日本時間の時刻を決めて試す

何を見るか(「その時刻に出るはずの記録が、リポジトリにあるか」):
  更新(6:43)  site/index.html の LAST_CHECK が今日の日付か
  調査        inbox/moves・money・vc・deep・world・gemini に、その曜日のファイルがあるか(壊れたJSONも検知)
  調査の新着  main に今日の commit が1件でもあるか(9:13以降)
  Gemini の枠  inbox/gemini/usage.jsonl で、その日の呼び出しが全部 429(枠切れ)なら「注意」
  宿題リスト  inbox/queue.json の先頭が何日も動いていないか
  月曜だけ    先週のGemini使用回数・やり直し・宿題リストの消化(scripts/gemini_usage_summary.py。回数中心、金額は「仮定」)
見られないもの: 共有リンクのアーティファクト(9:41の公開)と Cloudflare は、リポジトリに記録が残らない。
  定期タスク側(scripts/watchdog.py の外)で、公開ページの LAST_CHECK を読んで比べる。

判定: 問題 = 記録が無い・壊れている / 注意 = 動いたが気になる(枠切れなど) / 時刻前 = まだ確かめない。
終了コード: 問題があれば 1、なければ 0。記録は足すだけ(同じ日に2回なら -2 を付ける)。
"""
import argparse, datetime, glob, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JST = datetime.timezone(datetime.timedelta(hours=9))
GRACE_MIN = 90  # 予定の時刻から、この分数たってから確かめる

# (名前, 予定の時刻(時,分), 曜日(月=0。None=毎日), フォルダ, ファイル名の目印)
SCHEDULE = [
    ('引き抜き調査(moves)', (7, 26), None, 'inbox/moves', ''),
    ('お金の流れ調査(money)', (7, 52), (0, 3), 'inbox/money', ''),
    ('LP・VC調査(vc)', (7, 48), (1,), 'inbox/vc', ''),
    ('世界企業調査(world)', (7, 30), (2,), 'inbox/world', ''),
    ('深堀り調査(deep)', (7, 41), (4,), 'inbox/deep', ''),
    ('薄いところ調査(moves _thin)', (7, 38), (5,), 'inbox/moves', '_thin'),
    ('Gemini調査(gemini)', (8, 23), None, 'inbox/gemini', ''),
    ('開示ウォッチ(disclosures)', (10, 19), (1,), 'inbox/disclosures', ''),
    ('報道だけの数字の確かめ直し(verify)', (10, 23), (6,), 'inbox/verify', ''),
]


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True).stdout


def files_for(folder, date, mark):
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, folder, f'{date}*'))):
        b = os.path.basename(f)
        if mark and mark not in b:
            continue
        if b.endswith(('_verified.json', '_verified.md', '_process_raw.json')) and folder == 'inbox/gemini':
            continue
        out.append(f)
    return out


def check_json(files):
    """JSONの壊れているファイルの名前を返す"""
    bad = []
    for f in files:
        if f.endswith('.json'):
            try:
                json.load(open(f, encoding='utf-8'))
            except Exception:
                bad.append(os.path.basename(f))
    return bad


def last_check():
    s = open(os.path.join(ROOT, 'site', 'index.html'), encoding='utf-8', errors="ignore").read()
    m = re.search(r"const LAST_CHECK='([0-9-]+)'", s)
    return m.group(1) if m else None


def gemini_quota(date):
    """その日(日本時間)の Gemini 呼び出し(成功, 枠切れ)。記録が無ければ None"""
    p = os.path.join(ROOT, 'inbox', 'gemini', 'usage.jsonl')
    if not os.path.exists(p):
        return None
    ok = quota = 0
    for ln in open(p, encoding='utf-8'):
        try:
            e = json.loads(ln)
        except json.JSONDecodeError:
            continue
        t = str(e.get('at') or e.get('t') or e.get('time') or '')
        try:
            d = datetime.datetime.fromisoformat(t.replace('Z', '+00:00'))
            d = (d if d.tzinfo else d.replace(tzinfo=datetime.timezone.utc)).astimezone(JST).date().isoformat()
        except ValueError:
            d = t[:10]
        if d != date:
            continue
        if e.get('result') == 'ok':
            ok += 1
        elif e.get('result') == '429':
            quota += 1
    return ok, quota


def evaluate(now):
    rows = []  # (判定, 項目, ひとこと)
    for back in (1, 0):
        day = (now - datetime.timedelta(days=back)).date()
        d = day.isoformat()
        tag = '今日' if back == 0 else '前日'

        def due(hm):
            t = datetime.datetime.combine(day, datetime.time(*hm), tzinfo=JST) + datetime.timedelta(minutes=GRACE_MIN)
            return now >= t
        # 更新(6:43)
        if due((6, 43)):
            lc = last_check()
            if back == 0:
                rows.append(('OK' if lc == d else '問題', f'{tag} 毎朝の更新(6:43)',
                             f'LAST_CHECK = {lc}' + ('' if lc == d else f'(今日は {d}。更新が動いていないか、push されていない)')))
        for name, hm, wd, folder, mark in SCHEDULE:
            if wd is not None and day.weekday() not in wd:
                continue
            if not due(hm):
                rows.append(('時刻前', f'{tag} {name}', f'{hm[0]}:{hm[1]:02d}の予定。まだ確かめません'))
                continue
            fs = files_for(folder, d, mark)
            if not fs and folder == 'inbox/gemini':
                # 2026/11/21追加: 朝のGemini調査は、ファイル名の日付がUTCのずれで前日になることがある。
                # その日(日本時間)に Gemini を呼んだ記録(usage.jsonl)があれば、動いたとみなす
                q = gemini_quota(d)
                if q and (q[0] or q[1]):
                    rows.append(('OK', f'{tag} {name}', f'ファイルの日付は前日になっているが、Geminiを呼んだ記録あり(成功 {q[0]}・枠切れ {q[1]})'))
                    continue
            if not fs:
                rows.append(('問題', f'{tag} {name}', f'{folder}/ に {d} のファイルが無い(動かなかったか、push されていない)'))
                continue
            bad = check_json(fs)
            if bad:
                rows.append(('問題', f'{tag} {name}', 'JSONが壊れている: ' + ', '.join(bad)))
            else:
                rows.append(('OK', f'{tag} {name}', f'{len(fs)}ファイル'))
        # Gemini の枠
        q = gemini_quota(d) if due((8, 23)) else None
        if q and q[1] and not q[0]:
            rows.append(('注意', f'{tag} Geminiの無料枠', f'成功 0 回・枠切れ {q[1]} 回(今日の調査は後回し。宿題リストは状態を変えず翌朝に回る)'))
        elif q:
            rows.append(('OK', f'{tag} Geminiの無料枠', f'成功 {q[0]} 回・枠切れ {q[1]} 回'))
        # main の動き(9:13の「調査の新着」などが push したか)
        if due((9, 13)):
            n = run(['git', 'log', 'origin/main', f'--since={d}T00:00:00+09:00', f'--until={d}T23:59:59+09:00', '--oneline']).strip()
            c = len(n.splitlines()) if n else 0
            rows.append(('OK' if c else '問題', f'{tag} main への push', f'{c}件' + ('' if c else '(朝の作業が1つも push していない)')))
    # 宿題リスト
    qp = os.path.join(ROOT, 'inbox', 'queue.json')
    if os.path.exists(qp):
        q = json.load(open(qp, encoding='utf-8'))
        last = max([it.get('last_researched') or '' for it in q['items']] or [''])
        if last:
            age = (now.date() - datetime.date.fromisoformat(last)).days
            rows.append(('注意' if age >= 3 else 'OK', '宿題リスト', f'最後に調べたのは {last}({age}日前)' + ('。無料枠切れか、Geminiの調査が止まっている可能性' if age >= 3 else '')))
        else:
            rows.append(('注意', '宿題リスト', 'まだ1件も調べていない'))
    return rows


def to_md(now, rows):
    prob = [r for r in rows if r[0] == '問題']
    warn = [r for r in rows if r[0] == '注意']
    L = [f'# 見張り役の記録 {now:%Y-%m-%d %H:%M}(日本時間)', '',
         f'**結果: ' + ('問題あり' if prob else ('注意あり' if warn else 'すべて順調')) + f'**(問題 {len(prob)} / 注意 {len(warn)} / OK {sum(r[0]=="OK" for r in rows)})', '',
         '| 判定 | 項目 | ひとこと |', '|---|---|---|']
    for r in sorted(rows, key=lambda r: ['問題', '注意', 'OK', '時刻前'].index(r[0])):
        L.append(f'| {r[0]} | {r[1]} | {r[2]} |')
    if now.weekday() == 0:  # 月曜は、先週のGemini使用回数・やり直し・宿題リストの消化を付ける(2026/11/20追加)
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import gemini_usage_summary
            L += ['', gemini_usage_summary.summary(now.date()).rstrip()]
        except Exception as ex:
            L += ['', f'(Geminiの使用まとめを作れませんでした: {str(ex)[:100]})']
    L += ['', '※ 共有リンクのアーティファクト(9:41の公開)と Cloudflare は、リポジトリに記録が残らないため、この表では見ていません。']
    return '\n'.join(L) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--no-write', action='store_true')
    ap.add_argument('--now', help='日本時間の時刻(例 2026-11-20T10:30)')
    a = ap.parse_args()
    now = datetime.datetime.fromisoformat(a.now).replace(tzinfo=JST) if a.now else datetime.datetime.now(JST)
    run(['git', 'fetch', '-q', 'origin', 'main'])
    rows = evaluate(now)
    md = to_md(now, rows)
    print(md)
    if not a.no_write:
        d = os.path.join(ROOT, 'inbox', 'watchdog')
        os.makedirs(d, exist_ok=True)
        p, i = os.path.join(d, f'{now:%Y-%m-%d}.md'), 2
        while os.path.exists(p):
            p = os.path.join(d, f'{now:%Y-%m-%d}-{i}.md'); i += 1
        open(p, 'w', encoding='utf-8').write(md)
        print('保存:', os.path.relpath(p, ROOT))
    sys.exit(1 if any(r[0] == '問題' for r in rows) else 0)


if __name__ == '__main__':
    main()
