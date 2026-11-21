#!/usr/bin/env python3
"""Geminiの調べ方の履歴(目次)を作る。足すだけ・元の記録は書き換えない(2026/11/20)

読むもの: inbox/gemini/ の 日付.json(調査の結果と process=検索の言葉・見たページ)、
          日付_verified.json(確かめの結果)、日付_process_raw.json(試しに残した生の返答)
作るもの: inbox/gemini/README.md(日付ごとの目次) と inbox/gemini/history.html(見やすい版。共有リンクに公開する)
使い方:   python3 scripts/gemini_history.py
"""
import glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GDIR = os.path.join(ROOT, 'inbox', 'gemini')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def load(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return None


def runs():
    out = []
    for p in sorted(glob.glob(os.path.join(GDIR, '*.json'))):
        b = os.path.basename(p)[:-5]
        if b.endswith('_verified') or b == 'verified':
            continue
        d = load(p)
        if not isinstance(d, dict):
            continue
        if b.endswith('_raw'):  # 試しに残した生の返答 → 同じ形に直す
            if 'candidates' not in d:
                continue
            import gemini_research as gr
            pr = gr.process_info(d)
            txt = gr.resp_text(d)
            items = gr.parse_items(txt)
            pm = os.path.join(GDIR, b[:-4] + '.md')
            topic = ''
            if os.path.exists(pm):
                m = re.search(r'テーマ:\s*(.+)', open(pm, encoding='utf-8').read())
                topic = m.group(1).strip() if m else ''
            out.append({'id': b, 'date': b[:10], 'topic': topic or '(手動の試し)', 'model': '', 'items': items, 'process': pr,
                        'note': '試しに生の返答をそのまま残した記録'})
            continue
        if d.get('kind') != 'gemini':
            continue
        v = load(os.path.join(GDIR, b + '_verified.json')) or {}
        d = dict(d)
        d['id'] = b
        d['verify'] = v.get('results') or []
        out.append(d)
    return out


def esc(s):
    return html.escape(str(s or ''))


def state_of(it, verify):
    for r in verify:
        x = r.get('item') or {}
        if x.get('会社名') == it.get('会社名') and x.get('相手') == it.get('相手') and x.get('日付') == it.get('日付'):
            return r.get('verdict') or r.get('判定') or ''
    return ''


def to_md(rs):
    L = ['# Geminiの調べ方の履歴', '',
         'Gemini API で調べたときに、Geminiが**自分で打った検索の言葉**、**見たページ**、**出てきた候補**を日付ごとに並べた目次です。',
         'GeminiアプリやNotebookLMの履歴には出ないため、ここに残しています(`python3 scripts/gemini_history.py` で自動で作り直し)。',
         '見やすい版: inbox/gemini/history.html(共有リンクにも公開)', '']
    for r in sorted(rs, key=lambda x: x['id'], reverse=True):
        p = r.get('process') or {}
        L += [f"## {r['id']}　{r.get('topic','')}", '', f"- モデル: {r.get('model') or '(不明)'}　/　候補 {len(r.get('items') or [])}件" + (f"　/　{r['note']}" if r.get('note') else ''), '']
        if p.get('queries'):
            L += ['**Geminiが打った検索の言葉**', ''] + [f'- {q}' for q in p['queries']] + ['']
        else:
            L += ['**Geminiが打った検索の言葉**: (この回は記録なし)', '']
        srcs = r.get('grounding') or p.get('sources') or []
        if srcs:
            L += ['**見たページ**', ''] + [f'- [{t}]({u})' for t, u in srcs[:20]] + ['']
        if r.get('items'):
            L += ['**出てきた候補**', '']
            for it in r['items']:
                st = state_of(it, r.get('verify') or [])
                L.append(f"- {it.get('会社名','')} → {it.get('関係','')} → {it.get('相手','')}({it.get('日付','')})" + (f"【{st}】" if st else ''))
            L.append('')
        L.append(f"記録ファイル: inbox/gemini/{r['id']}.json" + (f" / {r['id']}.md" if os.path.exists(os.path.join(GDIR, r['id'] + '.md')) else ''))
        L.append('')
    return '\n'.join(L)


CSS = ('''<style>
:root{--bg:#f2f4f6;--surface:#fff;--fg:#161b22;--muted:#5d6875;--line:#d5dbe1;--accent:#4a5dd0;--ok:#1a7f4b;--ng:#b3261e}
@media (prefers-color-scheme:dark){:root{--bg:#11151a;--surface:#1a2027;--fg:#e8ecf0;--muted:#97a3b0;--line:#2e3741;--accent:#8394f5;--ok:#5fd39a;--ng:#ff8a80;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font-family:"Noto Sans JP",system-ui,sans-serif;line-height:1.6;padding:20px 16px}
.wrap{max-width:900px;margin:0 auto;display:grid;gap:14px}h1{margin:0;font-size:24px}p,.m{color:var(--muted);margin:0;font-size:14px}
details{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px}summary{cursor:pointer;font-weight:700;overflow-wrap:anywhere}
h3{font-size:13px;color:var(--muted);margin:14px 0 4px}ul{margin:0;padding-left:20px}li{overflow-wrap:anywhere;font-size:14px}
a{color:var(--accent)}.q{display:inline-block;background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:2px 10px;margin:2px 4px 2px 0;font-size:13px}
.ok{color:var(--ok);font-weight:700}.ng{color:var(--ng);font-weight:700}
</style>''')


def to_html(rs):
    B = []
    for i, r in enumerate(sorted(rs, key=lambda x: x['id'], reverse=True)):
        p = r.get('process') or {}
        qs = ''.join(f'<span class="q">{esc(q)}</span>' for q in p.get('queries') or []) or '<span class="m">この回は記録なし</span>'
        srcs = r.get('grounding') or p.get('sources') or []
        sl = ''.join(f'<li><a href="{esc(u)}" rel="noopener">{esc(t)}</a></li>' for t, u in srcs[:20]) or '<li class="m">なし</li>'
        il = ''
        for it in r.get('items') or []:
            st = state_of(it, r.get('verify') or [])
            cls = 'ok' if st == '合格' else ('ng' if st == '除外' else '')
            il += f"<li>{esc(it.get('会社名'))} → {esc(it.get('関係'))} → {esc(it.get('相手'))}({esc(it.get('日付'))}) " + (f'<span class="{cls}">{esc(st)}</span>' if st else '') + '</li>'
        B.append(f'<details{" open" if i == 0 else ""}><summary>{esc(r["id"])}　{esc(r.get("topic"))}</summary>'
                 f'<p>モデル: {esc(r.get("model") or "不明")} / 候補 {len(r.get("items") or [])}件{(" / " + esc(r["note"])) if r.get("note") else ""}</p>'
                 f'<h3>Geminiが打った検索の言葉</h3><div>{qs}</div><h3>見たページ</h3><ul>{sl}</ul><h3>出てきた候補</h3><ul>{il or "<li class=m>なし</li>"}</ul></details>')
    return ('<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Gemini調査の履歴</title>' + CSS + '</head><body><div class="wrap"><h1>Gemini調査の履歴</h1>'
            '<p>Gemini API の調査で、Geminiが打った検索の言葉・見たページ・出てきた候補を日付ごとに残しています。毎朝8:23の調査のあとに自動で増えます。</p>'
            + ''.join(B) + '</div></body></html>')


def build():
    rs = runs()
    open(os.path.join(GDIR, 'README.md'), 'w', encoding='utf-8').write(to_md(rs))
    open(os.path.join(GDIR, 'history.html'), 'w', encoding='utf-8').write(to_html(rs))
    print(f'履歴 {len(rs)}回分: inbox/gemini/README.md と inbox/gemini/history.html を作りました')
    return rs


if __name__ == '__main__':
    build()
