"""NotebookLM用の書き出し(その2): nblm_dump.js の JSON から、読みやすい Markdown のファイル群を作る。
使い方: python3 scripts/nblm_md.py /tmp/nblm_dump.json 出力フォルダ
・1ファイルは約80万バイト(日本語で約27万字)までに分ける(NotebookLMの1ソースの上限より十分小さくする)
・各ファイルの先頭に、題名・更新日・確かさの印の説明・目次を付ける
・出典URLは残す。メールアドレスや電話番号のような文字列は書き出さない
読むだけ。サイトのファイルは変えない。2026/11/19追加
"""
import json, os, re, sys, collections

SRC, OUTDIR = sys.argv[1], sys.argv[2]
LIMIT = 800_000
R = json.load(open(SRC, encoding='utf-8'))
ASOF = R['asof']
DS = R.get('DS') or {}
L = R['lists']
os.makedirs(OUTDIR, exist_ok=True)

CF = {'f': '開示', 'o': '公式', 's': '本人', 'r': '報道', 'e': '推定'}
CFJA = {'開示': 'f', '開示書類': 'f', '公式': 'o', '公式発表': 'o', '本人の発言': 's', '本人': 's', '報道': 'r', '報道ベース': 'r', '推定': 'e'}
KIND = {'deal': '取引(計算資源など)', 'invest': '出資', 'invest2': '出資', 'owns': '資本関係', 'govern': '信託・統治', 'uses': 'AIの利用',
        'member': '在籍・人事', 'from': '出身', 'moved': '移籍', 'conflict': '対立・係争', 'link': 'つながり'}
NK = {'c': '中心の会社', 'p': '人物', 'o': '会社・組織', 'i': '出資者・株主'}
EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
PHONE = re.compile(r'\b0\d{1,4}-\d{1,4}-\d{3,4}\b')

LEGEND = ('**確かさの印**(相関図と同じ決め方): 【開示】法定の書類(SEC・EDINET・決算資料など)で確かめられる / 【公式】会社・政府の公式発表 / '
          '【本人】本人の発言・投稿(番組・X・LinkedInなど) / 【報道】報道だけ(数字は報道ベース) / 【推定】推定・試算。'
          '印のない行は、出典が付いていないもの(Wikipedia・Wikidataなどの記載をもとにした在籍など)です。')


def clean(s):
    s = str(s if s is not None else '')
    s = s.replace('&nbsp;', ' ').replace('\n', ' ').replace('ダブルクリックで図を開きます。', '').strip()
    s = EMAIL.sub('(メールは省略)', s)
    s = PHONE.sub('(電話番号は省略)', s)
    return s


def link(t, u):
    t, u = clean(t) or 'リンク', clean(u)
    if not u.startswith('http'):
        return t
    return f'[{t.replace("[", "(").replace("]", ")")}]({u.replace(" ", "%20").replace(")", "%29")})'


def srcs(lst):
    out = []
    for x in lst or []:
        if isinstance(x, str):
            d = DS.get(x)
            if d:
                c = CF.get(CFJA.get(d[2], d[2])) if len(d) > 2 and d[2] else ''
                out.append(link(d[0], d[1]) + (f'〔{c}〕' if c else ''))
        elif isinstance(x, (list, tuple)) and len(x) >= 2:
            out.append(link(x[0], x[1]))
    return out


def cfm(c):
    c = CFJA.get(c, c)
    return f'【{CF[c]}】' if c in CF else ''


class Book:
    """1テーマのファイル。大きくなったら その1・その2 に分ける"""

    def __init__(self, fname, title, about):
        self.fname, self.title, self.about = fname, title, about
        self.secs = []  # (見出し, 本文)

    def add(self, head, body):
        self.secs.append((head, body))

    def write(self):
        parts, cur, size = [], [], 0
        for h, b in self.secs:
            n = len(h.encode()) + len(b.encode())
            if cur and size + n > LIMIT:
                parts.append(cur); cur, size = [], 0
            cur.append((h, b)); size += n
        if cur:
            parts.append(cur)
        names = []
        for i, p in enumerate(parts):
            suf = f'_その{i + 1}' if len(parts) > 1 else ''
            fn = f'{self.fname}{suf}.md'
            t = self.title + (f'(その{i + 1}/{len(parts)})' if len(parts) > 1 else '')
            toc = '\n'.join(f'- {h}' for h, _ in p) if len(p) <= 400 else \
                '\n'.join(f'- {h}' for h, _ in p[:400]) + f'\n- ほか {len(p) - 400}項目'
            head = (f'# {t}\n\n- 更新日: {ASOF}(相関図の最終確認日)\n- 出どころ: 「AI企業の相関図」のデータ(site/)から自動で書き出し\n'
                    f'- このファイルの中身: {self.about}\n\n{LEGEND}\n\n## 目次\n\n{toc}\n\n---\n\n')
            body = ''.join(f'## {h}\n\n{b}\n\n' for h, b in p)
            open(os.path.join(OUTDIR, fn), 'w', encoding='utf-8').write(head + body)
            names.append((fn, len((head + body).encode())))
        return names


