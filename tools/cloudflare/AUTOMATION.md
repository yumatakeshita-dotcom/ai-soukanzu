# クラウドで毎日動く Cloudflare の作業(2026-11-18 から)

PCなしで回すための定期タスクと、その決まりごと。

| 時刻(日本) | 定期タスク | やること |
|---|---|---|
| 毎日 9:41 | 相関図サイトの公開(Cloudflare) | `kigyo-relmap` が main の `site/` と同じかを確かめ、違えば Worker を置き直す(`tools/cloudflare/relmap/publish.sh`) |
| 毎日 9:57 | 人物を企業検索に足す(Cloudflare) | `inbox/moves/` の新しい移籍を、D1 `houjin` の `person` `person_role` `person_feed` に足す(`tools/cloudflare/d1_add.py`) |

## 決まりごと
- D1 には足すだけ。`d1_add.py` しか使わない(SELECT / PRAGMA / INSERT OR IGNORE だけ。行数が減ったら止まる)
- `wrangler d1 execute` で書き込み、`INSERT OR REPLACE`、PCの `sync_people.py` などの入れ替え型の道具は使わない
- **`kigyo-asiapac` `kigyo-europe` `kigyo-hito-tsunagari` は公開しない。** 公開は手元にないファイルを消すため。
  特に `kigyo-asiapac` はシンガポール(D1 `kigyo-sg`)を後から足してあり、PCの元ファイルから公開すると消える
  (足すときは `tools/kigyo-asiapac/add_sg_patch.py` を先に当てる)
- 鍵はクラウド環境「Default (MbTmFM)」の Network secret(api.cloudflare.com の Authorization)。
  wrangler には `CLOUDFLARE_API_TOKEN=placeholder` を渡せば、本物の鍵が付く。
  鍵を入れ直したあとは、新しく始まったセッションでだけ効く

## kigyo-relmap の作り(2026-11-18 変更)
- `tools/cloudflare/relmap/worker.mjs` が、GitHub(公開リポジトリ)の main の `site/` をそのまま配る。main が更新されると数分で公開側にも出る
- 以前の「ファイルを Cloudflare に上げる」形(wrangler deploy)は、クラウドの鍵の付け方だとファイル上げの許可証が上書きされて 401 になるので使わない
- Worker を置き直すのは `python3 tools/cloudflare/relmap/deploy_worker.py`(Workers スクリプトの API だけを使う)

## 人物の足し方(houjin)
- `person`: `q`(Wikidata の数字ID。Q を付けない文字列), `en`, `ja`, `intro`(英語版 Wikipedia の冒頭), `w`(言語 en/ja), `t`(Wikipedia の題名)
- `person_role`: `q`, `company`, `role`(日本語)。主キーがないので、同じ行があれば足さない
- `person_feed`: `q`, `ts`(YYYY-MM-DD), `src`(媒体名), `title`, `url`, `kind`(`move`)
- 処理済みの日付ファイルは `inbox/moves/d1_done.txt` に1行ずつ足す(消さない)

## PC から移した道具
`pc/` 以下。表の形と各サイトの作りは `pc/D1_SCHEMA.md`。
