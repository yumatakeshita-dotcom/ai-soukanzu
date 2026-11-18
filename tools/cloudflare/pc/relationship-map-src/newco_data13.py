from newco_data10 import st
from newco_data9 import P, O

N13 = '情報源は英語版Wikipedia(2026年11月確認)です。評価額・調達額は報道ベースで、調達のたびに変わります。'

# ---- ByteDance ----
st('st_bytedance', 'ByteDance', 2012, N13 + '2025〜2026年の評価額は、Wikipediaのページには載っていません(2024年11月で約3,000億ドル)。TikTok米国事業の再編(合弁会社)は、取得したページの範囲では確認できていません。', [
  P('zhang', 'チャン・イーミン(張一鳴)', 'Zhang Yiming', 2012, '共同創業者。2021年までCEO。議決権の過半数を持つと報じられています。', '共同創業者 / 元CEO', None, 1),
  P('liang', 'リャン・ルボ(梁汝波)', 'Liang Rubo', 2012, '共同創業者。2021年11月にCEOを引き継ぎ、現在もCEO。', 'CEO / 共同創業者', None, 1),
  P('chew', 'ショウ・ジー・チュー', 'Shou Zi Chew', 2021, 'TikTokのCEO(2021年〜)。元Xiaomi CFO。', 'TikTok CEO'),
  P('mayer', 'ケビン・メイヤー', 'Kevin Mayer', 2020, '2020年6月にTikTok CEO兼ByteDance COOに就任し、8月に辞任。', 'TikTok 元CEO', 2020),
  P('gao', 'ジュリー・ガオ', 'Julie Gao', 2021, '最高財務責任者(CFO)。就任年はWikipediaに記載なし。', 'CFO'),
  P('ma', 'ウェイイン・マー', 'Wei-Ying Ma', 2016, '2016年3月に設立したByteDance AI Labの責任者。', 'AI Lab責任者'),
  P('dantchik', 'アーサー・ダンチック', 'Arthur Dantchik', 2020, '取締役(Susquehanna International、2024年11月時点)。', '取締役'),
  P('ford', 'ウィリアム・フォード', 'William E. Ford', 2020, '取締役(General Atlantic、2024年11月時点)。', '取締役'),
  P('niel', 'グザビエ・ニール', 'Xavier Niel', 2020, '取締役(Iliad、2024年11月時点)。', '取締役'),
  P('shen', 'ニール・シェン(沈南鵬)', 'Neil Shen', 2020, '取締役(HongShan、2024年11月時点)。', '取締役'),
  O('susquehanna', 'Susquehanna International', 2015, '出資者(ジェフ・ヤス氏)。年・金額はWikipediaに記載なし。', '出資者', 'i'),
  O('sequoia', 'Sequoia Capital', 2014, '2014年に1億ドルの出資を主導(Wikipediaのチャン・イーミンの項)。', '出資者(2014年)', 'i'),
  O('softbank', 'SoftBank Group', 2015, '出資者(年・金額はWikipediaに記載なし)。', '出資者', 'i'),
  O('kkr', 'KKR', 2015, '出資者(年・金額はWikipediaに記載なし)。', '出資者', 'i'),
  O('ga', 'General Atlantic', 2015, '出資者・取締役を派遣。', '出資者', 'i'),
  O('g42', 'G42', 2023, '2023年に出資(金額は記載なし)。', '出資者(2023年)', 'i'),
  O('cniif', '中国インターネット投資基金', 2021, '2021年に、国有ファンドが北京ByteDance Technologyの1%を取得し、取締役を1人出す(『黄金株』)。', '国有出資者(2021年)', 'i'),
  O('tiktok', 'TikTok', 2017, '2017年9月に国際版を開始。2017年にmusical.lyを買収(Wikipediaの本社の項では約10億ドル、創業者の項では2018年に8億ドル)し、2018年に統合。', '主力サービス'),
  O('douyin', 'Douyin(抖音)', 2016, '中国版TikTok(2016年9月)。', '主力サービス'),
 ],
 [('zhang', 'liang', 'link', '共同創業'), ('liang', 'zhang', 'link', 'CEOを引き継ぐ', 2021), ('co', 'tiktok', 'owns'), ('co', 'douyin', 'owns'), ('chew', 'tiktok', 'link', 'CEO'), ('mayer', 'tiktok', 'link', 'CEO(〜2020年8月)')],
 '2012年3月に張一鳴(ジャン・イーミン)らが創業した、中国の巨大IT企業。ニュースアプリ「今日頭条」(2012年)、Douyin(2016年)、TikTok(2017年)、CapCut、Lark、AIアシスタントDoubaoなどを展開。')

