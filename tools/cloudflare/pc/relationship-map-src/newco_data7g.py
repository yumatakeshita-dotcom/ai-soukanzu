from newco_data import mk, std

# Applied Compute(2026年11月の調達を反映)と Adept(Amazonに創業者が移った会社)の図。
CO7G = {}
L_ = lambda label, url: [label, url]

# ---------------- Applied Compute ----------------
SRC_AC = L_('出典: SiliconANGLE(2026年11月3日、3.5億ドルの調達)', 'https://siliconangle.com/2026/11/03/ai-cloud-startup-applied-compute-raises-350m-after-reaching-key-revenue-milestone/')
SRC_AC0 = L_('出典: PYMNTS(元OpenAI社員の新会社)', 'https://www.pymnts.com/news/artificial-intelligence/2025/former-openai-employees-launch-their-own-startups/')
N = [
 {'id': 'appliedcompute', 'name': 'Applied Compute', 'kind': 'c', 'from': 2025, 'desc': 'OpenAIの技術系の元社員3人が、2025年にOpenAIを離れて起こした会社(PYMNTSは2025年5月ごろに離れたと報道。SiliconANGLEは、2026年11月時点で「設立から18か月足らず」)。LLMの学習と推論を動かすクラウド基盤と、顧客のプロジェクトを手伝う機械学習の研究者チーム、リクエストごとに最も費用効率のよいLLMへ振り分けるモデルルーター「Shift-1」を提供します。2026年11月3日に、3.5億ドルを評価額32.5億ドルで調達(Elad Gil主導)と発表。年間経常収益は1億ドルを超えたと、SiliconANGLEが伝えています。2026年4月には、8,000万ドル(評価額13億ドル)と報じられました(主導した会社は、資料によりKleiner PerkinsとBenchmarkで食い違い、確認できていません)。'},
 {'id': 'garg', 'name': 'リズム・ガーグ', 'kind': 'p', 'from': 2025, 'desc': '共同創業者。OpenAIに1年以上在籍した、技術系の社員だったと報じられています。', 'role': '共同創業者', 'founder': 1},
 {'id': 'li', 'name': 'リンデン・リー', 'kind': 'p', 'from': 2025, 'desc': '共同創業者。同上。', 'role': '共同創業者', 'founder': 1},
 {'id': 'patil', 'name': 'ヤシュ・パティル', 'kind': 'p', 'from': 2025, 'desc': '共同創業者でCEO。', 'role': '共同創業者 / CEO', 'founder': 1},
 {'id': 'gil', 'name': 'エラド・ギル', 'kind': 'i', 'from': 2026, 'desc': '2026年11月の3.5億ドルの調達を主導した、著名な個人投資家。2026年4月の調達にも参加したと報じられています。', 'role': '出資者(2026年11月を主導)'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2026, 'desc': '2026年11月の調達に参加。', 'role': '出資者(2026年11月)'},
 {'id': 'shopify', 'name': 'Shopify Ventures', 'kind': 'i', 'from': 2026, 'desc': '2026年11月の調達に参加。', 'role': '出資者(2026年11月)'},
 {'id': 'hubspot', 'name': 'HubSpot Ventures', 'kind': 'i', 'from': 2026, 'desc': '2026年11月の調達に参加。', 'role': '出資者(2026年11月)'},
 {'id': 'kleiner', 'name': 'Kleiner Perkins', 'kind': 'i', 'from': 2026, 'desc': '2026年4月の8,000万ドルを主導したと、法律事務所の発表などが伝えています(別の資料はBenchmarkとしており、確認できていません)。', 'role': '出資者(2026年4月、主導と報じられる)'},
 {'id': 'microsoft', 'name': 'Microsoft', 'kind': 'o', 'from': 2026, 'desc': '顧客として、SiliconANGLEが名前を挙げています。', 'role': '顧客'},
 {'id': 'doordash', 'name': 'DoorDash', 'kind': 'o', 'from': 2026, 'desc': '顧客として、SiliconANGLEが名前を挙げています。', 'role': '顧客'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2015, 'desc': '創業者3人の前の勤め先。', 'role': '創業者の前の勤め先'},
]
E = (std('appliedcompute') + "['garg','li','patil'].forEach(a=>E.push({a,b:'openai',k:'from'}));\n"
     "['microsoft','doordash'].forEach(a=>E.push({a,b:'appliedcompute',k:'link',label:'顧客',since:2026}));\n\n")
CO7G['appliedcompute'] = mk(N, E, {'garg': 'Rhythm Garg', 'li': 'Linden Li', 'patil': 'Yash Patil', 'gil': 'Elad Gil'}, {}, {}, {}, {},
 {'appliedcompute': [SRC_AC, SRC_AC0], 'garg': [SRC_AC0], 'patil': [SRC_AC], 'gil': [SRC_AC]}, 'appliedcompute')

