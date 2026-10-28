# Metalink and Torrents

Outcome: you can hand aria2 a file that
*describes* a download instead of the
download itself — and get verification
thrown in — and you understand what a
torrent adds: many sources, and duties
as well as downloads.

## Metalink: the self-describing download

A **Metalink** file (suffix `.meta4`)
is a small XML document that names a
file, its size, its hash, and one or
more addresses it can be fetched from.
The lab's, written by hand for
`hello.txt` and kept at
`aria2-lab/hello.txt.meta4`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metalink xmlns="urn:ietf:params:xml:ns:metalink">
  <file name="hello.txt">
    <size>117</size>
    <hash type="sha-256">90ad06db...</hash>
    <url>http://127.0.0.1:8377/hello.txt</url>
  </file>
</metalink>
```

Hand aria2 the Metalink's address and
two downloads happen (transcript
`aria2-lab/transcripts/t08-metalink.txt`):

```text
$ aria2c http://127.0.0.1:8377/hello.txt.meta4

d46336|OK  |   10KiB/s|/home/.../hello.txt.meta4
c146d6|OK  |   2.1KiB/s|/home/.../hello.txt
```

First the little XML file itself, then
the file it describes — and between
them, the line chapter 7 taught you to
want:

```text
[NOTICE] Verification finished successfully. file=/home/.../hello.txt
```

Nobody passed `--checksum`. The hash
rode inside the Metalink, so checking
was automatic. The lab proved the check
was real by serving a second Metalink
with four digits of the hash replaced
by zeros: the download fetched the file,
compared, and failed it — `Checksum
error detected`, exit 32, exactly as in
chapter 7. This is why projects that
publish large files like Metalink: the
description, the mirrors and the proof
travel together, so a downloader cannot
forget to check.

## Torrents: the swarm is the server

A `.torrent` file describes a download
the way a Metalink file does, with one
difference that changes everything:
among its fields is the address of a
**tracker**, a rendezvous service that
knows who else is fetching or offering
this file — the **swarm**. Instead of
one server there are **peers**, each
holding some **pieces** of the file,
each piece named in the torrent by its
SHA-1 hash. A downloader collects
pieces from whoever offers them, checks
each against its hash, and — this is
the social contract of the protocol —
uploads the pieces it has to peers who
need them, while it downloads and,
usually, for a while after.

The lab built the smallest honest swarm
that exhibits all of this: one file,
two aria2 instances, and a tracker
written for the purpose
(`aria2-lab/server/tracker.py`, about
eighty lines), because no public swarm
was going to be joined for a textbook
exercise. A third small script
(`aria2-lab/server/make_torrent.py`)
wrote the `.torrent`: 4 MiB in sixteen
256 KiB pieces.

**The seeder's lesson came first.** An
aria2 started on the torrent in a
folder already holding the complete
file refused to move:

```text
errorCode=13 File .../bigfile.bin exists, but a control
file(*.aria2) does not exist. Download was canceled in
order to prevent your file from being truncated to 0.
```

Read it as the compliment it is: aria2
cannot tell a finished file from a
half-finished one by looking, and it
will not risk destroying the former
while pretending to fetch the latter.
The seeder's flag is
`--bt-seed-unverified=true` — "this
file is complete; seed it without
re-checking every piece" — and with it
the seeder announced itself to the
tracker and listened on port 6881.

**Then the leecher.** A second aria2,
in an empty folder, given the same
torrent:

```text
$ aria2c ../../../bigfile.torrent --listen-port=6882 \
    --enable-dht=false --enable-peer-exchange=false --bt-enable-lpd=false
[#0a93c2 0B/4.0MiB(0%) CN:2 SD:0 DL:0B]
[#0a93c2 SEED(0.0) CN:1 SD:0]
```

On loopback the pieces crossed faster
than the once-a-second progress lines
could narrate: the second line already
reads **SEED** — the leecher had the
whole file and had become a seeder
itself. The evidence is on three sides
(transcript
`aria2-lab/transcripts/t09-torrent.txt`):
the tracker's log shows the leecher's
`announce ... event=completed`; the
seeder's results report `uploaded/
downloaded=4.0MiB/4.0MiB` and *"Seeding
is over"*; and the leecher's file
matches the fixture's SHA-256.

Two seed behaviours to carry away:

- **A finished torrent keeps seeding.**
  The lab's leecher sat at SEED until
  it was stopped by hand. `--seed-time`
  (minutes) and `--seed-ratio` bound
  the duty: the seeder above exited by
  itself when its ratio reached 1.0 —
  it had uploaded as much as it held.
  A download you obtained from a swarm
  was paid for by strangers' seeding;
  the ratio you choose is how much of
  that courtesy you return.
- **Discovery was switched off here, on
  purpose.** Real swarms find peers
  through trackers and also through
  **DHT** (a peer-run directory),
  **peer exchange**, and **local peer
  discovery** — all disabled in the lab
  so that the tracker exchange stayed
  visible and nothing left the machine.
  On a real network you would leave
  them on; the lab's arrangement is a
  dissection, not a recommendation.

**Magnet links** are the torrent idea
with the description shrunk to a hash:
a `magnet:` address names the content,
and the peer machinery fetches the full
description from the swarm itself.
aria2 accepts them anywhere it accepts
an address. The lab did not run one —
there was no swarm to ask — and the
text does not pretend otherwise; the
mechanics after the description arrives
are the ones this chapter demonstrated.
