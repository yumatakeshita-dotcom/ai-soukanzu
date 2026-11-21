// 変更のあとに必ず動かす確認。全ページを開いて、エラーが出ないかを見る。使い方: npm run check
const {chromium}=require('playwright');const {start}=require('./serve');
const PAGES=[
 ['index.html',"build('openai');build('anthropic');build('tsmc');build('jasm')"],
 ['index.html#common',"showCommon('Microsoft','Nvidia');showCommon('楽天グループ','OpenAI');build('openai');document.getElementById('gocommon').click()"],
 ['index.html#common',"showCommon('楽天グループ','OpenAI');document.getElementById('cmbrief').click();showCommon('トヨタ自動車','ソフトバンクグループ');document.getElementById('cmbrief').click()"],
 ['index.html',"showExecTl('openai');document.querySelector('[data-t=out]').click();document.querySelector('[data-y=\"2026\"]').click();showExecTl('anthropic');document.querySelector('[data-t=all]').click();showExecTl('xai');showExecTl('gdm');showExecTl('nvidia')"],
 ['credits.html',"document.getElementById('q').value='musk';document.getElementById('q').dispatchEvent(new Event('input'))"],['lab/route.html',''],['lab/stop.html',''],['lab/money.html',''],['lab/moves.html',''],['lab/cards.html',"document.getElementById('ten').click()"],['lab/sports.html',''],['legal/terms.html',''],['legal/privacy.html',''],['legal/tokushoho.html',''],['legal/contact.html','']
];
const {spawnSync}=require('child_process');
const seo=spawnSync('python3',[require('path').join(__dirname,'seo.py'),'--check'],{encoding:'utf8'});
console.log((seo.status===0?'OK  ':'NG  ')+'共有カード用 meta(seo.py --check)'+(seo.status===0?'':'\n'+seo.stdout+'→ python3 scripts/seo.py で直せます'));
(async()=>{const srv=await start(8123);const b=await chromium.launch();let bad=seo.status===0?0:1;
 for(const [p,act] of PAGES){for(const w of [1280,390]){const pg=await b.newPage({viewport:{width:w,height:900}});const errs=[];
  pg.on('pageerror',e=>errs.push(e.message));
  await pg.goto('http://localhost:8123/'+p,{waitUntil:'load',timeout:120000});await pg.waitForTimeout(1500);
  if(act)try{await pg.evaluate(act)}catch(e){errs.push(e.message)}
  const wide=await pg.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
  const ok=!errs.length&&!wide;if(!ok)bad++;
  console.log((ok?'OK  ':'NG  ')+p+' ('+w+'px)'+(errs.length?' エラー: '+errs.join(' / '):'')+(wide?' 横にはみ出しあり':''));await pg.close()}}
 await b.close();srv.close();console.log(bad?`\n${bad}件の問題があります`:'\nすべて問題ありません');process.exit(bad?1:0)})();
