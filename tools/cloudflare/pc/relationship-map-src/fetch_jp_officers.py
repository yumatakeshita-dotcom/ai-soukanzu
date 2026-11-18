"""日本の時価総額上位企業の役員を、有価証券報告書の「役員の状況」(kabutore.bizが転記している公式の表)から集める。Claude不要。途中から再開できる。
出力: jp_officers.json  {証券コード: {'asof': '2026年６月10日', 'rows': [[役職, 氏名], ...]}}
使い方: python fetch_jp_officers.py [コード ...]   (省略時は ranking_jp.txt の全社)"""
import json, os, re, sys, time, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
OUT = os.path.join(S, 'jp_officers.json')
ROLEKW = re.compile(r'取締役|社長|会長|副|執行|役員|監査|担当|専務|常務|代表|議長|委員|兼|統括|責任者|最高|グループ|本部|事業|部門|室長|長$|CEO|CFO|COO|CTO|CSO|顧問|相談役|名誉|理事|補佐|管掌|担当役')
DATE = re.compile(r'^\d{4}年[\d０-９]+月[\d０-９]+日(生)?$')
END = re.compile(r'^\(注\)|^（注）')


def zen2han(s):
    return s.translate(str.maketrans('０１２３４５６７８９', '0123456789'))


def parse(t):
    x = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    x = re.sub(r'<[^>]+>', '|', x)
    x = x.replace('&nbsp;', ' ')
    toks = [a for a in re.split(r'[\s|]+', x) if a]
    m = re.search(r'(\d{4}年[０-９\d]+月[０-９\d]+日)（有価証券報告書提出日）現在', x)
    asof = m.group(1) if m else ''
    # 役員一覧の表の位置: 「役職名|氏名|生年月日」の後
    try:
        s = next(i for i in range(len(toks) - 2) if toks[i] == '役職名' and toks[i + 1] == '氏名')
    except StopIteration:
        return asof, []
    # このページは過去の年の表も続くので、最新(最初)の表だけを使う
    # 表が複数ページに分かれて見出しが繰り返されるので、次の年の見出し『…（有価証券報告書提出日）現在』で切る
    e = next((k for k in range(s + 3, len(toks)) if '有価証券報告書提出日' in toks[k] and '現在' in ''.join(toks[k:k + 3])), len(toks))
    toks = toks[:e]
    births = [i for i in range(s, len(toks)) if DATE.match(toks[i]) and 1925 <= int(zen2han(toks[i])[:4]) <= 1995]
    rows, prev = [], s + 3
    for bi in births:
        j = bi - 1
        name = []
        while j > prev and len(name) < 6 and len(toks[j]) <= 6 and not ROLEKW.search(toks[j]) and not re.search(r'[（(）)*\d,]', toks[j]):
            name.insert(0, toks[j])
            j -= 1
        role = []
        while j > prev and len(role) < 7 and not re.fullmatch(r'[\d,.]+', toks[j]) and not END.match(toks[j]) and not re.search(r'\d{4}年|略歴|任期|所有株式|^\*', toks[j]):
            role.insert(0, toks[j])
            j -= 1
        if name:
            nm = '・'.join(name) if all(re.fullmatch(r'[ァ-ヴー]+', a) for a in name) and len(name) > 1 else ''.join(name)
            nm = re.sub(r'^[ＣＥＯＦＴＳＩＡＰＭＢ]{3}', '', nm)          # 役職の「ＣＥＯ」などが名前に付いたものを外す
            rl = ''.join(role)[:60]
            for _ in range(3):
                rl = re.sub(r'^([（(][^）)]*[）)]\*?\d?|[－\-]|\*\d)+', '', rl)
            if 2 <= len(nm) <= 14 and ROLEKW.search(rl) and '[' not in nm:
                rows.append([rl, nm])
        prev = bi
    # 同じ人は最初の1回だけ(最新の表が先頭)。人数は「男性○名 女性○名」の合計まで
    m = re.search(r'男性(\d+)名.{0,6}女性(\d+)名', ''.join(toks[s - 40:s]) if s > 40 else ''.join(toks[:s]))
    cap = int(m.group(1)) + int(m.group(2)) if m else 25
    seen, out = set(), []
    for rl, nm in rows:
        if nm in seen:
            continue
        seen.add(nm)
        out.append([rl, nm])
    return asof, out[:max(cap, 5)]


if __name__ == '__main__':
    res = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
    codes = sys.argv[1:] or [ln.split('|')[2] for ln in open(os.path.join(S, 'ranking_jp.txt'), encoding='utf-8')]
    for code in codes:
        if code in res and not sys.argv[1:]:
            continue
        try:
            t = urllib.request.urlopen(urllib.request.Request('https://www.kabutore.biz/genzaikabuka/yakuin.html?code=%s' % code, headers=UA), timeout=60).read().decode('utf-8', 'replace')
        except Exception as e:
            print(code, '失敗', str(e)[:60], flush=True)
            time.sleep(2)
            continue
        asof, rows = parse(t)
        res[code] = {'asof': asof, 'rows': rows}
        print(code, asof, len(rows), rows[:3], flush=True)
        json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        time.sleep(1.5)
