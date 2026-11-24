# 投稿の下書き(XとnoteはAI企業の相関図のデータから)

- `posts/drafts/日付.md` … その日の下書き。**投稿はしません**(祐真さん本人が出典を開いて確かめてから投稿)
- ジャンルの割り当ては `docs/post_calendar_2026-12.md`、道具は `scripts/post_draft.py`
  - `python3 scripts/post_draft.py genre 日付` その日のジャンル
  - `python3 scripts/post_draft.py pick 日付` 14日以内の候補(品質チェックで保留のものは除く)
  - `python3 scripts/post_draft.py check posts/drafts/日付.md` Xの文字数(280以内)・出典URL・確かさの印を確認
- Xの数え方: 全角1字=2、半角1字=1、URLは23。無料アカウントは280まで(全角で約120字+URL1本)。長く書くときはPremium向けの長文版を下書きに併記
- 毎朝の定期タスク「投稿の下書き 毎日」が、翌日分の下書きを作って main に足します(足すだけ。すでにある日付は上書きしない)
- 人物・線の材料探し(2026/11/24): `scripts/career_finder.py`(先に `node scripts/export_graph.js`)。`between A B`(2者の共通の線)・`conflicts`(訴訟の2者の共通の相手)・`coinvest`・`chains`・`bridges`・`hoppers`・`diaspora 会社`・`person 名前`・`pick 日付`。読むだけ。使い方はファイル先頭
