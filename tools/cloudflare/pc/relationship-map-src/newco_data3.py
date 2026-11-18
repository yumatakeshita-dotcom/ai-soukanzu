from newco_data import mk, std, wp

CO3 = {}

# ================= ソフトバンクグループ =================
N = [
 {'id': 'softbank', 'name': 'SoftBank Group', 'kind': 'c', 'from': 2014, 'desc': 'OpenAIの大株主(約11〜13%と報じられています)で、Armの親会社。2025年にOpenAI、Oracleと巨大AIインフラ計画「スターゲート」を発表しました。2020年以降、取締役15人のうち11人が入れ替わり、ビジョン・ファンドの幹部も約半数が去ったと報じられています。'},
 # 現在の取締役・幹部
 {'id': 'son', 'name': '孫正義', 'kind': 'p', 'from': 2014, 'desc': '創業者で会長兼社長。スターゲートの会長を務めます。', 'role': '創業者 / 会長兼社長', 'founder': 1},
 {'id': 'goto', 'name': '後藤芳光', 'kind': 'p', 'from': 2014, 'desc': '取締役でCFO。', 'role': '取締役 / CFO'},
 {'id': 'miyauchi', 'name': '宮内謙', 'kind': 'p', 'from': 2014, 'desc': '取締役。長年、孫正義の右腕として国内の通信事業を率い、ソフトバンク(通信)の社長・会長を務めました。', 'role': '取締役'},
 {'id': 'haas', 'name': 'レネ・ハース', 'kind': 'p', 'from': 2022, 'desc': '取締役でArmのCEO。以前はNvidiaに在籍しました。', 'role': '取締役 / Arm CEO'},
 {'id': 'miyakawa', 'name': '宮川潤一', 'kind': 'p', 'from': 2021, 'desc': '通信子会社ソフトバンクの社長兼CEO。LINEヤフーの株をめぐるNAVERとの交渉に臨んだと報じられています。', 'role': 'ソフトバンク(通信)社長'},
 {'id': 'clavel', 'name': 'アレックス・クラベル', 'kind': 'p', 'from': 2024, 'desc': 'ビジョン・ファンドの運用会社の単独CEO。2024年11月にミスラが退き、一人で率いる体制になりました。', 'role': 'ファンド運用会社CEO'},
 # 社外取締役
 {'id': 'matsuo', 'name': '松尾豊', 'kind': 'p', 'from': 2025, 'desc': '社外取締役。東京大学の教授で、日本のAI研究の第一人者です。', 'role': '社外取締役'},
 {'id': 'siegel', 'name': 'ケン・シーゲル', 'kind': 'p', 'from': 2020, 'desc': '社外取締役。', 'role': '社外取締役'},
 {'id': 'chao', 'name': 'デビッド・チャオ', 'kind': 'p', 'from': 2020, 'desc': '社外取締役。ベンチャーキャピタルDCMの共同創業者として知られます。', 'role': '社外取締役'},
 {'id': 'erikawa', 'name': '襟川恵子', 'kind': 'p', 'from': 2025, 'desc': '社外取締役。ゲーム会社コーエーテクモの経営者です。', 'role': '社外取締役'},
 {'id': 'iijima', 'name': '飯島彰己', 'kind': 'p', 'from': 2020, 'to': 2026, 'desc': '元三井物産の会長。2026年6月の株主総会で退任する予定と発表されました。', 'role': '元社外取締役'},
 {'id': 'ohashi', 'name': '大橋徹二', 'kind': 'p', 'from': 2026, 'desc': '元コマツのCEO。2026年6月の株主総会で、新任の取締役候補とされました。', 'role': '社外取締役(新任)'},
 # 元幹部
 {'id': 'arora', 'name': 'ニケシュ・アローラ', 'kind': 'p', 'from': 2014, 'to': 2016, 'desc': '元Google幹部。2014年に副会長に就任し、2015年に孫正義が後継者候補と認めたものの、2016年6月に退任しました。', 'role': '元副会長'},
 {'id': 'claure', 'name': 'マルセロ・クラウレ', 'kind': 'p', 'from': 2014, 'to': 2020, 'desc': '元COOで、米Sprintの会長も務めました。2020年11月に取締役を退任しました。', 'role': '元COO'},
 {'id': 'misra', 'name': 'ラジーブ・ミスラ', 'kind': 'p', 'from': 2014, 'to': 2020, 'desc': 'ビジョン・ファンドを率いた元幹部。2020年11月に取締役を退任し、2024年11月にファンド運用会社の共同トップも退きました。', 'role': '元ビジョン・ファンド責任者'},
 {'id': 'jackma', 'name': 'ジャック・マー', 'kind': 'p', 'from': 2014, 'to': 2020, 'desc': 'アリババの創業者。孫正義の長年の盟友で、2007年から2020年まで取締役を務めました。', 'role': '元取締役'},
 # 出資者
 {'id': 'pif', 'name': 'Saudi PIF', 'kind': 'i', 'from': 2016, 'desc': 'サウジアラビアの政府系ファンド。ビジョン・ファンドの最大の出資者(約450億ドル)。', 'role': '政府系ファンド'},
 {'id': 'mubadala', 'name': 'Mubadala', 'kind': 'i', 'from': 2016, 'desc': 'アブダビの政府系ファンド。ビジョン・ファンドの出資者。', 'role': '政府系ファンド'},
 {'id': 'apple', 'name': 'Apple', 'kind': 'i', 'from': 2017, 'desc': 'ビジョン・ファンドの出資者の一社と報じられています。', 'role': 'ファンドの出資者'},
 {'id': 'foxconn', 'name': 'Foxconn', 'kind': 'i', 'from': 2017, 'desc': 'ビジョン・ファンドの出資者の一社と報じられています。', 'role': 'ファンドの出資者'},
 {'id': 'qualcomm', 'name': 'Qualcomm', 'kind': 'i', 'from': 2017, 'desc': 'ビジョン・ファンドの出資者の一社と報じられています。', 'role': 'ファンドの出資者'},
 # 関連組織・投資先
 {'id': 'arm', 'name': 'Arm', 'kind': 'o', 'from': 2016, 'desc': '2016年に約3.3兆円で買収した半導体設計会社。', 'role': '子会社'},
 {'id': 'visionfund', 'name': 'Vision Fund', 'kind': 'o', 'from': 2017, 'desc': '2017年に設立した巨大な投資ファンド。', 'role': '投資ファンド'},
 {'id': 'softbankcorp', 'name': 'SoftBank Corp.', 'kind': 'o', 'from': 2014, 'desc': '上場している通信子会社。宮内氏、のち宮川氏が率いました。', 'role': '通信の子会社'},
 {'id': 'ly', 'name': 'LY Corporation', 'kind': 'o', 'from': 2019, 'desc': 'LINEヤフー。SoftBankとNAVERの共同の傘下で、A Holdings経由で約62.5%を保有(2024年の自己株買い後)と報じられています。', 'role': '共同で支配'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2024, 'desc': '2025年に約400億ドルを投資する取引が完了し、約11%を持つと報じられています(13%とする報道もあります)。', 'role': '大株主'},
 {'id': 'stargate', 'name': 'Stargate', 'kind': 'o', 'from': 2025, 'desc': 'OpenAI、Oracleと共に2025年1月に発表した、巨大なAIデータセンター計画。孫正義が会長。', 'role': '共同計画'},
 {'id': 'oracle', 'name': 'Oracle', 'kind': 'o', 'from': 2025, 'desc': 'スターゲートの共同パートナー。', 'role': '共同パートナー'},
 {'id': 'alibaba', 'name': 'Alibaba', 'kind': 'o', 'from': 2014, 'desc': '2000年に出資した中国のEC企業。大きな利益を生んだ投資として知られます。', 'role': '過去の大型投資'},
 {'id': 'ampere', 'name': 'Ampere', 'kind': 'o', 'from': 2025, 'desc': '米国の半導体設計会社。SoftBankによる買収が2025年に報じられました。', 'role': '買収(報道)'},
 {'id': 'wework', 'name': 'WeWork', 'kind': 'o', 'from': 2017, 'desc': 'シェアオフィス。大型の出資が行き詰まり、2019年に救済、2023年に破綻したと報じられています。', 'role': '投資の失敗例'},
 {'id': 'sprint', 'name': 'Sprint', 'kind': 'o', 'from': 2014, 'desc': '2013年に買収した米国の通信会社。2020年にT-Mobileと合併。', 'role': '元子会社'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'o', 'from': 2016, 'desc': 'SoftBankは保有株を全て売却したと報じられています。ハースの前の勤務先でもあります。', 'role': '売却(報道)'},
 {'id': 'altman', 'name': 'サム・アルトマン', 'kind': 'o', 'from': 2024, 'desc': 'OpenAIのCEO。出資とスターゲートで連携しています。', 'role': 'OpenAI CEO'},
 {'id': 'ellison', 'name': 'ラリー・エリソン', 'kind': 'o', 'from': 2025, 'desc': 'Oracleの共同創業者。スターゲートの共同パートナー。', 'role': 'スターゲートの共同パートナー'},
]
E = (std('softbank') +
 "E.push({a:'softbank',b:'arm',k:'owns',label:'約9割を保有'});\n"
 "E.push({a:'softbank',b:'visionfund',k:'owns'});\n"
 "E.push({a:'softbank',b:'softbankcorp',k:'owns',label:'上場子会社'});\n"
 "E.push({a:'softbank',b:'ly',k:'owns',label:'A Holdings経由(NAVERと共同)',since:2019});\n"
 "E.push({a:'softbank',b:'openai',k:'invest2',label:'約11〜13%(報道)',since:2024});\n"
 "E.push({a:'softbank',b:'alibaba',k:'invest2',label:'2000年に出資'});\n"
 "E.push({a:'softbank',b:'ampere',k:'invest2',since:2025});\n"
 "E.push({a:'softbank',b:'wework',k:'invest2',label:'2019年に救済'});\n"
 "E.push({a:'softbank',b:'sprint',k:'owns',label:'2020年にT-Mobileと合併'});\n"
 "E.push({a:'softbank',b:'stargate',k:'link',since:2025});\n"
 "E.push({a:'softbank',b:'nvidia',k:'link',label:'株式を売却(報道)'});\n"
 "E.push({a:'altman',b:'openai',k:'link'});\n"
 "E.push({a:'ellison',b:'oracle',k:'link'});\n"
 "E.push({a:'oracle',b:'stargate',k:'link'});\n"
 "E.push({a:'son',b:'jackma',k:'link',label:'盟友'});\n"
 "E.push({a:'jackma',b:'alibaba',k:'link',label:'創業'});\n"
 "E.push({a:'haas',b:'arm',k:'link'});\n"
 "E.push({a:'haas',b:'nvidia',k:'from'});\n"
 "E.push({a:'claure',b:'sprint',k:'link',label:'会長'});\n"
 "E.push({a:'claure',b:'wework',k:'link',label:'会長を兼任',since:2019});\n"
 "E.push({a:'misra',b:'visionfund',k:'link',label:'率いた'});\n"
 "E.push({a:'clavel',b:'visionfund',k:'link',label:'率いる',since:2024});\n"
 "E.push({a:'miyauchi',b:'softbankcorp',k:'link'});\n"
 "E.push({a:'miyakawa',b:'softbankcorp',k:'link',label:'社長'});\n\n")
