"""移籍の候補(JSON)から、D1 houjin に足す CSV を作る道具。D1 には書かない(読むだけ)。

使い方:
  python3 tools/cloudflare/moves_csv.py <入力.json> <出力フォルダ>
  → 出力フォルダに person.csv / person_role.csv / person_feed.csv / person_src.csv を作る。
    そのあと表ごとに d1_add.py add houjin <表> <CSV> --dry-run → 本番 の順で入れる。

入力は [{...}, ...]。1人1件:
  q        Wikidata の数字ID(Q なし)。Wikidata に本人の項目がない人は空にする → 仮の番号を付ける
  en, ja   名前(英語・日本語)
  intro, w, t   Wikipedia の冒頭・言語・題名(Wikipedia に記事があるときだけ)
  d        ひとことの説明(日本語。名前の下に出る)
  company, role   移った先の会社と役職(日本語)。行き先がないときは空
  date     移籍の日付 YYYY-MM-DD
  src      [[媒体名, URL], ...]  1件目をニュース(person_feed)の出典にする
  title    ニュースの日本語の短い説明

仮の番号の決まり(2026-11-18、企業検索のサイトの作りに合わせた):
  - 900000001 から始まる 9 桁の番号。サイトは 900000000 以上を「Wikidataに項目がない人」として扱い、
    Wikidata へのリンクを出さずに、person_src の出典を並べる
  - 今ある一番大きい仮の番号の次から順に付ける。同じ英語名か日本語名の人がすでにいれば、その番号を使い回す
  - intro は書かない(サイトが「Wikipediaの冒頭」と表示してしまうため)。代わりに d に説明、person_src に出典を入れる
  - あとで Wikidata に項目ができても、番号は書き換えない(足すだけ)
"""
import csv, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 900000000


def sel(sql):
    out = subprocess.run([sys.executable, os.path.join(HERE, 'd1_add.py'), 'select', 'houjin', sql],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out[out.index('['):])


def lit(s):
    return "'" + str(s).replace("'", "''") + "'"


def main(inp, outdir):
    items = json.load(open(inp, encoding='utf-8'))
    mx = sel(f"SELECT MAX(CAST(q AS INTEGER)) m FROM person WHERE CAST(q AS INTEGER) >= {BASE}")[0]['m'] or BASE
    nxt = int(mx) + 1
    P, R, F, S = [], [], [], []
    for it in items:
        q = str(it.get('q') or '').strip().lstrip('Q')
        prov = not q
        if prov:
            names = [n for n in (it.get('en'), it.get('ja')) if n]
            hit = sel("SELECT q FROM person WHERE CAST(q AS INTEGER) >= %d AND (en IN (%s) OR ja IN (%s))"
                      % (BASE, ','.join(map(lit, names)), ','.join(map(lit, names))))
            if hit:
                q = hit[0]['q']
            else:
                q = str(nxt); nxt += 1
        it['q'] = q
        P.append(dict(q=q, en=it.get('en', ''), ja=it.get('ja', ''), d=it.get('d', ''),
                      intro='' if prov else it.get('intro', ''), w='' if prov else it.get('w', ''),
                      t='' if prov else it.get('t', '')))
        if it.get('company'):
            R.append(dict(q=q, company=it['company'], role=it.get('role', '')))
        src = it.get('src') or []
        if src:
            F.append(dict(q=q, ts=it['date'], src=src[0][0], title=it.get('title', ''), url=src[0][1], kind='move'))
        if prov:
            for lab, url in src:
                S.append(dict(q=q, label=lab, url=url))
        print(q, '(仮)' if prov else '', it.get('ja') or it.get('en'))
    os.makedirs(outdir, exist_ok=True)
    for name, rows, cols in [('person', P, 'q en ja d intro w t'), ('person_role', R, 'q company role'),
                             ('person_feed', F, 'q ts src title url kind'), ('person_src', S, 'q label url')]:
        with open(os.path.join(outdir, name + '.csv'), 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=cols.split()); w.writeheader(); w.writerows(rows)
        print(name, len(rows), '行')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
