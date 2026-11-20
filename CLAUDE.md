# AI企業の相関図 プロジェクト

AI企業・半導体企業の人・出資・取引・移籍のつながりを見せるWebサイト。
本体の相関図(`site/index.html`)と、そのデータを使った実験ページ6つ(`site/lab/`)でできている。
2026年11月13日に claude.ai のアーティファクトからこのプロジェクトに移した。経緯は `docs/migration_memo.md`。

## 持ち主について
- 熊本ヴォルターズで事業開発をしている。エンジニアではない
- 返事は日本語。変更の説明は専門用語を使わずに短く
- 選択肢があるときは、おすすめを1つ示す
- 大きな変更の前は、やることを示してOKをもらう
- ファイルの削除・上書きの前は必ず確認する
- わからないことは推測せずに聞く

## 大事な前提
- **このリポジトリ(main)が正本。** 毎朝6:43(日本時間)にこのプロジェクトの定期タスク「AI企業の相関図 毎日更新(プロジェクト版)」がニュースを調べて `site/index.html` を更新し、main に push して、共有リンクのアーティファクトにも公開する
- そのため、**作業を始める前に必ず `git pull`** で最新を取り込む。終わったら commit して push する
- アーティファクトを直接直してはいけない(翌朝に上書きされる)。直すのはこのリポジトリ
- ビジネス化の検討、隙間のビジネス案、足りないものの一覧は `docs/business_notes.md` にある

## フォルダの中身
```
site/                 公開するもの(このフォルダをそのまま置けばサイトになる)
  index.html          本体の相関図(約5.4MB。会社ごとの相関図のデータと、毎日更新する部分が入っている)
  data/               本体のデータのうち、大きな一覧21個(AIスタートアップ、人物、ニュースなど)。本体が開くときに読み込む
  bulk.json ほか      本体が後から読み込むデータ(顔写真、人物、Googleニュースの見出し、pb/ 以下の追加データ)
  aw/                 AIスタートアップの小さな相関図のデータ(0〜73.json、必要なときに読み込む。2026/11/17追加)
  lab/                実験ページ6つ + index.html(一覧)
src/lab/              実験ページの元ファイル。ここを直して build する
scripts/              表示・確認・データ書き出しの道具
inbox/                調査タスク(引き抜き・お金の流れ・LP/VC・世界企業・深堀り)が毎朝保存する候補と、見るXアカウントの一覧(x_accounts.txt)
docs/                 移行メモなど
```

## よく使う操作
- 手元で見る: `npm run serve` → ブラウザで http://localhost:8000
- 変更のあとの確認(必ずやる): `npm run check`  ※初回だけ `npm install` と `npx playwright install chromium`
- 実験ページを作り直す: `npm run build-lab`(`src/lab/*.html` を直したあと)
- 本体のデータから実験ページ用データを作り直す:
  `node scripts/export_graph.js && node scripts/export_flows.js && python scripts/make_lab_data.py && npm run build-lab`

## 本体(site/index.html)の直し方
大きな一覧(`AIWD` `PERSONAL` `JPCO` `NEWS` `YCS` など21個)は 2026年11月18日に `site/data/` のファイルに分けた。これらを直すときは `site/data/` のファイルを直す。毎日更新する部分は今までどおり index.html にある。
**`site/data/` に新しいファイルを足したり中身を変えたりしたときは、共有リンクのアーティファクトにもそのファイルを公開する。**(毎日の自動更新は index.html しか公開しないため)
ファイルが大きいので、全体を読まずに目印で探して、その部分だけを直す。
- 毎日の更新記録: `/* UPDATES_START */` 〜 `/* UPDATES_END */` の間
  - `LAST_CHECK` = 最終確認日、`UPDATES` = 最近の変化(新しいものを先頭に足す)
