# Coverage gaps and outstanding work

Generated 2026-09-16. Scope: 140 targets, 7,530 ledger keys (all accounted for; see `verification.json`).

This file lists what the review did **not** establish. Nothing here was executed; no credentials were read; no installed skill was changed. Owner column: **you** = the machine owner (<user>); **vendor** = the skill publisher; **reviewer** = a follow-up review pass.

## 1. Headline numbers

- Finding keys decided: 7402 of 7,530; **unresolved: 128**.
- Target review status: 119 `reviewed_with_gaps`, 21 `reviewed_no_open_gaps` (the latter means every text file was read and nothing is unresolved - it is not a safety certification).
- File review depth across all 10904 indexed files: full 277, diffed against a read copy 0, partial line ranges 99, finding-context only 215, structural (OOXML) 20, grep/risk-sweep only 703, bulk hash-verified SEO `.venv` 8345, not individually reviewed 1245.
- Resumable worklist entries in `verification.json`: 212.

## 2. Unresolved findings (128 keys)

| Rule | Target | Keys | What is missing | Owner / next action |
|---|---|---|---|---|
| AE1 | Spreadsheets `ad421b645c52` | 1 | Complete line-by-line read of the referenced file. (SKILL.md) | reviewer: full read of the listed file (hash-pinned) |
| AE1 | embedded-captions `553101bd77f1` | 5 | Complete line-by-line read of the referenced file. (SKILL.md) | reviewer: full read of the listed file (hash-pinned) |
| AE1 | faceless-explainer `c8e57b32fda0` | 2 | Complete line-by-line read of the referenced file. (SKILL.md) | reviewer: full read of the listed file (hash-pinned) |
| AE1 | hyperframes-animation `35d2cc77762b` | 1 | Complete line-by-line read of the referenced file. (SKILL.md) | reviewer: full read of the listed file (hash-pinned) |
| AE1 | hyperframes-animation `52f41c05f4f3` | 1 | Complete line-by-line read of the referenced file. (SKILL.md) | reviewer: full read of the listed file (hash-pinned) |
| AE1 | hyperframes-audio `965b323bcb61` | 1 | Complete line-by-line read of the referenced file. (SKILL.md) | reviewer: full read of the listed file (hash-pinned) |
| AE1 | hyperframes-audio `c9c974271603` | 1 | Complete line-by-line read of the referenced file. (SKILL.md) | reviewer: full read of the listed file (hash-pinned) |
| AE1 | hyperframes-creative `72de3f297c9a` | 1 | Complete line-by-line read of the referenced file. (SKILL.md) | reviewer: full read of the listed file (hash-pinned) |
| AE1 | hyperframes-creative `dfac9a5b177c` | 1 | Complete line-by-line read of the referenced file. (SKILL.md) | reviewer: full read of the listed file (hash-pinned) |
| AE1 | motion-doctrine `0952da6cdbcd` | 1 | Complete line-by-line read of the referenced file. (SKILL.md) | reviewer: full read of the listed file (hash-pinned) |
| AE1 | motion-graphics `d9b54ccd300a` | 1 | Complete line-by-line read of the referenced file. (SKILL.md) | reviewer: full read of the listed file (hash-pinned) |
| AE1 | pr-to-video `cfe2ba681867` | 4 | Complete line-by-line read of the referenced file. (SKILL.md) | reviewer: full read of the listed file (hash-pinned) |
| AE1 | product-launch-video `f314adc72d30` | 2 | Complete line-by-line read of the referenced file. (SKILL.md) | reviewer: full read of the listed file (hash-pinned) |
| RA2 | media-use `086859be5f81` | 1 | Upstream CLI source (hyperframes telemetry) to confirm what is sent with the shared anonymousId; not in snapshot. (scripts/lib/telemetry.mjs) | vendor/reviewer: obtain hyperframes CLI telemetry source |
| RA2 | media-use `d98f7cb7b073` | 1 | Upstream CLI source (hyperframes telemetry) to confirm what is sent with the shared anonymousId; not in snapshot. (scripts/lib/telemetry.mjs) | vendor/reviewer: obtain hyperframes CLI telemetry source |
| SC4 | remotion-to-hyperframes `3c22157178ba` | 4 | Version-specific advisory check (OSV/GHSA lookup against the exact installed or locked version) - requires authorised offline advisory DB or network lookup. (2 files (e.g. assets/test-corpus/tier-1-title-card/remotion-src/package.json)) | reviewer: OSV/GHSA lookup for the exact versions (needs authorised network or offline advisory DB) |
| SC4 | remotion-to-hyperframes `673e7bf03075` | 4 | Version-specific advisory check (OSV/GHSA lookup against the exact installed or locked version) - requires authorised offline advisory DB or network lookup. (2 files (e.g. assets/test-corpus/tier-1-title-card/remotion-src/package.json)) | reviewer: OSV/GHSA lookup for the exact versions (needs authorised network or offline advisory DB) |
| SC4 | seo `63bc30fd9cdd` | 7 | Version-specific advisory check (OSV/GHSA lookup against the exact installed or locked version) - requires authorised offline advisory DB or network lookup. (requirements.txt) | reviewer: OSV/GHSA lookup for the exact versions (needs authorised network or offline advisory DB) |
| SC4 | sites-building `ffdb4e028568` | 1 | Version-specific advisory check (OSV/GHSA lookup against the exact installed or locked version) - requires authorised offline advisory DB or network lookup. (templates/vinext-starter/package-lock.json) | reviewer: OSV/GHSA lookup for the exact versions (needs authorised network or offline advisory DB) |
| SC8 | Presentations `a759b8ebafea` | 2 | Bytecode equivalence check with the matching CPython minor version (3.12 not installed) or recompilation in an isolated interpreter. (2 files (e.g. container_tools/__pycache__/)) | reviewer: install CPython 3.12 in an isolated env and compare code objects |
| SC9 | Presentations `a759b8ebafea` | 1 | Provenance for opaque native code: vendor signature / reproducible build / hash match against the upstream wheel or release artifact, or isolated dynamic analysis. (container_tools/__pycache__/runtime_helpers.cpython-312.pyc) | reviewer: obtain upstream wheel/release hashes or signatures (needs authorised network or offline mirror); else isolated dynamic analysis |
| SC9 | impeccable `2c076dbc72de` | 1 | Provenance for opaque native code: vendor signature / reproducible build / hash match against the upstream wheel or release artifact, or isolated dynamic analysis. (scripts/bin/darwin-arm64/impeccable) | reviewer: obtain upstream wheel/release hashes or signatures (needs authorised network or offline mirror); else isolated dynamic analysis |
| SC9 | impeccable `40a46b6bc1fa` | 1 | Provenance for opaque native code: vendor signature / reproducible build / hash match against the upstream wheel or release artifact, or isolated dynamic analysis. (scripts/bin/darwin-arm64/impeccable) | reviewer: obtain upstream wheel/release hashes or signatures (needs authorised network or offline mirror); else isolated dynamic analysis |
| SC9 | seo `63bc30fd9cdd` | 81 | Provenance for opaque native code: vendor signature / reproducible build / hash match against the upstream wheel or release artifact, or isolated dynamic analysis. (81 files (e.g. .venv/lib/python3.13/site-packages/81d243bd2c585b0f4821__mypyc.cpython-313-darwin.so)) | reviewer: obtain upstream wheel/release hashes or signatures (needs authorised network or offline mirror); else isolated dynamic analysis |
| YR4 | impeccable `2c076dbc72de` | 1 | Reverse engineering or isolated execution of the binary to determine whether the matched strings are ever emitted to an agent. (scripts/bin/darwin-arm64/impeccable) | reviewer: isolated reverse engineering of the impeccable binary |
| YR4 | impeccable `40a46b6bc1fa` | 1 | Reverse engineering or isolated execution of the binary to determine whether the matched strings are ever emitted to an agent. (scripts/bin/darwin-arm64/impeccable) | reviewer: isolated reverse engineering of the impeccable binary |

