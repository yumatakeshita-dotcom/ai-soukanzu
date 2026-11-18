# 追加調査(2026-11-02)で見つかった人物・出資者と、前の内容の訂正。
# 使い方: apply_adds(CO) が、会社データ(CO)に人物と出資者を足し、記載を直す。
def P_(id, name, f, desc, role, to=None, founder=False):
    d = {'id': id, 'name': name, 'kind': 'p', 'from': f, 'desc': desc, 'role': role}
    if to: d['to'] = to
    if founder: d['founder'] = 1
    return d
def I_(id, name, f, desc, role):
    return {'id': id, 'name': name, 'kind': 'i', 'from': f, 'desc': desc, 'role': role}
def O_(id, name, f, desc, role):
    return {'id': id, 'name': name, 'kind': 'o', 'from': f, 'desc': desc, 'role': role}

ADDS = {
 'openai': dict(
  nodes=[
   P_('pang', 'ルオミン・パン', 2026, '元AppleからMetaを経て、2026年2月にOpenAIへ移ったと報じられています(AIの基盤の責任者)。', 'AI基盤'),
   P_('zoph', 'バレット・ゾフ', 2026, '2026年1月にThinking Machines Labから戻ったと報じられています。', '復帰'),
   P_('metz', 'ルーク・メッツ', 2026, '2026年1月にThinking Machines Labから戻ったと報じられています。', '復帰'),
   P_('schoenholz', 'サム・ショーンホルツ', 2026, '2026年1月にThinking Machines Labから戻ったと報じられています。', '復帰'),
   O_('meta', 'Meta', 2025, 'パンが2025年に移った先。', '元の移籍先'),
   O_('periodic', 'Periodic Labs', 2025, '元OpenAIのVPリアム・フェダスらが設立し、2025年9月に約3億ドルのシードで表に出た、AIで科学の発見を自動化する会社。ダブルクリックで図を開きます。', '元VPが設立'),
   O_('adept', 'Adept', 2022, 'OpenAIの元VPデビッド・ルアンらが共同創業したAIエージェントの会社。2024年6月にAmazonが創業者5人を採用。ダブルクリックで図を開きます。', '元VPが創業'),
   O_('covariant', 'Covariant', 2017, 'OpenAIの元研究者ピーター・アビールらが2017年に創業した、ロボット向けAIの会社。2024年にAmazonが技術ライセンスと人材を獲得。ダブルクリックで図を開きます。', '元研究者が創業'),
   O_('appliedcompute', 'Applied Compute', 2025, 'OpenAIの技術系の元社員3人が2025年に起こした、企業向けAIエージェントの会社。ダブルクリックで図を開きます。', '元社員が創業'),
  ],
  en={'pang': 'Ruoming Pang', 'zoph': 'Barret Zoph', 'metz': 'Luke Metz', 'schoenholz': 'Sam Schoenholz'},
  patch={'altman': {'desc': '1985年シカゴ生まれ。2005年にスタンフォード大学を中退(2年在籍)し、同年にLooptを共同創業してCEOに(2012年3月にGreen Dotが4,340万ドルで買収)。2011年にY Combinatorのパートナー、2014年2月にポール・グレアムの後任で社長(2019年3月に退任)。2014年にはRedditのCEOを8日間務めました。2015年にOpenAIを共同創業し、2019年3月に専任CEOに。2023年11月17日に取締役会に解任され、同月21日までに復帰が決まりました(従業員約770人のうち700人超が、復帰を求める書簡に署名)。2024年2月にマスクに提訴され、2026年5月に陪審が、時効を理由にマスクの請求を退けました。Helion Energyの会長、Worldcoin(Tools for Humanity)の共同創業者でもあります。'}, 'brockman': {'desc': '1987年ノースダコタ州生まれ。ハーバード大学、のちMITに進み、2010年にMITを中退してStripeへ(2013年に初代CTO)。2015年5月にStripeを離れ、同年12月にOpenAIを共同創業(最初は自宅の居間で活動し、創業チームの採用を率いました)。2023年11月17日に、アルトマン解任に合わせて退社を表明し、数日後に復帰。2024年8〜11月は休職。2026年には、フィジー・シモの休職後、製品を含む役割を引き継ぎました。2019年11月に結婚(スツケバーが司式)。AI関連の政治団体などへの高額の寄付が報じられています(額・年の記載は資料で食い違っています)。'}, 'pachocki': {'desc': '1991年、ポーランドのグダニスク生まれ。ワルシャワ大学を出て、カーネギーメロン大学で博士号(指導教官はゲイリー・ミラー)。2012年にGoogle Code Jamで優勝し、ICPC世界大会では銀メダル。ハーバード大学とシモンズ研究所のポスドクを経て、2017年にOpenAIに入社。2021年に研究ディレクターとして、GPT-4とOpenAI Fiveの開発を率い、2024年5月に、スツケバーの退社後のチーフサイエンティストに(アルトマンは「世代を代表する頭脳の一人」と評しました)。'}, 'friar': {'desc': '1972年、北アイルランド生まれ。オックスフォード大学で冶金学・経済・経営を学び、スタンフォードでMBA。Arthur Andersen、McKinsey、Goldman Sachs(エクイティリサーチ)、Salesforceを経て、Squareの初代CFO(2012〜2018年)、Nextdoor CEO(2018〜2024年、2021年にSPACで上場)。2024年6月にOpenAIの初代CFOに就任(Reutersが同年6月10日に報道)。WalmartとConsenSysの取締役。2019年にOBE(大英帝国勲章)、2026年にTime100に選ばれました。'}, 'simo': {'desc': '1985年、フランス・セート生まれ。HEC Paris卒。eBay(2007〜2011年)を経て2011年にFacebookへ入り、約10年、Facebookアプリの責任者(VP)。2021年7月にInstacartのCEO(2023年9月の上場後は取締役会長)。2024年3月にOpenAIの取締役、2025年5月に、最初の「アプリケーション担当CEO」として発表され、同年8月に就任(のち「AGIデプロイメント担当CEO」に改称)。2026年1月にChatGPT Healthを主導。2026年7月にフルタイムを退き、非常勤のアドバイザーになったと報じられています。Shopifyの取締役、Metrodora Instituteの共同創業者。'}},
  career={'altman': [['1985', 'シカゴに生まれる'], ['2005', 'スタンフォード大学を中退し、Looptを共同創業'], ['2012', '3月、Looptを、Green Dotが買収'], ['2014', 'Y Combinatorの社長に(〜2019年)'], ['2015', 'OpenAIを共同創業'], ['2019', '3月、専任のCEOに'], ['2023', '11月17日に解任、21日までに復帰が決まる'], ['2024', '2月、マスクが提訴'], ['2026', '5月、陪審がマスクの請求を、時効を理由に退ける']], 'brockman': [['1987', 'ノースダコタ州に生まれる'], ['2010', 'MITを中退し、Stripeへ(2013年に初代CTO)'], ['2015', '5月にStripeを離れ、12月にOpenAIを共同創業'], ['2019', '11月に結婚(スツケバーが司式)'], ['2023', '11月17日に退社を表明、数日後に復帰'], ['2024', '8〜11月、休職'], ['2026', 'シモの休職後、製品を含む役割を引き継ぐ']], 'pachocki': [['1991', 'ポーランドのグダニスクに生まれる'], ['2012', 'Google Code Jamで優勝'], ['2017', 'OpenAIに入社'], ['2021', '研究ディレクターに(GPT-4、OpenAI Five)'], ['2024', '5月、チーフサイエンティストに']], 'friar': [['2012', 'Squareの初代CFOに(〜2018年)'], ['2018', 'Nextdoor CEOに(〜2024年)'], ['2021', 'NextdoorがSPACで上場'], ['2024', '6月、OpenAIの初代CFOに']], 'simo': [['2007', 'eBayに入社(〜2011年)'], ['2011', 'Facebookに入社'], ['2021', '7月、InstacartのCEOに'], ['2024', '3月、OpenAIの取締役に'], ['2025', '8月、アプリケーション担当CEOに就任'], ['2026', '1月にChatGPT Healthを主導。7月にフルタイムを退くと報じられる']]},
  edges="['zoph','metz','schoenholz'].forEach(a=>E.push({a,b:'tml',k:'from'}));\nE.push({a:'pang',b:'meta',k:'from'});\nE.push({a:'openai',b:'periodic',k:'link',label:'元VPが設立'});\nE.push({a:'openai',b:'covariant',k:'link',label:'元研究者が創業'});E.push({a:'openai',b:'adept',k:'link',label:'元VPが創業'});\nE.push({a:'openai',b:'appliedcompute',k:'link',label:'元社員が創業'});\n"),
 'anthropic': dict(
  nodes=[
   P_('cherny', 'ボリス・チェルニー', 2024, 'Claude Codeの責任者(2026年2月のポッドキャストでの肩書き)。', 'Claude Code責任者'),
   P_('askell', 'アマンダ・アスケル', 2021, '哲学者で、Claudeの性格づけに取り組むと紹介されています。', 'Claudeの性格設計'),
   P_('jumper', 'ジョン・ジャンパー', 2026, 'AlphaFoldでノーベル化学賞を受けた研究者。2026年6月にGoogle DeepMindから移ったと報じられています。', '研究者'),
   O_('deepmind', 'Google DeepMind', 2021, 'ジャンパーの出身元。', '出身元'),
   O_('mirendil', 'Mirendil', 2025, 'Anthropicの元研究者2人(ベナム・ネイシャブール、ハーシュ・メータ)が2025年12月ごろに離れて起こした、科学研究のAIの会社。ダブルクリックで図を開きます。', '元研究者が設立'),
   O_('humans', 'humans&', 2025, '元Anthropic研究者のアンディ・ペンらが2025年に作った会社。2026年1月に4.8億ドルのシードを発表。ダブルクリックで図を開きます。', '元研究者が共同創業'),
  ],
  en={'cherny': 'Boris Cherny', 'askell': 'Amanda Askell', 'jumper': 'John Jumper'},
  patch={'dario': {'desc': '1983年、サンフランシスコ生まれ。カリフォルニア工科大学からスタンフォード大学へ移り、2006年に物理学の学士、2011年にプリンストン大学で生物物理学・計算神経科学の博士号。2014年11月〜2015年10月にBaidu、2015年にGoogle Brain、2016年にOpenAIへ(AI安全のチームとスケーリング則のチームを率い、GPT-2、GPT-3、人間のフィードバックによる強化学習に貢献)。2020年に、ブロックマンやアルトマンとの対立の末、妹ダニエラらとOpenAIを離れ、2021年にAnthropicを共同創業しました。2023年11月に、OpenAIの取締役会から、アルトマンの後任と合併を打診されましたが、断りました。2024年10月にエッセイ「Machines of Loving Grace」、2026年1月に「The Adolescence of Technology」を発表。2026年2月、大量の国内監視や完全自律兵器へのClaudeの使用を禁じる契約条項を外すことを拒み、国防総省が「サプライチェーン上のリスク」と指定したと報じられ、3月26日に連邦地裁が一時差止めを命じました。'}, 'daniela': {'desc': '1987年、サンフランシスコ生まれ。UCサンタクルーズで英文学を学び、政治・国際保健の分野を経て、ペンシルベニア州選出の下院議員の広報を担当。2013年にStripeに初期の社員として入社し、2018年にOpenAIへ(GPT-2の開発期のチームを管理し、のち安全・政策担当VP)。兄ダリオらとOpenAIを離れ、Anthropicの共同創業者で社長に(離れた時期は、資料により2020年または2021年)。安全性とモデルの整合性のチームを率います。2023年9月に、ダリオとともにTimeの「AI分野で最も影響力のある100人」に選ばれました。'}, 'kaplan': {'desc': 'イリノイ数学科学アカデミーを2001年に卒業。スタンフォード大学で物理学・数学の学士、ハーバード大学で物理学の博士号(2009年、指導教官はニマ・アルカニ=ハメド)。SLACとスタンフォードでポスドクを経て、2012年からジョンズ・ホプキンス大学の物理学の教員(現在は准教授と記載)。2019年にOpenAIの研究者となり、2020年1月に「Scaling Laws for Neural Language Models」を共著、GPT-3の論文にも参加。Anthropicの共同創業者でチーフサイエンス・オフィサー。2024年10月に「Responsible Scaling Officer」に就くと発表されました。2025年12月のGuardianのインタビューで、AIに自分自身を改良させるかどうかを、2030年までに人類が決める必要があると述べました。'}, 'clark': {'desc': 'Anthropicの共同創業者(法人化は2021年1月26日)。肩書きは「共同創業者、公益担当責任者(Head of Public Benefit)、元・政策責任者」。2026年3月に発足した、AIを研究するシンクタンク「Anthropic Institute」を率います。元ジャーナリスト(Bloomberg、The Register)で、OpenAIの政策ディレクターを務めたのち、Anthropicへ。ニュースレター「Import AI」の発行者でもあります。'}, 'olah': {'desc': '1991〜92年ごろ、カナダ生まれ(Forbesによる)。トロントの大学で数学を1年学んで中退し、2012年にティール・フェローシップを得ました。2015年にGoogle Brainのインターン、のち研究者(DeepDreamなど、ニューラルネットの可視化に関与)。2017年3月に、機械学習の解説誌「Distill」を共同創刊。2018年にOpenAIの解釈可能性チームの責任者になり、2020年にOpenAIを離れ、Anthropicを共同創業。2024年5月には、モデルの内部の「特徴」を地図にする成果が報じられました。2025年にForbesが、Anthropicの持ち株で億万長者になったと報じています。'}, 'leike': {'desc': '1986または87年生まれ。フライブルク大学で学び、オーストラリア国立大学で機械学習の博士号(指導教官はマーカス・ハッター)。人類の未来研究所のポスドクを経てDeepMindでAI安全の実証研究に。2021年にOpenAIへ入り、2023年にスツケバーとともに「スーパーアラインメント」の共同責任者になりました。2024年5月に退社を表明し、安全の文化と手順が、華やかな製品の後回しになってきたと書き、経営陣への信頼を徐々に失ったと述べました。同月、Anthropicに参加しました(The Vergeの報道は5月28日)。'}},
  career={'dario': [['1983', 'サンフランシスコに生まれる'], ['2006', 'スタンフォード大学を卒業(物理学)'], ['2011', 'プリンストン大学で博士号'], ['2014', '11月、Baiduへ(〜2015年10月)'], ['2015', 'Google Brainへ'], ['2016', 'OpenAIへ(AI安全・スケーリング則を率いる)'], ['2020', 'OpenAIを離れる'], ['2021', 'Anthropicを共同創業'], ['2023', '11月、OpenAIの取締役会からの打診を断る'], ['2024', '10月、エッセイ「Machines of Loving Grace」'], ['2026', '1月にエッセイ。2月に国防総省と対立、3月に連邦地裁が一時差止め']], 'daniela': [['2013', 'Stripeに入社'], ['2018', 'OpenAIへ(のち安全・政策担当VP)'], ['2021', 'Anthropicを共同創業(社長)'], ['2023', '9月、Time「AI分野の100人」に']], 'kaplan': [['2009', 'ハーバード大学で博士号'], ['2012', 'ジョンズ・ホプキンス大学の物理学の教員に'], ['2019', 'OpenAIの研究者に'], ['2020', '1月、スケーリング則の論文を共著'], ['2021', 'Anthropicを共同創業(チーフサイエンス・オフィサー)'], ['2024', '10月、Responsible Scaling Officerに']], 'clark': [['〜', 'ジャーナリスト(Bloomberg、The Register)を経て、OpenAIの政策ディレクターに'], ['2021', 'Anthropicを共同創業'], ['2026', '3月、Anthropic Instituteを率いる']], 'olah': [['2012', 'ティール・フェローシップ'], ['2015', 'Google Brainに'], ['2017', '3月、Distillを共同創刊'], ['2018', 'OpenAIの解釈可能性チームの責任者に'], ['2020', 'OpenAIを離れる'], ['2021', 'Anthropicを共同創業'], ['2024', '5月、モデルの特徴を地図化する成果']], 'leike': [['2021', 'OpenAIに入社'], ['2023', 'スーパーアラインメントの共同責任者に'], ['2024', '5月、OpenAIを退社し、Anthropicに参加']]},
  edges="E.push({a:'jumper',b:'deepmind',k:'from',since:2026});\nE.push({a:'anthropic',b:'mirendil',k:'link',label:'元研究者が設立'});\nE.push({a:'anthropic',b:'humans',k:'link',label:'元研究者が共同創業'});\n"),
 'xai': dict(
  nodes=[
   P_('liberatore', 'マイク・リベラトーレ', 2025, '元CFO。2025年4月に入り、同年7月ごろに退いたと報じられています(理由は不明)。', '元CFO', to=2025),
   P_('armstrong', 'アンソニー・アームストロング', 2025, '元CFO。2025年10月から2026年4月まで在任と報じられています。', '元CFO', to=2026),
   P_('nicolls', 'マイケル・ニコルス', 2026, 'SpaceX出身。2026年4月に社長になったと報じられています。', '社長'),
   P_('shulkin', 'ジョナサン・シュルキン', 2026, '最高売上責任者(CRO)と報じられています。', 'CRO'),
   P_('johnsen', 'ブレット・ジョンセン', 2026, 'SpaceXのCFO。財務はSpaceX経由で運営されると報じられています。', 'SpaceX CFO'),
  ],
  en={'liberatore': 'Mike Liberatore', 'armstrong': 'Anthony Armstrong', 'nicolls': 'Michael Nicolls', 'shulkin': 'Jonathan Shulkin', 'johnsen': 'Bret Johnsen'},
  edges="E.push({a:'nicolls',b:'spacex',k:'from'});\nE.push({a:'johnsen',b:'spacex',k:'link',label:'CFO'});\n"),
 'meta': dict(
  nodes=[
   P_('beyer', 'ルーカス・ベイヤー', 2025, '2025年にOpenAIのチューリッヒ拠点からMSLへ移ったと報じられています。', '研究者'),
   P_('kolesnikov', 'アレクサンダー・コレスニコフ', 2025, '2025年にOpenAIからMSLへ移ったと報じられています。', '研究者'),
   P_('zhai', 'シャオファ・ザイ', 2025, '2025年にOpenAIからMSLへ移ったと報じられています。', '研究者'),
   P_('hren', 'ホンユー・レン', 2025, '2025年にOpenAIからMSLへ移ったと報じられています。', '研究者'),
   P_('jyu', 'ジアフイ・ユー', 2025, '2025年にOpenAIからMSLへ移ったと報じられています。', '研究者'),
   P_('jwei', 'ジェイソン・ウェイ', 2025, '2025年7月にOpenAIからMSLへ移ったと報じられています。', '研究者'),
   P_('hwchung', 'ヒョンウォン・チョン', 2025, '2025年7月にOpenAIからMSLへ移ったと報じられています。', '研究者'),
   P_('psun', 'ペイ・スン', 2025, 'Googleの研究者から、2025年にMSLへ移ったと報じられています。', '研究者'),
  ],
  en={'beyer': 'Lucas Beyer', 'kolesnikov': 'Alexander Kolesnikov', 'zhai': 'Xiaohua Zhai', 'hren': 'Hongyu Ren', 'jyu': 'Jiahui Yu', 'jwei': 'Jason Wei', 'hwchung': 'Hyung Won Chung', 'psun': 'Pei Sun'},
  edges="['beyer','kolesnikov','zhai','hren','jyu','jwei','hwchung'].forEach(a=>E.push({a,b:'openai',k:'from'}));\nE.push({a:'pang',b:'openai',k:'moved'});\n",
  patch={'pang': {'to': 2026, 'role': '元MSLの研究者', 'desc': '元Apple。2025年に巨額の報酬でMetaへ移り、2026年2月にOpenAIへ移ったと報じられています。'}}),
 'gdm': dict(
  nodes=[
   P_('silver', 'デビッド・シルバー', 2010, 'AlphaGoを率いた研究者。2026年1月に退社し、Ineffable Intelligenceを設立と報じられています(単独の報道)。', '元研究者', to=2026),
   P_('sifre', 'ローラン・シフル', 2010, 'Geminiの開発に関わった研究者。2025年に退社し、Holisticを立ち上げと報じられています。', '元研究者', to=2025),
   P_('tuyls', 'カール・タイルス', 2010, 'Geminiの開発に関わった研究者。2025年に退社し、Holisticを立ち上げと報じられています。', '元研究者', to=2025),
   O_('ineffable', 'Ineffable Intelligence', 2026, 'シルバーが設立と報じられています。', 'シルバーの新会社'),
   O_('holistic', 'Holistic', 2025, 'シフルとタイルスが立ち上げと報じられています。', '元研究者の新会社'),
  ],
  en={'silver': 'David Silver', 'sifre': 'Laurent Sifre', 'tuyls': 'Karl Tuyls'},
  edges="E.push({a:'silver',b:'ineffable',k:'moved'});\n['sifre','tuyls'].forEach(a=>E.push({a,b:'holistic',k:'moved'}));\n"),
 'msft': dict(
  nodes=[
   P_('subramanya', 'アマル・スブラマニャ', 2025, 'AI担当のコーポレートVP。Googleに16年在籍し、Geminiのチャットボットを率いた後、DeepMindの専門家20人超と共に移ったと報じられています。', 'AI担当CVP'),
   P_('farhadi', 'アリ・ファルハディ', 2026, '元Allen Institute for AIのCEO。2026年3月に、スレイマンの超知能チームを支えるCVPに就いたと報じられています。', 'CVP'),
   O_('ai2', 'Allen Institute for AI', 2026, 'ファルハディの出身元。', '出身元'),
  ],
  en={'subramanya': 'Amar Subramanya', 'farhadi': 'Ali Farhadi'},
  edges="E.push({a:'subramanya',b:'deepmind',k:'from'});\nE.push({a:'farhadi',b:'ai2',k:'from'});\n"),
 'tml': dict(
  nodes=[
   P_('parish', 'ジョリーン・パリッシュ', 2025, 'セキュリティを専門とする創設期のメンバー。2026年に退いたと報じられています。', '元メンバー', to=2026),
   P_('guy', 'リア・ガイ', 2025, '2026年に退社し、OpenAIへ移ると報じられています。', '元メンバー', to=2026),
   P_('oconnell', 'イアン・オコネル', 2025, '2026年に退社したと報じられています。', '元メンバー', to=2026),
  ],
  en={'parish': 'Jolene Parish', 'guy': 'Lia Guy', 'oconnell': 'Ian O\'Connell'},
  edges="E.push({a:'guy',b:'openai',k:'moved'});\n"),
 'ssi': dict(nodes=[I_('lightspeed', 'Lightspeed', 2025, '2025年の増資に、過去の出資者として参加と報じられています。', 'VC')], en={}, edges=""),
 'mistral': dict(
  nodes=[
   P_('bergqvist', 'ヨハン・ベルクビスト', 2025, 'CFOと報じられています(資金調達のまとめ記事)。', 'CFO'),
   P_('hall', 'ブライアン・ホール', 2025, 'CMOと報じられています(資金調達のまとめ記事)。', 'CMO'),
   I_('psg', 'PSG', 2025, '2025年のシリーズCの参加者として挙がっています。', '投資会社'),
  ],
  en={'bergqvist': 'Johan Bergqvist', 'hall': 'Brian Hall'}, edges=""),
 'nvidia': dict(
  nodes=[
   P_('puri', 'アジャイ・プリ', 2016, '全世界の現場の運営を担う上級副社長(2026年2月の10-K)。', 'EVP'),
   P_('shoquist', 'デボラ・ショキスト', 2016, '運営担当の上級副社長(2026年2月の10-K)。', 'EVP'),
   P_('teter', 'ティモシー・テーター', 2016, '上級副社長で法務責任者(2026年2月の10-K)。', 'EVP / 法務'),
   P_('coxe', 'テンチ・コックス', 2016, '1993年から取締役を務めています。', '取締役'),
   P_('dabiri', 'ジョン・ダビリ', 2020, '2020年から取締役を務めています。', '取締役'),
   P_('neal', 'スティーブン・ニール', 2016, '1997年から取締役を務めています。', '取締役'),
   P_('noraj', 'スザンヌ・ノラ・ジョンソン', 2026, '2026年7月13日付で取締役に就任(取締役会は11人に)。', '取締役'),
  ],
  en={'puri': 'Ajay Puri', 'shoquist': 'Debora Shoquist', 'teter': 'Timothy Teter', 'coxe': 'Tench Coxe', 'dabiri': 'John Dabiri', 'neal': 'Stephen Neal', 'noraj': 'Suzanne Nora Johnson'}, edges=""),
 'perplexity': dict(
  nodes=[
   I_('accel', 'Accel', 2023, '出資者の一社として挙がっています。', 'VC'),
   I_('bessemer', 'Bessemer Venture Partners', 2023, 'シリーズBの参加者として挙がっています。', 'VC'),
   I_('eladgil', 'イラッド・ギル', 2023, '個人の出資者として挙がっています。', '個人投資家'),
   I_('friedman', 'ナット・フリードマン', 2023, '個人の出資者として挙がっています。', '個人投資家'),
  ],
  en={'eladgil': 'Elad Gil', 'friedman': 'Nat Friedman'}, edges=""),
 'cohere': dict(
  nodes=[
   P_('blunsom', 'フィル・ブランサム', 2019, 'チーフサイエンティストからCTOに昇格したと報じられています。オックスフォード大学の教授でもあります。', 'CTO'),
   P_('chadwick', 'フランソワ・シャドウィック', 2025, '初のCFO。', 'CFO'),
   P_('kon', 'マーティン・コン', 2020, '元社長。2026年の体制の変更で役割から退いたと報じられています(関与は続く)。', '元社長', to=2026),
   P_('baji', 'ソラブ・バジ', 2021, '元CTO。ブランサムのCTO昇格に伴い退社と報じられています。', '元CTO', to=2025),
   I_('oracle', 'Oracle', 2023, '2023年のシリーズCに参加と報じられています。', '戦略出資者'),
   I_('salesforce', 'Salesforce Ventures', 2023, '2023年のシリーズCに参加と報じられています。', '戦略出資者'),
  ],
  en={'blunsom': 'Phil Blunsom', 'chadwick': 'François Chadwick', 'kon': 'Martin Kon', 'baji': 'Saurabh Baji'}, edges=""),
 'scale': dict(
  nodes=[P_('desouza', 'フランシス・デソーザ', 2026, 'CEO。2026年8月10日に就任と発表されました。元Google CloudのCOO、元IlluminaのCEO。', 'CEO')],
  en={'desouza': 'Francis deSouza'}, edges="E.push({a:'droege',b:'desouza',k:'link',label:'後任に引き継ぎ'});\n",
  patch={'droege': {'to': 2026, 'role': '元暫定CEO', 'desc': '2025年6月から暫定CEOを務め、2026年8月にデソーザへ引き継ぎました。Uber Eatsの元責任者。'}}),
 'databricks': dict(
  nodes=[
   P_('conte', 'デイブ・コンテ', 2024, 'CFO。元SplunkのCFOで、上場に向けて迎えられたと報じられています。', 'CFO'),
   P_('gabrisko', 'ロン・ガブリスコ', 2020, '最高売上責任者(CRO)。', 'CRO'),
   I_('insight', 'Insight Partners', 2025, '2025年12月のシリーズLを共同で主導と報じられています。', '投資会社'),
   I_('fidelity', 'Fidelity', 2025, 'シリーズLを共同で主導と報じられています。', '資産運用会社'),
   I_('jpmorgan', 'J.P. Morgan', 2025, 'シリーズLを共同で主導と報じられています。', '金融グループ'),
   I_('qia', 'Qatar Investment Authority', 2025, 'シリーズLに参加の政府系ファンドと報じられています。', '政府系ファンド'),
   I_('gic', 'GIC', 2025, 'シリーズLに参加の政府系ファンドと報じられています。', '政府系ファンド'),
   I_('temasek', 'Temasek', 2025, 'シリーズLに参加の政府系ファンドと報じられています。', '政府系ファンド'),
   I_('mgx', 'MGX', 2025, 'シリーズLに参加と報じられています。', 'ファンド'),
  ],
  en={'conte': 'Dave Conte', 'gabrisko': 'Ron Gabrisko'}, edges=""),
 'twitter': dict(
  nodes=[
   I_('crv', 'Charles River Ventures', 2007, '2007年のシリーズAの出資者。', '初期のVC'),
   I_('andreessen', 'マーク・アンドリーセン', 2007, '2007年のシリーズAの個人出資者(のちa16zを共同創業)。', '個人投資家'),
   I_('conway', 'ロン・コンウェイ', 2007, '2007年のシリーズAの個人出資者(シリコンバレーの著名なエンジェル)。', '個人投資家'),
   I_('sacca', 'クリス・サッカ', 2007, '最初期に出資した個人投資家として知られます。', '個人投資家'),
   I_('naval', 'ナヴァル・ラヴィカント', 2007, '2007年のシリーズAの個人出資者。', '個人投資家'),
   I_('spark', 'Spark Capital', 2008, '2008〜2009年の出資者として挙がっています。', '初期のVC'),
   I_('digitalgarage', 'デジタルガレージ', 2008, '日本の企業。2008〜2009年の出資者として挙がっています。', '日本の出資者'),
   I_('bezosexp', 'Bezos Expeditions', 2008, 'ベゾスの投資会社。2008年の出資者として挙がっています。', '初期の出資者'),
  ],
  en={'andreessen': 'Marc Andreessen', 'conway': 'Ron Conway', 'sacca': 'Chris Sacca', 'naval': 'Naval Ravikant'}, edges=""),
 'notion': dict(
  nodes=[
   P_('fuzzy', 'ファジー・コスロシャヒ', 2020, 'CTOと紹介されています(営業データ会社の一覧による)。', 'CTO'),
   P_('anderson', 'エリカ・アンダーソン', 2020, '最高売上責任者(CRO)と紹介されています(同上)。', 'CRO'),
   P_('katkar', 'ラマ・カトカル', 2020, 'CFOと紹介されています(同上)。', 'CFO'),
   P_('sachs', 'サラ・サックス', 2022, 'AI担当のリード(AIエンジニアリング)として紹介されています。', 'AIリード'),
   I_('gic', 'GIC', 2026, '2026年のテンダーオファー(約2.7億ドル、評価額約110億ドル)の買い手として挙がっています。', '政府系ファンド'),
  ],
  en={'fuzzy': 'Fuzzy Khosrowshahi', 'anderson': 'Erica Anderson', 'katkar': 'Rama Katkar', 'sachs': 'Sarah Sachs'}, edges=""),
 'figma': dict(
  nodes=[
   P_('yamashita', 'ユウキ・ヤマシタ', 2018, '最高製品責任者(CPO)。上場前の名簿による。', 'CPO'),
   P_('voskanian', 'ショーント・ヴォスカニアン', 2018, '最高売上責任者(CRO)。上場前の名簿による。', 'CRO'),
   P_('krasmussen', 'クリス・ラスムッセン', 2013, 'CTO。上場前の名簿による。', 'CTO'),
   P_('kramer', 'ケリー・クレーマー', 2021, '取締役(上場前の名簿)。', '取締役'),
   P_('lilly', 'ジョン・リリー', 2021, '取締役(上場前の名簿)。', '取締役'),
   P_('hamid', 'マムーン・ハミド', 2018, '取締役(上場前の名簿)。ベンチャーキャピタルKleiner Perkinsのパートナー。', '取締役'),
   P_('reed', 'アンドリュー・リード', 2018, '取締役(上場前の名簿)。', '取締役'),
   P_('rimer', 'ダニー・ライマー', 2013, '取締役(上場前の名簿)。Index Venturesのパートナー。', '取締役'),
   P_('vojvodich', 'リン・ボイボディッチ', 2021, '取締役(上場前の名簿)。', '取締役'),
   P_('mcdermott', 'ビル・マクダーモット', 2025, 'ServiceNowのCEO。上場時の資料で、取締役に加わったと報じられています。', '取締役'),
   P_('vonahn', 'ルイス・フォン・アーン', 2025, 'DuolingoのCEO。取締役に加わったと報じられています。', '取締役'),
  ],
  en={'yamashita': 'Yuhki Yamashita', 'voskanian': 'Shaunt Voskanian', 'krasmussen': 'Kris Rasmussen', 'kramer': 'Kelly Kramer', 'lilly': 'John Lilly', 'hamid': 'Mamoon Hamid',
      'reed': 'Andrew Reed', 'rimer': 'Danny Rimer', 'vojvodich': 'Lynn Vojvodich', 'mcdermott': 'Bill McDermott', 'vonahn': 'Luis von Ahn'}, edges=""),
 'stripe': dict(
  nodes=[
   P_('gaybrick', 'ウィル・ゲイブリック', 2020, '最高製品責任者(CPO)。', 'CPO'),
   P_('tomlinson', 'ステファン・トムリンソン', 2022, 'CFO。', 'CFO'),
   P_('omara', 'アイリーン・オマラ', 2018, '最高売上責任者から、2026年6月に副会長(取締役会)に移ったと報じられています。', '副会長'),
   P_('davies', 'クリスタ・デイビス', 2020, '取締役。', '取締役'),
   P_('greene', 'ダイアン・グリーン', 2018, '取締役。元Google CloudのCEO。', '取締役'),
   P_('jchadwick', 'ジョナサン・チャドウィック', 2020, '取締役。', '取締役'),
   P_('moritz', 'マイケル・モリッツ', 2011, '取締役。Sequoia Capitalの元幹部で、初期の出資者として知られます。', '取締役'),
  ],
  en={'gaybrick': 'Will Gaybrick', 'tomlinson': 'Steffan Tomlinson', 'omara': 'Eileen O\'Mara', 'davies': 'Christa Davies', 'greene': 'Diane Greene', 'jchadwick': 'Jonathan Chadwick', 'moritz': 'Michael Moritz'}, edges=""),
 'canva': dict(
  nodes=[
   P_('steckelberg', 'ケリー・ステッケルバーグ', 2021, 'CFO。元ZoomのCFOと報じられています。', 'CFO'),
   P_('humphreys', 'ブレンダン・ハンフリーズ', 2014, '元CTO。12年在籍し、2026年6月に退任と報じられています。', '元CTO', to=2026),
   P_('newton', 'サイモン・ニュートン', 2026, 'ハンフリーズの後任として、技術部門を率いると報じられています。', '技術部門の責任者'),
  ],
  en={'steckelberg': 'Kelly Steckelberg', 'humphreys': 'Brendan Humphreys', 'newton': 'Simon Newton'}, edges="E.push({a:'humphreys',b:'newton',k:'link',label:'後任'});\n"),
 'cursor': dict(
  nodes=[P_('mccarthy', 'ブライアン・マッカーシー', 2026, '2026年2月に、グローバルの売上・現場運営の社長に就任と発表されました。', '売上担当の社長')],
  en={'mccarthy': 'Brian McCarthy'}, edges="",
  patch={'spacex': {'desc': '2026年4月に、年内に約600億ドルで買収する権利を得る契約(行使しない場合は約100億ドルで協業を続ける)を結んだと、Fortuneなどが報じています。買収の完了は確認できていません。', 'role': '買収の権利(報道)'}},
  edge_replace=[("label:'買収の報道(未確認)'", "label:'年内に約600億ドルで買収する権利(報道)'")]),
 'slack': dict(
  nodes=[P_('harris', 'パーカー・ハリス', 2024, 'Salesforceの共同創業者。2024年3月に、ヘンダーソンの後任のCTOになりました。', 'CTO')],
  en={'harris': 'Parker Harris'}, edges="E.push({a:'harris',b:'henderson',k:'link',label:'後任のCTO'});\nE.push({a:'harris',b:'salesforce',k:'link',label:'共同創業者'});\n",
  patch={'henderson': {'to': 2024, 'role': '元CTO / 共同創業者', 'desc': '共同創業者で元CTO。2009年から在籍し、2024年3月に退きました(後任はSalesforce共同創業者のパーカー・ハリス)。'},
         'seaman': {'role': '暫定CEO', 'desc': '元の製品責任者。ドレッサーの退任後(2025年12月)に、暫定でSlackを率います。常任の後任は確認できていません。'}}),
 'uber': dict(
  nodes=[
   P_('macdonald', 'アンドリュー・マクドナルド', 2025, '社長兼COO。2025年6月から。', '社長兼COO'),
   P_('hazelbaker', 'ジル・ヘイゼルベイカー', 2019, '最高マーケティング責任者(CMO)。2019年6月から。', 'CMO'),
   P_('west', 'トニー・ウェスト', 2019, '上級副社長で最高法務責任者。', 'CLO'),
   P_('sugar', 'ロナルド・シュガー', 2017, '取締役会の独立議長(2026年の委任状)。', '取締役会議長'),
   P_('advaithi', 'レバティ・アドバイティ', 2020, '取締役。FlexのCEO。', '取締役'),
   P_('alnowaiser', 'トルキ・アルノワイザー', 2024, '取締役の候補。サウジの政府系ファンドPIFの幹部。', '取締役'),
  ],
  en={'macdonald': 'Andrew Macdonald', 'hazelbaker': 'Jill Hazelbaker', 'west': 'Tony West', 'sugar': 'Ronald Sugar', 'advaithi': 'Revathi Advaithi', 'alnowaiser': 'Turqi Alnowaiser'},
  edges="E.push({a:'alnowaiser',b:'pif',k:'link',label:'PIFの幹部'});\n"),
 'doordash': dict(
  nodes=[
   P_('yandell', 'キース・ヤンデル', 2020, '最高事業責任者(CBO)。2026年4月の委任状による。', 'CBO'),
   P_('sherringham', 'ティア・シェリンガム', 2020, '法務責任者(ゼネラル・カウンセル)。', '法務責任者'),
   P_('sbrown', 'ショナ・ブラウン', 2018, '取締役(筆頭の独立取締役とする資料があります)。', '取締役'),
   P_('alin', 'アルフレッド・リン', 2013, '取締役。Sequoia Capitalのパートナー。', '取締役'),
   P_('kovac', 'ミラン・コバッチ', 2026, '2026年1月に取締役に選任されました(取締役は11人に)。', '取締役'),
  ],
  en={'yandell': 'Keith Yandell', 'sherringham': 'Tia Sherringham', 'sbrown': 'Shona Brown', 'alin': 'Alfred Lin', 'kovac': 'Milan Kovac'},
  edges="E.push({a:'alin',b:'sequoia',k:'link',label:'パートナー'});\nE.push({a:'tang',b:'doordash',k:'link',label:'取締役'});\n"),
 'waymo': dict(
  nodes=[
   I_('bessemer', 'Bessemer Venture Partners', 2026, '2026年2月のラウンドに参加と報じられています。', 'VC'),
   I_('tiger', 'Tiger Global', 2026, '2026年2月のラウンドに参加と報じられています。', '投資会社'),
   I_('troweprice', 'T. Rowe Price', 2026, '2026年2月のラウンドに参加と報じられています。', '資産運用会社'),
   I_('fidelity', 'Fidelity', 2021, '2021年のラウンドと2026年のラウンドに参加と報じられています。', '資産運用会社'),
   I_('temasek', 'Temasek', 2026, '2026年2月のラウンドに参加と報じられています。', '政府系ファンド'),
  ],
  en={}, edges=""),
 'newmo': dict(
  nodes=[
   P_('sogawa', '曽川景介', 2024, 'CTO。メルペイの取締役、メルカリのCISOなどの経歴が紹介されています。', 'CTO'),
   P_('matsumoto', '松本龍祐', 2024, 'CPO(最高製品責任者)。', 'CPO'),
   P_('muto', '武藤健太郎', 2024, 'CFO(最高財務責任者)。', 'CFO'),
   P_('noji', '野地春菜', 2024, '経営メンバーとして紹介されています。', '経営メンバー'),
   P_('miyazaki', '宮崎聡', 2024, '経営メンバーとして紹介されています。', '経営メンバー'),
   I_('jafco', 'JAFCO', 2024, '2024年2月のシードに新規投資家として参加と報じられています。', 'VC'),
   I_('dcm', 'DCM Ventures', 2024, '2024年2月のシードに新規投資家として参加と報じられています。', 'VC'),
   I_('dualbridge', 'Dual Bridge Capital', 2025, '2025年7月の追加ラウンドに参加と報じられています。', 'VC'),
   I_('iwagin', 'いわぎん未来投資', 2025, '2025年7月の追加ラウンドに参加した、岩手銀行系のVC。', '地方金融系のVC'),
   I_('gogin', 'ごうぎんキャピタル', 2025, '2025年7月の追加ラウンドに参加した、山陰合同銀行系のVC。', '地方金融系のVC'),
  ],
  en={'sogawa': 'Keisuke Sogawa', 'matsumoto': 'Ryusuke Matsumoto', 'muto': 'Kentaro Muto', 'noji': 'Haruna Noji', 'miyazaki': 'Satoshi Miyazaki'}, edges="E.push({a:'sogawa',b:'mercari',k:'from'});\n",
  patch={'newmo': {'desc': '2024年1月に設立された、日本のモビリティの会社。大阪でタクシー会社を傘下に収め、府内3位規模のタクシーグループになったと説明されています。シリーズAは2025年7月に総額179億円でクローズし、創業からの累計の調達額は約199億円(2026年7月時点の採用ページ)。自動運転タクシー事業にも本格的に参入する方針と報じられています。'}}),
 'go': dict(
  nodes=[I_('docomo', 'NTT Docomo', 2020, '2026年6月に、主要株主でなくなったと報じられています(臨時報告書)。', '元の主要株主')],
  en={}, edges="",
  patch={'go': {'desc': 'タクシー配車アプリ「GO」の会社。2020年4月にDeNAのタクシー事業とJapanTaxiが統合してMobility Technologiesとなり、2023年にGO株式会社へ改称。東京証券取引所に上場(2026年)し、2026年2月に1株を100株に分割。従業員は約600人(2026年6月)。配車事業は2025年5月期に、通期で初めて黒字化と報じられています。'},
         'nakajima': {'role': '代表取締役社長', 'desc': '代表取締役社長。2026年5月期の決算短信と、2026年8月提出の有価証券報告書に記載されています。'},
         'kawanabe': {'role': '代表取締役会長', 'desc': '代表取締役会長。日本交通の経営者として知られます(2026年5月の通知文に記載)。'},
         'dena': {'desc': '2026年6月の臨時報告書で、議決権の割合が25.75%から4.99%に下がり、主要株主でなくなったと報じられています(上場に伴う売出し)。'},
         'nihonkotsu': {'desc': '日本交通ホールディングス。議決権の割合は25.75%(2026年1月31日現在)で、GOの「その他の関係会社」にあたります。'}}),
 'demaecan': dict(
  nodes=[
   P_('masuda', '舛田淳', 2020, '取締役(2025年8月時点の資料)。', '取締役'),
   P_('mori', '森一生', 2020, '取締役(2025年8月時点の資料)。', '取締役'),
   P_('toyama', '富山浩樹', 2020, '取締役(2025年8月時点の資料)。', '取締役'),
   P_('sakaue', '坂上亮介', 2020, '取締役(2025年8月時点の資料)。LINEヤフーの取締役CFOでもあります。', '取締役'),
  ],
  en={'masuda': 'Jun Masuda', 'mori': 'Ichio Mori', 'toyama': 'Hiroki Toyama', 'sakaue': 'Ryosuke Sakaue'}, edges=""),
 'boost': dict(
  nodes=[
   P_('ito', '伊藤浩樹', 2024, 'Director / Operating Partner。ピクシブの元代表取締役CEOで、2018年にアルプを創業しました(公式サイトのチーム紹介)。', 'Director / Operating Partner'),
   P_('b_takahashi', '高橋良暢', 2025, 'シニアコンサルタント。2025年7月に入社。NTTデータ、野村総合研究所を経ました(ブーストコンサルティング公式noteの社員紹介)。', 'シニアコンサルタント'),
   P_('b_taniguchi', '谷口航輝', 2025, 'AIエンジニア。サイバーエージェントでソーシャルゲームのバックエンドを担当した後に入社(同上)。', 'AIエンジニア'),
   P_('b_taguchi', '田口真言', 2025, 'AIプロダクトエンジニア。日本IBM、AppsFlyer、Brazeを経て入社(同上)。', 'AIプロダクトエンジニア'),
   P_('b_ishikawa', '石川寛人', 2025, 'シニアコンサルタント。NTTデータで大規模システム開発やDX推進を担当した後に入社(同上)。', 'シニアコンサルタント'),
   P_('b_aihara', '相原寛人', 2025, 'エンジニア。Speeeでデータ分析やAI活用の推進を担当した後に入社(同上)。', 'エンジニア'),
   O_('pixiv', 'ピクシブ', 2024, '伊藤氏が代表取締役CEOを務めた会社。', '出身元'),
   O_('alp', 'アルプ', 2024, '伊藤氏が2018年に創業した会社。', '伊藤氏が創業'),
   O_('nttdata', 'NTTデータ', 2025, '高橋氏と石川氏の出身元。', '出身元'),
   O_('nri', '野村総合研究所', 2025, '高橋氏の出身元。', '出身元'),
   O_('cyberagent', 'サイバーエージェント', 2025, '谷口氏の出身元。', '出身元'),
   O_('ibmjp', '日本IBM', 2025, '田口氏の出身元。', '出身元'),
   O_('appsflyer', 'AppsFlyer', 2025, '田口氏の出身元。', '出身元'),
   O_('braze', 'Braze', 2025, '田口氏の出身元。', '出身元'),
   O_('speee', 'Speee', 2025, '相原氏の出身元。', '出身元'),
   O_('happys', 'ハッピーズ', 2024, '高橋氏が役員や株主を兼ねる会社(公式サイト)。', '高橋氏の役員先'),
   O_('ezo', 'EZO CONSULTING GROUP', 2024, '高橋氏が役員や株主を兼ねる会社(公式サイト)。', '高橋氏の役員先'),
   O_('acrove', 'ACROVE', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('arch', 'ARCH', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('aeterlink', 'Aeterlink', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('comisma', 'COMISMA', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('driver', 'DRIVER Technologies', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('h2corp', 'H2Corporation', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('halu', 'HA-LU', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('kidou', 'Kidou Systems', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('legalagent', 'Legal Agent', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('noahlogy', 'Noahlogy', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('plugo', 'PLUGO', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('paradigm', 'Paradigm AI', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('qolony', 'Qolony', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('sova', 'SoVa', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('medimo', 'medimo', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
   O_('toggle', 'toggle holdings', 2024, '投資先(公式サイトのPortfolio)。', '投資先'),
  ],
  en={'ito': 'Hiroki Ito', 'b_takahashi': '高橋良暢', 'b_taniguchi': '谷口航輝', 'b_taguchi': '田口真言', 'b_ishikawa': '石川寛人', 'b_aihara': '相原寛人'},
  edges="['acrove','arch','aeterlink','comisma','driver','h2corp','halu','kidou','legalagent','noahlogy','plugo','paradigm','qolony','sova','medimo','toggle'].forEach(b=>E.push({a:'boostcap',b,k:'invest2'}));\nE.push({a:'ito',b:'pixiv',k:'from'});\nE.push({a:'ito',b:'alp',k:'link',label:'創業'});\n['b_takahashi','b_ishikawa'].forEach(a=>E.push({a,b:'nttdata',k:'from'}));\nE.push({a:'b_takahashi',b:'nri',k:'from'});\nE.push({a:'b_taniguchi',b:'cyberagent',k:'from'});\n['ibmjp','appsflyer','braze'].forEach(b=>E.push({a:'b_taguchi',b,k:'from'}));\nE.push({a:'b_aihara',b:'speee',k:'from'});\n['b_takahashi','b_taniguchi','b_taguchi','b_ishikawa','b_aihara'].forEach(a=>E.push({a,b:'boostcons',k:'link',label:'社員'}));\nE.push({a:'takahashi',b:'happys',k:'link',label:'役員'});\nE.push({a:'takahashi',b:'ezo',k:'link',label:'役員'});\nE.push({a:'takahashi',b:'terass',k:'link',label:'役員'});\n",
  patch={'ozawa': {'desc': '代表取締役。CSK、ビズシーク、楽天を経て、ヤフーで代表取締役社長 社長執行役員CEOを務めました(公式サイトのチーム紹介)。2024年1月にBoost Capitalを設立。2026年8月にラクスルの社外取締役にも就任しました。'},
         'hori': {'role': '取締役 / パートナー', 'desc': '取締役でパートナー(公式サイト)。ブーストコンサルティングの代表者とされます。Z Venture Capitalの代表を務め、著書に共著の『STARTUP』があります。'},
         'takahashi': {'role': '取締役 / パートナー', 'desc': '取締役でパートナー(公式サイト)。マッキンゼー、MBKパートナーズを経て、MITスローン経営大学院でMBAを取得。ハッピーズ、EZO CONSULTING GROUP、TERASSの役員や株主も兼ねます。'},
         'boostcons': {'desc': 'ブーストコンサルティング株式会社。2025年4月4日設立のAIネイティブ型のコンサルティング会社。代表者は堀新一郎氏、本社は東京・麻布台ヒルズ(求人票・公式の採用ページ)。公式noteで社員紹介を公開しており、ここでは名前の出ている5人を載せています。5年で売上300億円・従業員1,000人を目指すと募集ページに書かれています。'}}),
 'sakana': dict(
  nodes=[
   P_('schmidhuber', 'ユルゲン・シュミットフーバー', 2026, 'チーフ・サイエンティフィック・アドバイザー。2026年10月に就任と発表されました。世界モデルとフィジカルAIの開発を主導し、新設のRSI Labを支援します。', 'チーフ・サイエンティフィック・アドバイザー'),
   O_('rsilab', 'RSI Lab', 2026, 'シュミットフーバーの支援で新設された研究組織。', '新設の研究組織'),
  ],
  en={'schmidhuber': 'Jürgen Schmidhuber'}, edges="E.push({a:'schmidhuber',b:'rsilab',k:'link',label:'運営を支援'});\n"),
 'softbank': dict(nodes=[], en={}, edges="",
  patch={'son': {'desc': '創業者で会長兼社長。スターゲートの会長を務めます。持株比率は約32.7%で筆頭株主です(2026年3月期)。'}}),
 'pfn': dict(
  nodes=[
   P_('ono', '大野直人', 2025, 'COO。2025年4月に企画本部長として入社し、同年11月にCOOに就任しました。', 'COO'),
   P_('maruyama', '丸山宏', 2025, '取締役(監査等委員会委員長)兼PFN Fellow。2016年に入社し、2020〜2024年は花王に出向していました。', '取締役 / Fellow'),
   I_('mhi', 'Mitsubishi Heavy Industries', 2018, '三菱重工業。株主として挙がっています(株主情報サイト)。', '株主'),
   I_('gmo', 'GMO Internet Group', 2018, 'GMOインターネットグループ。株主として挙がっています(株主情報サイト)。', '株主'),
   I_('shinetsu', 'Shin-Etsu Chemical', 2018, '信越化学工業。株主として挙がっています(株主情報サイト)。', '株主'),
   I_('sbiinv', 'SBI Investment', 2018, 'SBIインベストメント。株主として挙がっています(株主情報サイト)。', '株主'),
  ],
  en={'ono': 'Naoto Ono', 'maruyama': 'Hiroshi Maruyama'}, edges="E.push({a:'ono',b:'okanohara',k:'link',label:'COO'});\n"),
 'pksha': dict(
  nodes=[
   P_('yoshida', '吉田幸弘', 2022, '社外取締役(掲載時期不明の一覧による)。', '社外取締役'),
   P_('mizutani', '水谷武彦', 2022, '社外取締役(同上)。', '社外取締役'),
   P_('sato', '佐藤裕介', 2022, '社外取締役(同上)。', '社外取締役'),
   P_('shimomura', '下村正之', 2022, '社外取締役(同上)。', '社外取締役'),
   P_('fujioka', '藤岡大輔', 2022, '社外取締役(同上)。', '社外取締役'),
  ],
  en={'yoshida': 'Yukihiro Yoshida', 'mizutani': 'Takehiko Mizutani', 'sato': 'Yusuke Sato', 'shimomura': 'Masayuki Shimomura', 'fujioka': 'Daisuke Fujioka'}, edges=""),
 'rakuten': dict(
  nodes=[
   P_('hirose', '廣瀬研二', 2020, '取締役副社長執行役員で、最高財務責任者(CFO)。2026年3月の有価証券報告書による。', 'CFO'),
   P_('kaga', '加賀栄一', 2020, '取締役常務執行役員。IRの問い合わせ先の責任者(2026年5月の決算短信)。', '取締役'),
  ],
  en={'hirose': 'Kenji Hirose', 'kaga': 'Eiichi Kaga'}, edges=""),
 'ly': dict(
  nodes=[
   P_('sakaue', '坂上亮介', 2023, '取締役CFO。2026年6月の株主総会で、取締役に選任されました。', '取締役CFO'),
   P_('tamatsuka', '玉塚元一', 2026, '社外取締役(独立役員)。2026年6月の株主総会で選任されました。元ローソンのCEOとして知られます。', '社外取締役'),
   O_('demaecan', 'Demae-can', 2019, '出前館。LINEヤフーの傘下(坂上氏が取締役を兼ねます)。', '傘下の会社'),
   P_('hide', '秀誠', 2026, '2026年10月1日付で新設されるCOOに選任されたと発表されました(コマースドメインリード)。', 'COO'),
  ],
  en={'sakaue': 'Ryosuke Sakaue', 'tamatsuka': 'Genichi Tamatsuka', 'hide': 'Makoto Hide'},
  edges="E.push({a:'sakaue',b:'demaecan',k:'link',label:'出前館の取締役'});\n",
  patch={'kawabe': {'desc': '元会長。2026年6月19日付で代表取締役会長を退任しました(2026年4月の取締役会で決議)。後任の会長は確認できていません。'}}),
}

LEGACY_KEYS = ('openai', 'anthropic', 'xai', 'meta')
LEGACY_EDGES = {
 'openai': [{'a': 'zoph', 'b': 'tml', 'k': 'from'}, {'a': 'metz', 'b': 'tml', 'k': 'from'}, {'a': 'schoenholz', 'b': 'tml', 'k': 'from'}, {'a': 'pang', 'b': 'meta', 'k': 'from'},
  {'a': 'openai', 'b': 'periodic', 'k': 'link', 'label': '元VPが設立'}, {'a': 'openai', 'b': 'covariant', 'k': 'link', 'label': '元研究者が創業'}, {'a': 'openai', 'b': 'adept', 'k': 'link', 'label': '元VPが創業'}, {'a': 'openai', 'b': 'appliedcompute', 'k': 'link', 'label': '元社員が創業'}],
 'anthropic': [{'a': 'jumper', 'b': 'deepmind', 'k': 'from', 'since': 2026}, {'a': 'anthropic', 'b': 'mirendil', 'k': 'link', 'label': '元研究者が設立'}, {'a': 'anthropic', 'b': 'humans', 'k': 'link', 'label': '元研究者が共同創業'}],
 'xai': [{'a': 'nicolls', 'b': 'spacex', 'k': 'from'}, {'a': 'johnsen', 'b': 'spacex', 'k': 'link', 'label': 'CFO'}],
 'meta': [{'a': x, 'b': 'openai', 'k': 'from'} for x in ('beyer', 'kolesnikov', 'zhai', 'hren', 'jyu', 'jwei', 'hwchung')] + [{'a': 'pang', 'b': 'openai', 'k': 'moved'}],
}
def legacy_json():
    out = {}
    for k in LEGACY_KEYS:
        a = ADDS[k]
        out[k] = {'nodes': a['nodes'], 'en': a['en'], 'patch': a.get('patch', {}), 'career': a.get('career', {}), 'edges': LEGACY_EDGES[k]}
    return out

def apply_adds(CO):
    for key, a in ADDS.items():
        if key in LEGACY_KEYS:
            continue
        c = CO[key]
        ids = {n['id'] for n in c['N']}
        for n in a.get('nodes', []):
            if n['id'] in ids:
                continue   # 同じidは追加しない
            c['N'].append(n); ids.add(n['id'])
        c['EN'].update(a.get('en', {}))
        c.setdefault('CAREER', {}).update(a.get('career', {}))
        for k, v in a.get('patch', {}).items():
            for n in c['N']:
                if n['id'] == k:
                    n.update(v)
        e = c['edges']
        for old, new in a.get('edge_replace', []):
            e = e.replace(old, new)
        if a.get('edges'):
            e = e.rstrip('\n') + '\n' + a['edges'] + '\n'
        c['edges'] = e
    return CO


# 主要人物の深掘り(adds_deep.py)を、patch・careerに足す
from adds_deep import DEEP
for _k, _v in DEEP.items():
    _a = ADDS.setdefault(_k, dict(nodes=[], en={}, edges=''))
    _a.setdefault('patch', {}).update(_v.get('patch', {}))
    _a.setdefault('career', {}).update(_v.get('career', {}))
