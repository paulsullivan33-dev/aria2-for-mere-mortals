# aria2 for Mere Mortals

A download sounds like the simplest job
a computer does: a file lives on a
server, you want it here, copy it. The
trouble is everything around the copy —
the connection that drops at 90%, the
server that caps a single connection to
a trickle, the forty files that all
need fetching, the file that arrives
and cannot be proved whole. **aria2**
is a command-line download program
built for the trouble around the copy.
One command, `aria2c`, speaks HTTP,
HTTPS, FTP, BitTorrent and Metalink,
and applies the same ideas to all of
them: fetch several files at once,
split one file across several
connections, resume what stopped, cap
the speed, and verify a cryptographic
hash of what arrived.

This guide explains how that works, how
to take your first download against a
practice server on your own machine,
how to make one file arrive in pieces
and prove — from the server's own log —
that it did, how an interrupted
download is resumed from the small
control file aria2 keeps beside it, and
how to check a download against its
published hash. It then works through
the plural cases: lists of addresses
with per-file options, sessions that
survive being killed, Metalink files
that carry their own hashes, a
two-machine BitTorrent swarm built
from parts you can read, and aria2
running as a background service that
other programs drive over RPC.

The lab behind this guide ran the real
thing: **aria2 1.37.0**, from its
distribution package, against a
small file server written for the
purpose — because the obvious practice
server cannot answer the Range requests
that segmented and resumed downloads
depend on, a gap the guide demonstrates
rather than assumes. Against that
server the lab ran single and
segmented downloads, an interrupted
download resumed to the byte, speed
caps measured against the clock, hash
checks that pass and hash checks that
fail, and an RPC daemon driven with
real calls. The BitTorrent chapters
were run against a swarm assembled on
the same machine from a hand-made
torrent, a hand-written tracker, a seed
and a leech, with the wider internet's
peer-discovery machinery switched off.

What the lab could not do, it did not
fake. It never joined a public swarm,
never downloaded over FTP, and never
fetched from the public internet; the
downloads it ran are the lab talking
to itself, on loopback. Those limits —
and the tool's own, including the
cheerful fact that a failed download
leaves its file on disk for you to
mistake for a good one — are stated in
the text and kept as a ledger in
`criteria.md`.

## What this guide covers

- [**What aria2 is**](what-aria2-is.md) —
  the mental model: a download engine
  for fragile, plural and delegated
  downloads, and the protocols it speaks
- [**The moving parts**](the-moving-parts.md) —
  tasks and GIDs, the results table and
  exit codes, pieces and connections,
  the control file, input files and
  sessions, the service face
- [**Installing aria2**](installing-aria2.md) —
  the distribution package on Linux (and
  why there is no official Linux build),
  the version page and its feature list
- [**Your first download**](your-first-download.md) —
  a practice server, a first fetch read
  line by line, and placing files with
  `-d` and `-o`
- [**Parallel and segmented downloads**](parallel-and-segmented.md) —
  several downloads at once versus one
  download in pieces, proven from the
  server's log, and the Range support
  the whole trick stands on
- [**Resuming downloads**](resuming-downloads.md) —
  the control file at work: interrupt,
  resume with `-c`, and the rules of the
  game; speed caps measured
- [**Checking what arrived**](checking-what-arrived.md) —
  `--checksum` and the verified
  download, the checksum failure with
  its exit code 32, and why a file's
  presence proves nothing
- [**Lists of downloads**](lists-of-downloads.md) —
  the mirror trap, `-Z`, input files
  with per-file options, and sessions
  that write themselves
- [**Metalink and torrents**](metalink-and-torrents.md) —
  downloads that describe themselves,
  and a working swarm: tracker, seed,
  leech, and the seeder's refusal that
  teaches the rules
- [**The RPC interface**](the-rpc-interface.md) —
  aria2 as a background service: adding
  downloads, asking their status, the
  secret that guards it, the graceful
  shutdown
- [**Recipes**](recipes.md) — overnight
  downloads, verified release lists,
  mirror races, a standing download
  box, seeding with a promised ratio
- [**The neighbours**](the-neighbours.md) —
  curl and wget, the browser, yt-dlp,
  rsync, dedicated torrent clients:
  what each does that aria2 doesn't
- [**Limits**](limits.md) — addresses
  not meanings, servers that won't
  play, hashes and the trust they can't
  carry, and etiquette as a limit
- [**Troubleshooting**](troubleshooting.md) —
  the failure table by exit code: not
  found, refused, the one-file-of-two,
  the split that never happens, the
  control file that will not die
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Getting files you have no right to, or
evading the limits of services you use:
aria2's power to open many connections
is taught with its etiquette attached.
Site-specific downloading — the kind
that needs an account, a form, or
knowledge of one website's insides —
belongs to other tools, and chapter 12
says which. Running aria2 as shared,
multi-user infrastructure is pointed
at, not taught; its security model is
one secret on one machine, and this
guide keeps it there.

## How to use this guide

Read chapters 1 and 2 first: the task
model and the control file explain
nearly every surprise later. Chapter 4
takes your first download against the
lab server in the same sitting as the
install. Chapters 5 through 8 are the
everyday craft — split, resume, verify,
list — and each ends in a check you
can run. Chapters 9 and 10 are the two
second halves of the tool, torrents
and the service face; neither is
required for the other. The lab's
transcripts live in
`aria2-lab/transcripts/`; its servers
are `aria2-lab/server/`; its fixture
maker is `aria2-lab/make-fixtures.py`;
everyday commands are collected in
`examples/commands.txt`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [curl for Mere Mortals](https://paulsullivan33-dev.github.io/curl-for-mere-mortals/)
- [yt-dlp for Mere Mortals](https://paulsullivan33-dev.github.io/yt-dlp-for-mere-mortals/)
- [rsync for Mere Mortals](https://paulsullivan33-dev.github.io/rsync-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/aria2-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/aria2-for-mere-mortals/blob/main/LICENSE-CODE).
