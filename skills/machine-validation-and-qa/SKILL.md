---
name: machine-validation-and-qa
description: Use when about to claim any work on this machine is done, fixed, or passing — before handing over an incident .md, MDX concept, .tex resume, helios perf change, or graph rebuild. Covers what counts as evidence per repo - npm run validate/build/link-check (onthejob), lint/build-concepts.js/_concepts-data.json (sysdesignvault), tectonic compile (resume), pytest + throughput_*.json benchmarks (helios), graphify benchmark/diagnose, tsc -b (arachne). Keywords - verification, QA, acceptance threshold, golden baseline.
---

# Machine validation and QA — what counts as evidence

## Overview

This skill defines the evidence bar on this machine: no work is claimed complete without
running the repo's verification command and quoting its output. It lists the verified
per-repo commands, the golden artifacts that new claims are measured against, and the
change-control rule for adding new checks. The user's standard, encoded: "always compile
before finishing", "no invented claims".

## When to use / when NOT to use

**Use when:**
- You are about to say "done", "fixed", "passing", "should work now", or hand any artifact back.
- You edited an incident `.md`, an MDX concept, `resume_faangpath.tex`, helios code, or a graph.
- You are defining success criteria for a campaign before starting it.

**NOT this skill:**
- How to make the edit itself → the per-project skills in this library
  (`Get-ChildItem C:\Users\subha\.claude\skills` for current names).
- Whether you may add/modify scripts, commit, or install → `machine-change-control`.
- Debugging a failure the checks surfaced → `superpowers:systematic-debugging` (plugin skill).

## The evidence bar (doctrine)

1. **Claims require command output, not reasoning.** "It should work" is not done.
   "The types line up" is not done. Done = the verification command ran and you quote its
   result (e.g. `30 incidents validated ✓`). If you cannot run the check, say so explicitly
   and hand over as UNVERIFIED — never imply it passed.
2. **If a verification command exists for the artifact you touched, run it.** The table
   below is the lookup. Exceptions are cost-gated commands (network, LLM tokens, model
   loads, long builds) — for those, state which gate you skipped and why.
3. **One mechanism must explain all observations — including the negative ones.** When
   diagnosing a failure, the explanation you accept must account for every symptom AND for
   everything that still works. A theory that explains the error but not why the other 29
   incidents still validate is not yet the mechanism. (This machine's history: the helios
   c=16 hang and the github-2020-proxysql ingest error were both solved only when a single
   root cause covered every data point.)
4. **Measured, never judged by eye.** `npm run preview` and screenshots are layout sanity
   checks, not correctness evidence. Numbers come from commands.
5. **Passing schema ≠ true content.** onthejob's Zod gate proves shape, not that a date or
   duration is real (fabricated `2023-01-01` dates passed validation once — see the
   ingest-quality rules in the onthejob project memory/skill). Factual claims need sources;
   resume claims need the inventory YAMLs.

Iron rules apply here as everywhere: **no git commit/push, no package installs** — prepare
evidence, leave the working tree for the user (see `machine-change-control`). If a check
needs a missing tool, STOP and give the user the install command.

## Quick reference — per-repo verification (verified 2026-07-06)

Status column: **EXEC** = I ran it this pass and quote output; **DOC** = command confirmed
to exist in package.json/pyproject/skill file, not executed (cost/side-effect gated).

