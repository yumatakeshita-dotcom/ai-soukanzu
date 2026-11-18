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
  r.sort((a,b)=>b.r-a.r||a.pct-b.pct);
  const lines=[`報道だけの線が多い会社(${new Date().toISOString().slice(0,10)})`,'順位 会社(キー) 報道だけ/公式・開示/確かめた割合'];
  r.slice(0,top).forEach((x,i)=>{lines.push(`${i+1}. ${x.name}(${x.k}) 報道${x.r} / 公式・開示${x.ok} / ${x.pct}%`);x.items.forEach(t=>lines.push('    - '+t))});
  const txt=lines.join('\n');console.log(txt);
  fs.mkdirSync(path.join(__dirname,'..','inbox','verify'),{recursive:true});fs.writeFileSync(path.join(__dirname,'..','inbox','verify','rank.txt'),txt+'\n');
  await b.close();srv.close();
})();
