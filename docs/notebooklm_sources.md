# 情報の取り元の一覧(調査元サイト・データ源)

- 更新日: {ASOF}
- このファイルの中身: 「AI企業の相関図」が情報を取ってきている元のサイト・データを、種類ごとに並べたもの。どのデータをどこから取ったか、毎朝・毎週の調査がどこを見ているか。
- 数字は、いま相関図のデータに入っているリンクの数(多い順。だいたいの目安)

## 目次

- 1. 会社の公式発表・一次情報
- 2. 法定の開示書類(いちばん確かなもの)
- 3. 百科事典・公開データベース
- 4. 会社・株価・資金調達のデータサイト
- 5. ニュース媒体(海外)
- 6. ニュース媒体(日本)
- 7. ニュースの集め方(まとめて拾う仕組み)
- 8. 本人の発信(X・YouTube・LinkedIn・ブログ)
- 9. VC・投資家の公式サイト
- 10. 各国の会社登記(企業検索サイト用)
- 11. 世界の日本人起業の一覧の出典
- 12. 定期の調査タスクと、それぞれが見ている所
- 13. つながらない・使っていない所

---

## 1. 会社の公式発表・一次情報

確かさの印では【公式】になります。

- 各社の公式ニュース: OpenAI(openai.com/news)、Anthropic(anthropic.com/news)、xAI(x.ai/news)、SpaceX(spacex.com/updates)、Meta(about.fb.com/news)、Microsoft(blogs.microsoft.com)、Google(blog.google・deepmind.google)、Nvidia(nvidia.com・nvidianews)、ソフトバンクグループ(group.softbank)、ソフトバンク(softbank.jp)、楽天(global.rakuten.com・corp.rakuten.co.jp)、LINEヤフー(lycorp.co.jp)、トヨタ(global.toyota)、NTT(group.ntt)、KDDI、ソニー、日立、三井物産、三菱UFJ、ASML、Arm、Oracle、Salesforce、Uber、TSMC・JASM(jasm.co.jp)、Sakana AI、Mistral、SSI、Thinking Machines、Cohere、Scale AI など
- 公式のリーダーシップのページ: Apple「Leadership」、Alphabet の取締役のページ など(米国の大手の役員)
- プレスリリースの配信サイト: PR TIMES(prtimes.jp、254件)、PR Newswire(44)、Business Wire(39)、GlobeNewswire、共同通信PRワイヤー(kyodonewsprwire.jp)
- 本人・創業者のサイト: Dario Amodei のエッセイ(darioamodei.com)、Sam Altman のブログ、Greg Brockman のブログ、Karpathy のサイト、Substack(aligned.substack.com など)、GitHub

## 2. 法定の開示書類(いちばん確かなもの)

確かさの印では【開示】になります。

- 米SEC EDGAR(sec.gov、160件): 上場申請(S-1・F-1)、公開価格が決まった書類(424B4)、大事な契約(8-K)、決算(10-K・10-Q)、ファンドの届出(Form D)。毎週火曜の「開示ウォッチ(SEC)」が SpaceX(xAI・X・Cursor)・Tesla・Nvidia・Microsoft・Oracle・CoreWeave・Alphabet・Amazon・Meta の新しい書類を見ています(data.sec.gov / efts.sec.gov)
- SEC の上場企業一覧(company_tickers_exchange.json): 全企業の名簿(bulk.json)の元
- EDINET(金融庁): 日本の有価証券報告書など。企業検索サイトの表(edinet)の元
- TDnet(東証の適時開示): PCの監視の道具(watch.py)が見ている
- 有価証券報告書の「役員の状況」: kabutore.biz が転記している公式の表から、日本の大手の役員を取得
- 日本取引所グループ(JPX)の東証上場銘柄一覧
- 各社の投資家向け資料(IR・決算資料)

## 3. 百科事典・公開データベース

出典の付いていない在籍・役職などの多くはここが元です(印なし)。

- 英語版 Wikipedia(en.wikipedia.org、約800件): 会社の経営陣・沿革、「List of mergers and acquisitions by …」(買収の一覧)、ユニコーン一覧、各VCの記事の投資先
- 日本語版 Wikipedia(ja.wikipedia.org、約300件): 日本の会社・人物
- Wikidata(wikidata.org、SPARQL・API): 創業者・CEO・会長・取締役・株主、子会社・親会社、生年・出身・学歴・職業、SNS(X・Instagram・YouTube)、AI分野の会社(AIスタートアップの小さな図2,960社)、人物名鑑(6,472人)、上場・買収の記録
- Wikimedia Commons: 顔写真(ライセンスを確かめたものだけ。Getty などは使わない)
- Y Combinator の公式ディレクトリ(公開の写し yc-oss のAPI、ycombinator.com): YC出身企業 6,376社
- 日経: 会社概要(代表者・資本金・従業員など)と「米国株 時価総額上位」ランキング(nikkei.com、221件)
- 国税庁 法人番号公表サイト: 日本の法人番号の全件データ(企業検索サイト用)

