# Your First Download

Outcome: you have fetched a file with
aria2, read the results table it prints,
and can say from aria2's own output —
not from the file's presence — that the
download completed. Everything in this
chapter happens against the guide's
practice server, on your own machine.

## The lab setup

The guide's lab files live in
`aria2-lab/`. Make the fixtures and start
the server:

```bash
python3 aria2-lab/make-fixtures.py aria2-lab/fixtures
python3 aria2-lab/server/range_server.py aria2-lab/fixtures aria2-lab/server.log 8377 &
```

The server listens on
`http://127.0.0.1:8377/`. It serves four
small files: `hello.txt`, `notes.txt`,
`data.csv`, and `bigfile.bin`, exactly
4 MiB of a repeating sentence whose
SHA-256 hash the later chapters use. The
range server exists because the
convenient alternative, `python3 -m
http.server`, cannot answer Range
requests; if you would rather practise
against a real site you own or have
permission to use, every command in this
chapter works unchanged with its address
in place of the lab's.

## The download

```bash
aria2c http://127.0.0.1:8377/hello.txt
```

That is the whole command shape: the
program, then the address. aria2 works
out the file's name from the address and
fetches it into the current folder. From
transcript `aria2-lab/transcripts/t01-first-download.txt`:

```text
$ aria2c http://127.0.0.1:8377/hello.txt

10/28 18:20:04 [NOTICE] Downloading 1 item(s)

10/28 18:20:04 [NOTICE] Download complete: /home/.../hello.txt

Download Results:
gid   |stat|avg speed  |path/URI
======+====+===========+========================
45cc90|OK  |   2.4KiB/s|/home/.../hello.txt

Status Legend:
(OK):download completed.
```

Three things to notice:

- **`Downloading 1 item(s)`** — aria2
  counts *tasks*, and says how many it
  has. Remember this line; chapter 8
  turns on a case where it says 1 when
  you expected 2.
- **The NOTICE lines are the diary** —
  timestamped, and prefixed with the log
  level. Errors later in the guide appear
  the same way, marked `[ERROR]`.
- **The results table is the verdict** —
  `OK`, an average speed, and where the
  file landed. On a real run the path is
  the full absolute path; it is shortened
  here and in later chapters.

Check: the file itself agrees.

```text
$ cat hello.txt
Hello from the aria2 lab.
This small file is the first download.
It is meant to be fetched, read, and fetched again.
```

In the lab's transcripts you will also
see the lab's own paths (its scratch
folder, its dates). Your paths and dates
will differ; the shape will not.

## Placing the file: `-d` and `-o`

`aria2c -d receipts -o march-invoice.pdf
<address>` puts the download in the
`receipts` folder under that name,
creating the folder if it is missing.
Two habits are worth forming early:

- **Name things at download time.**
  Servers name files for themselves
  (`download?id=8123` is not a name you
  will recognise in a month); `-o` names
  them for you.
- **Fetch into a scratch folder first**
  when the source is unfamiliar, and move
  the file once chapter 7's checks have
  passed. And know what happens when the
  name is taken: by default aria2 does
  *not* overwrite. It renames the new
  download, slipping a number in before
  the extension (transcript
  `aria2-lab/transcripts/t11-second-copy.txt`):

```text
[NOTICE] File already exists. Renamed to /home/.../hello.1.txt.
```

  `--allow-overwrite=true` changes that
  to genuine replacement — a setting to
  reach for deliberately, not by habit.

One more piece of reading fluency: on a
download that takes more than a few
seconds, aria2 prints a progress line
about once a second —

```text
[#851978 1.0MiB/4.0MiB(25%) CN:1 DL:346KiB ETA:8s]
```

— GID, bytes done of bytes total,
**CN** for connections in use, **DL**
for the current speed, and an estimated
time left. Chapter 5 reads these lines
closely; for now they are how you watch.
