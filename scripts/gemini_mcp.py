# -*- coding: utf-8 -*-
"""gemini_research.py を Claude Code から呼べるようにする、小さなMCPサーバー(2026/11/19)。

追加の部品は不要(Python だけで動く)。リポジトリ直下の .mcp.json に登録してある。
道具:
  gemini_status   … キーの有無・ファイル検索ストアの状態
  gemini_store    … 資料(notebooklm/ ほか)をファイル検索ストアに入れる(足すだけ)
  gemini_research … テーマを渡すと、新しい企業・人物・取引・移籍を表で返し、inbox/gemini/ に足す
  gemini_verify   … inbox/gemini/ の結果を確かめる(URL・重なり・日付・確かさ)。合格したものだけ取り込み候補にする(2026/11/19追加)
キーは環境変数 GEMINI_API_KEY から読む。未設定のときはドライラン(送る内容の確認)だけ返す。
"""
import io, json, os, sys
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gemini_research as g
import gemini_verify as gv

TOOLS = [
    {'name': 'gemini_status', 'description': 'Gemini調査の準備状態(キー・ファイル検索ストア)を返す',
     'inputSchema': {'type': 'object', 'properties': {}}},
    {'name': 'gemini_store', 'description': '共有フォルダの notebooklm/ などの資料を Gemini のファイル検索ストアに入れる(入れ済みは飛ばす)',
     'inputSchema': {'type': 'object', 'properties': {'dry_run': {'type': 'boolean'}}}},
    {'name': 'gemini_research',
     'description': 'Gemini + Google検索で、相関図にまだ無い企業・人物・取引・移籍を調べ、'
                    '「会社名/関係/相手/金額/日付/出典URL/確かさ/備考」の表で返す。結果は inbox/gemini/ に足す',
     'inputSchema': {'type': 'object', 'required': ['topic'], 'properties': {
         'topic': {'type': 'string', 'description': '調べるテーマ(例: 日本のAIスタートアップの資金調達 2026年11月)'},
         'max_items': {'type': 'integer', 'default': 10},
         'check': {'type': 'boolean', 'default': True, 'description': 'ファイル検索で既存資料と照らすか'},
         'dry_run': {'type': 'boolean', 'default': False}}}},
    {'name': 'gemini_verify',
     'description': 'inbox/gemini/ のGemini調査の結果を確かめる: 出典URLにつながるか(つながらないものは未確認)、既存データとの重なり、'
                    '日付の食い違い、確かさの印。合格したものだけ inbox/money・moves に足す。file を省くと、まだ確かめていないもの全部',
     'inputSchema': {'type': 'object', 'properties': {
         'file': {'type': 'string', 'description': '例: inbox/gemini/2026-11-19.json'},
         'dry_run': {'type': 'boolean', 'default': False}}}},
]


def call(name, a):
    buf = io.StringIO()
    with redirect_stdout(buf):  # 標準出力はMCPの通信に使うので、ログはここに集める
        logs = []
        log = logs.append
        if name == 'gemini_status':
            out = json.dumps(g.status(), ensure_ascii=False, indent=1)
        elif name == 'gemini_store':
            g.build_store(bool(a.get('dry_run')) or not g.key(), log)
            out = '\n'.join(logs)
        elif name == 'gemini_research':
            r = g.research(a['topic'], int(a.get('max_items') or 10), a.get('check', True), bool(a.get('dry_run')), log)
            out = '\n'.join(logs) + ('\n\n' + r['markdown'] if r.get('markdown') else '')
        elif name == 'gemini_verify':
            fs = [os.path.join(g.ROOT, a['file'])] if a.get('file') else gv.targets()
            gv.run(fs, dry=bool(a.get('dry_run')), log=log)
            out = '\n'.join(logs)
        else:
            raise ValueError('知らない道具: ' + name)
    return out


def reply(id_, result=None, error=None):
    msg = {'jsonrpc': '2.0', 'id': id_}
    msg['error' if error else 'result'] = error or result
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + '\n')
    sys.stdout.flush()


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        m, id_ = req.get('method'), req.get('id')
        if id_ is None:
            continue  # 通知(notifications/initialized など)には返事しない
        if m == 'initialize':
            ver = (req.get('params') or {}).get('protocolVersion') or '2025-06-18'
            reply(id_, {'protocolVersion': ver, 'capabilities': {'tools': {}},
                        'serverInfo': {'name': 'ai-soukanzu-gemini', 'version': '0.1.0'}})
        elif m == 'tools/list':
            reply(id_, {'tools': TOOLS})
        elif m == 'tools/call':
            p = req.get('params') or {}
            try:
                txt = call(p.get('name'), p.get('arguments') or {})
                reply(id_, {'content': [{'type': 'text', 'text': txt}]})
            except Exception as e:
                reply(id_, {'content': [{'type': 'text', 'text': f'失敗: {e}'}], 'isError': True})
        elif m == 'ping':
            reply(id_, {})
        else:
            reply(id_, error={'code': -32601, 'message': 'method not found: ' + str(m)})


if __name__ == '__main__':
    main()
