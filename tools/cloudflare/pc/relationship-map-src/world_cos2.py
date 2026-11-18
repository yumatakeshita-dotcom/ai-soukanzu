# 世界の企業(2): 東南アジア・インド。2026年11月8日に下の一覧ページ・記事から読み取ったもの(記載のある事実のみ)。
SRC2 = {
 'L': ('Failory『The Full List of 87 Unicorn Startups in India (2026)』', 'https://www.failory.com/startups/india-unicorns'),
 'M': ('Failory『The Full List of 30 Unicorn Startups in Singapore (2026)』', 'https://www.failory.com/startups/singapore-unicorns'),
 'N': ('Next Unicorn Ventures『The Full List of Unicorn Startups in Southeast Asia』', 'https://nextunicorn.ventures/the-full-list-of-unicorn-startups-in-southeast-asia/'),
 'O': ('wakka-inc『ベトナムの日本人起業家・日本企業の成功事例』', 'https://wakka-inc.com/blog/1634/'),
 'P': ('JETRO『アジア進出の一歩目をフィリピンで』', 'https://www.jetro.go.jp/biz/areareports/special/2018/0902/05f3df1343432c79.html'),
 'Q': ('日本総研『東南アジアで活躍し始めた日本人スタートアップ』(2016)', 'https://www.jri.co.jp/file/report/rim/pdf/9646.pdf'),
 'R': ('STORYTELLING『AERA「インドで起業」特集にCEO見上すぐりのインタビュー』', 'https://storytelling-jp.com/aera-ceo-mikami-interview/'),
}


def _u(rows, g):
    """Failory形式 '会社名|分野|設立年|評価額' → 世界の企業の行"""
    out = []
    for n, ind, est, who, val in rows:
        out.append((n, '', g, ind, 0, who, est, 'L' if g == 'インド' else 'M', ('評価額' + val) if val else ''))
    return out


