import { createApp } from './app.mjs'
export default {
  async fetch(request, env, ctx) {
    const getAsset = async (path) => {
      const r = await env.ASSETS.fetch(new Request(new URL(path, request.url)))
      return r.ok ? await r.text() : null
    }
    return createApp({ getAsset }).fetch(request, env, ctx)
  },
}
