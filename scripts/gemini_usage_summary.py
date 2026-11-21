#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gemini の使った回数・やり直し・宿題リストの消化を、1週間分まとめる(2026/11/20追加。読むだけ)。

使い方:
  python3 scripts/gemini_usage_summary.py                  # 直近7日(今日を含まない昨日まで)をMarkdownで表示
  python3 scripts/gemini_usage_summary.py --end 2026-11-23 # この日(日本時間)の前日までの7日
毎週月曜は scripts/watchdog.py が、この表を見張り役の記録(inbox/watchdog/日付.md)の最後に付ける。

見るもの(すべてリポジトリの記録から):
  使った回数  inbox/gemini/usage.jsonl(成功・枠切れ429・混雑・自分で決めた上限で停止)
  やり直し    inbox/gemini/queue.jsonl(枠切れで後回しにしたテーマ → やり直した数、まだ残っている数)
  宿題リスト  inbox/queue.json の history(その週に調査済みにした項目数・失敗した数)
金額: 回数が中心。有料にした場合の目安は inbox/gemini/limits.json の assumed_price(仮定)で計算し、必ず「仮定」と書く。
"""
import argparse, datetime, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JST = datetime.timezone(datetime.timedelta(hours=9))
G = os.path.join(ROOT, 'inbox', 'gemini')


def _jsonl(p):
    if not os.path.exists(p):
        return
    for ln in open(p, encoding='utf-8'):
        try:
            yield json.loads(ln)
        except json.JSONDecodeError:
            continue


def _jst_date(t):
    d = datetime.datetime.fromisoformat(str(t).replace('Z', '+00:00'))
    return (d if d.tzinfo else d.replace(tzinfo=JST)).astimezone(JST).date()  # queue.jsonl は日本時間のまま(tzなし)


def usage_rows(days):
    """days: 日付(date)の一覧 → 日ごとの集計"""
    out = {d: {'ok': 0, 'quota': 0, 'busy': 0, 'cap': 0, 'in': 0, 'out': 0} for d in days}
    for e in _jsonl(os.path.join(G, 'usage.jsonl')):
        try:
            d = datetime.datetime.fromisoformat(e['at']).astimezone(JST).date()
        except (KeyError, ValueError):
            continue
        if d not in out:
            continue
        k = {'ok': 'ok', '429': 'quota', '503': 'busy', '500': 'busy', 'cap': 'cap'}.get(e.get('result'))
        if k:
            out[d][k] += 1
        out[d]['in'] += e.get('in') or 0
        out[d]['out'] += e.get('out') or 0
    return out


def limits():
    try:
        return json.load(open(os.path.join(G, 'limits.json'), encoding='utf-8'))
    except Exception:
        return {}


def retries(days):
    s, e = min(days), max(days)
    queued = done = 0
    ev = list(_jsonl(os.path.join(G, 'queue.jsonl')))
    for x in ev:
        try:
            d = _jst_date(x['at'])
        except (KeyError, ValueError):
            continue
        if s <= d <= e:
            if x.get('ev') == 'queued': queued += 1
            elif x.get('ev') == 'done': done += 1
    finished = {x['id'] for x in ev if x.get('ev') == 'done'}
    pending = sum(1 for x in ev if x.get('ev') == 'queued' and x['id'] not in finished)
    return queued, done, pending


def homework(days):
    p = os.path.join(ROOT, 'inbox', 'queue.json')
    if not os.path.exists(p):
        return None
    q = json.load(open(p, encoding='utf-8'))
    ds = {d.isoformat() for d in days}
    ok = fail = cands = 0
    for it in q['items']:
        for h in it.get('history', []):
            if h.get('date') in ds:
                if h.get('result') == '失敗': fail += 1
                else:
                    ok += 1; cands += h.get('items') or 0
    left = sum(1 for it in q['items'] if it.get('status') == '未')
    return ok, fail, cands, left, len(q['items'])


def summary(end=None):
    end = end or datetime.datetime.now(JST).date()
    days = [end - datetime.timedelta(days=i) for i in range(7, 0, -1)]
    rows = usage_rows(days)
    lim = limits()
    cap = int(lim.get('daily_max_calls', 0) or 0)
    tot = {k: sum(r[k] for r in rows.values()) for k in ('ok', 'quota', 'busy', 'cap', 'in', 'out')}
    L = [f'## Geminiの使った回数(先週 {days[0]:%m/%d}〜{days[-1]:%m/%d}・日本時間)', '']
    L.append(f'- 1日の上限: ' + (f'{cap}回(`inbox/gemini/limits.json`)' if cap > 0 else '設定なし'))
    L.append(f'- 呼び出し: 成功 **{tot["ok"]}回** / 枠切れ(429) {tot["quota"]}回 / 混雑のやり直し {tot["busy"]}回 / 上限で止めた {tot["cap"]}回')
    if cap > 0:
        peak = max(rows.items(), key=lambda kv: kv[1]['ok'] + kv[1]['quota'] + kv[1]['busy'])
        used = peak[1]['ok'] + peak[1]['quota'] + peak[1]['busy']
        L.append(f'- いちばん多い日: {peak[0]:%m/%d} に {used}回(上限の {used*100//cap}%)')
        if tot['cap'] or tot['quota']:
            L.append('- ⚠ 上限・枠切れが出ました。調べ残しは、やり直す列と宿題リストで翌朝に回っています。足りない日が続くなら、上限を上げるか有料を検討')
    L += ['', '| 日付 | 成功 | 枠切れ | 混雑 | 上限で停止 |', '|---|---|---|---|---|']
    for d in days:
        r = rows[d]; L.append(f'| {d:%m/%d} | {r["ok"]} | {r["quota"]} | {r["busy"]} | {r["cap"]} |')
    qd, dn, pend = retries(days)
    L += ['', f'- やり直し: 後回しにしたテーマ {qd}件 / やり直した {dn}件 / いま残り {pend}件']
    hw = homework(days)
    if hw:
        ok, fail, cands, left, total = hw
        L.append(f'- 宿題リスト(`inbox/queue.json`): 先週の消化 {ok}件(候補 計{cands}件)・失敗 {fail}件 / 未着手の残り {left}件(全{total}件)')
    pr = lim.get('assumed_price') or {}
    if pr and tot['ok']:
        usd = (tot['in'] / 1e6 * pr.get('usd_per_million_input_tokens', 0) + tot['out'] / 1e6 * pr.get('usd_per_million_output_tokens', 0)
               + tot['ok'] * pr.get('usd_per_search_grounded_call', 0))
        yen = usd * pr.get('yen_per_usd', 150)
        L += ['', f'- **有料にした場合の目安(仮定)**: 先週と同じ使い方なら 約{usd:.2f}ドル(約{yen:,.0f}円)/週。'
              f'入力{tot["in"]:,}・出力{tot["out"]:,}トークン、検索つき{tot["ok"]}回で計算。'
              '単価は `limits.json` の仮定で、公式の料金表で確かめた値ではありません。実際の請求ではなく、無料枠のうちは0円です。']
    elif not tot['ok']:
        L += ['', '- 先週は成功した呼び出しの記録がありません(記録は2026/11/20から。まだ溜まっていない可能性)']
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--end', help='この日(日本時間)の前日までの7日。例 2026-11-23')
    a = ap.parse_args()
    print(summary(datetime.date.fromisoformat(a.end) if a.end else None))
