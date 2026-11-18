"""Arm(アーム・ホールディングス)の会社ページ・人物・買収・お金の流れ・くわしい事実(出典つき)を、公開側(D1)に足す。何度実行しても同じ結果(自分の行だけ消して入れ直す)。
出典は、依頼で指定された2つのページだけ: 日本語版Wikipedia『ARMホールディングス』と、Arm公式サイト(日本語)。書かれていないことは書かない。
使い方: python -u -X utf8 -I add_arm.py [--push]    (--push なしは、SQLを作るだけ)"""
import os, subprocess, sys
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')
W = 'https://ja.wikipedia.org/wiki/ARM%E3%83%9B%E3%83%BC%E3%83%AB%E3%83%87%E3%82%A3%E3%83%B3%E3%82%B0%E3%82%B9'
A = 'https://www.arm.com/ja/'
SLUG = 'arm_holdings'
NAME = 'Arm Holdings'
NOTE = 'イギリス・ケンブリッジに本社を置く、半導体の設計図(CPUのIP)を貸す会社。工場を持たないファブレス企業で、設計をライセンスしている。ソフトバンクグループが86.4%を持つ(2026年5月21日現在)。2023年9月にNASDAQに上場。CEOはレネ・ハース(2022年から)。出典: 日本語版Wikipediaと、Arm公式サイト。'
# (部門, 事実, 出典URL)
FACTS = [
    ('概要', '1990年11月27日に設立。エイコーン・コンピュータの技術者がスピンアウトし、VLSIテクノロジーとの合弁として、Advanced RISC Machines社が発足した。Apple Computerが資金を出し、共同創業者になった。', W),
    ('概要', '「ARM」という略称は、1983年に最初に使われ、当初は「Acorn RISC Machine」の略だった。', W),
    ('概要', '本社はイギリス・ケンブリッジ。実際の事業は、子会社のARM Ltd.が行う。日本法人のアーム株式会社は、1994年に東京に開設された。', W),
    ('概要', 'Armは、クラウド・個人用デバイスから、AI定義型の自動車・ロボットまで、幅広い分野に、性能・効率・柔軟性を提供している、と公式サイトに書かれている。', A),
    ('創業者', '創業者として、ロビン・サクスビー、ジェイミー・アークハート、マイク・ミュラー、チューダー・ブラウン、リー・スミス、ジョン・ビッグス、ハリー・オールドハム、デイブ・ハワード、ピート・ハロッド、ハリー・ミーキングス、アル・トーマス、アンディ・メリット、デイビッド・シールの13人が挙げられている(Wikipedia)。', W),
    ('経営', '歴代のCEOは、ロビン・サクスビー(1991〜2001年)、ウォーレン・イースト(2001〜2013年)、サイモン・シガース(2013〜2022年)。現在のCEOは、レネ・ハース(2022年〜)。', W),
    ('経営', 'Wikipediaには、初代CEOがラリー・テスラーとの記載もあるが、歴代CEOの記載と一致しないため、ここでは歴代CEOの記載を使っている。', W),
    ('株主', 'ソフトバンクグループが、株式の86.4%を保有している(2026年5月21日現在)。', W),
    ('上場', '1998年に、ロンドン証券取引所とNASDAQに上場した(当時の社名はAdvanced RISC Machines Ltd)。', W),
    ('上場', '2023年4月29日に、米国での上場を、非公開で規制当局に申請した。2023年9月14日に、NASDAQに上場した。', W),
    ('上場', '2026年10月9日の入れ替え時点で、NASDAQ 100の構成銘柄に含まれている。', W),
    ('買収', '2016年9月5日に、ソフトバンクグループが、全株式を約240億ポンド(約3.3兆円)で買収した。', W),
    ('買収', '2020年9月14日に、NVIDIAが全株式を4.2兆円で買収すると発表した。2022年2月8日に、買収を断念した。米FTCや英国の競争・市場庁などが独占化の懸念を示し、承認が下りなかったとされる。', W),
    ('買収', '買収計画の中止後、ソフトバンクグループは、米国での新規株式公開を検討した。', W),
    ('子会社', '2018年6月に、中国子会社(安謀科技、Arm China)の株式51%を、中国の政府系企業連合に売却し、合弁企業にした。', W),
    ('子会社', 'Armが買収してきた会社: 1999年 Micrologic Solutions、2000年 Allant Software・Infinite Designs・EuroMIPS、2001年 Noral Micrologicsの開発チーム、2002年 NurLogic Design、2003年 Adelante Technologies、2004年 Axys Design Automation・Artisan Components、2005年 KEIL Software・PowerEscapeの開発チーム、2006年 Falanx、2018年8月3日 Treasure Data。', W),
    ('事業モデル', '自社工場を持たない、ファブレスの会社。CPUの設計に関する知的財産(IP)を、各社にライセンスしている。自社でCPUを作らず、ライセンスを受けた数十社が製造している。', W),
    ('事業モデル', 'Arm Flexible Accessでは、ライセンス料は、テープアウト(設計の完成)のときにだけ発生する、と公式サイトに書かれている。', A),
    ('技術', 'ARMアーキテクチャは、低消費電力が特徴で、32ビットの組み込みCPUの75%以上で採用されている(Wikipedia)。開発ツールは、RealViewと、2005年に買収したKEILのブランドで知られる。', W),
    ('製品', 'CPU: Cortex-A(アプリケーション向け)、Cortex-M(マイクロコントローラ向け)、Cortex-R、Cortex-X、Neoverse CPU。サーバー向け: Neoverse CSS、Neoverse CSS N4(「Arm史上最もコンフィギュラブルなCSS」)。', A),
    ('製品', 'Arm AGI CPU(AIデータセンター向けサーバーへの導入のために、Armが設計したSoC)、Arm C2 CPUクラスター(エージェント型AI向け)、CSS for Mobile 2(AIネイティブ体験向けのモバイル基盤)、Zena CSS(自動運転車・ロボット向け)、AEテクノロジーズ(安全性・セキュリティ向けIP)。', A),
    ('製品', 'GPU・NPU: Mali GPU(Mali G2-Ultra NXを含む)、Ethos NPU(オンデバイスAI推論向け)。ほかに、SI L2システムインターコネクト、システムIP、セキュリティIP、サブシステムIP、開発ツール。', A),
    ('自社チップ', '2026年3月に、AIデータセンター向けのCPUを、自社で開発して提供する事業(Arm AGI CPU)への参入を発表した(Wikipedia)。公式サイトにも、Arm AGI CPUとNeoverse CSS N4の発表が出ている。', W),
    ('数字', 'これまでに出荷されたArmベースのチップは、3,750億個以上。Armで開発するソフトウェア開発者は、3,000万人以上。接続された世界人口の100%に、Armベースの製品が浸透している(公式サイトの記載)。', A),
    ('数字', '2027年3月期の第2四半期の売上高は、過去最高の14.4億ドルで、ライセンス事業は50%成長した、と公式サイトに書かれている(日付の詳細は、ページに記載なし)。', A),
    ('業績', '連結、2026年3月期: 売上高49.2億ドル、営業利益9億ドル、利益9.04億ドル、総資産107.03億ドル、純資産82.86億ドル。従業員は9,584人(2026年3月)。', W),
    ('顧客・提携', 'Armの設計を使うSoCとして、Apple、ファーウェイ、サムスン電子などが挙げられている。任天堂のNintendo Switch(2017年発売)、AppleのMシリーズ(M1〜M4。2020年〜)、ノートPC(Surface Pro、HP OmniBook X 14、Dell XPS 13、ASUS Zenbookなど)にも採用されている(Wikipedia)。', W),
    ('顧客・提携', '注目のパートナーとして、Metaが挙げられている。事例として、AGIBOT(ロボット)、Tensor(自律システム)、NeuReality(AI推論)が紹介されている。エコシステムのプログラムとして、Arm Total Designがあり、フィジカルAIにも広げている(公式サイト)。', A),
    ('顧客・提携', '2024年2月22日に、アメリカの自動運転スタートアップ、ニューロと、レベル4の自動運転の開発で提携した。2024年に、ブリストルにデザインセンターを新設した(Wikipedia)。', W),
    ('論争', 'NVIDIAによる買収計画が、独占化の懸念で、2022年に断念された(上の「買収」を参照)。Wikipediaに書かれている論争は、この件のみ。', W),
]
# (名前, 英語名, 役割, 開始年, 終了年, メモ)
PEOPLE = [
    ('レネ・ハース', 'Rene Haas', 'CEO', '2022', '', '現在のCEO(2022年から)。'),
    ('サイモン・シガース', 'Simon Segars', '元CEO', '2013', '2022', 'CEO(2013〜2022年)。'),
    ('ウォーレン・イースト', 'Warren East', '元CEO', '2001', '2013', 'CEO(2001〜2013年)。'),
    ('ロビン・サクスビー', 'Robin Saxby', '元CEO / 共同創業者', '1991', '2001', '共同創業者の1人で、CEO(1991〜2001年)。'),
    ('ジェイミー・アークハート', 'Jamie Urquhart', '共同創業者', '1990', '', '創業者として挙げられている。'),
    ('マイク・ミュラー', 'Mike Muller', '共同創業者', '1990', '', '創業者として挙げられている。'),
    ('チューダー・ブラウン', 'Tudor Brown', '共同創業者', '1990', '', '創業者として挙げられている。'),
    ('リー・スミス', 'Lee Smith', '共同創業者', '1990', '', '創業者として挙げられている。'),
    ('ジョン・ビッグス', 'John Biggs', '共同創業者', '1990', '', '創業者として挙げられている。'),
    ('ハリー・オールドハム', 'Harry Oldham', '共同創業者', '1990', '', '創業者として挙げられている。'),
    ('デイブ・ハワード', 'Dave Howard', '共同創業者', '1990', '', '創業者として挙げられている。'),
    ('ピート・ハロッド', 'Pete Harrod', '共同創業者', '1990', '', '創業者として挙げられている。'),
    ('ハリー・ミーキングス', 'Harry Meekings', '共同創業者', '1990', '', '創業者として挙げられている。'),
    ('アル・トーマス', 'Al Thomas', '共同創業者', '1990', '', '創業者として挙げられている。'),
    ('アンディ・メリット', 'Andy Merritt', '共同創業者', '1990', '', '創業者として挙げられている。'),
    ('デイビッド・シール', 'David Seal', '共同創業者', '1990', '', '創業者として挙げられている。'),
]
ACQ = [
    ('1999', 'Micrologic Solutions', '', 'Armが買収(Wikipedia)'), ('2000', 'Allant Software', '', 'Armが買収(Wikipedia)'), ('2000', 'Infinite Designs', '', 'Armが買収(Wikipedia)'),
    ('2000', 'EuroMIPS', '', 'Armが買収(Wikipedia)'), ('2001', 'Noral Micrologicsの開発チーム', '', 'Armが獲得(Wikipedia)'), ('2002', 'NurLogic Design', '', 'Armが買収(Wikipedia)'),
    ('2003', 'Adelante Technologies', '', 'Armが買収(Wikipedia)'), ('2004', 'Axys Design Automation', '', 'Armが買収(Wikipedia)'), ('2004', 'Artisan Components', '', 'Armが買収(Wikipedia)'),
    ('2005', 'KEIL Software', '', 'Armが買収(Wikipedia)'), ('2005', 'PowerEscapeの開発チーム', '', 'Armが獲得(Wikipedia)'), ('2006', 'Falanx', '', 'Armが買収(Wikipedia)'),
    ('2018', 'Treasure Data', '', 'Armが買収(2018年8月3日、Wikipedia)'),
]
# (出す側, 受ける側, 種類, ラベル, 年, 金額, メモ, 出典)
MONEY = [
    ('ソフトバンクグループ', 'Arm Holdings', '買収', '全株式の買収', '2016', '約240億ポンド(約3.3兆円)', '2016年9月5日。', W),
    ('ソフトバンクグループ', 'Arm Holdings', '大株主', '86.4%', '2026', '', '2026年5月21日現在の保有比率。', W),
    ('NVIDIA', 'Arm Holdings', '買収', '2022年に断念', '2020', '4.2兆円', '2020年9月14日に発表。米FTCや英国の競争・市場庁などの懸念で、2022年2月8日に断念。', W),
    ('Apple', 'Arm Holdings', '出資', '設立時の資金提供', '1990', '', 'Apple Computerが資金を出し、共同創業者になった(エイコーン、VLSIテクノロジーとの合弁)。', W),
    ('Arm Holdings', 'Treasure Data', '買収', '', '2018', '', '2018年8月3日。', W),
    ('Arm Holdings', 'Arm China', '出資', '51%を売却', '2018', '', '2018年6月に、中国子会社の株式51%を、中国の政府系企業連合に売却し、合弁企業にした。', W),
]
q = lambda v: "'" + str('' if v is None else v).replace("'", "''") + "'"
L = ['CREATE TABLE IF NOT EXISTS company_fact (slug TEXT, sec TEXT, text TEXT, url TEXT, ord INTEGER);', 'CREATE INDEX IF NOT EXISTS i_cfact ON company_fact(slug);']
for t in ('mapco', 'mapco_people', 'mapco_acq', 'company_fact'):
    L.append('DELETE FROM %s WHERE slug=%s;' % (t, q(SLUG)))
