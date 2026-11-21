#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Xで流れる英語のAI新プロジェクトを、日本語の解説つきで見せるページの道具(2026/11/21追加)。

流れ:
  1. find  : Gemini(Google検索つき)で、直近のAI会社の新しい製品・機能・プロジェクトの告知を探す(1日1回・Geminiを1回だけ使う)
             → inbox/xlearn/candidates-日付.json に足す(サイトには出ない。候補)
  2. 確かめ : Claude が候補の元の投稿・公式ページを開いて確かめ(x_check.py や公式ブログ)、
             日本語訳・解説・やり方を書いて inbox/xlearn/items.json に足す(足すだけ・消さない)
  3. build : items.json から site/xlearn/index.html(1枚で完結するページ)を作る

使い方:
  python3 scripts/xlearn.py find [--days 3] [--max 8]
  python3 scripts/xlearn.py check          # items.json の書式と、出典URLが開けるかを確かめる
  python3 scripts/xlearn.py build
"""
import argparse, datetime, html, json, os, re, sys, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'inbox', 'xlearn')
ITEMS = os.path.join(D, 'items.json')
OUT = os.path.join(ROOT, 'site', 'xlearn', 'index.html')
JST = datetime.timezone(datetime.timedelta(hours=9))

def accounts():
    out = []
    for ln in open(os.path.join(ROOT, 'inbox', 'x_accounts.txt'), encoding='utf-8'):
        if ln.startswith('@'):
            out.append(ln.split('|')[0].strip())
    return out

PROMPT = """You are helping a Japanese reader follow AI company announcements that circulate on X (Twitter) in English.
Using Google Search, find up to {n} NEW product / feature / project / model / tool announcements made in the last {days} days (today is {today}) by AI companies
(OpenAI, Anthropic, Google/DeepMind, xAI, Meta, Microsoft, NVIDIA, Mistral, Perplexity, Cursor, Cognition, Hugging Face, etc.).
Prefer things a non-engineer business person could try or care about. For each, give ONLY facts you saw in sources.
Return JSON only:
```json
{{"items":[{{"company":"","title":"short English title","date":"YYYY-MM-DD","what_en":"what it is, 1-2 sentences in English","how_to_try":"how a user can try it if the source says so, else empty","x_post_url":"https://x.com/... only if you actually saw it, else empty","official_url":"official blog/docs/GitHub page URL you saw","news_url":"news article URL you saw"}}]}}
```
Do not invent URLs. Leave a field empty if unsure."""

def find(days, n):
    import gemini_research as g
    today = datetime.datetime.now(JST).strftime('%Y-%m-%d')
    body = {'contents': [{'role': 'user', 'parts': [{'text': PROMPT.format(n=n, days=days, today=today)}]}],
            'tools': [{'google_search': {}}]}
    resp = g.gen(body)
    txt = g.resp_text(resp)
    m = re.search(r'```json\s*(.*?)```', txt, re.S)
    data = json.loads(m.group(1) if m else txt)
    data['grounding'] = g.grounding_sources(resp)
    data['model'] = g.model()
    path = os.path.join(D, f'candidates-{today}.json')
    k = 2
    while os.path.exists(path):
        path = os.path.join(D, f'candidates-{today}-{k}.json'); k += 1
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('候補', len(data.get('items', [])), '件 →', path)

def load():
    return json.load(open(ITEMS, encoding='utf-8')) if os.path.exists(ITEMS) else {'items': []}

REQ = ['id', 'company', 'date', 'title_en', 'title_ja', 'translation_ja', 'what_ja', 'howto', 'sources', 'confidence']

def check():
    st = load(); bad = 0
    for it in st['items']:
        miss = [k for k in REQ if not it.get(k)]
        if miss: print('足りない:', it.get('id'), miss); bad += 1
        for s in it.get('sources', []):
            try:
                req = urllib.request.Request(s[1], headers={'User-Agent': 'Mozilla/5.0 (compatible; relmap-checker)'})
                urllib.request.urlopen(req, timeout=20).read(2000)
            except urllib.error.HTTPError as e:
                print('開けない', e.code, s[1]); bad += 1 if e.code == 404 else 0
            except Exception as e:
                print('開けない', s[1], str(e)[:60])
    print('OK' if not bad else f'要確認 {bad}件'); return bad

def esc(s): return html.escape(str(s or ''))

def card(it):
    srcs = ''.join(f'<a href="{esc(u)}" rel="noopener" target="_blank">{esc(n)}</a>' for n, u in it['sources'])
    steps = ''.join(f'<li>{esc(x)}</li>' for x in it['howto'])
    note = f'<p class="note">{esc(it["howto_note"])}</p>' if it.get('howto_note') else ''
    return f'''<article class="card" data-co="{esc(it['company'])}">
<div class="meta"><span class="co">{esc(it['company'])}</span><span>{esc(it['date'])}</span><span class="cf cf-{esc(it['confidence'])}">{esc(it['confidence'])}</span></div>
<h2>{esc(it['title_ja'])}</h2><p class="en">{esc(it['title_en'])}</p>
<details open><summary>日本語訳(元の投稿・告知)</summary><blockquote>{esc(it['translation_ja'])}</blockquote></details>
<details open><summary>何ができる?(解説)</summary><p>{esc(it['what_ja'])}</p></details>
<details open><summary>試し方・使い方</summary><ol>{steps}</ol>{note}</details>
<div class="src"><b>元の出典:</b> {srcs}</div>
</article>'''

PAGE = '''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>英語のAI新着 日本語解説</title>
<style>
:root{--bg:#f2f4f6;--surface:#fff;--fg:#161b22;--muted:#5d6875;--line:#d5dbe1;--accent:#4a5dd0;--official:#1a7f4b;--report:#9a6700}
@media (prefers-color-scheme:dark){:root{--bg:#11151a;--surface:#1a2027;--fg:#e8ecf0;--muted:#97a3b0;--line:#2e3741;--accent:#8394f5;--official:#4cc38a;--report:#e3b341;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font-family:system-ui,"Noto Sans JP","Hiragino Sans",sans-serif;line-height:1.7;padding:20px max(16px,env(safe-area-inset-left,0px))}
.wrap{max-width:780px;margin:0 auto;display:grid;gap:14px}
h1{margin:0;font-size:24px}.lead{color:var(--muted);margin:0;font-size:14px}
.bar{display:flex;flex-wrap:wrap;gap:6px}.bar button{border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:99px;padding:5px 12px;font:inherit;font-size:13px;cursor:pointer}
.bar button[aria-pressed=true]{border-color:var(--accent);color:var(--accent);font-weight:700}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px;display:grid;gap:8px;overflow-wrap:anywhere}
.card h2{margin:0;font-size:18px}.en{margin:0;color:var(--muted);font-size:13px}
.meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:12px;color:var(--muted)}.co{font-weight:700;color:var(--fg)}
.cf{border:1px solid currentColor;border-radius:99px;padding:0 8px}.cf-公式{color:var(--official)}.cf-報道{color:var(--report)}
summary{cursor:pointer;font-weight:700;font-size:14px;color:var(--accent)}details p,details ol,blockquote{margin:6px 0 0}
blockquote{border-left:3px solid var(--line);padding-left:12px;color:var(--fg)}ol{padding-left:22px}
.note{color:var(--muted);font-size:13px}.src{font-size:13px;color:var(--muted)}.src a{color:var(--accent);margin-right:10px}
.paste{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px}textarea{width:100%;font:inherit;background:var(--bg);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:8px}.paste button{margin-top:6px;border:0;background:var(--accent);color:#fff;border-radius:8px;padding:8px 14px;font:inherit}pre{white-space:pre-wrap;font-size:12px}
.foot{font-size:12px;color:var(--muted)}
</style></head><body><div class="wrap">
<h1>英語のAI新着 日本語解説</h1>
<p class="lead">XなどでAI会社が流す英語の新プロジェクト・新機能を、日本語に訳して「何ができるか」「試し方」をまとめます。更新: __UPDATED__ / 出典つきのものだけ載せています。</p>
<details class="paste"><summary>気になる投稿を貼って、訳・解説してもらう</summary>
<p class="lead">投稿のURLか本文を貼ると、Claude/ChatGPTに渡す依頼文ができます。コピーして貼り付けてください(このページ自体は翻訳できないため)。</p>
<textarea id="pin" rows="4" placeholder="https://x.com/... または英語の本文"></textarea>
<button id="mk">依頼文を作ってコピー</button><pre id="out" hidden></pre></details>
<div class="bar" id="bar"></div>
<div id="list">
__CARDS__
</div>
<p class="foot">訳と解説はAIが作ったものです。「公式」は公式の告知・ページで確かめたもの、「報道」は報道ベースです。やり方は元の出典に書かれている範囲だけを載せています。料金・提供地域は変わるので、必ず元の出典で確かめてください。<br><a href="../index.html" style="color:var(--accent)">← AI企業の相関図へ</a></p>
</div>
<script>
document.getElementById('mk').onclick=function(){var v=document.getElementById('pin').value.trim(),o=document.getElementById('out');if(!v)return;
var t='次のXの投稿(AI関連)を、(1)日本語に訳す (2)何がすごいか・何ができるかを非エンジニア向けに解説 (3)試し方・使い方を、元の出典に書かれている範囲だけで説明、の順で答えてください。確かめられないことは「未確認」と書いてください。\n\n'+v;
o.hidden=false;o.textContent=t;try{navigator.clipboard.writeText(t)}catch(e){}};
(function(){var cs=[].slice.call(document.querySelectorAll('.card')),bar=document.getElementById('bar'),cos=['すべて'];
cs.forEach(function(c){var n=c.dataset.co;if(cos.indexOf(n)<0)cos.push(n)});
cos.forEach(function(n,i){var b=document.createElement('button');b.textContent=n;b.setAttribute('aria-pressed',i==0);
b.onclick=function(){[].forEach.call(bar.children,function(x){x.setAttribute('aria-pressed',x===b)});cs.forEach(function(c){c.hidden=!(i==0||c.dataset.co==n)})};bar.appendChild(b)})})();
</script></body></html>
'''

def build():
    items = sorted(load()['items'], key=lambda x: x['date'], reverse=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    upd = datetime.datetime.now(JST).strftime('%Y/%m/%d')
    open(OUT, 'w', encoding='utf-8').write(PAGE.replace('__UPDATED__', upd).replace('__CARDS__', '\n'.join(card(i) for i in items)))
    print('書き出し:', OUT, len(items), '件')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
    f = sp.add_parser('find'); f.add_argument('--days', type=int, default=3); f.add_argument('--max', type=int, default=8)
    sp.add_parser('check'); sp.add_parser('build')
    a = ap.parse_args()
    if a.cmd == 'find': find(a.days, a.max)
    elif a.cmd == 'check': sys.exit(1 if check() else 0)
    else: build()
