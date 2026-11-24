# xAIの創業メンバー11人は、どこから来て、どこへ行ったのか ― 論文の共著と「次の会社」を線でたどる

状態: 下書き(投稿はしていません)。段階式の深掘り(docs/deep_research.md)で作った版。材料は事実カード(facts.jsonl、68枚)だけ。
確かさ: 論文の著者は論文目録で確認(公式)。本人のXは埋め込みと自己紹介で確認(本人)。それ以外は報道ベース。★は事実カードにない・未確認のところ。

---

2023年3月9日、イーロン・マスク氏はネバダ州でAIの会社xAIを登記しました。公表は7月12日です。マスク氏のほかに、研究者・エンジニアが11人。それから3年たたない2026年3月28日までに、この11人は全員いなくなったと報じられました。

「人が定着しない会社」で片付けると、それで終わりです。ここでは、11人が**xAIの前にどこで何を書いていたか(論文)**と、**xAIの後にどこへ行ったか(本人のXの自己紹介)**を、1本ずつ線でたどります。すると、ニュースの見出しからは見えない3つのことが出てきます。

## 1. 11人は、xAIの前から「論文の共著」でつながっていた

創業チームの顔ぶれは、Fortuneが2023年11月20日に載せた組織図と、論文の著者の欄から、次のように確かめられます。

| 人 | xAIの前 | 代表的な仕事(論文) |
|---|---|---|
| イーゴリ・バブシュキン(チーフエンジニア) | DeepMind → OpenAIの技術スタッフを約2年 | DeepMindの「AlphaCode」、OpenAIの「Grokking」 |
| クリスチャン・セゲディ | Googleに約13年 | 画像認識の「Inception(GoogLeNet)」、AIをだます入力「敵対的サンプル」 |
| トニー・ウー | Googleの研究者 | Googleの数学に強いモデル「Minerva」、自分の推論で自分を鍛える「STaR」 |
| ジミー・バー | トロント大学 | 学習の手法「Adam」(AIで最も引用される論文の1つ) |
| グレッグ・ヤン | Microsoftの研究所に5年(xAIでの肩書きは「数学者」) | 大きなモデルの設定を小さなモデルから移す「Tensor Programs V(μP)」 |
| トビー・ポーレン | Google DeepMindに6年あまり | 「人の好みから報酬を学ぶ」、DeepMindの言語モデル「Gopher」 |
| マヌエル・クロイス | GoogleとDeepMind | ★論文は今回の目録で見つからず |
| グオドン・ジャン | DeepMindの研究者、トロント大学で博士号 | Googleの「Gemini」の論文(著者942人の1人) |
| ジハン・ダイ | Googleに3年あまり | 長い文章を扱う「Transformer-XL」(筆頭著者)、「XLNet」 |
| カイル・コシック | OnScale、Lucena Research → 2021年にOpenAI | (xAIではインフラの責任者) |
| ロス・ノルディーン | Teslaに約4年、技術プログラムマネージャー | (運営の担当) |

この表を「だれとだれが同じ論文に名前を並べたか」で読み直すと、創業の前から線が引かれていたことが分かります。

- **ウー氏とセゲディ氏**: 2022年5月25日、Googleで「自動形式化」の論文を共著しています。数学の証明を、AIが1行ずつ検証できる形に直す研究です。ウー氏が筆頭、セゲディ氏が最後の著者でした。
- **ヤン氏とバブシュキン氏**: 2022年3月7日の「Tensor Programs V」は、Microsoftのヤン氏と、OpenAIのバブシュキン氏の共著です。会社の違う2人が、xAIの1年前に同じ論文に名前を並べています。共著者には、のちにOpenAIの主任研究者になるヤクブ・パホツキ氏もいます。
- **ポーレン氏とバブシュキン氏**: 2021年12月8日のDeepMindの「Gopher」(著者80人)に、2人ともいます。
- **トロント大学**: バー氏はトロント大学の所属で、2019年7月19日にはジェフリー・ヒントン氏と論文を共著しています。ジャン氏はトロント大学で博士号をとっています。

