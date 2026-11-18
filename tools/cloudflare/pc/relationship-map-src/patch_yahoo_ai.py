import re
p = 'hub_template.html'
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


# 1) データの置き場
rep("const NEWS=/*NEWS*/[];", "const NEWS=/*NEWS*/[];\nconst YNEWS=/*YNEWS*/{};      /* 会社ごとのYahoo!ニュース {会社名:[[日付,見出し,URL,配信元],…]} */")
# 2) 会社の概要パネルに「最近のニュース」
rep("  ${acqBtn()}${vcBtn()}`;\n  wireAcq();wireVc();", "  ${yNewsHtml(COMPANIES[comp].name)}${acqBtn()}${vcBtn()}`;\n  wireAcq();wireVc();")
rep("function renderOverview(){", r"""function yNewsHtml(name){
  const rows=YNEWS[name]||YNEWS[(name||'').replace(/\s*[\(（].*?[\)）]/g,'')];
  if(!rows||!rows.length)return '';
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  return `<h3 style="margin:14px 0 6px;font-size:14px">最近のニュース(Yahoo!ニュース)</h3><ul class="rel">${rows.slice(0,4).map(r=>`<li><b>${esc(r[0].slice(5).replace('-','/'))}</b><a href="${esc(r[2])}" target="_blank" rel="noopener">${esc(r[1].slice(0,60))}</a> <span style="color:var(--muted)">${esc(r[3])}</span></li>`).join('')}</ul>`;
}
function renderOverview(){""")
# 3) 「AIに聞く」: 開いているページの会社のYahoo!ニュースと、質問の語に合う会社のYahoo!ニュースを根拠に足す
rep("    return lines.join('\\n').slice(0,14000);\n", r"""    try{
      Object.keys(YNEWS).forEach(nm=>{const nl=nm.toLowerCase();if(lo.some(t=>nl===t||(t.length>=3&&nl.includes(t))||(nl.length>=3&&t.includes(nl))))YNEWS[nm].slice(0,5).forEach(r=>add(`Yahoo!ニュース ${r[0]} ${nm}: ${r[1]} (${r[3]})`))});
    }catch(e){}
    return lines.join('\n').slice(0,14000);
""")
rep("    const body=`会社: ${C.name||comp}\\n注記:", "    const yn=(YNEWS[C.name]||[]).slice(0,5).map(r=>`${r[0]} ${r[1]} (${r[3]})`).join('\\n');\n    const body=`会社: ${C.name||comp}\\n注記:")
rep("右パネルに開いている内容:\\n${txt(panel)}`;", "${yn?`\\n最近のYahoo!ニュース:\\n${yn}\\n`:''}\\n右パネルに開いている内容:\\n${txt(panel)}`;")
# 4) AIの案内文
rep("質問のたびにあなたのClaude利用枠を使います", "最近のニュースは、毎日集めているYahoo!ニュースの見出しを根拠にします。質問のたびにあなたのClaude利用枠を使います")
open(p, 'w', encoding='utf-8').write(s)

q = 'inject_pauto.py'
t = open(q, encoding='utf-8').read()
a = "('const RELNEWS=/*RELNEWS*/[];', 'relation_news.json', '[]'))"
assert a in t
t = t.replace(a, "('const RELNEWS=/*RELNEWS*/[];', 'relation_news.json', '[]'), ('const YNEWS=/*YNEWS*/{};', 'yahoo_cos.json', '{}'))", 1)
open(q, 'w', encoding='utf-8').write(t)

r = open('refresh.py', encoding='utf-8').read()
b = "    run('-I', 'fetch_yahoo.py')\nrun('build_hub2.py')"
if 'fetch_yahoo_cos' not in r:
    assert "    run('-I', 'fetch_yahoo.py')" in r
    i = r.rfind("    run('-I', 'fetch_yahoo.py')")
    r = r[:i] + "    run('-I', 'fetch_yahoo.py')\n    run('-I', 'fetch_yahoo_cos.py')      # 会社ごとのYahoo!ニュース(1,800社ほど。時間がかかる)" + r[i + len("    run('-I', 'fetch_yahoo.py')"):]
    open('refresh.py', 'w', encoding='utf-8').write(r)
print('ok')