## 3. Opaque binaries, bytecode and native code

- **impeccable** (`~/.claude/skills/impeccable`, `~/.agents/skills/impeccable`): `scripts/bin/darwin-arm64/impeccable`, sha256 `0d48b6e16aa97664fdbe607d5da9ae320e389a1843e0ff1328f8c2530530320d`, 12,762,240 bytes, Rust Mach-O arm64, ad-hoc linker-signed (no Developer ID). Only `strings` output was reviewed. It is executed every session by SKILL.md setup and by optional hooks. **Next:** compare the hash with the vendor GitHub release checksum and signature, or build it from source. Until then, run it only in a sandboxed profile with no network. Owner: you/vendor.
- **SEO `.venv`** (`~/.claude/skills/seo`): 56 pip distributions pass RECORD sha256 verification (0 mismatched, 0 missing; INSTALLER=pip; no `direct_url.json`). All 2,947 `.pyc` files match `compile()` of the adjacent source by code-object equality. `bin/python` is byte-identical to the PSF-signed framework Python 3.13. The Playwright `node` binary is Node.js-Foundation-signed (`codesign -v` passes). **81 native `.so`/`.dylib` files are unresolved**: RECORD only proves they match what pip installed, not what PyPI published. **Next:** hash-compare against the matching PyPI wheels (network lookup needs authorisation). Owner: reviewer.
- **Presentations (Codex)** `container_tools/__pycache__/runtime_helpers.cpython-312.pyc`: the header source size (3,513) matches the adjacent `.py`, but CPython 3.12 is not installed, so bytecode equivalence was not verified. Owner: reviewer.
- **Artifact-template OOXML packages** (20 Codex templates): no macros, ActiveX, OLE, externalLink, customUI, DDE/WEBSERVICE/RTD formulas or unexpected external relationships were found (one `example.com` hyperlink). Embedded chart workbooks were checked recursively. Images and embedded `.odttf` fonts inside them were not content-analysed (scanner `opaque_content`/`archive_member_size_limit`: 11 members). Low priority.
- Remaining non-text `other_artifact` files (PNG/SVG icons, fonts, audio/video samples, LFS pointers) were not individually analysed. **changelog-video**: its media files are Git LFS pointer stubs, so the real assets are missing from the snapshot.

