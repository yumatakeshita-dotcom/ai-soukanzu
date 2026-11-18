from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Waste Management ----------------
deep('WM', 'Waste Management', 1968, NOTE + 'ゲイツ財団の信託が約6.7%を持つ株主です(MarketScreener)。', [
  P('buntrock', 'ディーン・バントロック', 'Dean Buntrock', 1968, '共同創業者。長く会長兼CEO。', '共同創業者', 1996, 1),
  P('huizenga', 'ウェイン・ハイゼンガ', 'Wayne Huizenga', 1968, '共同創業者。のちBlockbuster、AutoNationも創業。', '共同創業者', 1984, 1),
  P('steiner', 'デビッド・ステイナー', 'David Steiner', 2004, '2004〜2016年にCEO。', '元CEO', 2016),
  P('fish', 'ジェームズ・フィッシュ', 'James Fish', 2016, '2016年からCEO。', 'CEO'),
  P('rankin', 'デビナ・ランキン', 'Devina Rankin', 2013, 'CFO。', 'CFO'),
  O('gates', 'ゲイツ財団の信託', 2026, '約6.7%を持つ最大級の株主(MarketScreener)。', '株主(約6.7%)', 'i'),
  O('usawaste', 'USA Waste Services', 1998, '1998年に合併。', '合併(1998年)'),
  O('advanced', 'Advanced Disposal', 2020, '2020年に約46億ドルで買収。', '買収(2020年)'),
  O('stericycle', 'Stericycle', 2024, '2024年に約72億ドルで買収。', '買収(2024年)'),
  O('republic', 'Republic Services', 1998, '競合。ゲイツ氏のCascadeが約38%を持つ。', '競合'),
 ] + holders([('Vanguard', '6.3', M), ('BlackRock', '5.7', M), ('State Street', '4.5', M)]),
 [('buntrock', 'huizenga', 'link', '共同創業'), ('steiner', 'fish', 'link', '後任', 2016), ('co', 'usawaste', 'owns'), ('co', 'advanced', 'owns'), ('co', 'stericycle', 'owns'), ('co', 'republic', 'conflict', '競合')],
 '1968年にシカゴで創業した廃棄物処理の会社。2016年からジェームズ・フィッシュがCEOを務め、ゲイツ財団の信託が約6.7%を持っています。')

# ---------------- Monster Beverage ----------------
deep('MNST', 'Monster Beverage', 1990, NOTE + 'Brandon L.P. No. 2の保有(約6%)の背景は確認していません。', [
  P('sacks', 'ロドニー・サックス', 'Rodney Sacks', 1990, '1990年にHansen Naturalを買収。会長兼共同CEO。', '会長兼共同CEO'),
  P('schlosberg', 'ヒルトン・シュロスバーグ', 'Hilton Schlosberg', 1990, '副会長兼共同CEO。', '副会長兼共同CEO'),
  O('hansen', 'Hansen Natural', 1990, 'サックス氏とシュロスバーグ氏が買収した旧社名(2012年にMonster Beverageへ)。', '前身'),
  O('coke', 'The Coca-Cola Company', 2015, '2015年に約21.5億ドルで約17%を取得し、エナジードリンク事業を交換。現在も約20.9%を持つ最大の株主(MarketScreener)。', '最大の株主(約20.9%)', 'i'),
  O('brandon', 'Brandon L.P. No. 2', 2026, '約6%を持つ株主(MarketScreener)。', '株主(約6%)', 'i'),
  O('canarchy', 'CANarchy', 2022, '2022年に買収(クラフトビール)。', '買収(2022年)'),
  O('bang', 'Bang Energyのブランド', 2023, '2023年に約3.6億ドルで取得。', '買収(2023年)'),
 ] + holders([('Vanguard', '4.7', M), ('BlackRock', '4.6', M)]),
 [('sacks', 'schlosberg', 'link', '共同経営'), ('hansen', 'sacks', 'link', '買収'), ('co', 'hansen', 'owns', '前身'), ('co', 'canarchy', 'owns'), ('co', 'bang', 'owns')],
 'ロドニー・サックス氏らが1990年に買収したHansen Naturalが前身のエナジードリンクの会社。コカ・コーラが約20.9%を持つ最大の株主です。')

