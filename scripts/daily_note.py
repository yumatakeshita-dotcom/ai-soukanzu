# -*- coding: utf-8 -*-
"""Obsidian のデイリーノート(notes/daily/日付.md)に、その朝の調査の要点を足す。2026/11/27追加

- 材料は「調査の新着」(site/data/finds.js)のうち、その日に足された項目(add=日付)。
  出典があり、品質チェックを通ったものだけが入っているので、ここから短くまとめる
- 注意点として、品質チェックの記録(inbox/quality/日付.md)・取り込みで保留にした候補(inbox/quality/hold-日付.md)・
  企業検索の見張り(inbox/watchdog/kigyo-日付.md)の結果の1行を添える
- ノートの中で Claude が書くのは <!-- AUTO:START --> 〜 <!-- AUTO:END --> の間だけ。
  その外(「自分のメモ」など)は読みも書き換えもしない。ノートが無ければ作る。消さない
- merge_inbox.py(毎朝9:13の取り込み)の最後に動く。手で動かすとき:
    python3 scripts/daily_note.py            今日(日本時間)
    python3 scripts/daily_note.py 2026-11-27 日付を指定
"""
import json, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = '<!-- AUTO:START -->', '<!-- AUTO:END -->'
KIND_LABEL = [
    ('moves', '人材の移籍'),
    ('money', 'お金の流れ(出資・買収・取引)'),
    ('vc', '資金調達・VC'),
    ('world', '世界の企業'),
    ('deep', '深堀りした会社'),
]
MAX_PER_KIND = 8
WD = ['月', '火', '水', '木', '金', '土', '日']


def today_jst():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d')


def load_finds(root):
    p = os.path.join(root, 'site', 'data', 'finds.js')
    if not os.path.exists(p):
        return []
    for line in open(p, encoding='utf-8').read().splitlines():
        if line.startswith('const FINDS='):
            return json.loads(line[len('const FINDS='):].rstrip().rstrip(';'))
    return []


def short(s, n):
    s = re.sub(r'\s+', ' ', str(s or '')).strip()
    return s if len(s) <= n else s[:n - 1] + '…'


def md_text(s):
    # Obsidian でリンクや見出しに化けないように、[ ] と行頭の # をよける
    return s.replace('[', '［').replace(']', '］')


def first_bold(path):
    """記録ファイルの最初の **太字** の1行(結果のひとこと)を返す"""
    if not os.path.exists(path):
        return None
    for line in open(path, encoding='utf-8').read().splitlines():
        m = re.search(r'\*\*(.+?)\*\*(.*)', line)
        if m:
            return re.sub(r'^結果[:：]\s*', '', (m.group(1) + m.group(2)).strip())
    return None


def count_hold(root, day):
    p = os.path.join(root, 'inbox', 'quality', f'hold-{day}.json')
    try:
        return len(json.load(open(p, encoding='utf-8')))
    except Exception:
        return 0


def build_auto(root, day):
    rows = [r for r in load_finds(root) if r.get('add') == day]
    L = [START, '## 今朝の調査の要点(自動)', '',
         f'「調査の新着」に {day} に足された {len(rows)} 件から。出典は各行のリンク。'
         'くわしくはサイトのメニュー「調査の新着」。', '']
    if not rows:
        L += ['- 今朝は新しく足された項目はありませんでした', '']
    for kind, label in KIND_LABEL:
        rs = [r for r in rows if r.get('k') == kind]
        if not rs:
            continue
        L.append(f'### {label}({len(rs)}件)')
        for r in rs[:MAX_PER_KIND]:
            src = (r.get('src') or [[None, None]])[0]
            link = f' [出典]({src[1]})' if src and src[1] else ''
            c = f'〔{r["c"]}〕' if r.get('c') else ''
            t = re.sub(r'^\s*→\s*', '', str(r.get('t') or ''))  # 出す側が空の行の頭の矢印をとる
            L.append(f'- {md_text(short(t, 90))}{c}{link}')
        if len(rs) > MAX_PER_KIND:
            L.append(f'- ほか {len(rs) - MAX_PER_KIND} 件')
        L.append('')
    # 注意点
    notes = []
    q = first_bold(os.path.join(root, 'inbox', 'quality', f'{day}.md'))
    if q:
        notes.append(f'品質チェック: {q}(inbox/quality/{day}.md)')
    h = count_hold(root, day)
    if h:
        notes.append(f'取り込みで保留にした候補: {h} 件(出典・日付の問題。inbox/quality/hold-{day}.md)')
    w = first_bold(os.path.join(root, 'inbox', 'watchdog', f'kigyo-{day}.md'))
    if w:
        notes.append(f'企業検索の見張り: {w}')
    rep = sum(1 for r in rows if r.get('c') == '報道')
    if rep:
        notes.append(f'{rep} 件は報道ベース(公式発表では未確認)')
    L.append('### 注意点')
    L += [f'- {md_text(n)}' for n in notes] or ['- 特になし']
    L += ['', f'_自動で作成: scripts/daily_note.py(この枠の中は毎回書き直します。メモは枠の外へ)_', END]
    return '\n'.join(L)


def write_note(root=ROOT, day=None):
    day = day or today_jst()
    d = os.path.join(root, 'notes', 'daily')
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f'{day}.md')
    auto = build_auto(root, day)
    if os.path.exists(p):
        s = open(p, encoding='utf-8').read()
        if START in s and END in s and s.index(START) < s.index(END):
            s = s[:s.index(START)] + auto + s[s.index(END) + len(END):]
        else:
            s = s.rstrip('\n') + '\n\n' + auto + '\n'  # 人が作ったノートなら末尾に足すだけ
    else:
        dt = datetime.date.fromisoformat(day)
        prev = (dt - datetime.timedelta(days=1)).isoformat()
        s = '\n'.join([
            '---', f'date: {day}', 'tags: [daily]', '---',
            f'# {day}({WD[dt.weekday()]})', '',
            f'前の日: [[{prev}]] / 目次: [[はじめに]]', '',
            '## 自分のメモ', '', '', auto, ''])
    open(p, 'w', encoding='utf-8').write(s)
    return p


def main():
    day = sys.argv[1] if len(sys.argv) > 1 else None
    if day and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', day):
        print('日付は 2026-11-27 の形で'); sys.exit(1)
    p = write_note(ROOT, day)
    print('デイリーノートを書きました:', os.path.relpath(p, ROOT).replace(os.sep, '/'))


if __name__ == '__main__':
    main()
