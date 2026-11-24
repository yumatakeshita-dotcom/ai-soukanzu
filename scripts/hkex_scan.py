#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HKEX(香港)の出資・買収・提携の発表を、本文で確かめたものだけ自動で足す(2026/11/24追加)

ir_watch.py は相関図にある会社だけを見て、記録するだけ(inbox/money には足さない)。
こちらは HKEX の新着一覧(英語、約1日ぶん×2ファイル)を全社ぶん見て、AIに関係する
出資・買収・提携の発表を、TDnet(tdnet_scan.py)と同じ考え方で扱う。足すだけで、消さない。

自動で inbox/money に足す条件(どれか1つでも欠けたら足さず、記録だけ。理由つき):
  1. PDFが開け、本文に証券コード(Stock code / HKEX: 番号)がある
  2. 本文の日付が一覧の日付に近い(前後7日)
  3. 表題から「だれに・どんな形で」が決まる(「INVESTMENT IN ○○」「ACQUISITION OF …… IN ○○」
     「COOPERATION AGREEMENT WITH ○○」など。「処分(DISPOSAL)」は向きが逆なので扱わない)
  4. 相手の名前が本文に2回以上出てくる(表題の名前を、本文の書き方に直して使う)
  5. 本文にAI企業名(OpenAI・DeepSeek・Nvidia など)が1つ以上、またはAI系の語(AI・GPU・data centre・
     large language model・semiconductor など)が3回以上ある
  6. 出す側の会社の名前が本文の先頭から読める(相関図の会社なら相関図の名前を使う)
  足す先: inbox/money/日付-hkex.json(出典は開示のPDF、confidence は「開示」)。相関図への取り込みは merge_inbox.py(毎朝9:13)。
  記録: inbox/ir/hkex-scan-日付.json(items=本文で確かめたもの、skipped=AIに関係なかった等)

PDFが開けなかったものは、ir_watch.py と同じ再確認の列(inbox/ir/retry.json)に入れる(翌日から最大3回)。
ir_watch.py の最後に自動で動く(毎朝の引き抜き調査が ir_watch.py を動かすので、定期タスクの変更は要らない)。

使い方:
  python3 scripts/hkex_scan.py --dry          # 書き込まずに確かめる
  python3 scripts/hkex_scan.py --days 5 --max 40
