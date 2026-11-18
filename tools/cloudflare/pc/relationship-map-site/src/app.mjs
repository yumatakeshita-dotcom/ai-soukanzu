// 相関図サイトの本体。Hono のアプリ。データベースは db オブジェクト(all/get)を渡して使うので、
// 手元(Node の SQLite)でも、本番(Cloudflare D1)でも、同じコードが動く。画像は /img/ の静的ファイル。
import { Hono } from 'hono'

const KIND = { '101': '国の機関', '201': '地方公共団体', '301': '株式会社', '302': '有限会社', '303': '合名会社', '304': '合資会社', '305': '合同会社', '399': 'その他の設立登記法人', '401': '外国会社等', '499': 'その他' }
const WPRL = { founder: '創業者', ceo: 'CEO', chair: '会長', board: '取締役', owner: 'オーナー・大株主' }
const SITE = { name: '企業と人のつながり' }
const DATA_DATE = '2026-11-15'
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]))
const fmt = (n) => Number(n).toLocaleString('ja-JP')
const dateJa = (s) => (/^\d{4}-\d{2}-\d{2}$/.test(s || '') ? s.replace(/^(\d{4})-(\d{2})-(\d{2})$/, (_, y, m, d) => `${y}年${+m}月${+d}日`) : '')
const slug = (s) => String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60)
const STRIP = ['株式会社', '有限会社', '合同会社', '合資会社', '合名会社', '一般社団法人', '公益社団法人', '一般財団法人', '公益財団法人', '特定非営利活動法人', '医療法人社団', '医療法人財団', '医療法人', '社会福祉法人', '学校法人', '宗教法人', '協同組合', '(株)', '(有)', '(合)']
const core = (name) => {
  let s = String(name || '').normalize('NFKC').toLowerCase().replace(/ /g, '')
  let ch = true
  while (ch) {
    ch = false
    for (const t of STRIP) {
      if (s.startsWith(t) && s.length > t.length) { s = s.slice(t.length); ch = true }
      if (s.endsWith(t) && s.length > t.length) { s = s.slice(0, -t.length); ch = true }
    }
  }
  return s
}
const fnv = (k) => { let h = 2166136261; for (let i = 0; i < k.length; i++) h = Math.imul(h ^ k.charCodeAt(i), 16777619) >>> 0; return h }
const initial = (s) => esc(String(s || '?').replace(/^(株式会社|\(株\)|㈱)/, '').trim().slice(0, 1) || '?')

const CSS = `:root{--bg:#f4f6fa;--card:#fff;--fg:#18202e;--muted:#667085;--line:#e3e8ef;--accent:#2457d6;--accent2:#e8efff;--ok:#0f8a5f;--shadow:0 1px 2px rgba(16,24,40,.06),0 4px 14px rgba(16,24,40,.05)}
@media (prefers-color-scheme:dark){:root{--bg:#0e131b;--card:#161d28;--fg:#e8edf5;--muted:#96a2b4;--line:#263040;--accent:#7fb0ff;--accent2:#1d2a44;--ok:#4ad0a0;--shadow:none}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.75 system-ui,-apple-system,"Hiragino Sans","Yu Gothic UI","Meiryo",sans-serif}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--card) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top .in{max-width:960px;margin:0 auto;padding:10px 16px;display:flex;gap:14px;align-items:center}
.brand{display:flex;align-items:center;gap:9px;font-weight:800;color:var(--fg);letter-spacing:.01em;white-space:nowrap}.brand:hover{text-decoration:none}
.logo{width:30px;height:30px;border-radius:9px;background:linear-gradient(135deg,#2457d6,#7a5af8);display:grid;place-items:center;color:#fff;font-size:15px}
.top form{flex:1;display:flex;gap:8px;min-width:0}.navlink{font-weight:700;white-space:nowrap}
.ev{display:flex;gap:10px;align-items:flex-start;padding:10px 0;border-bottom:1px solid var(--line)}.ev:last-child{border-bottom:0}.ev .k{flex:none;min-width:5.6em;text-align:center;font-size:12px;font-weight:800;padding:2px 8px;border-radius:99px;background:var(--accent2);color:var(--accent)}.ev .k.hot{background:rgba(217,45,32,.12);color:#d92d20}.ev small{color:var(--muted);display:block;line-height:1.5}.tabs{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 14px}.tabs a{padding:5px 12px;border-radius:99px;background:var(--card);border:1px solid var(--line);color:var(--fg);font-size:14px}.tabs a.on{background:var(--accent);border-color:var(--accent);color:#fff}
input[type=search]{flex:1;min-width:0;font:inherit;padding:9px 14px;border:1px solid var(--line);border-radius:12px;background:var(--bg);color:var(--fg)}input[type=search]:focus{outline:2px solid var(--accent);outline-offset:1px}
button{font:inherit;padding:9px 18px;border:0;border-radius:12px;background:var(--accent);color:#fff;font-weight:700;cursor:pointer}
main{max-width:960px;margin:0 auto;padding:22px 16px 10px}
.hero{background:linear-gradient(135deg,#1c3f9e,#5b3fd0);color:#fff;border-radius:20px;padding:34px 24px;margin-bottom:20px;box-shadow:var(--shadow)}
.hero h1{margin:0 0 8px;font-size:28px;line-height:1.35}.hero p{margin:0 0 18px;opacity:.9}
.hero form{display:flex;gap:8px;max-width:560px}.hero input{background:#fff;color:#18202e;border:0;font-size:17px;padding:13px 16px}.hero button{background:#ffb938;color:#2a1c00;padding:13px 22px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}.chips span{background:rgba(255,255,255,.16);border-radius:99px;padding:3px 12px;font-size:13px}
h1.page{font-size:26px;line-height:1.35;margin:4px 0 4px}h2{font-size:18px;margin:0 0 10px}.muted{color:var(--muted);font-size:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;margin:0 0 16px;box-shadow:var(--shadow)}
.head{display:flex;gap:16px;align-items:center}.head .av{width:76px;height:76px;font-size:30px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.tile{display:flex;gap:12px;align-items:center;padding:12px;border:1px solid var(--line);border-radius:14px;background:var(--card);color:var(--fg)}.tile:hover{border-color:var(--accent);text-decoration:none}
.tile b{display:block;line-height:1.35}.tile small{color:var(--muted)}
.av{flex:none;width:44px;height:44px;border-radius:50%;background:var(--accent2);color:var(--accent);display:grid;place-items:center;font-weight:800;overflow:hidden}.av img{width:100%;height:100%;object-fit:cover;display:block}
.av.sq{border-radius:12px}
ul.list{list-style:none;padding:0;margin:0}ul.list>li{display:flex;gap:12px;align-items:center;padding:10px 0;border-bottom:1px solid var(--line)}ul.list>li:last-child{border-bottom:0}
ul.list .tx{min-width:0}ul.list small{color:var(--muted);display:block;line-height:1.5}
dl{display:grid;grid-template-columns:8.5em 1fr;gap:8px 14px;margin:0}dt{color:var(--muted)}dd{margin:0;overflow-wrap:anywhere}
.badge{display:inline-block;font-size:12px;padding:1px 9px;border-radius:99px;background:var(--accent2);color:var(--accent);margin-left:8px;vertical-align:2px;font-weight:700}
.badge.ok{background:rgba(15,138,95,.12);color:var(--ok)}
.btn{display:inline-block;padding:8px 14px;border-radius:12px;background:var(--accent2);color:var(--accent);font-weight:700}.btn:hover{text-decoration:none;filter:brightness(.97)}
.src{color:var(--muted);font-size:12.5px;margin-top:8px}
footer{max-width:960px;margin:10px auto 0;padding:18px 16px 44px;color:var(--muted);font-size:13px}footer p{margin:6px 0}
@media (max-width:560px){.hero{padding:24px 16px}.hero h1{font-size:22px}dl{grid-template-columns:1fr}dt{margin-top:6px}.head .av{width:60px;height:60px;font-size:24px}.top form button{padding:9px 12px}}`

function page({ title, desc = '', body, canonical = '', jsonld = null, noindex = false, image = '' }) {
  return `<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title><meta name="description" content="${esc(desc.slice(0, 160))}">${canonical ? `<link rel="canonical" href="${esc(canonical)}">` : ''}${noindex ? '<meta name="robots" content="noindex,follow">' : ''}
<meta property="og:title" content="${esc(title)}"><meta property="og:type" content="website">${image ? `<meta property="og:image" content="${esc(image)}">` : ''}<meta name="theme-color" content="#2457d6">
<style>${CSS}</style>${jsonld ? `<script type="application/ld+json">${JSON.stringify(jsonld).replace(/</g, '\\u003c')}</script>` : ''}</head><body>
<div class="top"><div class="in"><a class="brand" href="/"><span class="logo">∞</span>${SITE.name}</a><form action="/search" method="get" role="search"><input type="search" name="q" placeholder="会社名・人物名・法人番号" aria-label="会社名・人物名・法人番号で検索"><button>検索</button></form><a href="/events" class="navlink">出来事</a><a href="/today" class="navlink">きょうの動き</a><a href="/path" class="navlink">つながり検索</a><a href="/money" class="navlink">お金の流れ</a><a href="/vc" class="navlink">VCとLP</a></div></div>
<main>${body}</main>
<footer><p>出典: 国税庁法人番号公表サイト(<a href="https://www.houjin-bangou.nta.go.jp/" rel="noopener">https://www.houjin-bangou.nta.go.jp/</a>)のデータを加工して作成しています。このサービスの内容は、国税庁が保証したものではありません。EDINET提出者の情報は金融庁「EDINETコードリスト」によります。</p>
<p>人物の紹介文は Wikipedia(<a href="https://creativecommons.org/licenses/by-sa/4.0/deed.ja" rel="noopener">CC BY-SA 4.0</a>)、写真は Wikimedia Commons・各社の公式サイト・X などの公開された画像で、出どころは各ページに記載しています。</p>
<p>情報は公開データに基づきます。誤りや削除のご希望は、お問い合わせください。</p></footer></body></html>`
}

const evHtml = (rows) => rows.map((e) => `<div class="ev"><span class="k ${e.score >= 85 ? 'hot' : ''}">${esc(e.kind)}</span><div><a href="${esc(e.url)}" rel="noopener nofollow" target="_blank">${esc(e.title)}</a><small>${esc((e.ts || '').slice(5, 16))} ・ ${esc(e.src)}${e.num ? ` ・ <a href="/corp/${esc(e.num)}">${esc(e.company || '会社のページ')}</a>` : e.company ? ' ・ ' + esc(e.company) : ''}</small></div></div>`).join('')

