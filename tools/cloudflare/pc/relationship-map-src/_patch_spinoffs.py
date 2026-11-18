BS = chr(92)
NL = BS + 'n'   # ファイルの中に書く「\n」(文字としてのバックスラッシュとn)
# ---- build_hub2.py: 新しい図を読み込み、Metaの図に人物・組織を足す ----
p = 'build_hub2.py'
s = open(p, encoding='utf-8').read()
s = s.replace("from newco_data7c import CO7C\n", "from newco_data7c import CO7C\nfrom newco_data7d import CO7D\n", 1)
s = s.replace("**CO7B, **CO7C, **CO8}", "**CO7B, **CO7C, **CO7D, **CO8}", 1)
s = s.replace("**__import__('newco_data7c').CO7C,", "**__import__('newco_data7c').CO7C, **__import__('newco_data7d').CO7D,", 1)
nodes = """ {'id': 'koum', 'name': 'ジャン・クーム', 'kind': 'p', 'from': 2014, 'to': 2018, 'desc': 'WhatsAppの共同創業者でCEO。2018年4月に退任を発表。Facebookとの間で、プライバシー、広告、収益化をめぐる衝突があったと報じられています。', 'role': '元WhatsApp CEO'},
 {'id': 'acton', 'name': 'ブライアン・アクトン', 'kind': 'p', 'from': 2014, 'to': 2017, 'desc': 'WhatsAppの共同創業者。2017年9月に退社し、のちSignal Foundationを共同で設立しました。', 'role': '元WhatsApp共同創業者'},
 {'id': 'luckey', 'name': 'パルマー・ラッキー', 'kind': 'p', 'from': 2014, 'to': 2017, 'desc': 'Oculus VRの創業者。2017年3月にFacebookを離れ、同年6月にAnduril Industriesを共同創業しました。', 'role': '元Oculus創業者'},
 {'id': 'oculus', 'name': 'Oculus VR', 'kind': 'o', 'from': 2014, 'desc': '2014年にFacebookが買収したVRの会社(報道では約20億ドル)。ダブルクリックで図を開きます。', 'role': '2014年に買収'},
 {'id': 'signal', 'name': 'Signal Foundation', 'kind': 'o', 'from': 2018, 'desc': 'アクトンが2018年に共同で設立した非営利団体(Signalアプリを運営)。', 'role': 'アクトンが設立'},
 {'id': 'anduril', 'name': 'Anduril Industries', 'kind': 'o', 'from': 2017, 'desc': 'ラッキーが2017年に共同創業した防衛技術の会社。', 'role': 'ラッキーが設立'},
"""
a = " {'id': 'vanguard', 'name': 'Vanguard'"
assert s.count(a) == 1
s = s.replace(a, nodes + a, 1)
edges = ("E.push({a:'koum',b:'whatsapp',k:'from',label:'共同創業'});" + NL + "E.push({a:'acton',b:'whatsapp',k:'from',label:'共同創業'});" + NL +
         "E.push({a:'luckey',b:'oculus',k:'from',label:'創業'});" + NL + "E.push({a:'meta',b:'oculus',k:'owns',label:'2014年に買収',since:2014});" + NL +
         "E.push({a:'acton',b:'signal',k:'moved'});" + NL + "E.push({a:'luckey',b:'anduril',k:'moved'});" + NL +
         "E.push({a:'koum',b:'meta',k:'conflict',label:'2018年に衝突(報道)',since:2018});" + NL +
         "E.push({a:'luckey',b:'meta',k:'conflict',label:'2017年に退社(経緯は報道)',since:2017});" + NL)
