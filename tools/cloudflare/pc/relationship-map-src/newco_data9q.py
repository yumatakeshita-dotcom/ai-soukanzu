from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Intercontinental Exchange ----------------
deep('ICE', 'Intercontinental Exchange', 2000, NOTE, [
  P('sprecher', 'ジェフリー・スプレッチャー', 'Jeffrey Sprecher', 2000, '創業者。会長兼CEO。', '創業者 / 会長兼CEO', None, 1),
  P('jackson', 'ベンジャミン・ジャクソン', 'Benjamin Jackson', 2002, '社長。', '社長'),
  P('gardiner', 'ウォーレン・ガーディナー', 'Warren Gardiner', 2008, 'CFO。', 'CFO'),
  P('martin', 'リン・マーティン', 'Lynn Martin', 2018, 'ニューヨーク証券取引所グループの社長。', 'NYSE社長'),
  O('founders', '創業時の出資者', 2000, 'ゴールドマン・サックス、モルガン・スタンレー、BP、シェル、ドイツ銀行、ソシエテ・ジェネラル、トタル。', '創業時の出資者', 'i'),
  O('nybot', 'NYBOT', 2007, '2007年に約10億ドルで買収。', '買収(2007年)'),
  O('nyse', 'NYSE Euronext', 2013, '2013年に約82億ドルで買収。ニューヨーク証券取引所を傘下に。', '買収(2013年)'),
  O('elliemae', 'Ellie Mae', 2020, '2020年に約110億ドルで買収(住宅ローンのソフト)。', '買収(2020年)'),
  O('blackknight', 'Black Knight', 2023, '2023年に約118億ドルで買収。', '買収(2023年)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.7', M), ('Harris Associates', '3.2', M)]),
 [('sprecher', 'jackson', 'link', '経営陣'), ('founders', 'sprecher', 'link', '創業を支援'), ('co', 'nybot', 'owns'), ('co', 'nyse', 'owns'), ('co', 'elliemae', 'owns'), ('co', 'blackknight', 'owns')],
 '2000年にジェフリー・スプレッチャーが創業した取引所の会社。2013年にニューヨーク証券取引所を買収しました。')

