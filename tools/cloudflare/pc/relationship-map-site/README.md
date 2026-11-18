# 企業と人のつながり(サイト試作)

日本の法人(国税庁 法人番号)と、EDINET提出者を、1社1ページで見せるサイトの試作。

- 起動: `node src/dev.mjs`(http://localhost:8787)。データベースは `C:/Users/yumat/.claude/data/houjin.sqlite`(環境変数 HOUJIN_DB で変更可)
- データの作り方(`docs/rooms/relationship-map-src/`): `fetch_houjin.py` で国税庁の全件CSVを取得 → `rebuild_houjin_all.py`(法人DB → EDINETコード → 検索用の索引)
- 本体: `src/app.mjs`(Hono。db の all/get を渡せば、Node のSQLiteでも Cloudflare D1 でも動く)
- 本番(Cloudflare Workers + D1)にするには: Worker用の入口(`src/worker.mjs`)で D1 を db に包んで渡す。D1 へのデータの取り込みは別作業
- 出典表示(国税庁)は全ページのフッターにある。外すと利用条件に反するので、残すこと
