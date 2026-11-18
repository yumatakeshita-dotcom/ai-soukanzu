from newco_data import mk, std, wp

CO5 = {}

# ================= Uber / Uber Eats =================
N = [
 {'id': 'uber', 'name': 'Uber / Uber Eats', 'kind': 'c', 'from': 2009, 'desc': '2009年に創業した、配車とフードデリバリー(Uber Eats)の会社。2026年2月に新しいCFOを任命し、自動運転では20社以上と提携。2026年末までに最大15都市での自動運転の配車を目指すと報じられています。日本では2016年にUber Eatsを開始し、2026年10月に10周年を迎えました。'},
 {'id': 'kalanick', 'name': 'トラビス・カラニック', 'kind': 'p', 'from': 2009, 'to': 2019, 'desc': '共同創業者で、元CEO。2017年6月に辞任し、2019年に取締役も退きました。のちCloudKitchens(ゴーストキッチン)を率います。', 'role': '元CEO / 共同創業者', 'founder': 1},
 {'id': 'camp', 'name': 'ギャレット・キャンプ', 'kind': 'p', 'from': 2009, 'desc': '共同創業者。StumbleUponの創業者でもあります。', 'role': '共同創業者', 'founder': 1},
 {'id': 'khosrowshahi', 'name': 'ダラ・コスロシャヒ', 'kind': 'p', 'from': 2017, 'desc': 'CEO。2017年8月に、Expediaから招かれました。「何でもアプリ」の構想を語っています。', 'role': 'CEO'},
 {'id': 'krishnamurthy', 'name': 'バラジ・クリシュナムルティ', 'kind': 'p', 'from': 2026, 'desc': 'CFO。2026年2月に、投資家向け広報の責任者から昇格したと報じられています。', 'role': 'CFO'},
 {'id': 'mahendra', 'name': 'プラシャント・マヘンドラ=ラジャ', 'kind': 'p', 'from': 2023, 'to': 2026, 'desc': '元CFO。在任約27か月で、2026年2月に退任しました。', 'role': '元CFO'},
 {'id': 'brovkina', 'name': 'ユリア・ブロヴキナ', 'kind': 'p', 'from': 2025, 'desc': 'Uber Eats Japanの代表(ゼネラルマネージャー)。2025年11月に就任したと発表されました。', 'role': 'Uber Eats Japan代表'},
 {'id': 'nakagawa', 'name': '中川晋太郎', 'kind': 'p', 'from': 2016, 'to': 2025, 'desc': 'Uber Eats Japanの前の代表。2025年3月の事業戦略説明会に登壇しました。', 'role': '元Uber Eats Japan代表'},
 {'id': 'gurley', 'name': 'ビル・ガーリー', 'kind': 'i', 'from': 2010, 'desc': 'Benchmarkのパートナー。初期の出資者として知られ、2017年にカラニックを提訴しました。', 'role': '初期の出資者(Benchmark)'},
 {'id': 'benchmark', 'name': 'Benchmark', 'kind': 'i', 'from': 2010, 'desc': '初期の出資者(シリーズA)。2017年にカラニックを提訴しました。', 'role': '初期のVC'},
 {'id': 'gv', 'name': 'GV', 'kind': 'i', 'from': 2013, 'desc': 'Google傘下のVC。2013年に大きな出資をしたと報じられています。', 'role': 'VC'},
 {'id': 'pif', 'name': 'Saudi PIF', 'kind': 'i', 'from': 2016, 'desc': 'サウジアラビアの政府系ファンド。2016年に約35億ドルを出資と報じられています。', 'role': '政府系ファンド'},
 {'id': 'softbank', 'name': 'SoftBank Group', 'kind': 'i', 'from': 2018, 'desc': '2018年に大型の出資をしたと報じられています(約77億ドル)。', 'role': '出資者'},
 {'id': 'toyota', 'name': 'Toyota', 'kind': 'i', 'from': 2018, 'desc': '2018年に約5億ドルを出資と報じられています。', 'role': '出資者'},
 {'id': 'postmates', 'name': 'Postmates', 'kind': 'o', 'from': 2020, 'desc': '2020年に約26.5億ドルで買収したフードデリバリーの会社。', 'role': '買収'},
 {'id': 'cornershop', 'name': 'Cornershop', 'kind': 'o', 'from': 2020, 'desc': '食料品の配達の会社。Uberが買収したと報じられています。', 'role': '買収'},
 {'id': 'drizly', 'name': 'Drizly', 'kind': 'o', 'from': 2021, 'desc': 'お酒の配達の会社。2021年に買収。', 'role': '買収'},
 {'id': 'waymo', 'name': 'Waymo', 'kind': 'o', 'from': 2017, 'desc': '2017年に、自動運転の技術をめぐり訴訟に。のちに和解し、現在はAustinとAtlantaでUber経由の配車を提供する提携先です。', 'role': '元の対立・現在の提携'},
 {'id': 'rivian', 'name': 'Rivian', 'kind': 'o', 'from': 2026, 'desc': 'Uberが約12.5億ドルを出資し、2031年までに最大5万台のロボタクシーを導入する計画と報じられています。', 'role': '自動運転の提携先'},
 {'id': 'rakuten', 'name': 'Rakuten', 'kind': 'o', 'from': 2026, 'desc': 'Uber Eatsで楽天ポイントが使えるようになると、2026年10月の10周年発表で説明されました。', 'role': '日本での提携'},
 {'id': 'cloudkitchens', 'name': 'CloudKitchens', 'kind': 'o', 'from': 2016, 'desc': 'カラニックが率いる、デリバリー専用の厨房の会社。', 'role': 'カラニックの新事業'},
 {'id': 'stumbleupon', 'name': 'StumbleUpon', 'kind': 'o', 'from': 2009, 'desc': 'キャンプが創業したウェブ発見サービス。eBayが買収しました。', 'role': 'キャンプの前の会社'},
 {'id': 'expedia', 'name': 'Expedia', 'kind': 'o', 'from': 2017, 'desc': 'コスロシャヒの前の勤務先(CEO)。', 'role': '出身元'},
]
E = (std('uber') +
 "E.push({a:'kalanick',b:'camp',k:'link',label:'共同創業者'});\nE.push({a:'gurley',b:'kalanick',k:'conflict',label:'2017年に提訴',since:2017});\nE.push({a:'benchmark',b:'kalanick',k:'conflict',label:'2017年に提訴',since:2017});\nE.push({a:'gurley',b:'benchmark',k:'link',label:'パートナー'});\n"
 "E.push({a:'khosrowshahi',b:'expedia',k:'from'});\nE.push({a:'kalanick',b:'cloudkitchens',k:'moved'});\nE.push({a:'camp',b:'stumbleupon',k:'from'});\n"
 "['postmates','cornershop','drizly'].forEach(b=>E.push({a:'uber',b,k:'owns',label:b==='postmates'?'2020年に買収':''}));\n"
 "E.push({a:'uber',b:'waymo',k:'link',label:'訴訟→提携'});\nE.push({a:'uber',b:'rivian',k:'invest2',label:'約12.5億ドル(報道)'});\nE.push({a:'uber',b:'rakuten',k:'link',label:'楽天ポイント(日本)'});\n"
 "E.push({a:'brovkina',b:'nakagawa',k:'link',label:'後任'});\n\n")
