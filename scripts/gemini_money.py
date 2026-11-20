# -*- coding: utf-8 -*-
"""お金の流れの調査: 「探す」をGeminiに、「確かめる」をプログラムにまかせる(2026/11/19)。

流れ(Claudeが読むのは最後の「合格」だけ):
  1. search : Gemini + Google検索で、直近の出資・買収・創業者の出資を探して表にする(inbox/gemini/money/日付_raw.json)
  2. verify : 表の1件ずつを、プログラムで機械的に確かめる(inbox/gemini/money/日付_verified.json と 日付_pass.md)
       - 出典URLが実際に開けるか(転送リンク・クラウドから届かないサイトは「届かない」)
       - 開いたページに、会社名・金額が書いてあるか
       - ページの日付と、Geminiが書いた日付が合うか(7日を超えて違えば「日付の食い違い」)
       - すでに相関図・調査の保存(inbox/)にある事実でないか(重複)
  3. emit   : 合格したものだけを inbox/money/日付_gemini.json に書く(Claudeが pass.md を見て確認したあと)

Geminiの無料枠: 1日の呼び出し回数に上限を置く(既定 12回。環境変数 GEMINI_DAILY_LIMIT)。
429(枠切れ)が全モデルで出たら、その日は止める(inbox/gemini/usage.json に記録。あすは自動で再開)。
足すだけ: 既存のファイルは上書きしない(同じ日は -2, -3 …)。Cloudflare・D1・site/ には触らない。

使い方:
  python3 scripts/gemini_money.py run [--max 10] [--days 14]     # search + verify をまとめて
  python3 scripts/gemini_money.py search [--max 10]
  python3 scripts/gemini_money.py verify [ファイル]               # 省略なら今日の最新の raw
  python3 scripts/gemini_money.py emit [ファイル] [--only 1,3]    # 合格を inbox/money/ へ
  python3 scripts/gemini_money.py status
"""
import argparse, datetime, glob, html, json, os, re, ssl, sys, unicodedata, urllib.request, urllib.error
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gemini_research as gr  # 2026/11/19 PR39 の試作(Geminiへの呼び出しをそのまま使う)

ROOT = gr.ROOT
OUT = os.path.join(ROOT, 'inbox', 'gemini', 'money')  # 確かめた途中の記録(モードごとに名前を分ける)
USAGE = os.path.join(ROOT, 'inbox', 'gemini', 'usage.json')
KINDS = ['出資', '買収', '報酬', '共同創業', '支援']
MODE = 'money'  # 'money'(お金の流れ) か 'moves'(引き抜き・人の移籍)。--kind で切り替える(2026/11/20追加)
OUT_DIRS = {'money': os.path.join(ROOT, 'inbox', 'money'), 'moves': os.path.join(ROOT, 'inbox', 'moves')}
CONF = ['公式', '開示', '報道', '本人の発言', '推定']
UA = 'Mozilla/5.0 (compatible; relmap-verify/1.0)'


# ---------- 無料枠の見張り ----------
def today():
    return datetime.date.today().isoformat()


