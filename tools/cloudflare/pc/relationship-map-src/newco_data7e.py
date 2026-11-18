from newco_data import mk, std, wp

# OpenAI・Anthropicなどを離れた人たちが起こした会社の図。事実は、各項目に付けた出典(2026年11月に確認)に基づく。
# 報道どうしで食い違う数字は、食い違いのまま書く。確認できなかったこと(出資者・金額など)は書かない。
CO7E = {}
L_ = lambda label, url: [label, url]
WPD = lambda t: ['出典: Wikipedia(%s)' % t.replace('_', ' '), 'https://en.wikipedia.org/wiki/' + t]

# ---------------- Periodic Labs ----------------
SRC_TC = L_('出典: TechCrunch(2025年10月、3億ドルのシード)', 'https://techcrunch.com/2025/10/20/top-openai-google-brain-researchers-set-off-a-300m-vc-frenzy-for-their-startup-periodic-labs')
SRC_SA = L_('出典: SiliconANGLE(2025年10月1日)', 'https://siliconangle.com/2025/10/01/periodic-labs-raises-300m-accelerate-scientific-research-ai/')
N = [
 {'id': 'periodic', 'name': 'Periodic Labs', 'kind': 'c', 'from': 2025, 'desc': '2025年9月30日(米国時間)に、約3億ドルのシード資金とともに表に出た会社。AIで科学の発見を自動化する「AI科学者」を作り、粉末合成の自動実験室を動かします(超伝導体や半導体の材料から)。評価額は、約10億ドルとする報道が1件あります(確認できていません)。'},
 {'id': 'fedus', 'name': 'リアム・フェダス', 'kind': 'p', 'from': 2025, 'desc': '共同創業者。元OpenAIのVP(研究・ポストトレーニングの担当と報じられています)。', 'role': '共同創業者 / 元OpenAI VP', 'founder': 1},
 {'id': 'cubuk', 'name': 'エキン・ドーウス・チュブク', 'kind': 'p', 'from': 2025, 'desc': '共同創業者。Google DeepMindで材料・化学のチームを率い、材料発見のモデルGNoMEを共同で作りました。', 'role': '共同創業者 / 元DeepMind', 'founder': 1},
 {'id': 'a16z', 'name': 'Andreessen Horowitz', 'kind': 'i', 'from': 2025, 'desc': 'シードを主導したと、TechCrunchなど多くの報道が伝えています(1件の集計サイトは、Felicisを主導としています)。', 'role': 'シード出資者(主導と報じられる)'},
 {'id': 'felicis', 'name': 'Felicis', 'kind': 'i', 'from': 2025, 'desc': '最初の出資(first check)を出したと報じられています。', 'role': '出資者'},
 {'id': 'dst', 'name': 'DST Global', 'kind': 'i', 'from': 2025, 'desc': 'シードの出資者として報じられています。', 'role': '出資者'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2025, 'desc': 'シードの出資者(NVentures)として報じられています。', 'role': '出資者'},
 {'id': 'accel', 'name': 'Accel', 'kind': 'i', 'from': 2025, 'desc': 'シードの出資者として報じられています。', 'role': '出資者'},
 {'id': 'gil', 'name': 'エラド・ギル', 'kind': 'i', 'from': 2025, 'desc': '個人の出資者として報じられています。', 'role': '個人投資家'},
 {'id': 'dean', 'name': 'ジェフ・ディーン', 'kind': 'i', 'from': 2025, 'desc': '個人の出資者として報じられています。', 'role': '個人投資家'},
 {'id': 'schmidt', 'name': 'エリック・シュミット', 'kind': 'i', 'from': 2025, 'desc': '個人の出資者として報じられています。', 'role': '個人投資家'},
 {'id': 'bezos', 'name': 'ジェフ・ベゾス', 'kind': 'i', 'from': 2025, 'desc': '個人の出資者として報じられています。', 'role': '個人投資家'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2015, 'desc': 'フェダスの前の勤め先。', 'role': 'フェダスの前の勤め先'},
 {'id': 'deepmind', 'name': 'Google DeepMind', 'kind': 'o', 'from': 2010, 'desc': 'チュブクの前の勤め先(Google Brain、DeepMind)。', 'role': 'チュブクの前の勤め先'},
]
E = (std('periodic') + "E.push({a:'fedus',b:'openai',k:'from'});\nE.push({a:'cubuk',b:'deepmind',k:'from'});\nE.push({a:'fedus',b:'cubuk',k:'link',label:'共同創業'});\n\n")
CO7E['periodic'] = mk(N, E, {'fedus': 'Liam Fedus', 'cubuk': 'Ekin Dogus Cubuk', 'gil': 'Elad Gil', 'dean': 'Jeff Dean', 'schmidt': 'Eric Schmidt', 'bezos': 'Jeff Bezos'}, {'fedus': 'LiamFedus'}, {},
 wp(('fedus', 'Liam_Fedus'), ('openai', 'OpenAI'), ('deepmind', 'Google_DeepMind')),
 {'fedus': [['2025', '9月30日、Periodic Labsを共同創業者として公表(OpenAIの元VP)']], 'cubuk': [['〜', 'Google DeepMindで材料・化学のチームを率い、GNoMEを共同で作る'], ['2025', 'Periodic Labsを共同創業']]},
 {'periodic': [SRC_TC, SRC_SA], 'fedus': [SRC_TC], 'cubuk': [SRC_TC], 'a16z': [SRC_TC, SRC_SA], 'felicis': [SRC_TC], 'nvidia': [SRC_SA]}, 'periodic')

