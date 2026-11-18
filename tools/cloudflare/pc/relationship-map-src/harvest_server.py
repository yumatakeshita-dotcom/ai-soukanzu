"""Chromeで読んだ投稿を、手元(127.0.0.1)だけで受け取って social_harvest.jsonl に1行ずつ保存する小さな受け口。外には公開しない。"""
import http.server, json, os
S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, 'social_harvest.jsonl')
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get('content-length', 0))
        body = self.rfile.read(n).decode('utf-8', 'replace')
        try:
            json.loads(body)
            open(OUT, 'a', encoding='utf-8').write(body.replace('\n', ' ') + '\n')
        except Exception:
            pass
        self.send_response(204); self.send_header('Access-Control-Allow-Origin', '*'); self.end_headers()
    def do_OPTIONS(self):
        self.send_response(204)
        for k, v in (('Access-Control-Allow-Origin', '*'), ('Access-Control-Allow-Methods', 'POST'), ('Access-Control-Allow-Headers', '*')):
            self.send_header(k, v)
        self.end_headers()
    def log_message(self, *a): pass
http.server.HTTPServer(('127.0.0.1', 8799), H).serve_forever()
