from newco_data9 import deep, P, O

NOTE = '現在の役員は英語版Wikipedia(2026年11月取得)に基づきます。創業からの経緯、歴代の経営者、買収は広く知られた範囲で、提出書類では確認していません(買収額は報道ベース)。上位株主はYahoo FinanceまたはMarketScreenerに基づきます。顔写真がない人はイニシャル表示です。'

def holders(rows):
    return [O('h%d' % i, n, 2026, '上位株主(約%s%%、%s)。' % (p, s), '株主(約%s%%)' % p, 'i') for i, (n, p, s) in enumerate(rows)]
Y = 'Yahoo Finance、2026年6月30日時点'
M = 'MarketScreener、2026年11月'

# ---------------- Broadcom ----------------
deep('AVGO', 'Broadcom', 1991, NOTE, [
  P('nicholas', 'ヘンリー・ニコラス', 'Henry Nicholas', 1991, 'ブロードコム(旧Broadcom Corp.)の共同創業者。', '共同創業者', 2003, 1),
  P('samueli', 'ヘンリー・サミュエリ', 'Henry Samueli', 1991, '旧Broadcom Corp.の共同創業者。会長。', '共同創業者 / 会長', None, 1),
  P('tan', 'ホック・タン', 'Hock Tan', 2006, 'Avago(のちのBroadcom Inc.)のCEO(2006年から)。買収を重ねて成長させました。', 'CEO'),
  P('kawwas', 'チャーリー・カワス', 'Charlie Kawwas', 2006, '半導体ソリューション事業の社長。', '社長(半導体事業)'),
  P('spears', 'カーステン・スピアーズ', 'Kirsten Spears', 2006, 'CFO。', 'CFO'),
  O('kkr', 'KKR', 2005, '2005年にSilver Lakeとともに、アジレントの半導体部門(Avagoの前身)を買収。', '出資者(2005年)', 'i'),
  O('silverlake', 'Silver Lake', 2005, '2005年にKKRとともにAvagoを買収。', '出資者(2005年)', 'i'),
  O('lsi', 'LSI', 2014, '2014年に約66億ドルで買収。', '買収(2014年)'),
  O('broadcomcorp', 'Broadcom Corporation', 2016, '2016年に約370億ドルで買収し、社名をBroadcomに。', '買収(2016年)'),
  O('brocade', 'Brocade', 2017, '2017年に約59億ドルで買収。', '買収(2017年)'),
  O('ca', 'CA Technologies', 2018, '2018年に約189億ドルで買収。', '買収(2018年)'),
  O('symantec', 'Symantecの企業向け事業', 2019, '2019年に約107億ドルで買収。', '買収(2019年)'),
  O('vmware', 'VMware', 2023, '2023年に約690億ドルで買収。', '買収(2023年)'),
  O('openai', 'OpenAI', 2025, 'AI向け専用チップの提携先と報じられています。', '提携先(報道)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.2', M), ('State Street', '4.1', M)]),
 [('nicholas', 'samueli', 'link', '共同創業'), ('samueli', 'tan', 'link', '会長とCEO'), ('co', 'lsi', 'owns'), ('co', 'broadcomcorp', 'owns'), ('co', 'brocade', 'owns'), ('co', 'ca', 'owns'), ('co', 'symantec', 'owns'), ('co', 'vmware', 'owns'), ('co', 'openai', 'link')],
 '半導体とインフラソフトの会社。ホック・タンが2006年からCEOを務め、LSI、Broadcom Corp.、CA、VMwareなどの買収で拡大しました。')

