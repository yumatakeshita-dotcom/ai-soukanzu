#!/usr/bin/env python3
"""投稿(note・X)のための段階式の深掘りリサーチの道具(2026/11/24追加)。
手順の説明は docs/deep_research.md。調べた中身は posts/research/<名前>/ に足していく(消さない)。

  A テーマ   python3 scripts/deep_post.py init  <名前> "テーマ"        置き場を作る(plan.md・people.json)
  B 一次資料 python3 scripts/deep_post.py fetch <名前> URL [URL...]     ページを読んで sources/ に本文を保存。
                                                                     読めなかったサイトも記録する(許可リストの候補になる)
            python3 scripts/deep_post.py addsrc <名前> URL --via webfetch|search|x_check|browser --note "…"
                                                                     ほかの方法で読んだ資料を記録(WebFetch・検索結果・Xの確認など)
            python3 scripts/deep_post.py grep  <名前> 言葉            保存した本文から探す(事実カードを書く前の確かめ)
            事実カードは posts/research/<名前>/facts.jsonl に1行1枚で足す(形は docs/deep_research.md)
            python3 scripts/deep_post.py lint  <名前>                 事実カードの形・出典・日付を確かめる
  C 年表     python3 scripts/deep_post.py timeline <名前>              timeline.md(年表・人ごとの表・共通の相手)を作る
  D 穴       python3 scripts/deep_post.py gaps <名前>                  questions.md(分からない点の一覧)を作る
  E 執筆     (Claude が facts.jsonl だけを材料に note.md を書く)
  F 照合     python3 scripts/deep_post.py verify <名前> [note.md]      本文の数字・日付・固有名詞を事実カードと照らす
  まとめ     python3 scripts/deep_post.py stats <名前> [--old 前の下書き.md]   情報量・出典数を比べる
            python3 scripts/deep_post.py domains [<名前>]             読めなかったサイトの一覧(許可リストの候補)

サイト・inbox は変えない。読むだけ・足すだけ。
"""
import sys, os, re, json, html, datetime, subprocess, collections, unicodedata, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, 'posts', 'research')
UA = 'Mozilla/5.0 (compatible; relmap-research/1.0)'
CATS = ['学歴', '前職', '研究', '入社', '役割', '発言', '退社', '行き先', '資金', '会社', 'その他']
CFS = ['公式', '開示', '本人', '報道', '推定']
READS = ['本文', '検索結果', '本人投稿']
NEED = ['前職', '入社', '役割', '退社', '行き先']  # 人ごとに埋まっていてほしい欄
CATMAP = {'研究': '前職', '学歴': '前職'}  # 研究・学歴のカードは「前職」の欄に数える


def cat_of(f):
    return CATMAP.get(f.get('cat'), f.get('cat'))


def orgs_of(f, w):
    # org_by があれば人ごとの所属を使う(共著の相手の会社を、その人の所属と混ぜないため)
    return f.get('org_by', {}).get(w, f.get('org', []))


def today():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d')


def d(slug):
    p = os.path.join(BASE, slug)
    if not os.path.isdir(p):
        sys.exit(f'置き場がありません: {p}(先に init)')
    return p


def jl_read(path):
    out = []
    if not os.path.exists(path):
        return out
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        line = line.strip()
        if not line or line.startswith('//'):
            continue
        try:
            out.append(json.loads(line))
        except Exception as e:  # noqa: BLE001
            print(f'  ! {os.path.basename(path)} {i}行目が読めません: {e}')
    return out


def jl_add(path, obj):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False) + '\n')


# ---------- A ----------
def cmd_init(slug, theme):
    p = os.path.join(BASE, slug)
    os.makedirs(os.path.join(p, 'sources'), exist_ok=True)
    plan = os.path.join(p, 'plan.md')
    if not os.path.exists(plan):
        open(plan, 'w', encoding='utf-8').write(
            f'# {theme}\n\n作った日: {today()}\n\n## 問い(この記事で答えること)\n- \n\n'
            '## 登場する人・会社\n- \n\n## 調べる一次資料(人ごと)\n'
            '- 本人のX・ブログ・GitHub / 講演・ポッドキャストの字幕 / 論文 / 開示(SEC・TDnet・HKEX) / 公式ブログ・採用ページ / 報道\n')
    ppl = os.path.join(p, 'people.json')
    if not os.path.exists(ppl):
        open(ppl, 'w', encoding='utf-8').write('{\n  "English Name": ["日本語の書き方", "姓だけ"]\n}\n')
    for f in ('facts.jsonl', 'sources.jsonl'):
        open(os.path.join(p, f), 'a').close()
    print('作りました:', os.path.relpath(p, ROOT))


