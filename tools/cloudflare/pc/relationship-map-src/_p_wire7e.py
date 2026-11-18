BS = chr(92)
NL = BS + 'n'
# build_hub2.py
p = 'build_hub2.py'
s = open(p, encoding='utf-8').read()
s = s.replace("from newco_data7d import CO7D\n", "from newco_data7d import CO7D\nfrom newco_data7e import CO7E\n", 1)
s = s.replace("**CO7C, **CO7D, **CO8}", "**CO7C, **CO7D, **CO7E, **CO8}", 1)
s = s.replace("**__import__('newco_data7d').CO7D,", "**__import__('newco_data7d').CO7D, **__import__('newco_data7e').CO7E,", 1)
open(p, 'w', encoding='utf-8').write(s)
# build_mapco.py
p = 'build_mapco.py'
s = open(p, encoding='utf-8').read()
s = s.replace("CO_ALL.update(__import__('newco_data7d').CO7D)\n", "CO_ALL.update(__import__('newco_data7d').CO7D)\nCO_ALL.update(__import__('newco_data7e').CO7E)\n", 1)
open(p, 'w', encoding='utf-8').write(s)
# adds.py: OpenAI / Anthropicの図に、離れた人たちの会社を足す
p = 'adds.py'
s = open(p, encoding='utf-8').read()
a = "   O_('meta', 'Meta', 2025, 'パンが2025年に移った先。', '元の移籍先'),\n  ],"
assert a in s
s = s.replace(a, "   O_('meta', 'Meta', 2025, 'パンが2025年に移った先。', '元の移籍先'),\n"
  "   O_('periodic', 'Periodic Labs', 2025, '元OpenAIのVPリアム・フェダスらが設立し、2025年9月に約3億ドルのシードで表に出た、AIで科学の発見を自動化する会社。ダブルクリックで図を開きます。', '元VPが設立'),\n"
  "   O_('covariant', 'Covariant', 2017, 'OpenAIの元研究者ピーター・アビールらが2017年に創業した、ロボット向けAIの会社。2024年にAmazonが技術ライセンスと人材を獲得。ダブルクリックで図を開きます。', '元研究者が創業'),\n"
  "   O_('appliedcompute', 'Applied Compute', 2025, 'OpenAIの技術系の元社員3人が2025年に起こした、企業向けAIエージェントの会社。ダブルクリックで図を開きます。', '元社員が創業'),\n"
  "   O_('eureka', 'Eureka Labs', 2024, 'カルパシーが設立したAI教育企業。ダブルクリックで図を開きます。', 'カルパシーが設立'),\n  ],", 1)
a = "edges=\"['zoph','metz','schoenholz'].forEach(a=>E.push({a,b:'tml',k:'from'}));" + NL + "E.push({a:'pang',b:'meta',k:'from'});" + NL + "\"),"
assert a in s, 'openai edges'
s = s.replace(a, "edges=\"['zoph','metz','schoenholz'].forEach(a=>E.push({a,b:'tml',k:'from'}));" + NL + "E.push({a:'pang',b:'meta',k:'from'});" + NL +
  "E.push({a:'openai',b:'periodic',k:'link',label:'元VPが設立'});" + NL + "E.push({a:'openai',b:'covariant',k:'link',label:'元研究者が創業'});" + NL + "E.push({a:'openai',b:'appliedcompute',k:'link',label:'元社員が創業'});" + NL + "\"),", 1)
a = "   O_('deepmind', 'Google DeepMind', 2021, 'ジャンパーの出身元。', '出身元'),\n  ],"
assert a in s
s = s.replace(a, "   O_('deepmind', 'Google DeepMind', 2021, 'ジャンパーの出身元。', '出身元'),\n"
  "   O_('mirendil', 'Mirendil', 2025, 'Anthropicの元研究者2人(ベナム・ネイシャブール、ハーシュ・メータ)が2025年12月ごろに離れて起こした、科学研究のAIの会社。ダブルクリックで図を開きます。', '元研究者が設立'),\n"
  "   O_('humans', 'humans&', 2025, '元Anthropic研究者のアンディ・ペンらが2025年に作った会社。2026年1月に4.8億ドルのシードを発表。ダブルクリックで図を開きます。', '元研究者が共同創業'),\n  ],", 1)
a = "edges=\"E.push({a:'jumper',b:'deepmind',k:'from',since:2026});" + NL + "\"),"
assert a in s, 'anth edges'
s = s.replace(a, "edges=\"E.push({a:'jumper',b:'deepmind',k:'from',since:2026});" + NL + "E.push({a:'anthropic',b:'mirendil',k:'link',label:'元研究者が設立'});" + NL + "E.push({a:'anthropic',b:'humans',k:'link',label:'元研究者が共同創業'});" + NL + "\"),", 1)
a = "{'a': 'pang', 'b': 'meta', 'k': 'from'}],\n 'anthropic': [{'a': 'jumper', 'b': 'deepmind', 'k': 'from', 'since': 2026}],"
assert a in s, 'legacy edges'
s = s.replace(a, "{'a': 'pang', 'b': 'meta', 'k': 'from'},\n  {'a': 'openai', 'b': 'periodic', 'k': 'link', 'label': '元VPが設立'}, {'a': 'openai', 'b': 'covariant', 'k': 'link', 'label': '元研究者が創業'}, {'a': 'openai', 'b': 'appliedcompute', 'k': 'link', 'label': '元社員が創業'}],\n"
  " 'anthropic': [{'a': 'jumper', 'b': 'deepmind', 'k': 'from', 'since': 2026}, {'a': 'anthropic', 'b': 'mirendil', 'k': 'link', 'label': '元研究者が設立'}, {'a': 'anthropic', 'b': 'humans', 'k': 'link', 'label': '元研究者が共同創業'}],", 1)
open(p, 'w', encoding='utf-8').write(s)
# hub_template.html
p = 'hub_template.html'
t = open(p, encoding='utf-8').read()
note = '顔写真はWikipedia(Wikimedia Commons)掲載の画像です。写真がない人はイニシャル表示です。事実は、各項目の出典リンクの報道・Wikipediaに基づきます。報道どうしで食い違う数字は、食い違いのまま書き、確認できなかったこと(出資者・金額など)は載せていません。'
ent = ''
for key, name, mn in (('periodic', 'Periodic Labs', 2025), ('mirendil', 'Mirendil', 2025), ('humans', 'humans&', 2025), ('covariant', 'Covariant', 2017), ('appliedcompute', 'Applied Compute', 2025)):
    ent += "  %s:{name:'%s',min:%d,sub:1,note:'%s'},\n" % (key, name, mn, note)
k = "  instagram:{name:'Instagram'"
assert t.count(k) == 1
t = t.replace(k, ent + k, 1)
K = "const ALIAS={artifact:'artifact',"
assert t.count(K) == 1
t = t.replace(K, "const ALIAS={periodic:'periodic',mirendil:'mirendil',humans:'humans',covariant:'covariant',appliedcompute:'appliedcompute',artifact:'artifact',", 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
