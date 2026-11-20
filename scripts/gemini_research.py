# -*- coding: utf-8 -*-
"""Gemini API で「相関図にまだ無い」企業・人物・取引・移籍を調べる試作(2026/11/19)。

しくみ(2段):
  1. 調べる: Gemini + Google検索(グラウンディング)で、テーマについて新しい事実を探す。
     「すでにある範囲」(notebooklm-code/10_*.md)をそのまま渡して、重ならないものだけを返させる。
  2. 照らす: 共有フォルダの notebooklm/ と notebooklm-code/ を Gemini の「ファイル検索」
     (File Search ストア)に入れておき、1. の候補がもう資料にあるかを確かめる。
     ※ Gemini API はファイル検索とGoogle検索を同じ呼び出しで併用できないため、2回に分けている。
  さらに手元でも、既存の会社名・人物名の一覧(11_*.md)と名前を照らす。

結果は inbox/gemini/日付.json と 日付.md(表)に足す(同じ名前があれば -2, -3 … を付けて新しく作る。消さない・上書きしない)。
このフォルダは merge_inbox.py の対象外なので、サイトには自動では出ない(候補として人が見る)。

キー: 環境変数 GEMINI_API_KEY(コードに書かない)。モデル: GEMINI_MODEL(既定は gemini-2.5-flash。429 のときは次の候補を試す)。

使い方:
  python3 scripts/gemini_research.py status
  python3 scripts/gemini_research.py store [--dry-run]           # 資料をファイル検索ストアに入れる(1回でよい。足すだけ)
  python3 scripts/gemini_research.py research "テーマ" [--max 10] [--no-check] [--dry-run]
  python3 scripts/gemini_research.py daily [--dry-run]           # 曜日ごとのテーマで調べ、すぐ scripts/gemini_verify.py で確かめる(毎朝の定期タスク)
"""
import argparse, datetime, glob, json, mimetypes, os, re, ssl, sys, time, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, 'inbox', 'gemini')
STORE_FILE = os.path.join(OUT_DIR, 'store.json')
DOCS = os.environ.get('GEMINI_DOCS_DIR', '/mnt/project-files')
API = 'https://generativelanguage.googleapis.com'
CONF = ['公式', '開示', '報道', '本人の発言', '推定']
COLS = ['会社名', '関係', '相手', '金額', '日付', '出典URL', '確かさ', '備考']
EXTRA = ['人物', '役職', '移籍元', '移籍先']

# ファイル検索に入れる資料。コードそのもの(02〜05)は調べものに役立たないので入れない
DOC_GLOBS = ['notebooklm/*.md', 'notebooklm-code/00_*.md', 'notebooklm-code/10_*.md',
             'notebooklm-code/11_*.md', 'notebooklm-code/20_*.md']


def key():
    return os.environ.get('GEMINI_API_KEY', '').strip()


# 2026/11/19: 無料枠では Google検索つきの呼び出しが gemini-flash-latest などで 429(枠切れ)になり、
# gemini-2.5-flash だけ通った。そのため既定は gemini-2.5-flash にし、429 のときは次の候補を順に試す。
MODEL_FALLBACKS = ['gemini-2.5-flash', 'gemini-flash-latest', 'gemini-3.5-flash', 'gemini-2.5-pro']
_model_used = []


def models():
    env = os.environ.get('GEMINI_MODEL', '').strip()
    return [env] + [m for m in MODEL_FALLBACKS if m != env] if env else list(MODEL_FALLBACKS)


def model():
    return _model_used[-1] if _model_used else models()[0]


def _ctx():
    ca = os.environ.get('SSL_CERT_FILE') or os.environ.get('REQUESTS_CA_BUNDLE')
    return ssl.create_default_context(cafile=ca if ca and os.path.exists(ca) else None)


def http(method, url, body=None, headers=None, raw=False, timeout=300):
    h = {'x-goog-api-key': key()}
    h.update(headers or {})
    data = body
    if body is not None and not isinstance(body, (bytes, bytearray)):
        data = json.dumps(body).encode('utf-8')
        h.setdefault('Content-Type', 'application/json')
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, context=_ctx(), timeout=timeout) as r:
            txt = r.read().decode('utf-8') or '{}'
            return (r.headers, json.loads(txt)) if raw else json.loads(txt)
    except urllib.error.HTTPError as e:
        msg = e.read().decode('utf-8', 'replace')[:800]
        raise RuntimeError(f'Gemini API エラー {e.code}: {msg}')


