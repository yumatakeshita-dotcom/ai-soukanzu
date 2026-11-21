"""2026-11-18 2回目の変更: シンガポールの旧社名で検索できるようにし、版の表(ver)のいちばん新しい版を読むようにする。
add_sg_patch.py のあとに当てる。worker.js を書きかえる。"""
import os
p = os.path.join(os.path.dirname(__file__), "worker.js")
js = open(p).read()
def rep(a, b):
    global js
    assert js.count(a) == 1, a[:80]
    js = js.replace(a, b)
# 検索結果: 旧社名で当たったときは今の名前を出し、旧社名を添える。同じ会社は1回だけ
rep('''.slice(0, 80).map((r) => ({ cc: r[0], id: r[1], name: r[2], city: r[3] })) };
  }, "searchOne");''', '''.slice(0, 80).map((r) => ({ cc: r[0], id: r[1], name: r[4] || r[2], city: r[3], old: r[4] ? r[2] : "" })) };
  }, "searchOne");''')
rep('''    for (let i = 0; out.length < 80 && lists.some((l) => i < l.length); i++) for (const l of lists) if (i < l.length && out.length < 80) out.push(l[i]);''',
'''    const seen = /* @__PURE__ */ new Set();
    for (let i = 0; out.length < 80 && lists.some((l) => i < l.length); i++) for (const l of lists) if (i < l.length && out.length < 80 && !seen.has(l[i].cc + ":" + l[i].id)) {
      seen.add(l[i].cc + ":" + l[i].id);
      out.push(l[i]);
    }''')
rep('''${r.city ? " \\u30FB " + esc(r.city) : ""} \\u30FB \\u767B\\u8A18\\u756A\\u53F7 ${esc(r.id)}</small>''',
'''${r.city ? " \\u30FB " + esc(r.city) : ""} \\u30FB \\u767B\\u8A18\\u756A\\u53F7 ${esc(r.id)}${r.old ? " \\u30FB \\u65E7\\u793E\\u540D " + esc(r.old) : ""}</small>''')
# 会社のページ: 旧社名の行
rep('''since: r[6], sic: r[7] } : null;''', '''since: r[6], sic: r[7], old: r[8] || "" } : null;''')
rep('''r.sic && ["\\u4E8B\\u696D\\u306E\\u7A2E\\u985E", r.sic]].filter(Boolean);''', '''r.sic && ["\\u4E8B\\u696D\\u306E\\u7A2E\\u985E", r.sic], r.old && ["\\u65E7\\u793E\\u540D", r.old]].filter(Boolean);''')
# 版の表のいちばん新しい版を読む(圧縮してあれば戻す)。版がまだ無いときは、最初の版(そのままの形)を読む
rep('''    const getSgAsset = /* @__PURE__ */ __name(async (path) => env.SGDB ? await env.SGDB.prepare("SELECT data FROM f WHERE path = ?").bind(path).first("data") : null, "getSgAsset");''',
'''    let sgVer;
    const getSgAsset = /* @__PURE__ */ __name(async (path) => {
      if (!env.SGDB) return null;
      if (sgVer === void 0) sgVer = await env.SGDB.prepare("SELECT v, z FROM ver ORDER BY v DESC LIMIT 1").first().catch(() => null);
      const d = await env.SGDB.prepare("SELECT data FROM f WHERE path = ?").bind(sgVer ? `/${sgVer.v}${path}` : path).first("data");
      if (d == null || !sgVer?.z) return d;
      const bin = Uint8Array.from(atob(d), (ch) => ch.charCodeAt(0));
      return await new Response(new Blob([bin]).stream().pipeThrough(new DecompressionStream("gzip"))).text();
    }, "getSgAsset");''')
open(p, "w").write(js)
print("ok")
