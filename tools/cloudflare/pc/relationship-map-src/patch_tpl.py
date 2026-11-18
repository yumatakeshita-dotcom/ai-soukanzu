p='hub_template.html';s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(a[:60],s.count(a))
    s=s.replace(a,b)
rep("/* 関連組織をダブルクリックして開く図","""COMPANIES.__rank__={name:'米国 時価総額ランキング',min:2026,sub:1,note:''};
RANK.forEach(r=>{if(!r.new||COMPANIES[r.key])return;
  COMPANIES[r.key]={name:r.en,min:2026,sub:1,note:'役職は英語版Wikipediaの「Key people」(2026年11月2日に取得)に基づきます。2026年の交代を反映していない場合があります。時価総額は日経の米国株ランキング(2026年10月30日終値)です。大株主・投資家と、載せていない役員は、まだ調べていません。顔写真がない人はイニシャル表示です。'}});
/* 関連組織をダブルクリックして開く図""")
rep("paypay:'paypay',ivry:'ivry'","spacex:'us_SPCX',waymo:'waymo',slack:'slack',paypay:'paypay',ivry:'ivry'")
rep('  <div class="main">\n    <div class="stage">','''  <section id="rankview" hidden></section>
  <div class="main">
    <div class="stage">''')
rep("function build(key,drill){\n  stop();leavePerson();","function build(key,drill){\n  stop();leavePerson();hideRank();")
rep("let ctrail=[];","""let ctrail=[],rankPage=1;
const MAINEL=document.querySelector('.main'),RANKEL=document.getElementById('rankview');
function hideRank(){RANKEL.hidden=true;MAINEL.hidden=false;controls.hidden=false}
function ceoOf(key){
  if(!DATA[key])return '';
  try{const d=DATA[key]();const n=d.N.find(n=>n.kind==='p'&&/^(CEO|共同CEO)/.test(n.role||''))||d.N.find(n=>n.kind==='p'&&/^(会長兼CEO|社長兼CEO)/.test(n.role||''));return n?n.name:''}catch(e){return ''}
}
function showRank(p){
  stop();leavePerson();rankPage=p||rankPage;ctrail=[];
  MAINEL.hidden=true;controls.hidden=true;trailbar.hidden=true;document.getElementById('subbar').hidden=true;RANKEL.hidden=false;
  document.getElementById('title').textContent='米国 時価総額上位200社';document.title='米国 時価総額ランキング';
  document.querySelectorAll('#tabs button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.k==='__rank__')));
  const per=30,pages=Math.ceil(RANK.length/per),rows=RANK.slice((rankPage-1)*per,rankPage*per);
  const cap=c=>c>=1e6?(c/1e6).toFixed(2)+'兆ドル':Math.round(c/100)/10+'十億ドル';
  const pg=Array.from({length:pages},(_,i)=>`<button type="button" data-p="${i+1}" aria-pressed="${i+1===rankPage}">${i*per+1}–${Math.min((i+1)*per,RANK.length)}位</button>`).join('');
  RANKEL.innerHTML=`<p class="note">日経の「米国株 時価総額上位ランキング」(2026年11月2日更新、10月30日終値)の200社です。会社名をクリックすると、その会社の社長・経営陣の図(ピラミッド・相関図)が開きます。</p>
  <div class="tabs row" id="rankpg">${pg}</div>
  <table class="rtable"><thead><tr><th>順位</th><th>会社</th><th>ティッカー</th><th>時価総額</th><th>CEO</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${r.r}</td><td><a href="#" data-k="${r.key}">${r.en}</a><br><small>${r.jp}</small></td><td>${r.tk}</td><td>${cap(r.cap)}</td><td>${ceoOf(r.key)}</td></tr>`).join('')}</tbody></table>`;
  RANKEL.querySelectorAll('#rankpg button').forEach(b=>b.addEventListener('click',()=>showRank(+b.dataset.p)));
  RANKEL.querySelectorAll('a[data-k]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();ctrail=['__rank__'];build(a.dataset.k,true)}));
  window.scrollTo(0,0);
}""")
rep("document.getElementById('subback').addEventListener('click',()=>{const p=ctrail.pop();build(p,true)});","document.getElementById('subback').addEventListener('click',()=>{const p=ctrail.pop();if(p==='__rank__')showRank();else build(p,true)});")
rep(" ['日本の企業',['sakana','softbank','pfn','pksha','rakuten','ly','mercari','boost']]]"," ['日本の企業',['sakana','softbank','pfn','pksha','rakuten','ly','mercari','boost']],\n ['ランキング',['__rank__']]]")
rep("b.addEventListener('click',()=>{if(k!==comp)build(k)});g.append(b);","b.addEventListener('click',()=>{if(k==='__rank__')showRank();else if(k!==comp||!RANKEL.hidden)build(k)});g.append(b);")
rep("b.dataset.k=k;b.textContent=COMPANIES[k].name;","b.dataset.k=k;b.textContent=k==='__rank__'?'米国 時価総額上位200社':COMPANIES[k].name;")
rep("build(COMPANIES[h0]?h0:'openai');","if(h0==='rank')showRank(1);else build(COMPANIES[h0]?h0:'openai');")
rep("</style>",""".rtable{width:100%;border-collapse:collapse;font-size:14px;margin-top:10px}.rtable th,.rtable td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line)}.rtable small{opacity:.65}#rankview{overflow-x:auto}
</style>""")
open(p,'w',encoding='utf-8').write(s)
