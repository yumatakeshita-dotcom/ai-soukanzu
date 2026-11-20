// 確かな版の見本集の元データを作る(2026/11/20)。次に scripts/kakujitsu_samples.py を実行する
const {chromium}=require('playwright');const {start}=require(process.cwd()+'/scripts/serve');const fs=require('fs');
(async()=>{const srv=await start(8133);const b=await chromium.launch();const pg=await b.newPage();
await pg.goto('http://localhost:8133/index.html',{waitUntil:'load',timeout:120000});await pg.waitForTimeout(1500);
const rows=await pg.evaluate(()=>cfListRows().filter(x=>x.pct>=60&&x.tot>=5).sort((a,b)=>b.tot-a.tot));
fs.mkdirSync('/tmp/kk_samples',{recursive:true});const out=[];for(const r of rows){const h=await pg.evaluate(k=>{build(k);const D=kkData();return {html:kkHtml(D),pct:D.pct,cnt:D.cnt,title:D.title||''};},r.k);out.push({...r,...h});}
fs.writeFileSync('/tmp/kk_samples/kk5.json',JSON.stringify(out));console.log(out.map(o=>o.k+' '+o.pct+' '+o.html.length).join('\n'));
const css=await pg.evaluate(()=>typeof KK_CSS!=='undefined'?KK_CSS:'');fs.writeFileSync('/tmp/kk_samples/kkcss.txt',css);
await b.close();srv.close();})();
