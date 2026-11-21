# 英語のAI新着 日本語解説(site/xlearn/)
- データ: `inbox/xlearn/items.json`(足すだけ・消さない)。1件=元の投稿または公式発表+日本語訳+解説+やり方+出典+確かさ。`kind:"新モデル"` はモデル発表。
- 道具: `python3 scripts/xlearn.py find`(Geminiで候補探し・1日の上限に注意)/`check`/`build`
- 毎朝の流れ(定期タスクにする場合の手順):
  1. `find` で候補(Gemini)。新モデルは各社の公式ニュースページで確かめる(anthropic.com/news はクラウドから読める。openai.com・x.ai・blog.google は未許可なので、許可を足すか報道で確かめる)
  2. Claude が元の投稿(`scripts/x_check.py URL`)・公式ページを開いて確かめ、items.json に足す。やり方は出典に書かれている範囲だけ。確かめられないことは「未確認」と書く
  3. `python3 scripts/xlearn.py build` → `check` → commit・push
- 共有リンクに出すときは `site/xlearn/index.html` を公開する(1枚で完結)
