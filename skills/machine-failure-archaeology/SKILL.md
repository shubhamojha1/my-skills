---
name: machine-failure-archaeology
description: Use when investigating something odd or broken on this machine that might be a known settled battle — orphaned repos, leftover config backups, suspicious hooks or ad-injection remnants (.runtimeads, .vibe-ads, .kickbacks), stale analyses, benchmark hangs — or before re-debugging anything that smells historical. Triggers - settings.json.bak, runtimeads, vibe-ads, kickbacks, Projects\graphify remnant, helios hang, ingest mistakes, roofline README, why is this here, has this happened before.
---

# Machine Failure Archaeology — the settled battles

Chronicle of incidents on this machine, reconstructed from artifacts on 2026-07-06.
The user's own words: costliest failures = "all of them, I have lost track" — so entries
below are evidence-based, with interpretation confidence stated. Never re-fight a CLOSED
battle; OPEN items are fair game but start from the evidence here.

Written to the user's own postmortem standard (he builds systemsfailed.dev): no fabricated
dates, true triggers, honest multi-event mechanisms (see `onthejob-operations` for those rules).

## Entry 1 — The runtimeads hook infestation (CLOSED 2026-07-01, residue may remain)
- **Symptom:** `~/.claude/settings.json.bak` (dated 2026-07-01) preserves a settings state in
  which `C:\Users\subha\.runtimeads\hooks\runtimeads-claude-hook.sh` was registered as a hook
  **nine times each** on SessionStart, SessionEnd, UserPromptSubmit, PreToolUse (matcher `*`),
  PostToolUse (matcher `*`), PostToolUseFailure, Stop, and Notification — i.e., an external
  script intercepting every prompt, every tool call, and every session boundary.
- **Root cause:** an ad/monetization tool ("runtimeads", consistent with the sibling
  `~\.vibe-ads` VS Code extension and possibly `~\.kickbacks\auth.json`) self-installed its
  hook repeatedly. Exact install vector UNKNOWN.
- **Evidence:** the .bak file itself; current `settings.json` has `"hooks": {}`;
  `C:\Users\subha\.runtimeads` no longer exists (verified 2026-07-06); `.vibe-ads\debug.log`
  shows the VS Code-side extension ("injectionOn": true, build 2026-06-25) active through
  **2026-07-05**.
- **Status:** Claude-side CLEANED (2026-07-01, hooks emptied + dir removed). **OPEN residue:**
  the vibe-ads VS Code extension appears installed/active, and `.kickbacks\auth.json` remains.
  Surface this to the user before touching — removal is his call (never read/print auth.json).
- **Lesson:** on this machine, inspect `settings.json` hooks whenever behavior looks odd;
  a `.bak` next to a config is incident evidence, not clutter. Any future hook additions go
  through the user (`machine-change-control`).

## Entry 2 — Helios concurrency collapse → continuous-batching rebuild (mostly CLOSED)
- **Symptom (2026-05-22 benchmark):** TTFT p50 jumped to 43.7s at concurrency 8; 4 of 16
  requests hung ~2.6 hours at c=16 (total_ms ≈ 9,292,585 in `throughput_20260522_132213.json`).
- **Root causes (two, both confirmed in code):** (1) `main.py` overrode `max_batch_size` to 4
  while scheduler defaulted 8 — requests cohorted in 4s; (2) `decode_step` ran one forward
  pass PER REQUEST (N kernel launches).
