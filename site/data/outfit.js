/* ===== 装いとブランド(メニュー「装いとブランド」、2026/11/21追加・見本版) =====
   起業家・経営者の「公開の場での装い」と、そこに出てくるブランドとの関係を、出典つきで並べる。
   守ること: 本人の発言・信頼できる報道・ブランド公式が書いたブランドだけ。推測のブランド名は入れない。
   顔の識別や私生活の詮索はしない(公開の場の装いだけ)。出典が見つからない人は st:'調査中' で「わかっていません」と出す。
   採点(sc)は「参考の目安」。人の優劣ではなく、装いの特徴を1〜5で表す。理由(why)を必ず書く。足すだけ・消さない。
   1人 = {n:日本語名, en:英語名, co:会社, st:'済'|'調査中', look:装いのひとこと, sc:{f:フォーマル度,r:定番度,m:まねしやすさ,p:価格帯}, why:{f,r,m,p:理由},
           items:[{w:着ているもの, b:ブランド, rel:関係の種類, note:ひとこと, cf:'o'公式|'s'本人|'r'報道, src:[[出典名,URL]]}],
           scene:'こんな場面の参考に', asof:'確かめた日'}
   採点の見かた: f=フォーマル度(5=スーツ・ネクタイ、1=Tシャツ) r=定番度(5=ほぼいつも同じ装い) m=まねしやすさ(5=手に入れやすい・値段が手頃) p=価格帯(5=とても高い、1=手頃)。 */