もう1本、気づきにくい線があります。11人の論文の共著者には、のちにほかの会社の中心になる人が並んでいます。セゲディ氏の「敵対的サンプル」の共著者にはイリヤ・サツケバー氏(のちのOpenAI共同創業者)、ポーレン氏の「人の好みから報酬を学ぶ」にはダリオ・アモデイ氏(のちのAnthropic創業者)とヤン・ライケ氏。xAIは「OpenAIやAnthropicの対抗馬」と言われますが、人の線をたどると、もとは同じ研究の輪の中にいたことになります。

## 2. 抜けていった順番と、それぞれが持っていた仕事

| 時期 | 人 | xAIでの仕事 | 報じられたこと |
|---|---|---|---|
| 2024年4月 | コシック氏 | 最初の11人の社員の1人。投資家向け資料に大きく載っていた | OpenAIに戻った。OpenAIが復帰を認めた |
| 2025年2月 | セゲディ氏 | 研究者 | 退社 |
| 2025年8月13日 | バブシュキン氏 | チーフエンジニア | 本人のXで「今日がxAIの最後の日」 |
| 2026年1月20日 | ヤン氏 | 数学者 | ライム病の診断を受け、本人のXで第一線を退くと発表。非公式の助言役に |
| 2026年2月9日 | ウー氏 | 推論のチームの責任者 | 本人のXで「次の章に進む時だ」 |
| 2026年2月10日 | バー氏 | 研究と安全の責任者。マスク氏に直接報告 | 「チームの友人として近くにいる」 |
| 2026年2月26日 | ポーレン氏 | 事務の仕事を何でもこなすAIの計画「Macrohard」の責任者に任命されたばかり | 3年で去ると本人のXで発表。計画は一時停止と報道 |
| 2026年3月初め | ジャン氏、ダイ氏 | ジャン氏は「Grok Code」と画像・動画の「Grok Imagine」の責任者 | SpaceXとTeslaによる監査と時期が重なった |
| 2026年3月28日までに | クロイス氏、ノルディーン氏 | クロイス氏は事前学習のチーム、ノルディーン氏は「マスク氏の右腕の実務家」(Business Insiderの表現) | 最後の2人。11人全員がいなくなった |

会社の側では、この間に大きなことが続きました。2026年1月6日にxAIはシリーズEで200億ドルを調達し、NvidiaとCiscoが戦略投資家になりました(xAIの公式発表)。2月2日には、SpaceXがxAIを株式交換で買収(xAIの評価は2,500億ドル)。3月13日にはマスク氏が「xAIは最初の作り方が正しくなかったので、土台から作り直している」と投稿しています。

退社の理由を、本人たちはほとんど書いていません。バブシュキン氏だけが、Future of Life Instituteの創設者マックス・テグマーク氏との夕食で安全なAIについて話したことが、決めたきっかけだったと書いています。ここでは、それ以外の理由は書きません。

## 3. 行き先: 1つの会社に、また2人が集まった

### バブシュキン氏とコシック氏は、River AIでまた一緒になった

バブシュキン氏は2025年8月、最初は「AIの安全に投資する会社(Babuschkin Ventures)」を作ると表明しました。そのあと、2026年4月20日にネバダ州でRiver AIを登記し(本社はパロアルト)、6月に発表、8月11日に11億ドルの調達を発表しています。本人のXの自己紹介は、いま「CEO & Co-Founder @river_ai_inc」です。

ここで、コシック氏の線が戻ってきます。コシック氏は2024年にxAIからOpenAIへ戻り、2026年にはジェフ・ベゾス氏の新会社Project Prometheusに入ったとFT(英フィナンシャル・タイムズ)が報じました。ところが、本人のXの自己紹介は2026年11月24日の時点で「@river_ai_inc / prev @OpenAI, @xAI」です。**xAIの最初の11人の社員のうち2人が、別々の道を通って、同じ会社にまた集まっている**ことになります。これは報道の見出しには出てこない線で、本人の自己紹介を開いて初めて分かります。

