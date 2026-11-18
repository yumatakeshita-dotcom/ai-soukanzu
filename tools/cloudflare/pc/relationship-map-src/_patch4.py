p='hub_template.html';h=open(p,encoding='utf-8').read()
BS=chr(92)
i=h.index("  const RULES='");j=h.index("\n",i)
rules=("あなたは、企業・人物の相関図ページに組み込まれた質問係です。日本語で簡潔に、でも役に立つ答えを返してください。"+BS+"n"
"【根拠の順】①ページの内容 ②サイト全体の検索結果 ③一般知識。"+BS+"n"
"- ①②に書かれていることは、そのまま根拠にしてよい。"+BS+"n"
"- ①②だけでは足りないときも、断らない。分かる範囲をまず答え、足りない部分は③で補う。③の部分は文頭に「【一般知識】」を付け、確かさ(高い/中くらい/低い)を添える。"+BS+"n"
"- 「わからない」「控えます」だけで終えない。分からない部分があるときは、(1)何が分かって何が分からないか、(2)公式サイトや報道で何を調べれば確かめられるか、を1〜2文で添える。"+BS+"n"
"- 数字・年・肩書は、確かなものだけを書く。推測は「推測」と書き、報道ベースのことは断定しない。"+BS+"n"
"- 生年月日・資産・家族・健康・住所などの私生活は、本人が公表している範囲に限る。公表されていないことは書かない。"+BS+"n"
"- 質問が広いときは、要点を3〜5個にまとめ、最後に「もっと詳しく知りたい点」を1つ提案する。")
new="  const RULES='"+rules.replace("'","’")+"';"
h=h[:i]+new+h[j:]
# RULES2 text: keep, but adjust the last sentence about missing records
old_tail="検索結果に該当が無い場合は「このサイトの記録には見当たりません」と言い、【一般知識】で補う。"
if old_tail in h: pass
# add person career to siteSearch rows
old="(o.rows[0]&&o.rows[0].desc?' '+o.rows[0].desc.slice(0,160):''))"
assert old in h
h=h.replace(old,"(o.rows[0]&&o.rows[0].desc?' '+o.rows[0].desc.slice(0,200):'')+(o.career&&o.career.length?' 経歴: '+o.career.slice(0,10).map(c=>c[0]+' '+c[1]).join(' / '):''))",1)
# Web search link after each answer
old2="      turns.push({role:'assistant',content:r.text});"
assert old2 in h
h=h.replace(old2,old2+"\n      const lk=document.createElement('div');lk.className='h';const a=document.createElement('a');a.href='https://www.google.com/search?q='+encodeURIComponent(q);a.target='_blank';a.rel='noopener';a.textContent='この質問をWebで調べる ↗';lk.appendChild(a);$('aimsgs').appendChild(lk);",1)
h=h.replace("ページに載っていないことは「一般知識」と分けて答え、確認できないことは「わからない」と答えます。","ページに載っていないことは【一般知識】と分けて、確かさを添えて答えます。それでも確かめられない部分は、何をどこで調べればよいかを案内します。",1)
open(p,'w',encoding='utf-8').write(h);print('ok')
