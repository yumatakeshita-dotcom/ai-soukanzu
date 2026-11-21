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
  python3 scripts/gemini_research.py research "テーマ" [--max 10] [--no-check] [--no-verify] [--dry-run]
  python3 scripts/gemini_research.py daily [--dry-run]           # 曜日ごとのテーマで調べ、すぐ確かめる。そのあと宿題リスト(inbox/queue.json)の先頭を1件(毎朝の定期タスク)
  python3 scripts/gemini_research.py usage                         # 使った回数を日ごとに数える(無料枠が足りるかの目安)
  python3 scripts/gemini_research.py retry                         # 枠切れで後回しにしたテーマをやり直す
  python3 scripts/gemini_research.py limit                         # 今日の使った回数と1日の上限(inbox/gemini/limits.json)を見る
  python3 scripts/gemini_research.py verify inbox/gemini/日付.json   # 出典URLを開いて確かめ直す(日付_urlcheck.md を足す)
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
MODEL_FALLBACKS = ['gemini-2.5-flash', 'gemini-flash-latest', 'gemini-3.5-flash', 'gemini-3.1-pro-preview']
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
def media_leads(limit=12):
    """動画・ポッドキャストの新着から作った手がかり(inbox/media/)のタイトルだけを渡す(2026/11/21追加)。"""
    fs = sorted(glob.glob(os.path.join(ROOT, 'inbox', 'media', '2*.json')))
    if not fs:
        return ''
    try:
        leads = json.load(open(fs[-1], encoding='utf-8')).get('leads', [])[:limit]
    except Exception:  # noqa: BLE001
        return ''
    if not leads:
        return ''
    rows = '\n'.join(f"- {l['published']} {l['source']}: {l['title'][:90]}" for l in leads)
    return ('\n--- 最近の動画・ポッドキャストの題名(手がかり。ここから新しい事実を探してよいが、事実は必ず検索で別の出典を確かめる) ---\n' + rows + '\n')


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

{media_leads()}
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


# ---------- 使った回数の記録(2026/11/20追加。足すだけ) ----------
# 呼び出しのたびに inbox/gemini/usage.jsonl に1行足す(日時・モデル・結果・トークン数)。`usage` コマンドで日ごとに数える。
# 無料枠が足りるか、有料にするかの目安にする。記録に失敗しても調査は止めない。
USAGE = os.path.join(OUT_DIR, 'usage.jsonl')


def usage_log(model_name, result, resp=None):
    try:
        um = (resp or {}).get('usageMetadata') or {}
        os.makedirs(OUT_DIR, exist_ok=True)
        with open(USAGE, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), 'model': model_name,
                                'result': result, 'in': um.get('promptTokenCount'), 'out': um.get('candidatesTokenCount')},
                               ensure_ascii=False) + '\n')
    except Exception:
        pass


def usage_report(log=print):
    if not os.path.exists(USAGE):
        log('まだ記録がありません'); return {}
    jst = datetime.timezone(datetime.timedelta(hours=9))
    days = {}
    for ln in open(USAGE, encoding='utf-8'):
        try: e = json.loads(ln)
        except json.JSONDecodeError: continue
        d = datetime.datetime.fromisoformat(e['at']).astimezone(jst).strftime('%Y-%m-%d')
        x = days.setdefault(d, {'ok': 0, 'quota': 0, 'busy': 0, 'cap': 0, 'in': 0, 'out': 0, 'models': {}})
        key = {'ok': 'ok', '429': 'quota', '503': 'busy', '500': 'busy', 'cap': 'cap'}.get(e['result'])
        if key: x[key] += 1
        if e['result'] == 'ok': x['models'][e['model']] = x['models'].get(e['model'], 0) + 1
        x['in'] += e.get('in') or 0; x['out'] += e.get('out') or 0
    log('日付(日本時間) | 成功 | 枠切れ(429) | 混雑 | 上限で停止 | 入力トークン | 出力トークン | モデル別の成功')
    for d in sorted(days):
        x = days[d]
        log(f'{d} | {x["ok"]} | {x["quota"]} | {x["busy"]} | {x["cap"]} | {x["in"]:,} | {x["out"]:,} | ' + ', '.join(f'{m}:{c}' for m, c in x['models'].items()))
    n = len(days); tot = sum(x['ok'] for x in days.values())
    log(f'\n{n}日間で成功 {tot}回(1日あたり {tot/n:.1f}回)。無料枠は検索つきで1モデル1日20回前後。枠切れ(429)が出る日が続くなら、有料への切り替えを検討(docs/gemini_research.md)')
    return days


