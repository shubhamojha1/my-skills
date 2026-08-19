---
name: tailor
description: Tailor Shubham's LaTeX resume to a specific job description. Infers the target role family from the JD, selects tagged bullets from data/master-resume.md, applies that family's section-order recipe, edits resume_faangpath.tex below the content marker, runs the guardrail scan, compiles with Tectonic, and writes output + rationale to out/<company>-<role>/.
argument-hint: jds/<company>-<role>.md [--family SDE|BE|INFRA|AIE|SRE|DVO|HFT]
disable-model-invocation: true
allowed-tools: Read, Edit, Write, AskUserQuestion, Bash(tectonic *), Bash(pdftotext *), Bash(mkdir *), Bash(cp *), Bash(python scripts/tailor_check.py *)
---

# /tailor

Tailor the resume at `resume_faangpath.tex` to the job description at `$0`.

## Inviolable rules

1. **Never edit above the line `% ===== CONTENT BELOW — AI edits only below this line =====`** in `resume_faangpath.tex`. That covers `\documentclass`, packages, `\newcommand` macros, geometry, `\name`, `\address`. If the tailoring goal seems to require a preamble/macro change, stop and ask instead of touching it.
2. **`data/` is read-only.** Every claim in a tailored bullet comes from `data/master-resume.md`. Never edit that file to make a tailored output work — if content is missing, say so and stop. Confirmations the user gives you during a run apply to **that run only**; tell them the exact line to add to `data/master-resume.md` themselves.
3. **Never read `notes/`.** It holds unverified metrics and personal reminders that must never reach a PDF. Nothing in it is resume content. (This is a prohibition, not an enforced sandbox — the guardrail scan in step 6 is the backstop, since leaked notes content carries `⚠` and trips the abort.)
4. **No invented metrics or claims.** If the JD wants a skill the source has no bullet for, do not stretch an unrelated bullet to imply it. Ask (step 4), then record the gap in `rationale.md`.
5. **Escape on the way in.** Pipe every piece of prose you lift out of `data/master-resume.md` through `python scripts/tailor_check.py escape` before it becomes LaTeX. Never run it over LaTeX you wrote yourself — it will escape your own macros. The source is full of `80%` and `~50K`; an unescaped `%` silently truncates the rest of the line and the failure is invisible until someone reads the PDF.
6. **Scan before shipping, and honour the abort.** `python scripts/tailor_check.py scan resume_faangpath.tex --log resume_faangpath.log --pdf resume_faangpath.pdf` must exit 0. The PDF check requires Poppler's `pdftotext` and catches text-layer failures the LaTeX scan cannot see. A non-zero exit means stop and report — do not hand over the PDF, do not work around the check by deleting the marker it caught.
7. **Always compile.** `tectonic --keep-logs resume_faangpath.tex` from the repo root; on failure read `resume_faangpath.log`, fix, recompile. Never hand back a `.tex` that doesn't produce a PDF.
8. **Never auto-commit.** Leave the edited `.tex` as an uncommitted diff for the user to review.
9. If the resume's macros or section structure look different from what's described here, stop and ask before restructuring anything.

## Layout

```
data/master-resume.md   superset source: positioning lines, bullet bank, projects, writing, skills, education
data/keywords.md        ATS keyword priority per role family
resume_faangpath.tex    THE artifact (repo root; template and working file are the same file)
resume.cls              custom class: rSection environments
scripts/tailor_check.py escape / scan / selftest
jds/<company>-<role>.md input
out/<company>-<role>/   resume.pdf + tailored .tex + rationale.md
notes/                  NEVER read during a tailoring run
```

`resume_faangpath.tex` uses `resume.cls`: `rSection{NAME}` environments. Projects are
`\item \textbf{Name $\vert$ \href{url}{Github Link}} $\vert$ stack \hfill \\{description}`.
Experience entries are `\textbf{Title} \hfill dates \\ Company \hfill location` followed by a
bulleted `itemize`. SKILLS is a `tabular` — bare `&` is correct there.

## Role families

| Tag | Family |
|---|---|
| `[SDE]` | general software engineer / product company |
| `[BE]` | backend / distributed systems |
| `[INFRA]` | AI infra / inference / GPU |
| `[AIE]` | AI engineer / applied LLM |
| `[SRE]` | SRE / reliability |
| `[DVO]` | DevOps / platform / cloud |
| `[HFT]` | quant / high-frequency trading |