## 4. Dependencies and advisories

- **SEO `.venv` installed versions** (requests 2.34.2, lxml 6.1.1, pillow 12.2.0, urllib3 2.7.0, validators 0.35.0, weasyprint 68.1, openpyxl 3.1.5): the scanner matched advisories by package name only. No version-specific advisory check was possible offline, so these stay unresolved (7 SC4 keys).
- **sites-building (newer, `openai-curated-remote/sites/0.1.65`)** `package-lock.json`: esbuild 0.18.20 (dev-only, transitive through drizzle-kit) falls in the GHSA-67mh-4wv8-2f99 dev-server range and is **confirmed but low** (it matters only while a dev server is running and reachable). @babel/core 7.29.0 against CVE-2026-49356 is unresolved.
- **remotion-to-hyperframes** test-corpus fixtures (both copies) use caret ranges (confirmed SC1 hygiene issue). The react/react-dom/remotion/zod advisory matches are name-only and unresolved: the ranges would resolve at install time and nothing is installed in the snapshot.
- **Unpinned runtime fetches that no lockfile can cover:** `npx hyperframes …` / `npx hyperframes@latest` / `npx skills add` (HyperFrames family), `npx -y @ycse/nanobanana-mcp` (SEO banana extension), `uvx --from openai-whisper` (changelog-video), `pip install transformers torch …` (media-use BGM), `npx create-video@latest --yes` (remotion-best-practices), GitHub-HEAD prompt sync (`seo sync_flow.py`), and skill-installer installs from any GitHub ref. These cannot be assessed statically. Their risk is recorded as concerns in `SUMMARY.md`.

