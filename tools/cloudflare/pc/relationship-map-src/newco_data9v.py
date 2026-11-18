from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- MercadoLibre ----------------
deep('MELI', 'MercadoLibre', 1999, NOTE, [
  P('galperin', 'マルコス・ガルペリン', 'Marcos Galperin', 1999, '創業者。会長兼社長兼CEO。スタンフォード大学のMBA在学中に創業。', '創業者 / 会長兼CEO', None, 1),
  P('santos', 'マルティン・デ・ロス・サントス', 'Martin de los Santos', 2012, 'CFO。', 'CFO'),
  O('ebay', 'eBay', 2001, '2001年に約19.5%を出資(のち2016年に売却)。', '元の出資者(2001〜2016年)', 'i'),
  O('trust', 'Galperin Trust', 2026, '約6.7%を持つ最大の株主(MarketScreener)。', '最大の株主(約6.7%)', 'i'),
  O('baillie', 'Baillie Gifford', 2026, '約6.0%を持つ上位株主(MarketScreener)。', '株主(約6.0%)', 'i'),
  O('mercadopago', 'Mercado Pago', 2003, '決済・金融の事業。', '事業'),
 ] + holders([('Capital Group', '6.2', M)]),
 [('galperin', 'ebay', 'link', '出資を受ける', 2001), ('galperin', 'trust', 'link', '創業者の信託'), ('co', 'mercadopago', 'owns')],
 '1999年にマルコス・ガルペリンが創業した、中南米最大級のEC・決済の会社。創業者が会長兼CEOを務めています。')

# ---------------- Comcast ----------------
deep('CMCSA', 'Comcast', 1963, NOTE + 'ケーブルテレビ系事業の分離(2026年)は報道に基づきます。', [
  P('rroberts', 'ラルフ・ロバーツ', 'Ralph Roberts', 1963, '1963年に創業。ブライアン・ロバーツの父。', '創業者', 2015, 1),
  P('broberts', 'ブライアン・ロバーツ', 'Brian Roberts', 1981, '2002年からCEO。会長兼共同CEO。', '会長兼共同CEO'),
  P('cavanagh', 'マイク・カバナー', 'Michael Cavanagh', 2022, '2026年1月から共同CEO(社長も)。', '共同CEO'),
  P('armstrong', 'ジェイソン・アームストロング', 'Jason Armstrong', 2015, 'CFO。', 'CFO'),
  O('attbroadband', 'AT&T Broadband', 2002, '2002年に約470億ドルで買収。', '買収(2002年)'),
  O('nbcu', 'NBCUniversal', 2011, '2011年にGEから過半を取得(約138億ドル)。', '買収(2011年)'),
  O('dreamworks', 'DreamWorks Animation', 2016, '2016年に約38億ドルで買収。', '買収(2016年)'),
  O('sky', 'Sky', 2018, '2018年に約390億ドルで買収。', '買収(2018年)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.4', M), ('State Street', '5.5', M)]),
 [('rroberts', 'broberts', 'link', '親子'), ('broberts', 'cavanagh', 'link', '共同CEO', 2026), ('co', 'attbroadband', 'owns'), ('co', 'nbcu', 'owns'), ('co', 'dreamworks', 'owns'), ('co', 'sky', 'owns')],
 '1963年にラルフ・ロバーツが創業したケーブルとメディアの会社。ブライアン・ロバーツが会長兼共同CEOを務めています。')

# ---------------- Mondelez ----------------
deep('MDLZ', 'Mondelez International', 2012, NOTE + 'ハーシーへの買収提案(2024年)は報道に基づきます。', [
  P('rosenfeld', 'アイリーン・ローゼンフェルド', 'Irene Rosenfeld', 2006, 'Kraft Foodsの会長兼CEO。2012年のMondelez分離後、2017年までCEO。', '元CEO', 2017),
  P('vandeput', 'ディルク・ファン・デ・プット', 'Dirk Van de Put', 2017, '2017年11月からCEO(会長も)。', '会長兼CEO'),
  P('zaramella', 'ルカ・ザラメッラ', 'Luca Zaramella', 2018, 'CFO。', 'CFO'),
  O('kraft', 'Kraft Foods', 2012, '2012年に北米の食品事業を分離し、残りがMondelezに。', '分離元(2012年)'),
  O('cadbury', 'Cadbury', 2010, '2010年に約190億ドルで買収。', '買収(2010年)'),
  O('clif', 'Clif Bar', 2022, '2022年に約29億ドルで買収。', '買収(2022年)'),
  O('hershey', 'Hershey', 2024, '2024年に買収を打診したが、拒否されたと報じられています。', '買収提案(2024年・報道)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.6', M), ('Capital Group', '5.5', M)]),
 [('kraft', 'rosenfeld', 'link', '分離を主導'), ('rosenfeld', 'vandeput', 'link', '後任', 2017), ('co', 'kraft', 'owns', '分離'), ('co', 'cadbury', 'owns'), ('co', 'clif', 'owns'), ('co', 'hershey', 'link', '買収を打診')],
 '2012年にKraft Foodsから分離したスナック・菓子の会社。2017年からディルク・ファン・デ・プットがCEOを務めています。')

