# The RPC Interface

Outcome: aria2 runs in the background as
a download service, and another program
— here, `curl` from the command line —
hands it work, follows the work, and
shuts it down. Everything after this
chapter that calls itself a "download
manager" is, at heart, this chapter
with a face painted on.

## Starting the service

```bash
aria2c --enable-rpc --rpc-listen-port=6800 \
       --rpc-secret=labsecret --daemon=true -d work/t07
```

Three of those options are decisions,
not decoration:

- **`--enable-rpc`** opens the control
  channel (JSON-RPC or XML-RPC over
  HTTP) on port **6800** by default.
- **`--rpc-secret`** sets the password
  every caller must present. The lab
  invented one for the occasion; you
  should invent a real one, because the
  interface can add downloads of
  anything, to anywhere aria2 can write.
- **`--daemon=true`** detaches aria2
  into the background. `-d` gives its
  downloads a home folder instead of
  whichever folder the shell happened
  to be in.

By default the RPC port listens **only
on this machine** (loopback), and that
default is a security boundary: anyone
who can reach the port and pass the
secret owns your downloads.
`--rpc-listen-all=true` exists for
driving a download box from another
room; it should arrive together with
the secret, a firewall, and thought.

## Giving orders

An RPC call is an HTTP POST naming a
method and its parameters. Asking the
service who it is (transcript
`aria2-lab/transcripts/t07-rpc.txt`,
replies tidied by `python3 -m json.tool`):

```text
$ curl ... aria2.getVersion
{
    "result": {
        "enabledFeatures": [
            "Async DNS", "BitTorrent", "Firefox3 Cookie",
            "GZip", "HTTPS", "Message Digest",
            "Metalink", "XML-RPC", "SFTP"
        ],
        "version": "1.37.0"
    }
}
```

Note the first parameter in every call
below: `"token:labsecret"` — the secret,
presented in that exact shape. Adding a
download returns its GID:

```text
$ curl ... aria2.addUri  [["http://127.0.0.1:8377/hello.txt"]]
{ "result": "82d11b2f0c72cabc" }
```

and asking after it, by GID, returns
its state — here, narrowed to four
fields of the many `tellStatus` offers:

```text
$ curl ... aria2.tellStatus  ["82d11b2f0c72cabc"]
{
    "result": {
        "completedLength": "117",
        "files": [ { "path": ".../work/t07/hello.txt", ... } ],
        "status": "complete",
        "totalLength": "117"
    }
}
```

The vocabulary is the CLI's, translated:
a download is *active*, *waiting*,
*paused*, *complete* or *error*;
`tellActive` and `tellWaiting` list the
GIDs in each state; `aria2.pause` and
`aria2.remove` do what they say. A
program driving aria2 polls `tellStatus`
the way you watched the progress lines —
except it can do it for a hundred
downloads, all night, without getting
bored. The file, meanwhile, had really
arrived; the lab catted it from the
daemon's folder to prove the service
had done work and not merely reported
it.

## The secret, working

The same `getVersion` call *without*
the token parameter:

```text
$ curl ... aria2.getVersion   # no token
{
    "error": {
        "code": 1,
        "message": "Unauthorized"
    }
}
```

That refusal is the whole authentication
model: one shared secret, no accounts.
Treat it like the key it is — it will
appear in your scripts and shell
history, so keep the service on
loopback unless you have arranged
something stronger in front of it.

## Stopping the service

`aria2.shutdown` answers `"OK"` — and
then takes its time. The lab's first
probe, a second later, still got an
answer from the port; a few seconds
after that, the connection was refused
(curl's exit 7). Shutdown is a landing,
not a trapdoor: active downloads are
closed out, sessions saved if you asked
for that (chapter 8), and then the
process ends. Scripts that restart the
service should wait for the port to
actually close rather than trusting the
OK.

Ready-made faces exist for all of this
— web interfaces such as webui-aria2
and AriaNg run in a browser and speak
exactly this protocol to a daemon you
run; they are separate projects,
characterised here rather than run, and
the daemon cannot tell them apart from
your own curl commands. That is rather
the point of the design.
