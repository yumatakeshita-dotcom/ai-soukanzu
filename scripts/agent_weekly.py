#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""係ごとの調べた件数を、毎週まとめる道具(2026/11/24追加)。

inbox/ のファイルを数えて、係ごとに「動いた日数・足した候補の数・0件だった回」を出す。
サイトのデータには触らない(読むだけ)。出力は足すだけ・同じ日なら置き換え。
  - site/agents/weekly.html   … 画面(調査エージェント一覧の「係ごとの件数(週次)」から開く。1枚で完結)
  - site/agents/weekly.json   … 数字(画面が読む元と同じもの)
  - inbox/agents/weekly/日付.md … 文書版(日付ごとに残る。消さない)

使い方: python3 scripts/agent_weekly.py [--days 14] [--today 2026-11-24]
数え方:
  - 候補の数 = そのファイルの items の件数(確かめで落ちたもの rejected は数えない)
  - YouTube/ポッドキャストは新着の本数(videos / episodes)
  - 初回の拾い(-seed-)は毎日の成果ではないので数えない(別に「初回の拾い」として出す)
目安(増やす/そのまま/減らす)は、直近7日の件数だけから機械的に決めた案。最後に人が決める。
"""
import argparse, datetime, glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX = os.path.join(ROOT, 'inbox')
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
try:
    import jst
    TODAY = jst.today()
except Exception:  # 日本時間の道具が無いときの代わり
    TODAY = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).date()

# 係の一覧(表示する順番)。id は docs/agents.json の id に合わせた
AGENTS = [
    ('jinzai', '人材係'), ('okane', 'お金係'), ('fund', 'ファンド係'), ('kaiji', '開示係(IR)'),
    ('media', '動画・音声係'), ('x', 'X係'), ('gemini', 'Gemini係'), ('world', '世界・アジア係'),
    ('deep', '深堀り係'), ('fun', 'おもしろ情報係'), ('hiring', '採用・求人係'),
    ('jp_alliance', '日本の提携係'), ('jp_hr', '日本の人事係'), ('jp_funding', '日本の資金調達係'),
    ('datacenter', 'データセンター・電力係'),
]
NAME = dict(AGENTS)


def classify(kind, rest):
    """(フォルダ名, 日付のあとの文字) → 係のid。数えないものは None、わからないものは 'other'。"""
    r = rest.lower()
    if '-seed-' in r or r.startswith('-seed'):
        return 'seed'
    if 'gemini' in r:
        return 'gemini'
    if r.endswith('-ir') or r == '-ir':
        return 'kaiji'
    if 'hiring' in r:
        return 'hiring'
    if r.startswith('-jp-hr'):
        return 'jp_hr'
    if r.startswith('-jp-fund'):
        return 'jp_funding'
    if r.startswith('-jp'):
        return 'jp_alliance'
    if r.startswith('-dc'):
        return 'datacenter'
    if 'x-pc' in r:
        return 'x'
    if any(k in r for k in ('backlog', 'media')):
        return 'media'
    if any(k in r for k in ('thin', 'asia')):
        return 'world'
    if 'deep' in r:
        return 'deep'
    if 'verified' in r or 'recheck' in r:
        return 'other'
    base = {'moves': 'jinzai', 'money': 'okane', 'vc': 'fund', 'ir': 'kaiji', 'world': 'world',
            'deep': 'deep', 'fun': 'fun', 'youtube': 'media', 'podcasts': 'media'}.get(kind)
    if base and (r in ('', '.json') or re.match(r'^[-_](\d|past|manual)', r) or r in ('-zoph',)):
        return base
    return 'other' if base else None


def count_items(kind, d):
    if kind in ('youtube', 'podcasts'):  # 見た新着の本数は候補ではないので 0(本数は collect が別に数える)
        return 0
    if isinstance(d, dict):
        it = d.get('items')
        return len(it) if isinstance(it, list) else 0
    return len(d) if isinstance(d, list) else 0


def collect(days):
    start = TODAY - datetime.timedelta(days=days - 1)
    per = {a: {} for a, _ in AGENTS}      # id → {日付: [件数,...]}
    seed = {}                             # 初回の拾い id→件数
    other = 0
    seen = {}                             # 動画・音声: 日付→見た新着の本数
    for kind in ['moves', 'money', 'vc', 'ir', 'world', 'deep', 'fun', 'youtube', 'podcasts']:
        for p in sorted(glob.glob(os.path.join(INBOX, kind, '*.json'))):
            name = os.path.basename(p)[:-5]
            m = re.match(r'(\d{4}-\d{2}-\d{2})(.*)$', name)
            if not m:
                continue
            day = datetime.date.fromisoformat(m.group(1))
            if day < start or day > TODAY:
                continue
            who = classify(kind, m.group(2))
            try:
                d = json.load(open(p, encoding='utf-8'))
            except Exception:
                continue
            n = count_items(kind, d)
            if kind in ('youtube', 'podcasts') and isinstance(d, dict):
                seen[day.isoformat()] = seen.get(day.isoformat(), 0) + len(d.get('videos') or d.get('episodes') or [])
            if who == 'seed':
                sid = re.search(r'seed-?_?([a-z_]+)', m.group(2))
                key = sid.group(1) if sid else '?'
                seed[key] = seed.get(key, 0) + n
            elif who in per:
                per[who].setdefault(day.isoformat(), []).append(n)
            else:
                other += 1
    return start, per, seed, other, seen


# 動く予定の日(曜日 0=月)。週あたりの予定回数の目安に使う
SCHEDULE = {'jinzai': 7, 'okane': 2, 'fund': 1, 'kaiji': 7, 'media': 7, 'x': 7, 'gemini': 7, 'world': 2,
            'deep': 1, 'fun': 7, 'hiring': 3, 'jp_alliance': 7, 'jp_hr': 7, 'jp_funding': 7, 'datacenter': 3}


def judge(row):
    """直近7日の数字から、増やす/そのまま/減らす の案と理由を返す。"""
    runs, items, planned = row['runs7'], row['items7'], row['planned7']
    if planned == 0:
        return '—', ''
    if runs == 0:
        return '要確認', '直近7日に記録がない(動いていない可能性)'
    avg = items / runs
    if avg >= 2:
        return '増やす', f'1回あたり {avg:.1f} 件と多い'
    if items == 0 and runs >= 3:
        return '減らす', f'直近7日に {runs} 回動いて 0 件'
    if items <= 1 and runs >= 5:
        return '減らす', f'直近7日に {runs} 回動いて {items} 件だけ'
    return 'そのまま', f'1回あたり {avg:.1f} 件'


def build(days):
    start, per, seed, other, seen = collect(days)
    cut7 = TODAY - datetime.timedelta(days=6)
    rows = []
    for aid, name in AGENTS:
        pd = per[aid]
        runs = len(pd)
        items = sum(sum(v) for v in pd.values())
        r7 = {d: v for d, v in pd.items() if datetime.date.fromisoformat(d) >= cut7}
        row = {
            'id': aid, 'name': name, 'planned7': SCHEDULE[aid], 'runs': runs, 'items': items,
            'zero_runs': sum(1 for v in pd.values() if sum(v) == 0),
            'runs7': len(r7), 'items7': sum(sum(v) for v in r7.values()),
            'by_day': {d: sum(v) for d, v in sorted(pd.items())},
        }
        row['advice'], row['why'] = judge(row)
        if aid == 'media':
            s7 = sum(v for d, v in seen.items() if datetime.date.fromisoformat(d) >= cut7)
            row['why'] += f'(候補の数は動画・音声の手がかりから出た移籍・お金だけ。見た新着は直近7日で {s7} 本)'
        rows.append(row)
    return {'today': TODAY.isoformat(), 'start': start.isoformat(), 'days': days, 'rows': rows,
            'seed': seed, 'other_files': other, 'seen_by_day': seen}


def to_md(res):
    L = [f"# 係ごとの件数(週次) {res['today']}", '',
         f"期間: {res['start']} 〜 {res['today']}({res['days']}日)。`python3 scripts/agent_weekly.py` で作る。",
         '候補の数は「inbox/ の items の件数」。取り込みで重複・保留になる分は引いていない。', '',
         '| 係 | 直近7日: 動いた日 | 直近7日: 候補 | 期間: 動いた日 | 期間: 候補 | 0件の日 | 目安 | 理由 |',
         '|---|---|---|---|---|---|---|---|']
    for r in res['rows']:
        L.append(f"| {r['name']} | {r['runs7']} | {r['items7']} | {r['runs']} | {r['items']} | {r['zero_runs']} | {r['advice']} | {r['why']} |")
    if res['seed']:
        L += ['', '初回の拾い(過去の inbox から、1回だけ): ' + '、'.join(f'{k} {v}件' for k, v in sorted(res['seed'].items()))]
    L += ['', '※ 目安は直近7日の件数だけから機械的に出した案。最後は人が決める。']
    return '\n'.join(L) + '\n'


CSS = """:root{--bg:#f7f7f5;--fg:#1d1d1b;--mut:#6b6b66;--card:#fff;--line:#dcdcd6;--up:#1a7f4b;--down:#b3541e;--chk:#b3261e}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#161615;--fg:#ecece8;--mut:#9a9a94;--card:#201f1e;--line:#3a3935;--up:#5fd08f;--down:#f0a070;--chk:#ff8a80}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,-apple-system,'Hiragino Sans','Noto Sans JP',sans-serif}
main{max-width:980px;margin:0 auto;padding:20px 16px 48px}h1{font-size:1.4rem;margin:.2em 0}p.s{color:var(--mut);margin:.3em 0 1em}
.w{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--card)}table{border-collapse:collapse;width:100%;min-width:640px}
th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}th:first-child,td:first-child,td.l,th.l{text-align:left}
th{font-size:.8rem;color:var(--mut);font-weight:600}tr:last-child td{border-bottom:0}.a-up{color:var(--up);font-weight:700}.a-down{color:var(--down);font-weight:700}.a-chk{color:var(--chk);font-weight:700}
td.why{white-space:normal;color:var(--mut);font-size:.85rem;text-align:left}a{color:inherit}.n{color:var(--mut);font-size:.85rem;margin-top:1em}"""


def to_html(res):
    cls = {'増やす': 'a-up', '減らす': 'a-down', '要確認': 'a-chk'}
    rows = ''
    for r in res['rows']:
        rows += (f"<tr><td>{html.escape(r['name'])}</td><td>{r['runs7']}</td><td>{r['items7']}</td><td>{r['runs']}</td>"
                 f"<td>{r['items']}</td><td>{r['zero_runs']}</td><td class='{cls.get(r['advice'], '')}'>{r['advice']}</td>"
                 f"<td class='why'>{html.escape(r['why'])}</td></tr>")
    seed = ''
    if res['seed']:
        seed = '<p class="n">初回の拾い(過去の inbox から1回だけ。毎日の成果には数えない): ' + html.escape('、'.join(f'{k} {v}件' for k, v in sorted(res['seed'].items()))) + '</p>'
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>係ごとの件数(週次)</title>
<style>{CSS}</style></head><body><main>
<h1>係ごとの件数(週次)</h1>
<p class="s">{res['start']} 〜 {res['today']}({res['days']}日)。inbox/ に足された候補の数を係ごとに数えました。<a href="./">調査エージェント一覧へ</a></p>
<div class="w"><table><thead><tr><th class="l">係</th><th>7日:動いた日</th><th>7日:候補</th><th>期間:動いた日</th><th>期間:候補</th><th>0件の日</th><th>目安</th><th class="l">理由</th></tr></thead><tbody>{rows}</tbody></table></div>
{seed}
<p class="n">候補の数は取り込み前の件数です(重複・保留は引いていません)。「目安」は直近7日の件数から機械的に出した案で、最後は人が決めます。毎週 <code>python3 scripts/agent_weekly.py</code> で作り直します。</p>
</main></body></html>
"""


def main():
    global TODAY
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=14)
    ap.add_argument('--today')
    ap.add_argument('--print', action='store_true', help='書かずに表示だけ')
    a = ap.parse_args()
    if a.today:
        TODAY = datetime.date.fromisoformat(a.today)
    res = build(a.days)
    md = to_md(res)
    if a.print:
        print(md)
        return
    os.makedirs(os.path.join(INBOX, 'agents', 'weekly'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'site', 'agents'), exist_ok=True)
    open(os.path.join(INBOX, 'agents', 'weekly', f"{res['today']}.md"), 'w', encoding='utf-8').write(md)
    open(os.path.join(ROOT, 'site', 'agents', 'weekly.json'), 'w', encoding='utf-8').write(json.dumps(res, ensure_ascii=False, indent=1))
    open(os.path.join(ROOT, 'site', 'agents', 'weekly.html'), 'w', encoding='utf-8').write(to_html(res))
    print(md)


if __name__ == '__main__':
    main()
