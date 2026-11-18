from newco_data10 import st
from newco_data9 import P, O

# ---- Rippling ----
st('st_rippling', 'Rippling', 2017, '設立年は2016年とする記述もあります(Wikipedia)。Deelとの訴訟は互いに提訴し合っています。', [
  P('conrad', 'パーカー・コンラッド', 'Parker Conrad', 2017, '共同創業者でCEO。Zenefitsの共同創業者としても知られます。', '共同創業者 / CEO', None, 1),
  P('sankar', 'プラサンナ・サンカー', 'Prasanna Sankar', 2017, '共同創業者。', '共同創業者', None, 1),
  O('greenoaks', 'Greenoaks Capital', 2023, '2023年の調達の出資者。', '出資者(2023年)', 'i'),
  O('coatue', 'Coatue', 2024, '2024年の調達の出資者。', '出資者(2024年)', 'i'),
  O('gic', 'GIC', 2025, '2025年のシリーズGの出資者。', '出資者(2025年)', 'i'),
  O('baillie', 'Baillie Gifford', 2025, '2025年のシリーズGの出資者。', '出資者(2025年)', 'i'),
  O('svb', 'シリコンバレー銀行の破綻', 2023, '2023年、出金が止まった後に約5億ドルを調達し、取引銀行をJPモルガンへ移した。', '出来事(2023年)'),
  O('deel', 'Deel', 2025, '2025年3月に、企業スパイ行為でアイルランドの裁判所に提訴。Deelも米国で反訴。', '訴訟の相手(2025年)'),
 ],
 [('conrad', 'sankar', 'link', '共同創業'), ('co', 'deel', 'conflict', '提訴', 2025)],
 '2017年にパーカー・コンラッドらが創業した人事・IT・支出管理の会社(サンフランシスコ)。2025年5月のシリーズGは評価額168億ドルとWikipediaに載っています。')

# ---- OpenEvidence ----
st('st_openevidence', 'OpenEvidence', 2022, '評価額は2025年2月の10億ドルから2026年9月の150億ドルへ(Wikipediaの記載)。', [
  P('nadler', 'ダニエル・ナドラー', 'Daniel Nadler', 2022, '共同創業者でCEO。金融AIのKenshoの創業者としても知られます。', '共同創業者 / CEO', None, 1),
  P('ziegler', 'ザカリー・ジーグラー', 'Zachary Ziegler', 2022, '共同創業者。', '共同創業者', None, 1),
  O('sequoia', 'Sequoia Capital', 2025, '2025年2月のシリーズA(7,500万ドル、評価額10億ドル)を主導。', '出資者(2025年)', 'i'),
  O('gv', 'GV', 2025, '2025年7月の2.1億ドル(評価額35億ドル)を、Kleiner Perkinsとともに主導。', '出資者(2025年)', 'i'),
  O('kleiner', 'Kleiner Perkins', 2025, '2025年7月の調達を共同で主導。', '出資者(2025年)', 'i'),
  O('nvidia', 'Nvidia', 2025, '出資者。', '出資者', 'i'),
  O('thrive', 'Thrive Capital', 2025, '出資者。', '出資者', 'i'),
  O('blackstone', 'Blackstone', 2025, '出資者。', '出資者', 'i'),
  O('mayo', 'Mayo Clinic', 2025, '出資者。', '出資者', 'i'),
  O('cedars', 'Cedars-Sinai', 2026, '2026年5月に提携。', '提携先(2026年)'),
 ],
 [('nadler', 'ziegler', 'link', '共同創業'), ('co', 'cedars', 'link', '提携')],
 '2022年にマイアミで創業された、医師向けのAI検索の会社。ダニエル・ナドラーがCEOを務めています。')