# ---------------- Mirendil ----------------
SRC_DC = L_('出典: The Decoder(2026年3月14日、創業チーム)', 'https://the-decoder.com/ex-anthropic-researchers-launch-ai-startup-mirendil-to-tackle-scientific-research/')
SRC_MS = L_('出典: SiliconANGLE(2026年6月25日、2億ドルのシード)', 'https://siliconangle.com/2026/06/25/mirendil-raises-200m-speed-scientific-research-ai/')
N = [
 {'id': 'mirendil', 'name': 'Mirendil', 'kind': 'c', 'from': 2025, 'desc': 'Anthropicの元研究者2人が、2025年12月にAnthropicを離れて起こした、科学研究(生物学・材料科学など)を進めるAIの会社。2026年6月24日に、2億ドルのシードを評価額10億ドルで発表しました(a16zとKleiner Perkinsが共同で主導、Nvidiaが参加)。それ以前にThe Informationは、1.75億ドルの調達を交渉中と報じていました。さらに、最大10億ドルを評価額50億ドルで調達する交渉をBloombergが報じていますが、成立は確認できていません。2026年8月には、Google Cloudとの計算資源の契約(1億ドル超とCEOが述べた)が明らかになりました。'},
 {'id': 'neyshabur', 'name': 'ベナム・ネイシャブール', 'kind': 'p', 'from': 2025, 'desc': 'CEO。Anthropicで科学向けのAI推論チームを率い、その前はGoogle DeepMindに5年以上在籍。', 'role': '共同創業者 / CEO', 'founder': 1},
 {'id': 'mehta', 'name': 'ハーシュ・メータ', 'kind': 'p', 'from': 2025, 'desc': 'CTO。Anthropicのシニア研究サイエンティストだった人物。', 'role': '共同創業者 / CTO', 'founder': 1},
 {'id': 'salehian', 'name': 'シャヤン・サレヒアン', 'kind': 'p', 'from': 2026, 'desc': '創業チームの一人。元xAI。', 'role': 'チーム(元xAI)'},
 {'id': 'rezaei', 'name': 'タラ・レザイ', 'kind': 'p', 'from': 2026, 'desc': '創業チームの一人。元OpenAIのインターン。', 'role': 'チーム(元OpenAIインターン)'},
 {'id': 'a16z', 'name': 'Andreessen Horowitz', 'kind': 'i', 'from': 2026, 'desc': '2026年6月の2億ドルのシードを、Kleiner Perkinsと共同で主導したと報じられています(SiliconANGLEなど)。50億ドルの評価額での次の調達でも、再び出資する交渉と、Bloombergが報じています。', 'role': 'シードを共同で主導'},
 {'id': 'kleiner', 'name': 'Kleiner Perkins', 'kind': 'i', 'from': 2026, 'desc': '同シードを、a16zと共同で主導。次の調達(評価額50億ドル)でも、主導する交渉と報じられています(確認できていません)。', 'role': 'シードを共同で主導'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2026, 'desc': '2026年6月のシードに参加したと報じられています。', 'role': 'シードに参加'},
 {'id': 'googlecloud', 'name': 'Google Cloud', 'kind': 'o', 'from': 2026, 'desc': '2026年8月に、1億ドルを超える計算資源の契約が明らかになりました(CEOのネイシャブールの発言)。', 'role': '計算資源の契約'},
 {'id': 'anthropic', 'name': 'Anthropic', 'kind': 'o', 'from': 2021, 'desc': '創業者2人の前の勤め先。ダブルクリックで図を開きます。', 'role': '創業者の前の勤め先'},
 {'id': 'deepmind', 'name': 'Google DeepMind', 'kind': 'o', 'from': 2010, 'desc': 'ネイシャブールの、Anthropic以前の勤め先。', 'role': '前の勤め先'},
]
E = (std('mirendil') + "E.push({a:'googlecloud',b:'mirendil',k:'link',label:'計算資源の契約(1億ドル超)',since:2026});\nE.push({a:'neyshabur',b:'anthropic',k:'from'});\nE.push({a:'mehta',b:'anthropic',k:'from'});\nE.push({a:'neyshabur',b:'deepmind',k:'from'});\nE.push({a:'neyshabur',b:'mehta',k:'link',label:'共同創業'});\n\n")
CO7E['mirendil'] = mk(N, E, {'neyshabur': 'Behnam Neyshabur', 'mehta': 'Harsh Mehta', 'salehian': 'Shayan Salehian', 'rezaei': 'Tara Rezaei'}, {}, {},
 wp(('neyshabur', 'Behnam_Neyshabur')),
 {'neyshabur': [['〜', 'Google DeepMindに5年以上'], ['〜', 'Anthropicで科学向けAI推論チームを率いる'], ['2025', '12月ごろにAnthropicを離れ、Mirendilを共同創業']]},
 {'mirendil': [SRC_MS, SRC_DC], 'neyshabur': [SRC_DC], 'mehta': [SRC_DC], 'a16z': [SRC_MS], 'kleiner': [SRC_MS], 'nvidia': [SRC_MS]}, 'mirendil')

