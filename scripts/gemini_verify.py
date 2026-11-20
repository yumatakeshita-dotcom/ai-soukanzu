# -*- coding: utf-8 -*-
"""Gemini調査の結果(inbox/gemini/日付.json)を、機械的に確かめる(2026/11/19)。

確かめること(1件ずつ):
  1. 出典URLにつながるか。ページが開けたら、会社名・相手の名前がページに書いてあるかも見る
     - クラウドからつながらないサイト(日本のニュースサイトの多く)は「未確認」と書く(作ったURLかどうかは分からないため)
  2. すでにある情報と重なっていないか(site/index.html・site/data/*.js・inbox/ のほかの調査と、URLや名前で照らす)
  3. 日付の食い違い: Gemini の日付と、URLの中の日付・ページに書かれた公開日・相関図にある同じ組み合わせの日付を比べる
  4. 確かさの印が出典の種類と合うか(例: 「公式」なのに報道サイトのURL → 「報道」に下げる)

判定:
  合格  … つながって中身も合い、重なりも日付の食い違いもない → 取り込み候補
          inbox/money/日付-gemini.json か inbox/moves/日付-gemini.json に足す
          (毎朝9:13の「調査の新着」の定期タスクが、ほかの調査と同じようにサイトに足す)
  保留  … ページにつながらず「未確認」。ほかは問題なし → inbox/gemini/ に残すだけ(人が見て決める)
  除外  … 重なり・ページが無い・中身が合わない・日付の食い違い・出典なし → inbox/gemini/ に理由を残すだけ

結果は inbox/gemini/日付_verified.json と .md に足す(同じ名前があれば -2 … を付ける。消さない・上書きしない)。
確かめた元のファイルは inbox/gemini/verified.txt に1行ずつ足す(2回確かめない)。

使い方:
  python3 scripts/gemini_verify.py                 # まだ確かめていない inbox/gemini/*.json を全部
  python3 scripts/gemini_verify.py inbox/gemini/2026-11-19.json [--no-net] [--dry-run]
    --no-net   … URLを開かない(全部「未確認」になる。試し用)
    --dry-run  … どこにも書かずに結果だけ表示する
"""
import argparse, datetime, glob, html, json, os, re, ssl, sys, unicodedata
import urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GDIR = os.path.join(ROOT, 'inbox', 'gemini')
DONE = os.path.join(GDIR, 'verified.txt')
JST = datetime.timezone(datetime.timedelta(hours=9))
UA = 'Mozilla/5.0 (compatible; ai-soukanzu-verify/1.0)'
DATE_TOL = 7        # 日付のずれを許す日数
WIN = 400           # 名前の近さを見る文字数(重なりの判定)
REDIRECT = re.compile(r'vertexaisearch\.cloud\.google\.com/grounding-api-redirect')
MOVE_REL = re.compile(r'移籍|就任|退任|辞任|引き抜|採用|入社|退社|任命|交代')
REL_WORDS = re.compile(r'買収|出資|調達|提携|契約|取引|投資|ラウンド|退任|辞任|就任|移籍|CEO|上場')


def today():
    return datetime.datetime.now(JST).date()


def norm(s):
    s = unicodedata.normalize('NFKC', str(s or '')).lower()
    return re.sub(r'[\s・,、.()()「」\-_/\'"’]+', '', s)


def split_names(s):
    out = []
    for x in re.split(r'[,、/・&]| and |および|ほか|他', str(s or '')):
        x = re.sub(r'[((].*?[))]', '', x).strip()
        if x and x not in ('不明', '未公表', '非公表') and len(norm(x)) >= 2:
            out.append(x)
    return out


# ---------- 1. URLにつながるか ----------
def _ctx():
    ca = os.environ.get('SSL_CERT_FILE') or os.environ.get('REQUESTS_CA_BUNDLE')
    return ssl.create_default_context(cafile=ca if ca and os.path.exists(ca) else None)


