import json, re
S = r'C:\Users\yumat\.claude\docs\rooms\relationship-map-src'
src = r'C:\Users\yumat\.claude\output\openai-relationship-map.html'
dst = r'C:\Users\yumat\.claude\output\anthropic-relationship-map.html'
res = json.load(open(S + r'\anth.json'))
bad = {'patil', 'rao', 'israel', 'smith', 'vora', 'clark', 'olah', 'brown', 'mccandlish', 'mann'}
PH = {k: v['img'] for k, v in res.items() if v.get('img') and k not in bad}
WIKI = {k: v['wiki'] for k, v in res.items() if v.get('wiki') and k not in bad}
WIKI = {k: v for k, v in WIKI.items() if k not in ('leike_x',)}
WIKI.update({
 'anthropic': 'https://en.wikipedia.org/wiki/Anthropic', 'openai': 'https://en.wikipedia.org/wiki/OpenAI',
 'google': 'https://en.wikipedia.org/wiki/Google', 'amazon': 'https://en.wikipedia.org/wiki/Amazon_(company)',
 'microsoft': 'https://en.wikipedia.org/wiki/Microsoft', 'nvidia': 'https://en.wikipedia.org/wiki/Nvidia',
 'coatue': 'https://en.wikipedia.org/wiki/Coatue_Management', 'gic': 'https://en.wikipedia.org/wiki/GIC_Private_Limited',
 'iconiq': 'https://en.wikipedia.org/wiki/ICONIQ_Capital', 'foundersfund': 'https://en.wikipedia.org/wiki/Founders_Fund',
 'sequoia': 'https://en.wikipedia.org/wiki/Sequoia_Capital', 'ftx': 'https://en.wikipedia.org/wiki/FTX',
 'tml': 'https://en.wikipedia.org/wiki/Thinking_Machines_Lab'})
EN = {'dario': 'Dario Amodei', 'daniela': 'Daniela Amodei', 'kaplan': 'Jared Kaplan', 'clark': 'Jack Clark', 'olah': 'Chris Olah',
 'brown': 'Tom Brown', 'mccandlish': 'Sam McCandlish', 'mann': 'Ben Mann', 'krieger': 'Mike Krieger', 'patil': 'Rahul Patil',
 'rao': 'Krishna Rao', 'vora': 'Ami Vora', 'leike': 'Jan Leike', 'schulman': 'John Schulman', 'kingma': 'Durk Kingma',
 'karnofsky': 'Holden Karnofsky', 'hastings': 'Reed Hastings', 'narasimhan': 'Vas Narasimhan', 'liddell': 'Chris Liddell',
 'tallinn': 'Jaan Tallinn', 'moskovitz': 'Dustin Moskovitz', 'schmidt': 'Eric Schmidt'}
X = {'clark': 'jackclarkSF', 'olah': 'ch402', 'brown': 'nottombrown', 'krieger': 'mikeyk', 'leike': 'janleike', 'schulman': 'johnschulman2',
 'kingma': 'dpkingma', 'hastings': 'reedhastings', 'schmidt': 'ericschmidt', 'tallinn': 'jaantallinn', 'moskovitz': 'moskov',
 'anthropic': 'AnthropicAI', 'openai': 'OpenAI', 'amazon': 'amazon', 'nvidia': 'nvidia', 'microsoft': 'Microsoft', 'google': 'Google',
 'tml': 'thinkymachines'}
WEB = {'anthropic': 'https://www.anthropic.com', 'openai': 'https://openai.com', 'google': 'https://www.google.com', 'amazon': 'https://www.amazon.com',
 'microsoft': 'https://www.microsoft.com', 'nvidia': 'https://www.nvidia.com', 'coatue': 'https://www.coatue.com', 'iconiq': 'https://www.iconiq.com',
 'foundersfund': 'https://foundersfund.com', 'sequoia': 'https://www.sequoiacap.com', 'tml': 'https://thinkingmachines.ai'}
