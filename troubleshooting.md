# Troubleshooting

Every failure below was produced on
purpose in this guide's lab, except
where it says otherwise — the error
text is aria2's own. Start any
investigation with the two questions
aria2 answers precisely: what does the
results table say (`OK` or `ERR`), and
what was the exit code?

| Exit code | Meaning | Seen in |
|---|---|---|
| 1 | The connection could not be made | §2 below |
| 3 | Resource not found (HTTP 404 and kin) | §1 below |
| 13 | File exists without its control file (BitTorrent) | §5 below |
| 32 | Checksum error | Chapter 7 |

aria2's exit code is the error code of
the failed download; a run in which
everything succeeds exits 0.

## 1. `errorCode=3 Resource not found`

```text
$ aria2c http://127.0.0.1:8377/no-such-file.txt
[ERROR] CUID#7 - Download aborted. URI=...
  -> [HttpSkipResponseCommand.cc:218] errorCode=3 Resource not found
fd244d|ERR |       0B/s|http://127.0.0.1:8377/no-such-file.txt
exit: 3
```

(transcript
`aria2-lab/transcripts/t90-failures.txt`).
The server answered and said no: the
address is wrong, the file was moved,
or the site wants a different path. No
file is left behind. Check the address
character by character — and consider
chapter 13's warning: a "successful"
download of a tiny HTML page is often
this error's cousin, a login or error
page fetched without complaint.

## 2. `Failed to establish connection, cause: Connection refused`

```text
Exception: [AbstractCommand.cc:856] errorCode=1
  Failed to establish connection, cause: Connection refused
exit: 1
```

Nothing is listening at that address
and port. The service is down, the port
is wrong, or a firewall is rejecting
rather than dropping. If the same
address works in a browser, suspect a
proxy difference: aria2 honours the
`http_proxy` environment variable, and
a stale one sends traffic to a proxy
that is not there. The lab proved it by
pointing `http_proxy` at a dead port
and clearing `no_proxy` — downloads to
a healthy local server failed with this
exact error (transcript
`aria2-lab/transcripts/t12-proxy.txt`).
`env | grep -i proxy` shows what is
set; the `no_proxy` variable exempts
the addresses it lists, which is why
loopback usually escapes a proxy's
reach.

## 3. It downloaded, but only one file of my two

The mirror trap, chapter 8: several
addresses on one command line are
*sources for the same file*, and the
diary line `Downloading 1 item(s)` is
the tell. For separate files use `-Z`,
or an input file with `-i`.

## 4. Speeds are capped but the cap "does nothing" — or the split never happens

Both symptoms usually trace to the
server, not the settings. Watch a live
progress line: if **CN** never rises
above 1 with `-x`/`-s` set, the server
is not honouring Range requests
(chapter 5's built-in-server
demonstration) and aria2 has fallen
back — silently — to one connection.
Rate limits show their effect in the
results table's average speed, not
necessarily in the first seconds'
progress lines, which start from cold.

## 5. `errorCode=13 ... control file(*.aria2) does not exist`

aria2 refusing to touch a complete
file in a torrent folder because it
cannot prove the file is finished
(chapter 9). If the file *is* the
finished article and you mean to seed
it: `--bt-seed-unverified=true`. If it
is not, delete it (or pass
`--allow-overwrite=true`) and let the
download start honestly. Do not reach
for either flag until you have decided
which of those two the file is.

## 6. The checksum failed — but the file is right there

It is, and chapter 7 explains why: the
bytes were kept for repair, with a
control file beside them. Restarting
the same command (with `-c` for HTTP)
lets aria2 re-fetch only the pieces
that mismatch, where the protocol
supports piece checks. But until a run
reports `Verification finished
successfully`, treat the file as a
suspect, not a copy: move it aside,
never run it, never ship it.

## 7. The RPC daemon will not answer

In order: is it running (`aria2.shutdown`
is graceful — a restarted daemon can
collide with its predecessor still
closing the port, chapter 10)? Is the
port the one you think (6800 by
default, `--rpc-listen-port` moves it)?
Are you calling from another machine,
against a daemon still bound to
loopback by default? And is the token
the first parameter, in the
`token:secret` shape? — the lab's
no-token call got `Unauthorized`, which
at least proves the daemon is alive and
the secret is doing its job.

## 8. A `.aria2` file will not go away

That is a download that has not
finished, by definition — the control
file is deleted at completion, so its
presence is the most reliable detector
of unfinished business in a download
folder. Finish it with `-c`, or if the
download is truly abandoned, delete
the control file *and* its partial
file together; deleting only one
orphans the other.
