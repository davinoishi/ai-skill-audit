# Security review of installed Claude and Codex skills

Review date 2026-09-16. Inputs: `llm-review-handoff/` (manifest, files-to-review, triage ledger, target packets), the source snapshots under `deployment/skillspector/followup/input/`, `scan-results/manual-review.md` and `followup/runtime-results.json`.

**Method.** Static source review only. No skill script, hook, installer, binary or venv was executed. No credential contents were read. No installed skill or original finding was modified. No external network or model call was made. Everything in the skills was treated as untrusted data. The previous controlled runtime checks are cited where they apply.

**Bottom line.** I found no evidence of deliberately malicious skills. The real risk is **supply-chain and trust-boundary design**. Several popular skills change their own code and instructions from the network without asking. One runs an opaque native binary that emits agent directives not visible in its Markdown. Several fetch attacker-influenceable URLs from a machine that can reach the home LAN and the noBGP overlay. One stores long-lived tokens loosely. Each item below is tied to specific installed copies. Where copies with the same name differ, they are kept separate.

## Coverage in one paragraph

All **140 targets** and all **7,530 finding keys** are accounted for exactly once (`verification.json`, `checks_passed: true`). **7,402 keys are decided**: 71 confirmed concern, 6,192 expected behaviour, 1,139 false positive. **128 remain unresolved**, each with the missing evidence named. Every target has a review record: **119 are `reviewed_with_gaps` and 21 are `reviewed_no_open_gaps`**. The second label means every text file was read and nothing is unresolved; it does **not** mean safe. Reading depth is uneven. The entry instruction file (SKILL.md or command) was read in full for 125 targets, and so were the scripts behind the main risks below. For 15 targets the entry file was only read around flagged lines or grep-swept: Codex Presentations, Spreadsheets, excel-live-control, documents, visualize, both sites-building copies; Cowork docx, xlsx, pptx; both media-use copies; remotion-to-hyperframes (AI_Brain copy, diffed only at script level); remotion-best-practices; talking-head-recut. Many large helper scripts in the HyperFrames/media-use family and the big Codex Office skills were only read around the flagged lines or risk-grep-swept. The per-file depth and a resumable worklist are in `target-reviews.json`, `verification.json` and `coverage-gaps.md`. Most of the 7,530 keys are SEO `.venv` presence alerts (6,098 SC9). Those were settled by verifying pip RECORD hashes and `.pyc` equivalence, not by filename, and the 81 native libraries remain unresolved.

---

## 1. What to act on (ranked by impact × likelihood)