CO5['uber'] = mk(N, E,
 {'kalanick': 'Travis Kalanick', 'camp': 'Garrett Camp', 'khosrowshahi': 'Dara Khosrowshahi', 'krishnamurthy': 'Balaji Krishnamurthy', 'mahendra': 'Prashanth Mahendra-Rajah',
  'brovkina': 'Yulia Brovkina', 'nakagawa': 'Shintaro Nakagawa', 'gurley': 'Bill Gurley'},
 {'kalanick': 'travisk', 'khosrowshahi': 'dkhos', 'gurley': 'bgurley', 'uber': 'Uber', 'camp': 'gc'},
 {'uber': 'https://www.uber.com', 'benchmark': 'https://www.benchmark.com', 'softbank': 'https://group.softbank', 'toyota': 'https://global.toyota', 'rakuten': 'https://global.rakuten.com'},
 wp(('uber', 'Uber'), ('benchmark', 'Benchmark_(venture_capital_firm)'), ('gv', 'GV_(company)'), ('pif', 'Public_Investment_Fund'), ('softbank', 'SoftBank_Group'), ('toyota', 'Toyota'),
    ('postmates', 'Postmates'), ('cornershop', 'Cornershop'), ('drizly', 'Drizly'), ('waymo', 'Waymo'), ('rivian', 'Rivian'), ('rakuten', 'Rakuten'),
    ('cloudkitchens', 'CloudKitchens'), ('stumbleupon', 'StumbleUpon'), ('expedia', 'Expedia_Group')),
 {'kalanick': [['2009', 'Uberを共同創業'], ['2010', 'CEOに就任'], ['2017', '6月にCEOを辞任'], ['2019', '取締役を退く']],
  'khosrowshahi': [['2005', 'ExpediaのCEO'], ['2017', 'UberのCEOに就任']]}, {}, 'uber')

