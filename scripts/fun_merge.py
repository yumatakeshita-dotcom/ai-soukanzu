#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""「おもしろ情報」(メニュー「おもしろ」)に、調査タスクの結果を自動で足す。2026/11/21追加。

- 入力: inbox/fun/日付.json(毎朝の調査が足す。形は docs/fun_research.md)
- 出力: site/data/finds.js の4行目 `const FUN_AUTO={gear:[...],...}`(毎朝9:13の merge_inbox.py が書く。手で直さない)
- 足すだけ。手書きの site/data/fun.js は読まない・書き換えない(画面側で、同じ人+見出しは手書きを優先して重ねる)
- 入れる条件(1つでも欠けたら入れない。理由を表示する):
    欄(cat)が gear/book/name/habit/quote のどれか、人(p)・見出し(t)・ひとこと(note)がある、
    出典(src)に https のURLが1つ以上ある、確かさ(cf)が f/o/s/r のどれか、
    確認(chk)が o(ページを開いて確かめた)か s(複数の報道で確かめた)、
    名言(quote)で原文(q)があるときは、出典のページを開いて本文に原文がそのまま載っていること(chk が o のものだけ)
- 推測・うわさ・健康や家族などの私生活の話は入れない
"""
import glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'site', 'data', 'finds.js')
CATS = ('gear', 'book', 'name', 'habit', 'quote')


def ok_item(it):
    if it.get('cat') not in CATS:
        return '欄(cat)が違う'
    for k in ('p', 't', 'note'):
        if not str(it.get(k) or '').strip():
            return k + ' が空'
    srcs = [s for s in (it.get('src') or []) if isinstance(s, (list, tuple)) and len(s) >= 2 and re.match(r'https?://', str(s[1]))]
    if not srcs:
        return '出典のURLなし'
    if it.get('cf') not in ('f', 'o', 's', 'r'):
        return 'cf が違う'
    if it.get('chk') not in ('o', 's'):
        return 'chk が違う(o か s)'
    if it.get('q') and it.get('chk') != 'o':
        return '名言の原文は、ページを開いて確かめたもの(chk=o)だけ'
    return ''


def build():
    out = {c: [] for c in CATS}
    seen = set()
    skipped = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'inbox', 'fun', '*.json'))):
        try:
            rows = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            skipped.append((os.path.basename(f), '読めない: %s' % e)); continue
        if isinstance(rows, dict):
            rows = rows.get('items', [])
        for it in rows:
            why = ok_item(it)
            if why:
                skipped.append((os.path.basename(f) + ' ' + str(it.get('p', '?')), why)); continue
            key = (it['cat'], (it['p'] + '|' + it['t']).lower())
            if key in seen:
                continue
            seen.add(key)
            row = {k: it[k] for k in ('p', 'en', 't', 'note', 'q', 'y', 'cf', 'chk', 'asof', 'src', 'link') if it.get(k)}
            row['auto'] = 1
            out[it['cat']].append(row)
    return out, skipped


def js_line(out=None):
    out = build()[0] if out is None else out
    return ('const FUN_AUTO=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) +
            ';// おもしろ情報に自動で足したもの(scripts/fun_merge.py が inbox/fun/ から毎回作る。手で直さない)\n')


def report(out, skipped=()):
    print('おもしろ情報(自動): ' + '、'.join('%s %d件' % (c, len(v)) for c, v in out.items()) + '(合計%d件)' % sum(len(v) for v in out.values()))
    for n, w in skipped:
        print('  入れなかった: %s … %s' % (n, w))


def main():
    """単独で動かしたとき: finds.js の FUN_AUTO の行だけを書き換える(ほかの行はそのまま)"""
    out, skipped = build()
    lines = open(OUT, encoding='utf-8').read().splitlines(True)
    keep = [l for l in lines if not l.startswith('const FUN_AUTO=')]
    if keep and not keep[-1].endswith('\n'):
        keep[-1] += '\n'
    open(OUT, 'w', encoding='utf-8').write(''.join(keep) + js_line(out))
    report(out, skipped)


if __name__ == '__main__':
    main()
