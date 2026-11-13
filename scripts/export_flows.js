// 本体の相関図から、人の移籍データを書き出す。使い方: node scripts/export_flows.js
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+require('path').join(__dirname,'..','site','index.html'),{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
const F=await p.evaluate(()=>{const out=[];for(const c of Object.keys(DATA)){if(!COMPANIES[c])continue;let d;try{d=DATA[c]()}catch(e){continue}
 const by=Object.fromEntries(d.N.map(n=>[n.id,n]));const cn=COMPANIES[c].name;
 d.E.forEach(e=>{if(e.k!=='from'&&e.k!=='moved')return;let P=by[e.a],O=by[e.b];if(!P||!O)return;if(P.kind!=='p'){[P,O]=[O,P]}if(P.kind!=='p'||O.kind==='p')return;
  const en=(d.EN||{})[P.id]||P.name;
  if(e.k==='from')out.push({p:P.name,en,from:O.name,to:cn,y:e.since||P.from,desc:P.desc||''});
  else out.push({p:P.name,en,from:cn,to:O.name,y:P.to||e.since||'',desc:P.desc||''});
 })}return out});
fs.writeFileSync(require('path').join(__dirname,'..','src','lab','flows_raw.json'),JSON.stringify(F));console.log(F.length);
const c={};F.forEach(f=>{const k=f.from+' → '+f.to;c[k]=(c[k]||0)+1});console.log(Object.entries(c).sort((a,b)=>b[1]-a[1]).slice(0,50).map(x=>x.join(':')).join('\n'));
await b.close()})();
