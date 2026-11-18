p='hub_template.html';h=open(p,encoding='utf-8').read()
BS=chr(92)
fn=open('_ai_fn.js',encoding='utf-8').read()
a="  async function ask(){"
assert a in h and 'function siteSearch' not in h
h=h.replace(a,fn+a,1)
old="    const input=[{role:'user',content:`${RULES}"+BS+"n"+BS+"n【いま開いているページ】${c.kind}「${c.title}」"+BS+"n【ページの内容】"+BS+"n${c.body}`},...turns];"
assert old in h
new=("    const hits=siteSearch(q);"+"\n"+
"    const input=[{role:'user',content:`${RULES2}"+BS+"n"+BS+"n【いま開いているページ】${c.kind}「${c.title}」"+BS+"n【ページの内容】"+BS+"n${c.body}${hits?'"+BS+"n"+BS+"n【サイト全体の検索結果(質問の語に合う記録。ページに無いことはここを根拠に)】"+BS+"n'+hits:''}`},...turns];")
h=h.replace(old,new,1)
a="  const msg=(cls,t)=>{"
add="  const RULES2=RULES+'"+BS+"n- 「サイト全体の検索結果」がある場合は、それも根拠にしてよい。買収(会社そのものの取得)と、出資(一部の株式の取得)・提携・ライセンスは区別して答える。検索結果に該当が無い場合は「このサイトの記録には見当たりません」と言い、【一般知識】で補う。';"+"\n"
assert a in h
h=h.replace(a,add+a,1)
h=h.replace("いま画面に出ている人物・会社・表の内容をもとに答えます。","いま画面に出ている人物・会社・表の内容と、サイト全体(買収・子会社、世界の企業、VCの投資先)から質問の語に合う記録をもとに答えます。",1)
h=h.replace("chips:['最近の大きな買収は?','金額の大きい順に挙げて','分野ごとの傾向を教えて']","chips:['最近の大きな買収は?','金額の大きい順に挙げて','分野ごとの傾向を教えて','Metaグラスはどこかのメガネ会社を買収した?']",1)
open(p,'w',encoding='utf-8').write(h)
print('patched')