_IN = [
 ('PhonePe','フィンテック・決済',2015,'Burzin Engineer、Rahul Chari、Sameer Nigam','$15B'),
 ('BYJU\'S','教育(EdTech)',2011,'Byju Raveendran、Divya Gokulnath','$22B'),
 ('Dream11','ファンタジースポーツ',2008,'','$8B'),
 ('Razorpay','フィンテック・決済',2014,'Harshil Mathur、Shashank Kumar','$7.5B'),
 ('Zepto','食料品配達',2021,'Aadit Palicha、Kaivalya Vohra','$7B'),
 ('Groww','フィンテック',2016,'','$7B'),
 ('Snapdeal','小売',2005,'','$7B'),
 ('Ola','モビリティ',2010,'','$7B'),
 ('CRED','フィンテック',2018,'','$6.4B'),
 ('Lenskart','小売(メガネ)',2008,'','$6B'),
 ('Pine Labs','フィンテック',1998,'','$5B'),
 ('VerSe Innovation','メディア',2007,'','$5B'),
 ('ShareChat','SNS',2015,'','$5B'),
 ('OfBusiness','フィンテック',2015,'','$5B'),
 ('Meesho','小売(EC)',2015,'','$4B'),
 ('Upstox','フィンテック',2009,'','$4B'),
 ('OYO','旅行',2012,'','$4B'),
 ('Unacademy','教育',2015,'','$3.44B'),
 ('CARS24','モビリティ',2015,'','$3.3B'),
 ('Eruditus Executive Education','教育',2010,'','$3.1B'),
 ('Zetwerk','法人向け',2018,'','$3.1B'),
 ('BharatPe','フィンテック',2018,'','$3B'),
 ('Physics Wallah','教育',2014,'','$3B'),
 ('Infra.Market','法人向け',2016,'','$3B'),
 ('Games24x7','ゲーム',2006,'','$3B'),
 ('Mobile Premier League','ゲーム',2018,'','$2.45B'),
 ('UpGrad','教育',2015,'','$2.25B'),
 ('CoinDCX','暗号資産',2018,'','$2.15B'),
 ('Polygon','暗号資産',2017,'','$2B'),
 ('Rapido','モビリティ',2015,'','$2B'),
 ('Spinny','中古車',2015,'','$2B'),
 ('InMobi','広告',2007,'','$2B'),
 ('Glance','AI',2019,'','$2B'),
 ('Yubi','フィンテック',2017,'','$2B'),
 ('CoinSwitch','暗号資産',2017,'','$2B'),
 ('slice','フィンテック',2016,'','$2B'),
 ('Udaan','法人向けEC',2016,'','$2B'),
 ('Xpressbees','物流',2015,'','$2B'),
 ('DealShare','小売',2018,'','$2B'),
 ('Cult.fit','フィットネス',2016,'','$2B'),
 ('ElasticRun','小売',2016,'','$2B'),
 ('boAt','消費者向け機器',2016,'','$1.4B'),
 ('Rebel Foods','フードサービス',2011,'','$1.4B'),
 ('Pristyn Care','ヘルスケア',2018,'','$1.4B'),
 ('Purplle','美容EC',2012,'','$1.3B'),
 ('Shiprocket','物流',2017,'','$1.21B'),
 ('Porter','物流',2014,'','$1.2B'),
 ('Livspace','住宅インテリア',2014,'','$1.2B'),
 ('CarDekho','モビリティ',2008,'','$1.2B'),
 ('The Good Glamm Group','美容',2015,'','$1.2B'),
 ('Moneyview','フィンテック',2014,'','$1.2B'),
 ('Apna','求人',2019,'','$1.1B'),
 ('LEAD','教育',2012,'','$1.1B'),
 ('InCred','フィンテック',2016,'','$1.05B'),
 ('Krutrim','AI',2023,'','$1B'),
 ('Acko','保険(InsurTech)',2016,'','$1B'),
 ('Vedantu','教育',2011,'','$1B'),
 ('NoBroker','不動産',2014,'','$1B'),
 ('Licious','食品EC',2015,'','$1B'),
 ('Jumbotail','小売',2015,'','$1B'),
 ('Darwinbox','人事SaaS',2015,'','$1B'),
 ('Oxyzo','フィンテック',2016,'','$1B'),
 ('Open Financial Technologies','フィンテック',2017,'','$1B'),
 ('Droom','中古車',2014,'','$1B'),
 ('Rivigo','物流',2014,'','$1B'),
 ('Quikr','分類広告',2008,'','$1B'),
 ('Perfios Software Solutions','法人向けソフト',2008,'','$1B'),
 ('LeadSquared','SaaS',2011,'','$1B'),
 ('Hasura','クラウド',2017,'','$1B'),
 ('1mg','医薬品EC',2015,'','$1B'),
]
_SG = [
 ('Airwallex','決済・金融',2015,'Jack Zhang、Jacob Dai、Ki-Lok Wong、Lucy Yueting Liu、Max Li','$8B'),
 ('MiniMax','生成AI',2021,'Junjie Yan','$4B'),
 ('Grab Financial Group','金融サービス',2018,'Ankur Mehrotra','$3B'),
 ('Sky Mavis','ブロックチェーン・ゲーム',2019,'Aleksander Leonard Larsen、Jeffrey Zirlin','$3B'),
 ('Moglix','法人向けEC',2015,'Rahul Garg','$3B'),
 ('bolttech','保険(InsurTech)',2020,'Richard Li','$2.1B'),
 ('Trax','小売向け画像認識',2010,'Dror Feldheim、Joel Bar-El','$2B'),
 ('Matrixport','暗号資産',2019,'Daniel Yan、Jihan Wu、Yuesheng Ge','$2B'),
 ('Ninja Van','物流',2014,'','$2B'),
 ('Kredivo Group','フィンテック',2015,'','$2B'),
 ('Advance Intelligence Group','AI',2016,'','$2B'),
 ('Spark Education Group','教育',2016,'','$2B'),
 ('Coda','メディア',2011,'','$2B'),
 ('Nium','フィンテック',2014,'','$1.4B'),
 ('Klook','旅行',2014,'','$1.35B'),
 ('Carousell','マーケットプレイス',2012,'','$1.1B'),
 ('Airalo','eSIM',2019,'','$1B'),
 ('PatSnap','特許・技術インテリジェンス',2007,'','$1B'),
 ('Silicon Box','半導体',2021,'','$1B'),
 ('ONE Championship','格闘技メディア',2011,'','$1B'),
 ('Carro','中古車',2015,'','$1B'),
]
R2 = _u(_IN, 'インド') + _u(_SG, '東南アジア') + [
 ('Grab','シンガポール','東南アジア','配車・交通サービス',0,'Anthony Tan',0,'N',''),
 ('Sea (Garena/Shopee)','シンガポール','東南アジア','eコマース・ゲーム',0,'',0,'N',''),
 ('Razer','シンガポール','東南アジア','ゲーマー向けハードウェア',0,'',0,'N',''),
 ('Lazada','シンガポール','東南アジア','オンラインショッピング',0,'',0,'N',''),
 ('Gojek','インドネシア','東南アジア','配車・オンデマンドサービス',0,'',0,'N',''),
 ('Traveloka','インドネシア','東南アジア','旅行予約',0,'Ferry Unardi',0,'N',''),
 ('Tokopedia','インドネシア','東南アジア','オンラインマーケットプレイス',0,'',0,'N',''),
 ('Bukalapak','インドネシア','東南アジア','オンラインマーケットプレイス',0,'Achmad Zacky、Muhammad Fajrin Rasyid、Nugroho Herushyono',0,'N',''),
 ('Revolution Precrafted','フィリピン','東南アジア','プレファブ住宅・不動産',0,'Robbie Antonio',0,'N','日本人創業ではなく現地の企業(JETROの記事の記載)'),
 ('VNG','ベトナム','東南アジア','オンラインゲーム・eコマース',0,'',0,'N',''),
 # 日本人が創業・経営(東南アジア・インド)
 ('Manabie','ベトナム','東南アジア','オンライン学習(EdTech)',1,'本間拓也(共同創業者)',0,'O',''),
 ('Pizza 4P\'s','ベトナム','東南アジア','ピザレストランチェーン',1,'益子さん夫妻',0,'O',''),
 ('KAMEREO','ベトナム','東南アジア','飲食店向けのB2B仕入れ・サプライチェーン',1,'田中卓',0,'O',''),
 ('YOYO Holdings','シンガポール・フィリピン','東南アジア','ロックスクリーン広告アプリ',1,'',2012,'P','シンガポールで2012年創業、フィリピンで2014年にサービス開始(JETROの記事)'),
 ('Empag','シンガポール・タイ','東南アジア','産地直送野菜の宅配',1,'',0,'Q','2016年時点の日本総研資料の記載'),
 ('TalentEx','シンガポール','東南アジア','オンライン人材採用',1,'',0,'Q','2016年時点の日本総研資料の記載'),
 ('Sunrise Advertising Solutions','ベトナム','東南アジア','広告',1,'',2010,'Q','2010年にベトナムで設立(日本総研資料の記載)'),
 ('STORYTELLING LLP','インド','インド','日本企業のインド進出を支援するデジタルマーケティング',1,'見上すぐり',2016,'R','2016年に駐在員の配偶者としてインドへ渡り起業'),
 ('Incubate Fund India','インド','インド','インドのスタートアップへ投資するベンチャーキャピタル',1,'村上なお',2016,'R','日本発のVC。2016年設立'),
]