# ================= newmo =================
N = [
 {'id': 'newmo', 'name': 'newmo', 'kind': 'c', 'from': 2024, 'desc': '2024年1月に設立された、日本のモビリティの会社。大阪でタクシー会社を傘下に収め、府内3位規模のタクシーグループになったと説明されています。創業からの累計の調達額は約199億円(2026年7月時点の採用ページ)。'},
 {'id': 'aoyagi', 'name': '青柳直樹', 'kind': 'p', 'from': 2024, 'desc': '代表取締役CEO。メルカリ・メルペイの経営者を務めたのち、2024年にnewmoを設立しました。', 'role': '代表取締役CEO / 創業者', 'founder': 1},
 {'id': 'mercari', 'name': 'Mercari', 'kind': 'i', 'from': 2024, 'desc': '2024年2月のシード(約15億円、14社)に参加と報じられています。青柳氏の出身元でもあります。', 'role': '出資者・出身元'},
 {'id': 'michinori', 'name': 'Michinori Holdings', 'kind': 'i', 'from': 2024, 'desc': 'みちのりホールディングス。バスなどの地域交通の会社。2024年のシードに参加と報じられています。', 'role': '出資者'},
 {'id': 'anri', 'name': 'ANRI', 'kind': 'i', 'from': 2024, 'desc': '日本のVC。2024年のシードに参加と報じられています。', 'role': 'VC'},
 {'id': 'bdash', 'name': 'B Dash Ventures', 'kind': 'i', 'from': 2024, 'desc': '日本のVC。2024年のシードに参加と報じられています。', 'role': 'VC'},
 {'id': 'kansai', 'name': 'Kansai Mirai Venture Fund', 'kind': 'i', 'from': 2025, 'desc': '関西みらいベンチャーファンド。2025年7月に出資し、同ファンドの第1号案件になりました。', 'role': 'ファンド'},
 {'id': 'yamada', 'name': '山田進太郎', 'kind': 'o', 'from': 2024, 'desc': 'メルカリの創業者。青柳氏の元の上司にあたります。', 'role': 'メルカリ創業者'},
 {'id': 'osakataxi', 'name': '大阪のタクシー会社', 'kind': 'o', 'from': 2025, 'desc': '大阪のタクシー会社(複数)。newmoが傘下に収め、府内で3位規模のグループを形成したと説明されています。', 'role': '傘下のタクシー会社'},
 {'id': 'go', 'name': 'GO', 'kind': 'o', 'from': 2024, 'desc': 'タクシーアプリの大手。配車で競合します。', 'role': '競合'},
 {'id': 'uber', 'name': 'Uber', 'kind': 'o', 'from': 2024, 'desc': '日本でも配車で競合する世界最大手。', 'role': '競合'},
]
E = (std('newmo') + "E.push({a:'aoyagi',b:'mercari',k:'from'});\nE.push({a:'yamada',b:'mercari',k:'link',label:'創業者'});\nE.push({a:'aoyagi',b:'yamada',k:'link',label:'元の上司'});\n"
 "E.push({a:'newmo',b:'osakataxi',k:'owns',label:'傘下に収める'});\nE.push({a:'newmo',b:'go',k:'conflict',label:'配車で競合'});\nE.push({a:'newmo',b:'uber',k:'conflict',label:'配車で競合'});\n\n")
