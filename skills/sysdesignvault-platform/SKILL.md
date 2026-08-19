---
name: sysdesignvault-platform
description: Use when working in Projects\sysdesignvault — adding or editing MDX concepts, building widgets, the concepts data pipeline, progress tracking, learning paths, search, or platform-gap work. Triggers - sysdesignvault, MDX concept, _concepts-data.json, build-concepts.js, widget, WidgetRenderer, learning path, progress tracking, Clerk, Prisma, Next.js 16, USACO Guide.
---

# SysDesignVault — Platform Runbook & Gap Campaign

SysDesignVault (`C:\Users\subha\Projects\sysdesignvault`) is the user's systems-design
learning platform — ambition: "the USACO Guide for systems" (premium tiers planned).
Second-heaviest active work on this machine. Stack: **Next.js 16.2.1 + React 19.2.4 +
Tailwind 4 + Prisma 7 + Clerk + D3** — all post-training-data versions.

**The repo's own AGENTS.md warning is doctrine** (quote, verified 2026-07-06):
> "# This is NOT the Next.js you know — This version has breaking changes — APIs,
> conventions, and file structure may all differ from your training data. Read the relevant
> guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices."

## When to use / when not
- USE for: concept/MDX work, widgets, data pipeline, progress/paths/search platform work.
- NOT for: general session mechanics (`machine-run-and-operate`), evidence standards
  (`machine-validation-and-qa`), git/install gating (`machine-change-control`).

## The content pipeline (inviolable)

```
content\<domain>\<concept>.mdx   ←  YOU EDIT HERE (source of truth)
        │  node scripts\build-concepts.js
        ▼
src\data\_concepts-data.json     ←  GENERATED (469 KB as of 2026-07-06) — NEVER hand-edit
```

User doctrine (project memory, 2026-06): "NEVER edit `_concepts-data.json`; always write
MDX then run `node scripts/build-concepts.js`." The generated file shows as modified in
git status — that is regeneration output, normal.

Verification loop after any MDX change (from repo root):
```powershell
node scripts\build-concepts.js
Select-String -Path src\data\_concepts-data.json -Pattern "<some phrase you just wrote>" -Quiet   # True = landed
npm run lint
```
`npm run build` (= `prisma generate && node scripts/build-concepts.js && next build` via
prebuild) is the full gate — run before claiming platform work done.

MDX frontmatter schema (verified example `content\ai-foundations\rnn-basics.mdx`):
`id`, `name`, `description`, `category`, `introduced_by`, `systems[]`, `difficulty`
(beginner/…), `prerequisites[]` (concept ids), `widget` (widget slug — see below).

## Widget-first rule (user doctrine, no asking)

"Always build the interactive widget BEFORE content edits on any topic." Widgets live at
`src\components\content\<topic>\<Name>Widget.tsx` (real examples, verified:
`rnn\RNNWidget.tsx`, `layer-norm\LayerNormWidget.tsx`, `feed-forward\FeedForwardWidget.tsx`,
`thundering-herd\ThunderingHerdWidget.tsx`), rendered through
`src\components\content\WidgetRenderer.tsx`, referenced from MDX frontmatter `widget:` slug.
Copy an existing widget dir as the pattern. The widget layer is the platform's moat —
protect its quality.

## Current state (verified 2026-07-06 — expect drift, re-verify)

