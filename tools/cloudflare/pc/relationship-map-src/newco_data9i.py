from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- McDonald's ----------------
deep('MCD', "McDonald's", 1940, NOTE, [
  P('richard', 'リチャード・マクドナルド', "Richard McDonald", 1940, '1940年に弟モーリスと最初の店を開いた創業者。', '創業者', 1961, 1),
  P('maurice', 'モーリス・マクドナルド', "Maurice McDonald", 1940, '創業者。', '創業者', 1961, 1),
  P('kroc', 'レイ・クロック', 'Ray Kroc', 1955, '1955年にフランチャイズ事業を始め、1961年に権利を買い取りました。', '事実上の創業者', 1984, 1),
  P('skinner', 'ジム・スキナー', 'Jim Skinner', 2004, '2004〜2012年にCEO。', '元CEO', 2012),
  P('thompson', 'ドン・トンプソン', 'Don Thompson', 2012, '2012〜2015年にCEO。', '元CEO', 2015),
  P('easterbrook', 'スティーブ・イースターブルック', 'Steve Easterbrook', 2015, '2015〜2019年にCEO。社内規定違反で解任。', '元CEO', 2019),
  P('kempczinski', 'クリス・ケンプチンスキー', 'Chris Kempczinski', 2015, '2019年11月からCEO(会長も)。', '会長兼CEO'),
  P('borden', 'イアン・ボーデン', 'Ian Borden', 2023, 'CFO。', 'CFO'),
  O('chipotle', 'Chipotle', 1998, '1998年から出資し、2006年までに全株を売却。', '出資(1998〜2006年)'),
  O('bostonmarket', 'Boston Market', 1999, '1999年に買収(2007年に売却)。', '買収(1999年)'),
  O('dynamic', 'Dynamic Yield', 2019, '2019年に約3億ドルで買収(AI)。', '買収(2019年)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.1', M), ('State Street', '5.1', M)]),
 [('richard', 'maurice', 'link', '兄弟で創業'), ('kroc', 'richard', 'link', '権利を買い取る', 1961), ('skinner', 'thompson', 'link', '後任'), ('thompson', 'easterbrook', 'link', '後任'), ('easterbrook', 'kempczinski', 'link', '後任', 2019), ('co', 'chipotle', 'link', '出資'), ('co', 'bostonmarket', 'owns'), ('co', 'dynamic', 'owns')],
 '1940年にマクドナルド兄弟が始めたハンバーガーの店を、レイ・クロックが世界に広げた会社。2019年からクリス・ケンプチンスキーがCEOを務めています。')

# ---------------- Deere ----------------
deep('DE', 'Deere', 1837, NOTE, [
  P('jdeere', 'ジョン・ディア', 'John Deere', 1837, '1837年に鋼鉄製のプラウを作った鍛冶職人。', '創業者', 1886, 1),
  P('cdeere', 'チャールズ・ディア', 'Charles Deere', 1858, '創業者の息子。事業を大きくしました。', '元社長', 1907),
  P('hewitt', 'ウィリアム・ヒューイット', 'William Hewitt', 1955, '1955〜1982年にCEO。', '元CEO', 1982),
  P('becherer', 'ハンス・ベッヒャー', 'Hans Becherer', 1987, '1987〜2000年にCEO。', '元CEO', 2000),
  P('lane', 'ロバート・レーン', 'Robert Lane', 2000, '2000〜2009年にCEO。', '元CEO', 2009),
  P('allen', 'サミュエル・アレン', 'Samuel Allen', 2009, '2009〜2019年にCEO。', '元CEO', 2019),
  P('may', 'ジョン・メイ', 'John May', 1997, '2019年からCEO兼会長。', '会長兼CEO'),
  O('cascade', 'Cascade Investment', 2026, 'ビル・ゲイツ氏の資産管理会社。約7.3%を持つ最大の株主(MarketScreener、2026年11月)。', '最大の株主(約7.3%)', 'i'),
  O('bluerivertech', 'Blue River Technology', 2017, '2017年に約3.05億ドルで買収(農業のAI)。', '買収(2017年)'),
  O('wirtgen', 'Wirtgen', 2017, '2017年に約46億ユーロで買収(道路機械)。', '買収(2017年)'),
 ] + holders([('Vanguard', '6.1', M), ('BlackRock', '5.2', M), ('Capital Group', '4.3', M)]),
 [('jdeere', 'cdeere', 'link', '親子'), ('hewitt', 'becherer', 'link', '後任'), ('becherer', 'lane', 'link', '後任'), ('lane', 'allen', 'link', '後任'), ('allen', 'may', 'link', '後任', 2019), ('co', 'bluerivertech', 'owns'), ('co', 'wirtgen', 'owns')],
 '1837年にジョン・ディアが創業した農業機械の会社。2019年からジョン・メイがCEOを務め、ゲイツ氏のCascadeが最大の株主です。')

