#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDnet 新着一覧の見張り(日本の人事係用、2026/11/24追加)

TDnet(適時開示)の新着一覧を毎朝ぜんぶ見て、「気になる会社」の役員人事だけPDFを開く。
ir_watch.py は相関図にある会社だけを見る。こちらは、相関図にない会社でも
AI・DX・半導体・データの担当役員が決まった発表を拾うためのもの。足すだけで、消さない。

「気になる」の決め方(表題・会社名だけで決める。ここではPDFを開かない):
  1. 表題が役員人事・組織変更である(ir_watch.py と同じ言葉の判定)
  2. かつ、次のどれか: 会社名か表題に AI・DX・デジタル・データ・半導体・ロボ・ソフト・情報・システムなどの語がある
                       / 相関図の会社でない会社でも、表題に CDO・CIO・CTO・最高…責任者 がある
  相関図の会社(jpco.js・targets_extra.txt)は ir_watch.py が見るので、ここでは重ねない。
PDFを開いたら、本文に AI系の語があるものだけ保存する(人の名前・役職は本文で確かめる)。

PDFが開けなかったものは「見送り」にせず、ir_watch.py と同じ再確認の列(inbox/ir/retry.json)に入れる。
翌日から最大3回、ir_watch.py が開き直す。

  inbox/ir/tdnet-scan-日付.json  保存先(items=本文で確かめたもの、skipped=気にならなかった件数など)
  inbox/ir/seen.txt              見たものの目録(ir_watch.py と共通。足すだけ)

使い方:
  python3 scripts/tdnet_scan.py            # 直近2営業日
  python3 scripts/tdnet_scan.py --days 3 --max 30 --dry
  python3 scripts/tdnet_scan.py --kind alliance   # 日本の提携係: 提携・協業の発表(結果は inbox/ir/tdnet-scan-alliance-日付.json)
  python3 scripts/tdnet_scan.py --kind invest     # 出資・買収の発表(相関図にない会社も。結果は inbox/ir/tdnet-scan-invest-日付.json)

自動で inbox/money に足す条件(2026/11/24追加。alliance と invest。どれか1つでも欠けたら足さず、記録だけ):
  1. PDFが開け、会社名か証券コードが本文にある  2. 本文の日付が一覧の日付と近い
  3. 表題から「だれが・だれと」が決まる(「○○との業務提携」「○○の株式取得」など)  4. 相手の名前が本文にも出てくる
  5. 本文にAI企業名(OpenAI など)がある、またはAI系の語(AI・生成AI・GPU・データセンター・半導体など)が2回以上ある
  足す先は inbox/money/日付-tdnet.json(出典は開示のPDF、confidence は「開示」)。相関図への取り込みは merge_inbox.py(毎朝9:13)。
