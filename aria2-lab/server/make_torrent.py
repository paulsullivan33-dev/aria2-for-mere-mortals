#!/usr/bin/env python3
"""Build a .torrent file for one lab fixture.

Usage: make_torrent.py FILE TRACKER_URL OUT.torrent [PIECE_LENGTH]
"""

import hashlib
import sys

FILE = sys.argv[1]
TRACKER = sys.argv[2]
OUT = sys.argv[3]
PIECE = int(sys.argv[4]) if len(sys.argv) > 4 else 262144


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


data = open(FILE, "rb").read()
pieces = b"".join(
    hashlib.sha1(data[i : i + PIECE]).digest() for i in range(0, len(data), PIECE)
)
import os

info = {
    b"name": os.path.basename(FILE).encode(),
    b"length": len(data),
    b"piece length": PIECE,
    b"pieces": pieces,
}
torrent = {b"announce": TRACKER.encode(), b"info": info}
with open(OUT, "wb") as fh:
    fh.write(benc(torrent))
print(f"wrote {OUT}: {len(data)} bytes, {len(pieces) // 20} pieces of {PIECE}")
