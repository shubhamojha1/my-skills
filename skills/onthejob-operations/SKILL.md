---
name: onthejob-operations
description: Use when working in Projects\onthejob (public name systemsfailed.dev) — adding or editing incidents, running validate/build/link-check/archive, ingest extraction quality, taxonomy or failure classes, patterns, UI/design work, or launch/positioning copy. Triggers - onthejob, systemsfailed, postmortem, incident md, failure class, taxonomy.ts, Zod schema, vite-react-ssg, ingest, discovery bot, queue, og-cards.
---

# onthejob / systemsfailed.dev — Product Runbook

`C:\Users\subha\Projects\onthejob` is the user's flagship product: a curated, searchable
index of public engineering postmortems organized by **failure class** (not company).
Heaviest active work on this machine (198 of the last 400 sessions). Doctrine: **"the
taxonomy IS the product; curation quality is the moat."** Differentiator vs
danluu/post-mortems and k8s.af = the structured, queryable layer.

## Identity & positioning (as of 2026-07-02 memory + 2026-07-05 repo state)
- Live at **https://systemsfailed.dev** — use this name in ALL public-facing copy, never
  "onthejob.dev". Vercel deployment: onthejob-three.vercel.app. Deploys happen from git —
  which means the USER deploys by committing/pushing; you never do (iron rule).
- Repo is PRIVATE. Launch plan: X/HN first; open-source only if traction. CONTRIBUTING.md
  deliberately deferred until public (verified absent 2026-07-06).
