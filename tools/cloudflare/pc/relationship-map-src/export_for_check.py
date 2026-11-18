"""相関図のデータを、GeminiやChatGPTに渡して確認してもらうための Markdown に書き出す。Claude不要。
出力: C:\\Users\\yumat\\.claude\\output\\gemini-check\\ (日本企業を40社ずつ + ユニコーン + 質問文)
使い方: python export_for_check.py"""
import os, re, sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import newco_data8 as D

OUT = r'C:\Users\yumat\.claude\output\gemini-check'
os.makedirs(OUT, exist_ok=True)
KIND = {'p': '人物', 'i': '株主・出資者', 'o': '関連組織', 'c': '会社'}


def clip(s, n=140):
    s = re.sub(r'\s+', ' ', s or '').strip()
    return s if len(s) <= n else s[:n] + '…'


def section(title, co, extra=''):
    N = co['N']
    c = next(n for n in N if n['id'] == co['center'])
    lines = ['## %s' % title, '', clip(c['desc'], 300), '']
    if extra:
        lines += [extra, '']
    lines += ['| 区分 | 名前 | 役職・関係 | 年 | 根拠・注記 |', '|---|---|---|---|---|']
    for n in N:
        if n['id'] == co['center']:
            continue
        d = n.get('desc', '')
        if d.startswith('大株主の第'):
            d = re.sub(r'。.*', '', d)                       # 「大株主の第N位(持株比率…)」だけ
        elif d.startswith('有価証券報告書の「役員の状況」'):
            d = '有価証券報告書(自動抽出)'
        elif d.startswith('Wikidataの'):
            d = 'Wikidata'
        lines.append('| %s | %s | %s | %s | %s |' % (KIND.get(n['kind'], n['kind']), n['name'], clip(n.get('role', ''), 50), n.get('from', ''), clip(d, 110)))
    return '\n'.join(lines) + '\n'


jp = [(r['code'], r['name'], r['key']) for r in D.JPCO if r['key'].startswith('jp_')]
HEAD = ('# %s\n\n日本の時価総額ランキング上位企業の「役員・大株主」データです(2026年11月5日時点で自動収集・一部は手作業で確認)。\n'
        '役職・氏名・持株比率に、誤りや古い情報がないか確認してください。\n\n---\n\n')
files = []
for part, i in enumerate(range(0, len(jp), 40), 1):
    chunk = jp[i:i + 40]
    txt = HEAD % ('日本企業の相関図データ その%d(%d〜%d社目)' % (part, i + 1, i + len(chunk)))
    for code, name, key in chunk:
        txt += section('%s(証券コード %s)' % (name, code), D.CO8[key]) + '\n'
    fn = os.path.join(OUT, 'japan_%d.md' % part)
    open(fn, 'w', encoding='utf-8').write(txt)
    files.append((fn, len(chunk)))
uni = [r for r in D.JPCO if r['key'].startswith('un_')]
txt = '# ユニコーン(未上場の評価額10億ドル以上)の相関図データ\n\n英語版Wikipediaの一覧とWikidataから自動で集めた創業者・CEO・株主です。誤りがないか確認してください。\n\n---\n\n'
for r in uni:
    txt += section(r['name'], D.CO8[r['key']]) + '\n'
fn = os.path.join(OUT, 'unicorns.md')
open(fn, 'w', encoding='utf-8').write(txt)
files.append((fn, len(uni)))
prompt = """添付のMarkdownは、企業の「人物・役職・株主」の一覧です(2026年11月5日時点で自動収集したものです)。次の点を確認してください。

1. 各会社の「役職・氏名」が、現在(2026年11月時点)の公式情報と合っているか。違う、または古い箇所を一覧にしてください。
2. 大株主の持株比率が、最新の有価証券報告書(または公式の開示)と大きく食い違っていないか。
3. 重要な人物が抜けていないか(会長、社長、CEO、創業者など)。
4. 確認できなかった項目は「確認できず」と書き、推測で埋めないでください。
5. 回答は、会社ごとに「問題なし / 修正が必要 / 確認できず」で分け、修正が必要なものには、根拠(出典のURLなど)を付けてください。

一度に全部が難しければ、最初の5社だけ確認してください。"""
open(os.path.join(OUT, '00_Geminiへの質問文.txt'), 'w', encoding='utf-8').write(prompt)
for fn, n in files:
    print(os.path.basename(fn), n, '社', os.path.getsize(fn) // 1024, 'KB')
