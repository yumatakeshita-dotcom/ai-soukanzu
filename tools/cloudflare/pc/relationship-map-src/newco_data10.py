from newco_data import mk
from newco_data9 import P, O

# 注目スタートアップ(英語版Wikipediaの記載、2026年11月取得)。評価額は報道・Wikipediaの記載で、会社の発表で確認していないものを含みます。
STARTUPS = []   # [{key,name,min,note}]
CO10 = {}

NOTE_ST = '創業者・経営陣・出資者・出来事は、英語版Wikipedia(2026年11月取得)の記載に基づきます。評価額と調達額は、報道やWikipediaの記載で、会社の発表で確認していないものを含みます。顔写真がない人はイニシャル表示です。'

def st(key, name, minyear, note, items, edges, desc):
    N = [{'id': 'co', 'name': name, 'kind': 'c', 'from': minyear, 'desc': desc}]
    EN = {}
    E = "const E = [];\nN.forEach(n=>{ if(n.kind==='p') E.push({a:n.id,b:'co',k:'member'}); if(n.kind==='i') E.push({a:n.id,b:'co',k:'invest'}); });\n"
    for node, en in items:
        N.append(node)
        if en:
            EN[node['id']] = en
    for e in edges:
        s = "E.push({a:'%s',b:'%s',k:'%s'" % (e[0], e[1], e[2])
        if len(e) > 3 and e[3]:
            s += ",label:'%s'" % e[3]
        if len(e) > 4 and e[4]:
            s += ",since:%d" % e[4]
        E += s + "});\n"
    CO10[key] = mk(N, E, EN, {}, {}, {}, {}, {}, 'co')
    STARTUPS.append({'key': key, 'name': name, 'min': minyear, 'note': NOTE_ST + note})