# 子会社・買収(図に買収元の登録がない会社の案件)。2026年11月8日、報道・企業発表で確認したもの。形: (買収された会社, 国, 事業, 補足)
_M = [
 ('Avidity Biosciences','米国','RNAを標的とする送達技術','Novartisが約120億ドル(全額現金)で買収に合意、2025年10月26日発表(報道)'),
 ('Blueprint Medicines','米国','全身性肥満細胞症治療薬Ayvakit','Sanofiが最大95億ドル(前払い91億ドル、1株129ドル+CVR最大6ドル)で取得、2025年7月に完了(報道)'),
 ('Akero Therapeutics','米国','MASH治療薬efruxifermin','Novo Nordiskが最大52億ドル(前払い約47億ドル、1株54ドル+CVR最大6ドル)で買収、2025年10月(Novo Nordiskの発表)'),
 ('89bio','米国','MASH治療薬','Rocheが最大35億ドル(現金24億ドル、1株14.5ドル+CVR最大6ドル)で買収(報道)'),
 ('SpringWorks Therapeutics','米国','希少疾患・がん','Merck KGaAが約34〜39億ドルで買収(出どころにより金額が異なる)'),
 ('ezCater','米国','法人向けケータリングのマーケットプレイス','Uberが約23億ドル(現金)で買収に合意、2026年10月5日発表。取引総額は直近12か月で25億ドル超(Bloomberg・Boston Globe)'),
 ('Dominion Energy','米国','電力・ガス','NextEra Energyが668億ドルで合併、2026年5月18日発表(集計サイト。未確認)'),
 ('Coterra Energy','米国','石油・ガス','Devon Energyが580億ドルで買収、2026年2月発表(集計サイト。完了は出どころにより異なる)'),
 ('Unilever食品事業','英国','食品','McCormickが427〜448億ドルで統合、2026年3月31日発表(集計サイト)'),
 ('TK Elevator','ドイツ','エレベーター','Koneが約344億ドルで買収(集計サイト。未確認)'),
 ('Warner Bros. Discovery','米国','メディア','Paramount Skydanceが約1,100億ドルで買収、Netflixとの争奪戦。2026年10月に完了とする集計が1つ(未確認)'),
 ('第一三共ヘルスケア','日本','OTC医薬品','サントリーHDが2,465億円で段階的に取得(2029年6月までに完了予定)。第一三共は2026年4月に売却を発表(アンドプロ)'),
 ('GMOデジタルラボ(店舗販促アプリ事業)','日本','店舗向け販促アプリ','GMOコマースが2026年6月15日に子会社化を発表、取得価額7.01億円+最大1億円の成果対価(財経新聞)'),
 ('RGF International Recruitment','日本','国際人材紹介','Fullcastが6.09億円で取得、2026年1月発表・4月1日移転予定(リクルートが売却。Staffing Industry Analysts)'),
]
R2 = R2 + [(n, c, '子会社・買収', b + '。' + t, 0, '', 0, 'M', '') for n, c, b, t in _M]