# ---- Reflection AI ----
st('st_reflection', 'Reflection AI', 2024, 'CEOなどの役職は、Wikipediaに載っていないため、載せていません。', [
  P('laskin', 'ミシャ・ラスキン', 'Misha Laskin', 2024, '共同創業者。元Google DeepMind。', '共同創業者', None, 1),
  P('antonoglou', 'イオアニス・アントノグルー', 'Ioannis Antonoglou', 2024, '共同創業者。元Google DeepMind。', '共同創業者', None, 1),
  O('nvidia', 'Nvidia', 2025, '主要な出資者。', '出資者', 'i'),
  O('schmidt', 'エリック・シュミット', 2025, '元GoogleのCEO。出資者。', '出資者', 'i'),
  O('citi', 'Citigroup', 2025, '出資者。', '出資者', 'i'),
  O('lightspeed', 'Lightspeed Venture Partners', 2025, '出資者。', '出資者', 'i'),
  O('sequoia', 'Sequoia Capital', 2025, '出資者。', '出資者', 'i'),
  O('beam', 'Beam', 2026, '2026年10月に発表した初のLLM(5,010億パラメータ)。', '製品(2026年)'),
  O('shinsegae', 'Shinsegae', 2026, '2026年3月に、韓国で250MWのデータセンターの契約。', '提携先(2026年)'),
  O('spacex', 'SpaceX', 2026, '2026年6月に、計算資源の契約。', '契約先(2026年)'),
  O('deepmind', 'Google DeepMind', 2024, '創業者2人の前職。', '創業者の前職'),
 ],
 [('laskin', 'antonoglou', 'link', '共同創業'), ('laskin', 'deepmind', 'moved', '前職'), ('antonoglou', 'deepmind', 'moved', '前職'), ('co', 'beam', 'owns'), ('co', 'shinsegae', 'link', '提携'), ('co', 'spacex', 'link', '契約')],
 '2024年に元DeepMindの研究者が創業したAIの会社(ニューヨーク)。2025年10月に20億ドルを調達し(評価額80億ドル)、2026年6月には評価額250億ドルとWikipediaに載っています。')

