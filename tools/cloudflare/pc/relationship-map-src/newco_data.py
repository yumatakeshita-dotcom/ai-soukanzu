# 8社の会社データ。作りは build_hub2.py の xAI・Meta と同じ。
def mk(N, edges, EN, X, WEB, WIKI, CAREER, LINKS, center):
    return dict(N=N, edges=edges, EN=EN, X=X, WEB=WEB, WIKI=WIKI, CAREER=CAREER, LINKS=LINKS, center=center)

def std(center):
    return ("const E = [];\nN.forEach(n=>{\n  if(n.kind==='p') E.push({a:n.id,b:'%s',k:'member'});\n  if(n.kind==='i') E.push({a:n.id,b:'%s',k:'invest'});\n});\n" % (center, center))

def wp(*t):
    return {k: 'https://en.wikipedia.org/wiki/' + v for k, v in t}

CO = {}

# ---------------- Thinking Machines Lab ----------------
N = [
 {'id': 'tml', 'name': 'Thinking Machines Lab', 'kind': 'c', 'from': 2025, 'desc': '2025年2月に、元OpenAI CTOのムラティが設立したAI企業。確認できる最新の資金調達は2025年の約20億ドル(a16z主導、評価額は約120億ドル)です。共同創業者の退社が相次いでいると報じられています。'},
 {'id': 'murati', 'name': 'ミラ・ムラティ', 'kind': 'p', 'from': 2025, 'desc': '創業者でCEO。OpenAIでCTOを務めたのち、2024年9月に退社しました。', 'role': 'CEO / 創業者', 'founder': 1},
 {'id': 'schulman', 'name': 'ジョン・シュルマン', 'kind': 'p', 'from': 2025, 'desc': '共同創業者でチーフサイエンティスト。OpenAI、Anthropicを経て参加しました。', 'role': 'チーフサイエンティスト', 'founder': 1},
 {'id': 'weng', 'name': 'リリアン・ウェン', 'kind': 'p', 'from': 2025, 'desc': '共同創業者。OpenAIで安全システムを率いた研究者で、ブログ「Lil\'Log」でも知られます。', 'role': '共同創業者', 'founder': 1},
 {'id': 'zoph', 'name': 'バレット・ゾフ', 'kind': 'p', 'from': 2025, 'to': 2026, 'desc': '共同創業者でCTOだった人物。2026年1月に退社してOpenAIへ戻ったと報じられています。退社の経緯は報道により食い違います。', 'role': '元CTO', 'founder': 1},
 {'id': 'metz', 'name': 'ルーク・メッツ', 'kind': 'p', 'from': 2025, 'to': 2026, 'desc': '共同創業者。2026年1月にOpenAIへ戻ったと報じられています。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'tulloch', 'name': 'アンドリュー・タロック', 'kind': 'p', 'from': 2025, 'to': 2025, 'desc': '共同創業者。2025年10〜11月にMetaへ移ったと報じられています。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'schoenholz', 'name': 'サム・ショーンホルツ', 'kind': 'p', 'from': 2025, 'to': 2026, 'desc': '研究者。2026年1月にOpenAIへ戻ったと報じられています。', 'role': '元研究者'},
 {'id': 'chintala', 'name': 'スーミス・チンタラ', 'kind': 'p', 'from': 2026, 'desc': 'PyTorchの共同開発者。ゾフの退社後にCTOに就任と報じられています。', 'role': 'CTO'},
 {'id': 'a16z', 'name': 'Andreessen Horowitz', 'kind': 'i', 'from': 2025, 'desc': '2025年のシード(約20億ドル)を主導したと報じられています。', 'role': 'VC'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2025, 'desc': '2025年のシードの出資者として報じられています。', 'role': '出資 + GPU供給'},
 {'id': 'cisco', 'name': 'Cisco', 'kind': 'i', 'from': 2025, 'desc': '2025年のシードの出資者として報じられています。', 'role': '戦略出資者'},
 {'id': 'accel', 'name': 'Accel', 'kind': 'i', 'from': 2025, 'desc': 'シードの出資者として報じられています。2026年に新たな増資を主導する交渉との報道もあります(未確認)。', 'role': 'VC'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2025, 'desc': 'ムラティ、ゾフ、メッツ、ウェンらの出身元。2026年にはゾフらが戻ったと報じられています。', 'role': '出身元・戻り先'},
 {'id': 'meta', 'name': 'Meta', 'kind': 'o', 'from': 2025, 'desc': 'タロックの移籍先。チンタラの出身元でもあります。', 'role': '移籍先・出身元'},
 {'id': 'anthropic', 'name': 'Anthropic', 'kind': 'o', 'from': 2025, 'desc': 'シュルマンが、OpenAIからここを経て参加しました。', 'role': 'シュルマンの経由先'},
]
E = (std('tml') +
 "['murati','schulman','weng','zoph','metz','tulloch'].forEach(a=>E.push({a,b:'openai',k:'from'}));\n"
 "E.push({a:'schulman',b:'anthropic',k:'from'});\n"
 "['zoph','metz','schoenholz'].forEach(a=>E.push({a,b:'openai',k:'moved'}));\n"
 "E.push({a:'tulloch',b:'meta',k:'moved'});\n"
 "E.push({a:'chintala',b:'meta',k:'from'});\n\n")
