"""Yahoo!ニュースの検索ページ(公開されているもの)から、資金調達・IPO・買収・提携の見出しを集めて、ニュース(funding_news.json)と企業間の関係のニュース(relation_news.json)に足す。
保存するのは、見出し・リンク・日付・配信元・抜粋(検索結果に出ている短い文)だけ。本文は保存しない。Claude不要。
使い方: python -I fetch_yahoo.py"""
import datetime as dt, html, re, sys, time, urllib.parse, urllib.request
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
import fetch_sources as F
UA = {'User-Agent': 'Mozilla/5.0 (compatible; relationship-map-research/1.0; personal use)'}
FUND_Q = ['資金調達 シリーズA', '資金調達 シリーズB', '資金調達 シリーズC', 'シードラウンド 調達', 'プレシリーズA 調達', '第三者割当増資 億円 スタートアップ', '調達 AIスタートアップ 億円', 'ユニコーン 企業価値 調達',
          '新規上場 承認 スタートアップ', 'IPO 上場承認 グロース', 'ベンチャー 出資 億円 発表', '資金調達 ラウンド リード投資家', '資金調達 自動運転', '資金調達 ロボット', '資金調達 宇宙 スタートアップ']
REL_Q = ['買収 発表 億円', '完全子会社化 発表', 'TOB 発表 株式公開買い付け', '資本業務提携 発表', '経営統合 発表', '株式取得 子会社化', 'M&A 買収 AI企業', '買収 スタートアップ 米国', '出資 戦略的提携 発表', '共同開発 提携 発表 AI']
DATE = re.compile(r'(\d{1,2})/(\d{1,2})\(.\)\s*(\d{1,2}):(\d{2})')


def fetch(q):
    u = 'https://news.yahoo.co.jp/search?p=' + urllib.parse.quote(q) + '&ei=utf-8&fr=news_sw'
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode('utf-8', 'replace')
        except Exception:
            time.sleep(3 * (i + 1))
    return ''


def parse(page):
    out = []
    today = dt.date.today()
    for href, body in re.findall(r'<li class="[^"]*"><a href="(https://news\.yahoo\.co\.jp/articles/[0-9a-f]+)"(.*?)</li>', page, flags=re.S):
        body = re.sub(r'<!--.*?-->|</?em[^>]*>|<source[^>]*>|<img[^>]*>', '', body, flags=re.S)
        segs = [re.sub('[⁠​‌]', '', html.unescape(s)).strip() for s in re.sub(r'<[^>]+>', chr(1), body).split(chr(1))]
        segs = [s for s in segs if s and not s.startswith('data-cl-params')]
        di = next((i for i in range(len(segs) - 1, -1, -1) if DATE.search(segs[i])), None)
        if di is None or di < 3:
            continue
        m = DATE.search(segs[di])
        d = dt.date(today.year, int(m.group(1)), int(m.group(2)))
        if d > today:
            d = dt.date(today.year - 1, d.month, d.day)
        media = segs[di - 2]
        ti = next((i for i, x in enumerate(segs[:di - 2]) if len(x) >= 10 and not DATE.search(x)), None)
        if ti is None:
            continue
        title = re.sub(r'[\(（][^()（）]{2,20}[\)）]$', '', segs[ti]).strip()
        snip = ''.join(segs[ti + 1:di - 2])[:200]
        out.append({'u': href, 't': title[:160], 'd': d.isoformat(), 's': 'Yahoo!ニュース(' + media + ')', 'x': snip})
    return out


def main():
    hist = F.load('funding_news.json', [])
    seen = {h['u'] for h in hist}
    cut = (dt.date.today() - dt.timedelta(days=60)).isoformat()
    nf = 0
    for q in FUND_Q:
        for r in parse(fetch(q)):
            if r['u'] in seen or r['d'] < cut:
                continue
            if not (F.JP_KEY.search(r['t']) and F.JP_NEED.search(r['t'])):
                continue
            amt, uni = F.classify(r['t'], 'j')
            row = {'u': r['u'], 't': r['t'], 'd': r['d'], 's': r['s'], 'r': 'j', 'a': amt, 'c': uni, 'x': r['x']}
            row.update(F.parse_funding(r['t'], 'j', r['x']))
            hist.append(row)
            seen.add(r['u'])
            nf += 1
        time.sleep(1.5)
    hist.sort(key=lambda h: h['d'], reverse=True)
    F.save('funding_news.json', hist[:3000])
    rel = F.load('relation_news.json', [])
    seen = {h['u'] for h in rel}
    nr = 0
    for q in REL_Q:
        for r in parse(fetch(q)):
            if r['u'] in seen or r['d'] < cut:
                continue
            if not F.REL_JP.search(r['t'] + ' ' + r['x']):
                continue
            rel.append({'u': r['u'], 't': r['t'], 'd': r['d'], 's': 'Yahoo!ニュース', 'r': 'j', 'x': r['x'][:240]})
            seen.add(r['u'])
            nr += 1
        time.sleep(1.5)
    rel.sort(key=lambda h: h['d'], reverse=True)
    F.save('relation_news.json', rel[:3000])
    print(f'Yahoo!ニュース: 資金調達{nf}件・関係{nr}件を追加(履歴 {len(hist)} / {len(rel)})')


if __name__ == '__main__':
    main()
