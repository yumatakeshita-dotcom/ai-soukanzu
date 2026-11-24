# 投稿の下書き(XとnoteはAI企業の相関図のデータから)

- `posts/drafts/日付.md` … その日の下書き。**投稿はしません**(祐真さん本人が出典を開いて確かめてから投稿)
- ジャンルの割り当ては `docs/post_calendar_2026-12.md`、道具は `scripts/post_draft.py`
  - `python3 scripts/post_draft.py genre 日付` その日のジャンル
  - `python3 scripts/post_draft.py pick 日付` 14日以内の候補(品質チェックで保留のものは除く)
  - `python3 scripts/post_draft.py check posts/drafts/日付.md` Xの文字数(280以内)・出典URL・確かさの印を確認
- Xの数え方: 全角1字=2、半角1字=1、URLは23。無料アカウントは280まで(全角で約120字+URL1本)。長く書くときはPremium向けの長文版を下書きに併記
- 毎朝の定期タスク「投稿の下書き 毎日」が、翌日分の下書きを作って main に足します(足すだけ。すでにある日付は上書きしない)

## 深掘りの下書き(2026/11/24から)
- note記事は `posts/research/<日付>_<テーマ>/` で段階式に作る(手順 `docs/deep_research.md`、道具 `scripts/deep_post.py`)。本文は note.md、X用は `posts/drafts/日付.md`(同じ日の下書きがあれば `日付_deep.md`)
- 見本: 12/1 xAI創業メンバー11人の回(`posts/research/2026-12-01_xai-founders/`)
