# 2026-12-01(火)この人の経歴 下書き: ローレン・タン(Lauren Tan)

状態: **下書き(投稿はしていません)**。方針を「ニュースの要約」から「相関図の線をたどって初めて分かること」に改めて作り直しました(2026/11/24)。投稿前に出典ページを自分の目で開いて確かめること。
確かさ: 本人(X・GitHubのプロフィール。2026/11/24に実際に読んで確認)+ 公式(React公式ブログの著者欄)+ 開示(SECの8-K)。画像・顔写真は使いません。
※ カレンダー上の12/1は「役員人事」ですが、この日は経歴の回に差し替えました(役員人事のNVIDIA案は下の「予備」に残してあります)。

## X(本投稿・全角約100字+URL1本)
<!--X1-->
【この人】ローレン・タン氏の渡り歩き。Netflix→Meta(React Compilerの中心チーム)→Cursor→いまはSpaceXSI(旧xAI)でGrok Bot。(本人のプロフィールで確認)
https://x.com/poteto
<!--/X-->

## X(返信・2つ目)
<!--X2-->
【線をたどると】Cursorは8月にSpaceXの子会社になり、xAIも同じSpaceXの傘下。会社を替えたのか、親会社の中で移ったのかは公表されていません。(SEC提出書類で確認)
https://www.sec.gov/Archives/edgar/data/1181412/000162828026056945/spcx-20260814.htm
<!--/X-->

## X(Premium向けの長文版・任意)
【この人】ローレン・タン氏(ネット上の名前は「poteto」)の経歴を、相関図の線でたどると。
・Netflix → Meta: Reactの中心チームで、Reactのプログラムを自動で速くする「React Compiler」を作る。2025年10月の「React Compiler 1.0」発表の著者の一人(ほかにJoe Savona氏、Mofei Zhang氏)
・2026年春にCursorへ
・2026年8月にCursorがSpaceXの子会社に(SECの8-Kで買収の完了を確認)。同じSpaceX傘下のxAI(SpaceXSI)で、いまはGrok Botを作っている(本人のプロフィール)
会社を替えたのか、親会社の中で移ったのかは公表されていないので、書きません。(確かさ:本人・公式・開示)

## note(600〜1200字の骨子)
見出し: 「Reactを速くした人は、なぜいまGrokを作っているのか ― ローレン・タン氏の線をたどる」
1. 書き出し(2〜3行): 本人のX・GitHubのプロフィールに並ぶ4社(Netflix・Meta・Cursor・SpaceXSI)。会社の名前だけ見ると別々の業界に見えるが、相関図で線をひくと1本につながる
2. 年表(年・会社・役割・出典。**確かめられた年だけ書く**)
   - Netflix: 本人のプロフィールに「prev netflix」とあるだけ。役職・年は確かめられていないので書かない
   - Meta: Reactの「React Compiler」の中心チーム(GitHubのプロフィールに「react compiler core team」)
   - 2025年10月: React公式ブログ「React Compiler v1.0」の著者の一人(公式)
   - 2026年春: Cursorへ(月は資料で3月・4月と食い違うため「春」とだけ書く)
   - 2026年6月16日・8月14日: SpaceXがCursorの合併契約・買収完了(SEC 8-K)
   - いま: SpaceXSI(旧xAI)でGrok Bot(本人のプロフィール。GitHubの所属は @xai-org)
3. 線のおもしろいところ(相関図で見えること)
   - 本人のGitHubには、所属する組織として「reactjs」「anysphere(Cursorの運営会社)」「xai-org」が並ぶ。1人の中で、React→Cursor→xAIの3つの世界がつながっている
   - 10月12日のxAI公式発表で、Grok・Grok Bot・Cursor・X Premiumがひとつの購読(The X Subscription)にまとまった。本人が「前にいた」Cursorと「いま作っている」Grok Botが、同じ商品の中に並ぶことになった(出典の公式発表は投稿前に開いて確かめる)
   - 相関図の使いかた: 「xAI(SpaceXSI)」の図でローレン・タンを開くと、Meta・Cursorへの線が見える
4. 分かっていないこと: なぜ移ったのか、会社を替えたのか社内で移ったのか(公表なし)。肩書き(資料により食い違い)。学歴(別人の情報が混ざる疑いがあり書かない)
5. 出典の一覧(下の表)
末尾の定型文は docs/post_calendar_2026-12.md の「noteの末尾の定型文」のとおり。

## 出典と確かさ
| 内容 | 確かさ | 出典 |
|---|---|---|
| いまSpaceXSIでGrok Bot。前はCursor・Meta・Netflix。React Compilerの中心チーム | 本人 | https://x.com/poteto (自己紹介。`python3 scripts/x_check.py @poteto` で2026/11/24に確認) |
| 所属 @xai-org・@react compiler core team。組織に reactjs・anysphere・xai-org | 本人 | https://github.com/poteto (2026/11/24に確認) |
| React Compiler 1.0(2025/10/7)の著者: Lauren Tan・Joe Savona・Mofei Zhang | 公式 | https://react.dev/blog/2025/10/07/react-compiler-1 (この環境からは開けず、公式の翻訳ページ de.react.dev の検索結果で著者と日付を確認。**投稿前に自分で開く**) |
| CursorがSpaceXの子会社に(2026/8/14完了) | 開示 | https://www.sec.gov/Archives/edgar/data/1181412/000162828026056945/spcx-20260814.htm (相関図の記録。投稿前に開く) |
| 購読がひとつに(2026/10/12) | 公式 | https://x.ai/news/x-subscription (相関図の記録。この環境から開けず未確認。投稿前に開く) |

## 気をつけること(使わなかった情報)
- 調査メモ(Gemini)の「Netflix 2016/7〜」「Meta 2020/3〜2022/8」「2026/3にCursor入社」「Principal Engineer」は**出典が確かめられていない**ので使っていない
- 学歴(モナシュ大学・LSE)は別人の情報が混ざった疑いがあるので使わない
- 私生活(住所・家族)は書かない。顔写真・SNSの画像は載せない
- 「なぜ移ったか」は書かない(公表されていない)

## 予備(役員人事の回に戻すとき)
- NVIDIA: ジェンスン・フアン氏が11/22にCEOへ復帰(SEC 8-K https://www.sec.gov/Archives/edgar/data/1045810/000104581026000090/nvda-20261122.htm 、辞任は https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvda-20261111.htm )。辞任・復帰の理由は開示されていない。ニュースをなぞるだけにならないよう、使うなら「取締役会議長ハーヴェイ・ジョーンズ氏が初就任」などの人の線を足す

## 材料の元
- 相関図の人物カード(xAI・Meta・Cursorの図の「ローレン・タン」)、`inbox/gemini/2026-11-19_lauren-tan.md`(調査メモ。未確認の部分は使っていない)
