/* ===== 2社の共通のつながり(2026/11/18追加) =====
   2つの会社(または人)を選ぶと、共通の出資者・人物・取引先・使っているAIと、最短ルートを出す。
   営業先への「入り口」を探すための画面。データは本体の相関図(DATA)をその場でまとめるので、毎日の更新がそのまま反映される。
   本体(index.html)からは showCommon(a,b) と commonBtn()/wireCommon() を呼ぶだけ。 */
let CG=null,commonA='',commonB='',commonPas=false;
const CM_ALIAS={'o:yコンビネータ':'o:ycombinator','o:yコンビネーター':'o:ycombinator','o:softbank':'o:ソフトバンクグループ','o:ソフトバンク':'o:ソフトバンクグループ','o:googlebrain':'o:googledeepmind','o:エヌビディア':'o:nvidia','o:オープンai':'o:openai','o:マイクロソフト':'o:microsoft','o:アマゾン':'o:amazon','o:メタ':'o:meta','o:アンソロピック':'o:anthropic','o:google':'o:alphabet','o:spacex旧xai':'o:spacex'};
/* 株を持っているだけの信託銀行・大手運用会社。ほとんどの上場企業の株主なので、最初は「共通点」から外す */
const CM_PASSIVE=/(信託|カストディ|vanguard|blackrock|state ?street|jp ?morgan|chase bank|master ?trust|mellon|ssbtc|norway|持株会|自己株|ノルウェー|生命保険|custody|nominee|bnym|goldman sachs international|citibank|hsbc|morgan stanley & co|ステート|ジェーピー|バンク・オブ|ゴールドマン|シティバンク|モルガン|証券金融|chase|omnibus|secs? lending|bank of new york|ssbt|bny|nominees|trust company|custodian|jpmorgan)/i;
const CM_KLAB={member:'在籍',invest:'出資',invest2:'出資',owns:'保有',govern:'管理',deal:'取引',uses:'AIを使う',from:'出身',moved:'移籍',conflict:'対立',link:'関係'};
const CM_KCOL={member:'var(--active)',invest:'var(--invest)',invest2:'var(--invest)',owns:'var(--org)',govern:'var(--org)',deal:'var(--deal)',uses:'var(--uses)',from:'var(--left)',moved:'var(--left)',conflict:'var(--conflict)',link:'var(--muted)'};
const cmEsc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

