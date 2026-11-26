// 企業ごとの「情報の薄さ」を点数にする。使い方: node scripts/depth_score.js  → inbox/depth/latest.json と latest.md を作る(読むだけ・サイトは変えない)
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+path.join(__dirname,'..','site','index.html'),{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
const r=await p.evaluate(()=>{const out=[];
 for(const c of Object.keys(DATA)){if(!COMPANIES[c])continue;let d;try{d=DATA[c]()}catch(e){continue}
  const kinds={};d.E.forEach(e=>kinds[e.k]=(kinds[e.k]||0)+1);
  const people=d.N.filter(n=>n.kind==='p');
  const exec=people.filter(n=>n.role).length;
  const withSrc=d.E.filter(e=>e.src||e.s||e.ds).length;
  out.push({key:c,name:COMPANIES[c].name,nodes:d.N.length,edges:d.E.length,people:people.length,exec,kinds});}
 return out});
fs.mkdirSync(path.join(__dirname,'..','inbox','depth'),{recursive:true});
const rank=JSON.parse(fs.readFileSync(path.join(__dirname,'..','inbox','ranking','latest.json'),'utf8'));
fs.writeFileSync(path.join(__dirname,'..','inbox','depth','raw.json'),JSON.stringify(r,null,1));
console.log(r.length,'companies');console.log(Object.keys(rank));
await b.close()})();
