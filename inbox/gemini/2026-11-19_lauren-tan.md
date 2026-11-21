# Lauren Tan(ローレン・タン)を Gemini API で調べた結果(2026/11/19)

- 使ったもの: Gemini API + Google検索(gemini-2.5-flash、無料枠)。PR 39 の試作の呼び出しを使い、人物向けの質問を1回送った
- Geminiの生の答え: `inbox/gemini/2026-11-19_lauren-tan_raw.json`(検索に使った言葉と、根拠にしたサイトの一覧つき)
- そのあと Claude が、本人のX・GitHub・ウェブ検索で確かめ直した
- 相関図にある記述: xAI・Meta・Cursorの図(ブランチ claude/project-thread-5thdqb。**まだ main に入っていない**)。出典は s_ltanx(本人のX)、o_ltanrc(React公式ブログ)、o_ltanconf(React Conf)、s_ltangb(本人の講演)、r_ltancur(daily.dev)
- このファイルは候補として人が見るためのもの。サイトには自動では出ない

## 本人かどうかの根拠
- ネット上の名前「poteto」が、X(https://x.com/poteto)と GitHub(https://github.com/poteto)で同じ
- X の自己紹介(2026/11/19、scripts/x_check.py で確認): 「grok @bot at @SpaceXSI. react compiler core team, prev cursor, meta, netflix」
- GitHub の自己紹介(2026/11/19確認): 「Software engineer on the @xai-org and @react compiler core teams」、所属 @xai-org、場所 SoCal、X へのリンクあり
- React公式ブログの React Compiler 1.0 の著者(相関図の o_ltanrc と同じ)
- 同姓同名の別人: Gemini は「見つからない」と答えた。ただし Gemini が書いた学歴(モナシュ大学・LSE)は、本人の資料と結びつく出典が見つからず、**別人の情報が混ざった可能性がある**(下の「確かめられなかったもの」)

## 既存の記述と同じだったもの(確かめ直しになった)
| 内容 | 確かさ | 出典 |
|---|---|---|
| 今は SpaceXSI(旧xAI)で Grok Bot を作っている | 本人 | 本人のX https://x.com/poteto 、本人のGitHub https://github.com/poteto |
| 前は Cursor・Meta・Netflix。React Compiler の中心チーム | 本人 | 同上 |
| React Compiler 1.0 の発表(2025/10)の著者の一人(ほかに Joe Savona、Mofei Zhang) | 公式 | https://react.dev/blog/2025/10/07/react-compiler-1 |
| Netflixでは画面まわりの開発チームのマネージャー | 本人(Geminiの答え。下の日付は未確認) | — |

## 新しい点(相関図にまだないもの)
> **注意(2026/11/20追記):** 下の表の「cursor.com」の記事(https://cursor.com/ja/lp-team/lauren)は、2026/11/20時点で開けません(Cursorの料金ページに転送される)。本文は確かめられていないので、この記事を出典にしないでください。本人だと言える根拠は、Xの自己紹介(https://x.com/poteto)とGitHub(https://github.com/poteto)です。

※ cursor.com・teamday.ai・lennysnewsletter.com はクラウドから開けなかったため、ウェブ検索の見出しと抜粋で確かめた。足す前にページを開いて確かめること。

| 内容 | 確かさ | 出典 | 足すなら |
|---|---|---|---|
| Cursor の公式ブログで、自分の作業手順をまとめた道具「pstack」を無料公開(Cursorの社内で1週間に1万回使われた、と本人) | 本人(Cursor公式サイト上の本人の記事) | https://cursor.com/ja/lp-team/lauren(2026/11/20に開けず。出典にしない) | Cursorの図のローレン・タンの説明に1文 |
| Grok Bot は 2026/8/11 にベータ公開。ローレン・タンはその中心チームの一人 | 報道 | https://www.teamday.ai/ai/people/lauren-tan 、 https://lennysnewsletter.com/p/how-we-built-grok-bot-in-a-month | xAIの図の Grok Bot の説明。公開日は公式発表で確かめてから |
| AIのエージェントで大量のプルリクエスト(作業の単位)を出している。数は資料で違う(Gemini「月約4,000件」、teamday.ai「月11,000件、取り消し0.5%」) | 報道(本人の講演の要約) | https://www.teamday.ai/ai/lauren-tan-spacexsi-grok-bot-11000-agent-prs-lint-rules | 数字は入れない方がよい(食い違い) |
| GitHub の所属が @xai-org | 本人 | https://github.com/poteto | s_ltanx と並ぶ本人の出典として DS に足せる |

## 食い違う点・Geminiだけが言っていること(未確認)
Gemini は次の細かい年月を出したが、根拠のリンクが「Googleの転送リンク」で、しかも検索の根拠一覧に無いリンクだった(おそらく LinkedIn の経歴。クラウドからは開けない)。**入れる前に LinkedIn などで確かめる必要がある。**
| Geminiの答え | 既存の記述との関係 |
|---|---|
| Netflix 2016/7〜2017/11 シニアエンジニア、2017/11〜2020/2 エンジニアリングマネージャー | 既存は年なし。新しい |
| Meta 2020/3〜2021/11 スタッフエンジニア(React Server Components の社内試作)、2021/11〜2022/8 Reactチームのマネージャー、2022/8〜2026/3 React Compiler | 既存は「2020年ごろ入社」。合っている。マネージャーだった時期は新しい |
| 2026/3 に Cursor に入社(Member of Technical Staff) | 既存は「3月か4月。資料により食い違いあり」。3月の方を支える材料が1つ増えたが未確認 |
| 2026/8 から SpaceXAI の Principal Engineer | 既存は「肩書きは資料によって違うので書かない」。**ウェブ検索では Principal Engineer の肩書きは見つからなかった** |

## 確かめられなかったもの(入れない)
- 学歴(モナシュ大学で会計・金融、LSE で上位5%): 本人の資料と結びつく出典が見つからない。同姓同名の別人の可能性がある。人物の学歴は相関図に必要ないので入れない
- 「pstack を 2026年5月に公開」: 公開日の出典が見つからない

## Gemini の出力の質(ひとこと)
- 良い点: 1回の質問で経歴を年月つきで15件まとめてきた。検索の言葉も「poteto」で本人に絞れていた。既存の記述と矛盾する大きな間違いは無かった
- 弱い点: 出典URLがすべて Google の転送リンクで、元のサイトが分からない。答えの中のリンクの一部は根拠一覧に無く、文字が少し違うもの(写し間違い)もあった。確かさの印も、LinkedIn の経歴に「開示」(法定の書類の意味)を付けるなど、こちらの決まりに合っていない。学歴は別人が混ざった疑いがある。**そのまま足すのは不可、下調べの道具としては使える**