/* 会社ごとの相関図を1つの大きな図にまとめる(同じ人・同じ会社は1つの点に) */
function cmBuild(){
  if(CG)return CG;
  const nodes=[],idx=new Map(),edges=[],seen=new Map();
  const norm=s=>String(s||'').toLowerCase().replace(/[\s　\.\,・()（）]/g,'').replace(/(inc|corp|corporation|株式会社|holdings|group|グループ)$/,'');
  const add=(k,name,t,code)=>{k=CM_ALIAS[k]||k;if(!idx.has(k)){idx.set(k,nodes.length);nodes.push({k,n:name,t,code:null,en:'',pas:CM_PASSIVE.test(name)?1:0})}
    const o=nodes[idx.get(k)];if(code&&!o.code){o.code=code;o.n=name;o.t='c'}return idx.get(k)};
  for(const c of Object.keys(DATA)){if(!COMPANIES[c])continue;let d;try{d=DATA[c]()}catch(e){continue}
    const m={};
    d.N.forEach(n=>{const isC=n.id===d.center;const nm=isC?COMPANIES[c].name:n.name;const en=d.EN&&d.EN[n.id];
      const k=n.kind==='p'&&en?'p:'+en:(n.kind==='p'?'p:':'o:')+norm(nm);
      m[n.id]=add(k,nm,isC?'c':n.kind,isC?c:null);
      const o=nodes[m[n.id]];if(n.kind==='p'&&en&&!o.en)o.en=en;
      if(n.kind==='p'&&n.role)(o.r=o.r||[]).push([COMPANIES[c].name,n.role])});
    /* 同じ線が両方の会社の図にあるときは1本にまとめ、説明や出典があるほうを残す */
    d.E.forEach(e=>{const a=m[e.a],b=m[e.b];if(a==null||b==null||a===b)return;
      const kk=e.k==='invest2'?'invest':e.k,sym=kk==='deal'||kk==='link'||kk==='conflict';
      const sig=(sym?Math.min(a,b)+'|'+Math.max(a,b):a+'|'+b)+'|'+kk;
      const ne={a,b,k:e.k,l:e.label||'',y:e.since||'',d:(e.k==='deal'||e.k==='uses')?(e.d||''):'',src:e.src||null};
      if(seen.has(sig)){const o=edges[seen.get(sig)];if(!o.l&&ne.l)o.l=ne.l;if(!o.d&&ne.d)o.d=ne.d;if(!o.src&&ne.src)o.src=ne.src;if(!o.y&&ne.y)o.y=ne.y;return}
      seen.set(sig,edges.length);edges.push(ne)});
  }
  /* 相関図を持っていない会社の点も、名前が同じなら会社につなげる(クリックで開けるように) */
  const byName=new Map();for(const c of Object.keys(DATA)){if(COMPANIES[c])byName.set(norm(COMPANIES[c].name),c)}
  nodes.forEach(o=>{if(!o.code&&o.t!=='p'){const c=byName.get(o.k.slice(2));if(c)o.code=c}});
  const adj=nodes.map(()=>[]);edges.forEach((e,i)=>{adj[e.a].push([e.b,i]);adj[e.b].push([e.a,i])});
  CG={nodes,edges,adj,list:nodes.map((o,i)=>({i,n:o.n,l:o.n.toLowerCase(),deg:adj[i].length}))};
  return CG;
}
function cmFind(q){const G=cmBuild();q=String(q||'').trim().toLowerCase();if(!q)return[];
  const L=G.list,ex=L.filter(x=>x.l===q),st=L.filter(x=>x.l!==q&&x.l.startsWith(q)),inc=L.filter(x=>!x.l.startsWith(q)&&x.l.includes(q));
  const co=x=>G.nodes[x.i].t==='p'?0:1;   /* 同じくらいなら会社を先に */
  const s=(a,b)=>co(b)-co(a)||b.deg-a.deg;
  return ex.sort(s).concat(st.sort(s),inc.sort(s)).slice(0,12)}
function cmPick(v){const f=cmFind(v);return f.length?f[0].i:-1}

/* 線1本を文にする(向きは a→b) */
function cmSentence(e){const G=CG,A=G.nodes[e.a].n,B=G.nodes[e.b].n,l=e.l?`(${e.l})`:'';
  return {member:`${A} は ${B} に在籍${l}`,invest:`${A} が ${B} に出資${l}`,invest2:`${A} が ${B} に出資${l}`,owns:`${A} が ${B} を保有${l}`,govern:`${A} が ${B} を管理`,deal:`${A} と ${B} の取引${l}`,uses:`${A} が ${B} のAIを使う${l}`,from:`${A} は ${B} の出身`,moved:`${A} は ${B} へ移った`,conflict:`${A} と ${B} は対立${l}`,link:`${A} と ${B}${l||' がつながる'}`}[e.k]||`${A} — ${B}`}
function cmSrc(e){if(!e.src||typeof DS==='undefined')return '';const s=e.src.map(k=>DS[k]?`<a href="${cmEsc(DS[k][1])}" target="_blank" rel="noopener">${cmEsc(DS[k][0])}</a>`:'').filter(Boolean).join(' / ');return s?`<small class="cm-src">出典: ${s}</small>`:''}
function cmEdgeHtml(e){return `<span class="cm-e"><i style="background:${CM_KCOL[e.k]||'var(--muted)'}"></i>${cmEsc(cmSentence(e))}${e.y?` <span class="cm-y">${cmEsc(e.y)}年〜</span>`:''}</span>${e.d?`<small class="cm-d">${cmEsc(e.d)}</small>`:''}${cmSrc(e)}`}
function cmName(i){const o=CG.nodes[i];return o.code?`<a href="#" data-cmgo="${cmEsc(o.code)}"><b>${cmEsc(o.n)}</b></a>`:`<b>${cmEsc(o.n)}</b>`}
function cmTypeLabel(i){const t=CG.nodes[i].t;return t==='p'?'人':t==='i'?'出資者':'会社・組織'}

