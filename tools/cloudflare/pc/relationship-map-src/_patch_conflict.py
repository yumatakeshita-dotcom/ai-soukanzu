p = 'personal_data.py'
s = open(p, encoding='utf-8').read()
a = " (W, '買収元', 'Mark Zuckerberg', 'マーク・ザッカーバーグ', '2012年にFacebookがInstagramを買収"
i = s.index(a)
j = s.index('\n', i)
line_a = s[i:j]
conf_sys = " (R, '確執(報道)', 'Mark Zuckerberg', 'マーク・ザッカーバーグ', '買収は合意のうえでしたが、のちにInstagramの人員・資源・独立性をめぐって対立したと報じられ、2018年9月に退任。2025年のFTC裁判でシストロムは、ザッカーバーグがInstagramの成長を脅威とみて資源を絞ったと証言しました(Metaは否定)。'),"
s = s[:j + 1] + conf_sys + '\n' + s[j + 1:]
b = " (W, '買収した会社の創業者', 'Kevin Systrom', 'ケビン・シストロム', '2012年"
i = s.index(b)
j = s.index('\n', i)
conf_z = " (R, '確執(報道)', 'Kevin Systrom', 'ケビン・シストロム', 'Instagramの人員・資源・独立性をめぐり対立したと報じられ、シストロムは2018年に退任。2025年のFTC裁判で証言しました。Metaは、買収後にInstagramは大きく成長したと反論しています。'),"
s = s[:j + 1] + conf_z + '\n' + s[j + 1:]
open(p, 'w', encoding='utf-8').write(s)

p = 'newco_data7c.py'
s = open(p, encoding='utf-8').read()
s = s.replace("'role': '共同創業者 / 元CEO', 'founder': 1}", "'role': '共同創業者 / 元CEO', 'founder': 1}", 1)
s = s.replace("2018年9月に退任を発表。のちクリーガーとニュースアプリ「Artifact」を作りました。", "2018年9月に退任を発表。のちクリーガーとニュースアプリ「Artifact」を作りました。退任の背景には、買収後のInstagramの人員・資源・独立性をめぐるザッカーバーグとの対立があったと報じられています(2025年のFTC裁判で本人が証言。Metaは否定)。", 1)
s = s.replace(" \"E.push({a:'systrom',b:'krieger',k:'link',label:'共同創業'});\n\"", " \"E.push({a:'systrom',b:'krieger',k:'link',label:'共同創業'});\n\"\n \"E.push({a:'systrom',b:'zuckerberg',k:'conflict',label:'資源・独立性をめぐり対立(報道)',since:2017});\n\"", 1)
s = s.replace("2018年に創業者2人が退任しました。'}", "2018年に創業者2人が退任しました。FTC対Meta裁判(買収が競争を損なったかが争点)では、2025年11月に連邦地裁がMetaの勝訴と判断しました。'}", 1)
open(p, 'w', encoding='utf-8').write(s)

p = 'build_hub2.py'
s = open(p, encoding='utf-8').read()
anchor = "E.push({a:'zuckerberg',b:'instagram',k:'link',label:'買収を主導',since:2012});\n\""
assert anchor in s
s = s.replace(anchor, anchor + "\n \"E.push({a:'systrom',b:'zuckerberg',k:'conflict',label:'資源・独立性をめぐり対立(報道)',since:2017});\n\"", 1)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