class QuotaExhausted(RuntimeError):
    """全部のモデルで枠切れ(429)。無料枠の1日の上限に達したときなど。"""


# ---------- 1日の上限(2026/11/20追加) ----------
# inbox/gemini/limits.json の daily_max_calls(環境変数 GEMINI_DAILY_MAX があればそちら)を、1日(日本時間)の呼び出し回数の上限にする。
# 上限に達したら Gemini を呼ばず QuotaExhausted にする。→ 今ある「枠切れ」の流れ(やり直す列・宿題リストは翌朝に同じ項目)にそのまま乗る。
LIMITS = os.path.join(OUT_DIR, 'limits.json')
DEFAULT_DAILY_MAX = 18  # 無料枠(検索つきで1モデル1日20回前後)の範囲内


def daily_max():
    try:
        v = os.environ.get('GEMINI_DAILY_MAX')
        if v not in (None, ''):
            return int(v)
        return int(json.load(open(LIMITS, encoding='utf-8')).get('daily_max_calls', DEFAULT_DAILY_MAX))
    except Exception:
        return DEFAULT_DAILY_MAX


def calls_today():
    """今日(日本時間)の呼び出し回数。上限に止められた記録(cap)は数えない。"""
    if not os.path.exists(USAGE):
        return 0
    jst = datetime.timezone(datetime.timedelta(hours=9))
    today = datetime.datetime.now(jst).date()
    n = 0
    for ln in open(USAGE, encoding='utf-8'):
        try:
            e = json.loads(ln)
            if e.get('result') != 'cap' and datetime.datetime.fromisoformat(e['at']).astimezone(jst).date() == today:
                n += 1
        except Exception:
            continue
    return n

BUSY_WAITS = [20, 60, 120]  # 2026/11/19: 混雑(503・500)のときは時間をおいてやり直す(秒)


def gen(body):
    cap = daily_max()
    if cap > 0 and calls_today() >= cap:
        usage_log('-', 'cap')  # 自分で決めた上限で止めた記録(回数には数えない)
        raise QuotaExhausted(f'1日の上限 {cap} 回に達したため止めました(inbox/gemini/limits.json で変えられます)')
    last = None
    for m in models():
        for i in range(len(BUSY_WAITS) + 1):
            if cap > 0 and calls_today() >= cap:  # やり直しの途中で上限に達したら、そこで止める
                usage_log('-', 'cap')
                raise QuotaExhausted(f'1日の上限 {cap} 回に達したため止めました')
            try:
                r = http('POST', f'{API}/v1beta/models/{m}:generateContent', body)
                _model_used.append(m)
                usage_log(m, 'ok', r)
                return r
            except RuntimeError as e:
                last = e
                usage_log(m, next((c for c in ('429', '503', '500', '404') if f' {c}' in str(e)), 'error'))
                if (' 503' in str(e) or ' 500' in str(e)) and i < len(BUSY_WAITS):
                    print(f'[{m}] 混雑のため {BUSY_WAITS[i]}秒待ってやり直す', file=sys.stderr)
                    time.sleep(BUSY_WAITS[i])
                    continue
                if not any(c in str(e) for c in (' 429', ' 404', ' 503', ' 500')):
                    raise
                print(f'[{m}] 枠切れ・混雑・使えないため次のモデルを試す', file=sys.stderr)
                break
    if last is not None and ' 429' in str(last):
        raise QuotaExhausted(str(last)[:300])
    raise last


_last_process = {}


def process_info(resp):
    """2026/11/20: Geminiが実際に打った検索の言葉・見たページ・根拠の対応を取り出す(履歴用)"""
    queries, srcs, sup = [], [], []
    for c in resp.get('candidates') or []:
        g = c.get('groundingMetadata') or {}
        queries += g.get('webSearchQueries') or []
        base = len(srcs)
        for ch in g.get('groundingChunks') or []:
            w = ch.get('web') or {}
            srcs.append([w.get('title') or w.get('uri') or '', w.get('uri') or ''])
        for sp in g.get('groundingSupports') or []:
            sup.append({'text': (sp.get('segment') or {}).get('text', ''),
                        'idx': [base + i for i in sp.get('groundingChunkIndices') or []]})
    return {'queries': queries, 'sources': srcs, 'supports': sup, 'usage': resp.get('usageMetadata') or {}}


