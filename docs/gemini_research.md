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