CO3['softbank'] = mk(N, E,
 {'son': 'Masayoshi Son', 'goto': 'Yoshimitsu Goto', 'miyauchi': 'Ken Miyauchi', 'haas': 'Rene Haas', 'miyakawa': 'Junichi Miyakawa', 'clavel': 'Alex Clavel',
  'matsuo': 'Yutaka Matsuo', 'siegel': 'Ken Siegel', 'chao': 'David Chao', 'erikawa': 'Keiko Erikawa', 'iijima': 'Akimi Iijima', 'ohashi': 'Tetsuji Ohashi',
  'arora': 'Nikesh Arora', 'claure': 'Marcelo Claure', 'misra': 'Rajeev Misra', 'jackma': 'Jack Ma', 'altman': 'Sam Altman', 'ellison': 'Larry Ellison'},
 {'son': 'masason', 'haas': 'renehaas', 'altman': 'sama', 'softbank': 'softbank', 'openai': 'OpenAI', 'arora': 'nikesharora'},
 {'softbank': 'https://group.softbank', 'arm': 'https://www.arm.com', 'openai': 'https://openai.com', 'oracle': 'https://www.oracle.com', 'softbankcorp': 'https://www.softbank.jp'},
 wp(('softbank', 'SoftBank_Group'), ('arm', 'Arm_Holdings'), ('visionfund', 'SoftBank_Vision_Fund'), ('softbankcorp', 'SoftBank_Corp.'), ('ly', 'LY_Corporation'), ('openai', 'OpenAI'),
    ('stargate', 'Stargate_LLC'), ('alibaba', 'Alibaba_Group'), ('ampere', 'Ampere_Computing'), ('oracle', 'Oracle_Corporation'), ('wework', 'WeWork'), ('sprint', 'Sprint_Corporation'),
    ('nvidia', 'Nvidia'), ('pif', 'Public_Investment_Fund'), ('mubadala', 'Mubadala'), ('apple', 'Apple_Inc.'), ('foxconn', 'Foxconn'), ('qualcomm', 'Qualcomm')),
 {'son': [['1981', 'ソフトバンクを創業'], ['2000', 'アリババに出資'], ['2016', 'Armを買収'], ['2017', 'ビジョン・ファンドを設立'], ['2025', 'OpenAI・Oracleとスターゲートを発表']],
  'arora': [['2004', 'Googleに入社'], ['2014', 'ソフトバンク副会長に就任'], ['2016', '6月に退任']]},
 {}, 'softbank')

