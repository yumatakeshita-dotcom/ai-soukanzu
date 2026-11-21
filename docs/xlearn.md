# 英語のAI新着 日本語解説(site/xlearn/)
- データ: `inbox/xlearn/items.json`(足すだけ・消さない)。1件=元の投稿または公式発表+日本語訳+解説+やり方+出典+確かさ。`kind:"新モデル"` はモデル発表。
- 道具: `python3 scripts/xlearn.py find`(Geminiで候補探し・1日の上限に注意)/`check`/`build`
- 毎朝の流れ(定期タスクにする場合の手順):
  1. `find` で候補(Gemini)。新モデルは各社の公式ニュースページで確かめる(anthropic.com/news はクラウドから読める。openai.com・x.ai・blog.google は未許可なので、許可を足すか報道で確かめる)
  2. Claude が元の投稿(`scripts/x_check.py URL`)・公式ページを開いて確かめ、items.json に足す。やり方は出典に書かれている範囲だけ。確かめられないことは「未確認」と書く
  3. `python3 scripts/xlearn.py build` → `check` → commit・push
- 共有リンクに出すときは `site/xlearn/index.html` を公開する(1枚で完結)
- 定期タスク: 毎朝9:19(日本時間)「英語のAI新着・新モデルの日本語解説 毎日」(trig_01LX2MuZq99jhSirGcDdcg6w)。PRがmainに入るまでは動かず停止する
- 許可がまだなくて読めない公式サイト(2026/11/21調べ。許可されたら sources.txt に足す): x.ai / docs.x.ai(xAI)、microsoft.ai、blogs.microsoft.com、www.apple.com / machinelearning.apple.com(Apple)、aws.amazon.com(Amazon Nova)、cohere.com、deepseek.com / api-docs.deepseek.com、moonshotai.github.io / kimi.com(Moonshot)、qwen.ai / qwenlm.github.io(Alibaba)、z.ai、stability.ai、databricks.com、openrouter.ai。許可が出るまでは、報道(techcrunch・venturebeat・siliconangle・theverge など許可済み)とXの本人投稿で確かめ、確かさは「報道」にする
- z.ai(Zhipu・GLM)の調べ(2026/11/21): ブログの記事は https://z.ai/blog/glm-5.3 の形だが、ページは中身をあとから読み込む作りで、クラウドからは空の枠(約600バイト)しか読めない。一覧ページ(z.ai/blog/)は404。更新履歴は docs.z.ai/release-notes.md にあるが、docs.z.ai は未許可で読めない。docs.z.ai が許可されたら sources.txt に `Z.ai | https://docs.z.ai/release-notes.md` を足す。それまでは報道(最新はGLM-5.3、2026/8、報道ベース)で補う
- 本体のメニュー「AIの新着解説」(2026/11/21追加): index.html の `openXlearn()` が `xlearn/index.html` を別タブで開く(ホームの入口カードもある)。共有リンクのアーティファクトでは `xlearn/index.html` を `files` に足して公開しないと開けない(毎朝の更新は index.html しか公開しないため、9:19のタスクが解説ページを更新したら、共有リンクにも公開する)
