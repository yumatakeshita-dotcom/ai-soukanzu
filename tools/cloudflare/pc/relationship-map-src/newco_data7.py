from newco_data import mk, std, wp

# 子会社・関連会社の図(親会社の図で、関連組織をダブルクリックすると開く)
CO7 = {}

def eg(*t):
    """('a','b','kind'[,'label'[,since]]) の並びから、つながりのJSを作る"""
    out = ''
    for x in t:
        s = "E.push({a:'%s',b:'%s',k:'%s'" % (x[0], x[1], x[2])
        if len(x) > 3 and x[3]:
            s += ",label:'%s'" % x[3]
        if len(x) > 4:
            s += ",since:%d" % x[4]
        out += s + "});\n"
    return out

# ---------------- メルコイン ----------------
N = [
 {'id': 'melcoin', 'name': 'メルコイン', 'kind': 'c', 'from': 2022, 'desc': 'メルカリの暗号資産事業の子会社。ビットコインなどの売買サービスを運営しています(最新の役員構成と資本関係は公式資料で確認できていません)。'},
 {'id': 'nakamura', 'name': '中村奎太', 'kind': 'p', 'from': 2022, 'desc': '2022年10月からCPO(最高プロダクト責任者)を務め、のちにCEOへ就任したと報じられています(CEO就任の時期は確認できていません)。', 'role': 'CEO'},
 {'id': 'aoyagi', 'name': '青柳直樹', 'kind': 'p', 'from': 2022, 'to': 2024, 'desc': 'メルペイの経営者で、暗号資産子会社の代表も兼ねていたと報じられています(2020年代前半の報道)。2024年にメルカリを離れ、newmoを設立しました。', 'role': '元代表(兼務と報道)'},
 {'id': 'mercari', 'name': 'メルカリ', 'kind': 'o', 'from': 2022, 'desc': '親会社。'},
]
E = std('melcoin') + eg(('mercari', 'melcoin', 'owns', '親会社'))
CO7['melcoin'] = mk(N, E, {'nakamura': 'Keita Nakamura', 'aoyagi': 'Naoki Aoyagi'}, {}, {}, {}, {}, {}, 'melcoin')

# ---------------- メルペイ ----------------
N = [
 {'id': 'merpay', 'name': 'メルペイ', 'kind': 'c', 'from': 2017, 'desc': '2017年11月に、メルカリが100%出資して設立したスマホ決済・金融の会社。'},
 {'id': 'aoyagi', 'name': '青柳直樹', 'kind': 'p', 'from': 2017, 'to': 2024, 'desc': 'グリーの取締役CFOなどを経て参加し、設立時から代表を務めました。2020年の開示資料でも、メルカリの上級執行役員 兼 メルペイ代表取締役社長CEOと記載されています。2024年にメルカリを離れ、newmoを設立しました。', 'role': '代表取締役社長CEO(設立時〜)', 'founder': 1},
 {'id': 'nagasawa', 'name': '永沢岳志', 'kind': 'p', 'from': 2025, 'desc': '2025年12月のみんなの銀行とのBaaS提携のプレスリリースで、メルペイの代表取締役CEOと記載されています(就任時期は確認できていません)。', 'role': '代表取締役CEO(2025年12月時点)'},
 {'id': 'mercari', 'name': 'メルカリ', 'kind': 'o', 'from': 2017, 'desc': '親会社。設立時は100%出資。'},
 {'id': 'newmo', 'name': 'newmo', 'kind': 'o', 'from': 2024, 'desc': '青柳氏が2024年に設立した会社。'},
]
E = std('merpay') + eg(('mercari', 'merpay', 'owns', '100%出資(設立時)'), ('aoyagi', 'newmo', 'moved'))
CO7['merpay'] = mk(N, E, {'aoyagi': 'Naoki Aoyagi'}, {}, {}, {}, {}, {}, 'merpay')

