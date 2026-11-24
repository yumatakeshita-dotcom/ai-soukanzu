#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""覚書(MOU)の段階で入れた話が、あとで本当に実行されたかを確かめる(2026/11/24追加)

hkex_scan.py は、表題が覚書(MOU)・Possible(可能性)の発表も、本文で確かめたら inbox/money に足す。
その線のひとことには「覚書(MOU)の段階で、実行は未確定」と付く。こちらは、その後のHKEXの発表に
「正式な契約の締結」「完了」が出たかを見て、出ていたら印(正式契約を確認・完了を確認)を足す。足すだけで、消さない。

仕組み:
  1. inbox/money/*.json の中から「覚書(MOU)の段階」の注記がある線を拾い、目録 inbox/ir/mou_followup.json に登録する
     (登録するだけ。元の線は書き換えない)
  2. hkex_scan.py が本文を開いた発表ごとに observe() を呼ぶ。次を全部満たしたら「正式契約を確認」
       ・同じ会社の発表(証券コードが同じ。コードが記録にない古い線は、本文の先頭に出す側の名前がある)
       ・日付が覚書より後(400日以内)
       ・表題が覚書・Possible・仮契約ではなく、「契約の締結(Entering into / Formal / Definitive など)」か「完了(Completion)」
       ・本文に相手の名前がある
     表題に「完了(Completion)」があれば「完了を確認」、本文に覚書の失効・終了(lapse・terminate・not to proceed)があれば「失効・終了を記録」
  3. 確認できたものは、目録に出典つきで記録し、inbox/money/日付-hkex-followup.json に「覚書の続き」の線として足す
     (merge_inbox.py が毎朝9:13に相関図へ。出典が別のURLなので、覚書の線はそのまま残り、並んで出る)
  4. 120日たっても確認できないものは、一覧に「期限を過ぎて未確認」と出すだけ(線は消さない・書き換えない)

使い方:
  python3 scripts/mou_followup.py --sync     # 目録に登録して一覧を出す(書き込みは目録だけ)
  python3 scripts/mou_followup.py --list     # 一覧だけ
  python3 scripts/mou_followup.py --pdf URL --code 02255 --title "表題" --date 2026-12-01   # 1つの発表を手で確かめる(--apply で足す)
"""
import argparse, datetime, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ir_watch as W

STATE = os.path.join(W.ROOT, 'inbox', 'ir', 'mou_followup.json')
MOU_MARK = '覚書(MOU)の段階'
STALE_DAYS = 120
MAX_DAYS = 400

# 表題の判定
T_MOU = re.compile(r'memorandum|\bMOU\b|possible|proposed|non-?binding|letter of intent|\bLOI\b|term sheet|intention', re.I)
T_EXEC = re.compile(r'entering\s+into|entry\s+into|entered\s+into|signing\s+of|execution\s+of|formal\s+agreement|definitive\s+agreement|binding\s+agreement|'
                    r'capital\s+injection\s+agreement|equity\s+transfer\s+agreement|subscription\s+agreement|sale\s+and\s+purchase\s+agreement|'
                    r'cooperation\s+agreement|framework\s+agreement|investment\s+agreement|joint\s+venture\s+agreement|supplemental\s+agreement', re.I)
T_DONE = re.compile(r'completion\s+of|completed|closing\s+of', re.I)
# 本文
B_EXEC = re.compile(r'(?:has|have|had|was|were)?\s*(?:entered|enters|entering)\s+into\s+(?:an?\s+|the\s+)?(?:(?!memorandum|MOU)[\w\-,\' ]{0,80}?)\bagreement', re.I)
B_LAPSE = re.compile(r'\b(?:lapsed?|terminat\w+|not\s+to\s+proceed|will\s+not\s+proceed|ceased\s+to\s+have\s+effect|expired)\b', re.I)
B_MOU = re.compile(r'memorandum\s+of\s+understanding|\bMOU\b', re.I)


def squash_en(s):
    return re.sub(r'[^0-9a-z぀-ヿ一-鿿]+', '', W.nfkc(s).lower())


def load_state():
    if os.path.exists(STATE):
        try:
            return json.load(open(STATE, encoding='utf-8'))
        except Exception:  # noqa
            pass
    return {'items': {}}


def save_state(st):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(st, open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def sync(st, money_dir=None):
    """inbox/money の中の「覚書の段階」の線を目録に足す(すでにあるものは触らない)。足した件数を返す"""
    n = 0
    money_dir = money_dir or os.path.join(W.ROOT, 'inbox', 'money')
    for p in sorted(glob.glob(os.path.join(money_dir, '*.json'))):
        try:
            d = json.load(open(p, encoding='utf-8'))
        except Exception:  # noqa
            continue
        for it in d.get('items', []) if isinstance(d, dict) else []:
            if MOU_MARK not in (it.get('note') or ''):
                continue
            srcs = it.get('src') or []
            if not srcs or len(srcs[0]) < 2:
                continue
            url = srcs[0][1]
            if url in st['items']:
                continue
            st['items'][url] = {'from': it.get('from'), 'to': it.get('to'), 'kind': it.get('kind'), 'date': it.get('date'), 'code': it.get('code', ''),
                                'region': it.get('region', ''), 'url': url, 'src_name': srcs[0][0], 'from_file': os.path.basename(p),
                                'status': '未確認', 'history': []}
            n += 1
    return n


def open_items(st):
    return [v for v in st['items'].values() if v.get('status') == '未確認']


def codes(st):
    return {v['code'] for v in open_items(st) if v.get('code')}


def _day(s):
    try:
        return datetime.date.fromisoformat(str(s)[:10])
    except Exception:  # noqa
        return None


def evaluate(mou, code, day, title, text):
    """1件の発表が、1つの覚書の続きか。(状態, 理由)。状態は '実行' '完了' '失効' か None(関係なし)"""
    d0 = _day(mou.get('date'))
    if not d0 or not day or not (0 < (day - d0).days <= MAX_DAYS):
        return None, '日付が覚書の後でない'
    head = squash_en(text[:2500])
    if mou.get('code'):
        if W.nfkc(code).lstrip('0') != W.nfkc(mou['code']).lstrip('0'):
            return None, '会社が違う'
    else:
        f = squash_en(mou.get('from', ''))
        if not f or f not in head:
            return None, '会社が決められない(記録にコードがなく、本文の先頭に出す側の名前もない)'
    to = squash_en(mou.get('to', ''))
    if not to or to not in squash_en(text):
        return None, '本文に相手の名前がない'
    t = W.nfkc(title)
    body = text[:8000]
    if B_MOU.search(body) and B_LAPSE.search(body) and re.search(r'memorandum[^.]{0,200}?(?:lapse|terminat|expire|not\s+to\s+proceed)|(?:lapse|terminat|expire|not\s+to\s+proceed)[^.]{0,200}?memorandum', body, re.I):
        return '失効', '本文に覚書の失効・終了がある'
    if T_MOU.search(t):
        return None, '表題がまだ覚書・Possible・仮の段階'
    if T_DONE.search(t):
        return '完了', '表題に「完了(Completion)」がある'
    if T_EXEC.search(t) and B_EXEC.search(body):
        return '実行', '表題に契約の締結があり、本文にも「契約を締結した」とある'
    return None, '表題と本文に契約の締結・完了が見つからない'


def observe(st, c, text):
    """hkex_scan.py が開いた1件(c: code, title, url, day, co)を、未確認の覚書すべてと突き合わせる。確認できたものを返す(目録はここで書き換える)"""
    out = []
    for mou in open_items(st):
        if c['url'] == mou['url']:
            continue
        status, why = evaluate(mou, c['code'], c['day'], c['title'], text)
        if not status:
            continue
        label = {'実行': '正式契約を確認', '完了': '完了を確認', '失効': '失効・終了を記録'}[status]
        rec = {'status': label, 'date': str(c['day']), 'title': c['title'], 'url': c['url'], 'why': why}
        mou['status'] = label
        mou['history'].append(rec)
        out.append((mou, rec))
    return out


def followup_money(mou, rec, amount=''):
    """確認できた覚書の続きを、inbox/money に足す線にする(失効は線にしない)"""
    if rec['status'] == '失効・終了を記録':
        return None
    what = '正式な契約の締結' if rec['status'] == '正式契約を確認' else '取引の完了'
    return {'from': mou['from'], 'to': mou['to'], 'kind': mou['kind'], 'amount': amount, 'date': rec['date'], 'region': mou.get('region') or '香港',
            'mark': rec['status'], 'followup_of': mou['url'],
            'note': f"覚書(MOU、{mou['date']})の段階で入れた話の続き。{mou['from']}のHKEXの発表「{rec['title'][:70]}」({rec['date']})で、{what}を確認"
                    f"(PDFを開いて会社・相手の名前・表題と本文の契約の語を照合)。覚書の線({mou['date']})はそのまま残してある。金額は開示書類にある場合のみ記載",
            'src': [[f"HKEX {mou['from']}の開示({rec['date']}、{rec['status']})", rec['url']], [mou.get('src_name', '覚書の発表'), mou['url']]],
            'confidence': '開示'}


def write_followups(items, stamp):
    """足すだけ。同じ出典(1つ目)がすでにあれば足さない。パスを返す"""
    if not items:
        return None
    mp = os.path.join(W.ROOT, 'inbox', 'money', stamp + '-hkex-followup.json')
    md = json.load(open(mp, encoding='utf-8')) if os.path.exists(mp) else {'date': stamp, 'kind': 'money', 'items': []}
    have = {i['src'][0][1] for i in md['items']}
    md['items'] += [m for m in items if m['src'][0][1] not in have]
    json.dump(md, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return mp


def show(st):
    today = datetime.datetime.now(W.JST).date()
    its = list(st['items'].values())
    print(f'覚書の段階の線: {len(its)} 件(未確認 {len(open_items(st))} 件)')
    for v in sorted(its, key=lambda x: str(x.get('date'))):
        d0 = _day(v.get('date'))
        age = (today - d0).days if d0 else None
        flag = ''
        if v['status'] == '未確認' and age is not None and age > STALE_DAYS:
            flag = f'  ← {STALE_DAYS}日を過ぎて未確認(線は残す)'
        print(f"  {v['date']} {v['from']} → {v['to']}({v['kind']}) [{v['status']}]{flag}")
        for h in v['history']:
            print(f"      {h['date']} {h['status']}: {h['title'][:60]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sync', action='store_true')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--pdf')
    ap.add_argument('--code', default='')
    ap.add_argument('--title', default='')
    ap.add_argument('--date', default='')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    st = load_state()
    if a.sync:
        n = sync(st)
        save_state(st)
        print(f'目録に {n} 件足した')
    if a.pdf:
        text, err = W.pdf_text(a.pdf)
        if not text:
            print('開けなかった:', err)
            return
        c = {'code': a.code, 'title': a.title, 'url': a.pdf, 'day': _day(a.date)}
        evs = observe(st, c, text)
        print('確認できた:', [(m['from'], m['to'], r['status']) for m, r in evs] or 'なし')
        if a.apply and evs:
            save_state(st)
            p = write_followups([x for x in (followup_money(m, r) for m, r in evs) if x], a.date or str(datetime.date.today()))
            print('足した:', p)
    show(st)


if __name__ == '__main__':
    main()