anchor = "E.push({a:'systrom',b:'zuckerberg',k:'conflict',label:'資源・独立性をめぐり対立(報道)',since:2017});" + NL
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + edges, 1)
s = s.replace("'systrom': 'Kevin Systrom', 'krieger': 'Mike Krieger', 'friedman'", "'systrom': 'Kevin Systrom', 'krieger': 'Mike Krieger', 'koum': 'Jan Koum', 'acton': 'Brian Acton', 'luckey': 'Palmer Luckey', 'friedman'", 1)
s = s.replace("'whatsapp': [['出典: Wikipedia(WhatsApp)', 'https://en.wikipedia.org/wiki/WhatsApp']]}",
              "'whatsapp': [['出典: Wikipedia(WhatsApp)', 'https://en.wikipedia.org/wiki/WhatsApp']],\n      'koum': [['出典: Wikipedia(Jan Koum)', 'https://en.wikipedia.org/wiki/Jan_Koum'], ['出典: Wikipedia(WhatsApp)', 'https://en.wikipedia.org/wiki/WhatsApp']],\n      'acton': [['出典: Wikipedia(Brian Acton)', 'https://en.wikipedia.org/wiki/Brian_Acton'], ['出典: Wikipedia(Signal Foundation)', 'https://en.wikipedia.org/wiki/Signal_Foundation']],\n      'luckey': [['出典: Wikipedia(Palmer Luckey)', 'https://en.wikipedia.org/wiki/Palmer_Luckey']],\n      'oculus': [['出典: Wikipedia(Oculus VR)', 'https://en.wikipedia.org/wiki/Oculus_VR']],\n      'signal': [['出典: Wikipedia(Signal Foundation)', 'https://en.wikipedia.org/wiki/Signal_Foundation']],\n      'anduril': [['出典: Wikipedia(Anduril Industries)', 'https://en.wikipedia.org/wiki/Anduril_Industries']]}", 1)
open(p, 'w', encoding='utf-8').write(s)
# ---- build_mapco.py ----
p = 'build_mapco.py'
s = open(p, encoding='utf-8').read()
s = s.replace("CO_ALL['vc_instagram'] = __import__('newco_data7c').CO7C['instagram']\n", "CO_ALL['vc_instagram'] = __import__('newco_data7c').CO7C['instagram']\nCO_ALL.update(__import__('newco_data7d').CO7D)\n", 1)
open(p, 'w', encoding='utf-8').write(s)
# ---- hub_template.html: 会社の一覧と別名 ----
p = 'hub_template.html'
t = open(p, encoding='utf-8').read()
note = '顔写真はWikipedia(Wikimedia Commons)掲載の画像です。写真がない人はイニシャル表示です。事実は、英語版Wikipedia(2026年11月取得)と、各項目の出典リンクに基づきます。確認できなかったこと(出資者・金額など)は載せていません。'
ent = ("  artifact:{name:'Artifact(Nokto)',min:2022,sub:1,note:'" + note + "'},\n"
       "  whatsapp:{name:'WhatsApp',min:2009,sub:1,note:'" + note + "買収額は報道に基づく概算です。'},\n"
       "  signal:{name:'Signal Foundation',min:2018,sub:1,note:'" + note + "設立日は資料により食い違います(2018年1月10日または2月21日)。'},\n"
       "  oculus:{name:'Oculus VR',min:2012,sub:1,note:'" + note + "買収額は約20億ドルと報じられていますが、ザッカーバーグは裁判で30億ドルと証言しており、食い違っています。退社の経緯は報道に基づき、Facebookは政治的な理由を否定しています。'},\n"
       "  amilabs:{name:'AMI Labs',min:2025,sub:1,note:'" + note + "共同創業の時期は、2025年11月の退社確認と12月の共同創業とで、資料により異なります。出資者は共同主導に含まれる会社で、主導した会社の区別は確認できていません。'},\n"
       "  eureka:{name:'Eureka Labs',min:2024,sub:1,note:'" + note + "出資者と調達額は確認できていません。'},\n")
k = "  instagram:{name:'Instagram'"
assert t.count(k) == 1
t = t.replace(k, ent + k, 1)
K = "const ALIAS={instagram:'instagram',openai:'openai',"
assert t.count(K) == 1
t = t.replace(K, "const ALIAS={artifact:'artifact',whatsapp:'whatsapp',signal:'signal',oculus:'oculus',ami:'amilabs',amilabs:'amilabs',eureka:'eureka',instagram:'instagram',openai:'openai',", 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
