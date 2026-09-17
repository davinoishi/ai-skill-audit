# Claude & Codex skill security review: summary

**Date:** 2026-09-16  **Machine:** <user>'s Mac
**Detail:** `llm-review-handoff/review-output/` (SUMMARY.md, coverage-gaps.md, finding-assessments.json, target-reviews.json, verification.json)
**Changes and backups:** `remediation-2026-09-16/`

---

## 1. What was scanned

| Item | Count |
|---|---|
| Skill "targets" (distinct skill versions; same-named copies with different content kept separate) | **140** |
| Used by Claude only / Codex only / both | 74 / 40 / 26 |
| Installed locations those targets map to | 193 |
| Files indexed and hashed | **10,904** (558 MB) |
| of which source code / documentation | 2,295 |
| of which generated dependencies (the SEO skill's Python `.venv`) | 8,345 |
| of which other artifacts (images, fonts, Office templates, binaries) | 252 |
| of which compiled bytecode | 12 |
| Targets with scanner findings / without | 79 / 61 |
| Scanner findings | **7,530** (2 critical, 6,439 high, 1,032 medium, 57 low) |

**Sources covered:** `~/.claude/skills`, `~/.agents/skills`, `~/.codex/skills`, the Claude plugin cache (HyperFrames 0.8.3, etc.), Cowork skills, the Codex plugin caches (Office, Sites, template-creator, etc.), AI_Brain project skills, your own commands and scheduled tasks.

**Method:**
- Automated scan with [SkillSpector](https://github.com/NVIDIA/SkillSpector) 2.11.2 (NVIDIA, Apache-2.0).
- A static, evidence-based review of every target and every finding against copied snapshots.
- Nothing from the skills was executed, no credentials were read, and no network calls were made. Earlier controlled runtime tests were used as evidence where they applied.

## 2. Review results

| Finding disposition | Count |
|---|---|
| Confirmed concern | 71 |
| Expected behaviour (intended, sometimes privileged) | 6,192 |
| False positive (scanner noise) | 1,139 |
| **Unresolved** (evidence missing, named per finding) | **128** |

- **Mostly noise:** most of the 7,530 findings came from the SEO `.venv` (6,098) or were formatting and pattern matches. The venv was checked with pip install-record hashes and bytecode comparison, not dismissed by filename.
- **Things the scanner missed:** the review added about 40 concerns of its own, such as the Cowork docx shared LibreOffice profile, Sites auto-publish, the `~/Downloads/hyperframes` code fallback, and hidden directives inside the impeccable binary.
- **No evidence of deliberately malicious skills.** The risk is supply-chain and trust-boundary design.

## 3. Actionable findings (ranked)

| # | Finding | Affected | Severity |
|---|---|---|---|
| 1 | HyperFrames skills silently self-update ("run silently, don't ask") and auto-upgrade the CLI to `@latest`; package loader accepts `@latest` as pinned | HyperFrames plugin 0.8.3 workflow skills; `hyperframes*` / `general-video` in ~/.claude, ~/.agents, ~/.codex, AI_Brain | High |
| 2 | impeccable runs a 12.7 MB unsigned native binary every session; the binary contains agent directives (ignore autonomy statements, spawn subagents) not visible in its SKILL.md | ~/.claude/skills/impeccable, ~/.agents/skills/impeccable | High / Medium |
| 3 | media-use: URL guard bypassable (SSRF to LAN/overlay, reproduced); imports an unrelated ancestor `.env` (reproduced); auto `pip install` of torch/transformers; spawns `codex exec` without confirmation | media-use (both copies) | Medium |
| 4 | SEO skill: redirect/DNS SSRF; OAuth token written with default permissions; Gemini key in plaintext in `~/.claude/settings.json` plus unpinned `npx -y` MCP server (banana extension) | ~/.claude/skills/seo | Medium |
| 5 | embedded-captions runs code from `~/Downloads/hyperframes` if it exists | HyperFrames plugin | Low-Medium |
| 6 | Codex skill-installer installs from any GitHub ref without a commit pin | ~/.codex/skills/.system/skill-installer | Medium (when used) |
| 7 | Sites 0.1.65 publishes after every edit without conversational confirmation | Codex Sites plugin | Low-Medium |
| 8 | Cowork docx/xlsx/pptx reuse predictable `/tmp` LibreOffice profile / preload library | Cowork Office skills | Low on this Mac |
| 9 | Own SEO pipeline runs share-hosted scripts and binaries as root without checksums | weekly-seo-crawl, seo-pipeline-run | Low-Medium (unverified) |
| 10 | Default-on telemetry: media-use links usage to HeyGen email; HyperFrames posts render feedback publicly; impeccable pings vendor | media-use, hyperframes-cli, impeccable | Low (privacy) |

Also found, with broader context:
- **Tools could read the whole disk.** Claude Code and skill scripts ran as your user with full read access to the home folder. Codex trusted the entire home folder as a project.

## 4. Actions taken

| Action | Detail |
|---|---|
| HyperFrames silent update removed | Preamble deleted from 10 workflow skills; router and general-video now require your approval before any skill update or CLI upgrade |
| HyperFrames CLI pinned | All agent-facing `npx hyperframes` / `@latest` references changed to `hyperframes@0.8.32` (215 files across plugin cache, ~/.claude, ~/.agents, AI_Brain) |
| HyperFrames env | `HYPERFRAMES_SKIP_SKILLS=1`, `HYPERFRAMES_SKILL_PKG_VERSION=0.8.32` in Claude Code and Codex |
| impeccable removed | Both skill copies, 4 Claude subagents, `~/.impeccable`, and AI_Brain's Codex hooks moved to `remediation-2026-09-16/removed-impeccable/`; binaries made non-executable |
| Claude Code sandbox | All shell commands and skill scripts sandboxed with no unsandboxed fallback. Read/write limited to `~/Documents/Projects-AI`, `~/Documents/AI_Brain`, plus needed tool caches, `~/.config/gh` and `~/.heygen`. Claude's file tools blocked outside those folders; explicit deny rules for other Documents folders, Desktop, Downloads, `~/.ssh`, `~/.aws`, `~/.config`. **Verified:** Desktop, `~/.codex` and home writes are denied |
| gh | Runs outside the sandbox (`excludedCommands`) with normal approval, because its token is in the Keychain; `gh auth status` confirmed working |
| Codex trust | Home-folder (`/Users/<user>`) trusted-project entry removed |
| Telemetry off | Claude Code: `DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING`, feedback survey off. Codex: analytics, `/feedback`, OpenTelemetry exporters off. Both: `HYPERFRAMES_NO_TELEMETRY=1`, `DO_NOT_TRACK=1` |
| SEO OAuth token | Nothing to change: the OAuth flow was never run (no token file exists) |

Backups of every modified file are in `remediation-2026-09-16/backup/` and `backup-step2/`. The user settings file also has a `.bak-gh-heygen` copy.

## 5. Still open

### Needs a decision or action from you
- **SEO banana extension:** if you ever ran `setup_mcp.py`, move the Gemini key out of `~/.claude/settings.json` and pin the MCP package version. Also, audit untrusted third-party URLs from the noBGP cloud node, not the Mac.
- **SEO `google_auth.py`:** optionally patch it so any future OAuth token is written with mode 600.
- **media-use:** its code-level issues (URL guard, ancestor `.env`, auto pip install) are still present; the sandbox now contains their blast radius. Avoid feeding it untrusted URLs. Consider reporting upstream.
- **SEO pipeline:** add sha256 checks for the share-hosted scripts and binaries, and restrict write access to the share.
- **Codex:** its sandbox still allows reads of the whole disk (writes limited to the project). No equivalent read restriction was applied.
- **Plugin updates:** a HyperFrames plugin update will overwrite the plugin-cache edits. Re-apply or re-check after updating.
- **Unpinned installs remain as documented behaviour:** `npx -y` in SEO, `uvx openai-whisper`, `npx create-video@latest`, and skill-installer installs from GitHub refs.
- **Low-priority upstream reports:** Cowork Office `/tmp` LibreOffice profile and shim; skill-creator port-kill; Sites auto-publish (keep deploy approvals on).

### Unresolved review items (128 findings)
- 81 compiled libraries in the SEO `.venv`: install hashes match, but they weren't compared against PyPI.
- The impeccable binary: only its strings were reviewed. It is now removed, so this is moot unless it's reinstalled.
- 16 name-only vulnerability advisories need version-specific checks (SEO venv packages, @babel/core, remotion fixtures).
- 22 large scripts not fully read (mostly HyperFrames video workflows).
- One Python 3.12 bytecode file (Presentations) and two telemetry details that depend on HyperFrames CLI source that isn't in the snapshot.

### Coverage gaps
- **Entry files not fully read:** 15 targets' SKILL.md, including Codex Office, Sites, Cowork docx/xlsx/pptx and media-use.
- **Files not fully read:** 84 targets still have some. A resumable worklist is in `verification.json`.
- **Not reviewable:** HyperFrames CLI source, Codex Sites plugin-root scripts, connector implementations and noBGP share scripts are not in any snapshot.

### Proposed tests (not run; need approval and an isolated VM/container)
Seven tests are specified in `coverage-gaps.md` §8:
- SSRF redirect/DNS for media-use and SEO
- token file mode
- shared LibreOffice profile
- HyperFrames package-loader consent
- impeccable sandboxed run (moot unless reinstalled)
- `skills update` diff

### Inputs still needed
- Network or offline mirror for advisory and hash checks.
- A Python 3.12 sandbox.
- Read access to the noBGP share and its ACLs.
