from newco_data import mk, std, wp

CO2 = {}

# ---------------- ブースト(Boost Capital / Boost Consulting) ----------------
N = [
 {'id': 'boostcap', 'name': 'Boost Capital', 'kind': 'c', 'from': 2024, 'desc': '2024年1月に設立された、日本のIT系スタートアップに投資するベンチャーキャピタル。LINEヤフーが最初の出資者(アンカー)となり、複数の上場企業などから約100億円を集めたと報じられています。代表は小澤隆生氏。'},
 {'id': 'ozawa', 'name': '小澤隆生', 'kind': 'p', 'from': 2024, 'desc': '代表取締役で、共同ゼネラル・パートナー。元ヤフーの経営者で、楽天出身。2026年8月にラクスルの社外取締役にも就任しました。', 'role': '代表取締役 / 共同GP', 'founder': 1},
 {'id': 'hori', 'name': '堀新一郎', 'kind': 'p', 'from': 2024, 'desc': '共同ゼネラル・パートナー。ドリームインキュベータを経て、ヤフーのYJキャピタルでCOO、のちZ Venture Capitalの社長を務めました。', 'role': '共同GP', 'founder': 1},
 {'id': 'takahashi', 'name': '高橋健太', 'kind': 'p', 'from': 2024, 'desc': '共同ゼネラル・パートナー。マッキンゼー、MBKパートナーズを経て起業。在籍中にOMAKASEを創業して売却した経歴が紹介されています。', 'role': '共同GP', 'founder': 1},
 {'id': 'ly', 'name': 'LY Corporation', 'kind': 'i', 'from': 2024, 'desc': 'LINEヤフー。ファンドのアンカー出資者と報じられています。', 'role': 'アンカー出資者'},
 {'id': 'boostcons', 'name': 'Boost Consulting', 'kind': 'o', 'from': 2024, 'desc': 'ブーストコンサルティング株式会社。元ヤフーの小澤氏が率い、AI活用を軸にした経営支援と実装を担う会社。Boost Capitalの投資先支援とつながりがあるとされます。設立時期は確認できていません。', 'role': '姉妹会社'},
 {'id': 'kotoba', 'name': 'Kotoba Technologies', 'kind': 'o', 'from': 2025, 'desc': '音声AIの会社。2025年のシードを主導と報じられています。', 'role': '投資先'},
 {'id': 'ivry', 'name': 'IVRy', 'kind': 'o', 'from': 2025, 'desc': '電話の自動応答AIの会社。2025年11月のシリーズDに参加と報じられています。', 'role': '投資先'},
 {'id': 'solafune', 'name': 'Solafune', 'kind': 'o', 'from': 2026, 'desc': '衛星データ解析の会社。2026年3月のシリーズAに参加と報じられています。', 'role': '投資先'},
 {'id': 'terass', 'name': 'TERASS', 'kind': 'o', 'from': 2025, 'desc': '不動産の仲介の会社。2025年7月のシリーズCに参加と報じられています。', 'role': '投資先'},
 {'id': 'raksul', 'name': 'Raksul', 'kind': 'o', 'from': 2026, 'desc': '印刷・物流のプラットフォーム。小澤氏が2026年8月に社外取締役に就任しました。', 'role': '社外取締役'},
 {'id': 'rakuten', 'name': 'Rakuten', 'kind': 'o', 'from': 2024, 'desc': '小澤氏の出身元。オークション事業の担当役員などを務めました。', 'role': '出身元'},
]
E = (std('boostcap') +
 "E.push({a:'boostcap',b:'boostcons',k:'link',label:'姉妹会社'});\n"
 "E.push({a:'ozawa',b:'boostcons',k:'link',label:'率いる'});\n"
 "['kotoba','ivry','solafune','terass'].forEach(b=>E.push({a:'boostcap',b,k:'invest2'}));\n"
 "E.push({a:'ozawa',b:'raksul',k:'link',label:'社外取締役'});\n"
 "E.push({a:'ozawa',b:'rakuten',k:'from'});\n"
 "E.push({a:'ozawa',b:'ly',k:'from'});\n"
 "E.push({a:'hori',b:'ly',k:'from'});\n\n")
CO2['boost'] = mk(N, E,
 {'ozawa': 'Takao Ozawa', 'hori': 'Shinichiro Hori', 'takahashi': 'Kenta Takahashi'},
 {}, {'boostcap': 'https://boostcapital.co.jp'},
 wp(('rakuten', 'Rakuten'), ('raksul', 'Raksul'), ('ly', 'LY_Corporation')),
 {'ozawa': [['1999', 'ビズシークを設立(のち楽天へ)'], ['2005', '楽天野球団の取締役事業本部長'], ['2011', 'クロコスを設立(のちヤフーへ売却)'], ['2012', 'ヤフーに入社'], ['2024', 'Boost Capitalを設立、代表に'], ['2026', 'ラクスルの社外取締役に']]},
 {}, 'boostcap')