def load_usage():
    try:
        return json.load(open(USAGE, encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def save_usage(u):
    os.makedirs(os.path.dirname(USAGE), exist_ok=True)
    json.dump(u, open(USAGE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)


def daily_limit():
    try:
        return int(os.environ.get('GEMINI_DAILY_LIMIT', '12'))
    except ValueError:
        return 12


def quota_ok():
    d = load_usage().get(today(), {})
    if d.get('blocked'):
        return False, '今日は無料枠が切れている(429)ので止めている'
    if d.get('calls', 0) >= daily_limit():
        return False, f'今日の呼び出しが上限({daily_limit()}回)に達した'
    return True, ''


def note_call(blocked=False):
    u = load_usage()
    d = u.setdefault(today(), {'calls': 0, 'blocked': False})
    d['calls'] += 1
    if blocked:
        d['blocked'] = True
    save_usage(u)


# ---------- 1. 探す ----------
def recent_known(days=30, limit=80):
    """最近の調査の保存(inbox/money と inbox/gemini/money)から「すでに見つけた」一覧を作る。"""
    rows = []
    for f in sorted(glob.glob(os.path.join(OUT_DIRS[MODE], '*.json'))):
        try:
            for it in json.load(open(f, encoding='utf-8')).get('items', []):
                rows.append(f"{it.get('name_ja') or it.get('from')} → {it.get('to')} / {it.get('kind') or it.get('role','')} / {it.get('amount','')} / {it.get('date','')}")
        except (OSError, ValueError):
            pass
    return rows[-limit:]


MOVES_PROMPT = '''あなたはAI企業・半導体企業の相関図を作る調査担当です。今日は{today}です。
{start}から今日までに発表・報道された、AI企業・半導体企業の経営陣・主要研究者・エンジニアの移籍・就任・退任・引き抜きを、Google検索で確かめて最大{n}件返してください。対象の例: OpenAI, Anthropic, xAI, Meta, Google DeepMind, Microsoft, Apple, Nvidia, Mistral, Thinking Machines, Perplexity, Cursor, TSMC, Samsung, SK hynix, ソフトバンク, Sakana AI, Preferred Networks。
守ること:
- 出典は記事や発表の元のURL(媒体や会社自身のサイトのアドレス)。vertexaisearch.cloud.google.com などの転送リンクは絶対に書かない。元のアドレスがわからないものは入れない
- 出典は1件につき2つまで。2つ目は別の媒体で
- 日付は、移籍・就任が発表された日(YYYY-MM-DD)
- 本人の名前(英語と日本語)、移籍元(from)、移籍先(to)、役職(role)を書く。移籍先か移籍元が無い「退任」は from か to を空にしない(わからなければ入れない)
- 確かさは次のどれか1つ: 公式 / 開示 / 報道 / 本人の発言 / 推定
- 下の「すでに見つけた」と同じ人・同じ移籍は入れない

答えは次の形のJSONだけを ```json と ``` で囲んで返す(説明文は不要):
{{"items":[{{"name_en":"","name_ja":"","from":"移籍元の会社","to":"移籍先の会社","role":"役職","date":"YYYY-MM-DD","note":"60字以内の日本語の説明","src_name":"媒体名","src_url":"","src_name2":"","src_url2":"","confidence":"報道"}}]}}

--- すでに見つけた ---
{known}
'''


def build_prompt(n, days):
    if MODE == 'moves':
        d = datetime.date.today()
        start = d - datetime.timedelta(days=days)
        known = '\n'.join(recent_known()) or '(なし)'
        return MOVES_PROMPT.format(today=f'{d:%Y年%m月%d日}', start=f'{start:%Y年%m月%d日}', n=n, known=known)
    d = datetime.date.today()
    start = d - datetime.timedelta(days=days)
    known = '\n'.join(recent_known()) or '(なし)'
    rng = gr.read_doc('notebooklm-code/10_*.md')
    rng = ('\n--- 相関図の範囲 ---\n' + rng) if rng else ''
    return f"""あなたはAI企業・半導体企業の相関図を作る調査担当です。今日は{d:%Y年%m月%d日}です。
{start:%Y年%m月%d日}から今日までに発表された、AI・半導体企業にかかわる「お金の流れ」(出資・資金調達・買収・創業者や有名人の出資・大型契約に伴う出資)を、Google検索で確かめて最大{n}件返してください。
守ること:
- 出典は、記事や発表の元のURL(例 https://www.reuters.com/... のように、媒体や会社自身のサイトのアドレス)。vertexaisearch.cloud.google.com や google.com の転送リンク(grounding-api-redirect)は絶対に書かない。元のアドレスがわからないものは入れない。会社の公式発表・SEC書類があれば優先。うわさ・推測は入れない
- 出典は1件につき2つまで(出典URL と 出典URL2)。2つ目は別の媒体で
- 日付は、出来事が発表された日(YYYY-MM-DD)。記事の日付ではない。わからなければ入れない
- 金額は、記事に書いてある数字をそのまま(例「4.5億ドル」「約12億円」)。報道ベース・契約の上限・評価額などは備考に書く。不明なら空
- 確かさは次のどれか1つ: 公式 / 開示 / 報道 / 本人の発言 / 推定
- 種類(kind)は 出資 / 買収 / 報酬 / 共同創業 / 支援 のどれか
- 下の「すでに見つけた」と同じ事実は入れない(同じ会社でも、新しいラウンド・金額・日付なら入れてよい)

答えは次の形のJSONだけを ```json と ``` で囲んで返す(説明文は不要):
{{"items":[{{"from":"お金を出した人・会社","to":"受け取った人・会社","kind":"出資","amount":"","date":"YYYY-MM-DD","note":"60字以内の日本語の説明","src_name":"媒体名","src_url":"","src_name2":"","src_url2":"","confidence":"報道"}}]}}

--- すでに見つけた ---
{known}
{rng}
"""


def search(n=10, days=14, log=print):
    ok, why = quota_ok()
    if not ok:
        log('止めた: ' + why)
        return None
    if not gr.key():
        log('止めた: GEMINI_API_KEY が未設定')
        return None
    body = {'contents': [{'role': 'user', 'parts': [{'text': build_prompt(n, days)}]}],
            'tools': [{'google_search': {}}]}
    try:
        resp = gr.gen(body)
        note_call()
    except RuntimeError as e:
        blocked = ' 429' in str(e)
        note_call(blocked=blocked)
        log(('止めた: 無料枠が切れた(429)。あすまた動く' if blocked else '止めた: Gemini のエラー ' + str(e)[:200]))
        return None
    text = gr.resp_text(resp)
    m = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.S) or re.search(r'(\{.*\})', text, re.S)
    try:
        items = json.loads(m.group(1)).get('items') or [] if m else []
    except ValueError:
        items = []
    os.makedirs(OUT, exist_ok=True)
    p = new_path(prefix() + today() + '_raw')
    out = {'date': today(), 'kind': 'gemini-money', 'model': gr.model(), 'days': days, 'items': items,
           'grounding': gr.grounding_sources(resp)}
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f'Geminiの候補 {len(items)}件 → {os.path.relpath(p, ROOT)}')
    return p


def prefix():
    return 'moves_' if MODE == 'moves' else ''


def new_path(stem, ext='.json'):
    p, i = os.path.join(OUT, stem + ext), 1
    while os.path.exists(p):
        i += 1
        p = os.path.join(OUT, f'{stem}-{i}{ext}')
    return p


# ---------- 2. 確かめる ----------
def norm(s):
    s = unicodedata.normalize('NFKC', str(s or '')).lower()
    return re.sub(r'[\s・,、.()「」\-_/&\'’"]+', '', s)


def parties(it):
    """照らす名前。money は(出す側, 受け取る側)。moves は(本人の名前, 移籍先)。"""
    if MODE == 'moves':
        frs = name_variants(it.get('name_ja')) + name_variants(it.get('name_en'))
        return frs, name_variants(it.get('to'))
    return name_variants(it.get('from')), name_variants(it.get('to'))


def name_variants(s):
    """「A・B(共同リード)」「Google(Google Labs)」→ 照らす名前の候補。括弧の中身は別の名前としても使う。"""
    s = unicodedata.normalize('NFKC', str(s or ''))
    parts = re.split(r'[・、,/&]|\band\b|\bの\b', re.sub(r'\([^)]*\)', lambda m: ' ' + m.group(0)[1:-1] + ' ', s))
    drop = {'リード', '共同リード', '参加', '主導', '出資者', 'ほか', '他', 'など'}
    out = []
    for p in parts:
        p = norm(re.sub(r'(共同)?リード|主導|参加|ほか|など', '', p))
        if len(p) >= 2 and p not in drop and p not in out:
            out.append(p)
    return out


MAG = {'兆': 1e12, '億': 1e8, '万': 1e4, '千': 1e3, 'trillion': 1e12, 'billion': 1e9, 'bn': 1e9,
       'million': 1e6, 'mn': 1e6, 'm': 1e6, 'b': 1e9, 'k': 1e3, '百万': 1e6, '十億': 1e9}
NUM = re.compile(r'(\d[\d,]*(?:\.\d+)?)\s*(兆|億|万|百万|十億|trillion|billion|million|bn|mn|[mbk](?![a-z]))', re.I)


def amounts_in(text):
    """文章中の「数字+単位」を、実際の大きさの数に直した集合にする(4.5 billion → 4.5e9、45億 → 4.5e9)。"""
    t = unicodedata.normalize('NFKC', text)
    vals = set()
    for m in NUM.finditer(t):
        try:
            v = float(m.group(1).replace(',', ''))
        except ValueError:
            continue
        mag = MAG.get(m.group(2).lower())
        if mag:
            vals.add(round(v * mag))
    # 「4億5000万」のような複合
    for m in re.finditer(r'(\d+)億\s*(\d[\d,]*)万', t):
        vals.add(round(int(m.group(1)) * 1e8 + int(m.group(2).replace(',', '')) * 1e4))
    # 「$4,500,000,000」のような桁区切り
    for m in re.finditer(r'\d{1,3}(?:,\d{3}){2,}', t):
        vals.add(int(m.group(0).replace(',', '')))
    return vals


def amount_match(amount, page_vals):
    cand = amounts_in(amount)
    if not cand:
        return None, ''
    for c in cand:
        for v in page_vals:
            if v and abs(v - c) / max(v, c) <= 0.011:
                return True, ''
    return False, '、'.join(f'{c:,}' for c in sorted(cand))


MONTHS = {m: i + 1 for i, m in enumerate(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])}


