p = 'hub_template.html'
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:60]
    s = s.replace(a, b, 1)


js = r"""/* 100万人規模の人物(Wikidata: 職業ごとに集めた人物)。名前の先頭で400個のファイル(pb/NNN.json)に分けてあり、検索した語に合う1ファイルだけ読み込む */
const PBN=400,PBCACHE={};
const PBOCC={politician:'政治家',footballer:'サッカー選手','actor':'俳優',writer:'作家',painter:'画家',singer:'歌手',musician:'音楽家','film director':'映画監督',researcher:'研究者','university teacher':'大学教員',journalist:'ジャーナリスト',lawyer:'弁護士',businessperson:'実業家','basketball player':'バスケットボール選手','baseball player':'野球選手','ice hockey player':'アイスホッケー選手',cyclist:'自転車選手',composer:'作曲家',poet:'詩人',physician:'医師',engineer:'技術者',historian:'歴史家',mathematician:'数学者','tennis player':'テニス選手',swimmer:'水泳選手','military officer':'軍人',judge:'裁判官','television actor':'俳優','film actor':'俳優','stage actor':'俳優',screenwriter:'脚本家',novelist:'小説家',diplomat:'外交官',economist:'経済学者',physicist:'物理学者',chemist:'化学者',biologist:'生物学者',architect:'建築家',photographer:'写真家',sculptor:'彫刻家','Catholic priest':'司祭','association football manager':'サッカー監督',athlete:'スポーツ選手',sprinter:'短距離走者','racing driver':'レーシングドライバー',boxer:'ボクサー',golfer:'ゴルファー','rugby union player':'ラグビー選手','American football player':'アメフト選手',cricketer:'クリケット選手','voice actor':'声優','manga artist':'漫画家',idol:'アイドル','television presenter':'司会者',model:'モデル',entrepreneur:'起業家','computer scientist':'計算機科学者',programmer:'プログラマー',philosopher:'哲学者',theologian:'神学者',activist:'活動家','chess player':'チェス選手',DJ:'DJ',rapper:'ラッパー',guitarist:'ギタリスト',pianist:'ピアニスト',conductor:'指揮者','opera singer':'オペラ歌手'};
const pbFold=s=>String(s||'').normalize('NFKD').replace(/[̀-ͯ]/g,'').toLowerCase();
const pbToks=s=>pbFold(s).split(/[^\p{L}\p{N}]+/u).filter(Boolean);
const pbKey=t=>{const cp=Array.from(t);return(/^[a-z0-9]/.test(t)?cp.slice(0,3):cp.slice(0,2)).join('')};
const pbHash=k=>{let h=0;for(let i=0;i<k.length;i++)h=(Math.imul(h,31)+k.charCodeAt(i))>>>0;return h%PBN};
function pbShard(i){
  if(PBCACHE[i])return PBCACHE[i];
  const f='pb/'+String(i).padStart(3,'0')+'.json';
  return PBCACHE[i]=fetch(f).then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.json()}).catch(()=>[]);
}
let pbSeq=0;
async function pbAugment(raw){
  const qt=pbToks(raw);if(!qt.length)return;
  const k=pbKey(qt[0]);if(Array.from(k).length<(/^[a-z0-9]/.test(qt[0])?3:2))return;
  const my=++pbSeq;
  const rows=await pbShard(pbHash(k));
  if(my!==pbSeq||norm(qEl.value)!==norm(raw))return;
  const have=new Set();WPALL.forEach(p=>have.add(Number(String(p.q).replace('Q',''))));
  const out=[];
  for(const r of rows){
    if(have.has(r[0]))continue;
    const nt=pbToks(r[1]+' '+r[2]);
    if(qt.every(t=>nt.some(x=>x.startsWith(t))||(/[^\x00-\x7f]/.test(t)&&pbFold(r[2]).includes(t)))){
      out.push({t:'w',q:'Q'+r[0],en:r[1],ja:r[2],name:r[2]||r[1],roles:[],d:(PBOCC[r[3]]||r[3]),x:'',w:'',t0:'',sub:(PBOCC[r[3]]||r[3])+' / Wikipedia '+r[4]+'言語版',s:''});
      if(out.length>=12)break;
    }
  }
  if(!out.length)return;
  const ex=new Set(qItems.map(x=>(x.q||x.name)));
  out.forEach(o=>{if(!ex.has(o.q)&&qItems.length<42)qItems.push(o)});
  qRender();
}
"""
rep("function wpItems(){return WPEO}", "function wpItems(){return WPEO}\n" + js)
rep("  qItems=out.slice(0,30).map(x=>x[1]);qSel=qItems.length?0:-1;qRender();\n}", "  qItems=out.slice(0,30).map(x=>x[1]);qSel=qItems.length?0:-1;qRender();\n  pbAugment(qEl.value);\n}")
# showWPerson: handle empty roles
rep("""<div class="pf-sec"><h3>関わった会社(Wikidataの記録)</h3><ul>${it.roles.map(x=>`<li><a href="#" data-co="${esc(x[0])}">${esc(x[0])}</a> — ${esc(WPRL[x[1]]||x[1])}</li>`).join('')}</ul>
   <p><button type="button" id="wpmap">つながりの相関図を見る</button></p>""", """<div class="pf-sec">${it.roles.length?`<h3>関わった会社(Wikidataの記録)</h3><ul>${it.roles.map(x=>`<li><a href="#" data-co="${esc(x[0])}">${esc(x[0])}</a> — ${esc(WPRL[x[1]]||x[1])}</li>`).join('')}</ul>
   <p><button type="button" id="wpmap">つながりの相関図を見る</button></p>`:'<p class="note">この人は、会社の創業者・CEO・会長・取締役としてはWikidataに載っていないため、つながりの相関図はありません。下のリンクから経歴を調べられます。</p>'}""")
rep("  document.getElementById('wpmap').addEventListener('click',()=>wpMap(it));", "  if(document.getElementById('wpmap'))document.getElementById('wpmap').addEventListener('click',()=>wpMap(it));")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