# ---------------- Preferred Networks ----------------
N = [
 {'id': 'pfn', 'name': 'Preferred Networks', 'kind': 'c', 'from': 2014, 'desc': '2014年に、Preferred Infrastructureの事業から分社化して設立された、日本を代表するAI企業。深層学習と、独自のAI半導体を開発しています。'},
 {'id': 'nishikawa', 'name': '西川徹', 'kind': 'p', 'from': 2014, 'desc': '共同創業者。2025年11月に会長に就任したと報じられています(資料により肩書の表記が異なります)。', 'role': '会長 / 共同創業者', 'founder': 1},
 {'id': 'okanohara', 'name': '岡野原大輔', 'kind': 'p', 'from': 2014, 'desc': '共同創業者。2025年11月に社長に就任したと報じられています。', 'role': '社長 / 共同創業者', 'founder': 1},
 {'id': 'toyota', 'name': 'Toyota', 'kind': 'i', 'from': 2014, 'desc': 'トヨタ自動車。主要な出資者として報じられています。', 'role': '出資者'},
 {'id': 'fanuc', 'name': 'Fanuc', 'kind': 'i', 'from': 2014, 'desc': 'ファナック。主要な出資者として報じられています。', 'role': '出資者'},
 {'id': 'pfi', 'name': 'Preferred Infrastructure', 'kind': 'o', 'from': 2014, 'desc': '2006年に西川氏と岡野原氏が共同創業した会社。PFNの元になった事業の母体。', 'role': '母体'},
 {'id': 'utokyo', 'name': 'University of Tokyo', 'kind': 'o', 'from': 2014, 'desc': '二人が出会い、共に創業した起点の大学。', 'role': '出身校'},
]
E = std('pfn') + "['nishikawa','okanohara'].forEach(a=>E.push({a,b:'pfi',k:'from'}));\n['nishikawa','okanohara'].forEach(a=>E.push({a,b:'utokyo',k:'from'}));\nE.push({a:'pfi',b:'pfn',k:'owns',label:'2014年に分社化'});\n\n"
CO2['pfn'] = mk(N, E, {'nishikawa': 'Toru Nishikawa', 'okanohara': 'Daisuke Okanohara'},
 {'pfn': 'PreferredNetworks'}, {'pfn': 'https://www.preferred.jp', 'toyota': 'https://global.toyota', 'fanuc': 'https://www.fanuc.co.jp'},
 wp(('pfn', 'Preferred_Networks'), ('toyota', 'Toyota'), ('fanuc', 'Fanuc'), ('utokyo', 'University_of_Tokyo')),
 {'nishikawa': [['2006', 'Preferred Infrastructureを共同創業'], ['2014', 'Preferred Networksを設立'], ['2025', '11月に会長に(報道)']]}, {}, 'pfn')

# ---------------- PKSHA Technology ----------------
N = [
 {'id': 'pksha', 'name': 'PKSHA Technology', 'kind': 'c', 'from': 2012, 'desc': '2012年に東京大学の松尾研究室の出身者らが設立した、日本のAIソフトウェア企業。自然言語処理や画像認識を、企業向けに提供しています。2025年9月期の連結売上高は約218億円。'},
 {'id': 'uenoyama', 'name': '上野山勝也', 'kind': 'p', 'from': 2012, 'desc': '代表取締役で筆頭株主(約30%)。松尾研究室の出身で、2012年にPKSHAを創業しました。', 'role': '代表取締役 / 創業者', 'founder': 1},
 {'id': 'yamada', 'name': '山田尚史', 'kind': 'p', 'from': 2012, 'desc': '創業者の一人で、安定株主(約7.5%)と開示されています。', 'role': '創業者', 'founder': 1},
 {'id': 'toyota', 'name': 'Toyota', 'kind': 'i', 'from': 2018, 'desc': 'トヨタ自動車。少数株主(約2.5%)として挙がっています。', 'role': '少数株主'},
 {'id': 'luce', 'name': 'LUCE Capital', 'kind': 'i', 'from': 2018, 'desc': '約3.6%を保有する株主として挙がっています。', 'role': '株主'},
 {'id': 'matsuo', 'name': '松尾豊', 'kind': 'o', 'from': 2012, 'desc': '東京大学の教授で、日本のAI研究の第一人者。上野山氏が学んだ松尾研究室を率います。', 'role': '研究室の指導者'},
 {'id': 'utokyo', 'name': 'University of Tokyo', 'kind': 'o', 'from': 2012, 'desc': '創業者らの出身大学。', 'role': '出身校'},
]
E = std('pksha') + "E.push({a:'uenoyama',b:'matsuo',k:'from'});\nE.push({a:'matsuo',b:'utokyo',k:'link'});\nE.push({a:'uenoyama',b:'utokyo',k:'from'});\n\n"
CO2['pksha'] = mk(N, E, {'uenoyama': 'Katsuya Uenoyama', 'yamada': 'Naofumi Yamada', 'matsuo': 'Yutaka Matsuo'}, {},
 {'pksha': 'https://pkshatech.com'}, wp(('pksha', 'PKSHA_Technology'), ('toyota', 'Toyota'), ('utokyo', 'University_of_Tokyo')),
 {'uenoyama': [['〜', '東京大学の松尾研究室で研究'], ['2012', 'PKSHA Technologyを創業'], ['2016', '代表取締役に就任']]}, {}, 'pksha')