# ---------------- 鹿島アントラーズ ----------------
N = [
 {'id': 'antlers', 'name': '鹿島アントラーズ', 'kind': 'c', 'from': 2019, 'desc': 'Jリーグのクラブ(株式会社鹿島アントラーズ・エフ・シー)。2019年にメルカリが日本製鉄の持ち株の大半を譲り受け、筆頭株主になりました。'},
 {'id': 'koizumi', 'name': '小泉文明', 'kind': 'p', 'from': 2019, 'desc': '2019年8月30日に、メルカリの社長のまま鹿島アントラーズの新社長に就任しました(現在の社長は確認できていません)。', 'role': '代表取締役社長(2019年〜)'},
 {'id': 'mercari', 'name': 'メルカリ', 'kind': 'i', 'from': 2019, 'desc': '日本製鉄などが持つ発行済株式72.5%のうち61.6%を譲り受ける契約を結んだ(取得額は約15億8,800万円)。譲渡後の持ち株比率は、メルカリ約61.6%と発表されました(2019年時点の見込み)。', 'role': '筆頭株主(61.6%・2019年の見込み)'},
 {'id': 'nipponsteel', 'name': '日本製鉄', 'kind': 'i', 'from': 2019, 'desc': '譲渡前の筆頭株主。譲渡後も約11.0%を持つ予定と報じられました(2019年時点)。', 'role': '株主(約11.0%・2019年の見込み)'},
 {'id': 'municipal', 'name': '地方自治体', 'kind': 'i', 'from': 2019, 'desc': '地元の自治体が合計で約10.8%を持つ予定と報じられました(2019年時点)。', 'role': '株主(約10.8%・2019年の見込み)'},
]
E = std('antlers')
CO7['antlers'] = mk(N, E, {'koizumi': 'Fumiaki Koizumi'}, {}, {'antlers': 'https://www.antlers.co.jp'}, wp(('antlers', 'Kashima_Antlers')), {}, {}, 'antlers')

# ---------------- Mercari US ----------------
N = [
 {'id': 'mercariUS', 'name': 'Mercari US', 'kind': 'c', 'from': 2014, 'desc': 'メルカリの米国事業(Mercari, Inc.)。2024年6月期の売上高は約2.93億ドルで、約1,700万ドルの赤字でした。2026年6月期は黒字転換と報じられています。'},
 {'id': 'yamada', 'name': '山田進太郎', 'kind': 'p', 'from': 2025, 'desc': 'メルカリの創業者。2025年1月1日付で、米国のMercari, Inc.のCEOも兼任しています。', 'role': 'CEO(兼任・2025年1月〜)', 'founder': 1},
 {'id': 'lagerling', 'name': 'ジョン・ラガリング', 'kind': 'p', 'from': 2017, 'to': 2025, 'desc': 'メルカリの執行役 SVP of Global Strategy 兼 米国Mercari, Inc.のCEO。2024年12月31日付で執行役を退任しました。', 'role': '元CEO(〜2024年12月)'},
 {'id': 'mercari', 'name': 'メルカリ', 'kind': 'o', 'from': 2014, 'desc': '親会社。'},
]
E = std('mercariUS') + eg(('mercari', 'mercariUS', 'owns', '親会社'))
CO7['mercariUS'] = mk(N, E, {'yamada': 'Shintaro Yamada', 'lagerling': 'John Lagerling'}, {}, {}, {}, {}, {}, 'mercariUS')

