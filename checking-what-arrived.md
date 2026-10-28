# Checking What Arrived

Outcome: you can make aria2 refuse a
file that does not match its published
hash — and you know why the file sitting
on disk afterwards is not, by itself,
evidence of anything.

## The idea in one paragraph

A **hash** is a fingerprint computed
from a file's bytes: change one byte and
the fingerprint changes completely.
Publishers of large files print the
SHA-256 hash next to the download link.
If the hash of what arrived equals the
hash the publisher printed, the bytes
are the publisher's bytes — not
approximately, not probably: the same.
aria2 can do this check itself, as part
of the download, with `--checksum`.

## Checking at download time

From transcript
`aria2-lab/transcripts/t05-checksum.txt`.
The lab's `hello.txt` has the known
SHA-256
`90ad06db91e4a1dfeb4868041a3f51a060abac50a91cbcbc54f0e4f2f0dc3ff4`,
and giving it to aria2 changes what a
successful download says:

```text
$ aria2c --checksum=sha-256=90ad06db... http://127.0.0.1:8377/hello.txt

10/28 18:21:02 [NOTICE] Verification finished successfully. file=/home/.../hello.txt
10/28 18:21:02 [NOTICE] Download complete: /home/.../hello.txt
exit: 0
```

*Verification finished successfully* is
a separate event from *Download
complete*, and in that order: the bytes
were fetched, fingerprinted, and only
then declared done. The algorithm name
is part of the option (`sha-256=`; the
version output in chapter 3 lists the
hashes your build knows), and the value
is the publisher's hex string.

## When the hash is wrong

The same command with a hash that does
not match — the lab used a string of
zeros, standing in for a corrupted
transfer or a substituted file:

```text
$ aria2c --checksum=sha-256=00000000... -d bad http://127.0.0.1:8377/hello.txt

10/28 18:21:02 [ERROR] Checksum error detected. file=bad/hello.txt
10/28 18:21:02 [NOTICE] Download GID#f328e5... not complete: bad/hello.txt

f328e5|ERR |   3.0KiB/s|bad/hello.txt
exit: 32
```

Three facts here are worth memorising:

- **The exit code is 32** — aria2's
  specific code for a checksum error.
  A script that only tests "did it run"
  will miss failures; a script that
  reads the exit code, or greps the
  results table for `ERR`, will not.
- **The transfer itself was fine.** The
  file arrived complete and on time; it
  failed *verification*. aria2's message
  separates the two events, and so
  should your thinking: "download
  failed" and "download is not what was
  promised" are different problems with
  different fixes.
- **The bad file is still on disk.**
  The lab looked, and `bad/hello.txt`
  was there, all 117 bytes, next to a
  fresh `hello.txt.aria2` control file —
  aria2 keeps the pieces so a restart
  can re-check and repair rather than
  refetch. Which means: *a file existing
  proves nothing.* If the hash mattered
  enough to check, it matters enough to
  act on the exit code before anything
  opens that file.

## Checking after the fact

For a file already downloaded — by
aria2, by a browser, by anything — the
ordinary tool is the publisher's
checksum file, if they offer one (often
named `SHA256SUMS` or similar):

```bash
sha256sum -c SHA256SUMS
```

It prints `OK` or `FAILED` per file and
is the same fingerprint test without
aria2 in the loop. Use `--checksum`
when aria2 fetches, because the verdict
then lands in the results table and the
exit code where scripts already look;
use `sha256sum -c` for everything that
arrived any other way.

Two of aria2's protocols make this
chapter partly automatic. A **Metalink**
file carries the hashes inside it, and
aria2 verifies against them without
being asked (chapter 9). A **torrent**
carries a hash for every piece, checked
as each piece lands — a peer cannot
hand you wrong bytes that pass. Plain
HTTP and FTP carry nothing of the kind,
which is exactly why `--checksum`
exists.