River AIが作るのは、公開されたAIモデルを、会社が自分のデータで学び直させるための仕組みです(LoRAと強化学習のAPI。100万トークン単位の課金)。個人のAIを手元に置く機械も計画しています。社員は約20人で、創業チームはxAIとTeslaの出身者と報じられています。

### セゲディ氏は「自動形式化」を続けている

セゲディ氏は2025年にMorph Labsの主任研究者になり、9月に自動形式化の会社「Math Inc」を始めると発表したと報じられています(Morph Labsの最高経営責任者ジェシー・マイケル・ハン氏との共同創業とされます。★本文は未確認)。

ここにも線があります。

- 「自動形式化」は、セゲディ氏が2022年にGoogleでウー氏と共著した論文のテーマそのものです
- ハン氏は、2022年2月3日にOpenAIで、バブシュキン氏・サツケバー氏と数学の証明のAIの論文を共著しています

つまり、xAIの創業の前にあった「数学の証明をAIに検証させる」研究の輪が、xAIを出たあとに、別の会社の形でつながり直しています。

### ほかの8人は、まだ公の発表がない

ウー氏、バー氏、ヤン氏、ポーレン氏、ジャン氏、ダイ氏、クロイス氏、ノルディーン氏の次の勤め先は、2026年11月24日の時点で、公の発表を見つけられませんでした(ヤン氏の自己紹介は「xai cofounder. fighting lyme」のまま)。ウー氏とバー氏は、退社の投稿で次の行き先を書いていません。

## 4. お金の線: 同じ出し手が、両方の会社にいる

River AIの11億ドル(シードとシリーズA)の出し手は次のとおりです。

- **主導**: General CatalystとAMP PBC
- **戦略投資**: NvidiaとAMD Ventures
- **参加**: Y CombinatorとTemasek
- 企業価値は非公表。5月の時点でForbesは「最大10億ドル・企業価値最大50億ドルを目指し、本人も最大1億ドルを入れる」と報じていて、結果は目標を上回りました

これをxAIの線と並べると、こうなります。

1. **Nvidia**は、2026年1月にxAIのシリーズEに戦略投資家として入り(公式)、8月にはxAIを出たバブシュキン氏のRiver AIにも戦略投資しています
2. **AMP PBC**を作ったアンジニー・ミダ氏は、a16z(アンドリーセン・ホロウィッツ)の元ジェネラルパートナーで、a16zではMistral AIやBlack Forest Labsに投資した人です

人が会社を出ても、半導体メーカーのお金は「人の次の会社」にもついていく。少なくともNvidiaについては、xAIとRiver AIの両方に入っていることが、公式発表と報道で確かめられます。

## 5. この線から読み取れること(筆者の読み取り)

以下は事実カードの並びからの読み取りで、報道が言っていることではありません。

- **「創業メンバー」は、ゼロから集まった人たちではない。** 論文の共著でつながった研究の輪が、xAIという器に入った、と見るほうが実態に近い
- **器がこわれても、輪は残る。** River AIにはxAIの最初の社員が2人、Math Incには「自動形式化」の輪がつながり直している。次の会社を予想するなら、ニュースより論文の共著者の一覧のほうが手がかりになる
- **営業・事業開発で使うなら**: ある会社の人に会うとき、その人の「論文の共著者」と「前の会社の同僚が作った会社」は、紹介をお願いできる道筋の候補になる

## 6. まだ分かっていないこと

- 8人の次の勤め先(公の発表なし)
- コシック氏がProject PrometheusからRiver AIに移った時期(本人の自己紹介で「いまRiver AI」は確か。移った日は未確認)
- セゲディ氏がMorph Labsにいた正確な期間と、Math Incの本文(この環境から開けず、検索結果の要約だけ)
- クロイス氏とノルディーン氏の論文・前職の詳しい中身
- 退社の本当の理由(本人たちはほとんど書いていない)

<!--SOURCES-->
## 出典

