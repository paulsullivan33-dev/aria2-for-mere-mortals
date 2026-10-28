#!/usr/bin/env python3
"""A tiny static file server with HTTP Range support and request logging.

python3 -m http.server cannot answer Range requests, and aria2 needs
Range support to split a download into segments and to resume one.
This server exists for the aria2 guide's lab: it serves one folder on
loopback, honours a single Range per request, and appends one line
per request to a log file so segmented downloads can be proven from
the server's side.

Usage: range_server.py SERVE_DIR LOG_FILE [PORT]
"""

import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERVE_DIR = os.path.abspath(sys.argv[1])
LOG_FILE = sys.argv[2]
PORT = int(sys.argv[3]) if len(sys.argv) > 3 else 8377


def log(line):
    with open(LOG_FILE, "a") as fh:
        fh.write(line + "\n")


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # silence the default stderr log
        pass

    def _path(self):
        from urllib.parse import unquote, urlparse

        rel = unquote(urlparse(self.path).path).lstrip("/")
        path = os.path.normpath(os.path.join(SERVE_DIR, rel))
        if not path.startswith(SERVE_DIR):
            return None
        return path

    def do_GET(self):
        path = self._path()
        range_hdr = self.headers.get("Range", "-")
        if path is None or not os.path.isfile(path):
            log(f"GET {self.path} Range={range_hdr} -> 404")
            self.send_error(404)
            return
        size = os.path.getsize(path)
        start, end, status = 0, size - 1, 200
        if range_hdr.startswith("bytes="):
            m = re.fullmatch(r"bytes=(\d*)-(\d*)", range_hdr)
            if m:
                if m.group(1):
                    start = int(m.group(1))
                    end = int(m.group(2)) if m.group(2) else size - 1
                else:  # suffix range, bytes=-N
                    n = int(m.group(2))
                    start = max(0, size - n)
                    end = size - 1
                end = min(end, size - 1)
                status = 206
        length = end - start + 1
        log(f"GET {self.path} Range={range_hdr} -> {status} bytes {start}-{end}")
        self.send_response(status)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Length", str(length))
        self.send_header("Accept-Ranges", "bytes")
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        with open(path, "rb") as fh:
            fh.seek(start)
            remaining = length
            while remaining > 0:
                chunk = fh.read(min(65536, remaining))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    break
                remaining -= len(chunk)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    log(f"START serving {SERVE_DIR} on 127.0.0.1:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
