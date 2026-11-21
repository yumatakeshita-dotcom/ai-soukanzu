"""ニュージーランドを足す変更(2026-11-19 準備。データが入ってから当てて出す)。
add_sg_patch.py と add_sg_v2_patch.py のあとに当てる。worker.js を書きかえる。
D1「kigyo-nz」を NZDB という名前でつなぐ(deploy_worker.py の bindings にも足すこと)。"""
import os
p = os.path.join(os.path.dirname(__file__), "worker.js")
js = open(p).read()
def rep(a, b):
    global js
    assert js.count(a) == 1, a[:80]
    js = js.replace(a, b)
rep('''  SG: { name: "シンガポール",''', '''  // 2026-11-19 追加: ニュージーランド(データは D1「kigyo-nz」に、シンガポールと同じ形で入っている)
  NZ: { name: "ニュージーランド", reg: "ニュージーランド Companies Office(Ministry of Business, Innovation and Employment)", lic: "Companies Office Bulk Data Access Agreement", licUrl: "https://www.companiesoffice.govt.nz/data-services/ways-to-get-our-data/bulk-data-access-agreement/", url: /* @__PURE__ */ __name((id) => `https://www.nzbn.govt.nz/mynzbn/nzbndetails/${encodeURIComponent(id)}/`, "url") },
  SG: { name: "シンガポール",''')
rep('''  const getSgAsset = opts.getSgAsset || (async () => null);
  const SRC = [{ get: getAsset }, { get: getSgAsset, only: "SG" }];''', '''  const getSgAsset = opts.getSgAsset || (async () => null);
  const getNzAsset = opts.getNzAsset || (async () => null);
  const SRC = [{ get: getAsset }, { get: getSgAsset, only: "SG" }, { get: getNzAsset, only: "NZ" }];''')
# 読み込み先をデータベースごとに作れるようにする
rep('''    let sgVer;
    const getSgAsset = /* @__PURE__ */ __name(async (path) => {
      if (!env.SGDB) return null;
      if (sgVer === void 0) sgVer = await env.SGDB.prepare("SELECT v, z FROM ver ORDER BY v DESC LIMIT 1").first().catch(() => null);
      const d = await env.SGDB.prepare("SELECT data FROM f WHERE path = ?").bind(sgVer ? `/${sgVer.v}${path}` : path).first("data");
      if (d == null || !sgVer?.z) return d;
      const bin = Uint8Array.from(atob(d), (ch) => ch.charCodeAt(0));
      return await new Response(new Blob([bin]).stream().pipeThrough(new DecompressionStream("gzip"))).text();
    }, "getSgAsset");
    return createApp({ getAsset, getSgAsset }).fetch(request, env, ctx);''', '''    const dbGetter = /* @__PURE__ */ __name((db) => {
      let ver;
      return async (path) => {
        if (!db) return null;
        if (ver === void 0) ver = await db.prepare("SELECT v, z FROM ver ORDER BY v DESC LIMIT 1").first().catch(() => null);
        const d = await db.prepare("SELECT data FROM f WHERE path = ?").bind(ver ? `/${ver.v}${path}` : path).first("data");
        if (d == null || !ver?.z) return d;
        const bin = Uint8Array.from(atob(d), (ch) => ch.charCodeAt(0));
        return await new Response(new Blob([bin]).stream().pipeThrough(new DecompressionStream("gzip"))).text();
      };
    }, "dbGetter");
    return createApp({ getAsset, getSgAsset: dbGetter(env.SGDB), getNzAsset: dbGetter(env.NZDB) }).fetch(request, env, ctx);''')
open(p, "w").write(js)
print("ok")