# ---------------- Regeneron ----------------
deep('REGN', 'Regeneron', 1988, NOTE + '23andMeの買収競争(2025年)は報道に基づきます。', [
  P('schleifer', 'レナード・シュライファー', 'Leonard Schleifer', 1988, '創業者でCEO。', '創業者 / CEO', None, 1),
  P('yancopoulos', 'ジョージ・ヤンコポロス', 'George Yancopoulos', 1989, '共同創業者の1人で、最高科学責任者(CSO)。', '共同創業者 / CSO', None, 1),
  P('vagelos', 'ロイ・ヴァジェロス', 'Roy Vagelos', 1995, 'メルクの元CEO。1995〜2010年に会長。', '元会長', 2010),
  O('sanofi', 'Sanofi', 2007, '2007年から提携(Dupixent、Praluent)。かつては大株主でした。', '提携先'),
  O('decibel', 'Decibel Therapeutics', 2023, '2023年に約2.1億ドルで買収。', '買収(2023年)'),
  O('23andme', '23andMe', 2025, '2025年の破産手続きでの買収入札に参加したが、他社が落札したと報じられています。', '入札(2025年・報道)'),
  O('merck', 'Merck', 1995, 'ヴァジェロス氏の前職。', '前職'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.5', M), ('Dodge & Cox', '4.8', M)]),
 [('schleifer', 'yancopoulos', 'link', '共同創業'), ('vagelos', 'schleifer', 'link', '会長として支える'), ('vagelos', 'merck', 'moved', '前職'), ('co', 'sanofi', 'link', '提携'), ('co', 'decibel', 'owns'), ('co', '23andme', 'link', '入札')],
 '1988年にレナード・シュライファーらが創業したバイオ医薬の会社。創業者がCEOを務め続けています。')

# ---------------- Quanta Services ----------------
deep('PWR', 'Quanta Services', 1997, NOTE, [
  P('colson', 'ジョン・コルソン', 'John Colson', 1997, '創業者でCEO。のち会長。', '創業者', 2019, 1),
  P('austin', 'アール・"デューク"・オースティン', 'Earl Austin', 1998, '2019年からCEO。', 'CEO'),
  P('jensen', 'デリック・ジェンセン', 'Derrick Jensen', 2005, 'CFO。', 'CFO'),
  O('infrasource', 'InfraSource', 2007, '2007年に買収。', '買収(2007年)'),
  O('blattner', 'Blattner Energy', 2015, '2015年に買収(風力発電の建設)。', '買収(2015年)'),
  O('cupertino', 'Cupertino Electric', 2024, '2024年に約15億ドルで買収。', '買収(2024年)'),
  O('dynamic', 'Dynamic Systems', 2025, '2025年に約13.5億ドルで買収と報じられています。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.5', M), ('Vanguard Portfolio Mgmt', '4.6', M)]),
 [('colson', 'austin', 'link', '後任', 2019), ('co', 'infrasource', 'owns'), ('co', 'blattner', 'owns'), ('co', 'cupertino', 'owns'), ('co', 'dynamic', 'owns')],
 '1997年に創業した、送電網などのインフラ建設の会社。2019年からアール・オースティンがCEOを務めています。')

# ---------------- Constellation Energy ----------------
deep('CEG', 'Constellation Energy', 2022, NOTE + 'Calpineの買収(2025年)は報道に基づきます。', [
  P('dominguez', 'ジョセフ・ドミンゲス', 'Joseph Dominguez', 2022, '2022年の分離独立以来、社長兼CEO。', 'CEO'),
  P('eggers', 'ダン・エガース', 'Dan Eggers', 2022, 'CFO。', 'CFO'),
  O('exelon', 'Exelon', 2022, '2022年2月に発電部門を分離して誕生。', '分離元(2022年)'),
  O('microsoft', 'Microsoft', 2024, '2024年にスリーマイル島原発(Crane Clean Energy Center)の再稼働に向けた長期の電力購入契約。', '顧客(2024年)'),
  O('calpine', 'Calpine', 2025, '2025年に約164億ドルで買収と発表(報道)。', '買収(2025年・報道)'),
  O('ecp', 'Energy Capital Partners', 2026, '約4.1%を持つ上位株主(MarketScreener)。', '株主(約4.1%)', 'i'),
 ] + holders([('Vanguard', '5.9', M), ('State Street', '5.5', M), ('BlackRock', '5.3', M)]),
 [('exelon', 'dominguez', 'link', '分離を率いる'), ('co', 'exelon', 'owns', '分離'), ('co', 'microsoft', 'link', '電力供給'), ('co', 'calpine', 'owns')],
 '2022年にExelonから発電部門を分離して誕生した、米国最大級の原子力発電の会社。ジョセフ・ドミンゲスがCEOを務めています。')

# ---------------- Suncor ----------------
deep('SU', 'Suncor Energy', 1919, NOTE, [
  P('rgeorge', 'リック・ジョージ', 'Rick George', 1991, '1991〜2012年にCEO。', '元CEO', 2012),
  P('swilliams', 'スティーブ・ウィリアムズ', 'Steve Williams', 2012, '2012〜2019年にCEO。', '元CEO', 2019),
  P('little', 'マーク・リトル', 'Mark Little', 2019, '2019〜2023年にCEO。', '元CEO', 2023),
  P('kruger', 'リチャード・クルーガー', 'Richard Kruger', 2023, '2023年4月からCEO。エクソンモービルの元幹部。', 'CEO'),
  P('girling', 'ラッセル・ジャーリング', 'Russell Girling', 2022, '会長。', '会長'),
  O('sunoil', 'Sun Oil Company', 1919, '1919年に設立された米国の石油会社のカナダ事業が源流。', '源流(1919年)'),
  O('gcos', 'Great Canadian Oil Sands', 1967, '1967年に操業を始めたオイルサンドの先駆け。', '源流(1967年)'),
  O('petrocanada', 'Petro-Canada', 2009, '2009年に約190億ドルで合併。', '合併(2009年)'),
  O('totalep', 'Total E&P Canada', 2010, '2010年に買収。', '買収(2010年)'),
  O('elliott', 'Elliott Management', 2026, '約2.5%を持つ株主(MarketScreener)。', '株主(約2.5%)', 'i'),
 ] + holders([('Royal Trust Corporation of Canada', '5.7', M), ('BMO Bank NA', '3.4', M), ('Vanguard', '2.9', M)]),
 [('sunoil', 'rgeorge', 'link', '源流を継ぐ'), ('rgeorge', 'swilliams', 'link', '後任'), ('swilliams', 'little', 'link', '後任'), ('little', 'kruger', 'link', '後任', 2023), ('co', 'sunoil', 'owns'), ('co', 'petrocanada', 'owns'), ('co', 'totalep', 'owns'), ('co', 'gcos', 'owns')],
 '1919年のSun Oilのカナダ事業を源流とする石油・オイルサンドの会社。2023年からリチャード・クルーガーがCEOを務めています。')