# ---------- 資料 ----------
def doc_files():
    out = []
    for g in DOC_GLOBS:
        out += sorted(glob.glob(os.path.join(DOCS, g)))
    return out


def read_doc(pattern):
    fs = sorted(glob.glob(os.path.join(DOCS, pattern)))
    return open(fs[0], encoding='utf-8').read() if fs else ''


def norm(s):
    s = unicodedata.normalize('NFKC', str(s or '')).lower()
    return re.sub(r'[\s・,、.()()「」\-_/]+', '', s)


def known_names():
    """11_すでにある会社名と人物名.md から名前の集合を作る(「、」区切り)。"""
    txt = read_doc('notebooklm-code/11_*.md')
    names = set()
    for line in txt.splitlines():
        if line.startswith('#') or '、' not in line:
            continue
        for n in line.split('、'):
            n = norm(n)
            if len(n) >= 2:
                names.add(n)
    return names


# ---------- 1回目: Google検索で調べる ----------
def build_prompt(topic, n):
    rng = read_doc('notebooklm-code/10_*.md')
    return f"""あなたはAI企業・半導体企業の相関図を作る調査担当です。今日は{datetime.date.today():%Y年%m月%d日}です。
テーマ: {topic}

下の「すでにある範囲」に無い、新しい事実(企業間の出資・取引・提携・買収、人物の移籍・就任・退任)を、Google検索で確かめて最大{n}件返してください。
守ること:
- 出典は記事や発表の元のURL(https で始まる、そのページを開けば事実が書いてあるもの)。見つからないものは入れない。うわさ・推測は入れない
- 出典はできるだけ一次情報(会社の公式発表・ニュースルーム、SECなどの開示書類、本人のX)にする。無ければ英語の大手報道(Reuters・Bloomberg・CNBC・TechCrunch など)。日本語の記事しか無いときだけ日本語の記事にする
- 向きをそろえる: 出資・買収・取引は「会社名」がお金を出す側・買う側、「相手」が受ける側・買われる側。人の動きは「人物」に人の名前(英語)、「移籍元」「移籍先」に会社名、「役職」に新しい役職を書き、「会社名」には主な会社を書く
- 確かさは次のどれか1つ: 公式(会社の発表) / 開示(SEC・EDINET・決算資料など法定の書類) / 報道 / 本人の発言(本人のX・ブログ・動画) / 推定(試算)
- 金額が報道ベースや契約の上限なら、備考にそう書く。不明なら金額は空
- 日付は YYYY-MM-DD(わかる範囲で YYYY-MM でもよい)
- すでにある会社・人物でも、新しい関係・金額・日付・移籍なら新しい情報として扱ってよい

答えは次の形のJSONだけを ```json と ``` で囲んで返す(説明文は不要):
{{"items":[{{"会社名":"","関係":"出資/取引/提携/買収/移籍/就任/退任 など","相手":"","金額":"","日付":"","出典URL":"","出典名":"媒体名","確かさ":"報道","備考":"","人物":"(人の動きのときだけ)","役職":"","移籍元":"","移籍先":""}}]}}

--- すでにある範囲 ---
{rng}
"""


def parse_items(text):
    m = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.S) or re.search(r'(\{.*\})', text, re.S)
    if not m:
        return []
    try:
        return (json.loads(m.group(1)).get('items') or [])
    except json.JSONDecodeError:
        return []


def grounding_sources(resp):
    out = []
    for c in resp.get('candidates') or []:
        for ch in ((c.get('groundingMetadata') or {}).get('groundingChunks') or []):
            w = ch.get('web') or {}
            if w.get('uri'):
                out.append([w.get('title') or w['uri'], w['uri']])
    return out


def resp_text(resp):
    parts = []
    for c in resp.get('candidates') or []:
        for p in ((c.get('content') or {}).get('parts') or []):
            if p.get('text'):
                parts.append(p['text'])
    return '\n'.join(parts)