## 5. References that leave the snapshot or could not be resolved

The scanner logged 1043 `reference_unresolved` exceptions across 99 targets. A line-level heuristic re-classification gives: 669 name project or runtime artifacts that only exist once a workflow runs (e.g. `index.html`, `plan.json`, `BRIEF.md`, `hyperframes.json`), or files outside the skill; 251 are not paths (code, numbers, version strings); 53 resolve inside the snapshot (scanner ambiguity); 39 point at sibling skills (`../hyperframes-core/...`), which are separate targets in this inventory; 31 are placeholders (`<SKILL_DIR>`, `$PROJECT_DIR`).

Specific out-of-snapshot dependencies that affect security conclusions:
- **HyperFrames CLI / registry / studio** (`npx hyperframes`, `@hyperframes/producer`, registry fetched from GitHub `main`): the code that actually runs (render, capture, transcribe, remove-background, publish, feedback, telemetry) is not in any snapshot. Owner: vendor/reviewer.
- **Codex Sites plugin root scripts** (`<plugin-root>/scripts/build-site.mjs`, `package-site.mjs`, `configure-execution-profile.mjs`, `install-dependencies.mjs`, `project-setup.mjs`) are referenced by sites-building/sites-hosting 0.1.65 but not included. Neither is the `sites-preview` daemon.
- **Connector/tool implementations** (Sites, Google Drive, Plugin Management, docs connector, memory tools, scheduled tasks, Cowork widgets) enforce the approvals these skills rely on and are outside scope.
- **SEO extensions**: `extensions/dataforseo/install.sh` and other extension installers are mentioned but absent from the snapshot. **noBGP share contents** (`bootstrap.sh`, `audit.sh`, binaries under `/mnt/<overlay>/networks/<network>/<share>`) used by weekly-seo-crawl/seo-pipeline-run were not reviewed. Owner: you.
- **impeccable** downloads engine updates from GitHub releases and calls `impeccable.style` APIs; server behaviour is unknown.

## 6. Scanner analysis limits (per `targets/*.json`)

| reason_code | exceptions | targets | Handling in this review |
|---|---|---|---|
| excluded_executable_content | 5010 | 5 | SEO `.venv` bytecode/natives verified in bulk (section 3); impeccable binary strings-only; pptx/Presentations pyc handled at finding level |
| reference_unresolved | 1043 | 99 | Section 5 |
| static_parse_limit | 195 | 40 | Large JS/Python helpers; key scripts were read in full (see target-reviews depth). The rest are listed in the worklist |
| obfuscated_instruction_text | 60 | 24 | All 47 flagged files were scanned for zero-width, bidi-override, tag or other format/private-use Unicode characters, base64 runs of 120+ characters and escaped-byte runs. None were found. Most flagged files are minified gsap.min.js, OOXML XSD schemas and long HTML/JSON. The ones read in full (import-memory SKILL.md, api-map.md, failure-modes.md, data-attributes.md, docx_ooxml_patch.py) contain no hidden instructions. Minified vendor bundles were not de-minified or hash-matched to upstream releases |
| archive_member_size_limit | 11 | 7 | Section 3 (template media/fonts) |
| opaque_content | 11 | 7 | Section 3 |
| output_limit | 3 | 2 | package-lock.json / one pip vendored .pyc; lockfile covered by SC4/SC1 decisions |

## 7. Files not fully read (resumable worklist)

Every target has a per-file `review_depth` in `target-reviews.json`. Targets with the most source/documentation files not fully read:

