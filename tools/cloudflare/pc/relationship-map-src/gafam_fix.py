"""GAFAMの役員・取締役を、各社の公式ページ・SEC提出書類(2026年11月確認)に合わせて直す。人物の追加と、退任の反映。 使い方: python -u gafam_fix.py [--push]
出典: Apple https://www.apple.com/leadership/ / Meta https://investor.atmeta.com/corporate-governance/default.aspx / Microsoft https://news.microsoft.com/leadership/
      Amazon 2026年委任状説明書 https://www.sec.gov/Archives/edgar/data/1018724/000110465926041026/tm261382-1_def14a.htm / Alphabet 2026年委任状説明書(SEC)"""
import os, sqlite3, subprocess, sys
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')
db = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite'))
ADD = {
    'msft': [
        ('エイミー・フッド', 'Amy Hood', 'CFO', '', '', '執行副社長兼CFO。'),
        ('ジャドソン・アルトホフ', 'Judson Althoff', '商用事業CEO', '', '', '商用事業(Microsoft Commercial Business)のCEO。'),
        ('エイミー・コールマン', 'Amy Coleman', '最高人事責任者', '', '', '執行副社長兼最高人事責任者。'),
        ('ヌモト・タケシ', 'Takeshi Numoto', '最高マーケティング責任者', '', '', '執行副社長兼最高マーケティング責任者。'),
        ('サンドラ・ピーターソン', 'Sandra E. Peterson', '筆頭社外取締役', '', '', '取締役。'),
        ('カーマイン・ディ・シビオ', 'Carmine Di Sibio', '社外取締役', '', '', '取締役。EYの元グローバル会長兼CEO。'),
        ('ヒュー・ジョンストン', 'Hugh Johnston', '社外取締役', '', '', '取締役。ウォルト・ディズニーのCFO。'),
        ('テリー・リスト', 'Teri List', '社外取締役', '', '', '取締役。ギャップの元CFO。'),
        ('キャサリン・マクレガー', 'Catherine MacGregor', '社外取締役', '', '', '取締役。エンジーのCEO。'),
        ('マーク・メイソン', 'Mark Mason', '社外取締役', '', '', '取締役。シティの執行副会長。'),
        ('ペニー・プリツカー', 'Penny Pritzker', '社外取締役', '', '', '取締役。PSPパートナーズ創業者・会長。'),
        ('ジョン・デビッド・レイニー', 'John David Rainey', '社外取締役', '', '', '取締役。ウォルマートのCFO。'),
        ('チャールズ・シャーフ', 'Charles W. Scharf', '社外取締役', '', '', '取締役。ウェルズ・ファーゴの会長兼CEO。'),
        ('ジョン・スタントン', 'John W. Stanton', '社外取締役', '', '', '取締役。トリロジー・パートナーシップスの創業者・会長。'),
        ('エマ・ウォルズリー', 'Emma Walmsley', '社外取締役', '', '', '取締役。GSKの元CEO。'),
    ],
    'us_GOOGL': [
        ('ケント・ウォーカー', 'Kent Walker', '社長兼最高法務責任者', '', '', 'グローバル渉外担当の社長、最高法務責任者。'),
        ('トーマス・クリアン', 'Thomas Kurian', 'Google Cloud CEO', '', '', 'Google CloudのCEO(報道ベース)。'),
    ],
    'us_AMZN': [
        ('エディス・クーパー', 'Edith Cooper', '社外取締役', '', '', '取締役。報酬委員会の委員長。'),
        ('ダニエル・ハッテンロッカー', 'Daniel Huttenlocher', '社外取締役', '', '', '取締役。MITシュワルツマン・コンピューティング・カレッジの学部長。'),
        ('アンドリュー・ン', 'Andrew Ng', '社外取締役', '', '', '取締役。AI Fundの創業者・ジェネラルパートナー。'),
        ('ブラッド・D・スミス', 'Brad D. Smith', '社外取締役', '', '', '取締役。マーシャル大学の学長(マイクロソフトのブラッド・スミスとは別人)。'),
        ('ケビン・マンディア', 'Kevin Mandia', '社外取締役', '2026', '', '2026年9月に取締役に選任(8-K)。'),
    ],
    'us_META': [
        ('マーク・ザッカーバーグ', 'Mark Zuckerberg', '創業者 / 会長兼CEO', '2004', '', '創業者。会長兼CEO。'),
        ('ディナ・パウエル・マコーミック', 'Dina Powell McCormick', '社長兼副会長', '2026', '', '2026年1月から社長兼副会長。'),
        ('ハビエル・オリバン', 'Javier Olivan', 'COO', '2022', '', '最高執行責任者。'),
        ('スーザン・リー', 'Susan Li', 'CFO', '2022', '', '最高財務責任者。'),
        ('アンドリュー・ボスワース', 'Andrew Bosworth', 'CTO', '', '', '最高技術責任者。'),
        ('クリス・コックス', 'Chris Cox', '最高プロダクト責任者', '', '', 'CPO。'),
        ('C.J.マホニー', 'C.J. Mahoney', '最高法務責任者', '2026', '', '最高法務責任者。'),
        ('ロバート・キミット', 'Robert M. Kimmitt', '筆頭社外取締役', '', '', '取締役。'),
        ('ペギー・アルフォード', 'Peggy Alford', '社外取締役', '', '', '取締役。'),
        ('マーク・アンドリーセン', 'Marc L. Andreessen', '社外取締役', '', '', '取締役。a16zの共同創業者。'),
        ('ジョン・アーノルド', 'John Arnold', '社外取締役', '', '', '取締役。'),
        ('パトリック・コリソン', 'Patrick Collison', '社外取締役', '', '', '取締役。Stripeの共同創業者・CEO。'),
        ('ジョン・エルカン', 'John Elkann', '社外取締役', '', '', '取締役。'),
        ('アンドリュー・ヒューストン', 'Andrew W. Houston', '社外取締役', '', '', '取締役。Dropboxの共同創業者・CEO。'),
        ('ナンシー・キルファー', 'Nancy Killefer', '社外取締役', '', '', '取締役。'),
        ('チャーリー・ソングハースト', 'Charlie Songhurst', '社外取締役', '', '', '取締役。'),
        ('デイナ・ホワイト', 'Dana White', '社外取締役', '', '', '取締役。UFC社長。'),
        ('トニー・シュー', 'Tony Xu', '社外取締役', '', '', '取締役。DoorDashの共同創業者・CEO。'),
    ],
}
if not db.execute("SELECT 1 FROM mapco WHERE slug='us_META'").fetchone():
    db.execute("INSERT INTO mapco (slug,name,en,note,num,people,acq) VALUES ('us_META','Meta','Meta Platforms','Facebook・Instagram・WhatsAppなどを運営する会社。創業者のマーク・ザッカーバーグさんが会長兼CEO。経営陣と取締役は、Metaの公式ページ(2026年11月確認)に基づきます。','',0,0)")