## 4. 会社・株価・資金調達のデータサイト

ニュースの見出しのリンク先として多く入っています。数字は【報道】扱いです。

- 株主・株価: Yahoo!ファイナンス(日本・米国・カナダ・英国など)、MarketScreener、moomoo、TIKR、Investing.com、TradingKey、Simply Wall St、MarketBeat、TradingView、株探(kabutan.jp)、四季報オンライン、GuruFocus、MarketWatch、Seeking Alpha、TipRanks、Benzinga
- 資金調達のデータベース: Dealroom(app.dealroom.co、80件)、Crunchbase News、Tracxn、BigGo Finance、Form D の集計(formds.com)

## 5. ニュース媒体(海外)

【報道】になります。大きな出来事は2つの媒体で確かめる決まりです。

- テック・AI: TechCrunch(107件)、The Next Web(64)、Unite.AI(93)、SiliconANGLE(22)、GeekWire、The Decoder、The Information、Axios、Engadget、Let's Data Science、AI Magazine、IT Pro
- 経済・一般: Bloomberg(31)、Reuters(25)、CNBC、Fortune(30)、Forbes、The Wall Street Journal、Financial Times、NBC News、CNN、NPR、Irish Times、Bloomberg Law・Bloomberg Tax、PYMNTS
- 資金調達・VC: Tech Funding News(39)、Tech.eu(54)、EU-Startups(36)、Sifted、Pulse 2.0、AlleyWatch、Citybiz、Private Equity International、Global Venturing、Alternatives Watch、HedgeCo
- インド・アジア: Inc42、Entrackr、Indian Startup Times、Indian Startup News、YourStory、Business Today、Economic Times、Moneycontrol、Analytics India Magazine、e27、Wowtale、DigitalToday(韓国)、머니투데이(mt.co.kr)、経済日報(udn.com、台湾)、The Star(マレーシア)、Startup Daily(豪州)、BetaKit(カナダ)
- 計算資源・電力: World Nuclear News、Broadband Breakfast、presenc.ai(OpenAIの計算資源の契約まとめ)

## 6. ニュース媒体(日本)

- Yahoo!ニュース(news.yahoo.co.jp、約1,000件。会社ごとのニュースの多くはここ経由)
- 日経・日経クロステック・日経バイオテク、THE BRIDGE(72)、STARTUP LOG(33)、PR TIMES、ITmedia、CNET Japan、Impress Watch、ビジネス+IT(sbbit.jp)、ダイヤモンド、東洋経済、Forbes JAPAN、朝日新聞、読売新聞、時事通信、TBS NEWS DIG、マイナビニュース、GIGAZINE、ライブドアニュース、ニコニコニュース、インフォシーク、エキサイト、dメニューニュース、財経新聞、ロジスティクス・トゥデイ、レスポンス、note(note.com)、熊本日日新聞
- M&A: FIRST CVC、フォースタートアップス、TOBレーダー、M&A Online、manda.bz

## 7. ニュースの集め方(まとめて拾う仕組み)

- Googleニュースの検索(RSS): 会社ごとのニュース(約1,400社・5,268件)。転送リンクは毎朝9:47の定期タスクで元の記事のURLに直しています
- Yahoo!ニュースの検索: 資金調達・買収・提携の見出し、会社ごと(約350社)
- WordPress の公開API: TechCrunch・SiliconANGLE・THE BRIDGE の資金調達の記事から、会社・金額・ラウンド・出資者を取り出す
- PR TIMES の発表: 日本のスタートアップの資金調達と、日本のVCのファンド組成・LP
- 見出し・リンク・日付・金額だけを保存し、記事の本文は保存していません

## 8. 本人の発信(X・YouTube・LinkedIn・ブログ)

確かさの印では【本人】になります。くわしいアカウントの一覧は「accounts_2026-11-19.md」(前の回答)にあります。

