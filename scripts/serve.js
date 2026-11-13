// サイトを手元で表示するための小さなサーバー。使い方: npm run serve → http://localhost:8000
const http=require('http'),fs=require('fs'),path=require('path');
const ROOT=path.join(__dirname,'..','site');
const TYPES={'.html':'text/html; charset=utf-8','.json':'application/json; charset=utf-8','.css':'text/css','.js':'text/javascript','.png':'image/png','.jpg':'image/jpeg'};
function start(port=8000){return new Promise(res=>{const s=http.createServer((req,rep)=>{
  let p=decodeURIComponent(req.url.split('?')[0]);if(p.endsWith('/'))p+='index.html';
  const f=path.join(ROOT,p);if(!f.startsWith(ROOT)||!fs.existsSync(f)){rep.writeHead(404);return rep.end('not found')}
  rep.writeHead(200,{'Content-Type':TYPES[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(rep)});
  s.listen(port,()=>res(s))})}
if(require.main===module)start(+process.env.PORT||8000).then(()=>console.log('表示中: http://localhost:'+(process.env.PORT||8000)+'  (止めるときは Ctrl+C)'));
module.exports={start};