# ---------------- Royal Caribbean ----------------
deep('RCL', 'Royal Caribbean', 1968, NOTE, [
  P('wilhelmsen', 'アルネ・アレクサンダー・ウィルヘルムセン', 'Arne Alexander Wilhelmsen', 1968, 'ノルウェーの船主一族。創業時から出資し、約6.1%を保有(MarketScreener)。', '創業家の株主', None, 1),
  P('fain', 'リチャード・フェイン', 'Richard Fain', 1988, '1988〜2022年にCEO。', '元CEO', 2022),
  P('liberty', 'ジェイソン・リバティ', 'Jason Liberty', 2005, '2022年6月からCEO兼会長。', '会長兼CEO'),
  P('holtz', 'ナフタリ・ホルツ', 'Naftali Holtz', 2018, 'CFO。', 'CFO'),
  O('capital', 'Capital Group', 2026, '約12.8%を持つ上位株主(MarketScreener)。', '株主(約12.8%)', 'i'),
  O('celebrity', 'Celebrity Cruises', 1997, '1997年に取得。', '買収(1997年)'),
  O('silversea', 'Silversea Cruises', 2018, '2018年に67%を取得。', '買収(2018年)'),
 ] + holders([('Capital Group', '9.2', M)]),
 [('wilhelmsen', 'fain', 'link', '創業家のパートナー'), ('fain', 'liberty', 'link', '後任', 2022), ('co', 'celebrity', 'owns'), ('co', 'silversea', 'owns')],
 '1968年にノルウェーの船主3社が設立したクルーズの会社。2022年からジェイソン・リバティがCEOを務めています。')

