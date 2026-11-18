from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Bank of Nova Scotia ----------------
deep('BNS', 'Scotiabank', 1832, NOTE + '歴代の経営者以外の情報は少なく、確認できた範囲だけを載せています。', [
  P('godsoe', 'ピーター・ゴッドソー', 'Peter Godsoe', 1995, '1995〜2003年にCEO。', '元CEO', 2003),
  P('waugh', 'リック・ウォー', 'Rick Waugh', 2003, '2003〜2013年にCEO。', '元CEO', 2013),
  P('porter', 'ブライアン・ポーター', 'Brian Porter', 2013, '2013〜2023年にCEO。', '元CEO', 2023),
  P('thomson', 'スコット・トムソン', 'Scott Thomson', 2023, '2023年2月からCEO。', 'CEO'),
  P('viswanathan', 'ラジ・ビスワナタン', 'Raj Viswanathan', 2024, 'CFO。', 'CFO'),
  O('halifax', 'Bank of Nova Scotia (Halifax)', 1832, '1832年にハリファックスで創業。', '源流(1832年)'),
  O('ingdirectca', 'ING Direct Canada', 2012, '2012年に約31億カナダドルで買収。', '買収(2012年)'),
  O('keycorp', 'KeyCorp', 2024, '2024年に約28億ドルで約15%の株式を取得と報じられています。', '出資(2024年・報道)'),
 ] + holders([('Royal Trust Corporation of Canada', '5.3', M), ('BMO Bank NA', '3.9', M), ('Vanguard', '2.9', M)]),
 [('halifax', 'godsoe', 'link', '源流を継ぐ'), ('godsoe', 'waugh', 'link', '後任'), ('waugh', 'porter', 'link', '後任'), ('porter', 'thomson', 'link', '後任', 2023), ('co', 'ingdirectca', 'owns'), ('co', 'keycorp', 'invest2', '出資')],
 '1832年にハリファックスで創業したカナダの銀行。2023年からスコット・トムソンがCEOを務めています。')

# ---------------- CVS Health ----------------
deep('CVS', 'CVS Health', 1963, NOTE, [
  P('sgoldstein', 'スタンリー・ゴールドスタイン', 'Stanley Goldstein', 1963, '1963年にConsumer Value Storesを共同創業。', '共同創業者', 1990, 1),
  P('sidgoldstein', 'シドニー・ゴールドスタイン', 'Sidney Goldstein', 1963, '共同創業者。', '共同創業者', 1990, 1),
  P('hoagland', 'ラルフ・ホーグランド', 'Ralph Hoagland', 1963, '共同創業者。', '共同創業者', 1980, 1),
  P('ryan', 'トム・ライアン', 'Tom Ryan', 1998, '1998〜2010年にCEO。', '元CEO', 2010),
  P('merlo', 'ラリー・マーロ', 'Larry Merlo', 1990, '2011〜2021年にCEO。', '元CEO', 2021),
  P('lynch', 'カレン・リンチ', 'Karen Lynch', 2018, '2021〜2024年にCEO。', '元CEO', 2024),
  P('joyner', 'デビッド・ジョイナー', 'David Joyner', 2019, '2024年10月からCEO(2025年から会長も)。', '会長兼CEO'),
  P('newman', 'ブライアン・ニューマン', 'Brian Newman', 2024, 'CFO(MarketScreener)。', 'CFO'),
  O('caremark', 'Caremark', 2007, '2007年に約210億ドルで合併。', '合併(2007年)'),
  O('omnicare', 'Omnicare', 2015, '2015年に約127億ドルで買収。', '買収(2015年)'),
  O('targetpharm', 'Targetの薬局事業', 2015, '2015年に約19億ドルで買収。', '買収(2015年)'),
  O('aetna', 'Aetna', 2018, '2018年に約690億ドルで買収。', '買収(2018年)'),
  O('oak', 'Oak Street Health', 2023, '2023年に約106億ドルで買収。', '買収(2023年)'),
  O('signify', 'Signify Health', 2023, '2023年に約80億ドルで買収。', '買収(2023年)'),
 ] + holders([('BlackRock', '6.7', M), ('Vanguard', '6.5', M), ('Capital Group', '5.9', M), ('Dodge & Cox', '3.9', M)]),
 [('sgoldstein', 'sidgoldstein', 'link', '共同創業'), ('sgoldstein', 'hoagland', 'link', '共同創業'), ('ryan', 'merlo', 'link', '後任'), ('merlo', 'lynch', 'link', '後任', 2021), ('lynch', 'joyner', 'link', '後任', 2024), ('co', 'caremark', 'owns'), ('co', 'omnicare', 'owns'), ('co', 'targetpharm', 'owns'), ('co', 'aetna', 'owns'), ('co', 'oak', 'owns'), ('co', 'signify', 'owns')],
 '1963年にConsumer Value Storesとして創業したドラッグストアと医療保険の会社。2024年10月からデビッド・ジョイナーがCEOを務めています。')

