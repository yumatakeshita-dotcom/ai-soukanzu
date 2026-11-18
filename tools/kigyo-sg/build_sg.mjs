// シンガポール(ACRA)の会社を、kigyo-asiapac と同じ形の静的ファイルにする
import fs from 'node:fs';
const [,, src, out] = process.argv;
const LEG = new Set(["ltd","limited","plc","llp","llc","inc","lp","cic","sas","sarl","sa","sasu","eurl","sci","snc","as","asa","ans","da","ba","oy","oyj","ab","gmbh","ag","kg","ug","bv","nv","ou","tu","uu","mu","fie","co","company","the","pty","nl"]);
const core = (name) => { const s = String(name||"").normalize("NFKD").replace(/\p{M}/gu,"").toLowerCase();
  const toks = s.replace(/[^\p{L}\p{N}]+|_/gu," ").split(" ").filter(Boolean);
  for(;;){ if(toks.length>1&&LEG.has(toks[toks.length-1]))toks.pop(); else if(toks.length>1&&LEG.has(toks[0]))toks.shift();
    else if(toks.length>3&&(toks[0]==="trustee"||toks[0]==="trustees")&&(toks[1]==="for"||toks[1]==="of"))toks.splice(0,2); else break; }
  return toks.join(""); };
const fnv = (k) => { let h=2166136261; for(let i=0;i<k.length;i++) h=Math.imul(h^k.charCodeAt(i),16777619)>>>0; return h; };
// CSV
function parseCSV(t){ const rows=[]; let row=[],f='',q=false; for(let i=0;i<t.length;i++){const c=t[i];
  if(q){ if(c==='"'){ if(t[i+1]==='"'){f+='"';i++;} else q=false; } else f+=c; }
  else if(c==='"') q=true; else if(c===','){row.push(f);f='';} else if(c==='\n'){row.push(f);rows.push(row);row=[];f='';} else if(c!=='\r') f+=c; }
  if(f||row.length){row.push(f);rows.push(row);} return rows; }
const all = parseCSV(fs.readFileSync(src,'utf8')); const H = all.shift(); const ix = Object.fromEntries(H.map((h,i)=>[h,i]));
const recs = all.filter(r=>r.length===H.length);
// 業種コードの説明(説明のある行から、同じコードの説明を借りる)
const ssic = {}; for (const r of recs){ const c=r[ix.industry_code], d=r[ix.industry]; if(c&&d&&!ssic[c]) ssic[c]=d; }
const rows = recs.map(r=>{ const c=r[ix.industry_code]; const d=r[ix.industry]||ssic[c]||'';
  return { id:r[ix.id], name:r[ix.name], kind:r[ix.type], addr:r[ix.address], post:r[ix.postal_code], since:r[ix.established], sic: c ? (d? `${c} ${d}` : `SSIC ${c}`) : (d||''), core: Array.from(core(r[ix.name])) }; });
// よく出る先頭の文字(長さ2〜5)を「hot」にして、さらに1文字ずつ細かく分ける
const T = 1500, hot = {};
let cur = rows;
for (let L=2; L<6; L++){ const cnt=new Map(); for(const r of cur){ if(r.core.length>L){ const p=r.core.slice(0,L).join(''); cnt.set(p,(cnt.get(p)||0)+1);} }
  hot[L] = new Set([...cnt].filter(([,n])=>n>T).map(([p])=>p)); cur = cur.filter(r=>r.core.length>L && hot[L].has(r.core.slice(0,L).join(''))); }
const NB = 700, ND = 700;
const nb = Array.from({length:NB},()=>[]), nd = Array.from({length:ND},()=>[]);
for (const r of rows){ let L=2; while(L<6 && hot[L]?.has(r.core.slice(0,L).join('')) && r.core.length>L) L++;
  const key = r.core.slice(0,L).join(''); nb[fnv(key)%NB].push(['SG',r.id,r.name,r.addr]);
  nd[fnv('SG:'+r.id)%ND].push(['SG',r.id,r.name,r.kind,r.addr,r.post,r.since,r.sic]); }
fs.mkdirSync(out+'/c',{recursive:true}); fs.mkdirSync(out+'/n',{recursive:true});
nb.forEach((a,i)=>{ a.sort((x,y)=>x[2].localeCompare(y[2])); fs.writeFileSync(`${out}/n/${i}.json`,JSON.stringify(a)); });
nd.forEach((a,i)=>fs.writeFileSync(`${out}/c/${i}.json`,JSON.stringify(a)));
fs.writeFileSync(`${out}/n/hot.json`,JSON.stringify(Object.fromEntries(Object.entries(hot).map(([L,s])=>[L,[...s].sort()]))));
fs.writeFileSync(`${out}/c/meta.json`,JSON.stringify({total:rows.length,by:{SG:rows.length},nd:ND,nb:NB,built:new Date().toISOString().slice(0,10),source:"ACRA, data.gov.sg / Singapore Open Data Licence v1.0"}));
const sz = a=>Math.max(...a.map(x=>JSON.stringify(x).length));
console.log('rows',rows.length,'hot',Object.fromEntries(Object.entries(hot).map(([L,s])=>[L,s.size])),'max nb file',sz(nb),'max nd file',sz(nd));
