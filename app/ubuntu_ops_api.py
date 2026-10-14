#!/usr/bin/env python3

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            status = 200
            response = {
                "status": "ok",
                "service": "ubuntu-ops-api"
            }
        else:
            status = 404
            response = {"error": "not found"}

        body = json.dumps(response).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8080), APIHandler)
    print("ubuntu-ops-api listening on 127.0.0.1:8080", flush=True)
    server.serve_forever()