def parse_dates(s):
    s = unicodedata.normalize('NFKC', s)
    out = []
    for m in re.finditer(r'(20\d\d)[-/.年](\d{1,2})[-/.月](\d{1,2})', s):
        out.append((m.group(1), m.group(2), m.group(3)))
    for m in re.finditer(r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d\d)', s, re.I):
        out.append((m.group(3), MONTHS[m.group(1).lower()[:3]], m.group(2)))
    res = []
    for y, mo, d in out:
        try:
            res.append(datetime.date(int(y), int(mo), int(d)))
        except ValueError:
            pass
    return res


def page_dates(raw_html, text):
    """メタ情報の公開日 → 本文の先頭に出てくる日付、の順に探す。"""
    metas = re.findall(r'(?:article:published_time|datePublished|dateCreated|pubdate|og:updated_time|publishdate|date)["\'][^>]{0,80}?(?:content|datetime)?["\':=\s]+([0-9T:\-+Z./ ]{8,30})', raw_html, re.I)
    metas += re.findall(r'<time[^>]*datetime=["\']([^"\']+)', raw_html, re.I)
    d1 = [d for x in metas for d in parse_dates(x)]
    if d1:
        return d1, 'メタ情報'
    return parse_dates(text[:4000]), '本文の先頭'


def fetch(url, timeout=20):
    """(状態, 最終URL, HTML)。状態: ok / 転送リンク / 届かない:理由"""
    host = urlparse(url).netloc.lower()
    if 'vertexaisearch' in host or host.endswith('google.com') and '/url' in url:
        return '転送リンク(開けない)', url, ''
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'ja,en;q=0.8'})
    try:
        with urllib.request.urlopen(req, context=gr._ctx(), timeout=timeout) as r:
            final = r.geturl()
            if 'vertexaisearch' in final:
                return '転送リンク(開けない)', final, ''
            ct = r.headers.get('Content-Type', '')
            if 'html' not in ct and 'text' not in ct and 'xml' not in ct:
                return f'届かない:本文なし({ct[:30]})', final, ''
            raw = r.read(1_500_000)
            enc = re.search(r'charset=([\w-]+)', ct)
            return 'ok', final, raw.decode(enc.group(1) if enc else 'utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return f'届かない:HTTP {e.code}', url, ''
    except Exception as e:  # プロキシの拒否・タイムアウトなど
        return '届かない:' + str(e)[:80], url, ''


def html_text(raw):
    t = re.sub(r'<(script|style|noscript)[\s\S]*?</\1>', ' ', raw, flags=re.I)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', html.unescape(t))


def existing_blob(exclude=None):
    """重複の照合用: 既存の調査の保存・調査の新着・毎日の更新記録。(名前の近くに相手の名前があるかを調べる)"""
    parts = []
    for f in glob.glob(os.path.join(ROOT, 'inbox', '*', '*.json')) + glob.glob(os.path.join(ROOT, 'inbox', 'gemini', 'money', '*_verified*.json')):
        if exclude and exclude in open(f, encoding='utf-8').read(2000):
            continue  # 今確かめている回の前の結果は照合に使わない
        try:
            parts.append(open(f, encoding='utf-8').read())
        except OSError:
            pass
    for f in ['site/data/finds.js']:
        try:
            parts.append(open(os.path.join(ROOT, f), encoding='utf-8').read())
        except OSError:
            pass
    try:
        idx = open(os.path.join(ROOT, 'site', 'index.html'), encoding='utf-8').read()
        a, b = idx.find('/* UPDATES_START */'), idx.find('/* UPDATES_END */')
        if a >= 0 and b > a:
            parts.append(idx[a:b])
    except OSError:
        pass
    return norm('\n'.join(parts))


def is_dup(it, blob, self_json=None):
    """to の名前の近く(前後400字)に from の名前があり、同じ日付の月日 or 金額もあれば既存とみなす。"""
    frs, tos = parties(it)
    if not tos or not frs:
        return False, ''
    date = str(it.get('date') or '')
    dnorm = norm(date)
    av = amounts_in(str(it.get('amount') or ''))
    for t in tos:
        for m in re.finditer(re.escape(t), blob):
            win = blob[max(0, m.start() - 400): m.end() + 400]
            if any(f in win for f in frs):
                # 同じ組み合わせが近くにある。日付か金額の一部も合うなら重複と判断
                if dnorm and dnorm in win:
                    return True, '同じ組み合わせ・同じ日付が既にある'
                ds = re.search(r'(\d{4})-(\d{2})-(\d{2})', date)
                if ds and (ds.group(1) + ds.group(2) + ds.group(3)) in win:
                    return True, '同じ組み合わせ・同じ日付が既にある'
                if av and any(str(a)[:4] in win for a in av):
                    return True, '同じ組み合わせ・同じ金額が既にある'
                if MODE == 'moves':
                    return True, '同じ人・同じ移籍先が既にある'  # 引き抜きは同じ人の同じ移籍を二重に入れない
                return False, '同じ組み合わせが既にある(日付・金額は別)→新しい動きの可能性'
    return False, ''


def gemini_open(items, log=print):
    """クラウドから開けない出典を、Gemini の「URLを開く」機能(Google側で開く)で確かめる。1回の呼び出しにまとめる。
    開けたかは Gemini の自己申告ではなく、返ってくる取得結果(SUCCESS)で判断し、返ってきた本文の抜き出しを手元で同じ照合にかける。"""
    todo = []
    for it in items:
        for k in ('src_url', 'src_url2'):
            u = str(it.get(k) or '').strip()
            if u.startswith('http') and 'vertexaisearch' not in u and u not in todo and fetch(u)[0] != 'ok':
                todo.append(u)
    todo = todo[:24]
    if not todo:
        return {}
    out = {}
    for i in range(0, len(todo), 8):  # 1回8個まで(URLが二重に数えられ、20を超えると断られる)
        ok, why = quota_ok()
        if not ok:
            log('Gemini経由の確認を途中でやめた: ' + why)
            break
        out.update(_open_batch(todo[i:i + 8], log))
    log(f'Gemini経由で開けた出典: {len(out)}/{len(todo)}')
    return out


def _open_batch(urls, log):
    q = ('次の各URLを開き、ページの本文から「発表・公開の日付」と、お金に関する数字(金額)を含む文を原文のまま抜き出してください。'
         'ページが開けなかったURLは found を false にする。推測で書かない。\n'
         '答えはJSONだけ: ```json {"pages":[{"url":"","found":true,"date":"YYYY-MM-DD","text":"原文の抜き出し(会社名と金額を含む文を2〜5文)"}]} ```\n' + '\n'.join(urls))
    body = {'contents': [{'role': 'user', 'parts': [{'text': q}]}], 'tools': [{'url_context': {}}]}
    try:
        resp = gr.gen(body)
        note_call()
    except RuntimeError as e:
        note_call(blocked=' 429' in str(e))
        log('Gemini経由の確認に失敗: ' + str(e)[:150])
        return {}
    meta = {}
    for c in resp.get('candidates') or []:
        for m in (c.get('urlContextMetadata') or {}).get('urlMetadata') or []:
            u = m.get('retrievedUrl')
            meta[u] = meta.get(u, False) or 'SUCCESS' in str(m.get('urlRetrievalStatus', '')).upper()
    text = gr.resp_text(resp)
    m = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.S) or re.search(r'(\{.*\})', text, re.S)
    try:
        pages = json.loads(m.group(1)).get('pages') or [] if m else []
    except ValueError:
        pages = []
    out = {}
    for pg in pages:
        u = pg.get('url')
        if pg.get('found') and meta.get(u) and pg.get('text'):
            out[u] = {'text': str(pg['text']), 'dates': parse_dates(str(pg.get('date') or ''))}
    return out


