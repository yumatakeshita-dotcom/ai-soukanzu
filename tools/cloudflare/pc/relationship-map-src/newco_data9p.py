from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Duke Energy ----------------
deep('DUK', 'Duke Energy', 1904, NOTE, [
  P('jbduke', 'ジェームズ・B・デューク', 'James B. Duke', 1904, '1904年にSouthern Power(のちDuke Power)を創業した実業家。', '創業者', 1925, 1),
  P('rogers', 'ジム・ロジャース', 'Jim Rogers', 2006, '2006〜2013年にCEO。', '元CEO', 2013),
  P('good', 'リン・グッド', 'Lynn Good', 2009, '2013〜2024年にCEO。', '元CEO', 2025),
  P('sideris', 'ハリー・サイデリス', 'Harry Sideris', 2025, '2025年からCEO兼会長(英語版Wikipedia)。', '会長兼CEO'),
  P('savoy', 'ブライアン・サボイ', 'Brian Savoy', 2014, 'CFO。', 'CFO'),
  O('cinergy', 'Cinergy', 2006, '2006年に合併。', '合併(2006年)'),
  O('progress', 'Progress Energy', 2012, '2012年に約260億ドルで合併。', '合併(2012年)'),
  O('piedmont', 'Piedmont Natural Gas', 2016, '2016年に約49億ドルで買収。', '買収(2016年)'),
 ] + holders([('BlackRock', '7.6', M), ('Vanguard', '6.5', M), ('State Street', '5.8', M)]),
 [('jbduke', 'rogers', 'link', '源流を継ぐ'), ('rogers', 'good', 'link', '後任'), ('good', 'sideris', 'link', '後任', 2025), ('co', 'cinergy', 'owns'), ('co', 'progress', 'owns'), ('co', 'piedmont', 'owns')],
 '1904年にジェームズ・B・デュークが創業した電力会社を源流とする大手。2025年からハリー・サイデリスがCEOを務めています。')

# ---------------- HCA Healthcare ----------------
deep('HCA', 'HCA Healthcare', 1968, NOTE + 'Frisco Holding IIとHercules Holding IIは、2006年の非公開化の出資者の保有会社と見られます(MarketScreener)。', [
  P('frist', 'トーマス・フリスト・シニア', 'Thomas Frist Sr.', 1968, '1968年にHospital Corporation of Americaを共同創業した医師。', '共同創業者', 1990, 1),
  P('fristjr', 'トーマス・フリスト・ジュニア', 'Thomas Frist Jr.', 1968, '共同創業者。のち会長兼CEO。上院議員ビル・フリストの兄。', '共同創業者', 2001, 1),
  P('massey', 'ジャック・マッシー', 'Jack Massey', 1968, '共同創業者の投資家。ケンタッキーフライドチキンの再建でも知られます。', '共同創業者', 1990, 1),
  P('scott', 'リック・スコット', 'Rick Scott', 1987, '1987〜1997年にCEO。のちフロリダ州知事・米上院議員。', '元CEO', 1997),
  P('bovender', 'ジャック・ボベンダー', 'Jack Bovender', 1992, '2001〜2009年にCEO。', '元CEO', 2009),
  P('bracken', 'リチャード・ブラッケン', 'Richard Bracken', 2009, '2009〜2018年にCEO。', '元CEO', 2018),
  P('hazen', 'サム・ヘイゼン', 'Sam Hazen', 1982, '2018年からCEO。', 'CEO'),
  O('columbia', 'Columbia Healthcare', 1994, '1994年に合併(Columbia/HCA)。', '合併(1994年)'),
  O('frisco', 'Frisco Holding II', 2006, '約16.9%を持つ株主(MarketScreener)。', '株主(約16.9%)', 'i'),
  O('hercules', 'Hercules Holding II', 2006, '約14.9%を持つ株主(MarketScreener)。', '株主(約14.9%)', 'i'),
  O('lbo', 'ベインキャピタル・KKR・メリルリンチ', 2006, '2006年に約330億ドルの非公開化(LBO)で、フリスト家とともに出資。', 'LBOの出資者(2006年)', 'i'),
 ] + holders([('Vanguard', '4.7', M), ('BlackRock', '4.5', M), ('Sanders Capital', '4.1', M)]),
 [('frist', 'fristjr', 'link', '親子'), ('frist', 'massey', 'link', '共同創業'), ('fristjr', 'scott', 'link', '後任'), ('scott', 'bovender', 'link'), ('bovender', 'bracken', 'link', '後任'), ('bracken', 'hazen', 'link', '後任', 2018), ('co', 'columbia', 'owns')],
 '1968年にナッシュビルで創業した病院運営の会社。2018年からサム・ヘイゼンがCEOを務めています。')

