# What aria2 Is

A download sounds like the simplest job a
computer does: a file lives on a server,
you want it here, copy it. The trouble
starts with everything around that simple
sentence. The connection drops at 90%.
The server is slow and the file is huge.
You have forty files to fetch, not one.
The file arrives and you cannot tell
whether it arrived *whole*. **aria2** is
a program built for the trouble around
the copy. You give it addresses; it does
the fetching — patiently, in parallel,
and with a memory of what it has already
done.

aria2 speaks several download **protocols**
in one tool:

- **HTTP and HTTPS** — the web's way of
  serving files, and the one this guide
  exercises most.
- **FTP** — the older file-transfer
  protocol, still common on mirror sites.
- **BitTorrent** — the peer-to-peer
  protocol, where a file comes from many
  people's machines at once, including
  **magnet links**.
- **Metalink** — not a way of moving bytes
  but a small XML file that *describes* a
  download: its name, its size, its
  hashes, and a list of places it can be
  fetched from.

One command, `aria2c`, drives all of it.
The same habits apply across protocols:
split one file across several
connections, stop a download and resume
it later, cap the speed so a big fetch
does not flatten the household network,
and verify a cryptographic **hash** of
what arrived before trusting it.

## Why not just use the browser, or curl?

Often you should, and chapter 12 compares
the neighbours honestly. aria2 earns its
place in three situations:

1. **The download is fragile.** A two-hour
   fetch on a flaky connection is a
   different problem from a two-second
   one. aria2 keeps a small **control
   file** next to a partial download that
   remembers which pieces are done, so an
   interrupted transfer resumes where it
   stopped instead of starting over
   (chapter 6).
2. **The download is plural.** A list of
   addresses in a text file, each with
   its own name and folder, fetched with
   one command and a concurrency limit
   (chapter 8). Or one file fetched from
   several mirrors at once.
3. **The download is delegated.** aria2
   can run as a background service and
   take orders over a **remote procedure
   call (RPC)** interface: another program
   hands it an address, asks how the
   download is going, and collects the
   result (chapter 10). It is a download
   engine other tools can drive.

A rule of thumb: if a person will sit and
watch the progress bar, anything works.
aria2 is for the downloads nobody wants
to sit and watch.

## The lab, and the rule it followed

This guide was written against the real
program: **aria2 1.37.0**, run against a
small file server on the same machine, on
loopback addresses that never leave the
machine. The server was written for this
guide (`aria2-lab/server/range_server.py`)
because the obvious practice server,
Python's built-in one, cannot answer the
**Range** requests that segmented and
resumed downloads depend on — a gap the
lab demonstrated rather than assumed
(chapter 5). Against that server the lab
ran single downloads, a four-way
segmented download proven from the
server's own log, an interrupted download
resumed to the byte, a speed-capped
download, hash checks that pass and hash
checks that fail, a two-file list with
per-file options, a Metalink download
verified by the hash inside the Metalink
file, and a two-machine BitTorrent swarm
assembled from parts the lab also wrote:
a seed, a leech, and a minimal tracker.
Chapter 10 ran aria2 as a background
service and drove it with real RPC calls.

What the lab did not do, it did not fake.
It never joined a public swarm, never
used the peer-discovery machinery
(**DHT**, peer exchange, local peer
discovery — all switched off in the lab,
on purpose), never downloaded over FTP,
and never fetched from the public
internet; `criteria.md` keeps the full
ledger. Download only what you have the
right to download, from places you have
the right to download it from — that is
not a condition of this guide's lab, it
is a condition of using the tool.
