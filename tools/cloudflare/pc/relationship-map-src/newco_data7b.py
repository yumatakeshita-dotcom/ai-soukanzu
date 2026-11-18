from newco_data import mk, std
from newco_data7 import eg

# 第2弾: 投資先・関連会社
CO7B = {}

def P_(id, name, frm, desc, role, **kw):
    d = {'id': id, 'name': name, 'kind': 'p', 'from': frm, 'desc': desc, 'role': role}
    d.update(kw)
    return d

def O_(id, name, frm, desc, role='', kind='o'):
    return {'id': id, 'name': name, 'kind': kind, 'from': frm, 'desc': desc, 'role': role}

# ---------------- IVRy ----------------
N = [
 O_('ivry', 'IVRy(アイブリー)', 2019, '電話応対AIの会社。2019年3月設立(旧Peoplytics)。2024年5月にシリーズCで30億円を調達し、累計は約49.5億円と報じられました。', '', 'c'),
 P_('okunishi', '奥西亮賀', 2019, '創業者で代表取締役CEO。同志社大学大学院を修了し、リクルートを経て2019年3月に創業しました。', '代表取締役 CEO', founder=1),
 P_('tai', '田井義輝', 2019, '公式サイトのメンバー紹介にある役職(就任時期は確認できていません)。', 'CSO'),
 P_('nishio', '西尾知一', 2019, '公式サイトのメンバー紹介にある役職(就任時期は確認できていません)。', 'CHRO'),
 P_('machida', '町田雄哉', 2019, '公式サイトのメンバー紹介にある役職(就任時期は確認できていません)。', 'Head of Product'),
 P_('miyata', '宮田道生', 2019, '公式サイトのメンバー紹介にある役職(就任時期は確認できていません)。', 'Head of Strategy'),
 O_('boost', 'Boost Capital', 2025, '2025年11月のシリーズDに、共同投資家として参加と報じられています。', '出資者', 'i'),
]
CO7B['ivry'] = mk(N, std('ivry'), {'okunishi': 'Ryoga Okunishi', 'tai': 'Yoshiki Tai', 'nishio': 'Tomokazu Nishio', 'machida': 'Yuya Machida', 'miyata': 'Michinari Miyata'}, {}, {'ivry': 'https://ivry.jp'}, {}, {}, {}, 'ivry')

# ---------------- Kotoba Technologies ----------------
N = [
 O_('kotoba', 'Kotoba Technologies', 2023, 'リアルタイム音声AIモデルと同時通訳技術を開発する会社。米国法人は2023年7月、日本法人は2023年10月に設立(公式サイト)。', '', 'c'),
 P_('kojima', 'ノリユキ・コジマ', 2023, '共同創業者でCEO(Noriyuki Kojima)。公式サイトに記載。', 'CEO / 共同創業者', founder=1),
 P_('kasai', 'ジュンゴ・カサイ', 2023, '共同創業者でCTO(Jungo Kasai)。公式サイトに記載。', 'CTO / 共同創業者', founder=1),
 O_('boost', 'Boost Capital', 2025, '2025年8月のシードを主導したと報じられています。', '主導出資者', 'i'),
]
CO7B['kotoba'] = mk(N, std('kotoba'), {'kojima': 'Noriyuki Kojima', 'kasai': 'Jungo Kasai'}, {}, {'kotoba': 'https://site.kotoba.tech'}, {}, {}, {}, 'kotoba')

# ---------------- Solafune ----------------
N = [
 O_('solafune', 'Solafune', 2020, '衛星データの解析とデータ競技を手がける会社。', '', 'c'),
 P_('uechi', 'レン・ウエチ', 2020, 'CEO(公式サイトに「Representative, Ren Uechi」)。日本語の表記は確認できていません。', 'CEO'),
 O_('boost', 'Boost Capital', 2026, '2026年3月のシリーズAに、共同投資家として参加と報じられています。', '出資者', 'i'),
]
CO7B['solafune'] = mk(N, std('solafune'), {'uechi': 'Ren Uechi'}, {}, {'solafune': 'https://solafune.com'}, {}, {}, {}, 'solafune')