# ---------------- PayPay ----------------
N = [
 {'id': 'paypay', 'name': 'PayPay', 'kind': 'c', 'from': 2018, 'desc': 'ソフトバンクグループとLINEヤフー(旧Zホールディングス)の合弁として、2018年に発足したスマホ決済の会社。2026年3月12日(米国東部時間)にNasdaqへ上場しました(ティッカー「PAYP」、公募価格16ドル。報道)。'},
 {'id': 'nakayama', 'name': '中山一郎', 'kind': 'p', 'from': 2018, 'desc': '2018年6月にPayPayの社長・代表取締役・CEOに就任。2021年4月までヤフー(のちZホールディングス)の執行役員も務めました。2026年6月付で、ソフトバンクの取締役にも選ばれました。', 'role': '代表取締役 社長執行役員CEO', 'founder': 1},
 {'id': 'deya', 'name': '出谷剛', 'kind': 'p', 'from': 2026, 'desc': '非常勤取締役。2026年6月29日付の人事発表で再任(就任時期は確認できていません)。', 'role': '非常勤取締役'},
 {'id': 'goto', 'name': '後藤義光', 'kind': 'p', 'from': 2026, 'desc': '非常勤取締役。2026年6月29日付の人事発表で再任(就任時期は確認できていません)。', 'role': '非常勤取締役'},
 {'id': 'miyakawa', 'name': '宮川潤一', 'kind': 'p', 'from': 2026, 'desc': '非常勤取締役。ソフトバンクの代表取締役社長執行役員兼CEO。2026年6月29日付で再任。', 'role': '非常勤取締役'},
 {'id': 'takasu', 'name': '高須文哉', 'kind': 'p', 'from': 2026, 'desc': '非常勤取締役。2026年6月29日付の人事発表で新任。', 'role': '非常勤取締役(新任)'},
 {'id': 'karasawa', 'name': '唐澤康良', 'kind': 'p', 'from': 2026, 'desc': '社外取締役(監査等委員)。2026年6月29日付の人事発表に記載。', 'role': '社外取締役(監査等委員)'},
 {'id': 'yonamine', 'name': 'ポール・ヨナミネ', 'kind': 'p', 'from': 2026, 'desc': '社外取締役(監査等委員)。2026年6月29日付の人事発表に記載(Paul Yonamine)。', 'role': '社外取締役(監査等委員)'},
 {'id': 'softbank', 'name': 'ソフトバンクグループ', 'kind': 'o', 'from': 2018, 'desc': '合弁の親会社の一つ。上場後も、ソフトバンクグループと関連会社が過半数を保有し、連結子会社にとどまる見通しと報じられています(2026年2月時点)。', 'role': '親会社(合弁)'},
 {'id': 'ly', 'name': 'LINEヤフー', 'kind': 'o', 'from': 2018, 'desc': '合弁の親会社の一つ(旧ヤフー、Zホールディングス)。', 'role': '親会社(合弁)'},
 {'id': 'sbcorp', 'name': 'ソフトバンク', 'kind': 'o', 'from': 2018, 'desc': '通信事業のソフトバンク株式会社。', 'role': '関連会社'},
]
E = std('paypay') + eg(('softbank', 'paypay', 'owns', '合弁'), ('ly', 'paypay', 'owns', '合弁'), ('sbcorp', 'paypay', 'link', ''), ('nakayama', 'sbcorp', 'link', '取締役(2026年6月〜)'), ('miyakawa', 'sbcorp', 'link', '社長'))
CO7['paypay'] = mk(N, E, {'nakayama': 'Ichiro Nakayama', 'deya': 'Tsuyoshi Deya', 'goto': 'Yoshimitsu Goto', 'miyakawa': 'Junichi Miyakawa', 'takasu': 'Fumiya Takasu', 'karasawa': 'Yasuyoshi Karasawa', 'yonamine': 'Paul Yonamine'},
 {}, {'paypay': 'https://about.paypay.ne.jp'}, wp(('paypay', 'PayPay')),
 {'nakayama': [['2018', 'PayPayの社長・代表取締役・CEOに就任'], ['2021', 'ヤフー(Zホールディングス)の執行役員を退任'], ['2026', 'PayPayがNasdaqに上場(報道)・ソフトバンクの取締役に']]}, {}, 'paypay')