# ---------- B ----------
def to_text(raw):
    t = re.sub(r'(?is)<(script|style|noscript|svg|nav|footer)[^>]*>.*?</\1>', ' ', raw)
    t = re.sub(r'(?i)<br\s*/?>|</p>|</h\d>|</li>|</tr>', '\n', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    t = re.sub(r'[ \t ]+', ' ', t)
    t = re.sub(r'\n\s*\n+', '\n', t)
    return t.strip()


def next_no(p):
    ns = [int(m.group(1)) for f in os.listdir(os.path.join(p, 'sources')) for m in [re.match(r'(\d+)', f)] if m]
    return max(ns or [0]) + 1


def cmd_fetch(slug, urls):
    p = d(slug)
    seen = {s['url']: s for s in jl_read(os.path.join(p, 'sources.jsonl'))}
    for url in urls:
        if url in seen and seen[url].get('status') == 'ok':
            print('  済み', url, '→', seen[url].get('file'))
            continue
        x = re.match(r'https?://(x|twitter)\.com/[^/]+/status/\d+', url)
        if x:
            r = subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'x_check.py'), url],
                               capture_output=True, text=True, timeout=60)
            text, code = r.stdout, (200 if '"error"' not in r.stdout else 0)
        else:
            r = subprocess.run(['curl', '-sL', '-m', '25', '-A', UA, '-w', '\n__CODE__%{http_code}', url],
                               capture_output=True, text=True, errors='replace')
            body, _, c = r.stdout.rpartition('\n__CODE__')
            code = int(c) if c.isdigit() else 0
            if code == 200 and url.lower().endswith('.pdf'):
                tmp = os.path.join(p, 'sources', '_tmp.pdf')
                subprocess.run(['curl', '-sL', '-m', '40', '-A', UA, '-o', tmp, url])
                text = subprocess.run(['pdftotext', '-layout', tmp, '-'], capture_output=True, text=True).stdout
                os.remove(tmp)
            else:
                text = to_text(body)
        ok = code == 200 and len(text) > 400
        rec = {'url': url, 'host': urllib.parse.urlparse(url).netloc.lower(), 'via': 'curl', 'code': code,
               'status': 'ok' if ok else 'blocked', 'chars': len(text), 'date': today()}
        if ok:
            fn = f'{next_no(p):03d}_{re.sub(r"[^a-z0-9]+", "-", rec["host"])[:30]}.txt'
            open(os.path.join(p, 'sources', fn), 'w', encoding='utf-8').write(url + '\n\n' + text)
            rec['file'] = fn
            print(f'  読めた {code} {len(text):>6}字 {url} → sources/{fn}')
        else:
            print(f'  読めない {code} {url}  → WebFetch や検索で読んだら addsrc で記録')
        jl_add(os.path.join(p, 'sources.jsonl'), rec)


def cmd_addsrc(slug, url, via, note, textfile=None):
    p = d(slug)
    rec = {'url': url, 'host': urllib.parse.urlparse(url).netloc.lower(), 'via': via, 'status': 'ok',
           'note': note, 'date': today()}
    if textfile:
        fn = f'{next_no(p):03d}_{via}.txt'
        open(os.path.join(p, 'sources', fn), 'w', encoding='utf-8').write(url + '\n\n' + open(textfile, encoding='utf-8').read())
        rec['file'] = fn
    jl_add(os.path.join(p, 'sources.jsonl'), rec)
    print('記録しました:', url, via)


def cmd_grep(slug, word):
    p = d(slug)
    for f in sorted(os.listdir(os.path.join(p, 'sources'))):
        t = open(os.path.join(p, 'sources', f), encoding='utf-8', errors='replace').read()
        for m in re.finditer(re.escape(word), t, re.I):
            s = t[max(0, m.start() - 160): m.end() + 160].replace('\n', ' ')
            print(f'[{f}] …{s}…')


def facts(p):
    return jl_read(os.path.join(p, 'facts.jsonl'))


def people(p):
    f = os.path.join(p, 'people.json')
    try:
        return {k: v for k, v in json.load(open(f, encoding='utf-8')).items() if k != 'English Name'}
    except Exception:  # noqa: BLE001
        return {}


