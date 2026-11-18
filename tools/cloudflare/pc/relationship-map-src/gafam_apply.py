"""gafam_data.py の内容を、(1)公開ページのJS(部屋のN配列) (2)独立サイトのDB(mapco/mapco_people)に反映する。
使い方: python gafam_apply.py html <公開ページのコピー>   … 部屋のデータを書き換える(コピーに対して)
        python gafam_apply.py db                           … houjin.sqlite と D1送信用SQL(site/gafam_update.sql)を作る(送信は別に wrangler)"""
import json, os, re, sqlite3, sys
import gafam_data as G
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')


def node(i, name, role, frm, desc, founder=False):
    d = {'id': i, 'name': name, 'kind': 'p', 'from': frm, 'desc': desc, 'role': role}
    return json.dumps(d, ensure_ascii=False)


def patch_room(s, key, nodes, fixes=None, en=None):
    nl = '\r\n' if '\r\n' in s else '\n'
    i = s.index(key)
    j = s.index('}];', i)
    seg = s[i:j + 3]
    have = set(re.findall(r'"id": "([^"]+)"', seg))
    add = ', '.join(node(n[0], n[1], n[3], n[4], n[5]) for n in nodes if n[0] not in have)
    new = seg[:-2] + (', ' + add if add else '') + '];'
    for k, (desc, role, to) in (fixes or {}).items():
        m = re.search(r'\{"id": "%s",[^{}]*\}' % k, new)
        assert m, k
        o = json.loads(m.group(0))
        o['desc'] = desc
        if role:
            o['role'] = role
        if to:
            o['to'] = to
        new = new[:m.start()] + json.dumps(o, ensure_ascii=False) + new[m.end():]
    s = s[:i] + new + s[j + 3:]
    # EN(英語名)も足す: 部屋の const EN={...} に追加
    k = s.index('const EN=', i)
    e = s.index('};', k)
    ens = ', '.join('"%s": "%s"' % (n[0], n[2]) for n in nodes if n[0] not in have)
    if ens:
        s = s[:e] + (', ' if s[k + 9:e].strip() not in ('{', '{}') else '') + ens + s[e:]
    return s


def do_html(path):
    s = open(path, encoding='utf-8', newline='').read()
    s = patch_room(s, 'msft:()=>', G.MSFT)
    s = patch_room(s, 'us_GOOGL:()=>', G.GOOG)
    s = patch_room(s, 'us_AMZN:()=>', G.AMZN, fixes=G.AMZN_FIX)
    s = patch_room(s, 'meta:()=>', G.META)
    open(path, 'w', encoding='utf-8', newline='').write(s)
    print('html ok', len(s.encode()))


def q(v):
    return "'" + str('' if v is None else v).replace("'", "''") + "'"


def do_db():
    db = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite'))
    lines = []
    def put(slug, rows):
        for n in rows:
            since = str(n[4])
            db.execute('DELETE FROM mapco_people WHERE slug=? AND en=?', (slug, n[2]))
            db.execute('INSERT INTO mapco_people (slug,name,en,role,since,until,note) VALUES (?,?,?,?,?,?,?)', (slug, n[1], n[2], n[3], since, '', n[5]))
            lines.append("DELETE FROM mapco_people WHERE slug=%s AND en=%s;" % (q(slug), q(n[2])))
            lines.append("INSERT INTO mapco_people (slug,name,en,role,since,until,note) VALUES (%s,%s,%s,%s,%s,'',%s);" % (q(slug), q(n[1]), q(n[2]), q(n[3]), q(since), q(n[5])))
    put('msft', G.MSFT); put('us_GOOGL', G.GOOG); put('us_AMZN', G.AMZN)
    # Amazon の取締役の更新
    for en, (desc, role, to) in {'Keith Alexander': G.AMZN_FIX['alexander'], 'Jamie Gorelick': G.AMZN_FIX['gorelick']}.items():
        r = G.AMZN_FIX['alexander'][1] if en == 'Keith Alexander' else '筆頭社外取締役'
        until = '2026' if en == 'Keith Alexander' else ''
        db.execute('UPDATE mapco_people SET role=?,until=?,note=? WHERE slug=? AND en=?', (r, until, desc, 'us_AMZN', en))
        lines.append("UPDATE mapco_people SET role=%s,until=%s,note=%s WHERE slug='us_AMZN' AND en=%s;" % (q(r), q(until), q(desc), q(en)))
    # Meta の会社を新しく(なければ)
    mnote = 'Facebook、Instagram、WhatsAppなどを運営する企業。創業者のマーク・ザッカーバーグが会長兼CEOを務めます。経営陣と取締役は、Metaの公式ページ(2026年11月確認)に基づきます。'
    db.execute("DELETE FROM mapco WHERE slug='meta'")
    db.execute("INSERT INTO mapco (slug,name,en,note,num,people,acq) VALUES ('meta','Meta','',?,'',?,0)", (mnote, 4 + len(G.META)))
    lines.append("DELETE FROM mapco WHERE slug='meta';")
    lines.append("INSERT INTO mapco (slug,name,en,note,num,people,acq) VALUES ('meta','Meta','',%s,'',%d,0);" % (q(mnote), 4 + len(G.META)))
    core = [('zuckerberg', 'マーク・ザッカーバーグ', 'Mark Zuckerberg', '創業者 / 会長兼CEO', 2004, '創業者で、会長兼CEO(公式の経営陣一覧)。'),
            ('olivan', 'ハビエル・オリバン', 'Javier Olivan', 'COO', 2022, '最高執行責任者(COO、公式の経営陣一覧)。'),
            ('bosworth', 'アンドリュー・ボスワース', 'Andrew Bosworth', 'CTO', 2022, '最高技術責任者(CTO、公式の経営陣一覧)。'),
            ('cox', 'クリス・コックス', 'Chris Cox', '最高プロダクト責任者', 2005, '最高プロダクト責任者(CPO、公式の経営陣一覧)。')]
    put('meta', core + G.META)
    db.commit()
    open(os.path.join(SITE, 'gafam_update.sql'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('db ok', len(lines), '文')


if __name__ == '__main__':
    if sys.argv[1] == 'html':
        do_html(sys.argv[2])
    else:
        do_db()