# ---------------- 会社ごとの相関図 ----------------
def map_md(k, m, note_common=''):
    N = {n['id']: n for n in m['N']}
    c = N.get(m['center'], {})
    lines = []
    if m.get('min'):
        lines.append(f'- 設立: {m["min"]}年')
    if c.get('desc'):
        lines.append(f'- 概要: {clean(c["desc"])}')
    if c.get('web'):
        lines.append(f'- 公式サイト: {clean(c["web"])}')
    if c.get('wiki'):
        lines.append(f'- Wikipedia: {clean(c["wiki"])}')
    if m.get('note') and m['note'] != note_common:
        lines.append(f'- この図の情報源と注意: {clean(m["note"])}')
    lines.append(f'- 図のキー: `{k}`')
    groups = collections.OrderedDict((x, []) for x in ['p', 'i', 'o'])
    for n in m['N']:
        if n['id'] == m['center']:
            continue
        g = n['kind'] if n['kind'] in groups else 'o'
        t = f'- **{clean(n["name"])}**'
        if n.get('en') and n['en'] != n['name']:
            t += f'({clean(n["en"])})'
        if n.get('role'):
            t += f' — {clean(n["role"])}'
        yrs = ''
        if n.get('from') or n.get('to'):
            yrs = f'{n.get("from") or "?"}〜{n.get("to") or ""}'
        if yrs:
            t += f' 〔{yrs}〕'
        if n.get('founder'):
            t += ' 〔創業者〕'
        t += f' {cfm(n.get("cf"))}'
        if n.get('desc'):
            t += f' {clean(n["desc"])}'
        s = srcs(n.get('src'))
        if s:
            t += ' 出典: ' + ' / '.join(s)
        ex = []
        if n.get('wiki'):
            ex.append(f'Wikipedia {clean(n["wiki"])}')
        if n.get('x'):
            ex.append(f'X @{clean(n["x"])}')
        for lk in (m.get('links') or {}).get(n['id'], []) or []:
            if isinstance(lk, list) and len(lk) >= 2:
                ex.append(f'{clean(lk[0])} {clean(lk[1])}')
        if ex:
            t += ' (' + '、'.join(ex) + ')'
        car = (m.get('career') or {}).get(n['id'])
        if car:
            t += ' 経歴: ' + ' / '.join(f'{clean(a)} {clean(b)}' for a, b in car if True)
        groups[g].append(t.rstrip())
    for g, ls in groups.items():
        if ls:
            lines.append(f'\n**{NK[g]}**({len(ls)})\n')
            lines += ls
    el = []
    for e in m['E']:
        A, B = N.get(e['a']), N.get(e['b'])
        if not A or not B:
            continue
        if e['k'] == 'member' and not e.get('label') and not e.get('d') and m['center'] in (e['a'], e['b']):
            continue  # 中心の会社に在籍しているだけの線は、上の人物の一覧と同じ
        t = f'- {clean(A["name"])} → {clean(B["name"])}: {KIND.get(e["k"], e["k"])}'
        if e.get('label'):
            t += f'「{clean(e["label"])}」'
        if e.get('since'):
            t += f' 〔{e["since"]}年〜〕'
        t += f' {cfm(e.get("cf"))}'
        if e.get('d'):
            t += f' {clean(e["d"])}'
        s = srcs(e.get('src'))
        if s:
            t += ' 出典: ' + ' / '.join(s)
        el.append(t.rstrip())
    if el:
        lines.append(f'\n**つながり(線)**({len(el)})\n')
        lines += el
    if c.get('career') if isinstance(c, dict) else False:
        pass
    return '\n'.join(lines)