# ---------------- Eli Lilly ----------------
deep('LLY', 'Eli Lilly', 1876, NOTE, [
  P('elilly', 'イーライ・リリー大佐', 'Eli Lilly', 1876, '1876年にインディアナポリスで創業。', '創業者', 1898, 1),
  P('jklilly', 'ジョサイア・K・リリー', 'J. K. Lilly Sr.', 1898, '創業者の息子で、のち社長。', '元社長', 1948),
  P('taurel', 'シドニー・トーレル', 'Sidney Taurel', 1998, '1998〜2008年にCEO。', '元CEO', 2008),
  P('lechleiter', 'ジョン・レクライター', 'John Lechleiter', 2008, '2008〜2017年にCEO。', '元CEO', 2017),
  P('ricks', 'デビッド・リックス', 'David Ricks', 1996, '2017年からCEO兼会長。', 'CEO兼会長'),
  P('skovronsky', 'ダン・スコブロンスキー', 'Dan Skovronsky', 2010, '最高科学責任者(CSO)兼リリー研究所の社長。', 'CSO'),
  P('montarce', 'ルーカス・モンタルセ', 'Lucas Montarce', 1999, 'CFO(2024年から)。', 'CFO'),
  O('endowment', 'Lilly Endowment', 1937, '創業家が設立した財団。約9.6%を持つ最大の株主(MarketScreener、2026年11月)。', '最大の株主(約9.6%)', 'i'),
  O('loxo', 'Loxo Oncology', 2019, '2019年に約80億ドルで買収(がん)。', '買収(2019年)'),
  O('dermira', 'Dermira', 2020, '2020年に約11億ドルで買収。', '買収(2020年)'),
  O('prevail', 'Prevail Therapeutics', 2021, '2021年に約10億ドルで買収。', '買収(2021年)'),
  O('dice', 'DICE Therapeutics', 2023, '2023年に約24億ドルで買収。', '買収(2023年)'),
 ] + holders([('Vanguard', '5.7', M), ('PNC Wealth Management', '5.4', M), ('BlackRock', '5.4', M)]),
 [('elilly', 'jklilly', 'link', '親子'), ('taurel', 'lechleiter', 'link', '後任'), ('lechleiter', 'ricks', 'link', '後任'), ('co', 'loxo', 'owns'), ('co', 'dermira', 'owns'), ('co', 'prevail', 'owns'), ('co', 'dice', 'owns'), ('elilly', 'endowment', 'link', '創業家の財団')],
 '1876年創業の製薬会社。創業家の財団Lilly Endowmentが最大の株主で、2017年からデビッド・リックスがCEOを務めています。')

# ---------------- SpaceX ----------------
deep('SPCX', 'SpaceX', 2002, NOTE + 'SpaceXの上場(2026年6月12日、公募価格135ドル、調達約750億ドル)は報道に基づきます。', [
  P('musk', 'イーロン・マスク', 'Elon Musk', 2002, '2002年に創業。CEO、会長、CTO。TeslaとxAIも率います。', 'CEO兼会長兼CTO', None, 1),
  P('shotwell', 'グウィン・ショットウェル', 'Gwynne Shotwell', 2002, '2002年に入社し、2008年から社長兼COO。', '社長兼COO'),
  P('mueller', 'トム・ミューラー', 'Tom Mueller', 2002, '最初期の社員で推進系の責任者。', '推進系の責任者(初期)'),
  P('johnsen', 'ブレット・ジョンセン', 'Bret Johnsen', 2010, 'CFO。', 'CFO'),
  O('foundersfund', "Founders Fund", 2008, '2008年に2,000万ドルを出資(ピーター・ティール)。', '出資者(2008年)', 'i'),
  O('alphabet', 'Alphabet', 2015, '2015年にFidelityとともに約10億ドルを出資。上位株主(約6.7%)。', '出資者(2015年)', 'i'),
  O('fidelity', 'Fidelity', 2015, '2015年にGoogleとともに出資。', '出資者(2015年)', 'i'),
  O('valor', 'Valor Equity Partners', 2026, '上位株主(約6.1%、Yahoo Finance、2026年6月30日時点)。', '株主(約6.1%)', 'i'),
  O('xai', 'xAI', 2026, '2026年2月にSpaceXが買収したと報じられています。', '買収(2026年・報道)'),
  O('starlink', 'Starlink', 2019, '衛星インターネット事業。', '事業'),
  O('tesla', 'Tesla', 2008, 'マスクが率いる関連会社。', '関連会社'),
 ],
 [('musk', 'shotwell', 'link', 'COOを任せる'), ('co', 'xai', 'owns'), ('co', 'starlink', 'owns'), ('musk', 'tesla', 'link', 'CEO')],
 'イーロン・マスクが2002年に創業したロケットと衛星通信の会社。2026年6月にNasdaqへ上場しました。')

