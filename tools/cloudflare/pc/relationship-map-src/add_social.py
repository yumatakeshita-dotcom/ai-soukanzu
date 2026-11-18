"""Chromeで見たXの投稿(人物の最新の発信)を、ウォッチの出来事(watch.sqlite)に入れる。本文は短い抜粋(110字まで)と、投稿へのリンクだけを保存する。
使い方: add_social.py が持つ POSTS に、(人物名, アカウント, 日付, 抜粋, 投稿のパス) を足して実行"""
import datetime as dt, hashlib, os, sqlite3, sys
W = os.path.join(os.path.expanduser('~'), '.claude', 'data', 'watch.sqlite')
POSTS = [
 ('ビル・アックマン', 'BillAckman', '2026-11-12', 'This is the definition of insanity, and it shows how far the @UN has fallen.', '/BillAckman/status/2120670973267718283'),
 ('ビル・アックマン', 'BillAckman', '2026-11-10', 'And much of the same and more goes for @MIT .', '/BillAckman/status/2119959582340685905'),
 ('ビル・アックマン', 'BillAckman', '2026-11-09', 'Yes. Thank you @elonmusk !', '/BillAckman/status/2119750584349642963'),
 ('ジェフ・ベゾス', 'JeffBezos', '2026-10-03', '100% correct diagnosis and prescription. And it’s not just in Spain.', '/JeffBezos/status/2106184667569500302'),
 ('エリック・シュミット', 'ericschmidt', '2026-10-28', 'This is pretty extraordinary, and on an open model to boot.', '/ericschmidt/status/2115593600327426329'),
 ('エリック・シュミット', 'ericschmidt', '2026-08-03', 'This Asari approach works, imagine the improvement in inference and the reduction of data center ser…', '/ericschmidt/status/2084310193731514782'),
 ('パーマー・ラッキー', 'PalmerLuckey', '2026-11-12', 'China wants Jensen out, so I want him in.', '/PalmerLuckey/status/2120770412741263858'),
 ('アダム・ディアンジェロ', 'adamdangelo', '2026-08-26', 'Any "tokens" metric that includes tokens from multiple models is meaningless. Tokens cannot be compa…', '/adamdangelo/status/2092653952852533395'),
 ('アダム・ディアンジェロ', 'adamdangelo', '2026-06-01', 'Toyota lean manufacturing has an idea called "genchi genbutsu", essentially meaning managers should …', '/adamdangelo/status/2061282163027509434'),
 ('ビル・マクダーモット', 'BillRMcDermott', '2026-02-09', 'Belief is the ultimate force multiplier. When leaders believe in their team with purpose and heart..', '/BillRMcDermott/status/2020997095759483183'),
]
db = sqlite3.connect(W)
n = 0
now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
for who, h, d, tx, path in POSTS:
    url = 'https://x.com' + path
    eid = hashlib.sha1((url + '|x').encode()).hexdigest()[:16]
    if db.execute('select 1 from events where id=?', (eid,)).fetchone():
        continue
    db.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?)', (eid, d + ' 12:00:00', 'X(@%s)' % h, '%s: %s' % (who, tx[:110]), url, '発信(X)', 20, '', '', who, now))
    n += 1
db.commit()
print('Xの投稿を足しました', n, '件')