_M2 = [
 ('Discover Financial Services','米国','カード・決済','Capital Oneが全額株式(1株=1.0192株)で買収、約353億ドル。2024年2月発表、2025年5月18日完了(購入対価の公正価値は518億ドル。10-K)'),
 ('Fubo(FuboTV)','米国','ライブTVストリーミング','Disneyが約70%の持分を取得しHulu + Live TVと統合、2025年10月下旬に完了。Disneyが2.2億ドル支払い、1.45億ドルの融資(Deadline・Front Office Sports)'),
 ('NFL Network等のNFLメディア資産','米国','スポーツ放送','ESPNが2026年1月に取得し、NFLがESPNの10%の非支配持分を得る。公正価値は約30億ドル(Disneyの10-Q)'),
 ('ローソン(非公開化)','日本','コンビニ','KDDIが約5,000億円のTOB(1株10,360円)、2024年に成立。2024年8月15日から三菱商事とKDDIが議決権を50%ずつ保有(完全子会社化ではない。日経)'),
 ('Alphawave Semi','英国','コネクティビティ半導体','Qualcommが実質企業価値約24億ドル(183ペンス)で買収、2025年6月に合意、のちに完了(Seeking Alpha)'),
 ('Celestial AI','米国','光インターコネクト','Marvellが最低32.5億ドル(現金10億ドル+株式22.5億ドル)、最大55億ドル(売上条件)。2025年12月発表、のちに完了(CNBC・SDxCentral)'),
 ('Sana','スウェーデン','AIの学習・エージェント','Workdayが11億ドルで買収、2025年9月発表、完了は11月4日の報道'),
 ('Paradox','米国','会話型の採用AI','Workdayが2025年夏に発表、完了(Investing.com)'),
 ('Flowise','米国','ローコードのAIエージェント構築','Workdayが2025年8月に買収(報道)'),
 ('Consolidated Precision Products','米国','航空機部品','GE Aerospaceが117.5億ドルで買収に合意、完了は2027年後半の見込み(集計サイトの1つのみ)'),
 ('Ultra Maritime','英国','水中・対潜水艦','Lockheed Martinが34.5億ドルで買収に合意(集計サイト)'),
 ('Sundyne','米国','産業用ポンプ・コンプレッサー','Honeywellが2025年6月に21.6億ドルで取得(10-K)'),
]
R2 = R2 + [(n, c, '子会社・買収', b + '。' + t, 0, '', 0, 'M', '') for n, c, b, t in _M2]

# 日本のスタートアップのM&A(2026年1〜4月の78件)。FIRST CVC『2026年のスタートアップM&A事例一覧』(https://www.firstcvc.jp/m-a/year/2026)
SRC2['N2'] = ('FIRST CVC『2026年のスタートアップM&A事例一覧』', 'https://www.firstcvc.jp/m-a/year/2026')
import os as _os
_p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '_jpma.txt')
if _os.path.exists(_p):
    for _ln in open(_p, encoding='utf-8'):
        _a = _ln.strip().split('|')
        if len(_a) == 4:
            R2.append((_a[2], '日本', '子会社・買収', _a[3] + '。' + _a[1] + 'が買収(' + _a[0] + ')', 0, '', 0, 'N2', ''))

# AIスタートアップの2026年の買収(集計サイト Acquired・Tech Startups。金額は発表・報道ベース、『協議中』は未成立)
SRC2['N3'] = ('Acquired『AI startup acquisitions in 2026』', 'https://www.startupsacquired.com/reports/ai-startup-acquisitions-2026')
_AI = [
 ('Hugging Face','Nvidia','2026-09-03','Nvidiaの8-Kによると購入価格約119億ドル+従業員維持の株式報酬最大約10億ドル(129億ドルは両者の合計)'),
 ('World Labs','AMD','2026-09-28','82億ドル'),
 ('OpenRouter','Stripe','2026-08','75億ドル(別の表では8億ドル以上と食い違う)'),
 ('Poolside','Nvidia','2026-08-21','買収ではなく、開発技術のライセンス約60億ドルと100人超の採用(Toms Hardware)'),
 ('Modular','Qualcomm','2026-06-24','約39億ドル(株式。完了)。Chris Lattnerの会社'),
 ('Fin(旧Intercom)','Salesforce','2026-06-15','約36億ドル'),
 ('MaintainX','Autodesk','2026-05','36億ドル'),
 ('Listen Labs','Salesforce','2026-09-29','金額非公表(約20億ドルは交渉段階の報道)。11月2日に完了(Salesforceの発表)'),
 ('Arize AI','Dynatrace','2026-08-13','9.15億ドル(AIオブザーバビリティ)'),
 ('RealSense','Cognex','2026-09-22','約6億ドル(Intelからのスピンアウト)'),
 ('Coefficient Bio','Anthropic','2026','4億ドル(1つの集計サイトのみ)'),
 ('Topaz Labs','Adobe','2026-06-25','約3.4億ドル(AI映像・写真の高画質化)'),
 ('Glass Imaging','OpenAI','2026-09-14','3億ドル超(報道)'),
 ('Reflection','Nvidia','2026-10-10','約250億ドル(FT報道。協議中で未成立)'),
 ('Tenstorrent','Qualcomm','2026-06-15','80〜100億ドル(協議中で未成立)'),
 ('Decart','Amazon','2026-10-11','約70億ドル(WSJ報道。協議中で未成立)'),
 ('Inception','Microsoft','2026-05-13','10億ドル超(協議中で未成立)'),
]
R2 = R2 + [(n, '米国', '子会社・買収', buyer + 'が買収(' + d + ')。' + t, 0, '', 0, 'N3', '') for n, buyer, d, t in _AI]

