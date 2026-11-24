#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mou_followup.py の試験(2026/11/24追加)
実際の覚書の発表(ZCLOUD、2026/11/23、HKEXの発表の本文)を元に、あとの発表を模した文を作り、
 ・正式契約の締結 → 「正式契約を確認」  ・完了 → 「完了を確認」  ・失効 → 「失効・終了」
 ・決めてはいけないもの(別の会社・別の相手・日付が前・表題が覚書のまま・覚書の相手が本文にない・コードが違う)で誤りがないか
を数える。誤りが1件でもあれば失敗(終了コード1)。使い方: python3 scripts/test_mou_followup.py [-v]
"""
import datetime, json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mou_followup as M

D = datetime.date
mou = {'from': 'Hong Kong Zcloud Technology Construction', 'to': 'Shenzhen Yingshuo Cloud Technology', 'kind': '出資', 'date': '2026-11-23',
       'code': '09900', 'region': '香港', 'url': 'https://example.test/mou.pdf', 'src_name': 'HKEX ZCLOUDの開示(2026-11-23)', 'status': '未確認', 'history': []}
HEAD = 'Hong Kong Exchanges take no responsibility for the contents of this announcement.\n HONG KONG ZCLOUD TECHNOLOGY\n CONSTRUCTION LIMITED (Stock code: 9900)\n'
EXEC = HEAD + 'The Board announces that on 15 December 2026, the Company entered into the capital injection agreement with Shenzhen Yingshuo Cloud Technology Co., Ltd.'
DONE = HEAD + 'Completion of the capital injection into Shenzhen Yingshuo Cloud Technology Co., Ltd. took place on 20 January 2027.'
LAPSE = HEAD + 'The memorandum of understanding dated 23 November 2026 with Shenzhen Yingshuo Cloud Technology has lapsed and the parties decided not to proceed.'
STILL = HEAD + 'The Company entered into a memorandum of understanding with Shenzhen Yingshuo Cloud Technology Co., Ltd. regarding possible capital injection.'
OTHER = HEAD + 'The Company entered into a placing agreement with a placing agent.'
# (名前, 状態の期待 / None=関係なしと判定すること, コード, 日付, 表題, 本文)
CASES = [
    ('正式契約', '実行', '09900', D(2026, 12, 15), 'ENTERING INTO OF THE CAPITAL INJECTION AGREEMENT', EXEC),
    ('正式契約(コードが0つき)', '実行', '9900', D(2026, 12, 15), 'ENTRY INTO THE FORMAL AGREEMENT', EXEC),
    ('完了', '完了', '09900', D(2027, 1, 20), 'COMPLETION OF CAPITAL INJECTION', DONE),
    ('失効', '失効', '09900', D(2027, 3, 1), 'UPDATE ON THE MEMORANDUM OF UNDERSTANDING', LAPSE.replace('UPDATE', 'UPDATE')),
    ('表題が覚書のまま(別の覚書)', None, '09900', D(2026, 12, 1), 'FURTHER MEMORANDUM OF UNDERSTANDING IN RELATION TO POSSIBLE CAPITAL INJECTION', STILL),
    ('同じ会社だが相手が違う', None, '09900', D(2026, 12, 15), 'ENTERING INTO OF THE COOPERATION AGREEMENT', HEAD + 'The Company entered into the cooperation agreement with Another Cloud Co., Ltd.'),
    ('別の会社(コード違い)', None, '01234', D(2026, 12, 15), 'ENTERING INTO OF THE CAPITAL INJECTION AGREEMENT', EXEC),
    ('日付が覚書より前', None, '09900', D(2026, 11, 20), 'ENTERING INTO OF THE CAPITAL INJECTION AGREEMENT', EXEC),
    ('日付が覚書と同じ日(同じ発表の別版)', None, '09900', D(2026, 11, 23), 'ENTERING INTO OF THE CAPITAL INJECTION AGREEMENT', EXEC),
    ('400日より後', None, '09900', D(2028, 1, 15), 'ENTERING INTO OF THE CAPITAL INJECTION AGREEMENT', EXEC),
    ('関係ない契約(相手の名前がない)', None, '09900', D(2026, 12, 15), 'ENTERING INTO OF THE PLACING AGREEMENT', OTHER),
    ('表題に契約の語がない', None, '09900', D(2026, 12, 15), 'CHANGE OF AUDITOR', HEAD + 'Shenzhen Yingshuo Cloud Technology is mentioned. The Company entered into an agreement.'),
]
wrong = ok = 0
for name, exp, code, day, title, text in CASES:
    got, why = M.evaluate(mou, code, day, title, text)
    good = got == exp
    ok += good; wrong += (not good)
    if '-v' in sys.argv or not good:
        print(('正しい' if good else '誤り  '), f'{name:22} → {got or "-":4} ({why})')
# コードの記録がない古い線: 本文の先頭に出す側の名前があれば同じ会社とみなす
old = dict(mou, code='')
for name, exp, code, day, title, text in CASES[:1]:
    got, why = M.evaluate(old, code, day, title, text)
    good = got == '実行'; ok += good; wrong += (not good)
    if not good or '-v' in sys.argv: print(('正しい' if good else '誤り  '), 'コードなしの線', got, why)
got, why = M.evaluate(old, '09900', D(2026, 12, 15), 'ENTERING INTO OF THE CAPITAL INJECTION AGREEMENT', EXEC.replace('ZCLOUD', 'ZZZ').replace('Zcloud', 'Zzz'))
good = got is None; ok += good; wrong += (not good)
if not good or '-v' in sys.argv: print(('正しい' if good else '誤り  '), 'コードなし・別会社', got, why)
# 目録への登録と、続きの線の形(一時フォルダで。本物の inbox は触らない)
with tempfile.TemporaryDirectory() as td:
    json.dump({'items': [{'from': mou['from'], 'to': mou['to'], 'kind': '出資', 'date': '2026-11-23', 'code': '09900', 'region': '香港',
                          'note': '……。覚書(MOU)の段階で、実行は未確定。……', 'src': [[mou['src_name'], mou['url']]]},
                         {'from': 'X', 'to': 'Y', 'kind': '提携', 'date': '2026-11-23', 'note': '覚書ではない', 'src': [['a', 'https://example.test/other.pdf']]}]},
              open(os.path.join(td, '2026-11-23-hkex.json'), 'w', encoding='utf-8'))
    st = {'items': {}}
    n1 = M.sync(st, td); n2 = M.sync(st, td)
    good = (n1 == 1 and n2 == 0 and list(st['items']) == [mou['url']] and M.codes(st) == {'09900'})
    ok += good; wrong += (not good)
    if not good: print('誤り  登録', n1, n2, list(st['items']))
    evs = M.observe(st, {'code': '09900', 'title': 'ENTERING INTO OF THE CAPITAL INJECTION AGREEMENT', 'url': 'https://example.test/exec.pdf', 'day': D(2026, 12, 15)}, EXEC)
    good = len(evs) == 1 and st['items'][mou['url']]['status'] == '正式契約を確認' and not M.open_items(st)
    ok += good; wrong += (not good)
    if not good: print('誤り  observe', evs)
    fm = M.followup_money(evs[0][0], evs[0][1], '') if evs else None
    good = bool(fm) and fm['src'][0][1] == 'https://example.test/exec.pdf' and fm['src'][1][1] == mou['url'] and fm['mark'] == '正式契約を確認' and fm['confidence'] == '開示'
    ok += good; wrong += (not good)
    if not good: print('誤り  続きの線', fm)
    # 同じ発表をもう一度見ても二重にならない(確認済みは対象から外れる)
    again = M.observe(st, {'code': '09900', 'title': 'ENTERING INTO OF THE CAPITAL INJECTION AGREEMENT', 'url': 'https://example.test/exec.pdf', 'day': D(2026, 12, 15)}, EXEC)
    good = not again; ok += good; wrong += (not good)
    if not good: print('誤り  二重')
    # 失効は線にしない
    st2 = {'items': {mou['url']: dict(mou)}}
    evs2 = M.observe(st2, {'code': '09900', 'title': 'UPDATE ON THE MEMORANDUM OF UNDERSTANDING', 'url': 'https://example.test/l.pdf', 'day': D(2027, 3, 1)}, LAPSE)
    good = len(evs2) == 1 and M.followup_money(*evs2[0]) is None
    ok += good; wrong += (not good)
    if not good: print('誤り  失効')
print(f'正しい {ok}件・誤り {wrong}件')
sys.exit(1 if wrong else 0)
