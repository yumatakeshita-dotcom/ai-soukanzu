from http.server import BaseHTTPRequestHandler, HTTPServer
import os
S = os.path.dirname(os.path.abspath(__file__))

class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_POST(self):
        n = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(n)
        name = self.path.strip('/') or 'recv.json'
        with open(os.path.join(S, os.path.basename(name)), 'wb') as f:
            f.write(body)
        self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(b'ok')

HTTPServer(('127.0.0.1', 8766), H).serve_forever()