| # | Risk | Impact / likelihood | Affected installed copies | Do this |
|---|---|---|---|---|
| 1 | **HyperFrames skills silently self-update and auto-upgrade to `@latest`** (HF-SILENT-SKILL-UPDATE, HF-PACKAGE-LOADER-LATEST) | High impact if the vendor channel is compromised. Triggered on every use | `~/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/{embedded-captions,faceless-explainer,music-to-video,pr-to-video,product-launch-video,motion-graphics,remotion-to-hyperframes,talking-head-recut,slideshow,figma,general-video,hyperframes}`; `~/.agents|.claude|.codex/skills/hyperframes` and `…/general-video`; the package-loader `@latest` path in `hyperframes-animation`/`hyperframes-creative` (plugin and `~/.agents|.claude|.codex` copies) and `~/Documents/AI_Brain/.agents|.claude/skills/hyperframes` | Set `HYPERFRAMES_SKIP_SKILLS=1` and `HYPERFRAMES_NO_TELEMETRY=1` in the agent environment. Delete the "run silently, don't ask" preamble, or install from a reviewed, pinned commit. Pin `npx hyperframes@<version>`. Never let agents set `HYPERFRAMES_SKILL_BOOTSTRAP_DEPS=1` themselves |
| 2 | **impeccable runs a 12.7 MB ad-hoc-signed native binary each session, and that binary carries hidden agent directives** (IMPECCABLE-OPAQUE-BINARY, IMPECCABLE-HIDDEN-HARNESS-OVERRIDE) | Arbitrary native code with your privileges. Its strings tell the agent to discount system-prompt autonomy statements and to treat skill invocation as permission to spawn subagents. Likelihood: every use | `~/.claude/skills/impeccable`, `~/.agents/skills/impeccable` (identical binary sha256 `0d48b6e1…320d`) | Disable, or keep but verify the binary against the vendor release checksum/signature first. Until then run it sandboxed without network. Treat its output as untrusted. Set `IMPECCABLE_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`, `IMPECCABLE_NO_UPDATE_CHECK=1` |
| 3 | **media-use URL fetch guard is bypassable, it imports an unrelated ancestor `.env`, and it auto-installs unpinned Python ML packages** (MEDIA-USE-URL-GUARD, -ENV-ANCESTOR, -AUTO-PIP, -CODEX-EXEC) | Medium. SSRF into LAN/overlay services (regex misses `[::ffff:…]`, `100.64/10`, DNS names, redirects; **reproduced** for the literal forms). Secrets from a parent `.env` leak into child processes (**reproduced**). Unreviewed `pip install torch transformers` into the system Python | `~/.agents|.claude|.codex/skills/media-use` (`086859…`) **and** `~/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/media-use` (`d98f7c…`). The affected files are hash-identical in both | Don't pass untrusted URLs to `resolve --from`. Keep projects out of directories under a `.env` you care about. Pre-install BGM deps in a pinned venv or avoid the generate path. Upstream fix: resolve and validate every hop, disable redirects, allowlist env keys |
| 4 | **SEO skill: redirect/DNS SSRF, Google OAuth refresh token written with default permissions (0644 under the usual umask 022), plaintext Gemini key plus an unpinned MCP server launched on every Claude start** (SEO-SSRF-REDIRECT, SEO-OAUTH-TOKEN-PERMS, SEO-BANANA-MCP-SETUP) | Medium. Audits routinely fetch third-party sites from a host that can reach Home Assistant, Kuma and router admin pages. The token carries Search Console **write** plus Indexing scopes. `npx -y @ycse/nanobanana-mcp` runs the latest package with your key | `~/.claude/skills/seo` (`63bc30…`) | `chmod 600 ~/.config/claude-seo/*token*` and `chmod 700` the directory. If you used the banana extension, move the key out of `~/.claude/settings.json` and pin the MCP package version. Audit third-party URLs from the noBGP cloud node, not from the Mac/LAN |
| 5 | **embedded-captions loads and runs HyperFrames code from `~/Downloads/hyperframes`** when present, and previews with `--disable-web-security` (EMBEDDED-CAPTIONS-DOWNLOADS-FALLBACK) | Low-medium. Code execution if anything named `hyperframes` lands in Downloads | `~/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/embedded-captions` | Keep `~/Downloads/hyperframes` absent, or set `HYPERFRAMES_ROOT` explicitly to a reviewed checkout |
| 6 | **Codex skill-installer installs from any GitHub ref with no commit pin** (CODEX-SKILL-INSTALLER-UNPINNED) | Medium when used. Installed skills become persistent trusted instructions and scripts | `~/.codex/skills/.system/skill-installer` | Install by commit SHA and read the diff before enabling |
| 7 | **Sites 0.1.65 publishes after every create/edit with no conversational confirmation** (SITES-AUTO-PUBLISH) | Low-medium. Edits to an already shared or public site go live, gated only by runtime tool approval. The older copy asked first | `~/.codex/plugins/cache/openai-curated-remote/sites/0.1.65/skills/sites-hosting` (not the older `12a6f7…` copy) | Keep Codex approval required for `deploy_site_version` |
| 8 | **Shared `/tmp` LibreOffice state in the Cowork Office skills** (DOCX-ACCEPT-CHANGES-SHARED-PROFILE, OFFICE-SOFFICE-SHIM) | Low on this single-user Mac, medium on shared Linux sandboxes. A pre-planted macro profile or preload `.so` runs in your soffice | Cowork skills-plugin `docx` (profile and shim), `xlsx` and `pptx` (shim) under `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/…/skills/` | No action needed on this Mac beyond awareness. Report upstream: use a private `mkdtemp` profile and shim |
| 9 | **Your own SEO pipeline runs share-hosted scripts and binaries as root without checksums** (NOBGP-SHARE-SCRIPTS-AS-ADMIN, plausible) | Low-medium. Depends on who can write `/mnt/<overlay>/networks/<network>/<share>` | `~/.claude/scheduled-tasks/weekly-seo-crawl`, `~/.claude/skills/seo-pipeline-run` | Record sha256 values in the skill and verify before `admin:true` execution. Restrict share write access |
| 10 | **Default-on telemetry and public feedback** (MEDIA-USE-TELEMETRY links the PostHog id to your HeyGen email; HF-FEEDBACK-PUBLIC posts render feedback with environment details publicly; IMPECCABLE-TELEMETRY-NETWORK) | Privacy, low. Likely by default | media-use (both copies), hyperframes-cli (plugin and `~/.agents|.claude|.codex`), impeccable (both) | Set `HYPERFRAMES_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`, `IMPECCABLE_NO_TELEMETRY=1`. Tell agents not to send feedback without approval |

