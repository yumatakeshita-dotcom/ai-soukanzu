p = 'build_hub2.py'
b = open(p, encoding='utf-8').read()
old = "'friedman': 'natfriedman',"
assert b.count(old) == 1
b = b.replace(old, "'friedman': 'natfriedman', 'koum': 'jankoum', 'acton': 'brianacton',", 1)
open(p, 'w', encoding='utf-8').write(b)
p = 'newco_data7d.py'
s = open(p, encoding='utf-8').read()
old = "{'acton': 'brianacton'}, {'whatsapp': 'https://www.whatsapp.com'}"
assert old in s
s = s.replace(old, "{'acton': 'brianacton', 'koum': 'jankoum'}, {'whatsapp': 'https://www.whatsapp.com'}", 1)
open(p, 'w', encoding='utf-8').write(s)
# adds.py: OpenAIの図にAdeptを足す
p = 'adds.py'
a = open(p, encoding='utf-8').read()
k = "   O_('covariant', 'Covariant', 2017,"
assert a.count(k) == 1
a = a.replace(k, "   O_('adept', 'Adept', 2022, 'OpenAIの元VPデビッド・ルアンらが共同創業したAIエージェントの会社。2024年6月にAmazonが創業者5人を採用。ダブルクリックで図を開きます。', '元VPが創業'),\n" + k, 1)
k2 = "{'a': 'openai', 'b': 'covariant', 'k': 'link', 'label': '元研究者が創業'},"
assert a.count(k2) == 1
a = a.replace(k2, k2 + " {'a': 'openai', 'b': 'adept', 'k': 'link', 'label': '元VPが創業'},", 1)
k3 = "E.push({a:'openai',b:'covariant',k:'link',label:'元研究者が創業'});"
assert a.count(k3) == 1
a = a.replace(k3, k3 + "E.push({a:'openai',b:'adept',k:'link',label:'元VPが創業'});" , 1)
open(p, 'w', encoding='utf-8').write(a)
# template
p = 'hub_template.html'
t = open(p, encoding='utf-8').read()
note = '顔写真はWikipedia(Wikimedia Commons)掲載の画像です。写真がない人はイニシャル表示です。事実は、各項目の出典リンクの報道に基づきます。報道どうしで食い違う数字は、食い違いのまま書いています。'
k = "  instagram:{name:'Instagram'"
assert t.count(k) == 1
t = t.replace(k, "  adept:{name:'Adept',min:2022,sub:1,note:'" + note + "'},\n" + k, 1)
K = "const ALIAS={carelesspeople:'carelesspeople',"
assert t.count(K) == 1
t = t.replace(K, "const ALIAS={adept:'adept',carelesspeople:'carelesspeople',", 1)
open(p, 'w', encoding='utf-8').write(t)
# merge
p = '_merge_insta.py'
g = open(p, encoding='utf-8').read()
g = g.replace("'carelesspeople']", "'carelesspeople', 'adept']", 1)
g = g.replace("ADD = \"carelesspeople:'carelesspeople',", "ADD = \"adept:'adept',carelesspeople:'carelesspeople',", 1)
open(p, 'w', encoding='utf-8').write(g)
print('ok')