`[SDE]` is **one** family covering every product-tier company — FAANG, Atlassian, Adobe, Salesforce,
ServiceNow and the rest. Never split it by company tier.

If `--family` is not given, infer exactly one from the JD and **state which and why** before
selecting. Select bullets tagged with that family plus untagged ones. Section order differs by
family and is not cosmetic.

## Bullet ids and variants

Every bullet in `data/master-resume.md` carries an `id:`. Variants of the same bullet share one
id. **Pick exactly one variant.** Emit `% bullet-id: <id>` on its own line directly above each
`\item` you generate — the scan uses these to catch a duplicated variant, and a full-line LaTeX
comment renders nothing.

The one exception: `exp.tiaa.F`'s split variant deliberately emits two `\item`s under a single
`% bullet-id: exp.tiaa.F`.

## Section-order recipes

Order is listed section by section. Bullets are listed in emission order.

**Experience ranks above Projects in every family except `[HFT]`.** This is a seniority rule, not a
layout preference. The target is SDE-2 / L4 / P4, and at that level projects are supporting evidence
for what someone already does at work — leading with them reads as a candidate whose best work is
unpaid. `[HFT]` is the deliberate exception: a quant desk screens on language and low-level depth
first, and the C/C++/Rust projects are the only place that evidence exists.

**`[SDE]`** — Amazon, Nutanix, Wissen
- Order: Experience → Projects → Skills → Education
- Positioning: `pos.sde`
- TIAA bullets: `exp.tiaa.B` (SOAP-free variant), `exp.tiaa.C`, `exp.tiaa.D`, `exp.tiaa.F` (compressed)
- Projects: `proj.simplemq` → `proj.heimdall` → `proj.bifrost` *or* `proj.sqlite`
- Cut: `exp.tiaa.E`, `exp.tiaa.G`, the ML intern role, all AI-infra framing
- Drop order on overflow: `exp.tiaa.F` → `exp.iitp.A` → third project

**`[BE]`** — backend / distributed systems
- Order: Experience → Projects → Skills → Education
- Positioning: `pos.be`
- TIAA bullets: `exp.tiaa.B` (systems-vocabulary variant), `exp.tiaa.C` (cache-coherence variant), `exp.tiaa.D`, `exp.tiaa.F`
- Projects: `proj.simplemq` → `proj.heimdall` → `proj.scratchdb` *or* `proj.bifrost`
  (`proj.scratchdb` is `⚠ verify` — it has no scope line, so `proj.bifrost` is the working default)
- Drop order on overflow: `exp.tiaa.F` → `exp.iitp.A` → third project

**`[INFRA]`** — Fireworks, Together, Baseten, Sarvam
- Order: Experience → Projects → Writing → Skills → Education
- Positioning: `pos.infra`
- TIAA bullets: `exp.tiaa.A` first, then `exp.tiaa.B`, `exp.tiaa.C`. Trim TIAA to 3 bullets total.
- Projects: `proj.helios` → `proj.sommelier` → `proj.simplemq`
- `writing.entry` naming the inference post is mandatory here.
- Drop order on overflow: `proj.simplemq` → `exp.tiaa.C` → `exp.tiaaml.A`

**`[AIE]`** — applied LLM / AI engineer
- Order: Experience → Projects → Writing → Skills → Education
- Positioning: `pos.aie`
- TIAA bullets: **`exp.tiaa.A` first** (it is the whole reason this is a credible candidacy), then `exp.tiaa.C`, `exp.tiaa.B`
- Projects: `proj.helios` → `proj.mnemosyne` → `proj.simplemq`
- Drop order on overflow: `exp.tiaa.B` → `proj.simplemq` → `writing.entry`

**`[SRE]`**
- Order: Experience → Projects → Skills → Education
- Positioning: `pos.sre`
- TIAA bullets: `exp.tiaa.F` (split variant, two items), `exp.tiaa.D`, `exp.tiaa.C`, `exp.tiaa.B`
- Projects: `proj.heimdall` → `proj.systemsfailed` → `proj.simplemq`
- Never put `proj.loki` on paper — mention it verbally.
- Drop order on overflow: `exp.tiaa.B` → `exp.iitp.A` → `proj.simplemq`