Lower-severity items: SKILL-CREATOR-KILL-PORT and SKILL-CREATOR-NESTED-CLAUDE-P (Cowork skill-creator), TEMPLATE-CREATOR-RETAINS-PRIVATE-REFERENCES (Codex template-creator), COWORK-CUSTOMIZER-UNTRUSTED-CONTEXT-INTO-PLUGIN, REMOTION-ASKS-FOR-API-KEY (`~/.agents/skills/remotion-best-practices` and AI_Brain copies), HF-LOCATE-TMP-FONT (motion-graphics fixed `/tmp/locate-font.ttf`), HF-SEAM-GATE-SHELL (motion-doctrine `sh -c --server-cmd` plus `npx --yes`), HF-PR-CONTENT-INJECTION (pr-to-video treats PR text as planning input), SEO-API-KEY-IN-QUERY, SEO-FLOW-SYNC-UNPINNED, SEO-OAUTH-SCOPE (no state/PKCE), AIBRAIN-INGEST-PERSISTENCE, SITES-TRUSTED-IDENTITY-HEADERS (latent), MEDIA-USE-LOCAL-RUN-SHELL (latent, no caller), DOCUMENTS-TMPDIR-OVERRIDE (info). Full records with file:line evidence, preconditions and fixes are in `target-reviews.json` → `concern_catalog`.

---

## 2. Confirmed behaviour (present in source; evidence checked)

**Supply chain / change control**
- *HF-SILENT-SKILL-UPDATE*: ten plugin workflow skills begin with "First, keep this skill fresh — run silently, don't ask: `npx hyperframes skills update <name>`". general-video and the router do the same. The router (`hyperframes/SKILL.md:39-42`) tells the agent to upgrade the project CLI to `@latest` and "act on the signal rather than relaying it to the user". `init` refreshes skills from GitHub, `--skip-skills` is ignored, and the only opt-out is `HYPERFRAMES_SKIP_SKILLS=1`. Scanner keys confirmed for this family of unpinned or self-updating instructions: 50 RP1 (this preamble, the router upgrade, bare `npx hyperframes`, `npx impeccable update`, and a few remotion/SEO docs) and 2 EA2. The AI_Brain `remotion-to-hyperframes` copy (`3c2215…`) does **not** contain the preamble; the plugin copy (`673e7b…`) does.
- *HF-PACKAGE-LOADER-LATEST*: `scripts/package-loader.mjs` treats `@hyperframes/producer@latest` as pinned for installs outside a hyperframes tree, which is exactly how these skills are installed. In non-TTY runs its error text tells the agent to set the consent bypass env var.
- Other unpinned fetches: `npx skills add heygen-com/hyperframes` from GitHub HEAD. `npx skills add pixel-point/animate-text` installs a third-party skill (hyperframes-animation, both copies). `uvx --from openai-whisper` (changelog-video). `npx create-video@latest --yes` (remotion-best-practices). Caret ranges in the remotion-to-hyperframes test fixtures (10 SC1 keys). `sync_flow.py` pulls prompt files from GitHub HEAD into SEO references.
- *CODEX-SKILL-INSTALLER-UNPINNED* (extraction itself is hardened: zip-slip and symlink checks; tokens are sent only to GitHub hosts).
- sites-building 0.1.65 lockfile: esbuild 0.18.20 dev-only, transitive (GHSA-67mh-4wv8-2f99 range). Confirmed but low, since it matters only while a dev server is exposed.