# ---------------- Adept ----------------
SRC_AD = L_('出典: TechCrunch(2024年6月28日、Amazonが創業者を採用)', 'https://techcrunch.com/2024/06/28/amazon-hires-founders-away-from-ai-startup-adept')
N = [
 {'id': 'adept', 'name': 'Adept', 'kind': 'c', 'from': 2022, 'desc': 'ソフトウェアの作業を自然言語でこなすAI「エージェント」を作る会社(設立は、TechCrunchの2024年6月時点で「2年前」)。元OpenAIのVPデビッド・ルアンらが共同創業と報じられています。2024年6月28日に、Amazonがルアンら共同創業者5人を採用し、技術を非独占でライセンスすると発表。Adeptは、エンジニアリング責任者のザック・ブロックをCEOとして続けました。資金は累計4.15億ドル超、評価額は約10億ドル(TechCrunch)。'},
 {'id': 'luan', 'name': 'デビッド・ルアン', 'kind': 'p', 'from': 2022, 'to': 2024, 'desc': '共同創業者でCEO。元OpenAIのVPと報じられています。2024年6月にAmazonへ移り、ロヒット・プラサド率いる新しいAGIチームに就きました。のちAmazonのAGI研究所を率い、2026年にAmazonを離れると報じられています(GeekWireの見出し。日付は確認できていません)。', 'role': '共同創業者 / 元CEO', 'founder': 1},
 {'id': 'odena', 'name': 'オーガスタス・オデナ', 'kind': 'p', 'from': 2022, 'to': 2024, 'desc': '共同創業者。2024年6月にAmazonへ。', 'role': '共同創業者', 'founder': 1},
 {'id': 'nye', 'name': 'マクスウェル・ナイ', 'kind': 'p', 'from': 2022, 'to': 2024, 'desc': '共同創業者。2024年6月にAmazonへ。', 'role': '共同創業者', 'founder': 1},
 {'id': 'elsen', 'name': 'エリック・エルセン', 'kind': 'p', 'from': 2022, 'to': 2024, 'desc': '共同創業者。2024年6月にAmazonへ。', 'role': '共同創業者', 'founder': 1},
 {'id': 'szot', 'name': 'ケルシー・ゾット', 'kind': 'p', 'from': 2022, 'to': 2024, 'desc': '共同創業者。2024年6月にAmazonへ。', 'role': '共同創業者', 'founder': 1},
 {'id': 'brock', 'name': 'ザック・ブロック', 'kind': 'p', 'from': 2024, 'desc': 'エンジニアリング責任者から、2024年6月にCEOに就きました。', 'role': 'CEO(2024年6月〜)'},
 {'id': 'vaswani', 'name': 'アシシュ・ヴァスワニ', 'kind': 'p', 'from': 2022, 'to': 2023, 'desc': '初期の共同創業者。Adeptを離れました(TechCrunchの記載)。', 'role': '初期の共同創業者(のち離脱)'},
 {'id': 'parmar', 'name': 'ニキ・パルマー', 'kind': 'p', 'from': 2022, 'to': 2023, 'desc': '初期の共同創業者。Adeptを離れました(TechCrunchの記載)。', 'role': '初期の共同創業者(のち離脱)'},
 {'id': 'amazon', 'name': 'Amazon', 'kind': 'o', 'from': 2024, 'desc': '2024年6月に、創業者5人を採用し、Adeptの技術を非独占でライセンス(条件は非公開)。ルアンは、プラサド率いる新しいAGIチームへ。', 'role': '人材の採用とライセンス(2024年)'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2023, 'desc': '出資者として、TechCrunchが名前を挙げています。', 'role': '出資者'},
 {'id': 'atlassian', 'name': 'Atlassian', 'kind': 'i', 'from': 2023, 'desc': '出資者として、TechCrunchが名前を挙げています。', 'role': '出資者'},
 {'id': 'workday', 'name': 'Workday', 'kind': 'i', 'from': 2023, 'desc': '出資者として、TechCrunchが名前を挙げています。', 'role': '出資者'},
 {'id': 'greylock', 'name': 'Greylock', 'kind': 'i', 'from': 2022, 'desc': '出資者として、TechCrunchが名前を挙げています。', 'role': '出資者'},
 {'id': 'msft', 'name': 'Microsoft', 'kind': 'i', 'from': 2023, 'desc': '以前に出資していたと、TechCrunchが書いています。', 'role': '出資者(以前)'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2015, 'desc': 'ルアンの前の勤め先(VP)と報じられています。', 'role': 'ルアンの前の勤め先'},
]
E = (std('adept') + "E.push({a:'luan',b:'openai',k:'from'});\n"
     "E.push({a:'amazon',b:'adept',k:'link',label:'創業者5人を採用、技術をライセンス(2024年6月)',since:2024});\n"
     "['luan','odena','nye','elsen','szot'].forEach(a=>E.push({a,b:'amazon',k:'moved',since:2024}));\n"
     "['vaswani','parmar'].forEach(a=>E.push({a,b:'adept',k:'link',label:'初期の共同創業者(のち離脱)'}));\n"
     "E.push({a:'brock',b:'luan',k:'link',label:'CEOを引き継いだ',since:2024});\n\n")
CO7G['adept'] = mk(N, E, {'luan': 'David Luan', 'odena': 'Augustus Odena', 'nye': 'Maxwell Nye', 'elsen': 'Erich Elsen', 'szot': 'Kelsey Szot', 'brock': 'Zach Brock', 'vaswani': 'Ashish Vaswani', 'parmar': 'Niki Parmar'}, {}, {}, {},
 {'luan': [['2022', 'Adeptを共同創業(CEO)'], ['2024', '6月にAmazonへ移り、AGIチームに'], ['2026', 'Amazonを離れると報じられる(日付は未確認)']]},
 {'adept': [SRC_AD], 'luan': [SRC_AD], 'amazon': [SRC_AD], 'brock': [SRC_AD], 'nvidia': [SRC_AD], 'atlassian': [SRC_AD], 'workday': [SRC_AD], 'greylock': [SRC_AD], 'msft': [SRC_AD]}, 'adept')