/* 2点のあいだの線をまとめて返す */
function cmEdgesBetween(x,y){const G=CG;return G.adj[x].filter(([z])=>z===y).map(([,ei])=>G.edges[ei])}
/* 共通の相手を、営業で使いやすい順に分ける */
function cmCommon(s,t,usePas){
  const G=CG,na=new Map(),nb=new Map();
  G.adj[s].forEach(([y,ei])=>{if(!na.has(y))na.set(y,[]);na.get(y).push(G.edges[ei])});
  G.adj[t].forEach(([y,ei])=>{if(!nb.has(y))nb.set(y,[]);nb.get(y).push(G.edges[ei])});
  const out={person:[],investor:[],deal:[],invested:[],other:[]};let hid=0;
  for(const [x,ea] of na){if(x===t||x===s||!nb.has(x))continue;const eb=nb.get(x);
    if(G.nodes[x].pas&&!usePas){hid++;continue}
    const all=ea.concat(eb),ks=new Set(all.map(e=>e.k));
    const xInv=e=>(e.k==='invest'||e.k==='invest2'||e.k==='owns'||e.k==='govern')&&e.a===x;
    const intoX=e=>(e.k==='invest'||e.k==='invest2'||e.k==='owns')&&e.b===x;
    const row={x,ea,eb,deg:G.adj[x].length};
    if(G.nodes[x].t==='p')out.person.push(row);
    else if(ks.has('deal')||ks.has('uses'))out.deal.push(row);
    else if(ea.some(xInv)&&eb.some(xInv))out.investor.push(row);
    else if(ea.some(intoX)&&eb.some(intoX))out.invested.push(row);
    else out.other.push(row);
  }
  /* 小さく近い相手ほど紹介を頼みやすいので、つながりの少ない順に並べる */
  Object.values(out).forEach(L=>L.sort((a,b)=>a.deg-b.deg));
  return {groups:out,hidden:hid};
}
/* 最短の道を、途中の相手が違うものから最大 max 本 */
function cmPaths(s,t,usePas,max){
  const G=CG,n=G.nodes.length,ok=y=>usePas||!G.nodes[y].pas||y===s||y===t;
  const ds=new Int32Array(n).fill(-1);ds[s]=0;let q=[s],h=0;
  while(h<q.length){const x=q[h++];if(x===t)continue;for(const [y] of G.adj[x]){if(ds[y]>=0||!ok(y))continue;ds[y]=ds[x]+1;q.push(y)}}
  if(ds[t]<0)return {len:-1,paths:[]};
  const L=ds[t],paths=[];
  /* t から逆にたどって、1つ手前の点ごとに候補を作る。人を通る道を先に */
  const back=(x,acc)=>{if(paths.length>=400)return;if(x===s){paths.push(acc.slice().reverse());return}
    const pre=[];const sn=new Set();for(const [y] of G.adj[x]){if(ds[y]===ds[x]-1&&!sn.has(y)){sn.add(y);pre.push(y)}}
    pre.sort((a,b)=>(G.nodes[b].t==='p')-(G.nodes[a].t==='p')||G.adj[a].length-G.adj[b].length);
    for(const y of pre.slice(0,12)){acc.push(y);back(y,acc);acc.pop()}};
  back(t,[t]);
  const score=p=>p.slice(1,-1).reduce((a,y)=>a+(G.nodes[y].t==='p'?-1000:0)+G.adj[y].length,0);
  paths.sort((a,b)=>score(a)-score(b));
  const used=new Set(),pick=[];
  for(const p of paths){const mid=p.slice(1,-1).join(',');const key=p[1]+'|'+p[p.length-2];if(used.has(key)||used.has(mid))continue;used.add(key);used.add(mid);pick.push(p);if(pick.length>=max)break}
  return {len:L,paths:pick};
}

