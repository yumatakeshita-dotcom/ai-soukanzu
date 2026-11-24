#!/usr/bin/env python3
"""投稿の下書き用の道具(読むだけ。サイトも inbox も変えない)。
  python3 scripts/post_draft.py genre 2026-12-01     その日のジャンルと材料の置き場を出す
  python3 scripts/post_draft.py pick  2026-12-01     最近の inbox から候補を並べる(古い順に捨てる・保留は除く)
  python3 scripts/post_draft.py check posts/drafts/2026-12-01.md   Xの文字数・出典・確かさの印を確かめる
下書きの文章は Claude が書く(posts/drafts/日付.md)。実際の投稿は人が行う。
Xの数え方: 全角(日本語)は1字=2、半角は1字=1、URLは何文字でも23。無料は280まで(=全角で約128字+URL)。
"""
import sys, json, glob, re, datetime, os, unicodedata
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WD = ['月', '火', '水', '木', '金', '土', '日']
BASE = {0: '人の移籍の線', 1: '共通の線', 2: 'お金の連鎖', 3: '因縁の線', 4: '取引の裏の線', 5: 'この人の経歴', 6: 'おもしろ情報'}   # 2026/11/24 組み替え(docs/post_calendar_2026-12.md の3章)
SRC = {
 '人の移籍の線': ['python3 scripts/career_finder.py diaspora 会社名 / person 名前', 'inbox/moves/日付.json'],
 '共通の線': ['python3 scripts/career_finder.py between A B'],
 'お金の連鎖': ['python3 scripts/career_finder.py coinvest / chains / bridges', 'inbox/money/日付.json'],
 '因縁の線': ['python3 scripts/career_finder.py conflicts / between A B'],
 '取引の裏の線': ['python3 scripts/career_finder.py between A B', 'inbox/money/日付.json'],
 '人材の移籍': ['inbox/moves/日付.json', 'inbox/moves/日付-jp-hr.json'],
 '役員人事': ['site/data/exectl.js (ev)', 'inbox/ir/日付.json', 'inbox/moves/日付-jp-hr.json'],
 'お金の動き': ['inbox/money/日付*.json', 'site/data/invest.js'],
 '資金調達': ['inbox/vc/日付.json', 'inbox/money/日付-jp-fund.json'],
 '提携・協業': ['inbox/money/日付-jp.json', 'inbox/money/日付.json'],
 '買収・出資': ['inbox/ir/日付.json', 'inbox/money/日付-ir.json', 'inbox/disclosures/日付.json'],
 '計算資源・電力': ['inbox/money/日付-dc.json', 'docs/compute_deals_2026-11.html'],
 '採用の動き': ['inbox/moves/日付-hiring.json'],
 'この人の経歴': ['inbox/deep/日付.json', 'site/data/personal.js'],
 'おもしろ情報': ['inbox/fun/日付.json'],
}

def genre(d):
    wk = (d.day - 1) // 7 + 1  # 月の第何週(1〜7日=第1週)
    # カレンダー(docs/post_calendar_2026-12.md)は「12/1始まりの週」で数える。12月は日付の7日区切りと一致する
    g = BASE[d.weekday()]
    return g

def xlen(text):
    text = re.sub(r'https?://\S+', '', text)  # URL は別に23で数える
    n = 0
    for ch in text:
        n += 2 if unicodedata.east_asian_width(ch) in ('W', 'F', 'A') else 1
    return n

def xweight(text):
    urls = re.findall(r'https?://\S+', text)
    return xlen(text) + 23 * len(urls)

def cmd_genre(a):
    d = datetime.date.fromisoformat(a)
    g = genre(d)
    print(f'{a}({WD[d.weekday()]}) → {g}')
    for s in SRC[g]: print('  材料:', s)

def cmd_pick(a):
    d = datetime.date.fromisoformat(a)
    g = genre(d)
    print(f'# {a} {g} の候補(新しい順。出典のページを開いて確かめてから使う)')
    hold = ''
    for f in glob.glob(os.path.join(ROOT, 'inbox/quality/hold-*.md')): hold += open(f, encoding='utf-8').read()
    n = 0
    for f in sorted(glob.glob(os.path.join(ROOT, 'inbox/*/*.json')), reverse=True):
        rel = os.path.relpath(f, ROOT)
        m = re.search(r'(\d{4}-\d{2}-\d{2})', rel)
        if not m or m.group(1) > a: continue
        if (d - datetime.date.fromisoformat(m.group(1))).days > 14: continue
        kind = rel.split('/')[1]
        want = {'人の移籍の線': ['moves'], '共通の線': [], 'お金の連鎖': ['money'], '因縁の線': [], '取引の裏の線': ['money'], '人材の移籍': ['moves'], '役員人事': ['moves', 'ir'], 'お金の動き': ['money'], '資金調達': ['vc', 'money'],
                '提携・協業': ['money'], '買収・出資': ['ir', 'money', 'disclosures'], '計算資源・電力': ['money'],
                '採用の動き': ['moves'], 'この人の経歴': ['deep'], 'おもしろ情報': ['fun']}[g]
        if kind not in want: continue
        try: items = json.load(open(f, encoding='utf-8')).get('items', [])
        except Exception: continue
        for it in items:
            blob = json.dumps(it, ensure_ascii=False)
            url = (re.findall(r'https?://[^"\\ ]+', blob) or [''])[0]
            if url and url in hold: continue
            n += 1
            print(f'- [{rel}] {blob[:420]}')
    if not n: print('(候補なし → 予備ジャンル: おもしろ情報 → この人の経歴)')

def cmd_check(path):
    t = open(path, encoding='utf-8').read()
    ok = True
    for m in re.finditer(r'<!--X(\d*)-->\n(.*?)\n<!--/X-->', t, re.S):
        body = m.group(2).strip()
        w = xweight(body)
        flag = 'OK' if w <= 280 else 'NG(280超え。Premiumなら可)'
        print(f'X{m.group(1) or 1}: {w}/280 {flag}')
        if w > 280: ok = False
        if not re.search(r'https?://', body): print('  ! 出典URLがありません'); ok = False
        if not re.search(r'公式|開示|提出書類|本人|報道|推定', body): print('  ! 確かさの印がありません'); ok = False
        if re.search(r'買い時|上がる|下がる|おすすめ銘柄', body): print('  ! 売買をすすめる言葉'); ok = False
    if '<!--X' not in t: print('X欄(<!--X--> 〜 <!--/X-->)がありません'); ok = False
    if re.search(r'!\[', t): print('  ! 画像の埋め込みがあります(転載しない)'); ok = False
    # note本文の長さ(「## note(本文」から次の「## 出典の一覧」まで。空白を除いて数える。骨子だけの古い下書きには出さない)
    m = re.search(r'## note\(本文.*?\n(.*?)(?=\n## 出典の一覧)', t, re.S)
    if m:
        n = len(re.sub(r'\s', '', m.group(1)))
        print(f'note本文: {n}字', 'OK(2000字以上)' if n >= 2000 else '(2000字未満。土曜の本格版は2000〜4000字にする)')
    print('結果:', 'OK' if ok else '要直し')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else ''
    a = sys.argv[2] if len(sys.argv) > 2 else ''
    {'genre': cmd_genre, 'pick': cmd_pick, 'check': cmd_check}.get(c, lambda _: print(__doc__))(a)
