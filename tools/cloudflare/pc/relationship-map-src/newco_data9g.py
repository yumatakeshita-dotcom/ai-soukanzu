from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Wells Fargo ----------------
deep('WFC', 'Wells Fargo', 1852, NOTE + '連邦準備制度による資産上限(2018年〜)は、2025年6月に解除されたと報じられています。', [
  P('wells', 'ヘンリー・ウェルズ', 'Henry Wells', 1852, 'ウェルズ・ファーゴ(1852年)とアメリカン・エキスプレス(1850年)の共同創業者。', '共同創業者', 1878, 1),
  P('fargo', 'ウィリアム・ファーゴ', 'William Fargo', 1852, 'ウェルズ・ファーゴとアメリカン・エキスプレスの共同創業者。', '共同創業者', 1881, 1),
  P('kovacevich', 'ディック・コバセビッチ', 'Dick Kovacevich', 1993, 'ノーウェストのCEO。1998年の合併後、2009年までCEO。', '元CEO', 2009),
  P('stumpf', 'ジョン・スタンフ', 'John Stumpf', 1982, '2007〜2016年にCEO。不正口座問題で退任。', '元CEO', 2016),
  P('sloan', 'ティム・スローン', 'Tim Sloan', 1987, '2016〜2019年にCEO。', '元CEO', 2019),
  P('scharf', 'チャールズ・シャーフ', 'Charles Scharf', 2019, '2019年からCEO(2021年から会長も)。Visaの元CEO。', '会長兼CEO'),
  P('black', 'スティーブン・ブラック', 'Steven Black', 2018, '会長(英語版Wikipedia)。', '会長'),
  P('santomassimo', 'マイク・サントマッシモ', 'Mike Santomassimo', 2015, 'CFO。', 'CFO'),
  O('norwest', 'Norwest', 1998, '1998年に合併。', '合併(1998年)'),
  O('firstinterstate', 'First Interstate', 1996, '1996年に約116億ドルで買収。', '買収(1996年)'),
  O('wachovia', 'Wachovia', 2008, '2008年に約150億ドルで買収。', '買収(2008年)'),
  O('amex', 'American Express', 1850, '共同創業者を同じくする兄弟会社(のち分離)。', '源流が同じ'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.1', M), ('Fidelity', '5.0', M)]),
 [('wells', 'fargo', 'link', '共同創業'), ('kovacevich', 'stumpf', 'link', '後任'), ('stumpf', 'sloan', 'link', '後任'), ('sloan', 'scharf', 'link', '後任', 2019), ('co', 'norwest', 'owns'), ('co', 'firstinterstate', 'owns'), ('co', 'wachovia', 'owns'), ('wells', 'amex', 'moved', '共同創業')],
 '1852年に創業した銀行。2019年からチャールズ・シャーフがCEOを務めています。')

# ---------------- IBM ----------------
deep('IBM', 'IBM', 1911, NOTE, [
  P('flint', 'チャールズ・フリント', 'Charles Flint', 1911, 'CTR(IBMの前身)の創設者(1911年)。', '創設者', 1914, 1),
  P('watsonsr', 'トーマス・ワトソン・シニア', 'Thomas Watson Sr.', 1914, '1914〜1956年にトップ。IBMの名を付けた人物。', '元トップ', 1956),
  P('watsonjr', 'トーマス・ワトソン・ジュニア', 'Thomas Watson Jr.', 1946, '1956〜1971年にCEO。', '元CEO', 1971),
  P('gerstner', 'ルイス・ガースナー', 'Lou Gerstner', 1993, '1993〜2002年にCEO。IBMを立て直しました。', '元CEO', 2002),
  P('palmisano', 'サム・パルミサーノ', 'Sam Palmisano', 1973, '2002〜2011年にCEO。', '元CEO', 2011),
  P('rometty', 'ジニー・ロメッティ', 'Ginni Rometty', 1981, '2012〜2020年にCEO。', '元CEO', 2020),
  P('krishna', 'アルビンド・クリシュナ', 'Arvind Krishna', 1990, '2020年からCEO(会長も)。', '会長兼CEO'),
  P('kavanaugh', 'ジム・カバノー', 'Jim Kavanaugh', 1993, 'CFO(2017年から)。', 'CFO'),
  P('cohn', 'ゲーリー・コーン', 'Gary Cohn', 2020, '副会長(元ゴールドマン・サックス社長)。', '副会長'),
  O('pwc', 'PwC Consulting', 2002, '2002年に約35億ドルで買収。', '買収(2002年)'),
  O('redhat', 'Red Hat', 2019, '2019年に約340億ドルで買収。', '買収(2019年)'),
  O('kyndryl', 'Kyndryl', 2021, '2021年にITインフラ事業を分離。', '分離(2021年)'),
  O('hashicorp', 'HashiCorp', 2025, '2025年に約64億ドルで買収。', '買収(2025年)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.2', M), ('State Street', '5.9', M)]),
 [('flint', 'watsonsr', 'link', '経営を引き継ぐ'), ('watsonsr', 'watsonjr', 'link', '親子'), ('gerstner', 'palmisano', 'link', '後任'), ('palmisano', 'rometty', 'link', '後任'), ('rometty', 'krishna', 'link', '後任', 2020), ('co', 'pwc', 'owns'), ('co', 'redhat', 'owns'), ('co', 'kyndryl', 'owns'), ('co', 'hashicorp', 'owns')],
 '1911年に設立されたCTRを源流とするIT企業。2020年からアルビンド・クリシュナがCEOを務めています。')

# ---------------- Linde ----------------
deep('LIN', 'Linde', 1879, NOTE, [
  P('vonlinde', 'カール・フォン・リンデ', 'Carl von Linde', 1879, 'Linde AGの創業者(1879年)。冷凍技術の先駆者。', '源流の創業者', 1934, 1),
  P('reitzle', 'ヴォルフガング・ライツレ', 'Wolfgang Reitzle', 2003, 'Linde AGのCEO・会長。2018年の合併後はLinde plcの副会長。', '元会長', 2022),
  P('angel', 'スティーブ・エンジェル', 'Steve Angel', 2001, 'Praxair、のちLinde plcのCEO(2007〜2022年)。現在は会長。', '会長'),
  P('lamba', 'サンジーブ・ランバ', 'Sanjiv Lamba', 2018, '2022年3月からCEO。', 'CEO'),
  P('white', 'マシュー・ホワイト', 'Matthew White', 2018, 'CFO。', 'CFO'),
  O('praxair', 'Praxair', 1992, '1992年にユニオン・カーバイドから分離。2018年にLinde AGと統合。', '合併(2018年)'),
  O('lindeag', 'Linde AG', 1879, 'ドイツの老舗。2018年にPraxairと統合。', '合併(2018年)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '5.9', M), ('State Street', '4.4', M)]),
 [('vonlinde', 'reitzle', 'link', '源流を継ぐ'), ('reitzle', 'angel', 'link', '統合を主導', 2018), ('angel', 'lamba', 'link', '後任', 2022), ('co', 'praxair', 'owns'), ('co', 'lindeag', 'owns')],
 '2018年にドイツのLinde AGと米国のPraxairが統合して誕生した産業ガスの会社。2022年からサンジーブ・ランバがCEOを務めています。')

# ---------------- GE Vernova ----------------
deep('GEV', 'GE Vernova', 2024, NOTE + 'Trench Groupの買収(2026年10月28日)は、MarketScreenerに載っていたニュース見出しに基づきます。', [
  P('strazik', 'スコット・ストラジク', 'Scott Strazik', 2024, 'CEO。GEのガスパワー事業のCEOから昇格。', 'CEO'),
  P('angel', 'スティーブ・エンジェル', 'Steve Angel', 2024, '会長(英語版Wikipedia)。Linde plcの元CEO。', '会長'),
  P('parks', 'ケン・パークス', 'Ken Parks', 2024, 'CFO。', 'CFO'),
  O('ge', 'GE(GE Aerospace)', 2024, '2024年4月2日に分離した元の親会社。', '分離元'),
  O('alstom', 'アルストムの電力事業', 2015, '2015年にGEが約95億ドルで買収。', '源流の買収'),
  O('prolec', 'Prolec GE', 2025, '2025年に残りの持ち分を約53億ドルで取得と報じられています。', '買収(2025年・報道)'),
  O('trench', 'Trench Group', 2026, '2026年10月に、Triton社から約90億ドルで買収すると発表(報道)。', '買収(2026年・報道)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.3', M), ('Fidelity', '6.1', M)]),
 [('ge', 'strazik', 'link', '分離を率いる'), ('co', 'alstom', 'owns'), ('co', 'prolec', 'owns'), ('co', 'trench', 'owns'), ('co', 'ge', 'owns', '分離')],
 '2024年4月にGEから分離したエネルギー設備の会社。スコット・ストラジクがCEOを務めています。')

# ---------------- American Express ----------------
deep('AXP', 'American Express', 1850, NOTE, [
  P('wells', 'ヘンリー・ウェルズ', 'Henry Wells', 1850, '共同創業者。ウェルズ・ファーゴの共同創業者でもあります。', '共同創業者', 1868, 1),
  P('fargo', 'ウィリアム・ファーゴ', 'William Fargo', 1850, '共同創業者。', '共同創業者', 1881, 1),
  P('butterfield', 'ジョン・バターフィールド', 'John Butterfield', 1850, '共同創業者。', '共同創業者', 1869, 1),
  P('golub', 'ハーベイ・ゴルブ', 'Harvey Golub', 1991, '1993〜2000年にCEO。', '元CEO', 2001),
  P('chenault', 'ケン・シュノー', 'Ken Chenault', 1981, '2001〜2018年にCEO。', '元CEO', 2018),
  P('squeri', 'スティーブン・スクエリ', 'Stephen Squeri', 1985, '2018年からCEO兼会長。', '会長兼CEO'),
  P('lecaillec', 'クリストフ・ル・カイエック', 'Christophe Le Caillec', 2023, 'CFO。', 'CFO'),
  O('berkshire', 'Berkshire Hathaway', 1991, '1991年から保有。約22.5%を持つ最大の株主(MarketScreener、2026年11月)。', '最大の株主(約22.5%)', 'i'),
  O('resy', 'Resy', 2019, '2019年に買収。', '買収(2019年)'),
  O('kabbage', 'Kabbage', 2020, '2020年に買収。', '買収(2020年)'),
  O('wellsfargo', 'Wells Fargo', 1852, '共同創業者2人が1852年に創業した別会社。', '同じ源流'),
 ] + holders([('Vanguard', '5.2', M), ('BlackRock', '4.5', M), ('State Street', '4.3', M)]),
 [('wells', 'fargo', 'link', '共同創業'), ('wells', 'butterfield', 'link', '共同創業'), ('golub', 'chenault', 'link', '後任'), ('chenault', 'squeri', 'link', '後任', 2018), ('co', 'resy', 'owns'), ('co', 'kabbage', 'owns'), ('fargo', 'wellsfargo', 'moved', '別会社を創業')],
 '1850年に創業した決済・カードの会社。バークシャーが約22.5%を持つ最大の株主で、2018年からスティーブン・スクエリがCEOを務めています。')

# ---------------- Arista Networks ----------------
deep('ANET', 'Arista Networks', 2004, NOTE, [
  P('bechtolsheim', 'アンディ・ベクトルシャイム', 'Andy Bechtolsheim', 2004, '共同創業者。Sun Microsystemsの共同創業者で、グーグルの最初期の出資者。約14.3%を持つ最大の株主。', '共同創業者 / 最大の株主', None, 1),
  P('cheriton', 'デビッド・チェリトン', 'David Cheriton', 2004, '共同創業者。スタンフォード大学の教授で、グーグルの初期の出資者。', '共同創業者', None, 1),
  P('duda', 'ケン・ダダ', 'Ken Duda', 2004, '共同創業者で社長兼CTO。', '社長兼CTO', None, 1),
  P('ullal', 'ジャヤシュリー・ウラル', 'Jayshree Ullal', 2008, '2008年からCEO(会長も)。シスコの元幹部。', '会長兼CEO'),
  P('nightingale', 'トッド・ナイチンゲール', 'Todd Nightingale', 2023, '社長兼COO。', '社長兼COO'),
  P('breithaupt', 'シャンテル・ブライトハウプト', 'Chantelle Breithaupt', 2019, 'CFO。', 'CFO'),
  O('sun', 'Sun Microsystems', 1982, 'ベクトルシャイム氏の共同創業した会社。', '関連'),
  O('cisco', 'Cisco', 2008, 'ウラル氏の前職。競合でもあります。', '競合・前職'),
  O('bigswitch', 'Big Switch Networks', 2020, '2020年に買収。', '買収(2020年)'),
  O('pluribus', 'Pluribus Networks', 2022, '2022年に買収。', '買収(2022年)'),
  O('velocloud', 'VeloCloud', 2025, '2025年にBroadcomから買収(報道)。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '5.4', M), ('BlackRock', '5.4', M), ('State Street', '3.8', M)]),
 [('bechtolsheim', 'cheriton', 'link', '共同創業'), ('bechtolsheim', 'ullal', 'link', 'CEOに迎える', 2008), ('bechtolsheim', 'duda', 'link', '共同創業'), ('ullal', 'cisco', 'moved', '前職'), ('bechtolsheim', 'sun', 'link', '共同創業'), ('co', 'bigswitch', 'owns'), ('co', 'pluribus', 'owns'), ('co', 'velocloud', 'owns'), ('co', 'cisco', 'conflict', '競合')],
 '2004年にベクトルシャイム氏らが創業したデータセンター向けネットワークの会社。2008年からジャヤシュリー・ウラルがCEOを務めています。')

# ---------------- Gilead ----------------
deep('GILD', 'Gilead Sciences', 1987, NOTE, [
  P('riordan', 'マイケル・リオーダン', 'Michael Riordan', 1987, '創業者。', '創業者', 1996, 1),
  P('martin', 'ジョン・マーティン', 'John Martin', 1990, '1996〜2016年にCEO。', '元CEO', 2016),
  P('milligan', 'ジョン・ミリガン', 'John Milligan', 1990, '2016〜2019年にCEO。', '元CEO', 2019),
  P('oday', 'ダニエル・オデイ', "Daniel O'Day", 2019, '2019年からCEO兼会長。', '会長兼CEO'),
  P('dickinson', 'アンドリュー・ディキンソン', 'Andrew Dickinson', 2019, 'CFO。', 'CFO'),
  O('pharmasset', 'Pharmasset', 2012, '2012年に約110億ドルで買収(C型肝炎薬)。', '買収(2012年)'),
  O('kite', 'Kite Pharma', 2017, '2017年に約119億ドルで買収。', '買収(2017年)'),
  O('immunomedics', 'Immunomedics', 2020, '2020年に約210億ドルで買収。', '買収(2020年)'),
  O('fortyseven', 'Forty Seven', 2020, '2020年に約49億ドルで買収。', '買収(2020年)'),
  O('cymabay', 'CymaBay', 2024, '2024年に約43億ドルで買収。', '買収(2024年)'),
 ] + holders([('BlackRock', '7.1', M), ('Vanguard', '6.5', M), ('Fidelity', '5.4', M)]),
 [('riordan', 'martin', 'link', '後任'), ('martin', 'milligan', 'link', '後任'), ('milligan', 'oday', 'link', '後任', 2019), ('co', 'pharmasset', 'owns'), ('co', 'kite', 'owns'), ('co', 'immunomedics', 'owns'), ('co', 'fortyseven', 'owns'), ('co', 'cymabay', 'owns')],
 '1987年に創業したバイオ医薬の会社。2019年からダニエル・オデイがCEOを務めています。')

# ---------------- TotalEnergies ----------------
deep('TTE', 'TotalEnergies', 1924, NOTE + '従業員持株制度とアセットマネジメント会社の持ち分は、MarketScreener(2026年11月)の数字です。', [
  P('desmarest', 'ティエリー・デマレスト', 'Thierry Desmarest', 1995, '1995〜2007年にCEO。フィナ、エルフとの合併(1999〜2000年)を主導。', '元CEO', 2007),
  P('demargerie', 'クリストフ・ド・マルジェリー', 'Christophe de Margerie', 1974, '2007〜2014年にCEO。2014年に事故で亡くなりました。', '元CEO', 2014),
  P('pouyanne', 'パトリック・プヤンヌ', 'Patrick Pouyanne', 1997, '2014年からCEO兼会長。', '会長兼CEO'),
  O('cfp', 'Compagnie française des pétroles', 1924, '1924年に設立された源流の会社。', '源流(1924年)'),
  O('fina', 'Petrofina', 1999, '1999年に合併(ベルギー)。', '合併(1999年)'),
  O('elf', 'Elf Aquitaine', 2000, '2000年に合併(フランス)。', '合併(2000年)'),
  O('sunpower', 'SunPower', 2011, '2011年に約14億ドルで過半を取得(のち売却)。', '買収(2011年)'),
  O('saft', 'Saft', 2016, '2016年に約10億ユーロで買収(電池)。', '買収(2016年)'),
  O('directenergie', 'Direct Energie', 2018, '2018年に買収。', '買収(2018年)'),
  O('cpr', 'CPR Asset Management', 2026, '約9.0%を持つ上位株主(MarketScreener)。', '株主(約9.0%)', 'i'),
  O('amundi', 'Amundi', 2026, '約8.8%を持つ上位株主(MarketScreener)。', '株主(約8.8%)', 'i'),
  O('employees', '従業員持株制度', 2026, '約4.8%(MarketScreener)。', '株主(約4.8%)', 'i'),
 ],
 [('desmarest', 'demargerie', 'link', '後任'), ('demargerie', 'pouyanne', 'link', '後任', 2014), ('cfp', 'desmarest', 'link', '源流'), ('co', 'fina', 'owns'), ('co', 'elf', 'owns'), ('co', 'sunpower', 'owns'), ('co', 'saft', 'owns'), ('co', 'directenergie', 'owns')],
 '1924年設立のフランスの石油会社を源流とするエネルギー大手。2014年からパトリック・プヤンヌがCEOを務めています。')

# ---------------- TD Bank ----------------
deep('TD', 'TD Bank', 1955, NOTE, [
  P('baillie', 'チャールズ・ベイリー', 'Charles Baillie', 1998, '1998〜2002年にCEO。', '元CEO', 2002),
  P('clark', 'エド・クラーク', 'Ed Clark', 2000, '2002〜2014年にCEO。', '元CEO', 2014),
  P('masrani', 'バラット・マスラニ', 'Bharat Masrani', 1985, '2014〜2025年にCEO。', '元CEO', 2025),
  P('chun', 'レイモンド・チュン', 'Raymond Chun', 1987, '2025年2月からCEO。', 'CEO'),
  O('banktoronto', 'Bank of Toronto', 1955, '1955年に合併(TDの源流)。', '合併(1955年)'),
  O('dominion', 'Dominion Bank', 1955, '1955年に合併(TDの源流)。', '合併(1955年)'),
  O('canadatrust', 'Canada Trust', 2000, '2000年に買収。', '買収(2000年)'),
  O('commerce', 'Commerce Bancorp', 2008, '2008年に約85億ドルで買収(米国)。', '買収(2008年)'),
  O('ameritrade', 'TD Ameritrade', 2020, '2020年にチャールズ・シュワブに売却し、シュワブの株式を取得。', '売却(2020年)'),
  O('firsthorizon', 'First Horizon', 2023, '2022年に約134億ドルでの買収を発表したが、2023年に断念。', '買収断念(2023年)'),
  O('royaltrust', 'Royal Trust Corporation of Canada', 2026, '約6.3%を持つ(MarketScreener)。RBCの信託子会社。', '株主(約6.3%)', 'i'),
 ] + holders([('BMO Bank NA', '3.4', M), ('Vanguard', '3.0', M)]),
 [('baillie', 'clark', 'link', '後任'), ('clark', 'masrani', 'link', '後任'), ('masrani', 'chun', 'link', '後任', 2025), ('co', 'banktoronto', 'owns'), ('co', 'dominion', 'owns'), ('co', 'canadatrust', 'owns'), ('co', 'commerce', 'owns'), ('co', 'ameritrade', 'owns'), ('co', 'firsthorizon', 'link', '断念')],
 '1955年にトロント銀行とドミニオン銀行が合併して誕生したカナダの銀行。2025年からレイモンド・チュンがCEOを務めています。')

# ---------------- KLA ----------------
deep('KLAC', 'KLA', 1997, NOTE, [
  P('schroeder', 'ケン・シュローダー', 'Ken Schroeder', 1997, 'KLA-Tencor設立時(1997年)のCEO。', '元CEO', 2005),
  P('wallace', 'リック・ウォレス', 'Rick Wallace', 1988, '2006年からCEO。', 'CEO'),
  P('calderoni', 'ロバート・カルデローニ', 'Robert Calderoni', 2006, '会長。', '会長'),
  P('higgins', 'ブレン・ヒギンズ', 'Bren Higgins', 2017, 'CFO。', 'CFO'),
  O('klainstruments', 'KLA Instruments', 1997, '1997年にTencorと合併(KLA-Tencor)。', '合併(1997年)'),
  O('tencor', 'Tencor Instruments', 1997, '1997年にKLAと合併。', '合併(1997年)'),
  O('ade', 'ADE', 2006, '2006年に買収。', '買収(2006年)'),
  O('orbotech', 'Orbotech', 2019, '2019年に約34億ドルで買収(イスラエル)。', '買収(2019年)'),
 ] + holders([('BlackRock', '7.3', M), ('Vanguard', '6.5', M), ('State Street', '4.8', M)]),
 [('schroeder', 'wallace', 'link', '経営を引き継ぐ'), ('co', 'klainstruments', 'owns'), ('co', 'tencor', 'owns'), ('co', 'ade', 'owns'), ('co', 'orbotech', 'owns')],
 '1997年にKLAとTencorが合併して誕生した半導体検査装置の会社。2006年からリック・ウォレスがCEOを務めています。')