"""
import argparse, datetime, json, os, re, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ir_watch as W

AI_WORDS = re.compile(r'AI|ＡＩ|人工知能|DX|ＤＸ|デジタル|データ|半導体|ロボ|ソフトウェア|ソフトウエア|情報|システム|テクノロジ|IT|ＩＴ|クラウド|サイバー|ネットワーク', re.I)
BODY_AI = re.compile(r'AI|人工知能|DX|デジタル|データ|半導体|CDO|CIO|CTO|CAIO|最高(技術|情報|デジタル|データ)|情報システム|ロボ', re.I)
# 提携モード(--kind alliance, 2026/11/24追加): 日本の提携係用。表題が提携・協業で、本文にAI企業名・AI系の語があるものだけ残す
ALLI_TITLE = re.compile(r'業務提携|資本提携|資本業務提携|提携|協業|アライアンス|業務連携|共同開発|包括連携')
ALLI_BODY = re.compile(r'OpenAI|Anthropic|Claude|ChatGPT|Gemini|Google|NVIDIA|エヌビディア|Microsoft|マイクロソフト|Mistral|Sakana|生成AI|(?<![A-Za-z])AI(?![a-z])|人工知能|LLM|大規模言語|GPU|データセンター|半導体', re.I)
# 自動で inbox/money に足すときの「AIらしさ」(2026/11/24): AI企業名が1つでもある、またはAI系の語が2回以上
AI_COMPANY = re.compile(r'OpenAI|Anthropic|ChatGPT|Gemini|NVIDIA|エヌビディア|Mistral|Sakana|サカナ|xAI|Perplexity|Cohere|DeepSeek|Preferred Networks|プリファードネットワークス', re.I)
AI_WORD = re.compile(r'生成AI|(?<![A-Za-z])AI(?![a-z])|人工知能|LLM|大規模言語|GPU|データセンター|半導体|機械学習|ディープラーニング')
ALLI_PARTNER = re.compile(r'^(?P<p>[^「」]+?)と(?:の)?(?:の)?(?P<k>包括的?業務提携|資本業務提携|資本提携|業務提携|業務連携|包括連携|共同開発|協業|アライアンス)')
ALLI_BOTH = re.compile(r'^(?P<a>[^「」]+?)と(?P<b>[^「」]+?)の(?P<k>包括的?業務提携|資本業務提携|資本提携|業務提携|業務連携|共同開発|協業|アライアンス)')
TITLE_C = re.compile(r'CDO|CIO|CTO|CAIO|最高(技術|情報|デジタル|データ|AI)', re.I)

# 本文から提携の相手を読み取る(2026/11/24追加): 表題が長くて相手が決まらないときの代わり
# 「N．提携先(相手先)の概要 (1)名称 ○○」の欄を読む。次のどれかなら読み取らず、手動に回す(迷うものは足さない)
BODY_HEAD = re.compile(r'^\s*[0-9０-９一二三四五六七八九]+\s*[.．、]\s*[^\n]{0,30}?(提携先|相手先|相手方|提携の相手|連携先|協業先|共同開発先|契約の相手)[^\n]{0,10}?の概要', re.M)
BODY_NAME = re.compile(r'[（(]\s*[1１]\s*[）)]\s*名\s*称\s+(?P<n>[^\n]+)')
# 表題に1つでもあれば「提携の新規のつながり」ではない・当事者がこの会社ではない → 本文でも読み取らない
TITLE_NOT_NEW = re.compile(r'解消|終了|解除|契約期間|延長|日程|継続|経過|訂正|変更|締結の延期|連結子会社|当社子会社|子会社の|子会社と|による当社株式|基本方針|進捗|進捗|上市|販売提携')
CORP_WORD = re.compile(r'株式会社|有限会社|合同会社|Inc|Corp|Ltd|Limited|GmbH|LLC|S\.A|AG|Co\.|Group|グループ|ホールディングス|銀行|金庫|大学|機構|協会|省|庁|組合|研究所')


def body_partner(text, filer, title):
    """本文の「提携先の概要」欄から相手の名前を1つだけ読む。(名前, None) か (None, 手動に回す理由)"""
    if TITLE_NOT_NEW.search(W.nfkc(title)):
        return None, '表題に「解消・延長・子会社・継続」などがあり、新しいつながりと決められない'
    heads = list(BODY_HEAD.finditer(text))
    if not heads:
        return None, '本文に「提携先の概要」の欄がない'
    names = set()
    for h in heads:
        seg = text[h.end():h.end() + 700]
        m = BODY_NAME.search(seg)
        if m:
            # 同じ行に別の欄(2社が並ぶ表)があれば、ふた文字以上の空白で区切って最初だけ見る
            raw = re.split(r'\s{3,}', m.group('n').strip())
            if len(raw) > 1 and CORP_WORD.search(raw[1]):
                return None, '「提携先の概要」に複数の会社が並んでいる'
            nm = W.clean_name(raw[0])
            if nm:
                names.add(nm)
    if len(names) != 1:
        return None, ('「提携先の概要」に名前が読み取れない' if not names else '「提携先の概要」の名前が複数ある')
    nm = names.pop()
    filer_c = W.clean_name(filer)
    if not nm or len(nm) > 40 or nm in ('当社', '子会社') or re.search(r'[、,，]|および|及び', nm):
        return None, '名前が会社名として決められない'
    if nm == filer_c or nm in filer_c or filer_c in nm:
        return None, '相手が提出した会社自身と同じになる'
    sq = W.squash(text)
    if W.squash(nm) not in W.squash(title) and sq.count(W.squash(nm)) < 2:
        return None, '相手の名前が本文でもう1回出てこない(欄の1回だけ)'
    return nm, None


# 本文の「以下「○○」といいます」の定義から相手を読む(2026/11/24追加。HKEXの hkex_scan.py の「Target Company」の読み方の日本版)
# 「提携先の概要」の欄がない短い発表や、表題が「事業提携に関するお知らせ」とだけで相手がない発表のための代わり。
# 自動で足す条件(1つでも欠けたら手動のまま): 定義が「会社名(以下「呼び名」)」の形 / 呼び名が本文に3回以上出る /
#   出す側以外の会社の定義がちょうど1つ / 名前が会社名らしい(株式会社・Inc など。または呼び名が表題にある) / 定義の近くに提携・協業・契約・合意の語がある
DEF_RX = re.compile(r'以下\s*[「『“"]\s*(?P<al>[^」』”"]{1,30}?)\s*[」』”"]')
DEF_SPLIT = re.compile(r'[、。]|[」』）)]\s*と\s*|お知らせ|において|との間で|は、|が、|と、|および|及び')
DEF_CTX = re.compile(r'提携|協業|連携|契約|合意|パートナー|共同|アライアンス')
DEF_NOT_CO = re.compile(r'当社|本[契提件]|本基本|本合意|本取引|本株|本資本|本件|同社|当該|および|及び|目的|[0-9]{4}年|\bFA\b')


def flat_text(text):
    """PDFの行末の改行をつなぐ。日本語どうしは詰め、英数字がからむ所は空白1つ"""
    t = W.nfkc(text)
    t = re.sub(r'(?<=[^\x00-\x7f])[ \t]*\n[ \t]*(?=[^\x00-\x7f])', '', t)
    return re.sub(r'\s*\n\s*', ' ', t)


def def_partner(text, filer, title):
    """本文の定義「会社名(以下「呼び名」といいます)」から相手を1つだけ読む。(名前, None) か (None, 手動に回す理由)"""
    if TITLE_NOT_NEW.search(W.nfkc(title)):
        return None, '表題に「解消・延長・子会社・継続」などがあり、新しいつながりと決められない'
    ft = flat_text(text)
    sq = W.squash(text)
    sq_title = W.squash(title)
    found = {}
    for m in DEF_RX.finditer(ft):
        al = m.group('al').strip()
        head = ft[max(0, m.start() - 160):m.start()]
        op = max(head.rfind('('), head.rfind('（'))
        if op < 0:
            continue
        seg = DEF_SPLIT.split(head[:op])[-1].strip()
        if not seg or len(seg) > 60 or DEF_NOT_CO.search(seg) or DEF_NOT_CO.search(al):
            continue
        in_title = W.squash(al) in sq_title
        if not (CORP_WORD.search(seg) or in_title):
            continue
        if re.search(r'[^\x00-\x7f]', seg):
            seg = re.sub(r'\s+', '', seg)
        ctx = ft[max(0, m.start() - 200):m.end() + 200]
        if not DEF_CTX.search(ctx):
            continue
        found[W.squash(W.clean_name(seg)).lower()] = (seg, al, in_title)
    others = {k: v for k, v in found.items() if not (same_co(v[0], filer) or same_co(v[1], filer))}
    if not others:
        return None, '本文に相手の定義(「以下「○○」といいます」)が見つからない'
    if len(others) != 1:
        return None, '本文に出す側以外の会社の定義が複数あって1つに決められない'
    seg, al, in_title = next(iter(others.values()))
    if sq.count(W.squash(al)) < 3:
        return None, f'呼び名「{al}」が本文に3回以上出てこない'
    nm = al if in_title else W.clean_name(seg)
    if not name_ok(nm) or nm in ('当社', '子会社'):
        return None, '名前が会社名として決められない'
    return nm, None


def ai_strength(text):
    """本文のAIらしさ。(AI企業名の数, AI系の語の数)"""
    t = W.nfkc(text)
    return len(AI_COMPANY.findall(t)), len(AI_WORD.findall(t))


def deal_from_title(title, filer, mode):
    """表題から (出す側, 相手, 種類) が確実にとれたものだけ返す。とれなければ None"""
    t = W.nfkc(title).strip()
    t = re.sub(r'^\（?\(?(開示事項の(経過|変更)|変更|訂正)\)?\）?\s*', '', t)
    t = re.sub(r'\((証券コード|コード)[:：]?\s*\w+\)', '', t)
    t = re.sub(r'^当社(による|が|の)?\s*', '', t)
    if mode == 'invest':
        return W.money_from_title(title, filer)
    m = ALLI_PARTNER.match(t)
    if m and not re.search(r'との間|について|に関する', m.group('p')):
        p = W.clean_name(m.group('p'))
        if p and p not in ('当社', '子会社') and len(p) <= 40 and not re.search(r'[、,]', p):
            return filer, p, '出資' if '資本' in m.group('k') else '提携'
    m = ALLI_BOTH.match(t)
    if m:
        a, b = W.clean_name(m.group('a')), W.clean_name(m.group('b'))
        if a and b and a != b and len(a) <= 40 and len(b) <= 40 and not re.search(r'[、,]', a + b):
            return a, b, '出資' if '資本' in m.group('k') else '提携'
    return None


BAD_NAME = re.compile(r'^(の|と|が|を|子会社|当社|同社|[^\s]{1,4}企業)|取得|提携|買収|締結|契約|及び|並びに|について|[()（）]')


def name_ok(nm):
    """会社名として足してよい形か(「の…」で始まる・かっこや「取得」を含む・長すぎるものは手動に回す)"""
    return bool(nm) and len(nm) <= 40 and not BAD_NAME.search(nm)


def same_co(a, b):
    a, b = W.squash(W.clean_name(a)).lower(), W.squash(W.clean_name(b)).lower()
    return bool(a and b and (a == b or (len(min(a, b, key=len)) >= 3 and (a in b or b in a))))


def filer_name(short, text):
    """出す側の会社名。TDnetの一覧の名前は略称・市場の印つき(「Ｇ－イオレ」「りそなＨＤ」)なので、本文の先頭の「会社名 ○○」を使う。読めなければ印だけ外した略称"""
    base = W.clean_name(re.sub(r'^[ＧＳＰＭ]\s*[－\-]\s*', '', W.nfkc(short)))
    base = re.sub(r'^[A-Z]-', '', base)
    m = re.search(r'(?:会\s*社\s*名|社\s*名|商\s*号)\s+([^\n]{2,60})', text[:1200])
    if m:
        full = W.clean_name(re.sub(r'\s+', '', W.nfkc(re.split(r'\s{3,}', m.group(1).strip())[0])))
        # 共同発表で相手の名前が先頭に来ることがある。略称の先頭2文字が合わないものは使わない
        if full and name_ok(full) and len(full) >= 2 and base[:2].lower() == full[:2].lower():
            return full
    return base


def pick_deal(title, filer, mode, text):
    """表題と本文から (出す側, 相手, 種類) を決める。(deal, 決め方, 手動に回す理由)。
    表題と本文の両方で相手が読めて食い違うものは決めない。どちらかだけでも、会社名の形が整っていれば使う"""
    if mode == 'alliance' and TITLE_NOT_NEW.search(W.nfkc(title)):
        return None, '', '表題に「解消・延長・子会社・継続」などがあり、新しいつながりと決められない'
    dt = deal_from_title(title, filer, mode)
    if dt and not (name_ok(dt[0]) and name_ok(dt[1])):
        dt = None
    if mode != 'alliance':
        return dt, '表題', '' if dt else '表題から相手が決められない'
    how_def = False
    nm, why = body_partner(text, filer, title)
    if not nm and why in ('本文に「提携先の概要」の欄がない', '「提携先の概要」に名前が読み取れない', '名前が会社名として決められない'):
        nm2, why2 = def_partner(text, filer, title)  # 概要の欄がないときは、本文の定義から読む
        if nm2:
            nm, why, how_def = nm2, '', True
        else:
            why = why + '。定義からも決められない(' + why2 + ')'
    if dt and nm:
        other = dt[1] if W.clean_name(dt[0]) == W.clean_name(filer) else dt[0]
        if not same_co(other, nm):
            return None, '', f'表題の相手({other})と本文の相手({nm})が合わない'
        return dt, '表題と本文' + ('(定義)' if how_def else ''), ''
    if nm:
        return (filer, nm, '出資' if '資本' in W.nfkc(title) else '提携'), '本文(定義)' if how_def else '本文', ''
    if dt:
        return dt, '表題', ''
    return None, '', why or '表題からも本文からも相手が決められない'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=2)
    ap.add_argument('--max', type=int, default=30, help='1回に開くPDFの上限')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--kind', choices=['hr', 'alliance', 'invest'], default='hr',
                    help='hr=役員人事(既定) / alliance=業務提携・協業(日本の提携係用) / invest=出資・買収(相関図にない会社も)')
    a = ap.parse_args()
    mode = a.kind
    alli, inv = mode == 'alliance', mode == 'invest'
    CAT = {'hr': '役員人事', 'alliance': '提携', 'invest': '出資・買収'}[mode]
    BODY = ALLI_BODY if alli else BODY_AI
    os.makedirs(W.OUT, exist_ok=True)
    T = W.load_targets()
    seen = W.load_seen()
    today = datetime.datetime.now(W.JST).date()
    days, d = [], today
    while len(days) < a.days and (today - d).days < a.days + 6:
        if d.weekday() < 5:
            days.append(d)
        d -= datetime.timedelta(days=1)
    rows_n, short = 0, []
    for day in days:
        try:
            rows = W.tdnet_rows(day)
        except Exception as e:  # noqa
            print('TDnetの一覧が読めない:', str(e)[:80])
            return
        rows_n += len(rows)
        for tm, code5, name, title, pdf in rows:
            code = W.nfkc(code5)
            code = code[:-1] if len(code) == 5 and code.endswith('0') else code
            if 'TDNET|' + pdf in seen:
                continue
            kind = W.kind_of(title, W.JP_KINDS, W.JP_EXCLUDE)
            cat = CAT
            if inv:
                # 出資・買収。相関図の会社は ir_watch.py の担当なので重ねない(相関図にない会社だけ見る)
                if code in T['JP'] or kind not in ('出資', '買収') or '新株予約権' in W.nfkc(title):  # 新株予約権の発行は出資の線にしない
                    continue
                cat = kind
            elif alli:
                # 出資・買収の表題は invest の担当。ここは「業務提携・協業」だけ
                if kind in ('出資', '買収') or W.JP_EXCLUDE.search(W.nfkc(title)) or not ALLI_TITLE.search(W.nfkc(title)):
                    continue
            else:
                if code in T['JP']:
                    continue  # 相関図の会社は ir_watch.py の担当
                if kind != '役員人事':
                    continue
                nm = W.nfkc(name) + ' ' + W.nfkc(title)
                if not (AI_WORDS.search(nm) or TITLE_C.search(W.nfkc(title))):
                    continue
            short.append({'market': 'TDnet(日本)', 'tkey': 'TDNET|' + pdf, 'code': code, 'co': name, 'co_list': name, 'title': title,
                          'cat': cat, 'url': 'https://www.release.tdnet.info/inbs/' + pdf, 'day': day, 'time': tm, 'key': ''})
    print(f'一覧 {rows_n} 件 → 気になる {len(short)} 件(上限 {a.max} 件を開く)')
    items, skipped, fail, new_seen, money = [], [], [], [], []
    for c in short[:a.max]:
        text, err = W.pdf_text(c['url'])
        new_seen.append(c['tkey'])
        if not text or len(text) <= 120:
            fail.append(c)
            print('△ 開けず(再確認へ):', c['co'], c['title'][:30], err)
            continue
        n_co, n_w = ai_strength(text)
        if inv:
            body_ok = n_co >= 1 or n_w >= 2  # 出資・買収は件数が多いので、AIらしさが強いものだけ
        else:
            body_ok = bool(BODY.search(W.nfkc(text)))
        if not body_ok:
            skipped.append({'co': c['co'], 'title': c['title'], 'url': c['url'], 'why': '本文にAI企業名・AI・DX・半導体などの語がない(または少ない)'})
            print('× 関係なし:', c['co'], c['title'][:30])
        elif not W.date_ok(text, c['day']):
            skipped.append({'co': c['co'], 'title': c['title'], 'url': c['url'], 'why': '本文の日付が一覧と合わない'})
            print('× 日付:', c['co'], c['title'][:30])
        else:
            rec = {'d': str(c['day']), 'time': c['time'], 'market': c['market'], 'code': c['code'], 'co': c['co'], 'title': c['title'],
                   'cat': c['cat'], 'url': c['url'], 'cf': '開示', 'ai_hits': {'company': n_co, 'word': n_w},
                   'snippet': W.ctx_snippet(text, '提携' if alli else ('出資' if c['cat'] == '出資' else '取得') if inv else '異動の内容')}
            if mode == 'hr':
                rec['import'] = '記録のみ(人の名前・役職は本文を読んで確かめてから inbox/moves に足す)'
            else:
                filer = filer_name(c['co'], text)
                deal, how, why = pick_deal(c['title'], filer, mode, text)
                sq = W.squash(text)
                co_ok = bool(re.search(r'(コード番号|証券コード|コード)[^0-9A-Za-z]{0,12}' + re.escape(c['code']), sq)) or W.squash(filer) in sq
                strong = n_co >= 1 or n_w >= 2
                if deal and not co_ok:
                    why = '本文に会社名・証券コードが見つからない'
                elif deal and not strong:
                    why = 'AIらしさが弱い(AI企業名がなく、AI系の語が2回未満)'
                elif deal and not (W.squash(deal[1]) in sq or W.squash(W.clean_name(deal[1])) in sq):
                    why = '相手の名前が本文で確かめられない'
                rec['import'] = '手動(' + (why or '理由不明') + ')'
                if deal and co_ok and strong and not (why and why != ''):
                    fr, to, k = deal
                    rec['deal'] = {'from': fr, 'to': to, 'kind': k, 'amount': W.amount_near(text), 'partner_from': how}
                    rec['import'] = '自動(inbox/money)'
                    money.append({'from': fr, 'to': to, 'kind': k, 'amount': rec['deal']['amount'], 'date': rec['d'], 'region': '日本',
                                  'note': f"{c['co']}の適時開示「{c['title'][:60]}」で確認(TDnet、{rec['d']}。PDFを開いて会社・相手({how}で確認)・日付・AI関連の語を照合)。金額は開示書類にある場合のみ記載",
                                  'src': [[f"TDnet {c['co']}の開示({rec['d']})", c['url']]], 'confidence': '開示'})
            items.append(rec)
            print('○', c['co'], c['title'][:40], '→', rec['import'][:8])
        time.sleep(0.5)
    if a.dry:
        print(f'(dry) 確かめ済み {len(items)} 件・うち inbox/money に足す {len(money)} 件・関係なし {len(skipped)} 件・再確認へ {len(fail)} 件')
        for m in money:
            print('  money:', m['from'], '→', m['to'], m['kind'], m['amount'])
        return
    if fail:
        q = W.retry_load()
        have = {i['tkey'] for i in q['items']}
        q['items'] += [W.to_retry_item(c, 'PDFが開けない', tries=0) for c in fail if c['tkey'] not in have]
        W.retry_save(q)
    stamp = today.strftime('%Y-%m-%d')
    p = os.path.join(W.OUT, {'hr': f'tdnet-scan-{stamp}.json', 'alliance': f'tdnet-scan-alliance-{stamp}.json', 'invest': f'tdnet-scan-invest-{stamp}.json'}[mode])
    old = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'items': [], 'skipped': []}
    have = {x['url'] for x in old['items']}
    old['items'] += [x for x in items if x['url'] not in have]
    old['skipped'] = old.get('skipped', []) + skipped
    old.update({'date': stamp, 'kind': {'hr': 'ir-scan', 'alliance': 'ir-scan-alliance', 'invest': 'ir-scan-invest'}[mode], 'list_rows': rows_n, 'shortlist': len(short),
                'not_opened_over_limit': max(0, len(short) - a.max), 'retry_queued': len(fail)})
    json.dump(old, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if money:
        mp = os.path.join(W.ROOT, 'inbox', 'money', stamp + '-tdnet.json')
        md = json.load(open(mp, encoding='utf-8')) if os.path.exists(mp) else {'date': stamp, 'kind': 'money', 'items': []}
        have = {i['src'][0][1] for i in md['items']}
        md['items'] += [m for m in money if m['src'][0][1] not in have]
        json.dump(md, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('inbox/money に足した:', len(money), '→', mp)
    with open(W.SEEN, 'a', encoding='utf-8') as w:
        for k in new_seen:
            w.write(k + '\n')
    print(f'保存: {p}(確かめ済み {len(items)} 件・money へ {len(money)} 件・関係なし {len(skipped)} 件・再確認へ {len(fail)} 件)')


if __name__ == '__main__':
    main()