# ---------------- Adobe ----------------
deep('ADBE', 'Adobe', 1982, NOTE + '新CEO(2026年12月1日付)は、英語版Wikipediaの記載に基づきます。', [
  P('warnock', 'ジョン・ワーノック', 'John Warnock', 1982, '共同創業者。PostScriptを開発。', '共同創業者', 2017, 1),
  P('geschke', 'チャールズ・ゲシキ', 'Charles Geschke', 1982, '共同創業者。', '共同創業者', 2021, 1),
  P('chizen', 'ブルース・チゼン', 'Bruce Chizen', 1994, '2000〜2007年にCEO。', '元CEO', 2007),
  P('narayen', 'シャンタヌ・ナラヤン', 'Shantanu Narayen', 1998, '2007年からCEO兼会長。2026年12月1日にCEOを退く予定。', '会長兼CEO'),
  P('chakravarthy', 'アニル・チャクラヴァルティ', 'Anil Chakravarthy', 2021, '2026年12月1日付で社長兼CEOに就任予定。', '次期CEO'),
  P('durn', 'ダン・ダーン', 'Dan Durn', 2018, 'CFO。', 'CFO'),
  O('macromedia', 'Macromedia', 2005, '2005年に約34億ドルで買収(Flash、Dreamweaver)。', '買収(2005年)'),
  O('omniture', 'Omniture', 2009, '2009年に約18億ドルで買収。', '買収(2009年)'),
  O('marketo', 'Marketo', 2018, '2018年に約47.5億ドルで買収。', '買収(2018年)'),
  O('workfront', 'Workfront', 2020, '2020年に約15億ドルで買収。', '買収(2020年)'),
  O('frameio', 'Frame.io', 2021, '2021年に約12.8億ドルで買収。', '買収(2021年)'),
  O('figma', 'Figma', 2022, '2022年に約200億ドルでの買収を発表したが、規制当局の懸念で2023年12月に断念。違約金は10億ドル。', '買収断念(2023年)'),
 ] + holders([('BlackRock', '7.7', M), ('Vanguard', '6.8', M), ('State Street', '5.3', M)]),
 [('warnock', 'geschke', 'link', '共同創業'), ('chizen', 'narayen', 'link', '後任', 2007), ('narayen', 'chakravarthy', 'link', 'CEO交代(予定)', 2026), ('co', 'macromedia', 'owns'), ('co', 'omniture', 'owns'), ('co', 'marketo', 'owns'), ('co', 'workfront', 'owns'), ('co', 'frameio', 'owns'), ('co', 'figma', 'link', '買収を断念')],
 '1982年にジョン・ワーノックとチャールズ・ゲシキが創業したクリエイティブソフトの会社。2026年12月にアニル・チャクラヴァルティがCEOへ就任する予定です。')