- X(x.com): 調査が見るアカウント {XN} 個(inbox/x_accounts.txt。毎朝7:07に10個ずつ追加)。ログインが要る検索・タイムラインは見られないので、記事に載った投稿のURLを X 公式の埋め込みサービス(publish.x.com/oembed)で確かめる(scripts/x_check.py)。プロフィールの自己紹介も見られる
- YouTube: Y Combinator、AI at Meta、Colin and Samir、Cheeky Pint(Stripe)を毎回。ほかに 20VC、TBPN、All-In、a16z、Sequoia、Lenny's Podcast。公式RSSで説明文、字幕は取れないことが多い(ロボット確認)
- LinkedIn の個人ページ・投稿、Threads、Substack、ポッドキャストの書き起こし(cheekypint.substack.com など)

## 9. VC・投資家の公式サイト

- 海外: Sequoia(sequoiacap.com/our-companies)、a16z、Accel、Greylock、General Catalyst、Index Ventures、Union Square Ventures、Khosla Ventures、Kleiner Perkins(kpcb.com)、Founders Fund、Thrive、Lightspeed など(各VCの「投資先」ページ)
- 日本: Coral Capital、インキュベイトファンド、Beyond Next Ventures、SMBCベンチャーキャピタル、NTTドコモ・ベンチャーズ、UTEC、Genesia Ventures、グロービス、JAFCO、WiL、ANRI
- ファンドの規模: 米SECの Form D(募集総額・販売額)

## 10. 各国の会社登記(企業検索サイト用)

相関図とは別の「企業検索サイト」(kigyo-asiapac など)の元データです。

- 日本: 国税庁 法人番号公表サイト(全件CSV)、EDINET の提出者
- 台湾: 経済部 商工行政資料開放平台(data.gcis.nat.gov.tw)
- オーストラリア: ABN Bulk Extract(data.gov.au、CC BY 3.0 AU)
- シンガポール: ACRA Information on Corporate Entities(data.gov.sg)。毎月20日に更新
- ニュージーランド: NZBN Bulk data(nzbn.govt.nz)※準備中
- インド: IndiaAI AIKosh の会社マスター(候補)
- 英国: Companies House「BasicCompanyData」/ フランス: INSEE「Sirene」/ ノルウェー: Brønnøysund / エストニア: e-Business Register / フィンランド: PRH

## 11. 世界の日本人起業の一覧の出典

JETRO、日本総研、Failory(インド・シンガポールのユニコーン一覧)、Next Unicorn Ventures(東南アジア)、Techpoint Africa、Businessday、StartupMapHub、wakka-inc、AERA、THE BRIDGE、36Kr、Acquired(startupsacquired.com)、Crunchbase News など(くわしくは「32_日本のスタートアップと世界の日本人起業.md」の「出典記号」)

## 12. 定期の調査タスクと、それぞれが見ている所(日本時間)

| いつ | タスク | 主に見ている所 |
|---|---|---|
| 毎朝6:43 | 相関図の毎日更新 | ニュース検索 → 本体の「最近の変化」(UPDATES) |
| 毎朝7:07 | Xアカウントを10個追加 | WebSearch と X のプロフィール |
| 毎朝7:26 | 引き抜き(人の移籍) | ニュース検索、X の一覧、YouTube、過去の月のさかのぼり |
| 月・木7:52 | お金の流れ | YouTube 4チャンネル、ニュース(本文で数字を確認)、記事に載った X の投稿 |
| 火7:48 | LP・VC資金 | X、VC・スタートアップの公式サイト、PR TIMES・Business Wire、TechCrunch・Bloomberg・The Information・Axios・日経・INITIAL、SEC Form D |
| 水7:44 | 世界企業 | 各国の会社登記の更新、次の国の候補 |
| 金7:41 | 深堀り | 会社の公式サイト(About・Team・ニュース)、報道、X |
| 毎朝9:13 | 調査の新着をサイトに追加 | 上の調査の結果(inbox/) |
| 毎朝9:47 | ニュースのリンクを元記事に直す | news.google.com の転送先 |
| 毎朝9:57 | 人物を企業検索に足す | Wikidata・英語版 Wikipedia |
| 火10:19 | 開示ウォッチ(SEC) | sec.gov(EDGAR) |
| 火10:53 | 計算資源の1枚資料 | SEC の書類、各社の発表 |
| 日10:23 | 報道だけの数字を確かめ直す | 会社の公式発表・開示書類(SEC・EDINET・HKEX) |
| 月9:37 | 週のまとめ(ニュースレター) | 上の調査と最近の変化 |
| 毎月20日 | シンガポールの会社 | data.gov.sg(ACRA) |

## 13. つながらない・使っていない所

- クラウドからは開けない: x.ai(PCのブラウザで確認)、dealroom.co・startuphub.ai の一部、YouTube の字幕(ロボット確認)、X の検索とタイムライン
- 使わないと決めているもの: うわさ・出典のない話、Getty Images など権利表記のある写真、ログインが要る裏の方法
