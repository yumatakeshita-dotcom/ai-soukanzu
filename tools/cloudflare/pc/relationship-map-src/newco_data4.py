from newco_data import mk, std, wp

CO4 = {}

# ================= X (Twitter) =================
N = [
 {'id': 'twitter', 'name': 'X (Twitter)', 'kind': 'c', 'from': 2006, 'desc': '2006年にTwitterとして創業。2022年にマスクが約440億ドルで買収し、2023年に「X」に改称。2025年3月にxAIが買収(評価額約330億ドルと報じられています)、2026年2月にはSpaceXがxAIを買収しました。2025年7月にヤッカリーノCEOが退任し、後任は確認できていません。'},
 # 創業者
 {'id': 'dorsey', 'name': 'ジャック・ドーシー', 'kind': 'p', 'from': 2006, 'to': 2022, 'desc': '共同創業者。CEOを2007〜2008年と2015〜2021年に務め、2022年5月に取締役を退きました。Square(現Block)の創業者でもあります。', 'role': '元CEO / 共同創業者', 'founder': 1},
 {'id': 'williams', 'name': 'エヴァン・ウィリアムズ', 'kind': 'p', 'from': 2006, 'to': 2012, 'desc': '共同創業者。2008〜2010年にCEOを務めました。Bloggerの創業者で、のちMediumを設立。', 'role': '元CEO / 共同創業者', 'founder': 1},
 {'id': 'stone', 'name': 'ビズ・ストーン', 'kind': 'p', 'from': 2006, 'to': 2011, 'desc': '共同創業者。2011年に離れ、ウィリアムズと共にObviousを立ち上げました。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'glass', 'name': 'ノア・グラス', 'kind': 'p', 'from': 2006, 'to': 2006, 'desc': '共同創業者の一人。創業の年に退いたと伝えられます。', 'role': '元共同創業者', 'founder': 1},
 # 歴代の経営陣
 {'id': 'costolo', 'name': 'ディック・コストロ', 'kind': 'p', 'from': 2010, 'to': 2015, 'desc': '元CEO(2010〜2015年)。上場を主導しました。', 'role': '元CEO'},
 {'id': 'agrawal', 'name': 'パラグ・アグラワル', 'kind': 'p', 'from': 2011, 'to': 2022, 'desc': '元CEO(2021年11月〜2022年10月)。マスクによる買収の完了直後に解任されました。', 'role': '元CEO'},
 {'id': 'gadde', 'name': 'ビジャヤ・ガッデ', 'kind': 'p', 'from': 2011, 'to': 2022, 'desc': '法務・政策の責任者。2022年10月の買収の完了直後に解任されたと報じられています。', 'role': '元法務責任者'},
 {'id': 'segal', 'name': 'ネッド・シーガル', 'kind': 'p', 'from': 2017, 'to': 2022, 'desc': '元CFO。2022年10月の買収の完了直後に解任されたと報じられています。', 'role': '元CFO'},
 {'id': 'taylor', 'name': 'ブレット・テイラー', 'kind': 'p', 'from': 2011, 'to': 2022, 'desc': '元取締役会議長。2022年の買収をめぐり、Twitter側が買収の履行を求めてマスクを提訴した際の議長。現在はOpenAIの取締役会議長。', 'role': '元取締役会議長'},
 {'id': 'musk', 'name': 'イーロン・マスク', 'kind': 'p', 'from': 2022, 'desc': '2022年10月に約440億ドルで買収したオーナー。', 'role': 'オーナー'},
 {'id': 'yaccarino', 'name': 'リンダ・ヤッカリーノ', 'kind': 'p', 'from': 2023, 'to': 2025, 'desc': '元CEO(2023年6月〜2025年7月)。理由を明らかにせず退任し、後任は確認できていません。', 'role': '元CEO'},
 # 出資者
 {'id': 'usv', 'name': 'Union Square Ventures', 'kind': 'i', 'from': 2007, 'desc': '初期の出資者(2007年のシリーズA)として知られます。', 'role': '初期のVC'},
 {'id': 'benchmark', 'name': 'Benchmark', 'kind': 'i', 'from': 2008, 'desc': '2008年の資金調達に参加した初期のVC。', 'role': '初期のVC'},
 {'id': 'ellison', 'name': 'ラリー・エリソン', 'kind': 'i', 'from': 2022, 'desc': 'Oracleの共同創業者。マスクの買収資金に約10億ドルを出したと報じられています。', 'role': '買収資金の出資者'},
 {'id': 'alwaleed', 'name': 'アルワリード・ビン・タラール', 'kind': 'i', 'from': 2022, 'desc': 'サウジの王族投資家。保有分をマスクの買収後にも持ち越したと報じられています。', 'role': '買収時に持ち越し'},
 {'id': 'binance', 'name': 'Binance', 'kind': 'i', 'from': 2022, 'desc': 'マスクの買収資金に約5億ドルを出したと報じられています。', 'role': '買収資金の出資者'},
 {'id': 'sequoia', 'name': 'Sequoia Capital', 'kind': 'i', 'from': 2022, 'desc': 'マスクの買収資金に約8億ドルを出したと報じられています。', 'role': '買収資金の出資者'},
 {'id': 'a16z', 'name': 'Andreessen Horowitz', 'kind': 'i', 'from': 2022, 'desc': 'マスクの買収資金に約4億ドルを出したと報じられています。', 'role': '買収資金の出資者'},
 # 関連組織
 {'id': 'xai', 'name': 'xAI', 'kind': 'o', 'from': 2025, 'desc': '2025年3月にXを買収したマスクのAI企業。', 'role': '親会社'},
 {'id': 'spacex', 'name': 'SpaceX', 'kind': 'o', 'from': 2026, 'desc': '2026年2月にxAIを買収。Xはその傘下になりました。', 'role': '親会社の親会社'},
 {'id': 'odeo', 'name': 'Odeo', 'kind': 'o', 'from': 2006, 'desc': 'ウィリアムズらが先に創業したポッドキャスト会社。Twitterはここから生まれました。', 'role': '前身'},
 {'id': 'obvious', 'name': 'Obvious', 'kind': 'o', 'from': 2011, 'desc': 'ウィリアムズとストーンが2011年に立ち上げた会社。Mediumなどを生みました。', 'role': '創業者らの次の会社'},
 {'id': 'block', 'name': 'Block', 'kind': 'o', 'from': 2009, 'desc': '旧Square。ドーシーが共同創業しました。', 'role': 'ドーシーの会社'},
 {'id': 'bluesky', 'name': 'Bluesky', 'kind': 'o', 'from': 2019, 'desc': 'ドーシーが2019年に出資を始めた、分散型のSNS。ドーシーは取締役も務めました。', 'role': 'ドーシーが支援'},
]
E = (std('twitter') +
 "E.push({a:'musk',b:'twitter',k:'owns',label:'2022年10月に約440億ドルで買収'});\n"
 "E.push({a:'xai',b:'twitter',k:'owns',label:'2025年3月に買収'});\nE.push({a:'spacex',b:'xai',k:'owns',label:'2026年2月に買収'});\n"
 "E.push({a:'taylor',b:'musk',k:'conflict',label:'買収の履行を求め提訴(2022)'});\nE.push({a:'agrawal',b:'musk',k:'conflict',label:'買収完了後に解任(2022)'});\n"
 "['williams','stone','glass'].forEach(a=>E.push({a,b:'odeo',k:'from'}));\nE.push({a:'odeo',b:'twitter',k:'owns',label:'前身'});\n"
 "['williams','stone'].forEach(a=>E.push({a,b:'obvious',k:'moved'}));\nE.push({a:'dorsey',b:'block',k:'link',label:'共同創業'});\nE.push({a:'dorsey',b:'bluesky',k:'link',label:'支援'});\n"
 "E.push({a:'ellison',b:'musk',k:'link',label:'買収資金'});\n\n")
CO4['twitter'] = mk(N, E,
 {'dorsey': 'Jack Dorsey', 'williams': 'Evan Williams', 'stone': 'Biz Stone', 'glass': 'Noah Glass', 'costolo': 'Dick Costolo', 'agrawal': 'Parag Agrawal', 'gadde': 'Vijaya Gadde',
  'segal': 'Ned Segal', 'taylor': 'Bret Taylor', 'musk': 'Elon Musk', 'yaccarino': 'Linda Yaccarino', 'ellison': 'Larry Ellison', 'alwaleed': 'Alwaleed bin Talal'},
 {'dorsey': 'jack', 'williams': 'ev', 'stone': 'biz', 'costolo': 'dickc', 'agrawal': 'paraga', 'musk': 'elonmusk', 'yaccarino': 'lindayacc', 'twitter': 'X', 'xai': 'xai', 'bluesky': 'bluesky'},
 {'twitter': 'https://x.com', 'xai': 'https://x.ai', 'spacex': 'https://www.spacex.com', 'bluesky': 'https://bsky.social', 'block': 'https://block.xyz'},
 wp(('twitter', 'Twitter'), ('xai', 'XAI_(company)'), ('spacex', 'SpaceX'), ('usv', 'Union_Square_Ventures'), ('benchmark', 'Benchmark_(venture_capital_firm)'), ('binance', 'Binance'),
    ('sequoia', 'Sequoia_Capital'), ('a16z', 'Andreessen_Horowitz'), ('odeo', 'Odeo'), ('obvious', 'Obvious_Corporation'), ('block', 'Block,_Inc.'), ('bluesky', 'Bluesky')),
 {'dorsey': [['2006', 'Twitterを共同創業'], ['2009', 'Squareを共同創業'], ['2015', 'CEOに復帰'], ['2021', 'CEOを辞任'], ['2022', '5月に取締役も退く']],
  'musk': [['2022', '4月に買収を提案、10月に約440億ドルで完了'], ['2023', '社名を「X」に'], ['2025', 'xAIがXを買収'], ['2026', 'SpaceXがxAIを買収']]}, {}, 'twitter')

# ================= Notion =================
N = [
 {'id': 'notion', 'name': 'Notion', 'kind': 'c', 'from': 2013, 'desc': 'ノートや文書、データベースをまとめて扱うツールの会社。2021年のシリーズCで評価額は約100億ドル。2025年12月に約120億ドルで、社員の持ち株の売却(テンダーオファー)を検討と報じられています。2026年の増資は確認できていません。'},
 {'id': 'zhao', 'name': 'イワン・ジャオ', 'kind': 'p', 'from': 2013, 'desc': '共同創業者でCEO。ほぼ行き詰まった製品を作り直すため、京都に移住したことで知られます。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'last', 'name': 'サイモン・ラスト', 'kind': 'p', 'from': 2013, 'desc': '共同創業者。ジャオと共に京都で製品を作り直しました。', 'role': '共同創業者', 'founder': 1},
 {'id': 'kothari', 'name': 'アクシェイ・コタリ', 'kind': 'p', 'from': 2019, 'desc': 'COO(資料により共同創業者と表記)。ニュースアプリPulseの共同創業者で、PulseはLinkedInに買収されました。', 'role': 'COO'},
 {'id': 'sequoia', 'name': 'Sequoia Capital', 'kind': 'i', 'from': 2019, 'desc': '2019年のシリーズAを主導し、2021年にも出資したと報じられています。', 'role': 'VC'},
 {'id': 'index', 'name': 'Index Ventures', 'kind': 'i', 'from': 2020, 'desc': '2020年に約5,000万ドルを出資した(評価額約20億ドル)と報じられています。', 'role': 'VC'},
 {'id': 'coatue', 'name': 'Coatue', 'kind': 'i', 'from': 2021, 'desc': '2021年のシリーズC(約2.75億ドル、評価額約100億ドル)で名前が挙がっています。', 'role': '投資会社'},
 {'id': 'naval', 'name': 'ナヴァル・ラヴィカント', 'kind': 'i', 'from': 2016, 'desc': 'AngelListの共同創業者。初期の個人投資家の一人と報じられています。', 'role': '個人投資家'},
 {'id': 'kyoto', 'name': '京都', 'kind': 'o', 'from': 2015, 'desc': 'ジャオとラストが、ほぼ行き詰まった製品を作り直すため、移り住んだ都市。のちNotionの出発点として語られます。', 'role': '再出発の地'},
 {'id': 'inkling', 'name': 'Inkling', 'kind': 'o', 'from': 2013, 'desc': 'ジャオが創業前に勤めていた会社。', 'role': '出身元'},
 {'id': 'cron', 'name': 'Cron', 'kind': 'o', 'from': 2022, 'desc': 'カレンダーのアプリ。2022年に買収し、Notion Calendarに。', 'role': '買収'},
 {'id': 'skiff', 'name': 'Skiff', 'kind': 'o', 'from': 2024, 'desc': 'メールのアプリ。2024年に買収と報じられています。', 'role': '買収'},
 {'id': 'pulse', 'name': 'Pulse', 'kind': 'o', 'from': 2013, 'desc': 'コタリが共同創業したニュースアプリ。LinkedInに買収されました。', 'role': 'コタリの出身元'},
]
E = std('notion') + "E.push({a:'zhao',b:'kyoto',k:'link',label:'移住'});\nE.push({a:'last',b:'kyoto',k:'link',label:'移住'});\nE.push({a:'zhao',b:'inkling',k:'from'});\nE.push({a:'kothari',b:'pulse',k:'from'});\nE.push({a:'notion',b:'cron',k:'owns',label:'2022年に買収'});\nE.push({a:'notion',b:'skiff',k:'owns',label:'2024年に買収'});\n\n"
CO4['notion'] = mk(N, E, {'zhao': 'Ivan Zhao', 'last': 'Simon Last', 'kothari': 'Akshay Kothari', 'naval': 'Naval Ravikant'},
 {'zhao': 'ivanhzhao', 'notion': 'NotionHQ', 'naval': 'naval'}, {'notion': 'https://www.notion.com', 'sequoia': 'https://www.sequoiacap.com', 'index': 'https://www.indexventures.com'},
 wp(('notion', 'Notion_(productivity_software)'), ('sequoia', 'Sequoia_Capital'), ('index', 'Index_Ventures'), ('coatue', 'Coatue_Management'), ('naval', 'Naval_Ravikant'), ('inkling', 'Inkling_(company)')),
 {'zhao': [['〜', 'Inklingで働く'], ['2013', 'Notionを共同創業'], ['2015', '京都へ移住し、製品を作り直す'], ['2018', '新しいNotionを公開']]}, {}, 'notion')

# ================= Figma =================
N = [
 {'id': 'figma', 'name': 'Figma', 'kind': 'c', 'from': 2012, 'desc': 'ブラウザで動くデザインツールの会社。2022年にAdobeが約200億ドルで買収を発表しましたが、規制当局の懸念で2023年12月に白紙となり、違約金10億ドルが支払われました。2025年7月31日にNYSEへ上場(公開価格33ドル)。'},
 {'id': 'field', 'name': 'ディラン・フィールド', 'kind': 'p', 'from': 2012, 'desc': '共同創業者でCEO。2025年4月に会長にも就任。ティール・フェローで、ブラウン大学を中退して創業しました。二層株式で議決権の過半(約74%と報じられています)を握ります。', 'role': 'CEO / 会長 / 共同創業者', 'founder': 1},
 {'id': 'wallace', 'name': 'エヴァン・ウォレス', 'kind': 'p', 'from': 2012, 'to': 2021, 'desc': '共同創業者。ブラウン大学の同級生で、ブラウザで動く3D技術(WebGL)の専門家。2021年に離れ、株式の議決権はフィールドに委任されています。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'melwani', 'name': 'プラヴィール・メルワニ', 'kind': 'p', 'from': 2017, 'desc': 'CFO。上場時の資料に名前が出ています(2022年からCFOとする資料があります)。', 'role': 'CFO'},
 {'id': 'index', 'name': 'Index Ventures', 'kind': 'i', 'from': 2013, 'desc': '初期の出資者として知られます。', 'role': 'VC'},
 {'id': 'greylock', 'name': 'Greylock', 'kind': 'i', 'from': 2015, 'desc': '初期の出資者として知られます。', 'role': 'VC'},
 {'id': 'kleiner', 'name': 'Kleiner Perkins', 'kind': 'i', 'from': 2018, 'desc': '出資者の一社として報じられています。', 'role': 'VC'},
 {'id': 'sequoia', 'name': 'Sequoia Capital', 'kind': 'i', 'from': 2020, 'desc': '出資者の一社として報じられています。', 'role': 'VC'},
 {'id': 'thiel', 'name': 'ピーター・ティール', 'kind': 'o', 'from': 2012, 'desc': 'ティール・フェローシップを通じて、フィールドの創業を支えた人物。', 'role': 'フェローシップの主宰'},
 {'id': 'thielfellow', 'name': 'Thiel Fellowship', 'kind': 'o', 'from': 2012, 'desc': '大学を離れて起業する若者に資金を出す、ティールの奨学プログラム。フィールドが選ばれました。', 'role': '創業の支援'},
 {'id': 'adobe', 'name': 'Adobe', 'kind': 'o', 'from': 2022, 'desc': '2022年9月に約200億ドルでの買収を発表。規制当局の懸念で、2023年12月に断念しました(違約金10億ドル)。', 'role': '買収を断念'},
 {'id': 'nyse', 'name': 'NYSE', 'kind': 'o', 'from': 2025, 'desc': '2025年7月31日に上場(ティッカー「FIG」)。初日は公開価格の3倍超で取引されたと報じられています。', 'role': '上場先'},
 {'id': 'brown', 'name': 'Brown University', 'kind': 'o', 'from': 2012, 'desc': 'フィールドとウォレスの出会いの場。', 'role': '出身校'},
 {'id': 'linkedin', 'name': 'LinkedIn', 'kind': 'o', 'from': 2012, 'desc': 'フィールドが創業前にインターンとして働いた会社と報じられています。', 'role': '出身元'},
]
E = (std('figma') + "E.push({a:'adobe',b:'figma',k:'conflict',label:'200億ドルの買収を断念',since:2022});\nE.push({a:'figma',b:'nyse',k:'link',label:'2025年7月に上場',since:2025});\n"
 "['field','wallace'].forEach(a=>E.push({a,b:'brown',k:'from'}));\nE.push({a:'field',b:'linkedin',k:'from'});\nE.push({a:'thiel',b:'thielfellow',k:'link',label:'主宰'});\nE.push({a:'field',b:'thielfellow',k:'link',label:'フェロー'});\n"
 "E.push({a:'wallace',b:'field',k:'link',label:'議決権を委任'});\n\n")
CO4['figma'] = mk(N, E, {'field': 'Dylan Field', 'wallace': 'Evan Wallace', 'melwani': 'Praveer Melwani', 'thiel': 'Peter Thiel'},
 {'field': 'zoink', 'figma': 'figma'}, {'figma': 'https://www.figma.com', 'adobe': 'https://www.adobe.com'},
 wp(('figma', 'Figma'), ('index', 'Index_Ventures'), ('greylock', 'Greylock_Partners'), ('kleiner', 'Kleiner_Perkins'), ('sequoia', 'Sequoia_Capital'), ('thielfellow', 'Thiel_Fellowship'),
    ('adobe', 'Adobe_Inc.'), ('nyse', 'New_York_Stock_Exchange'), ('brown', 'Brown_University'), ('linkedin', 'LinkedIn')),
 {'field': [['〜', 'LinkedInでインターン'], ['2012', 'ティール・フェローに選ばれ、Figmaを共同創業'], ['2022', 'Adobeが買収を発表'], ['2023', '買収が白紙に'], ['2025', '上場、会長にも就任']]}, {}, 'figma')

# ================= Stripe =================
N = [
 {'id': 'stripe', 'name': 'Stripe', 'kind': 'c', 'from': 2010, 'desc': 'オンライン決済の会社。2026年2月の従業員向けの持ち株売却(テンダーオファー)で、評価額は約1,590億ドルと報じられています(2025年は約915億ドル)。経営陣は、当面の上場の予定はないと説明しています。'},
 {'id': 'pcollison', 'name': 'パトリック・コリソン', 'kind': 'p', 'from': 2010, 'desc': '共同創業者でCEO。アイルランド出身で、MITを中退しました。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'jcollison', 'name': 'ジョン・コリソン', 'kind': 'p', 'from': 2010, 'desc': '共同創業者で社長。パトリックの弟で、ハーバード大学を中退しました。', 'role': '社長 / 共同創業者', 'founder': 1},
 {'id': 'brockman', 'name': 'グレッグ・ブロックマン', 'kind': 'p', 'from': 2010, 'to': 2015, 'desc': '初期のエンジニアで、元CTO。2015年にStripeを離れ、OpenAIを共同創業しました。', 'role': '元CTO'},
 {'id': 'daniela', 'name': 'ダニエラ・アモデイ', 'kind': 'p', 'from': 2013, 'to': 2018, 'desc': '元幹部。2018年にOpenAIへ移り、のちAnthropicを共同創業しました。', 'role': '元幹部'},
 {'id': 'patil', 'name': 'ラフル・パティル', 'kind': 'p', 'from': 2020, 'to': 2025, 'desc': '元CTO。2025年10月にAnthropicのCTOに就任しました。', 'role': '元CTO'},
 {'id': 'sequoia', 'name': 'Sequoia Capital', 'kind': 'i', 'from': 2011, 'desc': '2011年のシリーズAを主導した初期の出資者。', 'role': 'VC'},
 {'id': 'foundersfund', 'name': 'Founders Fund', 'kind': 'i', 'from': 2011, 'desc': 'ピーター・ティールのVC。初期から出資しました。', 'role': 'VC'},
 {'id': 'a16z', 'name': 'Andreessen Horowitz', 'kind': 'i', 'from': 2012, 'desc': '初期の出資者で、2026年のテンダーオファーでも主な資金の出し手と報じられています。', 'role': 'VC'},
 {'id': 'thrive', 'name': 'Thrive Capital', 'kind': 'i', 'from': 2020, 'desc': '2026年のテンダーオファーの主な資金の出し手と報じられています。', 'role': 'VC'},
 {'id': 'coatue', 'name': 'Coatue', 'kind': 'i', 'from': 2020, 'desc': '2026年のテンダーオファーの主な資金の出し手と報じられています。', 'role': '投資会社'},
 {'id': 'tiger', 'name': 'Tiger Global', 'kind': 'i', 'from': 2020, 'desc': '出資者の一社。', 'role': '投資会社'},
 {'id': 'musk', 'name': 'イーロン・マスク', 'kind': 'i', 'from': 2011, 'desc': '2011年の初期の個人投資家の一人と報じられています。', 'role': '初期の個人投資家'},
 {'id': 'thiel', 'name': 'ピーター・ティール', 'kind': 'i', 'from': 2011, 'desc': 'Founders Fundを通じて、初期に出資しました。', 'role': '初期の個人投資家'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2015, 'desc': 'ブロックマンとアモデイの移籍先。', 'role': '移籍先'},
 {'id': 'anthropic', 'name': 'Anthropic', 'kind': 'o', 'from': 2021, 'desc': 'アモデイが共同創業し、パティルがCTOになった会社。', 'role': '移籍先'},
 {'id': 'auctomatic', 'name': 'Auctomatic', 'kind': 'o', 'from': 2010, 'desc': 'パトリックが10代で創業し、約500万ドルで売却した会社と伝えられます。', 'role': '創業前の会社'},
]
E = (std('stripe') + "E.push({a:'brockman',b:'openai',k:'moved'});\nE.push({a:'daniela',b:'openai',k:'moved'});\nE.push({a:'daniela',b:'anthropic',k:'moved'});\nE.push({a:'patil',b:'anthropic',k:'moved'});\n"
 "E.push({a:'pcollison',b:'jcollison',k:'link',label:'兄弟'});\nE.push({a:'pcollison',b:'auctomatic',k:'link',label:'創業'});\nE.push({a:'thiel',b:'foundersfund',k:'link'});\n\n")
CO4['stripe'] = mk(N, E, {'pcollison': 'Patrick Collison', 'jcollison': 'John Collison', 'brockman': 'Greg Brockman', 'daniela': 'Daniela Amodei', 'patil': 'Rahul Patil', 'musk': 'Elon Musk', 'thiel': 'Peter Thiel'},
 {'pcollison': 'patrickc', 'jcollison': 'collision', 'stripe': 'stripe', 'musk': 'elonmusk'}, {'stripe': 'https://stripe.com', 'openai': 'https://openai.com', 'anthropic': 'https://www.anthropic.com'},
 wp(('stripe', 'Stripe,_Inc.'), ('sequoia', 'Sequoia_Capital'), ('foundersfund', 'Founders_Fund'), ('a16z', 'Andreessen_Horowitz'), ('thrive', 'Thrive_Capital'), ('coatue', 'Coatue_Management'),
    ('tiger', 'Tiger_Global_Management'), ('openai', 'OpenAI'), ('anthropic', 'Anthropic')),
 {'pcollison': [['2008', 'Auctomaticを売却'], ['2010', 'Stripeを共同創業'], ['2026', 'テンダーオファーで評価額約1,590億ドル(報道)']]}, {}, 'stripe')

# ================= Canva =================
N = [
 {'id': 'canva', 'name': 'Canva', 'kind': 'c', 'from': 2013, 'desc': 'オーストラリア発のデザインツールの会社。2025年8月の従業員向けの持ち株売却で、評価額は約420億ドルと報じられています(さらに高い数字の報道もあります)。上場は「ここ数年のうちに」とされ、日程は確認できていません。'},
 {'id': 'perkins', 'name': 'メラニー・パーキンス', 'kind': 'p', 'from': 2013, 'desc': '共同創業者でCEO。投資家100社近くに断られた末に、創業した話で知られます。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'obrecht', 'name': 'クリフ・オブレヒト', 'kind': 'p', 'from': 2013, 'desc': '共同創業者でCOO。パーキンスの夫でもあります。上場は「数年以内」と語り、ナスダックを示唆しました(2025年11月)。', 'role': 'COO / 共同創業者', 'founder': 1},
 {'id': 'adams', 'name': 'キャメロン・アダムス', 'kind': 'p', 'from': 2013, 'desc': '共同創業者で、最高製品責任者。', 'role': 'CPO / 共同創業者', 'founder': 1},
 {'id': 'kawasaki', 'name': 'ガイ・カワサキ', 'kind': 'p', 'from': 2014, 'to': 2018, 'desc': '元チーフ・エバンジェリスト。Appleの元エバンジェリストとしても知られます。', 'role': '元チーフ・エバンジェリスト'},
 {'id': 'rasmussen', 'name': 'ラース・ラスムセン', 'kind': 'i', 'from': 2013, 'desc': 'Google Mapsの共同創業者。創業初期に出資・助言したと伝えられます。', 'role': '初期の個人投資家'},
 {'id': 'blackbird', 'name': 'Blackbird Ventures', 'kind': 'i', 'from': 2013, 'desc': '最大のVC出資者として報じられています。', 'role': 'VC'},
 {'id': 'sequoia', 'name': 'Sequoia Capital', 'kind': 'i', 'from': 2018, 'desc': '出資者の一社として報じられています。', 'role': 'VC'},
 {'id': 'felicis', 'name': 'Felicis', 'kind': 'i', 'from': 2015, 'desc': '出資者の一社として報じられています。', 'role': 'VC'},
 {'id': 'gc', 'name': 'General Catalyst', 'kind': 'i', 'from': 2019, 'desc': '出資者の一社として報じられています。', 'role': 'VC'},
 {'id': 'greenoaks', 'name': 'Greenoaks', 'kind': 'i', 'from': 2021, 'desc': '2021年の増資に参加と報じられています。', 'role': '投資会社'},
 {'id': 'troweprice', 'name': 'T. Rowe Price', 'kind': 'i', 'from': 2021, 'desc': '2021年の増資に参加と報じられています。', 'role': '資産運用会社'},
 {'id': 'franklin', 'name': 'Franklin Templeton', 'kind': 'i', 'from': 2021, 'desc': '2021年の増資に参加と報じられています。', 'role': '資産運用会社'},
 {'id': 'fusion', 'name': 'Fusion Books', 'kind': 'o', 'from': 2013, 'desc': 'パーキンスが2007年に始めた、学校の卒業アルバムを作るオンラインの事業。Canvaの原点。', 'role': '原点の事業'},
 {'id': 'uwa', 'name': 'University of Western Australia', 'kind': 'o', 'from': 2013, 'desc': 'パーキンスが学んだ大学。', 'role': '出身校'},
 {'id': 'affinity', 'name': 'Affinity', 'kind': 'o', 'from': 2024, 'desc': 'デザインソフトの会社(Serif)。2024年に買収しました。', 'role': '買収'},
 {'id': 'leonardo', 'name': 'Leonardo.ai', 'kind': 'o', 'from': 2024, 'desc': '画像生成AIの会社。2024年に買収しました。', 'role': '買収'},
 {'id': 'pexels', 'name': 'Pexels', 'kind': 'o', 'from': 2019, 'desc': '無料の写真・動画の素材サイト。2019年にPixabayと共に買収しました。', 'role': '買収'},
]
E = (std('canva') + "E.push({a:'perkins',b:'obrecht',k:'link',label:'夫婦'});\nE.push({a:'perkins',b:'fusion',k:'link',label:'創業'});\nE.push({a:'canva',b:'fusion',k:'owns',label:'原点'});\nE.push({a:'perkins',b:'uwa',k:'from'});\n"
 "['affinity','leonardo','pexels'].forEach(b=>E.push({a:'canva',b,k:'owns'}));\nE.push({a:'rasmussen',b:'perkins',k:'link',label:'助言・出資'});\n\n")
CO4['canva'] = mk(N, E, {'perkins': 'Melanie Perkins', 'obrecht': 'Cliff Obrecht', 'adams': 'Cameron Adams', 'kawasaki': 'Guy Kawasaki', 'rasmussen': 'Lars Rasmussen'},
 {'perkins': 'Mel_Perkins', 'canva': 'canva'}, {'canva': 'https://www.canva.com', 'blackbird': 'https://www.blackbird.vc'},
 wp(('canva', 'Canva'), ('blackbird', 'Blackbird_Ventures'), ('sequoia', 'Sequoia_Capital'), ('gc', 'General_Catalyst'), ('greenoaks', 'Greenoaks_Capital'), ('troweprice', 'T._Rowe_Price'),
    ('franklin', 'Franklin_Templeton'), ('uwa', 'University_of_Western_Australia'), ('affinity', 'Affinity_(software)'), ('leonardo', 'Leonardo_AI'), ('pexels', 'Pexels')),
 {'perkins': [['2007', 'Fusion Booksを始める'], ['2013', 'Canvaを共同創業'], ['2024', 'AffinityとLeonardo.aiを買収'], ['2025', '評価額約420億ドルの売却(報道)']]}, {}, 'canva')

# ================= Cursor (Anysphere) =================
N = [
 {'id': 'cursor', 'name': 'Anysphere (Cursor)', 'kind': 'c', 'from': 2022, 'desc': 'AIコード編集ツール「Cursor」の会社。2025年11月に約23億ドルのシリーズD(評価額約293億ドル)。2026年4月に約20億ドル・約500億ドルの増資が報じられましたが、成立は確認できていません。SpaceXによる買収の報道もありますが、信頼できる情報源では確認できていません。'},
 {'id': 'truell', 'name': 'マイケル・トゥルエル', 'kind': 'p', 'from': 2022, 'desc': '共同創業者でCEO。MITの出身。', 'role': 'CEO / 共同創業者', 'founder': 1},
 {'id': 'asif', 'name': 'スアレー・アシフ', 'kind': 'p', 'from': 2022, 'desc': '共同創業者。MITの出身。', 'role': '共同創業者', 'founder': 1},
 {'id': 'sanger', 'name': 'アマン・サンガー', 'kind': 'p', 'from': 2022, 'desc': '共同創業者。MITの出身。', 'role': '共同創業者', 'founder': 1},
 {'id': 'lunnemark', 'name': 'アルビッド・ルンネマルク', 'kind': 'p', 'from': 2022, 'to': 2025, 'desc': '共同創業者。2025年10月に退社し、AIの安全性を研究するIntegrous Researchを立ち上げたと報じられています。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'thrive', 'name': 'Thrive Capital', 'kind': 'i', 'from': 2025, 'desc': '2025年5月のシリーズB(約9億ドル、評価額約99億ドル)を主導と報じられています。', 'role': 'VC'},
 {'id': 'a16z', 'name': 'Andreessen Horowitz', 'kind': 'i', 'from': 2025, 'desc': '2025年のラウンドに参加と報じられています。', 'role': 'VC'},
 {'id': 'accel', 'name': 'Accel', 'kind': 'i', 'from': 2025, 'desc': '2025年11月のシリーズDを共同で主導と報じられています。', 'role': 'VC'},
 {'id': 'coatue', 'name': 'Coatue', 'kind': 'i', 'from': 2025, 'desc': '2025年11月のシリーズDを共同で主導と報じられています。', 'role': '投資会社'},
 {'id': 'dst', 'name': 'DST Global', 'kind': 'i', 'from': 2025, 'desc': '2025年5月のラウンドに参加と報じられています。', 'role': '投資会社'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2025, 'desc': '2025年11月のシリーズDに出資と報じられています。', 'role': '出資 + GPU供給'},
 {'id': 'google', 'name': 'Google', 'kind': 'i', 'from': 2025, 'desc': '2025年11月のシリーズDに出資と報じられています。', 'role': '戦略出資者'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2022, 'desc': 'OpenAIのスタートアップ向けファンドが、初期に出資したと報じられています。', 'role': '初期の出資者'},
 {'id': 'mit', 'name': 'MIT', 'kind': 'o', 'from': 2022, 'desc': '4人の共同創業者の出身校。', 'role': '出身校'},
 {'id': 'integrous', 'name': 'Integrous Research', 'kind': 'o', 'from': 2025, 'desc': 'ルンネマルクが2025年に立ち上げた、安全性を研究するAI研究所。', 'role': '退社後の会社'},
 {'id': 'spacex', 'name': 'SpaceX', 'kind': 'o', 'from': 2026, 'desc': '2026年6月に約600億ドルで買収したとする報道が一部にありますが、信頼できる情報源では確認できていません。', 'role': '買収の報道(未確認)'},
]
E = (std('cursor') + "['truell','asif','sanger','lunnemark'].forEach(a=>E.push({a,b:'mit',k:'from'}));\nE.push({a:'lunnemark',b:'integrous',k:'moved'});\nE.push({a:'openai',b:'cursor',k:'invest2',label:'初期出資'});\nE.push({a:'spacex',b:'cursor',k:'invest2',label:'買収の報道(未確認)',since:2026});\n\n")
CO4['cursor'] = mk(N, E, {'truell': 'Michael Truell', 'asif': 'Sualeh Asif', 'sanger': 'Aman Sanger', 'lunnemark': 'Arvid Lunnemark'},
 {'truell': 'mntruell', 'cursor': 'cursor_ai', 'nvidia': 'nvidia'}, {'cursor': 'https://cursor.com', 'nvidia': 'https://www.nvidia.com', 'a16z': 'https://a16z.com'},
 wp(('cursor', 'Cursor_(company)'), ('thrive', 'Thrive_Capital'), ('a16z', 'Andreessen_Horowitz'), ('accel', 'Accel_(company)'), ('coatue', 'Coatue_Management'), ('dst', 'DST_Global'),
    ('nvidia', 'Nvidia'), ('google', 'Google'), ('openai', 'OpenAI'), ('mit', 'Massachusetts_Institute_of_Technology'), ('spacex', 'SpaceX')),
 {}, {}, 'cursor')

# ================= Slack =================
N = [
 {'id': 'slack', 'name': 'Slack', 'kind': 'c', 'from': 2009, 'desc': '仕事のチャットツール。ゲーム「Glitch」を作っていた会社Tiny Speckから生まれました。2021年にSalesforceが約277億ドルで買収。2025年12月に、CEOのデニス・ドレッサーがOpenAIの最高売上責任者に移ると報じられました。'},
 {'id': 'butterfield', 'name': 'スチュワート・バターフィールド', 'kind': 'p', 'from': 2009, 'to': 2022, 'desc': '共同創業者でCEO。写真共有サービスFlickrの共同創業者でもあります。2022年に退任を発表しました。', 'role': '元CEO / 共同創業者', 'founder': 1},
 {'id': 'henderson', 'name': 'カル・ヘンダーソン', 'kind': 'p', 'from': 2009, 'desc': '共同創業者でCTO。Flickrの初期の開発者でもあります。', 'role': 'CTO / 共同創業者', 'founder': 1},
 {'id': 'jones', 'name': 'リディアン・ジョーンズ', 'kind': 'p', 'from': 2023, 'to': 2024, 'desc': '元CEO。のちマッチングアプリのBumbleのCEOに就任したと報じられています。', 'role': '元CEO'},
 {'id': 'dresser', 'name': 'デニス・ドレッサー', 'kind': 'p', 'from': 2023, 'to': 2025, 'desc': '元CEO。Salesforceに長く在籍し、2025年12月にOpenAIの最高売上責任者に就任と報じられています(就任時期は報道により食い違い)。', 'role': '元CEO'},
 {'id': 'seaman', 'name': 'ロブ・シーマン', 'kind': 'p', 'from': 2025, 'desc': 'ドレッサーの退任後に、暫定でSlackを率いたと報じられています。', 'role': '暫定の責任者'},
 {'id': 'benioff', 'name': 'マーク・ベニオフ', 'kind': 'p', 'from': 2021, 'desc': 'Salesforceの共同創業者でCEO。2021年にSlackを買収しました。', 'role': '親会社のCEO'},
 {'id': 'accel', 'name': 'Accel', 'kind': 'i', 'from': 2010, 'desc': '初期の出資者として知られます。', 'role': 'VC'},
 {'id': 'a16z', 'name': 'Andreessen Horowitz', 'kind': 'i', 'from': 2013, 'desc': '出資者の一社として報じられています。', 'role': 'VC'},
 {'id': 'socialcapital', 'name': 'Social Capital', 'kind': 'i', 'from': 2014, 'desc': '出資者の一社として報じられています。', 'role': 'VC'},
 {'id': 'salesforce', 'name': 'Salesforce', 'kind': 'o', 'from': 2021, 'desc': '2021年に約277億ドルで買収した親会社。', 'role': '親会社'},
 {'id': 'flickr', 'name': 'Flickr', 'kind': 'o', 'from': 2009, 'desc': 'バターフィールドとヘンダーソンが先に創業した写真共有サービス。', 'role': '前の会社'},
 {'id': 'glitch', 'name': 'Glitch', 'kind': 'o', 'from': 2009, 'desc': 'Tiny Speckが作っていたオンラインゲーム。社内の連絡用のツールが、Slackの原型になりました。', 'role': '原型'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2025, 'desc': 'ドレッサーの移籍先(最高売上責任者)。', 'role': '移籍先'},
 {'id': 'bumble', 'name': 'Bumble', 'kind': 'o', 'from': 2024, 'desc': 'ジョーンズの移籍先と報じられています。', 'role': '移籍先'},
]
E = (std('slack') + "E.push({a:'salesforce',b:'slack',k:'owns',label:'2021年に約277億ドルで買収'});\nE.push({a:'benioff',b:'salesforce',k:'link',label:'CEO'});\n"
 "['butterfield','henderson'].forEach(a=>E.push({a,b:'flickr',k:'from'}));\nE.push({a:'glitch',b:'slack',k:'owns',label:'原型'});\nE.push({a:'dresser',b:'openai',k:'moved'});\nE.push({a:'jones',b:'bumble',k:'moved'});\n\n")
CO4['slack'] = mk(N, E, {'butterfield': 'Stewart Butterfield', 'henderson': 'Cal Henderson', 'jones': 'Lidiane Jones', 'dresser': 'Denise Dresser', 'seaman': 'Rob Seaman', 'benioff': 'Marc Benioff'},
 {'butterfield': 'stewart', 'benioff': 'Benioff', 'slack': 'SlackHQ', 'openai': 'OpenAI'}, {'slack': 'https://slack.com', 'salesforce': 'https://www.salesforce.com', 'openai': 'https://openai.com'},
 wp(('slack', 'Slack_(software)'), ('accel', 'Accel_(company)'), ('a16z', 'Andreessen_Horowitz'), ('socialcapital', 'Social_Capital'), ('salesforce', 'Salesforce'), ('flickr', 'Flickr'),
    ('glitch', 'Glitch_(video_game)'), ('openai', 'OpenAI'), ('bumble', 'Bumble_(app)')),
 {'butterfield': [['2004', 'Flickrを共同創業(のちYahooが買収)'], ['2009', 'Tiny Speckを創業'], ['2013', 'Slackを公開'], ['2021', 'Salesforceが買収'], ['2022', '退任を発表']]}, {}, 'slack')