# ---------------- Union Pacific ----------------
deep('UNP', 'Union Pacific', 1862, NOTE + 'ノーフォーク・サザンとの合併(2025年7月発表)は、規制当局の審査中の報道に基づきます。', [
  P('lincoln', 'エイブラハム・リンカーン', 'Abraham Lincoln', 1862, '1862年の太平洋鉄道法に署名した米国大統領(会社の設立根拠)。', '設立の署名者', 1865, 1),
  P('durant', 'トーマス・デュラント', 'Thomas Durant', 1863, '初期の副社長兼ゼネラルマネージャー(1863〜1869年)。', '元幹部', 1869),
  P('dodge', 'グレンヴィル・ドッジ', 'Grenville Dodge', 1866, 'チーフエンジニア(1866〜1870年)。', '元幹部', 1870),
  P('harriman', 'E・H・ハリマン', 'E. H. Harriman', 1898, '1898〜1909年に会長、1901〜1909年に社長。', '元会長', 1909),
  P('fritz', 'ランス・フリッツ', 'Lance Fritz', 2005, '2015〜2023年にCEO。', '元CEO', 2023),
  P('vena', 'ジム・ヴェナ', 'Jim Vena', 2019, '2023年8月からCEO。', 'CEO'),
  P('whited', 'ベス・ホワイテッド', 'Beth Whited', 2023, '社長。', '社長'),
  P('mccarthy', 'マイク・マッカーシー', 'Mike McCarthy', 2020, '会長。', '会長'),
  O('nsc', 'Norfolk Southern', 2025, '2025年7月に約850億ドルでの合併を発表(規制当局の審査中と報じられています)。', '合併発表(2025年・報道)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.2', M), ('State Street', '4.7', M)]),
 [('lincoln', 'durant', 'link', '法律に基づき設立'), ('durant', 'dodge', 'link'), ('harriman', 'fritz', 'link', '歴代の経営者'), ('fritz', 'vena', 'link', '後任', 2023), ('co', 'nsc', 'link', '合併を発表', 2025)],
 '1862年にリンカーン大統領が署名した太平洋鉄道法で設立された鉄道会社。2023年からジム・ヴェナがCEOを務め、2025年にノーフォーク・サザンとの合併を発表しました。')

