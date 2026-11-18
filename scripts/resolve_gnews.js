// Googleニュースの転送リンクをブラウザで開き、元の記事のURLを記録する(元の記事のページ自体は読み込まない)。scripts/fix_gnews_links.py と組で使う
// Usage: node resolve.js urls.txt cache.jsonl [concurrency]
// Opens each Google News link in a headless browser and records where it forwards to (without loading the publisher page).
const fs=require('fs');const {chromium}=require('playwright');
const [,,inF,cacheF,concS]=process.argv;const conc=+concS||4;
const done=new Set();
if(fs.existsSync(cacheF))for(const l of fs.readFileSync(cacheF,'utf8').split('\n')){if(!l)continue;try{const o=JSON.parse(l);if(o.to)done.add(o.from)}catch(e){}}
const todo=[...new Set(fs.readFileSync(inF,'utf8').split('\n').filter(Boolean))].filter(u=>!done.has(u));
console.error('todo',todo.length,'done',done.size);
const out=fs.createWriteStream(cacheF,{flags:'a'});
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({locale:'ja-JP'});
 await ctx.route('**/*',r=>{const q=r.request();const h=new URL(q.url()).hostname;
  if(/googletagmanager|play\.google\.com|fonts\./.test(h)||['image','font','media'].includes(q.resourceType()))return r.abort();
  if(q.isNavigationRequest()&&!/(^|\.)google\.com$/.test(h)){const pg=q.frame().page();pg._found=q.url();return r.abort();}
  r.continue();});
 let i=0,ok=0;
 async function worker(){const p=await ctx.newPage();
  while(i<todo.length){const u=todo[i++];p._found=null;
   try{await p.goto(u.includes('hl=')?u:u+'&hl=ja&gl=JP&ceid=JP:ja',{waitUntil:'domcontentloaded',timeout:30000});
    for(let k=0;k<60&&!p._found;k++)await p.waitForTimeout(250);}catch(e){}
   const to=p._found&&/^https?:/.test(p._found)?p._found:null;if(to)ok++;
   out.write(JSON.stringify({from:u,to})+'\n');
   if(i%50===0)console.error(new Date().toISOString(),i,'/',todo.length,'ok',ok);
   await p.waitForTimeout(300);}
  await p.close();}
 await Promise.all(Array.from({length:conc},worker));out.end();await b.close();console.error('finished ok',ok,'of',todo.length);})();
