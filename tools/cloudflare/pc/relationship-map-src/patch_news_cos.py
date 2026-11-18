p = 'hub_template.html'
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


rep("const YNEWS=/*YNEWS*/{};", "const YNEWS=/*YNEWS*/{};\nconst GNEWS=/*GNEWS*/{};      /* 会社ごとのニュース(Googleニュース経由。日経・ロイター・TechCrunchなど) */")
# 会社ごとのニュースを、Yahoo!ニュースと他のサイトを合わせて新しい順に
rep("function yNewsHtml(name){\n  const rows=YNEWS[name]||YNEWS[(name||'').replace(/\\s*[\\(（].*?[\\)）]/g,'')];",
    """function coNews(name){
  const k=n=>YNEWS[n]||[],g=n=>GNEWS[n]||[];const nm2=(name||'').replace(/\\s*[\\(（].*?[\\)）]/g,'');
  const all=[...k(name),...k(nm2),...g(name),...g(nm2)];const seen=new Set(),out=[];
  all.sort((a,b)=>b[0].localeCompare(a[0])).forEach(r=>{const key=r[1].replace(/[\\s　「」『』、。,.\\-]/g,'').slice(0,18);if(seen.has(key))return;seen.add(key);out.push(r)});
  return out.slice(0,8);
}
function yNewsHtml(name){
  const rows=coNews(name);""")
rep("最近のニュース(Yahoo!ニュース)</h3><ul class=\"rel\">${rows.slice(0,4)", "最近のニュース(Yahoo!ニュース・日経・ロイターなど)</h3><ul class=\"rel\">${rows.slice(0,6)")
# AI
rep("      Object.keys(YNEWS).forEach(nm=>{const nl=nm.toLowerCase();if(lo.some(t=>nl===t||(t.length>=3&&nl.includes(t))||(nl.length>=3&&t.includes(nl))))YNEWS[nm].slice(0,5).forEach(r=>{const x=`Yahoo!ニュース ${r[0]} ${nm}: ${r[1]} (${r[3]})`;if(!seen.has(x)){seen.add(x);lines.unshift(x)}})});",
    "      [...new Set([...Object.keys(YNEWS),...Object.keys(GNEWS)])].forEach(nm=>{const nl=nm.toLowerCase();if(lo.some(t=>nl===t||(t.length>=3&&nl.includes(t))||(nl.length>=3&&t.includes(nl))))coNews(nm).slice(0,6).forEach(r=>{const x=`ニュース ${r[0]} ${nm}: ${r[1]} (${r[3]})`;if(!seen.has(x)){seen.add(x);lines.unshift(x)}})});")
rep("const yn=(YNEWS[C.name]||[]).slice(0,5)", "const yn=coNews(C.name).slice(0,6)")
rep("最近のYahoo!ニュース:", "最近のニュース(Yahoo!ニュース・他のニュースサイト):")
rep("最近のニュースは、毎日集めているYahoo!ニュースの見出しを根拠にします。", "最近のニュースは、毎日集めているYahoo!ニュースや日経・ロイターなどの見出しを根拠にします。")
open(p, 'w', encoding='utf-8').write(s)

q = 'inject_pauto.py'
t = open(q, encoding='utf-8').read()
a = "('const YNEWS=/*YNEWS*/{};', 'yahoo_cos.json', '{}'))"
assert a in t
t = t.replace(a, "('const YNEWS=/*YNEWS*/{};', 'yahoo_cos.json', '{}'), ('const GNEWS=/*GNEWS*/{};', 'news_cos.json', '{}'))", 1)
open(q, 'w', encoding='utf-8').write(t)
r = open('refresh.py', encoding='utf-8').read()
b = "    run('-I', 'fetch_yahoo_cos.py')"
assert b in r and 'fetch_news_cos' not in r
i = r.index(b)
j = r.index('\n', i)
r = r[:j] + "\n    run('-I', 'fetch_news_cos.py')      # 会社ごとのニュース(Googleニュース経由。日経・ロイターなど)" + r[j:]
open('refresh.py', 'w', encoding='utf-8').write(r)
print('ok')
