from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Howmet Aerospace ----------------
deep('HWM', 'Howmet Aerospace', 1888, NOTE + '歴代の経営者の情報は少なく、確認できた範囲だけを載せています。', [
  P('hall', 'チャールズ・マーティン・ホール', 'Charles Martin Hall', 1888, 'アルミ製錬法の発明者。1888年にPittsburgh Reduction Company(のちAlcoa)を創業。', '源流の創業者', 1914, 1),
  P('kleinfeld', 'クラウス・クラインフェルド', 'Klaus Kleinfeld', 2008, 'Alcoa、のちArconicのCEO(2008〜2017年)。', '元CEO', 2017),
  P('plant', 'ジョン・プラント', 'John Plant', 2017, '2017年からCEO(2020年のHowmet分離後も、会長兼CEO)。', '会長兼CEO'),
  O('alcoa', 'Alcoa', 1888, '源流の会社。2016年に分割してArconicに。', '源流'),
  O('arconic', 'Arconic', 2016, '2016年にAlcoaから分割。2020年にHowmetとArconicに再分割。', '前身(2016年)'),
  O('firth', 'Firth Rixson', 2014, '2014年に約28億ドルで買収。', '買収(2014年)'),
  O('rti', 'RTI International Metals', 2015, '2015年に約15億ドルで買収。', '買収(2015年)'),
  O('cam', 'Consolidated Aerospace Manufacturing', 2025, '2025年に約18億ドルで買収と報じられています。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '6.6', M), ('State Street', '6.1', M), ('BlackRock', '5.7', M)]),
 [('hall', 'alcoa', 'link', '創業'), ('kleinfeld', 'plant', 'link', '後任'), ('co', 'alcoa', 'owns'), ('co', 'arconic', 'owns'), ('co', 'firth', 'owns'), ('co', 'rti', 'owns'), ('co', 'cam', 'owns')],
 '1888年のAlcoaを源流とする航空機エンジン部品の会社。ジョン・プラントが会長兼CEOを務めています。')

# ---------------- Northrop Grumman ----------------
deep('NOC', 'Northrop Grumman', 1994, NOTE, [
  P('jnorthrop', 'ジャック・ノースロップ', 'Jack Northrop', 1939, '1939年にNorthrop Corporationを創業。', '源流の創業者', 1952, 1),
  P('lgrumman', 'リロイ・グラマン', 'Leroy Grumman', 1930, '1930年にGrumman Aerospaceを創業。', '源流の創業者', 1966, 1),
  P('sugar', 'ロン・シュガー', 'Ron Sugar', 2003, '2003〜2009年にCEO。のちAppleの取締役。', '元CEO', 2009),
  P('bush', 'ウェス・ブッシュ', 'Wes Bush', 2010, '2010〜2018年にCEO。', '元CEO', 2018),
  P('warden', 'キャシー・ウォーデン', 'Kathy Warden', 2008, '2019年1月からCEO(会長も)。', '会長兼CEO'),
  P('keffer', 'デイブ・ケッファー', 'Dave Keffer', 2020, 'CFO。', 'CFO'),
  O('northropcorp', 'Northrop Corporation', 1994, '1994年にGrummanと合併。', '合併(1994年)'),
  O('grummancorp', 'Grumman', 1994, '1994年にNorthropと合併。', '合併(1994年)'),
  O('litton', 'Litton Industries', 2001, '2001年に約51億ドルで買収。', '買収(2001年)'),
  O('trw', 'TRW', 2002, '2002年に約78億ドルで買収。', '買収(2002年)'),
  O('hii', 'Huntington Ingalls', 2011, '2011年に造船部門を分離。', '分離(2011年)'),
  O('orbital', 'Orbital ATK', 2018, '2018年に約92億ドルで買収。', '買収(2018年)'),
  O('apple', 'Apple', 2010, 'シュガー氏が取締役を務める会社。', '関連'),
 ] + holders([('State Street', '9.3', M), ('BlackRock', '7.0', M), ('Vanguard', '6.3', M)]),
 [('jnorthrop', 'lgrumman', 'link', '航空機の源流'), ('sugar', 'bush', 'link', '後任', 2010), ('bush', 'warden', 'link', '後任', 2019), ('sugar', 'apple', 'link', '取締役'), ('co', 'northropcorp', 'owns'), ('co', 'grummancorp', 'owns'), ('co', 'litton', 'owns'), ('co', 'trw', 'owns'), ('co', 'orbital', 'owns'), ('co', 'hii', 'owns', '分離')],
 '1994年にNorthropとGrummanが合併して誕生した防衛・航空宇宙の会社。2019年からキャシー・ウォーデンがCEOを務めています。')

# ---------------- Illinois Tool Works ----------------
deep('ITW', 'Illinois Tool Works', 1912, NOTE + '歴代の経営者の情報は少なく、確認できた範囲だけを載せています。', [
  P('bsmith', 'バイロン・スミス', 'Byron Smith', 1912, '1912年にシカゴで創業。', '創業者', 1940, 1),
  P('speer', 'デビッド・スピア', 'David Speer', 1982, '2006〜2015年にCEO。', '元CEO', 2015),
  P('santi', 'スコット・サンティ', 'Scott Santi', 1980, '2012〜2025年にCEO。現在は会長。', '会長'),
  P('oherlihy', 'クリストファー・オハーリヒー', "Christopher O'Herlihy", 1992, '現CEO兼社長(英語版Wikipedia)。', 'CEO兼社長'),
  O('briar', 'Briar Hall Management', 2026, '約9.1%を持つ最大の株主(MarketScreener)。', '最大の株主(約9.1%)', 'i'),
  O('statefarm', 'State Farm', 2026, '約7.4%を持つ上位株主(MarketScreener)。', '株主(約7.4%)', 'i'),
 ] + holders([('BlackRock', '6.4', M), ('Vanguard', '6.1', M)]),
 [('bsmith', 'speer', 'link', '源流を継ぐ'), ('speer', 'santi', 'link', '後任'), ('santi', 'oherlihy', 'link', '後任')],
 '1912年にシカゴで創業した産業機器の会社。クリストファー・オハーリヒーがCEOを務めています。')

# ---------------- Cigna ----------------
deep('CI', 'Cigna', 1982, NOTE + 'Humanaへの買収提案(2023年)は報道に基づきます。', [
  P('cordani', 'デビッド・コルダニ', 'David Cordani', 1991, '2009〜2025年にCEO。現在は執行会長。', '会長(執行)'),
  P('evanko', 'ブライアン・エバンコ', 'Brian Evanko', 2011, '現社長兼CEO(英語版Wikipedia)。', '社長兼CEO'),
  O('ina', 'Insurance Company of North America', 1982, '1982年にConnecticut Generalと合併してCIGNAに。', '合併(1982年)'),
  O('cgl', 'Connecticut General', 1982, '1982年にINAと合併。', '合併(1982年)'),
  O('express', 'Express Scripts', 2018, '2018年に約670億ドルで買収。', '買収(2018年)'),
  O('anthem', 'Anthem(現Elevance Health)', 2015, '2015年にAnthemが約540億ドルで買収を提案したが、2017年に断念。', '合併断念(2017年)'),
  O('humana', 'Humana', 2023, '2023年に買収を検討したが、見送ったと報じられています。', '買収検討(2023年・報道)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '5.7', M), ('State Street', '4.5', M)]),
 [('cordani', 'evanko', 'link', '後任'), ('co', 'ina', 'owns'), ('co', 'cgl', 'owns'), ('co', 'express', 'owns'), ('co', 'anthem', 'conflict', '合併を断念', 2017), ('co', 'humana', 'link', '買収を検討')],
 '1982年にINAとConnecticut Generalが合併して誕生した医療保険・薬剤給付の会社。2018年にExpress Scriptsを買収しました。')

# ---------------- Datadog ----------------
deep('DDOG', 'Datadog', 2010, NOTE + '歴代の経営者の情報は少なく、確認できた範囲だけを載せています。', [
  P('pomel', 'オリビエ・ポメル', 'Olivier Pomel', 2010, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('lequoc', 'アレクシス・レ＝コック', 'Alexis Le-Quoc', 2010, '共同創業者でCTO。', '共同創業者 / CTO', None, 1),
  P('obstler', 'デビッド・オブストラー', 'David Obstler', 2018, 'CFO。', 'CFO'),
  O('wireless', 'Wireless Generation', 2008, '二人が出会ったニューヨークの前職の会社。', '前職'),
  O('sqreen', 'Sqreen', 2021, '2021年に買収(セキュリティ)。', '買収(2021年)'),
  O('cloudcraft', 'Cloudcraft', 2022, '2022年に買収。', '買収(2022年)'),
 ] + holders([('Vanguard', '8.0', M)]),
 [('pomel', 'lequoc', 'link', '共同創業'), ('wireless', 'pomel', 'link', '前職'), ('co', 'sqreen', 'owns'), ('co', 'cloudcraft', 'owns')],
 '2010年にニューヨークで創業した、運用監視のクラウドの会社。創業者のオリビエ・ポメルがCEOを務めています。')

# ---------------- CPKC ----------------
deep('CP', 'CPKC', 1881, NOTE, [
  P('harrison', 'ハンター・ハリソン', 'Hunter Harrison', 2012, '2012〜2017年にCEO。効率化の名人として知られ、のちCSXのCEO。', '元CEO', 2017),
  P('creel', 'キース・クリール', 'Keith Creel', 2013, '2017年からCEO。', 'CEO'),
  P('trafton', 'ゴードン・トラフトン', 'Gordon Trafton', 2019, '会長。', '会長'),
  P('ackman', 'ビル・アックマン', 'Bill Ackman', 2011, 'Pershing Squareを率いる投資家。2011〜2012年に委任状争奪戦でハリソン氏のCEO就任を実現。', 'アクティビスト'),
  O('cp1881', 'Canadian Pacific Railway', 1881, '1881年に設立(カナダ横断鉄道)。', '源流(1881年)'),
  O('kcs', 'Kansas City Southern', 2023, '2023年に約310億ドルで合併し、CPKCに。', '買収(2023年)'),
  O('cn', 'Canadian National', 2021, '2021年にKCSをめぐり競合し、CPが合意。', '競合'),
  O('cramer', 'Cramer Rosenthal McGlynn', 2026, '約6.3%を持つ上位株主(MarketScreener)。', '株主(約6.3%)', 'i'),
 ] + holders([('TCI Fund Management', '5.2', M), ('Aperio Group', '5.0', M)]),
 [('ackman', 'harrison', 'link', 'CEOに迎える', 2012), ('harrison', 'creel', 'link', '後任', 2017), ('cp1881', 'harrison', 'link', '源流'), ('co', 'cp1881', 'owns'), ('co', 'kcs', 'owns'), ('co', 'cn', 'conflict', '競合')],
 '1881年設立のカナダ太平洋鉄道が、2023年にKansas City Southernと合併してできた鉄道会社。キース・クリールがCEOを務めています。')

# ---------------- Brookfield Asset Management ----------------
deep('BAM', 'Brookfield Asset Management', 2022, NOTE + 'Brookfield Corporationから2022年に分割・上場した資産運用会社です。', [
  P('teskey', 'コナー・テスキー', 'Connor Teskey', 2012, 'CEO。', 'CEO'),
  P('flatt', 'ブルース・フラット', 'Bruce Flatt', 2002, 'Brookfield Corporationを率いる創業者的存在。約0.9%を保有。', '関係者'),
  O('bn', 'Brookfield Corporation', 2022, '約68.9%を持つ最大の株主(MarketScreener)。', '最大の株主(約68.9%)', 'i'),
  O('partners', 'Partners Value Investments', 2026, '約1.8%を持つ株主(MarketScreener)。', '株主(約1.8%)', 'i'),
  O('oaktree', 'Oaktree Capital', 2019, '運用する傘下の会社(2019年に取得)。', '傘下'),
 ] + holders([('BAM Credit & Insurance Solutions Advisor', '4.0', M), ('Royal Trust Corporation of Canada', '1.3', M)]),
 [('flatt', 'teskey', 'link', '経営を託す'), ('bn', 'flatt', 'link', 'CEO'), ('co', 'oaktree', 'owns')],
 'Brookfield Corporationが2022年に分割・上場した資産運用会社。コナー・テスキーがCEOを務めています。')

# ---------------- Norfolk Southern ----------------
deep('NSC', 'Norfolk Southern', 1982, NOTE + '2023年のイーストパレスチナの脱線事故は広く報じられた内容です。ユニオン・パシフィックとの合併は2025年7月の発表で、審査中の報道です。', [
  P('shaw', 'アラン・ショー', 'Alan Shaw', 1995, '2022〜2025年にCEO。2023年の脱線事故への対応を問われました。', '元CEO', 2025),
  P('george', 'マーク・ジョージ', 'Mark George', 2025, '2025年からCEO(英語版Wikipedia)。', 'CEO'),
  O('nw', 'Norfolk and Western', 1982, '1982年にSouthern Railwayと合併して誕生。', '合併(1982年)'),
  O('southern', 'Southern Railway', 1982, '1982年にNorfolk and Westernと合併。', '合併(1982年)'),
  O('ancora', 'Ancora Holdings', 2024, 'アクティビスト。2024年に取締役の刷新を求めたと報じられています。', 'アクティビスト(2024年)', 'i'),
  O('unp', 'Union Pacific', 2025, '2025年7月に合併を発表(約850億ドル、審査中の報道)。', '合併発表(2025年)'),
  O('eastpalestine', '東パレスチナの脱線事故', 2023, '2023年2月に有害物質を積んだ列車が脱線。', '事故(2023年)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '5.7', M), ('State Street', '4.6', M)]),
 [('shaw', 'george', 'link', '後任', 2025), ('ancora', 'shaw', 'conflict', '経営陣の刷新を要求', 2024), ('co', 'nw', 'owns'), ('co', 'southern', 'owns'), ('co', 'unp', 'link', '合併を発表', 2025), ('co', 'eastpalestine', 'link', '事故')],
 '1982年にNorfolk and WesternとSouthern Railwayが合併して誕生した鉄道会社。2025年にユニオン・パシフィックとの合併を発表しました。')

# ---------------- Lumentum ----------------
deep('LITE', 'Lumentum', 2015, NOTE + '歴代の経営者の情報は少なく、確認できた範囲だけを載せています。', [
  P('lowe', 'アラン・ロウ', 'Alan Lowe', 2015, '2015〜2023年にCEO。', '元CEO', 2023),
  P('hurlston', 'マイケル・ハールストン', 'Michael Hurlston', 2024, '2024年からCEO。', 'CEO'),
  P('herscher', 'ペネロープ・ハーシャー', 'Penelope Herscher', 2015, '会長。', '会長'),
  O('jdsu', 'JDS Uniphase', 2015, '2015年に分離して誕生。', '分離元(2015年)'),
  O('oclaro', 'Oclaro', 2018, '2018年に約18億ドルで買収。', '買収(2018年)'),
  O('neophotonics', 'NeoPhotonics', 2022, '2022年に買収。', '買収(2022年)'),
 ] + holders([('BlackRock', '7.3', M), ('Vanguard', '5.6', M), ('JPMorgan Asset Mgmt', '4.5', M)]),
 [('lowe', 'hurlston', 'link', '後任', 2024), ('jdsu', 'lowe', 'link', '分離を率いる'), ('co', 'jdsu', 'owns', '分離'), ('co', 'oclaro', 'owns'), ('co', 'neophotonics', 'owns')],
 '2015年にJDS Uniphaseから分離した光部品の会社。2024年からマイケル・ハールストンがCEOを務めています。')

# ---------------- Colgate-Palmolive ----------------
deep('CL', 'Colgate-Palmolive', 1806, NOTE, [
  P('wcolgate', 'ウィリアム・コルゲート', 'William Colgate', 1806, '1806年にニューヨークで石けん・ろうそくの店を創業。', '創業者', 1857, 1),
  P('mark', 'ルーベン・マーク', 'Reuben Mark', 1984, '1984〜2007年にCEO。', '元CEO', 2007),
  P('cook', 'イアン・クック', 'Ian Cook', 1996, '2007〜2019年にCEO。', '元CEO', 2019),
  P('wallace', 'ノエル・ウォレス', 'Noel Wallace', 1992, '2020年1月からCEO(会長も)。', '会長兼CEO'),
  P('sutula', 'スタンレー・スチュラ', 'Stanley Sutula', 2019, 'CFO。', 'CFO'),
  O('palmolive', 'Palmolive', 1928, '1928年にColgateと合併(Colgate-Palmolive)。', '合併(1928年)'),
  O('hills', "Hill's Pet Nutrition", 1976, '1976年に買収。', '買収(1976年)'),
  O('toms', "Tom's of Maine", 2006, '2006年に買収。', '買収(2006年)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.0', M), ('State Street', '4.6', M)]),
 [('wcolgate', 'mark', 'link', '源流'), ('mark', 'cook', 'link', '後任'), ('cook', 'wallace', 'link', '後任', 2020), ('co', 'palmolive', 'owns'), ('co', 'hills', 'owns'), ('co', 'toms', 'owns')],
 '1806年にウィリアム・コルゲートが創業した日用品の会社。2020年からノエル・ウォレスがCEOを務めています。')