def search_step(topic, n):
    body = {'contents': [{'role': 'user', 'parts': [{'text': build_prompt(topic, n)}]}],
            'tools': [{'google_search': {}}]}
    resp = gen(body)
    _last_process.clear()
    _last_process.update(process_info(resp))
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


# ---------- 出典URLを実際に開いて確かめる(2026/11/20追加) ----------
# Gemini が書いたURLは作り話や日付ちがいのことがある。クラウドから開けるページは、
# 本文に会社名・相手の名前が載っているかまで確かめる。開けないサイトは「開けない」と正直に書く(確かめた扱いにしない)。
def _domain(u):
    m = re.match(r'https?://([^/]+)', u or '')
    return re.sub(r'^www\.', '', m.group(1).lower()) if m else ''


def _name_tokens(row):
    toks = []
    for x in (row.get('会社名'), row.get('相手')):
        for part in re.split(r'[,、/・]', str(x or '')):
            part = re.sub(r'\([^)]*\)|\uff08[^\uff09]*\uff09', '', part).strip()
            if len(part) >= 3 and part != '不明':
                toks.append(part)
    return toks[:6]


def check_url(row, grounded_domains, timeout=15):
    """行ごとに {'状態': ok|名前なし|開けない|エラー, '検索で見たサイト': bool, '詳細': str} を返す"""
    url = row['出典URL']
    res = {'検索で見たサイト': _domain(url) in grounded_domains}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; ai-soukanzu-check)'})
        with urllib.request.urlopen(req, timeout=timeout, context=_ctx()) as r:
            code = r.status
            html = r.read(600000).decode('utf-8', 'ignore')
    except urllib.error.HTTPError as e:
        res.update(状態='エラー', 詳細=f'HTTP {e.code}' + ('(ページが無い)' if e.code in (404, 410) else ''))
        return res
    except Exception as e:
        res.update(状態='開けない', 詳細='クラウドからつながらない(' + type(e).__name__ + ')')
        return res
    text = norm(re.sub(r'<[^>]+>', ' ', html))
    toks = _name_tokens(row)
    hit = [t for t in toks if norm(t) in text]
    title = re.search(r'<title[^>]*>(.*?)</title>', html, re.S)
    res['詳細'] = (re.sub(r'\s+', ' ', title.group(1)).strip()[:60] if title else '') or f'HTTP {code}'
    res['状態'] = 'ok' if hit or not toks else '名前なし'
    res['載っていた名前'] = hit
    return res


def verify_rows(rows, gsrc, log=print):
    gd = {_domain(u) for _, u in gsrc} | {re.sub(r'^www\.', '', str(t).lower()) for t, _ in gsrc}
    for r in rows:
        r['URL確認'] = check_url(r, gd)
        log(f'  {r["URL確認"]["状態"]:6} {r["会社名"]} ← {_domain(r["出典URL"])}')
    return rows


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
        u = r.get('URL確認')
        if u:
            lab = {'ok': 'URL確認:開けて名前も載っていた', '名前なし': 'URL確認:開けたが名前が見つからない',
                   '開けない': 'URL未確認:クラウドから開けない', 'エラー': 'URL確認:' + u.get('詳細', 'エラー')}[u['状態']]
            note += f'({lab}{"・検索で見たサイト" if u.get("検索で見たサイト") else ""})'
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


# ---------- 枠切れのときは、あとでやり直す列に足す(2026/11/20追加。足すだけ) ----------
# 無料枠は1日の回数に上限がある(429)。上限に達した日は、調べたいテーマを queue.jsonl に足しておき、
# 翌朝 `python3 scripts/gemini_research.py retry` でやり直す。やり直したら「done」の行を足す(消さない)。
QUEUE = os.path.join(OUT_DIR, 'queue.jsonl')


def _queue_events():
    if not os.path.exists(QUEUE):
        return []
    out = []
    for ln in open(QUEUE, encoding='utf-8'):
        ln = ln.strip()
        if ln:
            try: out.append(json.loads(ln))
            except json.JSONDecodeError: pass
    return out


