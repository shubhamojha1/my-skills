---
name: resume-and-career-ops
description: Use when touching the resume system (Projects\resume), tailoring to a job description, editing resume bullets or inventory YAMLs, compiling LaTeX with tectonic, or working the career surfaces (personal-site, github.io, portfolio positioning). Triggers - resume, tailor, JD, job description, inventory yaml, VERIFY tag, tectonic, resume_faangpath.tex, rationale.md, ATS, career, LaTeX escape.
---

# Resume & Career Ops — the career surface of this machine

`C:\Users\subha\Projects\resume` holds a LaTeX resume with an inventory-driven tailoring
system. The repo has its own project skill — **`/tailor` (at
`Projects\resume\.claude\skills\tailor\SKILL.md`) is authoritative for tailoring work inside
that repo**; invoke it there as `/tailor jds/<company>-<role>.md`. This machine-level skill
is orientation + the binding rules, so no session stumbles into the repo blind.

## The system (verified 2026-07-06)

| Piece | Role |
|---|---|
| `resume_faangpath.tex` | THE artifact. Line 21 is the marker: `% ===== CONTENT BELOW — AI edits only below this line =====` — everything above (documentclass, macros, name) is hands-off |
| `inventory\projects.yaml`, `inventory\experience.yaml` | **single source of truth for every claim**; the file header states it: every metric is either verbatim from the tex or flagged `[VERIFY]` |
| `jds\<company>-<role>.md` | input job descriptions (4 present) |
| `out\<company>-<role>\` | deliverables per application: resume.pdf + tailored .tex + rationale.md (3 present; don't enumerate names in documents — application history is sensitive) |
| `resume.cls` | custom class: `rSection` environments, EXPERIENCE / PROJECTS / SKILLS / Education order |
| tectonic | `C:\Users\subha\bin\tectonic.exe` (on User PATH) — the compile gate |

Inventory schema (real shape): each project/experience topic has `stack`, `links`, `tier`
(1–3, lower = stronger default), `archetype_tags` (`ai-infra | backend-sde | devops-sre |
fullstack`), `metrics`, and 1–3 bullet `variants` tagged `impact-led | systems-led |
scale-led`, each with a `source:` line tracing it to the tex. **8 `[VERIFY]` tags exist as
of 2026-07-06** — including a live conflict on Helios hardware ("Qwen2.5-3B on RTX 4070" vs
resume text "quantized Mistral-7B"). `[VERIFY]` = unconfirmed claim: only the user resolves it.

## The rules that bind ANY session in this repo (from /tailor — restated, not replaced)
1. Never edit above the line-21 marker. Preamble change seems needed → stop and ask.
2. No invented metrics or claims — inventory YAMLs only. `[VERIFY]` bullets: skip or ask;
   NEVER resolve by guessing.
3. JD wants something the inventory can't back → record the gap in `rationale.md`;
   don't stretch an unrelated bullet.
4. Escape LaTeX specials in prose you write: `% & _ # $ ~ ^` → `\% \& \_ \# \$
   \textasciitilde{} \textasciicircum{}`.
5. **Always compile before finishing**: `tectonic resume_faangpath.tex` from the repo root;
   on failure read `resume_faangpath.log`, fix, recompile until clean. Handing over an
   uncompiled .tex is a rule violation (`machine-validation-and-qa`).
6. Never auto-commit (iron rule anyway — `machine-change-control`): tailored .tex stays as
   an uncommitted diff for the user's review.
7. Structure looks different from what /tailor describes → stop and ask (drift guard).

## Keeping the inventory alive (how new work becomes resume material)
When a project hits a milestone (e.g. helios campaign phases complete, systemsfailed.dev
launches), the flow is: propose a new bullet variant in the matching inventory entry with
tier + archetype_tags + metrics; every number the user hasn't confirmed gets `[VERIFY]`;
the user confirms → tag drops. This is the ONLY path from "did the work" to "resume claims
it" — never edit the .tex bullets directly without an inventory backing.

## Adjacent career surfaces (pointers)
- **systemsfailed.dev** (Projects\onthejob) — the flagship portfolio piece; public-name
  discipline and launch plan in `onthejob-operations`.
- **personal-site** (Next.js, AGENTS.md present) and **shubhamojha1.github.io** (branch
  `first_post`, 42 uncommitted files — heaviest WIP in the portfolio; treat as mid-flight).
- **leetcode-company-wise-problems** — external clone, interview-prep data.
- The `/resume` slash command in session history is Claude Code's built-in session-resume,
  NOT this repo — don't confuse them.

## When NOT to use
Actual tailoring inside the repo → `/tailor` (it has the full workflow: JD analysis →
selection → edit below marker → compile → out\ + rationale.md). Site work → the repo's own
conventions + `frontend-design` plugin. This skill orients; it doesn't tailor.

## Provenance and maintenance
Authored 2026-07-06 from: tailor SKILL.md (read in full), inventory\projects.yaml header +
schema, marker-line grep (line 21), out\/jds\ counts, Get-Command tectonic. Re-verify:
```powershell
Select-String -Path C:\Users\subha\Projects\resume\resume_faangpath.tex -Pattern 'CONTENT BELOW' | Select-Object LineNumber   # marker intact (line 21 as of 2026-07-06)
(Select-String -Path C:\Users\subha\Projects\resume\inventory\*.yaml -Pattern '\[VERIFY\]' | Measure-Object).Count            # 8 as of 2026-07-06; rising = unconfirmed claims accumulating
Test-Path C:\Users\subha\Projects\resume\.claude\skills\tailor\SKILL.md   # project skill still present
(Get-Command tectonic).Source                                             # C:\Users\subha\bin\tectonic.exe
```
If /tailor's rules change, THIS summary must be re-synced the same day (one home per fact:
/tailor owns the rules; this skill mirrors them for discovery).