def verify_item(it, days, blob, viaG=None):
    r = {'checks': {}, 'status': '合格', 'reasons': []}
    flags = []

    def bad(msg, hard=True):
        flags.append(('却下' if hard else '要確認', msg))

    # 必須項目
    if MODE == 'moves':
        if not ((it.get('name_ja') or it.get('name_en')) and it.get('to')):
            bad('本人の名前か移籍先が欠けている')
    elif not (it.get('from') and it.get('to')):
        bad('会社名が欠けている')
    if MODE != 'moves' and it.get('kind') not in KINDS:
        bad(f'種類が不正({it.get("kind")})', hard=False)
    cf = it.get('confidence')
    if cf not in CONF:
        it['confidence'] = '推定'

    # 日付
    cand_date = None
    ds = parse_dates(str(it.get('date') or ''))
    if ds:
        cand_date = ds[0]
    else:
        bad('日付がない・読めない', hard=False)
    if cand_date:
        if cand_date > datetime.date.today():
            bad(f'日付が未来({cand_date})')
        elif (datetime.date.today() - cand_date).days > days + 3:
            bad(f'日付が古い({cand_date}。{days}日より前)', hard=False)

    # 出典の確認
    srcs = []
    for k in ('src_url', 'src_url2'):
        u = str(it.get(k) or '').strip()
        if u.startswith('http'):
            srcs.append((it.get('src_name' if k == 'src_url' else 'src_name2') or u, u))
    r['sources'] = []
    if not srcs:
        bad('出典URLがない')
    ok_pages = 0
    names_ok = amt_ok = None
    date_state = '未確認'
    pnames = list(parties(it))[::1]
    pnames = [pnames[0], pnames[1]]
    for nm, u in srcs:
        st, final, raw = fetch(u)
        info = {'name': nm, 'url': u, 'state': st}
        via = (viaG or {}).get(u)
        if st != 'ok' and via:
            st, raw, info['state'] = 'ok', via['text'], 'Gemini経由で開けた'
            info['via_gemini'] = True
        if st == 'ok':
            text = raw if info.get('via_gemini') else html_text(raw)
            nt = norm(text)
            to_hit = any(v in nt for v in pnames[1])
            fr_hit = any(v in nt for v in pnames[0])
            amt, miss = amount_match(str(it.get('amount') or ''), amounts_in(text))
            pds, how = (via['dates'], 'Gemini経由') if info.get('via_gemini') else page_dates(raw, text)
            info.update({'to_name': to_hit, 'from_name': fr_hit, 'amount': amt, 'page_dates': [d.isoformat() for d in pds[:3]], 'date_from': how})
            if to_hit or fr_hit:
                ok_pages += 1
                names_ok = (names_ok or False) or (to_hit and fr_hit)
                if amt is not None:
                    amt_ok = (amt_ok or False) or amt
                if cand_date and pds:
                    close = any(abs((d - cand_date).days) <= 7 for d in pds)
                    date_state = '合う' if close else ('食い違い' if date_state != '合う' else date_state)
        r['sources'].append(info)
    if srcs and not ok_pages:
        bad('出典ページを開けない、または会社名が見つからない(Claudeが別の方法で確かめる)', hard=False)
    elif ok_pages:
        if not names_ok:
            bad('開いたページに、出す側と受け取る側の両方の名前は見つからない', hard=False)
        if amt_ok is False and any(s.get('amount') is False for s in r['sources']):
            bad('ページの数字と金額が合わない(ページに書いてある金額に一致なし)', hard=False)
        if date_state == '食い違い':
            bad('日付の食い違い(ページの日付とGeminiの日付が7日を超えて違う)', hard=False)
    r['checks'] = {'ページを開けた数': ok_pages, '名前': names_ok, '金額': amt_ok, '日付': date_state}

    # 重複
    dup, why = is_dup(it, blob)
    r['checks']['重複'] = '既存' if dup else ('近い既存あり' if why else 'なし')
    if dup:
        bad('すでにある: ' + why)
    elif why:
        r['reasons'].append(why)
    for sev, m in flags:
        r['reasons'].append(m)
    if any(s == '却下' for s, _ in flags):
        r['status'] = '却下'
    elif flags:
        r['status'] = '要確認'
    # 合格の条件: 出典ページを開けて、名前が合い、(金額があれば)金額も合い、日付が合うか確かめられない場合も食い違いはない
    if r['status'] == '合格' and not (ok_pages and names_ok):
        r['status'] = '要確認'
    return r


