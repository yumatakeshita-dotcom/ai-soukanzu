#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tdnet_scan.py の「提携の相手を本文から読む」精度の試験(2026/11/24追加)
実際のTDnet提携の発表34件(2026/10/28〜11/20、本文は先頭8000字)で、相手を正しく決められるかを数える。
  expect  : 正解の相手(かならず決めたい)    →  正しく決められたら「当たり」、決められなければ「見送り」(安全だが取りこぼし)
  either  : 決めても見送ってもよい          →  決めたなら名前が合うこと
  どちらもなし: 決めてはいけない(解消・延長・子会社・本文なしなど)
  間違った相手を決めたら「誤り」。誤りが1件でもあれば失敗(終了コード1)。
使い方: python3 scripts/test_tdnet_body.py [-v]
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ir_watch as W
import tdnet_scan as S

cases = json.load(open(os.path.join(HERE, 'testdata', 'tdnet_alliance_2026-11-24.json'), encoding='utf-8'))
hit = miss = wrong = fine = 0
for c in cases:
    filer = S.filer_name(c['co'], c['text'])
    deal, how, why = S.pick_deal(c['title'], filer, 'alliance', c['text'])
    got = None
    if deal:
        got = deal[1] if W.clean_name(deal[0]) == filer else deal[0]
    if c.get('expect'):
        if got and S.same_co(got, c['expect']): hit += 1; tag = '当たり'
        elif got: wrong += 1; tag = '誤り'
        else: miss += 1; tag = '見送り'
    elif c.get('either'):
        if got and not S.same_co(got, c['either']): wrong += 1; tag = '誤り'
        else: fine += 1; tag = 'どちらでも'
    else:
        if got: wrong += 1; tag = '誤り'
        else: fine += 1; tag = '正しく見送り'
    if '-v' in sys.argv or tag == '誤り':
        print(f"{tag:6} {c['co'][:10]:10} → {got or '-':16} ({how or why})  {c['title'][:36]}")
n_exp = sum(1 for c in cases if c.get('expect'))
print(f'{len(cases)}件: 正解あり{n_exp}件のうち 当たり{hit}・見送り{miss}、決めてはいけない/どちらでも{fine}件、誤り{wrong}件')
sys.exit(1 if wrong else 0)
