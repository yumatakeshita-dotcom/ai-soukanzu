"""Gemini / ChatGPT などで作った時価総額の一覧を『貼り付け.txt』に貼ると、ranking.txt に取り込む(Claude不要)。
貼り付け.txt の書き方(1行に1社。区切りは何でもよい。ティッカーと時価総額があればよい):
    AAPL 4.94兆ドル
    NVDA, 4,869,646   ← 単位がなければ『百万ドル』とみなす(日経と同じ単位)
    MSFT $3.77T / GOOGL 1637B / アマゾン AMZN 2.66 trillion
単位: T・trillion・兆 = 1兆ドル、B・billion・十億・億ドル(×1)... は下の表のとおり。
注意: AIが出した数字は間違いがある。取り込み後に『前回から2.5倍以上変わった銘柄』を警告する。"""
import os, re, shutil, sys, time

S = os.path.dirname(os.path.abspath(__file__))
F_IN = os.path.join(S, '貼り付け.txt')
F_RANK = os.path.join(S, 'ranking.txt')

UNIT = [  # (正規表現, 百万ドルへの倍率)
    (r'兆', 1e6), (r'(?:trillion|tn|t)\b', 1e6), (r'(?:billion|bn|b)\b', 1e3), (r'十億', 1e3),
    (r'(?:million|mn|m)\b', 1.0), (r'百万', 1.0), (r'億', 100.0),
]


def load_rank():
    rows = []
    for ln in open(F_RANK, encoding='utf-8'):
        a = ln.rstrip('\n').split('|')
        if len(a) >= 4:
            rows.append({'jp': a[1], 'tk': a[2], 'cap': int(a[3])})
    return rows


def parse_line(ln, known):
    """1行から (ティッカー, 百万ドル) を取り出す。見つからなければNone"""
    s = ln.replace('，', ',').replace('．', '.').replace('＄', '$')
    tks = [t for t in re.findall(r'\b[A-Z]{1,5}(?:\.[A-Z])?\b', s) if t in known]
    if not tks:
        return None
    m = re.search(r'\$?\s*([\d][\d,]*(?:\.\d+)?)\s*([A-Za-z兆億]*(?:\s*dollars?|ドル)?)', s[s.find(tks[0]) + len(tks[0]):] or s)
    if not m:
        return None
    try:
        v = float(m.group(1).replace(',', ''))
    except ValueError:
        return None
    unit = m.group(2).lower().strip()
    mult = None
    for pat, k in UNIT:
        if re.search(pat, unit):
            mult = k
            break
    if mult is None:
        mult = 1.0 if v >= 100000 else (1e3 if v >= 10 else 1e6)  # 単位なし: 大きければ百万ドル、中くらいは十億ドル、小さければ兆ドル
        note = '単位なし→' + ('百万ドル' if mult == 1.0 else '十億ドル' if mult == 1e3 else '兆ドル') + 'とみなした'
    else:
        note = ''
    return tks[0], int(round(v * mult)), note


def main():
    if not os.path.exists(F_IN):
        open(F_IN, 'w', encoding='utf-8').write('# ここに貼り付けてください(1行に1社: ティッカーと時価総額)\n# 例: AAPL 4.94兆ドル\n')
        sys.exit('貼り付け.txt を作りました。ここにデータを貼ってから、もう一度実行してください。')
    rows = load_rank()
    known = {r['tk']: r for r in rows}
    got, warn = {}, []
    for ln in open(F_IN, encoding='utf-8'):
        if not ln.strip() or ln.lstrip().startswith('#'):
            continue
        r = parse_line(ln, known)
        if r is None:
            warn.append('読めない行: ' + ln.strip()[:60])
            continue
        tk, cap, note = r
        got[tk] = cap
        old = known[tk]['cap']
        if old and (cap / old > 2.5 or cap / old < 0.4):
            warn.append(f'{tk}: 前回{old:,}→今回{cap:,}(百万ドル)。変化が大きいので単位や数字を確認してください')
        elif note:
            warn.append(f'{tk}: {note}')
    if not got:
        sys.exit('取り込める行がありませんでした。\n' + '\n'.join(warn[:10]))
    shutil.copy(F_RANK, os.path.join(S, 'ranking_backup_%s.txt' % time.strftime('%Y%m%d_%H%M')))
    for tk, cap in got.items():
        known[tk]['cap'] = cap
    rows.sort(key=lambda r: -r['cap'])
    with open(F_RANK, 'w', encoding='utf-8') as f:
        for i, r in enumerate(rows[:200], 1):
            f.write('%d|%s|%s|%d\n' % (i, r['jp'], r['tk'], r['cap']))
    print(f'取り込み {len(got)}社 / 全{len(rows)}社のうち、貼り付けに無かった{len(rows) - len(got)}社は前回の数字のままです。')
    for w in warn:
        print('  注意:', w)


if __name__ == '__main__':
    main()
