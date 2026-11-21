// NotebookLM用の書き出し(その1): 本体の相関図を開いて、全部の会社の図と関連データを JSON に書き出す。
// 使い方: node scripts/nblm_dump.js [出力先.json]   ※続けて python3 scripts/nblm_md.py を実行する
// 読むだけ。サイトのファイルは変えない。顔写真(data:)は書き出さない。2026/11/19追加
const {chromium}=require('playwright');const fs=require('fs'),path=require('path'),vm=require('vm');
const OUT=process.argv[2]||'/tmp/nblm_dump.json';const SITE=path.join(__dirname,'..','site');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+path.join(SITE,'index.html'),{waitUntil:'load',timeout:180000});await p.waitForTimeout(4000);
const r=await p.evaluate(()=>{
 const strip=o=>JSON.parse(JSON.stringify(o,(k,v)=>typeof v==='string'&&v.startsWith('data:')?undefined:v));
 const one=(d,name,min,note)=>({name,min:min||'',note:note||'',center:d.center,
  N:d.N.map(n=>({id:n.id,name:n.name,kind:n.kind,role:n.role||'',from:n.from||'',to:n.to||'',desc:n.desc||'',en:(d.EN||{})[n.id]||'',cf:typeof nodeCf==='function'?nodeCf(n):'',src:(n.src||[]),wiki:(d.WIKI||{})[n.id]||'',x:(d.X||{})[n.id]||'',web:(d.WEB||{})[n.id]||'',founder:n.founder||0})),
  E:d.E.map(e=>({a:e.a,b:e.b,k:e.k,label:e.lb||e.label||'',d:e.d||'',since:e.since||'',cf:typeof edgeCf==='function'?edgeCf(e):'',src:e.src||[]})),
  links:strip(d.LINKS||{}),career:strip(d.CAREER||{})});
 const maps={};
 for(const k of Reflect.ownKeys(COMPANIES)){if(typeof k!=='string'||k.startsWith('__')||!DATA[k])continue;
  try{maps[k]=one(DATA[k](),COMPANIES[k].name,COMPANIES[k].min,COMPANIES[k].note)}catch(e){}}
 const g=n=>{try{return strip(eval(n))}catch(e){return null}};
 const aw={};(g('AIWD')||[]).forEach(x=>{aw[x.key]={name:x.name,min:x.min,note:x.note}});
 return {asof:LAST_CHECK,maps,aw,DS:g('DS'),UPDATES:g('UPDATES'),PRIMARY:g('PRIMARY'),EXECTL:g('EXECTL'),EXECTL_AUTO:g('EXECTL_AUTO'),FINDS:g('FINDS'),FINDLINKS:g('FINDLINKS'),VERIFY_PPL:g('VERIFY_PPL'),DEALS:g('DEALS'),BIGLINKS:g('BIGLINKS'),CFHIST:g('CFHIST')};
});
// AIスタートアップの小さな図(site/aw/)
r.awmaps={};for(const f of fs.readdirSync(path.join(SITE,'aw')))Object.assign(r.awmaps,JSON.parse(fs.readFileSync(path.join(SITE,'aw',f),'utf8')));
// site/data/ の大きな一覧
const ctx={window:{},console};vm.createContext(ctx);r.lists={};
for(const n of ['acq','exits','jpsu','news','pauto','personal','rank','relnews','sec','uni','vcnews','vcs','world','ycs','ynews']){
 const s=fs.readFileSync(path.join(SITE,'data',n+'.js'),'utf8');const vs=(s.match(/const\s+([A-Z_]+)\s*=/g)||[]).map(x=>x.replace(/const\s+|\s*=/g,''));
 vm.runInContext(s.replace(/\bconst\s+/g,'var '),ctx);vs.forEach(v=>r.lists[v]=ctx[v]);}
for(const n of ['people','gnews','x_info'])r.lists[n]=JSON.parse(fs.readFileSync(path.join(SITE,n+'.json'),'utf8'));
fs.writeFileSync(OUT,JSON.stringify(r,(k,v)=>typeof v==='string'&&v.startsWith('data:')?undefined:v));
console.log('maps',Object.keys(r.maps).length,'aw',Object.keys(r.awmaps).length,(fs.statSync(OUT).size/1e6).toFixed(1)+'MB →',OUT);await b.close()})();