"""
import argparse, datetime, json, os, re, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ir_watch as W
import mou_followup as MF

FEEDS = ['https://www.hkexnews.hk/ncms/json/eds/lcisehk1relsde_1.json',
         'https://www.hkexnews.hk/ncms/json/eds/lcisehk1relsde_2.json']
# 開く候補にする表題・分類の言葉(ここでは開かない。表題と分類だけで決める)
HK_WANT = re.compile(r'acqui|invest|subscri|joint venture|cooperat|partnership|capital injection|strategic|framework agreement|memorandum of understanding|collaborat|equity interest|\bMOU\b', re.I)
# 向きが逆・関係ないもの(処分・金融・リース・配当・株式の発行や買い戻しなど)
HK_NOT = re.compile(r'dispos|financial assistance|finance lease|sale and leaseback|placing|rights issue|open offer|share buyback|repurchase|continuing connected|renewal|'
                    r'notes?\b|bonds?|loan|deposit|banking facilit|EPC|vessel|property management|appointment of|independent financial adviser|general mandate|'
                    r'scheme of arrangement|trading halt|resumption|profit warning|acquisition of shares by|acquisition of (?:the )?shares of the company', re.I)
# 覚書(MOU)を入れた会社の発表は、契約・完了・失効の表題なら、HK_WANT に当たらなくても開く(mou_followup.py)
FOLLOW_TITLE = re.compile(r'agreement|completion|terminat|lapse|supplemental|update|further announcement', re.I)
# 本文の「AIらしさ」
AI_CO_EN = re.compile(r'OpenAI|Anthropic|DeepSeek|NVIDIA|Moonshot|Zhipu|Z\.ai|MiniMax|Baichuan|StepFun|Mistral|xAI|Perplexity|Cohere|Cambricon|Moore Threads|MetaX|Biren|Enflame|Sakana', re.I)
AI_WORD_EN = re.compile(r'artificial intelligence|\bAI\b|\bAIGC\b|large (?:language )?models?|\bLLMs?\b|\bGPUs?\b|data cent(?:re|er)s?|semiconductor|computing power|intelligent computing|machine learning|deep learning|humanoid|embodied intelligence', re.I)
# 表題から相手を読む形(上から順に見る)。x は相手の名前(大文字のことが多い)
TITLE_FORMS = [
    (re.compile(r'(?:FUND(?:\W*S)?\W+)?INVESTMENT\s+IN\s+(?P<x>.+)$', re.I), '出資'),
    (re.compile(r'SUBSCRIPTION\s+OF\s+(?:NEW\s+)?[\w%\. ]{0,60}?\bIN\s+(?P<x>.+)$', re.I), '出資'),
    (re.compile(r'CAPITAL\s+INJECTION\s+(?:INTO|IN)\s+(?P<x>.+)$', re.I), '出資'),
    (re.compile(r'ACQUISITION\s+OF\s+[\w%\. ,]{0,80}?\bIN\s+(?P<x>.+)$', re.I), '買収'),
    (re.compile(r'ACQUISITION\s+OF\s+(?:A\s+)?(?:[\d\.]+%\s+)?(?:THE\s+)?(?!.*\bSHARES?\b)(?P<x>[A-Z][\w&\.\-\' ]{2,60})$', re.I), '買収'),
    (re.compile(r'(?:STRATEGIC\s+)?(?:COOPERATION|PARTNERSHIP|COLLABORATION|FRAMEWORK)\s+AGREEMENT\s+WITH\s+(?P<x>.+)$', re.I), '提携'),
    (re.compile(r'MEMORANDUM\s+OF\s+UNDERSTANDING\s+WITH\s+(?P<x>.+)$', re.I), '提携'),
]
NOT_CO = re.compile(r'\b(PRODUCTS?|SECURITIES|NOTES|BONDS|DEPOSITS?|WEALTH|PROPERTY|PROPERTIES|LAND|ASSETS?|PORTFOLIO|FINANCIAL|ARRANGEMENTS?|TARGET|SUBJECT)\b', re.I)
GENERIC_X = re.compile(r'\b(TARGET|SUBSIDIARY|SUBSIDIARIES|COMPANY|VENDOR|PURCHASER|SUBSCRIBER|PARTY|PARTIES|GROUP|PROPERTY|PROPERTIES|FUND|THE|A|AN|AGREEMENT|TRANSACTION|SHARES|EQUITY|INTEREST|PROJECT)\b', re.I)


def norm_title(t):
    return re.sub(r'\s+', ' ', t or '').strip()


def x_from_title(title):
    """表題から (相手の名前[大文字のまま], 種類) を返す。決まらなければ (None, 理由)"""
    t = norm_title(title)
    t = re.sub(r'^(?:VOLUNTARY\s+ANNOUNCEMENT|ANNOUNCEMENT|JOINT\s+ANNOUNCEMENT)\s*[-:–]?\s*', '', t, flags=re.I)
    for rx, kind in TITLE_FORMS:
        m = rx.search(t)
        if not m:
            continue
        x = m.group('x').strip(" .,;:-–")
        x = re.split(r'\s+(?:AND|AS|PURSUANT|UNDER|THROUGH|BY|FOR|TO)\s+|[,;(（]|\s+[-–]\s+', x, maxsplit=1)[0].strip()
        x = re.sub(r'^(?:THE|A|AN)\s+', '', x, flags=re.I)
        for _ in range(3):
            x = re.sub(r'[\s,]+(?:CO\.?|LTD\.?|LIMITED|INC\.?|CORP\.?|CORPORATION|LLC)$', '', x, flags=re.I).strip(' .,')
        words = x.split()
        if not (1 <= len(words) <= 6) or len(x) < 3 or len(x) > 60 or re.match(r'\d', x) or GENERIC_X.search(re.sub(r"[^\w ]", '', x)) and len(words) <= 2:
            return None, f'表題から読んだ「{x}」が会社名として決められない'
        if NOT_CO.search(x):
            return None, f'表題から読んだ「{x}」は会社名ではない(商品・資産・Target Company など)'
        return x, kind
    return None, '表題から相手が決められない'


LABEL_RX = re.compile(r'^(?:THE\s+)?TARGET(?:\s+(?:COMPANY|GROUP|ENTITY))?$', re.I)
CO_WORD = re.compile(r'\b(?:Co\.?|Ltd\.?|Limited|Inc\.?|Corp\.?|Corporation|Company|Group|Holdings?|Technolog(?:y|ies)|Intelligence|AI|Cloud|Network|Partnership)\b', re.I)


def raw_title_x(title):
    """表題の形に合う相手の言葉を、会社名かどうかを見ずにそのまま返す(「Target Company」のような呼び名も含む)。合わなければ (None, None)"""
    t = norm_title(title)
    t = re.sub(r'^(?:VOLUNTARY\s+ANNOUNCEMENT|ANNOUNCEMENT|JOINT\s+ANNOUNCEMENT)\s*[-:–]?\s*', '', t, flags=re.I)
    for rx, kind in TITLE_FORMS:
        m = rx.search(t)
        if m:
            return re.sub(r'^(?:THE|A|AN)\s+', '', m.group('x').strip(" .,;:-–"), flags=re.I), kind
    return None, None


def resolve_label(label, text):
    """表題が「Target Company」のような呼び名のとき、本文の定義(Definitions の表、または「名前 (the “Target Company”)」)から会社名を読む。
    決まらなければ (None, 理由)。呼び名は本文に3回以上出てくること・定義が1つに決まること・名前が会社名らしいことを条件にする"""
    lab = re.sub(r'^(?:the\s+)?', '', label.strip(), flags=re.I)
    lab_rx = r'\s+'.join(re.escape(w) for w in lab.split())
    if len(re.findall(lab_rx, text, re.I)) < 3:
        return None, f'呼び名「{lab}」が本文に3回以上出てこない'
    cands = set()
    # (a) 定義の表: “Target Company”   (名前 ……)   の次の空行まで
    for m in re.finditer(r'[“"]' + lab_rx + r'[”"]\s+(?:means\s+)?(?P<n>[^\n]+(?:\n[ \t]+[^\n]+)*)', text, re.I):
        n = ' '.join(m.group('n').split())
        n = re.split(r'\s+(?:being|which|who|as defined|holding)\b', n, maxsplit=1)[0]
        cands.add(n.strip())
    # (b) 本文中: 名前 (the “Target Company”)
    for m in re.finditer(r'(?P<n>[A-Z][\w&\.,\-\' ]{4,90}?)\s*[（(]\s*(?:the\s+)?[“"]' + lab_rx + r'[”"]\s*[)）]', text, re.I):
        cands.add(' '.join(m.group('n').split()))
    names = set()
    for n in cands:
        n = re.sub(r'^[\s(（]+|[\s)）]+$', '', n).rstrip('*').strip(' .,;')
        if 2 <= len(n.split()) <= 8 and len(n) <= 90 and n[0].isupper() and CO_WORD.search(n) and not re.search(r'\b(?:a|an|the)\s+(?:company|limited|partnership)\b|incorporated|established', n, re.I):
            names.add(re.sub(r'\s+', ' ', n))
    if len(names) != 1:
        return None, ('本文に「' + lab + '」の定義が見つからない' if not names else f'「{lab}」の定義が複数あって1つに決められない')
    return names.pop(), ''


def in_body(x, text):
    """表題の名前(大文字)を、本文の書き方(DeepSeek など)で探す。(本文での書き方, 出てきた回数)。大文字小文字・空白は無視する"""
    words = [re.escape(w) for w in x.split()]
    rx = re.compile(r'\s+'.join(words), re.I)
    ms = list(rx.finditer(text))
    if not ms:
        return None, 0
    forms = [m.group(0) for m in ms if not m.group(0).isupper()]
    return (forms[0] if forms else ms[0].group(0).title()), len(ms)


def filer_en(text, fallback):
    """出す側の会社名(英語)。本文の先頭の注意書きのあと、「(Incorporated…」「(Stock code…」の前にある名前"""
    m = re.search(r'contents\s+of\s+this\s+announcement\.\s*(.{3,200}?)\(\s*(?:incorporated|stock\s*code|a\s+company|the\s+company|nyse|hkex)', text[:2500], re.I | re.S)
    if m:
        name = ' '.join(m.group(1).split())
        if 3 <= len(name) <= 80 and not re.search(r'announcement|joint|circular', name, re.I):
            return name
    return fallback


def en_clean(name):
    """英語の社名から Limited・Co., Ltd. などを外し、全部大文字なら先頭だけ大文字にする"""
    n = re.sub(r'\s+', ' ', name).strip(' ,.')
    if n.isupper():
        n = n.title()
    for _ in range(3):
        n = re.sub(r'[,\s]+(?:Co\.?,?\s*)?(?:Ltd\.?|Limited|Inc\.?|Corp(?:oration)?\.?|Company|LLC|Co\.?)$', '', n, flags=re.I).strip(' ,.')
    return n


def date_in_text(text, day, window=7):
    """本文の日付(23 November 2026 と November 23, 2026 の両方)のどれかが一覧の日付の前後 window 日以内か"""
    mon = {m: i + 1 for i, m in enumerate(['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'])}
    ds = []
    for m in re.finditer(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', text):
        if m.group(2).lower() in mon:
            ds.append((int(m.group(3)), mon[m.group(2).lower()], int(m.group(1))))
    for m in re.finditer(r'([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})', text):
        if m.group(1).lower() in mon:
            ds.append((int(m.group(3)), mon[m.group(1).lower()], int(m.group(2))))
    for y, mo, d in ds:
        try:
            if abs((datetime.date(y, mo, d) - day).days) <= window:
                return True
        except ValueError:
            pass
    return False


def code_in_text(text, code):
    c = code.lstrip('0')
    return bool(re.search(r'(?:stock\s*code|HKEX|SEHK|HK)\s*[:：]?\s*0*' + re.escape(c) + r'\b', text[:3000], re.I))


def ai_strength_en(text):
    return len(AI_CO_EN.findall(text)), len(AI_WORD_EN.findall(text))


def amount_en(text):
    m = re.search(r'(?:consideration|subscription (?:price|amount)|investment amount|capital contribution|total (?:investment|consideration))[^.\n]{0,160}?((?:HK\$|HKD|US\$|USD|RMB|CNY|S\$)\s?[\d,\.]+\s?(?:million|billion)?)', text, re.I)
    return (m.group(1) + '(開示書類の「' + m.group(0).split()[0].strip() + '」の近く)') if m else ''


def decide(c, text, T_name):
    """1件を確かめて (deal か None, 手動に回す理由) を返す。deal = {from, to, kind, amount, to_title}"""
    if not code_in_text(text, c['code']):
        return None, '本文に証券コード(Stock code)が見つからない'
    if not date_in_text(text, c['day']):
        return None, '本文の日付が一覧と合わない'
    n_co, n_w = ai_strength_en(text)
    if not (n_co >= 1 or n_w >= 3):
        return None, 'AIらしさが弱い(AI企業名がなく、AI系の語が3回未満)'
    x, kind = x_from_title(c['title'])
    resolved = False
    if not x:
        rx_, rk = raw_title_x(c['title'])
        if rx_ and LABEL_RX.match(rx_):  # 表題が「Target Company」とだけ書いてあるときは、本文の定義から相手の名前を読む
            nm, why = resolve_label(rx_, text)
            if not nm:
                return None, f'表題の相手が「{rx_.title()}」とだけあり、本文からも決められない({why})'
            x, kind, resolved = nm, rk, True
        else:
            return None, kind
    if resolved:
        form, n = x, 2  # 名前は定義に1回だけ出るのが普通。呼び名の出現回数は resolve_label で確かめ済み
    else:
        form, n = in_body(x, text)
    if n < 2:
        return None, f'相手の名前({x})が本文に2回以上出てこない'
    filer = T_name or en_clean(filer_en(text, ''))
    if not filer:
        return None, '出す側の会社の名前が本文から読めない'
    to = en_clean(form)
    if not to or to.lower() == filer.lower():
        return None, '相手が出す側の会社と同じになる'
    return {'from': filer, 'to': to, 'kind': kind, 'amount': amount_en(text), 'ai_hits': {'company': n_co, 'word': n_w}, 'to_from_definition': resolved}, ''


def rows_from_feeds(status):
    rows, ok = [], 0
    for u in FEEDS:
        try:
            d = json.loads(W.http(u, timeout=60, retries=1))
        except Exception as e:  # noqa
            status.setdefault('feeds_failed', []).append(u.rsplit('_', 1)[-1] + ':' + str(e)[:60])
            continue
        ok += 1
        rows += d.get('newsInfoLst') or []
    status['ok'] = ok > 0
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=5, help='この日数より古い発表は見ない')
    ap.add_argument('--max', type=int, default=40, help='1回に開くPDFの上限')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    os.makedirs(W.OUT, exist_ok=True)
    T = W.load_targets()
    seen = W.load_seen()
    today = datetime.datetime.now(W.JST).date()
    status = {}
    rows = rows_from_feeds(status)
    if not status['ok']:
        print('HKEXの一覧が読めない:', status.get('feeds_failed'))
        return
    mou_st = MF.load_state()
    MF.sync(mou_st)  # 覚書(MOU)の段階で入れた線を目録に登録(あとの発表で実行されたか確かめる。2026/11/24追加)
    mou_codes = MF.codes(mou_st)
    short, dup = [], set()
    for x in rows:
        title = norm_title(x.get('title', ''))
        blob = f"{x.get('sTxt', '')} {title}"
        follow = bool({(s_.get('sc') or '').lstrip('0').zfill(5) for s_ in (x.get('stock') or [])} & mou_codes) and bool(FOLLOW_TITLE.search(title))
        if x.get('ext') != 'pdf' or HK_NOT.search(blob) or W.HK_EXCLUDE.search(title) or not (HK_WANT.search(title) or HK_WANT.search(x.get('sTxt', '')) or follow):
            continue
        m = re.match(r'(\d+)/(\d+)/(\d+)\s+(\d+):(\d+)', x.get('relTime', ''))
        day = datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else today
        if (today - day).days > a.days:
            continue
        tk = 'HKX2|' + x['webPath']
        if tk in seen or tk in dup:
            continue
        dup.add(tk)
        for st in (x.get('stock') or [])[:1]:  # 複数社の共同発表は最初の会社だけ(向きが決められないので、実際は手動に回る)
            code = (st.get('sc') or '').lstrip('0').zfill(5)
            tg = T['HK'].get(code) or T['HK'].get(st.get('sc') or '')
            short.append({'market': 'HKEX(香港)', 'tkey': tk, 'code': code, 'co': tg['name'] if tg else st.get('sn', ''), 'co_list': st.get('sn', ''),
                          'title': title, 'cat': '出資', 'url': 'https://www.hkexnews.hk' + x['webPath'], 'day': day,
                          'time': (m.group(4) + ':' + m.group(5)) if m else '', 'key': (tg or {}).get('key', ''), 'in_map': bool(tg),
                          'hk_cat': x.get('sTxt', ''), 'multi': len(x.get('stock') or []) > 1})
    print(f'一覧 {len(rows)} 件 → 気になる {len(short)} 件(上限 {a.max} 件を開く)')
    items, skipped, fail, new_seen, money, follow_money = [], [], [], [], [], []
    for c in short[:a.max]:
        text, err = W.pdf_text(c['url'])
        new_seen.append(c['tkey'])
        if not text or len(text) <= 120:
            fail.append(c)
            print('△ 開けず(再確認へ):', c['co'], c['title'][:30], err)
            continue
        for mou, mrec in MF.observe(mou_st, c, text):  # 覚書の続きか(AIらしさに関係なく、同じ会社・相手なら確かめる)
            print('◎ 覚書の続き:', mou['from'], '→', mou['to'], mrec['status'], '|', mrec['title'][:40])
            fm = MF.followup_money(mou, mrec, amount_en(text))
            if fm:
                follow_money.append(fm)
        n_co, n_w = ai_strength_en(text)
        if not (n_co >= 1 or n_w >= 3):
            skipped.append({'co': c['co'], 'title': c['title'], 'url': c['url'], 'why': '本文にAI企業名・AI系の語がない(または少ない)'})
            continue
        deal, why = decide(c, text, c['co'] if c['in_map'] else '')
        if deal and c['multi']:
            deal, why = None, '複数の会社の共同発表で、出す側が決められない'
        rec = {'d': str(c['day']), 'time': c['time'], 'market': c['market'], 'code': c['code'], 'co': c['co'], 'title': c['title'], 'hk_cat': c['hk_cat'],
               'url': c['url'], 'cf': '開示', 'ai_hits': {'company': n_co, 'word': n_w}, 'snippet': W.ctx_snippet(text, 'invest' if re.search('invest', text, re.I) else 'agreement'),
               'import': '手動(' + why + ')'}
        if deal:
            rec['deal'] = deal
            rec['import'] = '自動(inbox/money)'
            note_extra = '。ファンドを通じた間接の出資(同社のファンドへの持分は一部)' if re.search(r"\bthe\s+fund\b", c['title'] + ' ' + text[:1500], re.I) else ''
            note_def = '。表題は相手を「Target Company」とだけ書いており、相手の名前は本文の定義から読んだ(英訳名)' if deal.get('to_from_definition') else ''
            note_mou = '。覚書(MOU)の段階で、実行は未確定' if re.search(r'memorandum of understanding|\bMOU\b|possible\s+(?:capital|investment|acquisition)', c['title'], re.I) else ''
            money.append({'from': deal['from'], 'to': deal['to'], 'kind': deal['kind'], 'amount': deal['amount'], 'date': rec['d'], 'region': '香港', 'code': c['code'],
                          'note': f"{c['co']}のHKEXの発表「{c['title'][:70]}」で確認({rec['d']}。PDFを開いて証券コード・日付・相手の名前・AI関連の語を照合){note_extra}{note_def}{note_mou}。金額は開示書類にある場合のみ記載",
                          'src': [[f"HKEX {c['co']}の開示({rec['d']})", c['url']]], 'confidence': '開示'})
        items.append(rec)
        print('○', c['co'], c['title'][:40], '→', rec['import'][:30])
        time.sleep(0.5)
    if a.dry:
        print(f'(dry) 本文を開いて確かめ済み {len(items)} 件・うち inbox/money に足す {len(money)} 件・関係なし {len(skipped)} 件・再確認へ {len(fail)} 件')
        for m in money:
            print('  money:', m['from'], '→', m['to'], m['kind'], m['amount'])
        for m in follow_money:
            print('  覚書の続き:', m['from'], '→', m['to'], m['kind'], m['mark'])
        return
    if fail:
        q = W.retry_load()
        have = {i['tkey'] for i in q['items']}
        q['items'] += [W.to_retry_item(c, 'PDFが開けない', tries=0) for c in fail if c['tkey'] not in have]
        W.retry_save(q)
    stamp = today.strftime('%Y-%m-%d')
    p = os.path.join(W.OUT, f'hkex-scan-{stamp}.json')
    old = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'items': [], 'skipped': []}
    have = {x['url'] for x in old['items']}
    old['items'] += [x for x in items if x['url'] not in have]
    old['skipped'] = old.get('skipped', []) + skipped
    old.update({'date': stamp, 'kind': 'ir-scan-hkex', 'list_rows': len(rows), 'shortlist': len(short), 'not_opened_over_limit': max(0, len(short) - a.max), 'retry_queued': len(fail)})
    json.dump(old, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if money:
        mp = os.path.join(W.ROOT, 'inbox', 'money', stamp + '-hkex.json')
        md = json.load(open(mp, encoding='utf-8')) if os.path.exists(mp) else {'date': stamp, 'kind': 'money', 'items': []}
        have = {i['src'][0][1] for i in md['items']}
        md['items'] += [m for m in money if m['src'][0][1] not in have]
        json.dump(md, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('inbox/money に足した:', len(money), '→', mp)
    MF.sync(mou_st)  # 今回足した覚書の線も登録
    MF.save_state(mou_st)
    if follow_money:
        print('覚書の続きを足した:', MF.write_followups(follow_money, stamp))
    with open(W.SEEN, 'a', encoding='utf-8') as w:
        for k in new_seen:
            w.write(k + '\n')
    print(f'保存: {p}(確かめ済み {len(items)} 件・money へ {len(money)} 件・関係なし {len(skipped)} 件・再確認へ {len(fail)} 件)')


if __name__ == '__main__':
    main()
