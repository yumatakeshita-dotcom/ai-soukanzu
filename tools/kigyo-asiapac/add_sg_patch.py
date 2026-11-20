js=open('w/orig_worker.js').read()
def rep(a,b):
    global js
    assert js.count(a)==1, a[:80]
    js=js.replace(a,b)
# 1) 国の一覧にシンガポールを足す
rep('''url: /* @__PURE__ */ __name((id) => `https://abr.business.gov.au/ABN/View?abn=${encodeURIComponent(id)}`, "url") }
};''','''url: /* @__PURE__ */ __name((id) => `https://abr.business.gov.au/ABN/View?abn=${encodeURIComponent(id)}`, "url") },
  // 2026-11-18 追加: シンガポール(データは D1「kigyo-sg」の表 f に、ファイルと同じ形で入っている)
  SG: { name: "シンガポール", reg: "シンガポール ACRA(Accounting and Corporate Regulatory Authority)、data.gov.sg", lic: "Singapore Open Data Licence v1.0", licUrl: "https://data.gov.sg/open-data-licence", url: /* @__PURE__ */ __name((id) => `https://www.bizfile.gov.sg/`, "url") }
};''')
# 2) 読み込み先を2つにする(今のファイル + シンガポールのデータベース)
rep('''  const getAsset = opts.getAsset || (async () => null);''','''  const getAsset = opts.getAsset || (async () => null);
  const getSgAsset = opts.getSgAsset || (async () => null);
  const SRC = [{ get: getAsset }, { get: getSgAsset, only: "SG" }];''')
rep('''  let hotCache = null, metaCache = null;
  const meta = /* @__PURE__ */ __name(async () => metaCache ||= JSON.parse(await getAsset("/c/meta.json").catch(() => null) || "{}"), "meta");
  const hotMap = /* @__PURE__ */ __name(async () => {
    if (hotCache) return hotCache;
    const t = await getAsset("/n/hot.json").catch(() => null);
    hotCache = {};
    for (const [L, arr] of Object.entries(t ? JSON.parse(t) : {})) hotCache[Number(L)] = new Set(arr);
    return hotCache;
  }, "hotMap");
  const shardRow = /* @__PURE__ */ __name(async (cc, id) => {
    const m = await meta();''','''  const srcMeta = /* @__PURE__ */ __name(async (s) => s.meta ||= JSON.parse(await s.get("/c/meta.json").catch(() => null) || "{}"), "srcMeta");
  const srcHot = /* @__PURE__ */ __name(async (s) => {
    if (s.hot) return s.hot;
    const t = await s.get("/n/hot.json").catch(() => null);
    const h = {};
    for (const [L, arr] of Object.entries(t ? JSON.parse(t) : {})) h[Number(L)] = new Set(arr);
    return s.hot = h;
  }, "srcHot");
  const meta = /* @__PURE__ */ __name(async () => {
    const ms = await Promise.all(SRC.map(srcMeta));
    const by = {};
    let total = 0;
    for (const m of ms) {
      Object.assign(by, m.by || {});
      total += m.total || 0;
    }
    return { by, total };
  }, "meta");
  const shardRow = /* @__PURE__ */ __name(async (cc, id) => {
    const s = SRC.find((x) => x.only === cc) || SRC[0];
    const getAsset = s.get;
    const m = await srcMeta(s);''')
rep('''  const search = /* @__PURE__ */ __name(async (q) => {
    const cq = core(q), cp = Array.from(cq);
    if (cp.length < 2) return { rows: [], short: true };
    const m = await meta(), hot = await hotMap();''','''  const search = /* @__PURE__ */ __name(async (q) => {
    const rs = await Promise.all(SRC.map((s) => searchOne(s, q).catch(() => ({ rows: [] }))));
    if (rs.every((r) => r.short)) return { rows: [], short: true };
    const out = [], lists = rs.map((r) => r.rows || []);
    for (let i = 0; out.length < 80 && lists.some((l) => i < l.length); i++) for (const l of lists) if (i < l.length && out.length < 80) out.push(l[i]);
    return { rows: out };
  }, "search");
  const searchOne = /* @__PURE__ */ __name(async (s, q) => {
    const getAsset = s.get;
    const cq = core(q), cp = Array.from(cq);
    if (cp.length < 2) return { rows: [], short: true };
    const m = await srcMeta(s), hot = await srcHot(s);''')
rep('''.slice(0, 80).map((r) => ({ cc: r[0], id: r[1], name: r[2], city: r[3] })) };
  }, "search");''','''.slice(0, 80).map((r) => ({ cc: r[0], id: r[1], name: r[2], city: r[3] })) };
  }, "searchOne");''')
# 3) 説明文
old_desc='desc: "\\u53F0\\u6E7E\\u30FB\\u30AA\\u30FC\\u30B9\\u30C8\\u30E9\\u30EA\\u30A2\\u306E'
rep(old_desc, 'desc: "\\u53F0\\u6E7E\\u30FB\\u30AA\\u30FC\\u30B9\\u30C8\\u30E9\\u30EA\\u30A2\\u30FB\\u30B7\\u30F3\\u30AC\\u30DD\\u30FC\\u30EB\\u306E')
# 4) シンガポールのデータベースから読む
rep('''    return createApp({ getAsset }).fetch(request, env, ctx);''','''    const getSgAsset = /* @__PURE__ */ __name(async (path) => env.SGDB ? await env.SGDB.prepare("SELECT data FROM f WHERE path = ?").bind(path).first("data") : null, "getSgAsset");
    return createApp({ getAsset, getSgAsset }).fetch(request, env, ctx);''')
open('w/worker.js','w').write(js)
print('ok',len(js))
