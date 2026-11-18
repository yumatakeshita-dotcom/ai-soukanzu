"""日経『米国株 時価総額上位』(7ページ・200社)を取得して ranking.txt を更新する。Claudeは使わない。
使い方: python update_ranking.py [--dry]
出力: ranking.txt(順位|社名|ティッカー|時価総額(百万ドル))。新規ランクイン/圏外になった銘柄を表示する。"""
import os, re, sys, time, urllib.request

S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
BASE = 'https://www.nikkei.com/marketdata/ranking-us/market-cap-high/'
ROW = re.compile(
    r'<td[^>]*><div><div class="">(\d+)</div></div></td>'               # 順位
    r'<td[^>]*><div><a title="([^"]*)"[^>]*>[^<]*</a>'                    # 社名
    r'<div[^>]*><span>([A-Z0-9.\-]+)</span>.*?</div></div></td>'            # ティッカー
    r'<td[^>]*><div><div class="">([\d,\.]+)</div>', re.S)                 # 時価総額


def fetch(page):
    url = BASE + ('' if page == 1 else f'?page={page}')
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
    for enc in ('utf-8', 'cp932'):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return raw.decode('utf-8', 'replace')


def main():
    rows = []
    for p in range(1, 8):
        html = fetch(p)
        got = ROW.findall(html)
        if not got:
            sys.exit(f'ページ{p}の表を読めませんでした(ページの作りが変わった可能性)。ranking.txt は変更していません。')
        rows += got
        time.sleep(2)
    rows.sort(key=lambda r: int(r[0]))
    if len(rows) < 190 or int(rows[0][0]) != 1:
        sys.exit(f'取得件数が不自然です({len(rows)}件)。ranking.txt は変更していません。')
    old = {}
    f = os.path.join(S, 'ranking.txt')
    if os.path.exists(f):
        for ln in open(f, encoding='utf-8'):
            a = ln.rstrip('\n').split('|')
            if len(a) >= 4:
                old[a[2]] = int(a[0])
    out = [f'{r[0]}|{r[1]}|{r[2]}|{int(float(r[3].replace(",", "")))}' for r in rows]
    new_t = {r[2] for r in rows}
    added = sorted(new_t - set(old))
    dropped = sorted(set(old) - new_t)
    if '--dry' not in sys.argv:
        open(f, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(f'取得 {len(rows)}社 / 新規ランクイン {added} / 圏外 {dropped}')
    return added


if __name__ == '__main__':
    main()
