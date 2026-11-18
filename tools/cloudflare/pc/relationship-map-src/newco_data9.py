from newco_data import mk

# 深掘りした米国企業の図(年スライダーで歴史が見られる)。キー=ティッカー
DEEP = {}

def P(id, name, en, frm, desc, role, to=None, founder=0):
    d = {'id': id, 'name': name, 'kind': 'p', 'from': frm, 'desc': desc, 'role': role}
    if to:
        d['to'] = to
    if founder:
        d['founder'] = 1
    return d, en

def O(id, name, frm, desc, role, kind='o'):
    return {'id': id, 'name': name, 'kind': kind, 'from': frm, 'desc': desc, 'role': role}, None

def deep(ticker, name, minyear, note, items, edges, center_desc):
    N = [{'id': 'co', 'name': name, 'kind': 'c', 'from': minyear, 'desc': center_desc}]
    EN = {}
    E = "const E = [];\nN.forEach(n=>{ if(n.kind==='p') E.push({a:n.id,b:'co',k:'member'}); if(n.kind==='i') E.push({a:n.id,b:'co',k:'invest'}); });\n"
    for node, en in items:
        N.append(node)
        if en:
            EN[node['id']] = en
    for e in edges:
        s = "E.push({a:'%s',b:'%s',k:'%s'" % (e[0], e[1], e[2])
        if len(e) > 3 and e[3]:
            s += ",label:'%s'" % e[3]
        if len(e) > 4 and e[4]:
            s += ",since:%d" % e[4]
        E += s + "});\n"
    DEEP[ticker] = dict(co=mk(N, E, EN, {}, {}, {}, {}, {}, 'co'), min=minyear, note=note)

