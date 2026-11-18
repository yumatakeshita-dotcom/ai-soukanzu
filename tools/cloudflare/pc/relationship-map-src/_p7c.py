BS = chr(92)
NL = BS + 'n'
p = 'newco_data7c.py'
s = open(p, encoding='utf-8').read()
old = "{'systrom': [['2010', 'Instagramを共同創業(CEO)'], ['2012', 'Facebookが買収'], ['2018', '9月に退任を発表'], ['2021', 'Artifactを共同創業']],"
assert old in s
new = ("{'systrom': [['2006', 'スタンフォード大学を卒業(経営科学・工学)'], ['〜', 'Googleでプロダクトマーケティングを約2年(Gmailなど)'], ['2010', 'BaselineとAndreessen Horowitzから50万ドルを得て、Instagramを共同創業(CEO)'],"
       " ['2012', '4月にFacebookが約10億ドルで買収'], ['2014', 'Walmartの取締役に(〜2018年)'], ['2018', '9月24日に退任を発表'], ['2020', 'Rt.liveを共同で公開'], ['2023', '1月31日にArtifactを公開'], ['2024', '1月に終了を発表、4月2日にYahooが買収を発表'], ['2025', '9月、Instagramの利用者が30億人に(本人は退任済み)']],")
s = s.replace(old, new, 1)
old2 = ' "E.push({a:\'instagram\',b:\'threads\',k:\'owns\',label:\'2023年に派生\',since:2023});' + NL + NL + '")'
assert old2 in s, 'e2'
s = s.replace(old2, ' "E.push({a:\'systrom\',b:\'walmart\',k:\'link\',label:\'取締役(2014〜2018年)\',since:2014});' + NL + '"\n' + old2, 1)
k = "    'artifact': [['出典: Wikipedia(Artifact)', 'https://en.wikipedia.org/wiki/Artifact_(app)']],"
assert k in s
s = s.replace(k, k + "\n    'walmart': [['出典: Wikipedia(Kevin Systrom)', 'https://en.wikipedia.org/wiki/Kevin_Systrom']],", 1)
open(p, 'w', encoding='utf-8').write(s)

# ---- Metaの図に、ハビエル・オリバン(COO)とシェリル・サンドバーグ(前COO)を足す ----
p = 'build_hub2.py'
b = open(p, encoding='utf-8').read()
nodes = """ {'id': 'olivan', 'name': 'ハビエル・オリバン', 'kind': 'p', 'from': 2013, 'desc': 'COO(最高執行責任者)。スペイン生まれ。スタンフォード大学のMBA(2007年修了)を経て、2007年10月にFacebookへ入り、国際的な成長の責任者に。2011〜2018年に成長担当のVP、2018〜2022年に中核製品のVP。2022年にサンドバーグの後任としてCOOに就きました(就任時期は、報道が6月、Wikipediaが8月と食い違っています)。2025年1月の再編で、Reality Labsの事業運営も見るようになりました。', 'role': 'COO(2022年〜)'},
 {'id': 'sandberg', 'name': 'シェリル・サンドバーグ', 'kind': 'p', 'from': 2013, 'to': 2022, 'desc': '2008年から約14年間COOを務め、2022年に退任。後任はオリバンです。', 'role': '元COO'},
"""
a = " {'id': 'vanguard', 'name': 'Vanguard'"
assert b.count(a) == 1
b = b.replace(a, nodes + a, 1)
edge_anchor = "E.push({a:'koum',b:'whatsapp',k:'from',label:'共同創業'});" + NL
assert b.count(edge_anchor) == 1
b = b.replace(edge_anchor, "E.push({a:'olivan',b:'sandberg',k:'link',label:'2022年に後任',since:2022});" + NL + edge_anchor, 1)
b = b.replace("'koum': 'Jan Koum',", "'olivan': 'Javier Olivan', 'sandberg': 'Sheryl Sandberg', 'koum': 'Jan Koum',", 1)
k2 = "      'koum': [['出典: Wikipedia(Jan Koum)'"
assert b.count(k2) == 1
b = b.replace(k2, "      'olivan': [['出典: Wikipedia(Javier Oliván)', 'https://en.wikipedia.org/wiki/Javier_Olivan']],\n      'sandberg': [['出典: Wikipedia(Sheryl Sandberg)', 'https://en.wikipedia.org/wiki/Sheryl_Sandberg']],\n" + k2, 1)
open(p, 'w', encoding='utf-8').write(b)
print('ok')