# ---------------- Micron ----------------
deep('MU', 'Micron Technology', 1978, NOTE, [
  P('wparkinson', 'ウォード・パーキンソン', 'Ward Parkinson', 1978, '共同創業者。', '共同創業者', 1990, 1),
  P('jparkinson', 'ジョー・パーキンソン', 'Joe Parkinson', 1978, '共同創業者。', '共同創業者', 1990, 1),
  P('wilson', 'デニス・ウィルソン', 'Dennis Wilson', 1978, '共同創業者。', '共同創業者', 1990, 1),
  P('pitman', 'ダグ・ピットマン', 'Doug Pitman', 1978, '共同創業者。', '共同創業者', 1990, 1),
  P('appleton', 'スティーブ・アップルトン', 'Steve Appleton', 1983, '1994〜2012年にCEO。2012年に亡くなりました。', '元CEO', 2012),
  P('durcan', 'マーク・ダーカン', 'Mark Durcan', 1984, '2012〜2017年にCEO。', '元CEO', 2017),
  P('mehrotra', 'サンジェイ・メロートラ', 'Sanjay Mehrotra', 2017, '2017年からCEO(サンディスク共同創業者)。', 'CEO兼会長'),
  P('arnzen', 'エイプリル・アーンゼン', 'April Arnzen', 2020, '最高人事責任者(CPO)。', 'CPO'),
  O('simplot', 'J. R. シンプロット', 1980, '初期に資金を支えた実業家。', '初期の出資者', 'i'),
  O('lexar', 'Lexar', 2006, '2006年に買収。', '買収(2006年)'),
  O('numonyx', 'Numonyx', 2010, '2010年に買収。', '買収(2010年)'),
  O('elpida', 'エルピーダメモリ', 2013, '2013年に約25億ドルで買収。', '買収(2013年)'),
  O('inotera', 'Inotera', 2016, '2016年に買収(台湾)。', '買収(2016年)'),
 ] + holders([('BlackRock', '9.3', Y), ('Vanguard', '6.5', Y), ('State Street', '4.4', Y)]),
 [('wparkinson', 'jparkinson', 'link', '兄弟'), ('appleton', 'durcan', 'link', '後任'), ('durcan', 'mehrotra', 'link', '後任'), ('simplot', 'wparkinson', 'link', '資金を支援'), ('co', 'lexar', 'owns'), ('co', 'numonyx', 'owns'), ('co', 'elpida', 'owns'), ('co', 'inotera', 'owns')],
 '1978年にアイダホ州ボイシで創業したメモリの会社。2017年からサンジェイ・メロートラがCEOを務めています。')

