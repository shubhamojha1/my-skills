---
name: onthejob-phase2-campaign
description: Use when executing onthejob/systemsfailed.dev Phase 2 work — open-sourcing the repo, building the patterns index pages, operating or extending the discovery bot, or the LLM ingest extraction pipeline. Triggers - phase 2, CONTRIBUTING, CODEOWNERS, issue templates, patterns page, pattern tags, discovery bot, queue, candidates.json, ingest, ingest-prep, ingest-apply, draft PR, extraction pipeline.
---

# onthejob Phase 2 — Execution Campaign

Decision-gated playbook for the Phase 2 roadmap of `C:\Users\subha\Projects\onthejob`
(systemsfailed.dev). Roadmap ORDER is user doctrine (project memory 2026-06/07):
**1) open-source setup → 2) patterns index → 3) discovery bot → 4) LLM extraction pipeline →
5) SysDesignVault cross-link.** Read `onthejob-operations` first for the runbook, taxonomy
discipline, and the four ingest-quality rules — they bind everything here.

**Reality check (verified 2026-07-06): the roadmap is partially overtaken.** Items 3 and 4
already have substantial implementations. Statuses below are ground truth; re-verify at
session start (commands in Provenance).

| Phase | Roadmap says | Actual state 2026-07-06 |
|---|---|---|
| 1. Open-source setup | prerequisite for external PRs | NOT started (CONTRIBUTING.md, CODEOWNERS, .github\ISSUE_TEMPLATE all absent) |
| 2. Patterns index | each pattern tag gets a page | NOT built; **104 distinct tags over 30 incidents (100 singletons)** — needs consolidation first |
| 3. Discovery bot | poll sources → GitHub Issues | **BUILT & scheduled**: scripts\discovery.ts + content\queue\ + .github\workflows\discovery.yml (daily 07:00 UTC, commits queue via git-auto-commit-action). Outputs queue JSON, not Issues |
| 4. Extraction pipeline | URL → Claude drafts → draft PR → human review | **Scripts exist**: ingest.ts / ingest-prep.ts / ingest-apply.ts (Anthropic SDK, ANTHROPIC_API_KEY, default model claude-sonnet-4-6, prompts\ dir, queue state in content\queue\) — maturity/end-to-end unverified |
| 5. SDV cross-link | future | UNSPECCED — fenced, do not start |

## Ground rules for every phase
- End state is always: uncommitted diff + summary → USER reviews, commits, pushes (Vercel
  deploys from git). You never commit/push (see `machine-change-control`).
- New npm deps → ask the user with the exact `npm i` command.
- Success is measured (page counts, validate green, tag counts), never judged by eye
  (`machine-validation-and-qa`).
- `npm run ingest` internally shells out to git (it builds a *draft PR*) — treat running it
  as a state-changing action: get explicit user go-ahead per run, and confirm what branch
  operations it performs by reading `scripts\ingest.ts` before the first run.

## Phase 1 — Open-source setup
Objective: everything needed for external incident submissions via PR.
Preconditions (all TRUE as of 2026-07-06):
```powershell
Test-Path C:\Users\subha\Projects\onthejob\CONTRIBUTING.md          # False
Test-Path C:\Users\subha\Projects\onthejob\.github\ISSUE_TEMPLATE   # False
Test-Path C:\Users\subha\Projects\onthejob\.github\CODEOWNERS       # False
```
Steps:
1. `CONTRIBUTING.md` — derive the incident-authoring section directly from
   `onthejob-operations` (frontmatter schema, filename=id, validate gate) and the FOUR
   ingest-quality rules; include the taxonomy discipline (no new classes via tags — propose
   in an issue instead). State the public name rule (systemsfailed.dev).
