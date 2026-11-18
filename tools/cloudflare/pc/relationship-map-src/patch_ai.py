p = 'hub_template.html'
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:60]
    s = s.replace(a, b, 1)


rep(r"""  function siteSearch(q){
    const toks=new Set();""", r"""  function siteSearch(q,extra){
    const toks=new Set();(extra||[]).forEach(t=>{t=String(t||'').trim();if(t.length>=2&&t.length<=40)toks.add(t)});""")
rep(r"const T=[...toks].filter(t=>t.length>=2&&!STOP.has(t)).slice(0,14);", r"const T=[...toks].filter(t=>t.length>=2&&!STOP.has(t)).slice(0,24);")
rep(r"const add=s=>{if(!seen.has(s)&&lines.length<70){", r"const add=s=>{if(!seen.has(s)&&lines.length<140){")
more = r"""    /* 6) ユニコーン・Y Combinator・日本のスタートアップ・ニュース・提携ニュース・全企業リスト・人物(全体)も探す */
    try{
      const hit=s=>lo.some(t=>s.toLowerCase().includes(t));
      UNI.forEach(u=>{if(hit(u.n+' '+(u.i||'')+' '+u.f.map(f=>f.n).join(' ')))add(`ユニコーン ${u.n}: 評価額 約${u.v}十億ドル 時期 ${u.d||''} 分野 ${u.i||''} 国 ${(u.c||[]).join('/')} 創業者 ${u.f.map(f=>f.n).join('、')}`)});
      YCS.forEach(r=>{if(hit(r[0]+' '+r[4]))add(`Y Combinator ${r[3]} ${r[0]}(${r[2]}) ${r[5]||''} ${r[6]||''}: ${(r[4]||'').slice(0,120)}`)});
      JPSU.forEach(r=>{if(hit(r.n+' '+(r.rep||'')+' '+(r.ind||'')))add(`日本のスタートアップ ${r.n}: ${[r.mkt,r.ind,r.est?'設立'+r.est:'',r.hq,r.rep?'代表 '+r.rep:'',(r.vcs||[]).length?'VC '+r.vcs.slice(0,5).join('・'):''].filter(Boolean).join(' / ')}`)});
      NEWS.forEach(n=>{if(hit(n.t+' '+(n.cn||'')))add(`ニュース ${n.d} ${n.s}: ${n.t}${n.cn?' [会社 '+n.cn+(n.rd?' '+n.rd:'')+']':''}${n.a?' '+n.a:''}`)});
      RELNEWS.forEach(n=>{if(hit(n.t))add(`提携・買収ニュース ${n.d} ${n.s}: ${n.t}`)});
      if(allState.data)allState.data.rows.forEach(r=>{if(lines.length<140&&hit(r[0]+' '+r[1]))add(`企業 ${r[0]}${r[1]?'('+r[1]+')':''} ${r[2]||''} ${r[3]||''}${r[4]?' 設立'+r[4]:''}`)});
      if(typeof WPALL!=='undefined'&&WPALL)WPALL.forEach(p=>{if(hit(p.en+' '+p.ja))add(`人物 ${p.ja||p.en}(${p.en}): ${p.roles.slice(0,4).map(x=>x[0]+' '+(WPRL[x[1]]||x[1])).join(' / ')}${p.d?' - '+p.d:''}${p.x?' '+p.x.slice(0,200):''}`)});
    }catch(e){}
    return lines.join('\n').slice(0,14000);
"""
rep("    return lines.join('\\n').slice(0,9000);\n", more)
rep(r"""    const hits=siteSearch(q);
    const input=""", r"""    let extra=[];
    try{out.textContent='調べています…';
      const k=await sample([{role:'user',content:'次の質問に答えるため、企業・人物データベースを検索する語を選んでください。質問に出る固有名詞(会社・人物・製品)の英語表記と日本語表記、別名、関係しそうな親会社・子会社・投資家名を最大12語、JSONの文字列配列だけで返してください。説明は不要。\n質問: '+q}],{cache:false,signal:ctl.signal});
      const m=(k.text||'').match(/\[[\s\S]*\]/);if(m)extra=JSON.parse(m[0]).filter(x=>typeof x==='string').slice(0,12);
    }catch(e){if(e&&e.code==='cancelled')throw e}
    out.textContent='考え中…';
    const hits=siteSearch(q,extra);
    const input=""")
rep("    ctl=new AbortController();\n    try{\n      const r=await sample(input", "    try{\n      const r=await sample(input")
rep("    const c=ctxNow();\n    turns.push({role:'user',content:q});", "    ctl=new AbortController();\n    const c=ctxNow();\n    turns.push({role:'user',content:q});")
# open: preload bulk + people
rep("btn.addEventListener('click',()=>{pn.hidden=false;btn.hidden=true;chips();$('aiq').focus()});", "btn.addEventListener('click',()=>{pn.hidden=false;btn.hidden=true;chips();$('aiq').focus();try{if(typeof wpLoad==='function')wpLoad();if(typeof allLoad==='function')allLoad(()=>{})}catch(e){}});")
# prompt
rep(r"- 質問が広いときは、要点を3〜5個にまとめ、最後に「もっと詳しく知りたい点」を1つ提案する。';", r"- 質問が広いときは、要点を3〜5個にまとめ、最後に「もっと詳しく知りたい点」を1つ提案する。\n- 答える前に、質問の中身(誰が・どの会社が・いつ・いくら)を整理し、検索結果の複数の記録を突き合わせて答える。例: 親会社→子会社→創業者の順にたどる、金額は最新の記録を優先する、記録どうしが食い違うときは両方書く。\n- 根拠はサイトの記録なら「(サイトの記録: 買収・子会社/ニュース/ユニコーン…)」のように短く出どころを添える。\n- 比較・ランキング・一覧の質問は、表のように箇条書きで整理する。年は西暦、金額はドルの後ろに(約…円)を添える。';")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
