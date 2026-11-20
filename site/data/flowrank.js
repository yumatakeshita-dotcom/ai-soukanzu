// ===== 人材の流れランキング(メニュー「人材の流れ」。2026年11月18日に追加) =====
// 人の出入りが多い会社を並べる。データは持たず、開いたときに各社の図(DATA)の「出身」「移籍先」の線と、
// 調査タスク(引き抜き)が足した人の動き(finds.js の FINDLINKS。各社の図に入っている)から数える。
// 同じ人の同じ移籍が2社の図に出てくるときは1件にまとめる。
let frSort='in',frPeriod='all',frQ='',frRows=null,frMoves=null,frView='co',frPair=null;
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
  // 経由の移籍(2026/11/19追加): 同じ人に A→X と X→B があるとき、図に「A出身でBへ」とある A→B は直接の移籍ではないので数えない
  // 例: シュルマンは OpenAI→Anthropic(2024)→Thinking Machines Lab(2025)。OpenAI→TML は経由として外す(データは消さない)
  const all=[...seen.values()],byP={};all.forEach(m=>{const k=fnorm(m.en||m.p);(byP[k]||(byP[k]=[])).push(m)});
  Object.values(byP).forEach(L=>{if(L.length<3)return;L.forEach(m=>{if(L.some(x=>x!==m&&x.a===m.a&&L.some(z=>z!==m&&z.a===x.b&&z.b===m.b)))m.via=1})});
  FR_VIA=all.filter(m=>m.via);
  return all.filter(m=>!m.via);
}
let FR_VIA=[];
function frAgg(moves){
  const R={};const row=(k,n)=>R[k]||(R[k]={k,name:n,inn:[],out:[]});
  moves.forEach(m=>{row(m.a,m.an).out.push(m);row(m.b,m.bn).inn.push(m)});
  return Object.values(R).map(r=>Object.assign(r,{i:r.inn.length,o:r.out.length,net:r.inn.length-r.out.length}));
}
function frTop(list,side){
  const c={};list.forEach(m=>{const n=side==='b'?m.bn:m.an,k=side==='b'?m.b:m.a;(c[k]||(c[k]=[n,0,k]))[1]++});
  return Object.values(c).sort((x,y)=>y[1]-x[1]||x[0].localeCompare(y[0]));
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
const FR_CSS=`<style>
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
  .frl .tops a,.frpr a{color:inherit;text-decoration:underline;text-decoration-color:var(--line)}
  .frsel{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:0 0 12px}
  .frsel select{min-width:0;max-width:100%;flex:1 1 200px;padding:6px 8px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--fg)}
  .frpv{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:10px;max-width:900px;margin:0 0 14px}
  .frpv>div{border:1px solid var(--line);border-radius:10px;background:var(--surface);padding:10px 12px;min-width:0;font-size:13px}
  .frpv h3{margin:0 0 6px;font-size:15px;overflow-wrap:anywhere}.frpv h3 b{font-size:22px;color:var(--active);font-variant-numeric:tabular-nums}
  .frpv ul{margin:0;padding:0;list-style:none;display:grid;gap:5px}.frpv li{overflow-wrap:anywhere}
  .frtalk{border:1px solid var(--line);border-left:4px solid var(--invest);border-radius:8px;background:var(--surface);padding:10px 12px;max-width:900px;margin:0 0 14px;font-size:14px;overflow-wrap:anywhere}
  .frpr{list-style:none;margin:0;padding:0;display:grid;gap:5px;max-width:900px}
  .frpr li{display:grid;grid-template-columns:2em minmax(0,1fr) auto;gap:8px;align-items:center;border:1px solid var(--line);border-radius:8px;background:var(--surface);padding:7px 10px;font-size:13.5px}
  .frpr .c{font-variant-numeric:tabular-nums;font-weight:700;text-align:right;white-space:nowrap}
  </style>`;
// 経由の移籍の一覧(2026/11/19追加): 数には入れず、「どこを経由したか」を小さく出す
function frViaPath(m){
  const k=fnorm(m.en||m.p);const L=frMoves.filter(x=>fnorm(x.en||x.p)===k);
  const x=L.find(x=>x.a===m.a&&L.some(z=>z.a===x.b&&z.b===m.b));return x?x.bn:'';
}
function frViaHtml(list,cls){
  if(!list.length)return '';
  return `<div class="${cls||''}" style="grid-column:1/-1;font-size:12.5px;color:var(--muted);max-width:900px;margin:0 0 12px"><h4 style="margin:4px 0;font-size:13px;color:var(--fg)">経由の移籍 <small class="meta">${list.length}件・数には入れていません</small></h4><ul style="margin:0;padding-left:18px;display:grid;gap:3px">${list.map(m=>{const v=frViaPath(m);return `<li><b style="color:var(--fg)">${frEsc(m.p)}</b> ${frEsc(m.an)} → ${v?`<b>${frEsc(v)}</b>(経由) → `:''}${frEsc(m.bn)}${m.y?` ・ ${m.y}年`:''}</li>`}).join('')}</ul></div>`;
}
function frEsc(s){return String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function frRender(){
  const Y=new Date().getFullYear();
  const P={all:[0,'全期間'],y3:[Y-2,`${Y-2}年から`],y1:[Y,`${Y}年だけ`]};
  const from=P[frPeriod][0];
  const moves=frMoves.filter(m=>!from||m.y>=from);
  if(frView==='pair')return frRenderPair(moves,P);
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
  const chips=(t,k,side)=>t.slice(0,3).map(([n,c,o])=>`<a href="#" data-pa="${frEsc(side==='b'?k:o)}" data-pb="${frEsc(side==='b'?o:k)}">${frEsc(n)}</a> <b>${c}</b>`).join('、')||'<span class="meta">なし</span>';
  FEEDEL.innerHTML=`${FR_CSS}
  ${frTabs()}
  <p style="font-size:13px;color:var(--muted);margin:0 0 10px;max-width:72ch">相関図に記録した「出身」「移籍先」のつながりと、毎朝の調査(引き抜き)で見つけた人の動きから、会社ごとの人の出入りを数えました。<b>流入</b>=ほかの会社から入ってきた人、<b>流出</b>=ほかの会社へ移った人、<b>純増</b>=流入−流出です。相関図に載っている人だけなので、実際の移籍の一部です。会社名を押すと、主な移籍先・出身元と人の一覧が開きます。移籍先・出身元の会社名を押すと、2社のあいだの流れを見られます。</p>
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
    <span class="tops">${r.o?`主な移籍先: ${chips(frTop(r.out,'b'),r.k,'b')}`:''}${r.o&&r.i?'<br>':''}${r.i?`主な出身元: ${chips(frTop(r.inn,'a'),r.k,'a')}`:''}</span></summary>
    <div class="frd">${r.i?`<div><h4>入ってきた人(${r.i}人)</h4><ul>${ppl(r.inn,'a')}</ul></div>`:''}${r.o?`<div><h4>出ていった人(${r.o}人)</h4><ul>${ppl(r.out,'b')}</ul></div>`:''}
    ${frViaHtml(FR_VIA.filter(m=>(m.a===r.k||m.b===r.k)&&(!from||m.y>=from)))}
    ${COMPANIES[r.k]?`<div style="grid-column:1/-1"><a href="#" data-k="${frEsc(r.k)}">${frEsc(r.name)}の相関図を見る ▸</a></div>`:''}</div></details></li>`).join('')}</ol>
  ${rows.length>150?`<p class="note">上位150社まで表示しています。会社名で絞り込むと、ほかの会社も見られます。</p>`:''}
  <div class="note" style="margin-top:14px;border-left:3px solid var(--line,#999);padding-left:10px"><b>参考: 業界全体の数字(報道ベース)</b><br>SignalFireの2025年5月のレポート(LinkedInのデータ)を、Fortuneなどが報じた内容です。2年間在籍する人の割合は Anthropic 80%・DeepMind 78%・OpenAI 67%・Meta 64%。OpenAIからAnthropicへ移る人は、逆の約8倍、DeepMindからAnthropicへは約11倍とされています。<span class="note">※SignalFireの原典ページは、この環境から開けず未確認です。LinkedInに載る人だけの数字で、この画面の数え方とは別物です。出典: <a href="https://fortune.com/2025/06/03/openai-deepmind-anthropic-loosing-engineers-ai-talent-war/" target="_blank" rel="noopener">Fortune(2025/6/3)</a>、<a href="https://www.signalfire.com/blog/signalfire-state-of-talent-report-2025" target="_blank" rel="noopener">SignalFire(原典)</a></span></div>
  <p class="note" style="margin-top:14px">年は、移った先に入った年(わかる場合)です。年がわからない移籍は「全期間」にだけ数えます。同じ人が同じ会社へ移った記録が2社の図にあるときは1件にまとめ、Google BrainはGoogle DeepMindにまとめ、大学などの出身校は数えていません。ほかの会社を経由した移籍(例: シュルマンのOpenAI→Thinking Machines LabはAnthropic経由)は、経由した先への移籍として数え、直接の移籍としては数えていません(${FR_VIA.length}件)。うち${fdN}件は毎朝の調査タスクが出典つきで足したもので、報道ベースのものを含みます。開いたときに各社の図から数え直すので、相関図に人が足されると自動で増えます。</p>`;
  FEEDEL.querySelectorAll('.frbar button[data-s]').forEach(b=>b.addEventListener('click',()=>{frSort=b.dataset.s;frRender()}));
  FEEDEL.querySelectorAll('.frbar button[data-p]').forEach(b=>b.addEventListener('click',()=>{frPeriod=b.dataset.p;frRender()}));
  const qi=document.getElementById('frq');qi.addEventListener('input',()=>{frQ=qi.value;const pos=qi.selectionStart;frRender();const n=document.getElementById('frq');n.focus();try{n.setSelectionRange(pos,pos)}catch(e){}});
  frWire();
  FEEDEL.querySelectorAll('.frl a[data-k]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();build(a.dataset.k);window.scrollTo(0,0)}));
}

// ----- 2社のあいだの流れ(2026年11月18日に追加): 2社を選ぶと、両方向の移籍と人の一覧、営業の話題の例を出す。下に、よくある移籍ルートの一覧 -----
function frTabs(){return `<div class="frbar" role="group" aria-label="見かた"><span class="meta">見かた</span><button type="button" data-v="co" aria-pressed="${frView==='co'}">会社のランキング</button><button type="button" data-v="pair" aria-pressed="${frView==='pair'}">2社のあいだの流れ</button></div>`}
function frWire(){
  FEEDEL.querySelectorAll('.frbar button[data-v]').forEach(b=>b.addEventListener('click',()=>{frView=b.dataset.v;frRender()}));
  FEEDEL.querySelectorAll('a[data-pa]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();frView='pair';frPair={a:a.dataset.pa,b:a.dataset.pb};frRender();window.scrollTo(0,0)}));
}
function frPairs(moves){
  const R={};moves.forEach(m=>{const [x,y]=m.a<m.b?[m.a,m.b]:[m.b,m.a];const k=x+'\u0001'+y;const r=R[k]||(R[k]={a:m.a,an:m.an,b:m.b,bn:m.bn,ab:0,ba:0});if(m.a===r.a)r.ab++;else r.ba++});
  return Object.values(R).map(r=>{if(r.ba>r.ab)[r.a,r.an,r.b,r.bn,r.ab,r.ba]=[r.b,r.bn,r.a,r.an,r.ba,r.ab];r.t=r.ab+r.ba;return r}).sort((x,y)=>y.t-x.t||y.ab-x.ab||x.an.localeCompare(y.an));
}
function frTalk(A,B,ab,ba){
  const last=l=>l.slice().sort((x,y)=>(y.y||0)-(x.y||0))[0];
  const one=(F,T,l)=>{if(!l.length)return '';const m=last(l);return `${F}から${T}へ${l.length}人が移っています(最近は${m.p}${m.y?'、'+m.y+'年':''})。`};
  let t=one(A,B,ab)+one(B,A,ba);
  if(!t)return `${A}と${B}のあいだの移籍は、相関図にはまだ記録がありません。`;
  if(ab.length&&ba.length)t+=`人の行き来がある2社です。`;
  else if(ab.length>=3)t+=`${A}の人材が${B}に集まっている流れです。`;
  else if(ba.length>=3)t+=`${B}の人材が${A}に集まっている流れです。`;
  return t;
}
function frRenderPair(moves,P){
  const cos=frAgg(frMoves).sort((x,y)=>(y.i+y.o)-(x.i+x.o)||x.name.localeCompare(y.name));
  const pairs=frPairs(moves);
  if(!frPair||!cos.some(c=>c.k===frPair.a)||!cos.some(c=>c.k===frPair.b)){const t=frPairs(frMoves)[0];frPair=t?{a:t.a,b:t.b}:{a:cos[0].k,b:cos[1].k}}
  const nm=k=>(cos.find(c=>c.k===k)||{}).name||k;
  const A=nm(frPair.a),B=nm(frPair.b);
  const ab=moves.filter(m=>m.a===frPair.a&&m.b===frPair.b),ba=moves.filter(m=>m.a===frPair.b&&m.b===frPair.a);
  const yr=y=>y?y+'年':'年不明';
  const ppl=l=>l.length?`<ul>${l.slice().sort((x,y)=>(y.y||0)-(x.y||0)).map(m=>`<li><b>${frEsc(m.p)}</b>${m.en&&m.en!==m.p?` <small class="meta">${frEsc(m.en)}</small>`:''} <span class="meta">${yr(m.y)}${m.fd?' ・ 調査で追加':''}</span>${m.src.length?`<br><small>出典: ${dealSrcHtml(m.src,m.cf)}</small>`:''}</li>`).join('')}</ul>`:'<p class="meta" style="margin:0">記録なし</p>';
  const opt=sel=>cos.map(c=>`<option value="${frEsc(c.k)}"${c.k===sel?' selected':''}>${frEsc(c.name)}(入${c.i}・出${c.o})</option>`).join('');
  const talk=frTalk(A,B,ab,ba);
  FEEDEL.innerHTML=`${FR_CSS}${frTabs()}
  <p style="font-size:13px;color:var(--muted);margin:0 0 10px;max-width:72ch">2社を選ぶと、そのあいだで動いた人を両方向に並べます。営業先との話題づくりや、どこからどこへ人が流れているかを見るのに使えます。下の「よくある移籍ルート」を押しても選べます。</p>
  <div class="frbar" role="group" aria-label="期間"><span class="meta">期間</span>${Object.entries(P).map(([v,[,t]])=>`<button type="button" data-p="${v}" aria-pressed="${frPeriod===v}">${t}</button>`).join('')}</div>
  <div class="frsel"><select id="frpa" aria-label="1社目">${opt(frPair.a)}</select><button type="button" id="frsw" title="入れかえる" aria-label="2社を入れかえる">⇄</button><select id="frpb" aria-label="2社目">${opt(frPair.b)}</select></div>
  <div class="frpv"><div><h3>${frEsc(A)} → ${frEsc(B)} <b>${ab.length}</b>人</h3>${ppl(ab)}</div><div><h3>${frEsc(B)} → ${frEsc(A)} <b>${ba.length}</b>人</h3>${ppl(ba)}</div></div>
  ${frViaHtml(FR_VIA.filter(m=>((m.a===frPair.a&&m.b===frPair.b)||(m.a===frPair.b&&m.b===frPair.a))&&(!P[frPeriod][0]||m.y>=P[frPeriod][0])),'frpv-via')}
  <div class="frtalk"><div class="meta" style="font-size:12px;margin-bottom:4px">話題の例(そのまま使う前に、出典を確かめてください)</div><span id="frtk">${frEsc(talk)}</span>
   <div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:6px"><button type="button" id="frcp">文をコピー</button>${COMPANIES[frPair.a]?`<a href="#" data-k="${frEsc(frPair.a)}">${frEsc(A)}の相関図 ▸</a>`:''}${COMPANIES[frPair.b]?`<a href="#" data-k="${frEsc(frPair.b)}">${frEsc(B)}の相関図 ▸</a>`:''}${COMPANIES[frPair.a]&&COMPANIES[frPair.b]&&typeof showCommon==='function'?`<a href="#" id="frcm">2社の共通のつながりを見る ▸</a>`:''}</div></div>
  <h3 style="margin:16px 0 6px;font-size:15px">よくある移籍ルート(${frEsc(P[frPeriod][1])}、上位${Math.min(30,pairs.length)})</h3>
  <ol class="frpr">${pairs.slice(0,30).map((r,i)=>`<li><span class="meta">${i+1}</span><span style="min-width:0;overflow-wrap:anywhere"><a href="#" data-pa="${frEsc(r.a)}" data-pb="${frEsc(r.b)}">${frEsc(r.an)} → ${frEsc(r.bn)}</a>${r.ba?` <span class="meta">(逆向き ${r.ba}人)</span>`:''}</span><span class="c">${r.ab}人</span></li>`).join('')}</ol>
  <p class="note" style="margin-top:14px">数え方は会社のランキングと同じです(相関図に載っている人だけ。同じ移籍は1件、出身校は数えない)。話題の例は記録から機械的に作った文です。</p>`;
  FEEDEL.querySelectorAll('.frbar button[data-p]').forEach(b=>b.addEventListener('click',()=>{frPeriod=b.dataset.p;frRender()}));
  const pa=document.getElementById('frpa'),pb=document.getElementById('frpb');
  pa.addEventListener('change',()=>{frPair={a:pa.value,b:pb.value};frRender()});pb.addEventListener('change',()=>{frPair={a:pa.value,b:pb.value};frRender()});
  document.getElementById('frsw').addEventListener('click',()=>{frPair={a:frPair.b,b:frPair.a};frRender()});
  document.getElementById('frcp').addEventListener('click',ev=>{const b=ev.currentTarget;const done=()=>{b.textContent='コピーしました'};try{navigator.clipboard.writeText(talk).then(done,()=>{})}catch(e){}});
  const cm=document.getElementById('frcm');if(cm)cm.addEventListener('click',ev=>{ev.preventDefault();showCommon(A,B)});
  FEEDEL.querySelectorAll('.frtalk a[data-k]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();build(a.dataset.k);window.scrollTo(0,0)}));
  frWire();
}

// ----- 営業資料(1枚、common.js の cmBriefData)から使う: 2社のあいだの移籍を両方向で返す(2026年11月18日に追加) -----
function frKeyOf(code,name){let k=code&&COMPANIES[code]?code:frKey('',name);return FR_MERGE[k]||k}
function frBetween(codeA,nameA,codeB,nameB){
  if(!frMoves)frMoves=frCollect();
  const a=frKeyOf(codeA,nameA),b=frKeyOf(codeB,nameB);if(a===b)return {ab:[],ba:[]};
  const srt=l=>l.sort((x,y)=>(y.y||0)-(x.y||0));
  return {ab:srt(frMoves.filter(m=>m.a===a&&m.b===b)),ba:srt(frMoves.filter(m=>m.a===b&&m.b===a))};
}