# ---------------- ソフトバンク(通信) ----------------
N = [
 {'id': 'sbcorp', 'name': 'ソフトバンク', 'kind': 'c', 'from': 2014, 'desc': '通信事業のソフトバンク株式会社(東証9434)。LINEヤフー、PayPayなどを傘下に持つ、ソフトバンクグループの上場子会社です。'},
 {'id': 'miyakawa', 'name': '宮川潤一', 'kind': 'p', 'from': 2018, 'desc': '代表取締役 社長執行役員 兼 CEO。2026年6月の株主総会で取締役に再任されました(2026年6月26日付のコーポレートガバナンス報告書に記載)。', 'role': '代表取締役 社長執行役員 兼 CEO'},
 {'id': 'shimba', 'name': '榛葉淳', 'kind': 'p', 'from': 2026, 'desc': '2026年4月1日付で取締役会長に異動。宮川氏とともに、引き続き経営を率います(2026年1月29日の発表)。', 'role': '取締役会長'},
 {'id': 'imai', 'name': '今井康之', 'kind': 'p', 'from': 2019, 'to': 2026, 'desc': '2026年4月1日付で、取締役会長から取締役特別顧問に異動。2026年6月の株主総会の取締役選任議案に名前はありません(任期満了)。', 'role': '元取締役会長'},
 {'id': 'son', 'name': '孫正義', 'kind': 'p', 'from': 2026, 'desc': 'ソフトバンクグループの創業者。2026年6月の株主総会で取締役に選ばれた13人に含まれます。', 'role': '取締役'},
 {'id': 'idezawa', 'name': '出澤剛', 'kind': 'p', 'from': 2026, 'desc': '取締役(2026年6月選任)。LINEヤフーの社長。', 'role': '取締役'},
 {'id': 'nakayama', 'name': '中山一郎', 'kind': 'p', 'from': 2026, 'desc': '取締役(2026年6月選任)。PayPayの社長CEO。', 'role': '取締役'},
 {'id': 'akiyama', 'name': '秋山修', 'kind': 'p', 'from': 2026, 'desc': '取締役(2026年6月選任)。', 'role': '取締役'},
 {'id': 'horiba', 'name': '堀場厚', 'kind': 'p', 'from': 2026, 'desc': '取締役(2026年6月選任)。', 'role': '取締役'},
 {'id': 'koshi', 'name': '越直美', 'kind': 'p', 'from': 2026, 'desc': '取締役(2026年6月選任)。', 'role': '取締役'},
 {'id': 'sakamoto', 'name': '坂本真樹', 'kind': 'p', 'from': 2026, 'desc': '取締役(2026年6月選任)。', 'role': '取締役'},
 {'id': 'sasaki', 'name': '佐々木裕子', 'kind': 'p', 'from': 2026, 'desc': '取締役(2026年6月選任)。', 'role': '取締役'},
 {'id': 'karaki', 'name': '唐木秀明', 'kind': 'p', 'from': 2026, 'desc': '取締役(2026年6月選任)。', 'role': '取締役'},
 {'id': 'onishi', 'name': '大西幸彦', 'kind': 'p', 'from': 2026, 'desc': '取締役(2026年6月選任)。', 'role': '取締役'},
 {'id': 'yuzaki', 'name': '湯﨑英彦', 'kind': 'p', 'from': 2026, 'desc': '取締役(2026年6月選任)。', 'role': '取締役'},
 {'id': 'naito', 'name': '内藤隆志', 'kind': 'p', 'from': 2026, 'desc': '監査役(2026年6月時点)。', 'role': '監査役'},
 {'id': 'kudo', 'name': '工藤陽子', 'kind': 'p', 'from': 2026, 'desc': '監査役(2026年6月時点)。', 'role': '監査役'},
 {'id': 'softbank', 'name': 'ソフトバンクグループ', 'kind': 'o', 'from': 2014, 'desc': '親会社。', 'role': '親会社'},
 {'id': 'ly', 'name': 'LINEヤフー', 'kind': 'o', 'from': 2019, 'desc': 'ソフトバンクの子会社(A Holdings経由)。', 'role': '子会社'},
 {'id': 'paypay', 'name': 'PayPay', 'kind': 'o', 'from': 2018, 'desc': 'スマホ決済。2026年3月にNasdaqへ上場したと報じられています。', 'role': '関連会社'},
]
E = std('sbcorp') + eg(('softbank', 'sbcorp', 'owns', '親会社'), ('sbcorp', 'ly', 'owns', '傘下'), ('sbcorp', 'paypay', 'link', ''), ('imai', 'shimba', 'moved'), ('son', 'softbank', 'link', '創業者'))
CO7['sbcorp'] = mk(N, E, {'miyakawa': 'Junichi Miyakawa', 'shimba': 'Jun Shimba', 'imai': 'Yasuyuki Imai', 'son': 'Masayoshi Son', 'idezawa': 'Takeshi Idezawa', 'nakayama': 'Ichiro Nakayama',
 'akiyama': 'Osamu Akiyama', 'horiba': 'Atsushi Horiba', 'koshi': 'Naomi Koshi', 'sakamoto': 'Maki Sakamoto', 'sasaki': 'Yuko Sasaki', 'karaki': 'Hideaki Karaki', 'onishi': 'Yukihiko Onishi', 'yuzaki': 'Hidehiko Yuzaki', 'naito': 'Takashi Naito', 'kudo': 'Yoko Kudo'},
 {}, {'sbcorp': 'https://www.softbank.jp/corp/'}, wp(('sbcorp', 'SoftBank_Corp.')), {}, {}, 'sbcorp')