# ================= Sakana AI =================
N = [
 {'id': 'sakana', 'name': 'Sakana AI', 'kind': 'c', 'from': 2023, 'desc': '2023年に東京で設立されたAI企業。2024年1月に約45億円、2024年9月のシリーズAで約300億円、2025年11月のシリーズBで約200億円(評価額は約4,000億円)を調達し、累計は約520億円と報じられています。2026年1月にGoogleとの戦略的な提携と出資を発表しました。'},
 {'id': 'ha', 'name': 'デイビッド・ハ', 'kind': 'p', 'from': 2023, 'desc': '共同創業者でCEO。元Google Brainの研究者です。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'jones', 'name': 'リオン・ジョーンズ', 'kind': 'p', 'from': 2023, 'desc': '共同創業者でCTO。AIの基盤「トランスフォーマー」の論文「Attention Is All You Need」の共著者の一人です。', 'role': 'CTO / 共同創業者', 'founder': 1},
 {'id': 'ito', 'name': '伊藤錬', 'kind': 'p', 'from': 2023, 'desc': '共同創業者。COOとして紹介されることが多く、代表取締役社長と表記する記事もあります(資料により食い違い)。元外務省、元メルカリです。', 'role': 'COO / 共同創業者', 'founder': 1},
 # シード(2024年1月)
 {'id': 'lux', 'name': 'Lux Capital', 'kind': 'i', 'from': 2023, 'desc': 'シード(初期)を主導したと報じられています。', 'role': 'VC'},
 {'id': 'ntt', 'name': 'NTT', 'kind': 'i', 'from': 2024, 'desc': '2024年1月のシードに参加と報じられています。', 'role': '国内の大手企業'},
 {'id': 'kddi', 'name': 'KDDI', 'kind': 'i', 'from': 2024, 'desc': '2024年1月のシードに参加と報じられています。シリーズAにも参加。', 'role': '国内の大手企業'},
 {'id': 'sony', 'name': 'Sony Group', 'kind': 'i', 'from': 2024, 'desc': '2024年1月のシードに参加と報じられています。', 'role': '国内の大手企業'},
 # シリーズA(2024年9月)
 {'id': 'nea', 'name': 'NEA', 'kind': 'i', 'from': 2024, 'desc': '2024年9月のシリーズAに参加と報じられています。', 'role': 'VC'},
 {'id': 'khosla', 'name': 'Khosla Ventures', 'kind': 'i', 'from': 2024, 'desc': '2024年9月のシリーズAに参加と報じられています。', 'role': 'VC'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2024, 'desc': '2024年9月のシリーズAに出資と報じられています。', 'role': '出資 + GPU供給'},
 {'id': 'mufg', 'name': 'MUFG', 'kind': 'i', 'from': 2024, 'desc': '三菱UFJフィナンシャル・グループ。2024年のシリーズAに参加し、2025年に戦略的パートナーシップを発表と報じられています。', 'role': '国内の金融グループ'},
 {'id': 'smbc', 'name': 'SMBC', 'kind': 'i', 'from': 2024, 'desc': '三井住友銀行。2024年のシリーズAに参加と報じられています。', 'role': '国内の金融グループ'},
 {'id': 'mizuho', 'name': 'Mizuho', 'kind': 'i', 'from': 2024, 'desc': 'みずほフィナンシャルグループ。2024年のシリーズAに参加と報じられています。', 'role': '国内の金融グループ'},
 {'id': 'nec', 'name': 'NEC', 'kind': 'i', 'from': 2024, 'desc': '2024年のシリーズAに参加と報じられています。', 'role': '国内の大手企業'},
 {'id': 'sbi', 'name': 'SBI Group', 'kind': 'i', 'from': 2024, 'desc': '2024年のシリーズAに参加と報じられています。', 'role': '国内の金融グループ'},
 {'id': 'daiichi', 'name': 'Dai-ichi Life', 'kind': 'i', 'from': 2024, 'desc': '第一生命。2024年のシリーズAに参加と報じられています。', 'role': '国内の金融グループ'},
 {'id': 'fujitsu', 'name': 'Fujitsu', 'kind': 'i', 'from': 2024, 'desc': '富士通。2024年のシリーズAに参加と報じられています。', 'role': '国内の大手企業'},
 {'id': 'nomura', 'name': 'Nomura', 'kind': 'i', 'from': 2024, 'desc': '野村ホールディングス。2024年のシリーズAに参加と報じられています。', 'role': '国内の金融グループ'},
 # シリーズB(2025年11月)以降
 {'id': 'daiwa', 'name': 'Daiwa Securities', 'kind': 'i', 'from': 2025, 'desc': '大和証券グループ。2025年に戦略的パートナーシップを発表と報じられています。', 'role': '国内の金融グループ'},
 {'id': 'santander', 'name': 'Santander', 'kind': 'i', 'from': 2025, 'desc': 'スペインの金融グループ。傘下のVCファンド(Mouro Capital)を通じて、シリーズBに参加と報じられています。', 'role': '海外の金融グループ'},
 {'id': 'citi', 'name': 'Citigroup', 'kind': 'i', 'from': 2025, 'desc': 'シリーズBの後に、戦略的な投資を発表と報じられています。', 'role': '海外の金融グループ'},
 {'id': 'google', 'name': 'Google', 'kind': 'i', 'from': 2026, 'desc': '2026年1月に、戦略的な提携と出資を発表と報じられています。', 'role': '戦略出資者'},
 {'id': 'googlebrain', 'name': 'Google Brain', 'kind': 'o', 'from': 2023, 'desc': 'ハとジョーンズの出身元。', 'role': '出身元'},
 {'id': 'mofa', 'name': 'Ministry of Foreign Affairs', 'kind': 'o', 'from': 2023, 'desc': '伊藤氏の出身元(外務省)。', 'role': '出身元'},
 {'id': 'mercari', 'name': 'Mercari', 'kind': 'o', 'from': 2023, 'desc': '伊藤氏の出身元(メルカリ)。', 'role': '出身元'},
]
E = (std('sakana') + "['ha','jones'].forEach(a=>E.push({a,b:'googlebrain',k:'from'}));\nE.push({a:'ito',b:'mofa',k:'from'});\nE.push({a:'ito',b:'mercari',k:'from'});\n\n")
CO3['sakana'] = mk(N, E, {'ha': 'David Ha', 'jones': 'Llion Jones', 'ito': 'Ren Ito'},
 {'ha': 'hardmaru', 'jones': 'YesThisIsLion', 'sakana': 'SakanaAILabs', 'nvidia': 'nvidia'},
 {'sakana': 'https://sakana.ai', 'nvidia': 'https://www.nvidia.com', 'khosla': 'https://www.khoslaventures.com', 'lux': 'https://www.luxcapital.com', 'ntt': 'https://group.ntt', 'kddi': 'https://www.kddi.com',
  'sony': 'https://www.sony.com', 'nec': 'https://jpn.nec.com', 'fujitsu': 'https://global.fujitsu'},
 wp(('sakana', 'Sakana_AI'), ('nvidia', 'Nvidia'), ('khosla', 'Khosla_Ventures'), ('lux', 'Lux_Capital'), ('nea', 'New_Enterprise_Associates'), ('mufg', 'Mitsubishi_UFJ_Financial_Group'),
    ('smbc', 'Sumitomo_Mitsui_Banking_Corporation'), ('mizuho', 'Mizuho_Financial_Group'), ('nec', 'NEC'), ('sbi', 'SBI_Holdings'), ('daiichi', 'Dai-ichi_Life'), ('fujitsu', 'Fujitsu'),
    ('nomura', 'Nomura_Holdings'), ('daiwa', 'Daiwa_Securities_Group'), ('santander', 'Santander_Group'), ('citi', 'Citigroup'), ('google', 'Google'), ('googlebrain', 'Google_Brain'),
    ('ntt', 'Nippon_Telegraph_and_Telephone'), ('kddi', 'KDDI'), ('sony', 'Sony_Group'), ('mercari', 'Mercari')),
 {'jones': [['〜', 'Googleで「Attention Is All You Need」を共著'], ['2023', 'Sakana AIを共同創業']], 'ha': [['〜', 'Google Brainの研究者'], ['2023', 'Sakana AIを共同創業']]},
 {'ha': [['ブログ', 'https://blog.otoro.net']]}, 'sakana')

# ================= Preferred Networks =================
N = [
 {'id': 'pfn', 'name': 'Preferred Networks', 'kind': 'c', 'from': 2014, 'desc': '2014年に、Preferred Infrastructureの事業から分社化して設立された、日本を代表するAI企業。深層学習と、独自のAI半導体を開発。従業員は約400人(2026年3月)。'},
 {'id': 'nishikawa', 'name': '西川徹', 'kind': 'p', 'from': 2014, 'desc': '共同創業者で代表取締役会長(2026年3月の会社概要)。', 'role': '会長 / 共同創業者', 'founder': 1},
 {'id': 'okanohara', 'name': '岡野原大輔', 'kind': 'p', 'from': 2014, 'desc': '共同創業者で代表取締役社長(2026年3月の会社概要)。Preferred ElementsのCEOも兼ねます。', 'role': '社長 / 共同創業者', 'founder': 1},
 {'id': 'koizumi', 'name': '小泉愼一', 'kind': 'p', 'from': 2020, 'desc': '社外取締役(2024年12月時点の資料)。', 'role': '社外取締役'},
 {'id': 'morikawa', 'name': '森川博之', 'kind': 'p', 'from': 2020, 'desc': '社外取締役(2024年12月時点の資料)。東京大学の教授です。', 'role': '社外取締役'},
 {'id': 'masuda', 'name': '増田要', 'kind': 'p', 'from': 2020, 'desc': '社外取締役(2024年12月時点の資料)。', 'role': '社外取締役'},
 {'id': 'toyota', 'name': 'Toyota', 'kind': 'i', 'from': 2014, 'desc': 'トヨタ自動車。主要な出資者として報じられています。', 'role': '出資者'},
 {'id': 'fanuc', 'name': 'Fanuc', 'kind': 'i', 'from': 2014, 'desc': 'ファナック。主要な出資者として報じられています。', 'role': '出資者'},
 {'id': 'ntt', 'name': 'NTT', 'kind': 'i', 'from': 2018, 'desc': 'PFN全体の出資企業として挙げられています。', 'role': '出資者'},
 {'id': 'hitachi', 'name': 'Hitachi', 'kind': 'i', 'from': 2018, 'desc': '日立製作所。PFN全体の出資企業として挙げられています。', 'role': '出資者'},
 {'id': 'mitsui', 'name': 'Mitsui & Co.', 'kind': 'i', 'from': 2018, 'desc': '三井物産。PFN全体の出資企業として挙げられています。', 'role': '出資者'},
 {'id': 'pfi', 'name': 'Preferred Infrastructure', 'kind': 'o', 'from': 2014, 'desc': '2006年に西川氏と岡野原氏が共同創業した会社。PFNの元になった事業の母体。', 'role': '母体'},
 {'id': 'utokyo', 'name': 'University of Tokyo', 'kind': 'o', 'from': 2014, 'desc': '二人が出会い、共に創業した起点の大学。', 'role': '出身校'},
 {'id': 'matlantis', 'name': 'Matlantis', 'kind': 'o', 'from': 2021, 'desc': '材料探索のAIサービスの会社。PFNとENEOSの共同事業と報じられています。', 'role': '子会社'},
 {'id': 'probots', 'name': 'Preferred Robotics', 'kind': 'o', 'from': 2021, 'desc': 'ロボットの子会社。', 'role': '子会社'},
 {'id': 'pci', 'name': 'Preferred Computing Infrastructure', 'kind': 'o', 'from': 2025, 'desc': '2025年1月に、三菱商事・IIJと設立した合弁会社。計算基盤を担います。', 'role': '合弁会社'},
 {'id': 'pfe', 'name': 'Preferred Elements', 'kind': 'o', 'from': 2023, 'desc': '2023年11月に設立された、マルチモーダルの基盤モデルを開発・販売する子会社。', 'role': '子会社'},
 {'id': 'pfcc', 'name': 'Preferred Computational Chemistry', 'kind': 'o', 'from': 2021, 'desc': '計算化学の子会社(2024年の資料)。', 'role': '子会社'},
 {'id': 'mitsubishi', 'name': 'Mitsubishi Corporation', 'kind': 'o', 'from': 2025, 'desc': '三菱商事。合弁のPreferred Computing Infrastructureのパートナー。', 'role': '合弁のパートナー'},
 {'id': 'iij', 'name': 'IIJ', 'kind': 'o', 'from': 2025, 'desc': 'インターネットイニシアティブ。合弁のPreferred Computing Infrastructureのパートナー。', 'role': '合弁のパートナー'},
]
E = (std('pfn') +
 "['nishikawa','okanohara'].forEach(a=>E.push({a,b:'pfi',k:'from'}));\n['nishikawa','okanohara'].forEach(a=>E.push({a,b:'utokyo',k:'from'}));\n"
 "E.push({a:'pfi',b:'pfn',k:'owns',label:'2014年に分社化'});\n['matlantis','probots','pfe','pfcc'].forEach(b=>E.push({a:'pfn',b,k:'owns'}));\n"
 "E.push({a:'pfn',b:'pci',k:'link',label:'合弁(2025年1月)'});\nE.push({a:'mitsubishi',b:'pci',k:'link'});\nE.push({a:'iij',b:'pci',k:'link'});\n"
 "E.push({a:'okanohara',b:'pfe',k:'link',label:'CEOを兼任'});\nE.push({a:'morikawa',b:'utokyo',k:'link',label:'教授'});\n\n")
CO3['pfn'] = mk(N, E, {'nishikawa': 'Toru Nishikawa', 'okanohara': 'Daisuke Okanohara', 'koizumi': 'Shinichi Koizumi', 'morikawa': 'Hiroyuki Morikawa', 'masuda': 'Kaname Masuda'},
 {'pfn': 'PreferredNetworks'}, {'pfn': 'https://www.preferred.jp', 'toyota': 'https://global.toyota', 'fanuc': 'https://www.fanuc.co.jp', 'hitachi': 'https://www.hitachi.co.jp', 'ntt': 'https://group.ntt', 'mitsui': 'https://www.mitsui.com'},
 wp(('pfn', 'Preferred_Networks'), ('toyota', 'Toyota'), ('fanuc', 'Fanuc'), ('ntt', 'Nippon_Telegraph_and_Telephone'), ('hitachi', 'Hitachi'), ('mitsui', 'Mitsui_%26_Co.'),
    ('utokyo', 'University_of_Tokyo'), ('mitsubishi', 'Mitsubishi_Corporation'), ('iij', 'Internet_Initiative_Japan')),
 {'nishikawa': [['2006', 'Preferred Infrastructureを共同創業'], ['2014', 'Preferred Networksを設立'], ['2025', '11月に会長に(報道)']],
  'okanohara': [['2006', 'Preferred Infrastructureを共同創業'], ['2014', 'Preferred Networksを設立'], ['2023', 'Preferred ElementsのCEOに'], ['2025', '11月に社長に(報道)']]}, {}, 'pfn')

# ================= PKSHA Technology =================
N = [
 {'id': 'pksha', 'name': 'PKSHA Technology', 'kind': 'c', 'from': 2012, 'desc': '2012年に東京大学の松尾研究室の出身者らが設立した、日本のAIソフトウェア企業。自然言語処理や画像認識を、企業向けに提供しています。2025年9月期の連結売上高は約218億円。M&Aで子会社を増やしています。'},
 {'id': 'uenoyama', 'name': '上野山勝也', 'kind': 'p', 'from': 2012, 'desc': '代表取締役で筆頭株主(約30%、情報源により29.5〜34.1%)。松尾研究室の出身で、2012年にPKSHAを創業しました。', 'role': '代表取締役 / 創業者', 'founder': 1},
 {'id': 'yamada', 'name': '山田尚史', 'kind': 'p', 'from': 2012, 'desc': '創業者の一人で、安定株主(約7.5%)と開示されています。', 'role': '創業者', 'founder': 1},
 {'id': 'toyota', 'name': 'Toyota', 'kind': 'i', 'from': 2018, 'desc': 'トヨタ自動車。少数株主(約2.5%)として挙がっています。', 'role': '少数株主'},
 {'id': 'luce', 'name': 'LUCE Capital', 'kind': 'i', 'from': 2018, 'desc': '約3.6%を保有する株主として挙がっています。', 'role': '株主'},
 {'id': 'matsuo', 'name': '松尾豊', 'kind': 'o', 'from': 2012, 'desc': '東京大学の教授で、日本のAI研究の第一人者。上野山氏が学んだ松尾研究室を率い、ソフトバンクグループの社外取締役も務めます。', 'role': '研究室の指導者'},
 {'id': 'utokyo', 'name': 'University of Tokyo', 'kind': 'o', 'from': 2012, 'desc': '創業者らの出身大学。', 'role': '出身校'},
 {'id': 'pkshacap', 'name': 'PKSHA Technology Capital', 'kind': 'o', 'from': 2020, 'desc': 'ベンチャー投資を担う子会社(合同会社)。', 'role': '子会社'},
 {'id': 'itec', 'name': 'ITEC', 'kind': 'o', 'from': 2022, 'desc': '株式会社アイテック。子会社で、Physical AIの事業などを担うと報じられています。', 'role': '子会社'},
 {'id': 'pkshaassoc', 'name': 'PKSHA Associates', 'kind': 'o', 'from': 2022, 'desc': '子会社。', 'role': '子会社'},
 {'id': 'triumph', 'name': 'Triumph', 'kind': 'o', 'from': 2024, 'desc': '株式会社トライアンフ。2024年4月に子会社化を決議。', 'role': '子会社(2024年)'},
 {'id': 'ernie', 'name': 'Ernie MLG', 'kind': 'o', 'from': 2024, 'desc': 'アーニーMLG株式会社。2024年12月に、追加取得して子会社化を決議。', 'role': '子会社(2024年)'},
 {'id': 'extone', 'name': 'Extone', 'kind': 'o', 'from': 2025, 'desc': '株式会社エクストーン。2025年1月に、子会社化を決議。', 'role': '子会社(2025年)'},
 {'id': 'infinity', 'name': 'PKSHA Infinity', 'kind': 'o', 'from': 2024, 'desc': '子会社。', 'role': '子会社'},
]
E = (std('pksha') + "E.push({a:'uenoyama',b:'matsuo',k:'from'});\nE.push({a:'matsuo',b:'utokyo',k:'link'});\nE.push({a:'uenoyama',b:'utokyo',k:'from'});\n"
 "['pkshacap','itec','pkshaassoc','triumph','ernie','extone','infinity'].forEach(b=>E.push({a:'pksha',b,k:'owns'}));\n\n")
CO3['pksha'] = mk(N, E, {'uenoyama': 'Katsuya Uenoyama', 'yamada': 'Naofumi Yamada', 'matsuo': 'Yutaka Matsuo'}, {},
 {'pksha': 'https://pkshatech.com', 'toyota': 'https://global.toyota'}, wp(('pksha', 'PKSHA_Technology'), ('toyota', 'Toyota'), ('utokyo', 'University_of_Tokyo')),
 {'uenoyama': [['〜', '東京大学の松尾研究室で研究'], ['2012', 'PKSHA Technologyを創業'], ['2016', '代表取締役に就任']]}, {}, 'pksha')

# ================= 楽天グループ =================
N = [
 {'id': 'rakuten', 'name': 'Rakuten', 'kind': 'c', 'from': 2003, 'desc': '三木谷浩史氏が創業した、ECと通信と金融の企業グループ。2023年にOpenAIと生成AIで協業に合意。2026年3月に、国産の大規模言語モデル「Rakuten AI 3.0」(約7,000億パラメータ)を公開しました。'},
 {'id': 'mikitani', 'name': '三木谷浩史', 'kind': 'p', 'from': 2003, 'desc': '創業者で会長兼社長。', 'role': '創業者 / 会長兼社長', 'founder': 1},
 {'id': 'momono', 'name': '百野研太郎', 'kind': 'p', 'from': 2025, 'desc': '代表取締役で副社長。2025年3月の株主総会で、三木谷氏と共に代表取締役に挙げられました。元トヨタ自動車の出身と紹介されています。', 'role': '代表取締役副社長'},
 {'id': 'hosaka', 'name': '穂坂雅之', 'kind': 'p', 'from': 2003, 'to': 2025, 'desc': '元代表取締役副会長。2025年3月28日の株主総会をもって任期満了で退任しました。', 'role': '元副会長'},
 {'id': 'murai', 'name': '村井純', 'kind': 'p', 'from': 2003, 'to': 2025, 'desc': '日本のインターネットの草分けとされる学者。取締役を務め、2025年3月に退任しました。', 'role': '元社外取締役'},
 {'id': 'takeda', 'name': '武田和徳', 'kind': 'p', 'from': 2003, 'to': 2025, 'desc': '取締役。2025年3月に退任しました。', 'role': '元取締役'},
 {'id': 'ozawa', 'name': '小澤隆生', 'kind': 'p', 'from': 2003, 'to': 2006, 'desc': '2003年にビズシークの合併で楽天に入社。オークションと野球団の役員を務め、2006年に楽天を離れ、のち顧問(2009〜2012年)になりました。', 'role': '元役員'},
 {'id': 'jpost', 'name': 'Japan Post Holdings', 'kind': 'i', 'from': 2021, 'desc': '日本郵政。2021年に約1,500億円を出資しました。', 'role': '出資者'},
 {'id': 'tencent', 'name': 'Tencent', 'kind': 'i', 'from': 2021, 'desc': '2021年に約657億円を出資しました。', 'role': '出資者'},
 {'id': 'walmart', 'name': 'Walmart', 'kind': 'i', 'from': 2021, 'desc': '2021年に出資し、西友などで提携。', 'role': '出資者'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2023, 'desc': '2023年に協業に合意。同年11月に戦略的パートナーとして参画。通信業界向けのAIツールを共同開発すると2024年に発表。', 'role': '戦略的パートナー'},
 {'id': 'altman', 'name': 'サム・アルトマン', 'kind': 'o', 'from': 2023, 'desc': 'OpenAIのCEO。2023年から楽天と提携しています。', 'role': 'OpenAIのCEO'},
 {'id': 'ai3', 'name': 'Rakuten AI 3.0', 'kind': 'o', 'from': 2026, 'desc': '2026年3月17日に公開した、日本語に強い大規模言語モデル(約7,000億パラメータ)。商用利用できるライセンスで無償公開されています。', 'role': '自社のAIモデル'},
 {'id': 'geniac', 'name': 'GENIAC', 'kind': 'o', 'from': 2024, 'desc': '経済産業省とNEDOが進める、生成AIの開発支援プロジェクト。Rakuten AI 3.0はこの支援で構築されました。', 'role': '国の開発支援'},
 {'id': 'mobile', 'name': 'Rakuten Mobile', 'kind': 'o', 'from': 2020, 'desc': '2020年に本格参入した携帯電話事業。', 'role': '通信事業'},
 {'id': 'softbank', 'name': 'SoftBank Group', 'kind': 'o', 'from': 2020, 'desc': '携帯電話市場での競合。', 'role': '競合'},
 {'id': 'bizseek', 'name': 'Bizseek', 'kind': 'o', 'from': 2003, 'desc': '小澤氏が1999年に創業し、楽天に統合されたネットオークションの会社。', 'role': '小澤氏が創業'},
 {'id': 'eagles', 'name': 'Rakuten Eagles', 'kind': 'o', 'from': 2004, 'desc': '2004年に参入したプロ野球球団。小澤氏は2005年に取締役事業本部長を務めました。', 'role': '野球団'},
]
E = (std('rakuten') +
 "E.push({a:'rakuten',b:'openai',k:'link',label:'2023年に協業'});\nE.push({a:'altman',b:'openai',k:'link'});\n"
 "E.push({a:'rakuten',b:'mobile',k:'owns'});\nE.push({a:'mobile',b:'softbank',k:'conflict',label:'携帯の競合'});\n"
 "E.push({a:'rakuten',b:'ai3',k:'owns',label:'2026年3月に公開'});\nE.push({a:'geniac',b:'ai3',k:'link',label:'開発支援'});\n"
 "E.push({a:'rakuten',b:'eagles',k:'owns'});\nE.push({a:'ozawa',b:'eagles',k:'link',label:'取締役'});\n"
 "E.push({a:'ozawa',b:'bizseek',k:'link',label:'創業'});\nE.push({a:'bizseek',b:'rakuten',k:'owns',label:'楽天に統合'});\n\n")
CO3['rakuten'] = mk(N, E, {'mikitani': 'Hiroshi Mikitani', 'momono': 'Kentaro Momono', 'hosaka': 'Masayuki Hosaka', 'murai': 'Jun Murai', 'takeda': 'Kazunori Takeda', 'ozawa': 'Takao Ozawa', 'altman': 'Sam Altman'},
 {'altman': 'sama', 'openai': 'OpenAI'}, {'rakuten': 'https://global.rakuten.com', 'openai': 'https://openai.com'},
 wp(('rakuten', 'Rakuten'), ('jpost', 'Japan_Post_Holdings'), ('tencent', 'Tencent'), ('walmart', 'Walmart'), ('openai', 'OpenAI'), ('mobile', 'Rakuten_Mobile'), ('softbank', 'SoftBank_Group'),
    ('eagles', 'Tohoku_Rakuten_Golden_Eagles')),
 {'mikitani': [['1997', '楽天を創業'], ['2023', 'OpenAIとの協業に合意'], ['2024', '通信向けAIツールを共同開発すると発表'], ['2026', 'Rakuten AI 3.0を公開']]}, {}, 'rakuten')

# ================= LINEヤフー =================
N = [
 {'id': 'ly', 'name': 'LY Corporation', 'kind': 'c', 'from': 2019, 'desc': '2019年にヤフーとLINEの経営統合が発表され、2023年に「LINEヤフー」が発足。SoftBankとNAVERの合弁会社A Holdingsが、約62.5%(2024年の自己株買い後)を持つと報じられています。2023〜24年の個人情報流出を受け、総務省が行政指導で、NAVERとの資本関係の見直しを求めました。'},
 {'id': 'idezawa', 'name': '出澤剛', 'kind': 'p', 'from': 2019, 'desc': '代表取締役社長。LINEの元CEO。NAVERに株式の売却を求めたと報じられています。2026年4月に、AIエージェント「Agent i」を始めたと報じられています。', 'role': '代表取締役社長CEO'},
 {'id': 'kawabe', 'name': '川邊健太郎', 'kind': 'p', 'from': 2019, 'to': 2026, 'desc': '元会長。2025年12月に、2026年6月の株主総会での退任を発表。退任後はAI分野での起業を目指していると報じられています。', 'role': '元会長'},
 {'id': 'softbank', 'name': 'SoftBank Group', 'kind': 'i', 'from': 2019, 'desc': 'NAVERと共に、A Holdingsを通じてLINEヤフーを支配します。', 'role': '親会社(共同)'},
 {'id': 'naver', 'name': 'NAVER', 'kind': 'i', 'from': 2019, 'desc': '韓国のIT企業。SoftBankと共にA Holdingsを通じて支配。総務省の行政指導で、資本関係の見直しを求められました。', 'role': '親会社(共同)'},
 {'id': 'ahold', 'name': 'A Holdings', 'kind': 'o', 'from': 2019, 'desc': 'SoftBankとNAVERの合弁会社。LINEヤフーの株を約62.5%保有(2024年の自己株買い後)と報じられています。', 'role': '合弁の持ち株会社'},
 {'id': 'miyakawa', 'name': '宮川潤一', 'kind': 'o', 'from': 2021, 'desc': '通信子会社ソフトバンクの社長兼CEO。NAVERとの株の買い取り交渉に臨んだと報じられています。', 'role': 'ソフトバンク社長'},
 {'id': 'miyauchi', 'name': '宮内謙', 'kind': 'o', 'from': 2019, 'desc': 'ソフトバンクグループの取締役。経営統合の発表時に、ソフトバンクの会長として関わりました。', 'role': 'ソフトバンクGの取締役'},
 {'id': 'choi', 'name': '崔秀妍', 'kind': 'o', 'from': 2024, 'desc': 'NAVERのCEO。総務省の行政指導をめぐる発言が紹介されています。', 'role': 'NAVER CEO'},
 {'id': 'lee', 'name': '李海珍', 'kind': 'o', 'from': 2019, 'desc': 'NAVERの創業者。LINEの生みの親としても知られます。', 'role': 'NAVER創業者'},
 {'id': 'miyasaka', 'name': '宮坂学', 'kind': 'o', 'from': 2019, 'desc': '元ヤフーの社長(2012〜2018年)。のち東京都の副知事を務めたと報じられています。', 'role': '元ヤフー社長'},
 {'id': 'ozawa', 'name': '小澤隆生', 'kind': 'o', 'from': 2019, 'desc': '元ヤフーの経営者。現在はBoost Capitalの代表で、LINEヤフーはそのアンカー出資者です。', 'role': '元ヤフー'},
 {'id': 'hori', 'name': '堀新一郎', 'kind': 'o', 'from': 2019, 'desc': 'ヤフーのYJキャピタルでCOO、Z Venture Capitalの社長を務め、現在はBoost Capitalの共同GP。', 'role': '元CVCの責任者'},
 {'id': 'paypay', 'name': 'PayPay', 'kind': 'o', 'from': 2019, 'desc': 'スマホ決済。川邊氏は、PayPayの黒字化を見届けたことを退任の理由に挙げたと報じられています。', 'role': '決済事業'},
 {'id': 'line', 'name': 'LINE', 'kind': 'o', 'from': 2019, 'desc': 'NAVER系のメッセージアプリ。2021年にヤフーと統合しました。', 'role': 'サービス'},
 {'id': 'mic', 'name': 'MIC Japan', 'kind': 'o', 'from': 2023, 'desc': '総務省。2023〜24年の個人情報流出を受けて、行政指導を行い、NAVERとの資本関係の見直しを求めました。', 'role': '行政'},
 {'id': 'boostcap', 'name': 'Boost Capital', 'kind': 'o', 'from': 2024, 'desc': '2024年にアンカー出資者として約100億円のファンドに参加と報じられています。', 'role': 'アンカー出資先'},
]
E = (std('ly') +
 "E.push({a:'ahold',b:'ly',k:'owns',label:'約62.5%(2024年)'});\nE.push({a:'softbank',b:'ahold',k:'link',label:'合弁'});\nE.push({a:'naver',b:'ahold',k:'link',label:'合弁'});\n"
 "E.push({a:'mic',b:'ly',k:'conflict',label:'行政指導(個人情報流出)',since:2023});\nE.push({a:'mic',b:'naver',k:'conflict',label:'資本関係の見直しを要請',since:2024});\n"
 "E.push({a:'ly',b:'paypay',k:'owns'});\nE.push({a:'ly',b:'line',k:'owns'});\nE.push({a:'lee',b:'line',k:'link',label:'生みの親'});\nE.push({a:'lee',b:'naver',k:'link',label:'創業者'});\nE.push({a:'choi',b:'naver',k:'link',label:'CEO'});\n"
 "E.push({a:'miyakawa',b:'softbank',k:'link',label:'ソフトバンク社長'});\nE.push({a:'miyauchi',b:'softbank',k:'link'});\n"
 "E.push({a:'ly',b:'boostcap',k:'invest2',label:'アンカー出資',since:2024});\nE.push({a:'ozawa',b:'boostcap',k:'link',label:'代表',since:2024});\nE.push({a:'hori',b:'boostcap',k:'link',label:'共同GP',since:2024});\n"
 "E.push({a:'miyasaka',b:'ozawa',k:'link',label:'元上司(ヤフー)'});\n\n")
CO3['ly'] = mk(N, E, {'idezawa': 'Takeshi Idezawa', 'kawabe': 'Kentaro Kawabe', 'miyakawa': 'Junichi Miyakawa', 'miyauchi': 'Ken Miyauchi', 'choi': 'Choi Soo-yeon', 'lee': 'Lee Hae-jin',
  'miyasaka': 'Manabu Miyasaka', 'ozawa': 'Takao Ozawa', 'hori': 'Shinichiro Hori'},
 {}, {'ly': 'https://www.lycorp.co.jp', 'softbank': 'https://group.softbank', 'naver': 'https://www.navercorp.com'},
 wp(('ly', 'LY_Corporation'), ('softbank', 'SoftBank_Group'), ('naver', 'Naver_Corporation'), ('paypay', 'PayPay'), ('line', 'Line_(software)')), {}, {}, 'ly')

# ================= ブースト =================
N = [
 {'id': 'boostcap', 'name': 'Boost Capital', 'kind': 'c', 'from': 2024, 'desc': '2024年1月に設立された、日本のIT系スタートアップに投資するベンチャーキャピタル。LINEヤフーが最初の出資者(アンカー)となり、複数の上場企業などから約100億円を集めたと報じられています。代表は小澤隆生氏。'},
 {'id': 'ozawa', 'name': '小澤隆生', 'kind': 'p', 'from': 2024, 'desc': '代表取締役で、共同ゼネラル・パートナー。元ヤフーの経営者で、楽天出身。2026年8月にラクスルの社外取締役にも就任しました。', 'role': '代表取締役 / 共同GP', 'founder': 1},
 {'id': 'hori', 'name': '堀新一郎', 'kind': 'p', 'from': 2024, 'desc': '共同ゼネラル・パートナー。ブーストコンサルティングの代表者とされます。ドリームインキュベータを経て、ヤフーのYJキャピタルでCOO、のちZ Venture Capitalの社長を務めました。', 'role': '共同GP / Boost Consulting代表', 'founder': 1},
 {'id': 'takahashi', 'name': '高橋健太', 'kind': 'p', 'from': 2024, 'desc': '共同ゼネラル・パートナー。マッキンゼー、MBKパートナーズを経て起業。在籍中にOMAKASEを創業して売却した経歴が紹介されています。', 'role': '共同GP', 'founder': 1},
 {'id': 'ly', 'name': 'LY Corporation', 'kind': 'i', 'from': 2024, 'desc': 'LINEヤフー。ファンドのアンカー出資者と報じられています(複数の上場企業も出資)。', 'role': 'アンカー出資者'},
 {'id': 'boostcons', 'name': 'Boost Consulting', 'kind': 'o', 'from': 2025, 'desc': 'ブーストコンサルティング株式会社。2025年4月に設立された、AIネイティブ型のコンサルティング会社。Boost Capitalを母体とし、AIコンサル、AI開発支援、新規事業支援、M&A支援を提供します。資本金は1億円、本社は東京都港区虎ノ門と、求人票に記載されています。', 'role': '母体を同じくする会社'},
 {'id': 'kotoba', 'name': 'Kotoba Technologies', 'kind': 'o', 'from': 2025, 'desc': '音声AIの会社。2025年のシードを主導と報じられています。', 'role': '投資先'},
 {'id': 'ivry', 'name': 'IVRy', 'kind': 'o', 'from': 2025, 'desc': '電話の自動応答AIの会社。2025年11月のシリーズDに参加と報じられています。', 'role': '投資先'},
 {'id': 'solafune', 'name': 'Solafune', 'kind': 'o', 'from': 2026, 'desc': '衛星データ解析の会社。2026年3月のシリーズAに参加と報じられています。', 'role': '投資先'},
 {'id': 'terass', 'name': 'TERASS', 'kind': 'o', 'from': 2025, 'desc': '不動産の仲介の会社。2025年7月のシリーズCに参加と報じられています。', 'role': '投資先'},
 {'id': 'raksul', 'name': 'Raksul', 'kind': 'o', 'from': 2026, 'desc': '印刷・物流のプラットフォーム。小澤氏が2026年8月に社外取締役に就任しました。', 'role': '社外取締役'},
 {'id': 'rakuten', 'name': 'Rakuten', 'kind': 'o', 'from': 2024, 'desc': '小澤氏の出身元。オークション事業の担当役員などを務めました。', 'role': '出身元'},
 {'id': 'yahoo', 'name': 'Yahoo Japan', 'kind': 'o', 'from': 2024, 'desc': '小澤氏が2012年に入社。堀氏もYJキャピタルなどで在籍しました。', 'role': '出身元'},
 {'id': 'mckinsey', 'name': 'McKinsey', 'kind': 'o', 'from': 2024, 'desc': '高橋氏の出身元。', 'role': '出身元'},
 {'id': 'mbk', 'name': 'MBK Partners', 'kind': 'o', 'from': 2024, 'desc': '高橋氏の出身元(PEファンド)。', 'role': '出身元'},
 {'id': 'dream', 'name': 'Dream Incubator', 'kind': 'o', 'from': 2024, 'desc': '堀氏の出身元(コンサルティングと投資)。', 'role': '出身元'},
]
E = (std('boostcap') +
 "E.push({a:'boostcap',b:'boostcons',k:'link',label:'母体を同じくする',since:2025});\nE.push({a:'hori',b:'boostcons',k:'link',label:'代表',since:2025});\nE.push({a:'ozawa',b:'boostcons',k:'link',label:'経営陣',since:2025});\n"
 "['kotoba','ivry','solafune','terass'].forEach(b=>E.push({a:'boostcap',b,k:'invest2'}));\n"
 "E.push({a:'ozawa',b:'raksul',k:'link',label:'社外取締役'});\nE.push({a:'ozawa',b:'rakuten',k:'from'});\nE.push({a:'ozawa',b:'yahoo',k:'from'});\nE.push({a:'hori',b:'yahoo',k:'from'});\n"
 "E.push({a:'takahashi',b:'mckinsey',k:'from'});\nE.push({a:'takahashi',b:'mbk',k:'from'});\nE.push({a:'hori',b:'dream',k:'from'});\n\n")
CO3['boost'] = mk(N, E, {'ozawa': 'Takao Ozawa', 'hori': 'Shinichiro Hori', 'takahashi': 'Kenta Takahashi'},
 {}, {'boostcap': 'https://boostcapital.co.jp'}, wp(('rakuten', 'Rakuten'), ('raksul', 'Raksul'), ('ly', 'LY_Corporation'), ('yahoo', 'Yahoo!_Japan'), ('mckinsey', 'McKinsey_%26_Company')),
 {'ozawa': [['1999', 'ビズシークを設立(のち楽天へ)'], ['2005', '楽天野球団の取締役事業本部長'], ['2011', 'クロコスを設立(のちヤフーへ売却)'], ['2012', 'ヤフーに入社'], ['2024', 'Boost Capitalを設立、代表に'], ['2026', 'ラクスルの社外取締役に']]},
 {}, 'boostcap')
