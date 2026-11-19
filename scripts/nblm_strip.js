// NotebookLM用: JSの大きなデータ(配列・オブジェクト・長い文字列)を「データ省略」に置きかえる。scripts/nblm_code.py が使う。2026/11/19追加
// 使い方: node strip.js 入力.js  → 大きなデータの値を省略した版を標準出力に
const acorn=require('acorn'),fs=require('fs');
function strip(src,lim=200){
  let ast;
  try{ast=acorn.parse(src,{ecmaVersion:'latest',sourceType:'script',allowReturnOutsideFunction:true});}
  catch(e){return null;}
  const reps=[];
  const hasFn=n=>{let f=false;(function w(x){if(f||!x||typeof x.type!=='string')return;if(/Function/.test(x.type)){f=true;return}for(const k in x){const v=x[k];if(Array.isArray(v))v.forEach(w);else if(v&&typeof v.type==='string')w(v)}})(n);return f};
  (function walk(n){
    if(!n||typeof n.type!=='string')return;
    const len=n.end-n.start;
    if(n.type==='ObjectExpression'&&n.properties.length>20&&hasFn(n)){
      // 同じ形の関数がたくさん並ぶ所(会社ごとの図を作る関数など)は、形ごとに1つだけ残す
      const norm=p=>src.slice(p.value?p.value.start:p.start,p.end).replace(/"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|`(?:[^`\\]|\\.)*`/g,'S').replace(/\d+(\.\d+)?/g,'0').replace(/\s+/g,'');
      const seen=new Map();
      n.properties.forEach(p=>{const k=norm(p);if(!seen.has(k))seen.set(k,{first:p,rest:[]});else seen.get(k).rest.push(p)});
      for(const g of seen.values()){walk(g.first);
        if(g.rest.length){const names=g.rest.map(p=>p.key?(p.key.name||p.key.value):'?');
          g.rest.forEach((p,i)=>{let e=p.end;if(src[e]===',')e++;reps.push([p.start,e,i===0?`\n/* 同じ形の項目を省略: ${names.length}件(${names.slice(0,8).join(', ')}${names.length>8?' ほか':''}) */\n`:''])});}}
      return;}
    if(len>lim){
      if((n.type==='ArrayExpression'||n.type==='ObjectExpression')&&!hasFn(n)){
        const cnt=n.type==='ArrayExpression'?n.elements.length:n.properties.length;
        const head=src.slice(n.start,n.start+80).replace(/\*\//g,'* /').replace(/\n/g,' ');
        reps.push([n.start,n.end,(n.type==='ArrayExpression'?'[':'{')+`/* データ省略: ${cnt}件・${len}文字。先頭: ${head}… */`+(n.type==='ArrayExpression'?']':'}')]);return;}
      if((n.type==='Literal'&&typeof n.value==='string')||n.type==='TemplateLiteral'){
        reps.push([n.start,n.end,`"" /* 長い文字列を省略: ${len}文字 */`]);return;}
    }
    for(const k in n){const v=n[k];if(Array.isArray(v))v.forEach(walk);else if(v&&typeof v.type==='string')walk(v)}
  })(ast);
  reps.sort((a,b)=>b[0]-a[0]);let out=src;for(const [s,e,r] of reps)out=out.slice(0,s)+r+out.slice(e);
  return out;
}
module.exports=strip;
if(require.main===module){const r=strip(fs.readFileSync(process.argv[2],'utf8'));if(r===null){console.error('PARSE_FAIL');process.exit(1)}process.stdout.write(r)}