# ---------------- U.S. Bancorp ----------------
deep('USB', 'U.S. Bancorp', 2001, NOTE, [
  P('grundhofer', 'ジェリー・グランドホファー', 'Jerry Grundhofer', 1993, '1993〜2007年にCEO(Star Banc、Firstar、US Bancorp)。', '元CEO', 2007),
  P('davis', 'リチャード・デイビス', 'Richard Davis', 1993, '2006〜2017年にCEO。', '元CEO', 2017),
  P('cecere', 'アンドリュー・セセア', 'Andrew Cecere', 1999, '2017〜2025年にCEO。現在は会長。', '会長'),
  P('kedia', 'ガンジャン・ケディア', 'Gunjan Kedia', 2018, '2025年4月からCEO。', 'CEO'),
  P('stern', 'ジョン・スターン', 'John Stern', 2022, 'CFO。', 'CFO'),
  O('firstar', 'Firstar', 2001, '2001年にU.S. Bancorpを買収して社名を継いだ。', '源流(2001年)'),
  O('unionbank', 'MUFG Union Bank', 2022, '2022年に三菱UFJから約80億ドルで買収。', '買収(2022年)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.0', M), ('State Street', '4.7', M)]),
 [('grundhofer', 'davis', 'link', '後任'), ('davis', 'cecere', 'link', '後任', 2017), ('cecere', 'kedia', 'link', '後任', 2025), ('co', 'firstar', 'owns'), ('co', 'unionbank', 'owns')],
 '2001年にFirstarがU.S. Bancorpを買収して誕生した銀行。2025年4月からガンジャン・ケディアがCEOを務めています。')