def verify(path=None, days=14, log=print, via=True):
    if not path:
        fs = sorted(glob.glob(os.path.join(OUT, prefix() + today() + '_raw*.json')))
        if not fs:
            log('今日の raw がない。先に search を実行')
            return None
        path = fs[-1]
    data = json.load(open(path, encoding='utf-8'))
    blob = existing_blob(exclude=os.path.relpath(path, ROOT))
    viaG = gemini_open(data.get('items', []), log) if via else {}
    res, seen = [], []
    for i, it in enumerate(data.get('items', []), 1):
        v = verify_item(it, days, blob, viaG)
        key = (norm(it.get('from')), norm(it.get('to')), str(it.get('date'))[:7])
        if key in seen:
            v['status'], v['reasons'] = '却下', v['reasons'] + ['同じ回の中で重複']
        seen.append(key)
        res.append({'no': i, 'item': it, 'verify': v})
    summ = {s: sum(1 for r in res if r['verify']['status'] == s) for s in ('合格', '要確認', '却下')}
    out = {'date': today(), 'source': os.path.relpath(path, ROOT), 'summary': summ, 'results': res}
    stem = os.path.basename(path).replace('_raw', '_verified').replace('.json', '')
    p = new_path(stem)
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    md = new_path(stem.replace('_verified', '_pass'), '.md')
    open(md, 'w', encoding='utf-8').write(to_md(out))
    log(f'確かめた結果: 合格 {summ["合格"]} / 要確認 {summ["要確認"]} / 却下 {summ["却下"]} → {os.path.relpath(md, ROOT)}')
    return p


