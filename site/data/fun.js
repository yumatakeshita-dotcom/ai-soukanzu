/* ===== おもしろ情報(メニュー「おもしろ」、2026/11/21追加) =====
   起業家・会社の「どうでもよさそうで、つい人に話したくなる」話を、5つの欄で見る画面。
   1 愛用品・服装 / 2 本・映画 / 3 社名の由来 / 4 朝の習慣 / 5 失敗談・名言
   データ(FUN)と画面(showFun)が同じファイル。毎朝の調査が足すもの(FUN_AUTO)は site/data/finds.js の4行目(scripts/fun_merge.py が inbox/fun/ から毎回作る。手で直さない)。
   守ること: 出典のURLを必ず付ける。うわさ・推測は入れない。本人や報道が公に話した範囲だけ(健康・家族などの私生活は入れない)。
   画像は載せない(出典へのリンクと文章だけ)。足すだけ・既存の行は消さない。
   1件 = {p:'人・会社の名前', en:'英語名', t:'見出し', note:'ひとこと(説明)', q:'英語の原文(名言のとき。出典の文面と一字一句同じもの)', y:'年(任意)',
          cf:'f開示 / o公式 / s本人 / r報道', chk:'o=出典のページを開いて本文で確かめた / s=検索で複数の報道に載っているのを確かめた(ページは開けていない)',
          asof:'確かめた日', works:[['作品名','作者']](本・映画の欄だけ。「影響の線」の図に使う), src:[['出典の名前','URL']], link:'相関図の会社のキー(任意。例 openai)'} */