**`[DVO]`** / cloud
- Order: Experience → Projects → Skills → Education
- Positioning: `pos.dvo`
- TIAA bullets: `exp.tiaa.F` (split variant), `exp.tiaa.B`, `exp.tiaa.C`
- Projects: `proj.heimdall` → `proj.systemsfailed` → `proj.helios` (framed as "deployed and operated a GPU inference service")
- Terraform and Prometheus are gaps, not skills — see `data/keywords.md`. Record in `rationale.md`, never list them.
- Drop order on overflow: `exp.tiaa.C` → `exp.iitp.A` → `proj.helios`

**`[HFT]`** — Tower, Optiver, Graviton, Quadeye, Da Vinci, IMC
- Order: **Skills → Competitive Programming → Projects → Experience → Education**
- This is the only family that leads with Skills, and the only one where Projects outrank Experience.
  A quant screener filters on language first: C++ must be visible in the top inch or the resume is
  binned before the experience section is read. Languages go first inside Skills, C/C++/Rust first
  inside languages (`data/keywords.md`).
- Positioning: `pos.hft`
- **`cp.line` is mandatory here and forbidden everywhere else.** See the gating rule below.
- Projects: `proj.bifrost` → `proj.sqlite` → `proj.chronos`. C, C++ and Rust lead by language, not
  by tier — `proj.heimdall` is the stronger project overall but it is Go, so it swaps in only when
  the JD emphasises networking or systems over language match.
- TIAA bullets: `exp.tiaa.D` (default variant) first — the only production bullet phrased as work
  taken *off* a hot path, and the latency delta is the point. Then `exp.tiaa.C` (cache-coherence
  variant). Then `exp.tiaa.B` (SOAP-free variant) as **the single line the entire Java / Spring /
  Kubernetes stack gets**. Never more than 3 TIAA bullets, never a fourth enterprise-stack line.
- Cut: `exp.tiaa.A`, `exp.tiaa.E`, `exp.tiaa.F`, `exp.tiaa.H`, `exp.tiaa.I`, `exp.tiaa.J`, the ML
  intern role, `writing.entry`, and all AI/LLM framing. None of it reads as a signal at a quant desk
  and every line of it costs space that a C++ project needs.
- Lock-free structures, kernel bypass (DPDK / io_uring), NUMA-aware layout and market-data protocols
  (FIX, ITCH) are **gaps, not skills** — `data/keywords.md`. Record in `rationale.md` every run.
- Drop order on overflow: `exp.tiaa.C` → `exp.iitp.A` → `proj.chronos`

## `cp.line` — family-gated, enforced mechanically

`cp.line` (competitive programming, §6 of `data/master-resume.md`) may appear **only** on an `[HFT]`
run. A rating is a credential at a quant desk and a liability at a product company, where a screener
reads it as "this person wants a different job".

This is not left to memory. `scan` aborts if `% bullet-id: cp.line` appears without `--family HFT`,
and defaults to refusing it when no family is passed. Pass the family you selected on every run:

```
python scripts/tailor_check.py scan resume_faangpath.tex --family <FAMILY>
```

Add further family-gated ids to `FAMILY_ONLY` in `scripts/tailor_check.py`, not to prose here.

## Hard guardrails

`data/master-resume.md` deliberately contains placeholders and cut-marked content. Output goes to
recruiters. **Abort and report — do not compile, do not hand over — if any of these reach the
`.tex`:**

- A rendered line containing `←`, `→`, `⚠`, `FILL THIS IN`, `needs`, or `[X]`
- Content from inside `~~strikethrough~~`
- More than one variant of the same bullet id
- A claim marked `⚠ verify`, unless the user explicitly approved it in step 4 of this run
- Non-ASCII in rendered content (no Unicode font is loaded — `escape` substitutes ASCII equivalents)

`scripts/tailor_check.py scan` enforces all of these mechanically except the `⚠ verify` approval,
which is yours to track. Fail loudly. A silent placeholder in a submitted resume is worse than no
output.

The scan ignores full-line LaTeX comments, since they render nothing — that is also why `needs`
being a common English verb does not fire on prose you didn't emit. It does still fire on `needs`
inside a real bullet; if that blocks a legitimate sentence, rephrase rather than disabling the check.

## Workflow