for slug, rows in ADD.items():
    for r in rows:
        if not db.execute('SELECT 1 FROM mapco_people WHERE slug=? AND (en=? OR name=?)', (slug, r[1], r[0])).fetchone():
            db.execute('INSERT INTO mapco_people (slug,name,en,role,since,until,note) VALUES (?,?,?,?,?,?,?)', (slug,) + r)
# 修正: Amazonのキース・アレクサンダーは、2026年4月に再選に立候補しないと通知。ジェイミー・ゴレリックは筆頭社外取締役。
db.execute("UPDATE mapco_people SET role='元取締役', until='2026', note='取締役。2026年4月、再選に立候補しないと会社に通知(2026年委任状説明書)。' WHERE slug='us_AMZN' AND en='Keith Alexander'")
db.execute("UPDATE mapco_people SET role='筆頭社外取締役', note='取締役。筆頭社外取締役(Lead Independent Director)。' WHERE slug='us_AMZN' AND en='Jamie Gorelick'")
for slug in ADD:
    n = db.execute('SELECT count(*) FROM mapco_people WHERE slug=?', (slug,)).fetchone()[0]
    db.execute('UPDATE mapco SET people=? WHERE slug=?', (n, slug))
db.commit()
print('反映', {s: db.execute('SELECT count(*) FROM mapco_people WHERE slug=?', (s,)).fetchone()[0] for s in ADD}, flush=True)
if '--push' in sys.argv:
    q1 = lambda v: "'" + str('' if v is None else v).replace("'", "''") + "'"
    L = []
    for slug in ADD:
        m = db.execute('SELECT slug,name,en,note,num,people,acq FROM mapco WHERE slug=?', (slug,)).fetchone()
        L.append("DELETE FROM mapco WHERE slug=%s;" % q1(slug))
        L.append("INSERT INTO mapco VALUES (%s);" % ','.join(q1(x) if i < 5 else str(x or 0) for i, x in enumerate(m)))
        L.append("DELETE FROM mapco_people WHERE slug=%s;" % q1(slug))
        for r in db.execute('SELECT slug,name,en,role,since,until,note,q FROM mapco_people WHERE slug=?', (slug,)):
            L.append("INSERT INTO mapco_people VALUES (%s);" % ','.join(q1(x) for x in r))
    sql = os.path.join(SITE, 'gafam.sql')
    open(sql, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    p = subprocess.run('npx wrangler d1 execute houjin --remote --yes --file="' + sql.replace(chr(92), '/') + '"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (p.stdout or '') + (p.stderr or '')
    print('D1', 'OK' if p.returncode == 0 and 'ERROR' not in out else 'NG ' + out[-300:], flush=True)
