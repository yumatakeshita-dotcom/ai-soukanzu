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
