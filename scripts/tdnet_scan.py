#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDnet 新着一覧の見張り(日本の人事係用、2026/11/24追加)

TDnet(適時開示)の新着一覧を毎朝ぜんぶ見て、「気になる会社」の役員人事だけPDFを開く。
ir_watch.py は相関図にある会社だけを見る。こちらは、相関図にない会社でも
AI・DX・半導体・データの担当役員が決まった発表を拾うためのもの。足すだけで、消さない。

「気になる」の決め方(表題・会社名だけで決める。ここではPDFを開かない):
  1. 表題が役員人事・組織変更である(ir_watch.py と同じ言葉の判定)
  2. かつ、次のどれか: 会社名か表題に AI・DX・デジタル・データ・半導体・ロボ・ソフト・情報・システムなどの語がある
                       / 相関図の会社でない会社でも、表題に CDO・CIO・CTO・最高…責任者 がある
  相関図の会社(jpco.js・targets_extra.txt)は ir_watch.py が見るので、ここでは重ねない。
PDFを開いたら、本文に AI系の語があるものだけ保存する(人の名前・役職は本文で確かめる)。

PDFが開けなかったものは「見送り」にせず、ir_watch.py と同じ再確認の列(inbox/ir/retry.json)に入れる。
翌日から最大3回、ir_watch.py が開き直す。

  inbox/ir/tdnet-scan-日付.json  保存先(items=本文で確かめたもの、skipped=気にならなかった件数など)
  inbox/ir/seen.txt              見たものの目録(ir_watch.py と共通。足すだけ)

使い方:
  python3 scripts/tdnet_scan.py            # 直近2営業日
  python3 scripts/tdnet_scan.py --days 3 --max 30 --dry
"""
import argparse, datetime, json, os, re, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ir_watch as W

AI_WORDS = re.compile(r'AI|ＡＩ|人工知能|DX|ＤＸ|デジタル|データ|半導体|ロボ|ソフトウェア|ソフトウエア|情報|システム|テクノロジ|IT|ＩＴ|クラウド|サイバー|ネットワーク', re.I)
BODY_AI = re.compile(r'AI|人工知能|DX|デジタル|データ|半導体|CDO|CIO|CTO|CAIO|最高(技術|情報|デジタル|データ)|情報システム|ロボ', re.I)
TITLE_C = re.compile(r'CDO|CIO|CTO|CAIO|最高(技術|情報|デジタル|データ|AI)', re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=2)
    ap.add_argument('--max', type=int, default=30, help='1回に開くPDFの上限')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    os.makedirs(W.OUT, exist_ok=True)
    T = W.load_targets()
    seen = W.load_seen()
    today = datetime.datetime.now(W.JST).date()
    days, d = [], today
    while len(days) < a.days and (today - d).days < a.days + 6:
        if d.weekday() < 5:
            days.append(d)
        d -= datetime.timedelta(days=1)
    rows_n, short = 0, []
    for day in days:
        try:
            rows = W.tdnet_rows(day)
        except Exception as e:  # noqa
            print('TDnetの一覧が読めない:', str(e)[:80])
            return
        rows_n += len(rows)
        for tm, code5, name, title, pdf in rows:
            code = W.nfkc(code5)
            code = code[:-1] if len(code) == 5 and code.endswith('0') else code
            if code in T['JP']:
                continue  # 相関図の会社は ir_watch.py の担当
            if 'TDNET|' + pdf in seen:
                continue
            if W.kind_of(title, W.JP_KINDS, W.JP_EXCLUDE) != '役員人事':
                continue
            nm = W.nfkc(name) + ' ' + W.nfkc(title)
            if not (AI_WORDS.search(nm) or TITLE_C.search(W.nfkc(title))):
                continue
            short.append({'market': 'TDnet(日本)', 'tkey': 'TDNET|' + pdf, 'code': code, 'co': name, 'co_list': name, 'title': title,
                          'cat': '役員人事', 'url': 'https://www.release.tdnet.info/inbs/' + pdf, 'day': day, 'time': tm, 'key': ''})
    print(f'一覧 {rows_n} 件 → 気になる {len(short)} 件(上限 {a.max} 件を開く)')
    items, skipped, fail, new_seen = [], [], [], []
    for c in short[:a.max]:
        text, err = W.pdf_text(c['url'])
        new_seen.append(c['tkey'])
        if not text or len(text) <= 120:
            fail.append(c)
            print('△ 開けず(再確認へ):', c['co'], c['title'][:30], err)
        elif not BODY_AI.search(W.nfkc(text)):
            skipped.append({'co': c['co'], 'title': c['title'], 'url': c['url'], 'why': '本文にAI・DX・半導体などの語がない'})
            print('× 関係なし:', c['co'], c['title'][:30])
        elif not W.date_ok(text, c['day']):
            skipped.append({'co': c['co'], 'title': c['title'], 'url': c['url'], 'why': '本文の日付が一覧と合わない'})
            print('× 日付:', c['co'], c['title'][:30])
        else:
            items.append({'d': str(c['day']), 'time': c['time'], 'market': c['market'], 'code': c['code'], 'co': c['co'], 'title': c['title'],
                          'cat': '役員人事', 'url': c['url'], 'cf': '開示', 'snippet': W.ctx_snippet(text, '異動の内容'),
                          'import': '記録のみ(人の名前・役職は本文を読んで確かめてから inbox/moves に足す)'})
            print('○', c['co'], c['title'][:40])
        time.sleep(0.5)
    if a.dry:
        return
    if fail:
        q = W.retry_load()
        have = {i['tkey'] for i in q['items']}
        q['items'] += [W.to_retry_item(c, 'PDFが開けない', tries=0) for c in fail if c['tkey'] not in have]
        W.retry_save(q)
    stamp = today.strftime('%Y-%m-%d')
    p = os.path.join(W.OUT, f'tdnet-scan-{stamp}.json')
    old = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'items': [], 'skipped': []}
    have = {x['url'] for x in old['items']}
    old['items'] += [x for x in items if x['url'] not in have]
    old['skipped'] = old.get('skipped', []) + skipped
    old.update({'date': stamp, 'kind': 'ir-scan', 'list_rows': rows_n, 'shortlist': len(short),
                'not_opened_over_limit': max(0, len(short) - a.max), 'retry_queued': len(fail)})
    json.dump(old, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(W.SEEN, 'a', encoding='utf-8') as w:
        for k in new_seen:
            w.write(k + '\n')
    print(f'保存: {p}(確かめ済み {len(items)} 件・関係なし {len(skipped)} 件・再確認へ {len(fail)} 件)')


if __name__ == '__main__':
    main()
