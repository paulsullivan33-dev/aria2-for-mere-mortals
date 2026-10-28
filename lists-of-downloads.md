# Lists of Downloads

Outcome: one command works through a
whole list of addresses, each landing in
its own folder under its own name — and
you are wise to the single most
surprising sentence in aria2's manual,
which this chapter demonstrates before
it explains.

## The trap, demonstrated

Two addresses, two different files —
what would you expect this to fetch?

```text
$ aria2c http://127.0.0.1:8377/hello.txt http://127.0.0.1:8377/notes.txt

10/28 18:21:14 [NOTICE] Downloading 1 item(s)
10/28 18:21:14 [NOTICE] Download complete: /home/.../hello.txt
```

**One item.** It fetched `hello.txt`,
and `notes.txt` was never downloaded —
it was treated as a *mirror*: another
address for the same file, to be drawn
on if the first source faltered
(chapter 5's mirror behaviour). On the
command line, several addresses mean
several *sources for one file*. aria2
has no way to know you meant two
different files — the addresses say
nothing about their contents — so the
manual's rule is absolute, and this
guide's lab confirmed it the puzzling
way first (transcript
`aria2-lab/transcripts/t06-input-file.txt`).

Two honest ways to fetch several
different files follow.

## Sequentially: `-Z`

`-Z` (`--force-sequential`) re-reads the
command line the way you meant it: each
address a separate download, taken in
order.

```text
$ aria2c -Z http://127.0.0.1:8377/hello.txt http://127.0.0.1:8377/notes.txt

10/28 18:21:20 [NOTICE] Downloading 2 item(s)
```

Two items, both completed. `-Z` is the
quick fix for a handful of files pasted
onto one command line.

## Properly: the input file

For anything longer-lived than a paste,
addresses belong in a text file, read
with `-i`. The format is one address
per line, and — the part that makes the
format worth learning — any line that
starts with whitespace is a list of
**options for the address above it**.
The lab's `aria2-lab/urls.txt`:

```text
http://127.0.0.1:8377/notes.txt
  out=notes-copy.txt
http://127.0.0.1:8377/data.csv
  dir=spreadsheet
```

Running it (same transcript):

```text
$ aria2c -i urls.txt

10/28 18:21:14 [NOTICE] Downloading 2 item(s)
10/28 18:21:14 [NOTICE] Download complete: spreadsheet/data.csv
10/28 18:21:14 [NOTICE] Download complete: /home/.../notes-copy.txt

$ find . -type f | sort
./notes-copy.txt
./spreadsheet/data.csv
./urls.txt
```

Each file landed where its own options
sent it: `notes.txt` renamed to
`notes-copy.txt`, `data.csv` filed
under `spreadsheet/`. Nearly every
`aria2c` option has an input-file
spelling — `out=`, `dir=`,
`max-download-limit=`, `checksum=` —
so a list can encode a whole fetching
policy: this file slowly, that file
only if its hash matches, these three
into the archive folder. Options on the
command line apply to every entry;
options in the file apply to one.

By default aria2 works through the list
**five downloads at a time** (`-j`,
chapter 5) — polite to servers and to
your own connection, and worth lowering
to 1 or 2 for a small server, or raising
when the list is long and the sources
are strangers to each other.

## Sessions: the list that writes itself

Chapter 6 mentioned `--save-session`;
here is its place in the story. Run a
list with it:

```bash
aria2c --save-session=session.txt -i urls.txt
```

and whenever aria2 exits — finished,
interrupted, killed — the tasks that
did *not* finish are written to
`session.txt` in input-file format,
options included. The lab's session
file, after its download was killed
five seconds in (transcript
`aria2-lab/transcripts/t10-session.txt`):

```text
http://127.0.0.1:8377/bigfile.bin
 gid=8770cd96ca35d77d
 max-download-limit=262144
```

Restarting is feeding it back:
`aria2c -i session.txt -c`. The
download resumed, still capped at the
256K it started with — 262144 bytes, as
the file plainly says — and still
answering to its original GID. A cron
job that runs `aria2c -i session.txt`
nightly is, in effect, a download queue
that survives reboots; several tools in
chapter 12's neighbourhood are exactly
that idea with a nicer face.
