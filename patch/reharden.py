#!/usr/bin/env python3
"""Re-apply the HyperFrames hardening after a plugin or skill update.

Companion to media-use.patch — see README.md. Unofficial; not affiliated with any vendor.

    python3 reharden.py            # apply (default)
    python3 reharden.py --dry-run  # show what would change
    HF_PIN=0.8.40 python3 reharden.py

What it does, to every installed HyperFrames-family skill copy:
  1. deletes the "First, keep this skill fresh - run silently, don't ask" preamble;
  2. pins agent-facing `npx hyperframes` / `npx hyperframes@latest` to a fixed version;
  3. adds a note to the router and general-video SKILL.md requiring the user's
     approval before any skill update or CLI upgrade, and rewrites the two
     instructions that told the agent to upgrade on its own.

Idempotent: running it twice changes nothing the second time. Every file it
rewrites is backed up under backups/<timestamp>/ next to this script.

Run it from your own Terminal — the Claude Code sandbox blocks writes to skill
folders on purpose.
"""
import os, re, sys, glob, shutil, datetime

PIN = os.environ.get("HF_PIN", "0.8.32")
DRY = "--dry-run" in sys.argv
HOME = os.path.expanduser("~")
HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(HERE, "backups", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

NAMES = ["general-video", "hyperframes", "hyperframes-animation", "hyperframes-audio",
         "hyperframes-cli", "hyperframes-core", "hyperframes-creative",
         "hyperframes-keyframes", "hyperframes-registry", "media-use"]

ROOTS = glob.glob(f"{HOME}/.claude/plugins/cache/claude-plugins-official/hyperframes/*/skills")
ROOTS += [f"{HOME}/.claude/skills/{n}" for n in NAMES]
ROOTS += [f"{HOME}/.agents/skills/{n}" for n in NAMES]
# Project-local skill folders, e.g. a repo with its own .agents/skills or .claude/skills:
#   HF_EXTRA_ROOTS=~/code/my-project/.agents/skills:~/other/.claude/skills python3 reharden.py
ROOTS += [os.path.expanduser(r) for r in os.environ.get("HF_EXTRA_ROOTS", "").split(":") if r]
# ~/.codex/skills/* are symlinks to ~/.claude/skills/*; realpath dedupe covers them.

GATE = ("> **Updates disabled on this machine (owner policy):** do not run `hyperframes skills update`, "
        "`npx skills add`, or any `hyperframes@latest` upgrade without first asking the user and getting a yes. "
        "`HYPERFRAMES_SKIP_SKILLS=1` is set; the CLI is pinned to hyperframes@" + PIN + ".\n\n")

PREAMBLE = re.compile(r"^> \*\*First, keep this skill fresh[^\n]*\n(\n)?", re.M)
NPX = re.compile(r"(npx (?:--yes |-y )?)hyperframes(?:@[\w.-]+)?(?![@\w-])")
CODE_FILES = {"audio/scripts/lib/tts.mjs", "scripts/transcribe.mjs",
              "scripts/lib/tts-local-provider.mjs", "scripts/preflight.mjs"}
SKIP_EXT = (".png", ".jpg", ".jpeg", ".mp3", ".wav", ".mp4", ".mov", ".webm", ".ttf",
            ".otf", ".woff", ".woff2", ".onnx", ".gif", ".ico", ".zip", ".pdf")

ROUTER_OLD = ("Act on the signal rather than relaying it to the user; never leave a bumped pin unverified.")
ROUTER_NEW = ("Do NOT apply the upgrade yourself: report the pinned and latest versions to the user and "
              "upgrade only if they explicitly approve; never leave a bumped pin unverified.")
GV_BLOCK = re.compile(
    r"Before relying on this workflow, run:\n\n```bash\nnpx hyperframes(?:@[\w.-]+)? skills update general-video\n```"
    r"\n\nA successful no-op means the skill is current\. Surface an update failure instead of continuing from memory\.\n")
GV_NEW = "Skill auto-updates are disabled on this machine: do not run `hyperframes skills update` without asking the user first.\n"

changed, seen = [], set()
for root in ROOTS:
    if not os.path.isdir(root):
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != "node_modules"]
        for name in filenames:
            path = os.path.join(dirpath, name)
            real = os.path.realpath(path)
            if real in seen or os.path.islink(path) or ".test." in name or name.endswith(SKIP_EXT):
                continue
            seen.add(real)
            try:
                text = open(path, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            out = PREAMBLE.sub("", text)
            out = NPX.sub(lambda m: m.group(1) + "hyperframes@" + PIN, out)
            if any(path.endswith("/" + c) for c in CODE_FILES):
                out = re.sub(r'\["hyperframes(?:@[\w.-]+)?", ', f'["hyperframes@{PIN}", ', out)
            parent = os.path.basename(dirpath)
            if name == "SKILL.md" and parent == "hyperframes":
                out = out.replace(ROUTER_OLD, ROUTER_NEW)
            if name == "SKILL.md" and parent == "general-video":
                out = GV_BLOCK.sub(GV_NEW, out)
            if name == "SKILL.md" and parent in ("hyperframes", "general-video") and "Updates disabled on this machine" not in out:
                m = re.match(r"^---\n.*?\n---\n", out, re.S)
                if m:
                    out = out[:m.end()] + "\n" + GATE + out[m.end():].lstrip("\n")
            if out == text:
                continue
            changed.append(path)
            if not DRY:
                dst = os.path.join(BACKUP, os.path.relpath(path, HOME))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(path, dst)
                open(path, "w", encoding="utf-8").write(out)

print(("WOULD CHANGE " if DRY else "CHANGED ") + f"{len(changed)} file(s); pin = hyperframes@{PIN}")
for p in changed[:10]:
    print("   " + p.replace(HOME, "~"))
if len(changed) > 10:
    print(f"   ... and {len(changed) - 10} more")
if changed and not DRY:
    print("Backups: " + BACKUP)
if not changed:
    print("Nothing to do — hardening already in place.")

# Environment check (informational; this script does not edit your settings).
def check(path, needle):
    try:
        return "found" if needle in open(os.path.expanduser(path), encoding="utf-8").read() else "missing"
    except FileNotFoundError:
        return "no-file"
    except OSError:
        return "unreadable"   # e.g. run from inside a sandbox that blocks this path
for path, needle, label in [("~/.claude/settings.json", "HYPERFRAMES_SKIP_SKILLS", "Claude Code"),
                            ("~/.codex/config.toml", "HYPERFRAMES_SKIP_SKILLS", "Codex")]:
    state = check(path, needle)
    if state in ("missing", "no-file"):
        print(f"WARNING: HYPERFRAMES_SKIP_SKILLS not set in {path} ({label}) — skill auto-update is not disabled there.")
    elif state == "unreadable":
        print(f"NOTE: could not read {path} ({label}) to confirm HYPERFRAMES_SKIP_SKILLS — run this from your own Terminal.")