# ---------------- Walmart ----------------
deep('WMT', 'Walmart', 1962, NOTE + 'ウォルトン家の持ち分(約44%とする情報サイトあり)は、出典が弱いため数字を載せていません。', [
  P('swalton', 'サム・ウォルトン', 'Sam Walton', 1962, '1962年に創業。1992年に亡くなりました。', '創業者', 1992, 1),
  P('glass', 'デビッド・グラス', 'David Glass', 1988, '1988〜2000年にCEO。', '元CEO', 2000),
  P('scott', 'リー・スコット', 'Lee Scott', 2000, '2000〜2009年にCEO。', '元CEO', 2009),
  P('duke', 'マイク・デューク', 'Mike Duke', 2009, '2009〜2014年にCEO。', '元CEO', 2014),
  P('mcmillon', 'ダグ・マクミロン', 'Doug McMillon', 1984, '2014年から2026年1月までCEO。', '元CEO', 2026),
  P('furner', 'ジョン・ファーナー', 'John Furner', 1993, '2026年2月からCEO。', 'CEO'),
  P('rainey', 'ジョン・デビッド・レイニー', 'John David Rainey', 2022, 'CFO。', 'CFO'),
  P('rwalton', 'ロブ・ウォルトン', 'Rob Walton', 1969, '創業者の息子。会長(1992〜2015年)。', '元会長', 2015),
  P('penner', 'グレッグ・ペナー', 'Greg Penner', 2008, '会長(2015年から)。ロブ・ウォルトンの娘婿。', '会長'),
  O('walton', 'ウォルトン家', 1962, '創業家が過半の議決権を持つ筆頭株主として知られます(比率は未確認)。', '筆頭株主(創業家)', 'i'),
  O('jet', 'Jet.com', 2016, '2016年に約33億ドルで買収。', '買収(2016年)'),
  O('flipkart', 'Flipkart', 2018, '2018年に約160億ドルで過半を取得(インド)。', '買収(2018年)'),
  O('asda', 'Asda', 1999, '1999年に買収(2021年に売却)。', '買収(1999年)'),
  O('seiyu', '西友', 2002, '2002年から出資し、2021年に売却(KKRと楽天)。', '出資(2002年〜2021年)'),
  O('rakuten', '楽天グループ', 2021, '2021年に西友の株式の一部を取得。', '西友の売却先'),
 ] + holders([('Vanguard', '6.5', M), ('Vanguard Portfolio Mgmt', '6.1', M), ('State Street', '5.3', M)]),
 [('swalton', 'rwalton', 'link', '親子'), ('rwalton', 'penner', 'link', '娘婿'), ('mcmillon', 'furner', 'link', '後任', 2026), ('glass', 'scott', 'link', '後任'), ('scott', 'duke', 'link', '後任'), ('duke', 'mcmillon', 'link', '後任'),
  ('co', 'jet', 'owns'), ('co', 'flipkart', 'owns'), ('co', 'asda', 'owns'), ('co', 'seiyu', 'owns'), ('seiyu', 'rakuten', 'moved', '売却先')],
 '1962年にサム・ウォルトンが創業した小売の会社。2026年2月からジョン・ファーナーがCEOを務め、創業家が筆頭株主です。')

# ---------------- JPMorgan ----------------
deep('JPM', 'JPMorgan Chase', 1799, NOTE, [
  P('harrison', 'ウィリアム・ハリソン', 'William Harrison', 2000, '2000〜2005年にCEO。', '元CEO', 2005),
  P('dimon', 'ジェイミー・ダイモン', 'Jamie Dimon', 2004, 'Bank Oneから2004年に参加し、2006年からCEO、2007年から会長。', '会長兼CEO'),
  P('piepszak', 'ジェニファー・ピエプザック', 'Jennifer Piepszak', 2001, 'COO(2024年から)。', 'COO'),
  P('pinto', 'ダニエル・ピント', 'Daniel Pinto', 1996, '社長(元CIB責任者)。', '社長'),
  P('barnum', 'ジェレミー・バーナム', 'Jeremy Barnum', 2000, 'CFO(2021年から)。', 'CFO'),
  P('lake', 'マリアンヌ・レイク', 'Marianne Lake', 2000, '消費者・コミュニティ銀行のCEO。', '部門CEO'),
  P('erdoes', 'メアリー・エルドース', 'Mary Erdoes', 1996, '資産・富裕層運用のCEO。', '部門CEO'),
  P('petno', 'ダグ・ペトノ', 'Doug Petno', 1993, 'コーポレート&投資銀行のCEO。', '部門CEO'),
  P('weill', 'サンディ・ワイル', 'Sandy Weill', 1998, 'シティグループの共同創業者。ダイモン氏の元上司。', '関係者', 1998),
  O('bankone', 'Bank One', 2004, '2004年に約580億ドルで合併。ダイモン氏の前職。', '合併(2004年)'),
  O('bearstearns', 'Bear Stearns', 2008, '2008年に救済買収。', '買収(2008年)'),
  O('wamu', 'Washington Mutual', 2008, '2008年に銀行部門を買収。', '買収(2008年)'),
  O('firstrepublic', 'First Republic Bank', 2023, '2023年に破綻後、買収。', '買収(2023年)'),
 ] + holders([('Vanguard', '6.1', M), ('BlackRock', '6.0', M), ('State Street', '4.7', M)]),
 [('weill', 'dimon', 'link', '元上司'), ('dimon', 'bankone', 'moved', '前職'), ('harrison', 'dimon', 'link', '後任', 2006), ('co', 'bankone', 'owns'), ('co', 'bearstearns', 'owns'), ('co', 'wamu', 'owns'), ('co', 'firstrepublic', 'owns')],
 '米国最大級の銀行。ジェイミー・ダイモンが2006年からCEO、2007年から会長を務めています。')

