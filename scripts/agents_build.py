#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""調査エージェント一覧を作る道具(2026/11/21追加)。

docs/agents.json(元データ)から、次の2つを作り直す。何度動かしても同じ結果。
  - docs/agents.md            … 文書版
  - site/agents/index.html    … 画面(メニュー「調査エージェント」から開く。1枚で完結)

使い方:
  python3 scripts/agents_build.py          # 作り直す
  python3 scripts/agents_build.py --check  # 元データの書式を確かめるだけ

係を足すとき: docs/agents.json の agents に足して、このスクリプトを実行する(足すだけ。消さない)。
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'docs', 'agents.json')
MD = os.path.join(ROOT, 'docs', 'agents.md')
OUT = os.path.join(ROOT, 'site', 'agents', 'index.html')
REQ = ['id', 'group', 'name', 'tagline', 'scope', 'sources', 'when', 'outputs', 'limits', 'tasks']


def load():
    d = json.load(open(SRC, encoding='utf-8'))
    ids = set()
    for a in d['agents']:
        miss = [k for k in REQ if k not in a]
        if miss:
            raise SystemExit(f'{a.get("name", "?")}: 足りない項目 {miss}')
        if a['id'] in ids:
            raise SystemExit(f'id が重複: {a["id"]}')
        ids.add(a['id'])
    return d


def timeline(d):
    """タスクの時刻(HH:MM)を拾って、1日の流れにする。"""
    rows = []
    for a in d['agents']:
        for t in a['tasks']:
            m = re.search(r'(\d{1,2}):(\d{2})', t['cron'])
            if not m or not t.get('on', True):
                continue
            hh, mm = int(m.group(1)), int(m.group(2))
            day = t['cron'][:m.start()].strip() or '毎日'
            rows.append((hh * 60 + mm, f'{hh}:{mm:02d}', day, a['name'], t['name']))
    rows.sort()
    return rows


def esc(s):
    return html.escape(str(s), quote=True)


def build_md(d):
    L = ['# 調査エージェント一覧', '',
         f'(元データ: `docs/agents.json`。`python3 scripts/agents_build.py` で作り直す。更新 {d["updated"]})', '',
         '調べる係(エージェント)が分野ごとに inbox/ へ候補を足し、取り込み係が朝9:13にサイトへ足す、という分け方です。',
         '時刻は日本時間。定期タスクの実際の名前・時間は claude.ai の定期タスクが正です。', '', '## 決まり', '']
    L += [f'- {p}' for p in d['principles']]
    for grp in ('調べる係', '運営係'):
        L += ['', f'## {grp}', '']
        for a in d['agents']:
            if a['group'] != grp:
                continue
            L += [f'### {a["name"]}', '', f'{a["tagline"]}', '',
                  f'- 担当範囲: {a["scope"]}',
                  '- 情報源: ' + ' / '.join(a['sources']),
                  f'- 動く時間: {a["when"]}',
                  '- 出力先: ' + '、'.join(f'`{o}`' if '/' in o and ' ' not in o else o for o in a['outputs']),
                  f'- 上限・決まり: {a["limits"]}']
            ts = [t for t in a['tasks'] if t['id']]
            if ts:
                L.append('- 定期タスク: ' + '、'.join(f'{t["name"]}({t["cron"]}、`{t["id"]}`)' for t in ts))
            if a.get('helpers'):
                L.append('- 道具: ' + '、'.join(a['helpers']))
            if a.get('note'):
                L.append(f'- 補足: {a["note"]}')
            L.append('')
    L += ['## 1日の流れ(日本時間)', '', '| 時刻 | 曜日 | 係 | タスク |', '|---|---|---|---|']
    for _, t, day, who, name in timeline(d):
        L.append(f'| {t} | {day} | {who} | {name} |')
    g = d['gemini_budget']
    L += ['', f'## {g["title"]}', '', '| 使い道 | 回数 | 備考 |', '|---|---|---|']
    L += [f'| {r[0]} | {r[1]} | {r[2]} |' for r in g['rows']]
    L += ['', g['note'], '', '## 変更案(まだ実施していません)', '']
    for p in d['proposals']:
        L += [f'### {p["title"]}', '', p['body'], '']
        if p['rows']:
            L += ['| いまの名前 | 案 |', '|---|---|'] + [f'| {r[0]} | {r[1]} |' for r in p['rows']] + ['']
    open(MD, 'w', encoding='utf-8').write('\n'.join(L).rstrip() + '\n')


CSS = """:root{--bg:#f2f4f6;--surface:#fff;--fg:#161b22;--muted:#5d6875;--line:#d5dbe1;--accent:#4a5dd0;--ok:#1a7f4b;--warn:#9a6700}
@media (prefers-color-scheme:dark){:root{--bg:#11151a;--surface:#1a2027;--fg:#e8ecf0;--muted:#97a3b0;--line:#2e3741;--accent:#8394f5;--ok:#4cc38a;--warn:#e3b341;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font-family:system-ui,"Noto Sans JP","Hiragino Sans",sans-serif;line-height:1.7;padding:20px max(16px,env(safe-area-inset-left,0px))}
.wrap{max-width:860px;margin:0 auto;display:grid;gap:14px}
h1{margin:0;font-size:24px}h2{margin:10px 0 0;font-size:19px}.lead{color:var(--muted);margin:0;font-size:14px}
a{color:var(--accent)}.back{font-size:13px}
.bar{display:flex;flex-wrap:wrap;gap:6px}.bar button{border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:99px;padding:5px 12px;font:inherit;font-size:13px;cursor:pointer}
.bar button[aria-pressed=true]{border-color:var(--accent);color:var(--accent);font-weight:700}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px;display:grid;gap:8px;overflow-wrap:anywhere}
.card h3{margin:0;font-size:18px}.tag{margin:0;color:var(--muted);font-size:14px}
.pill{display:inline-block;border:1px solid var(--line);border-radius:99px;padding:1px 10px;font-size:12px;color:var(--muted);margin-right:6px}
.pill.when{color:var(--accent);border-color:var(--accent)}
dl{margin:0;display:grid;grid-template-columns:7em 1fr;gap:4px 10px;font-size:14px}dt{color:var(--muted)}dd{margin:0}
dd ul{margin:0;padding-left:1.1em}code{font-size:12px;background:var(--bg);border-radius:4px;padding:1px 5px;overflow-wrap:anywhere}
.note{font-size:13px;color:var(--warn)}
.box{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px;font-size:14px}
.box ul{margin:6px 0 0;padding-left:1.2em}
.scroll{overflow-x:auto;background:var(--surface);border:1px solid var(--line);border-radius:12px}
table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;padding:6px 10px;border-bottom:1px solid var(--line);vertical-align:top}th{color:var(--muted);font-weight:600;white-space:nowrap}td:first-child{white-space:nowrap}
.prop{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 16px;font-size:14px}.prop h3{margin:0 0 4px;font-size:15px}.prop p{margin:0 0 6px}
@media (max-width:520px){dl{grid-template-columns:1fr}dt{margin-top:4px}}"""