def common_note(keys, maps):
    cnt = collections.Counter(maps[k].get('note', '') for k in keys)
    n, c = cnt.most_common(1)[0] if cnt else ('', 0)
    return n if c >= 5 else ''


maps = R['maps']
GROUPS = [
    ('10_相関図_AI主要企業と半導体', 'AI主要企業・半導体などの相関図(手作り)', lambda k: '_' not in k and not k.startswith('aw'),
     'OpenAI・Anthropic・xAI・Meta・Nvidia・ソフトバンク・TSMC/JASMなど、手で調べて作った会社の図。人物・出資者・取引先・移籍とその出典'),
    ('11_相関図_米国の時価総額上位', '米国の時価総額上位企業の相関図', lambda k: k.startswith('us_'), '日経「米国株 時価総額上位」の会社の、経営陣・取締役・株主・買収'),
    ('12_相関図_日本の上場企業', '日本の上場企業の相関図', lambda k: k.startswith('jp_'), '日本の時価総額上位企業の、代表者・役員・株主など'),
    ('13_相関図_ユニコーン', 'ユニコーン(評価額10億ドル以上の未上場企業)の相関図', lambda k: k.startswith('un_'), 'ユニコーン一覧の会社の創業者・CEO・株主'),
    ('14_相関図_注目スタートアップ', '注目スタートアップの相関図', lambda k: k.startswith('st_'), 'Ramp・Andurilなど注目スタートアップの創業者・経営陣・出資者'),
    ('15_相関図_買収された会社・子会社', '大企業が買収した会社・子会社の相関図', lambda k: k.startswith('aq_'), '買収・子会社の創業者・CEO・親会社'),
    ('16_相関図_VCの投資先', 'VCの投資先・資金調達が報じられた会社の相関図', lambda k: k.startswith('vc_'), 'VCの投資先の会社と出資したVC・ニュース'),
]
results = []
for fn, title, f, about in GROUPS:
    keys = [k for k in maps if f(k)]
    if not keys:
        continue
    cn = common_note(keys, maps)
    bk = Book(fn, title, about + f'(全{len(keys)}社)')
    if cn:
        bk.add('この分類の図に共通する情報源と注意', clean(cn))
    for k in keys:
        bk.add(clean(maps[k]['name']), map_md(k, maps[k], cn))
    results += bk.write()

# AIスタートアップの小さな図(Wikidata)
aw = R['awmaps']; awinfo = R.get('aw') or {}
bk = Book('17_相関図_AIスタートアップ(Wikidata)', 'AIスタートアップの小さな相関図(Wikidata由来)',
          f'Wikidataで分野がAIの会社の、創業者・CEO・出資者・親会社(全{len(aw)}社)。金額や持ち分は載っていない')
cn = common_note(list(awinfo), awinfo) if awinfo else ''
if cn:
    bk.add('この分類の図に共通する情報源と注意', clean(cn))
rows = []
for k, m in aw.items():
    N = {n['id']: n for n in m['N']}
    c = N.get(m['center'], {})
    ppl = [f'{clean(n["name"])}({clean(n.get("role", ""))})' for n in m['N'] if n['id'] != m['center']]
    rows.append(f'- **{clean(c.get("name", k))}**(設立 {c.get("from") or "?"}): {clean(c.get("desc", ""))} 関係: {"、".join(ppl) if ppl else "記録なし"} 〔キー {k}〕')
for i in range(0, len(rows), 300):
    bk.add(f'AIスタートアップ {i + 1}〜{min(i + 300, len(rows))}社目', '\n'.join(rows[i:i + 300]))
results += bk.write()

# ---------------- 最近の動き ----------------
bk = Book('02_最近の動き', '最近の動き(毎日の更新記録・調査の新着)',
          '毎朝の自動更新で足した「最近の変化」と、調査タスク(引き抜き・お金の流れ・LP/VC・世界企業・深堀り)が見つけた候補')
ul = []
for u in R.get('UPDATES') or []:
    c = CFJA.get(u.get('cf', ''), '') or ''
    s = u.get('src') or []
    ul.append(f'- {u.get("d")} {cfm(c)} {clean(u.get("t"))}(関係する図: {"、".join(u.get("co") or [])}) 出典: {link(s[0], s[1]) if len(s) >= 2 else "なし"}')
