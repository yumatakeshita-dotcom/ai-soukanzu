  /* サイト全体から、質問に出てくる語に合う記録を探して渡す(開いているページに無い買収・子会社・世界の企業なども答えられるように) */
  const ALIAS={'メタ':['Meta'],'アップル':['Apple'],'グーグル':['Google','Alphabet'],'アマゾン':['Amazon'],'マイクロソフト':['Microsoft'],'エヌビディア':['Nvidia'],'オープンai':['OpenAI'],'アンソロピック':['Anthropic'],'テスラ':['Tesla'],'ソフトバンク':['SoftBank','ソフトバンクグループ'],
    'メガネ':['eyewear','glasses','Ray-Ban','Oakley','EssilorLuxottica','メガネ'],'めがね':['eyewear','glasses','Ray-Ban','Oakley','EssilorLuxottica'],'眼鏡':['eyewear','glasses','Ray-Ban','EssilorLuxottica'],'グラス':['glasses','Ray-Ban','EssilorLuxottica'],'スマートグラス':['glasses','Ray-Ban','EssilorLuxottica','Oakley']};
  const STOP=new Set(['買収','会社','企業','どこ','どれ','した','して','です','ます','ある','いつ','いくら','金額','教えて','ありますか','買った','買って','ましたか','最近','最新','グループ','どこか']);
  function siteSearch(q){
    const toks=new Set();
    (q.match(/[A-Za-z][A-Za-z0-9.&+\-]{1,}/g)||[]).forEach(t=>toks.add(t));
    (q.match(/[ァ-ヶー]{2,}|[一-龥]{2,}/g)||[]).forEach(t=>{if(!STOP.has(t))toks.add(t)});
    const ql=q.toLowerCase();Object.keys(ALIAS).forEach(a=>{if(ql.includes(a))ALIAS[a].forEach(t=>toks.add(t))});
    const T=[...toks].filter(t=>t.length>=2&&!STOP.has(t)).slice(0,14);if(!T.length)return '';
    const lo=T.map(t=>t.toLowerCase());const lines=[];const seen=new Set();
    const add=s=>{if(!seen.has(s)&&lines.length<70){seen.add(s);lines.push(s)}};
    const row=(nm,r)=>`${nm}の買収・子会社: ${r[1]||'年不明'} ${r[0]}${r[2]?' ('+yenify(String(r[2]))+')':''}${r[3]?' '+yenify(String(r[3])).slice(0,160):''}`;
    Object.keys(COMPANIES).forEach(k=>{const nm=(COMPANIES[k].name||'');const nl=nm.toLowerCase();if(!nl)return;
      if(lo.some(t=>nl===t||(t.length>=3&&nl.startsWith(t)))){(ACQ[k]||[]).slice().sort((a,b)=>(b[1]||0)-(a[1]||0)).slice(0,40).forEach(r=>add(row(nm,r)))}});
    Object.keys(ACQ).forEach(k=>{const nm=(COMPANIES[k]||{}).name||k;ACQ[k].forEach(r=>{const s=(r[0]+' '+(r[3]||'')+' '+(r[2]||'')).toLowerCase();if(lo.some(t=>s.includes(t)))add(row(nm,r))})});
    worldRows().forEach(r=>{const s=(r.n+' '+r.c+' '+r.b+' '+(r.t||'')).toLowerCase();if(lo.some(t=>s.includes(t)))add(`${r.n}${r.c?'('+r.c+')':''}: ${(r.b||'')} ${(r.t||'').slice(0,220)}`)});
    Object.keys(VCS).forEach(k=>{const v=VCS[k];const vn=(v.jp||v.en||'');const vl=vn.toLowerCase();if(lo.some(t=>vl===t||(t.length>=3&&vl.includes(t))))add(`${vn}(VC): 投資先 ${v.p.length}件。例: ${v.p.slice(0,12).map(p=>p[0]).join('、')}`)});
    return lines.join('\n').slice(0,9000);
  }
