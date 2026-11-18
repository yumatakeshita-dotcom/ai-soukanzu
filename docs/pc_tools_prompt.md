# PCの道具をリポジトリに移すための文

PCで Claude Code を開き、下の枠の中をそのまま貼り付けてください。1回だけで終わります。

```
C:\Users\yumat\.claude\docs\rooms\relationship-map-src にある、Cloudflare(D1とWorkers)用の道具を
GitHub の yumatakeshita-dotcom/ai-soukanzu に移してください。

1. ai-soukanzu をまだ手元に持っていなければ clone し、あれば git pull する
2. ブランチ claude/project-thread-p95kma を取り込み(git fetch origin claude/project-thread-p95kma && git checkout claude/project-thread-p95kma)、
   tools/cloudflare/pc/ に次をコピーする(フォルダの形はそのまま):
   push_missing_to_d1.py, restore100.py, restore_mine.sql, newco_data*.py, moves_extra.json,
   publish_static.py, wrangler.toml, そのほか D1 への取り込み・Workers への公開に使っている .py / .sql / .json / .toml / .js
   (kigyo-asiapac の台湾・オーストラリア取り込みの道具や Worker のコードもあれば全部)
3. 鍵は絶対に入れない。.env、.dev.vars、トークンやパスワードが書かれた行、~/.wrangler の中身は除く。
   コピーしたファイルに API トークン・パスワードらしき文字列があれば "REMOVED" に置き換え、どこを置き換えたかを報告する
4. 100MB を超えるデータファイル(CSV など)は入れず、ファイル名と大きさだけ tools/cloudflare/pc/LARGE_FILES.txt に書く
5. 次を調べて tools/cloudflare/pc/D1_SCHEMA.md に書く(読むだけ。D1 の中身は一切変えない):
   - wrangler d1 list の結果(DB名と用途)
   - 各DBの表の作り: wrangler d1 execute <DB名> --remote --command "SELECT name, sql FROM sqlite_master WHERE type='table'"
   - 各表の行数(SELECT COUNT(*))
   - 会社の表では、国コードの列と、国ごとの行数(TW・AU)
6. git add して「PCのCloudflare用の道具をリポジトリに移す」と commit し、git push origin claude/project-thread-p95kma
7. 終わったら、移したファイルの一覧を日本語で短く教えてください
```

移したあとは、クラウドの作業がこれを読んで、足すだけの形に直して定期タスクに組み込みます。