# ---------------- BlackRock ----------------
deep('BLK', 'BlackRock', 1988, NOTE, [
  P('fink', 'ラリー・フィンク', 'Larry Fink', 1988, '共同創業者。会長兼CEO。', '共同創業者 / 会長兼CEO', None, 1),
  P('kapito', 'ロバート・カピト', 'Robert Kapito', 1988, '共同創業者。社長。', '共同創業者 / 社長', None, 1),
  P('wagner', 'スー・ワグナー', 'Sue Wagner', 1988, '共同創業者。Appleの取締役でもあります。', '共同創業者', 2012, 1),
  P('golub', 'ベン・ゴルブ', 'Ben Golub', 1988, '共同創業者。', '共同創業者', 2016, 1),
  P('schlosstein', 'ラルフ・シュロスタイン', 'Ralph Schlosstein', 1988, '共同創業者。', '共同創業者', 2007, 1),
  P('novick', 'バーバラ・ノビック', 'Barbara Novick', 1988, '共同創業者。', '共同創業者', 2022, 1),
  P('anderson', 'キース・アンダーソン', 'Keith Anderson', 1988, '共同創業者。', '共同創業者', 2005, 1),
  P('frater', 'ヒュー・フレーター', 'Hugh Frater', 1988, '共同創業者。', '共同創業者', 1990, 1),
  P('hildebrand', 'フィリップ・ヒルデブランド', 'Philipp Hildebrand', 2012, '副会長(元スイス国立銀行総裁)。', '副会長'),
  P('small', 'マーティン・スモール', 'Martin Small', 2019, 'CFO。', 'CFO'),
  O('blackstone', 'Blackstone', 1988, '1988年にBlackStone内の債券部門として始まり、のち独立。', '源流の親会社', 'i'),
  O('pnc', 'PNC', 1995, '1995年から大株主となり、2020年に売却。', '元の大株主(〜2020年)', 'i'),
  O('kia', 'Kuwait Investment Authority', 2026, '約5.2%を持つ上位株主(MarketScreener)。', '株主(約5.2%)', 'i'),
  O('temasek', 'Temasek', 2026, '約3.3%を持つ上位株主(MarketScreener)。', '株主(約3.3%)', 'i'),
  O('bgi', 'Barclays Global Investors', 2009, '2009年に約135億ドルで買収(iShares)。', '買収(2009年)'),
  O('gip', 'Global Infrastructure Partners', 2024, '2024年に約125億ドルで買収。', '買収(2024年)'),
  O('hps', 'HPS Investment Partners', 2025, '2025年に約120億ドルで買収。', '買収(2025年)'),
  O('preqin', 'Preqin', 2025, '2025年に約32億ドルで買収(データ)。', '買収(2025年)'),
 ] + holders([('Vanguard', '6.0', M), ('BlackRock', '5.1', M)]),
 [('fink', 'kapito', 'link', '共同創業'), ('fink', 'wagner', 'link', '共同創業'), ('fink', 'golub', 'link', '共同創業'), ('fink', 'novick', 'link', '共同創業'), ('fink', 'blackstone', 'moved', '源流'), ('co', 'bgi', 'owns'), ('co', 'gip', 'owns'), ('co', 'hps', 'owns'), ('co', 'preqin', 'owns')],
 '1988年にラリー・フィンクら8人が創業した資産運用会社。ラリー・フィンクが会長兼CEOを務めています。')

