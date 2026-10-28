# The Neighbours

aria2 is not the only way a file gets
from there to here. These are the tools
it lives next to, characterised honestly
— what each does that aria2 doesn't, and
vice versa. (The comparisons are
characterisations, not benchmarks; the
neighbours were not run in this guide's
lab.)

## curl and wget

**curl** is the web's swiss army knife:
it speaks to servers in every dialect
and shows you the whole conversation.
For *one* file it fetches as well as
anything — and it can resume (`-C -`)
and retry. What it is not is a download
*manager*: no queue, no sessions, no
built-in hash verdict in the results
table sense, no swarms. The companion
guide *curl for Mere Mortals* covers it
properly. **wget** is the older fetcher:
recursive website copying is its party
trick (`-r`, mirroring a whole site),
which aria2 does not attempt at all. If
the job is "that one file, now", reach
for either without guilt; when the job
grows a list, a schedule, or a second
protocol, aria2 is the step up.

## The browser

A browser download is aria2's opposite
in every design choice: no scriptable
verdict, weak resuming, invisible state —
and zero to learn, already installed,
and honest about being a convenience.
For a 2 MB PDF it is the right tool.
The crossover point is repetition and
size: the third time a browser download
dies at 90% of a large file, the
problem has become aria2-shaped.

## yt-dlp

**yt-dlp** (companion guide: *yt-dlp
for Mere Mortals*) answers a different
question. aria2 fetches the address you
give it; yt-dlp figures out *which*
address — the real media streams hiding
behind a video page — and then fetches
those, with site-specific knowledge
aria2 does not have and does not want.
They compose: nothing stops a list of
resolved addresses being handed to
aria2 for the fetching itself.

## rsync

**rsync** (companion guide: *rsync for
Mere Mortals*) synchronises *trees*:
folders compared file by file, only the
differences moved, between machines you
control, usually over SSH. aria2
fetches *files*, from places that
publish them, including places run by
strangers. "Keep my folder identical to
that folder" is rsync. "Those files,
from whoever has them, checked by
hash" is aria2.

## Dedicated torrent clients

Transmission, qBittorrent and their kin
are aria2's BitTorrent chapter grown
into a whole application: queues with
per-torrent limits, peer management,
watch folders, friendly interfaces.
If torrents are a daily habit, they are
the better home for it. aria2's
advantage is that BitTorrent is *one of
its four protocols* under the same
options, the same input files and the
same RPC as everything else — one tool
to script, whichever shape the next
download takes.

## Download managers and web UIs

Graphical download managers, and the
browser interfaces for aria2 itself
(chapter 10), sell the same engine with
a face: progress bars you can see,
queues you can drag. Underneath, the
honest ones are doing exactly what this
guide did from the command line. Learn
the engine here, and every face on it
becomes legible.