# 日本のスタートアップ・企業のM&A(2026年9〜10月)と中国の案件。フォースタートアップス『スタートアップM&Aニュース』、M&A Onlineの週次まとめ、報道
SRC2['N4'] = ('フォースタートアップス『スタートアップM&Aニュース』(2026年9〜10月)', 'https://www.forstartups.com/news/ma-news-20261019')
_JP2 = [
 ('サークレイス','日本','HHH1が2026-10-22にTOBで完全子会社化(上場廃止)。金額非公表'),
 ('BASE(Peer-to-Peer系)','日本','SBINMが2026-10-22にTOB。取得日10月28日、3,100万円(同名の別会社の可能性あり)'),
 ('レカムIEパートナー','日本','レカムが2026-10-19に完全子会社化。非公表'),
 ('With The World','日本','ビズメイツが2026-10-05に株式90.7%を取得して子会社化、2億96万円(取得日10月30日)'),
 ('Acrosstudio','日本','ココナラが2026-10-07に株式51%を取得して子会社化、8.67億円(取得日10月30日)'),
 ('富士テクニカルリサーチ','日本','日本企業成長投資が2026-10-07に完全子会社化(取得日10月1日)。非公開'),
 ('アウターク','日本','チェンジホールディングスが2026-09-16に株式約6割を取得して子会社化'),
 ('コラビット','日本','Faciloが2026-09-17に取得(内容は開示なし)'),
 ('シェアリングテクノロジー','日本','MP-2606がTOB・上場廃止(取得期間9月10日〜10月27日)、約390.77億円(2026-09-09発表)'),
 ('All Ads','日本','AA分割準備が2026-09-10に取得(取得時期10月)。非公開'),
 ('シニアライフクリエイト','日本','三井製糖(DM)が2026-09-10に完全子会社化(取得時期9月末)。非公開'),
 ('xbs','日本','ヒットが2026-10-15に買収、ナディアの取得と合わせて12.9億円で完全子会社化(M&A Online)'),
 ('moze','日本','MyDearestが2026-10-16に完全子会社化。金額非公表(M&A Online)'),
 ('Renew','日本','i-plugが2026-10-14に完全子会社化(M&A Online)'),
 ('エージェントキューブ','日本','TalentXが2026-10-01に子会社化(M&A Online)'),
 ('arcbricks','日本','サークレイスが2026-10-29に子会社化(システム開発。M&A Online)'),
 ('アロカ','日本','東陽テクニカルが2026-10-29に子会社化(放射線測定装置。M&A Online)'),
 ('ムラキ','日本','イクヨが2026-10-26にTOBで子会社化へ(M&A Online)'),
]
R2 = R2 + [(n, c, '子会社・買収', t, 0, '', 0, 'N4', '') for n, c, t in _JP2]
SRC2['N5'] = ('36Kr・Tracxn・報道(中国の買収案件)', 'https://eu.36kr.com/en/p/3768963813061123')
_CN = [
 ('Dingdong(叮咚買菜)の中国事業','中国','Meituanが2026年2月に約7.17億ドルで買収に合意(規制当局の承認待ち)。1,000か所超のマイクロフルフィルメントセンターを持つ生鮮EC'),
 ('Pupu(朴朴)','中国','Alibabaが2026年6月に15億ドルで入札したとの報道。Meituanと争い、結果は未確認(未成立)'),
 ('Lingxi Games(靈犀互娯)','中国','Alibabaの子会社を、Trustar Capitalが20億ドル超で買収する報道(2026年8月。未確認)'),
]
R2 = R2 + [(n, c, '子会社・買収', t, 0, '', 0, 'N5', '') for n, c, t in _CN]

_M3 = [
 ('ZFのADAS事業','ドイツ','先進運転支援システム','Samsung傘下のHarmanが約15億ユーロ(報道により17.6〜18億ドル)で買収、2025年12月23日発表。約3,750人が対象(KED Global・SamMobile)'),
 ('Masimoのオーディオ事業(Bowers & Wilkins含む)','米国','オーディオ','Harmanが3.5億ドルで取得(報道)'),
 ('FläktGroup','ドイツ','空調(データセンター冷却)','Samsung Electronicsが約15億ユーロ(約17億ドル)で買収に合意、2025年5月発表。Harman以来の最大の買収(Korea JoongAng Daily)'),
 ('Arduino','イタリア','オープンソースのハードウェア','Qualcommが2025年10月7日に買収に合意、金額非公表。Qualcommの独立した子会社として運営(EE Times)'),
 ('Ventana Micro Systems','米国','RISC-Vプロセッサ','Qualcommが買収を発表(RISC-Vの強化。Alphawave Semi完了と同月。Yahoo Finance)'),
 ('SambaNova Systems(買収交渉)','米国','AI半導体','Intelが約16億ドル(負債込み)の買収を協議したが2026年に不調に終わり、提携と3.5億ドルのラウンドへの参加になった。買収は未成立(CNBC・DCD)'),
 ('GMS','米国','建材の流通','Home Depot(SRS Distribution)が1株110ドル、株式価値約43億ドル(負債込み約55億ドル)で買収、2025年9月に完了(Retail Dive・Yahoo Finance)'),
 ('Foundation Building Materials(FBM)','米国','内装建材の流通','Lowe\'sが約88億ドルで買収、2025年8月20日発表・10月に完了(Lowe\'sの発表)'),
 ('Artisan Design Group','米国','住宅向け内装','Lowe\'sが約13億ドルで買収(報道)'),
 ('Mingledorff\'s','米国','HVAC(空調)','Home Depotが2026年5月に買収完了(金額は未確認)'),
 ('Vizio','米国','テレビ・スマートTV','Walmartが1株11.50ドル(株式価値約23億ドル)の現金で買収、2024年12月3日に完了(Walmartの発表)'),
]
R2 = R2 + [(n, c, '子会社・買収', b + '。' + t, 0, '', 0, 'M', '') for n, c, b, t in _M3]

