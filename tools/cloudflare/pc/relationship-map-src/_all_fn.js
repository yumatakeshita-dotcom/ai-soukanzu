/* 全企業リスト: bulk.json(SEC・東証・Wikidataの会社)を、開いたときに読み込んで、検索・絞り込みして見る */
const allState={q:'',src:'',c:'',lim:100,data:null,loading:false,err:''};
function allLoad(cb){
  if(allState.data||allState.loading){return}
  allState.loading=true;
  fetch('bulk.json').then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.json()}).then(d=>{allState.data=d;allState.loading=false;cb()}).catch(e=>{allState.loading=false;allState.err='全企業リストを読み込めませんでした('+e.message+')。';cb()});
}
function showAll(){
  stop();leavePerson();
  MAINEL.hidden=true;controls.hidden=true;trailbar.hidden=true;document.getElementById('subbar').hidden=true;RANKEL.hidden=true;PROFEL.hidden=true;UNIEL.hidden=true;FEEDEL.hidden=false;
  document.querySelectorAll('#tabs button').forEach(b=>b.setAttribute('aria-pressed','false'));
  document.getElementById('title').textContent='全企業リスト';document.title='全企業リスト';
  document.getElementById('note').textContent='米国の上場企業(SEC)、東証の上場企業(JPX)、英語版Wikipediaに記事のある世界の会社(Wikidata)をまとめた一覧です。他の画面(ユニコーン、Y Combinator、VCの投資先、世界の企業など)の会社は、ここには含めず、それぞれの画面にあります。上場・非上場や業種などは、出どころに記載のあるものだけです。';
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  if(!allState.data){
    FEEDEL.innerHTML=allState.err?`<p class="note">${esc(allState.err)}</p>`:'<p class="note">読み込み中…(約数MB)</p>';
    allLoad(showAll);window.scrollTo(0,0);return;
  }
  const D=allState.data,R=D.rows;const q=norm(allState.q);
  const cnt={};R.forEach(r=>{cnt[r[2]]=(cnt[r[2]]||0)+1});const top=Object.entries(cnt).sort((a,b)=>b[1]-a[1]).slice(0,14);
  const sc={S:0,J:0,W:0};R.forEach(r=>sc[r[5]]++);
  const rows=R.filter(r=>(!allState.src||r[5]===allState.src)&&(!allState.c||r[2]===allState.c)&&(!q||norm(r[0]+' '+r[1]+' '+r[2]+' '+r[3]+' '+r[6]).includes(q)));
  const btn=(attr,val,cur,label)=>`<button type="button" data-${attr}="${esc(val)}" aria-pressed="${String(cur)===String(val)}">${esc(label)}</button>`;
  const link=r=>{if(r[5]==='W')return `https://www.wikidata.org/wiki/${r[6]}`;if(r[5]==='S')return `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=${r[6].split('|')[0]}`;return `https://www.google.com/search?q=${encodeURIComponent((r[1]||r[0])+' 証券コード '+r[6].split('|')[0])}`};
  FEEDEL.innerHTML=`<p class="note">全企業リスト <b>${R.length.toLocaleString()}社</b>(米国上場 ${sc.S.toLocaleString()} / 東証上場 ${sc.J.toLocaleString()} / Wikidata ${sc.W.toLocaleString()})。作成日 ${esc(D.built||'')}。</p>
  <div class="pf-filter" style="margin:8px 0"><input id="alq" type="search" placeholder="会社名・国・業種・証券コードで絞り込み" value="${esc(allState.q)}" style="padding:6px 10px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--fg);min-width:260px">
   ${btn('s','',allState.src,'すべて')}${btn('s','S',allState.src,'米国上場')}${btn('s','J',allState.src,'東証上場')}${btn('s','W',allState.src,'Wikidata')}</div>
  <div class="pf-filter" style="margin:6px 0">${btn('c','',allState.c,'国: すべて')}${top.map(([c,n])=>btn('c',c,allState.c,`${c}(${n.toLocaleString()})`)).join('')}</div>
  <p class="note">${rows.length.toLocaleString()}社${rows.length>allState.lim?`(先頭${allState.lim}社を表示)`:''}</p>
  <table class="rtable"><thead><tr><th>会社</th><th>国</th><th>業種・市場</th><th>設立</th><th>出どころ</th></tr></thead><tbody>${rows.slice(0,allState.lim).map(r=>`<tr><td><a href="${esc(link(r))}" target="_blank" rel="noopener">${esc(r[0]||r[1])}</a>${r[0]&&r[1]?`<br><small>${esc(r[1])}</small>`:''}</td><td><small>${esc(r[2])}</small></td><td><small>${esc(r[3])}${r[5]==='J'?' / '+esc(r[6].split('|')[1]||'')+' '+esc(r[6].split('|')[0]):''}${r[5]==='S'?' / '+esc(r[6].split('|')[1]||''):''}</small></td><td>${r[4]||''}</td><td><small>${esc(({S:'SEC',J:'JPX',W:'Wikidata'})[r[5]])}</small></td></tr>`).join('')||'<tr><td colspan="5">該当なし</td></tr>'}</tbody></table>
  ${rows.length>allState.lim?'<p><button type="button" id="almore">さらに100社を表示</button></p>':''}
  <p class="note">出どころ: ${Object.entries(D.src).map(([k,v])=>`${esc(v[0])}(<a href="${esc(v[1])}" target="_blank" rel="noopener">${k}</a>)`).join(' / ')}</p>`;
  const qi=document.getElementById('alq');qi.addEventListener('input',()=>{allState.q=qi.value;allState.lim=100;clearTimeout(showAll.t);showAll.t=setTimeout(()=>{showAll();const e=document.getElementById('alq');e.focus();e.setSelectionRange(e.value.length,e.value.length)},250)});
  FEEDEL.querySelectorAll('button[data-s]').forEach(b=>b.addEventListener('click',()=>{allState.src=b.dataset.s;allState.lim=100;showAll()}));
  FEEDEL.querySelectorAll('button[data-c]').forEach(b=>b.addEventListener('click',()=>{allState.c=b.dataset.c;allState.lim=100;showAll()}));
  const mo=document.getElementById('almore');if(mo)mo.addEventListener('click',()=>{allState.lim+=100;showAll()});
  window.scrollTo(0,0);
}