# ---------------- Parker Hannifin ----------------
deep('PH', 'Parker Hannifin', 1917, NOTE, [
  P('aparker', 'アーサー・パーカー', 'Arthur Parker', 1917, '1917年にParker Applianceを創業。', '創業者', 1950, 1),
  P('washkewicz', 'ドン・ワシュケウィッツ', 'Don Washkewicz', 1983, '2001〜2015年にCEO。', '元CEO', 2015),
  P('williams', 'トム・ウィリアムズ', 'Tom Williams', 1988, '2015〜2023年にCEO。', '元CEO', 2023),
  P('parmentier', 'ジェニファー・パーメンティア', 'Jennifer Parmentier', 1993, '2023年からCEO(会長も)。', '会長兼CEO'),
  P('leombruno', 'トッド・レオンブルーノ', 'Todd Leombruno', 1996, 'CFO。', 'CFO'),
  O('clarcor', 'CLARCOR', 2017, '2017年に約43億ドルで買収。', '買収(2017年)'),
  O('lord', 'LORD Corporation', 2019, '2019年に約37億ドルで買収。', '買収(2019年)'),
  O('meggitt', 'Meggitt', 2022, '2022年に約88億ドルで買収(英国)。', '買収(2022年)'),
 ] + holders([('State Street', '7.4', M), ('Vanguard', '6.5', M), ('BlackRock', '6.4', M)]),
 [('aparker', 'washkewicz', 'link', '源流'), ('washkewicz', 'williams', 'link', '後任'), ('williams', 'parmentier', 'link', '後任', 2023), ('co', 'clarcor', 'owns'), ('co', 'lord', 'owns'), ('co', 'meggitt', 'owns')],
 '1917年創業のモーション・制御機器の会社。2023年からジェニファー・パーメンティアがCEOを務めています。')

# ---------------- Enbridge ----------------
deep('ENB', 'Enbridge', 1949, NOTE, [
  P('daniel', 'パット・ダニエル', 'Pat Daniel', 1991, '2001〜2012年にCEO。', '元CEO', 2012),
  P('monaco', 'アル・モナコ', 'Al Monaco', 1995, '2012〜2022年にCEO。', '元CEO', 2022),
  P('ebel', 'グレッグ・イーベル', 'Greg Ebel', 2017, '2023年1月からCEO。', 'CEO'),
  P('murray', 'パット・マレー', 'Pat Murray', 2017, 'CFO。', 'CFO'),
  O('ipl', 'Interprovincial Pipe Line', 1949, '1949年に設立された源流の会社。', '源流(1949年)'),
  O('spectra', 'Spectra Energy', 2017, '2017年に約280億ドルで統合。', '統合(2017年)'),
  O('dominion', 'Dominionのガス事業(米国)', 2023, '2023年に3つの米国ガス事業を約140億ドルで買収と発表。', '買収(2023年)'),
 ] + holders([('Royal Trust Corporation of Canada', '4.9', M), ('Vanguard', '2.8', M), ('BMO Bank NA', '2.5', M)]),
 [('ipl', 'daniel', 'link', '源流を継ぐ'), ('daniel', 'monaco', 'link', '後任'), ('monaco', 'ebel', 'link', '後任', 2023), ('co', 'spectra', 'owns'), ('co', 'dominion', 'owns')],
 '1949年のInterprovincial Pipe Lineを源流とするパイプライン大手。2023年からグレッグ・イーベルがCEOを務めています。')

