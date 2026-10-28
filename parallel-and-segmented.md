# Parallel and Segmented Downloads

Outcome: you can make one file arrive
over several connections at once, you can
prove from the *server's* log that it
really happened, and you know the
condition the whole trick depends on —
and what aria2 does, silently, when the
condition is missing.

## Two kinds of "at once"

aria2 parallelises in two different
directions, and the options are easy to
confuse:

- **Several downloads at once** —
  `-j N`, `--max-concurrent-downloads`.
  Whole tasks run side by side. This is
  the setting for chapter 8's lists; the
  default is 5.
- **One download in several pieces** —
  `-s N` splits a file into N **segments**,
  and `-x N` allows up to N connections to
  one server. Together they fetch the
  segments simultaneously and stitch them
  into place. `-k` sets the smallest
  segment aria2 will bother making
  (default 20 MiB, which is why small
  files never split; the lab passes
  `-k1M` for its 4 MiB file).

Why split one file at all? Because many
servers limit the speed of a single
connection, not the speed of a customer.
Four connections can each be allowed the
per-connection rate. And in BitTorrent
the same machinery is not an optimisation
but the design: the pieces *live* on
different machines (chapter 9).

One more source of pieces: **mirrors**.
Give one command several addresses that
all serve *the same file*, and aria2
treats them as one download with several
sources to draw segments from. Hold that
thought — chapter 8 shows what happens
when the addresses are different files
and aria2 cannot know.

## The segmented download, proven

From transcript
`aria2-lab/transcripts/t02-segmented.txt`,
fetching the lab's 4 MiB file in four
1 MiB segments:

```text
$ aria2c -x4 -s4 -k1M http://127.0.0.1:8377/bigfile.bin

10/28 18:20:08 [NOTICE] Download complete: /home/.../bigfile.bin

5fa271|OK  |   100MiB/s|/home/.../bigfile.bin
```

aria2's own output does not say how many
connections it used — on loopback the
file arrives before the progress lines
even settle. The proof is on the other
side, in the practice server's log, which
records the **Range** header of every
request (a Range request asks for one
slice of a file, by byte numbers):

```text
GET /bigfile.bin Range=- -> 200 bytes 0-4194303
GET /bigfile.bin Range=bytes=2097152-3145727 -> 206 bytes 2097152-3145727
GET /bigfile.bin Range=bytes=1048576-2097151 -> 206 bytes 1048576-2097151
GET /bigfile.bin Range=bytes=3145728-4194303 -> 206 bytes 3145728-4194303
```

Four connections; the last three ask
explicitly for the second, third and
fourth megabytes (reply code **206**,
"partial content"), while the first
connection asks for the file plainly and
takes the opening megabyte from the
front of the stream. The downloaded file's
SHA-256 matched the original exactly —
the stitching is invisible in the result.

Against a remote server you cannot read
the log, so judge by the progress line
instead: during a segmented download its
**CN** count rises above 1.

## The condition: the server must play

Segmentation — and resuming, chapter 6 —
stands entirely on Range requests. If
the server ignores or refuses them, the
pieces cannot be fetched separately.
Here is the same command against Python's
built-in server, which does not support
Range (transcript
`aria2-lab/transcripts/t02b-no-range-server.txt`):

```text
$ aria2c -x4 -s4 http://127.0.0.1:8378/bigfile.bin
...
0bf237|OK  |   114MiB/s|/home/.../bigfile.bin
```

Stat `OK`, correct hash, no complaint —
and **no segmentation happened**. aria2
quietly fell back to one ordinary
download. Nothing in the default output
tells you the `-x4 -s4` was ignored; only
the CN count staying at 1, or the
server's log, gives it away. This is the
chapter's real lesson: with aria2,
*asking* for parallelism and *getting* it
are different events, and the tool will
not always announce the difference. When
a big download will not speed up or will
not resume, suspect the server's Range
support first (chapter 14).

Two courtesies before you reach for `-x`:
some servers limit connections per
customer and treat a burst of them as
abuse, and every extra connection is
load somebody pays for. Four is a sane
default appetite; sixteen is a statement
you should mean.