CO['tml'] = mk(N, E,
 {'murati': 'Mira Murati', 'schulman': 'John Schulman', 'weng': 'Lilian Weng', 'zoph': 'Barret Zoph', 'metz': 'Luke Metz', 'tulloch': 'Andrew Tulloch', 'schoenholz': 'Sam Schoenholz', 'chintala': 'Soumith Chintala'},
 {'murati': 'miramurati', 'schulman': 'johnschulman2', 'weng': 'lilianweng', 'zoph': 'barret_zoph', 'chintala': 'soumithchintala', 'tml': 'thinkymachines', 'nvidia': 'nvidia', 'cisco': 'Cisco'},
 {'tml': 'https://thinkingmachines.ai', 'nvidia': 'https://www.nvidia.com', 'a16z': 'https://a16z.com'},
 wp(('tml', 'Thinking_Machines_Lab'), ('nvidia', 'Nvidia'), ('a16z', 'Andreessen_Horowitz'), ('cisco', 'Cisco'), ('accel', 'Accel_(company)'), ('openai', 'OpenAI'), ('meta', 'Meta_Platforms'), ('anthropic', 'Anthropic')),
 {'murati': [['2018', 'OpenAIに入社'], ['2022', 'CTOとしてChatGPT公開を主導'], ['2024', '9月に退社'], ['2025', '2月にThinking Machines Labを設立']],
  'schulman': [['2015', 'OpenAIを共同創業'], ['2024', '8月にAnthropicへ'], ['2025', '2月にThinking Machines Labへ']],
  'weng': [['〜', 'OpenAIで安全システムを率いる'], ['2025', 'Thinking Machines Labの共同創業者に']]},
 {'weng': [['ブログ(Lil\'Log)', 'https://lilianweng.github.io']], 'schulman': [['個人サイト', 'https://joschu.net'], ['GitHub', 'https://github.com/joschu']]},
 'tml')