# ---------------- Emerson ----------------
deep('EMR', 'Emerson Electric', 1890, NOTE + 'AspenTechの残りの株式の取得(2025年)は報道に基づきます。', [
  P('meston', 'チャールズ・メストン', 'Charles Meston', 1890, '1890年にセントルイスでEmersonを共同創業。', '共同創業者', 1920, 1),
  P('farr', 'デビッド・ファー', 'David Farr', 1990, '2000〜2021年にCEO。', '元CEO', 2021),
  P('karsanbhai', 'ラル・カルサンバイ', 'Lal Karsanbhai', 1990, '2021年からCEO。', 'CEO'),
  P('turley', 'ジム・ターリー', 'Jim Turley', 2020, '会長。', '会長'),
  P('baughman', 'マイク・ボーマン', 'Mike Baughman', 2022, 'CFO。', 'CFO'),
  O('rosemount', 'Rosemount', 1976, '1976年に買収(計測機器)。', '買収(1976年)'),
  O('copeland', 'Copeland', 2022, '2022年にブラックストーンへ約140億ドルで過半を売却。', '売却(2022年)'),
  O('ni', 'National Instruments', 2023, '2023年に約82億ドルで買収。', '買収(2023年)'),
  O('aspen', 'AspenTech', 2025, '2025年に残りの株式を約72億ドルで取得と報じられています。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '5.6', M), ('State Street', '5.0', M)]),
 [('meston', 'farr', 'link', '源流'), ('farr', 'karsanbhai', 'link', '後任', 2021), ('co', 'rosemount', 'owns'), ('co', 'copeland', 'owns', '売却'), ('co', 'ni', 'owns'), ('co', 'aspen', 'owns')],
 '1890年にセントルイスで創業した制御・自動化の会社。2021年からラル・カルサンバイがCEOを務めています。')

# ---------------- Intuit ----------------
deep('INTU', 'Intuit', 1983, NOTE, [
  P('cook', 'スコット・クック', 'Scott Cook', 1983, '共同創業者。', '共同創業者', None, 1),
  P('proulx', 'トム・プルークス', 'Tom Proulx', 1983, '共同創業者。', '共同創業者', 1990, 1),
  P('campbell', 'ビル・キャンベル', 'Bill Campbell', 1994, '1994〜1998年にCEO。Appleの取締役も務めた人物。', '元CEO', 1998),
  P('bennett', 'スティーブ・ベネット', 'Steve Bennett', 2000, '2000〜2007年にCEO。', '元CEO', 2007),
  P('smith', 'ブラッド・スミス', 'Brad Smith', 2003, '2008〜2018年にCEO。', '元CEO', 2018),
  P('goodarzi', 'ササン・グダルジ', 'Sasan Goodarzi', 2007, '2019年1月からCEO(会長も)。', '会長兼CEO'),
  P('aujla', 'サンディープ・アウジラ', 'Sandeep Aujla', 2019, 'CFO。', 'CFO'),
  O('mint', 'Mint', 2009, '2009年に約1.7億ドルで買収。', '買収(2009年)'),
  O('creditkarma', 'Credit Karma', 2020, '2020年に約71億ドルで買収。', '買収(2020年)'),
  O('mailchimp', 'Mailchimp', 2021, '2021年に約120億ドルで買収。', '買収(2021年)'),
  O('apple', 'Apple', 1997, 'キャンベル氏が取締役を務めた会社。', '関連'),
 ] + holders([('BlackRock', '7.1', M), ('Vanguard', '6.7', M), ('State Street', '5.0', M)]),
 [('cook', 'proulx', 'link', '共同創業'), ('cook', 'campbell', 'link', 'CEOに迎える', 1994), ('campbell', 'bennett', 'link'), ('bennett', 'smith', 'link', '後任'), ('smith', 'goodarzi', 'link', '後任', 2019), ('campbell', 'apple', 'link', '取締役'), ('co', 'mint', 'owns'), ('co', 'creditkarma', 'owns'), ('co', 'mailchimp', 'owns')],
 '1983年にスコット・クックらが創業した会計・税務ソフトの会社。2019年からササン・グダルジがCEOを務めています。')

# ---------------- Williams Companies ----------------
deep('WMB', 'Williams Companies', 1908, NOTE + '歴代の経営者以外の情報は少なく、確認できた範囲だけを載せています。', [
  P('armstrong', 'アラン・アームストロング', 'Alan Armstrong', 1999, '2011〜2024年にCEO。', '元CEO', 2025),
  P('zamarin', 'チャド・ザマリン', 'Chad Zamarin', 2013, '2025年からCEO。', 'CEO'),
  O('williamsbros', 'Williams Brothers Company', 1908, '1908年にタルサで設立された源流の建設会社。', '源流(1908年)'),
  O('transco', 'Transco(Transcontinental Gas Pipe Line)', 1995, '1995年に買収した米国最大級のガスパイプライン。', '買収(1995年)'),
  O('et', 'Energy Transfer', 2016, '2016年に約380億ドルの合併を発表したが、実現せず。', '合併断念(2016年)'),
 ] + holders([('BlackRock', '7.1', M), ('Vanguard', '6.5', M), ('State Street', '5.9', M)]),
 [('armstrong', 'zamarin', 'link', '後任', 2025), ('williamsbros', 'armstrong', 'link', '源流'), ('co', 'transco', 'owns'), ('co', 'et', 'link', '合併を断念')],
 '1908年にタルサで始まった天然ガスのインフラの会社。2025年からチャド・ザマリンがCEOを務めています。')

# ---------------- Elevance Health ----------------
deep('ELV', 'Elevance Health', 1944, NOTE, [
  P('schaeffer', 'レナード・シェーファー', 'Leonard Schaeffer', 1986, 'WellPointの初代CEO(〜2005年)。', '元CEO', 2005),
  P('braly', 'アンジェラ・ブレイリー', 'Angela Braly', 2007, '2007〜2012年にCEO。', '元CEO', 2012),
  P('swedish', 'ジョセフ・スウェディッシュ', 'Joseph Swedish', 2012, '2012〜2017年にCEO。', '元CEO', 2017),
  P('boudreaux', 'ゲイル・ブードロー', 'Gail Boudreaux', 2017, '2017年11月からCEO(社長も)。', 'CEO兼社長'),
  P('peru', 'レイミー・ペルー', 'Ramey Peru', 2020, '会長(英語版Wikipedia)。', '会長'),
  O('wellchoice', 'WellChoice', 2005, '2005年に約65億ドルで買収。', '買収(2005年)'),
  O('amerigroup', 'Amerigroup', 2012, '2012年に約49億ドルで買収。', '買収(2012年)'),
  O('cigna', 'Cigna', 2015, '2015年に約540億ドルでAnthemが買収を提案したが、司法省の訴えなどで2017年に断念。', '買収断念(2017年)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.3', M), ('State Street', '4.8', M), ('Wellington', '4.2', M)]),
 [('schaeffer', 'braly', 'link', '後任'), ('braly', 'swedish', 'link', '後任'), ('swedish', 'boudreaux', 'link', '後任', 2017), ('co', 'wellchoice', 'owns'), ('co', 'amerigroup', 'owns'), ('co', 'cigna', 'conflict', '買収を断念', 2017)],
 'ブルークロス系の保険会社を源流とする医療保険の会社(旧Anthem、WellPoint)。2017年からゲイル・ブードローがCEOを務めています。')

# ---------------- Cloudflare ----------------
deep('NET', 'Cloudflare', 2009, NOTE + 'Replicateの買収(2025年)は報道に基づきます。', [
  P('prince', 'マシュー・プリンス', 'Matthew Prince', 2009, '共同創業者でCEO。共同会長。', '共同創業者 / CEO', None, 1),
  P('zatlyn', 'ミシェル・ザトリン', 'Michelle Zatlyn', 2009, '共同創業者で社長。共同会長。', '共同創業者 / 社長', None, 1),
  P('holloway', 'リー・ホロウェイ', 'Lee Holloway', 2009, '共同創業者でエンジニア。2016年に病気で退任。', '共同創業者', 2016, 1),
  P('knecht', 'デーン・ネヒト', 'Dane Knecht', 2020, 'CTO。', 'CTO'),
  O('honeypot', 'Project Honey Pot', 2004, 'プリンス氏とホロウェイ氏が先に始めたスパム対策のプロジェクト。', '源流'),
  O('area1', 'Area 1 Security', 2022, '2022年に買収(メールの保護)。', '買収(2022年)'),
  O('replicate', 'Replicate', 2025, '2025年に買収と報じられています(AIモデルの実行基盤)。', '買収(2025年・報道)'),
 ] + holders([('Capital Group', '7.5', M), ('BlackRock', '5.3', M), ('Vanguard', '5.2', M)]),
 [('prince', 'zatlyn', 'link', '共同創業'), ('prince', 'holloway', 'link', '共同創業'), ('honeypot', 'prince', 'link', '源流'), ('co', 'area1', 'owns'), ('co', 'replicate', 'owns')],
 '2009年にマシュー・プリンスらが創業したネットワークとセキュリティのクラウド。プリンス氏がCEOを務めています。')

# ---------------- PNC ----------------
deep('PNC', 'PNC Financial Services', 1983, NOTE, [
  P('rohr', 'ジェームズ・ロア', 'James Rohr', 1992, '2000〜2013年にCEO。', '元CEO', 2013),
  P('demchak', 'ウィリアム・デムチャック', 'William Demchak', 2002, '2013年からCEO兼会長。', '会長兼CEO'),
  P('wiedman', 'マーク・ウィードマン', 'Mark Wiedman', 2025, '社長(英語版Wikipedia)。ブラックロックの元幹部。', '社長'),
  P('reilly', 'ロバート・ライリー', 'Robert Reilly', 2009, 'CFO。', 'CFO'),
  O('pittsburghnational', 'Pittsburgh National', 1983, '1983年にProvident Nationalと合併して誕生。', '合併(1983年)'),
  O('blackrockstake', 'BlackRock', 1995, 'PNCは長く大株主だった(2020年に売却)。', '元の大株主'),
  O('nationalcity', 'National City', 2008, '2008年に約56億ドルで買収。', '買収(2008年)'),
  O('rbcusa', 'RBC Bank (USA)', 2012, '2012年に約34.5億ドルで買収。', '買収(2012年)'),
  O('bbvausa', 'BBVA USA', 2021, '2021年に約116億ドルで買収。', '買収(2021年)'),
  O('firstbank', 'FirstBank', 2025, '2025年に約41億ドルで買収と報じられています。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.1', M), ('State Street', '4.6', M)]),
 [('rohr', 'demchak', 'link', '後任', 2013), ('demchak', 'wiedman', 'link', '社長', 2025), ('wiedman', 'blackrockstake', 'moved', '前職'), ('co', 'pittsburghnational', 'owns'), ('co', 'nationalcity', 'owns'), ('co', 'rbcusa', 'owns'), ('co', 'bbvausa', 'owns'), ('co', 'firstbank', 'owns')],
 '1983年にピッツバーグの2行が合併して誕生した銀行。ウィリアム・デムチャックが2013年から会長兼CEOを務めています。')

