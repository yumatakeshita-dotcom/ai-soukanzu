p='build_hub2.py';b=open(p,encoding='utf-8').read()
a=" {'id': 'cox', 'name': 'クリス・コックス',"
assert a in b
new=" {'id': 'mosseri', 'name': 'アダム・モセリ', 'kind': 'p', 'from': 2018, 'desc': 'Instagramの責任者(Head of Instagram)。2008年にFacebookへプロダクトデザイナーとして入り、のちにニュースフィードの製品・開発を率いました。2018年、Instagramの創業者2人の退任を受けて責任者に就任。Threadsも事実上統括していると報じられています。以前はTokBoxの最初のデザイナー、2002年に学生時代にデザイン会社Blank Mosseriを創業。ニューヨーク出身で、NYUのGallatin校で学びました(Metaの経営陣のページ・報道)。', 'role': 'Instagram責任者'},\n"
b=b.replace(a,new+a,1)
b=b.replace("'cox': 'Chris Cox', 'wang': 'Alexandr Wang',","'cox': 'Chris Cox', 'mosseri': 'Adam Mosseri', 'wang': 'Alexandr Wang',",1)
open(p,'w',encoding='utf-8').write(b)
p='hub_template.html';h=open(p,encoding='utf-8').read()
h=h.replace("const ALIAS={'メタ':['Meta'],","const ALIAS={'モセリ':['Mosseri'],'モッセリ':['Mosseri'],'メタ':['Meta'],",1)
a="    return lines.join('\n').slice(0,9000);\n  }\n"
assert a in h
add=("    /* 5) 人物(全社の相関図に載っている人)・組織。綴りの揺れ(sが1つ多い少ない)を許す */\n"
"    try{const col=s=>norm(s).replace(/(.)\1+/g,'$1');const idx=buildIndex();\n"
"      const lt=T.filter(t=>t.length>=3).map(t=>({n:norm(t),c:col(t)}));\n"
"      Object.values(PEOPLE).forEach(o=>{const nn=norm(o.jp+' '+o.en);const cc=col(o.jp+' '+o.en);if(lt.some(t=>nn.includes(t.n)||cc.includes(t.c)))add(`人物 ${o.jp}(${o.en}): `+o.rows.slice(0,6).map(r=>`${r.co}${r.role?' '+r.role:''}${r.from?' '+r.from+'〜'+(r.to||'現在'):''}`).join(' / ')+(o.rows[0]&&o.rows[0].desc?' '+o.rows[0].desc.slice(0,160):''))});\n"
"    }catch(e){}\n")
h=h.replace(a,add+a,1)
open(p,'w',encoding='utf-8').write(h)
print('ok')
