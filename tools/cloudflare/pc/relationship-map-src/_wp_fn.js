/* Wikidata由来の人物(創業者・CEO・会長): people.json を開いたあとに裏で読み込み、検索に加える。クリックすると小さな紹介ページ */
let WPEO=[],WPLOAD=false;
function wpLoad(){
  if(WPLOAD)return;WPLOAD=true;
  fetch('people.json').then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.json()}).then(d=>{
    const have=new Set();try{buildIndex();Object.keys(PEOPLE).forEach(k=>have.add(norm(k)))}catch(e){}
    WPEO=d.rows.filter(r=>!have.has(norm(r[1]))).map(r=>({t:'w',q:r[0],name:r[2]||r[1],en:r[1],ja:r[2]||'',roles:r[3],sub:r[3].slice(0,2).map(x=>x[0]+' '+x[1]).join(' / '),s:norm(r[1]+' '+(r[2]||'')+' '+r[3].map(x=>x[0]).join(' '))}));
    try{const n=(SIDX?SIDX.filter(x=>x.t==='p'||x.t==='q').length:0)+WPEO.length;qEl.placeholder='人・企業を検索(人物 '+n.toLocaleString()+'名)  例: 孫正義 / Altman / Apple  「/」キーで移動'}catch(e){}
    if(qEl.value)qSearch();
  }).catch(()=>{});
}
function wpItems(){return WPEO}
function showWPerson(it){
  stop();leavePerson();
  MAINEL.hidden=true;controls.hidden=true;trailbar.hidden=true;document.getElementById('subbar').hidden=true;RANKEL.hidden=true;UNIEL.hidden=true;FEEDEL.hidden=true;PROFEL.hidden=false;
  document.querySelectorAll('#tabs button').forEach(b=>b.setAttribute('aria-pressed','false'));
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  document.getElementById('title').textContent=it.name;document.title=it.name;
  document.getElementById('note').textContent='Wikidataの「創業者」「CEO」「会長」の記録から集めた人物です(言語版の記事が5つ以上ある人に絞っています)。経歴の詳細はありません。';
  const RL={founder:'創業者',ceo:'CEO',chair:'会長'};
  PROFEL.innerHTML=`<div class="pf-head"><div class="face ph" style="background:var(--core)">${esc(it.name.slice(0,2))}</div><div style="flex:1;min-width:240px"><h2>${esc(it.name)}</h2><p style="margin:6px 0 0">${it.ja&&it.en?esc(it.en):''}</p></div></div>
   <div class="pf-sec"><h3>関わった会社(Wikidataの記録)</h3><ul>${it.roles.map(x=>`<li>${esc(x[0])} — ${esc(RL[x[1]]||x[1])}</li>`).join('')}</ul>
   <p class="links"><a href="https://www.wikidata.org/wiki/${esc(it.q)}" target="_blank" rel="noopener">Wikidata ↗</a> <a href="https://en.wikipedia.org/wiki/Special:Search?search=${encodeURIComponent(it.en)}" target="_blank" rel="noopener">Wikipedia ↗</a> <a href="https://www.google.com/search?q=${encodeURIComponent((it.ja||it.en)+' 経歴')}" target="_blank" rel="noopener">Webで調べる ↗</a></p></div>`;
  window.scrollTo(0,0);
}