def fetch(url, timeout=25):
    """(状態, HTTPの番号, 本文, 最後に着いたURL) を返す。状態: ok / なし / 未確認"""
    host = (url.split('/')[2] if '//' in url else '').lower()
    ua = os.environ.get('SEC_UA') if host.endswith('sec.gov') and os.environ.get('SEC_UA') else UA
    req = urllib.request.Request(url, headers={'User-Agent': ua, 'Accept-Language': 'ja,en;q=0.8'})
    try:
        with urllib.request.urlopen(req, context=_ctx(), timeout=timeout) as r:
            body = r.read(2_000_000).decode(r.headers.get_content_charset() or 'utf-8', 'ignore')
            return 'ok', r.status, body, r.geturl()
    except urllib.error.HTTPError as e:
        final = e.geturl() if hasattr(e, 'geturl') else url
        if e.code in (404, 410):
            return 'なし', e.code, '', final
        return '未確認', e.code, '', final   # 401/403/429 など: サイトが自動の確認を断った
    except Exception as e:  # つながらない(クラウドの通信の制限・名前が引けない・時間切れ)
        return '未確認', 0, str(e)[:120], url


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def resolve_redirect(url, timeout=20):
    """Gemini の検索の転送リンクから、元の記事のURLを取り出す(開かずに行き先だけ読む)。わからなければ None"""
    op = urllib.request.build_opener(_NoRedirect, urllib.request.HTTPSHandler(context=_ctx()),
                                     urllib.request.ProxyHandler())
    try:
        op.open(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=timeout)
    except urllib.error.HTTPError as e:
        loc = e.headers.get('Location') if e.headers else None
        if e.code in (301, 302, 303, 307, 308) and loc and loc.startswith('http'):
            return loc
    except Exception:
        pass
    return None


def resolve_pool(grounding):
    """Gemini が検索で実際に見たページ(転送リンク)を、元のURLの一覧にする"""
    out = []
    for t, u in grounding or []:
        real = resolve_redirect(u) if REDIRECT.search(u or '') else u
        if real and real not in out:
            out.append(real)
    return out


_page_cache = {}


def fetch_cached(url):
    if url not in _page_cache:
        _page_cache[url] = fetch(url)
    return _page_cache[url]


def find_alt(names, pool):
    """Geminiが見たページのうち、会社名と相手(わかれば)の両方が書いてあるもの"""
    key = [n for n in names if len(norm(n)) >= 2]
    if not key:
        return None
    for u in pool:
        st, code, body, final = fetch_cached(u)
        if st != 'ok':
            continue
        txt = norm(page_text(body))
        if len(key) == 1:
            # 相手が「不明」で名前が1つだけのときは、まとめ記事に紛れるのを避けるため、ページの題名に名前があるものだけ
            m = re.search(r'<title[^>]*>(.*?)</title>', body, re.S | re.I)
            if m and norm(key[0]) in norm(html.unescape(m.group(1))):
                return final or u
        elif norm(key[0]) in txt and any(norm(n) in txt for n in key[1:]):
            return final or u
    return None


def page_text(body):
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', body, flags=re.S | re.I)
    return html.unescape(re.sub(r'<[^>]+>', ' ', t))


def page_dates(body):
    """ページに書かれた公開日(メタ情報)。見つかったものを全部返す"""
    pats = [r'(?:article:published_time|datePublished|pubdate|publish[_-]?date|date)"?\s*(?:content|:)\s*=?\s*"(\d{4}-\d{2}-\d{2})',
            r'<time[^>]+datetime="(\d{4}-\d{2}-\d{2})']
    out = []
    for p in pats:
        out += re.findall(p, body, flags=re.I)
    return sorted(set(out))[:5]


# ---------- 3. 日付 ----------
def parse_date(s):
    s = str(s or '').strip()
    for f, n in (('%Y-%m-%d', 10), ('%Y-%m', 7)):
        try:
            return datetime.datetime.strptime(s[:n], f).date()
        except ValueError:
            pass
    return None


def url_date(url):
    """URLの中の日付(/2026/11/12/ ・ 20261112 ・ /2611/14/ など)"""
    m = re.search(r'/(20\d{2})[/-](\d{1,2})[/-](\d{1,2})(?:/|-|$)', url)
    if m:
        y, mo, d = map(int, m.groups())
    else:
        m = re.search(r'(?<!\d)(20\d{2})(\d{2})(\d{2})(?!\d)', url)
        if m:
            y, mo, d = map(int, m.groups())
        else:
            m = re.search(r'/(\d{2})(\d{2})/(\d{2})/', url)  # EE Times Japan などの /2611/14/
            if not m:
                return None
            y, mo, d = 2000 + int(m.group(1)), int(m.group(2)), int(m.group(3))
    try:
        return datetime.date(y, mo, d)
    except ValueError:
        return None