# ---------------- Qualcomm ----------------
deep('QCOM', 'Qualcomm', 1985, NOTE + 'アルファウェーブの買収(2025年)は報道に基づきます。', [
  P('jacobs', 'アーウィン・ジェイコブス', 'Irwin Jacobs', 1985, '共同創業者。CEO(〜2005年)。', '共同創業者', 2005, 1),
  P('viterbi', 'アンドリュー・ビタビ', 'Andrew Viterbi', 1985, '共同創業者。ビタビ・アルゴリズムの考案者。', '共同創業者', 2000, 1),
  P('pjacobs', 'ポール・ジェイコブス', 'Paul Jacobs', 1990, '2005〜2014年にCEO。', '元CEO', 2014),
  P('mollenkopf', 'スティーブ・モレンコフ', 'Steve Mollenkopf', 1994, '2014〜2021年にCEO。のちボーイングの会長。', '元CEO', 2021),
  P('amon', 'クリスティアーノ・アモン', 'Cristiano Amon', 1995, '2021年6月からCEO。', 'CEO'),
  P('mclaughlin', 'マーク・マクラフリン', 'Mark McLaughlin', 2018, '会長。パロアルトネットワークスの元CEO。', '会長'),
  P('palkhiwala', 'アカシュ・パルキワラ', 'Akash Palkhiwala', 2002, 'CFO兼COO。', 'CFO兼COO'),
  O('broadcom', 'Broadcom', 2018, '2018年に約1,170億ドルの敵対的買収を提案したが、米国大統領が阻止。', '買収提案(2018年)'),
  O('nxp', 'NXP', 2016, '2016年に約470億ドルで買収を発表したが、中国当局の承認が得られず2018年に断念。', '買収断念(2018年)'),
  O('atheros', 'Atheros', 2011, '2011年に約31億ドルで買収。', '買収(2011年)'),
  O('csr', 'CSR', 2015, '2015年に約24億ドルで買収。', '買収(2015年)'),
  O('nuvia', 'Nuvia', 2021, '2021年に約14億ドルで買収(CPU)。', '買収(2021年)'),
  O('alphawave', 'Alphawave', 2025, '2025年に約24億ドルで買収と報じられています。', '買収(2025年・報道)'),
 ] + holders([('BlackRock', '6.4', M), ('Vanguard', '6.4', M), ('State Street', '4.9', M)]),
 [('jacobs', 'viterbi', 'link', '共同創業'), ('jacobs', 'pjacobs', 'link', '親子'), ('pjacobs', 'mollenkopf', 'link', '後任'), ('mollenkopf', 'amon', 'link', '後任', 2021), ('co', 'atheros', 'owns'), ('co', 'csr', 'owns'), ('co', 'nuvia', 'owns'), ('co', 'alphawave', 'owns'), ('co', 'broadcom', 'conflict', '敵対的買収を拒否', 2018), ('co', 'nxp', 'link', '買収を断念')],
 '1985年にアーウィン・ジェイコブスらが創業した通信半導体の会社。2021年からクリスティアーノ・アモンがCEOを務めています。')

# ---------------- NextEra Energy ----------------
deep('NEE', 'NextEra Energy', 1925, NOTE, [
  P('hay', 'ルー・ヘイ', 'Lew Hay', 2001, '2001〜2012年にCEO。', '元CEO', 2012),
  P('robo', 'ジム・ロボ', 'Jim Robo', 2003, '2012〜2022年にCEO。', '元CEO', 2022),
  P('ketchum', 'ジョン・ケッチャム', 'John Ketchum', 2002, '2022年からCEO(2022年から会長も)。', '会長兼CEO'),
  P('bores', 'スコット・ボアズ', 'Scott Bores', 2000, 'FPL(フロリダの電力会社)のCEO。', '子会社CEO'),
  P('bolster', 'ブライアン・ボルスター', 'Brian Bolster', 2000, '再生可能エネルギー部門(NEER)のCEO。', '部門CEO'),
  P('kujawa', 'レベッカ・クジャワ', 'Rebecca Kujawa', 2000, 'CFO(2021年〜)。', 'CFO'),
  O('fpl', 'Florida Power & Light', 1925, '1925年に設立された電力会社(フロリダ)。', '子会社(1925年〜)'),
  O('gulf', 'Gulf Power', 2019, '2019年に約65億ドルで買収。', '買収(2019年)'),
  O('xplr', 'XPLR Infrastructure', 2014, '再生可能エネルギーの資産を保有する上場子会社(旧NextEra Energy Partners)。', '関連会社'),
 ] + holders([('Vanguard', '6.5', M), ('State Street', '5.7', M), ('Geode', '2.4', M)]),
 [('hay', 'robo', 'link', '後任'), ('robo', 'ketchum', 'link', '後任', 2022), ('co', 'fpl', 'owns'), ('co', 'gulf', 'owns'), ('co', 'xplr', 'owns'), ('ketchum', 'bores', 'link'), ('ketchum', 'bolster', 'link')],
 '1925年設立のFlorida Power & Lightを中核とする電力会社。2022年からジョン・ケッチャムがCEOを務めています。')