2. `.github\ISSUE_TEMPLATE\` — at minimum: `new-incident.yml` (fields mirroring the schema:
   source URL required), `taxonomy-proposal.yml` (separate deliberate process, by design),
   `bug.yml`.
3. `.github\CODEOWNERS` — `* @shubhamojha1`.
GATE: `npm run validate` and `npm run build` still green (these files must not enter the
content pipeline); the user agrees the repo is ready to flip public (THE FLIP ITSELF IS THE
USER'S ACTION — repo visibility is an outward-facing, irreversible-ish change).
Fenced: do not add license/PR-bot/config beyond the three artifacts without asking; do not
make the repo public yourself (you can't and shouldn't try).

## Phase 2 — Patterns index (with the consolidation gate)
Objective: `/patterns` index + one page per pattern tag listing matching incidents.
**Precondition discovered 2026-07-06:** the pattern vocabulary is uncontrolled — 104
distinct tags across 30 incidents; only 4 tags (`operator-error`, `health-check-flapping`,
`no-staged-rollout`, `global-blast-radius`) appear twice; the rest are singletons. Shipping
pages now = 104 near-empty pages.
Step 0 (BLOCKING, user decision): propose a consolidated pattern vocabulary — cluster the
104 into ~20-30 curated patterns with a full old→new mapping table (same spirit as the
taxonomy: "the taxonomy IS the product"). Patterns are stored per-incident in frontmatter
`patterns:` (multi-line YAML lists), so consolidation = editing incident files + (optionally)
adding a `content\patterns.ts` registry mirroring taxonomy.ts. User approves the vocabulary
BEFORE any page work.
Then:
1. Apply the approved mapping across `content\incidents\*.md` (script it; keep the diff
   reviewable per-file).
2. Add pattern pages: register routes in `src\routes.tsx` (this is where SSG page
   enumeration lives — verified); follow the existing per-incident page pattern in `src\pages\`.
3. Wire chips → pages on the home feed.
GATE (numbers, not vibes): `npm run validate` green; `npm run build` page count =
30 incidents + N patterns + static pages (state N from the approved vocabulary; count build
output lines); every pattern page lists ≥1 incident; zero tags in incidents that aren't in
the registry (write a validate extension for this — propose it to the user as part of step 1).
If build page count ≠ expected → routes.tsx registration is the first suspect.
Measure the tag inventory any time with the counting recipe in Provenance.

## Phase 3 — Discovery bot (operate & harden; it already exists)
What exists (read scripts\discovery.ts before touching): sources = danluu/post-mortems
(README diff) + RSS feeds (cloudflare, slack-engineering, github-engineering,
netflix-tech-blog, stripe-engineering, sre-weekly, …); daily GitHub Action commits
`content\queue\**` (candidates.json, state.json).
Session-runnable: `npm run discover` (network — announce first), then inspect
`content\queue\candidates.json`.
Improvement menu (ranked; each needs user sign-off since the bot auto-commits in CI):
1. Candidate → GitHub Issue bridge (roadmap's original design) — needs a token decision
   (Actions GITHUB_TOKEN can open issues; no gh CLI locally as of 2026-07-06).
2. Source expansion (awesome-postmortem list; more engineering blogs).
3. Dedup/scoring improvements against existing 30 incidents.
GATE for any change: a dry run whose candidate diff you show the user; the Action stays
green on its next scheduled run (user checks, or you check the queue commit the next day).

## Phase 4 — Extraction pipeline (verify, then harden)
What exists: `npm run ingest -- <url>` → Anthropic API (needs ANTHROPIC_API_KEY in env —
if absent, that's an ask-the-user item; costs API tokens — announce before running) →
draft incident via `prompts\` templates → queue state (.pending-extract.md,
.pending-result.json) → `ingest-apply` writes the incident (+ git branch/PR steps inside —
READ ingest.ts + ingest-apply.ts first and report exactly what git it runs; get explicit
user approval for that part or run only the non-git stages).
First task when this phase opens: ONE supervised end-to-end run on a user-chosen URL,
scoring the draft against the four ingest-quality rules (that's the acceptance test — the
rules exist because past extractions failed exactly there). Record pass/fail per rule.
GATE: draft validates (`npm run validate` on the produced file), all four quality rules
pass on read-back against the source, human (user) approves the draft. NEVER auto-merge;
NEVER let the pipeline commit as you.
Fenced: batch-ingesting the whole queue before the single-URL acceptance test passes.

## Phase 5 — SysDesignVault cross-link: FENCED
Unspecced ("integration not yet specced" — memory). If asked, brainstorm with the user
first; do not invent an integration.

## Provenance and maintenance
Authored 2026-07-06 from: repo state (workflows, scripts, queue), package.json,
src\routes.tsx presence, pattern-tag census (Python recipe below), project memory
(project-onthejob roadmap), scripts\ingest.ts header, scripts\discovery.ts sources.
Re-verify:
```powershell
Test-Path C:\Users\subha\Projects\onthejob\CONTRIBUTING.md                                  # Phase 1 started?
Get-ChildItem C:\Users\subha\Projects\onthejob\.github\workflows                            # ci, archive, discovery
Get-ChildItem C:\Users\subha\Projects\onthejob\content\queue                                # bot output present?
(Get-ChildItem C:\Users\subha\Projects\onthejob\content\incidents -Filter *.md).Count       # 30 as of 2026-07-06
```
Pattern census (multi-line YAML lists — inline regex misses them): run a small Python
script that regex-extracts `^patterns:\n(\s+- …)+` blocks per incident and Counters the
tags (104 distinct / 30 incidents as of 2026-07-06). If the count drops near ~25, Phase 2
step 0 already happened — skip to page building.