# ---------- 4. 確かさの印 ----------
def url_cf(url, src_name, names):
    """出典の種類から決まる印(index.html の srcCf と同じ考え方)。f 開示 / o 公式 / s 本人 / r 報道"""
    h = (url.split('/')[2] if '//' in url else '').lower()
    t = str(src_name or '')
    if re.search(r'(^|\.)sec\.gov$|edinet|tdnet|hkexnews|^investors?\.|^ir\.', h) or re.search(r'有価証券|10-K|10-Q|8-K|決算短信', t):
        return 'f'
    if re.search(r'prnewswire\.com|businesswire\.com|globenewswire\.com|prtimes\.jp|^newsroom\.|^investor\.', h) or re.search(r'公式|プレスリリース|Press Release', t, re.I):
        return 'o'
    hn = norm(h.replace('www.', '').split('.')[0])
    if len(hn) >= 3 and any(hn and (hn in norm(n) or norm(n) in hn) for n in names if len(norm(n)) >= 3):
        return 'o'  # 会社自身のサイト(例: paloaltonetworks.com)
    if re.search(r'^(www\.)?(x\.com|twitter\.com|threads\.net|youtube\.com|youtu\.be)$', h) or re.search(r'linkedin\.com/(in|posts|pulse)/', url):
        return 's'
    return 'r'


CF2JA = {'f': '開示', 'o': '公式', 's': '本人の発言', 'r': '報道', 'e': '推定'}
JA2CF = {'開示': 'f', '公式': 'o', '本人の発言': 's', '本人': 's', '報道': 'r', '推定': 'e'}
RANK = {'f': 5, 'o': 4, 's': 3, 'r': 2, 'e': 1}


def check_cf(it, names):
    claimed = JA2CF.get(it.get('確かさ') or '', 'r')
    url = it.get('出典URL') or ''
    src_name = (it.get('src') or [['']])[0][0]
    by_url = url_cf(url, src_name, names)
    notes = []
    fixed = claimed
    if claimed == 'e':
        pass  # 推定はそのまま
    elif claimed in ('f', 'o', 's') and claimed != by_url and not (claimed == 'o' and by_url == 'f'):
        fixed = by_url
        notes.append(f'確かさ「{CF2JA[claimed]}」は出典の種類と合わないので「{CF2JA[by_url]}」にした')
    elif claimed == 'r' and RANK[by_url] > RANK['r']:
        fixed = by_url
        notes.append(f'出典が{CF2JA[by_url]}の種類なので「{CF2JA[by_url]}」にした')
    if fixed in ('o', 'f') and re.search(r'報道ベース|報道によると|とみられ', it.get('備考') or ''):
        notes.append('備考に「報道ベース」とある(金額などは報道の数字)')
    return CF2JA[fixed], notes