const OUTFIT=[
{n:'ジェンスン・フアン',en:'Jensen Huang',co:'NVIDIA',st:'済',asof:'2026-11-21',
 look:'黒の革ジャケットが定番。講演では毎回のように着ている。',
 sc:{f:2,r:5,m:2,p:5},
 why:{f:'革ジャケットにシャツやTシャツ。スーツではないが、きちんと感はある。',r:'講演の定番として知られ、競売に出たほど「顔」になっている。',m:'1着が数千〜1万ドル超と報じられ、まねしにくい。',p:'報道では数千〜1万ドル超。'},
 items:[
  {w:'黒の革ジャケット',b:'Tom Ford',rel:'着用(報道)',note:'専門家はTom Fordが多いと見ている。ただしどの講演でどのモデルかは専門家でも意見が分かれる。CES 2025のものは8,990ドルのワニ革風と報じられた。',cf:'r',src:[['Fortune(2025/3/23)','https://fortune.com/2025/03/23/jensen-huang-nvidia-ceo-black-leather-jackets-prices-thousands-dollars-tom-ford/']]},
  {w:'革ジャケット(一部)',b:'Theory',rel:'着用の可能性(報道)',note:'広報担当者が「すべてがTom Fordほど高いわけではない」と話し、Theoryのように見えるものもあると報じられた。確定ではない。',cf:'r',src:[['Bnext(2024)','https://www.bnext.com.tw/article/78648/jensen-huang-gtc-2024-leather-jacket']]},
  {w:'署名入りの黒い革ジャケット',b:'Tom Ford',rel:'競売(2026年7月)',note:'本人が着て署名したTom Fordの革ジャケットが、ニューヨークのSotheby\'sで96万ドルで売れた(予想は4〜6万ドル)。収益は慈善に使われる。',cf:'r',src:[['TechRadar(2026/7)','https://www.techradar.com/pro/nvidia-ceo-jensen-huangs-leather-jacket-sells-for-nearly-usd1-million-at-sothebys-auction'],['Fortune(2026/7/17)','https://fortune.com/2026/07/17/jensen-huang-black-leather-jacket-auction-sothebys-funds-going-to-philanthropy/']]}],
 scene:'「自分の定番」を一つ決めて見せたい場面。革ジャケットを使うなら、中は無地のシャツやニットで引き締める。'},
{n:'マーク・ザッカーバーグ',en:'Mark Zuckerberg',co:'Meta',st:'済',asof:'2026-11-21',
 look:'無地のグレーのTシャツが定番。見た目は普通でも、特注の高級品と報じられている。',
 sc:{f:1,r:5,m:3,p:4},
 why:{f:'Tシャツ。フォーマルな場向きではない。',r:'グレーのTシャツが長年の定番として知られる。',m:'同じ見た目の無地Tシャツは手頃に探せる(模したものが46ドルで売られた)。ただし本物は特注。',p:'1枚300〜400ドルと報じられた(900ドルとする報道もあるが外れ値)。'},
 items:[
  {w:'無地のグレーのTシャツ',b:'Brunello Cucinelli',rel:'着用(特注・報道)',note:'W Magazine(2018)が300ドルと報じ、ほかの報道は300〜400ドル。特注品で一般には売られていないとされる。',cf:'r',src:[['W Magazine','https://www.wmagazine.com/story/mark-zuckerberg-facebook-brunello-cucinelli-t-shirt'],['Entrepreneur(2017)','https://entrepreneur.com/living/for-46-you-can-dress-just-like-mark-zuckerberg/297691']]}],
 scene:'「服で悩まない」という考え方の参考に。フォーマルな場では、同じ無地でも黒や紺のニット+ジャケットに寄せると近い印象になる。'},
{n:'スティーブ・ジョブズ',en:'Steve Jobs',co:'Apple(故人)',st:'済',asof:'2026-11-21',
 look:'黒のタートルネック、リーバイス501、ニューバランスのスニーカー。',
 sc:{f:2,r:5,m:4,p:2},
 why:{f:'タートルネックとジーンズ。かしこまってはいないが、整って見える。',r:'毎日ほぼ同じ装いで、象徴になった。',m:'黒のタートルネックとジーンズは手に入れやすい。',p:'三宅一生のタートルネックは、2017年に復刻された版が270ドルと報じられた。'},
 items:[
  {w:'黒のタートルネック',b:'ISSEY MIYAKE(三宅一生)',rel:'着用+本人が語る(伝記)',note:'ジョブズは三宅一生に頼み、「100枚ほど作ってくれた」とウォルター・アイザックソンの伝記に書かれた。Appleの社員の制服を頼んだ話もあるが、社員には不評で実現しなかった。',cf:'r',src:[['NPR(2022/8/10)','https://www.npr.org/2022/08/10/1116769827/the-story-of-steve-jobs-and-issey-miyakes-friendship-and-a-nixed-apple-uniform'],['CS Monitor(2011)','https://csmonitor.com/Technology/Horizons/2011/1012/The-story-behind-Steve-Jobs-s-black-turtleneck']]},
  {w:'ジーンズ',b:"Levi's 501",rel:'着用(報道)',note:'黒のタートルネック・ジーンズ・ニューバランスが定番の「制服」。',cf:'r',src:[['MacRumors(2011)','https://www.macrumors.com/2011/10/11/steve-jobs-on-mock-turtlenecks-and-jeans/']]},
  {w:'スニーカー',b:'New Balance',rel:'着用(報道)',note:'グレーのニューバランス(991とする記事もある)。',cf:'r',src:[['NPR(2022/8/10)','https://www.npr.org/2022/08/10/1116769827/the-story-of-steve-jobs-and-issey-miyakes-friendship-and-a-nixed-apple-uniform']]}],
 scene:'カジュアル寄りのビジネスの場。黒の無地を軸に、素材のよさで見せる考え方の参考に。'},
{n:'小澤隆生',en:'Takao Ozawa',co:'Boost Capital',st:'調査中',asof:'2026-11-21',
 look:'まだ装いやブランドを書いた公開の記事・本人の投稿を確かめられていません。',
 sc:null,why:null,items:[],
 scene:'本人の発言・インタビュー・公式の記事でブランドがわかったものだけ足します。推測では載せません。(2026/11/21に日本語で検索したが、装いについて書かれた記事は見つからなかった)'}
];
const OF_AX=[['f','フォーマル度'],['r','定番度'],['m','まねしやすさ'],['p','価格帯']];
let ofSel=0;
function ofBar(v){return `<span class="of-bar" aria-label="${v}/5">${[1,2,3,4,5].map(i=>`<i${i<=v?' class="on"':''}></i>`).join('')}</span>`}
function ofRender(){
  const P=OUTFIT[ofSel],esc=kkEsc,out=document.getElementById('ofout');
  const cfm={o:'公式',s:'本人',r:'報道'};
  document.querySelectorAll('#oflist button').forEach((b,i)=>b.setAttribute('aria-pressed',String(i===ofSel)));
  const score=P.sc?`<section class="of-box"><h3>AIの採点(参考の目安)</h3><p class="meta">人の優劣ではなく、装いの特徴を1〜5で表したものです。</p>${OF_AX.map(([k,l])=>`<div class="of-sc"><span>${l}</span>${ofBar(P.sc[k])}<small>${esc(P.why[k])}</small></div>`).join('')}</section>`:'';
  const items=P.items.length?P.items.map(x=>`<li class="of-it"><div><b>${esc(x.b)}</b> <span class="of-rel">${esc(x.rel)}</span> <span class="cf-b">${cfm[x.cf]||''}</span></div><div>${esc(x.w)}</div><small>${esc(x.note)}</small><div class="of-src">${x.src.map(s=>`<a href="${esc(s[1])}" target="_blank" rel="noopener">${esc(s[0])}</a>`).join(' / ')}</div></li>`).join(''):'<li class="meta">確かめられたブランドはまだありません。</li>';
  const brands=[...new Set(P.items.map(x=>x.b))];
  out.innerHTML=`<h2 style="margin:0 0 4px">${esc(P.n)} <small class="meta">${esc(P.en)} / ${esc(P.co)}</small></h2>
  <p style="margin:0 0 10px">${esc(P.look)}</p>${score}
  <section class="of-box"><h3>関係のあるブランド${brands.length?`(${brands.length})`:''}</h3><ul class="of-items">${items}</ul></section>
  <section class="of-box"><h3>こんな場面の参考に</h3><p style="margin:0">${esc(P.scene)}</p></section>
  <p class="meta">確かめた日: ${esc(P.asof)}</p>`;
}
function showOutfit(){
  stop();leavePerson();ctrail=[];
  MAINEL.hidden=true;controls.hidden=true;trailbar.hidden=true;document.getElementById('subbar').hidden=true;RANKEL.hidden=true;PROFEL.hidden=true;UNIEL.hidden=true;FEEDEL.hidden=false;
  document.querySelectorAll('#tabs button').forEach(b=>b.setAttribute('aria-pressed','false'));
  document.getElementById('title').textContent='装いとブランド';document.title='装いとブランド';
  document.getElementById('note').textContent='';
  FEEDEL.innerHTML=`<style>
  .of-list{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px}
  .of-list button{font:inherit;padding:6px 12px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--fg);cursor:pointer}
  .of-list button[aria-pressed="true"]{background:var(--fg);color:var(--bg);border-color:var(--fg)}
  .of-box{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:0 0 12px;min-width:0}
  .of-box h3{margin:0 0 6px;font-size:15px}
  .of-sc{display:grid;grid-template-columns:7em auto minmax(0,1fr);gap:4px 10px;align-items:center;padding:4px 0;border-top:1px solid var(--line)}
  .of-sc small{color:var(--muted);grid-column:1/-1}
  .of-bar{display:inline-flex;gap:3px}.of-bar i{width:16px;height:8px;border-radius:2px;background:var(--soft)}.of-bar i.on{background:var(--invest)}
  .of-items{list-style:none;margin:0;padding:0;display:grid;gap:10px}
  .of-it{border-top:1px solid var(--line);padding-top:8px;overflow-wrap:anywhere}.of-it small{display:block;color:var(--muted)}
  .of-rel{font-size:12px;color:var(--deal)}.of-src{font-size:12px;margin-top:2px}
  </style>
  <p class="meta" style="margin:0 0 12px;max-width:72ch"><b>見本版です。</b>起業家・経営者が公開の場で着ているものと、関係のあるブランドを、出典つきで並べます。本人の発言・信頼できる報道・ブランド公式が書いたブランドだけを載せ、推測は載せません。採点はAIによる<b>参考の目安</b>で、人の優劣ではありません。</p>
  <div class="of-list" id="oflist" role="group" aria-label="人を選ぶ">${OUTFIT.map((p,i)=>`<button type="button" data-i="${i}" aria-pressed="false">${kkEsc(p.n)}${p.st==='調査中'?'(調査中)':''}</button>`).join('')}</div>
  <div id="ofout"></div>`;
  document.getElementById('oflist').onclick=e=>{const b=e.target.closest('button');if(!b)return;ofSel=Number(b.dataset.i);ofRender()};
  ofRender();
}