# ---- Anduril ----
st('st_anduril', 'Anduril Industries', 2017, N13 + '2026年の調達(3月に40億ドル・評価額600億ドル、5月に50億ドル・評価額610億ドル)は、同じ調達かどうか確認できておらず、報道ベースです。', [
  P('luckey', 'パルマー・ラッキー', 'Palmer Luckey', 2017, '共同創業者。Oculus Rift(VRヘッドセット)の発明者。2017年3月にFacebookを離れた。', '共同創業者', None, 1),
  P('stephens', 'トレー・スティーブンス', 'Trae Stephens', 2017, '共同創業者で会長。元Palantir、Founders Fundのパートナー。', '共同創業者 / 会長', None, 1),
  P('grimm', 'マット・グリム', 'Matt Grimm', 2017, '共同創業者。2021年のLAタイムズでCOOと紹介された。', '共同創業者', None, 1),
  P('chen', 'ジョー・チェン', 'Joe Chen', 2017, '共同創業者。', '共同創業者', None, 1),
  P('schimpf', 'ブライアン・シンフ', 'Brian Schimpf', 2017, '共同創業者でCEO。元Palantir。', '共同創業者 / CEO', None, 1),
  O('singerman', 'ブライアン・シンガーマン(Founders Fund)', 2017, '2017年のシードラウンドを、Founders Fundのパートナーとして主導。', '出資者(2017年)', 'i'),
  O('gil', 'エラッド・ギル', 2021, '2021年のシリーズD(4.5億ドル、評価額46億ドル)を主導。', '出資者(2021年)', 'i'),
  O('ff', 'Founders Fund', 2017, '2017年のシード、2024年のシリーズF(15億ドル、評価額140億ドル)を共同で主導。2025年6月には10億ドルを出資(Wikipedia:ピーター・ティールの項)。', '出資者', 'i'),
  O('a16z', 'Andreessen Horowitz', 2019, '2019年の1.2億ドル、2020年の2億ドルなどに参加。2026年の調達も主導と報じられる。', '出資者', 'i'),
  O('gc', 'General Catalyst', 2019, '2019年・2021年の調達に参加。', '出資者', 'i'),
  O('thrive', 'Thrive Capital', 2026, '2026年の調達に参加と報じられる。', '出資者(2026年・報道)', 'i'),
  O('sands', 'Sands Capital', 2024, '2024年のシリーズFを共同で主導。', '出資者(2024年)', 'i'),
  O('capital1789', '1789 Capital', 2025, '2025年6月の25億ドルの調達に参加。', '出資者(2025年)', 'i'),
  O('army', '米陸軍(IVAS)', 2025, '2025年2月、MicrosoftからIVAS(兵士向けの拡張現実ゴーグル)の開発を引き継ぐ。陸軍は最大12.1万台を発注する計画(試験が条件)。', '顧客'),
  O('airforce', '米空軍(CCA)', 2024, '2024年1月、無人戦闘機(CCA)の5社の1つに選ばれる。Fury(YFQ-44A)は2025年10月31日に初飛行。', '顧客'),
  O('openai', 'OpenAI', 2025, '対ドローン防衛で協力(Wikipedia)。', '提携'),
  O('edge', 'Edge Group(UAE)', 2025, '2025年11月に合弁の生産提携を結ぶ。', '提携'),
 ],
 [('luckey', 'stephens', 'link', '共同創業'), ('luckey', 'schimpf', 'link', '共同創業'), ('stephens', 'ff', 'link', 'Founders Fundのパートナー'), ('co', 'army', 'link', '契約'), ('co', 'airforce', 'link', '契約'), ('co', 'openai', 'link', '協力'), ('co', 'edge', 'link', '提携')],
 '2017年6月にパルマー・ラッキーらが創業した、米国の防衛テック企業。AIの指揮統制ソフト「Lattice」、ドローン、自律型の機体などを開発。評価額は2021年に約46億ドル、2024年に約140億ドル、2026年に約600億ドルと報じられています。')