def who(it):
    return it.get('name_ja') or it.get('from') or ''


def to_md(out):
    L = [f'# Gemini候補の機械チェック({out["date"]})', '',
         f'合格 {out["summary"]["合格"]} / 要確認 {out["summary"]["要確認"]} / 却下 {out["summary"]["却下"]}(元: {out["source"]})', '']
    L.append('## 合格(Claudeが読むのはここだけ)')
    for r in out['results']:
        if r['verify']['status'] != '合格':
            continue
        it, c = r['item'], r['verify']['checks']
        L += [f'- [{r["no"]}] {who(it)} → {it.get("to")} / {it.get("kind") or it.get("role") or ""} / {it.get("amount") or "金額なし"} / {it.get("date")} / {it.get("confidence")}',
              f'  - {it.get("note")}', f'  - 確認: 名前={c["名前"]} 金額={c["金額"]} 日付={c["日付"]} 重複={c["重複"]}']
        for s in r['verify']['sources']:
            L.append(f'  - 出典: {s["name"]} {s["url"]} [{s["state"]}]')
        for m in r['verify']['reasons']:
            L.append(f'  - 注意: {m}')
    L += ['', '## 要確認(開けない・合わない。必要なら上位3件だけ別の方法で確かめる)']
    for r in out['results']:
        if r['verify']['status'] == '要確認':
            it = r['item']
            L.append(f'- [{r["no"]}] {who(it)} → {it.get("to")} / {it.get("amount") or "-"} / {it.get("date")}: ' + ' / '.join(r['verify']['reasons']))
    L += ['', '## 却下(読まなくてよい)']
    for r in out['results']:
        if r['verify']['status'] == '却下':
            it = r['item']
            L.append(f'- [{r["no"]}] {who(it)} → {it.get("to")}: ' + ' / '.join(r['verify']['reasons']))
    return '\n'.join(L) + '\n'