LINKS = {
 'dario': [['エッセイ', 'https://www.darioamodei.com']],
 'olah': [['ブログ', 'https://colah.github.io']],
 'clark': [['Import AI(ニュースレター)', 'https://jack-clark.net']],
 'kingma': [['個人サイト', 'https://dpkingma.com']],
 'leike': [['Substack', 'https://aligned.substack.com']],
 'schulman': [['個人サイト', 'https://joschu.net'], ['GitHub', 'https://github.com/joschu']],
}
N = [
 {'id': 'anthropic', 'name': 'Anthropic', 'kind': 'c', 'from': 2021, 'desc': '2021年に元OpenAI勢が設立したAI企業(公益法人)。Claudeを開発。2026年10月26日にNasdaq上場(ティッカー「ANT」)を目指してS-1を提出したと報じられています。創業者のLLCが議決権の50.1%を持ち、Long-Term Benefit Trustが取締役の過半数を選びます。'},
 # 共同創業者
 {'id': 'dario', 'name': 'ダリオ・アモデイ', 'kind': 'p', 'from': 2021, 'desc': '共同創業者でCEO兼取締役。OpenAIで研究担当VPを務めたのち、2021年にAnthropicを設立しました。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'daniela', 'name': 'ダニエラ・アモデイ', 'kind': 'p', 'from': 2021, 'desc': '共同創業者で社長、取締役会議長。日々の運営を担当すると報じられています。', 'role': '社長 / 共同創業者', 'founder': 1},
 {'id': 'kaplan', 'name': 'ジャレッド・カプラン', 'kind': 'p', 'from': 2021, 'desc': '共同創業者。理論物理学者で、AIの「スケーリング則」の論文で知られます。', 'role': '共同創業者(研究)', 'founder': 1},
 {'id': 'clark', 'name': 'ジャック・クラーク', 'kind': 'p', 'from': 2021, 'desc': '共同創業者。元ジャーナリストでOpenAIの政策責任者。現在は公益(Public Benefit)担当と報じられています。', 'role': '共同創業者(政策)', 'founder': 1},
 {'id': 'olah', 'name': 'クリス・オラ', 'kind': 'p', 'from': 2021, 'desc': '共同創業者。モデルの内部を読み解く「解釈可能性」研究の第一人者です。', 'role': '共同創業者(解釈可能性)', 'founder': 1},
 {'id': 'brown', 'name': 'トム・ブラウン', 'kind': 'p', 'from': 2021, 'desc': '共同創業者。OpenAIでGPT-3の筆頭著者を務めました。', 'role': '共同創業者(計算基盤)', 'founder': 1},
 {'id': 'mccandlish', 'name': 'サム・マッキャンドリッシュ', 'kind': 'p', 'from': 2021, 'desc': '共同創業者。元CTOで、2025年から事前学習に集中するチーフアーキテクトと報じられています。', 'role': 'チーフアーキテクト / 共同創業者', 'founder': 1},
 {'id': 'mann', 'name': 'ベン・マン', 'kind': 'p', 'from': 2021, 'desc': '共同創業者。GPT-3の共著者。2026年にクリーガーと新部門Anthropic Labsを共同で率いると報じられています。', 'role': 'Anthropic Labs共同責任者 / 共同創業者', 'founder': 1},
 # 経営陣・研究
 {'id': 'rao', 'name': 'クリシュナ・ラオ', 'kind': 'p', 'from': 2022, 'desc': 'CFO。元Fanaticsの幹部。上場準備を含む財務を担当と報じられています。', 'role': 'CFO'},
 {'id': 'krieger', 'name': 'マイク・クリーガー', 'kind': 'p', 'from': 2024, 'desc': 'Instagram共同創業者。2024年にCPOとして入社し、のちAnthropic Labsの共同責任者に。', 'role': 'Anthropic Labs共同責任者'},
 {'id': 'patil', 'name': 'ラフル・パティル', 'kind': 'p', 'from': 2025, 'desc': '2025年10月に入社したCTO。元StripeのCTO。', 'role': 'CTO'},
 {'id': 'vora', 'name': 'アミ・ボーラ', 'kind': 'p', 'from': 2025, 'desc': 'CPO(最高製品責任者)。元WhatsAppのプロダクト担当VPと報じられています。', 'role': 'CPO'},
 {'id': 'leike', 'name': 'ヤン・ライケ', 'kind': 'p', 'from': 2024, 'desc': 'OpenAIを辞めた後、2024年にAnthropicのアラインメントサイエンス責任者に。', 'role': 'アラインメント責任者'},
 {'id': 'kingma', 'name': 'ダーク・キングマ', 'kind': 'p', 'from': 2024, 'desc': 'OpenAIの創業メンバーの一人。VAEやAdamの考案者として知られ、2024年に入社。', 'role': '研究者'},
 {'id': 'karnofsky', 'name': 'ホールデン・カーノフスキー', 'kind': 'p', 'from': 2025, 'desc': 'Open Philanthropyの共同創業者。2025年に入社したと報じられています。', 'role': '政策・安全の担当'},
 {'id': 'schulman', 'name': 'ジョン・シュルマン', 'kind': 'p', 'from': 2024, 'to': 2025, 'desc': 'OpenAI共同創業者。2024年8月にAnthropicへ移り、2025年2月に退社してThinking Machines Labへ。', 'role': '元研究者'},
 # 取締役
 {'id': 'hastings', 'name': 'リード・ヘイスティングス', 'kind': 'p', 'from': 2025, 'desc': 'Netflix共同創業者。2025年に取締役に就任。S-1ではLong-Term Benefit Trustが選ぶ取締役として名前が挙がったと報じられています。', 'role': '取締役'},
 {'id': 'narasimhan', 'name': 'バス・ナラシンハン', 'kind': 'p', 'from': 2026, 'desc': 'S-1で取締役として名前が挙がったと報じられています(製薬大手Novartis CEOとされます)。就任時期は確認できていません。', 'role': '取締役'},
 {'id': 'liddell', 'name': 'クリス・リデル', 'kind': 'p', 'from': 2026, 'desc': 'S-1で取締役として名前が挙がったと報じられています。就任時期は確認できていません。', 'role': '取締役'},
 # 出資者
 {'id': 'tallinn', 'name': 'ヤーン・タリン', 'kind': 'i', 'from': 2021, 'desc': 'Skype共同創業者。2021年のシリーズAを主導した初期の出資者。', 'role': '個人投資家'},
 {'id': 'moskovitz', 'name': 'ダスティン・モスコビッツ', 'kind': 'i', 'from': 2021, 'desc': 'Facebook共同創業者。初期の出資者の一人とされます。', 'role': '個人投資家'},
 {'id': 'schmidt', 'name': 'エリック・シュミット', 'kind': 'i', 'from': 2021, 'desc': '元Google CEO。初期の出資者の一人とされます。', 'role': '個人投資家'},
 {'id': 'ftx', 'name': 'FTX', 'kind': 'i', 'from': 2022, 'desc': '2022年にシリーズBで出資。のちに破綻し、保有分は売却されました。', 'role': '元出資者'},
 {'id': 'google', 'name': 'Google', 'kind': 'i', 'from': 2022, 'desc': '2025年の裁判資料で約14%を保有、上限は15%、議決権や取締役の権利はないとされます。2026年に最大100億ドルの出資意向と報じられています。', 'role': '約14%(2025年時点)'},
 {'id': 'amazon', 'name': 'Amazon', 'kind': 'i', 'from': 2023, 'desc': '2023年から出資し、累計約80億ドル。2026年に追加出資と報じられています。持ち分は非公表で、報道の数字はまちまちです。OpenAIにも出資しています。', 'role': '最大の戦略出資者'},
 {'id': 'microsoft', 'name': 'Microsoft', 'kind': 'i', 'from': 2025, 'desc': '2025年にAnthropicへの出資を発表と報じられています。OpenAIの最大の外部株主でもあります。', 'role': '戦略出資者'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2025, 'desc': '2025年にAnthropicへの出資を発表と報じられています。OpenAIにも出資しています。', 'role': '戦略出資者 + GPU供給'},
 {'id': 'coatue', 'name': 'Coatue', 'kind': 'i', 'from': 2026, 'desc': '2026年2月のシリーズG(300億ドル、評価額3,800億ドル)を、GICとともに主導。', 'role': 'VC・ヘッジファンド'},
 {'id': 'gic', 'name': 'GIC', 'kind': 'i', 'from': 2026, 'desc': 'シンガポールの政府系ファンド。2026年2月のシリーズGを主導。', 'role': '政府系ファンド'},
 {'id': 'iconiq', 'name': 'ICONIQ', 'kind': 'i', 'from': 2026, 'desc': 'シリーズGの共同主導者の一社。', 'role': 'VC'},
 {'id': 'foundersfund', 'name': 'Founders Fund', 'kind': 'i', 'from': 2026, 'desc': 'ピーター・ティールのVC。シリーズGの共同主導者の一社。', 'role': 'VC'},
 {'id': 'sequoia', 'name': 'Sequoia Capital', 'kind': 'i', 'from': 2026, 'desc': '2026年5月のシリーズH(650億ドル、評価額9,650億ドル)を、Altimeter、Dragoneer、Greenoaksとともに主導。', 'role': 'VC'},
 {'id': 'altimeter', 'name': 'Altimeter', 'kind': 'i', 'from': 2026, 'desc': 'シリーズHの主導者の一社。', 'role': '投資会社'},
 {'id': 'dragoneer', 'name': 'Dragoneer', 'kind': 'i', 'from': 2026, 'desc': 'シリーズGの共同主導、シリーズHの主導。', 'role': '投資会社'},
 # 関連組織
 {'id': 'ltbt', 'name': 'Long-Term Benefit Trust', 'kind': 'o', 'from': 2023, 'desc': 'Anthropic独自の信託。特別株(Class T)で取締役の過半数を選び、事業と公益のバランスを守る仕組みと説明されています。', 'role': 'ガバナンス'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2021, 'desc': '創業者の多くが前に在籍した会社。ライケ、シュルマン、キングマも在籍していました。', 'role': '出身元'},
 {'id': 'tml', 'name': 'Thinking Machines Lab', 'kind': 'o', 'from': 2025, 'desc': 'ムラティが設立した企業。シュルマンがAnthropicを経て参加。', 'role': 'シュルマンの移籍先'},
]
CAREER = {
 'dario': [['2016', 'OpenAIに入社、研究担当VP'], ['2020', 'OpenAIを退社'], ['2021', 'Anthropicを設立、CEO']],
 'daniela': [['2018', 'OpenAIに入社、安全・政策担当VP'], ['2021', 'Anthropicを共同設立、社長']],
 'kaplan': [['〜', 'ジョンズ・ホプキンス大学の理論物理学者'], ['2020', 'スケーリング則の論文を発表'], ['2021', 'Anthropicを共同設立']],
 'clark': [['〜', '元ジャーナリスト(Bloomberg、The Register)'], ['2018', 'OpenAIの政策責任者'], ['2021', 'Anthropicを共同設立']],
 'olah': [['〜', 'Google Brainの研究者、OpenAIの解釈可能性チーム'], ['2021', 'Anthropicを共同設立']],
 'brown': [['2020', 'OpenAIでGPT-3の筆頭著者'], ['2021', 'Anthropicを共同設立']],
 'krieger': [['2010', 'Instagramを共同創業'], ['2024', 'Anthropicに入社、CPO'], ['2026', 'Anthropic Labsの共同責任者に']],
 'leike': [['2021', 'OpenAIのアラインメント責任者'], ['2024', '5月にOpenAIを退社、Anthropicへ']],
 'schulman': [['2015', 'OpenAIを共同創業'], ['2024', '8月にAnthropicへ'], ['2025', '2月に退社、Thinking Machines Labへ']],
 'kingma': [['2015', 'OpenAIの創業メンバー'], ['2024', 'Anthropicに入社']],
 'karnofsky': [['2007', 'GiveWellを共同創業'], ['〜', 'Open Philanthropyを共同創業'], ['2025', 'Anthropicに入社と報道']],
 'hastings': [['1997', 'Netflixを共同創業'], ['2025', 'Anthropicの取締役に就任']],
 'tallinn': [['2003', 'Skypeを共同創業'], ['2021', 'AnthropicのシリーズAを主導']],
 'schmidt': [['2001', 'Google CEO(〜2011)'], ['2021', 'Anthropicに出資したとされる']],
}
edges = (
 "const E = [];\n"
 "N.forEach(n=>{\n"
 "  if(n.kind==='p') E.push({a:n.id,b:'anthropic',k:'member'});\n"
 "  if(n.kind==='i') E.push({a:n.id,b:'anthropic',k:'invest'});\n"
 "});\n"
 "['dario','daniela','kaplan','clark','olah','brown','mccandlish','mann','leike','schulman','kingma'].forEach(a=>E.push({a,b:'openai',k:'from'}));\n"
 "E.push({a:'schulman',b:'tml',k:'moved'});\n"
 "E.push({a:'ltbt',b:'anthropic',k:'govern',label:'取締役の過半数を選任'});\n"
 "['amazon','nvidia','microsoft'].forEach(a=>E.push({a,b:'openai',k:'invest2'}));\n"
 "E.push({a:'hastings',b:'ltbt',k:'govern'});\n\n"
)
dump = lambda o: json.dumps(o, ensure_ascii=False)
data = ("const N = %s;\nconst PH=%s;\nconst WIKI=%s;\nconst EN=%s;\nconst X=%s;\nconst WEB=%s;\nconst CAREER=%s;\nconst LINKS=%s;\n"
        % tuple(dump(o) for o in (N, PH, WIKI, EN, X, WEB, CAREER, LINKS)))
data += ("const li=n=>`https://www.linkedin.com/search/results/people/?keywords=${encodeURIComponent(EN[n.id]||n.name)}`;\n"
         "const xs=n=>`https://x.com/search?q=${encodeURIComponent(EN[n.id]||n.name)}&f=user`;\n")
h = open(src, encoding='utf-8').read()
a = h.index('const N = [')
b = h.index('const byId')
h = h[:a] + data + edges + h[b:]
# 個別のOpenAI向け特例を除去
h = '\n'.join(l for l in h.split('\n') if "e.a==='schulman'" not in l and "e.a==='musk'" not in l and "e.b==='sutskever'" not in l)
rep = [
 ('<title>OpenAI 相関図</title>', '<title>Anthropic 相関図</title>'),
 ('OpenAI 相関図 2015 → 2026', 'Anthropic 相関図 2021 → 2026'),
 ('min="2015"', 'min="2021"'),
 ('year=2015;slider', 'year=2021;slider'),
 ('aria-label="OpenAIの人物・投資家の相関図"', 'aria-label="Anthropicの人物・投資家の相関図"'),
 ('byId.openai.x=cx;byId.openai.y=cy;', 'byId.anthropic.x=cx;byId.anthropic.y=cy;'),
 ("n.id==='openai'", "n.id==='anthropic'"),
 ("o.id==='openai'", "o.id==='anthropic'"),
 ('退職後の行き先', '出身元・退職後の行き先'),
 ('<h2>${year}年のOpenAI</h2>', '<h2>${year}年のAnthropic</h2>'),
 ('OpenAI在籍', 'Anthropic在籍'),
 ("if(e.k==='moved'){col='var(--left)';dash='6 4'}", "if(e.k==='moved'||e.k==='from'){col='var(--left)';dash='6 4'}\n    if(e.k==='govern'){col='var(--org)';dash='2 3'}"),
 ("{moved:e.a===id?'行き先':'出身',", "{from:e.a===id?'出身元':'出身者',govern:'信託',moved:e.a===id?'行き先':'出身',"),
]
for o, n in rep:
    assert o in h, o
    h = h.replace(o, n)
# 在籍中の人のfrom edgeはmember edgeが退職済みの時だけ点線になるので、そのままでよい
h = re.sub(r'<p class="note">顔写真は.*?</p>',
 '<p class="note">顔写真はWikipedia(Wikimedia Commons)掲載の画像です。写真がない人はイニシャル表示です。上場申請(2026年10月26日)、出資額・評価額、役員の肩書は二次報道に基づきます。持ち分の比率は公式資料で確認できていないため、数字は載せていません。X(旧Twitter)は公開アカウント、LinkedInは検索リンクです。<br>OpenAIの相関図: <a href="https://claude.ai/artifact/UnEAdLq6bVyWTwCWFBY4k6" target="_blank" rel="noopener">こちら</a></p>', h, flags=re.S)
h = h.replace('創業メンバー、退職者、現役幹部、投資家のつながりを年ごとに見られます。', '創業者、経営陣、取締役、投資家のつながりを年ごとに見られます。')
open(dst, 'w', encoding='utf-8').write(h)
print(len(h), len(PH), sorted(PH))
