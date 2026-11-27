# Obsidian と Claude Code の連携

2026/11/27 に設定。

## しくみ
- このリポジトリのフォルダ(`Desktop\新しい\ai-soukanzu`)を、Obsidian の保管庫(Vault)「ai-soukanzu」として登録した
- Obsidian で開いているのはリポジトリのファイルそのもの。コピーではないので、Obsidian で書いたことは Claude Code にすぐ見え、Claude Code が書いたことも Obsidian にすぐ出る
- 熊本ヴォルターズの仕事用の保管庫(`Documents\Obsidian Vault`)とは別。Obsidian の左下の保管庫の切り替えで行き来する

## どこを見る・書くか
| フォルダ | 中身 | Obsidian での扱い |
|---|---|---|
| `notes/` | 自分のメモ | 自由に書いてよい |
| `posts/drafts/` | note の下書き | 読む・直してよい |
| `docs/` | 説明・企画メモ | 読む |
| `inbox/` | 毎朝の調査結果 | 読むだけ(自動で足されるため) |
| `site/` `src/` `scripts/` | サイト本体・道具 | Obsidian の一覧には出さない設定 |

## Obsidian 側の設定(PCごと。git には入れない)
- `.obsidian/app.json` で `node_modules/` `site/` `src/` `scripts/` `tools/` `newsletter/` を「除外するファイル」にしている(検索やグラフが重くならないように)
- 新しいノートの作成先は `notes/`

## 注意
- 毎朝の自動更新が `git pull` / `push` をするので、`notes/` のメモも Claude Code が commit すると GitHub に入る(リポジトリは非公開でも、他人に見せたくないことは書かない)
- 別のPCで使うときは、そのPCで Obsidian の「フォルダを保管庫として開く」からこのフォルダを選ぶ

## デイリーノート(2026/11/27追加)
- 毎朝9:13の取り込みのあとに、`notes/daily/日付.md` ができる。中身は、その朝「調査の新着」に足された項目の要点(人材の移籍・お金の流れ・資金調達・世界の企業・深堀り)と注意点。各行に出典のリンクが付く
- Claude が書くのは `<!-- AUTO:START -->` と `<!-- AUTO:END -->` の間だけ。上の「自分のメモ」に書いたことは消えない(同じ日にもう一度動くと、枠の中だけ書き直す)
- Obsidian のカレンダーの「今日のノート」ボタン(デイリーノート)を押すと、その日のノートが開く(このPCでは保存先を notes/daily、名前を YYYY-MM-DD に設定ずみ)
- 手で作り直すとき: `python3 scripts/daily_note.py 2026-11-27`
- PC で見るには、PC のフォルダに main の最新を取り込む(`git pull`)必要がある
