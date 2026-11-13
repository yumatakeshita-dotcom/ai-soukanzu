// 本体の相関図から、ラボ用のデータ(全体のつながり)を書き出す。使い方: node scripts/export_graph.js
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+require('path').join(__dirname,'..','site','index.html'),{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
const g=await p.evaluate(()=>{
  const nodes=[],idx=new Map(),edges=[],seen=new Set();
  const norm=s=>String(s||'').toLowerCase().replace(/[\s　\.\,・()（）]/g,'').replace(/(inc|corp|corporation|株式会社|holdings|group|グループ)$/,'');
  const keyOf=(d,n,c)=>{const en=d.EN&&d.EN[n.id];if(n.kind==='p'&&en)return 'p:'+en;const nm=n.id===d.center?COMPANIES[c].name:n.name;return (n.kind==='p'?'p:':'o:')+norm(nm)};
  const add=(k,name,kind,c)=>{if(!idx.has(k)){idx.set(k,nodes.length);nodes.push({k,n:name,t:kind,c:[]})}const o=nodes[idx.get(k)];if(c&&!o.c.includes(c))o.c.push(c);return idx.get(k)};
  for(const c of Object.keys(DATA)){if(!COMPANIES[c])continue;let d;try{d=DATA[c]()}catch(e){continue}
    const m={};d.N.forEach(n=>{const k=keyOf(d,n,c);const nm=n.id===d.center?COMPANIES[c].name:n.name;m[n.id]=add(k,nm,n.id===d.center?'c':n.kind,n.id===d.center?c:null);
      const o=nodes[m[n.id]];if(n.kind==='p'){(o.r=o.r||[]).push([COMPANIES[c].name,n.role||'',n.from||'',n.to||''])}});
    d.E.forEach(e=>{const a=m[e.a],bb=m[e.b];if(a==null||bb==null||a===bb)return;const sig=a+'|'+bb+'|'+e.k;if(seen.has(sig))return;seen.add(sig);edges.push([a,bb,e.k,e.label||'',e.since||'',e.k==='deal'?(e.d||''):''])});
  }
  return {nodes,edges};
});
fs.writeFileSync(require('path').join(__dirname,'..','src','lab','graph_raw.json'),JSON.stringify(g));
const kinds={};g.edges.forEach(e=>kinds[e[2]]=(kinds[e[2]]||0)+1);
console.log('nodes',g.nodes.length,'edges',g.edges.length,kinds,'MB',(fs.statSync(require('path').join(__dirname,'..','src','lab','graph_raw.json')).size/1e6).toFixed(2));
await b.close()})();
