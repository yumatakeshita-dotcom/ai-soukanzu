"""日経『日本企業 時価総額上位』(7ページ・約200社)を取得して ranking_jp.txt を更新する。Claudeは使わない。
使い方: python update_ranking_jp.py [--dry]
出力: ranking_jp.txt(順位|社名|証券コード|市場|時価総額(百万円)|更新日時)"""
import os, re, sys, time, urllib.request

S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
BASE = 'https://www.nikkei.com/marketdata/ranking-jp/market-cap-high/'
ROW = re.compile(
    r'<td[^>]*><div><div class="">(\d+)</div></div></td>'                       # 順位
    r'<td[^>]*><div><a title="([^"]*)"[^>]*>[^<]*</a>'                            # 社名
    r'<div[^>]*><span>([0-9A-Z]{4})</span><span>([^<]*)</span></div></div></td>'   # 証券コード・市場
    r'<td[^>]*><div><div class="">([\d,]+)</div>', re.S)                          # 時価総額(円)
STAMP = re.compile(r'(\d{4})年(\d{2})月(\d{2})日')


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
    rows, stamp = [], ''
    for p in range(1, 8):
        html = fetch(p)
        got = ROW.findall(html)
        if not got:
            sys.exit(f'ページ{p}の表を読めませんでした(ページの作りが変わった可能性)。ranking_jp.txt は変更していません。')
        if not stamp:
            m = STAMP.search(html)
            stamp = '%s-%s-%s' % m.groups() if m else ''
        rows += got
        time.sleep(2)
    rows.sort(key=lambda r: int(r[0]))
    if len(rows) < 150 or int(rows[0][0]) != 1:
        sys.exit(f'取得件数が不自然です({len(rows)}件)。ranking_jp.txt は変更していません。')
    f = os.path.join(S, 'ranking_jp.txt')
    old = set()
    if os.path.exists(f):
        for ln in open(f, encoding='utf-8'):
            a = ln.rstrip('\n').split('|')
            if len(a) >= 4:
                old.add(a[2])
    out = [f'{r[0]}|{r[1]}|{r[2]}|{r[3]}|{int(r[4].replace(",", "")) // 1000000}|{stamp}' for r in rows]
    new_t = {r[2] for r in rows}
    if '--dry' not in sys.argv:
        open(f, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(f'日本株 取得 {len(rows)}社 / 新規ランクイン {sorted(new_t - old)} / 圏外 {sorted(old - new_t)}')


if __name__ == '__main__':
    main()
