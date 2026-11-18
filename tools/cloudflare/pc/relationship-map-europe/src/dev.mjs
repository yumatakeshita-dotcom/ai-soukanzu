import { serve } from '@hono/node-server'
import { readFile } from 'node:fs/promises'
import { createApp } from './app.mjs'
const getAsset = async (p) => { try { return await readFile('./public' + p, 'utf8') } catch { return null } }
const port = Number(process.env.PORT || 8788)
serve({ fetch: createApp({ getAsset }).fetch, port }, () => console.log(`http://localhost:${port}`))