bk.add('毎日の更新記録(最近の変化)', '\n'.join(ul) or 'なし')
KN = {'moves': '引き抜き(人の移籍)', 'money': 'お金の流れ', 'vc': 'LP・VC資金', 'world': '世界企業', 'deep': '深堀り'}
by = collections.defaultdict(list)
for f in R.get('FINDS') or []:
    t = f'- {f.get("d")} {cfm(f.get("c", ""))} **{clean(f.get("t"))}** {clean(f.get("x", ""))} 出典: {" / ".join(srcs(f.get("src")))}'
    by[f.get('k')].append(t)
for k, ls in by.items():
    bk.add(f'調査の新着: {KN.get(k, k)}({len(ls)}件)', '\n'.join(ls))
results += bk.write()

# ---------------- 幹部の年表 ----------------
bk = Book('03_幹部の年表', '幹部の年表(OpenAI・Anthropic)', '経営陣・幹部の入社・退社・役割の変更。上場の準備書類の前後で並べたもの')
TT = {'in': '入社', 'out': '退社', 'role': '役割の変更', 'co': '会社の出来事'}
auto = R.get('EXECTL_AUTO') or {}
for ck, tl in (R.get('EXECTL') or {}).items():
    ls = [f'- 時点: {tl.get("asof")}', f'- 説明: {clean(tl.get("note"))}']
    if tl.get('ipo'):
        ls.append(f'- 上場の準備: {tl["ipo"].get("d")} {clean(tl["ipo"].get("label"))}')
    ls.append('\n**いまの主な顔ぶれ**\n')
    ls += [f'- {clean(a)}: {clean(b)}({clean(c)})' for a, b, c in tl.get('now', [])]
    ls.append('\n**出来事(古い順)**\n')
    evs = [(e, '') for e in tl.get('ev', [])] + [(e, '〔毎朝の移籍の調査から自動で追加〕') for e in auto.get(ck, [])]
    evs.sort(key=lambda x: x[0].get('d', ''))
    for e, tag in evs:
        t = f'- {e.get("d")} {TT.get(e.get("t"), e.get("t"))}: **{clean(e.get("p"))}**'
        if e.get('en'):
            t += f'({clean(e["en"])})'
        if e.get('role'):
            t += f' — {clean(e["role"])}'
        if e.get('to'):
            t += f' → 移った先: {clean(e["to"])}'
        if e.get('from'):
            t += f' ← 前の会社: {clean(e["from"])}'
        t += f' {cfm(e.get("cf"))} {clean(e.get("note", ""))} {tag} 出典: {" / ".join(srcs(e.get("src")))}'
        ls.append(t)
    bk.add(clean(tl.get('name', ck)), '\n'.join(ls))
results += bk.write()

# ---------------- 計算資源の取引・大手どうしの線・確かさ ----------------
bk = Book('04_お金と取引の大きな流れ', '計算資源の取引・大手どうしのつながり・確かさの記録',
          'AI企業のクラウド・GPU・電力の取引(金色の線)、大手どうしの出資・合弁、一次情報のリンク、本人の投稿で確かめた人の動き、確かさの割合の記録')
for ck, dd in (R.get('DEALS') or {}).items():
    ls = [f'- まとめ: {clean(dd.get("note"))} 出典: {" / ".join(srcs(dd.get("src")))}']
    for row in dd.get('list', []):
        key, name, lab, yr, desc, sk = (row + [None] * 6)[:6]
        ls.append(f'- **{clean(name)}**「{clean(lab)}」〔{yr}年〜〕 {clean(desc)} 出典: {" / ".join(srcs(sk))}')
    bk.add(f'計算資源の取引: {clean((maps.get(ck) or {}).get("name", ck))}', '\n'.join(ls))
nm = lambda k: clean((maps.get(k) or {}).get('name', k))
bl = []
for row in R.get('BIGLINKS') or []:
    a, b, kk, lab, yr, desc, sk = (row + [None] * 7)[:7]
    bl.append(f'- {nm(a)} → {nm(b)}: {KIND.get(kk, kk)}「{clean(lab)}」〔{yr}年〜〕 {clean(desc)} 出典: {" / ".join(srcs(sk))}')
