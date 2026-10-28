# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's traffic is the lab talking to itself.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 13 names what the tool
   cannot do: fetch meanings instead of addresses, split or
   resume against a server that will not play, prove a file by
   its presence, carry trust in a hash, act as shared
   multi-user infrastructure, or grab without etiquette.
8. **The ethics rule is in the text, early.** Chapter 1 and the
   README state the condition plainly — download only what you
   have the right to download, from places you have the right
   to use — and the limits chapter returns to it where the
   tooling makes excess easy.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a shared Ubuntu 24.04 sandbox. aria2
**1.37.0** — the current release, and the version Ubuntu
24.04's package carries (t00b) — was obtained from that
package and extracted into a scratch folder (never installed
system-wide, out of respect for the shared machine) and run
from there; the binary, its feature list and every behaviour
below are the package's own. Downloads were served by a
range-capable file server written for this guide
(`aria2-lab/server/range_server.py`) on loopback, because
Python's built-in server cannot answer Range requests.
Transcripts are the lab's real output with two disclosed
cosmetics: terminal colour codes were stripped (aria2 1.37
emits them even when piped, and offers no option to stop),
and in chapter quotations the lab's long scratch paths are
shortened — the kept transcripts show them in full.
All transcripts live in `aria2-lab/transcripts/`.

Run for real, with transcripts as evidence:

- Version and compiled feature list; the Ubuntu package's
  candidate version read through apt (t00, t00b).
- A single HTTP download, read back with `cat` (t01).
- A four-segment download (`-x4 -s4 -k1M`), proven from the
  server's own request log: three explicit Range requests
  plus the opening connection, and a matching SHA-256 (t02).
- The same segmented command against Python's built-in
  server, which has no Range support: a successful,
  unsplit, unremarked fallback (t02b).
- An interrupted download — killed mid-flight at a capped
  speed — leaving a partial file and a 59-byte control file,
  then resumed with `-c` to a hash-identical finish, the
  server log showing the resume re-fetching from the last
  complete piece boundary (t03).
- A rate-capped download: 512K cap, 508KiB/s reported
  average, 8.1 seconds on the clock for 4 MiB (t04).
- `--checksum` with the correct SHA-256 (verification
  notice, exit 0) and with a wrong one (checksum error,
  exit 32, the unverified file left on disk with its
  control file) (t05).
- An input file with per-URL `out=` and `dir=` options;
  the two-addresses-one-item mirror trap; `-Z` fetching
  the same two addresses as two downloads (t06).
- The RPC daemon: `getVersion`, `addUri` returning a GID,
  `tellStatus` reporting it complete, the downloaded file
  read from the daemon's folder, a tokenless call refused
  with `Unauthorized`, `shutdown` answering OK, and the
  port refusing connections a few seconds later (t07).
  The secret used is a lab invention, not a credential.
- A Metalink download verified by the hash inside the
  hand-written `.meta4`, and a tampered-hash Metalink
  failing with exit 32 (t08).
- A complete BitTorrent transfer between two aria2
  instances on loopback: `.torrent` written by
  `aria2-lab/server/make_torrent.py`, a minimal tracker
  (`aria2-lab/server/tracker.py`) logging both announces
  and the leecher's `event=completed`, the seeder
  reporting 4.0MiB uploaded and exiting at share ratio
  1.0, the leecher's file matching the fixture SHA-256.
  DHT, peer exchange and local peer discovery were
  disabled throughout, by design (t09).
- The seeder's refusal (errorCode=13) to seed an existing
  file without a control file, and its remedy,
  `--bt-seed-unverified=true` (t09, raw output).
- Session save and resume: a killed download's session
  file preserving its address, GID and 256K cap, and the
  restart from `-i session.txt -c` finishing under the
  same cap (t10).
- A repeat download renaming instead of overwriting
  (`hello.1.txt`) (t11).
- aria2 honouring `http_proxy` and `no_proxy`: with the
  proxy pointed at a dead port and `no_proxy` cleared, a
  healthy local download failed with connection refused
  (t12).
- Failures by the book: HTTP 404 exiting 3 and a refused
  connection exiting 1, leaving nothing behind (t90).

Documented only — described from the project's
documentation, not run, and the text does not claim
otherwise:

- That the project's release page offers no pre-built
  Linux binary was verified against the project's own
  release list during the build; Windows and macOS
  installs themselves were not performed.
- FTP and SFTP downloads (the lab had no local server for
  them; the feature list confirms the build supports
  them, and chapters present the protocols as named, not
  demonstrated).
- Magnet links: the mechanics after the description
  arrives are the demonstrated ones, but no magnet was
  resolved in the lab — its swarm would have had to be a
  real one.
- Public swarms, DHT, peer exchange, local peer
  discovery, and NAT traversal: deliberately excluded.
  The lab's swarm was a dissection on loopback.
- Downloads from the public internet over HTTPS: the lab
  stayed on loopback throughout.
- Web interfaces for the RPC daemon (webui-aria2,
  AriaNg), and the neighbour tools of chapter 12:
  characterised, not run.
- RPC methods beyond the five exercised (pause, remove,
  tellActive/tellWaiting and friends) are named from the
  API's documentation.

Fixtures are this guide's own and deliberately generic:
three small text files, a CSV of fruit, and 4 MiB of a
repeating pangram, all generated by
`aria2-lab/make-fixtures.py`, which reproduces them — and
the SHA-256 hashes quoted in the chapters — exactly.
Nothing was downloaded from anywhere the lab did not
itself serve, and nothing in the lab is modelled on any
real person, network, service or organisation.
