---
name: projects-atlas
description: Use when a session needs to locate which repo under C:\Users\subha\Projects owns a task, what a repo is for, its build/test entry, branch, or state — or when the user names a project (helios, onthejob, sysdesignvault, arachne, mimir, bifrost, heimdall, hermes, mjolnir, joust, sqlite, roofline, my-wiki, resume...). Triggers - which repo, where does X live, project map, portfolio, repo purpose, stalled project, external clone.
---

# Projects Atlas — the portfolio map

Every repo under `C:\Users\subha\Projects` (verified 2026-07-06). Naming culture: Norse/Greek
mythology for infrastructure built from scratch. Almost every repo carries uncommitted WIP —
that is deliberate review-before-commit workflow, **never clean it up or commit it**
(`machine-change-control`).

## Active work (2026-06/07 commits or heavy session traffic)

| Repo | Branch | Dirty | Last commit | What it is / entry points |
|---|---|---|---|---|
| **onthejob** | main | 10 | 2026-07-05 | systemsfailed.dev postmortem index (PRIVATE product). → `onthejob-operations`, `onthejob-phase2-campaign` |
| **sysdesignvault** | ai-concepts | 19 | 2026-06-15 | systems-design learning platform, Next.js 16. → `sysdesignvault-platform` |
| **resume** | main | 10 | 2026-07-01 | LaTeX resume + inventory YAMLs + /tailor project skill. → `resume-and-career-ops` |
| **arachne** | main | 9 | 2026-07-01 | WebGPU + TypeScript + Vite experiment, 1 commit, README is just "# arachne" — UNDOCUMENTED (candidate for a README once it has shape) |
| **helios** | main | 10 | 2026-05-24 | from-scratch LLM inference server. → `helios-continuous-batching-campaign` |
| **personal-site** | main | 15 | 2026-05-28 | Next.js personal website (has AGENTS.md) |
| leetcode-company-wise-problems | main | 0 | 2026-06-25 | EXTERNAL clone (liquidslr) — interview prep data |

## ML / performance lab

| Repo | Branch | Dirty | Last commit | Notes |
|---|---|---|---|---|
| flash-attention-from-scratch | main | 1 | 2026-05-30 | CUDA Flash Attention learning build |
| roofline | main | 11 | 2026-05-30 | perf analysis; **README is a copy-paste artifact** — says "# flash-attention-from-scratch" (see machine-failure-archaeology) |
| parameter-golf | main | 2 | 2026-03-21 | EXTERNAL clone of openai/parameter-golf (org SSH remote) |
| rag-lab | main | 9 | 2025-08-19 | RAG experiments — STALLED |

## Systems-from-scratch (mostly stalled prototypes — stalling is a normal outcome here)

| Repo | Branch | Dirty | Last commit | What it is |
|---|---|---|---|---|
| bifrost | storage-engine | 18 | 2025-10-17 | storage engine (in-memory works, has tests) — STALLED |
| heimdall | main | 8 | 2025-05-17 | Go load balancer — STALLED |
| hermes | broker | 3 | 2026-04-07 | Java message broker (gradle) |
| mjolnir | main | 8 | 2026-05-10 | Makefile-built project, 12 commits |
| joust | main | 3 | 2026-05-05 | single commit, early |
| sqlite | main | 1 | 2026-01-18 | build-your-own-sqlite |
| db-indexing | main | 3 | 2026-01-22 | DB indexing experiments (Java) |

## Knowledge & memory tools

| Repo | Branch | Dirty | Last commit | What it is |
|---|---|---|---|---|
| my-wiki | master | 0 | 2026-05-20 | personal wiki, 243 commits, AGENTS.md (NOTE: its AGENTS.md predates the no-commit iron rule — the rule wins, see machine-change-control) |
| notes | main | 1 | 2026-03-18 | book notes (interpreter-in-Go) |
| research-papers | ai_papers | 8 | 2025-06-22 | paper notes; English + Sanskrit tokenizers |
| mimir | prototyping | 33 | 2025-10-27 | memory/knowledge prototype (Python) — STALLED |
| synapse | prototype | 10 | 2025-12-08 | memory prototype ("memory works") — STALLED |

## Public surface & external

| Repo | Branch | Dirty | Notes |
|---|---|---|---|
| shubhamojha1.github.io | first_post | 42 | GitHub Pages site — heaviest WIP in the portfolio |
| claw-code | main | 0 | EXTERNAL clone (instructkr) |
| TutionProject | main | 0 | EXTERNAL collab (Oblivious19) |

## Non-git folders under Projects\ (workspaces, not repos)
`ai_stuff`, `blog_projects`, `BLUEJ projects`, `claw-code-new`, `coding-agent`,
`competitive_coding`, `mimir_other`, `open_source` (contains the system-design-resources
clone), `playground`, `study` — scratch/course material; no build contract; browse before
assuming anything.

**Special case:** `Projects\graphify` is NOT a repo — an orphaned `.git\objects\pack`
remnant (2026-05-30). Details in `machine-failure-archaeology`. The graphify TOOL is
pip-installed; see `graphify-operations`.

## Conventions that hold across the portfolio
- Remotes: `git@github.com:shubhamojha1/<name>.git` (SSH), externals keep their origins.
- Python repos: per-repo `venv\` (helios), or bare requirements.txt (mimir, rag-lab).
- Node repos: standard npm scripts; check `package.json` scripts block first, README second.
- Build/verify entries per repo: see `machine-validation-and-qa` for the command table.
- Sessions per repo (last-400 history sample, 2026-07-06): onthejob 198, sysdesignvault 149,
  resume 14, personal-site 12, helios 7, arachne 6 — expect the campaign skills to matter
  in that order.

## When NOT to use
Deep work inside a repo → that repo's own skill (see pointers above). Machine-level layout
→ `machine-map`. This skill is the routing table, not the runbook.

## Provenance and maintenance
Authored 2026-07-06; branch/dirty/last-commit measured that day (they drift daily — treat
as snapshot, re-measure before quoting). Re-verify the whole table:
```powershell
foreach ($r in (Get-ChildItem -Directory C:\Users\subha\Projects)) { $p=$r.FullName; if (Test-Path "$p\.git") { $b=git -C $p rev-parse --abbrev-ref HEAD; $d=(git -C $p status --porcelain | Measure-Object).Count; $l=git -C $p log -1 --format='%cs %s'; "{0,-30} {1,-15} dirty={2,-3} {3}" -f $r.Name,$b,$d,$l } }
```
New repo appears → add a row + a one-line purpose; repo graduates/stalls → update its flag.
