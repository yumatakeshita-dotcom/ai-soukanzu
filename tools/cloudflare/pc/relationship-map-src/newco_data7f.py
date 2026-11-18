from newco_data import mk, std, wp

# サラ・ウィン・ウィリアムズの回顧録『Careless People』(2025年3月)と、その登場人物・関係者の図。
# 本の中身は、本人の「主張」であり、事実として確定したものではない。Metaの反論・調査結果・係争の状況を併記する。
# 登場人物は、英語版Wikipediaと報道(NBC、CNN)で、本の中の役割が確認できた人物だけを載せる(本の全文・索引は確認できていない)。
CO7F = {}
WPD = lambda t, label=None: ['出典: Wikipedia(%s)' % (label or t.replace('_', ' ')), 'https://en.wikipedia.org/wiki/' + t]
NBC = ['出典: NBC News(ハラスメントの主張とMetaの反応)', 'https://www.nbcnews.com/tech/social-media/facebook-alleges-harassment-sandberg-kaplan-sarah-wynn-williams-rcna195130']
CNN = ['出典: CNN(2025年3月11日、著者へのインタビュー)', 'https://www.cnn.com/2025/03/11/tech/meta-whistleblower-book-sarah-wynn-williams']
N = [
 {'id': 'book', 'name': '『Careless People』', 'kind': 'c', 'from': 2011, 'desc': '正式な題は『Careless People: A Cautionary Tale of Power, Greed, and Lost Idealism』。2025年3月11日に、Flatiron Books(米)とMacmillan(英)から出た、元Facebook幹部の回顧録(382ページ)。2011年から2017年までのFacebookでの経験をもとに、中国市場への進出の試み、ミャンマー、10代への影響、職場での行為などを「主張」しています。Metaは「古い、すでに報じられた主張の混ぜ物」「ここにある主張は虚偽」と反論しています。ニューヨーク・タイムズのベストセラー1位(2025年3月下旬)。'},
 {'id': 'wynn', 'name': 'サラ・ウィン・ウィリアムズ', 'kind': 'p', 'from': 2011, 'desc': 'ニュージーランド出身の弁護士・外交官。2002〜2007年にニュージーランドの外交官、2007〜2011年に在米大使館で政治・政府関係を担当。2011年にFacebookへ入り、グローバル公共政策のディレクターに。2017年に会社から解雇されました(会社は「成績不振と有害な言動」を理由とし、本人は上司ジョエル・カプランをハラスメントで報告したことへの報復だと主張)。著者。', 'role': '著者 / 元Facebookのグローバル公共政策ディレクター'},
 {'id': 'zuckerberg', 'name': 'マーク・ザッカーバーグ', 'kind': 'p', 'from': 2011, 'desc': '本の中心人物の一人。著者は、中国市場への進出のために、検閲やデータ共有の仕組みを求めたこと、その件で議会に虚偽を述べたことを主張しています(未確認・Metaは否定)。', 'role': 'CEO(本の登場人物)'},
 {'id': 'sandberg', 'name': 'シェリル・サンドバーグ', 'kind': 'p', 'from': 2011, 'to': 2022, 'desc': '当時のCOO。著者は、ダボスから戻る自家用機で、同じベッドで寝るよう繰り返し勧められたと主張しています(サンドバーグはコメントを控えています)。', 'role': '元COO(本の登場人物)'},
 {'id': 'kaplan', 'name': 'ジョエル・カプラン', 'kind': 'p', 'from': 2011, 'desc': '本の中の主な敵対者。当時のグローバル公共政策のVPで、著者の上司。著者は、カプランをハラスメントで報告したと主張しています。Metaは、報告があったことは認めたうえで、2017年の調査で問題なしと判断されたと説明しています。現在はMetaのチーフ・グローバル・アフェアーズ・オフィサー。', 'role': 'Metaのグローバル・アフェアーズ責任者(本の登場人物)'},
 {'id': 'schrage', 'name': 'エリオット・シュレージ', 'kind': 'p', 'from': 2011, 'desc': '著者の上司だった人物。「繰り返された問題への対応の失敗」を理由に、自分が著者を解雇したと、声明で述べています。', 'role': '著者の上司(本の登場人物)'},
 {'id': 'guo', 'name': '郭文貴(グオ・ウェングイ)', 'kind': 'p', 'from': 2015, 'desc': '中国政府の批判者。著者は、中国の規制当局の示唆を受けて、Facebookが郭氏のアカウントを制限したと主張しています。', 'role': '中国政府の批判者(本の登場人物)'},
 {'id': 'meta', 'name': 'Meta', 'kind': 'o', 'from': 2011, 'desc': '旧Facebook。回顧録を、「古い・すでに報じられた主張」「虚偽の主張」と反論し、非難しない合意(非中傷条項)をもとに、仲裁を申し立てました。ダブルクリックで図を開きます。', 'role': '著者の元の勤め先'},
 {'id': 'gowen', 'name': 'ニコラス・ゴーウェン', 'kind': 'p', 'from': 2025, 'desc': '米国仲裁協会(AAA)の緊急仲裁人。2025年3月に、Metaやその役員・取締役・従業員を中傷する発言を、著者がしてはならないという命令を出しました。', 'role': '緊急仲裁人(2025年)'},
 {'id': 'grassley', 'name': 'チャック・グラスリー', 'kind': 'p', 'from': 2025, 'desc': '米上院議員。2025年4月中旬に、ザッカーバーグへ書簡を送り、Metaが著者を黙らせようとしたとの疑いについて、従業員が保護される形で内部告発できるようにするよう求めました。', 'role': '上院議員(書簡)'},
 {'id': 'senate', 'name': '米上院 司法委員会', 'kind': 'o', 'from': 2025, 'desc': '2025年4月9日の公聴会「A Time for Truth」で、著者が、Facebookが中国政府と「手を携えて」検閲したと証言しました。', 'role': '公聴会(2025年4月9日)'},
 {'id': 'flatiron', 'name': 'Flatiron Books / Macmillan', 'kind': 'o', 'from': 2025, 'desc': '本の出版社(米: Flatiron Books、英: Macmillan)。Macmillanは、仲裁人の命令を無視すると表明しました(命令は、出版社への行動命令を含んでいません)。', 'role': '出版社'},
]
E = (std('book') +
 "E.push({a:'wynn',b:'book',k:'link',label:'著者'});\n"
 "E.push({a:'wynn',b:'meta',k:'from',label:'2011〜2017年に在籍'});\n"
 "E.push({a:'wynn',b:'kaplan',k:'conflict',label:'ハラスメントを報告したと主張(Metaは調査で問題なしと説明)',since:2017});\n"
 "E.push({a:'wynn',b:'sandberg',k:'conflict',label:'本の中での主張(サンドバーグはコメントせず)',since:2025});\n"
 "E.push({a:'wynn',b:'zuckerberg',k:'conflict',label:'中国進出などを巡る主張(Metaは否定)',since:2025});\n"
 "E.push({a:'meta',b:'wynn',k:'conflict',label:'2017年に解雇、2025年に仲裁を申し立て',since:2025});\n"
 "E.push({a:'gowen',b:'wynn',k:'link',label:'発言を禁じる命令(2025年3月)',since:2025});\n"
 "E.push({a:'schrage',b:'wynn',k:'link',label:'上司(解雇を行ったと説明)',since:2017});\n"
 "E.push({a:'guo',b:'zuckerberg',k:'link',label:'アカウント制限の件',since:2015});\n"
 "E.push({a:'grassley',b:'zuckerberg',k:'link',label:'書簡(2025年4月)',since:2025});\n"
 "E.push({a:'flatiron',b:'book',k:'link',label:'出版'});\nE.push({a:'wynn',b:'senate',k:'link',label:'証言(2025年4月9日)',since:2025});\n\n")
