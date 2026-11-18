// アジア・オセアニアの会社を調べるサイト(静的ファイル方式)。データベースは使わず、/c/(会社ページ用)と /n/(名前検索用)の静的ファイルだけで動く。
import { Hono } from 'hono'
import { CSS, esc, fmt } from '../../relationship-map-site/src/app.mjs'

const CC = {
  TW: { name: '台湾', reg: '台湾 経済部商業発展署(商工行政資料開放平台)', lic: '政府資料開放授權條款 第1版', licUrl: 'https://data.gov.tw/license', url: (id) => `https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do?banNo=${encodeURIComponent(id)}` },
  AU: { name: 'オーストラリア', reg: 'オーストラリア ABN Lookup(Australian Business Register)', lic: 'CC BY 3.0 AU', licUrl: 'https://creativecommons.org/licenses/by/3.0/au/', url: (id) => `https://abr.business.gov.au/ABN/View?abn=${encodeURIComponent(id)}` },
}
const SITE = { name: 'アジア・オセアニアの会社を調べる' }
const LEG = new Set(['ltd', 'limited', 'plc', 'llp', 'llc', 'inc', 'lp', 'cic', 'sas', 'sarl', 'sa', 'sasu', 'eurl', 'sci', 'snc', 'as', 'asa', 'ans', 'da', 'ba', 'oy', 'oyj', 'ab', 'gmbh', 'ag', 'kg', 'ug', 'bv', 'nv', 'ou', 'tu', 'uu', 'mu', 'fie', 'co', 'company', 'the', 'pty', 'nl'])
// build_asiapac_shards.py の core() と同じ規則
const core = (name) => {
  const s = String(name || '').normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase()
  const toks = s.replace(/[^\p{L}\p{N}]+|_/gu, ' ').split(' ').filter(Boolean)
  for (;;) {
    if (toks.length > 1 && LEG.has(toks[toks.length - 1])) toks.pop()
    else if (toks.length > 1 && LEG.has(toks[0])) toks.shift()
    else if (toks.length > 3 && (toks[0] === 'trustee' || toks[0] === 'trustees') && (toks[1] === 'for' || toks[1] === 'of')) toks.splice(0, 2)
    else break
  }
  return toks.join('')
}
const fnv = (k) => { let h = 2166136261; for (let i = 0; i < k.length; i++) h = Math.imul(h ^ k.charCodeAt(i), 16777619) >>> 0; return h }
const initial = (s) => esc(String(s || '?').trim().slice(0, 1).toUpperCase() || '?')

function page({ title, desc = '', body, canonical = '', noindex = false }) {
  const srcs = Object.values(CC).map((c) => `${esc(c.reg)}(<a href="${esc(c.licUrl)}" rel="noopener">${esc(c.lic)}</a>)`).join(' ・ ')
  return `<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title><meta name="description" content="${esc(desc.slice(0, 160))}">${canonical ? `<link rel="canonical" href="${esc(canonical)}">` : ''}${noindex ? '<meta name="robots" content="noindex,follow">' : ''}<meta name="theme-color" content="#2457d6">
<style>${CSS}</style></head><body>
<div class="top"><div class="in"><a class="brand" href="/"><span class="logo">∞</span>${SITE.name}</a><form action="/search" method="get" role="search"><input type="search" name="q" placeholder="会社名(例: 台積電 / Telstra / 鴻海)" aria-label="会社名で検索"><button>検索</button></form></div></div>
<main>${body}</main>
<footer><p>各国の政府が公開している会社登記データを、加工して作成しています。出典: ${srcs}。このサービスの内容は、各国の登記所が保証したものではありません。</p><p>登記の最新の内容は、各ページの「公式の登記で見る」のリンクでご確認ください。誤りや削除のご希望は、お問い合わせください。</p></footer></body></html>`
}

