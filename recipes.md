# Recipes

Short answers to the shapes downloads
actually come in. Each assumes the
ideas of its chapter; the transcripts
behind them are in `aria2-lab/`.

## A big file, overnight, on a shared connection

Cap it, make it resumable, and let it
save its own progress:

```bash
aria2c -c --max-download-limit=1M \
  --save-session=session.txt \
  https://example.org/big-archive.tar
```

If the machine sleeps or the connection
drops, tomorrow's `aria2c -i session.txt
-c` picks it up. The `-c` and the
session together are belt and braces:
the session remembers the *task*, the
control file remembers the *pieces*
(chapters 6 and 8).

## A folder of release files, each verified

Publishers who offer a checksum per
file let you write the whole policy
into the input file (chapter 8):

```text
https://example.org/tool-2.1-linux.tar.gz
  dir=downloads
  checksum=sha-256=<the published hash>
https://example.org/tool-2.1-macos.tar.gz
  dir=downloads
  checksum=sha-256=<the published hash>
```

Run `aria2c -i list.txt` and read the
exit code before trusting anything in
`downloads/` — a single `ERR` row means
that file failed its fingerprint, and
chapter 7 explains why the file may be
sitting there anyway.

## The same file, from the fastest of three mirrors

One command line, three addresses, one
file (chapter 5's mirror rule):

```bash
aria2c -x4 \
  https://mirror-a.example.org/file.iso \
  https://mirror-b.example.org/file.iso \
  https://mirror-c.example.org/file.iso
```

aria2 draws segments from all three.
Add `--checksum` and the result is
verified regardless of which mirror
served which piece — the correct amount
of trust to place in a stranger's
server.

## A standing download box

On a machine that is always on, run
the service face (chapter 10) under
whatever your system uses to keep
services alive, with a configuration
file instead of a command line:

```text
# ~/.config/aria2/aria2.conf
enable-rpc=true
rpc-secret=<a real secret>
dir=/srv/downloads
max-overall-download-limit=2M
save-session=/srv/downloads/session.txt
input-file=/srv/downloads/session.txt
continue=true
```

From your laptop, any RPC client —
including a browser-based one — queues
the day's downloads to the box, and the
household network feels only the capped
2M. The `input-file`/`save-session`
pair means the queue itself survives
the box rebooting (chapter 8).

## Seeding something you published

You made a file; you want the swarm to
carry it. Make the torrent with any
torrent creator, then seed from the
folder holding the complete file
(chapter 9):

```bash
aria2c --bt-seed-unverified=true \
  --seed-ratio=2.0 release.torrent
```

`--seed-ratio=2.0` says the duty ends
after uploading twice the file's size
in total — a concrete promise, kept by
the program, not by your memory. Leave
the flag off only if you mean "forever,
or until I stop it".
