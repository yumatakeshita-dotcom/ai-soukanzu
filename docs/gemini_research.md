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

## 調べ方の履歴を見る(2026/11/20追加)
Gemini API で調べても、Geminiアプリ・NotebookLM の履歴には残らない。そこで毎回の調査で、Geminiが実際に打った検索の言葉・見たページ・根拠の対応(`process`)を `inbox/gemini/日付.json` に残し、`python3 scripts/gemini_history.py` で日付ごとの目次を作る(調査のたびに自動で作り直す)。
- 文章の目次: `inbox/gemini/README.md`(GitHubで読める)
- 見やすい版: `inbox/gemini/history.html`(共有リンクにも公開。毎朝の定期タスクが公開し直す)
- 試しに残した生の返答(`*_process_raw.json`)も同じ目次に出る。足すだけで、元の記録は書き換えない
- 2026/11/20より前の調査は、検索の言葉が残っていない(「この回は記録なし」と出る)
