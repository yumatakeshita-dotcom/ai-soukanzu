p='hub_template.html';h=open(p,encoding='utf-8').read()
BS=chr(92)
if "'モセリ':['Mosseri']" not in h:
    h=h.replace("const ALIAS={'メタ':['Meta'],","const ALIAS={'モセリ':['Mosseri'],'モッセリ':['Mosseri'],'メタ':['Meta'],",1)
key="    return lines.join('"+BS+"n').slice(0,9000);"
assert key in h
add=("    /* 5) 人物(全社の相関図に載っている人)。綴りの揺れ(sが1つ多い少ない)を許す */\n"
"    try{const col=s=>norm(s).replace(/(.)"+BS+"1+/g,'$1');buildIndex();\n"
"      const lt=T.filter(t=>t.length>=3).map(t=>({n:norm(t),c:col(t)}));\n"
"      Object.values(PEOPLE).forEach(o=>{const nn=norm(o.jp+' '+o.en);const cc=col(o.jp+' '+o.en);if(lt.some(t=>nn.includes(t.n)||cc.includes(t.c)))add('人物 '+o.jp+'('+o.en+'): '+o.rows.slice(0,6).map(r=>r.co+(r.role?' '+r.role:'')+(r.from?' '+r.from+'〜'+(r.to||'現在'):'')).join(' / ')+(o.rows[0]&&o.rows[0].desc?' '+o.rows[0].desc.slice(0,160):''))});\n"
"    }catch(e){}\n")
if "5) 人物(全社" not in h:
    h=h.replace(key,add+key,1)
open(p,'w',encoding='utf-8').write(h);print('ok')