| Repo | Command (from repo root) | Proves | Cost / gate | Status |
|---|---|---|---|---|
| onthejob | `npm run validate` | Zod schema on all incidents; no file generation | seconds | EXEC: `30 incidents validated ✓` |
| onthejob | `npm run link-check` | every incident `source` URL answers HEAD | **network** | DOC |
| onthejob | `npm run build` | full gate: prebuild (index + OG cards) → SSG; page count | minutes | DOC |
| onthejob | `npm run preview` | serves prod build on port 4173 (visual only) | local server | DOC |
| sysdesignvault | `npm run lint` (= `eslint .`) | lint clean | ~min | DOC |
| sysdesignvault | `node scripts/build-concepts.js` | MDX → `src\data\_concepts-data.json` regenerated | seconds | DOC (script exists) |
| sysdesignvault | `npm run build` | prebuild (`prisma generate && node scripts/build-concepts.js`) → `next build` | minutes | DOC |
| resume | `tectonic resume_faangpath.tex` | .tex compiles to PDF | writes .pdf/.log in repo | DOC (binary at `C:\Users\subha\bin\tectonic.exe`, EXEC-confirmed present) |
| helios | `venv\Scripts\python.exe -m pytest tests\memory\test_memory.py -v` | MemoryManager unit tests (model-free, fast) | seconds | DOC (pytest 9.0.2 in venv — EXEC-confirmed) |
| helios | `venv\Scripts\python.exe -m pytest tests\engine\test_engine.py -v` | engine tests | **loads model** | DOC |
| helios | `python benchmarks\throughput.py` (harness) | new `benchmarks\output\throughput_*.json` | **loads Qwen2.5-3B; c=16 has hung ~2.6h** | DOC |
| graphify graphs | `python -m graphify benchmark` | token reduction vs naive full-corpus | reads graph.json | DOC (in `--help`) |
| graphify graphs | `python -m graphify diagnose multigraph` | same-endpoint edge-collapse report (`--json` for machine-readable) | read-only | DOC (in `--help`) |
| arachne | `npm run build` (= `tsc -b && vite build`) | typecheck + bundle | ~min | DOC |
| personal-site | `npm run build` (= `next build`); `npm run lint` | build/lint pass | minutes | DOC |
| others | read the repo's `package.json` / `Makefile` / `go.mod` / `build.gradle` first | — | — | heimdall=go, hermes=gradle, mjolnir=make; no verified harness |

