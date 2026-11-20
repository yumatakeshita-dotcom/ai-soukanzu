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

// ===== 2026-11-20 追加: Stripe 課金(Payment Link → webhook → アクセスキー自動発行) =====
// 秘密の値はコードに書かず、Worker の「秘密設定」で渡す: STRIPE_WEBHOOK_SECRET(whsec_...)、STRIPE_SECRET_KEY(sk_...)、PRO_KEY_SECRET(自分で作るランダムな長い文字列)
// アクセスキーは PRO_KEY_SECRET と購入IDから計算で作る(保存するのはハッシュだけ)。同じ購入からは必ず同じキーになるので、webhook が2回届いても二重に発行されない。
const BUSINESS_MIN_AMOUNT = 5000; // 円。これ以上の支払いは法人プラン(価格は仮: 個人980円/法人9,800円)

function b64url(buf) {
  let s = ''; for (const b of new Uint8Array(buf)) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
async function hmacKey(secret, usage) {
  return crypto.subtle.importKey('raw', new TextEncoder().encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, usage);
}
async function deriveKey(env, purchaseId) {
  const sig = await crypto.subtle.sign('HMAC', await hmacKey(env.PRO_KEY_SECRET, ['sign']), new TextEncoder().encode('pro-key:' + purchaseId));
  return b64url(sig).slice(0, 32);
}
// Stripe-Signature(t=時刻,v1=署名)を確かめる。5分より古いものは断る(使い回し対策)
async function verifyStripeSig(raw, header, secret) {
  const parts = Object.fromEntries((header || '').split(',').map(p => p.split('=')).filter(p => p.length === 2));
  const t = Number(parts.t); const sigs = (header || '').split(',').filter(p => p.startsWith('v1=')).map(p => p.slice(3));
  if (!t || !sigs.length || Math.abs(Date.now() / 1000 - t) > 300) return false;
  const k = await hmacKey(secret, ['verify']);
  for (const sig of sigs) {
    const bytes = new Uint8Array((sig.match(/../g) || []).map(h => parseInt(h, 16)));
    if (bytes.length === 32 && await crypto.subtle.verify('HMAC', k, bytes, new TextEncoder().encode(t + '.' + raw))) return true;
  }
  return false;
}

async function stripeWebhook(req, env) {
  if (req.method !== 'POST') return reply({ ok: false, error: 'method' }, 405);
  if (!env.DB || !env.STRIPE_WEBHOOK_SECRET || !env.PRO_KEY_SECRET) return reply({ ok: false, error: 'not_ready' }, 503);
  const raw = await req.text(); // 署名は本文そのままに対してかけるので、JSONにする前の文字列を使う
  if (!await verifyStripeSig(raw, req.headers.get('stripe-signature'), env.STRIPE_WEBHOOK_SECRET)) return reply({ ok: false, error: 'signature' }, 400);
  let ev; try { ev = JSON.parse(raw); } catch (e) { return reply({ ok: false, error: 'bad_json' }, 400); }
  const o = (ev.data && ev.data.object) || {};
  const now = new Date().toISOString();
  if (ev.type === 'checkout.session.completed') {
    // 支払い済みのときだけキーを作る(後払い・未払いのときは checkout.session.async_payment_succeeded で別に来る)
    if (o.payment_status === 'paid') await issueFromSession(env, o, now);
  } else if (ev.type === 'checkout.session.async_payment_succeeded') {
    await issueFromSession(env, o, now);
  } else if (ev.type === 'customer.subscription.deleted') {
    await setStatus(env, 'stripe_subscription', o.id, 'canceled');
  } else if (ev.type === 'customer.subscription.updated') {
    // 支払いが止まった(past_due / unpaid)ら無効、戻ったら有効に戻す。active のほかは使えない
    const st = ['active', 'trialing'].includes(o.status) ? 'active' : (o.status === 'canceled' ? 'canceled' : o.status);
    await setStatus(env, 'stripe_subscription', o.id, st);
  } else if (ev.type === 'charge.refunded') {
    if (o.refunded) await setStatus(env, 'stripe_customer', o.customer, 'refunded'); // 全額返金のときだけ
  } else if (ev.type === 'charge.dispute.created') {
    await setStatus(env, 'stripe_customer', o.customer || null, 'disputed');
  }
  return reply({ ok: true }); // 知らない種類のイベントも 200 で返す(Stripe に何度も再送させない)
}
async function issueFromSession(env, s, now) {
  const purchaseId = s.subscription || s.id;
  const key = await deriveKey(env, purchaseId);
  const plan = (s.amount_total || 0) >= BUSINESS_MIN_AMOUNT ? 'business' : 'personal';
  // 足すだけ(同じキーがすでにあれば何もしない)。メールアドレスは保存しない
  await env.DB.prepare('INSERT OR IGNORE INTO pro_keys (key_hash, plan, status, expires_at, note, created_at, stripe_customer, stripe_subscription) VALUES (?1, ?2, \'active\', NULL, ?3, ?4, ?5, ?6)')
    .bind(await sha256Hex(key), plan, 'stripe ' + (s.customer || s.id), now, s.customer || null, s.subscription || null).run();
}
async function setStatus(env, col, id, status) {
  if (!id) return; // 対象がわからないときは何もしない
  const c = col === 'stripe_subscription' ? 'stripe_subscription' : 'stripe_customer';
  await env.DB.prepare(`UPDATE pro_keys SET status = ?1 WHERE ${c} = ?2`).bind(status, id).run();
}
// 購入後のページ(/pro/thanks.html?session_id=...)が、買った本人にキーを見せるための入口。
// Stripe に「その session は支払い済みか」を問い合わせ、済みのときだけ同じ計算でキーを返す。session_id は推測できない長い文字列。
async function claimKey(req, env, url) {
  if (req.method !== 'POST') return reply({ ok: false, error: 'method' }, 405);
  const origin = req.headers.get('origin');
  if (origin && origin !== url.origin) return reply({ ok: false, error: 'origin' }, 403);
  if (!env.DB || !env.STRIPE_SECRET_KEY || !env.PRO_KEY_SECRET) return reply({ ok: false, error: 'not_ready' }, 503);
  let id; try { id = String((await req.json()).session_id || ''); } catch (e) { return reply({ ok: false, error: 'bad_json' }, 400); }
  if (!/^cs_(test|live)_[A-Za-z0-9]{10,200}$/.test(id)) return reply({ ok: false, error: 'bad_id' }, 400);
  const r = await fetch('https://api.stripe.com/v1/checkout/sessions/' + id, { headers: { authorization: 'Bearer ' + env.STRIPE_SECRET_KEY } });
  if (!r.ok) return reply({ ok: false, error: 'not_found' }, 404);
  const s = await r.json();
  if (s.status !== 'complete' || s.payment_status !== 'paid') return reply({ ok: false, error: 'not_paid' }, 402);
  // webhook がまだ届いていなくても、ここで同じ行を足しておく(同じキーなので二重にならない)
  await issueFromSession(env, s, new Date().toISOString());
  return reply({ ok: true, key: await deriveKey(env, s.subscription || s.id) });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname === '/api/stripe/webhook') return stripeWebhook(req, env);
    if (url.pathname === '/api/pro/claim') return claimKey(req, env, url);
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