# ---------------- Arm ----------------
N = [
 {'id': 'arm', 'name': 'Arm', 'kind': 'c', 'from': 2016, 'desc': '英国の半導体設計会社。2016年にソフトバンクグループが買収し、2023年にNasdaqへ再上場しました。ソフトバンクグループが支配株主で、非業務執行取締役はすべてソフトバンクグループが指名しています(2026年3月期の20-F)。'},
 {'id': 'haas', 'name': 'レネ・ハース', 'kind': 'p', 'from': 2022, 'desc': '2022年2月からArmのCEO兼取締役。2026年4月に、ソフトバンクグループ傘下の「SoftBank Group International」のCEOにも就きました(Armの業務を妨げない限定的な役割と説明)。2023年6月からソフトバンクグループの取締役。', 'role': 'CEO', 'founder': 0},
 {'id': 'child', 'name': 'ジェイソン・チャイルド', 'kind': 'p', 'from': 2022, 'desc': 'EVP兼CFO。2022年11月から(20-F)。', 'role': 'CFO'},
 {'id': 'eaton', 'name': 'シャーロット・イートン', 'kind': 'p', 'from': 2024, 'desc': 'Chief People Officer(最高人事責任者)。2024年11月から(20-F)。', 'role': 'Chief People Officer'},
 {'id': 'son', 'name': '孫正義', 'kind': 'p', 'from': 2016, 'desc': 'ソフトバンクグループの創業者。第三者の情報サイトはArmの会長としていますが、Armの提出書類では確認できていません。', 'role': '親会社の創業者(Arm会長とする情報サイトあり・未確認)'},
 {'id': 'softbank', 'name': 'ソフトバンクグループ', 'kind': 'o', 'from': 2016, 'desc': '支配株主。株主間協定により、取締役候補のうち7人を指名できます(2026年3月期の20-F)。2023年の再上場直後は、約90%を保有と報じられました(現在の比率は未確認)。', 'role': '支配株主'},
]
E = std('arm') + eg(('softbank', 'arm', 'owns', '支配株主'), ('haas', 'softbank', 'link', '取締役(2023年6月〜)'))
CO7['arm'] = mk(N, E, {'haas': 'Rene Haas', 'child': 'Jason Child', 'eaton': 'Charlotte Eaton', 'son': 'Masayoshi Son'}, {}, {'arm': 'https://www.arm.com'}, wp(('arm', 'Arm_Holdings')), {}, {}, 'arm')

# ---------------- Matlantis (PFCC) ----------------
N = [
 {'id': 'pfcc', 'name': 'Matlantis(PFCC)', 'kind': 'c', 'from': 2021, 'desc': '2021年6月1日に、PFNとENEOSの共同出資で設立された株式会社Preferred Computational Chemistry。材料探索のシミュレーターMatlantisを提供しています。設立時の出資比率はPFN 51%、ENEOS 49%(2024年以降の比率は未確認)。'},
 {'id': 'okanohara', 'name': '岡野原大輔', 'kind': 'p', 'from': 2021, 'desc': '設立時から代表取締役社長。PFNの共同創業者で、代表取締役 最高技術責任者を兼ねています(2025年7月の経歴資料)。', 'role': '代表取締役社長', 'founder': 1},
 {'id': 'eneos', 'name': 'ENEOS', 'kind': 'i', 'from': 2021, 'desc': '共同出資者(設立時49%)。', 'role': '出資者(設立時49%)'},
 {'id': 'mitsubishi', 'name': '三菱商事', 'kind': 'i', 'from': 2024, 'desc': '2024年6月に、業務・資本提携を締結したと、公式の沿革にあります。', 'role': '提携・出資(2024年6月)'},
 {'id': 'pfn', 'name': 'Preferred Networks', 'kind': 'o', 'from': 2021, 'desc': '共同出資者(設立時51%)。', 'role': '親会社(設立時51%)'},
]
E = std('pfcc') + eg(('pfn', 'pfcc', 'owns', '設立時51%'))
CO7['pfcc'] = mk(N, E, {'okanohara': 'Daisuke Okanohara'}, {}, {'pfcc': 'https://matlantis.com'}, {}, {}, {}, 'pfcc')