PowerShell 5.1 note: no `&&`. Chain as `Set-Location C:\Users\subha\Projects\onthejob; npm run validate`
(the `&&` inside npm scripts runs in npm's own shell and is fine).

## Per-repo detail

### onthejob (systemsfailed.dev)

- **Touched an incident .md** → run `npm run validate`. It is documented in the README as
  "Zod schema check on all incidents (no file generation)" — safe, fast, run it every time.
- **`npm run link-check`** HEAD-requests every `source` URL. It is a network action:
  document that you ran it (or didn't), don't fire it routinely — only when you added or
  changed a `source`/`archive_url`.
- **`npm run build`** is the full gate: prebuild runs `tsx scripts/build-index.ts && tsx scripts/og-cards.ts`
  (schema validation fails loudly), then `vite-react-ssg build` prerenders pages.
  **Expected page count = one page per incident + the static pages.** The README's
  "(16 prerendered pages)" is stale — the corpus is 30 incidents as of 2026-07-06. Read
  the page count from the build output itself; if it is below the incident count, an
  incident was silently dropped — that is a failure, investigate.
- Never hand-edit `src\generated\` (produced by build-index.ts; gitignored).

### sysdesignvault

- **After ANY MDX edit** (content lives in `content\<domain>\*.mdx`, 57 files as of
  2026-07-06): run `node scripts/build-concepts.js`, then confirm your change actually
  landed in the generated JSON — read-only diff:
  `git -C C:\Users\subha\Projects\sysdesignvault diff --stat src/data/_concepts-data.json`
  or `Select-String -Path C:\Users\subha\Projects\sysdesignvault\src\data\_concepts-data.json -Pattern '<a distinctive phrase you added>'`.
  **Direction is MDX → JSON, never the reverse.** Editing `_concepts-data.json` by hand is
  a known forbidden move (iron rule 4 in the dossier; the file is generated).
- `npm run lint` for code changes; `npm run build` is the full gate (its prebuild runs
  `prisma generate` then build-concepts, so a green `next build` also proves the content
  pipeline ran).

### resume

- The gate is: `tectonic resume_faangpath.tex` **from the repo root** produces
  `resume_faangpath.pdf`. On failure, read `resume_faangpath.log`, fix, recompile — loop
  until clean. The project's own `/tailor` skill states it as an inviolable rule:
  "Always compile before finishing. … Never hand back a `.tex` that doesn't produce a PDF."
  A .tex handed over uncompiled is a rule violation on this machine, full stop.
- The .pdf and .log appearing in the repo root are expected outputs, not stray files.

### helios

Ground truth of the harness (verified 2026-07-06 — the README documents NO test or
benchmark commands; the tests carry their own usage comments):

- `tests\memory\test_memory.py` — pytest-style, pure-Python (MemoryManager only, no model).
  In-file usage: `python -m pytest tests/memory/test_memory.py -v` from repo root.
  This is the cheap check — run it via the repo venv:
  `C:\Users\subha\Projects\helios\venv\Scripts\python.exe -m pytest tests\memory\test_memory.py -v`.
- `tests\engine\test_engine.py` — pytest-style but constructs `Engine` (loads the model): slow gate.
- `tests\scheduler\test_scheduler_manual.py` — **not a pytest test**; a manual asyncio
  script: `python -m tests.scheduler.test_scheduler_manual` (loads model).
- `conftest.py` at repo root; `pyproject.toml` has `[tool.pytest.ini_options] pythonpath = ["."]`
  — so run pytest FROM the repo root or imports break. pytest 9.0.2 is in the venv (verified).
- **Benchmarks**: harness `benchmarks\throughput.py`; outputs
  `benchmarks\output\throughput_YYYYMMDD_HHMMSS.json` — 5 exist as of 2026-07-06
  (`throughput_20260522_132213.json` … `throughput_20260530_023958.json`). JSON shape: a
  list of records with keys `concurrency, max_tokens, ttft_p50_ms, ttft_p95_ms,
  throughput_tokens_per_sec, per_request`.
- **Perf-claim rule: a new performance claim requires a new comparable JSON** — same
  concurrency levels and `max_tokens` as the baseline, compared number-to-number. "Decode
  loop looks batched now" is not a perf claim. Warning: in the 20260522 baseline, 4
  requests at c=16 hung ~2.6h — time-box any benchmark run and never launch one casually.

### graphify graphs

- Read-only quality diagnostics (both confirmed in `python -m graphify --help`, 2026-07-06):
  - `python -m graphify benchmark` — measures token reduction vs naive full-corpus approach.
  - `python -m graphify diagnose multigraph` — same-endpoint edge-collapse report; add
    `--json` for machine-readable, `--graph <path>` for a non-default location.
- Quality metric to quote from any graph's `GRAPH_REPORT.md`: the audit line. helios's
  (as of the 2026-05-31 build): `66% EXTRACTED · 34% INFERRED · 0% AMBIGUOUS · INFERRED: 181 edges (avg confidence: 0.54)`.
  High EXTRACTED % and INFERRED avg confidence well above 0.5 = healthy; 0.54 avg is the
  bimodal-collapse smell the graphify skill warns about.
- **Do not run full extract/update pipelines to "verify" a graph — they cost LLM tokens.**
  Diagnostics above are the free checks. Rebuilds are proposed to the user.

### arachne / personal-site / everything else

- arachne: `npm run build` = `tsc -b && vite build` — the typecheck is the gate.
- personal-site: `npm run build` (`next build`), `npm run lint`.
- Any other repo: read its `package.json` scripts / `Makefile` / `go.mod` / `build.gradle`
  BEFORE claiming a gate exists. If no harness exists, say "no verification harness in this
  repo" — do not invent one, and do not add one silently (see below).

## Golden / certified inventory (the baselines new claims are measured against)

| Artifact | Location | Status as of 2026-07-06 |
|---|---|---|
| helios benchmark JSONs | `Projects\helios\benchmarks\output\throughput_*.json` (5 files) | Golden perf baselines. `throughput_20260522_132213.json` is the analyzed baseline (dossier §7: c=16 TTFT p95 128.5s, 4 hung requests). Latest: `throughput_20260530_023958.json`. |
| onthejob incident corpus | `Projects\onthejob\content\incidents\*.md` | 30 Zod-validated live incidents (was 18 at the 2026-07-02 launch — corpus grew; README counts are stale). This corpus is the product; validate output is its certificate. |
| resume inventory YAMLs | `Projects\resume\inventory\projects.yaml`, `experience.yaml` | Sole source of resume claims. 8 `[VERIFY]` tags (5 projects, 3 experience) = **unconfirmed claims that only the user can certify** — never promote a `[VERIFY]` bullet into a resume without his confirmation. |
| graphify graphs | `Projects\helios\graphify-out\` (the ONLY graphify-out on the machine) | **Stale-version artifact**: built 2026-05-31 pre-0.8.21 (primitive-type god nodes like `str --uses--> Engine` still present); local engine is 0.8.25. A rebuild would improve it but costs tokens — user's call. Don't treat its warts as current-engine behavior. |

## How to add a check (change-control)

Where validation code lives per repo:

- onthejob: `scripts\*.ts` wired as package.json scripts (`validate-incidents.ts`,
  `link-check.ts`, `build-index.ts`, `og-cards.ts`, plus ingest/discovery scripts).
- sysdesignvault: `scripts\` (`build-concepts.js`, `check-war-story-links.ts`).
- helios: `tests\<component>\test_*.py` + `benchmarks\throughput.py`.
- resume: the compile step inside the `/tailor` project skill.

**The rule: new validation scripts are PROPOSED to the user, never silently added.**
Specifically: do not add entries to `package.json` scripts, and above all do not wire
anything into `predev`/`prebuild` lifecycle hooks (those execute automatically on every
`dev`/`build` — a surprise there is a booby trap). Write the proposed script + the exact
package.json diff, leave it uncommitted, and summarize for review. Full policy:
`machine-change-control`.

## Acceptance-threshold discipline for campaigns

The campaign skills in this library (helios continuous-batching, and the onthejob and
sysdesignvault campaigns — `Get-ChildItem C:\Users\subha\.claude\skills` for exact names)
must each define **numeric gates BEFORE any work runs**, and success is measured against
them, never judged by eye:

1. Write the gate down first, with the command that measures it. Examples of well-formed
   gates on this machine:
   - helios: "new `throughput_*.json` at c=1/4/8/16, same `max_tokens=256`; c=8 TTFT p50
     < 43,697 ms baseline; zero hung requests" — measured by diffing the two JSONs.
   - onthejob: "`npm run validate` passes; build page count = 30 incidents + static pages;
     link-check clean for every touched source URL."
   - sysdesignvault: "`npm run lint` and `npm run build` green; the edited concept's text
     present in `_concepts-data.json` after regeneration."
2. Run the measurement, quote the numbers next to the gate.
3. A missed gate is a missed gate — report it as such. Do not renegotiate thresholds after
   seeing results; propose a revised gate to the user instead.

## Common mistakes

- Claiming done off a clean-looking diff. The diff is the change; the command output is the evidence.
- Trusting the onthejob README's "(16 prerendered pages)" — stale. Formula: incidents (30
  as of 2026-07-06) + static pages; read the count from the build output.
- Running `npm run link-check` as a routine gate — it hits the network per source URL; run
  it only when sources changed, and say so.
- Editing `_concepts-data.json` to make a check pass. Direction is MDX → regenerate → diff.
- Running helios pytest from anywhere but the repo root (pythonpath breaks), or with system
  Python instead of `venv\Scripts\python.exe`.
- "Verifying" helios perf by feel, or launching a c=16 benchmark without a time-box (prior
  run hung requests for ~2.6h).
- Handing over a .tex without a tectonic compile — explicit rule violation per the tailor skill.
- Accepting a failure theory that explains the error but not the survivors — the mechanism
  must cover ALL observations, including negatives.
- Installing a missing checker (pytest, eslint, etc.) to unblock verification — iron rule:
  ask the user with the exact install command.

## Provenance and maintenance

Authored 2026-07-06 from the machine dossier + direct re-verification. Commands I executed
that day: `npm run validate` in onthejob (output: `30 incidents validated ✓`),
`python -m graphify --help` (benchmark + diagnose subcommands present),
`venv pytest --version` in helios (`pytest 9.0.2`). All build/link-check/tectonic/benchmark
commands were confirmed against package.json / pyproject.toml / skill files but NOT executed.

Re-verify volatile facts (all read-only, PowerShell 5.1-safe):

| Fact | Command |
|---|---|
| npm script names (4 repos) | `Get-Content C:\Users\subha\Projects\onthejob\package.json` (likewise `sysdesignvault`, `arachne`, `personal-site`) |
| incident count | `(Get-ChildItem C:\Users\subha\Projects\onthejob\content\incidents\*.md).Count` |
| MDX count | `(Get-ChildItem C:\Users\subha\Projects\sysdesignvault\content -Recurse -Filter *.mdx).Count` |
| benchmark JSONs | `Get-ChildItem C:\Users\subha\Projects\helios\benchmarks\output` |
| helios tests + pytest | `Get-ChildItem C:\Users\subha\Projects\helios\tests -Recurse -Filter *.py` and `C:\Users\subha\Projects\helios\venv\Scripts\python.exe -m pytest --version` |
| `[VERIFY]` tag count | `(Select-String -Path C:\Users\subha\Projects\resume\inventory\*.yaml -Pattern '\[VERIFY\]').Count` |
| tectonic present | `Test-Path C:\Users\subha\bin\tectonic.exe` |
| graphify subcommands | `python -m graphify --help` |
| graph audit line | `Select-String -Path C:\Users\subha\Projects\helios\graphify-out\GRAPH_REPORT.md -Pattern 'EXTRACTED'` |
| only graphify-out | `Get-ChildItem C:\Users\subha\Projects -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'graphify-out') }` |