BUSY_WAITS = [20, 60, 120]  # 2026/11/19: 混雑(503・500)のときは時間をおいてやり直す(秒)


def gen(body):
    last = None
    for m in models():
        for i in range(len(BUSY_WAITS) + 1):
            try:
                r = http('POST', f'{API}/v1beta/models/{m}:generateContent', body)
                _model_used.append(m)
                return r
            except RuntimeError as e:
                last = e
                if (' 503' in str(e) or ' 500' in str(e)) and i < len(BUSY_WAITS):
                    print(f'[{m}] 混雑のため {BUSY_WAITS[i]}秒待ってやり直す', file=sys.stderr)
                    time.sleep(BUSY_WAITS[i])
                    continue
                if not any(c in str(e) for c in (' 429', ' 404', ' 503', ' 500')):
                    raise
                print(f'[{m}] 枠切れ・混雑・使えないため次のモデルを試す', file=sys.stderr)
                break
    raise last


def search_step(topic, n):
    body = {'contents': [{'role': 'user', 'parts': [{'text': build_prompt(topic, n)}]}],
            'tools': [{'google_search': {}}]}
    resp = gen(body)
    return parse_items(resp_text(resp)), grounding_sources(resp)


# ---------- 2回目: ファイル検索で既存資料と照らす ----------
def check_step(items, store):
    lst = '\n'.join(f'{i+1}. {it.get("会社名")} / {it.get("関係")} / {it.get("相手")} / {it.get("金額")} / {it.get("日付")}'
                    for i, it in enumerate(items))
    q = f"""次の候補それぞれについて、資料(AI企業の相関図の書き出し)にすでに同じ関係が書かれているかを調べてください。
同じ会社・人物でも、関係・金額・日付が違えば「新しい」とします。
答えはJSONだけ: ```json {{"results":[{{"no":1,"already":true,"where":"資料のどこに書いてあったか(短く)"}}]}} ```
候補:
{lst}"""
    body = {'contents': [{'role': 'user', 'parts': [{'text': q}]}],
            'tools': [{'file_search': {'file_search_store_names': [store]}}]}
    text = resp_text(gen(body))
    m = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.S) or re.search(r'(\{.*\})', text, re.S)
    try:
        return {int(r['no']): r for r in json.loads(m.group(1)).get('results', [])} if m else {}
    except (ValueError, KeyError, json.JSONDecodeError):
        return {}


# ---------- ファイル検索ストア ----------
def load_store():
    return json.load(open(STORE_FILE, encoding='utf-8')) if os.path.exists(STORE_FILE) else {}


