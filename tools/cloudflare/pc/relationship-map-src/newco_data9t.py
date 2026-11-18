from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Vertiv ----------------
deep('VRT', 'Vertiv', 2016, NOTE, [
  P('johnson', 'ロブ・ジョンソン', 'Rob Johnson', 2016, '2016〜2019年にCEO(Emersonから独立した初代)。', '元CEO', 2019),
  P('albertazzi', 'ジョルダーノ・アルベルタッツィ', 'Giordano Albertazzi', 2019, '2020年からCEO。', 'CEO'),
  P('cote', 'デビッド・コート', 'David Cote', 2020, '会長。ハネウェルの元CEO。2020年のSPAC上場を主導。', '会長'),
  O('emerson', 'Emerson', 2016, 'Emerson Network Powerとして、2016年にPlatinum Equityへ約40億ドルで売却。', '元の親会社'),
  O('platinum', 'Platinum Equity', 2016, '2016年に約40億ドルで買収。', '出資者(2016年)', 'i'),
  O('spac', 'GS Acquisition Holdings', 2020, '2020年にSPACと合併して上場。', '上場の手段(2020年)'),
  O('purge', 'Purge Rite', 2025, '2025年に約10億ドルで買収と報じられています。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.6', M), ('State Street', '4.3', M)]),
 [('emerson', 'johnson', 'link', '独立を率いる'), ('johnson', 'albertazzi', 'link', '後任'), ('cote', 'albertazzi', 'link', '会長として支える'), ('co', 'emerson', 'owns', '元の親会社'), ('co', 'purge', 'owns')],
 'Emersonのネットワーク電源事業を2016年に買収して独立した、データセンターの電源・冷却の会社。ジョルダーノ・アルベルタッツィがCEOを務めています。')

# ---------------- Moderna ----------------
deep('MRNA', 'Moderna', 2010, NOTE, [
  P('rossi', 'デリック・ロッシ', 'Derrick Rossi', 2010, '共同創業者。ハーバード大学の幹細胞研究者。', '共同創業者', 2014, 1),
  P('afeyan', 'ヌバー・アフェヤン', 'Noubar Afeyan', 2010, '共同創業者。Flagship Pioneeringの創業者で、会長。', '共同創業者 / 会長', None, 1),
  P('langer', 'ロバート・ランガー', 'Robert Langer', 2010, '共同創業者。MITの教授。', '共同創業者', None, 1),
  P('chien', 'ケネス・チエン', 'Kenneth Chien', 2010, '共同創業者。', '共同創業者', 2013, 1),
  P('bancel', 'ステファン・バンセル', 'Stephane Bancel', 2011, '2011年からCEO。約5.6%を保有(MarketScreener)。', 'CEO'),
  P('hoge', 'スティーブン・ホージ', 'Stephen Hoge', 2012, '社長。', '社長'),
  P('mock', 'ジェイミー・モック', 'Jamey Mock', 2022, 'CFO。', 'CFO'),
  O('flagship', 'Flagship Pioneering', 2010, 'アフェヤン氏の創業したベンチャー。', '創業時の出資者', 'i'),
  O('fidelity', 'Fidelity', 2026, '約13.0%を持つ最大の株主(MarketScreener)。', '最大の株主(約13.0%)', 'i'),
  O('covid', 'COVID-19ワクチン', 2020, '2020年にmRNAワクチンを開発し、会社は急成長。', '主力製品(2020年)'),
 ] + holders([('BlackRock', '6.3', M), ('Vanguard', '5.8', M), ('Capital Group', '5.6', M)]),
 [('afeyan', 'rossi', 'link', '共同創業'), ('afeyan', 'langer', 'link', '共同創業'), ('afeyan', 'chien', 'link', '共同創業'), ('flagship', 'afeyan', 'link', '創業'), ('bancel', 'covid', 'link', '開発を率いる'), ('co', 'covid', 'owns')],
 '2010年に創業されたmRNA医薬の会社。ステファン・バンセルが2011年からCEOを務め、2020年にCOVID-19ワクチンで急成長しました。')

# ---------------- Brookfield Corporation ----------------
deep('BN', 'Brookfield', 1899, NOTE + 'Brookfield Asset Managementとは別の上場会社です(2022年に分割)。', [
  P('flatt', 'ブルース・フラット', 'Bruce Flatt', 2002, 'CEO。約5.0%を保有(MarketScreener)。', 'CEO'),
  P('mckenna', 'フランク・マッケナ', 'Frank McKenna', 2013, '会長。元ニューブランズウィック州首相。', '会長'),
  O('pvi', 'Partners Value Investments', 2026, '約8.1%を持つ最大の株主(MarketScreener)。', '最大の株主(約8.1%)', 'i'),
  O('bam', 'Brookfield Asset Management', 2022, '2022年にアセットマネジメント事業を分割・上場。', '分割(2022年)'),
  O('oaktree', 'Oaktree Capital', 2019, '2019年に約47億ドルで過半を取得。', '買収(2019年)'),
  O('westinghouse', 'Westinghouse Electric', 2023, '2023年にCamecoとともに約79億ドルで買収。', '買収(2023年)'),
 ] + holders([('Royal Trust Corporation of Canada', '5.3', M), ('Capital Group', '3.5', M), ('Vanguard', '2.8', M)]),
 [('flatt', 'mckenna', 'link', '経営陣'), ('co', 'bam', 'owns', '分割'), ('co', 'oaktree', 'owns'), ('co', 'westinghouse', 'owns')],
 'カナダの資産運用・投資会社。ブルース・フラットがCEOを務め、2022年にBrookfield Asset Managementを分割しました。')

# ---------------- Cintas ----------------
deep('CTAS', 'Cintas', 1968, NOTE + 'UniFirstへの買収提案(2025年)は報道に基づきます。', [
  P('dfarmer', 'リチャード・ファーマー', 'Richard Farmer', 1968, '創業者(家族経営のユニフォーム会社)。長く会長。', '創業者', 2015, 1),
  P('sfarmer', 'スコット・ファーマー', 'Scott Farmer', 1979, '創業者の息子。2003〜2021年にCEO、現在は執行会長。約14.0%を保有(MarketScreener)。', '会長(執行) / 筆頭株主'),
  P('schneider', 'トッド・シュナイダー', 'Todd Schneider', 1993, '2021年7月からCEO。', 'CEO'),
  O('gk', 'G&K Services', 2017, '2017年に約22億ドルで買収。', '買収(2017年)'),
  O('unifirst', 'UniFirst', 2025, '2025年に約50億ドル超の買収を提案したが、断念したと報じられています。', '買収提案(2025年・報道)'),
 ] + holders([('Vanguard', '5.5', M), ('BlackRock', '5.2', M), ('State Street', '3.9', M)]),
 [('dfarmer', 'sfarmer', 'link', '親子'), ('sfarmer', 'schneider', 'link', '後任', 2021), ('co', 'gk', 'owns'), ('co', 'unifirst', 'link', '買収提案')],
 '1968年にファーマー家が創業したユニフォーム・設備管理の会社。2021年からトッド・シュナイダーがCEOを務め、創業家のスコット・ファーマーが約14%の筆頭株主です。')