def queue_add(topic, n, reason):
    os.makedirs(OUT_DIR, exist_ok=True)
    qid = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    with open(QUEUE, 'a', encoding='utf-8') as f:
        f.write(json.dumps({'id': qid, 'ev': 'queued', 'topic': topic, 'n': n, 'at': datetime.datetime.now().isoformat(timespec='seconds'),
                            'reason': reason[:120]}, ensure_ascii=False) + '\n')
    return qid


def queue_pending():
    ev = _queue_events()
    done = {e['id'] for e in ev if e.get('ev') in ('done', 'gave_up')}
    return [e for e in ev if e.get('ev') == 'queued' and e['id'] not in done]


def queue_mark(qid, ev, note=''):
    with open(QUEUE, 'a', encoding='utf-8') as f:
        f.write(json.dumps({'id': qid, 'ev': ev, 'at': datetime.datetime.now().isoformat(timespec='seconds'), 'note': note}, ensure_ascii=False) + '\n')


def retry_queue(log=print, max_items=3):
    """やり直す列にあるテーマを、古い順に最大 max_items 件やり直す。また枠切れなら、残りは次の日に回す。"""
    pend = queue_pending()
    if not pend:
        log('やり直す列は空です'); return 0
    done = 0
    for q in pend[:max_items]:
        log(f'やり直し: {q["topic"]}')
        try:
            r = research(q['topic'], q.get('n', 10), True, False, log, True, queue_on_quota=False)
        except QuotaExhausted:
            log('まだ枠切れです。残りは次の日にやり直します'); break
        queue_mark(q['id'], 'done', r.get('saved', ''))
        done += 1
    log(f'{done}件をやり直しました(残り {len(queue_pending())}件)')
    return done


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def resolve_redirect(url, timeout=15):
    """Googleの転送リンク(vertexaisearch…)を、実際の記事のURLに直す。直せなければ元のまま。"""
    if 'vertexaisearch.cloud.google.com/grounding-api-redirect' not in url:
        return url
    try:
        op = urllib.request.build_opener(_NoRedirect, urllib.request.HTTPSHandler(context=_ctx()))
        op.open(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=timeout)
    except urllib.error.HTTPError as e:
        loc = e.headers.get('Location', '')
        if e.code in (301, 302, 303, 307, 308) and loc.startswith('http'):
            return loc
    except Exception:
        pass
    return url