# ---------- 3. 取り込み ----------
def emit(path=None, only=None, log=print):
    if not path:
        fs = sorted(glob.glob(os.path.join(OUT, prefix() + today() + '_verified*.json')))
        if not fs:
            log('今日の verified がない')
            return None
        path = fs[-1]
    data = json.load(open(path, encoding='utf-8'))
    items = []
    for r in data['results']:
        if r['verify']['status'] != '合格' or (only and r['no'] not in only):
            continue
        it = r['item']
        src = [[s['name'], s['url']] for s in r['verify']['sources'] if s['state'] == 'ok']
        note = (it.get('note') or '').strip()
        if MODE == 'moves':
            items.append({'name_en': it.get('name_en', ''), 'name_ja': it.get('name_ja', ''), 'from': it.get('from', ''),
                          'to': it['to'], 'role': it.get('role', ''), 'date': it.get('date', ''), 'note': note,
                          'src': src, 'confidence': it.get('confidence', '報道')})
        else:
            items.append({'from': it['from'], 'to': it['to'], 'kind': it['kind'], 'amount': it.get('amount', ''),
                          'date': it.get('date', ''), 'note': note, 'quote': '', 'video': '', 'src': src,
                          'confidence': it.get('confidence', '報道')})
    d = today()
    od = OUT_DIRS[MODE]
    p, i = os.path.join(od, f'{d}_gemini.json'), 1
    while os.path.exists(p):
        i += 1
        p = os.path.join(od, f'{d}_gemini-{i}.json')
    json.dump({'date': d, 'kind': MODE, 'items': items,
               'notes': f'Geminiが探し、プログラムが出典・金額・日付・重複を確かめた合格分({os.path.relpath(path, ROOT)})。'},
              open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f'{len(items)}件 → {os.path.relpath(p, ROOT)}')
    return p


