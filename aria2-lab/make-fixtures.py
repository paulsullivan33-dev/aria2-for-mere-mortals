#!/usr/bin/env python3
"""Regenerate the lab's fixture files.

Usage: make-fixtures.py TARGET_DIR

Creates hello.txt, notes.txt, data.csv and bigfile.bin (exactly
4 MiB of a repeating sentence, so its SHA-256 is stable and known)
in TARGET_DIR, and prints their SHA-256 hashes. Serve the folder
with server/range_server.py while working through the guide.
"""

import hashlib
import os
import sys

TARGET = sys.argv[1]
os.makedirs(TARGET, exist_ok=True)

files = {
    "hello.txt": (
        "Hello from the aria2 lab.\n"
        "This small file is the first download.\n"
        "It is meant to be fetched, read, and fetched again.\n"
    ),
    "notes.txt": (
        "Field notes, day one.\n"
        "The kettle took four minutes.\n"
        "The path by the river was clear.\n"
    ),
    "data.csv": "item,quantity,price\napples,12,0.50\npears,6,0.75\nplums,20,0.30\n",
}

for name, text in files.items():
    with open(os.path.join(TARGET, name), "w") as fh:
        fh.write(text)

pattern = b"The quick brown fox jumps over the lazy dog. 0123456789\n"
block = pattern * (1024 * 1024 // len(pattern) + 1)
data = (block * 4)[: 4 * 1024 * 1024]
with open(os.path.join(TARGET, "bigfile.bin"), "wb") as fh:
    fh.write(data)

for name in sorted(os.listdir(TARGET)):
    path = os.path.join(TARGET, name)
    with open(path, "rb") as fh:
        print(hashlib.sha256(fh.read()).hexdigest(), name)