# ---------------- Pfizer ----------------
deep('PFE', 'Pfizer', 1849, NOTE + 'Metseraの買収(2025年)は報道に基づきます。', [
  P('cpfizer', 'チャールズ・ファイザー', 'Charles Pfizer', 1849, '1849年に従兄弟のエルハートとニューヨークで創業。', '共同創業者', 1906, 1),
  P('erhart', 'チャールズ・エルハート', 'Charles Erhart', 1849, '共同創業者。', '共同創業者', 1891, 1),
  P('mckinnell', 'ハンク・マッキンネル', 'Hank McKinnell', 2001, '2001〜2006年にCEO。', '元CEO', 2006),
  P('kindler', 'ジェフ・キンドラー', 'Jeff Kindler', 2002, '2006〜2010年にCEO。', '元CEO', 2010),
  P('read', 'イアン・リード', 'Ian Read', 2010, '2010〜2019年にCEO。', '元CEO', 2019),
  P('bourla', 'アルバート・ブーラ', 'Albert Bourla', 1993, '2019年からCEO兼会長。', '会長兼CEO'),
  P('denton', 'デビッド・デントン', 'David Denton', 2022, 'CFO。', 'CFO'),
  O('warnerlambert', 'Warner-Lambert', 2000, '2000年に約900億ドルで買収。', '買収(2000年)'),
  O('pharmacia', 'Pharmacia', 2003, '2003年に約600億ドルで買収。', '買収(2003年)'),
  O('wyeth', 'Wyeth', 2009, '2009年に約680億ドルで買収。', '買収(2009年)'),
  O('hospira', 'Hospira', 2015, '2015年に約170億ドルで買収。', '買収(2015年)'),
  O('viatris', 'Viatris', 2020, '2020年にUpjohnを分離し、Mylanと統合。', '分離(2020年)'),
  O('seagen', 'Seagen', 2023, '2023年に約430億ドルで買収。', '買収(2023年)'),
  O('metsera', 'Metsera', 2025, '2025年に約100億ドルで買収と報じられています(肥満症薬)。', '買収(2025年・報道)'),
 ] + holders([('BlackRock', '6.7', M), ('Vanguard', '6.5', M), ('State Street', '5.4', M)]),
 [('cpfizer', 'erhart', 'link', '共同創業'), ('mckinnell', 'kindler', 'link', '後任'), ('kindler', 'read', 'link', '後任'), ('read', 'bourla', 'link', '後任', 2019), ('co', 'warnerlambert', 'owns'), ('co', 'pharmacia', 'owns'), ('co', 'wyeth', 'owns'), ('co', 'hospira', 'owns'), ('co', 'viatris', 'owns', '分離'), ('co', 'seagen', 'owns'), ('co', 'metsera', 'owns')],
 '1849年にニューヨークで創業した製薬会社。2019年からアルバート・ブーラがCEOを務めています。')