CAREER = {'wynn': [['2002', 'ニュージーランドの外交官に(〜2007年)'], ['2007', '在米大使館で、政治・政府関係を担当(〜2011年)'], ['2011', 'Facebookに入社(グローバル公共政策)'], ['2017', 'Facebookから解雇'],
                   ['2025', '3月11日に『Careless People』を出版。仲裁人が発言を制限。4月9日に上院司法委員会で証言'], ['2026', '6月、Metaを提訴(仲裁の命令を「不当・違法」と主張)。ヘイ・フェスティバルでは、法的命令のため発言せず']]}
LINKS = {'book': [WPD('Careless_People'), CNN, NBC], 'wynn': [WPD('Sarah_Wynn-Williams'), CNN], 'kaplan': [NBC, WPD('Careless_People')], 'sandberg': [WPD('Careless_People')], 'schrage': [NBC],
         'zuckerberg': [WPD('Careless_People')], 'guo': [WPD('Careless_People')], 'gowen': [WPD('Careless_People')], 'grassley': [WPD('Careless_People')], 'senate': [WPD('Careless_People')]}
CO7F['carelesspeople'] = mk(N, E, {'wynn': 'Sarah Wynn-Williams', 'zuckerberg': 'Mark Zuckerberg', 'sandberg': 'Sheryl Sandberg', 'kaplan': 'Joel Kaplan', 'schrage': 'Elliot Schrage', 'guo': 'Guo Wengui', 'gowen': 'Nicholas Gowen', 'grassley': 'Chuck Grassley'}, {},
 {}, wp(('book', 'Careless_People'), ('wynn', 'Sarah_Wynn-Williams'), ('zuckerberg', 'Mark_Zuckerberg'), ('sandberg', 'Sheryl_Sandberg'), ('kaplan', 'Joel_Kaplan'), ('guo', 'Guo_Wengui'), ('grassley', 'Chuck_Grassley')),
 CAREER, LINKS, 'book')