def research(topic, n=10, check=True, dry=False, log=print, verify=True, queue_on_quota=True):
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
    try:
        items, gsrc = search_step(topic, n)
    except QuotaExhausted as e:
        if not queue_on_quota:
            raise
        qid = queue_add(topic, n, str(e))
        log(f'今日は枠切れ(無料枠の1日の上限)です。「{topic}」はやり直す列に足しました(id {qid})。'
            '翌朝に `python3 scripts/gemini_research.py retry` でやり直します')
        return {'queued': qid, 'items': []}
    rows = clean(items, known_names(), gsrc)
    for r in rows:  # Googleの転送リンクは実際の記事のURLに直す(もとのリンクは「転送リンク」に残す)
        real = resolve_redirect(r['出典URL'])
        if real != r['出典URL']:
            r['転送リンク'] = r['出典URL']; r['出典URL'] = real
            r['src'] = [[r['src'][0][0], real]]
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
    if verify and rows:
        log('出典URLを開いて確かめる:')
        verify_rows(rows, gsrc, log)
    meta = {'date': date, 'model': model(), 'checked': checked, 'grounding': gsrc}
    p = new_path(date, '')
    json.dump({'date': date, 'kind': 'gemini', 'topic': topic, 'model': meta['model'], 'checked': checked,
               'items': rows, 'grounding': gsrc, 'grounding_resolved': gres,
               'process': dict(_last_process)}, open(p + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p + '.md', 'w', encoding='utf-8').write(to_md(topic, rows, meta))
    log(f'{len(rows)}件を保存: {os.path.relpath(p, ROOT)}.json / .md')
    try:  # 履歴の目次を作り直す(2026/11/20)。失敗しても調査は止めない
        import gemini_history
        gemini_history.build()
    except Exception as e:
        print('履歴の目次を作れなかった:', e, file=sys.stderr)
    return {'items': rows, 'saved': os.path.relpath(p, ROOT) + '.md', 'markdown': to_md(topic, rows, meta)}


# 毎朝の定期タスクで使うテーマ(曜日ごと。2026/11/19追加)。月=0 … 日=6
DAILY_THEMES = [
    '直近3日のAI企業・半導体企業の大型の資金調達と買収(世界)',
    '直近3日のAI企業・半導体企業の経営陣・主要研究者の移籍・就任・退任',
    '直近3日の計算資源(GPU・データセンター・電力・メモリ)の大型契約と提携',
    '直近3日の日本のAIスタートアップの資金調達・提携と、日本の大企業とAI企業の提携',
    '直近3日のAIスタートアップの買収(大手IT・半導体・SaaS企業による)と、新しく設立されたAI企業',
    '直近3日のアジア(台湾・韓国・インド・中東と、東南アジアのシンガポール・インドネシア・ベトナム・タイ)のAI企業の資金調達・提携・人の動き。出典は Inc42・TechCrunch・DealStreetAsia など本文を開ける報道の記事URLを優先',
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
    dd.add_argument('--no-queue', action='store_true', help='宿題リストの1件を調べない')
    r = sp.add_parser('research'); r.add_argument('topic'); r.add_argument('--max', type=int, default=10)
    r.add_argument('--no-check', action='store_true'); r.add_argument('--dry-run', action='store_true')
    r.add_argument('--no-verify', action='store_true')
    v = sp.add_parser('verify'); v.add_argument('file')
    sp.add_parser('retry')
    sp.add_parser('usage')
    sp.add_parser('limit')
    a = ap.parse_args()
    if a.cmd == 'status':
        print(json.dumps(status(), ensure_ascii=False, indent=1))
    elif a.cmd == 'store':
        if not key() and not a.dry_run:
            print('GEMINI_API_KEY が未設定なので、ドライランにします'); a.dry_run = True
        build_store(a.dry_run)
    elif a.cmd == 'retry':
        retry_queue()
    elif a.cmd == 'usage':
        usage_report()
    elif a.cmd == 'limit':
        c, m = calls_today(), daily_max()
        print(f'今日(日本時間)の呼び出し {c} 回 / 1日の上限 ' + (f'{m} 回(残り {max(m - c, 0)} 回)' if m > 0 else 'なし'))
    elif a.cmd == 'verify':
        d = json.load(open(a.file, encoding='utf-8'))
        rows = verify_rows(d['items'], d.get('grounding') or [])
        out = re.sub(r'(_raw)?\.json$', '', a.file) + '_urlcheck.md'
        if os.path.exists(out):
            print(f'{out} がすでにあるので上書きしません'); return
        meta = {'date': d.get('date', ''), 'model': d.get('model', ''), 'checked': d.get('checked', '')}
        open(out, 'w', encoding='utf-8').write(to_md(d.get('topic', ''), rows, meta))
        print('保存:', out)
    elif a.cmd == 'daily':
        topic = daily_theme()
        print('今日のテーマ: ' + topic)
        res = research(topic, a.max, True, a.dry_run)
        if res.get('saved'):
            import gemini_verify  # 2026/11/19: 調べたらすぐ確かめる(合格したものだけ inbox/money・moves に足す)
            gemini_verify.run([os.path.join(ROOT, res['saved'][:-3] + '.json')])
        # 2026/11/20: そのあと、調べる順番の一覧(inbox/queue.json)の先頭を1件だけ調べる。人の指示は要らない。
        # 無料枠が切れていたら状態を変えずに終わる(次の朝に同じ項目)。--no-queue で省ける
        if not a.no_queue:
            try:
                import research_queue
                research_queue.run_next(a.dry_run)
            except Exception as e:
                print('宿題リストの調査をできなかった:', str(e)[:200], file=sys.stderr)
        # 2026/11/20: 枠切れで後回しにしたテーマが列にあれば、今日の分のあとに1件だけやり直す(定期タスクの文を変えずに拾うため)
        if not a.dry_run and queue_pending():
            retry_queue(max_items=1)
    else:
        res = research(a.topic, a.max, not a.no_check, a.dry_run, verify=not a.no_verify)
        if res.get('markdown'):
            print(res['markdown'])


if __name__ == '__main__':
    main()
