# Installing aria2

Outcome: `aria2c --version` runs on your
machine, and you know where your copy
came from. The install has one surprise
worth knowing before you start: **there
is no official pre-built aria2 for Linux
at all.** The project's release page
offers finished builds for Windows,
macOS and Android, and source code for
everyone else. Linux users are expected
to take their distribution's package —
which is not a hardship, because the
packages are current. This guide's lab
verified the claim against the project's
own release list, and then used Ubuntu's
package: version **1.37.0**, the current
release.

## On Linux: your distribution's package

Debian and Ubuntu:

```bash
sudo apt install aria2
aria2c --version
```

The same idea elsewhere: `dnf install
aria2` on Fedora, `pacman -S aria2` on
Arch. What the lab's Ubuntu 24.04 machine
reported about the package before
installing (transcript
`aria2-lab/transcripts/t00b-apt.txt`):

```text
$ apt-cache policy aria2
aria2:
  Installed: (none)
  Candidate: 1.37.0+debian-1build3
```

Check: the version command prints a page
of information, not one line. Its head
(transcript `aria2-lab/transcripts/t00-version.txt`):

```text
$ aria2c --version
aria2 version 1.37.0
Copyright (C) 2006, 2019 Tatsuhiro Tsujikawa
```

and further down, a **Configuration**
section listing the features your build
was compiled with:

```text
Enabled Features: Async DNS, BitTorrent, Firefox3 Cookie,
GZip, HTTPS, Message Digest, Metalink, XML-RPC, SFTP
Hash Algorithms: sha-1, sha-224, sha-256, sha-384, sha-512,
md5, adler32
```

Read that list once, now. It is the
authoritative answer to "can my aria2 do
X?" — a build without *BitTorrent* in
that line cannot open a `.torrent` file
no matter what options you pass it, and a
build without *Message Digest* cannot
check the hashes of chapter 7. Minimal
containers and some distributions ship
leaner builds; the version page is how
you find out before a chapter depends on
a feature you do not have.

## On Windows and macOS

Windows and macOS are the platforms with
official builds: the project's GitHub
release page carries a ready-to-run
`aria2c.exe` for 64-bit Windows, and a
macOS build; package managers offer the
same program (`winget install aria2`,
`brew install aria2`). These routes are
described from the project's
documentation — the lab ran the Linux
package only, and `criteria.md` labels
them documented-only. Whichever route
you take, finish with the same check:
`aria2c --version`, and a glance at the
feature list.

## Where downloads go, by default

One behaviour to set deliberately before
chapter 4: with no options, aria2 writes
downloads into the **current folder**,
under the name the address ends with.
That is convenient in a scratch folder
and messy everywhere else. The options
`-d` (folder) and `-o` (file name) place
a download exactly, and chapter 8's
input files let every address carry its
own. If you always want the same landing
place, put it in the configuration file,
`~/.config/aria2/aria2.conf`:

```text
dir=/home/you/Downloads
```

Every option in this guide can live in
that file, written as its long name
without the dashes. Command-line options
win over the file, which is the right
order: the file holds your defaults, the
command line holds this download's
exceptions.