# ---------------- AMD ----------------
deep('AMD', 'AMD', 1969, NOTE, [
  P('sanders', 'ジェリー・サンダース', 'Jerry Sanders', 1969, '1969年に創業し、2002年までCEO。', '創業者 / 元CEO', 2002, 1),
  P('ruiz', 'ヘクター・ルイズ', 'Hector Ruiz', 2000, '2002〜2008年にCEO。', '元CEO', 2008),
  P('meyer', 'ダーク・マイヤー', 'Dirk Meyer', 1995, '2008〜2011年にCEO。', '元CEO', 2011),
  P('read', 'ローリー・リード', 'Rory Read', 2011, '2011〜2014年にCEO。', '元CEO', 2014),
  P('su', 'リサ・スー', 'Lisa Su', 2012, '2014年からCEO(2022年から会長も)。', '会長兼CEO'),
  P('papermaster', 'マーク・ペーパーマスター', 'Mark Papermaster', 2011, 'CTO。', 'CTO'),
  P('hu', 'ジーン・フー', 'Jean Hu', 2022, 'CFO。', 'CFO'),
  P('norrod', 'フォレスト・ノロッド', 'Forrest Norrod', 2014, 'データセンター事業の責任者。', 'データセンター責任者'),
  O('ati', 'ATI', 2006, '2006年に約54億ドルで買収(GPU)。', '買収(2006年)'),
  O('globalfoundries', 'GlobalFoundries', 2009, '2009年に製造部門を分社(ムバダラが出資)。', '分社(2009年)'),
  O('xilinx', 'Xilinx', 2022, '2022年に約490億ドルで買収。', '買収(2022年)'),
  O('pensando', 'Pensando', 2022, '2022年に約19億ドルで買収。', '買収(2022年)'),
  O('zt', 'ZT Systems', 2025, '2025年に約49億ドルで買収。', '買収(2025年)'),
  O('openai', 'OpenAI', 2025, 'AIチップの大型契約の相手と報じられています。', '提携先(報道)'),
 ] + holders([('BlackRock', '9.2', Y), ('Vanguard', '6.5', Y), ('State Street', '4.6', Y)]),
 [('sanders', 'ruiz', 'link', '後任'), ('ruiz', 'meyer', 'link', '後任'), ('meyer', 'read', 'link', '後任'), ('read', 'su', 'link', '後任', 2014), ('co', 'ati', 'owns'), ('co', 'globalfoundries', 'owns'), ('co', 'xilinx', 'owns'), ('co', 'pensando', 'owns'), ('co', 'zt', 'owns'), ('co', 'openai', 'link')],
 '1969年にジェリー・サンダースが創業した半導体の会社。2014年からリサ・スーがCEOを務め、Xilinx、ATIなどを買収しました。')