JS = """const bar=document.getElementById('bar');const cards=[...document.querySelectorAll('.card')];
bar.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
[...bar.children].forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
const g=b.dataset.g;cards.forEach(c=>{c.hidden=!(g==='all'||c.dataset.g===g)})});"""


def li(items, code=False):
    return '<ul>' + ''.join(f'<li>{"<code>" + esc(i) + "</code>" if code and "/" in i and " " not in i else esc(i)}</li>' for i in items) + '</ul>'


def build_html(d):
    cards = []
    for a in d['agents']:
        ts = [t for t in a['tasks'] if t['id']]
        rows = [('担当範囲', esc(a['scope'])), ('情報源', li(a['sources'])), ('動く時間', esc(a['when'])),
                ('出力先', li(a['outputs'], True)), ('上限・決まり', esc(a['limits']))]
        if ts:
            rows.append(('定期タスク', li([f'{t["name"]}({t["cron"]})' for t in ts])))
        if a.get('helpers'):
            rows.append(('道具', li(a['helpers'], True)))
        dl = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows)
        note = f'<p class="note">補足: {esc(a["note"])}</p>' if a.get('note') else ''
        cards.append(f'<section class="card" id="{esc(a["id"])}" data-g="{esc(a["group"])}">'
                     f'<h3>{esc(a["name"])}</h3><p class="tag">{esc(a["tagline"])}</p>'
                     f'<div><span class="pill">{esc(a["group"])}</span><span class="pill when">{esc(a["when"].split("/")[0].strip())}</span></div>'
                     f'<dl>{dl}</dl>{note}</section>')
    tl = ''.join(f'<tr><td>{t}</td><td>{esc(day)}</td><td>{esc(who)}</td><td>{esc(name)}</td></tr>' for _, t, day, who, name in timeline(d))
    g = d['gemini_budget']
    gb = ''.join(f'<tr><td>{esc(r[0])}</td><td>{esc(r[1])}</td><td>{esc(r[2])}</td></tr>' for r in g['rows'])
    props = []
    for p in d['proposals']:
        tb = ''
        if p['rows']:
            tb = '<div class="scroll"><table><tr><th>いまの名前</th><th>案</th></tr>' + ''.join(f'<tr><td style="white-space:normal">{esc(r[0])}</td><td style="white-space:normal">{esc(r[1])}</td></tr>' for r in p['rows']) + '</table></div>'
        props.append(f'<div class="prop"><h3>{esc(p["title"])}</h3><p>{esc(p["body"])}</p>{tb}</div>')
    n_r = sum(1 for a in d['agents'] if a['group'] == '調べる係')
    n_o = sum(1 for a in d['agents'] if a['group'] == '運営係')
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>調査エージェント一覧</title>
<style>{CSS}</style></head><body><div class="wrap">
<a class="back" href="../index.html">← 相関図にもどる</a>
<h1>調査エージェント一覧</h1>
<p class="lead">毎日の調べ物を、分野ごとの「係」に分けて見せるページです。調べる係が {n_r} つ、サイトに足したり見張ったりする運営係が {n_o} つ。時刻は日本時間。更新 {esc(d['updated'])}(元データ <code>docs/agents.json</code>)。</p>
<div class="box"><b>決まり</b>{li(d['principles'])}</div>
<div class="bar" id="bar"><button type="button" data-g="all" aria-pressed="true">すべて</button><button type="button" data-g="調べる係" aria-pressed="false">調べる係({n_r})</button><button type="button" data-g="運営係" aria-pressed="false">運営係({n_o})</button></div>
{''.join(cards)}
<h2>1日の流れ(日本時間)</h2>
<div class="scroll"><table><tr><th>時刻</th><th>曜日</th><th>係</th><th>タスク</th></tr>{tl}</table></div>
<h2>{esc(g['title'])}</h2>
<div class="scroll"><table><tr><th>使い道</th><th>回数</th><th>備考</th></tr>{gb}</table></div>
<p class="lead">{esc(g['note'])}</p>
<h2>変更案(まだ実施していません)</h2>
{''.join(props)}
</div><script>{JS}</script></body></html>
"""


def main():
    d = load()
    if '--check' in sys.argv:
        print(f'OK: 係 {len(d["agents"])}、変更案 {len(d["proposals"])}')
        return
    build_md(d)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(build_html(d))
    print('作りました:', os.path.relpath(MD, ROOT), os.path.relpath(OUT, ROOT))


if __name__ == '__main__':
    main()