- **Evidence:** benchmark JSONs in `Projects\helios\benchmarks\output\`; `notes.md` run
  history; the TTFT arithmetic showed batch-size-4 before the code did — the house's best
  example of numbers→hypothesis→confirmation (`research-methodology-and-frontier`).
- **Status:** CLOSED for the core (continuous batching landed 2026-05-24: 43.6 → 179 tok/s
  at c=16). OPEN: Run-4 token-budget regression + 5 issues in `issues.md` —
  live campaign in `helios-continuous-batching-campaign`.
- **Lesson:** performance claims require the benchmark JSON; a "hang" was really scheduling
  starvation, not deadlock.

## Entry 3 — The four ingest-extraction failures (CLOSED — codified as rules)
Four incident files on systemsfailed.dev shipped with extraction errors; each produced a
standing rule (full text + stories in `onthejob-operations`): fabricated placeholder date
(incident-io connection-pool); vendor-window-vs-user-impact duration (aws-outage-cascade,
3h42m vs ~10h30m); amplifier-as-trigger (gke-dataplane); conflated multi-event mechanism
(github proxysql). **Status:** rules codified in project memory + enforced by read-back
self-review before writing `.pending-result.json`. The extraction pipeline (Phase 2) must
pass all four on a supervised run before batch use.

## Entry 4 — The orphaned graphify clone (CLOSED as harmless remnant)
- **Symptom:** `Projects\graphify` contains ONLY `.git\objects\pack\pack-33d3316d….{pack,idx,rev}`
  (2026-05-30 18:24) — no HEAD, no config, no working tree; git refuses to recognize it.
- **Interpretation (MEDIUM confidence):** partial deletion of a source clone after switching
  to the pip-installed engine — same day the helios graph was built.
- **Status:** dead remnant; the pack still holds ~798 commits of upstream history (recovered
  read-only on 2026-07-06 via scratch-repo resurrection). Deleting the folder is the user's
  call; it costs ~33MB to keep.
- **Recovery recipe (generic, reusable):** in a SCRATCH dir (never in place):
  `git init scratch; copy the pack files into scratch\.git\objects\pack\; git -C scratch fsck --lost-found`
  → each "dangling commit" is a branch tip; `git branch tipN <sha>` then log/read normally.
- **Lesson:** the pip-vs-uv install question (see `graphify-operations`) plus this remnant
  both trace to the same 2026-05-30 setup session.

## Entry 5 — Stale analyses overtaken by the code (recurring pattern, stay alert)
Three documented cases where a written analysis/memo aged out while work continued:
1. Helios memory `project_continuous_batching.md` (2026-05-23) still says "Bug 2 not fixed" —
   fixed the next day (notes.md is authoritative).
2. onthejob project memory lists a superseded taxonomy (data-corruption/network-partition/
   human-error/observability-gap → actual: bad-deploy/data-loss/dns-bgp/automation-misfire,
   verified in `content\taxonomy.ts`) and 18 incidents (actual: 30).
3. sysdesignvault gaps memo (2026-06-16) lists progress tracking as absent — it's implemented
   in the working tree (localStorage + Clerk/Prisma sync).
**Lesson (the load-bearing one):** on this machine, WRITTEN STATE LAGS CODE. Memory files and
memos record decisions and direction reliably, but STATUS claims must be re-verified against
the repo before acting. Every skill in this library carries re-verification commands for
exactly this reason.
**Status:** OPEN as a standing risk; the skills (2026-07-06) reset the baseline.

## Entry 6 — sysdesignvault platform-gaps deadline slip (OPEN, softened)
Memo dated 2026-06-16 set a 2026-06-23 deadline for five platform gaps. Deadline passed;
gap #1 (progress tracking) has since been implemented, #2 is mid-flight (AI-paths expansion
untracked in the working tree). **Lesson recorded in the memo itself:** "Don't let content
work crowd out platform work indefinitely." Surface remaining gaps when the user asks
"what next" (see `sysdesignvault-platform`).

## Entry 7 — Minor artifacts (LOW severity, known)
- `Projects\roofline\README.md` first line says "# flash-attention-from-scratch" —
  copy-paste from the sibling repo. Harmless; rename is a one-line user-approved fix.
- Portfolio-wide uncommitted WIP (dirty counts 1–42) — NOT an incident; deliberate
  review-before-commit workflow. The failure mode would be a session "helpfully" committing.
- resume inventory carries 8 `[VERIFY]` tags including a real conflict (Helios hardware:
  "Qwen2.5-3B on RTX 4070" vs resume text "quantized Mistral-7B") — unresolved by design;
  only the user resolves [VERIFY] items (`resume-and-career-ops`).

## How to add an entry
Symptom → Root cause → Evidence (files/dates) → Status (OPEN/CLOSED + confidence) → Lesson.
Add here when a battle SETTLES; while live, it belongs in the campaign/project skill and in
project memory (`machine-memory-and-docs`). Never invent specifics the artifacts don't show.

## OPEN questions worth asking the user someday
1. Is the vibe-ads VS Code extension intentional? (`.vibe-ads\debug.log` active 2026-07-05.)
2. What are `.kickbacks\auth.json` and the `.openclaw\identity` for — keep or clean?
3. May we delete the `Projects\graphify` pack remnant (after archiving the mined history)?
4. Should the stale helios/onthejob memory files be corrected to point at the new skills?

## When NOT to use
Live debugging of a NEW fault → `machine-debugging-playbook` first (this skill tells you
whether it's actually old). Project-specific live problems → the campaign skills.

## Provenance and maintenance
Authored 2026-07-06 from: settings.json.bak (read in full), .vibe-ads\debug.log,
Projects\graphify listing, helios benchmarks + notes.md + memory, onthejob memory +
taxonomy.ts, sysdesignvault memo + working tree, resume inventory. Re-verify:
```powershell
Test-Path C:\Users\subha\.runtimeads                                  # False = still clean
Get-Item C:\Users\subha\.vibe-ads\debug.log | Select-Object LastWriteTime   # still active?
(Get-Content C:\Users\subha\.claude\settings.json -Raw | ConvertFrom-Json).hooks   # should be empty
Get-ChildItem C:\Users\subha\Projects\graphify -Recurse -Force | Measure-Object    # still just the pack (6 items)?
```
When an OPEN item closes, move it to CLOSED with the closing evidence and date.
