#!/usr/bin/env python3
"""「AI計算資源の契約まとめ」(docs/compute_deals_2026-11.html)の「開示ウォッチの新着」を更新する(2026/11/19追加)

inbox/disclosures/*.json(scripts/sec_watch.py が保存したもの)から、
大事な契約(1.01)・買収や売却の完了(2.01)・決算(2.02)・上場や資金調達の書類(S-1・424B4・Form D)を選び、
<!-- WATCH_START --> と <!-- WATCH_END --> の間に足す。足すだけで、前の行は消さない。

使い方: python3 scripts/compute_brief.py
最後に「足した行: N件」と出す。N が 1 以上なら、共有リンクにも公開し直す。
Anthropic の 424B4(上場の値段が決まった正式な書類)が見つかったときは、そう知らせる。
"""
import glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'docs', 'compute_deals_2026-11.html')
ITEMS = {'1.01', '2.01', '2.02'}
FORMS = {'S-1', 'S-1/A', '424B4', 'D', 'D/A'}
FORM_JA = {'S-1': '上場の届け出書', 'S-1/A': '上場の届け出書(訂正)', '424B4': '上場の値段の確定',
           'D': '資金調達の届け出', 'D/A': '資金調達の届け出(訂正)', '8-K': '臨時の報告'}


def pick():
    rows = {}
    for p in sorted(glob.glob(os.path.join(ROOT, 'inbox', 'disclosures', '*.json'))):
        try:
            data = json.load(open(p, encoding='utf-8'))
        except Exception:
            continue
        for x in data:
            if x.get('form') in FORMS or ITEMS & set(x.get('items', [])):
                rows[x['acc']] = x
    return sorted(rows.values(), key=lambda x: x['d'], reverse=True)


def ja_num(v):
    """'14.6 billion' → '146億ドル'、'431 million' → '4.31億ドル'。ほかはそのまま"""
    m = re.fullmatch(r'([\d.,]+) (billion|million)', v)
    if not m:
        return v
    n = float(m.group(1).replace(',', '')) * (10 if m.group(2) == 'billion' else 0.01)
    return f'{n:,.2f}'.rstrip('0').rstrip('.') + '億ドル'


def row_html(x):
    what = FORM_JA.get(x['form'], x['form'])
    its = [j for i, j in zip(x.get('items', []), x.get('items_ja', [])) if i in ITEMS]
    if its:
        what += '(' + '・'.join(its) + ')'
    nums = ''
    if x.get('numbers'):
        nums = '<br>' + html.escape('、'.join(f'{k} {ja_num(v)}' for k, v in x['numbers'].items()))
    e = html.escape
    return (f'  <tr data-acc="{e(x["acc"])}"><td class="amt">{e(x["d"])}</td><td>{e(x["co"])}</td>'
            f'<td>{e(what)}{nums}</td><td class="wl"><a href="{e(x["url"])}" target="_blank" rel="noopener">書類</a> '
            f'<span class="cf f">開示</span></td></tr>')


def main():
    s = open(PAGE, encoding='utf-8').read()
    m = re.search(r'(<!-- WATCH_START -->)(.*?)(\s*<!-- WATCH_END -->)', s, re.S)
    if not m:
        sys.exit('目印(WATCH_START / WATCH_END)が見つかりません')
    body = m.group(2)
    have = set(re.findall(r'data-acc="([^"]+)"', body))
    new = [x for x in pick() if x['acc'] not in have]
    old_rows = re.findall(r'\s*<tr data-acc=.*?</tr>', body, re.S)
    if new or not body.strip():
        rows = '\n'.join(row_html(x) for x in new) + ''.join(old_rows)
        block = ('\n  <div class="tw"><table>\n  <thead><tr><th>日付</th><th>会社</th><th>書類</th><th>確かさ</th></tr></thead>\n'
                 '  <tbody>\n' + rows.strip('\n') + '\n  </tbody>\n  </table></div>' if rows.strip() else
                 '\n  <p class="note">まだありません。</p>')
        s = s[:m.start(2)] + block + s[m.start(3):]
        open(PAGE, 'w', encoding='utf-8').write(s)
    print(f'足した行: {len(new)}件')
    for x in new:
        print(' ', x['d'], x['co'], x['form'], '・'.join(x.get('items_ja', [])), x['url'])
        if x['form'] == '424B4' and x.get('key') == 'anthropic':
            print('  ★ Anthropic の 424B4(上場の値段の確定)が出ました。「上場の条件」の値段を開示に書き直してください')


if __name__ == '__main__':
    main()