function showCommon(a,b){
  stop();leavePerson();ctrail=[];
  MAINEL.hidden=true;controls.hidden=true;trailbar.hidden=true;document.getElementById('subbar').hidden=true;RANKEL.hidden=true;PROFEL.hidden=true;UNIEL.hidden=true;FEEDEL.hidden=false;
  document.querySelectorAll('#tabs button').forEach(b=>b.setAttribute('aria-pressed','false'));
  document.getElementById('title').textContent='2社の共通のつながり';document.title='2社の共通のつながり';
  document.getElementById('note').textContent='';
  if(typeof a==='string')commonA=a;if(typeof b==='string')commonB=b;
  if(!commonA&&!commonB){commonA='トヨタ自動車';commonB='ソフトバンクグループ'}
  FEEDEL.innerHTML=`<style>
  .cm-pick{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr) auto;gap:10px;align-items:end;max-width:900px}
  .cm-f{position:relative;display:grid;gap:4px;min-width:0}.cm-f label{font-size:12px;color:var(--muted)}
  .cm-f input{width:100%;box-sizing:border-box;padding:9px 12px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--fg);font:inherit;font-size:16px}
  .cm-sug{position:absolute;left:0;right:0;top:100%;z-index:20;margin:2px 0 0;padding:4px;list-style:none;background:var(--surface);border:1px solid var(--line);border-radius:8px;max-height:280px;overflow:auto;box-shadow:0 8px 24px rgba(0,0,0,.18)}
  .cm-sug li{padding:6px 10px;border-radius:6px;cursor:pointer;display:flex;gap:8px;align-items:baseline;min-width:0}
  .cm-sug li:hover,.cm-sug li[aria-selected="true"]{background:var(--soft)}
  .cm-sug small{color:var(--muted);margin-left:auto;font-family:var(--font-mono);font-size:11px;white-space:nowrap}
  .cm-ar{font-family:var(--font-mono);color:var(--muted);padding-bottom:10px}
  #cmgo{padding:9px 18px;font-weight:700;border-radius:8px;border:1px solid var(--fg);background:var(--fg);color:var(--bg);cursor:pointer;font:inherit}
  .cm-sum{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0 4px}
  .cm-sum div{border:1px solid var(--line);border-radius:10px;padding:8px 12px;background:var(--surface);min-width:0}
  .cm-sum b{display:block;font-family:var(--font-mono);font-size:24px;line-height:1.1}
  .cm-sum small{color:var(--muted);font-size:12px}
  .cm-g{margin:20px 0 0}.cm-g h3{margin:0 0 4px;font-size:15px}.cm-g>p{margin:0 0 8px;font-size:13px;color:var(--muted)}
  .cm-l{list-style:none;margin:0;padding:0;display:grid;gap:8px}
  .cm-l>li{border:1px solid var(--line);border-left:4px solid var(--c,var(--line));border-radius:8px;padding:8px 12px;background:var(--surface);min-width:0;overflow-wrap:anywhere}
  .cm-l .cm-k{font-size:11px;font-family:var(--font-mono);color:var(--muted);margin-left:6px}
  .cm-two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:4px 14px;margin-top:4px;font-size:13px}
  .cm-two>div{min-width:0}.cm-two .cm-h{font-size:11px;color:var(--muted)}
  .cm-e{display:inline}.cm-e i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px;vertical-align:middle}
  .cm-y,.cm-src,.cm-d{color:var(--muted);font-size:12px}.cm-d,.cm-src{display:block}
  .cm-route{list-style:none;margin:6px 0 0;padding:0}
  .cm-route li{position:relative;padding:0 0 0 26px;min-height:30px}
  .cm-route li::before{content:"";position:absolute;left:6px;top:6px;bottom:-4px;width:3px;background:var(--line);border-radius:2px}
  .cm-route li:last-child::before{display:none}
  .cm-route .cm-dot{position:absolute;left:0;top:3px;width:15px;height:15px;border-radius:50%;background:var(--c,var(--org))}
  .cm-route .cm-rel{display:block;font-size:12.5px;color:var(--muted);margin:1px 0 6px}
  .cm-more{font:inherit;font-size:13px;background:none;border:0;color:var(--active);cursor:pointer;padding:4px 0}
  #cmmemo{width:100%;box-sizing:border-box;min-height:140px;padding:10px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--fg);font:13px/1.6 var(--font-body)}
  @media (max-width:720px){.cm-pick{grid-template-columns:minmax(0,1fr)}.cm-ar{display:none}.cm-two{grid-template-columns:minmax(0,1fr)}}
  </style>
  <p class="meta" style="margin:0 0 12px;max-width:72ch">2つの会社(人でも選べます)を選ぶと、両方とつながっている人・出資者・取引先・使っているAIと、一番短いつながりの道を探します。営業先に、だれを通して入れそうかを見るための画面です。</p>
  <div class="cm-pick">
    <div class="cm-f"><label for="cma">自分の側(自社・知っている会社)</label><input id="cma" autocomplete="off" placeholder="例: トヨタ自動車" value="${cmEsc(commonA)}"><ul class="cm-sug" id="cmsa" role="listbox" hidden></ul></div>
    <div class="cm-ar">⇄</div>
    <div class="cm-f"><label for="cmb">相手(営業先)</label><input id="cmb" autocomplete="off" placeholder="例: ソフトバンクグループ" value="${cmEsc(commonB)}"><ul class="cm-sug" id="cmsb" role="listbox" hidden></ul></div>
    <button id="cmgo" type="button">探す</button>
  </div>
  <div class="row" style="margin-top:10px;flex-wrap:wrap;gap:6px" id="cmpre">
    <span class="meta" style="font-size:12px">例:</span>
    <button type="button" data-a="トヨタ自動車" data-b="ソフトバンクグループ">トヨタ ⇄ ソフトバンクG</button>
    <button type="button" data-a="楽天グループ" data-b="OpenAI">楽天 ⇄ OpenAI</button>
    <button type="button" data-a="Microsoft" data-b="Nvidia">Microsoft ⇄ Nvidia</button>
    <button type="button" data-a="トヨタ自動車" data-b="TSMC">トヨタ ⇄ TSMC</button>
    <button type="button" data-a="NTT" data-b="KDDI">NTT ⇄ KDDI</button>
  </div>
  <label style="display:flex;gap:6px;align-items:center;margin-top:10px;font-size:13px;color:var(--muted)"><input type="checkbox" id="cmpas" ${commonPas?'checked':''}> 株を持っているだけの信託銀行・大手運用会社(BlackRockなど)も含める</label>
  <div id="cmout" aria-live="polite" style="margin-top:6px"></div>`;
  const $=id=>document.getElementById(id);
  const wire=(inp,ul)=>{let items=[],sel=-1;
    const render=()=>{ul.innerHTML=items.map((x,k)=>`<li role="option" aria-selected="${k===sel}" data-k="${k}">${cmEsc(x.n)}<small>${cmTypeLabel(x.i)}・${x.deg}</small></li>`).join('');ul.hidden=!items.length};
    inp.addEventListener('input',()=>{items=cmFind(inp.value);sel=-1;render()});
    inp.addEventListener('keydown',ev=>{if(ev.key==='Enter'&&ul.hidden){ev.preventDefault();cmRun();return}if(ul.hidden)return;
      if(ev.key==='ArrowDown'){sel=Math.min(items.length-1,sel+1);render();ev.preventDefault()}else if(ev.key==='ArrowUp'){sel=Math.max(0,sel-1);render();ev.preventDefault()}
      else if(ev.key==='Enter'){if(sel>=0)inp.value=items[sel].n;ul.hidden=true;ev.preventDefault();cmRun()}else if(ev.key==='Escape')ul.hidden=true});
    ul.addEventListener('mousedown',ev=>{const li=ev.target.closest('li');if(!li)return;inp.value=items[+li.dataset.k].n;ul.hidden=true;ev.preventDefault();cmRun()});
    inp.addEventListener('blur',()=>setTimeout(()=>{ul.hidden=true},150));
  };
  wire($('cma'),$('cmsa'));wire($('cmb'),$('cmsb'));
  $('cmgo').addEventListener('click',cmRun);
  $('cmpas').addEventListener('change',e=>{commonPas=e.target.checked;cmRun()});
  $('cmpre').querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{$('cma').value=b.dataset.a;$('cmb').value=b.dataset.b;cmRun()}));
  /* 名前のリンク: その会社の相関図を開く。戻るとこの画面に戻れるように、選んだ2社は覚えておく */
  $('cmout').addEventListener('click',ev=>{const a=ev.target.closest('a[data-cmgo]');if(a){ev.preventDefault();build(a.dataset.cmgo);return}
    const m=ev.target.closest('button[data-cmmore]');if(m){const ul=$(m.dataset.cmmore);ul.querySelectorAll('li[hidden]').forEach(li=>li.hidden=false);m.remove()}});
  cmRun();
  if(typeof navSync==='function')navSync();
  window.scrollTo(0,0);
}
function cmRun(){
  const $=id=>document.getElementById(id);const G=cmBuild();
  const out=$('cmout');
  if(!$('cma').value.trim()||!$('cmb').value.trim()){out.innerHTML='<p class="meta" style="margin-top:12px">2つめの会社を入力して、候補から選んでください。</p>';return}
  const s=cmPick($('cma').value),t=cmPick($('cmb').value);
  if(s<0||t<0){out.innerHTML=`<p>「${cmEsc(s<0?$('cma').value:$('cmb').value)}」が見つかりませんでした。入力すると出る候補から選んでください。この画面で選べるのは、企業の相関図に載っている会社と人です。</p>`;return}
  if(s===t){out.innerHTML='<p>同じ会社が選ばれています。別の会社を選んでください。</p>';return}
  $('cma').value=G.nodes[s].n;$('cmb').value=G.nodes[t].n;commonA=G.nodes[s].n;commonB=G.nodes[t].n;
  try{history.replaceState(null,'','#common')}catch(e){}
  const A=G.nodes[s].n,B=G.nodes[t].n,usePas=commonPas;
  const direct=cmEdgesBetween(s,t);
  const {groups,hidden}=cmCommon(s,t,usePas);
  const P=cmPaths(s,t,usePas,5);
  const GRP=[
    ['person','共通の人物','両方の会社に、いま・以前に関わった人です。一番声をかけやすい入り口です。','var(--active)'],
    ['investor','共通の出資者・株主','両方に出資している投資家や親会社です。投資先どうしの紹介をお願いできることがあります。','var(--invest)'],
    ['deal','共通の取引先・使っているAI','両方と取引がある会社や、両方が使っているAI(または両方に使われているAI)です。','var(--deal)'],
    ['invested','どちらも出資している会社','両方が株を持っている会社です。株主どうしとして話のきっかけになります。','var(--org)'],
    ['other','そのほかの共通の相手','提携・出身・対立など、そのほかの関係で両方とつながっている相手です。','var(--muted)']];
  const nCommon=GRP.reduce((a,g)=>a+groups[g[0]].length,0);
  const row=r=>`<div><b>${cmName(r.x)}</b><span class="cm-k">${cmTypeLabel(r.x)}・つながり${r.deg}</span></div>
    <div class="cm-two"><div><span class="cm-h">${cmEsc(A)} との関係</span><br>${r.ea.map(cmEdgeHtml).join('<br>')}</div><div><span class="cm-h">${cmEsc(B)} との関係</span><br>${r.eb.map(cmEdgeHtml).join('<br>')}</div></div>`;
  const grpHtml=GRP.map(([k,h,p,c])=>{const L=groups[k];if(!L.length)return '';const id='cml_'+k;
    return `<section class="cm-g"><h3>${h} <span class="cm-k">${L.length}</span></h3><p>${p}</p><ul class="cm-l" id="${id}" style="--c:${c}">${L.map((r,i)=>`<li${i>=8?' hidden':''}>${row(r)}</li>`).join('')}</ul>${L.length>8?`<button type="button" class="cm-more" data-cmmore="${id}">ほかの${L.length-8}件も見る ▾</button>`:''}</section>`}).join('');
  const TC={p:'var(--active)',i:'var(--invest)',o:'var(--org)',c:'var(--fg)'};
  const routeHtml=p=>`<ol class="cm-route">${p.map((x,k)=>{const nx=p[k+1];let rel='';
    if(nx!=null){const e=cmEdgesBetween(x,nx)[0];rel=e?`<span class="cm-rel">${cmEsc(cmSentence(e))} <span class="cm-k">${CM_KLAB[e.k]||''}</span></span>`:''}
    return `<li style="--c:${TC[G.nodes[x].t]||'var(--org)'}"><span class="cm-dot"></span>${cmName(x)} <span class="cm-k">${cmTypeLabel(x)}</span>${rel}</li>`}).join('')}</ol>`;
  const pathsHtml=P.len<0?`<p class="meta">この相関図の中では、${cmEsc(A)} と ${cmEsc(B)} をつなぐ道は見つかりませんでした。</p>`
    :P.len===1?`<p class="meta">直接つながっています(上の「直接のつながり」)。</p>`
    :`<p class="meta" style="margin:0 0 6px">${P.len}ステップでつながります。途中の相手が違う道を${P.paths.length}本まで、人を通る道を先に出しています。</p>${P.paths.map((p,i)=>`<div style="border:1px solid var(--line);border-radius:8px;padding:8px 12px;background:var(--surface);margin-bottom:8px;min-width:0;overflow-wrap:anywhere"><div class="cm-k" style="margin:0 0 4px">道 ${i+1}</div>${routeHtml(p)}</div>`).join('')}`;
  /* 営業メモ(コピーして使う) */
  const memo=[`【${A} と ${B} の接点】(AI企業の相関図より)`];
  if(direct.length)memo.push('■ 直接のつながり',...direct.map(e=>'・'+cmSentence(e)));
  GRP.forEach(([k,h])=>{const L=groups[k];if(!L.length)return;memo.push(`■ ${h}(${L.length})`);L.slice(0,5).forEach(r=>memo.push(`・${G.nodes[r.x].n}: ${r.ea.map(cmSentence).join('、')} / ${r.eb.map(cmSentence).join('、')}`))});
  if(P.len>1&&P.paths[0])memo.push(`■ 最短ルート(${P.len}ステップ)`,'・'+P.paths[0].map(x=>G.nodes[x].n).join(' → '));
  memo.push('※ 相関図に載っている範囲の情報です。連絡の前に、最新の状況を確かめてください。');
  out.innerHTML=`<div class="cm-sum">
     <div><b>${direct.length}</b><small>直接のつながり</small></div>
     <div><b>${groups.person.length}</b><small>共通の人物</small></div>
     <div><b>${groups.investor.length}</b><small>共通の出資者</small></div>
     <div><b>${groups.deal.length}</b><small>共通の取引先・AI</small></div>
     <div><b>${P.len<0?'—':P.len}</b><small>最短ステップ</small></div></div>
   ${direct.length?`<section class="cm-g"><h3>直接のつながり</h3><ul class="cm-l" style="--c:var(--fg)">${direct.map(e=>`<li>${cmEdgeHtml(e)}</li>`).join('')}</ul></section>`:''}
   ${grpHtml||`<section class="cm-g"><h3>共通の相手</h3><p>両方と直接つながっている相手は、この相関図の中にはいませんでした。下の「最短ルート」を見てください。</p></section>`}
   ${hidden&&!usePas?`<p class="note" style="margin-top:10px">株を持っているだけの信託銀行・大手運用会社 ${hidden}社は外しています(上のチェックで含められます)。</p>`:''}
   <section class="cm-g"><h3>最短ルート</h3>${pathsHtml}</section>
   <section class="cm-g"><h3>営業メモ</h3><p>そのまま社内のメモやメールの下書きに貼れます。</p><textarea id="cmmemo" aria-label="営業メモ">${cmEsc(memo.join('\n'))}</textarea>
     <div class="row" style="margin-top:6px"><button type="button" id="cmcp">メモをコピー</button><span id="cmcpm" class="meta" style="font-size:12px"></span></div></section>
   <p class="note" style="margin-top:16px">データは企業の相関図(${Object.keys(DATA).filter(c=>COMPANIES[c]).length.toLocaleString()}社の図、${G.nodes.length.toLocaleString()}の人と会社、${G.edges.length.toLocaleString()}本の線)です。会社名をクリックすると、その会社の相関図を開きます。相関図に載っていない関係は出ません。</p>`;
  document.getElementById('cmcp').addEventListener('click',()=>{const ta=document.getElementById('cmmemo');const m=document.getElementById('cmcpm');
    (navigator.clipboard?navigator.clipboard.writeText(ta.value):Promise.reject()).then(()=>{m.textContent='コピーしました'}).catch(()=>{ta.select();m.textContent='選択しました。コピーしてください'})});
}
/* 会社の相関図の右の欄に出すリンク */
function commonBtn(){const nm=COMPANIES[comp]?COMPANIES[comp].name:'';if(!nm)return '';
  return `<div class="links"><a href="#" id="gocommon"><b>${cmEsc(nm)}と、ほかの会社の共通のつながりを探す ▸</b></a><small style="display:block;color:var(--muted)">共通の出資者・人物・取引先と最短ルート(営業先との接点探しに)</small></div>`}
function wireCommon(){const g=document.getElementById('gocommon');if(g)g.addEventListener('click',ev=>{ev.preventDefault();const nm=COMPANIES[comp].name;showCommon(nm,commonA&&commonA!==nm?commonA:'');setTimeout(()=>{const b=document.getElementById('cmb');if(b&&!b.value)b.focus()},50)})}