本文を読んで確かめたもの
- Wikipedia「SpaceXAI」(旧xAI) https://en.wikipedia.org/wiki/XAI_(company)
- Wikipedia「Kyle Kosic」 https://en.wikipedia.org/wiki/Kyle_Kosic
- Fortune「xAIの組織図」(2023/11/20) https://fortune.com/2023/11/20/xai-organizational-structure-elon-musk-top-executives/
- Fortune(2024/6/28、コシック氏のOpenAI復帰) https://fortune.com/2024/06/28/xai-original-employee-departure-kyle-kosic-engineer/
- Fortune(2026/2/11、創業12人のうち6人) https://fortune.com/2026/02/11/half-of-xai-founding-team-has-left-elon-musks-ai-company-potentially-complicating-his-plans-for-a-blockbuster-spacex-ipo/
- Fortune(2026/3/16、作り直しとMacrohard) https://fortune.com/2026/03/16/elon-musk-xai-rebuilding-cofounders-engineers-exodus-macrohard-project-spacex-acquisition/
- TechCrunch(2026/2/10、ウー氏・バー氏) https://techcrunch.com/2026/02/10/okay-now-exactly-half-of-xais-founding-team-has-left-the-company/
- TechCrunch(2026/8/11、River AIの調達) https://techcrunch.com/2026/08/11/general-catalyst-leads-1-1b-round-into-2-month-old-river-ai/
- The Next Web(2026/3/28、11人全員) https://thenextweb.com/news/xai-all-cofounders-departed-musk-spacex-rebuild
- The Next Web(2026/8/11、River AI) https://thenextweb.com/news/river-ai-1-1-billion-babuschkin-general-catalyst-open-weights
- SiliconANGLE(2025/8/13、バブシュキン氏の退社) https://siliconangle.com/2025/08/13/xai-co-founder-igor-babuschkin-leaving-company-focus-ai-safety/
- Dealroom(2026/8/11、River AI) https://dealroom.co/news/144372-igor-babuschkins-river-ai-raises-1-1b-to-build-an-open-ai-stack/
- xAI公式発表(2026/1/6、シリーズE。相関図の記録) https://x.ai/news/series-e

本人(Xで確認、2026/11/24)
- バブシュキン氏の退社の投稿(2025/8/13) https://x.com/ibab/status/1955741698690322585
- 自己紹介: https://x.com/ibab ・ https://x.com/kylekosic ・ https://x.com/TheGregYang ・ https://x.com/jimmybajimmyba ・ https://x.com/Guodzh

論文(著者と日付を論文目録で確認)
- Adam https://arxiv.org/abs/1412.6980 / Inception https://arxiv.org/abs/1409.4842 / 敵対的サンプル https://arxiv.org/abs/1312.6199
- 自動形式化 https://arxiv.org/abs/2205.12615 / STaR https://arxiv.org/abs/2203.14465 / Minerva https://arxiv.org/abs/2206.14858
- Tensor Programs V https://arxiv.org/abs/2203.03466 / Gopher https://arxiv.org/abs/2112.11446 / 人の好みから報酬 https://arxiv.org/abs/1811.06521
- Transformer-XL https://arxiv.org/abs/1901.02860 / XLNet https://arxiv.org/abs/1906.08237 / AlphaCode https://arxiv.org/abs/2203.07814
- Grokking https://arxiv.org/abs/2201.02177 / 数学の証明(ハン氏と) https://arxiv.org/abs/2202.01344 / Lookahead https://arxiv.org/abs/1907.08610 / Gemini https://arxiv.org/abs/2312.11805

検索結果の要約だけ(本文は未確認)
- ヤン氏のライム病の発表(2026/1/20)、ポーレン氏の退社(Bloomberg 2026/2/27)、ジャン氏の担当と退社、セゲディ氏のMorph Labs・Math Inc(TWIML ほか)

この記事は、AI企業の人・出資・取引のつながりを集めた「AI企業の相関図」のデータから書いています。各項目の確かさは本文の印のとおりです。出典のリンクから元の記事をご確認ください。(発行日 ○○)