def save_store(st):
    os.makedirs(OUT_DIR, exist_ok=True)
    json.dump(st, open(STORE_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def build_store(dry=False, log=print):
    files = doc_files()
    st = load_store()
    done = set(st.get('uploaded', []))
    todo = [f for f in files if os.path.relpath(f, DOCS) not in done]
    log(f'資料 {len(files)} 個(入れ済み {len(files)-len(todo)}、これから {len(todo)})。合計 {sum(os.path.getsize(f) for f in todo)/1e6:.1f}MB')
    if dry:
        for f in todo:
            log('  入れる予定: ' + os.path.relpath(f, DOCS))
        return st
    if not st.get('name'):
        r = http('POST', f'{API}/v1beta/fileSearchStores', {'displayName': 'ai-soukanzu-notebooklm'})
        st = {'name': r['name'], 'created': datetime.date.today().isoformat(), 'uploaded': []}
        save_store(st)
        log('ストアを作った: ' + st['name'])
    for f in todo:
        rel = os.path.relpath(f, DOCS)
        size = os.path.getsize(f)
        hdr, _ = http('POST', f'{API}/upload/v1beta/{st["name"]}:uploadToFileSearchStore',
                      {'displayName': rel, 'mimeType': 'text/plain'},
                      {'X-Goog-Upload-Protocol': 'resumable', 'X-Goog-Upload-Command': 'start',
                       'X-Goog-Upload-Header-Content-Length': str(size),
                       'X-Goog-Upload-Header-Content-Type': 'text/plain'}, raw=True)
        url = hdr.get('x-goog-upload-url') or hdr.get('X-Goog-Upload-URL')
        op = http('POST', url, open(f, 'rb').read(),
                  {'X-Goog-Upload-Command': 'upload, finalize', 'X-Goog-Upload-Offset': '0',
                   'Content-Type': 'text/plain'})
        name = op.get('name')
        for _ in range(120):  # 最大10分待つ
            if op.get('done') or not name:
                break
            time.sleep(5)
            op = http('GET', f'{API}/v1beta/{name}')
        if op.get('error'):
            log(f'  失敗: {rel} {op["error"]}')
            continue
        st['uploaded'].append(rel)
        save_store(st)
        log(f'  入れた: {rel}')
    return st


# ---------- まとめ・保存 ----------
def clean(items, names, extra_src):
    out = []
    for it in items:
        url = str(it.get('出典URL') or '').strip()
        if not url.startswith('http'):
            continue  # 出典が無いものは入れない
        cf = str(it.get('確かさ') or '').strip()
        if cf not in CONF:
            cf = '本人の発言' if cf == '本人' else '推定'
        if re.search(r'sec\.gov|edinet-fsa|disclosure', url) and cf == '報道':
            cf = '開示'
        row = {c: str(it.get(c) or '').strip() for c in COLS}
        for c in EXTRA:  # 人の動きのときの項目(2026/11/19追加)。あるときだけ残す
            if str(it.get(c) or '').strip():
                row[c] = str(it[c]).strip()
        row['確かさ'] = cf
        row['src'] = [[str(it.get('出典名') or url), url]]
        known = [x for x in (it.get('会社名'), it.get('相手')) if norm(x) in names]
        row['既存の名前'] = known
        out.append(row)
    return out


def to_md(topic, rows, meta):
    lines = [f'# Gemini調査の候補({meta["date"]})', '',
             f'- テーマ: {topic}', f'- モデル: {meta["model"]}',
             f'- 既存資料との照らし合わせ: {meta["checked"]}', '',
             '| ' + ' | '.join(COLS) + ' |', '|' + '---|' * len(COLS)]
    for r in rows:
        note = r['備考']
        if r.get('既存の名前'):
            note += f'(既存の名前: {"・".join(r["既存の名前"])})'
        if r.get('資料に既出'):
            note += f'(資料に既出の可能性: {r["資料に既出"]})'
        vals = [r[c] for c in COLS[:-1]] + [note]
        lines.append('| ' + ' | '.join(v.replace('|', '/').replace('\n', ' ') for v in vals) + ' |')
    if meta.get('grounding'):
        lines += ['', '## Google検索で見た元ページ', ''] + [f'- [{t}]({u})' for t, u in meta['grounding'][:30]]
    return '\n'.join(lines) + '\n'


def new_path(date, ext):
    os.makedirs(OUT_DIR, exist_ok=True)
    base, i = os.path.join(OUT_DIR, date), 1
    p = base
    while os.path.exists(p + '.json') or os.path.exists(p + '.md'):
        i += 1
        p = f'{base}-{i}'
    return p


def research(topic, n=10, check=True, dry=False, log=print):
    date = datetime.date.today().isoformat()
    if dry or not key():
        prompt = build_prompt(topic, n)
        st = load_store()
        log('【ドライラン】Gemini には送っていません' + ('' if key() else '(GEMINI_API_KEY が未設定)'))
        log(f'- モデル: {model()}')
        log(f'- 1回目(Google検索つき)に送る文: {len(prompt):,}文字。先頭:\n' + prompt[:400] + '…')
        log(f'- 2回目(ファイル検索): ' + (st.get('name') or 'ストア未作成(先に store を実行)') if check else '- 2回目: しない')
        log(f'- 手元で照らす既存の名前: {len(known_names()):,}件')
        log(f'- 保存先(本番のとき): {os.path.relpath(new_path(date, ""), ROOT)}.json / .md')
        return {'dry_run': True, 'items': []}
    items, gsrc = search_step(topic, n)
    rows = clean(items, known_names(), gsrc)
    # 検索で見たページの転送リンクは数時間で使えなくなるので、すぐ元のURLにしておく(2026/11/19)
    try:
        import gemini_verify
        gres = gemini_verify.resolve_pool(gsrc)
    except Exception as e:
        print('転送リンクを元のURLにできなかった:', e, file=sys.stderr)
        gres = []
    st = load_store()
    checked = 'しない'
    if check and rows and st.get('name'):
        res = check_step(rows, st['name'])
        for i, r in enumerate(rows):
            x = res.get(i + 1)
            if x and x.get('already'):
                r['資料に既出'] = x.get('where') or 'あり'
        checked = f'ファイル検索({st["name"]})'
    elif check:
        checked = 'ストア未作成のため、名前の照らし合わせだけ'
    meta = {'date': date, 'model': model(), 'checked': checked, 'grounding': gsrc}
    p = new_path(date, '')
    json.dump({'date': date, 'kind': 'gemini', 'topic': topic, 'model': meta['model'], 'checked': checked,
               'items': rows, 'grounding': gsrc, 'grounding_resolved': gres}, open(p + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p + '.md', 'w', encoding='utf-8').write(to_md(topic, rows, meta))
    log(f'{len(rows)}件を保存: {os.path.relpath(p, ROOT)}.json / .md')
    return {'items': rows, 'saved': os.path.relpath(p, ROOT) + '.md', 'markdown': to_md(topic, rows, meta)}


# 毎朝の定期タスクで使うテーマ(曜日ごと。2026/11/19追加)。月=0 … 日=6
DAILY_THEMES = [
    '直近3日のAI企業・半導体企業の大型の資金調達と買収(世界)',
    '直近3日のAI企業・半導体企業の経営陣・主要研究者の移籍・就任・退任',
    '直近3日の計算資源(GPU・データセンター・電力・メモリ)の大型契約と提携',
    '直近3日の日本のAIスタートアップの資金調達・提携と、日本の大企業とAI企業の提携',
    '直近3日のAIスタートアップの買収(大手IT・半導体・SaaS企業による)と、新しく設立されたAI企業',
    '直近3日のアジア(台湾・韓国・シンガポール・インド・中東)のAI企業の資金調達・提携・人の動き',
    '直近1週間のVC・投資会社のAI分野の大型案件と、新しいファンド',
]


def daily_theme(d=None):
    d = d or datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date()
    return DAILY_THEMES[d.weekday()]


def status():
    st = load_store()
    return {'GEMINI_API_KEY': 'あり' if key() else 'なし', 'model': model(), 'docs_dir': DOCS,
            'docs': len(doc_files()), 'store': st.get('name') or '未作成',
            'uploaded': len(st.get('uploaded', []))}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('status')
    s = sp.add_parser('store'); s.add_argument('--dry-run', action='store_true')
    dd = sp.add_parser('daily', help='曜日ごとのテーマで調べて、そのまま確かめる(毎朝の定期タスク用)')
    dd.add_argument('--max', type=int, default=10); dd.add_argument('--dry-run', action='store_true')
    r = sp.add_parser('research'); r.add_argument('topic'); r.add_argument('--max', type=int, default=10)
    r.add_argument('--no-check', action='store_true'); r.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    if a.cmd == 'status':
        print(json.dumps(status(), ensure_ascii=False, indent=1))
    elif a.cmd == 'store':
        if not key() and not a.dry_run:
            print('GEMINI_API_KEY が未設定なので、ドライランにします'); a.dry_run = True
        build_store(a.dry_run)
    elif a.cmd == 'daily':
        topic = daily_theme()
        print('今日のテーマ: ' + topic)
        res = research(topic, a.max, True, a.dry_run)
        if res.get('saved'):
            import gemini_verify  # 2026/11/19: 調べたらすぐ確かめる(合格したものだけ inbox/money・moves に足す)
            gemini_verify.run([os.path.join(ROOT, res['saved'][:-3] + '.json')])
    else:
        res = research(a.topic, a.max, not a.no_check, a.dry_run)
        if res.get('markdown'):
            print(res['markdown'])


if __name__ == '__main__':
    main()
