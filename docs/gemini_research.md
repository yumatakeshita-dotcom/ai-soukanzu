# Gemini API で新しいつながりを調べる(試作、2026/11/19)

NotebookLM に渡している資料(共有フォルダの `notebooklm/` と `notebooklm-code/`)を、Google の Gemini API に渡して、
相関図に**まだ無い**企業・人物・取引・移籍を、出典URLと確かさの印付きで探す試作です。

## しくみ
1. **調べる**: Gemini + Google検索で、テーマについて新しい事実を探す。「すでにある範囲」(`notebooklm-code/10_*.md`)を渡して、重ならないものだけ返させる
2. **照らす**: 資料を Gemini の「ファイル検索(File Search)」に入れておき、1. の候補がもう資料にあるかを確かめる
   (Gemini API はファイル検索とGoogle検索を同じ呼び出しで一緒に使えないので、2回に分けている)
3. 手元でも、既存の会社名・人物名(`11_*.md`、約1万1千件)と名前を照らし、備考に「既存の名前」と書く

結果は `inbox/gemini/日付.json` と `日付.md`(表: 会社名/関係/相手/金額/日付/出典URL/確かさ/備考)に**足す**。
同じ日に2回やると `-2` が付いた別のファイルになる(消さない・上書きしない)。
このフォルダは `merge_inbox.py` の対象外なので、サイトには自動では出ない。人が見て、よいものだけを相関図に入れる。

## 使い方
```
python3 scripts/gemini_research.py status                  # 準備の状態
python3 scripts/gemini_research.py store                   # 資料をファイル検索に入れる(最初の1回。入れ済みは飛ばす)
python3 scripts/gemini_research.py research "日本のAIスタートアップの資金調達 2026年11月"
python3 scripts/gemini_research.py research "テーマ" --dry-run   # 送らずに、送る内容だけ確かめる
```
Claude Code からは MCP サーバー `ai-soukanzu-gemini`(`scripts/gemini_mcp.py`、`.mcp.json` に登録)の
`gemini_status` / `gemini_store` / `gemini_research` で同じことができる。

- キー: 環境変数 `GEMINI_API_KEY`(コードには書かない)。無いときは自動でドライランになる
- モデル: 環境変数 `GEMINI_MODEL`。無ければ `gemini-2.5-flash`。枠切れ(429)のときは gemini-flash-latest → gemini-3.5-flash → gemini-2.5-pro の順に試す(2026/11/19: 無料枠ではGoogle検索つきが gemini-2.5-flash しか通らなかったため)
- 出典URLは Gemini が書いたもの。相関図に入れる前に元ページを開いて確かめる(初回の試しでは日付の誤りが1件あった。`inbox/gemini/2026-11-19_review.md`)
- ファイル検索の入れ先の名前は `inbox/gemini/store.json` に記録する(キーは入っていない)
- 資料の場所を変えるときは `GEMINI_DOCS_DIR`(既定は `/mnt/project-files`)

## 出典URLの確かめ(2026/11/20追加)
`research` の最後に、各行の出典URLを実際に開いて確かめる(`--no-verify` で省く)。昨日の結果は `python3 scripts/gemini_research.py verify inbox/gemini/日付.json` で確かめ直せる(`日付_urlcheck.md` を足す。あれば上書きしない)。
- 開けて、会社名・相手の名前が本文に載っていた → 「URL確認:開けて名前も載っていた」
- 開けたが名前が無い → 「名前が見つからない」(作り話か別の記事の疑い。使わない)
- 404 など → 「エラー」
- クラウドから開けない(許可されていないサイト) → 「URL未確認」。**確かめた扱いにはしない**。許可を足せば確かめられる
- Gemini が検索で実際に見たサイトの一覧に、そのドメインが入っているかも「検索で見たサイト」として付ける

初回の結果(2026/11/20に確かめ直し): 10件中8件が404、1件が403、1件が別の記事。Geminiが書くURLはほとんど実在しない。**URLを確かめて「開けて名前も載っていた」ものだけ使う**。

## 無料枠と、枠切れのときのやり直し(2026/11/20追加)
- **このAPIキーは無料枠です**(2026/11/20に確かめた。上限のエラーに「Free Tier」と出る)。Geminiアプリの有料プラン(Gemini Pro)とは別の契約で、APIの枠には効きません
- 無料枠の上限(2026/11/20時点で、Google検索つきの gemini-2.5-flash は1日20回)に達すると 429 が返る。そのときは、調べたいテーマを `inbox/gemini/queue.jsonl` に足して(消さない)、あとでやり直す
- やり直し: `python3 scripts/gemini_research.py retry`(古い順に最大3件。まだ枠切れなら残りは次の日)。やり直したら queue.jsonl に「done」の行を足す
- Google検索の転送リンク(vertexaisearch…)は、たどって実際の記事のURLに直して保存する(もとのリンクは `転送リンク` に残す)

### 有料に切り替える手順(請求先の設定)
1. https://aistudio.google.com/apikey を開く(キーを作ったのと同じGoogleアカウントで)
2. 使っているキーの横の「無料枠(Free tier)」の表示、または「課金を設定(Set up billing)」を押す
3. Google Cloud の請求先アカウントを作って(クレジットカード)、そのプロジェクトにひも付ける
4. しばらくすると、同じキーのまま有料枠(Tier 1)になる。キーの入れ直しは不要
5. 料金は使った分だけ。事前に Google Cloud の「予算とアラート」で上限額(例: 月 1,000円)を決めておくと安心。料金表は https://ai.google.dev/gemini-api/docs/pricing(Google検索つきの料金も別にあるので、切り替え前に見る)

