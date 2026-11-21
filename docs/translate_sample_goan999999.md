# 翻訳・解説ページの見本(1件目)

2026-11-21 に祐真さんのPCのChromeで読んだ(読むだけ)。見本として残す。

## 読んだ投稿
- 投稿A(元): Residual(@res1dualedge)2026-11-21 https://x.com/res1dualedge/status/2123821360807842114 (英語。表示4.9万回)
- 投稿B(依頼のURL): G哥(@goan999999)2026-11-21 https://x.com/goan999999/status/2123973337336668246 (中国語。投稿Aの紹介)
- 投稿Aが引用している記事: Hanako(@hanakoxbt)2026-08-23「Loops and Graphs: how to stop babysitting agents and only approve the last step (full course)」。X上では冒頭しか読めていない。動画・記事の本文は見ていない

## 原文(投稿A・英語)
This is f*cking insane. Anthropic engineer: "Prompting is basically over. 95% of our engineers already run self-improving loops. The next move is graphs." In just 10 minutes, she builds her entire Claude Code setup live, straight from an empty terminal. Empty Terminal → Agents → Loops → Graphs → Self-Improving System. Prompting was the old way. Engineering the system around the model is the new one. Save it and watch it today, then read the article below.

## 日本語訳
とんでもない。Anthropicのエンジニアいわく「プロンプトを書く時代はほぼ終わった。うちのエンジニアの95%はすでに、自分で改善していく『ループ』を動かしている。次は『グラフ』だ」。彼女は10分で、空のターミナルから自分のClaude Code環境をその場で作り上げる。空のターミナル → エージェント → ループ → グラフ → 自己改善するシステム。プロンプトは古いやり方で、モデルの周りの仕組みを作ることが新しいやり方。保存して今日見て、そのあと下の記事を読もう。

投稿B(中国語)も同じ内容の紹介で、「ChatGPT・Claude・Grokのどれか1つでも使ったことがあるなら見るべき」「プロンプトの書き方より、AIに自分で仕事させ、自分で確認させ、仕組みごと改善させる方向へ」と言っている。

## 解説
- **何の話か**: 「うまい指示文(プロンプト)を書く」より、「AIが自分で動き、自分でチェックし、直し続ける仕組み」を作るほうが大事、という主張。
- **ことばの意味**: ループ=AIが「実行→確認→直す」を繰り返す仕組み。グラフ=複数の作業や担当(エージェント)を線でつないだ流れ図のようなもの。エージェント=自分で作業を進めるAI。Claude Code=ターミナルで動くAnthropicのコーディング用AI。
- **何がすごいか(と言われている点)**: 人が1手ずつ見張らなくても、最後の確認だけで済む形にできる、という点。記事の題名もそう言っている(「見張りをやめて、最後の1手だけ承認する」)。
- **注意**: 「Anthropicのエンジニア」「95%」は、投稿者の言い分。動画の人物や数字は、公式の出典で確かめていない。元の記事は2026-08-23のもので、今日の新発表ではなく、今日バズって再投稿された。

## どう試すか(祐真さん向けの最小の手順)
1. 動画と、Hanakoさんの記事(上のX投稿から開ける)を読む
2. 今やっている小さな作業を1つ選ぶ(例: 毎朝のXの読み取り)
3. 「やる→確認する→直す」を1つのループにして、Claudeに回させる
4. 人が見るのは最後の結果だけにする(今回の相関図の仕事で、毎朝の定期タスクがこれに近い)

## 追記(2026-11-21)
- 引用元のHanakoさん(@hanakoxbt)は、同じ型の投稿を別の人物名で繰り返している(9/12は「Sam Altman」、11/6は「Grok」)。「◯◯が言った」の肩書きは、公式の出典で確かめるまで信じない
- 記事の本文はXの画面から読めなかった(検索で題名の冒頭だけ)
- 翻訳ページ: Claudeのページ(アーティファクト)として公開。元のHTMLは `docs/translate_page_source.html`