1. **Read the JD** at `$0`. Extract role title, seniority, minimum years, must-have vs nice-to-have requirements, ATS keywords, and implicit signals ("owns inference latency" → `[INFRA]`). If `$0` doesn't exist, tell the user to paste the JD into `jds/<company>-<role>.md` first and stop.

   **Run an eligibility preflight before tailoring.** Full-time experience starts July 2024. Rate the application:
   - `GREEN` — minimum is 2 years or less and the central stack/domain is backed by professional evidence.
   - `AMBER` — minimum is 3 years, or a central requirement is backed only by a personal project. Tailor only after naming the gap; recommend a referral or recruiter conversation rather than a blind application.
   - `RED` — minimum is 4+ years, or the role centrally requires staff/lead/mentoring/roadmap ownership absent from the master. Stop and ask whether the user deliberately wants a low-probability stretch application. A `/tailor` invocation alone is not approval to ignore this gate.

   Put the rating and reasons at the top of `rationale.md`. Tailoring cannot repair an eligibility mismatch.

2. **Pick the family.** State it and the evidence from the JD. Load its recipe above and its row in `data/keywords.md`.

3. **Read `data/master-resume.md`** and the current `resume_faangpath.tex`. Select bullets per the recipe, adjusting for what the JD actually emphasises. Pick exactly one variant per id. Mirror the JD's terminology lightly in wording — never keyword-stuff, never change the underlying facts. Check §0 for title handling.

4. **Pause and ask before writing anything.** Collect two lists, then ask about both in one batched `AskUserQuestion`:

   **(a) Gaps** — every JD must-have (and prominent nice-to-have) the source has no evidence for. Ask whether they have real experience with each.
   - **No** → record it in `rationale.md`. Never invent.
   - **Yes** → ask for concrete details (what they built, tech, scale/metric, which project or role). Use it in this run, and at the end give them the exact block to paste into `data/master-resume.md` so it's reusable. You do not write to `data/`.

   **(b) `⚠ verify` claims you want to use** — show the exact claim and ask if it's accurate and OK to include.
   - **Yes** → use it this run, and at the end tell them to replace that `⚠ verify` line in `data/master-resume.md` with a dated `confirmed:` note and tick the box in `notes/verification-queue.md`.
   - **Corrected** → use their value; same follow-up.
   - **No / unsure** → skip the claim, note it in `rationale.md`.

   Only facts the user states count. Don't embellish.

5. **Edit only below the content marker.** Reorder the `rSection` blocks per the recipe, emit the OBJECTIVE block, and replace `\item` lines.

   OBJECTIVE carries two things in order: `descriptor` (fixed, identical on every family, never
   tailored and never dropped for the page limit) then that family's `pos.*` paragraph. See
   `data/master-resume.md` §1.
 Every bullet gets its `% bullet-id:` comment. Escape all lifted prose (rule 5).

6. **Scan, then compile, then scan again with the log:**
   ```
   python scripts/tailor_check.py scan resume_faangpath.tex --family <FAMILY>
   tectonic --keep-logs resume_faangpath.tex
   python scripts/tailor_check.py scan resume_faangpath.tex --family <FAMILY> --log resume_faangpath.log --pdf resume_faangpath.pdf
   ```
   `--family` is the family you selected in step 2. Omitting it does not disable the check — it makes
   the check strictest, refusing every family-gated id.
   The first scan catches placeholders before wasting a compile. The second adds the page count and
   checks the compiled text layer for missing identity fields, image-only output, replacement characters,
   and Unicode presentation-form ligatures.

7. **One page, always.** If the scan reports more than 1 page, drop the next bullet from that family's drop order and recompile. **Never shrink the font below 10pt or margins below 0.2in** — both already sit at that floor, and both live in the preamble, which is off-limits anyway (rule 1). Cut content instead. Each family's drop order lists 3 items — that is the cap. If it still overflows after all 3, stop and report rather than gutting the resume by improvisation.

   Measured 2026-07-29 on `[INFRA]` (positioning line + new WRITING section + 3 projects + 3 TIAA bullets + IIT Patna + skills + education): **1 page with zero drops.** The budget has room; treat the drop order as insurance, not an expectation. That measurement predates the 2026-08-04 section reorder, which moves content without adding any — the page budget is unchanged.

8. **Write outputs** to `out/<company>-<role>/`:
   - `resume.pdf` — copy of the compiled PDF
   - `resume_faangpath.tex` — copy of the tailored source
   - `rationale.md` — why this family, these bullets, this order, mapped to specific JD requirements; which variant was chosen per id and why; every gap the source couldn't back; every `⚠ verify` claim used and the user's exact approval; every bullet dropped for the page limit. `/scout` reads this file — keep it.

9. **Report back**: family chosen, bullets used, scan result, page count, and any `data/master-resume.md` lines the user should update by hand. Remind them the edit to `resume_faangpath.tex` is uncommitted and awaiting review.