# ---------------- Isomorphic Labs ----------------
N = [
 {'id': 'isomorphic', 'name': 'Isomorphic Labs', 'kind': 'c', 'from': 2021, 'desc': 'Alphabet傘下の、AI創薬の会社。2026年5月12日に、21億ドルのシリーズBを発表しました(Thrive Capital主導。評価額は非公開)。'},
 {'id': 'hassabis', 'name': 'デミス・ハサビス', 'kind': 'p', 'from': 2021, 'desc': '創業者でCEO(今回の検索では役職を確認できていないため、広く知られた情報に基づきます)。Google DeepMindのCEOも務めています。', 'role': 'CEO / 創業者', 'founder': 1},
 {'id': 'jaderberg', 'name': 'マックス・ジェイダーバーグ', 'kind': 'p', 'from': 2021, 'desc': 'President。シリーズBの発表資料に、その肩書の談話が載っています。', 'role': 'President'},
 {'id': 'thrive', 'name': 'Thrive Capital', 'kind': 'i', 'from': 2025, 'desc': '2026年のシリーズBを主導した既存の出資者。最初の資金調達も主導しました(2025年)。', 'role': '主導出資者'},
 {'id': 'alphabet', 'name': 'Alphabet', 'kind': 'i', 'from': 2021, 'desc': '親会社。シリーズBにも既存の出資者として参加。', 'role': '親会社・出資者'},
 {'id': 'gv', 'name': 'GV', 'kind': 'i', 'from': 2025, 'desc': 'シリーズBに、既存の出資者として参加。', 'role': '出資者'},
 {'id': 'mgx', 'name': 'MGX', 'kind': 'i', 'from': 2026, 'desc': 'シリーズBの新規の出資者。', 'role': '出資者(2026年)'},
 {'id': 'temasek', 'name': 'Temasek', 'kind': 'i', 'from': 2026, 'desc': 'シリーズBの新規の出資者。', 'role': '出資者(2026年)'},
 {'id': 'capitalg', 'name': 'CapitalG', 'kind': 'i', 'from': 2026, 'desc': 'シリーズBの新規の出資者。', 'role': '出資者(2026年)'},
 {'id': 'uksai', 'name': 'UK Sovereign AI Fund', 'kind': 'i', 'from': 2026, 'desc': 'シリーズBの新規の出資者。', 'role': '出資者(2026年)'},
 {'id': 'deepmind', 'name': 'Google DeepMind', 'kind': 'o', 'from': 2021, 'desc': 'ハサビスが率いる姉妹組織。', 'role': '関連組織'},
]
E = std('isomorphic') + eg(('alphabet', 'isomorphic', 'owns', '親会社'), ('hassabis', 'deepmind', 'link', 'CEO'))
CO7['isomorphic'] = mk(N, E, {'hassabis': 'Demis Hassabis', 'jaderberg': 'Max Jaderberg'}, {}, {'isomorphic': 'https://www.isomorphiclabs.com'}, wp(('isomorphic', 'Isomorphic_Labs')), {}, {}, 'isomorphic')

# ---------------- 楽天モバイル ----------------
N = [
 {'id': 'rakutenmobile', 'name': '楽天モバイル', 'kind': 'c', 'from': 2018, 'desc': '楽天グループの携帯電話事業の会社。'},
 {'id': 'yazawa', 'name': '矢澤俊介', 'kind': 'p', 'from': 2023, 'desc': '代表取締役社長として名前が出ている人物(2023年10月の報道。現在の社長かどうかは確認できていません)。', 'role': '代表取締役社長(2023年10月の報道)'},
 {'id': 'mikitani', 'name': '三木谷浩史', 'kind': 'p', 'from': 2018, 'desc': '親会社の楽天グループの会長兼社長。', 'role': '親会社の会長兼社長'},
 {'id': 'rakuten', 'name': '楽天グループ', 'kind': 'o', 'from': 2018, 'desc': '親会社。', 'role': '親会社'},
]
E = std('rakutenmobile') + eg(('rakuten', 'rakutenmobile', 'owns', '親会社'))
CO7['rakutenmobile'] = mk(N, E, {'yazawa': 'Shunsuke Yazawa', 'mikitani': 'Hiroshi Mikitani'}, {}, {}, {}, {}, {}, 'rakutenmobile')

