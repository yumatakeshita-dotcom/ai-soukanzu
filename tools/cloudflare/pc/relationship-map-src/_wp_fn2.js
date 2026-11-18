/* Wikidata由来の人物(創業者・CEO・会長・取締役): people.json を開いたあとに裏で読み込み、検索に加える。クリックすると紹介ページ(説明・Wikipediaの冒頭・関わった会社)と、つながりの相関図 */
let WPEO=[],WPALL=[],WPCO=null,WPLOAD=false;
const WPRL={founder:'創業者',ceo:'CEO',chair:'会長',board:'取締役',owner:'オーナー・大株主'};
function wpLoad(){
  if(WPLOAD)return;WPLOAD=true;
  fetch('people.json').then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.json()}).then(d=>{
    const have=new Set();try{buildIndex();Object.keys(PEOPLE).forEach(k=>have.add(norm(k)))}catch(e){}
    WPALL=d.rows.map(r=>({q:r[0],en:r[1],ja:r[2]||'',name:r[2]||r[1],roles:r[3],d:r[4]||'',x:r[5]||'',w:r[6]||'',t:r[7]||''}));
    WPEO=WPALL.filter(r=>!have.has(norm(r.en))).map(r=>Object.assign({t0:r.t,t:'w',sub:r.roles.slice(0,2).map(x=>x[0]+' '+(WPRL[x[1]]||x[1])).join(' / '),s:norm(r.en+' '+r.ja+' '+r.roles.map(x=>x[0]).join(' '))},r,{t:'w'}));
    try{const n=(SIDX?SIDX.filter(x=>x.t==='p'||x.t==='q').length:0)+WPEO.length;qEl.placeholder='人・企業を検索(人物 '+n.toLocaleString()+'名)  例: 孫正義 / Altman / Apple  「/」キーで移動'}catch(e){}
    if(qEl.value)qSearch();
  }).catch(()=>{});
}
function wpItems(){return WPEO}
function wpCoIndex(){
  if(WPCO)return WPCO;WPCO={};
  WPALL.forEach(p=>p.roles.forEach(([c,r])=>{(WPCO[c]=WPCO[c]||[]).push({p,role:r})}));
  return WPCO;
}
/* 人物を中心にした相関図(関わった会社と、同じ会社の他の人物)。実行時に作る */
function wpMap(it){
  const key='wp_'+it.q;
  if(!COMPANIES[key]){
    const co=wpCoIndex();const N=[{id:'me',name:it.name,kind:'c',from:1990,desc:(it.d||'')+(it.d?'。':'')+'Wikidataの記録に基づく、この人と関わった会社・人物のつながりです。'}];const E=[];const EN={me:it.en};
    it.roles.slice(0,6).forEach(([c,r],i)=>{
      const cid='c'+i;N.push({id:cid,name:c,kind:'o',from:1990,desc:'この人が「'+(WPRL[r]||r)+'」として載っている会社(Wikidata)。',role:WPRL[r]||r});E.push({a:cid,b:'me',k:'link',label:WPRL[r]||r});
      (co[c]||[]).filter(x=>x.p.q!==it.q).slice(0,6).forEach((x,j)=>{const pid='p'+i+'_'+j;N.push({id:pid,name:x.p.name,kind:'p',from:1990,desc:'この会社に「'+(WPRL[x.role]||x.role)+'」として載っている人物(Wikidata)。',role:WPRL[x.role]||x.role});EN[pid]=x.p.en;E.push({a:pid,b:cid,k:'member'})});
    });
    COMPANIES[key]={name:it.name,min:1990,sub:1,note:'Wikidataの「創業者・CEO・会長・取締役」の記録から、実行時に作った図です。人物の経歴や、会社どうしの出資関係は含みません。'};
    DATA[key]=()=>({N,PH:{},WIKI:{},EN,X:{},WEB:{},CAREER:{},LINKS:{},E,center:'me'});
  }
  ctrail=[];build(key);window.scrollTo(0,0);
}
/* 会社を中心にした相関図(その会社に載っている人物) */
function wpCoMap(cname){
  const key='wc_'+norm(cname).slice(0,40);
  if(!COMPANIES[key]){
    const rows=(wpCoIndex()[cname]||[]).slice(0,30);
    const N=[{id:'co',name:cname,kind:'c',from:1990,desc:'Wikidataで、創業者・CEO・会長・取締役として人物が記録されている会社です。'}];const E=[];const EN={};
    rows.forEach((x,i)=>{const pid='p'+i;N.push({id:pid,name:x.p.name,kind:'p',from:1990,desc:(x.p.d||'')+'(Wikidata)',role:WPRL[x.role]||x.role,founder:x.role==='founder'?1:0});EN[pid]=x.p.en;E.push({a:pid,b:'co',k:'member'})});
    COMPANIES[key]={name:cname,min:1990,sub:1,note:'Wikidataの記録から、実行時に作った図です。出資者や株主は含みません。'};
    DATA[key]=()=>({N,PH:{},WIKI:{},EN,X:{},WEB:{},CAREER:{},LINKS:{},E,center:'co'});
  }
  ctrail=[];build(key);window.scrollTo(0,0);
}
function showWPerson(it){
  stop();leavePerson();
  MAINEL.hidden=true;controls.hidden=true;trailbar.hidden=true;document.getElementById('subbar').hidden=true;RANKEL.hidden=true;UNIEL.hidden=true;FEEDEL.hidden=true;PROFEL.hidden=false;
  document.querySelectorAll('#tabs button').forEach(b=>b.setAttribute('aria-pressed','false'));
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  document.getElementById('title').textContent=it.name;document.title=it.name;
  document.getElementById('note').textContent='Wikidataの「創業者」「CEO」「会長」「取締役」の記録から集めた人物です。紹介文はWikipedia(CC BY-SA)の冒頭と、Wikidataの短い説明です。経歴の詳細ではありません。';
  const wl=it.t&&it.w?`https://${it.w}.wikipedia.org/wiki/${encodeURIComponent(it.t)}`:`https://en.wikipedia.org/wiki/Special:Search?search=${encodeURIComponent(it.en)}`;
  PROFEL.innerHTML=`<div class="pf-head"><div class="face ph" style="background:var(--core)">${esc(it.name.slice(0,2))}</div><div style="flex:1;min-width:240px"><h2>${esc(it.name)}</h2><p style="margin:6px 0 0">${it.ja&&it.en?esc(it.en):''}${it.d?(it.ja&&it.en?' / ':'')+esc(it.d):''}</p></div></div>
   ${it.x?`<div class="pf-sec"><h3>紹介</h3><p style="margin:0">${esc(it.x)}</p><p class="note">出どころ: <a href="${esc(wl)}" target="_blank" rel="noopener">Wikipedia(${it.w==='ja'?'日本語版':'英語版'})「${esc(it.t)}」</a>の冒頭(CC BY-SA)</p></div>`:`<div class="pf-sec"><p class="note">紹介文は見つかっていません。下のリンクから調べられます。</p></div>`}
   <div class="pf-sec"><h3>関わった会社(Wikidataの記録)</h3><ul>${it.roles.map(x=>`<li><a href="#" data-co="${esc(x[0])}">${esc(x[0])}</a> — ${esc(WPRL[x[1]]||x[1])}</li>`).join('')}</ul>
   <p><button type="button" id="wpmap">つながりの相関図を見る</button></p>
   <p class="links"><a href="https://www.wikidata.org/wiki/${esc(it.q)}" target="_blank" rel="noopener">Wikidata ↗</a> <a href="${esc(wl)}" target="_blank" rel="noopener">Wikipedia ↗</a> <a href="https://www.google.com/search?q=${encodeURIComponent((it.ja||it.en)+' 経歴')}" target="_blank" rel="noopener">Webで調べる ↗</a></p></div>`;
  document.getElementById('wpmap').addEventListener('click',()=>wpMap(it));
  PROFEL.querySelectorAll('a[data-co]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();wpCoMap(a.dataset.co)}));
  window.scrollTo(0,0);
}