**Opaque code / hidden instruction channel**
- *IMPECCABLE-OPAQUE-BINARY* and *IMPECCABLE-HIDDEN-HARNESS-OVERRIDE*: the directive strings `AUTONOMY_DIRECTIVE_CHECK` and `SUBAGENT_AUTHORIZATION` are present in the binary, and SKILL.md tells the agent to run `scripts/impeccable context` and "follow its directives". The launcher also honours `$IMPECCABLE_BIN`, `~/.impeccable/bin` and `PATH`, and downloads updates with a same-origin `.sha256` (integrity, not authenticity).

**Network / SSRF**
- *MEDIA-USE-URL-GUARD*: `scripts/lib/freeze.mjs:8-35,56-70` uses a literal-hostname regex and default `redirect:'follow'`. Earlier runtime check (no real network): `[::ffff:7f00:1]` and `[::ffff:c0a8:101]` were accepted, and a mocked redirect wrote a private response.
- *SEO-SSRF-REDIRECT*: `fetch_page.py:92-115` checks one IPv4 resolution then follows redirects. `validate_url()` never resolves DNS. `nlp_analyze`/`verify_backlinks` follow redirects. Sub-skill docs overstate this protection. Not exercised at runtime.

**Secrets and data handling**
- *MEDIA-USE-ENV-ANCESTOR* (`audio/scripts/lib/heygen.mjs:19-46`, both copies; **runtime-reproduced**). The PE3 keys for both copies are confirmed.
- *SEO-OAUTH-TOKEN-PERMS* (`scripts/google_auth.py:173-177` writes the token with default mode; the bundled `release_report.py` even documents this). *SEO-BANANA-MCP-SETUP* (`extensions/banana/scripts/setup_mcp.py:21-99`). *SEO-API-KEY-IN-QUERY*.
- *MEDIA-USE-TELEMETRY*: `$identify` maps the anonymous id to the email in `~/.heygen/credentials`. *HF-FEEDBACK-PUBLIC*.

**Execution / temp files / process control**
- *EMBEDDED-CAPTIONS-DOWNLOADS-FALLBACK* (`scripts/matte.cjs` hfCli, `scripts/preview-frames.cjs`).
- *DOCX-ACCEPT-CHANGES-SHARED-PROFILE*: `accept_changes.py:16,58-66,91-118`. The scanner did not detect this as a vulnerability. *OFFICE-SOFFICE-SHIM*: `soffice.py` sha256 `c1b83a67…` is identical in xlsx/docx/pptx; the runtime check reproduced only the path selection. 3 AST4 keys for the shim and 2 for the profile are confirmed.
- *SKILL-CREATOR-KILL-PORT*: `eval-viewer/generate_review.py:288-306` SIGTERMs whatever listens on port 3117 (1 AST4 key confirmed). *SKILL-CREATOR-NESTED-CLAUDE-P*: `run_eval.py` runs `claude -p` with ambient permissions.
- *MEDIA-USE-AUTO-PIP* (`bgm.mjs`) and *MEDIA-USE-CODEX-EXEC* (`codex exec -s workspace-write` with "Do not ask for confirmation").
- *SITES-AUTO-PUBLISH*: `sites-hosting/SKILL.md` Rules and `references/publishing.md` in 0.1.65.

## 3. Plausible but unverified

- **impeccable directive emission**: the strings are in the binary and SKILL.md says to follow its output, but the binary was not run, so whether and when they reach the agent is inferred. Test 6 in `coverage-gaps.md` would settle it.
- **noBGP share scripts as root**: whether anything other than you can write the share is unknown (ACLs not reviewed).
- **SEO and media-use SSRF against real LAN services**: code paths are confirmed, but no live redirect or DNS-rebinding test was run (tests 1-2).
- **Native `.so`/`.dylib` in the SEO venv (81)**: RECORD proves they are what pip installed, not what PyPI published.
- **Advisories**: the SEO venv packages (7 keys), @babel/core 7.29.0, and remotion fixture ranges are name-only matches without version verification.
- **HyperFrames CLI behaviour** (what `skills update`, feedback and telemetry actually send or replace): the CLI source is not in any snapshot.
- **Presentations 3.12 `.pyc`**: header matches the source size; equivalence not verified.
- **COWORK-CUSTOMIZER-UNTRUSTED-CONTEXT-INTO-PLUGIN** and **HF-PR-CONTENT-INJECTION**: prompt-injection surfaces by design; no exploit demonstrated.

## 4. Expected privileged or data-sharing functionality (by design; know it's there)

