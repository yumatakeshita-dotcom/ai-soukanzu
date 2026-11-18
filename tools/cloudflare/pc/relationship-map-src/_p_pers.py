p = 'personal_data.py'
s = open(p, encoding='utf-8').read()
a = " (W, '元COO', 'Sheryl Sandberg', 'シェリル・サンドバーグ', '2022年までCOOを務めました。'),"
assert a in s
s = s.replace(a, a + "\n (W, 'COO', 'Javier Olivan', 'ハビエル・オリバン', '2022年にサンドバーグの後任としてCOOに就きました。'),", 1)
add = """'Javier Olivan': [
 (W, '上司', 'Mark Zuckerberg', 'マーク・ザッカーバーグ', 'MetaのCEO。'),
 (W, '前任', 'Sheryl Sandberg', 'シェリル・サンドバーグ', '2022年に、COOを引き継ぎました。'),
 (W, '元の上司', 'Chamath Palihapitiya', 'チャマス・パリハピティヤ', '2007年に、国際的な成長の責任者として入社したときの上司。'),
 (M, '同僚', 'Chris Cox', 'クリス・コックス', 'MetaのCPO。'),
],
'Jan Koum': [
 (W, '共同創業者', 'Brian Acton', 'ブライアン・アクトン', 'WhatsAppを共に創業。'),
 (W, '買収元', 'Mark Zuckerberg', 'マーク・ザッカーバーグ', '2014年にFacebookがWhatsAppを買収。2018年に衝突が報じられ、退任。'),
],
'Brian Acton': [
 (W, '共同創業者', 'Jan Koum', 'ジャン・クーム', 'WhatsAppを共に創業。'),
 (W, '共同設立者', 'Moxie Marlinspike', 'モクシー・マーリンスパイク', '2018年にSignal Foundationを共同で設立。'),
],
'Palmer Luckey': [
 (W, '買収元', 'Mark Zuckerberg', 'マーク・ザッカーバーグ', '2014年にFacebookがOculusを買収。2017年に退社。'),
 (W, '初代CEO', 'Brendan Iribe', 'ブレンダン・イリベ', 'Oculusの最初のCEO。'),
],
"""
k = "'Kevin Systrom': ["
assert s.count(k) == 1
s = s.replace(k, add + k, 1)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