# ---------------- Motorola Solutions ----------------
deep('MSI', 'Motorola Solutions', 1928, NOTE + 'Silvusの買収(2025年)は報道に基づきます。', [
  P('pgalvin', 'ポール・ガルビン', 'Paul Galvin', 1928, '1928年に弟とGalvin Manufacturing(のちのMotorola)を創業。', '創業者', 1959, 1),
  P('jgalvin', 'ジョセフ・ガルビン', 'Joseph Galvin', 1928, '共同創業者(弟)。', '共同創業者', 1944, 1),
  P('zander', 'エド・ザンダー', 'Ed Zander', 2004, '2004〜2008年にCEO。', '元CEO', 2008),
  P('brown', 'グレッグ・ブラウン', 'Greg Brown', 2008, '2008年からCEO(2011年の分離後はMotorola Solutions、会長も)。', '会長兼CEO'),
  P('winkler', 'ジェイソン・ウィンクラー', 'Jason Winkler', 2017, 'CFO。', 'CFO'),
  O('mobility', 'Motorola Mobility', 2011, '2011年に分離。2012年にGoogleが約125億ドルで買収。', '分離(2011年)'),
  O('avigilon', 'Avigilon', 2018, '2018年に約10億ドルで買収。', '買収(2018年)'),
  O('silvus', 'Silvus Technologies', 2025, '2025年に約44億ドルで買収と報じられています。', '買収(2025年・報道)'),
  O('google', 'Google', 2012, 'Motorola Mobilityを買収。', '買収先'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.1', M), ('State Street', '5.1', M)]),
 [('pgalvin', 'jgalvin', 'link', '兄弟で創業'), ('zander', 'brown', 'link', '後任'), ('co', 'mobility', 'owns', '分離'), ('mobility', 'google', 'moved', '売却'), ('co', 'avigilon', 'owns'), ('co', 'silvus', 'owns')],
 '1928年にガルビン兄弟が創業したMotorolaの流れをくむ通信機器の会社。2011年に携帯部門を分離し、グレッグ・ブラウンがCEOを務めています。')

# ---------------- Travelers ----------------
deep('TRV', 'Travelers', 1864, NOTE, [
  P('batterson', 'ジェームズ・バターソン', 'James Batterson', 1864, '1864年にハートフォードでTravelersを創業(米国初の旅行傷害保険)。', '創業者', 1901, 1),
  P('weill', 'サンディ・ワイル', 'Sandy Weill', 1993, 'シティグループの共同創業者。Travelers Group(1993年〜)を率いました。', '元会長', 2005),
  P('fishman', 'ジェイ・フィッシュマン', 'Jay Fishman', 2001, '2001〜2015年にCEO。2016年に亡くなりました。', '元CEO', 2015),
  P('schnitzer', 'アラン・シュニッツァー', 'Alan Schnitzer', 1995, '2015年12月からCEO(会長も)。', '会長兼CEO'),
  P('frey', 'ダニエル・フレイ', 'Daniel Frey', 2016, 'CFO。', 'CFO'),
  O('citi', 'Citigroup', 1993, '1993〜2005年に親会社だった。', '元の親会社(〜2005年)'),
  O('stpaul', 'St. Paul Companies', 2004, '2004年に合併して現在のTravelersに。', '合併(2004年)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.0', M), ('State Street', '5.0', M)]),
 [('batterson', 'fishman', 'link', '源流を継ぐ'), ('weill', 'fishman', 'link', '上場を率いる'), ('fishman', 'schnitzer', 'link', '後任', 2015), ('citi', 'weill', 'link', '合併'), ('co', 'stpaul', 'owns')],
 '1864年創業の損害保険の会社。2004年にSt. Paulと合併し、2015年からアラン・シュニッツァーがCEOを務めています。')

# ---------------- UPS ----------------
deep('UPS', 'UPS', 1907, NOTE + 'アンドラウアーの買収(2025年)は報道に基づきます。', [
  P('casey', 'ジム・ケイシー', 'Jim Casey', 1907, '1907年にシアトルでAmerican Messenger Companyを創業(UPSの源流)。', '創業者', 1962, 1),
  P('ryan', 'クロード・ライアン', 'Claude Ryan', 1907, '共同創業者。', '共同創業者', 1913, 1),
  P('eskew', 'マイク・エスキュー', 'Mike Eskew', 1972, '2002〜2007年にCEO。', '元CEO', 2007),
  P('davis', 'スコット・デイビス', 'Scott Davis', 1986, '2008〜2014年にCEO。', '元CEO', 2014),
  P('abney', 'デビッド・アブニー', 'David Abney', 1974, '2014〜2020年にCEO。', '元CEO', 2020),
  P('tome', 'キャロル・トメ', 'Carol Tome', 2020, '2020年6月からCEO。ホーム・デポの元CFO。', 'CEO'),
  P('johnson', 'ウィリアム・ジョンソン', 'William Johnson', 2017, '会長(英語版Wikipedia)。', '会長'),
  P('dykes', 'ブライアン・ダイクス', 'Brian Dykes', 2024, 'CFO。', 'CFO'),
  O('overnite', 'Overnite', 2005, '2005年に約12.5億ドルで買収(のち売却)。', '買収(2005年)'),
  O('coyote', 'Coyote Logistics', 2015, '2015年に買収。', '買収(2015年)'),
  O('andlauer', 'Andlauer Healthcare', 2025, '2025年に約16億ドルで買収と報じられています。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '6.2', Y), ('BlackRock', '5.2', Y)]),
 [('casey', 'ryan', 'link', '共同創業'), ('eskew', 'davis', 'link', '後任'), ('davis', 'abney', 'link', '後任'), ('abney', 'tome', 'link', '後任', 2020), ('co', 'overnite', 'owns'), ('co', 'coyote', 'owns'), ('co', 'andlauer', 'owns')],
 '1907年にシアトルで始まった宅配・物流の会社。2020年からキャロル・トメがCEOを務めています。')

# ---------------- Sherwin-Williams ----------------
deep('SHW', 'Sherwin-Williams', 1866, NOTE, [
  P('hsherwin', 'ヘンリー・シャーウィン', 'Henry Sherwin', 1866, '1866年にクリーブランドで共同創業。', '共同創業者', 1916, 1),
  P('ewilliams', 'エドワード・ウィリアムズ', 'Edward Williams', 1866, '共同創業者。', '共同創業者', 1900, 1),
  P('morikis', 'ジョン・モリキス', 'John Morikis', 1984, '2016〜2021年にCEO。', '元CEO(執行会長)', 2024),
  P('petz', 'ハイジ・ペッツ', 'Heidi Petz', 1996, '2021年10月からCEO(会長も)。', '会長兼CEO'),
  P('mistysyn', 'アレン・ミスティシン', 'Allen Mistysyn', 2022, 'CFO。', 'CFO'),
  O('valspar', 'Valspar', 2017, '2017年に約113億ドルで買収。', '買収(2017年)'),
  O('esop', '従業員持株制度(ESOP)', 2026, '約6.1%を持つ株主(MarketScreener)。', '株主(約6.1%)', 'i'),
 ] + holders([('State Street', '6.4', M), ('Vanguard', '6.2', M), ('BlackRock', '5.7', M)]),
 [('hsherwin', 'ewilliams', 'link', '共同創業'), ('morikis', 'petz', 'link', '後任', 2021), ('co', 'valspar', 'owns')],
 '1866年にクリーブランドで創業した塗料の会社。2021年からハイジ・ペッツがCEOを務めています。')

# ---------------- Hilton ----------------
deep('HLT', 'Hilton', 1919, NOTE, [
  P('chilton', 'コンラッド・ヒルトン', 'Conrad Hilton', 1919, '1919年にテキサス州で最初のホテルを購入した創業者。', '創業者', 1979, 1),
  P('barron', 'バロン・ヒルトン', 'Barron Hilton', 1966, '創業者の息子。長く会長。', '元会長', 2007),
  P('nassetta', 'クリス・ナセッタ', 'Chris Nassetta', 2007, '2007年からCEO(社長も)。', '社長兼CEO'),
  P('gray', 'ジョナサン・グレイ', 'Jonathan Gray', 2007, '会長。Blackstoneの社長兼COO。', '会長'),
  P('jacobs', 'ケビン・ジェイコブス', 'Kevin Jacobs', 2013, 'CFO。', 'CFO'),
  O('blackstone', 'Blackstone', 2007, '2007年に約260億ドルのLBOで買収し、2013年に再上場。', '元の買い手(2007年)', 'i'),
  O('hna', 'HNAグループ', 2016, '2016〜2017年にブラックストーンから約25%を取得(のち売却)。', '元の出資者', 'i'),
  O('promus', 'Promus Hotel', 1999, '1999年に買収(Doubletreeなど)。', '買収(1999年)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.1', M), ('Fidelity', '5.0', M)]),
 [('chilton', 'barron', 'link', '親子'), ('blackstone', 'nassetta', 'link', 'CEOを維持'), ('gray', 'blackstone', 'link', '社長'), ('co', 'promus', 'owns')],
 '1919年にコンラッド・ヒルトンが創業したホテルの会社。2013年に再上場し、クリス・ナセッタが2007年からCEOを務めています。')

# ---------------- SLB ----------------
deep('SLB', 'SLB', 1926, NOTE, [
  P('conrad', 'コンラッド・シュルンベルジェ', 'Conrad Schlumberger', 1926, '1926年に兄弟で創業。', '共同創業者', 1936, 1),
  P('marcel', 'マルセル・シュルンベルジェ', 'Marcel Schlumberger', 1926, '共同創業者。', '共同創業者', 1953, 1),
  P('riboud', 'ジャン・リブー', 'Jean Riboud', 1965, '1965〜1985年にCEO。', '元CEO', 1985),
  P('gould', 'アンドリュー・グールド', 'Andrew Gould', 2003, '2003〜2011年にCEO。', '元CEO', 2011),
  P('kibsgaard', 'ポール・キブスゴー', 'Paal Kibsgaard', 2011, '2011〜2019年にCEO。', '元CEO', 2019),
  P('lepeuch', 'オリビエ・ル・ペシュ', 'Olivier Le Peuch', 2019, '2019年8月からCEO。', 'CEO'),
  P('hackett', 'ジェームズ・ハケット', 'James Hackett', 2019, '会長。アナダルコの元CEO。', '会長'),
  O('smith', 'Smith International', 2010, '2010年に約113億ドルで買収。', '買収(2010年)'),
  O('cameron', 'Cameron International', 2016, '2016年に約148億ドルで買収。', '買収(2016年)'),
  O('championx', 'ChampionX', 2025, '2025年に約78億ドルで買収と報じられています。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '6.6', M), ('State Street', '6.1', M), ('BlackRock', '5.7', M)]),
 [('conrad', 'marcel', 'link', '兄弟で創業'), ('riboud', 'gould', 'link'), ('gould', 'kibsgaard', 'link', '後任'), ('kibsgaard', 'lepeuch', 'link', '後任', 2019), ('co', 'smith', 'owns'), ('co', 'cameron', 'owns'), ('co', 'championx', 'owns')],
 '1926年にシュルンベルジェ兄弟が創業した油田サービスの会社(旧Schlumberger)。2019年からオリビエ・ル・ペシュがCEOを務めています。')
