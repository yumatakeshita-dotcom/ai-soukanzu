// 報道だけの線が多い会社の順位を出す(2026/11/18追加)
// 使い方: node scripts/cf_rank.js [件数]   → inbox/verify/rank.txt にも保存
// 毎週日曜の「報道だけの数字を確かめ直す」タスクは、この上位の会社から順に確かめる
const {chromium}=require('playwright');const {start}=require('./serve');const fs=require('fs');const path=require('path');
(async()=>{
  const top=+process.argv[2]||20;const port=8130+Math.floor(Math.random()*50);
  const srv=await start(port);const b=await chromium.launch();const pg=await b.newPage();
  await pg.goto(`http://localhost:${port}/index.html`,{waitUntil:'load',timeout:120000});await pg.waitForTimeout(1500);
  const r=await pg.evaluate(()=>{const out=[];Object.keys(COMPANIES).forEach(k=>{if(!DATA[k])return;try{build(k)}catch(e){return}
    const D=kkData();const weak=D.ref.filter(x=>x.cf==='r');
    out.push({k,name:D.name,pct:D.pct,ok:D.cnt.o+D.cnt.f+D.cnt.s,r:weak.length,items:weak.slice(0,8).map(x=>`${x.who}|${x.kind}|${x.label}`)})});return out});
  // 週ごとの記録(2026/11/19追加): 確かさの一覧と同じ数え方で、全体と会社ごとの割合を site/data/cfhist.js に足す。同じ日の記録だけ置き換え、前の記録は消さない
  const snap=await pg.evaluate(()=>{const rows=cfListRows();const ok=rows.reduce((s,x)=>s+x.o+x.f+x.s,0),tot=rows.reduce((s,x)=>s+x.tot,0);
    const c={};rows.forEach(x=>c[x.k]=x.pct);return {ok,tot,pct:tot?Math.round(ok*100/tot):0,c}});
  const t=new Date(Date.now()+9*3600e3);snap.d=t.toISOString().slice(0,10); // 日本時間の日付
  const hf=path.join(__dirname,'..','site','data','cfhist.js');let hist=[];
  if(fs.existsSync(hf)){const m=fs.readFileSync(hf,'utf8').match(/=\s*(\[[\s\S]*\]);?\s*$/);if(m)hist=JSON.parse(m[1])}
  hist=hist.filter(h=>h.d!==snap.d);hist.push({d:snap.d,pct:snap.pct,ok:snap.ok,tot:snap.tot,c:snap.c});hist.sort((a,b)=>a.d<b.d?-1:1);
  fs.writeFileSync(hf,'// 確かさの一覧の週ごとの記録(scripts/cf_rank.js が足す。手で消さない)。d=日付 pct=全体の割合 ok/tot=件数 c=会社ごとの割合\nconst CFHIST=[\n'+hist.map(h=>JSON.stringify(h)).join(',\n')+'\n];\n');
  console.log(`記録: ${snap.d} 全体${snap.pct}%(${snap.ok}/${snap.tot}) → site/data/cfhist.js`);
  r.sort((a,b)=>b.r-a.r||a.pct-b.pct);
  const lines=[`報道だけの線が多い会社(${new Date(Date.now()+9*3600e3).toISOString().slice(0,10)})`,'順位 会社(キー) 報道だけ/公式・開示/確かめた割合'];
  r.slice(0,top).forEach((x,i)=>{lines.push(`${i+1}. ${x.name}(${x.k}) 報道${x.r} / 公式・開示${x.ok} / ${x.pct}%`);x.items.forEach(t=>lines.push('    - '+t))});
  const txt=lines.join('\n');console.log(txt);
  fs.mkdirSync(path.join(__dirname,'..','inbox','verify'),{recursive:true});fs.writeFileSync(path.join(__dirname,'..','inbox','verify','rank.txt'),txt+'\n');
  await b.close();srv.close();
})();