def status():
    u = load_usage().get(today(), {})
    return {'GEMINI_API_KEY': 'あり' if gr.key() else 'なし', '今日の呼び出し': u.get('calls', 0),
            '上限': daily_limit(), '枠切れで停止中': bool(u.get('blocked'))}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    for n in ('run', 'search'):
        s = sp.add_parser(n); s.add_argument('--max', type=int, default=10); s.add_argument('--days', type=int, default=14)
        s.add_argument('--kind', choices=['money', 'moves'], default='money')
    v = sp.add_parser('verify'); v.add_argument('file', nargs='?'); v.add_argument('--days', type=int, default=14)
    v.add_argument('--kind', choices=['money', 'moves'], default='money')
    e = sp.add_parser('emit'); e.add_argument('file', nargs='?'); e.add_argument('--only')
    e.add_argument('--kind', choices=['money', 'moves'], default='money')
    sp.add_parser('status')
    a = ap.parse_args()
    global MODE
    MODE = getattr(a, 'kind', 'money')
    if a.cmd == 'status':
        print(json.dumps(status(), ensure_ascii=False, indent=1))
    elif a.cmd == 'search':
        search(a.max, a.days)
    elif a.cmd == 'verify':
        verify(a.file, a.days)
    elif a.cmd == 'emit':
        emit(a.file, {int(x) for x in a.only.split(',')} if a.only else None)
    else:
        p = search(a.max, a.days)
        if p:
            verify(p, a.days)


if __name__ == '__main__':
    main()
