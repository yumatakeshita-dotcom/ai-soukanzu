#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""決算資料・適時開示(IR)ウォッチ(2026/11/21追加)

日本(TDnet)・香港(HKEX)・シンガポール(SGX)の取引所の新着開示から、相関図にある会社の
「出資・買収・役員人事」に関する提出書類を拾い、PDFを実際に開いて確かめる。
確かめを通ったものだけ保存する。足すだけで、前の記録は消さない。

  inbox/ir/YYYY-MM-DD.json   確かめを通った開示(出資・買収・役員人事・資本提携)の記録
  inbox/ir/seen.txt          見たものの目録(2回拾わない)
  inbox/ir/status.json       取引所ごとの取得結果(読めなかった理由も入る。毎回上書き)
  inbox/ir/targets_extra.txt 見る会社の追加(日本・香港・シンガポール。1行1社、足すだけ)
  inbox/money/YYYY-MM-DD-ir.json  買収・出資のうち、表題から相手の名前が確実にとれたものだけ(自動)
                                  → 毎朝の merge_inbox.py が「調査の新着」と相関図に足す

役員人事は、人の名前を自動で取り違えると相関図が汚れるので、記録(inbox/ir/)にだけ残し、
inbox/moves/ に足すのは毎朝の調査(Claude)が本文を読んで名前を確かめてから行う。

確かめの内容(1件ごと。全部通ったものだけ保存):
  1. PDFが開ける(本文が取れる)
  2. 本文に、会社のコード(または会社名)が出てくる
  3. 本文の日付が、一覧の日付の前後(日本は7日・香港は7日)にある
  4. 本文にも、表題と同じ種類の言葉(出資・買収・取締役 など)がある
  5. (自動で相関図に足す場合)相手の名前が本文にも出てくる

使い方:
  python3 scripts/ir_watch.py                 # 直近3営業日ぶんを見る(毎朝)
  python3 scripts/ir_watch.py --days 7        # さかのぼる日数
  python3 scripts/ir_watch.py --dry           # 保存しない(試し)
  python3 scripts/ir_watch.py --only tdnet    # tdnet / hkex / sgx のどれかだけ
