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