_M4 = [
 ('USスチール','米国','鉄鋼','日本製鉄が1株55ドルで全株を取得し完全子会社化、約141〜142億ドル(約2兆円)。2025年6月18日に完了、NYSEを上場廃止(日経)'),
 ('Aspen Insurance','バミューダ','保険','SOMPOインターナショナルが約35億ドルの現金で買収に合意、2025年8月。完了は2026年上期の見込み(S&P・Insurance Journal)'),
 ('Legal & Generalの米国事業','米国','保険','明治安田が約23億ドルで買収、2026年2月に完了と報道(Insurance Journal)'),
 ('Resolution Life Group','米国','保険','日本生命が約1.2兆円(約84億ドル)で買収、2025年10月に完了、豪州事業はAcenda Groupに統合と報道(Fitch・Bloomberg)'),
 ('Shriram Finance(20%出資)','インド','ノンバンク','三菱UFJ銀行が第三者割当増資を引き受け20%を取得、約6,823億円(約3,962億ルピー)。2025年12月発表、2026年4月8日に完了(MUFGの発表)'),
 ('Yes Bank(20%出資)','インド','銀行','三井住友FGが約15.8億ドルで20%を取得、2024年にも追加取得(報道。2024年頃の古い案件)'),
 ('CADENAS','ドイツ','製造業向けソフト','キーエンスが2025年5月に買収を発表、数百億円規模とみられる(日経)'),
 ('TraceParts','フランス','CADデータ','キーエンスが2026年10月23日に買収を発表(報道)'),
 ('日立GLS(白物家電)','日本','家電','ノジマが1,000億円超(約1,100億円)で買収、2026年4月発表(日経。日立の家電事業)'),
 ('Evolution Championship Series(EVO)','米国','格闘ゲーム大会','ソニー・インタラクティブエンタテインメントがTriple Perfectから買収、金額非公表(報道)'),
]
R2 = R2 + [(n, c, '子会社・買収', b + '。' + t, 0, '', 0, 'M', '') for n, c, b, t in _M4]

# 2026年のスタートアップ買収(金額の大きい順の上位。Acquired『Top startup acquisitions of 2026』)。金額は集計サイトの値で、発表・報道ベース
SRC2['N6'] = ('Acquired『Top startup acquisitions of 2026』', 'https://www.startupsacquired.com/top-startup-acquisitions/2026')
_p6 = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '_sa2026.txt')
if _os.path.exists(_p6):
    for _ln in open(_p6, encoding='utf-8'):
        _a = _ln.strip().split('|')
        if len(_a) == 5:
            R2.append((_a[2], '', '子会社・買収', _a[4] + '。' + _a[1] + 'が買収(' + _a[0] + '、' + _a[3] + ')', 0, '', 0, 'N6', ''))

# スポーツチームの買収・売却(報道ベース。承認待ち・未成立・未確認のものはその旨を書いた)
SRC2['N7'] = ('S&P Global・ESPN・Yahoo Sports・Forbes Japan・Insider等の報道(スポーツチームの売買)', 'https://www.spglobal.com/market-intelligence/en/news-insights/articles/2026/7/record-seahawks-sale-highlights-surge-in-sports-team-valuations-103791988')
_SP = [
 ('Los Angeles Lakers(2026年の売却)','米国','NBA','Bob IgerとJosh Kushnerが支配持分を評価額約125億ドルで買う合意(報道。NBAの承認待ち。Yahooは120億ドル)。2025年にMark Walterが100億ドルで買ったばかりで、米国スポーツチーム売買の最高額'),
 ('Los Angeles Lakers(2025年の売却)','米国','NBA','Mark Walter(Dodgers共同オーナー、TWG Global CEO)がBuss家から約100億ドルで取得(2025年。報道)'),
 ('Seattle Seahawks','米国','NFL','Khosla家(Vinod Khoslaのグループ)がPaul Allenの遺産管理団体から96億ドルで買う合意、NFL記録(2026年。NFLの承認待ち)'),
 ('Boston Celtics','米国','NBA','Bill Chisholmが率いるグループが評価額61億ドル超で取得、NBAが承認(2025年)'),
 ('Portland Trail Blazers','米国','NBA','Tom DundonがPaul Allenの遺産管理団体から約42.5億ドルで取得(2026年。GiveMeSport・SI)'),
 ('Los Angeles Angels','米国','MLB','Stan KroenkeがArte Moreno氏から約40億ドル(約6,300億円)で買うと報道(2026年。MLB史上最高額、完了は未確認)'),
 ('San Diego Padres','米国','MLB','Feliciano & Kwanza Jonesが約39億ドルで買う合意(2026年5月。2012年の取得額は8億ドル)'),
 ('Washington Commanders','米国','NFL','Josh Harrisが約60.5億ドルで取得(2023年。参考)'),
 ('Liverpool FC(40%の売却)','英国','プレミアリーグ','Fenway Sports Groupが保有の40%を、Jeff Bezosを含むコンソーシアムに売却したと報道(2026年。S&P Global)。FSGは別の新球団の支配持分(約27億ドル)の協議にも入った(2026年11月5日。合意は未発表)'),
 ('Everton FC','英国','プレミアリーグ','Friedkin Groupが売却を模索。評価額は約8億ポンド(スタジアム債務約3.5億ポンド込み)〜10億ポンド。新オーナーは復活祭後に確定し得るが、完了は2027年4〜5月の見込み(Yahoo Sports・Insider。未確定)'),
 ('West Ham United(25%)','英国','プレミアリーグ','Amanda StaveleyとMehrdad GhodoussiがGold家から25%を買う合意と報道(Substack。他の出どころで未確認)'),
 ('島根スサノオマジック','日本','Bリーグ','バンダイナムコエンターテインメントが経営権を取得(発表時期は未確認。fundbookの記事)'),
 ('東北楽天ゴールデンイーグルス','日本','NPB','2026年6月にサイバーエージェントへの売却の最終調整が噂になった(SNSのまとめ。正式発表なし)。2025年1月にはイーロン・マスク氏による買収報道もあるが、成立は未確認'),
]
R2 = R2 + [(n, c, '子会社・買収', b + '。' + t, 0, '', 0, 'N7', '') for n, c, b, t in _SP]

