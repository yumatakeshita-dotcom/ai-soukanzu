/* ===== 出資の一覧(2026/11/20追加) =====
   「どの企業が、どの企業に出資しているか」を、会社(や人)を選んで見る画面。
   データは持たず、開いたときに本体の相関図(DATA)から cmBuild()(data/common.js)でまとめる。
   毎日の更新・調査の新着がそのまま反映される。出資の線(invest・invest2)だけを使う。
   本体(index.html)からは showInvest(名前) を呼ぶだけ。 */
let invSel=-1;
function invEdges(){
  const G=cmBuild();
  if(G._inv)return G._inv;
  const inc=G.nodes.map(()=>[]),out=G.nodes.map(()=>[]);
  G.edges.forEach(e=>{if(e.k!=='invest'&&e.k!=='invest2')return;out[e.a].push(e);inc[e.b].push(e)});
  return G._inv={inc,out};
}
/* 線の出典のうち一番確かなものの印(公式・開示・本人・報道) */
function invCf(e){
  if(!e.src||typeof DS==='undefined')return '';
  let best='';e.src.forEach(k=>{const c=DS[k]?dsCf(k):'';if(c&&(CFRANK[c]||0)>(CFRANK[best]||0))best=c});
  return best?cfBadge(best):'';
}
function invYear(e){return Number(String(e.y||'').slice(0,4))||0}
function invRows(list,otherOf){
  const rows=list.slice().sort((x,y)=>invYear(y)-invYear(x)||(y.l?1:0)-(x.l?1:0));
  return rows.map(e=>{const i=otherOf(e);
    return `<li><span style="display:block">${cmName(i)} <span class="cm-k">${cmTypeLabel(i)}</span>${e.l?` <b class="inv-l">${cmEsc(e.l)}</b>`:''}${e.y?` <span class="cm-y">${cmEsc(e.y)}年〜</span>`:''} ${invCf(e)}</span>${e.ed?`<small class="cm-d">${cmEsc(e.ed)}</small>`:''}${e.src&&e.src.length?cmSrc(e):'<small class="cm-src">出典の記録なし(相関図の線のみ)</small>'}</li>`}).join('');
}
function invTop(){
  const G=cmBuild(),{inc,out}=invEdges();
  const pick=(arr)=>G.nodes.map((n,i)=>({i,c:arr[i].length})).filter(x=>x.c>0&&!G.nodes[x.i].pas).sort((a,b)=>b.c-a.c).slice(0,30);
  return {inv:pick(out),to:pick(inc)};
}
function showInvest(q){
  stop();leavePerson();ctrail=[];
  MAINEL.hidden=true;controls.hidden=true;trailbar.hidden=true;document.getElementById('subbar').hidden=true;RANKEL.hidden=true;PROFEL.hidden=true;UNIEL.hidden=true;FEEDEL.hidden=false;
  document.querySelectorAll('#tabs button').forEach(b=>b.setAttribute('aria-pressed','false'));
  document.getElementById('title').textContent='出資の一覧';document.title='出資の一覧';
  document.getElementById('note').textContent='';
  const G=cmBuild();
  if(typeof q==='string'&&q){const i=cmPick(q);invSel=i}
  FEEDEL.innerHTML=`<style>
  .inv-f{position:relative;max-width:560px;display:grid;gap:4px}.inv-f label{font-size:12px;color:var(--muted)}
  .inv-f input{width:100%;box-sizing:border-box;padding:9px 12px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--fg);font:inherit;font-size:16px}
  .inv-sug{position:absolute;left:0;right:0;top:100%;z-index:20;margin:2px 0 0;padding:4px;list-style:none;background:var(--surface);border:1px solid var(--line);border-radius:8px;max-height:280px;overflow:auto;box-shadow:0 8px 24px rgba(0,0,0,.18)}
  .inv-sug li{padding:6px 10px;border-radius:6px;cursor:pointer;display:flex;gap:8px;align-items:baseline;min-width:0}
  .inv-sug li:hover{background:var(--soft)}.inv-sug small{color:var(--muted);margin-left:auto;font-size:11px;white-space:nowrap}
  .inv-cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:18px;margin-top:16px}
  .inv-cols>section{min-width:0}.inv-cols h3{margin:0 0 4px;font-size:15px}.inv-cols>section>p{margin:0 0 8px;font-size:13px;color:var(--muted)}
  .inv-l{color:var(--invest)}
  .inv-top{list-style:none;margin:0;padding:0;display:grid;gap:4px}
  .inv-top li{display:flex;gap:8px;align-items:baseline;border-bottom:1px solid var(--line);padding:4px 0;min-width:0}
  .inv-top button{font:inherit;background:none;border:0;color:var(--active);cursor:pointer;padding:0;text-align:left;font-weight:700;overflow-wrap:anywhere}
  .inv-top small{margin-left:auto;color:var(--muted);font-family:var(--font-mono);white-space:nowrap}
  @media (max-width:720px){.inv-cols{grid-template-columns:minmax(0,1fr)}}
  </style>
  <p class="meta" style="margin:0 0 12px;max-width:72ch">会社(人でも選べます)を選ぶと、<b>その会社に出資している企業・人</b>と、<b>その会社が出資している先</b>を並べます。相関図にある出資の線から、開いたときにまとめています(網羅ではありません)。印は線の出典から自動で決まります。出典が付いていない線は「出典の記録なし」と出します。</p>
  <div class="inv-f"><label for="invq">会社・人の名前</label><input id="invq" type="search" placeholder="例: OpenAI、ソフトバンクグループ、Nvidia" autocomplete="off" value="${invSel>=0?cmEsc(G.nodes[invSel].n):''}"><ul class="inv-sug" id="invsug" hidden></ul></div>
  <div id="invout"></div>`;
  const out=document.getElementById('invout');
  function render(){
    const {inc,out:o2}=invEdges();
    if(invSel<0){const t=invTop();
      out.innerHTML=`<div class="inv-cols"><section><h3>出資先が多い企業・人</h3><p>相関図に出資の線が多い順(上位30)。名前を押すと中身が見られます。</p><ul class="inv-top">${t.inv.map(x=>`<li><button type="button" data-ii="${x.i}">${cmEsc(G.nodes[x.i].n)}</button><small>${x.c}先</small></li>`).join('')}</ul></section><section><h3>出資を受けている数が多い会社</h3><p>出資者が多い順(上位30)。</p><ul class="inv-top">${t.to.map(x=>`<li><button type="button" data-ii="${x.i}">${cmEsc(G.nodes[x.i].n)}</button><small>${x.c}者</small></li>`).join('')}</ul></section></div>`;return}
    const n=G.nodes[invSel],a=inc[invSel],b=o2[invSel];
    out.innerHTML=`<h2 style="font-size:18px;margin:18px 0 0">${cmName(invSel)} <span class="cm-k">${cmTypeLabel(invSel)}</span></h2><p class="meta" style="margin:2px 0 0">出資している先 ${b.length}件 ・ 出資を受けている ${a.length}件${n.code?` ・ <a href="#" data-cmgo="${cmEsc(n.code)}">この会社の相関図を開く</a>`:''}</p>
    <div class="inv-cols"><section><h3>${cmEsc(n.n)} に出資している</h3><p>${a.length}件</p>${a.length?`<ul class="cm-l">${invRows(a,e=>e.a)}</ul>`:'<p class="meta">相関図に出資の線がありません。</p>'}</section>
    <section><h3>${cmEsc(n.n)} が出資している先</h3><p>${b.length}件</p>${b.length?`<ul class="cm-l">${invRows(b,e=>e.b)}</ul>`:'<p class="meta">相関図に出資の線がありません。</p>'}</section></div>
    <p class="note" style="margin-top:16px"><button type="button" class="cm-more" id="invback">← 一覧にもどる</button></p>`;
  }
  render();
  const input=document.getElementById('invq'),sug=document.getElementById('invsug');
  function suggest(){const v=input.value.trim();if(!v){sug.hidden=true;return}
    const f=cmFind(v);sug.innerHTML=f.map(x=>`<li data-ii="${x.i}">${cmEsc(x.n)}<small>${cmTypeLabel(x.i)}・線${x.deg}本</small></li>`).join('');sug.hidden=!f.length}
  input.addEventListener('input',suggest);
  input.addEventListener('keydown',ev=>{if(ev.key==='Enter'){const i=cmPick(input.value);if(i>=0){invSel=i;sug.hidden=true;input.value=G.nodes[i].n;render()}}});
  sug.addEventListener('click',ev=>{const li=ev.target.closest('li[data-ii]');if(!li)return;invSel=Number(li.dataset.ii);sug.hidden=true;input.value=G.nodes[invSel].n;render();window.scrollTo(0,0)});
  out.addEventListener('click',ev=>{
    const a=ev.target.closest('a[data-cmgo]');if(a){ev.preventDefault();build(a.dataset.cmgo);return}
    const bt=ev.target.closest('button[data-ii]');if(bt){invSel=Number(bt.dataset.ii);input.value=G.nodes[invSel].n;render();window.scrollTo(0,0);return}
    if(ev.target.id==='invback'){invSel=-1;input.value='';render()}});
}
