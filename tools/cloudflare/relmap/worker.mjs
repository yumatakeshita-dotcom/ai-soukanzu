// kigyo-relmap: 相関図の公開版。GitHub の main の site/ をそのまま配る(2026-11-18 から)。
// ファイルをCloudflareに上げ直さなくても、main が更新されると数分で公開側にも出る。
const ORIGIN = 'https://raw.githubusercontent.com/yumatakeshita-dotcom/ai-soukanzu/main/site';
const TYPES = {
  html: 'text/html; charset=utf-8', js: 'text/javascript; charset=utf-8', json: 'application/json; charset=utf-8',
  css: 'text/css; charset=utf-8', svg: 'image/svg+xml', png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg',
  webp: 'image/webp', gif: 'image/gif', ico: 'image/x-icon', txt: 'text/plain; charset=utf-8', xml: 'application/xml',
};
export default {
  async fetch(req) {
    if (req.method !== 'GET' && req.method !== 'HEAD') return new Response('Method Not Allowed', { status: 405 });
    const url = new URL(req.url);
    let path = decodeURIComponent(url.pathname);
    if (path.includes('..')) return new Response('Not Found', { status: 404 });
    if (path.endsWith('/')) path += 'index.html';
    let ext = (path.split('/').pop().split('.')[1] || '').toLowerCase();
    if (!ext) { // /lab のような「フォルダ」は / を付けて案内する
      return Response.redirect(url.origin + url.pathname + '/' + url.search, 301);
    }
    const r = await fetch(ORIGIN + path.split('/').map(encodeURIComponent).join('/'), {
      cf: { cacheTtl: 300, cacheEverything: true },
    });
    if (!r.ok) return new Response('Not Found', { status: r.status === 404 ? 404 : 502 });
    const h = new Headers({
      'content-type': TYPES[ext] || 'application/octet-stream',
      'cache-control': 'public, max-age=300',
      'x-content-type-options': 'nosniff',
    });
    return new Response(req.method === 'HEAD' ? null : r.body, { status: 200, headers: h });
  },
};
