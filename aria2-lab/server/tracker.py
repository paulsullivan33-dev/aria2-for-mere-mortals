#!/usr/bin/env python3
"""A minimal BitTorrent tracker for the aria2 guide's lab.

Just enough of the tracker protocol for two aria2 instances on
loopback to find each other: peers announce over HTTP, the tracker
remembers (address, port) per info_hash and hands the list back in
compact form. No statistics, no event handling, no expiry.

Usage: tracker.py LOG_FILE [PORT]
"""

import socket
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

LOG_FILE = sys.argv[1]
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8379
PEERS = {}  # info_hash bytes -> set of (ip, port)


def benc(x):
    if isinstance(x, int):
        return b"i" + str(x).encode() + b"e"
    if isinstance(x, bytes):
        return str(len(x)).encode() + b":" + x
    if isinstance(x, str):
        return benc(x.encode())
    if isinstance(x, list):
        return b"l" + b"".join(benc(i) for i in x) + b"e"
    if isinstance(x, dict):
        items = sorted(x.items(), key=lambda kv: kv[0] if isinstance(kv[0], bytes) else kv[0].encode())
        return b"d" + b"".join(benc(k) + benc(v) for k, v in items) + b"e"
    raise TypeError(type(x))


def log(line):
    with open(LOG_FILE, "a") as fh:
        fh.write(line + "\n")


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        raw_query = urlparse(self.path).query
        # The info_hash is arbitrary bytes, percent-escaped. Decoding it
        # as text corrupts it, so take it from the raw query string,
        # still escaped -- any stable key identifies the swarm.
        info_hash = ""
        for part in raw_query.split("&"):
            if part.startswith("info_hash="):
                info_hash = part[len("info_hash="):]
        q = parse_qs(raw_query)
        port = int(q.get("port", ["0"])[0])
        event = q.get("event", [""])[0]
        ip = self.client_address[0]
        PEERS.setdefault(info_hash, set()).add((ip, port))
        compact = b"".join(
            socket.inet_aton(pip) + pport.to_bytes(2, "big")
            for (pip, pport) in PEERS[info_hash]
        )
        log(f"announce from {ip}:{port} event={event or '-'} peers={len(PEERS[info_hash])}")
        body = benc({b"interval": 30, b"complete": 1, b"incomplete": 1, b"peers": compact})
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    log(f"START tracker on 127.0.0.1:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