# ---------------- Vision Fund ----------------
N = [
 {'id': 'visionfund', 'name': 'Vision Fund', 'kind': 'c', 'from': 2017, 'desc': 'ソフトバンクグループの投資ファンド(SB Investment Advisersが運用)。'},
 {'id': 'clavel', 'name': 'アレックス・クラベル', 'kind': 'p', 'from': 2017, 'desc': '2024年11月に、ミスラ氏の退任により、Vision Fundの運用会社の単独CEOになったと報じられています。', 'role': 'CEO(単独・2024年11月〜)'},
 {'id': 'misra', 'name': 'ラジーヴ・ミスラ', 'kind': 'p', 'from': 2017, 'to': 2025, 'desc': 'Vision Fundの共同CEO。2022年にソフトバンクグループの役員を退き、2024年11月に運用会社の指導的な役職を退くと発表されました(2026年7月の再報道とする記事は、確認できていません)。', 'role': '元共同CEO'},
 {'id': 'son', 'name': '孫正義', 'kind': 'p', 'from': 2017, 'desc': 'ソフトバンクグループの創業者。Vision Fund 2には、より直接関わるようになりました(2022年の報道)。', 'role': '創業者(親会社)'},
 {'id': 'softbank', 'name': 'ソフトバンクグループ', 'kind': 'o', 'from': 2017, 'desc': '親会社。', 'role': '親会社'},
]
E = std('visionfund') + eg(('softbank', 'visionfund', 'owns', '運用'))
CO7['visionfund'] = mk(N, E, {'clavel': 'Alex Clavel', 'misra': 'Rajeev Misra', 'son': 'Masayoshi Son'}, {}, {}, {}, {}, {}, 'visionfund')

# ---------------- Preferred Robotics ----------------
N = [
 {'id': 'probots', 'name': 'Preferred Robotics', 'kind': 'c', 'from': 2021, 'desc': 'Preferred Networksの主要子会社(2025年のファクトシート)。ロボットの会社です。'},
 {'id': 'isobe', 'name': '礒部達', 'kind': 'p', 'from': 2021, 'desc': '代表取締役CEO。2021年の開示資料と、2026年のプレスリリースの両方に、この肩書で記載されています。', 'role': '代表取締役CEO'},
 {'id': 'pfn', 'name': 'Preferred Networks', 'kind': 'o', 'from': 2021, 'desc': '親会社。', 'role': '親会社'},
]
E = std('probots') + eg(('pfn', 'probots', 'owns', '親会社'))
CO7['probots'] = mk(N, E, {'isobe': 'Tatsu Isobe'}, {}, {}, {}, {}, {}, 'probots')

# ---------------- Ernie MLG (PKSHA) ----------------
N = [
 {'id': 'ernie', 'name': 'アーニーMLG', 'kind': 'c', 'from': 2024, 'desc': 'PKSHA Technologyが、2024年12月の開示で、株式の追加取得による子会社化を決議した会社。'},
 {'id': 'hashimoto', 'name': '橋本聡', 'kind': 'p', 'from': 2024, 'desc': '2024年12月の開示時点の代表取締役(現在の代表かどうかは確認できていません)。', 'role': '代表取締役(2024年12月時点)'},
 {'id': 'pksha', 'name': 'PKSHA Technology', 'kind': 'o', 'from': 2024, 'desc': '親会社。代表取締役は上野山勝也氏(2024年12月〜2025年1月の開示)。', 'role': '親会社'},
]
E = std('ernie') + eg(('pksha', 'ernie', 'owns', '子会社化'))
CO7['ernie'] = mk(N, E, {'hashimoto': 'Satoshi Hashimoto'}, {}, {}, {}, {}, {}, 'ernie')