CO5['newmo'] = mk(N, E, {'aoyagi': 'Naoki Aoyagi', 'yamada': 'Shintaro Yamada'},
 {}, {'newmo': 'https://newmo.me'}, wp(('mercari', 'Mercari'), ('anri', 'ANRI'), ('uber', 'Uber')),
 {'aoyagi': [['〜', 'メルカリ・メルペイの経営者'], ['2024', '1月にnewmoを設立、2月にシード約15億円'], ['2025', '大阪のタクシー会社を傘下に'], ['2026', '累計調達額は約199億円(7月時点)']]}, {}, 'newmo')

# ================= GO =================
N = [
 {'id': 'go', 'name': 'GO', 'kind': 'c', 'from': 2020, 'desc': 'タクシー配車アプリ「GO」の会社。2020年4月にDeNAのタクシー事業とJapanTaxiが統合してMobility Technologiesとなり、2023年にGO株式会社へ改称。従業員は約600人(2026年6月)。配車事業は2025年5月期に、通期で初めて黒字化と報じられています。'},
 {'id': 'kawanabe', 'name': '川鍋一朗', 'kind': 'p', 'from': 2020, 'desc': '日本交通の会長で、GOの経営に関わる中心人物として知られます。', 'role': '会長(報道)'},
 {'id': 'nakajima', 'name': '中島宏', 'kind': 'p', 'from': 2020, 'desc': 'Mobility TechnologiesからGOへの社長と報じられています(最新の役職は要確認)。', 'role': '社長(報道・要確認)'},
 {'id': 'namba', 'name': '南場智子', 'kind': 'o', 'from': 2020, 'desc': 'DeNAの創業者。DeNAのタクシー事業を、統合に出しました。', 'role': 'DeNA創業者'},
 {'id': 'dena', 'name': 'DeNA', 'kind': 'i', 'from': 2020, 'desc': '2020年に、タクシーアプリ事業を統合して出資しました。', 'role': '出資者'},
 {'id': 'nihonkotsu', 'name': 'Nihon Kotsu', 'kind': 'i', 'from': 2020, 'desc': '日本交通。JapanTaxiの親会社で、統合の当事者。', 'role': '出資者'},
 {'id': 'waymo', 'name': 'Waymo', 'kind': 'o', 'from': 2025, 'desc': '2025年から、東京で自動運転技術のテストに向けて、GO、日本交通と協業。', 'role': '自動運転の提携先'},
 {'id': 'iris', 'name': 'IRIS', 'kind': 'o', 'from': 2022, 'desc': 'GOのグループ会社(タクシーの運行支援など)。', 'role': 'グループ会社'},
 {'id': 'newmo', 'name': 'newmo', 'kind': 'o', 'from': 2024, 'desc': '大阪などで配車事業に取り組む会社。競合。', 'role': '競合'},
 {'id': 'uber', 'name': 'Uber', 'kind': 'o', 'from': 2020, 'desc': '日本でも配車で競合する世界最大手。', 'role': '競合'},
]
E = (std('go') + "E.push({a:'namba',b:'dena',k:'link',label:'創業者'});\nE.push({a:'kawanabe',b:'nihonkotsu',k:'link',label:'会長'});\nE.push({a:'go',b:'iris',k:'owns'});\n"
 "E.push({a:'go',b:'waymo',k:'link',label:'東京で自動運転のテスト',since:2025});\nE.push({a:'go',b:'newmo',k:'conflict',label:'配車で競合',since:2024});\nE.push({a:'go',b:'uber',k:'conflict',label:'配車で競合'});\n\n")