# ---------------- TERASS ----------------
N = [
 O_('terass', 'TERASS(テラス)', 2019, '不動産仲介のプロが集まる「次世代不動産エージェントファーム」。2019年4月設立(公式サイト)。', '', 'c'),
 P_('eguchi', '江口亮介', 2019, '代表取締役社長(公式の会社概要)。', '代表取締役社長'),
 P_('kosaka', '高坂昌行', 2019, '創業者でCTO(公式サイトの記載)。取締役かどうかは確認できていません。', 'CTO / 創業者', founder=1),
 P_('inoue', '井上利勉', 2019, '取締役COO(公式の会社概要)。', '取締役 COO'),
 P_('morio', '森尾健一郎', 2019, '取締役CFO(公式の会社概要)。', '取締役 CFO'),
 P_('murata', '村田祐介', 2019, '社外取締役(公式の会社概要)。', '社外取締役'),
 P_('takahashi', '高橋健太', 2019, '社外取締役(公式の会社概要)。', '社外取締役'),
 O_('boost', 'Boost Capital', 2025, '2025年7月のシリーズCに、共同投資家として参加と報じられています。', '出資者', 'i'),
]
CO7B['terass'] = mk(N, std('terass'), {'eguchi': 'Ryosuke Eguchi', 'kosaka': 'Masayuki Kosaka', 'inoue': 'Toshikatsu Inoue', 'morio': 'Kenichiro Morio', 'murata': 'Yusuke Murata', 'takahashi': 'Kenta Takahashi (TERASS)'}, {}, {'terass': 'https://terass.com'}, {}, {}, {}, 'terass')

# ---------------- ラクスル ----------------
N = [
 O_('raksul', 'ラクスル', 2009, '印刷・物流・金融などを手がける会社。載せた役員は、公式サイトの経営陣のページに基づきます。', '', 'c'),
 P_('nagami', '永見世央', 2024, '代表取締役社長 グループCEO(公式サイト。就任時期は確認できていません)。', '代表取締役社長 グループCEO'),
 P_('matsumoto', '松本恭攝', 2009, '創業者で取締役会長。ジョーシスの代表取締役社長を兼任。', '取締役会長 / 創業者', founder=1),
 P_('itoki', '糸木悠', 2024, '社外取締役。', '社外取締役'),
 P_('kang', '姜嘉承', 2024, '社外取締役。', '社外取締役'),
 P_('ozawa', '小澤隆生', 2026, '社外取締役。2026年8月3日の発表で就任。Boost Capitalの代表取締役。', '社外取締役'),
 P_('takaie', '高家正行', 2026, '社外取締役。2026年9月18日の発表で就任。カインズの代表取締役社長CEO。', '社外取締役'),
 P_('kobayashi', '小林賢治', 2024, '社外取締役。', '社外取締役'),
 P_('utsunomiya', '宇都宮純子', 2024, '社外取締役。', '社外取締役'),
 P_('watanabe', '渡邊建', 2024, '上級執行役員(ラクスル事業本部長、金融事業本部長)。ハンコヤドットコムの代表取締役社長CEOを兼任。', '上級執行役員'),
 P_('tabe', '田部正樹', 2024, '上級執行役員 グループCRO。ノバセルの代表取締役社長を兼任。', '上級執行役員 グループCRO'),
 P_('takeuchi', '竹内俊治', 2024, '上級執行役員 グループCTO。', '上級執行役員 グループCTO'),
 O_('boost', 'Boost Capital', 2026, '小澤氏が代表を務める投資会社。', '関連'),
]
CO7B['raksul'] = mk(N, std('raksul') + eg(('matsumoto', 'nagami', 'link', '後任のCEO'), ('ozawa', 'boost', 'link', '代表取締役')),
 {'nagami': 'Seo Nagami', 'matsumoto': 'Yasukane Matsumoto', 'itoki': 'Yu Itoki', 'kang': 'Kasyou Kang', 'ozawa': 'Takao Ozawa', 'takaie': 'Masayuki Takaie', 'kobayashi': 'Kenji Kobayashi', 'utsunomiya': 'Junko Utsunomiya', 'watanabe': 'Ken Watanabe (Raksul)', 'tabe': 'Masaki Tabe', 'takeuchi': 'Shunji Takeuchi'},
 {}, {'raksul': 'https://corp.raksul.com'}, {}, {}, {}, 'raksul')

