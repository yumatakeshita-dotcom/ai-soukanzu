// kigyo-relmap: 相関図の公開版。GitHub の main の site/ をそのまま配る(2026-11-18 から)。
// ファイルをCloudflareに上げ直さなくても、main が更新されると数分で公開側にも出る。
//
// 2026-11-20 追加: プロ会員のための小さなAPI(/api/pro/*)。D1 の束ね名 DB が付いているときだけ動く。
//   POST /api/pro/waitlist {email, plan}  先行案内の申し込みを D1 の pro_waitlist に足す(足すだけ)
//   POST /api/pro/verify   {key}          アクセスキーが有効かを返す(キーそのものは保存せず、ハッシュで照らす)
// DB が付いていないとき(まだ準備中)は 503 を返す。画面側は「会員ではない」として扱うので、ほかの機能には影響しない。
const ORIGIN = 'https://raw.githubusercontent.com/yumatakeshita-dotcom/ai-soukanzu/main/site';
const TYPES = {
  html: 'text/html; charset=utf-8', js: 'text/javascript; charset=utf-8', json: 'application/json; charset=utf-8',
  css: 'text/css; charset=utf-8', svg: 'image/svg+xml', png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg',
  webp: 'image/webp', gif: 'image/gif', ico: 'image/x-icon', txt: 'text/plain; charset=utf-8', xml: 'application/xml',
};
const JSON_HEADERS = { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', 'x-content-type-options': 'nosniff' };
const reply = (obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: JSON_HEADERS });

async function sha256Hex(s) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

async function proApi(req, env, url) {
  if (req.method !== 'POST') return reply({ ok: false, error: 'method' }, 405);
  // 別のサイトのページからの呼び出しは受けない(Origin が付いていて、自分と違うものは断る)
  const origin = req.headers.get('origin');
  if (origin && origin !== url.origin) return reply({ ok: false, error: 'origin' }, 403);
  if (!env.DB) return reply({ ok: false, error: 'not_ready' }, 503);
  let body;
  try {
    const text = await req.text();
    if (text.length > 2000) return reply({ ok: false, error: 'too_large' }, 413);
    body = JSON.parse(text);
  } catch (e) { return reply({ ok: false, error: 'bad_json' }, 400); }

  if (url.pathname === '/api/pro/waitlist') {
    const email = String(body.email || '').trim().toLowerCase();
    const plan = ['personal', 'business'].includes(body.plan) ? body.plan : 'personal';
    if (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return reply({ ok: false, error: 'email' }, 400);
    await env.DB.prepare('INSERT OR IGNORE INTO pro_waitlist (email, plan, created_at) VALUES (?1, ?2, ?3)')
      .bind(email, plan, new Date().toISOString()).run();
    return reply({ ok: true });
  }
  if (url.pathname === '/api/pro/verify') {
    const key = String(body.key || '').trim();
    if (!/^[A-Za-z0-9_-]{20,80}$/.test(key)) return reply({ ok: false, error: 'key_format' }, 400);
    const row = await env.DB.prepare('SELECT plan, status, expires_at FROM pro_keys WHERE key_hash = ?1')
      .bind(await sha256Hex(key)).first();
    const alive = row && row.status === 'active' && (!row.expires_at || row.expires_at > new Date().toISOString());
    return reply(alive ? { ok: true, plan: row.plan } : { ok: false, error: 'invalid' });
  }
  return reply({ ok: false, error: 'not_found' }, 404);
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname.startsWith('/api/pro/')) return proApi(req, env, url);
    if (req.method !== 'GET' && req.method !== 'HEAD') return new Response('Method Not Allowed', { status: 405 });
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