## キーの取り方と入れ方
1. https://aistudio.google.com/apikey を開き、Google アカウントでログインして「APIキーを作成」を押す
2. 出てきたキーをコピーする(チャットには貼らない)
3. claude.ai のこのプロジェクトの「プロジェクト設定」→「クラウド環境」→ 使っている環境の歯車 → 環境変数に
   `GEMINI_API_KEY=コピーしたキー` を1行足して保存する
4. 新しく始めたセッションから使える

注意: 環境変数は、その環境を使うセッションのすべてのコマンドから読める。
ファイル検索に入れた資料の保存は無料、入れるとき(文字をベクトルにする処理)と検索の結果を読ませるときに料金がかかる(Google の料金表で確かめる)。

## 毎朝の自動の調査と確かめ(2026/11/19追加)
毎朝8:23(日本時間)の定期タスク「Gemini調査(確かめつき) 毎日」が、次を行う。

1. `python3 scripts/gemini_research.py daily` … 曜日ごとのテーマ(`DAILY_THEMES`)で Gemini に調べさせ、`inbox/gemini/日付.json` に足す。
   そのまま `scripts/gemini_verify.py` で確かめる
2. `scripts/gemini_verify.py` の確かめ方(1件ずつ)
   - **出典URLにつながるか**: ページを実際に開き、会社名・相手の名前が書いてあるかも見る。開けないサイトは「未確認」と書く
     - Gemini が書いたURLが無い・中身が違うときは、Gemini が検索で実際に見たページ(転送リンクを元のURLに直したもの)から、同じ名前が書いてあるページを探して置き換える
   - **重なり**: 同じ出典URL、または同じ会社と相手が近い日付で、すでに相関図(index.html・data/*.js)や他の調査(inbox/)にあるもの
   - **日付の食い違い**: Gemini の日付と、URLの中の日付・ページの公開日が7日以上ずれるもの。未来の日付
   - **確かさの印**: 出典の種類と合わない印を直す(例:「公式」なのに報道サイト → 「報道」。SECの書類なら「開示」)
3. 判定
   - **合格**(つながって中身も合い、重なり・日付の食い違いが無い)… `inbox/money/日付-gemini.json` か `inbox/moves/日付-gemini.json` に足す。
     毎朝9:13の「調査の新着」の定期タスクが、ほかの調査と同じようにサイトに足す
   - **保留**(開けず「未確認」)… 定期タスクが WebSearch で開ける別の出典(会社の発表・英語の報道)を探し、見つかれば `日付-recheck.json` にして確かめ直す
   - **除外** … 理由を `日付_verified.md` に残すだけ
4. 結果は `inbox/gemini/日付_verified.json / .md` に足す。確かめた元のファイルは `inbox/gemini/verified.txt` に記録(2回確かめない)

### わかったこと(2026/11/19〜20)
- 日本のニュースサイトがクラウドから開けるようになった(2026/11/19、PR TIMES・日経・ITmedia・マイナビ・Impress・EE Times Japan・JETRO・創業手帳・財経新聞など15か所を許可)
- 開いてみると、初回の試し(10件)で **Gemini が書いた出典URLの7件はページが無かった**(404)。1件はページはあるが別の記事。
  Gemini が書くURLは作り話のことが多いので、確かめ無しには使えない
- Gemini の検索の転送リンク(vertexaisearch…)は、数時間で使えなくなる。調べた直後に元のURLにして `grounding_resolved` に保存している
- 無料枠は混雑(503)が多い。20秒・60秒・120秒待ってやり直す

## チャットに出た案は先にGeminiへ(2026/11/20から)
プロジェクトのチャットに書かれたテーマ・案・質問は、まず Claude ではなく Gemini で広げて調べる(`python3 scripts/gemini_research.py research "テーマ"`)。そのあと `python3 scripts/gemini_verify.py inbox/gemini/日付-N.json` で出典を開いて確かめ、通ったものだけが `inbox/money/` か `inbox/moves/` に足される。Claude は「出典の確認と取り込み」だけを受け持つ(使う量を減らすため)。最初の1回(2026/11/20)は4テーマ中3テーマが動き、合格は1件だけだった(Geminiの出典URLの多くが開けない・重複のため)。無料枠が切れる(429)と別のモデルが404で止まるので、その日の残りは翌日に回す。
## 調べ方の履歴を見る(2026/11/20追加)
Gemini API で調べても、Geminiアプリ・NotebookLM の履歴には残らない。そこで毎回の調査で、Geminiが実際に打った検索の言葉・見たページ・根拠の対応(`process`)を `inbox/gemini/日付.json` に残し、`python3 scripts/gemini_history.py` で日付ごとの目次を作る(調査のたびに自動で作り直す)。
- 文章の目次: `inbox/gemini/README.md`(GitHubで読める)
- 見やすい版: `inbox/gemini/history.html`(共有リンクにも公開。毎朝の定期タスクが公開し直す)
- 試しに残した生の返答(`*_process_raw.json`)も同じ目次に出る。足すだけで、元の記録は書き換えない
- 2026/11/20より前の調査は、検索の言葉が残っていない(「この回は記録なし」と出る)