export function createApp(opts = {}) {
  const app = new Hono()
  const getAsset = opts.getAsset || (async () => null)
  const origin = (c) => new URL(c.req.url).origin
  let hotCache = null, metaCache = null
  const meta = async () => (metaCache ||= JSON.parse((await getAsset('/c/meta.json').catch(() => null)) || '{}'))
  const hotMap = async () => {
    if (hotCache) return hotCache
    const t = await getAsset('/n/hot.json').catch(() => null)
    hotCache = {}
    for (const [L, arr] of Object.entries(t ? JSON.parse(t) : {})) hotCache[Number(L)] = new Set(arr)
    return hotCache
  }
  const shardRow = async (cc, id) => {
    const m = await meta()
    if (!m.nd) return null
    const t = await getAsset(`/c/${fnv(cc + ':' + id) % m.nd}.json`)
    const r = t && JSON.parse(t).find((x) => x[0] === cc && x[1] === id)
    return r ? { cc: r[0], id: r[1], name: r[2], kind: r[3], city: r[4], post: r[5], since: r[6], sic: r[7] } : null
  }
  const search = async (q) => {
    const cq = core(q), cp = Array.from(cq)
    if (cp.length < 2) return { rows: [], short: true }
    const m = await meta(), hot = await hotMap()
    let L = 2
    while (L < 6 && hot[L]?.has(cp.slice(0, L).join('')) && cp.length > L) L++
    if (cp.length < L) return { rows: [], short: true }
    const t = await getAsset(`/n/${fnv(cp.slice(0, L).join('')) % (m.nb || 1)}.json`)
    if (!t) return { rows: [] }
    return { rows: JSON.parse(t).filter((r) => core(r[2]).startsWith(cq)).slice(0, 80).map((r) => ({ cc: r[0], id: r[1], name: r[2], city: r[3] })) }
  }

  app.get('/', async (c) => {
    const m = await meta()
    const by = m.by || {}
    const total = m.total || Object.values(by).reduce((a, b) => a + b, 0)
    const body = `<section class="hero"><h1>アジア・オセアニアの会社を、会社名で調べる</h1><p>各国の政府が公開している会社登記から、現存する会社を検索できます。</p>
<form action="/search" method="get" role="search"><input type="search" name="q" placeholder="例: 台積電 / 鴻海 / Telstra / Woolworths" aria-label="検索"><button>検索</button></form>
<div class="chips"><span>掲載 ${fmt(total)}社</span>${Object.entries(CC).map(([k, v]) => by[k] ? `<span>${esc(v.name)} ${fmt(by[k])}社</span>` : '').join('')}</div></section>
<div class="card"><h2>掲載している国と出典</h2><ul class="list">${Object.entries(CC).map(([k, v]) => `<li><span class="av sq">${esc(k)}</span><div class="tx"><b>${esc(v.name)}</b> ${by[k] ? `<span class="muted">${fmt(by[k])}社</span>` : ''}<small>${esc(v.reg)} ・ <a href="${esc(v.licUrl)}" rel="noopener">${esc(v.lic)}</a></small></div></li>`).join('')}</ul></div>
<p class="muted">日本の会社は<a href="https://kigyo-hito-tsunagari.yuma-takeshita.workers.dev/">日本の会社と人のつながり</a>、ヨーロッパの会社は<a href="https://kigyo-europe.yuma-takeshita.workers.dev/">ヨーロッパの会社を調べる</a>で調べられます。</p>`
    return c.html(page({ title: `${SITE.name}`, desc: '台湾・オーストラリアの会社登記から、会社名で検索できます。', body, canonical: origin(c) + '/' }))
  })

  app.get('/search', async (c) => {
    const q = (c.req.query('q') || '').trim().slice(0, 60)
    const { rows, short } = q ? await search(q) : { rows: [], short: true }
    const body = `<h1 class="page">「${esc(q)}」の検索結果</h1><div class="card">${short ? '<p>2文字以上で入力してください(会社名の先頭からの一致で探します)。</p>' : rows.length ? `<ul class="list">${rows.map((r) => `<li><span class="av sq">${esc(r.cc)}</span><div class="tx"><a href="/e/${esc(r.cc)}/${encodeURIComponent(r.id)}"><b>${esc(r.name)}</b></a><small>${esc(CC[r.cc]?.name || r.cc)}${r.city ? ' ・ ' + esc(r.city) : ''} ・ 登記番号 ${esc(r.id)}</small></div></li>`).join('')}</ul>` : '<p>見つかりませんでした。会社名の先頭からの一致で探しています。</p>'}</div>`
    return c.html(page({ title: `「${q}」の検索結果 | ${SITE.name}`, body, noindex: true }))
  })

  app.get('/e/:cc/:id', async (c) => {
    const cc = c.req.param('cc'), id = c.req.param('id')
    if (!CC[cc] || !/^[A-Za-z0-9\-]{1,20}$/.test(id)) return c.notFound()
    const r = await shardRow(cc, id)
    if (!r) return c.html(page({ title: '見つかりません', body: '<div class="card"><h1 class="page">見つかりません</h1><p>この登記番号の会社は、掲載していません(閉鎖された会社などの可能性があります)。</p></div>', noindex: true }), 404)
    const info = CC[cc]
    const rows = [['国', info.name], ['登記番号', r.id], ['会社名', r.name], r.kind && ['種類', r.kind], r.city && ['所在地(市区町村)', r.city], r.post && ['郵便番号', r.post], r.since && ['設立・登記の日', r.since], r.sic && ['事業の種類', r.sic]].filter(Boolean)
    const body = `<div class="card head"><span class="av sq">${esc(cc)}</span><div><h1 class="page">${esc(r.name)}</h1><p class="muted" style="margin:0">${esc(info.name)}${r.kind ? ' ・ ' + esc(r.kind) : ''}${r.city ? ' ・ ' + esc(r.city) : ''}</p></div></div>
<div class="card"><h2>登記の情報</h2><dl>${rows.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl><p class="src"><a href="${esc(info.url(r.id))}" rel="noopener nofollow" target="_blank">公式の登記で見る ↗</a></p></div>
<p class="src">出典: ${esc(info.reg)}の公開データ(<a href="${esc(info.licUrl)}" rel="noopener">${esc(info.lic)}</a>)を加工して作成しています。</p>`
    return c.html(page({ title: `${r.name}(${info.name}・${r.id}) | ${SITE.name}`, desc: `${r.name}の登記情報。${info.name}${r.city ? '・' + r.city : ''}。`, body, canonical: `${origin(c)}/e/${cc}/${encodeURIComponent(id)}` }))
  })

  app.get('/robots.txt', (c) => c.text('User-agent: *\nAllow: /\nDisallow: /search\n'))
  app.get('/favicon.ico', (c) => c.body(null, 204))
  return app
}