- 57 MDX files across `content\<domain>\` (count:
  `(Get-ChildItem C:\Users\subha\Projects\sysdesignvault\content -Recurse -Filter *.mdx).Count`).
- Working tree (last commit 2026-06-15 "page change"): the **AI-paths expansion is mid-flight
  and untracked** — new domains `content\ai-foundations\`, `content\transformer-internals\`,
  plus 13 new widget dirs (attention, feed-forward, flash-attention, glove, kv-cache,
  layer-norm, lstm-gru, multi-head-attention, positional-encoding, rnn, seq2seq,
  sparse-attention, tokenization, word2vec). Untracked ≠ unwanted — do NOT clean up or commit
  (see `machine-change-control`).
- **Progress tracking is IMPLEMENTED** (was gap #1 in the 2026-06-16 memo — the memo is
  stale on this): `src\lib\progress.ts` = localStorage-first (`sysvault:progress` key,
  read/completed/validated maps) with fire-and-forget sync to `src\app\api\progress\route.ts`
  (Clerk `auth()` + Prisma `db.user/progress/completions` upserts); `ProgressSync.tsx` wired
  in `app\layout.tsx`. Auth/db are REAL, not dormant: `prisma\schema.prisma` exists.
  End-to-end persistence across devices: unverified — needs a signed-in manual check.
- App surface: `src\app\{api, compare, concepts, graph, paths, simulator, simulators, systems}`.
- Extra validation script exists: `scripts\check-war-story-links.ts`.

## The gap campaign (memo of 2026-06-16, deadline 2026-06-23 SLIPPED; statuses updated 2026-07-06)

Work top-down; each phase gated; diffs stay uncommitted; new deps = ask user.

1. **Progress tracking — mostly DONE, needs verification close-out.**
   GATE to declare closed: signed-out user can mark-read (localStorage persists across
   reload); signed-in user's progress survives a different browser (server round-trip);
   `npm run build` clean, no hydration errors. If gaps found (e.g. `validated` map not
   synced — progress.ts syncs only concept/simulator), list them for the user.
2. **Content breadth** — 57 concepts vs ~170-topic backlog across 14 domains (memory
   `topics_expansion.md` holds the curriculum list). Flow per topic: widget first → MDX with
   full frontmatter (prerequisites correct!) → regenerate → lint. Batch by domain (the
   untracked ai-foundations pattern is the model). GATE per batch: concept count increases,
   every new concept renders with its widget, build green.
3. **Search** — no way to find a concept by name/keyword. Menu (ranked): (a) client-side
   index (MiniSearch — proven pattern in onthejob, see `onthejob-operations`) over
   the generated concepts data; (b) simple client filter over names only (fast, weaker);
   (c) server search (overkill while static). New dep = user approval first.
   GATE: known concept findable by partial name from any page; no build-size blowup (>~50KB
   index → discuss).
4. **Cross-linking** — `prerequisites[]` exists in frontmatter (verified) but doesn't render
   as inline links in content. Surface them (e.g. prerequisite chips on the concept page +
   inline [[concept]] resolution if cheap). GATE: clicking a prerequisite navigates correctly
   for 3 spot-checked concepts with no 404s (slug = frontmatter `id`).
5. **In-browser exercise runner — FENCED.** "Implement It" sections stay text skeletons by
   explicit deferred decision (memory `feedback_implement_it.md`). Do not build unless the
   user re-opens it.

Already ahead of USACO Guide (don't regress while closing gaps): interactive widgets
(unique in this space), content depth, layered difficulty per path.

## Traps
- Writing Next.js from memory — read `node_modules\next\dist\docs\` first (Next 16 ≠ your
  training data). Same caution for React 19 and Tailwind 4 syntax.
- Editing `_concepts-data.json` or `src\data\paths.ts` expecting content changes to stick —
  check first whether the file is generated (`paths.ts` is currently hand-maintained AND
  modified in the working tree; confirm before touching).
- Forgetting `prisma generate` — it runs inside `npm run build` prebuild, but a bare
  `next build` after schema changes will use stale client types.
- Adding a topic without its widget (violates widget-first) or with an unresolvable
  `prerequisites` id (breaks cross-linking later).

## Provenance and maintenance
Authored 2026-07-06 from: repo state (git log/status), package.json, AGENTS.md,
`src\lib\progress.ts`, `src\app\api\progress\route.ts`, `content\ai-foundations\rnn-basics.mdx`,
widget dir listing, and project memory (vision / widget-first / MDX source-of-truth /
implement-it / platform-gaps / topics-expansion). Re-verify:
```powershell
git -C C:\Users\subha\Projects\sysdesignvault log -1 --format='%cs %s'                        # past 2026-06-15 = re-check state
(Get-ChildItem C:\Users\subha\Projects\sysdesignvault\content -Recurse -Filter *.mdx).Count  # 57 as of 2026-07-06
Test-Path C:\Users\subha\Projects\sysdesignvault\src\lib\progress.ts                          # progress impl still present
Get-Content C:\Users\subha\Projects\sysdesignvault\package.json | Select-String '"next"'     # still 16.2.1?
Get-ChildItem C:\Users\subha\Projects\sysdesignvault\scripts                                  # build-concepts.js still there
```
If the AI-paths expansion gets committed or the memo's gaps close, update the campaign
statuses here and date-stamp the edit.