# ---------------- ExxonMobil ----------------
deep('XOM', 'ExxonMobil', 1870, NOTE + '上位株主は取得できていません。', [
  P('rockefeller', 'ジョン・D・ロックフェラー', 'John D. Rockefeller', 1870, '1870年にスタンダード・オイルを創業(エクソンの源流)。', '創業者', 1897, 1),
  P('raymond', 'リー・レイモンド', 'Lee Raymond', 1993, '1993〜2005年にCEO。モービルとの合併(1999年)を主導。', '元CEO', 2005),
  P('tillerson', 'レックス・ティラーソン', 'Rex Tillerson', 1975, '2006〜2016年にCEO。のち米国務長官。', '元CEO', 2016),
  P('woods', 'ダレン・ウッズ', 'Darren Woods', 1992, '2017年からCEO兼会長。', '会長兼CEO'),
  P('mikells', 'キャシー・ミケルズ', 'Kathy Mikells', 2021, 'CFO。', 'CFO'),
  O('mobil', 'Mobil', 1999, '1999年に約810億ドルで合併。', '合併(1999年)'),
  O('xto', 'XTO Energy', 2010, '2010年に約310億ドルで買収(シェールガス)。', '買収(2010年)'),
  O('pioneer', 'Pioneer Natural Resources', 2024, '2024年に約600億ドルで買収。', '買収(2024年)'),
  O('imperial', 'Imperial Oil', 1898, 'カナダの子会社(約67%を保有、MarketScreener)。', '子会社(約67.4%)'),
 ],
 [('raymond', 'tillerson', 'link', '後任'), ('tillerson', 'woods', 'link', '後任', 2017), ('co', 'mobil', 'owns'), ('co', 'xto', 'owns'), ('co', 'pioneer', 'owns'), ('co', 'imperial', 'owns')],
 'ロックフェラーのスタンダード・オイルに源流を持つ石油大手。2017年からダレン・ウッズがCEOを務めています。')

# ---------------- Berkshire Hathaway ----------------
deep('BRK', 'Berkshire Hathaway', 1965, NOTE + '保有銘柄の持ち分比率は、MarketScreener(2026年11月)に載っていた数字です。', [
  P('buffett', 'ウォーレン・バフェット', 'Warren Buffett', 1965, '1965年に経営権を取得し、2025年末までCEO。名誉会長。', 'CEO(〜2025年)/ 名誉会長', None, 1),
  P('munger', 'チャーリー・マンガー', 'Charlie Munger', 1978, '副会長。2023年11月に亡くなりました。', '元副会長', 2023),
  P('abel', 'グレッグ・エイベル', 'Greg Abel', 1999, '2026年1月からCEO(エネルギー事業の責任者を経て)。', 'CEO'),
  P('jain', 'アジット・ジェイン', 'Ajit Jain', 1986, '保険事業の副会長。', '副会長(保険)'),
  P('hbuffett', 'ハワード・G・バフェット', 'Howard G. Buffett', 2010, '会長(英語版Wikipediaの記載)。ウォーレンの息子。', '会長'),
  P('combs', 'トッド・コームズ', 'Todd Combs', 2010, '投資担当。のちJPモルガンに移籍。', '元投資担当', 2025),
  P('weschler', 'テッド・ウェシュラー', 'Ted Weschler', 2012, '投資担当。', '投資担当'),
  O('geico', 'GEICO', 1996, '1996年に完全子会社化。', '子会社(1996年)'),
  O('bnsf', 'BNSF鉄道', 2010, '2010年に約340億ドルで買収。', '買収(2010年)'),
  O('pcc', 'Precision Castparts', 2016, '2016年に約370億ドルで買収。', '買収(2016年)'),
  O('alleghany', 'Alleghany', 2022, '2022年に約116億ドルで買収。', '買収(2022年)'),
  O('bhe', 'Berkshire Hathaway Energy', 2000, 'エネルギー子会社(旧MidAmerican)。', '子会社'),
  O('apple', 'Apple', 2016, '最大級の保有銘柄。', '保有銘柄'),
  O('amex', 'American Express', 1991, '約22.5%を保有(MarketScreener)。', '保有銘柄(約22.5%)'),
  O('bofa', 'Bank of America', 2011, '約6.9%を保有(MarketScreener)。', '保有銘柄(約6.9%)'),
  O('coke', 'Coca-Cola', 1988, '約9.3%を保有(Yahoo Finance)。', '保有銘柄(約9.3%)'),
  O('chevron', 'Chevron', 2020, '約4.3%を保有(MarketScreener)。', '保有銘柄(約4.3%)'),
  O('moodys', "Moody's", 2000, '約14.2%を保有(MarketScreener)。', '保有銘柄(約14.2%)'),
  O('chubb', 'Chubb', 2023, '約8.9%を保有(MarketScreener)。', '保有銘柄(約8.9%)'),
 ] + holders([('BlackRock', '8.6', Y), ('Vanguard', '8.4', Y), ('State Street', '5.4', Y)]),
 [('buffett', 'munger', 'link', '共同経営'), ('buffett', 'abel', 'link', '後継CEO', 2026), ('buffett', 'hbuffett', 'link', '親子'), ('buffett', 'combs', 'link'), ('buffett', 'weschler', 'link'), ('munger', 'buffett', 'link'),
  ('co', 'geico', 'owns'), ('co', 'bnsf', 'owns'), ('co', 'pcc', 'owns'), ('co', 'alleghany', 'owns'), ('co', 'bhe', 'owns'), ('abel', 'bhe', 'link', '率いた'),
  ('co', 'apple', 'invest2'), ('co', 'amex', 'invest2'), ('co', 'bofa', 'invest2'), ('co', 'coke', 'invest2'), ('co', 'chevron', 'invest2'), ('co', 'moodys', 'invest2'), ('co', 'chubb', 'invest2')],
 'ウォーレン・バフェットが1965年に経営権を握った投資持株会社。2026年1月からグレッグ・エイベルがCEOを務めています。')