# ---- Telegram ----
st('st_telegram', 'Telegram', 2013, N13 + '2025〜2026年の評価額はWikipediaのページに載っていません。', [
  P('pdurov', 'パベル・ドゥーロフ', 'Pavel Durov', 2013, '共同創業者でCEO。ロシアのSNS「VKontakte」の創業者(2014年に追われる)。2024年8月にフランスで逮捕・起訴された。', '共同創業者 / CEO', None, 1),
  P('ndurov', 'ニコライ・ドゥーロフ', 'Nikolai Durov', 2013, '共同創業者。通信方式MTProtoを作り、TONのコードを書いた。', '共同創業者', None, 1),
  O('mubadala', 'Mubadala', 2021, '2021年3月の債券の一部(1.5億ドル)を、Abu Dhabi Catalyst Partnersとともに購入。', '出資者(2021年)', 'i'),
  O('kleiner', 'Kleiner Perkins', 2018, '2018年の約17億ドルの私募(TON関連)に参加。', '出資者(2018年)', 'i'),
  O('sequoia', 'Sequoia Capital', 2018, '2018年の私募に参加。', '出資者(2018年)', 'i'),
  O('benchmark', 'Benchmark', 2018, '2018年の私募に参加。', '出資者(2018年)', 'i'),
  O('xai', 'xAI', 2025, '2025年にドゥーロフ氏がAI機能の提携を発表したが、Wikipediaは「実現しなかった」と記載。', '提携(実現せず)'),
  O('sec', '米SEC', 2020, '2020年にTONのGram配布を停止させ、Telegramは1,850万ドルの罰金で和解。', '規制当局'),
 ],
 [('pdurov', 'ndurov', 'link', '共同創業'), ('co', 'xai', 'link', '提携の発表(実現せず)', 2025), ('co', 'sec', 'conflict', 'Gram配布を停止(2020)', 2020)],
 '2013年にドゥーロフ兄弟が立ち上げた、暗号化メッセージアプリ。月間利用者は2025年3月に10億人。本拠はドバイ、登記はブリティッシュ・ヴァージン諸島。2024年12月に黒字化したとCEOが述べています。')