L.append("DELETE FROM money_flow WHERE media='Arm(日本語版Wikipedia・公式)';")
L.append('INSERT INTO mapco VALUES (%s);' % ','.join([q(SLUG), q(NAME), q('Arm Holdings'), q(NOTE), q(''), str(len(PEOPLE)), str(len(ACQ))]))
for n, en, role, y, y2, note in PEOPLE:
    L.append('INSERT INTO mapco_people (slug,name,en,role,since,until,note) VALUES (%s);' % ','.join(q(x) for x in (SLUG, n, en, role, y, y2, note)))
for y, t, amt, note in ACQ:
    L.append('INSERT INTO mapco_acq VALUES (%s);' % ','.join(q(x) for x in (SLUG, y, t, amt, note)))
for i, (sec, tx, u) in enumerate(FACTS):
    L.append('INSERT INTO company_fact VALUES (%s,%s,%s,%s,%d);' % (q(SLUG), q(sec), q(tx), q(u), i))
for a, b, k, lab, y, amt, note, u in MONEY:
    L.append('INSERT INTO money_flow VALUES (%s);' % ','.join(q(x) for x in (a, b, k, lab, y, amt, note, u, 'Arm(日本語版Wikipedia・公式)', '')))
sql = os.path.join(SITE, 'arm.sql')
open(sql, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('文', len(L), '/ 事実', len(FACTS), '/ 人物', len(PEOPLE), '/ 買収', len(ACQ), '/ お金', len(MONEY), flush=True)
if '--push' in sys.argv:
    p = subprocess.run('npx wrangler d1 execute houjin --remote --yes --file="' + sql.replace(chr(92), '/') + '"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (p.stdout or '') + (p.stderr or '')
    if p.returncode != 0 or 'ERROR' in out:
        print('失敗', out[-400:])
        sys.exit(1)
    print('D1へ反映しました', flush=True)