# ---------------- 楽天グループ ----------------
N = [
 {'id': 'rakuten', 'name': 'Rakuten', 'kind': 'c', 'from': 2003, 'desc': '三木谷浩史氏が創業した、ECと通信と金融の企業グループ。2023年にOpenAIと生成AIで協業に合意し、同年11月にOpenAIが戦略的パートナーとして参画、「Rakuten AI for Business」を発表しました。'},
 {'id': 'mikitani', 'name': '三木谷浩史', 'kind': 'p', 'from': 2003, 'desc': '創業者で会長兼社長。', 'role': '創業者 / 会長兼社長', 'founder': 1},
 {'id': 'ozawa', 'name': '小澤隆生', 'kind': 'p', 'from': 2003, 'to': 2006, 'desc': '2003年にビズシークの合併で楽天に入社。オークションと野球団の役員を務め、2006年に楽天を離れ、のち顧問(2009〜2012年)になりました。', 'role': '元役員'},
 {'id': 'jpost', 'name': 'Japan Post Holdings', 'kind': 'i', 'from': 2021, 'desc': '日本郵政。2021年に約1,500億円を出資しました。', 'role': '出資者'},
 {'id': 'tencent', 'name': 'Tencent', 'kind': 'i', 'from': 2021, 'desc': '2021年に約657億円を出資しました。', 'role': '出資者'},
 {'id': 'walmart', 'name': 'Walmart', 'kind': 'i', 'from': 2021, 'desc': '2021年に出資し、楽天西友ネットスーパーなどで提携。', 'role': '出資者'},
 {'id': 'altman', 'name': 'サム・アルトマン', 'kind': 'o', 'from': 2023, 'desc': 'OpenAIのCEO。2023年から楽天と提携しています。', 'role': 'OpenAIのCEO'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2023, 'desc': '2023年に協業に合意。通信業界向けのAIツールを共同開発すると2024年に発表。', 'role': '戦略的パートナー'},
 {'id': 'mobile', 'name': 'Rakuten Mobile', 'kind': 'o', 'from': 2020, 'desc': '2020年に本格参入した携帯電話事業。', 'role': '通信事業'},
 {'id': 'softbank', 'name': 'SoftBank Group', 'kind': 'o', 'from': 2020, 'desc': '携帯電話市場での競合。', 'role': '競合'},
 {'id': 'bizseek', 'name': 'Bizseek', 'kind': 'o', 'from': 2003, 'desc': '小澤氏が1999年に創業し、楽天に統合されたネットオークションの会社。', 'role': '小澤氏が創業'},
]
E = (std('rakuten') +
 "E.push({a:'rakuten',b:'openai',k:'link',label:'2023年に協業'});\n"
 "E.push({a:'altman',b:'openai',k:'link'});\n"
 "E.push({a:'rakuten',b:'mobile',k:'owns'});\n"
 "E.push({a:'mobile',b:'softbank',k:'conflict',label:'携帯の競合'});\n"
 "E.push({a:'ozawa',b:'bizseek',k:'link',label:'創業'});\n"
 "E.push({a:'bizseek',b:'rakuten',k:'owns',label:'楽天に統合'});\n\n")
CO2['rakuten'] = mk(N, E, {'mikitani': 'Hiroshi Mikitani', 'ozawa': 'Takao Ozawa', 'altman': 'Sam Altman'},
 {'altman': 'sama', 'openai': 'OpenAI'}, {'rakuten': 'https://global.rakuten.com', 'openai': 'https://openai.com'},
 wp(('rakuten', 'Rakuten'), ('jpost', 'Japan_Post_Holdings'), ('tencent', 'Tencent'), ('walmart', 'Walmart'), ('openai', 'OpenAI'), ('mobile', 'Rakuten_Mobile'), ('softbank', 'SoftBank_Group')),
 {'mikitani': [['1997', '楽天を創業'], ['2023', 'OpenAIとの協業に合意'], ['2024', '通信向けAIツールを共同開発すると発表']]}, {}, 'rakuten')