bk.add('大手どうしのつながり(抜けていた線を足したもの)', '\n'.join(bl))
pr = [f'- {nm(k)}: ' + ' / '.join(link(a, b) for a, b in v) for k, v in (R.get('PRIMARY') or {}).items()]
bk.add('一次情報のリンク(公式ニュース・SEC)', '\n'.join(pr))
vp = [f'- {clean(r[0])}(相手: {clean(r[1]) or "—"}): {clean(r[3])}{"(" + clean(r[4]) + "に確認)" if len(r) > 4 else ""} 出典: {" / ".join(srcs([r[2]]))}' for r in R.get('VERIFY_PPL') or []]
bk.add('本人の投稿・公式発表で確かめた人の動き', '\n'.join(vp))
ch = []
for h in R.get('CFHIST') or []:
    top = sorted(((v, nm(k)) for k, v in (h.get('c') or {}).items()), reverse=True)[:15]
    ch.append(f'- {h["d"]}: 全体 {h["pct"]}%({h["ok"]}/{h["tot"]}本が公式・開示などで確認済み)。高い会社: ' + '、'.join(f'{n} {v}%' for v, n in top))
bk.add('確かさの割合の記録(公式・開示で確かめた線の割合)', '\n'.join(ch))
results += bk.write()

# ---------------- 人物 ----------------
bk = Book('20_人物_関係と経歴', '人物の関係(家族・師弟・仕事)と経歴', '主要人物の家族・師・共同創業者などの関係と、Wikidataの生年・出身・学歴・職業')
PA = L.get('PAUTO') or {}
PE = L.get('PERSONAL') or {}
names = list(dict.fromkeys(list(PE) + list(PA)))
G = {'family': '家族', 'mentor': '師弟', 'work': '仕事', 'org': '組織', 'rival': '対立'}
rows = []
for n in names:
    t = f'### {clean(n)}\n'
    a = PA.get(n)
    if a:
        jp = clean(a[6]) if len(a) > 6 and a[6] else ''
        born = a[0][0][1:11] if a[0] and a[0][0] else ''
        t += f'- 日本語名: {jp} / 生年月日: {born} / 出身: {"・".join(map(clean, a[1] or []))} / 国籍: {"・".join(map(clean, a[2] or []))} / 学歴: {"・".join(map(clean, a[3] or []))} / 職業: {"・".join(map(clean, a[4] or []))}(Wikidata)\n'
    for r in PE.get(n, []):
        g, rel, en, jp, desc = (r + [''] * 5)[:5]
        t += f'- {G.get(g, g)}・{clean(rel)}: {clean(jp) or clean(en)}({clean(en)}) {clean(desc)}\n'
    rows.append(t)
for i in range(0, len(rows), 400):
    bk.add(f'人物 {i + 1}〜{min(i + 400, len(rows))}人目', '\n'.join(rows[i:i + 400]))
results += bk.write()

P = (L.get('people') or {}).get('rows', [])
bk = Book('21_人物名鑑(Wikidata)', '人物名鑑(Wikidataの創業者・CEO・会長・取締役)',
          f'Wikidataで会社の創業者・CEO・会長・取締役として記録のある人物{len(P)}人の、短い説明とWikipediaの冒頭')
RO = {'founder': '創業者', 'ceo': 'CEO', 'chair': '会長', 'board': '取締役', 'owner': '株主・所有者'}
rows = []
for r in P:
    q, en, jp, orgs, short, intro = (r + [''] * 6)[:6]
    o = '、'.join(f'{clean(a)}({RO.get(b, b)})' for a, b in (orgs or []))
    rows.append(f'- **{clean(jp) or clean(en)}**({clean(en)}, Wikidata {q}): {clean(short)}。関わった会社: {o}。{clean(intro)[:300]}')
for i in range(0, len(rows), 500):
    bk.add(f'人物名鑑 {i + 1}〜{min(i + 500, len(rows))}人目', '\n'.join(rows[i:i + 500]))
results += bk.write()

# ---------------- VC・投資家 ----------------
bk = Book('30_VC・投資家と投資先', 'VC・投資家と投資先、上場・買収した投資先', 'VC・CVC・投資家ごとの投資先(Wikipedia・各VCの公式サイト)、投資先の上場・買収(Wikidata)、VCの投資ニュース')
EX = L.get('EXITS') or {}
for k, v in (L.get('VCS') or {}).items():
    ps = v.get('p') or []
    t = f'- 英語名: {clean(v.get("en"))} / 地域: {clean(v.get("region"))} / 種類: {clean(v.get("kind"))} / 説明: {clean(v.get("desc"))}'
    if v.get('site'):
        t += f' / 投資先ページ: {clean(v["site"])}'
    if v.get('wiki'):
        t += f' / Wikipedia({v["wiki"][0]}): {clean(v["wiki"][1])}'
    t += f'\n- 投資先({len(ps)}社): ' + '、'.join(clean(p[1] or p[0]) + (f'({clean(p[0])})' if p[1] and p[1] != p[0] else '') for p in ps)
    bk.add(f'{clean(v.get("jp") or v.get("en"))}', t)