# 日本企業のTOB(2026年1〜5月分)。TOBレーダー『2026年 TOB一覧』。買付総額はページに記載がない。『不成立』『価格変更』『MBO』は一覧の表示
SRC2['N8'] = ('TOBレーダー『2026年 TOB一覧』', 'https://tobradar.com/tob/list2026/')
_p8 = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '_tob2026.txt')
if _os.path.exists(_p8):
    for _ln in open(_p8, encoding='utf-8'):
        _a = _ln.rstrip('\n').split('|')
        if len(_a) == 5:
            _note = ('、' + _a[4]) if _a[4] else ''
            R2.append((_a[2], '日本', '子会社・買収', 'TOB(公開買付け)。' + _a[1] + 'が1株' + _a[3] + 'で(公表' + _a[0] + _note + ')', 0, '', 0, 'N8', ''))

# 日本企業の大型M&A・スポーツクラブの経営権(2025〜2026年)
SRC2['N9'] = ('PR TIMES・M&A Online・kotora・fundbook等の日本のM&A集計', 'https://prtimes.jp/main/html/rd/p/000000311.000034249.html')
_JP3 = [
 ('豊田自動織機(非公開化)','日本','トヨタグループが買付代金最大4兆6,632億円、一連の買収総額5兆9,200億円(kotoraは約5.9兆円)で非公開化。日本企業同士の買収として最大(M&A Online・PR TIMES)'),
 ('ディアジオの東アフリカ事業','英国','アサヒグループが4,654億円で取得(PR TIMES)'),
 ('CSG Systems International','米国','NECが4,447億円で子会社化(PR TIMES・日経テレコン)'),
 ('トナミホールディングス','日本','日本郵便が約6,000億円で買収(fundbook)'),
 ('東武住販','日本','カチタスが1株2,000円のTOBで完全子会社化(2026年10月13日公表、買付期間10月14日〜12月3日)'),
 ('リソー教育グループ','日本','ヒューリックが1株295円のTOBで完全子会社化(2026年10月13日公表)'),
 ('太陽ホールディングス','日本','KJ005がTOBを予定、11月下旬の開始を目指すと公表(2026年10月9日)'),
 ('横浜エクセレンス(Bリーグ)','日本','リアルホールディングスグループが株式の追加取得で2025年7月1日付けで子会社化(同社の発表)'),
 ('姫路イーグレッツ(Wリーグ)','日本','広島ドラゴンフライズの運営会社が株式を取得しフランチャイズを移転、Bリーグのクラブが女子クラブの株式を取得する初のケース(2026年2月16日の記者会見)'),
 ('テゲバジャーロ宮崎(J2)','日本','いちごが2024シーズンからオーナー。2026年6月末でJリーグトップパートナー契約を終了し、同クラブに経営資源を集中(いちごの2026年4月14日の発表)'),
 ('FC町田ゼルビア','日本','サイバーエージェントが約80%を保有と紹介される(個人のまとめサイトによる。正確な持ち株比率はJリーグ・各社の開示で要確認)'),
 ('鹿島アントラーズ','日本','メルカリが約61.6%を保有と紹介される(同上。要確認)'),
 ('サンロッカーズ渋谷','日本','日立製作所が全株式をセガサミーホールディングスへ譲渡する契約(2022年。参考)'),
 ('千葉ジェッツ','日本','ミクシィが運営会社を子会社化(2019年。参考)'),
 ('広島ドラゴンフライズ','日本','NOVAホールディングスが運営会社を子会社化(2018年。参考)'),
]
R2 = R2 + [(n, c, '子会社・買収', t, 0, '', 0, 'N9', '') for n, c, t in _JP3]