SRC = '(Apple公式の幹部紹介ページ、2026年11月取得)'
deep('AAPL', 'Apple', 1976,
 '役員・取締役は、Apple公式の「Leadership」ページ(2026年11月取得)とMarketScreenerに基づきます。歴代の経営者と買収は、英語版Wikipediaに基づきます(買収額は報道ベースのものを含みます)。Q.aiの買収(2026年)は報道に基づきます。取締役の就任年は、Appleの提出書類で確かめていません。顔写真がない人はイニシャル表示です。',
 [
  # --- 創業期 ---
  P('jobs', 'スティーブ・ジョブズ', 'Steve Jobs', 1976, '共同創業者。1985年にAppleを去り、NeXTとPixarを経て、1997年に復帰。2000年に正式なCEOになり、2011年に亡くなるまで率いました。', '共同創業者 / CEO', 2011, 1),
  P('woz', 'スティーブ・ウォズニアック', 'Steve Wozniak', 1976, '共同創業者でエンジニア。Apple IIを設計しました。', '共同創業者', 1985, 1),
  P('wayne', 'ロナルド・ウェイン', 'Ronald Wayne', 1976, '共同創業者の1人。持ち分を手放し、設立から2週間足らずで離れました。', '共同創業者(早期に離脱)', 1977, 1),
  P('markkula', 'マイク・マークラ', 'Mike Markkula', 1977, '初期の出資者で、のちに会長。', '出資者 / 元会長', 1997),
  P('mscott', 'マイケル・スコット', 'Michael Scott', 1977, '最初の社長兼CEO。', '初代CEO', 1981),
  P('sculley', 'ジョン・スカリー', 'John Sculley', 1983, 'ペプシコから迎えられたCEO。1985年にジョブズが去る形になった時期の経営者。', '元CEO', 1993),
  P('spindler', 'マイケル・スピンドラー', 'Michael Spindler', 1993, 'CEO(1993〜1996年)。', '元CEO', 1996),
  P('amelio', 'ギル・アメリオ', 'Gil Amelio', 1996, 'CEO。1997年7月に取締役会に退任させられ、NeXTの買収を主導しました。', '元CEO', 1997),
  P('oppenheimer', 'ピーター・オッペンハイマー', 'Peter Oppenheimer', 1996, '長くCFOを務めました。', '元CFO', 2014),
  P('tevanian', 'アビー・テバニアン', 'Avie Tevanian', 1997, 'NeXTから参加したソフトウェア責任者。', '元ソフトウェア責任者', 2006),
  P('fadell', 'トニー・ファデル', 'Tony Fadell', 2001, 'iPodの開発を率いました。', '元iPod責任者', 2008),
  P('forstall', 'スコット・フォーストール', 'Scott Forstall', 1997, 'iOSの開発を率いました。2012年に退社。', '元iOS責任者', 2012),
  P('ive', 'ジョナサン・アイブ', 'Jony Ive', 1992, '長くデザインを率いました。2019年に退社し、自身の会社LoveFromを設立。', '元デザイン責任者', 2019),
  P('williams', 'ジェフ・ウィリアムズ', 'Jeff Williams', 1998, 'COO。2025年7月にCOOがサビー・カーン氏に交代しました。', '元COO', 2025),
  P('maestri', 'ルカ・マエストリ', 'Luca Maestri', 2013, 'CFO。2025年1月にケヴァン・パレク氏へ交代。', '元CFO', 2025),
  # --- 現在の経営陣 ---
  P('cook', 'ティム・クック', 'Tim Cook', 1998, '1998年に入社し、2011年から2026年8月までCEO。2026年9月からは執行会長(Executive Chair)。', '会長(執行)', None),
  P('ternus', 'ジョン・ターナス', 'John Ternus', 2001, 'ハードウェア・エンジニアリング担当の上級副社長を経て、2026年9月1日付でCEOに就任(Apple発表。MarketScreenerは8月31日付)。', 'CEO'),
  P('khan', 'サビー・カーン', 'Sabih Khan', 1995, 'COO(2025年7月から)。', 'COO'),
  P('parekh', 'ケヴァン・パレク', 'Kevan Parekh', 2013, 'CFO(2025年1月から)。', 'CFO'),
  P('cue', 'エディー・キュー', 'Eddy Cue', 1989, 'サービス・ヘルスケア担当の上級副社長。', '上級副社長(サービス・ヘルス)'),
  P('federighi', 'クレイグ・フェデリギ', 'Craig Federighi', 2009, 'ソフトウェア・エンジニアリング担当の上級副社長。', '上級副社長(ソフトウェア)'),
  P('joswiak', 'グレッグ・ジョズウィアク', 'Greg Joswiak', 1986, '全世界マーケティング担当の上級副社長。', '上級副社長(マーケティング)'),
  P('srouji', 'ジョニー・スルージ', 'Johny Srouji', 2008, 'ハードウェア担当の最高責任者(Chief Hardware Officer)。自社チップの開発を率いてきました。', 'ハードウェア最高責任者'),
  P('newstead', 'ジェニファー・ニューステッド', 'Jennifer Newstead', 2026, '法務・政府対応担当の上級副社長(顧問弁護士)。', '上級副社長(法務)'),
  P('obrien', 'ディアドラ・オブライエン', "Deirdre O'Brien", 1988, 'リテールと人事担当の上級副社長。', '上級副社長(リテール・人事)'),
  P('schiller', 'フィル・シラー', 'Phil Schiller', 1997, 'Apple Fellow。長くマーケティングを率い、App Storeなども担当しました。', 'Apple Fellow'),
  P('anderson', 'モリー・アンダーソン', 'Molly Anderson', 2026, '工業デザイン担当の副社長(公式ページ)。就任時期は確認できていません。', '副社長(工業デザイン)'),
  P('fenger', 'マイク・フェンジャー', 'Mike Fenger', 2026, '全世界セールス担当の副社長(公式ページ)。', '副社長(セールス)'),
  P('lemay', 'スティーブ・ルメイ', 'Steve Lemay', 2026, 'ヒューマンインターフェースデザイン担当の副社長(公式ページ)。', '副社長(HIデザイン)'),
  P('mahe', 'イザベル・ゲ・マエ', 'Isabel Ge Mahe', 2026, '大中華圏の副社長兼マネージングディレクター(公式ページ)。', '副社長(大中華圏)'),
  P('myhren', 'トア・ミレン', 'Tor Myhren', 2026, 'マーケティング・コミュニケーション担当の副社長(公式ページ)。', '副社長(マーケコミュ)'),
  P('quayle', 'クリスティン・ヒューゲ・クエイル', 'Kristin Huguet Quayle', 2026, '全世界コミュニケーション担当の副社長(公式ページ)。', '副社長(広報)'),
  # --- 取締役 ---
  P('levinson', 'アート・レビンソン', 'Arthur Levinson', 2000, '長く非業務執行の会長(2011年から)を務め、2026年9月から筆頭社外取締役。', '筆頭社外取締役'),
  P('jung', 'アンドレア・ジョン', 'Andrea Jung', 2008, '取締役。Grameen America社長兼CEO。', '社外取締役'),
  P('sugar', 'ロン・シュガー', 'Ron Sugar', 2010, '取締役。ノースロップ・グラマンの元CEO兼会長。', '社外取締役'),
  P('wagner', 'スー・ワグナー', 'Sue Wagner', 2014, '取締役。ブラックロックの共同創業者。', '社外取締役'),
  P('lozano', 'モニカ・ロサノ', 'Monica Lozano', 2021, '取締役。College Futures Foundationの元社長兼CEO。', '社外取締役'),
  P('gorsky', 'アレックス・ゴルスキー', 'Alex Gorsky', 2021, '取締役。ジョンソン・エンド・ジョンソンの元CEO兼執行会長。', '社外取締役'),
  P('austin', 'ワンダ・オースティン', 'Wanda Austin', 2024, '取締役。エアロスペース・コーポレーションの元社長兼CEO。', '社外取締役'),
  P('gore', 'アル・ゴア', 'Al Gore', 2003, '元取締役(2003〜2020年)。', '元取締役', 2020),
  P('campbell', 'ビル・キャンベル', 'Bill Campbell', 1997, '元取締役。ジョブズの相談役として知られました。', '元取締役', 2016),
  P('ellison', 'ラリー・エリソン', 'Larry Ellison', 1997, 'オラクルの創業者。元取締役(1997〜2002年)。', '元取締役', 2002),
  P('schmidt', 'エリック・シュミット', 'Eric Schmidt', 2006, 'グーグルの元CEO。元取締役(2006〜2009年)。', '元取締役', 2009),
  # --- 出資者 ---
  O('rock', 'アーサー・ロック', 1978, '初期の出資者。', '初期の出資者', 'i'),
  O('microsoft', 'Microsoft', 1997, '1997年に経営難のAppleへ出資(1.5億ドルと報じられています)。', '出資者(1997年)', 'i'),
  O('brk', 'Berkshire Hathaway', 2016, '2016年から保有。Appleの大口の株主として知られます(現在の比率は確認できていません)。', '株主(2016年〜)', 'i'),
  O('vanguard', 'Vanguard', 2026, '上位株主(約6.6%、Yahoo Finance、2026年6月30日時点)。', '株主(約6.6%)', 'i'),
  O('blackrock', 'BlackRock', 2026, '上位株主(約8.0%、Yahoo Finance、2026年6月30日時点)。', '株主(約8.0%)', 'i'),
  O('statest', 'State Street', 2026, '上位株主(約4.2%、Yahoo Finance、2026年6月30日時点)。', '株主(約4.2%)', 'i'),
  # --- 買収・関連 ---
  O('next', 'NeXT', 1997, '1997年に約4.04億ドルで買収。ジョブズの復帰とmacOSの土台になりました。', '買収(1997年)'),
  O('pasemi', 'P.A. Semi', 2008, '2008年に約2.78億ドルで買収。自社チップ開発の起点になりました。', '買収(2008年)'),
  O('anobit', 'Anobit', 2011, '2011年に約5億ドルで買収(フラッシュメモリ)。', '買収(2011年)'),
  O('authentec', 'AuthenTec', 2012, '2012年に約3.56億ドルで買収(指紋認証)。', '買収(2012年)'),
  O('primesense', 'PrimeSense', 2013, '2013年に約3.6億ドルで買収(3Dセンサー)。', '買収(2013年)'),
  O('beats', 'Beats Electronics', 2014, '2014年に約30億ドルで買収。', '買収(2014年)'),
  O('turi', 'Turi', 2016, '2016年に約2億ドルで買収(機械学習)。', '買収(2016年)'),
  O('shazam', 'Shazam', 2018, '2018年に買収(音楽認識)。', '買収(2018年)'),
  O('intelmodem', 'Intelのモデム事業', 2019, '2019年に約10億ドルで買収。', '買収(2019年)'),
  O('xnor', 'Xnor.ai', 2020, '2020年に約2億ドルで買収(端末上のAI)。', '買収(2020年)'),
  O('darksky', 'Dark Sky', 2020, '2020年に買収(天気アプリ)。', '買収(2020年)'),
  O('kudos', 'Credit Kudos', 2022, '2022年に約1.5億ドルで買収(英国の信用データ)。', '買収(2022年)'),
  O('qai', 'Q.ai', 2026, '2026年に約20億ドルで買収と報じられています(英語版Wikipediaの買収一覧)。', '買収(2026年・報道)'),
  O('openai', 'OpenAI', 2024, 'ChatGPTをAppleの製品に組み込む提携(2024年発表)。', '提携'),
 ],
 [
  ('jobs', 'woz', 'link', '共同創業'), ('jobs', 'wayne', 'link', '共同創業'), ('markkula', 'jobs', 'link', '出資・助言'),
  ('sculley', 'jobs', 'conflict'), ('amelio', 'jobs', 'link', '復帰を促す'),
  ('jobs', 'cook', 'link', '後継者に指名'), ('cook', 'ternus', 'link', 'CEO交代', 2026),
  ('williams', 'khan', 'link', 'COOを引き継ぐ', 2025), ('maestri', 'parekh', 'link', 'CFOを引き継ぐ', 2025),
  ('ive', 'jobs', 'link', 'デザインを率いる'), ('forstall', 'jobs', 'link'), ('fadell', 'jobs', 'link'),
  ('jobs', 'next', 'moved', 'NeXTを創業'), ('amelio', 'next', 'link', '買収を主導'),
  ('co', 'next', 'owns'), ('co', 'pasemi', 'owns'), ('co', 'anobit', 'owns'), ('co', 'authentec', 'owns'), ('co', 'primesense', 'owns'),
  ('co', 'beats', 'owns'), ('co', 'turi', 'owns'), ('co', 'shazam', 'owns'), ('co', 'intelmodem', 'owns'), ('co', 'xnor', 'owns'),
  ('co', 'darksky', 'owns'), ('co', 'kudos', 'owns'), ('co', 'qai', 'owns'), ('co', 'openai', 'link'),
 ],
 'ティム・クックが2011年から率いた世界最大級の時価総額の会社。1976年にジョブズ、ウォズニアック、ウェインが創業。2026年9月1日にジョン・ターナスがCEOへ就任し、クックは執行会長になりました。')