ex = [f'- {clean(k)}: {x[0]}{" " + str(x[1]) + "年" if x[1] else ""}{"(" + clean(x[2]) + ")" if len(x) > 2 and x[2] else ""}' for k, x in EX.items()]
bk.add('投資先の上場(IPO)・買収(M&A)(Wikidata)', '\n'.join(ex))
vn = [f'- {x.get("d")} {clean(x.get("c"))} ← {"、".join(map(clean, x.get("v") or []))}: {link(x.get("t"), x.get("u"))}({clean(x.get("s"))})〔報道〕' for x in L.get('VCNEWS') or []]
bk.add('VCの投資ニュース(見出し)', '\n'.join(vn))
results += bk.write()

# ---------------- ユニコーン・買収 ----------------
bk = Book('31_ユニコーンと買収の一覧', 'ユニコーン一覧と大企業の買収一覧', '英語版Wikipediaのユニコーン一覧(評価額は報道ベースの推定)と、各社の買収・子会社の一覧(Wikipedia・Wikidata)')
ul = []
for u in L.get('UNI') or []:
    ul.append(f'- {u.get("r")}位 **{clean(u.get("n"))}**: 評価額 約{u.get("v")}億ドル({u.get("d")}時点・報道ベース) / 分野: {clean(u.get("i"))} / 国: {"・".join(u.get("c") or [])} / 創業者など: {"、".join(clean(f.get("n")) for f in u.get("f") or [])}')
bk.add(f'ユニコーン一覧({len(ul)}社)', '\n'.join(ul))
for k, v in (L.get('ACQ') or {}).items():
    ls = [f'- {clean(a[0])} {a[1] or ""}年 {clean(a[2])} {clean(a[3])}'.rstrip() for a in v]
    bk.add(f'買収・子会社: {nm(k)}({len(ls)}件)', '\n'.join(ls) + '\n\n(出典: 英語版Wikipedia「List of mergers and acquisitions by …」とWikidata。金額は報道ベース)')
results += bk.write()

# ---------------- 日本のスタートアップ・世界 ----------------
bk = Book('32_日本のスタートアップと世界の日本人起業', '日本のスタートアップと、海外で活躍する日本人の会社', '日本のスタートアップ(東証・VC・ニュース・ユニコーン)と、世界の日本人創業・日本企業の会社')
jl = []
for s in L.get('JPSU') or []:
    bits = [f'{a}: {clean(s.get(b))}' for a, b in [('市場', 'mkt'), ('業種', 'ind'), ('本社', 'hq'), ('代表', 'rep'), ('資本金', 'cap'), ('従業員', 'emp'), ('サイト', 'url')] if s.get(b)]
    if s.get('est'):
        bits.append(f'設立: {s["est"]}')
    if s.get('vcs'):
        bits.append('出資したVC: ' + '、'.join(map(clean, s['vcs'])))
    jl.append(f'- **{clean(s.get("n"))}** ' + ' / '.join(bits) + f'(情報元: {"、".join(s.get("src") or [])})')
bk.add(f'日本のスタートアップ({len(jl)}社)', '\n'.join(jl))
W = L.get('WORLD') or {}
WS = W.get('s') or W.get('src') or {k: v for k, v in W.items() if k != 'r'}
wl = []
for x in W.get('r') or []:
    wl.append(f'- **{clean(x.get("n"))}**({clean(x.get("c"))}・{clean(x.get("g"))}): {clean(x.get("b"))}{" / 創業者: " + clean(x.get("f")) if x.get("f") else ""}{" / 設立: " + str(x.get("e")) if x.get("e") else ""}{" / 日本人の創業" if x.get("j") else ""} 出典記号: {",".join(x.get("s") or [])}')
bk.add(f'世界の日本人起業・日本企業の会社({len(wl)}社)', '\n'.join(wl))
if isinstance(WS, dict):
    sl = []
    for k, v in WS.items():
        if isinstance(v, list) and len(v) >= 2 and isinstance(v[1], str):
            sl.append(f'- {k}: {link(v[0], v[1])}')
        elif isinstance(v, dict):
            for k2, v2 in v.items():
                if isinstance(v2, list) and len(v2) >= 2:
                    sl.append(f'- {k2}: {link(v2[0], v2[1])}')
    bk.add('上の一覧の出典記号', '\n'.join(sl))