# ---------------- Visa ----------------
deep('V', 'Visa', 1958, NOTE, [
  P('hock', 'ディー・ホック', 'Dee Hock', 1970, 'ビザの組織を築いた創設者。', '創設者', 1984, 1),
  P('saunders', 'ジョー・ソンダース', 'Joe Saunders', 2007, '2007〜2013年にCEO。2008年のIPOを率いました。', '元CEO', 2013),
  P('scharf', 'チャールズ・シャーフ', 'Charles Scharf', 2012, '2012〜2016年にCEO。のちウェルズ・ファーゴCEO。', '元CEO', 2016),
  P('kelly', 'アル・ケリー', 'Al Kelly', 2016, '2016〜2023年にCEO。', '元CEO', 2023),
  P('mcinerney', 'ライアン・マキナニー', 'Ryan McInerney', 2013, '2023年からCEO。', 'CEO'),
  P('lundgren', 'ジョン・ランドグレン', 'John Lundgren', 2020, '会長。', '会長'),
  P('suh', 'クリス・スー', 'Chris Suh', 2022, 'CFO。', 'CFO'),
  P('jenkyn', 'オリバー・ジェンキン', 'Oliver Jenkyn', 2017, 'グローバル市場担当のグループ社長。', 'グループ社長'),
  O('bofa', 'Bank of America', 1958, 'BankAmericardとして、ビザの源流を創業。', '源流(1958年)'),
  O('visaeurope', 'Visa Europe', 2016, '2016年に買収。', '買収(2016年)'),
  O('plaid', 'Plaid', 2020, '2020年に約53億ドルでの買収を発表したが、反トラスト当局の訴えで2021年に撤回。', '買収未了(2020年)'),
  O('currencycloud', 'Currencycloud', 2021, '2021年に買収。', '買収(2021年)'),
  O('featurespace', 'Featurespace', 2024, '2024年に買収(不正検知)。', '買収(2024年)'),
 ] + holders([('Vanguard', '6.2', M), ('BlackRock', '6.0', M), ('State Street', '4.9', M)]),
 [('hock', 'bofa', 'moved', '源流'), ('saunders', 'scharf', 'link', '後任'), ('scharf', 'kelly', 'link', '後任'), ('kelly', 'mcinerney', 'link', '後任', 2023), ('co', 'visaeurope', 'owns'), ('co', 'plaid', 'link', '買収を断念'), ('co', 'currencycloud', 'owns'), ('co', 'featurespace', 'owns')],
 '1958年のBankAmericardを源流とする決済ネットワーク。2023年からライアン・マキナニーがCEOを務めています。')