# 桜十字グループ(熊本)の事業承継・M&A。公式サイト sakurajuji.com、熊本日日新聞、PR TIMES(M&Aキャピタルパートナーズ)、東洋経済、manda.bz
SRC2['N10'] = ('桜十字グループ公式サイト(お知らせ)', 'https://sakurajuji.com/')
SRC2['N11'] = ('熊本日日新聞『桜十字グループ、2医療機関運営の「御幸会」を承継』', 'https://www.kumanichi.com/articles/1817929')
SRC2['N12'] = ('PR TIMES『障害者福祉事業のアイムと桜十字グループのM&Aを支援』(2025-10-28)', 'https://prtimes.jp/main/html/rd/p/000000446.000051639.html')
SRC2['N13'] = ('東洋経済『九州最大の病院チェーン「桜十字」急成長の秘密』', 'https://toyokeizai.net/articles/-/855415')
SRC2['N14'] = ('manda.bz『桜十字によるSTORIESの株式譲渡M&A』(2026-06-13)', 'https://info.manda.bz/2026/06/13/sakurajuji-stories-disability-welfare-ma/')
_SK = [
 ('桜十字グループ','日本','日本の企業','熊本市の医療・介護・福祉グループ。病院、高齢者住宅、予防医療、フィットネス、在宅、障害福祉、不妊治療、歯科支援などを展開し、事業承継・M&A支援も事業の一つ。2005年に林ヶ原記念病院を買収して医療事業を開始し、21病院・約3,000床の九州最大規模の病院チェーンに。売上は2005年度約40億円から2024年度800億円超の見込み(東洋経済・公式サイト)。法人名は「株式会社桜十字」「医療法人桜十字グループ」と記事により異なる','N13N10'),
 ('林ヶ原記念病院','日本','子会社・買収','桜十字が2005年に買収した熊本の老人病院(2000年の保険金をめぐる報道で注目、事件性は後に否定)。一部を解体して桜十字病院として新たに開業(東洋経済)','N13'),
 ('医療法人社団大浦会(熊本市東区)','日本','子会社・買収','桜十字グループが事業承継(承継時期は未確認)。現在は医療法人熊本東桜十字として病院や老健などを運営(桜十字グループ公式・高齢者住宅新聞)','N10'),
 ('東京建物スタッフィング','日本','子会社・買収','東京建物が連結子会社の株式を桜十字に譲渡すると2023年8月29日に発表(東京建物の開示)','N10'),
 ('医療法人社団御幸会(熊本市)','日本','子会社・買収','2025年2月に東京地裁に自己破産を申請し、事業を続けながら譲渡先を探していた。2025年6月に桜十字グループが経営を引き継ぐ。運営する2医療機関のうち夢眠ホスピタルくまもと(旧熊本循環器科病院)が確認でき、病床と雇用を維持(熊本日日新聞)','N11'),
 ('アイム(神奈川県川崎市)','日本','子会社・買収','放課後等デイサービス、グループホーム、生活介護事業所、日中一時支援を運営する障害者福祉事業。M&Aキャピタルパートナーズが2025年10月28日にM&Aの成約を発表。桜十字側は児童福祉分野での関東進出が狙いとされる。前代表は佐藤典雅氏。金額は非公表(PR TIMES)','N12'),
 ('STORIES(埼玉県春日部市)','日本','子会社・買収','障がい者グループホームを10棟運営し全施設が黒字。桜十字が株式を取得して子会社化し、2026年6月13日の記事で成約が報じられた(取得日・金額は未公表)。元代表は木村航氏(manda.bz)','N14'),
 ('PTS(IT企業)','日本','子会社・買収','2026年9月4日にグループ会社となった。IT・DXの強化が目的(桜十字グループ公式)','N10'),
]
R2 = R2 + [(n, c, g, t, 0, '', 0, s, '') for n, c, g, t, s in [(a[0], a[1], a[2], a[3], a[4]) for a in _SK]]

# AIスタートアップの買収(2026年、続き)。Acquired『AI startup acquisitions in 2026』『Top AI startup acquisitions』と Crunchbase News。金額は集計サイトの値で、非公開が大半
SRC2['N15'] = ('Acquired『AI startup acquisitions in 2026』', 'https://www.startupsacquired.com/reports/ai-startup-acquisitions-2026')
SRC2['N16'] = ('Crunchbase News『AI startup acquisitions』', 'https://news.crunchbase.com/ma/ai-startup-acquisitions-legal-healthcare-openai/')
_p15 = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '_ai2026.txt')
if _os.path.exists(_p15):
    for _ln in open(_p15, encoding='utf-8'):
        _a = _ln.rstrip('\n').split('|')
        if len(_a) == 4:
            R2.append((_a[2], '', '子会社・買収', 'AI。' + _a[1] + 'が買収(' + _a[0] + '、' + _a[3] + ')', 0, '', 0, 'N15N16', ''))

R2 = R2 + [('EssilorLuxottica(Metaの出資先)', '', '子会社・買収', 'Ray-BanとOakleyを作るメガネ大手。Metaが約3%(約30億ユーロ=約35億ドル)を取得と報道(2025年7月。Bloomberg・Reuters)。2025年12月に同社の取締役が「少なくとも3%、最大約5%」と述べた。買収ではなく少数株主としての出資で、Ray-Ban MetaとOakley Metaのスマートグラスは共同開発(PYMNTS・Yahoo Finance)', 0, '', 0, 'M', '')]