function reportBox(path) {
  return `<details class="card" style="margin-top:12px"><summary style="cursor:pointer"><b>このページの誤りを知らせる</b></summary><form method="post" action="/report" style="margin-top:8px"><input type="hidden" name="page" value="${esc(path)}"><p style="margin:0 0 6px"><label>どこが違いますか(出典のURLがあれば、あわせて)<br><textarea name="text" required maxlength="1000" rows="4" style="width:100%"></textarea></label></p><p style="display:none"><input name="website" tabindex="-1" autocomplete="off"></p><button class="btn" type="submit">送る</button><span class="muted"> 個人情報は書かないでください。確認して直します。</span></form></details>`
}
function updated(extra) {
  return `<p class="src">データ更新日: ${DATA_DATE}${extra ? ' ・ ' + extra : ''}</p>`
}
export function createApp(db, opts = {}) {
  const app = new Hono()
  const origin = (c) => opts.origin || new URL(c.req.url).origin
  let statsCache = null
  const getAsset = opts.getAsset || (async () => null)
  let hotCache = null
  async function hotMap() {
    if (hotCache) return hotCache
    const t = await getAsset('/n/hot.json').catch(() => null)
    const o = t ? JSON.parse(t) : {}
    hotCache = {}
    for (const [L, arr] of Object.entries(o)) hotCache[Number(L)] = new Set(arr)
    return hotCache
  }
  // 会社ページ用の静的ファイル(法人番号 % 6000)から1社を探す
  async function shardRow(num) {
    const t = await getAsset(`/c/${Number(num) % 6000}.json`)
    if (!t) return null
    const r = JSON.parse(t).find((x) => x[0] === num)
    return r ? { num: r[0], name: r[1], kind: r[2], pref: r[3], city: r[4], street: r[5], zip: r[6], en: r[7], kana: r[8], since: r[9], upd: r[10] } : null
  }
  // 名前検索用の静的ファイル(核となる名前の頭2〜6文字)から、先頭一致で探す
  async function shardSearch(q) {
    const cq = core(q)
    const cp = Array.from(cq)
    if (cp.length < 2) return []
    const hot = await hotMap()
    let L = 2
    while (L < 6 && hot[L]?.has(cp.slice(0, L).join('')) && cp.length > L) L++
    if (cp.length < L) return []
    const t = await getAsset(`/n/${fnv(cp.slice(0, L).join('')) % 8000}.json`)
    if (!t) return []
    return JSON.parse(t).filter((r) => core(r[1]).startsWith(cq)).slice(0, 60).map((r) => ({ num: r[0], name: r[1], kind: '', pref: r[2], city: '', listed: null }))
  }

  async function stats() {
    if (statsCache) return statsCache
    const q1 = async (sql) => (await db.get(sql).catch(() => null))?.n || 0
    statsCache = {
      corps: await q1('SELECT MAX(rowid) AS n FROM corp'),
      shard: JSON.parse((await getAsset('/c/meta.json').catch(() => null)) || '{}').total || 0,
      listed: await q1("SELECT COUNT(*) AS n FROM edinet WHERE listed='上場'"),
      mapco: await q1('SELECT COUNT(*) AS n FROM mapco'),
      persons: await q1('SELECT COUNT(*) AS n FROM person'),
    }
    return statsCache
  }

  // 画像のある人を調べる(D1 は1回の問い合わせで束縛できる値が100個までなので、80個ずつ)
  async function imgMap(keys) {
    const m = new Map()
    const ks = [...new Set(keys.filter(Boolean))]
    for (let i = 0; i < ks.length; i += 80) {
      const part = ks.slice(i, i + 80)
      const rows = await db.all(`SELECT key, ext, src, url FROM img WHERE key IN (${part.map(() => '?').join(',')})`, part).catch(() => [])
      for (const r of rows) m.set(r.key, r)
    }
    return m
  }
  const avatar = (key, name, imgs, cls = '') => {
    const im = key && imgs?.get(key)
    return im ? `<span class="av ${cls}"><img src="/img/${esc(key)}.${esc(im.ext)}" alt="${esc(name)}" loading="lazy" width="96" height="96"></span>` : `<span class="av ${cls}">${initial(name)}</span>`
  }

  app.get('/', async (c) => {
    const s = await stats()
    const hotEv = await db.all("SELECT ts, src, title, url, kind, score, num, company FROM events WHERE score>=70 AND ts >= datetime('now','-2 days','localtime') ORDER BY ts DESC LIMIT 8").catch(() => [])
    const [top, listed, pers] = await Promise.all([
      db.all('SELECT slug, name, people, acq FROM mapco ORDER BY people DESC LIMIT 12').catch(() => []),
      db.all("SELECT e.num AS num, e.name AS name, e.industry AS industry, e.sec AS sec FROM edinet e WHERE e.listed='上場' AND e.num<>'' ORDER BY e.sec LIMIT 12").catch(() => []),
      db.all("SELECT p.q AS q, p.ja AS ja, p.en AS en, p.d AS d, i.ext AS ext FROM person p JOIN img i ON i.key='q-'||p.q ORDER BY p.q LIMIT 12").catch(() => []),
    ])
    const body = `<section class="hero"><h1>日本の会社と、人のつながりを調べる</h1><p>法人番号・上場企業・経営陣・買収と子会社・最近のニュースを、1か所でたどれます。</p>
<form action="/search" method="get" role="search"><input type="search" name="q" placeholder="例: トヨタ自動車 / ソニー / Apple / 孫正義" aria-label="検索"><button>検索</button></form>
<div class="chips"><span>掲載 ${fmt(Math.max(s.corps, s.shard))}社</span><span>上場 ${fmt(s.listed)}社</span><span>相関図 ${fmt(s.mapco)}社</span><span>人物 ${fmt(s.persons)}人</span></div></section>
${hotEv.length ? `<div class="card"><h2>新しい出来事</h2>${evHtml(hotEv)}<p class="src"><a href="/events">もっと見る →</a></p></div>` : ''}
<div class="card"><h2>相関図の注目会社</h2><div class="grid">${top.map((m) => `<a class="tile" href="/co/${esc(m.slug)}"><span class="av sq">${initial(m.name)}</span><span><b>${esc(m.name)}</b><small>人物 ${m.people}人 ・ 買収・子会社 ${m.acq}件</small></span></a>`).join('')}</div></div>
<div class="card"><h2>人物の例</h2><div class="grid">${pers.map((p) => `<a class="tile" href="/p/${esc(p.q)}">${avatar('q-' + p.q, p.ja || p.en, new Map([['q-' + p.q, { ext: p.ext }]]))}<span><b>${esc(p.ja || p.en)}</b><small>${esc(p.d || '')}</small></span></a>`).join('')}</div></div>
<div class="card"><h2>上場企業の例</h2><div class="grid">${listed.map((r) => `<a class="tile" href="/corp/${esc(r.num)}"><span class="av sq">${initial(r.name)}</span><span><b>${esc(r.name)}</b><small>${esc(r.industry)} ・ ${esc((r.sec || '').slice(0, 4))}</small></span></a>`).join('')}</div></div>
<p class="muted">日本の現存する法人(約506万社)のうち、現在 ${fmt(Math.max(s.corps, s.shard))}社を掲載しています(日本の全法人。会社名の先頭からの検索と、法人番号ページに対応)。</p>`
    return c.html(page({ title: `${SITE.name} | 日本の会社と、人のつながりを調べる`, desc: '日本の法人を会社名・法人番号で検索。上場企業の情報、経営陣、買収・子会社、最近のニュースも。', body, canonical: origin(c) + '/' }))
  })

  app.get('/search', async (c) => {
    const q = (c.req.query('q') || '').trim().slice(0, 60)
    if (/^\d{13}$/.test(q)) return c.redirect('/corp/' + q, 302)
    let rows = [], mc = [], ps = []
    if (q.length >= 2) {
      mc = await db.all('SELECT slug, name, people, acq FROM mapco WHERE name LIKE ? OR name LIKE ? LIMIT 20', [q + '%', '%' + q + '%']).catch(() => [])
      const ca = await db.all('SELECT m.slug AS slug, m.name AS name, m.people AS people, m.acq AS acq FROM company_alias a JOIN mapco m ON m.slug = a.slug WHERE a.alias LIKE ? LIMIT 5', [q + '%']).catch(() => [])
      mc = [...ca, ...mc.filter((x) => !ca.some((y) => y.slug === x.slug))]
      ps = await db.all('SELECT q, ja, en, d FROM person WHERE ja LIKE ? OR en LIKE ? OR ja LIKE ? LIMIT 20', [q + '%', q + '%', '%' + q + '%']).catch(() => [])
      const pa = await db.all('SELECT p.q AS q, p.ja AS ja, p.en AS en, p.d AS d FROM person_alias a JOIN person p ON p.q = a.q WHERE a.alias LIKE ? LIMIT 10', ['%' + q + '%']).catch(() => [])
      for (const x of pa) if (!ps.some((y) => y.q === x.q)) ps.push(x)
      const seen = new Set()
      const SUF = ['', '株式会社', '有限会社', '合同会社']
      const exact = [...new Set(SUF.flatMap((x) => [q + x, x + q]))]
      const sel = 'SELECT c.num AS num, c.name AS name, c.kind AS kind, c.pref AS pref, c.city AS city, e.listed AS listed FROM corp c LEFT JOIN edinet e ON e.num=c.num'
      const r1 = await db.all(`${sel} WHERE c.name IN (${exact.map(() => '?').join(',')})`, exact)
      const r2 = await db.all('SELECT c.num AS num, c.name AS name, c.kind AS kind, c.pref AS pref, c.city AS city, e.listed AS listed FROM edinet e JOIN corp c ON c.num=e.num WHERE e.name LIKE ? OR e.name LIKE ? LIMIT 30', [q + '%', '%' + q + '%'])
      for (const x of [...r1, ...r2]) if (!seen.has(x.num)) { seen.add(x.num); rows.push(x) }
      for (const p of [q, '株式会社' + q, '有限会社' + q, '合同会社' + q, '一般社団法人' + q]) {
        const r = await db.all(`${sel} WHERE c.name>=? AND c.name<? LIMIT 60`, [p, p + '\uffff'])
        for (const x of r) if (!seen.has(x.num)) { seen.add(x.num); rows.push(x) }
        if (rows.length >= 120) break
      }
      const exactSet = new Set(exact)
      rows.sort((a, b) => ((b.listed === '上場') - (a.listed === '上場')) || (exactSet.has(b.name) - exactSet.has(a.name)) || a.name.length - b.name.length)
      for (const x of await shardSearch(q).catch(() => [])) if (!seen.has(x.num)) { seen.add(x.num); rows.push(x) }
      rows = rows.slice(0, 50)
    }
    const imgs = await imgMap(ps.map((p) => 'q-' + p.q))
    const li = (href, av, name, badge, sub) => `<li><a href="${href}">${av}</a><div class="tx"><a href="${href}"><b>${esc(name)}</b></a>${badge}<small>${sub}</small></div></li>`
    const none = !mc.length && !ps.length && !rows.length
    const body = `<h1 class="page">「${esc(q)}」の検索結果</h1><div class="card">${q.length < 2 ? '<p>2文字以上で入力してください。</p>' : none ? '<p>見つかりませんでした。社名や人物名の先頭からの一致で探しています。</p>' : `<ul class="list">${[
      ...mc.map((m) => li(`/co/${esc(m.slug)}`, `<span class="av sq">${initial(m.name)}</span>`, m.name, '<span class="badge">相関図</span>', `人物 ${m.people}人 ・ 買収・子会社 ${m.acq}件`)),
      ...ps.map((p) => li(`/p/${esc(p.q)}`, avatar('q-' + p.q, p.ja || p.en, imgs), p.ja || p.en, '<span class="badge">人物</span>', esc(p.d || ''))),
      ...rows.map((r) => li(`/corp/${esc(r.num)}`, `<span class="av sq">${initial(r.name)}</span>`, r.name, r.listed === '上場' ? '<span class="badge ok">上場</span>' : '', `${esc(KIND[r.kind] || '')}${r.kind ? ' ・ ' : ''}${esc(r.pref)}${esc(r.city)}`)),
    ].join('')}</ul>`}</div>`
    return c.html(page({ title: `「${q}」の検索結果 | ${SITE.name}`, body, noindex: true }))
  })

  app.get('/corp/:num', async (c) => {
    const num = c.req.param('num')
    if (!/^\d{13}$/.test(num)) return c.notFound()
    const r = (await db.get('SELECT * FROM corp WHERE num=?', [num]).catch(() => null)) || (await shardRow(num).catch(() => null))
    if (!r) return c.html(page({ title: '見つかりません', body: '<div class="card"><h1 class="page">見つかりません</h1><p>この法人番号は、掲載している法人にありません(閉鎖・合併などの可能性があります)。</p></div>', noindex: true }), 404)
    const [e, mcp] = await Promise.all([db.get('SELECT * FROM edinet WHERE num=?', [num]).catch(() => null), db.get('SELECT slug, name FROM mapco WHERE num=?', [num]).catch(() => null)])
    const evs = await db.all('SELECT ts, src, title, url, kind, score, num, company FROM events WHERE num=? ORDER BY ts DESC LIMIT 10', [num]).catch(() => [])
    const [near, people, news, acqs] = await Promise.all([
      db.all('SELECT num, name FROM corp WHERE pref=? AND city=? AND num<>? ORDER BY since DESC LIMIT 8', [r.pref, r.city, num]),
      db.all("SELECT name, en, role, since, until FROM rel_people WHERE num=? ORDER BY (until<>'') , since LIMIT 60", [num]).catch(() => []),
      db.all('SELECT d, title, url, media FROM rel_news WHERE num=? ORDER BY d DESC LIMIT 8', [num]).catch(() => []),
      mcp ? db.all('SELECT year, target, amount, note FROM mapco_acq WHERE slug=? ORDER BY year DESC LIMIT 20', [mcp.slug]).catch(() => []) : [],
    ])
    const imgs = await imgMap(people.map((x) => 'm-' + slug(x.en)))
    const addr = `${r.pref}${r.city}${r.street}`
    const rows = [
      ['法人番号', r.num], ['商号又は名称', r.name], r.en && ['英語表記', r.en], r.kana && ['フリガナ', r.kana], ['種別', KIND[r.kind] || r.kind],
      ['所在地', (r.zip ? `〒${r.zip.replace(/^(\d{3})(\d{4})$/, '$1-$2')} ` : '') + addr], r.since && ['法人番号の指定', dateJa(r.since)], r.upd && ['最終更新', dateJa(r.upd)],
      e && ['EDINET', `${e.kind}${e.listed ? '(' + e.listed + ')' : ''}${e.sec ? ' ・ 証券コード ' + e.sec.slice(0, 4) : ''}`], e && e.industry && ['業種', e.industry],
    ].filter(Boolean)
    const roleTx = (x) => `${esc(x.role || '')}${x.since ? (/創業者/.test(x.role || '') ? ` ・ ${esc(x.since)}年創業` : ` ・ ${esc(x.since)}年〜${x.until ? esc(x.until) + '年' : '現在'}`) : ''}`
    const body = `<div class="card head"><span class="av sq">${initial(r.name)}</span><div><h1 class="page">${esc(r.name)}${e && e.listed === '上場' ? '<span class="badge ok">上場</span>' : ''}</h1><p class="muted" style="margin:0">${esc(KIND[r.kind] || '')} ・ ${esc(addr)}</p></div></div>
${mcp ? `<p><a class="btn" href="/co/${esc(mcp.slug)}">相関図のページを見る(人物・買収・子会社・ニュース) →</a></p>` : ''}
<div class="card"><h2>法人情報</h2><dl>${rows.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl><p class="src"><a href="https://www.houjin-bangou.nta.go.jp/henkorireki-johoto.html?selHouzinNo=${esc(num)}" rel="noopener nofollow">国税庁 法人番号公表サイトで見る ↗</a></p></div>
${evs.length ? `<div class="card"><h2>最近の出来事</h2>${evHtml(evs)}<p class="src"><a href="/events">すべての出来事を見る →</a></p></div>` : ''}
${acqs.length ? `<div class="card"><h2>買収・子会社</h2><ul class="list">${acqs.map((a) => `<li><div class="tx">${esc(a.target)}<small>${esc(a.year)}年${a.amount ? ' ・ ' + esc(a.amount) : ''}${a.note ? ' ・ ' + esc(a.note) : ''}</small></div></li>`).join('')}</ul></div>` : ''}
${people.length ? `<div class="card"><h2>人物(経営陣・創業者など)</h2><ul class="list">${people.map((x) => `<li>${avatar('m-' + slug(x.en), x.name, imgs)}<div class="tx"><b>${esc(x.name)}</b>${x.en ? ` <span class="muted">(${esc(x.en)})</span>` : ''}<small>${roleTx(x)}</small></div></li>`).join('')}</ul><p class="src">公開情報をもとに集めた記録です。誤りは、お問い合わせください。</p></div>` : ''}
${news.length ? `<div class="card"><h2>最近のニュース</h2><ul class="list">${news.map((x) => `<li><div class="tx"><a href="${esc(x.url)}" rel="noopener nofollow" target="_blank">${esc(x.title)}</a><small>${esc(x.d)} ・ ${esc(x.media)}</small></div></li>`).join('')}</ul><p class="src">見出しと出典へのリンクのみ。内容は各サイトでご確認ください。</p></div>` : ''}
${near.length ? `<div class="card"><h2>同じ市区町村の法人(新しい順)</h2><ul class="list">${near.map((n) => `<li><span class="av sq">${initial(n.name)}</span><div class="tx"><a href="/corp/${esc(n.num)}">${esc(n.name)}</a></div></li>`).join('')}</ul></div>` : ''}`
    const jsonld = { '@context': 'https://schema.org', '@type': 'Organization', name: r.name, identifier: r.num, address: { '@type': 'PostalAddress', addressRegion: r.pref, addressLocality: r.city, streetAddress: r.street, postalCode: r.zip, addressCountry: 'JP' } }
    return c.html(page({ title: `${r.name}(法人番号 ${r.num}) | ${SITE.name}`, desc: `${r.name}の法人情報。${addr}。${KIND[r.kind] || ''}。`, body, canonical: `${origin(c)}/corp/${num}`, jsonld }))
  })

  app.get('/co/:slug', async (c) => {
    const sl = c.req.param('slug')
    if (!/^[A-Za-z0-9_\-]{1,60}$/.test(sl)) return c.notFound()
    const m = await db.get('SELECT * FROM mapco WHERE slug=?', [sl])
    if (!m) return c.html(page({ title: '見つかりません', body: '<div class="card"><h1 class="page">見つかりません</h1></div>', noindex: true }), 404)
    const [people, news, acq, corp] = await Promise.all([
      db.all("SELECT name, en, role, since, until, note, q FROM mapco_people WHERE slug=? ORDER BY (until<>'') , since LIMIT 80", [sl]),
      db.all('SELECT d, title, url, media FROM mapco_news WHERE slug=? ORDER BY d DESC LIMIT 8', [sl]),
      db.all('SELECT year, target, amount, note FROM mapco_acq WHERE slug=? ORDER BY year DESC LIMIT 60', [sl]),
      m.num ? db.get('SELECT num, name, pref, city FROM corp WHERE num=?', [m.num]).catch(() => null) : null,
    ])
    const pnames = [...new Set(people.filter((x) => !x.until).flatMap((x) => [x.en, x.name]).filter(Boolean))].slice(0, 90)
    const pfeed = pnames.length ? await db.all(`SELECT ts, src, title, url, kind, company FROM events WHERE kind IN ('発信(X)','出演(YouTube)','発信(YouTube)') AND company IN (${pnames.map(() => '?').join(',')}) ORDER BY ts DESC LIMIT 8`, pnames).catch(() => []) : []
    const money = await db.all('SELECT src, dst, kind, label, year, amount, note, url, media FROM money_flow WHERE dst=? OR src=? ORDER BY year DESC LIMIT 40', [m.name, m.name]).catch(() => [])
    const facts = await db.all('SELECT sec, text, url FROM company_fact WHERE slug=? ORDER BY ord', [sl]).catch(() => [])
    const imgs = await imgMap(people.map((x) => 'm-' + slug(x.en)))
    const moves = people.flatMap((x) => [x.since && !(String(x.since) === '2026' && /公式ページ|確認できていません/.test(x.note || '')) && { y: x.since, kind: '就任', name: x.name, role: x.role }, x.until && { y: x.until, kind: '退任', name: x.name, role: x.role }].filter(Boolean)).filter((x) => /^\d{4}$/.test(String(x.y))).sort((a, b) => String(b.y).localeCompare(String(a.y))).slice(0, 14)
    const roleTx = (x) => `${esc(x.role || '')}${x.since ? ` ・ ${esc(x.since)}年〜${x.until ? esc(x.until) + '年' : '現在'}` : ''}`
    const body = `<div class="card head"><span class="av sq">${initial(m.name)}</span><div><h1 class="page">${esc(m.name)}</h1><p class="muted" style="margin:0">相関図の記録 ・ 人物 ${people.length}人 ・ 買収・子会社 ${acq.length}件</p></div></div>
${corp ? `<p><a class="btn" href="/corp/${esc(corp.num)}">法人情報(法人番号 ${esc(corp.num)}・${esc(corp.pref)}${esc(corp.city)})を見る →</a></p>` : ''}
${m.note ? `<div class="card"><p style="margin:0">${esc(m.note)}</p></div>` : ''}
${facts.length ? `<div class="card"><h2>くわしく(出典つき)</h2>${[...new Set(facts.map((f) => f.sec))].map((sec) => `<h3 style="margin:12px 0 4px;font-size:1rem">${esc(sec)}</h3><ul class="list">${facts.filter((f) => f.sec === sec).map((f) => `<li><div class="tx">${esc(f.text)}<small><a href="${esc(f.url)}" rel="noopener nofollow" target="_blank">出典 ↗</a></small></div></li>`).join('')}</ul>`).join('')}<p class="src">出典に書かれている事実だけを載せています。数字は、各出典の時点のものです。</p></div>` : ''}
${people.length ? `<div class="card"><h2>人物(経営陣・創業者・出資者など)</h2><ul class="list">${people.map((x) => `<li>${avatar('m-' + slug(x.en), x.name, imgs)}<div class="tx"><b>${x.q ? `<a href="/p/${esc(x.q)}">${esc(x.name)}</a>` : esc(x.name)}</b>${x.en ? ` <span class="muted">(${esc(x.en)})</span>` : ''}<small>${roleTx(x)}</small></div></li>`).join('')}</ul></div>` : ''}
${pfeed.length ? `<div class="card"><h2>人物の最近の発信・出演</h2>${evHtml(pfeed.map((f) => ({ ...f, title: (f.company ? f.company + ': ' : '') + String(f.title).split(': ').slice(1).join(': '), company: '', num: '', score: 0 })))}<p class="src">直近2週間ほどの、見出し・投稿の抜粋と出典へのリンクのみ。</p></div>` : ''}
${moves.length ? `<div class="card"><h2>人の動き(就任・退任)</h2><ul class="list">${moves.map((x) => `<li><div class="tx"><b>${esc(x.y)}年</b> <span class="badge">${x.kind}</span> <b>${esc(x.name)}</b><small>${esc(x.role || '')}</small></div></li>`).join('')}</ul><p class="src">この会社の人物の記録(就任年・退任年)から並べています。記録のある範囲です。</p></div>` : ''}
${money.length ? `<div class="card"><h2>お金の流れ(出資・資金調達)</h2><ul class="list">${money.map((r) => `<li><div class="tx"><b>${esc(r.src)}</b> → <b>${esc(r.dst)}</b> <span class="badge">${esc(r.kind)}</span>${r.label ? ' ' + esc(r.label) : ''}${r.amount ? ' <b>' + esc(r.amount) + '</b>' : ''}<small>${esc(r.year || '')}${r.url ? ` ・ <a href="${esc(r.url)}" rel="noopener nofollow" target="_blank">${esc(r.media || '出典')}</a>` : (r.note ? ' ・ ' + esc(r.note) : '')}</small></div></li>`).join('')}</ul><p class="src"><a href="/money">お金の流れ全体を見る →</a></p></div>` : ''}
${acq.length ? `<div class="card"><h2>買収・子会社</h2><ul class="list">${acq.map((a) => `<li><div class="tx">${esc(a.target)}<small>${esc(a.year)}年${a.amount ? ' ・ ' + esc(a.amount) : ''}${a.note ? ' ・ ' + esc(a.note) : ''}</small></div></li>`).join('')}</ul></div>` : ''}
${news.length ? `<div class="card"><h2>最近のニュース</h2><ul class="list">${news.map((x) => `<li><div class="tx"><a href="${esc(x.url)}" rel="noopener nofollow" target="_blank">${esc(x.title)}</a><small>${esc(x.d)} ・ ${esc(x.media)}</small></div></li>`).join('')}</ul><p class="src">見出しと出典へのリンクのみ。内容は各サイトでご確認ください。</p></div>` : ''}
<p class="src">出どころ: 公開情報(Wikipedia・Wikidata・各社の公式発表・報道など)をもとに集めた記録です。誤りや削除のご希望は、下のフォームからお知らせください。</p>${updated('公開情報をもとにした記録')}<p class="src"><a href="/feed/co/${esc(sl)}.xml">この会社の動きをRSSで購読</a> ・ <a href="/path">つながり検索</a></p>${reportBox('/co/' + sl)}`
    return c.html(page({ title: `${m.name}の人物・買収・子会社 | ${SITE.name}`, desc: `${m.name}の経営陣・創業者・出資者と、買収・子会社、最近のニュース。`, body, canonical: `${origin(c)}/co/${sl}` }))
  })

  const personPage = async (c, mode) => {
    const q = c.req.param('q')
    if (!/^\d{1,12}$/.test(q)) return c.notFound()
    const p = await db.get('SELECT * FROM person WHERE q=?', [q]).catch(() => null)
    if (!p) return c.html(page({ title: '見つかりません', body: '<div class="card"><h1 class="page">見つかりません</h1></div>', noindex: true }), 404)
    const [soc, quotes, feed] = await Promise.all([
      db.get('SELECT x, ig, yt, web FROM person_social WHERE q=?', [q]).catch(() => null),
      db.all('SELECT w, t, text FROM person_quote WHERE q=? LIMIT 6', [q]).catch(() => []),
      db.all('SELECT ts, src, title, url, kind FROM person_feed WHERE q=? ORDER BY ts DESC LIMIT 8', [q]).catch(() => []),
    ])
    const srcs = await db.all('SELECT label, url FROM person_src WHERE q=?', [q]).catch(() => [])
    const [relp, tl, chk] = await Promise.all([
      db.all('SELECT r.rq AS rq, r.rel AS rel, p.ja AS ja, p.en AS en, p.d AS d FROM person_rel r LEFT JOIN person p ON p.q=r.rq WHERE r.q=? ORDER BY r.rel', [q]).catch(() => []),
      db.all('SELECT y, y2, kind, label, ref FROM person_timeline WHERE q=? ORDER BY CASE WHEN y IS NULL THEN 1 ELSE 0 END, y', [q]).catch(() => []),
      db.get('SELECT grp, checked_at FROM top100 WHERE q=?', [q]).catch(() => null),
    ])
    const roles = await db.all('SELECT company, role FROM person_role WHERE q=?', [q])
    const mcs = new Map()
    for (const r of roles) {
      const m = await db.get('SELECT slug FROM mapco WHERE name=? LIMIT 1', [r.company]).catch(() => null)
      if (m) mcs.set(r.company, m.slug)
    }
    const imgs = await imgMap(['q-' + q, ...relp.map((x) => 'q-' + x.rq)])
    const im = imgs.get('q-' + q)
    const name = p.ja || p.en
    const wl = p.t && p.w ? `https://${p.w}.wikipedia.org/wiki/${encodeURIComponent(p.t)}` : ''
    const imgSrc = im ? (/^https?:/.test(im.url || '') ? im.url : '') : ''
    const posts = mode === 'posts'
    const tabsHtml = `<nav class="tabs" style="display:flex;gap:8px;margin:0 0 12px"><a class="btn" ${posts ? '' : 'aria-current="page" style="font-weight:700"'} href="/p/${q}">プロフィール<small> (Wikipedia・Wikidata)</small></a><a class="btn" ${posts ? 'aria-current="page" style="font-weight:700"' : ''} href="/p/${q}/posts">発信・SNS<small> (X・YouTubeなど)</small></a></nav>`
    const body = `<div class="card head">${avatar('q-' + q, name, imgs)}<div><h1 class="page">${esc(name)}${chk ? '<span class="badge ok">確認済み</span>' : ''}</h1><p class="muted" style="margin:0">${p.ja && p.en ? esc(p.en) + (p.d ? ' ・ ' : '') : ''}${esc(p.d || '')}</p></div></div>
${tabsHtml}
${chk ? `<p class="src" style="margin-top:-6px">注目の100人 ・ 確認日 ${esc(chk.checked_at)} ・ 出典は各項目に記載 ・ <a href="/trust">確認の基準と状況</a></p>` : ''}
${!posts && p.intro ? `<div class="card"><h2>紹介</h2><p style="margin:0">${esc(p.intro)}</p><p class="src">出どころ: ${p.w === 'x' ? `本人のXのプロフィールと、下の出典のページ(Wikipediaに記事がないため、確認できた事実だけを書いています)` : `${wl ? `<a href="${esc(wl)}" rel="noopener nofollow" target="_blank">Wikipedia(${p.w === 'ja' ? '日本語版' : '英語版'})「${esc(p.t)}」</a>` : 'Wikipedia'}の冒頭(<a href="https://creativecommons.org/licenses/by-sa/4.0/deed.ja" rel="noopener">CC BY-SA 4.0</a>)`}</p></div>` : ''}
${!posts && srcs.length ? `<div class="card"><h2>出典</h2><ul class="list">${srcs.map((x) => `<li><div class="tx"><a href="${esc(x.url)}" rel="noopener nofollow" target="_blank">${esc(x.label)}</a></div></li>`).join('')}</ul></div>` : ''}
${!posts && relp.length ? `<div class="card"><h2>関係する人物</h2><ul class="list">${relp.map((x) => `<li>${avatar('q-' + x.rq, x.ja || x.en || '', imgs)}<div class="tx"><a href="/p/${esc(x.rq)}"><b>${esc(x.ja || x.en || 'Q' + x.rq)}</b></a><span class="badge">${esc(x.rel)}</span><small>${esc(x.d || '')}</small></div></li>`).join('')}</ul><p class="src">出典: <a href="https://www.wikidata.org/wiki/Q${esc(q)}" rel="noopener nofollow" target="_blank">Wikidata</a>に記録された関係(配偶者・兄弟姉妹・共同創業者)。親や子は載せていません。</p></div>` : ''}
${!posts && tl.length ? `<div class="card"><h2>年表</h2><ul class="list">${tl.map((t) => `<li><div class="tx"><b>${t.y ? esc(t.y) + (t.y2 ? '〜' + esc(t.y2) : '') + '年' : '年不明'}</b> <span class="badge">${esc(t.kind)}</span> ${esc(t.label)}${t.ref ? '' : ' <span class="muted">(出典なし)</span>'}</div></li>`).join('')}</ul><p class="src">出典: <a href="https://www.wikidata.org/wiki/Q${esc(q)}" rel="noopener nofollow" target="_blank">Wikidata</a>の記録。「出典なし」は、Wikidata上で出典が付いていない項目です。</p></div>` : ''}
${posts && !(soc && (soc.x || soc.ig || soc.yt || soc.web)) && !feed.length ? '<div class="card"><p class="muted" style="margin:0">本人確認できたSNSと、最近の発信は、まだ登録がありません。</p></div>' : ''}
${posts && soc && (soc.x || soc.ig || soc.yt || soc.web) ? `<div class="card"><h2>SNS・公式サイト</h2><p style="margin:0">${[soc.x && `<a class="btn" href="https://x.com/${esc(soc.x)}" rel="noopener nofollow" target="_blank">X @${esc(soc.x)}</a>`, soc.ig && `<a class="btn" href="https://www.instagram.com/${esc(soc.ig)}/" rel="noopener nofollow" target="_blank">Instagram @${esc(soc.ig)}</a>`, soc.yt && `<a class="btn" href="https://www.youtube.com/channel/${esc(soc.yt)}" rel="noopener nofollow" target="_blank">YouTube</a>`, soc.web && `<a class="btn" href="${esc(/^https?:/.test(soc.web) ? soc.web : 'https://' + soc.web)}" rel="noopener nofollow" target="_blank">公式サイト</a>`].filter(Boolean).join(' ')}</p><p class="src">${chk ? 'Xは、表示名とプロフィールを見て、本人のものと確認したアカウントです。YouTube・Instagram・公式サイトは、Wikidataに登録されているものです(本人のものかどうかは、各サービスでご確認ください)。' : 'Wikidataに登録されているアカウントです。本人のものかどうかは、各サービスでご確認ください。'}</p></div>` : ''}
${posts && feed.length ? `<div class="card"><h2>最近の発信・出演</h2>${evHtml(feed.map((f) => ({ ...f, company: '', num: '', score: 0 })))}<p class="src">見出し・投稿の抜粋と出典へのリンクのみ。X・YouTubeの確認は、定期的に行っています(常時ではありません)。</p></div>` : ''}
${!posts && quotes.length ? `<div class="card"><h2>名言</h2><ul class="list">${quotes.map((x) => `<li><div class="tx">${esc(x.text)}</div></li>`).join('')}</ul><p class="src">出典: <a href="https://${esc(quotes[0].w)}.wikiquote.org/wiki/${encodeURIComponent(quotes[0].t)}" rel="noopener nofollow" target="_blank">Wikiquote「${esc(quotes[0].t)}」</a>(<a href="https://creativecommons.org/licenses/by-sa/4.0/deed.ja" rel="noopener">CC BY-SA 4.0</a>)。引用の正確さは、出典のページでご確認ください。</p></div>` : ''}
${!posts && roles.length ? `<div class="card"><h2>関わった会社</h2><ul class="list">${roles.map((r) => `<li><span class="av sq">${initial(r.company)}</span><div class="tx">${mcs.has(r.company) ? `<a href="/co/${esc(mcs.get(r.company))}"><b>${esc(r.company)}</b></a>` : `<b>${esc(r.company)}</b>`}<small>${esc(WPRL[r.role] || r.role)}</small></div></li>`).join('')}</ul></div>` : ''}
<p class="src">${im ? `写真: ${imgSrc ? `<a href="${esc(imgSrc)}" rel="noopener nofollow" target="_blank">${esc(im.src)}</a>` : esc(im.src)}。` : ''}${Number(q) < 900000000 ? `<a href="https://www.wikidata.org/wiki/Q${esc(q)}" rel="noopener nofollow" target="_blank">Wikidata ↗</a>` : 'Wikidataに項目がないため、出典を各項目に記載しています'}</p>
${updated(chk ? '確認日 ' + esc(chk.checked_at) : '')}<p class="src"><a href="/feed/p/${esc(q)}.xml">この人の発信・出演をRSSで購読</a> ・ <a href="/path?a=${encodeURIComponent(name)}">この人とのつながりを調べる</a></p>${reportBox('/p/' + q + (posts ? '/posts' : ''))}`
    const jsonld = { '@context': 'https://schema.org', '@type': 'Person', name, alternateName: p.en, description: p.d }
    return c.html(page({ title: posts ? `${name}の発信・SNS | ${SITE.name}` : `${name}(${p.en}) | ${SITE.name}`, desc: posts ? `${name}のX・YouTubeなどの最近の発信と、公式SNS。` : `${name}の紹介と、関わった会社。${p.d || ''}`, body, canonical: `${origin(c)}/p/${q}${posts ? '/posts' : ''}`, jsonld, image: im ? `${origin(c)}/img/q-${q}.${im.ext}` : '' }))
  }
  app.get('/p/:q', (c) => personPage(c, 'profile'))
  app.get('/p/:q/posts', (c) => personPage(c, 'posts'))

  app.post('/report', async (c) => {
    const o = c.req.header('origin') || ''
    if (o && new URL(o).host !== new URL(c.req.url).host) return c.text('forbidden', 403)
    const f = await c.req.parseBody()
    const text = String(f.text || '').trim().slice(0, 1000)
    const pg = String(f.page || '').slice(0, 200)
    if (f.website || !text || !/^\/[\w\-\/]*$/.test(pg)) return c.html(page({ title: '送れませんでした', body: `<div class="card"><p>内容を確認して、もう一度お試しください。</p></div>`, noindex: true }), 400)
    if (db.run) {
      const n = await db.get("SELECT count(*) AS n FROM reports WHERE ts > ?", [new Date(Date.now() - 86400000).toISOString()]).catch(() => null)
      if (n && n.n > 300) return c.text('混み合っています。時間をおいてお試しください。', 429)
      await db.run('INSERT INTO reports (ts, page, text) VALUES (?,?,?)', [new Date().toISOString(), pg, text]).catch(() => null)
    }
    return c.html(page({ title: '受け付けました', body: `<div class="card"><h1 class="page">ありがとうございます</h1><p>内容を確認して、必要なら直します。</p><p><a class="btn" href="${esc(pg)}">元のページへ戻る</a></p></div>`, noindex: true }))
  })

  app.get('/admin/reports', async (c) => {
    const key = c.req.query('key') || ''
    const want = (c.env && c.env.ADMIN_KEY) || (typeof process !== 'undefined' && process.env && process.env.ADMIN_KEY) || ''
    if (!want || key.length !== want.length || key !== want) return c.text('not found', 404)
    const rows = await db.all('SELECT id, ts, page, text FROM reports ORDER BY id DESC LIMIT 200').catch(() => [])
    const body = `<div class="card"><h1 class="page">誤りの指摘(${rows.length}件)</h1><ul class="list">${rows.map((r) => `<li><div class="tx"><a href="${esc(r.page)}" target="_blank">${esc(r.page)}</a> <small>${esc(r.ts)} ・ #${r.id}</small><div style="white-space:pre-wrap">${esc(r.text)}</div></div></li>`).join('') || '<li>まだありません</li>'}</ul></div>`
    c.header('Referrer-Policy', 'no-referrer')
    return c.html(page({ title: '誤りの指摘(管理)', body, noindex: true }))
  })

  app.get('/investor', async (c) => {
    const n = String(c.req.query('n') || '').trim().slice(0, 80)
    if (!n) return c.redirect('/money')
    const rows = await db.all("SELECT dst, kind, label, year, amount, note, url, media FROM money_flow WHERE src=? AND kind <> '大株主' ORDER BY year DESC, dst LIMIT 300", [n]).catch(() => [])
    const from = await db.all("SELECT src, kind, label, year, amount, url, media FROM money_flow WHERE dst=? AND kind <> '大株主' ORDER BY year DESC, src LIMIT 100", [n]).catch(() => [])
    const link = (x) => `<a href="/investor?n=${encodeURIComponent(x)}">${esc(x)}</a>`
    const li = (r, who, name) => `<li><div class="tx"><b>${link(name)}</b> <span class="badge">${esc(r.kind)}</span>${r.label ? ' ' + esc(r.label) : ''}${r.amount ? ' <b>' + esc(r.amount) + '</b>' : ''}<small>${esc(r.year || '')}${r.url ? ` ・ <a href="${esc(r.url)}" rel="noopener nofollow" target="_blank">${esc(r.media || '出典')}</a>` : (r.note ? ' ・ ' + esc(r.note) : '')}</small></div></li>`
    const body = `<h1 class="page">${esc(n)}</h1><p class="muted">この名前の、出資・投資と、資金を受けた記録です。 <a href="/money">お金の流れ</a> ・ <a href="/vc">VCのファンド規模とLP</a> ・ <a href="/path?a=${encodeURIComponent(n)}">つながり検索</a></p>
${rows.length ? `<div class="card"><h2>出資・投資した先(${rows.length}件)</h2><ul class="list">${rows.map((r) => li(r, 'dst', r.dst)).join('')}</ul></div>` : ''}
${from.length ? `<div class="card"><h2>資金を受けた記録</h2><ul class="list">${from.map((r) => li(r, 'src', r.src)).join('')}</ul></div>` : ''}
${!rows.length && !from.length ? '<div class="card"><p>この名前の記録は、まだありません。</p></div>' : ''}${updated('')}${reportBox('/investor')}`
    return c.html(page({ title: `${n}の出資・投資 | ${SITE.name}`, desc: `${n}の出資先と、資金調達の記録。`, body, canonical: `${origin(c)}/investor?n=${encodeURIComponent(n)}`, noindex: !rows.length && !from.length }))
  })

  app.get('/money', async (c) => {
    const [ai, yc, rounds, inv, big, top] = await Promise.all([
      db.all("SELECT src, dst, kind, label, url FROM money_flow WHERE media LIKE '相関図%' ORDER BY kind, src LIMIT 60").catch(() => []),
      db.get("SELECT count(*) AS n FROM money_flow WHERE kind='出資(YC)'").catch(() => null),
      db.all("SELECT src, dst, label, amount, note, url, media, d FROM money_flow WHERE kind='資金調達' ORDER BY d DESC, dst LIMIT 160").catch(() => []),
      db.all("SELECT src, dst, label, year, note FROM money_flow WHERE kind='出資' ORDER BY year DESC, src LIMIT 200").catch(() => []),
      db.all("SELECT src, dst, label, note FROM money_flow WHERE kind='大株主' ORDER BY dst LIMIT 200").catch(() => []),
      db.all("SELECT src, count(*) AS n FROM money_flow WHERE kind IN ('出資','資金調達') GROUP BY src ORDER BY n DESC, src LIMIT 15").catch(() => []),
    ])
    const grp = new Map()
    for (const r of rounds) {
      const k = r.dst + '|' + r.d + '|' + r.url
      if (!grp.has(k)) grp.set(k, { ...r, srcs: [] })
      grp.get(k).srcs.push(r.src)
    }
    const link = (n) => `<a href="/investor?n=${encodeURIComponent(n)}">${esc(n)}</a>`
    const body = `<h1 class="page">お金の流れ</h1><p class="muted">誰が、どの会社に出資しているか。相関図の記録と、資金調達の報道から集めています。</p>
<div class="card"><h2>最近の資金調達(出資者が報じられたもの)</h2><ul class="list">${[...grp.values()].map((g) => `<li><div class="tx"><b>${link(g.dst)}</b> ${g.label ? `<span class="badge">${esc(g.label)}</span>` : ''}${g.amount ? ` <b>${esc(g.amount)}</b>` : ''}<small>出資: ${g.srcs.map(link).join('、')} ・ ${esc(g.d)} ・ <a href="${esc(g.url)}" rel="noopener nofollow" target="_blank">${esc(g.media || '出典')}</a></small></div></li>`).join('') || '<li>まだありません</li>'}</ul><p class="src">報道の見出しに出資者が書かれたものだけです。金額・出資者は、出典でご確認ください。</p></div>
${ai.length ? `<div class="card"><h2>AI企業のお金の循環(出資と支払い)</h2><ul class="list">${ai.map((r) => `<li><div class="tx"><b>${link(r.src)}</b> → <b>${link(r.dst)}</b> <span class="badge">${esc(r.kind)}</span> ${esc(r.label || '')}</div></li>`).join('')}</ul><p class="src">出資は青、支払いは金色の光の粒で流れる図は、<a href="${esc(ai[0].url)}" rel="noopener" target="_blank">相関図のページ</a>で見られます。金額は契約の上限や報道ベースを含みます(2026年11月13日時点)。</p></div>` : ''}
${yc && yc.n ? `<div class="card"><h2>Y Combinatorの出資先</h2><p style="margin:0">${link('Y Combinator')}が出資した${yc.n.toLocaleString()}社を、会社ごとのページとつながり検索で使えます。出典: <a href="https://www.ycombinator.com/companies" rel="noopener nofollow" target="_blank">YC公式の企業一覧</a>。</p></div>` : ''}
<div class="card"><h2>出資・投資をしている主なところ</h2><p style="margin:0">${top.map((t) => `${link(t.src)}(${t.n})`).join(' ・ ')}</p><p class="src" style="margin-top:8px">VCが集めたファンドの規模と、公表されたLP(出資者)は、<a href="/vc">VCのファンド規模とLP →</a></p></div>
<div class="card"><h2>主な出資・投資の記録</h2><ul class="list">${inv.map((r) => `<li><div class="tx"><b>${link(r.src)}</b> → <b>${link(r.dst)}</b>${r.label ? ` <span class="badge">${esc(r.label)}</span>` : ''}<small>${esc(r.year || '')}${r.note ? ' ・ ' + esc(r.note) : ''}</small></div></li>`).join('')}</ul><p class="src">相関図の記録(Wikipedia・報道など、各会社の図に出典を記載)から集めたものです。</p></div>
<div class="card"><h2>大株主(上位の機関投資家)</h2><ul class="list">${big.map((r) => `<li><div class="tx"><b>${link(r.src)}</b> → <b>${link(r.dst)}</b>${r.label ? ` <span class="badge">${esc(r.label)}</span>` : ''}<small>${esc(r.note || '')}</small></div></li>`).join('')}</ul><p class="src">Yahoo Financeなどの2026年6月30日時点の記録です。</p></div>${updated('')}${reportBox('/money')}`
    return c.html(page({ title: `お金の流れ(出資・資金調達) | ${SITE.name}`, desc: '誰がどの会社に出資しているか。資金調達と出資の記録。', body, canonical: `${origin(c)}/money` }))
  })

  app.get('/vc', async (c) => {
    const [rows, lps, cm, cpf, csf, wsf, vpp] = await Promise.all([
      db.all('SELECT mgr, fund, size, usd_m, whenx, status, lp, note, url, conf FROM vc_fund ORDER BY (usd_m IS NULL), usd_m DESC, mgr').catch(() => []),
      db.all('SELECT lp, what, url FROM lp_side').catch(() => []),
      db.all('SELECT lp, fund, total_m, commit_m, year, url FROM lp_commit ORDER BY commit_m DESC, fund').catch(() => []),
      db.all("SELECT mgr, fund, vintage, committed_usd, asof, url FROM lp_fund WHERE lp='CalPERS' ORDER BY mgr, vintage DESC, fund").catch(() => []),
      db.all("SELECT mgr, fund, vintage, committed_usd, asof, url FROM lp_fund WHERE lp='CalSTRS' ORDER BY committed_usd DESC").catch(() => []),
      db.all("SELECT mgr, fund, vintage, committed_usd, asof, url FROM lp_fund WHERE lp='WSIB' ORDER BY vintage DESC, committed_usd DESC").catch(() => []),
      db.all("SELECT r.company AS company, r.role AS role, p.q AS q, COALESCE(NULLIF(p.ja,''), p.en) AS name FROM person_role r JOIN person p ON p.q=r.q WHERE r.company IN (SELECT DISTINCT mgr FROM vc_fund) OR r.company IN ('Sequoia Capital','Thrive Capital','Founders Fund','Lightspeed Venture Partners','General Catalyst','Kleiner Perkins','Andreessen Horowitz','Tiger Global') ORDER BY r.company, p.en").catch(() => []),
    ])
    const vpBy = new Map()
    for (const x of vpp) { if (!vpBy.has(x.company)) vpBy.set(x.company, []); vpBy.get(x.company).push(x) }
    const cpBy = new Map()
    for (const f of cpf) { if (!cpBy.has(f.mgr)) cpBy.set(f.mgr, { sum: 0, n: 0, rows: [] }); const g = cpBy.get(f.mgr); g.sum += f.committed_usd; g.n += 1; g.rows.push(f) }
    const cpOrder = [...cpBy.entries()].sort((a, b) => b[1].sum - a[1].sum)
    const usd = (n) => (n >= 1e9 ? (n / 1e9).toFixed(2) + '億' : (n / 1e8).toFixed(1) + '億').replace('億億', '') 
    const cmSum = cm.reduce((a, x) => a + (x.commit_m || 0), 0)
    const yen = (m) => (m >= 100 ? (m / 100).toLocaleString('ja-JP', { maximumFractionDigits: 1 }) + '億円' : m + '百万円')
    const invSet = new Set((await db.all("SELECT DISTINCT src FROM money_flow WHERE kind <> '大株主'").catch(() => [])).map((x) => x.src))
    const tr = rows.map((r) => `<tr><td><b>${invSet.has(r.mgr) ? `<a href="/investor?n=${encodeURIComponent(r.mgr)}">${esc(r.mgr)}</a>` : esc(r.mgr)}</b><br><small>${esc(r.fund)}</small></td><td>${esc(r.size)}<br><small>${esc(r.whenx)}</small></td><td><span class="badge">${esc(r.status)}</span></td><td>${esc(r.lp)}</td><td><small>${esc(r.note)}</small></td><td><a href="${esc(r.url)}" rel="noopener nofollow" target="_blank">出典</a><br><small>確度: ${esc(r.conf)}</small></td></tr>`).join('')
    const body = `<h1 class="page">VCのファンド規模とLP</h1><p class="muted">どのVCが、どのくらいの資金を集めて投資しているか。LP(ファンドに出資する年金・財団・事業会社など)の内訳は、多くが非公開です。公表されたものだけを載せ、分からない部分は「非公開」「未確定」としています。</p>
<div class="card" style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:14px"><thead><tr><th align="left">運用会社・ファンド</th><th align="left">規模・時期</th><th align="left">状態</th><th align="left">公表されたLP</th><th align="left">補足</th><th align="left">出典</th></tr></thead><tbody>${tr}</tbody></table><p class="src">確度: 高=本人の発表・公的資料 / 中=報道・信頼できる集計 / 低=集計サイトの記載(要確認)。「協議中」「目標」は、確定した金額ではありません。金額は表記のまま(円・ドルの換算はしていません)。</p></div>
<div class="card"><h2>LP側の公開資料(例)</h2><ul class="list">${lps.map((l) => `<li><div class="tx"><b>${esc(l.lp)}</b><small>${esc(l.what)} ・ <a href="${esc(l.url)}" rel="noopener nofollow" target="_blank">出典</a></small></div></li>`).join('')}</ul><p class="src">年金基金などは、投資先ファンドを開示する場合があります。大学基金・財団・事業会社は、多くが公表していません。</p></div>
${cpf.length ? `<div class="card" style="overflow-x:auto"><h2>CalPERSが出資しているVCファンド(公式の一覧)</h2><p class="muted" style="margin:0 0 8px">米国最大級の公的年金(カリフォルニア州職員退職年金基金)が、LPとして出資している、VC・成長投資のファンドです。運用会社ごとの合計と、ファンド別の出資約束額を載せています。</p>${cpOrder.map(([m, g]) => `<details style="margin:6px 0"><summary><b>${esc(m)}</b> ・ ${g.n}本 ・ 合計 ${(g.sum / 1e8).toFixed(1)}億ドル</summary><table style="width:100%;border-collapse:collapse;font-size:14px;margin-top:6px"><tbody>${g.rows.map((f) => `<tr><td>${esc(f.fund)}</td><td align="right">${esc(f.vintage)}年</td><td align="right">${(f.committed_usd / 1e6).toLocaleString('ja-JP', { maximumFractionDigits: 1 })}百万ドル</td></tr>`).join('')}</tbody></table></details>`).join('')}<p class="src">出典: <a href="${esc(cpf[0].url)}" rel="noopener nofollow" target="_blank">CalPERS Private Equity Program Fund Performance Review</a>(${esc(cpf[0].asof)}時点)。出資約束額(コミット額)で、実際の払込額ではありません。運用会社の名前は、ファンド名から対応づけています。CalPERSのほかの出資先(買収・不動産など)は、含みません。</p></div>` : ''}
${csf.length ? `<div class="card" style="overflow-x:auto"><h2>CalSTRSが新たに出資したVCファンド(2025年下半期)</h2><p class="muted" style="margin:0 0 8px">米国の教職員退職年金基金(CalSTRS)が、2025年下半期に、新しくコミットしたVC・成長投資のファンドです(公式の半期報告)。</p><table style="width:100%;border-collapse:collapse;font-size:14px"><tbody>${csf.map((f) => `<tr><td><b>${esc(f.fund)}</b><br><small>${esc(f.mgr)}</small></td><td align="right">${(f.committed_usd / 1e6).toLocaleString('ja-JP')}百万ドル</td></tr>`).join('')}</tbody></table><p class="src">出典: <a href="${esc(csf[0].url)}" rel="noopener nofollow" target="_blank">CalSTRS Investment Committee Semi-Annual Activity Report(Private Equity、${esc(csf[0].asof)}時点)</a>。コミット額です。同じ資料には、買収などの出資先も載っていますが、ここではVC・成長投資だけを抜き出しました。</p></div>` : ''}
${vpBy.size ? `<div class="card"><h2>ファンドを運営する人たち</h2><ul class="list">${[...vpBy.entries()].map(([co, ps]) => `<li><div class="tx"><b>${esc(co)}</b><small>${ps.map((p) => `<a href="/p/${esc(p.q)}">${esc(p.name)}</a>(${esc(p.role)})`).join(' ・ ')}</small></div></li>`).join('')}</ul><p class="src">Wikipediaに記事のある人だけです。役職は、Wikipediaの記述に基づく目安です。</p></div>` : ''}
${wsf.length ? `<div class="card" style="overflow-x:auto"><h2>ワシントン州投資委員会(WSIB)が出資しているVCファンド(一部)</h2><p class="muted" style="margin:0 0 8px">米ワシントン州の公的年金の運用機関が、公開しているPE一覧のうち、近年に出資した主なVCファンドです。</p><table style="width:100%;border-collapse:collapse;font-size:14px"><tbody>${wsf.map((f) => `<tr><td><b>${esc(f.fund)}</b><br><small>${esc(f.mgr)}</small></td><td align="right">${esc(f.vintage)}年</td><td align="right">${(f.committed_usd / 1e6).toLocaleString('ja-JP')}百万ドル</td></tr>`).join('')}</tbody></table><p class="src">出典: <a href="${esc(wsf[0].url)}" rel="noopener nofollow" target="_blank">WSIB Private Equity Portfolio</a>(${esc(wsf[0].asof)})。コミット額と初回出資の年は、資料の表記のままです(表の列がずれる箇所があるため、近年のファンドだけを抜き出しました。古い小規模ファンドは載せていません)。確度: 中。</p></div>` : ''}
${cm.length ? `<div class="card" style="overflow-x:auto"><h2>公的LP: 中小機構が出資したVCファンド(${cm.length}本・合計 ${yen(cmSum)})</h2><p class="muted" style="margin:0 0 8px">独立行政法人 中小企業基盤整備機構(中小機構)が、LPとして出資しているファンドの一覧です。2014〜2019年開始分で、運営会社名はページに記載がないため、ファンド名のみ載せています。</p><table style="width:100%;border-collapse:collapse;font-size:14px"><thead><tr><th align="left">ファンド</th><th align="right">ファンド総額</th><th align="right">中小機構の出資額</th><th align="right">開始</th></tr></thead><tbody>${cm.map((x) => `<tr><td>${esc(x.fund)}</td><td align="right">${x.total_m ? yen(x.total_m) : '—'}</td><td align="right">${yen(x.commit_m)}</td><td align="right">${x.year || '—'}</td></tr>`).join('')}</tbody></table><p class="src">出典: <a href="${esc(cm[0].url)}" rel="noopener nofollow" target="_blank">EXPACT(中小機構)の出資ファンド一覧</a>(ページ上は2020年7月現在、最終更新2024年5月)。出資額は当時の約束額です。</p></div>` : ''}${updated('調査日 2026年11月15日')}${reportBox('/vc')}`
    return c.html(page({ title: `VCのファンド規模とLP | ${SITE.name}`, desc: 'VCが集めたファンドの規模と、公表されたLP(出資者)。出典つき。', body, canonical: `${origin(c)}/vc` }))
  })

  // ---- きょうの動き ----
  app.get('/today', async (c) => {
    const rows = await db.all("SELECT ts, src, title, url, kind, score, num, company FROM events WHERE ts >= datetime('now','-2 days','localtime') AND kind NOT IN ('発信(X)','出演(YouTube)','発信(YouTube)') ORDER BY score DESC, ts DESC LIMIT 400").catch(() => [])
    const feed = await db.all("SELECT ts, src, title, url, kind, score, num, company FROM events WHERE ts >= datetime('now','-3 days','localtime') AND kind IN ('発信(X)','出演(YouTube)','発信(YouTube)') ORDER BY ts DESC LIMIT 30").catch(() => [])
    const by = new Map()
    for (const r of rows) { if (!by.has(r.kind)) by.set(r.kind, []); if (by.get(r.kind).length < 8) by.get(r.kind).push(r) }
    const order = ['不祥事・調査', '役員・人事', '買収・M&A', '資金調達', '上場・IPO', '提携', '決算・業績', '株主還元・報酬']
    const kinds = [...order.filter((k) => by.has(k)), ...[...by.keys()].filter((k) => !order.includes(k))]
    const body = `<h1 class="page">きょうの動き</h1><p class="muted">この2日間の、会社と人の動きです。東証の適時開示・プレスリリース・報道から自動で拾っています。 <a href="/feed/events.xml">RSSで購読</a></p>
${kinds.map((k) => `<div class="card"><h2>${esc(k)}</h2>${evHtml(by.get(k))}</div>`).join('') || '<div class="card"><p>まだありません。</p></div>'}
${feed.length ? `<div class="card"><h2>人物の最近の発信・出演</h2>${evHtml(feed)}</div>` : ''}
<p class="src"><a href="/events">すべての出来事 →</a> ・ 見出しと出典へのリンクのみ。分類と重要度は、見出しの語から自動で付けています。</p>`
    return c.html(page({ title: `きょうの動き | ${SITE.name}`, desc: '会社と人の、この2日間の動き(役員の交代・買収・資金調達・不祥事など)を1画面で。', body, canonical: origin(c) + '/today' }))
  })

  // ---- RSS(更新の購読) ----
  const atom = (c, title, path, items) => {
    const o = origin(c)
    const x = (t) => String(t ?? '').replace(/[<>&"]/g, (m) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[m]))
    const iso = (ts) => {
      const s = String(ts || '')
      const d = new Date(s.includes('T') || s.length > 19 ? s : s.replace(' ', 'T') + (s.length > 10 ? '+09:00' : 'T00:00:00+09:00'))
      return isNaN(d) ? new Date().toISOString() : d.toISOString()
    }
    const xml = `<?xml version="1.0" encoding="UTF-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>${x(title)}</title><id>${o}${path}</id><link href="${o}${path}" rel="self"/><updated>${new Date().toISOString()}</updated>${items.map((i) => `<entry><title>${x(i.title)}</title><id>${x(i.url)}</id><link href="${x(i.url)}"/><updated>${iso(i.ts)}</updated><summary>${x(i.sub || '')}</summary></entry>`).join('')}</feed>`
    return c.body(xml, 200, { 'content-type': 'application/atom+xml; charset=utf-8', 'cache-control': 'public, max-age=300' })
  }
  app.get('/feed/events.xml', async (c) => {
    const r = await db.all("SELECT ts, src, title, url, kind, company FROM events WHERE ts >= datetime('now','-3 days','localtime') AND score >= 70 ORDER BY ts DESC LIMIT 60").catch(() => [])
    return atom(c, `${SITE.name}: きょうの動き`, '/feed/events.xml', r.map((e) => ({ ts: e.ts, url: e.url, title: `[${e.kind}] ${e.title}`, sub: `${e.company || ''} ${e.src || ''}` })))
  })
  app.get('/feed/p/:q', async (c) => {
    const q = c.req.param('q').replace(/\.xml$/, '')
    if (!/^\d{1,12}$/.test(q)) return c.notFound()
    const p = await db.get('SELECT ja, en FROM person WHERE q=?', [q]).catch(() => null)
    if (!p) return c.notFound()
    const r = await db.all('SELECT ts, src, title, url, kind FROM person_feed WHERE q=? ORDER BY ts DESC LIMIT 30', [q]).catch(() => [])
    return atom(c, `${p.ja || p.en}の発信・出演`, `/feed/p/${q}.xml`, r.map((e) => ({ ts: e.ts, url: e.url, title: `[${e.kind}] ${e.title}`, sub: e.src })))
  })
  app.get('/feed/co/:slug', async (c) => {
    const sl = c.req.param('slug').replace(/\.xml$/, '')
    if (!/^[A-Za-z0-9_\-]{1,60}$/.test(sl)) return c.notFound()
    const m = await db.get('SELECT name FROM mapco WHERE slug=?', [sl]).catch(() => null)
    if (!m) return c.notFound()
    const [ev, nw] = await Promise.all([
      db.all('SELECT ts, src, title, url, kind FROM events WHERE company=? ORDER BY ts DESC LIMIT 30', [m.name]).catch(() => []),
      db.all('SELECT d AS ts, media AS src, title, url FROM mapco_news WHERE slug=? ORDER BY d DESC LIMIT 30', [sl]).catch(() => []),
    ])
    const all = [...ev.map((e) => ({ ts: e.ts, url: e.url, title: `[${e.kind}] ${e.title}`, sub: e.src })), ...nw.map((e) => ({ ts: e.ts, url: e.url, title: e.title, sub: e.src }))].sort((a, b) => String(b.ts).localeCompare(String(a.ts))).slice(0, 40)
    return atom(c, `${m.name}の動き`, `/feed/co/${sl}.xml`, all)
  })

  // ---- つながり検索 ----
  const resolveNode = async (name) => {
    name = String(name || '').trim().slice(0, 60)
    if (!name) return null
    const p = await db.get('SELECT q, ja, en FROM person WHERE ja=? OR en=? LIMIT 1', [name, name]).catch(() => null)
    if (p) return { id: 'p:' + p.q, label: p.ja || p.en, href: '/p/' + p.q }
    const m = await db.get('SELECT slug, name FROM mapco WHERE name=? OR en=? LIMIT 1', [name, name]).catch(() => null)
    if (m) return { id: 'c:' + m.name, label: m.name, href: '/co/' + m.slug }
    const fx = await db.get("SELECT dst AS n FROM money_flow WHERE kind <> '大株主' AND (dst=? OR src=?) LIMIT 1", [name, name]).catch(() => null)
    if (fx) return { id: 'c:' + name, label: name, href: '/search?q=' + encodeURIComponent(name) }
    const p2 = await db.get('SELECT q, ja, en FROM person WHERE ja LIKE ? OR en LIKE ? ORDER BY length(ja) LIMIT 1', [name + '%', name + '%']).catch(() => null)
    if (p2) return { id: 'p:' + p2.q, label: p2.ja || p2.en, href: '/p/' + p2.q }
    const m2 = await db.get('SELECT slug, name FROM mapco WHERE name LIKE ? ORDER BY length(name) LIMIT 1', [name + '%']).catch(() => null)
    if (m2) return { id: 'c:' + m2.name, label: m2.name, href: '/co/' + m2.slug }
    const f = await db.get("SELECT dst AS n FROM money_flow WHERE kind <> '大株主' AND (dst=? OR src=?) LIMIT 1", [name, name]).catch(() => null)
    return f ? { id: 'c:' + name, label: name, href: '/search?q=' + encodeURIComponent(name) } : null
  }
  const ph = (n) => new Array(n).fill('?').join(',')
  const expand = async (nodes) => {
    const ps = nodes.filter((n) => n.startsWith('p:')).map((n) => n.slice(2)).slice(0, 80)
    const cs = nodes.filter((n) => n.startsWith('c:')).map((n) => n.slice(2)).slice(0, 80)
    const E = []
    const run = async (sql, args, f) => { if (!args.length) return; const r = await db.all(sql, args).catch(() => []); for (const x of r) E.push(f(x)) }
    await Promise.all([
      run(`SELECT q, company, role FROM person_role WHERE q IN (${ph(ps.length)})`, ps, (x) => ['p:' + x.q, 'c:' + x.company, x.role || '関わり']),
      run(`SELECT p.q AS q, m.name AS company, mp.role AS role FROM person p JOIN mapco_people mp ON mp.en = p.en JOIN mapco m ON m.slug = mp.slug WHERE p.q IN (${ph(ps.length)}) AND p.en <> '' LIMIT 400`, ps, (x) => ['p:' + x.q, 'c:' + x.company, x.role || '関わり']),
      run(`SELECT q, rq, rel FROM person_rel WHERE q IN (${ph(ps.length)})`, ps, (x) => ['p:' + x.q, 'p:' + x.rq, x.rel]),
      run(`SELECT q, rq, rel FROM person_rel WHERE rq IN (${ph(ps.length)})`, ps, (x) => ['p:' + x.q, 'p:' + x.rq, x.rel]),
      run(`SELECT q, company, role FROM person_role WHERE company IN (${ph(cs.length)}) LIMIT 400`, cs, (x) => ['p:' + x.q, 'c:' + x.company, x.role || '関わり']),
      run(`SELECT p.q AS q, m.name AS company, mp.role AS role FROM mapco m JOIN mapco_people mp ON mp.slug = m.slug JOIN person p ON p.en = mp.en WHERE m.name IN (${ph(cs.length)}) AND mp.en <> '' LIMIT 400`, cs, (x) => ['p:' + x.q, 'c:' + x.company, x.role || '関わり']),
      run(`SELECT src, dst, kind FROM money_flow WHERE kind <> '大株主' AND src IN (${ph(cs.length)})`, cs, (x) => ['c:' + x.src, 'c:' + x.dst, x.kind]),
      run(`SELECT src, dst, kind FROM money_flow WHERE kind <> '大株主' AND dst IN (${ph(cs.length)})`, cs, (x) => ['c:' + x.src, 'c:' + x.dst, x.kind]),
      run(`SELECT m.name AS a, t.target AS b FROM mapco m JOIN mapco_acq t ON t.slug = m.slug WHERE m.name IN (${ph(cs.length)}) LIMIT 400`, cs, (x) => ['c:' + x.a, 'c:' + x.b, '買収・子会社']),
      run(`SELECT m.name AS a, t.target AS b FROM mapco m JOIN mapco_acq t ON t.slug = m.slug WHERE t.target IN (${ph(cs.length)}) LIMIT 400`, cs, (x) => ['c:' + x.a, 'c:' + x.b, '買収・子会社']),
    ])
    return E
  }
  const DIRL = { '出資': ['出資した', '出資を受けた'], '出資(YC)': ['出資した', '出資を受けた'], '支払い': ['支払った', '支払いを受けた'], '株の権利': ['株を受け取る権利を渡した', '株を受け取る権利を得た'], '買収・子会社': ['買収・子会社化した', '買収・子会社化された'] }
  const arrow = (n) => { const d = DIRL[n.label]; return d ? (n.back ? '↑ ' + d[1] : '↓ ' + d[0]) : '↓ ' + (WPRL[n.label] || n.label || '') }
  const companiesOf = async (node) => {
    if (node.id.startsWith('c:')) return [node.id.slice(2)]
    const q = node.id.slice(2)
    const [r1, r2] = await Promise.all([
      db.all('SELECT company FROM person_role WHERE q=?', [q]).catch(() => []),
      db.all("SELECT m.name AS company FROM person p JOIN mapco_people mp ON mp.en = p.en JOIN mapco m ON m.slug = mp.slug WHERE p.q = ? AND p.en <> ''", [q]).catch(() => []),
    ])
    return [...new Set([...r1, ...r2].map((x) => x.company))].slice(0, 40)
  }
  const commonCard = async (A, B) => {
    const [ca, cb] = await Promise.all([companiesOf(A), companiesOf(B)])
    const both = ca.filter((x) => cb.includes(x))
    let inv = []
    if (ca.length && cb.length) {
      inv = await db.all(`SELECT a.src AS src, count(*) AS n FROM money_flow a WHERE a.kind <> '大株主' AND a.dst IN (${ph(ca.length)}) AND a.src IN (SELECT b.src FROM money_flow b WHERE b.kind <> '大株主' AND b.dst IN (${ph(cb.length)})) GROUP BY a.src ORDER BY n DESC LIMIT 12`, [...ca, ...cb]).catch(() => [])
    }
    if (!both.length && !inv.length) return ''
    const lk = (x) => `<a href="/investor?n=${encodeURIComponent(x)}">${esc(x)}</a>`
    return `<div class="card"><h2>共通点</h2>${both.length ? `<p style="margin:0 0 8px"><b>どちらも関わる会社</b>: ${both.map(lk).join('、')}</p>` : ''}${inv.length ? `<p style="margin:0"><b>どちらの関係会社にも出資している投資家</b>: ${[...new Map(inv.map((x) => [x.src.toLowerCase(), x.src])).values()].map(lk).join('、')}</p>` : ''}<p class="src">${esc(A.label)}と${esc(B.label)}の、記録上の関わり先(役職の記録のある会社)と、出資の記録から、共通するものを並べています。</p></div>`
  }
  app.get('/path', async (c) => {
    const a = c.req.query('a') || '', b = c.req.query('b') || ''
    let result = ''
    let commonHtml = ''
    if (a && b) {
      const [A, B] = await Promise.all([resolveNode(a), resolveNode(b)])
      if (A && B && A.id !== B.id) commonHtml = await commonCard(A, B)
      if (!A || !B) result = `<div class="card"><p>${!A ? esc(a) : esc(b)} が、記録の中に見つかりませんでした。名前(日本語か英語)を確認してください。</p></div>`
      else if (A.id === B.id) result = '<div class="card"><p>同じ相手です。</p></div>'
      else {
        const prev = new Map([[A.id, null]])
        let frontier = [A.id], found = false
        for (let depth = 0; depth < 4 && frontier.length && !found; depth++) {
          const E = await expand(frontier)
          const next = []
          const cur = new Set(frontier)
          for (const [x, y, label] of E) for (const [from, to] of [[x, y], [y, x]]) {
            if (cur.has(from) && !prev.has(to)) { prev.set(to, { from, label, back: from !== x }); next.push(to); if (to === B.id) found = true }
          }
          frontier = [...new Set(next)].sort((m, n) => (m.startsWith('p:') ? 0 : 1) - (n.startsWith('p:') ? 0 : 1)).slice(0, 80)
        }
        if (!found) result = `<div class="card"><p>${esc(A.label)}と${esc(B.label)}の、記録上のつながりは、4つ先までは見つかりませんでした(記録のある範囲です)。</p></div>`
        else {
          const chain = []
          for (let n = B.id; n; n = prev.get(n)?.from) chain.unshift({ id: n, label: prev.get(n)?.label, back: prev.get(n)?.back })
          const names = await Promise.all(chain.map(async (n) => {
            if (n.id === A.id) return A
            if (n.id === B.id) return B
            if (n.id.startsWith('p:')) { const p = await db.get('SELECT ja, en FROM person WHERE q=?', [n.id.slice(2)]).catch(() => null); return { label: p ? (p.ja || p.en) : n.id, href: '/p/' + n.id.slice(2) } }
            const m = await db.get('SELECT slug FROM mapco WHERE name=? LIMIT 1', [n.id.slice(2)]).catch(() => null)
            return { label: n.id.slice(2), href: m ? '/co/' + m.slug : '/search?q=' + encodeURIComponent(n.id.slice(2)) }
          }))
          result = `<div class="card"><h2>${esc(A.label)} → ${esc(B.label)}(${chain.length - 1}つ)</h2><ol class="list">${chain.map((n, i) => `<li><div class="tx">${i ? `<small>${esc(arrow(n))}</small><br>` : ''}<a href="${esc(names[i].href)}"><b>${esc(names[i].label)}</b></a></div></li>`).join('')}</ol><p class="src">記録(Wikidata・相関図・出資の記録)にあるつながりだけをたどっています。1つの経路を出しています(他の経路もありえます)。</p></div>`
        }
      }
    }
    const body = `<h1 class="page">つながり検索</h1><p class="muted">2人(または会社)が、出資・同じ会社・家族・買収で、どうつながっているかを調べます。</p>
<form method="get" action="/path" class="card"><p style="margin:0 0 8px"><input name="a" value="${esc(a)}" placeholder="たとえば、サム・アルトマン" style="width:100%"></p><p style="margin:0 0 8px"><input name="b" value="${esc(b)}" placeholder="たとえば、マーク・ザッカーバーグ" style="width:100%"></p><button class="btn" type="submit">つながりを調べる</button></form>${result}${commonHtml}`
    return c.html(page({ title: `つながり検索 | ${SITE.name}`, desc: '2人・2社が、出資・同じ会社・家族・買収でどうつながっているかを調べます。', body, canonical: origin(c) + '/path', noindex: !!(a || b) }))
  })

  app.get('/trust', async (c) => {
    const rows = await db.all('SELECT t.q AS q, t.grp AS grp, t.checked_at AS at, t.photo AS photo, t.intro AS intro, t.timeline AS timeline, t.sns AS sns, t.feed AS feed, t.quotes AS quotes, p.ja AS ja, p.en AS en FROM top100 t LEFT JOIN person p ON p.q=t.q ORDER BY t.grp, t.rowid').catch(() => [])
    const mk = (v) => (v ? '<span style="color:var(--ok);font-weight:800">✓</span>' : '<span class="muted">—</span>')
    const cols = [['photo', '写真'], ['intro', '紹介'], ['timeline', '年表'], ['sns', 'SNS'], ['feed', '発信'], ['quotes', '名言']]
    const tot = rows.length
    const cnt = Object.fromEntries(cols.map(([k]) => [k, rows.filter((r) => r[k]).length]))
    const groups = [...new Set(rows.map((r) => r.grp))]
    const body = `<h1 class="page">注目の100人の確認状況</h1><p class="muted">相関図を公開したときに、必ず見られる100人(現役の経営者・投資家)を、先に丁寧に整えています。何がそろっていて、何がまだかを、そのまま見せます。</p>
<div class="card"><h2>確認の基準</h2><ul class="plain" style="margin:0;padding-left:1.2em"><li>出典がないものは載せません。年表・関係・名言は、出典のリンクを付けます。</li><li>SNSは、本人のものと確認できたものだけを載せます。</li><li>写真は、ライセンスと作者を確認できたものだけを使います。</li><li>親や子など、家族のうち、公に記録のない人は載せません。</li><li>誤りの指摘は、各ページの出典をたどって、お知らせください。</li></ul></div>
<div class="card"><h2>そろい具合(${tot}人中)</h2><p style="margin:0">${cols.map(([k, l]) => `<span class="badge${cnt[k] === tot ? ' ok' : ''}">${l} ${cnt[k]}/${tot}</span>`).join(' ')}</p></div>
${groups.map((g) => `<div class="card"><h2>${esc(g)}</h2><div class="tbl" style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:14px"><tr><th style="text-align:left;padding:6px 8px">人物</th>${cols.map(([, l]) => `<th style="padding:6px 8px">${l}</th>`).join('')}</tr>${rows.filter((r) => r.grp === g).map((r) => `<tr><td style="padding:6px 8px;border-top:1px solid var(--line)"><a href="/p/${esc(r.q)}">${esc(r.ja || r.en || 'Q' + r.q)}</a></td>${cols.map(([k]) => `<td style="padding:6px 8px;text-align:center;border-top:1px solid var(--line)">${mk(r[k])}</td>`).join('')}</tr>`).join('')}</table></div></div>`).join('')}`
    return c.html(page({ title: `注目の100人の確認状況 | ${SITE.name}`, desc: '公開時に必ず見られる100人を、出典つきで整えています。確認の基準と、そろい具合を公開しています。', body, canonical: origin(c) + '/trust' }))
  })
  app.get('/events', async (c) => {
    const k = c.req.query('k') || ''
    const hot = c.req.query('s') === 'score'
    const kinds = ['不祥事・調査', '買収・M&A', '資金調達', '上場・IPO', '役員・人事', '提携', '決算・業績', '株主還元・報酬', '発信(X)', '出演(YouTube)', '発信(YouTube)']
    const rows = await db.all(`SELECT ts, src, title, url, kind, score, num, company FROM events WHERE (?='' OR kind=?) ${hot ? "AND ts >= datetime('now','-3 days','localtime')" : ''} ORDER BY ${hot ? 'score DESC, ts DESC' : 'ts DESC'} LIMIT 120`, [k, k]).catch(() => [])
    const tab = (label, kk, ss) => `<a class="${(k === kk && (hot ? 'score' : '') === ss) ? 'on' : ''}" href="/events?${kk ? 'k=' + encodeURIComponent(kk) : ''}${ss ? (kk ? '&' : '') + 's=score' : ''}">${esc(label)}</a>`
    const body = `<h1 class="page">会社の出来事</h1><p class="muted">東証の適時開示・プレスリリース・報道から、資金調達、買収、役員の交代、不祥事などを、自動で拾っています(10分おきに更新)。</p>
<div class="tabs">${tab('新着', '', '')}${tab('重要順(3日間)', '', 'score')}${kinds.map((x) => tab(x, x, '')).join('')}</div>
<div class="card">${rows.length ? evHtml(rows) : '<p>まだ出来事がありません。</p>'}</div><p class="src">見出しと出典へのリンクのみ。内容は各リンク先でご確認ください。分類と重要度は、見出しの語から自動でつけたもので、誤りを含みます。</p>`
    return c.html(page({ title: `会社の出来事 | ${SITE.name}`, desc: '資金調達・買収・役員の交代・不祥事などの会社の出来事を、適時開示と報道から自動で拾っています。', body, canonical: origin(c) + '/events' }))
  })
  app.get('/robots.txt', (c) => c.text(`User-agent: *\nAllow: /\nDisallow: /search
Disallow: /admin\nSitemap: ${origin(c)}/sitemap.xml\n`))
  const xml = (c, urls) => c.body(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls.map((u) => `<url><loc>${u}</loc></url>`).join('')}</urlset>`, 200, { 'content-type': 'application/xml; charset=utf-8' })
  app.get('/sitemap.xml', async (c) => {
    const s = await stats()
    const n = Math.ceil(s.corps / 50000)
    const items = ['listed', 'co', 'p'].map((k) => `<sitemap><loc>${origin(c)}/sitemap-${k}.xml</loc></sitemap>`)
    for (let i = 0; i < n; i++) items.push(`<sitemap><loc>${origin(c)}/sitemap-${i}.xml</loc></sitemap>`)
    return c.body(`<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${items.join('')}</sitemapindex>`, 200, { 'content-type': 'application/xml; charset=utf-8' })
  })
  app.get('/sitemap-listed.xml', async (c) => xml(c, (await db.all("SELECT num FROM edinet WHERE listed='上場' AND num<>''")).map((x) => `${origin(c)}/corp/${x.num}`)))
  app.get('/sitemap-co.xml', async (c) => xml(c, (await db.all('SELECT slug FROM mapco').catch(() => [])).map((x) => `${origin(c)}/co/${x.slug}`)))
  app.get('/sitemap-p.xml', async (c) => xml(c, (await db.all('SELECT q FROM person').catch(() => [])).map((x) => `${origin(c)}/p/${x.q}`)))
  app.get('/:f{sitemap-[0-9]+\\.xml}', async (c) => {
    const i = parseInt(c.req.param('f').replace(/\D/g, ''), 10)
    if (!(i >= 0 && i < 1000)) return c.notFound()
    const r = await db.all('SELECT num FROM corp WHERE rowid>? AND rowid<=?', [i * 50000, (i + 1) * 50000])
    return xml(c, r.map((x) => `${origin(c)}/corp/${x.num}`))
  })
  app.get('/favicon.ico', (c) => c.body(null, 204))
  return app
}

export { CSS, esc, fmt }