# ---------------- SSI ----------------
N = [
 {'id': 'ssi', 'name': 'Safe Superintelligence', 'kind': 'c', 'from': 2024, 'desc': '2024年6月にスツケバーらが設立した、安全な超知能の開発だけを目指す会社。拠点はパロアルトとテルアビブ。Metaが買収を持ちかけて断られたと報じられています。'},
 {'id': 'sutskever', 'name': 'イリヤ・スツケバー', 'kind': 'p', 'from': 2024, 'desc': '共同創業者。グロスの退社後にCEOを引き継ぎました。OpenAIの元チーフサイエンティスト。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'levy', 'name': 'ダニエル・レヴィ', 'kind': 'p', 'from': 2024, 'desc': '共同創業者で社長。元OpenAIの研究者です。', 'role': '社長 / 共同創業者', 'founder': 1},
 {'id': 'gross', 'name': 'ダニエル・グロス', 'kind': 'p', 'from': 2024, 'to': 2025, 'desc': '共同創業者。2025年半ばに退き、Metaに移ったと報じられています。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'sequoia', 'name': 'Sequoia Capital', 'kind': 'i', 'from': 2024, 'desc': '2024年の最初の資金調達(約10億ドル)に参加と報じられています。', 'role': 'VC'},
 {'id': 'a16z', 'name': 'Andreessen Horowitz', 'kind': 'i', 'from': 2024, 'desc': '2024年の最初の資金調達に参加と報じられています。', 'role': 'VC'},
 {'id': 'dst', 'name': 'DST Global', 'kind': 'i', 'from': 2024, 'desc': '2024年の最初の資金調達に参加と報じられています。', 'role': '投資会社'},
 {'id': 'friedman', 'name': 'ナット・フリードマン', 'kind': 'i', 'from': 2024, 'desc': 'グロスと運営する投資会社NFDGを通じて出資と報じられています。2025年にMetaへ。', 'role': '個人投資家'},
 {'id': 'greenoaks', 'name': 'Greenoaks', 'kind': 'i', 'from': 2025, 'desc': '2025年の増資(評価額約320億ドル)を主導と報じられています。', 'role': '投資会社'},
 {'id': 'alphabet', 'name': 'Google', 'kind': 'i', 'from': 2025, 'desc': '2025年の増資に参加と報じられています。', 'role': '戦略出資者'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2025, 'desc': '2025年の増資に参加と報じられています。', 'role': '出資 + GPU供給'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2024, 'desc': 'スツケバーとレヴィの出身元。', 'role': '出身元'},
 {'id': 'meta', 'name': 'Meta', 'kind': 'o', 'from': 2025, 'desc': 'グロスの移籍先。SSIの買収を打診して断られたと報じられています。', 'role': '移籍先'},
]
E = (std('ssi') + "['sutskever','levy'].forEach(a=>E.push({a,b:'openai',k:'from'}));\nE.push({a:'gross',b:'meta',k:'moved'});\nE.push({a:'meta',b:'ssi',k:'conflict',label:'買収を打診(報道)',since:2025});\n\n")
CO['ssi'] = mk(N, E,
 {'sutskever': 'Ilya Sutskever', 'levy': 'Daniel Levy', 'gross': 'Daniel Gross', 'friedman': 'Nat Friedman'},
 {'sutskever': 'ilyasut', 'friedman': 'natfriedman', 'gross': 'danielgross', 'ssi': 'ssi', 'nvidia': 'nvidia'},
 {'ssi': 'https://ssi.inc', 'nvidia': 'https://www.nvidia.com', 'a16z': 'https://a16z.com', 'sequoia': 'https://www.sequoiacap.com'},
 wp(('ssi', 'Safe_Superintelligence_Inc.'), ('nvidia', 'Nvidia'), ('a16z', 'Andreessen_Horowitz'), ('sequoia', 'Sequoia_Capital'), ('dst', 'DST_Global'), ('alphabet', 'Google'), ('openai', 'OpenAI'), ('meta', 'Meta_Platforms')),
 {'sutskever': [['2015', 'OpenAIを共同創業、のちチーフサイエンティスト'], ['2024', '5月にOpenAIを退社、6月にSSIを設立']],
  'gross': [['2024', 'SSIを共同創業'], ['2025', 'SSIを退き、Metaへ移ったと報道']]},
 {}, 'ssi')

# ---------------- Google DeepMind ----------------
N = [
 {'id': 'deepmind', 'name': 'Google DeepMind', 'kind': 'c', 'from': 2010, 'desc': '2010年にロンドンで設立され、2014年にGoogleが買収。2023年にGoogle Brainと統合。2026年8月にハサビスが日々の運営から退き、カブクチュオグルが率いると報じられています。'},
 {'id': 'hassabis', 'name': 'デミス・ハサビス', 'kind': 'p', 'from': 2010, 'desc': '共同創業者。2024年にAlphaFoldでノーベル化学賞。2026年8月に日々の運営から退き、DeepMindの会長兼Alphabetのチーフサイエンティストになったと報じられています。Isomorphic Labsは引き続き率います。', 'role': '共同創業者 / 会長', 'founder': 1},
 {'id': 'legg', 'name': 'シェーン・レッグ', 'kind': 'p', 'from': 2010, 'desc': '共同創業者でチーフAGIサイエンティスト。「AGI」という言葉を広めた一人です。', 'role': '共同創業者', 'founder': 1},
 {'id': 'suleyman', 'name': 'ムスタファ・スレイマン', 'kind': 'p', 'from': 2010, 'to': 2019, 'desc': '共同創業者。2019年にGoogleへ移り、のちInflection AIを設立。2024年からMicrosoft AIを率います。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'kavukcuoglu', 'name': 'コライ・カブクチュオグル', 'kind': 'p', 'from': 2012, 'desc': '2026年8月にDeepMindを率いるSVPになったと報じられています。ピチャイCEOの直属です。', 'role': 'SVP', },
 {'id': 'vinyals', 'name': 'オリオール・ビニャルズ', 'kind': 'p', 'from': 2016, 'desc': '研究担当VP。Geminiを率いる一人。AlphaStarの責任者としても知られます。', 'role': '研究担当VP'},
 {'id': 'dean', 'name': 'ジェフ・ディーン', 'kind': 'p', 'from': 2023, 'to': 2026, 'desc': 'Googleの伝説的エンジニア。27年在籍し、2026年にDiscovery Loopを立ち上げるため退社と報じられています。', 'role': '元チーフサイエンティスト'},
 {'id': 'jumper', 'name': 'ジョン・ジャンパー', 'kind': 'p', 'from': 2017, 'to': 2026, 'desc': 'AlphaFoldを開発し、2024年にハサビスとノーベル化学賞。2026年6月にAnthropicへ移ったと報じられています。', 'role': '元研究者'},
 {'id': 'hinton', 'name': 'ジェフリー・ヒントン', 'kind': 'p', 'from': 2013, 'to': 2023, 'desc': 'ディープラーニングの父の一人。2013年にGoogleに加わり、2023年にAIのリスクを語るため退社。2024年ノーベル物理学賞。', 'role': '元Google研究者'},
 {'id': 'pichai', 'name': 'サンダー・ピチャイ', 'kind': 'p', 'from': 2015, 'desc': 'GoogleとAlphabetのCEO。DeepMindの上司にあたります。', 'role': 'Google / Alphabet CEO'},
 {'id': 'thiel', 'name': 'ピーター・ティール', 'kind': 'i', 'from': 2010, 'desc': 'Founders Fundを通じて、設立初期に出資したとされます。', 'role': '初期の出資者'},
 {'id': 'musk', 'name': 'イーロン・マスク', 'kind': 'i', 'from': 2012, 'desc': '初期の出資者の一人とされます。のちにOpenAIの共同創業へ。', 'role': '初期の出資者'},
 {'id': 'tallinn', 'name': 'ヤーン・タリン', 'kind': 'i', 'from': 2012, 'desc': 'Skype共同創業者。初期の出資者の一人とされます。', 'role': '初期の出資者'},
 {'id': 'alphabet', 'name': 'Alphabet', 'kind': 'o', 'from': 2014, 'desc': 'Googleの親会社。2014年にDeepMindを買収しました。', 'role': '親会社'},
 {'id': 'isomorphic', 'name': 'Isomorphic Labs', 'kind': 'o', 'from': 2021, 'desc': 'ハサビスが2021年に設立した、AI創薬の会社。', 'role': 'ハサビスが設立'},
 {'id': 'inflection', 'name': 'Inflection AI', 'kind': 'o', 'from': 2022, 'desc': 'スレイマンが2022年にホフマンらと設立。2024年にMicrosoftが人材と技術の権利を獲得。', 'role': 'スレイマンが設立'},
 {'id': 'microsoft', 'name': 'Microsoft', 'kind': 'o', 'from': 2024, 'desc': 'スレイマンの移籍先。', 'role': '移籍先'},
 {'id': 'anthropic', 'name': 'Anthropic', 'kind': 'o', 'from': 2026, 'desc': 'ジャンパーの移籍先と報じられています。', 'role': '移籍先'},
 {'id': 'discovery', 'name': 'Discovery Loop', 'kind': 'o', 'from': 2026, 'desc': 'ディーンが立ち上げる新会社と報じられています。', 'role': 'ディーンが設立'},
]
E = (std('deepmind') +
 "E.push({a:'alphabet',b:'deepmind',k:'owns',label:'2014年に買収'});\n"
 "E.push({a:'hassabis',b:'isomorphic',k:'link',label:'設立'});\n"
 "E.push({a:'suleyman',b:'inflection',k:'link',label:'設立',since:2022});\n"
 "E.push({a:'suleyman',b:'microsoft',k:'moved'});\n"
 "E.push({a:'suleyman',b:'inflection',k:'moved'});\n"
 "E.push({a:'jumper',b:'anthropic',k:'moved'});\n"
 "E.push({a:'dean',b:'discovery',k:'moved'});\n"
 "E.push({a:'pichai',b:'alphabet',k:'link'});\n\n")
CO['gdm'] = mk(N, E,
 {'hassabis': 'Demis Hassabis', 'legg': 'Shane Legg', 'suleyman': 'Mustafa Suleyman', 'kavukcuoglu': 'Koray Kavukcuoglu', 'vinyals': 'Oriol Vinyals', 'dean': 'Jeff Dean',
  'jumper': 'John Jumper', 'hinton': 'Geoffrey Hinton', 'pichai': 'Sundar Pichai', 'thiel': 'Peter Thiel', 'musk': 'Elon Musk', 'tallinn': 'Jaan Tallinn'},
 {'hassabis': 'demishassabis', 'legg': 'ShaneLegg', 'suleyman': 'mustafasuleyman', 'kavukcuoglu': 'koraykv', 'vinyals': 'OriolVinyalsML', 'dean': 'JeffDean', 'pichai': 'sundarpichai',
  'deepmind': 'GoogleDeepMind', 'musk': 'elonmusk', 'tallinn': 'jaantallinn'},
 {'deepmind': 'https://deepmind.google', 'alphabet': 'https://abc.xyz', 'isomorphic': 'https://www.isomorphiclabs.com'},
 wp(('deepmind', 'Google_DeepMind'), ('alphabet', 'Alphabet_Inc.'), ('isomorphic', 'Isomorphic_Labs'), ('inflection', 'Inflection_AI'), ('microsoft', 'Microsoft'), ('anthropic', 'Anthropic'), ('discovery', 'Jeff_Dean')),
 {'hassabis': [['1990年代', 'チェスの天才少年、ゲーム開発者に'], ['2010', 'DeepMindを共同創業'], ['2014', 'Googleに買収される'], ['2024', 'ノーベル化学賞(AlphaFold)'], ['2026', '8月に日々の運営から退き会長に(報道)']],
  'hinton': [['2013', 'Googleに参加'], ['2023', '退社してAIのリスクを発信'], ['2024', 'ノーベル物理学賞']]},
 {}, 'deepmind')

# ---------------- Microsoft ----------------
N = [
 {'id': 'msft', 'name': 'Microsoft', 'kind': 'c', 'from': 2019, 'desc': 'OpenAIの最大の外部株主(2025年10月の再編後は約27%、2026年6月末で約25%と報じられています)。Anthropicにも出資し、自社でもMAIモデルを開発しています。'},
 {'id': 'nadella', 'name': 'サティア・ナデラ', 'kind': 'p', 'from': 2014, 'desc': 'CEO。2019年にOpenAIへ最初の10億ドルを出資する提携を主導しました。', 'role': 'CEO / 会長'},
 {'id': 'gates', 'name': 'ビル・ゲイツ', 'kind': 'p', 'from': 1975, 'desc': '共同創業者。ナデラにCEOを譲り、現在は慈善活動が中心です。', 'role': '共同創業者', 'founder': 1},
 {'id': 'smith', 'name': 'ブラッド・スミス', 'kind': 'p', 'from': 2015, 'desc': '副会長兼社長。法務・渉外を率い、OpenAIとの提携交渉にも関わります。', 'role': '副会長 / 社長'},
 {'id': 'scott', 'name': 'ケビン・スコット', 'kind': 'p', 'from': 2017, 'desc': 'CTO。OpenAIとの戦略的な関係を担う人物として報じられています。', 'role': 'CTO'},
 {'id': 'suleyman', 'name': 'ムスタファ・スレイマン', 'kind': 'p', 'from': 2024, 'desc': 'Microsoft AIのCEO。2026年3月の再編で、Copilotから離れ、モデル開発と超知能に集中する体制になったと報じられています。', 'role': 'Microsoft AI CEO'},
 {'id': 'simonyan', 'name': 'カレン・シモニャン', 'kind': 'p', 'from': 2024, 'desc': 'Inflection AIの共同創業者。スレイマンと共にMicrosoftへ移り、Microsoft AIのチーフサイエンティスト。', 'role': 'チーフサイエンティスト'},
 {'id': 'andreou', 'name': 'ジェイコブ・アンドリュー', 'kind': 'p', 'from': 2026, 'desc': '2026年3月に、ConsumerとEnterpriseのCopilotを統合した組織の責任者に就任と報じられています。', 'role': 'Copilot責任者'},
 {'id': 'hoffman', 'name': 'リード・ホフマン', 'kind': 'p', 'from': 2017, 'desc': 'LinkedIn共同創業者。LinkedInの買収後、取締役を務めています。OpenAIの初期出資者でもあります。', 'role': '取締役'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2019, 'desc': '2019年に10億ドルを出資して提携。累計約130億ドルを投じる契約と報じられています。', 'role': '最大の外部株主として出資'},
 {'id': 'anthropic', 'name': 'Anthropic', 'kind': 'o', 'from': 2025, 'desc': '2025年に出資を発表と報じられています。', 'role': '出資先'},
 {'id': 'inflection', 'name': 'Inflection AI', 'kind': 'o', 'from': 2024, 'desc': '2024年に、約6.5億ドルで技術のライセンスと人材を獲得したと報じられています。', 'role': '人材・技術を獲得'},
 {'id': 'mistral', 'name': 'Mistral AI', 'kind': 'o', 'from': 2024, 'desc': '2024年に少額を出資し提携したと報じられています。', 'role': '出資先'},
 {'id': 'deepmind', 'name': 'Google DeepMind', 'kind': 'o', 'from': 2019, 'desc': 'スレイマンの出身元(共同創業者)。', 'role': '出身元'},
]
E = (std('msft') +
 "E.push({a:'msft',b:'openai',k:'invest2',label:'約25%(報道)'});\n"
 "E.push({a:'msft',b:'anthropic',k:'invest2'});\n"
 "E.push({a:'msft',b:'inflection',k:'invest2',label:'約6.5億ドル'});\n"
 "E.push({a:'msft',b:'mistral',k:'invest2'});\n"
 "E.push({a:'suleyman',b:'inflection',k:'from'});\n"
 "E.push({a:'simonyan',b:'inflection',k:'from'});\n"
 "E.push({a:'suleyman',b:'deepmind',k:'from'});\n\n")
CO['msft'] = mk(N, E,
 {'nadella': 'Satya Nadella', 'gates': 'Bill Gates', 'smith': 'Brad Smith', 'scott': 'Kevin Scott', 'suleyman': 'Mustafa Suleyman', 'simonyan': 'Karen Simonyan', 'andreou': 'Jacob Andreou', 'hoffman': 'Reid Hoffman'},
 {'nadella': 'satyanadella', 'gates': 'BillGates', 'smith': 'BradSmi', 'scott': 'kevin_scott', 'suleyman': 'mustafasuleyman', 'hoffman': 'reidhoffman', 'msft': 'Microsoft', 'openai': 'OpenAI', 'anthropic': 'AnthropicAI'},
 {'msft': 'https://www.microsoft.com', 'openai': 'https://openai.com', 'anthropic': 'https://www.anthropic.com', 'mistral': 'https://mistral.ai'},
 wp(('msft', 'Microsoft'), ('openai', 'OpenAI'), ('anthropic', 'Anthropic'), ('inflection', 'Inflection_AI'), ('mistral', 'Mistral_AI'), ('deepmind', 'Google_DeepMind')),
 {'nadella': [['1992', 'Microsoftに入社'], ['2014', 'CEOに就任'], ['2019', 'OpenAIへ10億ドルを出資']],
  'suleyman': [['2010', 'DeepMindを共同創業'], ['2022', 'Inflection AIを設立'], ['2024', 'Microsoft AIのCEOに'], ['2026', '3月の再編でモデル開発に集中(報道)']]},
 {'gates': [['ブログ(Gates Notes)', 'https://www.gatesnotes.com']]}, 'msft')

# ---------------- Mistral AI ----------------
N = [
 {'id': 'mistral', 'name': 'Mistral AI', 'kind': 'c', 'from': 2023, 'desc': '2023年にパリで設立された、欧州を代表するAI企業。2025年9月にASMLが主導した約17億ユーロの増資(評価額は約117億ユーロ)を行いました。2026年の新たな増資の交渉は未確認です。'},
 {'id': 'mensch', 'name': 'アルチュール・メンシュ', 'kind': 'p', 'from': 2023, 'desc': '共同創業者でCEO。元DeepMindの研究者です。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'lample', 'name': 'ギヨーム・ランプル', 'kind': 'p', 'from': 2023, 'desc': '共同創業者でチーフサイエンティスト。元Metaで、LLaMAの開発に参加しました。', 'role': 'チーフサイエンティスト / 共同創業者', 'founder': 1},
 {'id': 'lacroix', 'name': 'ティモテ・ラクロワ', 'kind': 'p', 'from': 2023, 'desc': '共同創業者でCTO。元Metaの研究者です。', 'role': 'CTO / 共同創業者', 'founder': 1},
 {'id': 'asml', 'name': 'ASML', 'kind': 'i', 'from': 2025, 'desc': '2025年9月に約13億ユーロを出資し、約11%を持つ最大株主になったと報じられています。戦略委員会にも席があります。', 'role': '最大株主(報道)'},
 {'id': 'a16z', 'name': 'Andreessen Horowitz', 'kind': 'i', 'from': 2023, 'desc': '2023年のシリーズAを主導したと報じられています。', 'role': 'VC'},
 {'id': 'lightspeed', 'name': 'Lightspeed', 'kind': 'i', 'from': 2024, 'desc': '出資者の一社。', 'role': 'VC'},
 {'id': 'generalcatalyst', 'name': 'General Catalyst', 'kind': 'i', 'from': 2024, 'desc': '出資者の一社。', 'role': 'VC'},
 {'id': 'bpifrance', 'name': 'Bpifrance', 'kind': 'i', 'from': 2024, 'desc': 'フランスの公的投資銀行。', 'role': '公的投資銀行'},
 {'id': 'dst', 'name': 'DST Global', 'kind': 'i', 'from': 2025, 'desc': '2025年の増資に参加と報じられています。', 'role': '投資会社'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2024, 'desc': '出資者の一社。2025年の増資にも参加と報じられています。', 'role': '出資 + GPU供給'},
 {'id': 'microsoft', 'name': 'Microsoft', 'kind': 'i', 'from': 2024, 'desc': '2024年に少額を出資し提携したと報じられています。', 'role': '戦略出資者'},
 {'id': 'niel', 'name': 'グザビエ・ニール', 'kind': 'i', 'from': 2023, 'desc': 'フランスの通信会社Iliadの創業者。初期の出資者の一人と報じられています。', 'role': '個人投資家'},
 {'id': 'deepmind', 'name': 'Google DeepMind', 'kind': 'o', 'from': 2023, 'desc': 'メンシュの出身元。', 'role': '出身元'},
 {'id': 'meta', 'name': 'Meta', 'kind': 'o', 'from': 2023, 'desc': 'ランプルとラクロワの出身元(FAIR)。', 'role': '出身元'},
]
E = (std('mistral') + "E.push({a:'mensch',b:'deepmind',k:'from'});\n['lample','lacroix'].forEach(a=>E.push({a,b:'meta',k:'from'}));\n\n")
CO['mistral'] = mk(N, E,
 {'mensch': 'Arthur Mensch', 'lample': 'Guillaume Lample', 'lacroix': 'Timothée Lacroix', 'niel': 'Xavier Niel'},
 {'mensch': 'arthurmensch', 'mistral': 'MistralAI', 'nvidia': 'nvidia', 'microsoft': 'Microsoft'},
 {'mistral': 'https://mistral.ai', 'asml': 'https://www.asml.com', 'nvidia': 'https://www.nvidia.com', 'a16z': 'https://a16z.com'},
 wp(('mistral', 'Mistral_AI'), ('asml', 'ASML_Holding'), ('a16z', 'Andreessen_Horowitz'), ('lightspeed', 'Lightspeed_Venture_Partners'), ('generalcatalyst', 'General_Catalyst'), ('bpifrance', 'Bpifrance'),
     ('dst', 'DST_Global'), ('nvidia', 'Nvidia'), ('microsoft', 'Microsoft'), ('deepmind', 'Google_DeepMind'), ('meta', 'Meta_Platforms'), ('niel', 'Xavier_Niel')),
 {'mensch': [['〜', 'DeepMindの研究者'], ['2023', 'Mistral AIを共同創業'], ['2025', 'ASMLが主導する増資']]}, {}, 'mistral')

# ---------------- Sakana AI ----------------
N = [
 {'id': 'sakana', 'name': 'Sakana AI', 'kind': 'c', 'from': 2023, 'desc': '2023年に東京で設立されたAI企業。2025年11月に約200億円の増資(評価額は約400億円〜約26.5億ドルと報じられています)を行いました。2026年1月にGoogleとの提携と出資が発表されています。'},
 {'id': 'ha', 'name': 'デイビッド・ハ', 'kind': 'p', 'from': 2023, 'desc': '共同創業者でCEO。元Google Brainの研究者です。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'jones', 'name': 'リオン・ジョーンズ', 'kind': 'p', 'from': 2023, 'desc': '共同創業者でCTO。AIの基盤「トランスフォーマー」の論文「Attention Is All You Need」の共著者の一人です。', 'role': 'CTO / 共同創業者', 'founder': 1},
 {'id': 'ito', 'name': '伊藤錬', 'kind': 'p', 'from': 2023, 'desc': '共同創業者。元外務省、元メルカリで、COOとして報じられています。', 'role': 'COO / 共同創業者', 'founder': 1},
 {'id': 'khosla', 'name': 'Khosla Ventures', 'kind': 'i', 'from': 2024, 'desc': '出資者の一社と報じられています。', 'role': 'VC'},
 {'id': 'lux', 'name': 'Lux Capital', 'kind': 'i', 'from': 2023, 'desc': 'シード(初期)を主導したと報じられています。', 'role': 'VC'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2024, 'desc': '出資者の一社と報じられています。', 'role': '出資 + GPU供給'},
 {'id': 'mufg', 'name': 'MUFG', 'kind': 'i', 'from': 2025, 'desc': '三菱UFJフィナンシャル・グループ。2025年の増資に参加と報じられています。', 'role': '国内の金融グループ'},
 {'id': 'google', 'name': 'Google', 'kind': 'i', 'from': 2026, 'desc': '2026年1月に戦略的な提携と出資を発表と報じられています。', 'role': '戦略出資者'},
 {'id': 'googlebrain', 'name': 'Google Brain', 'kind': 'o', 'from': 2023, 'desc': 'ハとジョーンズの出身元。', 'role': '出身元'},
]
E = std('sakana') + "['ha','jones'].forEach(a=>E.push({a,b:'googlebrain',k:'from'}));\n\n"
CO['sakana'] = mk(N, E,
 {'ha': 'David Ha', 'jones': 'Llion Jones', 'ito': 'Ren Ito'},
 {'ha': 'hardmaru', 'jones': 'YesThisIsLion', 'sakana': 'SakanaAILabs', 'nvidia': 'nvidia'},
 {'sakana': 'https://sakana.ai', 'nvidia': 'https://www.nvidia.com', 'khosla': 'https://www.khoslaventures.com', 'lux': 'https://www.luxcapital.com'},
 wp(('sakana', 'Sakana_AI'), ('nvidia', 'Nvidia'), ('khosla', 'Khosla_Ventures'), ('lux', 'Lux_Capital'), ('mufg', 'Mitsubishi_UFJ_Financial_Group'), ('google', 'Google'), ('googlebrain', 'Google_Brain')),
 {'jones': [['〜', 'Googleで「Attention Is All You Need」を共著'], ['2023', 'Sakana AIを共同創業']],
  'ha': [['〜', 'Google Brainの研究者'], ['2023', 'Sakana AIを共同創業']]},
 {'ha': [['ブログ', 'https://blog.otoro.net']]}, 'sakana')

# ---------------- SoftBank ----------------
N = [
 {'id': 'softbank', 'name': 'SoftBank Group', 'kind': 'c', 'from': 2016, 'desc': 'OpenAIの大株主(約11〜13%と報じられています)。2025年にはOpenAI、オラクルと共に巨大AIインフラ計画「スターゲート」を発表。Armの親会社でもあります。'},
 {'id': 'son', 'name': '孫正義', 'kind': 'p', 'from': 2016, 'desc': '創業者で会長兼社長。スターゲートの会長を務めます。', 'role': '創業者 / 会長兼社長', 'founder': 1},
 {'id': 'goto', 'name': '後藤芳光', 'kind': 'p', 'from': 2016, 'desc': '取締役でCFO。', 'role': 'CFO'},
 {'id': 'haas', 'name': 'レネ・ハース', 'kind': 'p', 'from': 2022, 'desc': 'ArmのCEO。以前はNvidiaに在籍しました。', 'role': 'Arm CEO'},
 {'id': 'claure', 'name': 'マルセロ・クラウレ', 'kind': 'p', 'from': 2016, 'to': 2020, 'desc': 'SoftBankの元COOで、米Sprintの会長も務めました。2020年に退任と報じられています。', 'role': '元COO'},
 {'id': 'altman', 'name': 'サム・アルトマン', 'kind': 'o', 'from': 2024, 'desc': 'OpenAIのCEO。SoftBankとは出資とスターゲートで連携しています。', 'role': 'OpenAI CEO'},
 {'id': 'jackma', 'name': 'ジャック・マー', 'kind': 'o', 'from': 2016, 'desc': 'アリババの創業者。孫正義が2000年に約20億円を出資した、長年の盟友として知られます。', 'role': '盟友'},
 {'id': 'ellison', 'name': 'ラリー・エリソン', 'kind': 'o', 'from': 2025, 'desc': 'オラクルの共同創業者。スターゲートの共同パートナー。', 'role': 'スターゲートの共同パートナー'},
 {'id': 'pif', 'name': 'Saudi PIF', 'kind': 'i', 'from': 2016, 'desc': 'サウジアラビアの政府系ファンド。ビジョン・ファンドの最大の出資者。', 'role': '政府系ファンド'},
 {'id': 'mubadala', 'name': 'Mubadala', 'kind': 'i', 'from': 2016, 'desc': 'アブダビの政府系ファンド。ビジョン・ファンドの出資者。', 'role': '政府系ファンド'},
 {'id': 'arm', 'name': 'Arm', 'kind': 'o', 'from': 2016, 'desc': '2016年に約3.3兆円で買収した半導体設計会社。', 'role': '子会社'},
 {'id': 'visionfund', 'name': 'Vision Fund', 'kind': 'o', 'from': 2017, 'desc': '2017年に設立した巨大な投資ファンド。', 'role': '投資ファンド'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2024, 'desc': '2025年に約400億ドルを投資する取引が完了し、約11%を持つと報じられています(13%とする報道もあります)。', 'role': '大株主'},
 {'id': 'stargate', 'name': 'Stargate', 'kind': 'o', 'from': 2025, 'desc': 'OpenAI、オラクルと共に2025年1月に発表した、巨大なAIデータセンター計画。孫正義が会長。', 'role': '共同計画'},
 {'id': 'alibaba', 'name': 'Alibaba', 'kind': 'o', 'from': 2016, 'desc': '2000年にSoftBankが出資した、中国のEC企業。大きな利益を生んだ投資として知られます。', 'role': '過去の大型投資'},
 {'id': 'ampere', 'name': 'Ampere', 'kind': 'o', 'from': 2025, 'desc': '米国の半導体設計会社。SoftBankによる買収が2025年に報じられました。', 'role': '買収(報道)'},
 {'id': 'oracle', 'name': 'Oracle', 'kind': 'o', 'from': 2025, 'desc': 'スターゲートの共同パートナー。', 'role': '共同パートナー'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'o', 'from': 2016, 'desc': 'SoftBankは保有株を全て売却したと報じられています。ハースの前の勤務先。', 'role': '売却(報道)'},
]
E = (std('softbank') +
 "E.push({a:'softbank',b:'openai',k:'invest2',label:'約11〜13%(報道)',since:2024});\n"
 "E.push({a:'softbank',b:'arm',k:'owns',label:'約9割を保有'});\n"
 "E.push({a:'softbank',b:'visionfund',k:'owns'});\n"
 "E.push({a:'softbank',b:'stargate',k:'link',since:2025});\n"
 "E.push({a:'softbank',b:'alibaba',k:'invest2',label:'2000年に出資'});\n"
 "E.push({a:'softbank',b:'ampere',k:'invest2',since:2025});\n"
 "E.push({a:'altman',b:'openai',k:'link'});\n"
 "E.push({a:'son',b:'jackma',k:'link',label:'盟友'});\n"
 "E.push({a:'ellison',b:'oracle',k:'link'});\n"
 "E.push({a:'oracle',b:'stargate',k:'link'});\n"
 "E.push({a:'haas',b:'arm',k:'link'});\n"
 "E.push({a:'haas',b:'nvidia',k:'from'});\n\n")
CO['softbank'] = mk(N, E,
 {'son': 'Masayoshi Son', 'goto': 'Yoshimitsu Goto', 'haas': 'Rene Haas', 'claure': 'Marcelo Claure', 'altman': 'Sam Altman', 'jackma': 'Jack Ma', 'ellison': 'Larry Ellison'},
 {'son': 'masason', 'haas': 'renehaas', 'altman': 'sama', 'softbank': 'softbank', 'openai': 'OpenAI'},
 {'softbank': 'https://group.softbank', 'arm': 'https://www.arm.com', 'openai': 'https://openai.com', 'oracle': 'https://www.oracle.com'},
 wp(('softbank', 'SoftBank_Group'), ('arm', 'Arm_Holdings'), ('visionfund', 'SoftBank_Vision_Fund'), ('openai', 'OpenAI'), ('stargate', 'Stargate_LLC'), ('alibaba', 'Alibaba_Group'),
    ('ampere', 'Ampere_Computing'), ('oracle', 'Oracle_Corporation'), ('nvidia', 'Nvidia'), ('pif', 'Public_Investment_Fund'), ('mubadala', 'Mubadala')),
 {'son': [['1981', 'ソフトバンクを創業'], ['2000', 'アリババに出資'], ['2016', 'Armを買収'], ['2017', 'ビジョン・ファンドを設立'], ['2025', 'OpenAI・オラクルとスターゲートを発表']]},
 {}, 'softbank')

# ---------------- Nvidia ----------------
N = [
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'c', 'from': 2016, 'desc': 'AI向けGPUの供給元で、主要なAI企業の出資者。2026年は出資の約束が400億ドルを超えたと報じられています。ジェンスン・フアンは「勝者を選ばない」方針と語っています。'},
 {'id': 'huang', 'name': 'ジェンスン・フアン', 'kind': 'p', 'from': 2016, 'desc': '共同創業者でCEO。2016年にOpenAIへ最初のAIスーパーコンピューターDGXを届けたことで知られます。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'malachowsky', 'name': 'クリス・マラコウスキー', 'kind': 'p', 'from': 2016, 'desc': '共同創業者。', 'role': '共同創業者', 'founder': 1},
 {'id': 'kress', 'name': 'コレット・クレス', 'kind': 'p', 'from': 2016, 'desc': 'CFO。', 'role': 'CFO'},
 {'id': 'dally', 'name': 'ビル・ダリー', 'kind': 'p', 'from': 2016, 'desc': 'チーフサイエンティスト。スタンフォード大学の元教授。', 'role': 'チーフサイエンティスト'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2016, 'desc': '2016年に最初のDGXを届けた相手。2026年に約300億ドルの出資が確定したと報じられています(当初の1,000億ドルの構想は見送り)。', 'role': '出資先'},
 {'id': 'anthropic', 'name': 'Anthropic', 'kind': 'o', 'from': 2025, 'desc': '2025年11月に最大100億ドルを出資と報じられています。', 'role': '出資先'},
 {'id': 'xai', 'name': 'xAI', 'kind': 'o', 'from': 2024, 'desc': '資金調達に参加(2026年1月の約200億ドルの増資を含む)と報じられています。', 'role': '出資先'},
 {'id': 'mistral', 'name': 'Mistral AI', 'kind': 'o', 'from': 2024, 'desc': '出資先の一社。', 'role': '出資先'},
 {'id': 'ssi', 'name': 'Safe Superintelligence', 'kind': 'o', 'from': 2025, 'desc': '出資先の一社と報じられています。', 'role': '出資先'},
 {'id': 'tml', 'name': 'Thinking Machines Lab', 'kind': 'o', 'from': 2025, 'desc': '出資先の一社と報じられています。', 'role': '出資先'},
 {'id': 'sakana', 'name': 'Sakana AI', 'kind': 'o', 'from': 2024, 'desc': '出資先の一社と報じられています。', 'role': '出資先'},
 {'id': 'softbank', 'name': 'SoftBank Group', 'kind': 'o', 'from': 2016, 'desc': 'かつての株主。保有株を売却したと報じられています。', 'role': '元株主'},
]
E = (std('nvidia') +
 "E.push({a:'nvidia',b:'openai',k:'invest2',label:'約300億ドル(報道)',since:2025});\n"
 "E.push({a:'nvidia',b:'anthropic',k:'invest2',label:'最大100億ドル'});\n"
 "['xai','mistral','ssi','tml','sakana'].forEach(b=>E.push({a:'nvidia',b,k:'invest2'}));\n"
 "E.push({a:'softbank',b:'nvidia',k:'link',label:'株式を売却(報道)'});\n"
 "E.push({a:'huang',b:'openai',k:'link',label:'DGXを寄贈',since:2016});\n\n")
CO['nvidia'] = mk(N, E,
 {'huang': 'Jensen Huang', 'malachowsky': 'Chris Malachowsky', 'kress': 'Colette Kress', 'dally': 'Bill Dally'},
 {'nvidia': 'nvidia', 'openai': 'OpenAI', 'anthropic': 'AnthropicAI', 'xai': 'xai', 'mistral': 'MistralAI', 'ssi': 'ssi', 'tml': 'thinkymachines', 'sakana': 'SakanaAILabs'},
 {'nvidia': 'https://www.nvidia.com', 'openai': 'https://openai.com', 'anthropic': 'https://www.anthropic.com', 'xai': 'https://x.ai', 'mistral': 'https://mistral.ai', 'ssi': 'https://ssi.inc', 'tml': 'https://thinkingmachines.ai', 'sakana': 'https://sakana.ai'},
 wp(('nvidia', 'Nvidia'), ('openai', 'OpenAI'), ('anthropic', 'Anthropic'), ('xai', 'XAI_(company)'), ('mistral', 'Mistral_AI'), ('ssi', 'Safe_Superintelligence_Inc.'), ('tml', 'Thinking_Machines_Lab'),
    ('sakana', 'Sakana_AI'), ('softbank', 'SoftBank_Group')),
 {'huang': [['1993', 'Nvidiaを共同創業'], ['2016', 'OpenAIへDGXを届ける'], ['2026', '「勝者を選ばず、皆を支援する」と語る']]}, {}, 'nvidia')