# ---- Epic Games ----
st('st_epic', 'Epic Games', 1991, N13 + '2025〜2026年の評価額はページに載っていません(最新は2022年4月の約320億ドル)。', [
  P('sweeney', 'ティム・スウィーニー', 'Tim Sweeney', 1991, '創業者でCEO。支配株主(約41%と記載)。', '創業者 / CEO', None, 1),
  P('rein', 'マーク・レイン', 'Mark Rein', 1992, '副社長。1992年に事業パートナーとして参加(約4%を保有と記載)。', '副社長'),
  P('libreri', 'キム・リブレリ', 'Kim Libreri', 2018, '最高技術責任者(CTO)。', 'CTO'),
  P('sussman', 'アダム・サスマン', 'Adam Sussman', 2022, '社長(Wikipediaのインフォボックスの記載)。', '社長'),
  P('wen', 'チャーリー・ウェン', 'Charlie Wen', 2022, '最高クリエイティブ責任者。', 'CCO'),
  P('bleszinski', 'クリフ・ブレジンスキー', 'Cliff Bleszinski', 1992, 'デザイン責任者(Gears of Warなど)。2012年10月に退社。', '元デザイン責任者', 2012),
  P('capps', 'マイク・キャップス', 'Mike Capps', 2000, '社長。2012年12月に退任を発表。', '元社長', 2012),
  O('tencent', 'Tencent', 2012, '2012年6月に3.3億ドルで約40%を取得(議決権付き株の48.4%)。取締役の指名権を持つ。', '出資者(2012年)', 'i'),
  O('sony', 'Sony', 2020, '2020年に2.5億ドル、2021年に2億ドル、2022年に約10億ドルを出資。', '出資者(2020年〜)', 'i'),
  O('disney', 'Disney', 2024, '2024年2月、15億ドル(約9%)の出資で合意(当局の承認が条件)。', '出資者(2024年)', 'i'),
  O('kkr', 'KKR', 2018, '2018年10月の12.5億ドル(評価額約150億ドル)に参加。', '出資者(2018年)', 'i'),
  O('kirkbi', 'Kirkbi(レゴの親会社)', 2022, '2022年4月に約10億ドルを出資(約3%)。', '出資者(2022年)', 'i'),
  O('apple', 'Apple', 2020, '2020年にFortniteをApp Storeから外された訴訟(Epic v. Apple)で対立。2025年4月、Appleの対応は不十分との判断。', '訴訟の相手'),
  O('google', 'Google', 2020, '2023年12月の陪審でEpicが全面勝訴。2025年7月に控訴審が支持、2026年3月に和解(手数料の引き下げ、外部ストアを許可)。', '訴訟の相手'),
 ],
 [('sweeney', 'rein', 'link', '事業パートナー'), ('co', 'apple', 'conflict', 'App Store訴訟(2020〜)', 2020), ('co', 'google', 'conflict', 'Google Play訴訟(2020〜2026)', 2020), ('bleszinski', 'sweeney', 'from', '元の同僚')],
 '1991年にティム・スウィーニーが創業した、ゲーム・ゲームエンジンの会社。Fortnite(2017年)、Unreal Engine、Epic Games Storeを展開。2026年3月に1,000人超の人員削減を発表したとWikipediaに載っています。')