results += bk.write()

# ---------------- ニュース ----------------
bk = Book('40_ニュースの見出し', 'ニュースの見出し(資金調達・買収・会社ごと)', '相関図に入っているニュースの見出しとリンク。中身は報道(会社の発表を含む)')
nl = [f'- {x.get("d")} {link(x.get("t"), x.get("u"))}({clean(x.get("s"))}){" 金額: " + clean(x.get("a")) if x.get("a") else ""}{" ラウンド: " + clean(x.get("rd")) if x.get("rd") else ""}' for x in L.get('NEWS') or []]
bk.add(f'資金調達のニュース({len(nl)}件)', '\n'.join(nl))
rl = [f'- {x.get("d")} {link(x.get("t"), x.get("u"))}({clean(x.get("s"))})' for x in L.get('RELNEWS') or []]
bk.add(f'買収・提携などのニュース({len(rl)}件)', '\n'.join(rl))
for title, dct in [('Yahoo!ニュース', L.get('YNEWS') or {}), ('Googleニュース経由', L.get('gnews') or {})]:
    rows = []
    for co, items in dct.items():
        rows.append(f'### {clean(co)}\n' + '\n'.join(f'- {a} {link(b, c)}({clean(d)})' for a, b, c, d in [(i + [''] * 4)[:4] for i in items]))
    for i in range(0, len(rows), 300):
        bk.add(f'会社ごとのニュース({title}) {i + 1}〜{min(i + 300, len(rows))}社目', '\n'.join(rows[i:i + 300]))
sl = [f'- {x.get("d")} {x.get("f")} {clean(x.get("n"))}: {clean(x.get("u"))}〔開示〕' for x in L.get('SEC') or []]
bk.add(f'米SECの上場申請など({len(sl)}件)', '\n'.join(sl))
results += bk.write()

# ---------------- YC ----------------
Y = L.get('YCS') or []
bk = Book('41_YC出身企業の一覧', 'Y Combinator 出身企業の一覧', f'Y Combinatorの出身スタートアップ{len(Y)}社(公開データ yc-oss のAPI、YC公式ディレクトリの写し)。会社名・サイト・国・期・説明・分野')
rows = [f'- {clean(r[0])} | {clean(r[3])} | {clean(r[2])} | {clean(r[5])} | {clean(r[4])} | {clean(r[1])}' for r in Y]
for i in range(0, len(rows), 1500):
    bk.add(f'YC出身企業 {i + 1}〜{min(i + 1500, len(rows))}社目(会社名 | 期 | 国 | 分野 | 説明 | サイト)', '\n'.join(rows[i:i + 1500]))
results += bk.write()

# ---------------- 出典一覧 ----------------
bk = Book('90_出典の一覧', '出典の一覧(手で付けた出典)', '相関図の線・数字に付けた出典(DS)の全部。キー・媒体名・URL・確かさ')
dl = []
for k, v in DS.items():
    c = ''
    if len(v) > 2 and v[2]:
        c = CF.get(CFJA.get(v[2], v[2]), '')
    dl.append(f'- `{k}` {link(v[0], v[1])}{"〔" + c + "〕" if c else ""}')
bk.add(f'出典({len(dl)}件)', '\n'.join(dl))
results += bk.write()

# ---------------- 01 取り元の一覧(docs/notebooklm_sources.md から) ----------------
here = os.path.dirname(os.path.abspath(__file__))
xn = 0
try:
    xn = sum(1 for l in open(os.path.join(here, '..', 'inbox', 'x_accounts.txt'), encoding='utf-8') if l.startswith('@'))
except OSError:
    pass
t = open(os.path.join(here, '..', 'docs', 'notebooklm_sources.md'), encoding='utf-8').read().replace('{ASOF}', ASOF).replace('{XN}', str(xn))
fn = '01_情報の取り元(調査元サイト一覧).md'
open(os.path.join(OUTDIR, fn), 'w', encoding='utf-8').write(t)
results.insert(0, (fn, len(t.encode())))

