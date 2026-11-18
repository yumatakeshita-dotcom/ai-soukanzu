// ===== 人材の流れランキング(メニュー「人材の流れ」。2026年11月18日に追加) =====
// 人の出入りが多い会社を並べる。データは持たず、開いたときに各社の図(DATA)の「出身」「移籍先」の線と、
// 調査タスク(引き抜き)が足した人の動き(finds.js の FINDLINKS。各社の図に入っている)から数える。
// 同じ人の同じ移籍が2社の図に出てくるときは1件にまとめる。
let frSort='in',frPeriod='all',frQ='',frRows=null,frMoves=null;
function frKey(id,name){
  if(id&&COMPANIES[id])return id;
  if(id&&ALIAS[id]&&COMPANIES[ALIAS[id]])return ALIAS[id];
  // 名前の照らし合わせは会社だけにする(「MIT」を同じ名前のVC・ソフトなどにしない)
  const k=typeof fres==='function'?fres(name):null;
  return k&&COMPANIES[k]&&!/^(vc|aq)_/.test(k)?k:'n:'+fnorm(name);
}
// Google Brain は Google DeepMind にまとめる(移籍マップと同じ)
const FR_MERGE={'n:googlebrain':'gdm'};
// 大学・学校(出身校)と本の題名は会社の出入りに数えない
const FR_SCHOOL=/出身校|大学|University|College|カレッジ|^MIT$|^UC|Stanford|Harvard|Berkeley|高校|高等専門学校|^『/;  // 『』は本の題名(会社ではない)
function frCollect(){
  const seen=new Map();
  Reflect.ownKeys(COMPANIES).forEach(c=>{
    if(typeof c!=='string'||c.startsWith('__')||!DATA[c])return;let d;try{d=DATA[c]()}catch(e){return}
    const by=Object.fromEntries(d.N.map(n=>[n.id,n]));const cn=COMPANIES[c].name;
    d.E.forEach(e=>{
      if(e.k!=='from'&&e.k!=='moved')return;let P=by[e.a],O=by[e.b];if(!P||!O)return;
      if(P.kind!=='p'){[P,O]=[O,P]}if(P.kind!=='p'||O.kind==='p'||O.id===d.center||FR_SCHOOL.test(O.role||'')||FR_SCHOOL.test(O.name))return;
      let ok=frKey(O.id,O.name);ok=FR_MERGE[ok]||ok;const ck=FR_MERGE[c]||c;if(ok===ck)return;
      const on=COMPANIES[ok]?COMPANIES[ok].name:O.name;
      const en=(d.EN||{})[P.id]||'';
      const m=e.k==='from'?{a:ok,an:on,b:ck,bn:cn,y:+(e.since||P.from)||0}:{a:ck,an:cn,b:ok,bn:on,y:+(P.to||e.since)||0};
      const pk=fnorm(en||P.name)+'|'+m.a+'|'+m.b;
      const src=(e.src||[]).filter(k=>DS[k]);
      const old=seen.get(pk);
      if(old){if(!old.y&&m.y)old.y=m.y;src.forEach(k=>{if(!old.src.includes(k))old.src.push(k)});if(e.fd)old.fd=1;if(e.cf&&!old.cf)old.cf=e.cf;return}
      seen.set(pk,Object.assign(m,{p:P.name,en,src,fd:e.fd?1:0,cf:e.cf||P.cf||''}));
    });
  });
  return [...seen.values()];
}
function frAgg(moves){
  const R={};const row=(k,n)=>R[k]||(R[k]={k,name:n,inn:[],out:[]});
  moves.forEach(m=>{row(m.a,m.an).out.push(m);row(m.b,m.bn).inn.push(m)});
  return Object.values(R).map(r=>Object.assign(r,{i:r.inn.length,o:r.out.length,net:r.inn.length-r.out.length}));
}
function frTop(list,side){
  const c={};list.forEach(m=>{const k=side==='b'?m.bn:m.an;c[k]=(c[k]||0)+1});
  return Object.entries(c).sort((x,y)=>y[1]-x[1]||x[0].localeCompare(y[0]));
}
function showFlowRank(){
  stop();leavePerson();ctrail=[];
  MAINEL.hidden=true;controls.hidden=true;trailbar.hidden=true;document.getElementById('subbar').hidden=true;RANKEL.hidden=true;PROFEL.hidden=true;UNIEL.hidden=true;FEEDEL.hidden=false;
  document.querySelectorAll('#tabs button').forEach(b=>b.setAttribute('aria-pressed','false'));
  document.getElementById('title').textContent='人材の流れランキング';document.title='人材の流れランキング';
  document.getElementById('note').textContent='';
  FEEDEL.innerHTML='<p class="meta" style="padding:20px 0">各社の図から人の動きを数えています…</p>';
  setTimeout(()=>{if(!frMoves)frMoves=frCollect();frRender()},30);
}
function frEsc(s){return String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function frRender(){
  const Y=new Date().getFullYear();
  const P={all:[0,'全期間'],y3:[Y-2,`${Y-2}年から`],y1:[Y,`${Y}年だけ`]};
  const from=P[frPeriod][0];
  const moves=frMoves.filter(m=>!from||m.y>=from);
  let rows=frAgg(moves);
  const S={in:(a,b)=>b.i-a.i||b.net-a.net,out:(a,b)=>b.o-a.o||a.net-b.net,net:(a,b)=>b.net-a.net||b.i-a.i,loss:(a,b)=>a.net-b.net||b.o-a.o};
  rows.sort(S[frSort]);
  if(frSort==='net')rows=rows.filter(r=>r.net>0);if(frSort==='loss')rows=rows.filter(r=>r.net<0);
  const q=fnorm(frQ);if(q)rows=rows.filter(r=>fnorm(r.name).includes(q));
  const all=frAgg(moves);
  const topIn=all.slice().sort(S.in)[0],topOut=all.slice().sort(S.out)[0],topNet=all.slice().sort(S.net)[0];
  const fdN=moves.filter(m=>m.fd).length;
  const max=Math.max(1,...rows.map(r=>Math.max(r.i,r.o)));
  const yr=y=>y?y+'年':'年不明';
  const ppl=(list,side)=>list.slice().sort((x,y)=>(y.y||0)-(x.y||0)).map(m=>`<li><b>${frEsc(m.p)}</b>${m.en&&m.en!==m.p?` <small class="meta">${frEsc(m.en)}</small>`:''} <span class="meta">${side==='b'?'→ '+frEsc(m.bn):'← '+frEsc(m.an)} ・ ${yr(m.y)}${m.fd?' ・ 調査で追加':''}</span>${m.src.length?`<br><small>出典: ${dealSrcHtml(m.src,m.cf)}</small>`:''}</li>`).join('');
  const chips=t=>t.slice(0,3).map(([n,c])=>`${frEsc(n)} <b>${c}</b>`).join('、')||'<span class="meta">なし</span>';
  FEEDEL.innerHTML=`<style>
  .frt{display:flex;flex-wrap:wrap;gap:10px;margin:4px 0 12px}
  .frt div{border:1px solid var(--line);border-radius:10px;padding:8px 12px;background:var(--surface);min-width:0;max-width:100%}
  .frt b{display:block;font-size:22px;line-height:1.2;font-variant-numeric:tabular-nums;overflow-wrap:anywhere}.frt small{color:var(--muted);font-size:12px}
  .frbar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:0 0 8px;font-size:13px}
  .frbar button[aria-pressed="true"]{background:var(--fg);color:var(--bg)}
  .frbar input{min-width:0;max-width:100%;padding:5px 8px;border:1px solid var(--line);border-radius:8px;background:var(--surface)}
  .frl{list-style:none;margin:0;padding:0;display:grid;gap:6px;max-width:900px}
  .frl>li{border:1px solid var(--line);border-radius:8px;background:var(--surface);min-width:0}
  .frl summary{display:grid;grid-template-columns:2em minmax(0,1fr) auto;gap:4px 10px;align-items:center;padding:8px 10px;cursor:pointer;list-style:none}
  .frl summary::-webkit-details-marker{display:none}
  .frl .rk{font-variant-numeric:tabular-nums;color:var(--muted);font-size:13px}
  .frl .nm{font-weight:700;min-width:0;overflow-wrap:anywhere}
  .frl .nt{font-size:18px;font-weight:700;font-variant-numeric:tabular-nums;text-align:right}
  .frl .up{color:var(--active)}.frl .dn{color:var(--left)}.frl .ev{color:var(--muted)}
  .frl .bars{grid-column:2/-1;display:grid;grid-template-columns:3.6em minmax(0,1fr);gap:2px 6px;font-size:12px;color:var(--muted);align-items:center}
  .frl .bars i{display:block;height:7px;border-radius:4px;min-width:2px}
  .frl .tops{grid-column:2/-1;font-size:12.5px;color:var(--muted);overflow-wrap:anywhere}
  .frl .tops b{color:var(--fg)}
  .frd{padding:0 10px 10px 10px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:10px;font-size:13px}
  .frd h4{margin:6px 0 4px;font-size:13px}
  .frd ul{margin:0;padding:0;list-style:none;display:grid;gap:5px}.frd li{overflow-wrap:anywhere}
  </style>
  <p style="font-size:13px;color:var(--muted);margin:0 0 10px;max-width:72ch">相関図に記録した「出身」「移籍先」のつながりと、毎朝の調査(引き抜き)で見つけた人の動きから、会社ごとの人の出入りを数えました。<b>流入</b>=ほかの会社から入ってきた人、<b>流出</b>=ほかの会社へ移った人、<b>純増</b>=流入−流出です。相関図に載っている人だけなので、実際の移籍の一部です。会社名を押すと、主な移籍先・出身元と人の一覧が開きます。</p>
  <div class="frt"><div><b>${moves.length}</b><small>移籍の件数(${frEsc(P[frPeriod][1])})</small></div>
   ${topIn?`<div><b>${frEsc(topIn.name)}</b><small>いちばん人が入った会社(${topIn.i}人)</small></div>`:''}
   ${topOut?`<div><b>${frEsc(topOut.name)}</b><small>いちばん人が出た会社(${topOut.o}人)</small></div>`:''}
   ${topNet&&topNet.net>0?`<div><b>${frEsc(topNet.name)}</b><small>純増がいちばん多い会社(+${topNet.net})</small></div>`:''}</div>
  <div class="frbar" role="group" aria-label="期間"><span class="meta">期間</span>${Object.entries(P).map(([v,[,t]])=>`<button type="button" data-p="${v}" aria-pressed="${frPeriod===v}">${t}</button>`).join('')}</div>
  <div class="frbar" role="group" aria-label="並べ方"><span class="meta">並べ方</span>${[['in','流入が多い順'],['out','流出が多い順'],['net','純増(集まる会社)'],['loss','純減(出ていく会社)']].map(([v,t])=>`<button type="button" data-s="${v}" aria-pressed="${frSort===v}">${t}</button>`).join('')}</div>
  <div class="frbar"><input type="search" id="frq" placeholder="会社名で絞り込む" value="${frEsc(frQ)}" aria-label="会社名で絞り込む"> <span class="meta">${rows.length}社</span></div>
  <ol class="frl">${rows.slice(0,150).map((r,i)=>`<li><details><summary><span class="rk">${i+1}</span><span class="nm">${frEsc(r.name)}</span>
    <span class="nt ${r.net>0?'up':r.net<0?'dn':'ev'}" title="純増">${r.net>0?'+':''}${r.net}</span>
    <span class="bars"><span>流入 ${r.i}</span><i style="width:${r.i*100/max}%;background:var(--active)"></i><span>流出 ${r.o}</span><i style="width:${r.o*100/max}%;background:var(--left)"></i></span>
    <span class="tops">${r.o?`主な移籍先: ${chips(frTop(r.out,'b'))}`:''}${r.o&&r.i?'<br>':''}${r.i?`主な出身元: ${chips(frTop(r.inn,'a'))}`:''}</span></summary>
    <div class="frd">${r.i?`<div><h4>入ってきた人(${r.i}人)</h4><ul>${ppl(r.inn,'a')}</ul></div>`:''}${r.o?`<div><h4>出ていった人(${r.o}人)</h4><ul>${ppl(r.out,'b')}</ul></div>`:''}
    ${COMPANIES[r.k]?`<div style="grid-column:1/-1"><a href="#" data-k="${frEsc(r.k)}">${frEsc(r.name)}の相関図を見る ▸</a></div>`:''}</div></details></li>`).join('')}</ol>
  ${rows.length>150?`<p class="note">上位150社まで表示しています。会社名で絞り込むと、ほかの会社も見られます。</p>`:''}
  <p class="note" style="margin-top:14px">年は、移った先に入った年(わかる場合)です。年がわからない移籍は「全期間」にだけ数えます。同じ人が同じ会社へ移った記録が2社の図にあるときは1件にまとめ、Google BrainはGoogle DeepMindにまとめ、大学などの出身校は数えていません。うち${fdN}件は毎朝の調査タスクが出典つきで足したもので、報道ベースのものを含みます。開いたときに各社の図から数え直すので、相関図に人が足されると自動で増えます。</p>`;
  FEEDEL.querySelectorAll('.frbar button[data-s]').forEach(b=>b.addEventListener('click',()=>{frSort=b.dataset.s;frRender()}));
  FEEDEL.querySelectorAll('.frbar button[data-p]').forEach(b=>b.addEventListener('click',()=>{frPeriod=b.dataset.p;frRender()}));
  const qi=document.getElementById('frq');qi.addEventListener('input',()=>{frQ=qi.value;const pos=qi.selectionStart;frRender();const n=document.getElementById('frq');n.focus();try{n.setSelectionRange(pos,pos)}catch(e){}});
  FEEDEL.querySelectorAll('.frl a[data-k]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();build(a.dataset.k);window.scrollTo(0,0)}));
}
