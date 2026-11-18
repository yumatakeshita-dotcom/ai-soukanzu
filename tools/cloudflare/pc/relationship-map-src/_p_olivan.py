import re
p = 'personal_data.py'
s = open(p, encoding='utf-8').read()
i = s.index("'Javier Olivan': [")
j = s.index("],\n", i) + 3
new = """'Javier Olivan': [
 (W, '上司(CEO)', 'Mark Zuckerberg', 'マーク・ザッカーバーグ', '2007年に、スタンフォードのMBA修了後、ザッカーバーグからの採用の申し出を受けて入社。現在のMetaのCEO。'),
 (W, '前任(COO)', 'Sheryl Sandberg', 'シェリル・サンドバーグ', '約14年務めたCOOを2022年に退き、オリバンが引き継ぎました(就任は、報道が6月、Wikipediaが8月)。'),
 (W, '入社時の上司', 'Chamath Palihapitiya', 'チャマス・パリハピティヤ', '2007年10月、Facebookの国際的な成長の責任者として入ったときの上司(成長チームの責任者)。'),
 (W, '同僚', 'Chris Cox', 'クリス・コックス', 'MetaのCPO。'),
 (W, '助言した買収', 'WhatsApp', 'WhatsApp', '成長チームの責任者として、WhatsApp(2014年)の買収に助言したとされます。'),
 (W, '助言した買収', 'Onavo', 'Onavo', '同じく、Onavoの買収に助言したとされます。'),
 (W, '推進した取り組み', 'Internet.org', 'Internet.org', '成長チームの責任者(2011〜2018年)として、推進に関わりました。'),
 (W, '推進した取り組み', 'Facebook Lite', 'Facebook Lite', '同じく、軽量版アプリの推進に関わりました。'),
 (W, '2025年に追加の担当', 'Reality Labs', 'Reality Labs', '2025年1月の再編で、Reality Labsの事業運営も見るようになりました。'),
 (O, '外部の取締役(元)', 'Mercado Libre', 'Mercado Libre', 'ラテンアメリカのEコマース企業。取締役を6年務めました(期間の詳細は確認できていません)。'),
 (O, '外部の取締役(現)', 'Endeavor Global', 'Endeavor Global', '起業家を支援する非営利団体の取締役。'),
 (O, '取締役(SPAC)', 'Vy Global Growth', 'Vy Global Growth', '特別買収目的会社。Satellogicへの出資で知られ、2022年の合併前に取締役を務めました。'),
 (O, '合併先', 'Satellogic', 'Satellogic', '衛星画像の会社。Vy Global Growthとの2022年の合併で上場しました。'),
 (O, 'フェロー(2014年)', 'Aspen Institute', 'アスペン研究所', '2014年に、ヘンリー・クラウン・フェローに選ばれました。'),
 (O, '最初の職場', 'Siemens', 'Siemens', 'ミュンヘンで研究開発エンジニア。画像処理のアルゴリズムで特許を取りました。のちSiemens Mobileでプロダクトマネージャー。'),
 (O, '転職先', 'NTT Data', 'NTT Data', '東京へ移り、無線の映像技術に取り組みました。'),
 (O, 'MBA(2005〜2007年)', 'Stanford University', 'スタンフォード大学', '2005年に入学し、2007年に修了。授業でFacebookも事例として学びました。'),
 (O, '学部(1995〜2002年)', 'Tecnun, University of Navarra', 'ナバラ大学(テクヌン)', 'スペイン・パンプローナ。電気工学・産業工学を学びました。'),
 (O, '学生時代の挑戦', 'Nosuni', 'Nosuni', 'スタンフォード在学中に、友人とスペイン語版のFacebookを作りましたが、うまくいきませんでした。これがきっかけで、Facebookに採用されたと報じられています。'),
],
"""
s = s[:i] + new + s[j:]
open(p, 'w', encoding='utf-8').write(s)

p = 'build_hub2.py'
b = open(p, encoding='utf-8').read()
old = [x for x in b.split('\n') if "{'id': 'olivan'" in x]
assert len(old) == 1
newl = " {'id': 'olivan', 'name': 'ハビエル・オリバン', 'kind': 'p', 'from': 2013, 'desc': 'COO(最高執行責任者)。1977年スペイン生まれ。ナバラ大学(テクヌン)で工学を学び、Siemens、NTT Dataを経て、スタンフォードのMBA(2007年修了)へ。2007年10月にFacebookへ入り、国際的な成長の責任者に(上司はパリハピティヤ)。2011〜2018年に成長担当のVP(Internet.org、Facebook Liteを推進。WhatsApp、Onavoの買収に助言)、2018年に信頼と安全の担当、2018〜2022年に中核製品のVPを務めました。2022年にサンドバーグの後任としてCOOに就きました(就任時期は、報道が6月、Wikipediaが8月と食い違っています)。2025年1月の再編で、Reality Labsの事業運営も見るようになりました。外部ではEndeavor Globalの取締役、元Mercado Libreの取締役(6年)。ダブルクリックで、個人の相関図を開きます。', 'role': 'COO(2022年〜)'},"
b = b.replace(old[0], newl, 1)
# 経歴(CAREER)
k = "mC = {\n"
assert b.count(k) == 1
b = b.replace(k, k + " 'olivan': [['1977', 'スペインに生まれる'], ['2002', 'ナバラ大学(テクヌン)を卒業'], ['2007', 'スタンフォードのMBAを修了し、10月にFacebookへ(国際的な成長の責任者)'], ['2011', '成長担当のVPに(〜2018年)'], ['2014', 'アスペン研究所のヘンリー・クラウン・フェロー'], ['2018', '信頼と安全の担当、のち中核製品のVP'], ['2022', 'サンドバーグの後任としてCOOに'], ['2025', '1月、Reality Labsの事業運営も担当']],\n 'sandberg': [['2008', 'Facebookに入社しCOOに'], ['2022', 'COOを退任(約14年)']],\n", 1)
open(p, 'w', encoding='utf-8').write(b)
print('ok')
