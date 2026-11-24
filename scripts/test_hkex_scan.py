#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hkex_scan.py の精度の試験(2026/11/24追加)
 (1) 表題だけの読み取り: 実在の形の表題を並べ、相手が正しく読めるか・読んではいけないものを読まないかを数える
 (2) 実際のHKEXの発表(2026/11/23〜24、本文は先頭7000字)13件で、自動で足す/足さないの判定を数える
誤りが1件でもあれば失敗(終了コード1)。使い方: python3 scripts/test_hkex_scan.py [-v]
"""
import json, os, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hkex_scan as H

# (表題, 正しい相手(大文字)と種類 / None=読んではいけない)
TITLES = [
    ("VOLUNTARY ANNOUNCEMENT THE FUND'S INVESTMENT IN DEEPSEEK", ('DEEPSEEK', '出資')),
    ("VOLUNTARY ANNOUNCEMENT INVESTMENT IN MOONSHOT AI", ('MOONSHOT AI', '出資')),
    ("DISCLOSEABLE TRANSACTION SUBSCRIPTION OF SHARES IN ZHIPU", ('ZHIPU', '出資')),
    ("STRATEGIC COOPERATION AGREEMENT WITH NVIDIA", ('NVIDIA', '提携')),
    ("VERY SUBSTANTIAL ACQUISITION IN RELATION TO THE ACQUISITION OF 100% EQUITY INTEREST IN SHANGHAI JINGGUAN INTELLIGENT TECHNOLOGY CO., LTD.", ('SHANGHAI JINGGUAN INTELLIGENT TECHNOLOGY', '買収')),
    ("MEMORANDUM OF UNDERSTANDING WITH SENSETIME", ('SENSETIME', '提携')),
    ("MEMORANDUM OF UNDERSTANDING IN RELATION TO POSSIBLE CAPITAL INJECTION INTO THE TARGET COMPANY", None),
    ("INVESTMENT IN WEALTH MANAGEMENT PRODUCTS", None),
    ("INVESTMENT IN THE TARGET COMPANY", None),
    ("ENTERING INTO THE COOPERATION AGREEMENT", None),
    ("DISCLOSEABLE TRANSACTION IN RELATION TO FORMATION OF JOINT VENTURE", None),
    ("CONNECTED TRANSACTION NEW OPEL C-SUV COOPERATION AGREEMENT", None),
    ("ACQUISITION OF SHARES IN THE SUBSIDIARY", None),
    ("INVESTMENT IN 3 PROPERTIES", None),
    ("INSIDE INFORMATION ANNOUNCEMENT - PROPOSED ACQUISITION OF SHARES BY A CONTROLLING SHAREHOLDER", None),
]
# 実際の発表: (銘柄の名前の一部, 期待: (出す側, 相手, 種類) / None)
REAL = {'HUISHENG': ('Huisheng International Holdings', 'Shanghai Jingguan Intelligent Technology', '買収'),
        'ZHIHU': ('Zhihu(知乎)', 'DeepSeek', '出資'),
        'ZCLOUD': ('Hong Kong Zcloud Technology Construction', 'Shenzhen Yingshuo Cloud Technology', '出資')}

wrong = ok = 0
for t, exp in TITLES:
    x, kind = H.x_from_title(t)
    got = (x, kind) if x else None
    good = (got is None and exp is None) or (got and exp and H.W.nfkc(got[0]).upper().strip(' .,') == exp[0] and got[1] == exp[1])
    if good: ok += 1
    else:
        wrong += 1; print('誤り(表題):', t[:70], '→', got, '/ 期待', exp)
cases = json.load(open(os.path.join(HERE, 'testdata', 'hkex_2026-11-24.json'), encoding='utf-8'))
auto = 0
for c in cases:
    c['day'] = datetime.date.fromisoformat(c['day'])
    deal, why = H.decide(c, c['text'], c['co'] if c['in_map'] else '')
    key = next((k for k in REAL if k in c['sn']), None)
    exp = REAL.get(key)
    got = (deal['from'], deal['to'], deal['kind']) if deal else None
    if got == exp: ok += 1
    else:
        wrong += 1; print('誤り(本文):', c['sn'], c['title'][:50], '→', got or why, '/ 期待', exp)
    auto += bool(deal)
    if '-v' in sys.argv: print('○' if deal else '·', c['sn'], '→', got or why)
# 「Target Company」の呼び名を本文の定義から読む部分(人工の本文): (本文, 期待の名前 / None=決めてはいけない)
DEF = 'The Target Company is mentioned. ' * 3
LABELS = [
    ('“Target Company”      (Shenzhen Yingshuo Cloud Technology\n                       Co., Ltd.*)\n\n' + DEF, 'Shenzhen Yingshuo Cloud Technology Co., Ltd'),
    ('Alpha Intelligent Technology Co., Ltd. (the “Target Company”) ' + DEF, 'Alpha Intelligent Technology Co., Ltd'),
    (DEF, None),                                                                   # 定義がない
    ('“Target Company”   a company incorporated in the PRC\n\n' + DEF, None),        # 定義が説明文で、名前ではない
    ('“Target Company”   Alpha Cloud Co., Ltd.\n\n“Target Company”   Beta Cloud Co., Ltd.\n\n' + DEF, None),  # 定義が2つ
    ('“Target Company”   Alpha Cloud Co., Ltd.\n\nThe Target Company once.', None),  # 呼び名が本文に3回未満
]
for body, exp in LABELS:
    got, why = H.resolve_label('Target Company', body)
    if got == exp: ok += 1
    else:
        wrong += 1; print('誤り(定義):', body[:50].replace('\n', ' '), '→', got or why, '/ 期待', exp)
print(f'表題{len(TITLES)}件・実際の発表{len(cases)}件: 正しい{ok}件・誤り{wrong}件(うち自動で足すのは実際の発表のうち{auto}件)')
sys.exit(1 if wrong else 0)