- Publishing and deployment: Codex `sites-hosting` (private by default; see risk 7). SEO `indexing_notify.py` pushes URL updates to Google Indexing API. `contribute-catalog` publishes to hyperframes.dev and opens PRs. HyperFrames cloud/lambda renders.
- Live control of your data: `excel-live-control` edits open workbooks (add-in install and sign-in left to you). `schedule` creates autonomous recurring tasks. `consolidate-memory` and `import-memory` rewrite memory (import-memory is additive, filtered and confirm-first). `explain-usage` reads session transcripts.
- Third-party APIs using your keys from the environment: HeyGen, ElevenLabs, OpenAI, Groq, DataForSEO, Moz, Google APIs, Gemini. `pr-to-video` reads PRs via `gh`. `template-creator` exports Google Workspace files through the Drive connector.
- Persistent configuration writes: `plugin-creator` writes to `~/.agents/plugins/marketplace.json`, `skill-creator`/`template-creator` to `~/.codex/skills`. impeccable hooks and live mode (explicit consent). media-use keeps a global asset cache.
- Hardened helpers worth noting: sites-building install scripts verify the lockfile integrity and the vinext tarball hash. `sites-hosting` packaging rejects symlinks and paths outside the project. `visualize` renders in a sandboxed iframe with a strict CSP and binds to localhost. The template-creator export receiver confines writes to the workspace with `O_EXCL` and `0600`.
- The 20 Codex `artifact-template-*` skills are inert reference documents: no macros, ActiveX, OLE, external links or DDE/WEBSERVICE formulas; one `example.com` hyperlink.

## 5. False positives (scanner noise, with counts)

1,139 keys. Main groups:
- **P9** (713): long Markdown table rows padded for alignment, flagged as context stuffing.
- **P2** (200): 61 distinct benign HTML comment bodies.
- **LP3** (35): missing `allowed-tools`. This grants nothing; normal permission prompts still apply, and Codex ignores the field.
- **AE1** (28 of 50): the "evasion" files are local plain text and were read in full. The other 22 remain unresolved until read.
- **RP1** (31): commands that resolve locally or are documentation.
- **EA2** (30), **AR2** (15), **MP2** (10), **EA3** (7), **EA4** (6), **TM3** (5), **E1** (10), **SSRF1** (3): phrase matches such as "no warning" or "not limited to" in license text; loop *prohibitions*; blocklists and test fixtures listing `169.254.169.254`; `rm -rf ~` inside a comment explaining argv safety.

The initial ledger was rechecked, not trusted. 39 RP1 keys the ledger had marked `confirmed_concern` were reclassified: 27 false positive and 12 expected behaviour. All 513 ledger `expected_behavior` keys (P9 formatting checks) were reclassified as false positives, since they describe formatting, not behaviour. 34 keys the ledger left unresolved are now confirmed concerns.

## 6. Disposition by scanner rule