# ---- Moonshot AI ----
st('st_moonshot', 'Moonshot AI', 2023, '評価額350億ドル(2026年7月)は、Wikipediaの記載に基づきます。Anthropicの指摘(2026年)は、同社側の主張として載っています。', [
  P('yang', 'ヤン・ジーリン', 'Yang Zhilin', 2023, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('zhou', 'ジョウ・シンユー', 'Zhou Xinyu', 2023, '共同創業者。', '共同創業者', None, 1),
  P('wu', 'ウー・ユーシン', 'Wu Yuxin', 2023, '共同創業者。', '共同創業者', None, 1),
  O('alibaba', 'Alibaba', 2024, '2024年2月の10億ドルの調達を主導。', '出資者(2024年)', 'i'),
  O('tencent', 'Tencent', 2024, '出資者。', '出資者', 'i'),
  O('kimi', 'Kimi', 2023, '2023年10月に公開したチャットボット。', '製品(2023年)'),
  O('k2', 'Kimi K2', 2025, '2025年7月に公開した1兆パラメータのオープンウェイトモデル。', '製品(2025年)'),
  O('k3', 'Kimi K3', 2026, '2026年7月に公開した2.8兆パラメータのモデル。', '製品(2026年)'),
  O('anthropic', 'Anthropic', 2026, '2026年2月にClaudeの蒸留、9月にClaudeへのリクエストの中継を、Moonshotに対して指摘。', '指摘した側(2026年)'),
 ],
 [('yang', 'zhou', 'link', '共同創業'), ('yang', 'wu', 'link', '共同創業'), ('co', 'kimi', 'owns'), ('co', 'k2', 'owns'), ('co', 'k3', 'owns'), ('co', 'anthropic', 'conflict', '指摘された', 2026)],
 '2023年に北京で創業された、AI「Kimi」の会社。ヤン・ジーリンがCEOを務め、AlibabaとTencentが出資しています。')

# ---- Zhipu AI ----
st('st_zhipu', 'Zhipu AI (Z.ai)', 2019, '香港上場(2026年1月8日、ティッカー2513)は、Wikipediaの記載に基づきます。', [
  P('tang', 'タン・ジエ', 'Tang Jie', 2019, '共同創業者(清華大学)。', '共同創業者', None, 1),
  P('li', 'リー・ジュアンジー', 'Li Juanzi', 2019, '共同創業者(清華大学)。', '共同創業者', None, 1),
  P('zhang', 'チャン・ポン', 'Zhang Peng', 2019, 'CEO。', 'CEO'),
  O('tsinghua', '清華大学', 2019, '2019年に清華大学から分離して設立。', '源流(2019年)'),
  O('alibaba', 'Alibaba', 2023, '2023年の調達の出資者。', '出資者(2023年)', 'i'),
  O('tencent', 'Tencent', 2023, '2023年の調達の出資者。', '出資者(2023年)', 'i'),
  O('meituan', 'Meituan', 2023, '2023年の調達の出資者。', '出資者(2023年)', 'i'),
  O('ant', 'Ant Group', 2023, '2023年の調達の出資者。', '出資者(2023年)', 'i'),
  O('xiaomi', 'Xiaomi', 2023, '2023年の調達の出資者。', '出資者(2023年)', 'i'),
  O('glm', 'GLM', 2021, 'オープンウェイトの大規模言語モデルのシリーズ。', '主力製品'),
  O('entity', '米商務省のエンティティリスト', 2025, '2025年1月に追加された。', '規制(2025年)'),
  O('hkipo', '香港証券取引所に上場', 2026, '2026年1月8日に上場(2513)。', '上場(2026年)'),
 ],
 [('tang', 'li', 'link', '共同創業'), ('tsinghua', 'tang', 'link', '源流'), ('co', 'glm', 'owns'), ('co', 'entity', 'link', '規制'), ('co', 'hkipo', 'owns')],
 '2019年に清華大学の研究者が創業した中国のAI企業(国際名Z.ai)。2026年1月に香港で上場しました。')

# ---- DeepSeek ----
st('st_deepseek', 'DeepSeek', 2023, '評価額と上場の見通し(2026年)は、Wikipediaに「報じられた」と書かれた内容です。Anthropicの指摘は、同社側の主張です。', [
  P('liang', 'リャン・ウェンフォン', 'Liang Wenfeng', 2023, '創業者でCEO。ヘッジファンドHigh-Flyerの創業者でもあります。', '創業者 / CEO', None, 1),
  O('highflyer', 'High-Flyer(幻方量化)', 2023, '2023年7月、AGI研究部門を分離して設立。出資・運営する中国のヘッジファンド。', '親会社・出資者', 'i'),
  O('r1', 'DeepSeek-R1', 2025, '2025年1月に公開。アプリが米国のApp Storeの無料1位になり、Nvidia株が1日で18%下落。', '製品(2025年)'),
  O('v32', 'V3.2', 2025, '2025年12月に公開。', '製品(2025年)'),
  O('v4', 'V4', 2026, '2026年4月24日にプレビュー、9月10日にV4.1-Flashを公開。', '製品(2026年)'),
  O('seriesa', 'シリーズA', 2026, '2026年5月に70億ドルを調達(評価額520億ドル)。7月には2027年にも上場の準備、評価額700億ドルの協議と報じられています。', '調達(2026年)'),
  O('anthropic', 'Anthropic', 2026, '2026年2月に、不正なアカウントでClaudeとの会話を学習に使ったと指摘。', '指摘した側(2026年)'),
  O('nvidia', 'Nvidia', 2025, 'R1の公開で株価が急落。', '影響を受けた会社'),
  O('ndaa', '米国防権限法の規制', 2026, '2026会計年度の法律で、国防・情報機関の端末からの削除を指示。', '規制'),
 ],
 [('liang', 'highflyer', 'link', '創業'), ('highflyer', 'co', 'owns', '分離して設立'), ('co', 'r1', 'owns'), ('co', 'v32', 'owns'), ('co', 'v4', 'owns'), ('co', 'seriesa', 'link', '調達'), ('co', 'anthropic', 'conflict', '指摘された', 2026), ('r1', 'nvidia', 'conflict', '株価が急落', 2025)],
 '2023年に中国のヘッジファンドHigh-Flyerの研究部門から分離して設立されたAI企業(杭州)。2025年1月のR1で世界の注目を集めました。')

# ---- CoreWeave ----
st('st_coreweave', 'CoreWeave', 2017, '2025年3月のNasdaq上場(CRWV)と各社との契約は、Wikipediaの記載に基づきます。', [
  P('intrator', 'マイケル・イントレーター', 'Michael Intrator', 2017, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('venturo', 'ブライアン・ベンチュロ', 'Brian Venturo', 2017, '共同創業者で最高戦略責任者。', '共同創業者 / CSO', None, 1),
  P('mcbee', 'ブラニン・マクビー', 'Brannin McBee', 2017, '共同創業者で最高事業開発責任者。', '共同創業者', None, 1),
  P('salanki', 'ピーター・サランキ', 'Peter Salanki', 2017, '共同創業者でCTO。', '共同創業者 / CTO', None, 1),
  P('agrawal', 'ニティン・アグラワル', 'Nitin Agrawal', 2024, 'CFO(2024年から)。', 'CFO'),
  O('atlantic', 'Atlantic Crypto', 2017, '2017年にニュージャージー州で設立された旧社名(2019年にCoreWeaveへ)。', '前身'),
  O('nvidia', 'Nvidia', 2023, '2023年に1億ドル、2026年1月に20億ドルを出資。', '出資者', 'i'),
  O('coatue', 'Coatue', 2024, '2024年5月の11億ドルの調達を主導。', '出資者(2024年)', 'i'),
  O('cisco', 'Cisco', 2024, '2024年の売り出しに参加。', '出資者(2024年)', 'i'),
  O('openai', 'OpenAI', 2025, '2025年3月に、約120億ドル(5年)の契約。', '顧客(2025年)'),
  O('anthropic', 'Anthropic', 2026, '2026年に、複数年のGPU契約。', '顧客(2026年)'),
  O('meta', 'Meta', 2026, '2026年4月に、210億ドルの拡大契約。', '顧客(2026年)'),
  O('wandb', 'Weights & Biases', 2025, '2025年に約17億ドルで買収。', '買収(2025年)'),
  O('corescientific', 'Core Scientific', 2025, '2025年10月に、約90億ドルの買収案が株主に否決された。', '買収断念(2025年)'),
 ],
 [('intrator', 'venturo', 'link', '共同創業'), ('intrator', 'mcbee', 'link', '共同創業'), ('intrator', 'salanki', 'link', '共同創業'), ('atlantic', 'co', 'owns', '改称'), ('co', 'openai', 'link', '大型契約'), ('co', 'anthropic', 'link', '契約'), ('co', 'meta', 'link', '契約'), ('co', 'wandb', 'owns'), ('co', 'corescientific', 'link', '買収断念')],
 'もとは暗号資産のマイニング会社で、AI向けGPUクラウドに転換した会社。2025年3月にNasdaqへ上場しました。')

# ---- Surge AI ----
st('st_surge', 'Surge AI', 2020, '評価額の数字は、報道を引用したWikipediaの記載で、確認は十分ではありません。', [
  P('chen', 'エドウィン・チェン', 'Edwin Chen', 2020, '創業者でCEO。約75%を保有(2025年9月)。', '創業者 / CEO(筆頭株主)', None, 1),
  O('a16z', 'Andreessen Horowitz', 2025, '2025年7月に出資の協議と報じられています。', '出資協議(2025年・報道)', 'i'),
  O('warburg', 'Warburg Pincus', 2025, '2025年7月に出資の協議と報じられています。', '出資協議(2025年・報道)', 'i'),
  O('tpg', 'TPG', 2025, '2025年7月に出資の協議と報じられています。', '出資協議(2025年・報道)', 'i'),
  O('classaction', '集団訴訟', 2025, '2025年5月に、作業者を個人事業主として扱ったことをめぐる集団訴訟。', '訴訟(2025年)'),
  O('leak', '内部文書の流出', 2025, '2025年7月に、学習・安全のガイドライン等の内部文書が流出。', '事案(2025年)'),
 ],
 [('co', 'classaction', 'link', '提訴された'), ('co', 'leak', 'link', '事案')],
 '2020年にエドウィン・チェンが創業した、AI向けのデータ作成の会社。外部からの出資を受けずに運営してきたとWikipediaに載っています。')