# ---- Kalshi ----
st('st_kalshi', 'Kalshi', 2018, N13 + '2026年の評価額(5月に約220億ドル)は、TCV主導の調達という記載で、報道ベースです。主要な出資者(Sequoiaなど)は、取得したページに載っていません。', [
  P('mansour', 'タレク・マンスール', 'Tarek Mansour', 2018, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('lopes', 'ルアナ・ロペス・ララ', 'Luana Lopes Lara', 2018, '共同創業者。', '共同創業者', None, 1),
  P('trumpjr', 'ドナルド・トランプ・ジュニア', 'Donald Trump Jr.', 2025, '2025年1月に戦略アドバイザーに。報酬に30万ドル超のKalshi株を含む。', '戦略アドバイザー'),
  O('tcv', 'TCV', 2026, '2026年5月の調達(評価額約220億ドル)を主導。', '出資者(2026年)', 'i'),
  O('cftc', '米CFTC(商品先物取引委員会)', 2020, '2020年11月に取引所の免許を付与。2023年に選挙の予測契約を認めず、Kalshiが提訴。', '規制当局'),
  O('robinhood', 'Robinhood', 2025, '2025年、Robinhoodの予測市場ハブの基盤をKalshiが担う。', '提携'),
  O('cnbc', 'CNBC', 2025, '2025年12月に独占提携。', '提携'),
  O('cnn', 'CNN', 2025, '2025年後半に公式の予測市場パートナーに。', '提携'),
  O('polymarket', 'Polymarket', 2025, '競合の予測市場。トランプ・ジュニア氏は同社の顧問にも就いた。', '競合'),
 ],
 [('mansour', 'lopes', 'link', '共同創業'), ('co', 'cftc', 'conflict', '選挙契約をめぐる訴訟(2023〜)', 2023), ('co', 'robinhood', 'link', '提携'), ('co', 'cnbc', 'link', '提携'), ('co', 'cnn', 'link', '提携'), ('co', 'polymarket', 'conflict', '競合'), ('trumpjr', 'polymarket', 'link', '顧問(2025)')],
 '2018年に創業された、米国で規制を受けた予測市場(スポーツや選挙などの結果に賭ける取引所)。2020年にCFTCの免許、2021年に公開。州との訴訟が続いており、2026年5月に評価額約220億ドルと報じられています。')

# ---- Helion Energy ----
st('st_helion', 'Helion Energy', 2013, N13 + '2021年の調達のうち、アルトマン氏の出資額(3.75億ドルとする資料もある)は、Wikipediaに内訳がなく未確認です。シリーズGは4.65億ドルと5億ドルの2つの記載があります。', [
  P('kirtley', 'デビッド・カートリー', 'David Kirtley', 2013, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('slough', 'ジョン・スロー', 'John Slough', 2013, '共同創業者。現在の役職は記載なし。', '共同創業者', None, 1),
  P('pihl', 'クリス・ピール', 'Chris Pihl', 2013, '共同創業者でCTO。', '共同創業者 / CTO', None, 1),
  P('votroubek', 'ジョージ・ボトルーベク', 'George Votroubek', 2013, '共同創業者。主任科学者。', '共同創業者', None, 1),
  P('altman', 'サム・アルトマン', 'Sam Altman', 2021, '会長(執行会長とする記載もあり)。2021年11月のシリーズE(5億ドル)を主に主導。', '会長 / 出資者'),
  O('yc', 'Y Combinator', 2014, '2014年8月に150万ドルをMithril Capitalと出資。', '出資者(2014年)', 'i'),
  O('mithril', 'Mithril Capital', 2014, '2014年に出資。', '出資者(2014年)', 'i'),
  O('softbank', 'SoftBank(ビジョン・ファンド2)', 2025, '2025年1月のシリーズF(4.25億ドル、評価額54億ドル)に参加。', '出資者(2025年)', 'i'),
  O('lightspeed', 'Lightspeed', 2025, '2025年1月のシリーズFに参加。', '出資者(2025年)', 'i'),
  O('thrive', 'Thrive Capital', 2026, '2026年6月のシリーズG(4.65億ドル、評価額155億ドル)を主導。', '出資者(2026年)', 'i'),
  O('nucor', 'Nucor', 2023, '2023年10月、同社の工場に50万キロワット級の発電所を置く合意(2030年稼働目標)。2025年にはシリーズFにも参加。', '提携・出資者'),
  O('msft', 'Microsoft', 2023, '2023年5月、2028年から5万キロワットを供給する合意(世界初の商業核融合の契約)。2025年7月にワシントン州Malagaで発電所Orionを計画。', '顧客'),
  O('commerce', '米商務省', 2026, '2026年10月、CHIPS法に基づき最大2.25億ドルの支援の意向書。', '政府支援'),
 ],
 [('kirtley', 'slough', 'link', '共同創業'), ('kirtley', 'pihl', 'link', '共同創業'), ('kirtley', 'votroubek', 'link', '共同創業'), ('altman', 'co', 'link', '会長'), ('co', 'msft', 'link', '電力の供給契約', 2023), ('co', 'nucor', 'link', '発電所の合意', 2023), ('co', 'commerce', 'link', '支援の意向書', 2026)],
 '2013年に創業された、核融合発電の会社。試作機Polarisは2024年に完成、2026年2月に測定可能なD-T核融合と1.5億度のプラズマを報告。評価額は2021年に約30億ドル、2025年に約54億ドル、2026年に約155億ドル。')

# ---- Tether ----
st('st_tether', 'Tether', 2014, N13 + '2026年の資金調達の評価額(3,500億ドル)は、取得したページに載っていません(Wikipedia上のユニコーン一覧に記載)。Devasini氏はCFOではなく会長と記載されています。', [
  P('ardoino', 'パオロ・アルドイノ', 'Paolo Ardoino', 2017, '2023年10月にCTOからCEOへ。AIや金への関与を進める。', 'CEO'),
  P('devasini', 'ジャンカルロ・デバシーニ', 'Giancarlo Devasini', 2014, '2025年3月に会長に就任。Bitfinexとの関係でも知られる(報道)。', '会長'),
  P('mcwilliams', 'サイモン・マクウィリアムズ', 'Simon McWilliams', 2025, '2025年3月にCFOに。', 'CFO'),
  P('pierce', 'ブロック・ピアス', 'Brock Pierce', 2014, '前身プロジェクト「Realcoin」(2014年)の共同創業者の1人。', '共同創業者', None, 1),
  P('collins', 'リーブ・コリンズ', 'Reeve Collins', 2014, 'Realcoinの共同創業者の1人。', '共同創業者', None, 1),
  P('sellars', 'クレイグ・セラーズ', 'Craig Sellars', 2014, 'Realcoinの共同創業者の1人。Mastercoin FoundationのCTOも務めた。', '共同創業者', None, 1),
  P('velde', 'ジャンルイ・ファン・デル・ベルデ', 'Jean-Louis van der Velde', 2018, '元CEO。2023年にアルドイノ氏が後任。', '元CEO', 2023),
  P('hines', 'ボー・ハインズ', 'Bo Hines', 2025, '2025年9月、米国向けステーブルコインUSATの発表とともに米国部門のCEOに。', '米国部門CEO'),
  O('cantor', 'Cantor Fitzgerald', 2024, '2024年1月にラトニックCEOが、Tetherの準備資産の保管を担うと発言(本人の発言に基づく)。2026年1月にUSATの準備資産の保管機関にも。', '保管機関'),
  O('ifinex', 'iFinex / Bitfinex', 2014, 'Tether LimitedとBitfinex取引所の親会社。', '関連会社'),
  O('juventus', 'Juventus', 2025, '2025年2月に少数株を取得。2025年12月の約12.9億ドルの買収提案は拒否された。', '投資先'),
  O('rumble', 'Rumble', 2024, '2024年12月に7.75億ドルを出資。', '投資先'),
  O('northern', 'Northern Data', 2023, '2023年9月、6.1億ドルの与信枠(株式取得と関連)。', '投資先'),
  O('adecoagro', 'Adecoagro', 2025, '2025年7月、南米の農業企業に出資。', '投資先'),
  O('nyag', 'ニューヨーク州司法長官', 2021, '2021年2月に1,850万ドルで和解(不正の認定なし)。2021年10月にはCFTCが4,160万ドルの罰金。', '規制当局'),
 ],
 [('pierce', 'collins', 'link', '共同創業'), ('pierce', 'sellars', 'link', '共同創業'), ('velde', 'ardoino', 'link', 'CEOを引き継ぐ', 2023), ('co', 'ifinex', 'owns'), ('co', 'cantor', 'link', '準備資産の保管'), ('co', 'juventus', 'owns'), ('co', 'rumble', 'owns'), ('co', 'northern', 'owns'), ('co', 'adecoagro', 'owns'), ('co', 'nyag', 'conflict', '和解(2021)', 2021)],
 '2014年に「Realcoin」として始まった、米ドルに連動するステーブルコイン(USDT)の発行会社。2026年6月末の流通量は約1,846億ドル、本社は2025年1月にエルサルバドルへ。Juventus、Rumble、金、ビットコイン採掘などにも投資。')
