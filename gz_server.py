#!/usr/bin/env python3
"""Static server with gzip support for pre-gzipped files (serves .gz with Content-Encoding)."""
import os, re
from http.server import HTTPServer, SimpleHTTPRequestHandler

ROOT = '/home/agentuser/shotform'

class GzipHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        p = self.translate_path(self.path)
        if os.path.isfile(p + '.gz') and 'gzip' in self.headers.get('Accept-Encoding', ''):
            self.send_gz(p + '.gz', os.path.getsize(p) if os.path.isfile(p) else None)
            return
        super().do_GET()

    def do_HEAD(self):
        self.do_GET_body_only() if False else super().do_HEAD()

    def send_gz(self, gzpath, orig_size):
        try:
            with open(gzpath, 'rb') as f:
                data = f.read()
        except OSError:
            self.send_error(404)
            return
        orig = gzpath[:-3]
        ctype = self.guess_type(orig)
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Encoding', 'gzip')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'public, max-age=86400')
        self.end_headers()
        self.wfile.write(data)

if __name__ == '__main__':
    os.chdir(ROOT)
    HTTPServer(('127.0.0.1', 8791), GzipHandler).serve_forever()