- 計算資源の取引(金色の線): `const DEALS={` と、出典の `const DS={`
- 半導体の会社(TSMC・JASM・ASML・Samsung・SK hynix): `// ===== 半導体の相関図` の部分
- 一次情報のリンク: `const PRIMARY={`
- 使わない写真の一覧: `const PHBLOCK=`
- 週のまとめ(ニュースレター): `scripts/weekly.py` が inbox/ と UPDATES から作る。`newsletter/` と `site/weekly/index.html`。共有リンクは相関図と別(https://claude.ai/artifact/WnWyUzjmrSVHcxVgzKWPCM)。毎週月曜9:37の定期タスクが作って公開する。くわしくは `newsletter/README.md`
- 2社の共通のつながり(メニュー「共通のつながり」): `site/data/common.js`。データは持たず、開いたときに本体の相関図(DATA)からまとめる。2026/11/18追加
  - 営業先ごとの1枚資料: 同じ `site/data/common.js` の後半(`cmShowBrief`)。共通のつながりの結果画面の「営業資料(1枚)を作る」から開く。だれに会うか・紹介を頼める人・最近のニュース・最初のひとこと(案)・出典をまとめ、印刷(PDF保存)・テキストのコピー・.txt保存ができる。2026/11/18追加
- ニュースのリンク: Googleニュースの転送リンク(news.google.com/rss/articles/…)は元の記事のURLに直す。`python3 scripts/fix_gnews_links.py --auto` で、まだ直していないものを調べて置き換える(わからないものは残す)。毎朝9:47の定期タスク「ニュースのリンクを元記事に直す 毎日」が実行する。対応表は `scripts/gnews_map.json`
- 幹部の年表(メニュー「幹部の年表」、2026/11/19追加): `site/data/exectl.js`。OpenAIとAnthropicの経営陣の入社・退社・役割の変更を、上場の準備書類の前後で並べる。データ(`EXECTL`)と画面(`showExecTl`)が同じファイル。1件ごとに出典URLと確かさ(`cf`)を書く。新しい幹部の動きは `ev` に足す(足すだけ)。ほかの会社を足すときは `EXECTL` に同じ形で足す
  - 2026/11/20: NVIDIAを追加(CEO交代の3件だけ。公式発表で確かめたもの)。足し方は同じ(`EXECTL` に `nvidia:` を足す)
  - 2026/11/20: xAI(SpaceX傘下)とGoogle DeepMindを追加(`EXECTL` の `xai` `gdm`。この2社には上場の線がない)。`exectl_auto.py` の `COMPANIES` にも足した
  - 2026/11/19: Anthropicを追加(画面の「会社」で切り替え)。毎朝の移籍の調査(inbox/moves/)から、OpenAI・Anthropicの幹部の動きを `scripts/exectl_auto.py` が `site/data/finds.js` の3行目(`EXECTL_AUTO`)に自動で足す(画面では「自動で追加」の印)。`scripts/merge_inbox.py` の最後に動くので、毎朝9:13の「調査の新着」の定期タスクで更新される。手で書いた年表に同じ人の前後1か月の行があれば足さない。この3行目は手で直さない(直したいものは exectl.js に手で書く)
- 調査の新着(メニュー「調査の新着」): `site/data/finds.js`。毎朝9:13の定期タスクが `python3 scripts/merge_inbox.py` で inbox/ から足す(足すだけ・重複なし)。手で消さない
  - 同じファイルの2行目 `FINDLINKS` は、候補を相関図の人物・会社・線として出すためのもの(`scripts/finds_map.py` が inbox/ から作る)。どの会社の図に付けるかは index.html の `applyFinds` が名前で照らして決める。既存の人物・線は書き換えない
- 確かさの印(公式・開示・本人・報道・推定。2026/11/18追加): index.html の `// ===== 確かさの印` の部分。線や数字の出典から自動で決まり、画面の「確かさ」で絞り込める
  - 自動の決め方: 出典の名前やURLに「公式」「プレスリリース」などがあれば公式、SEC・EDINET・投資家向け資料なら開示、YouTube・Xなら本人、それ以外は報道
  - 自動で合わないときは、`DS` の出典に3番目の値を書く(例: `x:['媒体名(日付)','URL','o']` o=公式 f=開示 s=本人 r=報道 e=推定)。線や人物には `cf:'公式'` のように書ける。`UPDATES` の1件にも `cf:'報道'` を書ける
  - 毎週日曜10:23の定期タスク「報道だけの数字を確かめ直す 毎週」が、報道だけの数字を5件ずつ公式発表・開示書類で確かめ、`// 2026/11/18 確かめ直し:` の DS に出典を足す(足すだけ)。記録は `inbox/verify/`
    - **選び方(2026/11/18から): まず `npm run cf-rank` を実行し、`inbox/verify/rank.txt` の上位(報道だけの線が多い会社)から順に確かめる。** 前の週に確かめられなかったもの(`inbox/verify/` の記録の「確かめられなかったもの」)は飛ばす。公式の出典は `DS` に `'o'` か `'f'` を付けて足し、線の説明に「(日付、○○で確認)」と書き添える。一部しか確かめられないときは「○○は報道ベース」と書き添える
  - 週ごとの記録(2026/11/19追加): `npm run cf-rank` を実行するたびに、確かさの一覧と同じ数え方の割合(全体と会社ごと)を `site/data/cfhist.js` に1件足す(同じ日なら置き換え、前の記録は消さない)。確かさの一覧に「○/○の記録から +N pt」を出す(7日以上前の一番新しい記録と比べる)。**日曜の確かめ直しタスクは、確かめ終わったあとにもう一度 `npm run cf-rank` を実行し、`data/cfhist.js` も共有リンクのアーティファクトに公開する**
  - 共有リンクでの保存(.txt): index.html の `saveTextFile` が `claude.use('downloads')` を使う。共有リンクのアーティファクトは `downloads` の権限を宣言済み(公開のときに capabilities を省けば引き継がれる)
  - 確かな版(2026/11/18追加): 会社の図の概要にある「確かな版を作る」から開く。公式・開示の線だけを本文、報道などは「参考」に分けた資料を、開いている図から自動で作る(データは持たない)。印刷(PDF)・コピー・.txt保存ができる。コードは index.html の `// ===== 確かな版` の部分
  - 人の動き(採用・退任)は、本人の投稿(本人)で確かめたものも確かな版の本文と割合に数える(2026/11/18から)。調査タスクが足した人の線(finds.js)は書き換えず、index.html の `VERIFY_PPL` に [人の名前, 相手の会社名, 出典キー, ひとこと] を足すと、図を作るときに出典が付く
  - 確かさの一覧(メニュー「確かさの一覧」、2026/11/18追加): 全社の「公式・開示で確かめた割合」を並べる画面。index.html の `// ===== 確かさの一覧` の部分。データは持たず、開いたときに各社の図から確かな版と同じ数え方で数える
  - Xの確かめ方(2026/11/19から): クラウド環境から x.com と YouTube に直接つながる。`python3 scripts/x_check.py @名前` でプロフィールの自己紹介、`python3 scripts/x_check.py https://x.com/名前/status/番号` で投稿の本文と日付が見られる(X公式の埋め込みサービスを使う)。ログインが要る検索やタイムラインの一覧は見られないので、投稿のURLは報道などで探す。確かめたら `DS` に `'s'`(本人)で出典を足し、`VERIFY_PPL` に5番目の値で確かめた日を書く
  - 報道からXの投稿をたどる(2026/11/19から): `python3 scripts/x_from_news.py --kind money 記事URL` で、記事に載っているXの投稿を拾い、埋め込みサービスで投稿者・日付・本文を確かめる。`inbox/x_accounts.txt` の見るアカウントの投稿には `watched:true` が付く
  - YouTubeの字幕(2026/11/19から): `python3 scripts/yt_fetch.py 動画ID` が、断られたら60秒・3分・10分待ってやり直す。だめなら説明文はチャンネルのRSSから取り、動画を `inbox/money/yt_retry.txt` に足す(次の回に `--retry-queue` でやり直し、取れたら `yt_retry_done.txt` に足す。引き抜きの調査は `--kind moves` で `inbox/moves/` に記録)。クラウドからは字幕がロボット確認で断られやすい
  - techcrunch.com はクラウド環境から記事の本文を読める(2026/11/19に許可)
  - **引き抜き調査(inbox/moves/)で本人の投稿も集める(2026/11/19から)**: 人の動きを見つけたら、本人のX・LinkedIn(個人ページや投稿)・YouTubeでの発表を探し、見つかったら `src` の先頭に `["本人のX(2026/11/19)","https://x.com/名前/status/番号"]` のように入れる。`python3 scripts/x_check.py 投稿のURL` で本文と日付を確かめてから入れる(見つからなければ報道だけでよい。作らない・推測しない)。本人の投稿がある人の動きは、`confidence` が「報道」でも図では最初から「本人」の印になる(index.html の `selfPost`。会社のLinkedInページは含めない)。会社の公式発表があれば `confidence` は「公式」にする
  - 本人のXで確かめた移籍に「本人」の印を足す(2026/11/20から): `python3 scripts/moves_x_apply.py` が inbox/moves/ の候補(confidence が「本人の発言」「公式」)の出典にある本人のXの投稿・プロフィールを、X公式の埋め込みで実際に開いて確かめる(投稿者の名前が出典と同じ・表示名が英語名と合う・プロフィールなら自己紹介に移籍先がある)。`--apply` を付けると、確かめられたものだけ index.html の `/*XV_DS_START*/〜/*XV_DS_END*/`(出典)と `/*XV_PPL_START*/〜/*XV_PPL_END*/`(`VERIFY_PPL`)の間に足す(足すだけ。すでにある人は飛ばす)。確かめられなかったものは理由つきで表示するだけで、足さない。`selfPost` は出典が x.com なら確かめずに「本人」にするので、確かめられなかった表示が出たら、その出典が本人のものか見直す
  - 調査タスクの `confidence` は「公式」「開示」「報道」「本人の発言」「推定」のどれか。開示=法定の書類(SEC・EDINET・決算資料)、推定=自分や他社の推定・試算の数字

- Gemini API で新しいつながりを調べる試作(2026/11/19追加): `scripts/gemini_research.py` と MCP サーバー `scripts/gemini_mcp.py`(`.mcp.json`)。結果は `inbox/gemini/` に足すだけ(サイトには自動で出ない)。キーは環境変数 `GEMINI_API_KEY`。くわしくは `docs/gemini_research.md`
  - 毎朝8:23の定期タスク「Gemini調査(確かめつき) 毎日」が `python3 scripts/gemini_research.py daily` を動かし、`scripts/gemini_verify.py` で出典URL(実際に開く)・重なり・日付・確かさを確かめる(2026/11/19追加)。合格したものだけ `inbox/money/日付-gemini.json`・`inbox/moves/日付-gemini.json` に足し、9:13の「調査の新着」がサイトに出す。Geminiが書いたURLは作り話が多いので、確かめを通らないものは相関図に入れない
- 幹部の年表に Nvidia を追加(2026/11/19)。SECの臨時報告書(8-K)から取締役・経営陣の入れ替わり12件。`scripts/exectl_auto.py` も Nvidia を対象にした
- xAI(SpaceXSI)の「モデル・製品の年表」と「Colossusの貸し借り」(2026/11/18追加): index.html の `// ===== 製品とモデルの年表` と `// ===== Colossusの貸し借り` の部分(`PRODTL` `COLOSSUS`)。会社の図の概要に出る。公式発表・開示で確かめたものを足すだけ
- 開示ウォッチ(2026/11/18追加): `python3 scripts/sec_watch.py` が米国の開示書類(SEC EDGAR)から、SpaceX・Anthropic・Perplexity・Nvidia・Microsoftなどの新しい提出書類(未上場の会社は資金調達の届け出 Form D も)を `inbox/disclosures/日付.json` に足す。SpaceXの決算からはAI(SI)部門の売上なども拾う。SECの決まりで User-Agent に名前とメールが要る(環境変数 `SEC_UA` か、gitに入れない `inbox/disclosures/ua.txt`)。クラウドの環境で www.sec.gov・data.sec.gov・efts.sec.gov を許可済み
- AI計算資源の契約まとめ(1枚資料、2026/11/18作成・11/19第2版): `docs/compute_deals_2026-11.html`。共有リンク https://claude.ai/artifact/Cs3yFwHEieKF4AhvAn18bu 。「上場の条件」(Anthropicの上場。1株83ドルは2026/11/18の S-1MEF で開示を確認。424B4 が出たら株数・金額を確かめ直す)と「開示ウォッチの新着」(`<!-- WATCH_START -->`〜`<!-- WATCH_END -->`)がある。新着は `python3 scripts/compute_brief.py` が inbox/disclosures/ から足す(足すだけ)。毎週火曜10:53の定期タスク「計算資源の1枚資料を更新 毎週」が実行して公開し直す

## 守ること
- 事実を足すときは、公式発表か信頼できる報道で確かめ、出典のURLを必ず付ける。うわさは入れない
- 数字が報道ベースや契約の上限のときは、そう書く
- 顔写真は、利用の権利(ライセンス)を確かめられたものだけ使う。Getty Images など権利表記のある写真は使わない
- 既存のデータは消さない。直すときは「いつ、何を直したか」が説明文でわかるようにする
- 色は必ずCSSの変数(`--active` `--invest` `--deal` など)を使い、ライト・ダークの両方で読めるようにする
- スマホの幅(390px)で横にはみ出さないこと。`npm run check` が確かめる