# ---------------- Johnson Controls ----------------
deep('JCI', 'Johnson Controls', 1885, NOTE, [
  P('wjohnson', 'ウォーレン・ジョンソン', 'Warren Johnson', 1885, '1885年に電気式サーモスタットを発明し、会社を創業。', '創業者', 1911, 1),
  P('molinaroli', 'アレックス・モリナロリ', 'Alex Molinaroli', 1983, '2013〜2017年にCEO。', '元CEO', 2017),
  P('oliver', 'ジョージ・オリバー', 'George Oliver', 2016, '2017〜2025年にCEO。Tycoのトップとして2016年の合併を主導。', '元CEO', 2025),
  P('weidemanis', 'ヨアキム・ヴァイデマニス', 'Joakim Weidemanis', 2025, '2025年3月からCEO。', 'CEO'),
  P('vandiepenbeeck', 'マルク・ヴァンディエペンビーク', 'Marc Vandiepenbeeck', 2023, 'CFO。', 'CFO'),
  O('york', 'York International', 2005, '2005年に約32億ドルで買収。', '買収(2005年)'),
  O('tyco', 'Tyco International', 2016, '2016年に約165億ドルで統合。アイルランドに本社を移す合併。', '合併(2016年)'),
  O('dodgecox', 'Dodge & Cox', 2026, '約9.2%を持つ最大の株主(MarketScreener)。', '最大の株主(約9.2%)', 'i'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '5.9', M), ('State Street', '4.7', M)]),
 [('wjohnson', 'molinaroli', 'link', '源流'), ('molinaroli', 'oliver', 'link', '後任', 2017), ('oliver', 'weidemanis', 'link', '後任', 2025), ('co', 'york', 'owns'), ('co', 'tyco', 'owns')],
 '1885年にウォーレン・ジョンソンが電気式サーモスタットで創業したビル設備の会社。2025年3月からヨアキム・ヴァイデマニスがCEOを務めています。')