SGX は api.sgx.com / links.sgx.com が環境の許可に入っていないと読めない(読めないときは理由を status.json に残す)。
韓国DART・EDINET は今は読めないので対象外。
"""
import argparse, datetime, glob, json, os, re, subprocess, sys, tempfile, time, unicodedata, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'inbox', 'ir')
SEEN = os.path.join(OUT, 'seen.txt')
EXTRA = os.path.join(OUT, 'targets_extra.txt')
UA = 'Mozilla/5.0 (compatible; ai-soukanzu-ir-watch)'
JST = datetime.timezone(datetime.timedelta(hours=9))

# ---------- 種類の判定 ----------
# 表題の言葉 → 種類。上から順に見る。除外(自己株式・株式報酬など)にあたるものは拾わない
JP_EXCLUDE = re.compile(r'自己株式|自己投資口|譲渡制限付|株式報酬|持株会|ストック・?オプション|新株予約権の(行使|発行|割当)|取得価額|不動産|信託受益権|'
                        r'配当|業績予想|決算短信|決算説明|決算参考|実効性|公認会計士|会計監査人|株主優待|株主総会(招集|の開催)|定時株主総会|四半期|月次|訂正|'
                        r'払込完了|行使完了|消却|格付|社債|転換社債|売出し|コーポレート・ガバナンス|資金の借入|ToSTNeT')
JP_KINDS = [
    ('買収', re.compile(r'株式の取得|株式取得|子会社化|買収|公開買付|TOB|株式交換|吸収合併|事業譲受|事業の譲受|持分の取得|持分取得|連結子会社の異動|子会社の異動|経営統合')),
    ('出資', re.compile(r'出資|資本業務提携|資本提携|第三者割当|合弁|共同出資|ジョイント・?ベンチャー|ファンドへの')),
    ('役員人事', re.compile(r'代表取締役の異動|役員の異動|役員人事|社長交代|代表取締役.*(異動|交代|選定)|取締役.*(就任|退任|辞任|異動)|執行役員.*(人事|異動)|新任|CEO.*交代|人事異動|役員候補者|取締役候補者')),
]
JP_BODY_HINT = {'売却・異動': re.compile(r'譲渡|売却|異動'), '買収': re.compile(r'取得|買収|子会社|公開買付|合併|譲受'), '出資': re.compile(r'出資|提携|割当|合弁'),
                '役員人事': re.compile(r'取締役|執行役員|就任|退任|選定|異動')}
HK_CATS = re.compile(r'Discloseable Transaction|Major Transaction|Very Substantial|Connected Transaction|Takeovers Code|Change in Directors|'
                     r'Notifiable Transaction|Inside Information', re.I)
HK_KINDS = [
    ('役員人事', re.compile(r'Change in Directors|appointment|resignation|retirement|change of (chairman|director|chief)|cessation|director', re.I)),
    ('買収', re.compile(r'acquisition|acquire|disposal|takeover|offer|merger|privatisation|subscription of shares in', re.I)),
    ('出資', re.compile(r'investment|subscription|joint venture|capital injection|strategic cooperation|strategic investment|equity interest', re.I)),
]
HK_EXCLUDE = re.compile(r'share buyback|next day disclosure|proxy form|circular|results|dividend|date of board|notice of (agm|egm)|constitutional|'
                        r'monthly return|list of directors|share option|share scheme|remuneration|expected timetable', re.I)
SG_KINDS = HK_KINDS


# ---------- 道具 ----------
def nfkc(s):
    return unicodedata.normalize('NFKC', str(s or ''))


def clean_name(s):
    s = nfkc(s)
    s = re.sub(r'(株式会社|有限会社|合同会社|㈱|\(株\)|Inc\.?|Corp(oration)?\.?|Ltd\.?|Limited|Pte\.?|PTE\.?|LTD\.?|社$)', '', s)
    s = re.sub(r'^[\s　・「『(]+|[\s　・」』)]+$', '', s)
    return s.strip()


def http(url, timeout=40, binary=False, retries=2):
    last = None
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'ja,en;q=0.8'})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                b = r.read()
            return b if binary else b.decode('utf-8', 'replace')
        except Exception as e:  # noqa
            last = e
            time.sleep(1 + i * 2)
    raise last


def pdf_text(url):
    """PDFを落として本文を取る(pdftotext)。取れなければ ''"""
    try:
        b = http(url, timeout=60, binary=True)
    except Exception as e:  # noqa
        return '', f'PDFが開けない({str(e)[:60]})'
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'x.pdf')
        open(p, 'wb').write(b)
        try:
            t = subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, timeout=60).stdout.decode('utf-8', 'replace')
        except Exception as e:  # noqa
            return '', f'本文が取れない({str(e)[:60]})'
    return t, ''


def squash(t):
    """本文の空白をつめる(「会 社 名」のような字間の空白で名前が探せなくなるのを防ぐ)"""
    return re.sub(r'\s+', '', nfkc(t))


def load_targets():
    """見る会社。{市場: {コード: {name, aliases}}}"""
    T = {'JP': {}, 'HK': {}, 'SG': {}}
    p = os.path.join(ROOT, 'site', 'data', 'jpco.js')
    if os.path.exists(p):
        s = open(p, encoding='utf-8').read()
        arr = json.loads(s[s.index('=') + 1:].strip().rstrip(';'))
        for a in arr:
            if a.get('code'):
                T['JP'][nfkc(a['code'])] = {'name': a['name'], 'key': a.get('key', '')}
    if os.path.exists(EXTRA):
        for line in open(EXTRA, encoding='utf-8'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            f = line.split('\t')
            if len(f) < 3:
                f = re.split(r'\s+', line, maxsplit=2)
            if len(f) >= 3 and f[0] in T:
                T[f[0]].setdefault(nfkc(f[1]), {'name': f[2], 'key': ''})
    return T


def load_seen():
    return set(x.strip() for x in open(SEEN, encoding='utf-8')) if os.path.exists(SEEN) else set()


def kind_of(title, kinds, exclude):
    t = nfkc(title)
    if exclude and exclude.search(t):
        return ''
    if re.search(r'譲渡|売却|disposal', t, re.I) and not re.search(r'取得|買収|公開買付|子会社化|acqui|takeover|offer', t, re.I) and \
            re.search(r'子会社|事業|株式|持分|disposal', t, re.I):
        return '売却・異動'
    for k, rx in kinds:
        if rx.search(t):
            return k
    return ''


def first_dates(text, n=6):
    """本文の最初の方に出る日付(YYYY-MM-DD)を返す。日本語・英語・数字の形に対応"""
    t = nfkc(text[:4000])
    out = []
    for m in re.finditer(r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日', t):
        out.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    mon = {m: i + 1 for i, m in enumerate(['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'])}
    for m in re.finditer(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', t):
        mm = mon.get(m.group(2).lower())
        if mm:
            out.append((int(m.group(3)), mm, int(m.group(1))))
    ds = []
    for y, mo, d in out:
        try:
            ds.append(datetime.date(y, mo, d))
        except ValueError:
            pass
    return ds[:n]


def date_ok(text, day, window=7):
    ds = first_dates(text)
    return any(abs((d - day).days) <= window for d in ds)


def amount_near(text):
    """「取得価額」「譲渡価額」などの近くにある金額を拾う。なければ ''"""
    t = nfkc(text)
    m = re.search(r'(取得価額|取得価格|取得金額|譲渡価額|買付代金|買付け等の価格|払込金額の総額|発行総額|出資額|出資金額|投資額)[^0-9\n]{0,40}([0-9][0-9,\.]*)\s*(百万円|億円|千円|万円|円|百万米ドル|百万ドル|米ドル|ドル)',
                  t)
    if m:
        return f'{m.group(2)}{m.group(3)}(開示書類の「{m.group(1)}」)'
    return ''


def money_from_title(title, filer):
    """表題から (買った側, 買われた側, 種類) が確実にとれるものだけ返す。とれなければ None"""
    t = nfkc(title).strip()
    t = re.sub(r'^\（?\(?(開示事項の(経過|変更)|変更|訂正)\)?\）?\s*', '', t)
    t = re.sub(r'\((証券コード|コード)[:：]?\s*\w+\)', '', t)
    t = re.sub(r'^当社(による|が|の)\s*', '', t)
    m = re.match(r'^(?P<a>.+?)による(?P<t>.+?)(の株式|の株券等|株式|株券等)?(\(.*?\))?に対する(株券等に対する)?公開買付け', t)
    if m:
        a, tg = clean_name(m.group('a')), clean_name(m.group('t'))
        if tg in ('当社', '当社の'):
            tg = filer
        if a in ('当社', ''):
            a = filer
        tg = re.sub(r'\(証券コード[:：]?\w+\)', '', tg).strip()
        if a and tg and a != tg:
            return a, tg, '買収'
    m = re.match(r'^(?P<t>[^「」]+?)(の株式|の持分|の全株式|の発行済株式)(の)?(取得|譲受)\s*(\(.*?\))?', t)
    if m and not re.search(r'自己|当社株式|当社の株式', t):
        tg = clean_name(m.group('t'))
        if tg and tg not in ('当社', '子会社') and len(tg) <= 40:
            return filer, tg, '買収'
    m = re.match(r'^(?:(?:米国|英国|中国|欧州|国内|海外)\s*)?(?P<t>[^「」]+?)(社)?の(買収|完全子会社化|子会社化)(完了)?(について|に関する|を|に)', t)
    if m:
        tg = clean_name(m.group('t'))
        if tg and tg not in ('当社', '子会社') and len(tg) <= 40:
            return filer, tg, '買収'
    m = re.match(r'^(?P<p>[^「」]+?)との(資本業務提携|資本提携|出資に関する基本合意書の締結|合弁会社設立|合弁契約)', t)
    if m and re.search(r'出資|資本', t):
        p = clean_name(m.group('p'))
        if p and p not in ('当社',) and len(p) <= 40:
            return filer, p, '出資'
    return None


def ctx_snippet(text, kw, width=360):
    t = re.sub(r'[ \t　]+', ' ', text)
    t = re.sub(r'\n\s*\n+', '\n', t)
    i = t.find(kw) if kw else -1
    s = t[max(0, i - 40): i + width] if i >= 0 else t[:width + 40]
    return re.sub(r'\s+', ' ', s).strip()[:width]


# ---------- 取引所ごとの取得 ----------
def tdnet_rows(day):
    """TDnetのその日の一覧(全ページ)。[(時刻, コード5桁, 会社名, 表題, PDFの相対パス)]"""
    rows = []
    ymd = day.strftime('%Y%m%d')
    for p in range(1, 12):
        try:
            h = http(f'https://www.release.tdnet.info/inbs/I_list_{p:03d}_{ymd}.html', timeout=30, retries=1)
        except Exception:
            break
        got = 0
        for r in re.findall(r'<tr[^>]*>(.*?)</tr>', h, re.S):
            m = re.search(r'kjTime[^>]*>([^<]*)<.*?kjCode[^>]*>([^<]*)<.*?kjName[^>]*>([^<]*)<.*?kjTitle[^>]*>(.*?)</td>', r, re.S)
            if not m:
                continue
            a = re.search(r'href="([^"]+\.pdf)"[^>]*>(.*?)</a>', m.group(4), re.S)
            if not a:
                continue
            got += 1
            import html as _h
            rows.append((m.group(1).strip(), m.group(2).strip(), _h.unescape(m.group(3)).strip(),
                         _h.unescape(re.sub('<.*?>', '', a.group(2))).strip(), a.group(1)))
        if got == 0 or '次へ' not in h:
            break
    return rows


def run_tdnet(days, T, seen, status):
    out = []
    today = datetime.datetime.now(JST).date()
    n_rows = 0
    checked_days = []
    d = today
    while len(checked_days) < days and (today - d).days < days + 6:
        if d.weekday() < 5:
            checked_days.append(d)
        d -= datetime.timedelta(days=1)
    for day in checked_days:
        try:
            rows = tdnet_rows(day)
        except Exception as e:  # noqa
            status['tdnet'] = {'ok': False, 'why': str(e)[:100]}
            return out
        n_rows += len(rows)
        for tm, code5, name, title, pdf in rows:
            code = nfkc(code5)
            code = code[:-1] if len(code) == 5 and code.endswith('0') else code
            tg = T['JP'].get(code)
            if not tg:
                continue
            kind = kind_of(title, JP_KINDS, JP_EXCLUDE)
            if not kind:
                continue
            url = 'https://www.release.tdnet.info/inbs/' + pdf
            if 'TDNET|' + pdf in seen:
                continue
            out.append({'market': 'TDnet(日本)', 'tkey': 'TDNET|' + pdf, 'code': code, 'co': tg['name'], 'co_list': name, 'title': title,
                        'cat': kind, 'url': url, 'day': day, 'time': tm, 'key': tg.get('key', '')})
    status['tdnet'] = {'ok': True, 'rows': n_rows, 'days': [str(x) for x in checked_days]}
    return out


def run_hkex(T, seen, status):
    out = []
    try:
        d = json.loads(http('https://www.hkexnews.hk/ncms/json/eds/lcisehk1relsde_1.json', timeout=60))
    except Exception as e:  # noqa
        status['hkex'] = {'ok': False, 'why': str(e)[:100]}
        return out
    L = d.get('newsInfoLst') or []
    for x in L:
        for st in x.get('stock') or []:
            code = (st.get('sc') or '').lstrip('0').zfill(5)
            tg = T['HK'].get(code) or T['HK'].get(st.get('sc') or '')
            if not tg:
                continue
            blob = f"{x.get('sTxt','')} {x.get('title','')}"
            if HK_EXCLUDE.search(x.get('title', '')) or not (HK_CATS.search(blob) or kind_of(x.get('title', ''), HK_KINDS, None)):
                continue
            kind = kind_of(blob, HK_KINDS, None)
            if not kind:
                continue
            url = 'https://www.hkexnews.hk' + x['webPath']
            if 'HKEX|' + x['webPath'] in seen:
                continue
            m = re.match(r'(\d+)/(\d+)/(\d+)\s+(\d+):(\d+)', x.get('relTime', ''))
            day = datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else datetime.datetime.now(JST).date()
            out.append({'market': 'HKEX(香港)', 'tkey': 'HKEX|' + x['webPath'], 'code': code, 'co': tg['name'], 'co_list': st.get('sn', ''),
                        'title': x.get('title', ''), 'cat': kind, 'url': url, 'day': day, 'time': (m.group(4) + ':' + m.group(5)) if m else '', 'key': tg.get('key', ''),
                        'hk_cat': x.get('sTxt', '')})
    status['hkex'] = {'ok': True, 'rows': len(L)}
    return out


def run_sgx(days, T, seen, status):
    """SGXの会社発表。データの置き場(api.sgx.com)が許可されていないと読めない"""
    out = []
    end = datetime.datetime.now(JST)
    start = end - datetime.timedelta(days=days)
    fmt = lambda d: d.astimezone(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')
    url = f'https://api.sgx.com/announcements/v1.1/?periodstart={fmt(start)}&periodend={fmt(end)}&cat=ANNC&value=&exactsearch=true&pagestart=0&pagesize=200'
    try:
        d = json.loads(http(url, timeout=40, retries=1))
    except Exception as e:  # noqa
        status['sgx'] = {'ok': False, 'why': 'api.sgx.com に接続できない(環境の許可に api.sgx.com / links.sgx.com を足す必要がある): ' + str(e)[:80]}
        return out
    items = d.get('data') or d.get('items') or []
    for x in items:
        code = (x.get('issuer_code') or x.get('security_code') or x.get('code') or '').strip()
        tg = T['SG'].get(code)
        if not tg:
            continue
        title = x.get('title') or x.get('announcement_title') or ''
        kind = kind_of(title + ' ' + (x.get('category_name') or ''), SG_KINDS, HK_EXCLUDE)
        if not kind:
            continue
        link = x.get('url') or x.get('link') or ''
        if not link.startswith('http'):
            continue
        if 'SGX|' + link in seen:
            continue
        out.append({'market': 'SGX(シンガポール)', 'tkey': 'SGX|' + link, 'code': code, 'co': tg['name'], 'co_list': x.get('issuer_name', ''), 'title': title,
                    'cat': kind, 'url': link, 'day': end.date(), 'time': '', 'key': tg.get('key', '')})
    status['sgx'] = {'ok': True, 'rows': len(items)}
    return out


# ---------- 確かめ ----------
def verify(c):
    """候補を1件確かめる。(通ったか, 確かめの結果, 本文)"""
    text, err = pdf_text(c['url'])
    chk = {'PDFが開ける': bool(text and len(text) > 120)}
    if not chk['PDFが開ける']:
        return False, chk, err or '本文が短すぎる', ''
    sq = squash(text)
    code = c['code']
    name_stems = {clean_name(c['co']), clean_name(c['co_list'])}
    name_stems = {s for s in name_stems if len(s) >= 2}
    chk['会社を確認'] = bool(re.search(r'(コード番号|証券コード|Stock\s*code|stock code|コード)[^0-9A-Za-z]{0,12}' + re.escape(code.lstrip('0') if c['market'].startswith('HKEX') else code), sq, re.I)) or \
        any(squash(s) in sq for s in name_stems) or (code.lstrip('0') in sq and c['market'].startswith('HKEX') and len(code.lstrip('0')) >= 3)
    chk['日付が合う'] = date_ok(text, c['day'])
    if c['market'].startswith('TDnet'):
        chk['内容が合う'] = bool(JP_BODY_HINT[c['cat']].search(nfkc(text)))
    else:
        chk['内容が合う'] = bool(HK_KINDS[0][1].search(text) if c['cat'] == '役員人事' else re.search(r'dispos', text, re.I) if c['cat'] == '売却・異動' else (HK_KINDS[1][1].search(text) or HK_KINDS[2][1].search(text)))
    ok = all(chk.values())
    return ok, chk, '' if ok else '確かめで落ちた: ' + '、'.join(k for k, v in chk.items() if not v), text


def build_record(c, chk, text):
    rec = {'d': str(c['day']), 'time': c['time'], 'market': c['market'], 'code': c['code'], 'co': c['co'], 'key': c['key'],
           'title': c['title'], 'cat': c['cat'], 'url': c['url'], 'checks': chk, 'cf': '開示',
           'snippet': ctx_snippet(text, '異動の内容' if c['cat'] == '役員人事' else '')}
    deal = money_from_title(c['title'], clean_name(c['co'])) if c['market'].startswith('TDnet') and c['cat'] in ('買収', '出資') else None
    if deal:
        a, t, k = deal
        # 相手の名前が本文にも出てくるときだけ、自動で相関図に足す
        sq = squash(text)
        if squash(t) in sq or squash(clean_name(t)) in sq:
            rec['deal'] = {'from': a, 'to': t, 'kind': k, 'amount': amount_near(text)}
            rec['import'] = '自動(inbox/money)'
        else:
            rec['import'] = '手動(相手の名前が本文で確かめられなかった)'
    else:
        rec['import'] = '記録のみ(役員人事は名前を本文で確かめてから inbox/moves に足す)' if c['cat'] == '役員人事' else '手動(表題から相手が決められない)'
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=3)
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--only', choices=['tdnet', 'hkex', 'sgx'])
    ap.add_argument('--max', type=int, default=60, help='1回に開くPDFの上限')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    T = load_targets()
    seen = load_seen()
    status = {}
    cands = []
    if a.only in (None, 'tdnet'):
        cands += run_tdnet(a.days, T, seen, status)
    if a.only in (None, 'hkex'):
        cands += run_hkex(T, seen, status)
    if a.only in (None, 'sgx'):
        cands += run_sgx(a.days, T, seen, status)
    print('対象:', {k: len(v) for k, v in T.items()}, '/ 候補:', len(cands))
    recs, rejected, new_seen = [], [], []
    for c in cands[:a.max]:
        ok, chk, why, text = verify(c)
        new_seen.append(c['tkey'])
        if ok:
            recs.append(build_record(c, chk, text))
            print('○', c['market'], c['co'], c['cat'], c['title'][:50])
        else:
            rejected.append({'co': c['co'], 'title': c['title'], 'url': c['url'], 'why': why})
            print('×', c['market'], c['co'], c['title'][:40], '→', why)
        time.sleep(0.5)
    if len(cands) > a.max:
        print(f'上限 {a.max} 件で止めた。残り {len(cands) - a.max} 件は次の回')
    status['saved_at'] = datetime.datetime.now(JST).isoformat(timespec='seconds')
    status['n_candidates'] = len(cands)
    status['n_verified'] = len(recs)
    status['n_rejected'] = len(rejected)
    if a.dry:
        print(json.dumps(status, ensure_ascii=False))
        return
    today = datetime.datetime.now(JST).strftime('%Y-%m-%d')
    if recs:
        p = os.path.join(OUT, today + '.json')
        old = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'items': []}
        have = {x['url'] for x in old['items']}
        old['items'] += [r for r in recs if r['url'] not in have]
        old.update({'date': today, 'kind': 'ir', 'rejected': (old.get('rejected') or []) + rejected})
        json.dump(old, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        # 買収・出資(自動)は inbox/money に足す(merge_inbox.py が「調査の新着」と相関図に出す)
        money = []
        for r in recs:
            if r.get('deal'):
                dl = r['deal']
                money.append({'from': dl['from'], 'to': dl['to'], 'kind': dl['kind'], 'amount': dl['amount'], 'date': r['d'],
                              'region': {'TDnet(日本)': '日本', 'HKEX(香港)': '香港', 'SGX(シンガポール)': 'シンガポール'}.get(r['market'], ''),
                              'note': f"{r['co']}の適時開示「{r['title'][:60]}」で確認({r['market']}、{r['d']}。PDFを開いて会社・日付・内容を照合)。金額は開示書類にある場合のみ記載",
                              'src': [[f"{r['market']} {r['co']}の開示({r['d']})", r['url']]], 'confidence': '開示'})
        if money:
            mp = os.path.join(ROOT, 'inbox', 'money', today + '-ir.json')
            md = json.load(open(mp, encoding='utf-8')) if os.path.exists(mp) else {'date': today, 'kind': 'money', 'items': []}
            have = {i['src'][0][1] for i in md['items']}
            md['items'] += [m for m in money if m['src'][0][1] not in have]
            json.dump(md, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print('inbox/money に足した:', len(money))
    elif rejected:
        p = os.path.join(OUT, today + '.json')
        if not os.path.exists(p):
            json.dump({'date': today, 'kind': 'ir', 'items': [], 'rejected': rejected}, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(SEEN, 'a', encoding='utf-8') as w:
        for k in new_seen:
            w.write(k + '\n')
    json.dump(status, open(os.path.join(OUT, 'status.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(status, ensure_ascii=False))


if __name__ == '__main__':
    main()
