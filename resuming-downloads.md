# Resuming Downloads

Outcome: a download that is cut off —
laptop closed, connection dropped,
process killed — can be finished later
without fetching the completed part
again, and you can point at the small
file that makes it possible.

## The experiment

The lab started the 4 MiB file at a
capped speed so the interruption would
land mid-download, then killed the
process the unceremonious way. From
transcript
`aria2-lab/transcripts/t03-resume.txt`:

```text
$ aria2c --max-download-limit=256K http://127.0.0.1:8377/bigfile.bin &
$ sleep 5; kill 65723
10/28 18:20:22 [NOTICE] Downloading 1 item(s)
10/28 18:20:28 [NOTICE] Emergency shutdown sequence commencing...
10/28 18:20:28 [NOTICE] Download GID#1bbc32... not complete: /home/.../bigfile.bin

$ ls -la
-rw-rw---- 1 root root 1071104 bigfile.bin
-rw-rw---- 1 root root      59 bigfile.bin.aria2
```

Two files remain. `bigfile.bin` holds
the bytes fetched so far — about one
megabyte of the four. `bigfile.bin.aria2`,
all 59 bytes of it, is the **control
file** from chapter 2: the record of the
file's total size, its piece size, and
which pieces are already complete.

The resume is the same address with one
flag added, `-c` (`--continue`):

```text
$ aria2c -c http://127.0.0.1:8377/bigfile.bin
...
ccefbd|OK  |    56MiB/s|/home/.../bigfile.bin

$ ls -la
-rw-rw---- 1 root root 4194304 bigfile.bin

$ sha256sum bigfile.bin
7213df7e265412054c3cbcc23f9b592f5e3d61347d35f602946499fc483c9862  bigfile.bin
```

aria2 read the control file and asked
the server only for what was missing —
the server's log shows the request as
`Range=bytes=1064960-4194303`, starting
a few kilobytes *before* the 1,071,104
bytes on disk: a half-written piece is
fetched again from its boundary, never
trusted. On completion aria2 deleted
the control file —
its disappearance is your confirmation
that nothing remains outstanding. The
hash, matching the fixture's known
SHA-256, is the proof that resumed and
uninterrupted downloads end at the same
bytes.

## The rules of the game

- **Without `-c`, a repeated command
  does not resume.** It starts a new
  download, and since the name is taken
  it renames the result (`hello.1.txt`,
  chapter 4) — leaving the half-finished
  file and its control file still
  sitting there. `-c` is what turns a
  restart into a continuation.
- **The control file is the memory.**
  Delete `bigfile.bin.aria2` and the
  record is gone; the partial file
  becomes an anonymous lump aria2 will
  not trust or reuse for HTTP downloads.
  Housekeeping scripts that sweep up
  "stray" files should leave `.aria2`
  files alone — or accept that they are
  cancelling downloads.
- **Resuming needs the server's help.**
  Exactly like segmentation (chapter 5),
  continuing an HTTP download means
  asking for a byte range. Against a
  server without Range support there is
  nothing to resume *with*; the download
  restarts from zero. BitTorrent does
  not have this problem — pieces and
  their hashes are the protocol's own
  idea.
- **A queue can resume too.**
  `--save-session` writes unfinished
  tasks to a file as aria2 exits; the
  session transcript
  (`aria2-lab/transcripts/t10-session.txt`)
  shows a killed download restarted from
  its session file, keeping even its
  speed cap and its GID, because the
  session format is the input-file format
  of chapter 8 with the options written
  back in.

## A note on capped speeds, while they are here

The `--max-download-limit=256K` used to
slow this experiment down is worth
knowing in its own right: it caps this
download's speed (K means KiB per
second; M and G work too), so a large
fetch can share a connection with the
rest of the household. The lab also ran
a full download at a 512K cap as
transcript
`aria2-lab/transcripts/t04-rate-limit.txt`:
the results table reported an average of
**508KiB/s**, and the clock said 8.1
seconds for 4 MiB — the cap is a cap on
the average the whole download runs at,
not a suggestion. `--max-overall-download-limit`
does the same for all of a run's tasks
together, which is the version you want
alongside chapter 8's lists.
