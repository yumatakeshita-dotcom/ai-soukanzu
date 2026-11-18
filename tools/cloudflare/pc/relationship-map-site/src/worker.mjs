// Cloudflare Workers 用の入口。D1 を db(all/get) の形に包み、静的ファイル(/c/・/n/)を env.ASSETS から読む関数を渡す。
import { createApp } from './app.mjs'

export default {
  async fetch(request, env, ctx) {
    const db = {
      async all(sql, params = []) { return (await env.DB.prepare(sql).bind(...params).all()).results },
      async get(sql, params = []) { return await env.DB.prepare(sql).bind(...params).first() },
      async run(sql, params = []) { return await env.DB.prepare(sql).bind(...params).run() },
    }
    const getAsset = async (path) => {
      const r = await env.ASSETS.fetch(new Request(new URL(path, request.url)))
      return r.ok ? await r.text() : null
    }
    return createApp(db, { getAsset }).fetch(request, env, ctx)
  },
}
