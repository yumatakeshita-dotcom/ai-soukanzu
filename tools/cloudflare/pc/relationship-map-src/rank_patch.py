"""移籍マップ(ラボ)に、会社別の出入りランキングを足す。build_move_lab.py から呼ぶ。"""
CSS = """
.rk{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.rk h3{font-size:14px;margin:0 0 6px}
.rk ol{margin:0;padding:0;list-style:none;display:grid;gap:4px}
.rk li{display:grid;grid-template-columns:1.6em minmax(0,1fr) 3.2em;gap:6px;align-items:center;font-size:13px}
.rk .n{font-family:var(--font-mono);color:var(--muted);font-size:12px}
.rk .bar{position:relative;height:20px;background:var(--bg);border-radius:5px;overflow:hidden}
.rk .bar i{position:absolute;left:0;top:0;bottom:0;border-radius:5px;opacity:.35}
.rk .bar span{position:relative;padding:0 6px;line-height:20px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:block}
.rk .v{text-align:right;font-family:var(--font-mono)}
"""
HTML = '<section class="box"><h2>会社別の出入りランキング</h2><p class="muted" style="margin:0 0 10px;font-size:13px" id="rkn"></p><div class="rk" id="rk"></div></section>'
JS = """
function rankDraw(list){
  const nm=o=>(o==='Google'||o==='Google DeepMind')?'Google(DeepMind含む)':o;
  const inn={},out={};list.forEach(f=>{const b=nm(f.b),a=nm(f.a);inn[b]=(inn[b]||0)+1;out[a]=(out[a]||0)+1});
  const orgs=[...new Set([...Object.keys(inn),...Object.keys(out)])];
  const top=(arr,n)=>arr.sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,n);
  const I=top(orgs.map(o=>[o,inn[o]||0]).filter(x=>x[1]>0),10),O=top(orgs.map(o=>[o,out[o]||0]).filter(x=>x[1]>0),10);
  const N=top(orgs.map(o=>[o,(inn[o]||0)-(out[o]||0)]).filter(x=>x[1]>0),10),L=top(orgs.map(o=>[o,(out[o]||0)-(inn[o]||0)]).filter(x=>x[1]>0),10);
  const P={};list.forEach(f=>{const k=nm(f.a)+' → '+nm(f.b);P[k]=(P[k]||0)+1});const PA=top(Object.entries(P),10);
  const box=(t,a,col)=>{const m=Math.max(1,...a.map(x=>x[1]));return '<div><h3>'+t+'</h3><ol>'+(a.map((x,i)=>'<li><span class="n">'+(i+1)+'</span><span class="bar"><i style="width:'+Math.round(x[1]/m*100)+'%;background:'+col+'"></i><span>'+esc(x[0])+'</span></span><span class="v">'+x[1]+'</span></li>').join('')||'<li><span></span><span class="muted">該当なし</span></li>')+'</ol></div>'};
  const s1=PA[0],s2=N[0],s3=L[0],tot=list.length;
  $('sum').textContent=tot?('要約: この一覧の移籍は'+tot+'件。最も多い流れは「'+(s1?s1[0]+'」('+s1[1]+'人)':'—」')+'。差し引きで最も人が増えたのは'+(s2?s2[0]+'(+'+s2[1]+')':'—')+'、最も減ったのは'+(s3?s3[0]+'(−'+s3[1]+')':'—')+'です。'):'この条件の移籍はありません。';
  $('rkn').textContent=(focus?focus+' に関する移籍だけで集計(会社の選択を外すと全体)。':'')+'人数は、この一覧の移籍(その年まで)の件数です。同じ人が複数回移ると、その回数ぶん数えます。';
  $('rk').innerHTML=box('受け入れた人数が多い会社',I,'var(--active)')+box('出ていった人数が多い会社',O,'var(--left)')+box('差し引きで人が増えた会社',N,'var(--invest)')+box('差し引きで人が減った会社',L,'var(--conflict)')+box('移籍の多い組み合わせ(元 → 先)',PA,'var(--deal)');
}
"""
def apply(html):
    old = "`}\n$('y').oninput"
    assert old in html, 'draw() の末尾が見つかりません'
    html = html.replace(old, "`;rankDraw(list)}\n$('y').oninput", 1)
    html = html.replace('</style>', CSS + '</style>', 1)
    assert '</header>' in html
    html = html.replace('</header>', '<p id="sum" class="lead" style="margin-top:10px;color:var(--fg)"></p></header>', 1)
    assert '<footer>' in html
    html = html.replace('<footer>', HTML + '\n  <footer>', 1)
    assert 'draw();\n</script>' in html
    html = html.replace('draw();\n</script>', JS + 'draw();\n</script>', 1)
    return html
