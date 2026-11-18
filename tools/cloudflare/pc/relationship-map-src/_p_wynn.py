BS = chr(92)
NL = BS + 'n'
p = 'newco_data7f.py'
s = open(p, encoding='utf-8').read()
s = s.replace(", 'role': '著者 / 元Facebookのグローバル公共政策ディレクター', 'founder': 1}", ", 'role': '著者 / 元Facebookのグローバル公共政策ディレクター'}", 1)
s = s.replace("{'book': 'https://us.macmillan.com/books/9781250391261/carelesspeople/'}", "{}", 1)
open(p, 'w', encoding='utf-8').write(s)
# build_hub2
p = 'build_hub2.py'
b = open(p, encoding='utf-8').read()
b = b.replace("from newco_data7e import CO7E\n", "from newco_data7e import CO7E\nfrom newco_data7f import CO7F\n", 1)
b = b.replace("**CO7D, **CO7E, **CO8}", "**CO7D, **CO7E, **CO7F, **CO8}", 1)
b = b.replace("**__import__('newco_data7e').CO7E,", "**__import__('newco_data7e').CO7E, **__import__('newco_data7f').CO7F,", 1)
nodes = """ {'id': 'wynn', 'name': 'サラ・ウィン・ウィリアムズ', 'kind': 'p', 'from': 2013, 'to': 2017, 'desc': 'ニュージーランド出身の弁護士・外交官。2011年にFacebookへ入り、グローバル公共政策のディレクターに。2017年に解雇され、2025年3月に回顧録『Careless People』を出版しました(Metaは反論し、仲裁で発言を制限)。', 'role': '元グローバル公共政策ディレクター / 著者'},
 {'id': 'kaplan', 'name': 'ジョエル・カプラン', 'kind': 'p', 'from': 2013, 'desc': 'Metaのチーフ・グローバル・アフェアーズ・オフィサー。ウィン・ウィリアムズの元の上司で、本の中の主な敵対者。ハラスメントの主張について、Metaは2017年の調査で問題なしと判断したと説明しています。', 'role': 'グローバル・アフェアーズ責任者'},
 {'id': 'carelesspeople', 'name': '『Careless People』', 'kind': 'o', 'from': 2025, 'desc': 'ウィン・ウィリアムズの回顧録(2025年3月11日)。Metaは「古い、すでに報じられた主張」「虚偽」と反論。ダブルクリックで、登場人物の図を開きます。', 'role': '元幹部の回顧録'},
"""
a = " {'id': 'vanguard', 'name': 'Vanguard'"
assert b.count(a) == 1
b = b.replace(a, nodes + a, 1)
anchor = "E.push({a:'olivan',b:'sandberg',k:'link',label:'2022年に後任',since:2022});" + NL
assert b.count(anchor) == 1
b = b.replace(anchor, anchor + "E.push({a:'wynn',b:'carelesspeople',k:'link',label:'著者'});" + NL + "E.push({a:'wynn',b:'kaplan',k:'conflict',label:'ハラスメントを報告したと主張',since:2017});" + NL + "E.push({a:'wynn',b:'meta',k:'conflict',label:'2017年に解雇、2025年に仲裁',since:2025});" + NL, 1)
b = b.replace("'olivan': 'Javier Olivan',", "'olivan': 'Javier Olivan', 'wynn': 'Sarah Wynn-Williams', 'kaplan': 'Joel Kaplan',", 1)
k2 = "      'olivan': [['出典: Wikipedia(Javier Oliván)'"
assert b.count(k2) == 1
b = b.replace(k2, "      'wynn': [['出典: Wikipedia(Sarah Wynn-Williams)', 'https://en.wikipedia.org/wiki/Sarah_Wynn-Williams']],\n      'kaplan': [['出典: Wikipedia(Joel Kaplan)', 'https://en.wikipedia.org/wiki/Joel_Kaplan']],\n      'carelesspeople': [['出典: Wikipedia(Careless People)', 'https://en.wikipedia.org/wiki/Careless_People']],\n" + k2, 1)
open(p, 'w', encoding='utf-8').write(b)
# build_mapco
p = 'build_mapco.py'
m = open(p, encoding='utf-8').read()
m = m.replace("CO_ALL.update(__import__('newco_data7e').CO7E)\n", "CO_ALL.update(__import__('newco_data7e').CO7E)\nCO_ALL.update(__import__('newco_data7f').CO7F)\n", 1)
open(p, 'w', encoding='utf-8').write(m)
# template
p = 'hub_template.html'
t = open(p, encoding='utf-8').read()
note = '顔写真はWikipedia(Wikimedia Commons)掲載の画像です。写真がない人はイニシャル表示です。本の内容は、著者の「主張」であり、事実として確定したものではありません。Metaの反論と、係争の状況を併記しています。登場人物は、役割が確認できた人物だけで、本の全文・索引は確認できていません。'
k = "  instagram:{name:'Instagram'"
assert t.count(k) == 1
t = t.replace(k, "  carelesspeople:{name:'『Careless People』',min:2011,sub:1,note:'" + note + "'},\n" + k, 1)
K = "const ALIAS={periodic:'periodic',"
assert t.count(K) == 1
t = t.replace(K, "const ALIAS={carelesspeople:'carelesspeople',periodic:'periodic',", 1)
open(p, 'w', encoding='utf-8').write(t)
# personal_data
p = 'personal_data.py'
s = open(p, encoding='utf-8').read()
add = """'Sarah Wynn-Williams': [
 (W, '元の上司(本の敵対者)', 'Joel Kaplan', 'ジョエル・カプラン', 'ハラスメントを報告したと主張。Metaは、2017年の調査で問題なしと説明しています。'),
 (W, '元の上司', 'Elliot Schrage', 'エリオット・シュレージ', '2017年に著者を解雇したと、声明で述べています。'),
 (R, '本の中の主張', 'Mark Zuckerberg', 'マーク・ザッカーバーグ', '中国市場への進出などをめぐる主張(Metaは否定)。'),
 (R, '本の中の主張', 'Sheryl Sandberg', 'シェリル・サンドバーグ', 'ダボスからの自家用機での出来事についての主張(サンドバーグはコメントを控えています)。'),
 (R, '係争', 'Meta', 'Meta', '2025年に仲裁で発言を制限され、2026年6月にMetaを提訴。'),
 (O, '元の勤め先', 'Facebook', 'Facebook', '2011〜2017年にグローバル公共政策のディレクター。'),
 (O, '元の勤め先', 'New Zealand diplomatic service', 'ニュージーランド外務省', '2002〜2007年に政策アドバイザー、2007〜2011年に在米大使館で政治・政府関係。'),
],
"""
k = "'Javier Olivan': ["
assert s.count(k) == 1
s = s.replace(k, add + k, 1)
open(p, 'w', encoding='utf-8').write(s)
# merge script
p = '_merge_insta.py'
g = open(p, encoding='utf-8').read()
g = g.replace("'covariant', 'appliedcompute']", "'covariant', 'appliedcompute', 'carelesspeople']", 1)
g = g.replace("ADD = \"periodic:", "ADD = \"carelesspeople:'carelesspeople',periodic:", 1)
g = g.replace("NEWE = (\"b:'instagram'\",", "NEWE = (\"b:'carelesspeople'\", \"a:'wynn'\", \"b:'instagram'\",", 1)
g = g.replace("assert 14 <= len(mine_e) <= 20", "assert 14 <= len(mine_e) <= 26", 1)
open(p, 'w', encoding='utf-8').write(g)
print('ok')