# ---------------- humans& ----------------
SRC_H = L_('出典: TechCrunch(2026年1月20日、4.8億ドルのシード)', 'https://techcrunch.com/2026/01/20/humans-a-human-centric-ai-startup-founded-by-anthropic-xai-google-alums-raised-480m-seed-round')
SRC_HC = L_('出典: Crunchbase News(評価額と資金の使い道)', 'https://news.crunchbase.com/ai/humans-raises-huge-seed-round-unicorn-valuation/')
N = [
 {'id': 'humans', 'name': 'humans&', 'kind': 'c', 'from': 2025, 'desc': 'Anthropic、xAI、Googleの出身者が作った会社。2025年10月に始まり、2026年1月20日に、4.8億ドルのシードを評価額約44.8億ドルで発表しました。「AIは、人を置き換えるのでなく、人に力を与える」という考え方で、人とAIの協働(強化学習、記憶、利用者の理解)に取り組みます。調達の大半は、学習用の計算資源に使うと、ペンがCrunchbase Newsに話しています。社員は約20人で、OpenAI、Meta、Reflection、AI2、MITの出身者(TechCrunch)。人が協力するためのソフト(AI版のメッセージアプリのようなもの)を作り、AIが利用者に情報を尋ねて記憶する、新しい学習の方法にも取り組むとされます。'},
 {'id': 'peng', 'name': 'アンディ・ペン', 'kind': 'p', 'from': 2025, 'desc': '共同創業者。元Anthropicの研究者で、Claude 3.5〜4.5の強化学習とポストトレーニングに関わったと報じられています。', 'role': '共同創業者 / 元Anthropic', 'founder': 1},
 {'id': 'zelikman', 'name': 'エリック・ゼリクマン', 'kind': 'p', 'from': 2025, 'desc': '共同創業者。元xAIの研究者。CEOとする報道が1件あります。', 'role': '共同創業者 / 元xAI', 'founder': 1},
 {'id': 'he', 'name': 'ユーチェン・ヒー', 'kind': 'p', 'from': 2025, 'desc': '共同創業者。元xAI(1件の集計サイトの記載)。', 'role': '共同創業者 / 元xAI', 'founder': 1},
 {'id': 'harik', 'name': 'ジョージズ・ハリク', 'kind': 'p', 'from': 2025, 'desc': '共同創業者。Googleの7番目の社員で、初期の広告システムの設計者。調達の共同主導とする報道があります。', 'role': '共同創業者 / 元Google', 'founder': 1},
 {'id': 'goodman', 'name': 'ノア・グッドマン', 'kind': 'p', 'from': 2025, 'desc': '共同創業者。スタンフォード大学の教授。', 'role': '共同創業者 / 教授', 'founder': 1},
 {'id': 'svangel', 'name': 'SV Angel', 'kind': 'i', 'from': 2026, 'desc': '参加した出資者として報じられています。TechCrunchは、主導した会社を明記していません(別の報道は、SV Angelとハリクが共同で主導したとしています)。', 'role': '出資者'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2026, 'desc': '参加した出資者として報じられています。', 'role': '出資者'},
 {'id': 'gv', 'name': 'GV', 'kind': 'i', 'from': 2026, 'desc': '参加した出資者として報じられています。', 'role': '出資者'},
 {'id': 'bezos', 'name': 'ジェフ・ベゾス', 'kind': 'i', 'from': 2026, 'desc': '個人の出資者として報じられています。', 'role': '個人投資家'},
 {'id': 'emerson', 'name': 'Emerson Collective', 'kind': 'i', 'from': 2026, 'desc': '参加した出資者として、1件の集計サイトが伝えています。', 'role': '出資者(報道1件)'},
 {'id': 'anthropic', 'name': 'Anthropic', 'kind': 'o', 'from': 2021, 'desc': 'ペンの前の勤め先。ダブルクリックで図を開きます。', 'role': 'ペンの前の勤め先'},
 {'id': 'xai', 'name': 'xAI', 'kind': 'o', 'from': 2023, 'desc': 'ゼリクマンとヒーの前の勤め先。', 'role': '前の勤め先'},
 {'id': 'google', 'name': 'Google', 'kind': 'o', 'from': 1998, 'desc': 'ハリクの前の勤め先(7番目の社員)。', 'role': 'ハリクの前の勤め先'},
]
E = (std('humans') + "E.push({a:'peng',b:'anthropic',k:'from'});\nE.push({a:'zelikman',b:'xai',k:'from'});\nE.push({a:'he',b:'xai',k:'from'});\nE.push({a:'harik',b:'google',k:'from'});\n"
     "E.push({a:'peng',b:'zelikman',k:'link',label:'共同創業'});\n\n")
