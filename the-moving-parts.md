# The Moving Parts

aria2 has fewer pieces than most tools
that do this much, and one idea explains
most of them: **a download is a task, not
a command.** You describe tasks; aria2
works through them, remembers their
state, and reports how each one ended.

## The one command

Everything is `aria2c`. In its simplest
shape it takes an address and downloads
it into the current folder. Its options —
there are hundreds — fall into families
this guide meets chapter by chapter:
where files go (`-d`, `-o`), how hard it
pulls (`-x`, `-s`, `-j`,
`--max-download-limit`), how it proves
what arrived (`--checksum`), and how it
behaves as a service (`--enable-rpc`).
Options can also live in a configuration
file, `~/.config/aria2/aria2.conf`, one
`name=value` per line, which is where
settings you always want belong.

## Tasks, GIDs, and the results table

Each download gets a **GID**, a short hex
identifier (`fcfa56`, `851978`). While
aria2 runs it prints progress lines keyed
by that GID; when it finishes, every run
ends with the same **results table**:

```text
Download Results:
gid   |stat|avg speed  |path/URI
======+====+===========+=================
fcfa56|OK  |   3.1KiB/s|.../hello.txt

Status Legend:
(OK):download completed.
```

The table is the contract. `OK` means
the file is complete and — if you gave a
hash — verified. `ERR` means it is not,
and the command's **exit code** then
equals aria2's numeric error code for
what went wrong: 3 for "resource not
found", 32 for a checksum failure, 1 for
a connection that could not be made
(chapters 7 and 14 show all three). A
script does not need to parse aria2's
prose; the exit code and the table say
enough. Note what the table does *not*
promise: an `ERR` download may still
leave a file on disk — the partial
download, kept deliberately so it can be
resumed. A file's presence is not proof
of its completeness; the hash is
(chapter 7).

## Pieces and connections

aria2 does not treat a file as one
indivisible stream. It divides work into
**pieces** and can fetch different pieces
over different **connections** at the
same time — from several mirrors of the
same file, or from one server that
supports Range requests, or, in
BitTorrent, from several peers, which is
where the idea comes from. How many
connections a server will tolerate, and
how small a piece may be, are options
(`-x`, `-s`, `-k`); chapter 5 shows the
server's side of a four-way split.

## The control file

Next to an unfinished download aria2
keeps a small file with the same name
plus `.aria2` — the **control file**. It
records the file's size, the piece size,
and a bitmap of which pieces are already
safely on disk. It is the whole secret of
resuming: with the control file present,
`aria2c -c` asks the server only for the
pieces that are missing. When a download
completes, the control file is deleted —
so a `.aria2` file sitting in a folder is
a reliable sign of an unfinished
download, and deleting one deliberately
throws away the record of what was done.
Chapter 6 interrupts a real download and
reads the evidence.

## Input files and sessions

Addresses can come from a text file
(`-i`), one per line, each optionally
followed by its own indented options —
name, folder, speed cap, hash. That file
format does double duty: with
`--save-session`, aria2 writes the
*unfinished* tasks, with their options,
to a file in the same format as it shuts
down. Feeding that file back with `-i`
on a later run is how a whole queue
survives a reboot or a closed laptop
(chapter 8).

## The service face

Started with `--enable-rpc`, the same
engine stays running and listens — by
default only on this machine — for
JSON-RPC calls: add a download, ask its
status, pause it, remove it, shut the
engine down. Nothing about the downloads
changes; what changes is who is giving
the orders. A program, a script, or a web
interface running in your browser can
drive aria2 the way you drive it from
the keyboard (chapter 10).

## Who holds what, when it breaks

- The **server** decides whether a
  download can be split or resumed at
  all: no Range support, no segments —
  and aria2 falls back silently, which
  chapter 5 demonstrates.
- The **control file** holds the memory.
  Lose it and a 90%-done file starts over
  or, in BitTorrent's case, refuses to
  move at all (chapter 14).
- The **results table and exit code**
  hold the verdict; a file merely
  existing holds nothing.
- In BitTorrent, the **tracker** (or the
  discovery machinery) holds the list of
  who has the pieces; the pieces
  themselves are checked against hashes
  in the `.torrent` file, so a helpful
  stranger cannot hand you a poisoned
  piece without it being caught.