| Not fully read / text files | Target | Installed at |
|---|---|---|
| 129 / 136 | media-use `086859be5f81` | `/Users/<user>/.agents/skills/media-use` |
| 125 / 132 | media-use `d98f7cb7b073` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/media-use` |
| 119 / 121 | hyperframes-animation `52f41c05f4f3` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/hyperframes-animation` |
| 119 / 121 | hyperframes-animation `35d2cc77762b` | `/Users/<user>/.agents/skills/hyperframes-animation` |
| 111 / 118 | sites-building `ffdb4e028568` | `/Users/<user>/.codex/plugins/cache/openai-curated-remote/sites/0.1.65/skills/sites-building` |
| 92 / 93 | embedded-captions `553101bd77f1` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/embedded-captions` |
| 79 / 79 | documents `164205dccb5d` | `/Users/<user>/.codex/plugins/cache/openai-primary-runtime/documents/26.909.12148/skills/documents` |
| 71 / 72 | hyperframes-creative `dfac9a5b177c` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/hyperframes-creative` |
| 71 / 72 | hyperframes-creative `72de3f297c9a` | `/Users/<user>/.agents/skills/hyperframes-creative` |
| 64 / 65 | music-to-video `c3c9064f3716` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/music-to-video` |
| 63 / 64 | remotion-to-hyperframes `673e7bf03075` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/remotion-to-hyperframes` |
| 62 / 64 | remotion-to-hyperframes `3c22157178ba` | `/Users/<user>/Documents/AI_Brain/.agents/skills/remotion-to-hyperframes` |
| 61 / 61 | docx `d351bbfe01bf` | `/Users/<user>/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/<cowork-session-id>/<cowork-workspace-id>/skills/docx` |
| 57 / 58 | Presentations `a759b8ebafea` | `/Users/<user>/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations` |
| 56 / 63 | seo `63bc30fd9cdd` | `/Users/<user>/.claude/skills/seo` |
| 56 / 56 | pptx `4c0807ecbc74` | `/Users/<user>/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/<cowork-session-id>/<cowork-workspace-id>/skills/pptx` |
| 53 / 53 | xlsx `b08cbf3a6afb` | `/Users/<user>/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/<cowork-session-id>/<cowork-workspace-id>/skills/xlsx` |
| 47 / 53 | impeccable `40a46b6bc1fa` | `/Users/<user>/.agents/skills/impeccable` |
| 46 / 48 | impeccable `2c076dbc72de` | `/Users/<user>/.claude/skills/impeccable` |
| 45 / 46 | hyperframes `a64d3df49f24` | `/Users/<user>/Documents/AI_Brain/.agents/skills/hyperframes` |
| 43 / 46 | seo-flow `516fc04f9f2e` | `/Users/<user>/.claude/skills/seo-flow` |
| 34 / 39 | remotion-best-practices `02ff1414aad6` | `/Users/<user>/.agents/skills/remotion-best-practices` |
| 28 / 30 | pr-to-video `cfe2ba681867` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/pr-to-video` |
| 27 / 28 | product-launch-video `f314adc72d30` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/product-launch-video` |
| 23 / 24 | faceless-explainer `c8e57b32fda0` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/faceless-explainer` |
| 22 / 22 | talking-head-recut `5e13536b89a4` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/talking-head-recut` |
| 21 / 23 | motion-graphics `d9b54ccd300a` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/motion-graphics` |
| 19 / 20 | hyperframes-core `f6d981ad2343` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/hyperframes-core` |
| 19 / 20 | hyperframes-core `79accbf4da5d` | `/Users/<user>/.agents/skills/hyperframes-core` |
| 18 / 18 | Spreadsheets `ad421b645c52` | `/Users/<user>/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.909.12148/skills/spreadsheets` |
| 16 / 18 | skill-creator `50d502c03129` | `/Users/<user>/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/<cowork-session-id>/<cowork-workspace-id>/skills/skill-creator` |
| 15 / 17 | hyperframes `6934b94a090a` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/hyperframes` |
| 15 / 17 | hyperframes `5b039b2ddf0d` | `/Users/<user>/.agents/skills/hyperframes` |
| 13 / 13 | excel-live-control `073e2df9fa89` | `/Users/<user>/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.909.12148/skills/excel-live-control` |
| 12 / 15 | seo-google `f5130a147104` | `/Users/<user>/.claude/skills/seo-google` |
| 11 / 12 | hyperframes-registry `d13d741b97b1` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/hyperframes-registry` |
| 11 / 12 | hyperframes-registry `92186ae18b0b` | `/Users/<user>/.agents/skills/hyperframes-registry` |
| 10 / 11 | hyperframes-cli `ed6cdebae152` | `/Users/<user>/.agents/skills/hyperframes-cli` |
| 10 / 11 | hyperframes-cli `a439d7e7b106` | `/Users/<user>/.claude/plugins/cache/claude-plugins-official/hyperframes/0.8.3/skills/hyperframes-cli` |
| 9 / 11 | imagegen `e27465f2b192` | `/Users/<user>/.codex/skills/.system/imagegen` |
| … | 44 more targets | see verification.json worklist |