# ---------- 2. 重なり ----------
def load_corpus():
    files = [os.path.join(ROOT, 'site', 'index.html')] + sorted(glob.glob(os.path.join(ROOT, 'site', 'data', '*.js')))
    for k in ['moves', 'money', 'vc', 'world', 'deep']:
        files += sorted(glob.glob(os.path.join(ROOT, 'inbox', k, '*.json')))
    raw, nrm = [], []
    for f in files:
        try:
            s = open(f, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        raw.append(s)
        nrm.append((os.path.relpath(f, ROOT), norm(s)))
    return '\n'.join(raw), nrm


def find_near(nrm, a, b, win=WIN):
    """a と b が近くに書いてある場所を返す(最初の1つ)。[(ファイル, 近くの文字)]"""
    na, nb = norm(a), norm(b)
    if len(na) < 2 or len(nb) < 2:
        return None
    for f, s in nrm:
        i = s.find(na)
        n = 0
        while i >= 0 and n < 300:
            seg = s[max(0, i - win):i + win]
            if nb in seg:
                return f, seg
            i = s.find(na, i + 1)
            n += 1
    return None


def seg_dates(seg):
    """正規化した文字(「-」が消えて 20261112 になる)から日付を拾う"""
    out = []
    for y, m, d in re.findall(r'(?<!\d)(20[12]\d)(\d{2})(\d{2})(?!\d)', seg):
        try:
            out.append(datetime.date(int(y), int(m), int(d)))
        except ValueError:
            pass
    return out


# 関係の言い換え(Gemini の書き方と、相関図の書き方の違いを吸収する)
REL_SYN = [
    (r'買収', ['買収', 'acqui', '取得', '傘下']),
    (r'出資|調達|投資|ラウンド', ['出資', '調達', '投資', 'invest', 'ラウンド', 'raise', 'シリーズ']),
    (r'退任|辞任|退社', ['退任', '辞任', 'resign', '退く', 'stepdown', '退社']),
    (r'就任|任命|交代', ['就任', '任命', 'appoint', '暫定', 'ceoに']),
    (r'移籍|引き抜|入社|採用', ['移籍', '加わ', 'join', '入社', '引き抜']),
    (r'提携|契約|取引', ['提携', '契約', 'partner', '取引', 'deal']),
    (r'IPO|上場', ['上場', 'ipo']),
]


def rel_words(rel):
    out = []
    for pat, ws in REL_SYN:
        if re.search(pat, rel or '', re.I):
            out += ws
    return [norm(w) for w in out]


def check_dup(it, raw, nrm):
    """(重なりの説明 or None, 近くで見つかった日付の一覧)"""
    url = (it.get('出典URL') or '').strip()
    if url and url in raw:
        return '同じ出典URLがすでにある', None
    a = it.get('会社名') or ''
    bs = split_names(it.get('相手')) + split_names(it.get('人物')) + split_names(it.get('人物_ja'))
    d = parse_date(it.get('日付'))
    rw = rel_words(it.get('関係'))
    seen_dates = []
    # (1) 会社名と相手が近くに書いてあり、近い日付か同じ種類の関係の言葉もある
    for b in bs:
        hit = find_near(nrm, a, b)
        if not hit:
            continue
        f, seg = hit
        ds = seg_dates(seg)
        seen_dates += ds
        if any(d and abs((x - d).days) <= 31 for x in ds):
            return f'「{a}」と「{b}」の組み合わせがすでにある({f}、近い日付あり)', ds
        close = find_near(nrm, a, b, 120)  # 日付が無いときは、すぐ近くに同じ種類の関係の言葉があるときだけ
        if close and any(w in close[1] for w in rw):
            return f'「{a}」と「{b}」の組み合わせがすでにある({close[0]})', ds
    # (2) 会社名の近くに、同じ日付(前後2日)と同じ種類の関係の言葉がある(人の名前が日本語で書かれている場合など)
    na = norm(a)
    if d and rw and len(na) >= 4:  # AMD のような短い名前は、関係ないところにも出てくるので使わない
        for f, s in nrm:
            i, n = s.find(na), 0
            while i >= 0 and n < 2000:
                seg = s[max(0, i - 150):i + 150]
                if any(abs((x - d).days) <= 2 for x in seg_dates(seg)) and any(w in seg for w in rw):
                    return f'「{a}」の同じころ({d})の同じ種類の出来事がすでにある({f})', seen_dates
                i, n = s.find(na, i + 1), n + 1
    return None, seen_dates


# ---------- 1件を確かめる ----------
def verify_item(it, raw, nrm, net=True, pool=None):
    names = [it.get('会社名') or ''] + split_names(it.get('相手')) + split_names(it.get('人物'))
    r = {'item': it, 'checks': {}, 'notes': []}
    url = (it.get('出典URL') or '').strip()
    if not url.startswith('http'):
        r['verdict'] = '除外'; r['notes'].append('出典URLがない'); return r
    # 1. つながるか
    def use_url(new_url, why):
        nonlocal it, url
        it = dict(it, 出典URL=new_url, Geminiが書いたURL=it.get('Geminiが書いたURL') or url)
        it['src'] = [[new_url.split('/')[2], new_url]]
        r['item'] = it
        url = new_url
        r['notes'].append(why)
    if net and REDIRECT.search(url):
        # Gemini の検索の転送リンク(2026/11/19): 元の記事のURLに置き換える
        real = resolve_redirect(url)
        if real:
            use_url(real, 'Geminiの転送リンクを元の記事のURLに置き換えた')
    st, code, body, final = fetch_cached(url) if net else ('未確認', 0, 'つながりを確かめていない(--no-net)', url)
    if st == 'ok':
        txt0 = norm(page_text(body))
        if not any(len(norm(n)) >= 2 and norm(n) in txt0 for n in names):
            st = 'ok_nomatch'
    if net and pool and (st in ('なし', 'ok_nomatch') or REDIRECT.search(url)):
        # Geminiが書いたURLが開けない・中身が違う → Geminiが検索で実際に見たページから、同じ名前が書いてあるものを探す
        alt = find_alt(names, pool)
        if alt and alt != url:
            why = {'なし': 'ページが無い', 'ok_nomatch': '中身が違う'}.get(st, '開けない')
            use_url(alt, f'Geminiが書いたURLは{why}ため、Geminiが検索で実際に見たページに置き換えた')
            st, code, body, final = fetch_cached(url)
    if st == 'ok_nomatch':
        st = 'ok'
    if REDIRECT.search(url):
        st = '未確認'
        r['notes'].append('Geminiの転送リンクで、元の記事のURLにたどり着けない')
    r['checks']['url'] = {'state': st, 'code': code, 'final': final}
    pdates = []
    if st == 'ok':
        txt = norm(page_text(body))
        hits = [n for n in names if len(norm(n)) >= 2 and norm(n) in txt]
        r['checks']['url']['names_on_page'] = hits
        if not hits:
            st = '中身が合わない'
            r['notes'].append('ページは開けたが、会社名・相手の名前が書かれていない')
        pdates = page_dates(body)
    elif st == 'なし':
        r['notes'].append(f'ページが無い(HTTP {code})')
    else:
        r['notes'].append('未確認: クラウドから出典のページにつながらない' + (f'(HTTP {code})' if code else '') + '。人が開いて確かめる')
    # 2. 重なり
    dup, ex_dates = check_dup(it, raw, nrm)
    if dup:
        r['notes'].append('重なり: ' + dup)
    r['checks']['dup'] = dup or ''
    # 3. 日付
    d = parse_date(it.get('日付'))
    probs = []
    if not d:
        probs.append('日付が読めない')
    else:
        if d > today() + datetime.timedelta(days=1):
            probs.append('日付が未来')
        ud = url_date(url)
        if ud and abs((ud - d).days) > DATE_TOL:
            probs.append(f'URLの中の日付({ud})と{abs((ud - d).days)}日ずれる')
        for pd in pdates:
            p = parse_date(pd)
            if p and abs((p - d).days) > DATE_TOL and abs((p - d).days) < 4000:
                probs.append(f'ページの公開日({pd})と{abs((p - d).days)}日ずれる')
                break
        if ex_dates and not dup:
            far = [x for x in ex_dates if abs((x - d).days) > 31]
            if far and len(far) == len(ex_dates):
                probs.append(f'相関図の同じ組み合わせの日付({far[0]})と違う(別の出来事かもしれない)')
    r['checks']['date'] = probs
    hard_date = [p for p in probs if not p.startswith('相関図の')]
    r['notes'] += ['日付: ' + p for p in probs]
    # 4. 確かさ
    cf, cnotes = check_cf(it, names)
    r['checks']['cf'] = {'claimed': it.get('確かさ') or '', 'fixed': cf}
    r['notes'] += cnotes
    # 判定
    if dup or st in ('なし', '中身が合わない') or hard_date:
        r['verdict'] = '除外'
    elif st == 'ok':
        r['verdict'] = '合格'
    else:
        r['verdict'] = '保留'
    r['confidence'] = cf
    return r


# ---------- 合格したものを、ほかの調査と同じ形にする ----------
def to_inbox(r):
    it = r['item']
    src = it.get('src') or [[it.get('出典名') or it['出典URL'], it['出典URL']]]
    note = (it.get('備考') or '')[:80] + '(Gemini調査・自動の確かめを通過)'
    rel = it.get('関係') or ''
    if MOVE_REL.search(rel):
        person = it.get('人物') or (split_names(it.get('相手')) or [''])[0]
        out = '退任' in rel or '辞任' in rel or '退社' in rel
        return 'moves', {
            'name_en': person, 'name_ja': it.get('人物_ja') or '',
            'from': it.get('移籍元') or (it.get('会社名') if out else ''),
            'to': it.get('移籍先') or ('' if out else it.get('会社名') or ''),
            'role': it.get('役職') or '', 'date': it.get('日付') or '',
            'note': note, 'src': src, 'confidence': r['confidence'], 'via': 'gemini'}
    fr, to = it.get('会社名') or '', it.get('相手') or ''
    if re.search(r'調達', rel) or not split_names(to):
        # 「資金調達」や相手が「不明」のときは、会社名がお金を受け取る側(出した側は相手。不明なら空)
        fr, to = ('' if not split_names(to) else to), it.get('会社名') or ''
    return 'money', {
        'from': fr, 'to': to, 'kind': rel,
        'amount': it.get('金額') or '', 'date': it.get('日付') or '', 'note': note,
        'quote': '', 'video': '', 'src': src, 'confidence': r['confidence'], 'via': 'gemini'}


def new_path(base, ext):
    p, i = base, 1
    while os.path.exists(p + ext):
        i += 1
        p = f'{base}-{i}'
    return p + ext


def to_md(src_rel, res):
    cnt = {v: sum(1 for r in res if r['verdict'] == v) for v in ('合格', '保留', '除外')}
    L = [f'# Gemini調査の確かめ({today()})', '',
         f'- 元のファイル: {src_rel}',
         f'- 合格 {cnt["合格"]}件(取り込み候補) / 保留 {cnt["保留"]}件(未確認) / 除外 {cnt["除外"]}件', '',
         '| 判定 | 会社名 | 関係 | 相手 | 日付 | 確かさ | 出典 | 理由・メモ |', '|---|---|---|---|---|---|---|---|']
    for r in res:
        it = r['item']
        cells = [r['verdict'], it.get('会社名'), it.get('関係'), it.get('相手') or it.get('人物'), it.get('日付'),
                 r.get('confidence', ''), it.get('出典URL'), ' / '.join(r['notes']) or '問題なし']
        L.append('| ' + ' | '.join(str(c or '').replace('|', '/').replace('\n', ' ') for c in cells) + ' |')
    L += ['', '合格したものは inbox/money/ か inbox/moves/ の「日付-gemini.json」に足しました。毎朝9:13の「調査の新着」でサイトに出ます。',
          '保留(未確認)は、出典のページをクラウドから開けなかったものです。人が開いて確かめてください。']
    return '\n'.join(L) + '\n'


def done_set():
    return set(open(DONE, encoding='utf-8').read().split()) if os.path.exists(DONE) else set()


def targets():
    done = done_set()
    out = []
    for f in sorted(glob.glob(os.path.join(GDIR, '*.json'))):
        b = os.path.basename(f)
        if '_verified' in b or b == 'store.json':
            continue
        if os.path.relpath(f, ROOT) not in done:
            out.append(f)
    return out


def run(files, net=True, dry=False, log=print):
    raw, nrm = load_corpus()
    summary = []
    for f in files:
        rel = os.path.relpath(f, ROOT)
        d = json.load(open(f, encoding='utf-8'))
        pool = resolve_pool(d.get('grounding_resolved') or d.get('grounding')) if net else []
        if d.get('grounding_resolved'):
            pool = list(dict.fromkeys(d['grounding_resolved'] + pool))
        res = [verify_item(it, raw, nrm, net, pool) for it in d.get('items') or [] if isinstance(it, dict)]
        ok = [r for r in res if r['verdict'] == '合格']
        md = to_md(rel, res)
        if dry:
            log(md)
        else:
            base = os.path.splitext(f)[0] + '_verified'
            pj = new_path(base, '.json')
            json.dump({'date': str(today()), 'source': rel, 'results': res}, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            open(pj[:-5] + '.md', 'w', encoding='utf-8').write(md)
            by = {}
            for r in ok:
                k, row = to_inbox(r)
                by.setdefault(k, []).append(row)
            for k, rows in by.items():
                p = new_path(os.path.join(ROOT, 'inbox', k, f'{today()}-gemini'), '.json')
                json.dump({'date': str(today()), 'kind': k, 'items': rows,
                           'notes': f'Gemini調査({rel})のうち、scripts/gemini_verify.py の確かめを通ったもの'},
                          open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
                log(f'取り込み候補 {len(rows)}件 → {os.path.relpath(p, ROOT)}')
            with open(DONE, 'a', encoding='utf-8') as w:
                w.write(rel + '\n')
            log(f'{rel}: 合格 {len(ok)} / 保留 {sum(r["verdict"]=="保留" for r in res)} / 除外 {sum(r["verdict"]=="除外" for r in res)} → {os.path.relpath(pj, ROOT)}')
        summary.append({'file': rel, 'results': res})
    if not files:
        log('確かめる新しいファイルはありません')
    return summary


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('files', nargs='*')
    ap.add_argument('--no-net', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    files = [os.path.abspath(f) for f in a.files] or targets()
    run(files, net=not a.no_net, dry=a.dry_run)


if __name__ == '__main__':
    main()