CO7E['humans'] = mk(N, E, {'peng': 'Andi Peng', 'zelikman': 'Eric Zelikman', 'he': 'Yuchen He', 'harik': 'Georges Harik', 'goodman': 'Noah Goodman', 'bezos': 'Jeff Bezos'}, {}, {},
 wp(('harik', 'Georges_Harik')),
 {'harik': [['1999', 'Googleの7番目の社員として、初期の広告システムを設計'], ['2025', '10月にhumans&を共同創業']], 'peng': [['〜', 'Anthropicで強化学習とClaudeのポストトレーニングに関わる'], ['2025', 'humans&を共同創業']]},
 {'humans': [SRC_H, SRC_HC], 'peng': [SRC_H], 'zelikman': [SRC_H], 'harik': [SRC_H], 'svangel': [SRC_H], 'nvidia': [SRC_H], 'gv': [SRC_H], 'bezos': [SRC_H]}, 'humans')

# ---------------- Covariant ----------------
N = [
 {'id': 'covariant', 'name': 'Covariant', 'kind': 'c', 'from': 2017, 'desc': '旧名はEmbodied Intelligence。2017年に、ピーター・アビールらが創業した、ロボット向けのAIの会社(カリフォルニア州エメリービル)。倉庫でのピッキングなどをこなすソフト「Covariant Brain」と、2024年3月発表のロボット基盤モデルRFM-1を作りました。出資額の累計は約2.22億ドル(2023年の評価額は6.25億ドル)。'},
 {'id': 'abbeel', 'name': 'ピーター・アビール', 'kind': 'p', 'from': 2017, 'to': 2024, 'desc': '共同創業者で社長兼チーフサイエンティスト。UCバークレーのロボット学習研究室の責任者。OpenAIに在籍した経歴があります。2024年にAmazonへ。', 'role': '共同創業者 / チーフサイエンティスト', 'founder': 1},
 {'id': 'chen', 'name': 'ピーター・チェン', 'kind': 'p', 'from': 2017, 'to': 2024, 'desc': '共同創業者でCEO。アビールの元教え子で、OpenAIに在籍した経歴があります。2024年にAmazonへ。', 'role': '共同創業者 / CEO', 'founder': 1},
 {'id': 'duan', 'name': 'ロッキー・ドゥアン', 'kind': 'p', 'from': 2017, 'to': 2024, 'desc': '共同創業者でCTO。アビールの元教え子で、OpenAIに在籍した経歴があります。2024年にAmazonへ。', 'role': '共同創業者 / CTO', 'founder': 1},
 {'id': 'zhang', 'name': 'ティエンハオ・ジャン', 'kind': 'p', 'from': 2017, 'desc': '共同創業者。アビールの元教え子で、Microsoftに在籍した経歴があります。', 'role': '共同創業者', 'founder': 1},
 {'id': 'index', 'name': 'Index Ventures', 'kind': 'i', 'from': 2020, 'desc': '2020年5月の4,000万ドル(シリーズB)を主導しました。', 'role': 'シリーズBを主導'},
 {'id': 'amazon', 'name': 'Amazon', 'kind': 'i', 'from': 2024, 'desc': '2024年8月30日に、技術の「非独占」ライセンスを得て、従業員の約25%を採用し、アビール、チェン、ドゥアンを迎えると発表しました。2025年1月に、内部告発の申立てが報じられ、実質的な買収(約3.8億ドル)だという主張がありますが、これは申立てで、確認された事実ではありません。', 'role': 'ライセンスと人材の獲得(2024年)'},
 {'id': 'abb', 'name': 'ABB', 'kind': 'o', 'from': 2020, 'desc': '2020年2月に提携を発表した顧客・提携先。', 'role': '提携先'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2016, 'desc': 'アビール、チェン、ドゥアンの前の勤め先(2016〜2017年の研究者)。', 'role': '創業者の前の勤め先'},
]
E = (std('covariant') + "['abbeel','chen','duan'].forEach(a=>E.push({a,b:'openai',k:'from'}));\nE.push({a:'abbeel',b:'amazon',k:'moved',since:2024});\nE.push({a:'chen',b:'amazon',k:'moved',since:2024});\nE.push({a:'duan',b:'amazon',k:'moved',since:2024});\n"
     "E.push({a:'amazon',b:'covariant',k:'link',label:'技術ライセンス(2024年8月)',since:2024});\n"
     "E.push({a:'abb',b:'covariant',k:'link',label:'提携'});\n\n")
CO7E['covariant'] = mk(N, E, {'abbeel': 'Pieter Abbeel', 'chen': 'Peter Chen', 'duan': 'Rocky Duan', 'zhang': 'Tianhao Zhang'}, {}, {}, wp(('covariant', 'Covariant_(company)'), ('abbeel', 'Pieter_Abbeel')),
 {'abbeel': [['〜', 'UCバークレーのロボット学習研究室を率い、OpenAIに在籍'], ['2017', 'Embodied Intelligence(のちCovariant)を共同創業'], ['2024', '8月にAmazonへ']]},
 {'covariant': [WPD('Covariant_(company)')], 'amazon': [WPD('Covariant_(company)')], 'abbeel': [WPD('Pieter_Abbeel')]}, 'covariant')

# Applied Compute と Adept は newco_data7g.py(2026年11月の調達を反映)
from newco_data7g import CO7G
CO7E.update(CO7G)