# ---------------- LINEヤフー ----------------
N = [
 {'id': 'ly', 'name': 'LY Corporation', 'kind': 'c', 'from': 2019, 'desc': '2019年にヤフーとLINEの経営統合が発表され、2023年に「LINEヤフー」が発足。SoftBankとNAVERの共同の傘下にあります。2026年5月に、AIエージェント化を進める方針が示されました。'},
 {'id': 'idezawa', 'name': '出澤剛', 'kind': 'p', 'from': 2019, 'desc': '代表取締役社長。LINEの元CEO。2026年4月に、多くのサービスでAIエージェント「Agent i」を始めたと報じられています。', 'role': '代表取締役社長CEO'},
 {'id': 'kawabe', 'name': '川邊健太郎', 'kind': 'p', 'from': 2019, 'to': 2026, 'desc': '元会長。2025年12月に、2026年6月の株主総会で退任すると発表しました。退任後はAI分野での起業を目指していると報じられています。', 'role': '元会長'},
 {'id': 'softbank', 'name': 'SoftBank Group', 'kind': 'i', 'from': 2019, 'desc': 'NAVERと共に、親会社を通じてLINEヤフーを支配します。', 'role': '親会社(共同)'},
 {'id': 'naver', 'name': 'NAVER', 'kind': 'i', 'from': 2019, 'desc': '韓国のIT企業。SoftBankと共に、親会社を通じてLINEヤフーを支配します。', 'role': '親会社(共同)'},
 {'id': 'ozawa', 'name': '小澤隆生', 'kind': 'o', 'from': 2019, 'desc': '元ヤフーの経営者。現在はBoost Capitalの代表で、LINEヤフーはそのアンカー出資者です。', 'role': '元ヤフー'},
 {'id': 'hori', 'name': '堀新一郎', 'kind': 'o', 'from': 2019, 'desc': 'ヤフーのYJキャピタルでCOO、Z Venture Capitalの社長を務め、現在はBoost Capitalの共同GP。', 'role': '元CVCの責任者'},
 {'id': 'boostcap', 'name': 'Boost Capital', 'kind': 'o', 'from': 2024, 'desc': '2024年にアンカー出資者として約100億円のファンドに参加と報じられています。', 'role': 'アンカー出資先'},
 {'id': 'paypay', 'name': 'PayPay', 'kind': 'o', 'from': 2019, 'desc': 'スマホ決済。川邊氏は、PayPayの黒字化を見届けたことを退任の理由に挙げたと報じられています。', 'role': '決済事業'},
]
E = (std('ly') +
 "E.push({a:'ly',b:'boostcap',k:'invest2',label:'アンカー出資',since:2024});\n"
 "E.push({a:'ozawa',b:'boostcap',k:'link',label:'代表',since:2024});\n"
 "E.push({a:'hori',b:'boostcap',k:'link',label:'共同GP',since:2024});\n"
 "E.push({a:'ly',b:'paypay',k:'owns'});\n\n")
CO2['ly'] = mk(N, E, {'idezawa': 'Takeshi Idezawa', 'kawabe': 'Kentaro Kawabe', 'ozawa': 'Takao Ozawa', 'hori': 'Shinichiro Hori'},
 {}, {'ly': 'https://www.lycorp.co.jp', 'softbank': 'https://group.softbank', 'naver': 'https://www.navercorp.com'},
 wp(('ly', 'LY_Corporation'), ('softbank', 'SoftBank_Group'), ('naver', 'Naver_Corporation'), ('paypay', 'PayPay')), {}, {}, 'ly')