# ---------------- 楽天カード ----------------
N = [
 O_('rcard', '楽天カード', 2005, '楽天グループのクレジットカード会社。', '', 'c'),
 P_('nakamuraK', '中村晃一', 2026, '代表取締役社長(2026年4月1日時点の会社概要)。', '代表取締役社長'),
 O_('rakuten', '楽天グループ', 2005, '株式の85.0002%を保有(2026年4月1日時点)。', '親会社(85.0002%)', 'i'),
 O_('mizuho', 'みずほ銀行', 2005, '株式の14.9998%を保有(2026年4月1日時点)。', '株主(14.9998%)', 'i'),
 O_('rbank', '楽天銀行', 2026, '2026年10月1日付で、楽天銀行が楽天カードを株式交付で子会社にする予定と開示されています(2026年5月20日)。', '株式交付の予定'),
]
CO7B['rcard'] = mk(N, std('rcard') + eg(('rbank', 'rcard', 'owns', '株式交付(2026年10月予定)', 2026)), {'nakamuraK': 'Koichi Nakamura'}, {}, {}, {}, {}, {}, 'rcard')

# ---------------- 楽天銀行 ----------------
N = [
 O_('rbank', '楽天銀行', 2000, '楽天グループのネット銀行。', '', 'c'),
 P_('tohbayashi', '東林知隆', 2020, '代表取締役社長。2026年6月24日の定時株主総会後の取締役会で、代表取締役の選定が正式決定する予定でした(結果は確認できていません)。', '代表取締役社長'),
 O_('rcard', '楽天カード', 2026, '2026年10月1日付で、株式交付により子会社になる予定と開示されています。', '子会社化の予定'),
 O_('rsec', '楽天証券', 2026, '楽天証券ホールディングスが、株式交付により楽天銀行の子会社になる予定と開示されています。', '子会社化の予定'),
]
CO7B['rbank'] = mk(N, std('rbank') + eg(('rbank', 'rcard', 'owns', '株式交付(2026年10月予定)', 2026), ('rbank', 'rsec', 'owns', '株式交付(2026年10月予定)', 2026)), {'tohbayashi': 'Tomotaka Tohbayashi'}, {}, {}, {}, {}, {}, 'rbank')

# ---------------- 楽天証券 ----------------
N = [
 O_('rsec', '楽天証券', 2000, '楽天グループのネット証券。', '', 'c'),
 P_('kusunoki', '楠雄治', 2020, '代表取締役社長(2026年9月1日現在の会社概要でも記載)。', '代表取締役社長'),
 O_('rbank', '楽天銀行', 2026, '楽天証券ホールディングスを、株式交付で子会社にする予定(2026年10月1日)と開示されています。', '親会社になる予定'),
]
CO7B['rsec'] = mk(N, std('rsec') + eg(('rbank', 'rsec', 'owns', '株式交付(2026年10月予定)', 2026)), {'kusunoki': 'Yuji Kusunoki'}, {}, {}, {}, {}, {}, 'rsec')

# 楽天グループの図に、金融の子会社を足す
import adds as _adds
_r = _adds.ADDS['rakuten']
_have = {n['id'] for n in _r['nodes']}
for _n in [O_('rcard', '楽天カード', 2005, '楽天グループのクレジットカード会社。代表取締役社長は中村晃一氏(2026年4月1日時点)。', '子会社(カード)'),
           O_('rbank', '楽天銀行', 2000, 'ネット銀行。代表取締役社長は東林知隆氏。2026年10月1日付で、楽天カードと楽天証券を株式交付で子会社にする予定と開示されています。', '子会社(銀行)'),
           O_('rsec', '楽天証券', 2000, 'ネット証券。代表取締役社長は楠雄治氏(2026年9月時点)。', '子会社(証券)')]:
    if _n['id'] not in _have:
        _r['nodes'].append(_n)
_r['edges'] = (_r.get('edges') or '') + "['rcard','rbank','rsec'].forEach(b=>E.push({a:'rakuten',b,k:'owns'}));" + chr(10)