- 30 incidents live in `content\incidents\` (verified count 2026-07-06; memory's "18" is stale).

## Stack (LOCKED — do not propose alternatives)
Vite 5 + React 18 + Tailwind 3 + vite-react-ssg 0.9 (SSG) + react-router-dom v6.
NO Astro, NO meta-framework swaps (user doctrine, project memory 2026-06-25).

## Command table (verified against package.json 2026-07-06)

| Command | What it does | Notes |
|---|---|---|
| `npm run dev` | prebuild (build-index + og-cards) + Vite dev server (SSR) | |
| `npm run build` | schema validation → SSG build | page count ≈ incidents + static pages; watch it |
| `npm run preview` | serve production build on port 4173 | |
| `npm run validate` | Zod schema check on all incidents (`scripts\validate-incidents.ts`) | fast, no file gen — run before claiming ANY incident work done |
| `npm run link-check` | HEAD-checks every source URL | network — tell the user before running |
| `npm run archive` | saves source URLs to archive.org, writes back `archive_url` | MUTATES content files + network — treat as needs-care |
| `npm run cards` | regenerate OG card images (`scripts\og-cards.ts`) | runs in pre-hooks too |
| `npm run discover` / `queue` | discovery bot: poll sources → `content\queue\` | also runs daily via `.github\workflows\discovery.yml` (07:00 UTC cron) |
| `npm run ingest` / `ingest-prep` / `ingest-apply` | LLM extraction pipeline stages | see onthejob-phase2-campaign before touching |

`predev`/`prebuild` lifecycle hooks run `tsx scripts/build-index.ts && tsx scripts/og-cards.ts`.
`src\generated\` is build output (gitignored) — NEVER hand-edit (see machine-change-control).

## The taxonomy (verified from content\taxonomy.ts 2026-07-06 — NOT the older memory list)

10 failure classes in `FAILURE_CLASSES` (single source of truth, `content\taxonomy.ts`):
`split-brain`, `cascade`, `thundering-herd`, `config-change`, `resource-exhaustion`,
`bad-deploy`, `data-loss`, `dns-bgp`, `dependency`, `automation-misfire`.

NOTE: project memory (2026-06-25) lists an older set (data-corruption, network-partition,
human-error, observability-gap) — the taxonomy has since been revised. Trust taxonomy.ts.

**Taxonomy discipline (inviolable):** changes to failure classes are a SEPARATE, deliberate
process — never sneak a new class in via an incident's tags. Future AI-incident classes
(model-degradation, training-pipeline, prompt-injection, data-poisoning) are to be proposed
as a batch when enough incidents justify each, per project memory `project-ai-incidents.md`.

## Adding an incident

1. Create `content\incidents\<id>.md` — filename = id, lowercase-hyphens,
   convention `company-year-slug` (e.g. `github-2018-splitbrain`).
2. Frontmatter, all fields required unless marked optional (schema enforced by
   `scripts\validate-incidents.ts`): `id` (= filename), `company`, `title`, `year`,
   `date` (YYYY-MM-DD), `duration`, `classes[]` (≥1, from taxonomy.ts), `patterns[]`,
   `impact`, `trigger`, `mechanism`, `lesson`, `interview`, `source` (valid URL),
   `sourceLabel`, `source_quote` (optional), `archive_url` (leave blank — `npm run archive`
   fills it), `date_added`, `last_verified` (optional), `verified` (bool).
3. `npm run validate` → must be green. `npm run dev` regenerates the index; the incident
   appears on the home feed and at `/incident/<id>`.
4. Hand over as uncommitted diff; the user reviews, commits, and Vercel deploys.

## THE FOUR INGEST-QUALITY RULES (user doctrine, each learned from a real mistake)

Self-review every extracted incident against these BEFORE writing the file — read
`trigger`, `duration`, `date`, `mechanism` back against the source text and ask: faithful,
or simplified/fabricated?

1. **Never placeholder dates.** No exact date in the source → infer the best approximate
   month from context, never `YYYY-01-01`. (Origin: incident-io-2023-connection-pool-exhaustion
   shipped with a fabricated 2023-01-01.)
2. **Duration = full user-facing impact window,** not the vendor's outage window. (Origin:
   incident-io-2025-aws-outage-cascade listed ~3h42m — AWS's window — but the product's
   Scribe was down ~10h30m.)
3. **`trigger` = the true initiating event,** not a later amplifier. (Origin:
   incident-io-2023-gke-dataplane listed a runaway query; the real trigger was post-migration
   connection churn exposing GKE Dataplane V2 CPU amplification.)
4. **Multi-event incidents: describe each event honestly** — never claim they "replayed the
   same failure" when proximate causes differed. (Origin: github-2020-proxysql — four events,
   different triggers, root cause LimitNOFILE capping found only in event 3.)

## Design identity (from project memory — binds all UI work)
"Status page, inverted": light palette, typography Archivo / Public Sans / IBM Plex Mono,
the uptime tick strip as the visual signature. **Dark themes were explicitly rejected as
"AI-default".** Class colors live in taxonomy.ts per class. Don't introduce a new visual
language in a session.

## Traps
- Import `<Head>` from `vite-react-ssg`, NEVER `<Helmet>` from react-helmet-async —
  vite-react-ssg owns the HelmetProvider; a second instance can't find the provider.
- Route enumeration lives in `src\routes.tsx` — new page types (e.g. per-pattern pages)
  must be registered there for SSG to prerender them.
- `npm run archive` rewrites frontmatter — run validate after, and never run it on a dirty
  incident you haven't finished reviewing.
- The repo has ~10 uncommitted files at any time — normal review-before-commit WIP; leave it.

## Phase 2 status (verified 2026-07-06 — ahead of the written roadmap)
1. Open-source setup (CONTRIBUTING.md, issue templates, CODEOWNERS): **NOT STARTED** (all absent).
2. Patterns index pages: **NOT built** (patterns are filter chips only).
3. Discovery bot: **BUILT** — `scripts\discovery.ts` + `content\queue\` + daily GitHub Action.
4. LLM extraction pipeline: **scripts exist** (`ingest.ts`, `ingest-prep.ts`, `ingest-apply.ts`) —
   maturity unverified.
5. SysDesignVault cross-link: unspecced.
Execution playbook: see `onthejob-phase2-campaign`.

## Provenance and maintenance
Authored 2026-07-06 from: package.json, content\taxonomy.ts, content\incidents\ (30 files),
.github\workflows\{ci,archive,discovery}.yml, scripts\ listing, README.md, and project memory
(project-onthejob, feedback-ingest-quality, project-ai-incidents, project-design-identity).
Re-verify:
```powershell
(Get-ChildItem C:\Users\subha\Projects\onthejob\content\incidents -Filter *.md).Count   # 30 as of 2026-07-06
Select-String -Path C:\Users\subha\Projects\onthejob\content\taxonomy.ts -Pattern '^\s+"[a-z-]+":' | Measure-Object   # 10 classes
(Get-Content C:\Users\subha\Projects\onthejob\package.json -Raw | ConvertFrom-Json).scripts   # command table still accurate?
Test-Path C:\Users\subha\Projects\onthejob\CONTRIBUTING.md                                # False until repo goes public
git -C C:\Users\subha\Projects\onthejob log -1 --format='%cs %s'
```
If taxonomy classes or scripts change, update this file and date-stamp the edit; also flag
the stale class list in project memory to the user.