# ---------------- Perplexity ----------------
N = [
 {'id': 'perplexity', 'name': 'Perplexity', 'kind': 'c', 'from': 2022, 'desc': '2022年に設立されたAI検索の会社。2026年は、約200億ドルの評価額の調達が報じられ、さらにNvidia主導で300億ドル超の評価額の交渉が伝えられています(確認できていません)。'},
 {'id': 'srinivas', 'name': 'アラヴィンド・スリニバス', 'kind': 'p', 'from': 2022, 'desc': '共同創業者でCEO。元OpenAIの研究者です。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'yarats', 'name': 'デニス・ヤラッツ', 'kind': 'p', 'from': 2022, 'desc': '共同創業者でCTO。元Metaの研究者です。', 'role': 'CTO / 共同創業者', 'founder': 1},
 {'id': 'ho', 'name': 'ジョニー・ホー', 'kind': 'p', 'from': 2022, 'desc': '共同創業者。', 'role': '共同創業者', 'founder': 1},
 {'id': 'konwinski', 'name': 'アンディ・コンウィンスキー', 'kind': 'p', 'from': 2022, 'desc': '共同創業者。Databricksの共同創業者でもあります。', 'role': '共同創業者', 'founder': 1},
 {'id': 'bezos', 'name': 'ジェフ・ベゾス', 'kind': 'i', 'from': 2023, 'desc': 'Amazon創業者。出資者の一人として挙げられています。', 'role': '個人投資家'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2023, 'desc': '出資者の一社。2026年にさらに出資する交渉と報じられています(未確認)。', 'role': '出資 + GPU供給'},
 {'id': 'softbank', 'name': 'SoftBank Group', 'kind': 'i', 'from': 2024, 'desc': '出資者の一社と報じられています。', 'role': '出資者'},
 {'id': 'nea', 'name': 'NEA', 'kind': 'i', 'from': 2023, 'desc': '初期の出資者の一社。', 'role': 'VC'},
 {'id': 'ivp', 'name': 'IVP', 'kind': 'i', 'from': 2023, 'desc': '出資者の一社。', 'role': 'VC'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2022, 'desc': 'スリニバスの出身元(研究者)。', 'role': '出身元'},
 {'id': 'databricks', 'name': 'Databricks', 'kind': 'o', 'from': 2022, 'desc': 'コンウィンスキーが共同創業した会社。', 'role': '共同創業者の出身元'},
]
E = std('perplexity') + "E.push({a:'srinivas',b:'openai',k:'from'});\nE.push({a:'konwinski',b:'databricks',k:'from'});\n\n"
CO2['perplexity'] = mk(N, E, {'srinivas': 'Aravind Srinivas', 'yarats': 'Denis Yarats', 'ho': 'Johnny Ho', 'konwinski': 'Andy Konwinski', 'bezos': 'Jeff Bezos'},
 {'srinivas': 'AravSrinivas', 'perplexity': 'perplexity_ai', 'bezos': 'JeffBezos', 'nvidia': 'nvidia'},
 {'perplexity': 'https://www.perplexity.ai', 'nvidia': 'https://www.nvidia.com'},
 wp(('perplexity', 'Perplexity_AI'), ('nvidia', 'Nvidia'), ('softbank', 'SoftBank_Group'), ('nea', 'New_Enterprise_Associates'), ('openai', 'OpenAI'), ('databricks', 'Databricks')),
 {'srinivas': [['〜', 'UCバークレーで博士課程'], ['〜', 'OpenAIの研究者'], ['2022', 'Perplexityを共同創業']]}, {}, 'perplexity')

# ---------------- Cohere ----------------
N = [
 {'id': 'cohere', 'name': 'Cohere', 'kind': 'c', 'from': 2019, 'desc': '2019年にカナダのトロントで設立された、企業向けの大規模言語モデルの会社。2025年8月に約5億ドルを調達(評価額約68億ドル)。2026年は、報道により数字が食い違います。'},
 {'id': 'gomez', 'name': 'エイダン・ゴメス', 'kind': 'p', 'from': 2019, 'desc': '共同創業者でCEO。AIの基盤「トランスフォーマー」の論文の共著者で、Google Brain出身です。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'frosst', 'name': 'ニック・フロスト', 'kind': 'p', 'from': 2019, 'desc': '共同創業者。Google Brainのトロント拠点で、ヒントンの下で研究しました。', 'role': '共同創業者', 'founder': 1},
 {'id': 'zhang', 'name': 'アイバン・ジャン', 'kind': 'p', 'from': 2019, 'desc': '共同創業者。', 'role': '共同創業者', 'founder': 1},
 {'id': 'pineau', 'name': 'ジョエル・ピノー', 'kind': 'p', 'from': 2025, 'desc': 'Chief AI Officerとして報じられています。Metaの元FAIR責任者です。', 'role': 'Chief AI Officer'},
 {'id': 'index', 'name': 'Index Ventures', 'kind': 'i', 'from': 2024, 'desc': '2026年1月のシリーズD(約4.5億ドル)を主導したと報じられています。', 'role': 'VC'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2023, 'desc': '出資者として繰り返し挙がっています。', 'role': '出資 + GPU供給'},
 {'id': 'radical', 'name': 'Radical Ventures', 'kind': 'i', 'from': 2025, 'desc': '2025年の増資を共同で主導と報じられています。', 'role': 'VC'},
 {'id': 'inovia', 'name': 'Inovia Capital', 'kind': 'i', 'from': 2025, 'desc': '2025年の増資を共同で主導と報じられています。', 'role': 'VC'},
 {'id': 'tiger', 'name': 'Tiger Global', 'kind': 'i', 'from': 2023, 'desc': '出資者の一社。', 'role': '投資会社'},
 {'id': 'amd', 'name': 'AMD Ventures', 'kind': 'i', 'from': 2025, 'desc': '2025年の増資に参加と報じられています。', 'role': '戦略出資者'},
 {'id': 'hinton', 'name': 'ジェフリー・ヒントン', 'kind': 'o', 'from': 2019, 'desc': 'ゴメスとフロストが学んだ、トロント大学の教授。Cohereの出資者の一人としても知られます。', 'role': '師'},
 {'id': 'googlebrain', 'name': 'Google Brain', 'kind': 'o', 'from': 2019, 'desc': 'ゴメスとフロストの出身元。', 'role': '出身元'},
 {'id': 'meta', 'name': 'Meta', 'kind': 'o', 'from': 2025, 'desc': 'ピノーの出身元。', 'role': '出身元'},
]
E = std('cohere') + "['gomez','frosst'].forEach(a=>E.push({a,b:'googlebrain',k:'from'}));\nE.push({a:'pineau',b:'meta',k:'from'});\n['gomez','frosst'].forEach(a=>E.push({a,b:'hinton',k:'link',label:'師'}));\n\n"
CO2['cohere'] = mk(N, E, {'gomez': 'Aidan Gomez', 'frosst': 'Nick Frosst', 'zhang': 'Ivan Zhang', 'pineau': 'Joelle Pineau', 'hinton': 'Geoffrey Hinton'},
 {'gomez': 'aidangomez', 'frosst': 'nickfrosst', 'cohere': 'cohere', 'nvidia': 'nvidia'}, {'cohere': 'https://cohere.com', 'nvidia': 'https://www.nvidia.com'},
 wp(('cohere', 'Cohere'), ('index', 'Index_Ventures'), ('nvidia', 'Nvidia'), ('radical', 'Radical_Ventures'), ('tiger', 'Tiger_Global_Management'), ('meta', 'Meta_Platforms'), ('googlebrain', 'Google_Brain')),
 {'gomez': [['2017', 'Google Brainで「Attention Is All You Need」を共著'], ['2019', 'Cohereを共同創業']]}, {}, 'cohere')

# ---------------- Scale AI ----------------
N = [
 {'id': 'scale', 'name': 'Scale AI', 'kind': 'c', 'from': 2016, 'desc': '2016年に設立された、AI向けのデータ整備の会社。2025年6月にMetaが約143億ドルを出資して(約49%と報じられています)、創業者のワンがMetaへ移りました。'},
 {'id': 'wang', 'name': 'アレクサンドル・ワン', 'kind': 'p', 'from': 2016, 'to': 2025, 'desc': '創業者で元CEO。2025年にMetaのChief AI Officerになりました。Scaleの取締役の席は残すと報じられています。', 'role': '元CEO / 創業者', 'founder': 1},
 {'id': 'guo', 'name': 'ルーシー・グオ', 'kind': 'p', 'from': 2016, 'to': 2018, 'desc': '共同創業者。のちに離れ、クリエイター向けのプラットフォームPassesを創業しました。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'droege', 'name': 'ジェイソン・ドロージ', 'kind': 'p', 'from': 2024, 'desc': 'CEO。Uber Eatsの元責任者で、2025年にワンの後任として昇格しました(暫定とする報道もあります)。', 'role': 'CEO'},
 {'id': 'meta', 'name': 'Meta', 'kind': 'i', 'from': 2025, 'desc': '2025年に約143億ドルを出資(約49%と報じられています)。', 'role': '大株主'},
 {'id': 'accel', 'name': 'Accel', 'kind': 'i', 'from': 2017, 'desc': '初期の出資者の一社。', 'role': 'VC'},
 {'id': 'index', 'name': 'Index Ventures', 'kind': 'i', 'from': 2018, 'desc': '初期の出資者として報じられています。', 'role': 'VC'},
 {'id': 'foundersfund', 'name': 'Founders Fund', 'kind': 'i', 'from': 2018, 'desc': '出資者の一社。', 'role': 'VC'},
 {'id': 'dragoneer', 'name': 'Dragoneer', 'kind': 'i', 'from': 2019, 'desc': '初期の出資者として報じられています。', 'role': '投資会社'},
 {'id': 'tiger', 'name': 'Tiger Global', 'kind': 'i', 'from': 2019, 'desc': '初期の出資者として報じられています。', 'role': '投資会社'},
 {'id': 'yc', 'name': 'Y Combinator', 'kind': 'i', 'from': 2016, 'desc': '2016年に始動した起点のアクセラレーター。', 'role': '出身のアクセラレーター'},
 {'id': 'quora', 'name': 'Quora', 'kind': 'o', 'from': 2016, 'desc': 'ワンとグオが、創業前に働いた会社と報じられています。', 'role': '出身元'},
 {'id': 'mit', 'name': 'MIT', 'kind': 'o', 'from': 2016, 'desc': 'ワンが中退して、Scaleを創業した大学。', 'role': '出身校'},
]
E = std('scale') + "['wang','guo'].forEach(a=>E.push({a,b:'quora',k:'from'}));\nE.push({a:'wang',b:'mit',k:'from'});\nE.push({a:'meta',b:'scale',k:'invest2',label:'約143億ドル',since:2025});\n\n"
CO2['scale'] = mk(N, E, {'wang': 'Alexandr Wang', 'guo': 'Lucy Guo', 'droege': 'Jason Droege'},
 {'wang': 'alexandr_wang', 'scale': 'scale_AI'}, {'scale': 'https://scale.com'},
 wp(('scale', 'Scale_AI'), ('meta', 'Meta_Platforms'), ('accel', 'Accel_(company)'), ('index', 'Index_Ventures'), ('foundersfund', 'Founders_Fund'), ('dragoneer', 'Dragoneer_Investment_Group'),
    ('tiger', 'Tiger_Global_Management'), ('yc', 'Y_Combinator'), ('quora', 'Quora'), ('mit', 'Massachusetts_Institute_of_Technology')),
 {'wang': [['2016', 'Scale AIを創業'], ['2025', '6月にMetaへ移り、Chief AI Officerに']]}, {}, 'scale')

# ---------------- Databricks ----------------
N = [
 {'id': 'databricks', 'name': 'Databricks', 'kind': 'c', 'from': 2013, 'desc': '2013年に、UCバークレーの研究者らが設立した、データとAIの会社。2026年2月に約50億ドルを調達(評価額約1,340億ドル)しました。上場は未定で、2027年以降とする報道があります。'},
 {'id': 'ghodsi', 'name': 'アリ・ゴドシ', 'kind': 'p', 'from': 2013, 'desc': '共同創業者でCEO。2026年6月に「上場には悪い年」と語りました。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'zaharia', 'name': 'マテイ・ザハリア', 'kind': 'p', 'from': 2013, 'desc': '共同創業者でCTO。Apache Sparkの開発者で、UCバークレーの教授。', 'role': 'CTO / 共同創業者', 'founder': 1},
 {'id': 'stoica', 'name': 'イオン・ストイカ', 'kind': 'p', 'from': 2013, 'desc': '共同創業者。UCバークレーの教授で、Anyscaleも共同創業しました。', 'role': '共同創業者', 'founder': 1},
 {'id': 'xin', 'name': 'レイノルド・シン', 'kind': 'p', 'from': 2013, 'desc': '共同創業者。Sparkの主要な開発者の一人。', 'role': 'チーフアーキテクト / 共同創業者', 'founder': 1},
 {'id': 'konwinski', 'name': 'アンディ・コンウィンスキー', 'kind': 'p', 'from': 2013, 'to': 2022, 'desc': '共同創業者。のちにPerplexityを共同創業しました。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'wendell', 'name': 'パトリック・ウェンデル', 'kind': 'p', 'from': 2013, 'desc': '共同創業者。Sparkの開発に参加。', 'role': '共同創業者', 'founder': 1},
 {'id': 'a16z', 'name': 'Andreessen Horowitz', 'kind': 'i', 'from': 2013, 'desc': '最初期のシリーズAを主導したと報じられています。', 'role': 'VC'},
 {'id': 'nea', 'name': 'NEA', 'kind': 'i', 'from': 2014, 'desc': '初期の出資者の一社。', 'role': 'VC'},
 {'id': 'microsoft', 'name': 'Microsoft', 'kind': 'i', 'from': 2019, 'desc': '出資者の一社で、クラウドでも提携。', 'role': '戦略出資者'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2023, 'desc': '出資者の一社。', 'role': '出資 + GPU供給'},
 {'id': 'thrive', 'name': 'Thrive Capital', 'kind': 'i', 'from': 2025, 'desc': '出資者の一社として報じられています。', 'role': 'VC'},
 {'id': 'berkeley', 'name': 'UC Berkeley', 'kind': 'o', 'from': 2013, 'desc': '創業者らの母体の大学。', 'role': '出身校'},
 {'id': 'mosaic', 'name': 'MosaicML', 'kind': 'o', 'from': 2023, 'desc': '2023年に約13億ドルで買収した、AI学習基盤の会社。', 'role': '買収'},
 {'id': 'perplexity', 'name': 'Perplexity', 'kind': 'o', 'from': 2022, 'desc': 'コンウィンスキーが共同創業したAI検索の会社。', 'role': '移籍先'},
]
E = std('databricks') + "['ghodsi','zaharia','stoica','xin','konwinski','wendell'].forEach(a=>E.push({a,b:'berkeley',k:'from'}));\nE.push({a:'databricks',b:'mosaic',k:'invest2',label:'2023年に買収'});\nE.push({a:'konwinski',b:'perplexity',k:'moved'});\n\n"
CO2['databricks'] = mk(N, E, {'ghodsi': 'Ali Ghodsi', 'zaharia': 'Matei Zaharia', 'stoica': 'Ion Stoica', 'xin': 'Reynold Xin', 'konwinski': 'Andy Konwinski', 'wendell': 'Patrick Wendell'},
 {'ghodsi': 'alighodsi', 'zaharia': 'matei_zaharia', 'xin': 'rxin', 'databricks': 'databricks', 'nvidia': 'nvidia', 'microsoft': 'Microsoft'},
 {'databricks': 'https://www.databricks.com', 'nvidia': 'https://www.nvidia.com', 'microsoft': 'https://www.microsoft.com'},
 wp(('databricks', 'Databricks'), ('a16z', 'Andreessen_Horowitz'), ('nea', 'New_Enterprise_Associates'), ('microsoft', 'Microsoft'), ('nvidia', 'Nvidia'), ('thrive', 'Thrive_Capital'),
    ('berkeley', 'University_of_California,_Berkeley'), ('mosaic', 'MosaicML'), ('perplexity', 'Perplexity_AI')),
 {'ghodsi': [['2013', 'Databricksを共同創業'], ['2016', 'CEOに就任'], ['2026', '2月に評価額約1,340億ドルで調達']]}, {}, 'databricks')

# ---------------- Hugging Face ----------------
N = [
 {'id': 'hf', 'name': 'Hugging Face', 'kind': 'c', 'from': 2016, 'desc': '2016年に設立された、AIモデルを共有するプラットフォーム。2023年に約2.35億ドル(評価額約45億ドル)を調達。2026年8月に、約130億ドルでの売却を探っていると報じられています(合意は未確認)。'},
 {'id': 'delangue', 'name': 'クレモン・ドラング', 'kind': 'p', 'from': 2016, 'desc': '共同創業者でCEO。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'chaumond', 'name': 'ジュリアン・ショーモン', 'kind': 'p', 'from': 2016, 'desc': '共同創業者でCTO。', 'role': 'CTO / 共同創業者', 'founder': 1},
 {'id': 'wolf', 'name': 'トーマス・ウルフ', 'kind': 'p', 'from': 2016, 'desc': '共同創業者でチーフサイエンティスト。元特許弁護士。', 'role': 'チーフサイエンティスト / 共同創業者', 'founder': 1},
 {'id': 'salesforce', 'name': 'Salesforce', 'kind': 'i', 'from': 2023, 'desc': '2023年のシリーズDを主導したと報じられています。', 'role': '戦略出資者'},
 {'id': 'google', 'name': 'Google', 'kind': 'i', 'from': 2023, 'desc': '2023年のシリーズDに参加。', 'role': '戦略出資者'},
 {'id': 'amazon', 'name': 'Amazon', 'kind': 'i', 'from': 2023, 'desc': '2023年のシリーズDに参加。', 'role': '戦略出資者'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2023, 'desc': '2023年のシリーズDに参加。', 'role': '出資 + GPU供給'},
 {'id': 'intel', 'name': 'Intel', 'kind': 'i', 'from': 2023, 'desc': '2023年のシリーズDに参加。', 'role': '戦略出資者'},
 {'id': 'lux', 'name': 'Lux Capital', 'kind': 'i', 'from': 2019, 'desc': '初期からの出資者。', 'role': 'VC'},
 {'id': 'sequoia', 'name': 'Sequoia Capital', 'kind': 'i', 'from': 2022, 'desc': '出資者の一社。', 'role': 'VC'},
]
E = std('hf')
CO2['hf'] = mk(N, E, {'delangue': 'Clément Delangue', 'chaumond': 'Julien Chaumond', 'wolf': 'Thomas Wolf'},
 {'delangue': 'ClementDelangue', 'chaumond': 'julien_c', 'wolf': 'Thom_Wolf', 'hf': 'huggingface'},
 {'hf': 'https://huggingface.co', 'nvidia': 'https://www.nvidia.com', 'salesforce': 'https://www.salesforce.com'},
 wp(('hf', 'Hugging_Face'), ('salesforce', 'Salesforce'), ('google', 'Google'), ('amazon', 'Amazon_(company)'), ('nvidia', 'Nvidia'), ('intel', 'Intel'), ('lux', 'Lux_Capital'), ('sequoia', 'Sequoia_Capital')),
 {}, {}, 'hf')