| Rule | Total | confirmed_concern | expected_behavior | false_positive | unresolved |
|---|---|---|---|---|---|
| SC9 | 6098 | 0 | 6014 | 0 | 84 |
| P9 | 713 | 0 | 0 | 713 | 0 |
| P2 | 200 | 0 | 0 | 200 | 0 |
| RP1 | 94 | 50 | 13 | 31 | 0 |
| AE1 | 50 | 0 | 0 | 28 | 22 |
| EA2 | 44 | 2 | 12 | 30 | 0 |
| LP3 | 35 | 0 | 0 | 35 | 0 |
| AST4 | 35 | 6 | 29 | 0 | 0 |
| E1 | 32 | 0 | 22 | 10 | 0 |
| SC1 | 28 | 10 | 18 | 0 | 0 |
| RA2 | 27 | 0 | 22 | 3 | 2 |
| SC4 | 17 | 1 | 0 | 0 | 16 |
| AR2 | 15 | 0 | 0 | 15 | 0 |
| SC8 | 15 | 0 | 13 | 0 | 2 |
| PE3 | 14 | 2 | 6 | 6 | 0 |
| AS3 | 11 | 0 | 5 | 6 | 0 |
| MP2 | 10 | 0 | 0 | 10 | 0 |
| TM1 | 8 | 0 | 6 | 2 | 0 |
| E2 | 7 | 0 | 5 | 2 | 0 |
| EA3 | 7 | 0 | 0 | 7 | 0 |
| EA4 | 6 | 0 | 0 | 6 | 0 |
| TM2 | 6 | 0 | 4 | 2 | 0 |
| TM3 | 5 | 0 | 0 | 5 | 0 |
| PE2 | 5 | 0 | 4 | 1 | 0 |
| OH3 | 4 | 0 | 0 | 4 | 0 |
| AST7 | 4 | 0 | 0 | 4 | 0 |
| RA1 | 4 | 0 | 1 | 3 | 0 |
| SSRF2 | 4 | 0 | 4 | 0 | 0 |
| EA5 | 4 | 0 | 4 | 0 | 0 |
| SSRF1 | 3 | 0 | 0 | 3 | 0 |
| MP3 | 3 | 0 | 0 | 3 | 0 |
| P6 | 3 | 0 | 0 | 3 | 0 |
| YR4 | 3 | 0 | 0 | 1 | 2 |
| AS1 | 3 | 0 | 2 | 1 | 0 |
| E5 | 2 | 0 | 2 | 0 | 0 |
| TT3 | 2 | 0 | 2 | 0 | 0 |
| P7 | 2 | 0 | 2 | 0 | 0 |
| AE2 | 2 | 0 | 0 | 2 | 0 |
| AE4 | 1 | 0 | 0 | 1 | 0 |
| AR1 | 1 | 0 | 0 | 1 | 0 |
| BH1 | 1 | 0 | 1 | 0 | 0 |
| P1 | 1 | 0 | 0 | 1 | 0 |
| OH1 | 1 | 0 | 1 | 0 | 0 |

## 7. Review coverage and outstanding work

| Item | Status |
|---|---|
| Targets accounted for | 140 / 140 (79 with findings, 61 without). Each has a record in `target-reviews.json` |
| Finding keys accounted for | 7,530 / 7,530, no duplicates. `finding_id` and rule match the ledger for every key |
| Keys decided | 7,402 (71 confirmed, 6,192 expected, 1,139 false positive) |
| Keys unresolved | 128: SC9 84 (81 SEO native libs, impeccable binary ×2, Presentations pyc), AE1 22, SC4 16, SC8 2, RA2 2, YR4 2 |
| Target status | 119 `reviewed_with_gaps`, 21 `reviewed_no_open_gaps` (not a safety label) |
| Files fully read | Entry SKILL.md/command file for 125 of 140 targets (the 15 exceptions are listed at the top), plus the key scripts behind each concern. Large helper scripts in embedded-captions, pr/product/faceless video, hyperframes-animation/creative, media-use (outside the read set), Codex Presentations/Spreadsheets/excel-live-control and sites-building SKILL.md bodies were read partially or grep-swept only |
| Not in any snapshot | HyperFrames CLI/registry code; Codex Sites plugin-root scripts and preview daemon; connector/tool implementations; noBGP share scripts; SEO extension installers; changelog-video LFS media |
| Proposed isolated tests (not run) | 7 tests in `coverage-gaps.md` §8 (SSRF redirect/DNS, token file mode, LibreOffice profile, package-loader consent, impeccable sandboxed run, `skills update` diff) |
| Needs your authorisation or input | Network or offline mirror for advisory and upstream-hash checks; a CPython 3.12 sandbox; read access to the noBGP share and its ACLs; approval to run the tests |

**Resume:** `verification.json` → `resumable_worklist` has 212 entries: 128 unresolved keys plus 84 targets with files not fully read, each with sample paths. `coverage-gaps.md` §7 gives the priority order.

## 8. Deliverables

- `finding-assessments.json`: one record per ledger key (`key`, `finding_id`, `rule`, `severity`, the original ledger decision, `disposition`, `reason`, `evidence` {snapshot path, file, sha256, line, scanner match}, `preconditions`, `impact`, `recommended_action`, `review_method`, `decision_group` enumerating equivalence groups, and `missing_evidence` for unresolved keys).
- `target-reviews.json`: one record per target with installed locations, `review_status`, per-file sha256 and `review_depth`, findings by disposition, additional concerns, runtime/permission assumptions, gaps and next steps, plus the full `concern_catalog`.
- `coverage-gaps.md`: unresolved items, opaque artifacts, advisories, out-of-snapshot references, scanner limits, worklist, proposed tests.
- `verification.json`: reconciliation counts and resumable worklist.
