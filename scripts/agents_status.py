#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""調査エージェント一覧の「今朝動いたか」の色を決める(2026/11/21追加)。

リポジトリに残った記録(inbox/ の当日ファイル・LAST_CHECK・BUILT など)だけから、係ごとに判定して
site/agents/status.json に書く。一覧ページ(site/agents/index.html)がこれを読んで色を出す。
- 読むだけ。inbox/ は書き換えない。Gemini は使わない。status.json は毎回作り直す(今日の状態だけ。履歴は見張り役の記録 inbox/watchdog/)
- 判定: ok=今日の記録あり(緑) / ng=予定の時刻を過ぎたのに記録なし(赤) / wait=まだ時刻前(灰) / off=今日は予定なし(灰) / na=記録が残らない係で見られない(灰) / pre=作る前の日(灰)
- 時刻の猶予は見張り役と同じ90分。見張り役(watchdog.py)の最後と agents_build.py が動かす
使い方: python3 scripts/agents_status.py            # status.json を作り直して表示
        python3 scripts/agents_status.py --now 2026-11-22T10:30  # 日本時間の時刻を決めて試す
"""
import argparse, datetime, fnmatch, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
JST = datetime.timezone(datetime.timedelta(hours=9))
GRACE_MIN = 90
OUT = os.path.join(ROOT, 'site', 'agents', 'status.json')
NEW6 = '2026-11-22'  # 新しい6係(採用〜解説)と品質チェック係を作った日。それより前は見ない

# 係のid -> 確かめること。f=ファイルの場所({d}=今日の日付)、days=曜日(月=0。省くと毎日)、hm=予定の時刻
FILES = {
    'people': [dict(f='inbox/moves/{d}.json', hm=(7, 29), t='引き抜き調査')],
    'money': [dict(f='inbox/money/{d}.json', days=(0, 3), hm=(7, 52), t='お金の流れ調査')],
    'fund': [dict(f='inbox/vc/{d}.json', days=(1,), hm=(7, 48), t='LP・VC調査')],
    'disclosure': [dict(f='inbox/ir/{d}.json', hm=(7, 29), t='決算資料・適時開示(IR)')],
    'media': [dict(f='inbox/youtube/{d}.json', hm=(7, 29), t='YouTube確認')],
    'world': [dict(f='inbox/world/{d}.json', days=(2,), hm=(7, 44), t='世界企業調査'),
              dict(f='inbox/moves/{d}*_thin*.json', days=(5,), hm=(7, 38), t='薄いところ調査')],
    'deep': [dict(f='inbox/deep/{d}.json', days=(4,), hm=(7, 41), t='深堀り調査')],
    'fun': [dict(f='inbox/fun/{d}.json', hm=(8, 53), t='おもしろ情報')],
    'verify': [dict(f='inbox/verify/{d}*', days=(6,), hm=(10, 23), t='確かめ直し')],
    'weekly': [dict(f='newsletter/issues/{d}.json', days=(0,), hm=(9, 37), t='週のまとめ')],
    'watch': [dict(f='inbox/watchdog/{d}*.md', hm=(10, 31), t='見張り役の記録')],
    'quality': [dict(f='inbox/quality/{d}*.json', hm=(9, 5), since=NEW6, t='品質チェック')],
    'hiring': [dict(f='inbox/moves/{d}-hiring.json', days=(6, 1, 4), hm=(8, 5), since=NEW6, t='採用・求人')],
    'jp_alliance': [dict(f='inbox/money/{d}-jp.json', hm=(8, 11), since=NEW6, t='日本の提携')],
    'jp_hr': [dict(f='inbox/moves/{d}-jp-hr.json', hm=(8, 14), since=NEW6, t='日本の人事')],
    'jp_funding': [dict(f='inbox/money/{d}-jp-fund.json', hm=(8, 17), since=NEW6, t='日本の資金調達')],
    'datacenter': [dict(f='inbox/money/{d}-dc.json', days=(6, 2, 5), hm=(8, 20), since=NEW6, t='データセンター・電力')],
    'column': [dict(f='newsletter/column/{d}.md', days=(6,), hm=(20, 0), since=NEW6, t='解説まとめ')],
}
# 記録がリポジトリに残らない係(動いたかは見張り役・各サービス側で確かめる)
# 日付つきのファイルを作らない係は、そのファイルを最後に commit した日(git)で見る(2026/11/22追加)
GIT = {
    'x': dict(f='inbox/x_accounts.txt', hm=(7, 7), t='Xアカウントの追加'),
    'xlearn': dict(f='inbox/xlearn/items.json', hm=(9, 19), t='新モデル解説の追記'),
}
NA = {
    'publish': '公開(9:41)はリポジトリに記録が残らない。公開ページの LAST_CHECK で確かめる',
    'kigyo': 'Cloudflare 側の作業で、リポジトリに記録が残らない(inbox/watchdog/kigyo-日付.md は見張りの記録)',
}


def read(p):
    try:
        return open(os.path.join(ROOT, p), encoding='utf-8', errors='ignore').read()
    except OSError:
        return ''


def last_check():
    m = re.search(r"const LAST_CHECK='([0-9-]+)'", read('site/index.html'))
    return m.group(1) if m else ''


def built():
    m = re.search(r"const BUILT='([0-9-]+) ", read('site/index.html'))
    return m.group(1) if m else ''


def gemini_ok(d, files_for, gemini_quota):
    fs = files_for('inbox/gemini', d, '')
    if fs:
        return True
    q = gemini_quota(d)
    return bool(q and (q[0] or q[1]))


def evaluate(now):
    import watchdog as wd
    d = now.date().isoformat()
    wk = now.weekday()

    def due(hm):
        return now >= datetime.datetime.combine(now.date(), datetime.time(*hm), tzinfo=JST) + datetime.timedelta(minutes=GRACE_MIN)

    def st(state, label, detail=''):
        return {'state': state, 'label': label, 'detail': detail}
    out = {}
    # 記録の形がちがう係
    out['daily'] = (st('ok', '動いた', f'LAST_CHECK = {last_check()}') if last_check() == d else
                    (st('ng', '記録なし', f'LAST_CHECK = {last_check()}(今日は {d})') if due((6, 43)) else st('wait', 'まだ時刻前', '6:43の予定')))
    out['merge'] = (st('ok', '動いた', f'BUILT = {built()}') if built() == d else
                    (st('ng', '記録なし', f'BUILT = {built()}(今日は {d}。9:13の取り込みの記録が無い)') if due((9, 13)) else st('wait', 'まだ時刻前', '9:13の予定')))
    if wd and (gemini_ok(d, wd.files_for, wd.gemini_quota)):
        out['gemini'] = st('ok', '動いた', 'inbox/gemini/ か Geminiを呼んだ記録あり')
    else:
        out['gemini'] = st('ng', '記録なし', 'inbox/gemini/ にも呼び出しの記録にも今日の分が無い') if due((8, 23)) else st('wait', 'まだ時刻前', '8:23の予定')
    for aid, checks in FILES.items():
        res = []
        for c in checks:
            if c.get('since') and d < c['since']:
                res.append(('pre', c['t']))
            elif c.get('days') is not None and wk not in c['days']:
                res.append(('off', c['t']))
            elif not due(c['hm']):
                res.append(('wait', c['t'] + f'({c["hm"][0]}:{c["hm"][1]:02d}の予定)'))
            elif glob.glob(os.path.join(ROOT, c['f'].format(d=d))):
                res.append(('ok', c['t']))
            else:
                res.append(('ng', c['t'] + f'({c["f"].format(d=d)} が無い)'))
        kinds = {r[0] for r in res}
        det = '・'.join(r[1] for r in res if r[0] in ('ok', 'ng', 'wait')) or ' '
        if 'ng' in kinds:
            out[aid] = st('ng', '記録なし', '、'.join(r[1] for r in res if r[0] == 'ng') + '(動かなかったか、まだ push されていない)')
        elif 'wait' in kinds:
            out[aid] = st('wait', 'まだ時刻前', det)
        elif 'ok' in kinds:
            out[aid] = st('ok', '動いた', det)
        elif kinds == {'pre'}:
            out[aid] = st('pre', '作る前', f'{NEW6} から見る')
        else:
            out[aid] = st('off', '今日は予定なし', '曜日の予定に入っていない')
    for aid, c in GIT.items():
        if not due(c['hm']):
            out[aid] = st('wait', 'まだ時刻前', f'{c["hm"][0]}:{c["hm"][1]:02d}の予定')
            continue
        r = subprocess.run(['git', 'log', '-1', '--format=%cI', '--', c['f']], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        try:
            last = datetime.datetime.fromisoformat(r).astimezone(JST).date().isoformat()
        except ValueError:
            out[aid] = st('na', '見られない', f'{c["f"]} の commit の日付を取れない')
            continue
        out[aid] = st('ok', '動いた', f'{c["f"]} を今日 commit した') if last == d else st('ng', '記録なし', f'{c["f"]} の最後の commit は {last}')
    for aid, why in NA.items():
        out[aid] = st('na', '見られない', why)
    return out


def write(now=None):
    now = now or datetime.datetime.now(JST)
    res = evaluate(now)
    doc = {'date': now.date().isoformat(), 'at': now.strftime('%Y-%m-%d %H:%M'), 'tz': '日本時間', 'agents': res}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(doc, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return doc


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--now')
    a = ap.parse_args()
    now = datetime.datetime.fromisoformat(a.now).replace(tzinfo=JST) if a.now else None
    doc = write(now)
    c = {}
    for v in doc['agents'].values():
        c[v['state']] = c.get(v['state'], 0) + 1
    print(f'{doc["at"]} 時点: ' + ' / '.join(f'{k} {n}' for k, n in sorted(c.items())))
    for k, v in doc['agents'].items():
        if v['state'] == 'ng':
            print('  記録なし:', k, v['detail'])


if __name__ == '__main__':
    main()