CO5['go'] = mk(N, E, {'kawanabe': 'Kenichiro Kawanabe', 'nakajima': 'Hiroshi Nakajima', 'namba': 'Tomoko Namba'},
 {'go': 'GO_taxiapp'}, {'go': 'https://go.mo-t.com'}, wp(('dena', 'DeNA'), ('nihonkotsu', 'Nihon_Kotsu'), ('waymo', 'Waymo'), ('uber', 'Uber')), {}, {}, 'go')

# ================= 出前館 =================
N = [
 {'id': 'demaecan', 'name': 'Demae-can', 'kind': 'c', 'from': 2018, 'desc': '出前館。日本のフードデリバリーの大手で、LINEヤフーの傘下。2025年8月期の売上高は約397億円(前期比約21%減)で、赤字が続いています。'},
 {'id': 'yano', 'name': '矢野哲', 'kind': 'p', 'from': 2025, 'desc': '社長(2025年8月期の資料)。', 'role': '社長'},
 {'id': 'fujii', 'name': '藤井英雄', 'kind': 'p', 'from': 2020, 'to': 2025, 'desc': '前の社長(2024年8月期の資料)。', 'role': '元社長'},
 {'id': 'ly', 'name': 'LY Corporation', 'kind': 'i', 'from': 2019, 'desc': 'LINEヤフー。親会社として、取締役の推薦権を持つと開示されています(2024年11月)。保有比率を減らす変更報告書も提出しています。', 'role': '親会社'},
 {'id': 'ubereats', 'name': 'Uber Eats', 'kind': 'o', 'from': 2018, 'desc': '最大の競合。2020年ごろには統合の話もあったと報じられました。', 'role': '競合'},
 {'id': 'wolt', 'name': 'Wolt Japan', 'kind': 'o', 'from': 2021, 'desc': '2026年2月に、DoorDashが日本からの撤退を発表したと報じられています。', 'role': '競合(撤退)'},
 {'id': 'line', 'name': 'LINE', 'kind': 'o', 'from': 2019, 'desc': '2019年にLINEが出資し、出前館と連携を強めました。', 'role': '元の出資者'},
]
E = (std('demaecan') + "E.push({a:'demaecan',b:'ubereats',k:'conflict',label:'最大の競合'});\nE.push({a:'demaecan',b:'wolt',k:'conflict',label:'競合(2026年に撤退)'});\nE.push({a:'yano',b:'fujii',k:'link',label:'前任'});\nE.push({a:'line',b:'ly',k:'link',label:'統合'});\n\n")
CO5['demaecan'] = mk(N, E, {'yano': 'Satoshi Yano', 'fujii': 'Hideo Fujii'},
 {}, {'demaecan': 'https://demae-can.com', 'ly': 'https://www.lycorp.co.jp'}, wp(('ly', 'LY_Corporation'), ('line', 'Line_(software)'), ('ubereats', 'Uber_Eats'), ('wolt', 'Wolt')), {}, {}, 'demaecan')

