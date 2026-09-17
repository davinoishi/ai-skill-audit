# Auditing 140 AI agent skills: report and patch

A security review of every Claude Code, Claude Cowork and Codex **skill** installed on one Mac — 140 distinct skill versions across 193 installed locations, 10,904 files, and the 7,530 findings [NVIDIA's SkillSpector](https://github.com/NVIDIA/SkillSpector) scanner produced for them.

Companion material for the Empty Folder video. Everything here is evidence you can check: each finding carries a file, a line, a sha256 and a verdict.

## Start here

| File | What it is |
|---|---|
| `OVERVIEW.md` | What was scanned, what was found, what was fixed, what's still open |
| `report/SUMMARY.md` | The full write-up: risks ranked by impact and likelihood, with evidence and fixes |
| `report/coverage-gaps.md` | What the review could **not** establish, plus proposed follow-up tests |
| `report/verification.json` | Counts proving all 140 skills and all 7,530 findings are accounted for exactly once |
| `report/finding-assessments.json` | Every finding: rule, severity, file, line, hash, verdict, reasoning (17 MB) |
| `report/target-reviews.json` | Every skill: per-file review depth and hashes, concerns, gaps, next steps (4 MB) |
| `patch/` | A tested patch for two confirmed flaws in the media-use skill, plus `reharden.py` — the script that strips the silent-update instructions and pins the CLI, re-runnable after every vendor update |

## The short version

- **Nothing malicious was found.** The risk is supply-chain and trust-boundary design.
- **7,530 findings → 71 confirmed concerns, 6,192 expected behaviour, 1,139 false positives, 128 unresolved.** Most of the noise came from one skill's bundled Python environment (6,098 findings), settled by verifying pip install-record hashes and recompiling every `.pyc`, not by dismissing filenames.
- **The headline issues:** skills that update their own instructions from the network "silently, don't ask"; an unsigned native binary that emits agent directives not present in its Markdown; URL guards that miss IPv4-mapped IPv6 and carrier-grade NAT addresses and don't re-check redirects; a `.env` loader that imports every variable from a parent folder; credentials written with default permissions; publishing that stopped asking.
- **The largest single finding was the reviewer's own setup:** the agents could read the entire home folder, and one had the whole home directory marked as a trusted project.

## Method, and its limits

Static review only. No skill script, hook, installer, binary or bundled environment was executed. No credentials were read. Everything inside the skills was treated as untrusted data. Prior controlled runtime checks are cited where they apply, and named as such.

Coverage is uneven and the report says where: the entry instruction file was read in full for 125 of 140 skills, some large helper scripts were only read around the flagged lines, and 128 findings stayed unresolved with the missing evidence named for each. `coverage-gaps.md` and the worklist in `verification.json` are the honest list.

## Redaction

These files are sanitized copies. Replaced throughout: the machine username (`/Users/<user>`), app session identifiers, one overlay-network share path, and one analytics account ID. Nothing else was altered — findings, reasoning, hashes and counts are as produced.

## Reusing this

The report names three vendors' products and quotes their instruction text, because that's the evidence. No intent is claimed and none was found. If you maintain one of these skills and have fixed something here, that's the outcome this was written for.

The scan used [SkillSpector](https://github.com/NVIDIA/SkillSpector) 2.11.2 — the 7,530 findings reviewed here are its raw output. The review, the verdicts and the patch are independent work, unaffiliated with NVIDIA or any vendor named. No warranty — check the evidence yourself before acting on it.

Licensed [MIT](LICENSE). Quoted instruction text from the reviewed skills remains the property of its respective authors and is reproduced here as evidence under fair use.