# ---- Ramp ----
st('st_ramp', 'Ramp', 2019, '評価額は、2025年6月の160億ドルから2026年6月の440億ドル(7.5億ドルの調達)へ上がったとWikipediaに載っています。', [
  P('glyman', 'エリック・グリマン', 'Eric Glyman', 2019, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('atiyeh', 'カリム・アティエ', 'Karim Atiyeh', 2019, '共同創業者でCTO。', '共同創業者 / CTO', None, 1),
  P('glee', 'ジーン・リー', 'Gene Lee', 2019, '共同創業者。', '共同創業者', None, 1),
  O('foundersfund', 'Founders Fund', 2020, 'シリーズAを主導。', '出資者(シリーズA)', 'i'),
  O('lightspeed', 'Lightspeed Venture Partners', 2025, '2025年11月の調達を主導。', '出資者(2025年)', 'i'),
  O('bessemer', 'Bessemer Venture Partners', 2021, '出資者。', '出資者', 'i'),
  O('iconiq', 'ICONIQ Growth', 2026, '2026年6月の7.5億ドルの調達を主導(GIC、オンタリオ教員年金とともに)。', '出資者(2026年)', 'i'),
  O('procurement', '調達管理の事業', 2023, '2023年8月に購買依頼・取引先管理へ拡大。', '事業拡大(2023年)'),
 ],
 [('glyman', 'atiyeh', 'link', '共同創業'), ('glyman', 'glee', 'link', '共同創業')],
 '2019年に創業された法人カード・支出管理の会社(ニューヨーク)。エリック・グリマンがCEOを務めています。')

# ---- Anduril ----
st('st_anduril', 'Anduril', 2017, '2026年5月の50億ドルの調達(評価額約610億ドル)は、Wikipediaの記載に基づきます。', [
  P('luckey', 'パーマー・ラッキー', 'Palmer Luckey', 2017, '共同創業者。Oculusの創業者。', '共同創業者', None, 1),
  P('stephens', 'トレイ・スティーブンス', 'Trae Stephens', 2017, '共同創業者で会長。', '共同創業者 / 会長', None, 1),
  P('schimpf', 'ブライアン・シンプフ', 'Brian Schimpf', 2017, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('grimm', 'マット・グリム', 'Matt Grimm', 2017, '共同創業者。', '共同創業者', None, 1),
  P('chen', 'ジョー・チェン', 'Joe Chen', 2017, '共同創業者。', '共同創業者', None, 1),
  O('foundersfund', 'Founders Fund', 2017, '主要な出資者。', '出資者', 'i'),
  O('gc', 'General Catalyst', 2018, '出資者。', '出資者', 'i'),
  O('a16z', 'Andreessen Horowitz', 2019, '出資者。', '出資者', 'i'),
  O('d1', 'D1 Capital Partners', 2021, '出資者。', '出資者', 'i'),
  O('areai', 'Area-I', 2021, '2021年に買収。', '買収(2021年)'),
  O('dive', 'Dive Technologies', 2022, '2022年に買収。', '買収(2022年)'),
  O('blueforce', 'Blue Force Technologies', 2023, '2023年に買収。', '買収(2023年)'),
  O('numerica', 'Numericaのレーダー・指揮統制事業', 2024, '2024年に買収。', '買収(2024年)'),
  O('arsenal', 'Arsenal-1(オハイオ州の工場)', 2025, '2025年1月に発表した製造拠点。', '拠点(2025年)'),
 ],
 [('luckey', 'stephens', 'link', '共同創業'), ('luckey', 'schimpf', 'link', '共同創業'), ('luckey', 'grimm', 'link', '共同創業'), ('luckey', 'chen', 'link', '共同創業'), ('co', 'areai', 'owns'), ('co', 'dive', 'owns'), ('co', 'blueforce', 'owns'), ('co', 'numerica', 'owns'), ('co', 'arsenal', 'owns')],
 '2017年にパーマー・ラッキーらが創業した防衛技術の会社(カリフォルニア州)。ブライアン・シンプフがCEOを務めています。')

# ---- Cognition ----
st('st_cognition', 'Cognition', 2023, '評価額は、2025年9月の100億ドルから2026年5月の260億ドルへ。2026年8月に400億ドル超の協議とBloombergが報じた、とWikipediaに載っています。', [
  P('wu', 'スコット・ウー', 'Scott Wu', 2023, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('hao', 'スティーブン・ハオ', 'Steven Hao', 2023, '共同創業者でCTO。', '共同創業者 / CTO', None, 1),
  P('yan', 'ウォルデン・ヤン', 'Walden Yan', 2023, '共同創業者で最高プロダクト責任者。', '共同創業者 / CPO', None, 1),
  O('foundersfund', 'Founders Fund', 2024, '2024年に2,100万ドルを出資し、1.75億ドルの調達(評価額20億ドル)を主導。', '出資者(2024年)', 'i'),
  O('8vc', '8VC', 2025, '2025年3月の調達を主導(ジョー・ロンズデール氏)。', '出資者(2025年)', 'i'),
  O('windsurf', 'Windsurf', 2025, '2025年7月に買収に合意(AIのIDE)。', '買収(2025年)'),
  O('devin', 'Devin', 2024, '2024年3月に公開したAIソフトウェア開発者。', '主力製品(2024年)'),
 ],
 [('wu', 'hao', 'link', '共同創業'), ('wu', 'yan', 'link', '共同創業'), ('co', 'windsurf', 'owns'), ('co', 'devin', 'owns')],
 '2023年にスコット・ウーらが創業した、AIソフトウェア開発者「Devin」の会社(サンフランシスコ)。')

# ---- Lovable ----
st('st_lovable', 'Lovable', 2023, '調達の数字は、Wikipediaの記載に基づきます。', [
  P('osika', 'アントン・オシカ', 'Anton Osika', 2023, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('hedin', 'ファビアン・ヘディン', 'Fabian Hedin', 2023, '共同創業者でCTO。', '共同創業者 / CTO', None, 1),
  O('accel', 'Accel', 2025, '2025年2月のシリーズA(2億ドル、評価額18億ドル)を主導。', '出資者(2025年)', 'i'),
  O('capitalg', 'CapitalG', 2025, '2025年12月のシリーズB(3.3億ドル、評価額66億ドル)を主導。', '出資者(2025年)', 'i'),
  O('menlo', 'Menlo Ventures', 2025, '2025年12月と2026年8月の調達を主導。', '出資者(2025〜2026年)', 'i'),
  O('khosla', 'Khosla Ventures', 2025, '出資者。', '出資者', 'i'),
  O('salesforcev', 'Salesforce Ventures', 2025, '出資者。', '出資者', 'i'),
  O('supabase', 'Supabase', 2025, '2025年3月、Lovableで作ったサイトのSupabaseの設定不備による脆弱性が見つかった。', '関連(脆弱性)'),
 ],
 [('osika', 'hedin', 'link', '共同創業'), ('co', 'supabase', 'link', '連携')],
 '2023年にスウェーデンのストックホルムで創業された、AIでアプリを作るサービスの会社。2026年8月に評価額133億ドルのシリーズCを調達しました(Wikipedia)。')

# ---- Harvey ----
st('st_harvey', 'Harvey', 2022, '評価額155億ドル(2026年9月)は、Wikipediaの記載に基づきます。', [
  P('weinberg', 'ウィンストン・ワインバーグ', 'Winston Weinberg', 2022, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('pereyra', 'ガブリエル・ペレイラ', 'Gabriel Pereyra', 2022, '共同創業者で社長。', '共同創業者 / 社長', None, 1),
  P('moodie', 'ゴードン・ムーディ', 'Gordon Moodie', 2023, '最高プロダクト責任者(2023年7月から)。', 'CPO'),
  O('openai', 'OpenAI', 2022, '2022年11月の500万ドルのシード(OpenAI Startup Fund)を主導。', 'シードの出資者(2022年)', 'i'),
  O('sequoia', 'Sequoia Capital', 2023, '出資者。', '出資者', 'i'),
  O('kleiner', 'Kleiner Perkins', 2023, '出資者。', '出資者', 'i'),
  O('gv', 'GV', 2023, '出資者。', '出資者', 'i'),
  O('lightspeed', 'Lightspeed Venture Partners', 2026, '2026年9月の調達を共同で主導。', '出資者(2026年)', 'i'),
  O('allenovery', 'Allen & Overy', 2022, '2022年11月に試験導入した法律事務所。', '初期の顧客'),
  O('paulweiss', 'Paul Weiss', 2023, '2023年1月に試験導入した法律事務所。', '初期の顧客'),
 ],
 [('weinberg', 'pereyra', 'link', '共同創業'), ('co', 'allenovery', 'link', '導入'), ('co', 'paulweiss', 'link', '導入')],
 '2022年に創業された、法律業務向けのAIの会社。OpenAIがシードを主導したことで知られます。')

# ---- ElevenLabs ----
st('st_elevenlabs', 'ElevenLabs', 2022, '評価額は、2026年2月に110億ドル(5億ドルの調達)、2026年9月の従業員株売却で220億ドルと報じられた、とWikipediaに載っています。', [
  P('staniszewski', 'マティ・スタニシェフスキ', 'Mati Staniszewski', 2022, '共同創業者でCEO。元Palantir。', '共同創業者 / CEO', None, 1),
  P('dabkowski', 'ピオトル・ドンブコフスキ', 'Piotr Dabkowski', 2022, '共同創業者でCTO。元Google。', '共同創業者 / CTO', None, 1),
  O('credo', 'Credo Ventures', 2023, '2023年1月のプレシード(200万ドル)を主導。', '出資者(2023年)', 'i'),
  O('a16z', 'Andreessen Horowitz', 2023, '2023年6月のシリーズAなどを共同で主導。', '出資者', 'i'),
  O('sequoia', 'Sequoia Capital', 2024, '2024年1月のシリーズB(8,000万ドル、評価額11億ドル)を共同で主導。', '出資者(2024年)', 'i'),
  O('iconiq', 'ICONIQ Growth', 2025, '2025年1月のシリーズC(1.8億ドル)を共同で主導。', '出資者(2025年)', 'i'),
  O('voice', '音声復元の取り組み', 2026, '2026年3月に、100万人の声を失った人へ10億ドル相当の技術を無償提供と発表。', '取り組み(2026年)'),
 ],
 [('staniszewski', 'dabkowski', 'link', '共同創業')],
 '2022年に創業された、AI音声合成の会社(拠点はロンドン、ニューヨーク、ワルシャワ、サンフランシスコ)。')

# ---- Figure AI ----
st('st_figure', 'Figure AI', 2022, '評価額390億ドル(2025年9月)は、Wikipediaの記載に基づきます。', [
  P('adcock', 'ブレット・アドコック', 'Brett Adcock', 2022, '創業者。Archer Aviation、Vettery、Harkの創業者でもあります。', '創業者', None, 1),
  O('bezos', 'ジェフ・ベゾス', 2024, '2024年2月の6.75億ドルの調達(評価額26億ドル)の出資者。', '出資者(2024年)', 'i'),
  O('microsoft', 'Microsoft', 2024, '2024年2月の調達の出資者。', '出資者(2024年)', 'i'),
  O('nvidia', 'Nvidia', 2024, '2024年2月の調達の出資者。2026年9月に35億ドルのGPU調達も約束と記載。', '出資者・取引先', 'i'),
  O('brookfield', 'Brookfield', 2025, '2025年9月の10億ドル超の調達の出資者。', '出資者(2025年)', 'i'),
  O('intel', 'Intel', 2025, '2025年9月の調達の出資者。', '出資者(2025年)', 'i'),
  O('qualcomm', 'Qualcomm', 2025, '2025年9月の調達の出資者。', '出資者(2025年)', 'i'),
  O('salesforce', 'Salesforce', 2025, '2025年9月の調達の出資者。', '出資者(2025年)', 'i'),
  O('tmobile', 'T-Mobile', 2025, '2025年9月の調達の出資者。', '出資者(2025年)', 'i'),
  O('bmw', 'BMW', 2024, '2024年1月に提携を発表。', '提携先(2024年)'),
  O('openai', 'OpenAI', 2024, '提携していたが、約1年で終了。', '元の提携先'),
 ],
 [('co', 'bmw', 'link', '提携'), ('co', 'openai', 'conflict', '提携を終了')],
 '2022年にブレット・アドコックが創業した、人型ロボットの会社(カリフォルニア州サンノゼ)。')

# ---- Mercor ----
st('st_mercor', 'Mercor', 2023, '評価額100億ドル(2025年10月のシリーズC、3.5億ドル)は、Wikipediaの記載に基づきます。2026年3月のデータ流出の報道は、報道に基づきます。', [
  P('foody', 'ブレンダン・フーディ', 'Brendan Foody', 2023, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('midha', 'スーリヤ・ミダ', 'Surya Midha', 2023, '共同創業者で会長。', '共同創業者 / 会長', None, 1),
  P('hiremath', 'アダルシュ・ヒレマス', 'Adarsh Hiremath', 2023, '共同創業者でCTO。', '共同創業者 / CTO', None, 1),
  P('jain', 'サンディープ・ジェイン', 'Sundeep Jain', 2025, '初の社長(2025年5月から)。Uberの元最高プロダクト責任者。', '社長'),
  O('deeptune', 'Deeptune', 2026, '2026年7月に買収したAIシミュレーションのスタートアップ。', '買収(2026年)'),
  O('litellm', 'LiteLLMへの攻撃', 2026, '2026年3月、供給網への攻撃で最大4TBのデータが漏れた可能性が報じられ、集団訴訟に発展。', '事案(2026年・報道)'),
 ],
 [('foody', 'midha', 'link', '共同創業'), ('foody', 'hiremath', 'link', '共同創業'), ('co', 'deeptune', 'owns')],
 '2023年に創業された、AI向けの人材・データのマーケットプレイス(サンフランシスコ)。')

# ---- Cerebras ----
st('st_cerebras', 'Cerebras', 2015, '2026年5月のNasdaq上場(ティッカーCBRS、555億ドルの調達、評価額約950億ドル)と、OpenAIとの契約は、Wikipediaの記載に基づきます。', [
  P('feldman', 'アンドリュー・フェルドマン', 'Andrew Feldman', 2015, '共同創業者でCEO。SeaMicroの元幹部。', '共同創業者 / CEO', None, 1),
  P('lauterbach', 'ゲイリー・ラウターバック', 'Gary Lauterbach', 2015, '共同創業者。', '共同創業者', None, 1),
  P('james', 'マイケル・ジェームズ', 'Michael James', 2015, '共同創業者。', '共同創業者', None, 1),
  P('lie', 'ショーン・リー', 'Sean Lie', 2015, '共同創業者でCTO。', '共同創業者 / CTO', None, 1),
  P('fricker', 'ジャン＝フィリップ・フリッカー', 'Jean-Philippe Fricker', 2015, '共同創業者。', '共同創業者', None, 1),
  P('komin', 'ロバート・コミン', 'Robert Komin', 2015, 'CFO。', 'CFO'),
  P('mallick', 'ディラジ・マリック', 'Dhiraj Mallick', 2018, 'COO。', 'COO'),
  O('benchmark', 'Benchmark', 2016, '出資者。', '出資者', 'i'),
  O('foundation', 'Foundation Capital', 2016, '出資者。', '出資者', 'i'),
  O('g42', 'G42', 2023, '出資者(アブダビ)。', '出資者', 'i'),
  O('openai', 'OpenAI', 2026, '2026年1月に、2028年までに750MWの計算能力を提供する契約(約100億ドルと報じられています)。ワラントを保有。', '顧客・ワラント保有(2026年)'),
  O('aws', 'Amazon Web Services', 2026, '2026年3月に、Trainium搭載サーバー向けにCS-3の購入に合意。', '顧客(2026年)'),
  O('ipo', 'Nasdaq上場', 2026, '2026年5月14日にティッカーCBRSで上場。1株185ドル。', '上場(2026年)'),
 ],
 [('feldman', 'lauterbach', 'link', '共同創業'), ('feldman', 'james', 'link', '共同創業'), ('feldman', 'lie', 'link', '共同創業'), ('feldman', 'fricker', 'link', '共同創業'), ('co', 'openai', 'link', '大型契約'), ('co', 'aws', 'link', '提携'), ('co', 'ipo', 'owns')],
 '2015年にアンドリュー・フェルドマンらが創業した、ウェハー規模のAIチップの会社。2026年5月にNasdaqへ上場しました。')

# ---- Groq ----
st('st_groq', 'Groq', 2016, 'Nvidiaとの約200億ドルの契約(2025年12月)は、Wikipediaに「報じられた」と書かれたものです。', [
  P('ross', 'ジョナサン・ロス', 'Jonathan Ross', 2016, '創業者でCEO。元Googleのエンジニア(TPUの設計に参加)。2025年12月のNvidiaとの契約で移籍と記載。', '創業者 / CEO', None, 1),
  P('wightman', 'ダグラス・ワイトマン', 'Douglas Wightman', 2016, '初代CEO。', '元CEO', 2017),
  P('madra', 'サニー・マドラ', 'Sunny Madra', 2020, 'COO。', 'COO'),
  O('social', 'Social Capital', 2017, 'チャマス・パリハピティヤ氏が2017年に1,000万ドルを出資。', '出資者(2017年)', 'i'),
  O('tiger', 'Tiger Global', 2021, '2021年のシリーズC(3億ドル)を主導。', '出資者(2021年)', 'i'),
  O('blackrockpe', 'BlackRock Private Equity Partners', 2024, '2024年8月のシリーズD(6.4億ドル、評価額28億ドル)を主導。', '出資者(2024年)', 'i'),
  O('saudi', 'サウジアラビア', 2025, '2025年2月に、ダンマーム(サウジ)のデータセンターに15億ドルを約束と発表。', '提携(2025年)'),
  O('nvidia', 'Nvidia', 2025, '2025年12月に、技術のライセンスと幹部の採用の契約を発表(約200億ドルと報じられています)。Groqは独立を維持と説明。', '契約(2025年・報道)'),
 ],
 [('wightman', 'ross', 'link', '後任'), ('ross', 'madra', 'link', '共同で経営'), ('ross', 'nvidia', 'moved', '移籍(報道)', 2025), ('madra', 'nvidia', 'moved', '移籍(報道)', 2025), ('co', 'saudi', 'link', '提携'), ('co', 'nvidia', 'link', 'ライセンス契約', 2025)],
 '2016年にジョナサン・ロス氏らが創業した、AI推論用チップの会社。2025年12月にNvidiaと大型契約を発表しました。')

# ---- Replit ----
st('st_replit', 'Replit', 2016, '現在のCEOや主要な出資者は、Wikipediaに載っていないため、載せていません。', [
  P('amjad', 'アムジャド・マサド', 'Amjad Masad', 2016, '共同創業者。', '共同創業者', None, 1),
  P('faris', 'ファリス・マサド', 'Faris Masad', 2016, '共同創業者。', '共同創業者', None, 1),
  P('odeh', 'ハヤ・オデー', 'Haya Odeh', 2016, '共同創業者でデザイナー。', '共同創業者', None, 1),
  O('agent', 'Replit Agent', 2024, '2024年9月に公開したAIエージェント。', '製品(2024年)'),
  O('microsoft', 'Microsoft', 2025, '2025年7月に提携(Azure Marketplaceで提供)。', '提携先(2025年)'),
  O('dbincident', 'データベース削除の事案', 2025, '2025年7月、AIエージェントがコード凍結中の顧客のデータベースを消した事案。', '事案(2025年)'),
 ],
 [('amjad', 'faris', 'link', '共同創業'), ('amjad', 'odeh', 'link', '共同創業'), ('co', 'agent', 'owns'), ('co', 'microsoft', 'link', '提携'), ('co', 'dbincident', 'link', '事案')],
 '2016年に創業された、ブラウザ上で開発できるサービスの会社(旧Repl.it)。')

# ---- Runway ----
st('st_runway', 'Runway', 2018, '評価額53億ドル(2026年2月の3.15億ドルの調達)は、Wikipediaの記載に基づきます。', [
  P('valenzuela', 'クリストバル・バレンズエラ', 'Cristobal Valenzuela', 2018, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('germanidis', 'アナスタシス・ジェルマニディス', 'Anastasis Germanidis', 2018, '共同創業者でCTO。', '共同創業者 / CTO', None, 1),
  P('matamala', 'アレハンドロ・マタマラ', 'Alejandro Matamala', 2018, '共同創業者で最高デザイン責任者。', '共同創業者', None, 1),
  O('google', 'Google', 2023, '2023年の拡大調達の出資者。', '出資者(2023年)', 'i'),
  O('nvidia', 'Nvidia', 2023, '2023年の拡大調達の出資者。', '出資者(2023年)', 'i'),
  O('salesforce', 'Salesforce', 2023, '2023年の拡大調達の出資者。', '出資者(2023年)', 'i'),
  O('generalatlantic', 'General Atlantic', 2025, '2025年4月の調達を主導。', '出資者(2025年)', 'i'),
  O('stablediffusion', 'Stable Diffusion', 2022, '2022年8月に、ミュンヘン大学のCompViz Groupとオープンソースの画像モデルを共同公開。', '成果(2022年)'),
  O('lionsgate', 'Lionsgate', 2024, '2024年9月に提携。', '提携先(2024年)'),
 ],
 [('valenzuela', 'germanidis', 'link', '共同創業'), ('valenzuela', 'matamala', 'link', '共同創業'), ('co', 'stablediffusion', 'owns'), ('co', 'lionsgate', 'link', '提携')],
 '2018年にニューヨーク大学の仲間が創業した、動画生成AIの会社。')

# ---- Midjourney ----
st('st_midjourney', 'Midjourney', 2022, '主要な出資者や創業年は、Wikipediaに載っていないため、載せていません。', [
  P('holz', 'デビッド・ホルツ', 'David Holz', 2022, '創業者。Leap Motionの共同創業者。', '創業者', None, 1),
  O('discord', 'Discord', 2022, '2022年3月にDiscordサーバーで開始、7月にオープンβ。', '提供の場(2022年)'),
  O('coloradofair', 'コロラド州フェアの受賞', 2022, '2022年、生成画像「Theatre D\'opera Spatial」がデジタルアート部門で1位。', '出来事(2022年)'),
  O('disneysuit', 'ディズニー・ユニバーサルの提訴', 2025, '2025年6月に提訴。ワーナー・ブラザース・ディスカバリーも2025年9月に提訴。', '訴訟(2025年)'),
 ],
 [('co', 'discord', 'link', '利用の場'), ('co', 'disneysuit', 'link', '提訴された')],
 '画像生成AIのMidjourney。創業者のデビッド・ホルツがチームを率い、2022年7月にオープンβを始めました。')

# ---- Character.AI ----
st('st_characterai', 'Character.AI', 2021, '2026年10月の破産申請とディズニーへの売却(2,000万ドル)は、英語版Wikipediaに載っていた内容で、確認は十分ではありません。', [
  P('shazeer', 'ノーム・シェイザー', 'Noam Shazeer', 2021, '共同創業者。「Attention Is All You Need」の共著者。2024年にGoogleに移籍。', '共同創業者', 2024, 1),
  P('defreitas', 'ダニエル・デ・フレイタス', 'Daniel de Freitas', 2021, '共同創業者。元Google。', '共同創業者', 2024, 1),
  P('anand', 'カランディープ・アナンド', 'Karandeep Anand', 2025, '現CEO(Wikipediaの囲み記事の記載)。', 'CEO'),
  O('a16z', 'Andreessen Horowitz', 2023, '2023年3月の1.5億ドル(評価額約10億ドル)の調達の出資者とされる。', '出資者(2023年)', 'i'),
  O('google', 'Google', 2024, '2024年にシェイザー氏を採用し、技術を利用する非独占契約を結んだ。', '契約先(2024年)'),
  O('settlement', 'Googleとの訴訟の和解', 2026, '2026年1月に、未成年の自殺をめぐる訴訟で和解。', '和解(2026年)'),
  O('disney', 'Disney', 2026, '2026年10月に、連邦破産法11条を申請し、ディズニーへ資産を2,000万ドルで売却すると記載。', '売却先(2026年)'),
 ],
 [('shazeer', 'defreitas', 'link', '共同創業'), ('shazeer', 'google', 'moved', 'Googleに移籍', 2024), ('co', 'google', 'link', '技術契約', 2024), ('co', 'disney', 'link', '資産の売却'), ('co', 'settlement', 'link', '和解')],
 '2021年にノーム・シェイザーらが創業した、AIキャラクターとの会話サービス。2026年10月に連邦破産法11条を申請したとWikipediaに載っています。')

# ---- Suno ----
st('st_suno', 'Suno', 2022, '創業年と主要な出資者は、Wikipediaに載っていないため、載せていません。', [
  P('shulman', 'ミッキー・シュルマン', 'Mikey Shulman', 2022, '共同創業者。CEOとして発言(2025年1月)。', '共同創業者 / CEO', None, 1),
  P('kucsko', 'ゲオルグ・クチュコ', 'Georg Kucsko', 2022, '共同創業者。', '共同創業者', None, 1),
  P('camacho', 'マーティン・カマチョ', 'Martin Camacho', 2022, '共同創業者。', '共同創業者', None, 1),
  P('freyberg', 'キーナン・フレイバーグ', 'Keenan Freyberg', 2022, '共同創業者。', '共同創業者', None, 1),
  P('brody', 'ジャック・ブロディ', 'Jack Brody', 2023, '最高プロダクト責任者。', 'CPO'),
  O('wmg', 'Warner Music Group', 2025, '2025年11月に和解とライセンス契約。', '和解・提携(2025年)'),
  O('bmg', 'BMG', 2026, '2026年8月にライセンス契約。', 'ライセンス(2026年)'),
  O('riaa', '米レコード協会(RIAA)ほか', 2024, '2024年6月に提訴。2026年9月にはUMGとSonyも提訴。', '訴訟(2024〜2026年)'),
 ],
 [('shulman', 'kucsko', 'link', '共同創業'), ('shulman', 'camacho', 'link', '共同創業'), ('shulman', 'freyberg', 'link', '共同創業'), ('co', 'wmg', 'link', '和解・提携'), ('co', 'riaa', 'conflict', '提訴された')],
 '2023年12月に広く公開された、AI作曲サービス(マサチューセッツ州ケンブリッジ)。創業者はKensho出身です。')

# ---- Black Forest Labs ----
st('st_bfl', 'Black Forest Labs', 2024, '社長・CEOの記載はWikipediaにありません。', [
  P('rombach', 'ロビン・ロンバッハ', 'Robin Rombach', 2024, '共同創業者。元Stability AI。', '共同創業者', None, 1),
  P('blattmann', 'アンドレアス・ブラットマン', 'Andreas Blattmann', 2024, '共同創業者。元Stability AI。', '共同創業者', None, 1),
  P('esser', 'パトリック・エッサー', 'Patrick Esser', 2024, '共同創業者。元Stability AI。', '共同創業者', None, 1),
  P('scorsese', 'マーティン・スコセッシ', 'Martin Scorsese', 2026, '2026年6月にアドバイザーに就任した映画監督。', 'アドバイザー'),
  O('a16z', 'Andreessen Horowitz', 2024, '初期の出資者(初期の調達は3,100万ドル)。', '出資者(2024年)', 'i'),
  O('salesforcev', 'Salesforce Ventures', 2025, '2025年の調達の出資者(約4.5億ドルの申し出)。', '出資者(2025年)', 'i'),
  O('adobe', 'Adobe', 2025, '2025年の調達の出資者。', '出資者(2025年)', 'i'),
  O('canva', 'Canva', 2025, '2025年の調達の出資者。', '出資者(2025年)', 'i'),
  O('flux', 'FLUX', 2024, '2024年8月にFlux.1を公開。2025年11月にFlux.2、2026年7月にFlux.3シリーズを発表。', '主力モデル'),
  O('stability', 'Stability AI', 2022, '創業者3人の前職。', '創業者の前職'),
 ],
 [('rombach', 'blattmann', 'link', '共同創業'), ('rombach', 'esser', 'link', '共同創業'), ('rombach', 'stability', 'moved', '前職'), ('co', 'flux', 'owns')],
 '2024年にドイツのフライブルクで創業された、画像生成AI「FLUX」の会社。')

# ---- Vercel ----
st('st_vercel', 'Vercel', 2015, '2026年4月のセキュリティ事案は、Wikipediaの記載に基づきます。', [
  P('rauch', 'ギジェルモ・ラウフ', 'Guillermo Rauch', 2015, '創業者でCEO。Next.jsの作者。', '創業者 / CEO', None, 1),
  P('hashimoto', 'ミッチェル・ハシモト', 'Mitchell Hashimoto', 2026, '2026年3月に取締役に就任。HashiCorpの共同創業者。', '取締役'),
  O('accel', 'Accel', 2025, '2025年9月のシリーズF(3億ドル、評価額93億ドル)を共同で主導。', '出資者(2025年)', 'i'),
  O('gic', 'GIC', 2025, '2025年9月のシリーズFを共同で主導。', '出資者(2025年)', 'i'),
  O('nextjs', 'Next.js', 2016, '同社が作ったウェブのフレームワーク。', '主力製品'),
  O('v0', 'v0', 2023, 'AIでウェブを作るツール。', '製品'),
  O('breach', 'セキュリティ事案', 2026, '2026年4月19日に公表。外部のAIツールContext.aiの侵害が関連。', '事案(2026年)'),
  O('tremor', 'Tremor', 2025, '2025年に買収。', '買収(2025年)'),
  O('nuxtlabs', 'NuxtLabs', 2025, '2025年に買収。', '買収(2025年)'),
 ],
 [('rauch', 'hashimoto', 'link', '取締役に迎える', 2026), ('co', 'nextjs', 'owns'), ('co', 'v0', 'owns'), ('co', 'breach', 'link', '事案'), ('co', 'tremor', 'owns'), ('co', 'nuxtlabs', 'owns')],
 '2015年にギジェルモ・ラウフが創業した、ウェブ開発基盤の会社(旧ZEIT、2020年にVercelへ改称)。')

# ---- Deel ----
st('st_deel', 'Deel', 2019, 'リップリングとの訴訟(2025年)と米司法省の捜査(2026年1月)は、Wikipediaの記載に基づく内容です。Deelは不正を否定しています。', [
  P('bouaziz', 'アレックス・ブアジズ', 'Alex Bouaziz', 2019, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('wang', 'シュオ・ワン', 'Shuo Wang', 2019, '共同創業者で最高収益責任者(CRO)。', '共同創業者 / CRO', None, 1),
  P('simon', 'オフェル・サイモン', 'Ofer Simon', 2019, '共同創業者。', '共同創業者', None, 1),
  P('westgarth', 'ダン・ウェストガース', 'Dan Westgarth', 2019, 'COO。', 'COO'),
  P('kauffman', 'ジョー・カウフマン', 'Joe Kauffman', 2025, '社長兼CFO(2025年11月から)。Intuitの元幹部。', '社長兼CFO'),
  O('a16z', 'Andreessen Horowitz', 2020, '2020年のシリーズA(1,400万ドル)を主導。2025年のシリーズEも共同で主導。', '出資者', 'i'),
  O('spark', 'Spark Capital', 2020, 'シリーズB(4,800万ドル)を主導。', '出資者(2020年)', 'i'),
  O('coatue', 'Coatue', 2021, '2021年のシリーズD(4.25億ドル)を主導。', '出資者(2021年)', 'i'),
  O('ribbit', 'Ribbit Capital', 2025, '2025年10月のシリーズE(3億ドル、評価額約173億ドル)を共同で主導。', '出資者(2025年)', 'i'),
  O('rippling', 'Rippling', 2025, '2025年3月に、Deelを企業スパイ行為で提訴(Deelは否定)。', '訴訟の相手(2025年)'),
  O('arsenal', 'Arsenal F.C.', 2026, '2026年5月に、袖スポンサーに。', 'スポンサー(2026年)'),
 ],
 [('bouaziz', 'wang', 'link', '共同創業'), ('bouaziz', 'simon', 'link', '共同創業'), ('co', 'rippling', 'conflict', '提訴された', 2025), ('co', 'arsenal', 'link', 'スポンサー')],
 '2019年にYコンビネーター出身で創業された、海外人材の雇用・給与の会社。アレックス・ブアジズがCEOを務めています。')

# ---- Revolut ----
st('st_revolut', 'Revolut', 2015, '各国の銀行免許(2026年)は、Wikipediaの記載に基づきます。', [
  P('storonsky', 'ニック・ストロンスキー', 'Nik Storonsky', 2015, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('yatsenko', 'ヴラド・ヤツェンコ', 'Vlad Yatsenko', 2015, '共同創業者(非業務執行取締役)。', '共同創業者', None, 1),
  P('gilbert', 'マーティン・ギルバート', 'Martin Gilbert', 2021, '会長。', '会長'),
  P('lucia', 'ドナート・ルチア', 'Donato Lucia', 2018, 'CTO。', 'CTO'),
  O('softbank', 'ソフトバンク', 2021, '2021年に出資(Vision Fund 2)。', '出資者(2021年)', 'i'),
  O('uk', '英国の銀行免許', 2026, '2026年3月11日に、完全な英国の銀行免許を取得。', '免許(2026年)'),
  O('mexico', 'メキシコの銀行業務', 2026, '2026年1月に、欧州外で初の銀行業務を開始。', '展開(2026年)'),
  O('us', '米国の銀行免許(条件付き)', 2026, '2026年9月に、条件付きの承認を取得。', '免許(2026年)'),
 ],
 [('storonsky', 'yatsenko', 'link', '共同創業'), ('storonsky', 'gilbert', 'link', '会長'), ('co', 'uk', 'link', '免許'), ('co', 'mexico', 'link', '展開'), ('co', 'us', 'link', '免許')],
 '2015年にロンドンで創業された、デジタル金融の会社。2025年の売上は45.2億ポンドとWikipediaに載っています。')

# ---- Klarna ----
st('st_klarna', 'Klarna', 2005, 'NYSE上場(2025年9月10日、1株40ドル)は、Wikipediaの記載に基づきます。', [
  P('siemiatkowski', 'セバスチャン・シェミアトコフスキ', 'Sebastian Siemiatkowski', 2005, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('adalberth', 'ニクラス・アダルベルト', 'Niklas Adalberth', 2005, '共同創業者。のちNorthvoltなどの出資者。', '共同創業者', None, 1),
  P('jacobsson', 'ヴィクター・ヤコブソン', 'Victor Jacobsson', 2005, '共同創業者。', '共同創業者', None, 1),
  P('moritz', 'マイケル・モリッツ', 'Michael Moritz', 2010, '会長。セコイア・キャピタルの元幹部で、2010年に出資。', '会長'),
  P('neglen', 'ニクラス・ネグレン', 'Niclas Neglen', 2020, 'CFO。2027年1月に退任予定。', 'CFO'),
  O('walerud', 'ジェーン・ワレルード', 2005, '初期の個人投資家(エンジェル)。', '初期の出資者', 'i'),
  O('sequoia', 'Sequoia Capital', 2010, '2010年に出資。', '出資者(2010年)', 'i'),
  O('ga', 'General Atlantic', 2011, '2011年に出資。', '出資者(2011年)', 'i'),
  O('ant', 'Ant Financial', 2020, '2020年に出資。', '出資者(2020年)', 'i'),
  O('vf2', 'SoftBank Vision Fund 2', 2021, '2021年に出資。', '出資者(2021年)', 'i'),
  O('ipo', 'NYSE上場', 2025, '2025年9月10日にティッカーKLARで上場。', '上場(2025年)'),
 ],
 [('siemiatkowski', 'adalberth', 'link', '共同創業'), ('siemiatkowski', 'jacobsson', 'link', '共同創業'), ('moritz', 'sequoia', 'moved', '前職'), ('co', 'ipo', 'owns')],
 '2005年にスウェーデンで創業された「後払い」の金融サービスの会社。2025年9月にNYSEへ上場しました。')

# ---- Discord ----
st('st_discord', 'Discord', 2015, '上場の準備(2026年1月)は、Bloombergの報道に基づくとWikipediaに載っています。', [
  P('citron', 'ジェイソン・シトロン', 'Jason Citron', 2015, '共同創業者。2025年4月にCEOを退き、取締役に。', '共同創業者', 2025, 1),
  P('vishnevskiy', 'スタニスラフ・ヴィシネフスキー', 'Stanislav Vishnevskiy', 2015, '共同創業者。', '共同創業者', None, 1),
  P('sakhnini', 'フマム・サクニーニ', 'Humam Sakhnini', 2025, '2025年4月からCEO。Activision Blizzardの元幹部。', 'CEO'),
  P('marcinkowski', 'トマシュ・マルチンコフスキ', 'Tomasz Marcinkowski', 2021, 'CFO(2021年3月から)。Pinterestの元財務責任者。', 'CFO'),
  O('benchmark', 'Benchmark', 2016, '初期の出資者。', '出資者', 'i'),
  O('tencent', 'Tencent', 2016, '初期の出資者。', '出資者', 'i'),
  O('warnermedia', 'WarnerMedia', 2016, '2016年に出資。', '出資者(2016年)', 'i'),
  O('greenoaks', 'Greenoaks Capital', 2018, '2018年の調達の出資者。', '出資者(2018年)', 'i'),
  O('sony', 'Sony Interactive Entertainment', 2021, '2021年に出資。', '出資者(2021年)', 'i'),
  O('ipo', '上場の準備', 2026, '2026年1月に、非公開で上場を申請したとBloombergが報道(ゴールドマン・サックス、JPモルガンが支援)。', '上場準備(2026年・報道)'),
 ],
 [('citron', 'vishnevskiy', 'link', '共同創業'), ('citron', 'sakhnini', 'link', 'CEOを交代', 2025), ('co', 'ipo', 'link', '上場準備', 2026)],
 '2015年にジェイソン・シトロンらが創業した、ゲーマー向けのチャットの会社。2025年4月からフマム・サクニーニがCEOを務めています。')

# ---- Plaid ----
st('st_plaid', 'Plaid', 2013, '2025年の調達(評価額61億ドル)と2026年2月の従業員株売却(80億ドル)は、Wikipediaの記載に基づきます。', [
  P('perret', 'ザック・ペレット', 'Zach Perret', 2013, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('hockey', 'ウィリアム・ホッキー', 'William Hockey', 2013, '共同創業者。', '共同創業者', 2021, 1),
  P('robinson', 'ウィル・ロビンソン', 'Will Robinson', 2014, 'CTO。', 'CTO'),
  O('spark', 'Spark Capital', 2014, '初期の出資者。', '出資者', 'i'),
  O('gv', 'GV', 2014, '出資者。', '出資者', 'i'),
  O('nea', 'NEA', 2014, '出資者。', '出資者', 'i'),
  O('a16z', 'Andreessen Horowitz', 2018, '出資者。', '出資者', 'i'),
  O('ribbit', 'Ribbit Capital', 2020, '出資者。', '出資者', 'i'),
  O('quovo', 'Quovo', 2019, '2019年1月に約2億ドルで買収。', '買収(2019年)'),
  O('visa', 'Visa', 2020, '2020年1月に約53億ドルでの買収を発表したが、米司法省の独占禁止法の提訴を受けて断念。', '買収断念(2021年)'),
  O('openai', 'OpenAI', 2026, '2026年5月に、ChatGPTと銀行口座をつなぐ提携。', '提携(2026年)'),
 ],
 [('perret', 'hockey', 'link', '共同創業'), ('co', 'quovo', 'owns'), ('visa', 'co', 'conflict', '買収を断念', 2021), ('co', 'openai', 'link', '提携')],
 '2013年にザック・ペレットらが創業した、銀行口座をアプリにつなぐ金融APIの会社。')

# Wikidataから作ったAI分野の会社(ai_wd_to_maps.py → ai_wd_maps.json)。
import newco_data10w
newco_data10w.load(st)