# ================= DoorDash =================
N = [
 {'id': 'doordash', 'name': 'DoorDash', 'kind': 'c', 'from': 2013, 'desc': '米国のフードデリバリーの最大手。2022年にWolt、2025年10月にDeliveroo(約39〜40億ドルと報じられています)を買収しました。2026年2月に、日本、カタール、シンガポール、ウズベキスタンからの撤退を発表したと報じられています。'},
 {'id': 'xu', 'name': 'トニー・シュー', 'kind': 'p', 'from': 2013, 'desc': '共同創業者で会長兼CEO。スタンフォード大学で、同期3人と共に創業しました。', 'role': 'CEO / 会長 / 共同創業者', 'founder': 1},
 {'id': 'fang', 'name': 'アンディ・ファン', 'kind': 'p', 'from': 2013, 'desc': '共同創業者。', 'role': '共同創業者', 'founder': 1},
 {'id': 'tang', 'name': 'スタンリー・タン', 'kind': 'p', 'from': 2013, 'desc': '共同創業者。', 'role': '共同創業者', 'founder': 1},
 {'id': 'moore', 'name': 'エヴァン・ムーア', 'kind': 'p', 'from': 2013, 'to': 2013, 'desc': '創業時の共同創業者の一人。初期に離れたと伝えられます。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'inukonda', 'name': 'ラビ・イヌコンダ', 'kind': 'p', 'from': 2024, 'desc': 'CFO。', 'role': 'CFO'},
 {'id': 'adarkar', 'name': 'プラビール・アダルカー', 'kind': 'p', 'from': 2020, 'desc': 'COO兼社長。', 'role': 'COO / 社長'},
 {'id': 'kuusi', 'name': 'ミキ・クーシ', 'kind': 'p', 'from': 2022, 'desc': 'Woltの共同創業者。DoorDash Internationalを率い、2025年10月からDeliveroo CEOも兼ねます。', 'role': 'International責任者'},
 {'id': 'softbank', 'name': 'SoftBank Group', 'kind': 'i', 'from': 2018, 'desc': '2018年に出資したと報じられています。', 'role': '出資者'},
 {'id': 'sequoia', 'name': 'Sequoia Capital', 'kind': 'i', 'from': 2013, 'desc': '初期の出資者。', 'role': 'VC'},
 {'id': 'kleiner', 'name': 'Kleiner Perkins', 'kind': 'i', 'from': 2014, 'desc': '初期の出資者の一社。', 'role': 'VC'},
 {'id': 'yc', 'name': 'Y Combinator', 'kind': 'i', 'from': 2013, 'desc': '2013年に参加したアクセラレーター。', 'role': '初期の支援者'},
 {'id': 'wolt', 'name': 'Wolt', 'kind': 'o', 'from': 2022, 'desc': 'フィンランド発のデリバリー。2022年に約81億ドルで買収。', 'role': '買収'},
 {'id': 'deliveroo', 'name': 'Deliveroo', 'kind': 'o', 'from': 2025, 'desc': '英国のデリバリー。2025年10月に買収が完了しました。', 'role': '買収'},
 {'id': 'caviar', 'name': 'Caviar', 'kind': 'o', 'from': 2019, 'desc': '2019年に買収した高級路線のデリバリー。', 'role': '買収'},
 {'id': 'jp', 'name': '日本事業(Wolt Japan)', 'kind': 'o', 'from': 2026, 'desc': 'Woltの日本事業。2026年2月に、撤退を発表したと報じられています。', 'role': '撤退'},
 {'id': 'stanford', 'name': 'Stanford University', 'kind': 'o', 'from': 2013, 'desc': '共同創業者らが出会った大学。', 'role': '出身校'},
]
E = (std('doordash') + "['xu','fang','tang','moore'].forEach(a=>E.push({a,b:'stanford',k:'from'}));\nE.push({a:'doordash',b:'wolt',k:'owns',label:'2022年に買収'});\nE.push({a:'doordash',b:'deliveroo',k:'owns',label:'2025年10月に買収'});\nE.push({a:'doordash',b:'caviar',k:'owns'});\n"
 "E.push({a:'kuusi',b:'wolt',k:'link',label:'共同創業者'});\nE.push({a:'kuusi',b:'deliveroo',k:'link',label:'CEOを兼任',since:2025});\nE.push({a:'wolt',b:'jp',k:'link',label:'2026年2月に撤退',since:2026});\n\n")
CO5['doordash'] = mk(N, E, {'xu': 'Tony Xu', 'fang': 'Andy Fang', 'tang': 'Stanley Tang', 'moore': 'Evan Moore', 'inukonda': 'Ravi Inukonda', 'adarkar': 'Prabir Adarkar', 'kuusi': 'Miki Kuusi'},
 {'xu': 'tonyxu', 'doordash': 'DoorDash'}, {'doordash': 'https://www.doordash.com', 'softbank': 'https://group.softbank'},
 wp(('doordash', 'DoorDash'), ('softbank', 'SoftBank_Group'), ('sequoia', 'Sequoia_Capital'), ('kleiner', 'Kleiner_Perkins'), ('yc', 'Y_Combinator'), ('wolt', 'Wolt'), ('deliveroo', 'Deliveroo'),
    ('caviar', 'Caviar_(delivery_service)'), ('stanford', 'Stanford_University')),
 {'xu': [['2013', 'DoorDashを共同創業、CEOに'], ['2022', 'Woltを買収'], ['2025', '10月にDeliveroo買収を完了'], ['2026', '日本などからの撤退を発表(報道)']]}, {}, 'doordash')

# ================= Waymo =================
N = [
 {'id': 'waymo', 'name': 'Waymo', 'kind': 'c', 'from': 2009, 'desc': 'Googleの自動運転プロジェクト(2009年)が前身の、Alphabet傘下の自動運転の会社。2026年2月に約160億ドルを調達(評価額は約1,260億ドルと報じられています)。米国の6都市でロボタクシーを提供し、2026年にワシントンDCと英国への展開を予定しています。'},
 {'id': 'mawakana', 'name': 'テケドラ・マワカナ', 'kind': 'p', 'from': 2021, 'desc': '共同CEO。2021年に、クラフチックの後任として就任しました。', 'role': '共同CEO'},
 {'id': 'dolgov', 'name': 'ドミトリ・ドルゴフ', 'kind': 'p', 'from': 2014, 'desc': '共同CEO(元CTO)。スタンフォード大学で、スランの下で学びました。', 'role': '共同CEO'},
 {'id': 'krafcik', 'name': 'ジョン・クラフチック', 'kind': 'p', 'from': 2015, 'to': 2021, 'desc': '元CEO(2015〜2021年)。Hyundai Motor Americaの元CEO。', 'role': '元CEO'},
 {'id': 'urmson', 'name': 'クリス・アームソン', 'kind': 'p', 'from': 2009, 'to': 2016, 'desc': 'プロジェクトの初期の責任者。2016年に退き、Auroraを共同創業しました。', 'role': '元プロジェクト責任者'},
 {'id': 'thrun', 'name': 'セバスチャン・スラン', 'kind': 'p', 'from': 2009, 'to': 2012, 'desc': 'プロジェクトの創設者の一人。のちUdacityを共同創業しました。', 'role': '創設者', 'founder': 1},
 {'id': 'levandowski', 'name': 'アンソニー・レヴァンドウスキー', 'kind': 'p', 'from': 2009, 'to': 2016, 'desc': '元エンジニア。2016年に退社してOttoを創業し、Uberに買収されました。2017年の訴訟の中心人物です。', 'role': '元エンジニア'},
 {'id': 'alphabet', 'name': 'Alphabet', 'kind': 'i', 'from': 2009, 'desc': '過半数を保有する親会社。', 'role': '親会社'},
 {'id': 'dragoneer', 'name': 'Dragoneer', 'kind': 'i', 'from': 2026, 'desc': '2026年2月の約160億ドルのラウンドを主導と報じられています。', 'role': '投資会社'},
 {'id': 'dst', 'name': 'DST Global', 'kind': 'i', 'from': 2026, 'desc': '2026年2月のラウンドを主導と報じられています。', 'role': '投資会社'},
 {'id': 'sequoia', 'name': 'Sequoia Capital', 'kind': 'i', 'from': 2026, 'desc': '2026年2月のラウンドを主導と報じられています。', 'role': 'VC'},
 {'id': 'a16z', 'name': 'Andreessen Horowitz', 'kind': 'i', 'from': 2026, 'desc': '2026年2月のラウンドに参加と報じられています。', 'role': 'VC'},
 {'id': 'mubadala', 'name': 'Mubadala Capital', 'kind': 'i', 'from': 2024, 'desc': '2026年のラウンドに参加と報じられています。', 'role': '政府系'},
 {'id': 'silverlake', 'name': 'Silver Lake', 'kind': 'i', 'from': 2024, 'desc': '出資者の一社として報じられています。', 'role': '投資会社'},
 {'id': 'uber', 'name': 'Uber', 'kind': 'o', 'from': 2017, 'desc': '2017年に自動運転の技術をめぐり訴訟。のちに和解し、AustinとAtlantaでUber経由の配車を提供する提携先です。', 'role': '元の対立・現在の提携'},
 {'id': 'go', 'name': 'GO', 'kind': 'o', 'from': 2025, 'desc': '2025年から、東京で自動運転技術のテストに向けて、GO、日本交通と協業しています。', 'role': '日本での協業'},
 {'id': 'nihonkotsu', 'name': 'Nihon Kotsu', 'kind': 'o', 'from': 2025, 'desc': '日本交通。東京での自動運転のテストに協業。', 'role': '日本での協業'},
 {'id': 'aurora', 'name': 'Aurora', 'kind': 'o', 'from': 2016, 'desc': 'アームソンが共同創業した自動運転の会社。', 'role': 'アームソンの新会社'},
 {'id': 'otto', 'name': 'Otto', 'kind': 'o', 'from': 2016, 'desc': 'レヴァンドウスキーが創業した自動運転トラックの会社。Uberが買収。', 'role': '元エンジニアの会社'},
 {'id': 'udacity', 'name': 'Udacity', 'kind': 'o', 'from': 2012, 'desc': 'スランが共同創業したオンライン学習の会社。', 'role': 'スランの新会社'},
]
E = (std('waymo') + "E.push({a:'alphabet',b:'waymo',k:'owns',label:'過半数を保有'});\nE.push({a:'waymo',b:'uber',k:'conflict',label:'2017年に訴訟→提携',since:2017});\nE.push({a:'waymo',b:'go',k:'link',label:'東京で協業',since:2025});\nE.push({a:'waymo',b:'nihonkotsu',k:'link',since:2025});\n"
 "E.push({a:'urmson',b:'aurora',k:'moved'});\nE.push({a:'levandowski',b:'otto',k:'moved'});\nE.push({a:'otto',b:'uber',k:'owns',label:'Uberが買収'});\nE.push({a:'thrun',b:'udacity',k:'moved'});\nE.push({a:'dolgov',b:'thrun',k:'link',label:'師'});\n\n")
CO5['waymo'] = mk(N, E, {'mawakana': 'Tekedra Mawakana', 'dolgov': 'Dmitri Dolgov', 'krafcik': 'John Krafcik', 'urmson': 'Chris Urmson', 'thrun': 'Sebastian Thrun', 'levandowski': 'Anthony Levandowski'},
 {'waymo': 'Waymo'}, {'waymo': 'https://waymo.com', 'uber': 'https://www.uber.com'},
 wp(('waymo', 'Waymo'), ('alphabet', 'Alphabet_Inc.'), ('dragoneer', 'Dragoneer_Investment_Group'), ('dst', 'DST_Global'), ('sequoia', 'Sequoia_Capital'), ('a16z', 'Andreessen_Horowitz'),
    ('silverlake', 'Silver_Lake_(investment_firm)'), ('uber', 'Uber'), ('aurora', 'Aurora_Innovation'), ('otto', 'Otto_(company)'), ('udacity', 'Udacity')),
 {'thrun': [['2009', 'Googleの自動運転プロジェクトを創設'], ['2012', 'Udacityを共同創業']]}, {}, 'waymo')