def cmd_lint(slug):
    p = d(slug)
    fs = facts(p)
    bad = 0
    ids = collections.Counter(f.get('id') for f in fs)
    for f in fs:
        why = []
        if ids[f.get('id')] > 1: why.append('idが重なり')
        if not re.match(r'^\d{4}(-\d{2}(-\d{2})?)?$', str(f.get('date', ''))): why.append('日付の形(YYYY / YYYY-MM / YYYY-MM-DD)')
        if f.get('cat') not in CATS: why.append('cat')
        if f.get('cf') not in CFS: why.append('cf')
        if f.get('read') not in READS: why.append('read')
        if not str(f.get('src', '')).startswith('http'): why.append('出典URLなし')
        if not f.get('fact'): why.append('factが空')
        if str(f.get('date', '')) > today(): why.append('日付が未来')
        if why:
            bad += 1
            print('  !', f.get('id'), '・'.join(why))
    print(f'事実カード {len(fs)}枚、問題 {bad}枚')
    return bad


# ---------- C ----------
def cmd_timeline(slug):
    p = d(slug)
    fs = sorted(facts(p), key=lambda f: str(f.get('date')))
    ppl = people(p)
    ja = {k: (v[0] if v else k) for k, v in ppl.items()}
    L = [f'# 年表と共通の相手({slug})', '', f'作った日: {today()}(`deep_post.py timeline` が facts.jsonl から作る。手で直さない)', '',
         '## 1. 年表(日付順)', '', '| 日付 | だれ | 何をした | 確かさ | 出典 |', '|---|---|---|---|---|']
    for f in fs:
        who = '・'.join(ja.get(w, w) for w in f.get('who', []))
        L.append(f"| {f['date']} | {who} | {f['fact']} | {f['cf']}({f['read']}) | [{f.get('src_name') or 'リンク'}]({f['src']}) `{f['id']}` |")
    L += ['', '## 2. 人ごと(欄の埋まり方)', '', '| 人 | ' + ' | '.join(NEED) + ' | カード数 |', '|---|' + '---|' * (len(NEED) + 1)]
    by = collections.defaultdict(list)
    for f in fs:
        for w in f.get('who', []):
            by[w].append(f)
    for w in (list(ppl) or sorted(by)):
        row = []
        for c in NEED:
            hit = [f for f in by[w] if cat_of(f) == c]
            row.append(('○' + ''.join('公開本報推'[CFS.index(h['cf'])] for h in hit[:3])) if hit else '—')
        L.append(f'| {ja.get(w, w)} | ' + ' | '.join(row) + f' | {len(by[w])} |')
    L += ['', '(○のあとの字 = 確かさ。公=公式 開=開示 本=本人 報=報道 推=推定)', '',
          '## 3. 共通の相手(2人以上の線に出てくる会社・組織)', '']
    org = collections.defaultdict(set)
    for f in fs:
        for w in f.get('who', []):
            for o in orgs_of(f, w):
                org[o].add(w)
    rows = sorted(((o, s) for o, s in org.items() if len(s) >= 2), key=lambda x: -len(x[1]))
    for o, s in rows:
        L.append(f'- **{o}**({len(s)}人): ' + '、'.join(ja.get(w, w) for w in sorted(s)))
    if not rows:
        L.append('- (まだ無い)')
    open(os.path.join(p, 'timeline.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(f'timeline.md を作りました(カード{len(fs)}枚・共通の相手{len(rows)}件)')


# ---------- D ----------
def cmd_gaps(slug):
    p = d(slug)
    fs = facts(p)
    ppl = people(p)
    ja = {k: (v[0] if v else k) for k, v in ppl.items()}
    by = collections.defaultdict(list)
    for f in fs:
        for w in f.get('who', []):
            by[w].append(f)
    Q = []
    for w in (list(ppl) or sorted(by)):
        for c in NEED:
            hit = [f for f in by[w] if cat_of(f) == c]
            if not hit:
                Q.append(f'- [ ] {ja.get(w, w)}: 「{c}」の事実カードが無い')
            elif all(h['cf'] == '報道' for h in hit) and len({h['src'] for h in hit}) < 2:
                Q.append(f'- [ ] {ja.get(w, w)}: 「{c}」が報道1本だけ({hit[0]["id"]})。本人・公式・2本目の報道で確かめる')
    for f in fs:
        if f.get('read') == '検索結果':
            Q.append(f'- [ ] {f["id"]}: 検索結果の要約だけで本文を読んでいない → 本文(WebFetch・ブラウザ)で確かめる')
        if f.get('conflict'):
            Q.append(f'- [ ] {f["id"]}: 食い違い「{f["conflict"]}」→ どちらが正しいか一次資料で')
    manual = ''
    qp = os.path.join(p, 'questions.md')
    if os.path.exists(qp):
        t = open(qp, encoding='utf-8').read()
        if '## 手で足した問い' in t:
            manual = t[t.index('## 手で足した問い'):]
    out = [f'# 分からない点の一覧({slug})', '', f'作った日: {today()}。上の「自動」は `deep_post.py gaps` が作り直す。'
           '下の「手で足した問い」は残る。', '', f'## 自動({len(Q)}件)', ''] + (Q or ['- (無し)']) + ['', manual or '## 手で足した問い\n- \n']
    open(qp, 'w', encoding='utf-8').write('\n'.join(out))
    print(f'questions.md を作りました(自動の問い {len(Q)}件)')


# ---------- F ----------
KANJI_NUM = None


def corpus(p):
    fs = facts(p)
    parts = []
    for f in fs:
        parts += [f.get('fact', ''), f.get('quote', ''), ' '.join(f.get('who', [])), ' '.join(f.get('org', [])),
                  f.get('src_name', ''), f.get('note', '')]
    for k, v in people(p).items():
        parts += [k] + v
    extra = os.path.join(p, 'glossary.txt')  # 一般の言葉(会社名の書き方など)。事実ではないもの
    if os.path.exists(extra):
        parts.append(open(extra, encoding='utf-8').read())
    return unicodedata.normalize('NFKC', '\n'.join(parts)), {str(f.get('date')) for f in fs}


def cmd_verify(slug, note=None):
    p = d(slug)
    note = note or os.path.join(p, 'note.md')
    t = open(note, encoding='utf-8').read()
    body = t.split('<!--SOURCES-->')[0]
    body = re.sub(r'https?://\S+', '', body)
    body = unicodedata.normalize('NFKC', body)
    C, dates = corpus(p)
    miss = collections.OrderedDict()

    def chk(tok, ok, kind):
        if not ok:
            miss.setdefault(kind, []).append(tok)

    for m in re.finditer(r'(\d{4})年(\d{1,2})月(?:(\d{1,2})日)?', body):
        y, mo, dd = m.group(1), int(m.group(2)), m.group(3)
        key = f'{y}-{mo:02d}' + (f'-{int(dd):02d}' if dd else '')
        chk(m.group(0), any(x.startswith(key) for x in dates) or m.group(0) in C, '日付')
    for m in re.finditer(r'(?<![年\d])(\d{1,2})月(\d{1,2})日', body):
        key = f'-{int(m.group(1)):02d}-{int(m.group(2)):02d}'
        chk(m.group(0), any(x.endswith(key) for x in dates) or m.group(0) in C, '日付')
    for m in re.finditer(r'\d[\d,.]*\s*(?:億|万|兆)?\s*(?:ドル|円|人|件|社|本|%|倍|字|年|か月|カ月|GW|MW|パラメータ)', body):
        tok = m.group(0).replace(' ', '')
        if re.fullmatch(r'\d{4}年', tok):
            continue
        num = re.match(r'[\d,.]+', tok).group(0)
        chk(tok, tok in C.replace(' ', '') or (len(num) >= 2 and num in C), '数字')
    for m in re.finditer(r'[A-Z][A-Za-z0-9&.\-]+(?:\s[A-Z][A-Za-z0-9&.\-]+)*', body):
        tok = m.group(0)
        if len(tok) < 3 or tok in ('X', 'AI', 'API', 'GPU', 'CEO', 'CTO', 'VC', 'note'):
            continue
        chk(tok, tok.lower() in C.lower(), '英字の名前')
    for m in re.finditer(r'[ァ-ヴー]{3,}(?:・[ァ-ヴー]{2,})*', body):
        tok = m.group(0)
        chk(tok, tok in C, 'カタカナの名前')
    seen = set()
    L = [f'# 照合の結果({os.path.basename(note)})', '', f'作った日: {today()}。本文の数字・日付・名前のうち、事実カード(facts.jsonl)・'
         '人の名前(people.json)・言葉の表(glossary.txt)に無いもの。**投稿前に、直すか★を付ける。**', '']
    n = 0
    for k, v in miss.items():
        u = [x for x in v if not (x in seen or seen.add(x))]
        if u:
            n += len(u)
            L.append(f'## {k}({len(u)})')
            L += [f'- {x}' for x in u]
            L.append('')
    if not n:
        L.append('すべて事実カードにありました。')
    open(os.path.join(p, 'verify.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    stars = body.count('★')
    print(f'照合: カードに無いもの {n}件(★の印 {stars}個)→ verify.md')
    return n


# ---------- まとめ ----------
def measure(path):
    t = open(path, encoding='utf-8').read()
    m = re.search(r'## note記事.*?\n(.*?)(?:\n---\n|\Z)', t, re.S)
    body = m.group(1) if m else t
    urls = set(re.findall(r'https?://[^\s)>\]]+', t))
    plain = re.sub(r'https?://\S+|[#|*\-`>]', '', body)
    return {'本文の字数': len(re.sub(r'\s', '', plain)), '出典URL(ちがうもの)': len(urls),
            '出典のサイト数': len({urllib.parse.urlparse(u).netloc for u in urls}), '★の数': body.count('★')}


def cmd_stats(slug, old=None):
    p = d(slug)
    fs = facts(p)
    srcs = [s for s in jl_read(os.path.join(p, 'sources.jsonl')) if s.get('status') == 'ok']
    new = measure(os.path.join(p, 'note.md')) if os.path.exists(os.path.join(p, 'note.md')) else {}
    new.update({'事実カード': len(fs), '読んだ資料': len({s['url'] for s in srcs}),
                '一次資料のカード(公式・開示・本人)': sum(f['cf'] in ('公式', '開示', '本人') for f in fs),
                '本文を読んだカード': sum(f['read'] != '検索結果' for f in fs),
                'カードのある人': len({w for f in fs for w in f.get('who', [])})})
    rows = [('項目', '前の下書き', '今回')]
    o = measure(old) if old else {}
    for k, v in new.items():
        rows.append((k, str(o.get(k, '—')), str(v)))
    out = '\n'.join(f'| {a} | {b} | {c} |' if i else f'| {a} | {b} | {c} |\n|---|---|---|' for i, (a, b, c) in enumerate(rows))
    open(os.path.join(p, 'stats.md'), 'w', encoding='utf-8').write(f'# 情報量のくらべ({today()})\n\n' + out + '\n')
    print(out)


def cmd_domains(slug=None):
    dirs = [d(slug)] if slug else [os.path.join(BASE, x) for x in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, x))]
    st = collections.defaultdict(lambda: [0, 0, set()])
    for p in dirs:
        for s in jl_read(os.path.join(p, 'sources.jsonl')):
            if s.get('via') != 'curl':
                continue
            h = s['host'].removeprefix('www.')
            st[h][0 if s['status'] == 'ok' else 1] += 1
            st[h][2].add(str(s.get('code')))
    print('# この環境から直接読めなかったサイト(許可リストの候補)')
    for h, (ok, ng, codes) in sorted(st.items(), key=lambda x: -x[1][1]):
        if ng and not ok:
            print(f'{h}\t読めない{ng}回(応答 {",".join(sorted(codes))})')


def main(a):
    if len(a) < 1 or a[0] in ('-h', '--help'):
        print(__doc__); return
    c = a[0]
    if c == 'init': cmd_init(a[1], a[2] if len(a) > 2 else a[1])
    elif c == 'fetch': cmd_fetch(a[1], a[2:])
    elif c == 'addsrc':
        via = a[a.index('--via') + 1] if '--via' in a else 'webfetch'
        note = a[a.index('--note') + 1] if '--note' in a else ''
        tf = a[a.index('--text') + 1] if '--text' in a else None
        cmd_addsrc(a[1], a[2], via, note, tf)
    elif c == 'grep': cmd_grep(a[1], ' '.join(a[2:]))
    elif c == 'lint': sys.exit(1 if cmd_lint(a[1]) else 0)
    elif c == 'timeline': cmd_timeline(a[1])
    elif c == 'gaps': cmd_gaps(a[1])
    elif c == 'verify': sys.exit(1 if cmd_verify(a[1], a[2] if len(a) > 2 else None) else 0)
    elif c == 'stats': cmd_stats(a[1], a[a.index('--old') + 1] if '--old' in a else None)
    elif c == 'domains': cmd_domains(a[1] if len(a) > 1 else None)
    else: print(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