const FUN_CATS=[
 {k:'gear',n:'愛用品・服装',d:'いつも身につけているもの・決まった服装。本人や報道が公に語ったものだけ'},
 {k:'book',n:'本・映画',d:'誰が、どの本・映画に影響を受けた(関わった)と語っているか(人 → 作品・作者)'},
 {k:'name',n:'社名の由来',d:'会社名・サービス名の名前の由来'},
 {k:'habit',n:'朝の習慣',d:'公の場で本人が話した習慣・日課(健康や家族の話は扱いません)'},
 {k:'quote',n:'失敗談・名言',d:'株主あての手紙や上場の書類など、一次の出典で文面を確かめられたものを優先'}
];
const FUN={
gear:[
 {p:'スティーブ・ジョブズ',en:'Steve Jobs',t:'黒のハイネック・ジーンズ・スニーカーが「制服」',note:'イッセイ ミヤケの黒い長袖モックネック、リーバイス501、ニューバランス991をいつも着ていたと紹介されている。本人が伝記作家に「自分の制服がほしくなった」と話したとも。',y:'2000年代',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Steve Jobs」(服装の項。脚注に伝記の出典)','https://en.wikipedia.org/wiki/Steve_Jobs']],link:''},
 {p:'ジェンスン・ファン(NVIDIA)',en:'Jensen Huang',t:'黒い革ジャンがトレードマーク',note:'黒い革ジャンは「トレードマーク」として報じられている。2024年3月にはザッカーバーグが、お互いの定番の上着を着た写真を自分のInstagramに投稿した。',y:'2024',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Jensen Huang」(服装と、ザッカーバーグの投稿の項)','https://en.wikipedia.org/wiki/Jensen_Huang']],link:'nvidia'},
 {p:'マーク・ザッカーバーグ(Meta)',en:'Mark Zuckerberg',t:'灰色のTシャツから、2024年に装いを変えた',note:'長いあいだ、ほぼ同じ灰色のシャツとジーンズで人前に出ていたが、2024年から金のネックレスや流行の服装に変えたと報じられている。',y:'2024',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Mark Zuckerberg」(装いの変化の項)','https://en.wikipedia.org/wiki/Mark_Zuckerberg']],link:'meta'},
 {p:'ジェフ・ベゾス(Amazon)',en:'Jeff Bezos',t:'ロケット打ち上げには「縁起のよい」カウボーイブーツ',note:'ブルーオリジンの事故のあと、ロケットの打ち上げにはいつも「ラッキー」なテキサスのカウボーイブーツを履くようになったと報じられている。',y:'2010年代',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Jeff Bezos」(宇宙事業の項)','https://en.wikipedia.org/wiki/Jeff_Bezos']],link:''}
],
book:[
 {p:'イーロン・マスク',en:'Elon Musk',works:[['指輪物語','J・R・R・トールキン'],['ファウンデーション','アイザック・アシモフ'],['銀河ヒッチハイク・ガイド','ダグラス・アダムズ']],t:'「指輪物語」「ファウンデーション」「銀河ヒッチハイク・ガイド」',note:'本の虫で、成功の一部はこの3作を読んだおかげだと語ってきたと紹介されている。',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Elon Musk」(生い立ちの項)','https://en.wikipedia.org/wiki/Elon_Musk']],link:'xai'},
 {p:'孫正義(ソフトバンクグループ)',en:'Masayoshi Son',works:[['竜馬がゆく','司馬遼太郎']],t:'司馬遼太郎「竜馬がゆく」',note:'高校に入ったころ、家庭教師にすすめられた「竜馬がゆく」を愛読したと紹介されている。(日本語版Wikipediaの記述。そのあとの「脱藩にあこがれて渡米を決めた」部分には、同ページで「要出典」の印が付いているので載せていません)',y:'1973年ごろ',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「孫正義」(高校・大学時代の項)','https://ja.wikipedia.org/wiki/孫正義']],link:'softbank'},
 {p:'マーク・ザッカーバーグ',en:'Mark Zuckerberg',t:'2015年「2週間に1冊読む」宣言。最初の1冊は「The End of Power」',note:'2015年1月、「A Year of Books」と名づけた読書の挑戦を始め、最初にモイセス・ナイムの「The End of Power」を選んだ。この本はAmazonで売り切れたと報じられた。',y:'2015',works:[['The End of Power','モイセス・ナイム']],cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「The End of Power」(受容の項)','https://en.wikipedia.org/wiki/The_End_of_Power']],link:'meta'},
 {p:'ジェフ・ベゾス(Amazon)',en:'Jeff Bezos',works:[['スター・トレック','']],t:'アレクサの目標は「スタートレックのコンピューター」。映画にも出演',note:'2011年、アレクサのもとになる計画の最初の相談で、技術の責任者に「目標はスタートレックのコンピューターをつくること」と話したと紹介されている。2016年の映画「スター・トレック BEYOND」には、ベゾスが宇宙艦隊の宇宙人の役でカメオ出演(アレクサと音声認識への関心から、制作会社に自分で頼んだと報じられている)。家族の会社「Zefram LLC」の名前も、作中の人物ゼフラム・コクランから。',y:'2011〜2016',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Jeff Bezos」(スター・トレックの記述)','https://en.wikipedia.org/wiki/Jeff_Bezos'],['Wikipedia「Star Trek Beyond」(出演者の項)','https://en.wikipedia.org/wiki/Star_Trek_Beyond']],link:''},
 {p:'ジェフ・ベゾス',en:'Jeff Bezos',t:'いちばん好きな小説は、カズオ・イシグロ「日の名残り」',note:'2003年のNPRの夏の読書特集で、「いちばん好きな小説」として挙げたと報じられている。後に「とても完璧な小説」と話したという報道もある。(「後悔しない選び方」の考え方とつなげる解説は筆者の推測なので載せていません)',y:'2003',works:[['日の名残り','カズオ・イシグロ']],cf:'r',chk:'s',asof:'2026/11/21',src:[['NPR「Summer Reading: Jeff Bezos」(2003/6/8)','https://www.npr.org/2003/06/08/1291535/summer-reading-jeff-bezos']],link:''},
 {p:'イーロン・マスク',en:'Elon Musk',t:'映画「アイアンマン2」に、本人役で出演',note:'2010年の映画「アイアンマン2」に、テスラのCEOとして本人の役で登場する。オラクルのラリー・エリソンも同じく本人役で出ている。',works:[['アイアンマン2(映画)','']],y:'2010',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Iron Man 2」(出演者の項)','https://en.wikipedia.org/wiki/Iron_Man_2']],link:'xai'},
 {p:'サム・アルトマン(OpenAI)',en:'Sam Altman',t:'GPT-4oの発表の日に、「her」とだけ投稿',note:'2024年5月13日、GPT-4oの宣伝として「her」の1語を投稿した。2013年の映画「Her」は、スカーレット・ヨハンソンが声を演じるAIの話。GPT-4oの声の1つ「Sky」が彼女の声に似ていると話題になり、OpenAIは「別の女優の声で、まねではない」と説明したうえで、5月20日にこの声を止めた。',works:[['Her(2013年の映画)','']],y:'2024',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「GPT-4o」(論争の項)','https://en.wikipedia.org/wiki/GPT-4o']],link:'openai'}
],
name:[
 {p:'Google',en:'Google',t:'「googol(10の100乗)」のつづり違い',note:'1の後ろに0が100個つく数「googol」を、つづりを変えて社名にした。ものすごく多くのページを探せる、という意味を込めたと説明されている。上場書類(S-1/A)に付いているPlayboy誌のインタビューにも、同じ説明がある。',y:'1998',cf:'f',chk:'o',asof:'2026/11/21',src:[['Google 上場の書類 S-1/A(SEC、2004/8、Playboyインタビューの章)','https://www.sec.gov/Archives/edgar/data/1288776/000119312504142742/ds1a.htm'],['Wikipedia「Google」','https://en.wikipedia.org/wiki/Google']],link:'google'},
 {p:'NVIDIA',en:'Nvidia',t:'ラテン語で「うらやましさ」を意味する「invidia」から',note:'ファンと創業者の1人プリエムの両方が、名前を思いついたのは自分だと話している。もとは別の名前をつけていて、トイレットペーパーの会社にすでに使われていたため変えた、という経緯も書かれている。',y:'1990年代',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Nvidia」(創業の項)','https://en.wikipedia.org/wiki/Nvidia']],link:'nvidia'},
 {p:'Amazon',en:'Amazon',t:'最初の社名は「Cadabra(カダブラ)」',note:'1994年7月、ベゾスがワシントン州ベルビューの自宅でオンライン書店として「Cadabra」の名前で創業。1995年に今の名前になった。',y:'1994',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Amazon (company)」','https://en.wikipedia.org/wiki/Amazon_(company)']],link:'amazon'},
 {p:'Samsung',en:'Samsung',t:'漢字で「三星」=3つの星',note:'創業者の説明では、「三」は大きい・多い・力強いこと、「星」は永遠を表す。',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Samsung」(語源の項)','https://en.wikipedia.org/wiki/Samsung']],link:''},
 {p:'Sakana AI',en:'Sakana AI',t:'「魚」。魚の群れのように、小さなAIが集まって賢くなる',note:'社名は日本語の「魚」から。単純なルールで魚の群れがまとまって動くように、小さなAIを組み合わせて強いAIをつくる考えを表している。',y:'2023',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Sakana AI」(英語版・名称の項)','https://en.wikipedia.org/wiki/Sakana_AI'],['Wikipedia「Sakana AI」(日本語版・名称の項)','https://ja.wikipedia.org/wiki/Sakana_AI']],link:'sakana'},
 {p:'Mistral AI',en:'Mistral AI',t:'南フランスに吹く冷たい強風「ミストラル」',note:'フランスの会社らしく、南仏に吹く強い北西風の名前から。',y:'2023',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Mistral AI」(名前の項)','https://en.wikipedia.org/wiki/Mistral_AI']],link:'mistral'},
 {p:'Apple',en:'Apple',t:'リンゴ農園を訪ねたときの思いつき',note:'ジョブズ本人の説明では、果物だけを食べる食事法をしていたころにリンゴ農園を訪ねたのが名前のきっかけ。',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Apple Inc.」(ロゴと名前の項)','https://en.wikipedia.org/wiki/Apple_Inc.']],link:''},
 {p:'Cisco',en:'Cisco',t:'「San Francisco」の後半',note:'社名はサンフランシスコから。初期の技術者たちは、小文字の「cisco」で書くことにこだわった。ロゴはゴールデンゲートブリッジの2つの塔をかたどっている。',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Cisco」(歴史の項)','https://en.wikipedia.org/wiki/Cisco']],link:''},
 {p:'Twitter(現X)',en:'Twitter / X',t:'最初の名前は母音のない「twttr」',note:'2006年の創業時の名前は「twttr」で、数か月後に「Twitter」に変わった。',y:'2006',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Twitter」','https://en.wikipedia.org/wiki/Twitter']],link:'twitter'}
],
habit:[
 {p:'ティム・クック(Apple)',en:'Tim Cook',t:'朝は3時45分起き、という報道が定番',note:'米USA Todayなどの報道を、Business Insiderなどが何度も紹介している。最初にメールを読み、5時ごろにジムへ。一方、のちのWSJインタビューを伝える記事は「朝5時より前に起きる」と書いていて、最近は少し違う可能性がある。',cf:'r',chk:'s',asof:'2026/11/21',src:[['SCMP「Tim Cook starts his day at 3:45am」','https://www.scmp.com/magazines/style/celebrity/article/3026879/apple-ceo-tim-cook-starts-his-day-345am-can-following-his'],['TIME「Tim Cook」(2012に本人がTIMEに語った起床時間)','https://time.com/3548342/tim-cook-apple/']],link:''},
 {p:'ビル・ゲイツ',en:'Bill Gates',t:'夜の皿洗いは自分でやる',note:'2014年2月のRedditの質問会で「毎晩皿洗いをする。ほかの人が代わると言ってくれるけど、自分のやり方が好きだから」と答えたと、複数の報道が伝えている。2014年当時の話で、今も続いているかは確かめられていない。',y:'2014',cf:'s',chk:'s',asof:'2026/11/21',src:[['NBC News「The 7 Most Fascinating Things Bill Gates Said in His Reddit Chat」','https://www.nbcnews.com/news/amp/wbna54347432'],['Engadget(2014/2/10)','https://www.engadget.com/2014/02/10/bill-gates-on-microsoft-philanthropy-chairs/']],link:''},
 {p:'マーク・ザッカーバーグ',en:'Mark Zuckerberg',t:'「2週間に1冊」の読書を1年続ける宣言',note:'2015年の新年の目標。ほかの人に目標を提案してもらい、その中でいちばん多かった「もっと読む」を選んだと伝えられている。',y:'2015',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「The End of Power」(読書の挑戦の記述)','https://en.wikipedia.org/wiki/The_End_of_Power']],link:'meta'}
],
quote:[
 {p:'マーク・ザッカーバーグ',en:'Mark Zuckerberg',t:'「Move fast and break things(速く動いて、壊せ)」',note:'Facebookの上場書類(S-1、2012年)にある創業者の手紙の言葉。「何も壊さないなら、たぶん十分に速く動けていない」という意味だと本人が説明している。',q:'We have a saying: “Move fast and break things.” The idea is that if you never break anything, you’re probably not moving fast enough.',y:'2012',cf:'f',chk:'o',asof:'2026/11/21',src:[['Facebook S-1(SEC、2012/2、創業者の手紙)','https://www.sec.gov/Archives/edgar/data/1326801/000119312512034517/d287954ds1.htm']],link:'meta'},
 {p:'マーク・ザッカーバーグ',en:'Mark Zuckerberg',t:'「危険を冒さなければ、必ず失敗する」',note:'同じ上場書類の「大胆に」の節。変化が速い世の中では、リスクを取らないことがいちばん確実な失敗だという考え。',q:'However, in a world that’s changing so quickly, you’re guaranteed to fail if you don’t take any risks.',y:'2012',cf:'f',chk:'o',asof:'2026/11/21',src:[['Facebook S-1(SEC、2012/2、創業者の手紙)','https://www.sec.gov/Archives/edgar/data/1326801/000119312512034517/d287954ds1.htm']],link:'meta'},
 {p:'ジェフ・ベゾス(Amazon)',en:'Jeff Bezos',t:'「失敗と発明は、切り離せない双子」',note:'2015年版の株主あての手紙(2016年4月公表)。「世界でいちばん失敗するのに向いた場所だ(練習は十分している)」とも書いている。',q:'I believe we are the best place in the world to fail (we have plenty of practice!), and failure and invention are inseparable twins.',y:'2016',cf:'f',chk:'o',asof:'2026/11/21',src:[['Amazon 株主あての手紙(SEC提出のExhibit 99.1、2016/4)','https://www.sec.gov/Archives/edgar/data/1018724/000119312516530910/d168744dex991.htm']],link:'amazon'},
 {p:'ラリー・ペイジ/セルゲイ・ブリン(Google)',en:'Larry Page / Sergey Brin',t:'「Don’t be evil(邪悪になるな)」',note:'上場書類(S-1/A、2004年)の節の見出しにもなった言葉。短期の利益をあきらめても、世界によいことをする会社のほうが長い目で見て得をする、と書いている。',q:'Don’t be evil. We believe strongly that in the long term, we will be better served—as shareholders and in all other ways—by a company that does good things for the world even if we forgo some short term gains.',y:'2004',cf:'f',chk:'o',asof:'2026/11/21',src:[['Google S-1/A(SEC、2004/8)','https://www.sec.gov/Archives/edgar/data/1288776/000119312504142742/ds1a.htm']],link:'google'},
 {p:'ジェンスン・ファン(NVIDIA)',en:'Jensen Huang',t:'NVIDIAは、デニーズ(ファミレス)の席から始まった',note:'ファンは15歳のとき、地元のデニーズで皿洗い・バスボーイ・ウェイターとして働き(1978〜83年)、1993年にサンノゼのデニーズでNVIDIAを共同創業した、と紹介されている。',y:'1993',cf:'r',chk:'o',asof:'2026/11/21',src:[['Wikipedia「Jensen Huang」','https://en.wikipedia.org/wiki/Jensen_Huang']],link:'nvidia'}
]
};
/* 毎朝の調査が足すもの(FUN_AUTO は finds.js の4行目にある)と手書きを合わせる。同じ(欄・人・見出し)は手書きを優先 */
function funAll(){
  const out={};const auto=(typeof FUN_AUTO!=='undefined'&&FUN_AUTO)||{};
  FUN_CATS.forEach(c=>{const seen=new Set();out[c.k]=[];
    (FUN[c.k]||[]).concat(auto[c.k]||[]).forEach(e=>{const key=(e.p+'|'+e.t).toLowerCase();if(seen.has(key))return;seen.add(key);out[c.k].push(e)})});
  return out;
}
/* 2社(や人)に関わる小ネタを探す。共通のつながり(common.js)から呼ぶ。2026/11/21追加 */
function funFor(names,codes){
  const all=funAll(),out=[];const nm=(names||[]).map(x=>String(x||'').toLowerCase()).filter(x=>x.length>=2);
  FUN_CATS.forEach(c=>all[c.k].forEach(e=>{
    const hay=[e.p,e.en].join(' ').toLowerCase();
    if((e.link&&(codes||[]).includes(e.link))||nm.some(n=>hay.includes(n)||n.includes(String(e.en||e.p).toLowerCase().replace(/\(.*\)/,'').trim())&&String(e.en||'').length>=3))out.push(Object.assign({catn:c.n},e))}));
  return out;
}
/* 本・映画: 「誰が → どの作品(作者)」の線の図。works のある件から作る */
function funInfluenceSvg(list){
  const pe=[],wk=[],ed=[];
  list.forEach(e=>(e.works||[]).forEach(w=>{const pn=e.p.replace(/\(.*\)$/,'');let a=pe.indexOf(pn);if(a<0){a=pe.length;pe.push(pn)}const k=w[0]+'|'+w[1];let b=wk.findIndex(x=>x[0]+'|'+x[1]===k);if(b<0){b=wk.length;wk.push(w)}ed.push([a,b])}));
  if(!ed.length)return '';
  const rowH=34,n=Math.max(pe.length,wk.length),H=n*rowH+16,W=760;
  const y=(i,m)=>8+(n*rowH-m*rowH)/2+i*rowH+rowH/2;
  const cut=(t,m)=>t.length>m?t.slice(0,m-1)+'…':t;
  return `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="誰がどの作品に影響を受けたかの線の図" style="max-width:${W}px;display:block;margin:6px 0 14px">
  ${ed.map(([a,b])=>`<line x1="210" y1="${y(a,pe.length)}" x2="${W-330}" y2="${y(b,wk.length)}" stroke="var(--pink)" stroke-width="1.6" opacity=".7"/>`).join('')}
  ${pe.map((t,i)=>`<g><circle cx="204" cy="${y(i,pe.length)}" r="5" fill="var(--active)"/><text x="196" y="${y(i,pe.length)+4}" text-anchor="end" font-size="12" fill="var(--fg)">${funEsc(cut(t,16))}</text></g>`).join('')}
  ${wk.map((w,i)=>`<g><circle cx="${W-324}" cy="${y(i,wk.length)}" r="5" fill="var(--deal)"/><text x="${W-314}" y="${y(i,wk.length)+4}" font-size="12" fill="var(--fg)">${funEsc(cut(w[0],22))}<tspan fill="var(--muted)" font-size="10.5"> ${funEsc(cut(w[1],16))}</tspan></text></g>`).join('')}
  </svg>`;
}
let funCat='gear',funQ='';
function funEsc(s){return String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function funSafe(u){return /^https?:\/\//.test(u)?u:'#'}
function showFun(cat){
  if(cat&&FUN_CATS.some(c=>c.k===cat))funCat=cat;
  stop();leavePerson();ctrail=[];
  MAINEL.hidden=true;controls.hidden=true;trailbar.hidden=true;document.getElementById('subbar').hidden=true;RANKEL.hidden=true;PROFEL.hidden=true;UNIEL.hidden=true;FEEDEL.hidden=false;
  document.querySelectorAll('#tabs button').forEach(b=>b.setAttribute('aria-pressed','false'));
  document.getElementById('title').textContent='おもしろ情報';document.title='おもしろ情報';
  document.getElementById('note').textContent='';
  funRender();
}
function funRender(){
  const all=funAll(),cur=FUN_CATS.find(c=>c.k===funCat),q=funQ.trim().toLowerCase();
  const list=all[funCat].filter(e=>!q||[e.p,e.en,e.t,e.note,e.q].join(' ').toLowerCase().includes(q));
  const nAuto=all[funCat].filter(e=>e.auto).length;
  const card=e=>{
    const chk=e.chk==='o'?'<span class="fn-chk">出典のページを開いて確認</span>':'<span class="fn-chk fn-chk2">報道の記事で確認(ページは開けていません)</span>';
    return `<li class="fn-c"><div class="fn-h"><b>${funEsc(e.p)}</b>${e.en&&e.en!==e.p?` <span class="cm-k">${funEsc(e.en)}</span>`:''} ${typeof cfBadge==='function'?cfBadge(e.cf):''}${e.auto?' <span class="cm-k">自動で追加</span>':''}</div>
    <h3>${funEsc(e.t)}</h3>${e.q?`<blockquote lang="en">${funEsc(e.q)}</blockquote>`:''}<p>${funEsc(e.note)}</p>
    <div class="fn-s">${chk}${e.y?` <span class="cm-y">${funEsc(e.y)}</span>`:''}${(e.src||[]).map(s=>` <a href="${funEsc(funSafe(s[1]))}" target="_blank" rel="noopener noreferrer">${funEsc(s[0])}</a>`).join('')}${e.asof?` <small>(${funEsc(e.asof)}に確認)</small>`:''}${e.link&&typeof COMPANIES!=='undefined'&&COMPANIES[e.link]?` <a href="#" data-fgo="${funEsc(e.link)}">相関図を開く</a>`:''}</div></li>`};
  FEEDEL.innerHTML=`<style>
  .fn-tabs{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}.fn-tabs button{padding:6px 12px;border-radius:999px}
  .fn-tabs button[aria-pressed=true]{border-color:var(--active);color:var(--active);font-weight:700}
  .fn-q{max-width:420px;margin:0 0 12px}.fn-q input{width:100%;box-sizing:border-box;padding:9px 12px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--fg);font:inherit;font-size:16px}
  .fn-l{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));gap:12px}
  .fn-c{min-width:0;border:1px solid var(--line);border-radius:12px;background:var(--surface);padding:14px}
  .fn-c h3{margin:6px 0;font-size:15px;overflow-wrap:anywhere}.fn-c p{margin:0 0 8px;font-size:13px;color:var(--muted);overflow-wrap:anywhere}
  .fn-c blockquote{margin:6px 0;padding:6px 10px;border-left:3px solid var(--deal);font-size:13px;overflow-wrap:anywhere}
  .fn-s{font-size:12px;display:flex;flex-wrap:wrap;gap:4px 8px;align-items:baseline}.fn-s a{color:var(--invest);overflow-wrap:anywhere}
  .fn-chk{color:var(--active)}.fn-chk2{color:var(--left)}
  </style>
  <p class="meta" style="margin:0 0 12px;max-width:72ch">どうでもよさそうで、つい人に話したくなる話を5つの欄にまとめました。<b>すべて出典つき</b>で、推測は載せていません。本人や報道が公に語った範囲だけです。印は出典で決まり、「開示」は上場の書類などの法定の書類、「報道」は報道・Wikipediaなどです。各件の「確認」は、出典のページを実際に開いて確かめたかどうかです。初回は見本(${FUN_CATS.reduce((a,c)=>a+all[c.k].length,0)}件)で、毎朝の調査で少しずつ増やします。</p>
  <div class="fn-tabs" role="group" aria-label="欄">${FUN_CATS.map(c=>`<button type="button" data-fc="${c.k}" aria-pressed="${c.k===funCat}">${c.n}(${all[c.k].length})</button>`).join('')}</div>
  <p class="meta" style="margin:0 0 8px">${funEsc(cur.d)}${nAuto?`(うち自動で追加 ${nAuto}件)`:''}</p>
  <div class="fn-q"><input id="fnq" type="search" placeholder="人・会社・ことばで絞る(例: ベゾス)" value="${funEsc(funQ)}" aria-label="絞り込み"></div>
  ${funCat==='book'?`<h3 style="margin:4px 0 0;font-size:14px">つながりの線(人 → 作品・作者)</h3>${funInfluenceSvg(all.book)}`:''}
  ${list.length?`<ul class="fn-l">${list.map(card).join('')}</ul>`:'<p class="meta">当てはまるものがありません。</p>'}`;
  FEEDEL.querySelectorAll('button[data-fc]').forEach(b=>b.addEventListener('click',()=>{funCat=b.dataset.fc;funRender()}));
  const inp=document.getElementById('fnq');
  inp.addEventListener('input',()=>{funQ=inp.value;const pos=inp.selectionStart;funRender();const n=document.getElementById('fnq');n.focus();n.setSelectionRange(pos,pos)});
  FEEDEL.querySelectorAll('a[data-fgo]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();build(a.dataset.fgo);window.scrollTo(0,0)}));
}

/* 会社の相関図の概要に出す「おもしろ」の入口(1件だけ。index.html の概要の組み立てから呼ぶ。2026/11/21) */
function funBtn(){
  const nm=(typeof COMPANIES!=='undefined'&&COMPANIES[comp])?COMPANIES[comp].name:'';if(!nm)return '';
  const fz=funFor([nm],[comp]).filter(e=>e.chk==='o'||e.cf==='f');if(!fz.length)return '';
  const e=fz.find(x=>x.cf==='f')||fz[0];
  return `<div class="links"><a href="#" id="gofun"><b>おもしろ情報: ${funEsc(e.p)} ${funEsc(e.catn)} ▸</b></a><small style="display:block;color:var(--muted)">${funEsc(e.t)} ${typeof cfBadge==='function'?cfBadge(e.cf):''} ${(e.src&&e.src[0])?`(出典: ${funEsc(e.src[0][0])})`:''}</small></div>`;
}
function wireFun(){const g=document.getElementById('gofun');if(g)g.addEventListener('click',ev=>{ev.preventDefault();const nm=COMPANIES[comp].name;const e=funFor([nm],[comp])[0];funQ=nm.length>=3?nm:'';funCat=(FUN_CATS.find(c=>c.n===(e&&e.catn))||FUN_CATS[0]).k;showFun();window.scrollTo(0,0)})}

/* 会社の相関図に「人 → 作品」の線を足す(試作、2026/11/21)。本・映画の件で works と link(会社のキー)があるものだけ。
   人が図にいるときだけ足す(いなければ何もしない)。作品は「関連企業」の色の小さな丸、線は灰色の細い線(種類 fun)。
   出典と確かさの印は件のものをそのまま付ける。既存の人・線は書き換えない。index.html の DATA の組み立てから呼ぶ。 */
function applyFun(c,d){
  let all;try{all=funAll()}catch(e){return}
  const norm=s=>String(s||'').toLowerCase().normalize('NFKC').replace(/[\s・,、.()()'’"“”\-]/g,'');
  const ids=new Set(d.N.map(n=>n.id));
  const yMin=(typeof COMPANIES!=='undefined'&&COMPANIES[c]&&COMPANIES[c].min)||2000;
  (all.book||[]).forEach(e=>{
    if(e.link!==c||!e.works||!e.works.length)return;
    const pn=norm(e.p.replace(/\(.*\)$/,'')),pe=norm(e.en);
    const person=d.N.find(n=>n.kind==='p'&&(norm(d.EN[n.id])===pe||norm(n.name)===pn));
    if(!person)return;
    e.works.forEach(w=>{
      const id='fun_'+norm(w[0]).slice(0,24);
      if(!ids.has(id)){ids.add(id);d.N.push({id,name:w[0]+(w[1]?'('+w[1]+')':''),kind:'o',from:yMin,desc:'おもしろ情報より。'+e.t+'。'+e.note,role:'作品',fd:1})}
      if(d.E.some(x=>x.a===person.id&&x.b===id))return;
      const src=(e.src||[]).map((s,i)=>{const k='fn_'+norm(e.p+w[0]).slice(0,16)+i;if(typeof DS!=='undefined'&&!DS[k])DS[k]=[s[0],s[1]];return k});
      d.E.push({a:person.id,b:id,k:'fun',since:yMin,d:e.t+'(おもしろ情報)',src,lb:'',fd:1,cf:(typeof CFJA!=='undefined'&&CFJA[e.cf])||''});
    });
  });
}
