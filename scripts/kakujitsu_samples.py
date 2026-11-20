# 確かな版の見本集を作り直す(2026/11/20)。使い方: node scripts/kakujitsu_samples.js && python3 scripts/kakujitsu_samples.py → docs/samples/kakujitsu_samples.html
# 確かめた割合が60%以上(出典のある線5件以上)の会社を自動で選ぶ。新しい会社の説明は JA / WHAT に足す
import json,re,html
d=json.load(open('/tmp/kk_samples/kk5.json'));hist=json.loads(re.search(r'=\s*(\[.*\])\s*;',open('site/data/cfhist.js',encoding='utf8').read(),re.S).group(1))[-1];N=len(d);NUM='五六七八九'[0];css=open('/tmp/kk_samples/kkcss.txt').read()
src=open('site/index.html',encoding='utf8').read()
tok=re.search(r'(:root\{.*?color-scheme:dark\}\n)',src,re.S).group(1)
cfc='\n'.join(re.findall(r'\.cf(?:-[a-z])?\{[^}]*\}',src)[:6])
JA={'anthropic':'Anthropic','xai':'xAI','periodic':'Periodic Labs','us_GOOGL':'Alphabet(Google)','cfs':'Commonwealth Fusion Systems','tensorwave':'TensorWave'}
WHAT={'anthropic':'Claudeを作るAI会社。Amazon・Google・Microsoft/Nvidiaの出資、計算資源の契約、人の動き','xai':'イーロン・マスク氏のAI会社。資金調達・Teslaとの取引・人の動き','periodic':'元OpenAI・元Google DeepMindの研究者が作った、AIで新素材を探す会社','us_GOOGL':'Googleの親会社。出資先・計算資源の取引','cfs':'核融合発電の会社。Google・Nvidiaなどが出資','tensorwave':'AMDのGPUを貸し出すクラウドの会社'}
rows=''.join(f'<tr><td><a href="#c-{o["k"]}">{html.escape(JA.get(o["k"],o["name"]))}</a><br><small>{WHAT.get(o["k"],"")}</small></td><td class="num"><b>{o["pct"]}%</b></td><td class="num">{round(o["pct"]*o["tot"]/100)} / {o["tot"]}</td><td><div class="bar"><i style="width:{o["pct"]}%"></i></div></td></tr>' for o in d)
secs=''.join(f'<details class="co" id="c-{o["k"]}"{" open" if i==0 else ""}><summary><span>{html.escape(JA.get(o["k"],o["name"]))}</span><b>{o["pct"]}%</b></summary>{o["html"]}</details>' for i,o in enumerate(d))
page=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>確かな版 見本集</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=Noto+Sans+JP:wght@400;700&display=swap">
<style>
{tok}*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--font-body);font-size:15px;line-height:1.7;padding:24px max(16px,env(safe-area-inset-right)) 56px max(16px,env(safe-area-inset-left))}}
.w{{max-width:860px;margin:0 auto;display:grid;gap:18px;grid-template-columns:minmax(0,1fr)}}
.eb{{font-family:var(--font-mono);font-size:12px;letter-spacing:.12em;color:var(--muted)}}
h1{{font-size:clamp(24px,5vw,34px);line-height:1.3;margin:4px 0 8px;text-wrap:balance}}
h2{{font-size:18px;margin:0 0 10px}}
.lead{{color:var(--muted);margin:0;max-width:62ch}}
.box{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px;min-width:0}}
.big{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}}
.big div{{border:1px solid var(--line);border-radius:10px;padding:12px 14px}}
.big b{{display:block;font-size:30px;line-height:1.1;font-variant-numeric:tabular-nums}}
.big .hi b{{color:var(--active)}}.big small{{color:var(--muted);font-size:13px}}
table{{width:100%;border-collapse:collapse;font-size:14px}}th,td{{text-align:left;padding:8px 6px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font-size:12px;color:var(--muted);font-weight:400}}td small{{color:var(--muted);font-size:12px}}.num{{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}}
td b{{color:var(--active)}}.bar{{height:8px;background:var(--line);border-radius:4px;min-width:60px;margin-top:8px}}.bar i{{display:block;height:100%;background:var(--active);border-radius:4px}}
@media (max-width:520px){{th:last-child,td:last-child{{display:none}}}}
ul.pt{{margin:0;padding-left:20px;display:grid;gap:6px}}
.who{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}}
.who div{{border-left:3px solid var(--invest);padding:2px 0 2px 12px}}.who b{{display:block}}
.co{{background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
.co summary{{display:flex;justify-content:space-between;gap:12px;padding:14px 18px;cursor:pointer;font-weight:700;list-style:none}}
.co summary::-webkit-details-marker{{display:none}}.co summary::before{{content:"▸";color:var(--muted);margin-right:4px}}.co[open] summary::before{{content:"▾"}}
.co summary span{{flex:1}}.co summary b{{color:var(--active);font-variant-numeric:tabular-nums}}
.co .kk-doc{{border:0;border-top:1px solid var(--line);border-radius:0}}
a{{color:var(--invest)}}footer{{font-size:12.5px;color:var(--muted)}}
{cfc}
{css}
</style></head><body><div class="w">
<header><div class="eb">AI企業の相関図 ・ 確かな版 見本集</div>
<h1>うわさと報道を分けた、出典つきの企業のつながり</h1>
<p class="lead">AI企業の出資・取引・人の動きを、会社の公式発表と法定の書類で確かめたものだけ本文に載せ、報道だけのものは「参考」に分けた資料です。全社の中から、確かめられた割合が60%以上になった{N}社をそのまま見本にしました。</p></header>
<section class="box big"><div class="hi"><b>{N}社</b><small>確かめた割合が60%以上(出典のある線が5件以上の会社)</small></div><div><b>{hist["pct"]}%</b><small>相関図全体の平均({hist["tot"]}件のうち{hist["ok"]}件)</small></div><div><b>毎週</b><small>報道だけの数字を、公式発表・開示書類で確かめ直して割合を上げています</small></div></section>
<section class="box"><h2>見本の{N}社</h2><table><thead><tr><th>会社</th><th class="num">確かめた割合</th><th class="num">件数</th><th>割合</th></tr></thead><tbody>{rows}</tbody></table>
<p class="lead" style="margin-top:10px;font-size:13px">件数は「公式・開示(人の動きは本人の投稿も含む)で確かめた件数 / 出典のある線・数字の件数」。{hist["d"].replace("-","/")}時点。</p></section>
<section class="box"><h2>普通のまとめ記事と、どこが違うか</h2><ul class="pt">
<li>線の1本1本に、<i class="cf cf-o">公式</i><i class="cf cf-f">開示</i><i class="cf cf-s">本人</i><i class="cf cf-r">報道</i>の印と出典のURLが付いています</li>
<li>報道だけの数字(契約の上限や「関係者によると」の金額)は本文から外し、参考として分けています。社内資料にそのまま貼っても、出どころを聞かれて困りません</li>
<li>毎朝ニュースを調べて相関図を更新し、毎週日曜に報道だけの数字を確かめ直します。資料はその日の図から自動で作るので、いつでも最新です</li></ul></section>
<section class="box"><h2>使ってほしい人</h2><div class="who">
<div><b>事業会社の調査・企画の担当</b>AI企業との提携や取引先の調査で、出典つきの一覧がすぐ要るとき</div>
<div><b>金融機関・投資の担当</b>出資の連鎖や計算資源の契約を、開示書類ベースで追いたいとき</div>
<div><b>記者・リサーチャー</b>報道と公式の差(どこまでが確定か)を一目で確かめたいとき</div></div></section>
<section><h2 style="margin:6px 0 10px">見本(タップで開く)</h2><div style="display:grid;gap:12px">{secs}</div></section>
<footer>この見本は「AI企業の相関図」の各社の図から自動で作ったものです({hist["d"].replace("-","/")})。報道ベースの数字や契約の上限は、そのように書いています。</footer>
</div><script>document.querySelectorAll('a[href^="#c-"]').forEach(a=>a.addEventListener('click',()=>{{const d=document.getElementById(a.getAttribute('href').slice(1));if(d)d.open=true}}));</script></body></html>'''
open('docs/samples/kakujitsu_samples.html','w').write(page)
print(len(page))