# ---------------- Marvell ----------------
deep('MRVL', 'Marvell Technology', 1995, NOTE, [
  P('ssutardja', 'セハット・スタジャ', 'Sehat Sutardja', 1995, '共同創業者で長くCEO。2016年に退任。', '共同創業者 / 元CEO', 2016, 1),
  P('dai', 'ウェイリ・ダイ', 'Weili Dai', 1995, '共同創業者。2016年に退任。', '共同創業者', 2016, 1),
  P('psutardja', 'パンタス・スタジャ', 'Pantas Sutardja', 1995, '共同創業者でCTO。', '共同創業者', 2016, 1),
  P('murphy', 'マット・マーフィー', 'Matt Murphy', 2016, '2016年からCEO(会長も)。', '会長兼CEO'),
  P('koopmans', 'クリス・クープマンズ', 'Chris Koopmans', 2020, 'COO兼社長。', 'COO兼社長'),
  P('meintjes', 'ウィレム・メインチェス', 'Willem Meintjes', 2021, 'CFO。', 'CFO'),
  O('cavium', 'Cavium', 2018, '2018年に約60億ドルで買収。', '買収(2018年)'),
  O('inphi', 'Inphi', 2021, '2021年に約100億ドルで買収。', '買収(2021年)'),
  O('innovium', 'Innovium', 2021, '2021年に約10億ドルで買収。', '買収(2021年)'),
 ] + holders([('BlackRock', '7.1', M), ('Vanguard', '6.6', M), ('Fidelity', '6.5', M)]),
 [('ssutardja', 'dai', 'link', '共同創業(夫婦)'), ('ssutardja', 'psutardja', 'link', '共同創業(兄弟)'), ('ssutardja', 'murphy', 'link', '後任', 2016), ('co', 'cavium', 'owns'), ('co', 'inphi', 'owns'), ('co', 'innovium', 'owns')],
 '1995年にスタジャ夫妻らが創業した半導体の会社。2016年からマット・マーフィーがCEOを務めています。')

# ---------------- Welltower ----------------
deep('WELL', 'Welltower', 1970, NOTE + '歴代の経営者の情報は少なく、確認できた範囲だけを載せています。', [
  P('chapman', 'ジョージ・チャップマン', 'George Chapman', 1996, '1996〜2014年にCEO。', '元CEO', 2014),
  P('derosa', 'トム・デローザ', 'Tom DeRosa', 2014, '2014〜2022年にCEO。', '元CEO', 2022),
  P('mitra', 'シャンク・ミトラ', 'Shankh Mitra', 2022, '2022年からCEO。', 'CEO'),
  O('hcreit', 'Health Care REIT', 1970, '1970年に設立された旧社名(2015年にWelltowerへ変更)。', '旧社名'),
 ] + holders([('BlackRock', '8.5', M), ('Vanguard', '6.4', M), ('State Street', '5.8', M)]),
 [('chapman', 'derosa', 'link', '後任'), ('derosa', 'mitra', 'link', '後任', 2022), ('hcreit', 'chapman', 'link', '源流')],
 '1970年に設立された、高齢者向け住宅や医療施設のREIT(旧Health Care REIT)。2022年からシャンク・ミトラがCEOを務めています。')

# ---------------- Sandisk ----------------
deep('SNDK', 'Sandisk', 1988, NOTE, [
  P('harari', 'エリ・ハラリ', 'Eli Harari', 1988, '共同創業者でCEO(〜2011年)。', '共同創業者', 2011, 1),
  P('mehrotra', 'サンジェイ・メロートラ', 'Sanjay Mehrotra', 1988, '共同創業者でCEO(2011〜2016年)。現在はMicronのCEO。', '共同創業者 / 元CEO', 2016, 1),
  P('yuan', 'ジャック・ユアン', 'Jack Yuan', 1988, '共同創業者。', '共同創業者', 1995, 1),
  P('goeckeler', 'デビッド・ゲッケラー', 'David Goeckeler', 2020, 'Western Digitalの元CEO。2025年のSandisk分離後のCEO。', 'CEO'),
  O('wdc', 'Western Digital', 2016, '2016年に約190億ドルでSanDiskを買収。2025年2月にフラッシュ事業を分離・再上場。', '元の親会社(2016〜2025年)'),
  O('micron', 'Micron', 2016, 'メロートラ氏が現在CEOを務める会社。', '関連'),
 ],
 [('harari', 'mehrotra', 'link', '共同創業'), ('harari', 'yuan', 'link', '共同創業'), ('co', 'wdc', 'link', '2016年に買収され、2025年に分離'), ('mehrotra', 'micron', 'link', 'CEO')],
 '1988年に創業したフラッシュメモリの会社。2016年にWestern Digitalに買収され、2025年2月に分離して再上場。デビッド・ゲッケラーがCEOを務めています。')