Priority order for the next pass: (0) full reads of the entry SKILL.md for the 15 targets where it was not fully read: Presentations, Spreadsheets, excel-live-control, documents, visualize, sites-building ×2, docx, xlsx, pptx, media-use ×2, remotion-to-hyperframes `3c2215`, remotion-best-practices, talking-head-recut; (1) embedded-captions `make-theme.cjs` (459 KB) and `make-cinematic.cjs`; (2) pr-to-video/product-launch-video/faceless-explainer `build-frame.mjs`, `audio.mjs`, `ingest.mjs`, `assemble-index.mjs`; (3) hyperframes-animation/creative `animation-map.mjs`, `contrast-report.mjs`, `package-loader.mjs`; (4) media-use scripts outside the already-read set; (5) Codex Presentations `container_tools` and Spreadsheets/excel-live-control SKILL.md bodies; (6) sites-building SKILL.md bodies; (7) SEO sub-skill scripts that were only grep-swept.

## 8. Proposed isolated tests (not run; need your go-ahead)

Each test should run in a throwaway VM or container with no real credentials, a fake HOME and egress limited to a local mock server.
1. **media-use URL guard (both copies):** replay `resolve --from` against a local HTTP server that 302-redirects to `127.0.0.1`/`100.64.x.x`, and against a DNS name resolving to RFC1918. Confirm redirect following and cache writes. (Earlier runtime results already cover the literal IPv4-mapped IPv6 acceptance and a mocked redirect.)
2. **SEO `fetch_page.py` / `capture_screenshot.py`:** same redirect and DNS-rebinding harness, to confirm private content reaches stdout or screenshots.
3. **SEO OAuth token file mode:** run `_save_oauth_token` with a dummy token under umask 022 and confirm the resulting mode is 0644.
4. **docx `accept_changes.py`:** as user A, pre-create `/tmp/libreoffice_docx_profile/user/basic/Standard/Module1.xba` containing a benign marker macro. Run the script as user B and check whether the marker executes.
5. **HyperFrames package-loader:** in a non-TTY run, confirm the error text steers the agent to set `HYPERFRAMES_SKILL_BOOTSTRAP_DEPS=1`, and that `@latest` passes `assertPinnedPackageSpecs`. Use a local npm registry mock.
6. **impeccable binary:** run `impeccable context` under a sandbox-exec profile with network denied and file access logged. Capture the directive text it emits (AUTONOMY_DIRECTIVE_CHECK / SUBAGENT_AUTHORIZATION) and every network attempt.
7. **`npx hyperframes skills update`:** point it at a local registry mirror and diff the files it would replace.

## 9. Inputs or authorisation still needed

- Network (or an offline mirror) for advisory lookups (OSV/GHSA) and upstream hash/signature comparison of the SEO wheels and the impeccable release. This review deliberately made no external requests.
- A CPython 3.12 interpreter in an isolated environment for the Presentations `.pyc` check.
- Read access to the noBGP Cloud share scripts (`bootstrap.sh`, `audit.sh`, cached binaries) and their ACLs, to settle NOBGP-SHARE-SCRIPTS-AS-ADMIN.
- Your approval to run the isolated tests in section 8.
