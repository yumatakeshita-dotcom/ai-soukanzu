p = 'build_hub2.py'
s = open(p, encoding='utf-8').read()
n0 = len(s)
s = s.replace("from newco_data7b import CO7B\n", "from newco_data7b import CO7B\nfrom newco_data7c import CO7C\n", 1)
s = s.replace("**CO7, **CO7B, **CO8}", "**CO7, **CO7B, **CO7C, **CO8}", 1)
s = s.replace("__import__('newco_data7b').CO7B,", "__import__('newco_data7b').CO7B, **__import__('newco_data7c').CO7C,", 1)
nodes = """ {'id': 'instagram', 'name': 'Instagram', 'kind': 'o', 'from': 2012, 'desc': '2012年にFacebookが買収した写真・動画SNS(報道では約10億ドル)。創業者のシストロムとクリーガーは2018年に退任しました。ダブルクリックで、Instagramの図を開きます。', 'role': '2012年に買収'},
 {'id': 'systrom', 'name': 'ケビン・シストロム', 'kind': 'p', 'from': 2012, 'to': 2018, 'desc': 'Instagramの共同創業者でCEO。買収後もInstagramを率い、2018年9月に退任しました。', 'role': '元Instagram CEO'},
 {'id': 'krieger', 'name': 'マイク・クリーガー', 'kind': 'p', 'from': 2012, 'to': 2018, 'desc': 'Instagramの共同創業者でCTO。2018年9月に退任し、2024年にAnthropicへ入社しました。', 'role': '元Instagram CTO'},
 {'id': 'whatsapp', 'name': 'WhatsApp', 'kind': 'o', 'from': 2014, 'desc': '2014年にFacebookが買収したメッセージアプリ(報道では約190億ドル)。', 'role': '2014年に買収'},
"""
s = s.replace(" {'id': 'vanguard', 'name': 'Vanguard'", nodes + " {'id': 'vanguard', 'name': 'Vanguard'", 1)
edges = ("E.push({a:'meta',b:'instagram',k:'owns',label:'2012年に買収',since:2012});\\n"
         "E.push({a:'meta',b:'whatsapp',k:'owns',label:'2014年に買収',since:2014});\\n"
         "E.push({a:'systrom',b:'instagram',k:'from',label:'共同創業'});\\n"
         "E.push({a:'krieger',b:'instagram',k:'from',label:'共同創業'});\\n"
         "E.push({a:'mosseri',b:'instagram',k:'link',label:'責任者'});\\n"
         "E.push({a:'zuckerberg',b:'instagram',k:'link',label:'買収を主導',since:2012});\\n")
anchor = ' "E.push({a:\'meta\',b:\'scale\',k:\'invest2\',label:\'約143億ドル出資\'});\\n"\n'
assert anchor in s
s = s.replace(anchor, ' "' + edges + '"\n' + anchor, 1)
s = s.replace("'friedman': 'Nat Friedman', 'zhao'", "'systrom': 'Kevin Systrom', 'krieger': 'Mike Krieger', 'friedman': 'Nat Friedman', 'zhao'", 1)
open(p, 'w', encoding='utf-8').write(s)
t = open('hub_template.html', encoding='utf-8').read()
note = "顔写真はWikipedia(Wikimedia Commons)掲載の画像です。写真がない人はイニシャル表示です。買収額(約10億ドル)と出資者(2010〜2012年の各ラウンド)は報道に基づき、正確な持ち分は公開されていません。2018年の創業者の退任は本人の発表によります。"
t = t.replace("  melcoin:{name:'メルコイン'", "  instagram:{name:'Instagram',min:2010,sub:1,note:'" + note + "'},\n  melcoin:{name:'メルコイン'", 1)
t = t.replace("const ALIAS={openai:'openai',", "const ALIAS={instagram:'instagram',openai:'openai',", 1)
open('hub_template.html', 'w', encoding='utf-8').write(t)
print('ok', len(s) - n0)