# ---------------- 00 はじめに(入れ方と目次) ----------------
results.sort(key=lambda x: x[0])
ORDER = [('まず入れる(基本の5つ)', ['00_', '01_', '02_', '03_', '04_']),
         ('次に入れる(会社の相関図)', ['10_', '11_', '12_', '13_', '14_', '15_', '16_', '17_']),
         ('必要なら入れる(人物・VC・一覧・ニュース・出典)', ['20_', '21_', '30_', '31_', '32_', '40_', '41_', '90_'])]
desc = {}
for f, s in results:
    first = open(os.path.join(OUTDIR, f), encoding='utf-8').read(3000)
    m = re.search(r'このファイルの中身: (.+)', first)
    desc[f] = (m.group(1)[:120] if m else '', s)
g = ''
for title, pre in ORDER:
    g += f'\n### {title}\n\n| ファイル | 大きさ | 中身 |\n|---|---|---|\n'
    if pre[0] == '00_':
        g += '| 00_はじめに(読み込み手順と目次).md | — | このファイル |\n'
    for f, s in results:
        if any(f.startswith(p) for p in pre):
            g += f'| {f} | {s / 1e6:.2f}MB | {desc[f][0]} |\n'
total = len(results) + 1
guide = f"""# はじめに(NotebookLMへの読み込み手順と目次)

- 更新日: {ASOF}(相関図の最終確認日)
- このファイルの中身: 「AI企業の相関図」に入っている情報を、NotebookLM(Googleのノートブック)に読み込ませるために書き出したファイルの一覧と、入れる順番

## 目次

- このファイル群について
- 入れ方(手順)
- ファイルの一覧(入れる順)
- 質問のしかたの例
- 注意

## このファイル群について

- 相関図(site/index.html と site/data/)に入っている会社・人物・つながり(出資・取引・在籍・移籍)・お金の流れ・幹部の年表・確かさの印・出典URLを、全部 Markdown に書き出しました(全{total}ファイル)
- 各ファイルの先頭に、題名・更新日・確かさの印の説明・目次があります
- 1ファイルは0.8MB(日本語で約27万字)までに分けてあります。NotebookLMの1ソースの上限(約50万語・200MB)より小さいので、そのまま入ります
- 写真、鍵、メールアドレスなどの個人の連絡先は入れていません

{LEGEND}

## 入れ方(手順)

1. https://notebooklm.google.com を開き、「新規作成」でノートブックを作る(名前の例: AI企業の相関図 {ASOF})
2. 「ソースを追加」→「ファイルをアップロード」で、下の「まず入れる(基本の5つ)」を選んで入れる
3. 続けて「次に入れる(会社の相関図)」を入れる。ここまでで、AI企業・大手・日本企業・スタートアップの図が全部入ります
4. 人物やVC、ニュースの見出しについても聞きたいときは「必要なら入れる」も入れる
5. 無料版は1つのノートブックに50ソースまで(有料版は300)なので、全部入れても収まります
6. 新しい版を入れるときは、古い同じ名前のソースを消してから入れ直すと、答えが混ざりません

## ファイルの一覧(入れる順)
{g}
## 質問のしかたの例

- 「OpenAIの計算資源の取引を、確かさ(公式・開示・報道)ごとに分けて、出典のURL付きで表にして」
- 「Anthropicに移った元OpenAIの人を、移った年の順に並べて」
- 「ソフトバンクグループとつながっている会社を、出資・取引・人の動きに分けてまとめて」
- 「報道だけで、公式に確かめられていない大きな数字を挙げて」
- 「楽天とOpenAIの共通のつながりは?」

## 注意

- 【報道】の数字は報道ベースです。契約の上限の数字もあります。大事な判断の前は、出典のURLで確かめてください
- 印のない在籍・役職は、Wikipedia・Wikidataの記載が元で、最新の人事が入っていないことがあります
- 相関図は毎朝更新されます。この書き出しは {ASOF} 時点のものです
"""
open(os.path.join(OUTDIR, '00_はじめに(読み込み手順と目次).md'), 'w', encoding='utf-8').write(guide)
results.insert(0, ('00_はじめに(読み込み手順と目次).md', len(guide.encode())))
json.dump(results, open(os.path.join(OUTDIR, '_files.json'), 'w', encoding='utf-8'), ensure_ascii=False)
tot = sum(s for _, s in results)
for f, s in results:
    print(f'{s / 1e6:6.2f}MB  {f}')
print(f'合計 {len(results)}ファイル {tot / 1e6:.1f}MB')