# ---------------- Stryker ----------------
deep('SYK', 'Stryker', 1941, NOTE, [
  P('hstryker', 'ホーマー・ストライカー', 'Homer Stryker', 1941, '1941年に創業した整形外科医。', '創業者', 1980, 1),
  P('jwbrown', 'ジョン・W・ブラウン', 'John W. Brown', 1977, '1977〜2003年にCEO。約5.2%を保有(MarketScreener)。', '元CEO・名誉会長', 2003),
  P('macmillan', 'スティーブン・マクミラン', 'Stephen MacMillan', 2003, '2005〜2012年にCEO。', '元CEO', 2012),
  P('lobo', 'ケビン・ロボ', 'Kevin Lobo', 2011, '2012年からCEO(会長も)。', '会長兼CEO'),
  P('scannell', 'ティモシー・スキャネル', 'Timothy Scannell', 1999, '社長兼COO。', '社長兼COO'),
  P('rstryker', 'ロンダ・ストライカー', 'Ronda Stryker', 1984, '創業者の孫。取締役。', '取締役'),
  P('boehnlein', 'グレン・ボーンライン', 'Glenn Boehnlein', 2007, 'CFO。', 'CFO'),
  O('mako', 'Mako Surgical', 2013, '2013年に約16.5億ドルで買収(ロボット)。', '買収(2013年)'),
  O('wright', 'Wright Medical', 2020, '2020年に約54億ドルで買収。', '買収(2020年)'),
  O('vocera', 'Vocera', 2022, '2022年に約30億ドルで買収。', '買収(2022年)'),
  O('inari', 'Inari Medical', 2025, '2025年に約49億ドルで買収と報じられています。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '6.0', M), ('BlackRock', '5.3', M), ('JPMorgan Asset Mgmt', '4.5', M)]),
 [('hstryker', 'jwbrown', 'link', '源流'), ('jwbrown', 'macmillan', 'link', '後任'), ('macmillan', 'lobo', 'link', '後任', 2012), ('hstryker', 'rstryker', 'link', '孫'), ('co', 'mako', 'owns'), ('co', 'wright', 'owns'), ('co', 'vocera', 'owns'), ('co', 'inari', 'owns')],
 '1941年にホーマー・ストライカーが創業した整形外科・医療機器の会社。2012年からケビン・ロボがCEOを務め、創業家が影響力を持ちます。')

# ---------------- Valero ----------------
deep('VLO', 'Valero Energy', 1980, NOTE, [
  P('greehey', 'ビル・グリーヒー', 'Bill Greehey', 1979, '1979〜2005年にCEO。Valeroを大手に育てました。', '元CEO', 2005),
  P('klesse', 'ビル・クレッセ', 'Bill Klesse', 2005, '2005〜2014年にCEO。', '元CEO', 2014),
  P('gorder', 'ジョー・ゴーダー', 'Joe Gorder', 2014, '2014〜2025年にCEO。', '元CEO', 2026),
  P('riggs', 'レーン・リッグス', 'Lane Riggs', 2026, '2026年からCEO(英語版Wikipedia)。', 'CEO'),
  P('bhullar', 'ホーマー・ブラー', 'Homer Bhullar', 2020, 'CFO。', 'CFO'),
  O('udscorp', 'Ultramar Diamond Shamrock', 2001, '2001年に約60億ドルで買収。', '買収(2001年)'),
  O('premcor', 'Premcor', 2005, '2005年に約80億ドルで買収。', '買収(2005年)'),
 ] + holders([('BlackRock', '6.7', M), ('Vanguard', '6.7', M), ('State Street', '6.6', M)]),
 [('greehey', 'klesse', 'link', '後任'), ('klesse', 'gorder', 'link', '後任'), ('gorder', 'riggs', 'link', '後任', 2026), ('co', 'udscorp', 'owns'), ('co', 'premcor', 'owns')],
 '1980年に設立された石油精製の会社。2026年からレーン・リッグスがCEOを務めています。')

# ---------------- Booking Holdings ----------------
deep('BKNG', 'Booking Holdings', 1996, NOTE, [
  P('bruinsma', 'ヘールト＝ヤン・ブルインスマ', 'Geert-Jan Bruinsma', 1996, 'Booking.com(オランダ、1996年)の創業者。', 'Booking.com創業者', 2005, 1),
  P('walker', 'ジェイ・ウォーカー', 'Jay Walker', 1997, 'Priceline.comの創業者。', 'Priceline創業者', 2000, 1),
  P('boyd', 'ジェフ・ボイド', 'Jeff Boyd', 2002, '2013〜2016年にCEO。', '元CEO', 2016),
  P('fogel', 'グレン・フォーゲル', 'Glenn Fogel', 2016, '2017年からCEO。', 'CEO'),
  P('mylod', 'ロバート・マイロッド', 'Robert Mylod', 2013, '会長。', '会長'),
  O('priceline', 'Priceline', 1997, '1997年創業。2005年にBooking.comを買収し、のち社名をBooking Holdingsへ。', '前身'),
  O('bookingcom', 'Booking.com', 2005, '2005年に約1.33億ドルで買収。', '買収(2005年)'),
  O('agoda', 'Agoda', 2007, '2007年に買収(アジア)。', '買収(2007年)'),
  O('kayak', 'KAYAK', 2013, '2013年に約18億ドルで買収。', '買収(2013年)'),
  O('opentable', 'OpenTable', 2014, '2014年に約26億ドルで買収。', '買収(2014年)'),
 ] + holders([('Vanguard', '6.4', M), ('BlackRock', '5.9', M), ('State Street', '4.4', M)]),
 [('walker', 'priceline', 'link', '創業'), ('boyd', 'fogel', 'link', '後任', 2017), ('bruinsma', 'bookingcom', 'link', '創業'), ('co', 'priceline', 'owns'), ('co', 'bookingcom', 'owns'), ('co', 'agoda', 'owns'), ('co', 'kayak', 'owns'), ('co', 'opentable', 'owns')],
 'Priceline.comがBooking.comなどを買収して成長した旅行予約の会社。2017年からグレン・フォーゲルがCEOを務めています。')

# ---------------- Newmont ----------------
deep('NEM', 'Newmont', 1916, NOTE, [
  P('thompson', 'ウィリアム・ボイス・トンプソン', 'William Boyce Thompson', 1916, '1916年にNewmont Mining Corporationを創業。', '創業者', 1930, 1),
  P('goldberg', 'ゲイリー・ゴールドバーグ', 'Gary Goldberg', 2013, '2013〜2019年にCEO。', '元CEO', 2019),
  P('palmer', 'トム・パーマー', 'Tom Palmer', 2019, '2019年から2025年初めまでCEO。Goldcorp(2019年)とNewcrest(2023年)の買収を主導。', '元CEO', 2025),
  P('viljoen', 'ナターシャ・ビルジョーン', 'Natascha Viljoen', 2025, '2025年からCEO(英語版Wikipedia)。', 'CEO'),
  P('boyce', 'グレゴリー・ボイス', 'Gregory Boyce', 2019, '会長。', '会長'),
  O('goldcorp', 'Goldcorp', 2019, '2019年に約100億ドルで買収。', '買収(2019年)'),
  O('newcrest', 'Newcrest Mining', 2023, '2023年に約168億ドルで買収(豪州)。', '買収(2023年)'),
 ] + holders([('BlackRock', '7.4', M), ('Vanguard', '6.6', M), ('State Street', '5.0', M)]),
 [('thompson', 'goldberg', 'link', '源流'), ('goldberg', 'palmer', 'link', '後任', 2019), ('palmer', 'viljoen', 'link', '後任', 2025), ('co', 'goldcorp', 'owns'), ('co', 'newcrest', 'owns')],
 '1916年創業の世界最大級の金鉱山会社。2025年からナターシャ・ビルジョーンがCEOを務めています。')

# ---------------- Phillips 66 ----------------
deep('PSX', 'Phillips 66', 2012, NOTE + 'エリオットの出資と取締役の提案(2025年)は報道に基づきます。', [
  P('garland', 'グレッグ・ガーランド', 'Greg Garland', 2012, '2012〜2022年にCEO。', '元CEO', 2022),
  P('lashier', 'マーク・ラシア', 'Mark Lashier', 2022, '2022年7月からCEO兼会長。', '会長兼CEO'),
  P('mitchell', 'ケビン・ミッチェル', 'Kevin Mitchell', 2015, 'CFO。', 'CFO'),
  O('conoco', 'ConocoPhillips', 2012, '2012年に精製・販売部門を分離して誕生。', '分離元(2012年)'),
  O('cpchem', 'Chevron Phillips Chemical', 2000, 'シェブロンと50%ずつの化学の合弁会社。', '合弁(50%)'),
  O('dcp', 'DCP Midstream', 2017, 'ガス処理の子会社(2023年に完全子会社化)。', '子会社'),
  O('elliott', 'Elliott Management', 2025, '2025年に出資し、取締役の提案を行ったと報じられています。約4.8%を持つ株主(MarketScreener)。', '株主(約4.8%・アクティビスト)', 'i'),
 ] + holders([('BlackRock', '7.0', M), ('Vanguard', '6.6', M), ('State Street', '6.5', M)]),
 [('conoco', 'garland', 'link', '分離を率いる'), ('garland', 'lashier', 'link', '後任', 2022), ('co', 'cpchem', 'invest2', '50%出資'), ('co', 'dcp', 'owns')],
 '2012年にコノコフィリップスから分離した石油精製・化学の会社。2022年からマーク・ラシアがCEOを務めています。')

# ---------------- ServiceNow ----------------
deep('NOW', 'ServiceNow', 2004, NOTE + 'Armisの買収(2025年)は報道に基づきます。', [
  P('luddy', 'フレッド・ラディ', 'Fred Luddy', 2004, '創業者。会長。', '創業者 / 会長', None, 1),
  P('slootman', 'フランク・スルートマン', 'Frank Slootman', 2011, '2011〜2017年にCEO。のちSnowflakeのCEO・会長。', '元CEO', 2017),
  P('donahoe', 'ジョン・ドナホー', 'John Donahoe', 2017, '2017〜2019年にCEO。のちNikeのCEO。', '元CEO', 2019),
  P('mcdermott', 'ビル・マクダーモット', 'Bill McDermott', 2019, '2019年11月からCEO兼会長。SAPの元CEO。', '会長兼CEO'),
  P('mastantuono', 'ジーナ・マスタントゥオーノ', 'Gina Mastantuono', 2019, 'CFO(のち社長兼CFO)。', 'CFO'),
  O('elementai', 'Element AI', 2020, '2020年に買収(カナダのAI)。', '買収(2020年)'),
  O('moveworks', 'Moveworks', 2025, '2025年に約28.5億ドルで買収と報じられています。', '買収(2025年・報道)'),
  O('armis', 'Armis', 2025, '2025年に約77.5億ドルで買収と報じられています。', '買収(2025年・報道)'),
  O('snowflake', 'Snowflake', 2019, 'スルートマン氏が率いる別会社。', '関連'),
 ] + holders([('BlackRock', '6.7', M), ('Vanguard', '6.5', M), ('State Street', '4.5', M)]),
 [('luddy', 'slootman', 'link', '経営を託す'), ('slootman', 'donahoe', 'link', '後任'), ('donahoe', 'mcdermott', 'link', '後任', 2019), ('slootman', 'snowflake', 'moved', 'CEOに就任'), ('co', 'elementai', 'owns'), ('co', 'moveworks', 'owns'), ('co', 'armis', 'owns')],
 '2004年にフレッド・ラディが創業したワークフローのクラウドの会社。2019年11月からビル・マクダーモットがCEOを務めています。')
