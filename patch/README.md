# media-use patch: URL guard + `.env` loading

Fixes two confirmed issues in the HeyGen **media-use** skill, found during a security review of 140 installed Claude/Codex skills (see `../report/SUMMARY.md`, concerns `MEDIA-USE-URL-GUARD` and `MEDIA-USE-ENV-ANCESTOR`).

Built against media-use as shipped in the HyperFrames 0.8.3 plugin and the standalone skill install, September 2026:

| File | sha256 (before) |
|---|---|
| `scripts/lib/freeze.mjs` | `77e664bb548cdcaba779f602754a0430df28a613fd940e093e383428a7bc620c` |
| `audio/scripts/lib/heygen.mjs` | `ab6d3f3bceaec3aebc4196c1a356afcfe1931027fad4bdc183c7efcac9e0cc62` |

If your copies differ, the installer refuses to touch them. That's the intended behaviour, not a failure.

## What it changes

**`scripts/lib/freeze.mjs` — the URL guard.** Upstream matches the hostname against a text pattern and lets `fetch` follow redirects on its own. The patch:
- checks addresses by parsing them, not by matching text, so `[::ffff:7f00:1]` (IPv4-mapped loopback) and `[::ffff:c0a8:101]` (IPv4-mapped `192.168.1.1`) are refused — both were accepted before;
- adds `100.64.0.0/10` (carrier-grade NAT, used by overlay networks such as Tailscale-style meshes), `198.18/15`, `0.0.0.0/8`, multicast and reserved ranges, NAT64 and 6to4 embedded addresses, and `::`;
- refuses `.local`, `.lan`, `.home.arpa`, `.internal` and single-label hostnames;
- resolves DNS and requires **every** answer to be public, so a public name pointing at a private address is refused;
- follows redirects manually, re-checking each hop, with a limit of 5.

**`audio/scripts/lib/heygen.mjs` — `.env` loading.** Upstream walks up to five folders above the project, finds the first `.env`, and imports every variable in it into the process environment, where child processes inherit it. The patch imports only `HEYGEN_API_KEY`, `HYPERFRAMES_API_KEY`, `HEYGEN_CONFIG_DIR`, `ELEVENLABS_API_KEY`, `GEMINI_API_KEY` and `GOOGLE_API_KEY`, and stops climbing at the first project boundary (a folder holding `hyperframes.json`, `package.json` or `.git`).

**Known limit:** a DNS answer that changes between the check and the connection (rebinding) isn't pinned, and when a proxy is in use the proxy does its own resolution. Treat this as defence in depth alongside an OS-level sandbox, not as a replacement for one.

## Contents

| File | What it is |
|---|---|
| `media-use.patch` | Unified diff, applied with `patch -p1` from the skill root |
| `install.sh` | Applies it to every installed copy, with hash checks, backups and verification |
| `restore.sh` | Puts the originals back from the newest backup |
| `patch.test.mjs` | Node test suite: 6 tests, no network |

## Install

```bash
bash install.sh
```

It only patches a file whose sha256 still matches the reviewed version, backs up everything it replaces to `backups/<timestamp>/`, verifies the result, and then runs the tests. Running it twice is a no-op. It looks for these copies, so edit the `COPIES` list if yours differ:

```
~/.claude/skills/media-use
~/.agents/skills/media-use
~/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/media-use
```

Restart Claude Code and Codex afterwards.

## Verify it yourself

```bash
# read the change
less media-use.patch

# run the tests against a copy of the patched files
mkdir -p /tmp/mu && cp ~/.claude/skills/media-use/scripts/lib/freeze.mjs /tmp/mu/ \
  && cp ~/.claude/skills/media-use/audio/scripts/lib/heygen.mjs /tmp/mu/ \
  && PATCH_DIR=/tmp/mu node --test patch.test.mjs
```

Expect `# pass 6`. The same tests against unpatched files fail 5 of 6, which is the point: the tests encode the actual bypasses. The skill's own `freeze.test.mjs` still passes unchanged.

## Undo

```bash
bash restore.sh
```

## After a HyperFrames update

An update overwrites these files. Run `install.sh` again. If upstream has changed them, you'll get WARNINGs and nothing is modified — rebuild the patch against the new version at that point, and check whether upstream fixed it themselves.

## Note

Unofficial, not affiliated with HeyGen or Anthropic. The diff is offered as security commentary; the skill's code remains its authors'. No warranty — read it before you run it.
