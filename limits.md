# Limits

What aria2 cannot do, and where its
strengths stop being strengths. Read
this chapter before building anything
important on it.

## It fetches addresses, not meanings

aria2 downloads the URL it is given.
It does not know that a page *contains*
a download link, that a site wants a
login form filled in first, or that the
real file hides three redirects and a
cookie consent banner behind the
address you found. Tools that understand
particular sites (chapter 12's yt-dlp)
or that drive a browser exist because
this gap is real. When a download comes
back as a small HTML page instead of
the large file you expected, aria2 has
usually done its job perfectly — on an
address that was never the file.

## Half its powers depend on the server

Segmentation, resuming, and mirror
balancing all rest on the server's
Range support and honest metadata. A
server can refuse ranges, lie about a
file's size, or change the file between
your first connection and your fifth —
aria2 detects some of this (a changed
file fails piece checks and errors),
but the polite fallbacks mean a
download can quietly be slower and
less resumable than you configured.
Chapter 5's silent single-connection
download is the type specimen.

## A file on disk is not a verified file

Chapter 7's lesson, restated as a
limit: aria2 optimises for *recoverable*
transfers, which means partial and
even failed downloads leave files and
control files behind. Any workflow that
treats "the file exists" as "the
download succeeded" will eventually
ship a truncated archive. The contract
is the exit code, the results table,
and the hash — use at least one.

## Verification is only as good as the hash's journey

`--checksum` proves the bytes match a
hash. It says nothing about whether the
hash itself is the publisher's: a hash
copied from the same compromised page
as the download link verifies a bad
file beautifully. aria2 cannot fix the
trust problem; it can only execute the
check faithfully. Hashes obtained over
a separate, trusted channel are worth
more than hashes from the same page.

## BitTorrent, honestly bounded

aria2 is a competent torrent client,
not a specialist one (chapter 12).
Its seeding, queueing and peer controls
are serviceable rather than deep, and
this guide verified it only as a
two-machine loopback swarm with
discovery switched off. Large public
swarms, hostile peers, NAT traversal
trouble, and the legal exposure of
seeding content you have no right to
share are all beyond both the lab and
this chapter. The protocol also
advertises your address to the swarm
by design; people who need otherwise
need different tools entirely.

## One machine, one user, by assumption

The RPC interface's whole security
model is a shared secret and, by
default, a loopback socket. There are
no accounts, no per-user permissions,
no audit trail of who queued what. As
a personal engine on your own machine
or home server it is exactly enough;
as shared infrastructure for a group
it is a component, not a solution —
put real access control in front of
it, or keep it on loopback.

## Etiquette is a limit too

aria2 makes it easy to open sixteen
connections and pull as fast as the
path allows. Somebody pays for the
other end of that. Servers ban,
throttle, and block clients that behave
greedily, and small mirrors — often
volunteer-run — can be genuinely hurt
by segmented downloads of popular
files. The caps and concurrency limits
in this guide are not only
self-protection; they are how a
well-behaved guest fetches.
