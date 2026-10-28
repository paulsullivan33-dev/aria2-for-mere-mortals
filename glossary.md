# Glossary

**aria2c** — the aria2 program itself;
one command-line tool that downloads
over HTTP, HTTPS, FTP, BitTorrent and
Metalink.

**Checksum** — see *hash*. The
`--checksum=sha-256=...` option makes
aria2 verify a download against a
given hash and fail it (exit code 32)
if the bytes disagree.

**Concurrency (`-j`)** — how many
downloads run at once from a list or
queue. Distinct from connections per
download (`-x`).

**Connection** — one open channel to a
server or peer. A segmented download
uses several at once, each carrying a
different piece.

**Control file** — the small
`<name>.aria2` file kept beside an
unfinished download, recording its
size, piece size, and which pieces are
complete. The memory that makes
resuming possible; deleted when the
download completes.

**Daemon** — a program that stays
running in the background, taking work
from others. aria2 with
`--daemon=true` and `--enable-rpc` is
one.

**DHT (Distributed Hash Table)** — the
trackerless way BitTorrent peers find
each other: a directory the peers
themselves maintain. Switched off in
this guide's lab.

**Exit code** — the number a program
hands back to whatever ran it. aria2
exits 0 when all downloads succeed,
and with the specific error code (3,
13, 32, ...) of the failure when they
do not.

**GID** — a download's identifier, a
short hex string (`fcfa56`). Progress
lines, results tables and RPC calls
all refer to downloads by GID.

**Hash** — a fixed-length fingerprint
computed from a file's bytes (SHA-256
is the one this guide uses). Any
change to the bytes changes the
fingerprint, so a matching hash proves
an unchanged file.

**Input file** — a text file of
addresses, read with `-i`, where
indented lines under an address set
that download's options. Session files
use the same format.

**Magnet link** — a `magnet:` address
that identifies content by its hash
alone; the full torrent description is
fetched from the swarm itself.

**Metalink** — an XML file (`.meta4`)
describing a download: name, size,
hashes, and one or more source
addresses. aria2 verifies against the
enclosed hashes automatically.

**Mirror** — another address serving
the same file. Several addresses on
one command line are treated as
mirrors of a single download, not as
separate downloads.

**Peer** — another participant in a
BitTorrent swarm, downloading and
uploading pieces at the same time.
A peer with the complete file is a
**seed**; one still fetching is a
**leech**.

**Piece** — the unit a file is divided
into for parallel and peer-to-peer
downloading. BitTorrent pieces are
named in the torrent by their SHA-1
hashes and checked as they arrive.

**Range request** — an HTTP request
for one byte-range of a file
(`Range: bytes=1048576-2097151`),
answered with status 206. Segmented
downloading and HTTP resuming both
stand on it.

**RPC (remote procedure call)** —
asking a running program to do
something by sending it a structured
message. aria2's JSON-RPC interface
lets other programs add downloads and
ask their status.

**Segment** — a contiguous slice of a
file as fetched over one connection;
`-s` sets how many a download is split
into, `-k` the smallest size worth
making.

**Session** — with `--save-session`,
the file aria2 writes on exit listing
the downloads that did not finish, in
input-file format, to be fed back with
`-i` later.

**Swarm** — all the peers sharing one
torrent, plus the tracker (if any)
that introduces them.

**Tracker** — the rendezvous service
named in a `.torrent` file: peers
announce themselves to it and receive
the list of the swarm.