# ---------------- CSX ----------------
deep('CSX', 'CSX', 1980, NOTE, [
  P('ward', 'マイケル・ウォード', 'Michael Ward', 1981, '2003〜2017年にCEO。', '元CEO', 2017),
  P('harrison', 'ハンター・ハリソン', 'Hunter Harrison', 2017, '2017年にCEO。鉄道の効率化で知られる人物で、同年12月に亡くなりました。', '元CEO', 2017),
  P('hinrichs', 'ジョー・ヒンリクス', 'Joe Hinrichs', 2022, '2022〜2025年にCEO。', '元CEO', 2025),
  P('angel', 'スティーブ・エンジェル', 'Steve Angel', 2025, '2025年9月からCEO(Linde plcの元CEO)。', 'CEO'),
  P('zillmer', 'ジョン・ジルマー', 'John Zillmer', 2019, '会長。', '会長'),
  O('chessie', 'Chessie System', 1980, '1980年にSeaboard Coast Lineと合併して誕生。', '合併(1980年)'),
  O('seaboard', 'Seaboard Coast Line', 1980, '1980年にChessie Systemと合併。', '合併(1980年)'),
  O('mantle', 'Mantle Ridge', 2017, 'アクティビスト。2017年にハンター・ハリソン氏のCEO就任を実現。', '株主(2017年)', 'i'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.4', M), ('State Street', '4.9', M)]),
 [('ward', 'harrison', 'link', '後任', 2017), ('mantle', 'harrison', 'link', 'CEOに迎える', 2017), ('harrison', 'hinrichs', 'link', '後任'), ('hinrichs', 'angel', 'link', '後任', 2025), ('co', 'chessie', 'owns'), ('co', 'seaboard', 'owns')],
 '1980年にチェシー・システムとシーボード・コーストラインが合併して誕生した鉄道会社。2025年9月からスティーブ・エンジェルがCEOを務めています。')

# ---------------- Marsh McLennan ----------------
deep('MRSH', 'Marsh McLennan', 1905, NOTE, [
  P('hmarsh', 'ヘンリー・マーシュ', 'Henry Marsh', 1905, '1905年にMarshを共同創業。', '共同創業者', 1923, 1),
  P('mclennan', 'ドナルド・マクレナン', 'Donald McLennan', 1905, '1923年にMarshと合併したMcLennanの創業者。', '共同創業者', 1940, 1),
  P('jgreenberg', 'ジェフリー・グリーンバーグ', 'Jeffrey Greenberg', 1999, '1999〜2004年にCEO。ニューヨーク州司法長官の調査の中で退任。', '元CEO', 2004),
  P('cherkasky', 'マイケル・チェルカスキー', 'Michael Cherkasky', 2004, '2004〜2008年にCEO。', '元CEO', 2008),
  P('duperreault', 'ブライアン・デュペロー', 'Brian Duperreault', 2008, '2008〜2012年にCEO。', '元CEO', 2012),
  P('glaser', 'ダン・グレイザー', 'Dan Glaser', 1982, '2013〜2025年にCEO。', '元CEO', 2025),
  P('doyle', 'ジョン・Q・ドイル', 'John Q. Doyle', 2011, '現CEO(英語版Wikipedia)。', 'CEO'),
  P('hanway', 'エドワード・ハンウェイ', 'H. Edward Hanway', 2012, '会長(英語版Wikipedia)。', '会長'),
  P('burke', 'ドミニク・バーク', 'Dominick Burke', 2013, '副会長(英語版Wikipedia)。', '副会長'),
  O('mercer', 'Mercer', 1959, '1959年に取得(人事コンサルティング)。', '買収(1959年)'),
  O('oliverwyman', 'Oliver Wyman', 2003, '2003年に買収(コンサルティング)。', '買収(2003年)'),
  O('jlt', 'Jardine Lloyd Thompson', 2019, '2019年に約56億ドルで買収。', '買収(2019年)'),
  O('spitzer', 'ニューヨーク州司法長官の調査', 2004, '2004年に保険料の不透明な手数料問題で調査を受け、約8.5億ドルで和解。', '調査(2004年)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.1', M), ('State Street', '4.7', M)]),
 [('hmarsh', 'mclennan', 'link', '1923年に合併'), ('jgreenberg', 'cherkasky', 'link', '後任', 2004), ('cherkasky', 'duperreault', 'link', '後任'), ('duperreault', 'glaser', 'link', '後任', 2013), ('glaser', 'doyle', 'link', '後任', 2025), ('co', 'mercer', 'owns'), ('co', 'oliverwyman', 'owns'), ('co', 'jlt', 'owns'), ('jgreenberg', 'spitzer', 'link', '調査の対象')],
 '1905年のMarshと1923年に合併したMcLennanを源流とする保険仲介・コンサルティングの会社。ジョン・Q・ドイルがCEOを務めています。')
