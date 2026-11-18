// 手元で動かすための起動ファイル。Node 標準の SQLite(node:sqlite)で法人データベースを読み、/img/ は public フォルダから返す。
// 使い方: node src/dev.mjs   (データベースの場所は環境変数 HOUJIN_DB で変えられる)
import { serve } from '@hono/node-server'
import { serveStatic } from '@hono/node-server/serve-static'
import { Hono } from 'hono'
import { DatabaseSync } from 'node:sqlite'
import { readFile } from 'node:fs/promises'
import { createApp } from './app.mjs'

const path = process.env.HOUJIN_DB || 'C:/Users/yumat/.claude/data/houjin.sqlite'
const sqlite = new DatabaseSync(path, { readOnly: true })
const db = {
  async all(sql, params = []) { return sqlite.prepare(sql).all(...params) },
  async get(sql, params = []) { return sqlite.prepare(sql).get(...params) },
  async run(sql, params = []) { return sqlite.prepare(sql).run(...params) },
}
const root = new Hono()
root.use('/img/*', serveStatic({ root: './public' }))
const getAsset = async (p) => { try { return await readFile('./public' + p, 'utf8') } catch { return null } }
root.route('/', createApp(db, { getAsset }))
const port = Number(process.env.PORT || 8787)
serve({ fetch: root.fetch, port }, () => console.log(`http://localhost:${port}`))
