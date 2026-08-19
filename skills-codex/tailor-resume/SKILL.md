---
name: tailor-resume
description: Tailor Shubham Ojha's one-page LaTeX resume to a job description and produce a submission-ready PDF grounded only in verified evidence. Use when the user asks Codex to tailor, customize, rewrite, optimize, or generate a resume for a specific role or JD; asks whether a resume fits a role; or wants a final factual, ATS-readable, natural-sounding resume that avoids generic AI prose. Also use for regenerating an existing tailored variant after facts or formatting change.
---

# Tailor Resume

Produce a selective resume, not a keyword-expanded version of the master. Optimize for truthful role fit, fast human scanning, and defensibility in an SDE-2 interview.

Never promise that text is "AI-undetectable." No reliable process can guarantee that. Make the resume sound natural by preserving specific human evidence, removing generic model prose, and refusing invented or weakly supported claims. Never use detector-evasion or "humanizer" tools.

## Required inputs and boundaries

Work from the resume repository root. Read `AGENTS.md` if present, then read:

1. The supplied JD file or pasted JD.
2. `data/master-resume.md`, the only resume-content source of truth.
3. `data/keywords.md` only for terminology that the evidence genuinely supports.
4. `resume_faangpath.tex` only as the layout/preamble template.
5. `references/writing-gate.md` in this skill on every run.
6. `references/role-shapes.md` after classifying the role.

Do not read `inventory/` for facts; it is superseded. Do not read `notes/` while selecting content; it contains reminders and unverified material. Do not alter `data/` during a tailoring run.

Preserve all user changes. Do not edit the root `resume_faangpath.tex`; copy it into a temporary build directory. Keep identity, links, document class, and macros unchanged. In the temporary copy only, increase margins to at least 0.45 inches when the template is tighter, then fit the page by cutting content. Never create or amend a commit without explicit approval.

**Output hygiene:** Build and validate outside `out/`; the only newly persisted artifact from a run is `Shubham_Ojha_Resume.pdf`. In particular, never leave `resume_faangpath.pdf`, `resume_page.png`, `resume.cls`, or `resume_faangpath.log` in a job output directory. Do not delete or rename any pre-existing output file unless the user explicitly names it for cleanup.

## Non-negotiable evidence rules

- Trace every rendered claim to a bullet id or confirmed note in `data/master-resume.md`.
- Never emit content marked `⚠ verify`, a placeholder, strikethrough, or a source conflict.
- Do not treat one-run verbal approval as sufficient for a submission artifact. If the user supplies a new fact, ask whether to record it in the master as a separate explicit update; use it only after it is recorded with a dated `confirmed:` note.
- Do not convert adjacency into experience: project Go is not professional Go; in-memory caching is not Redis; EKS is not generic AWS architecture ownership; a PoC is not production.
- Include a skill only when a work bullet, selected project, public contribution, education item, or confirmed master note supports it.
- Use public project metrics only when the benchmark setup and result are recorded in the master and do not conflict with the linked repository. If a selected project has a public URL, cross-check its title, stack, model/version, and core scope. Use the conservative intersection or omit the claim.
- Treat missing must-haves as gaps, not keywords to insert.

## Workflow

### 1. Run the eligibility preflight

Extract minimum years, level, central stack, domain, location, work authorization, and leadership expectations. Rate the application:

- `GREEN`: minimum experience is at most two years and the central requirements have professional evidence.
- `AMBER`: minimum is three years, or one central requirement is project-only.
- `RED`: minimum is four or more years, or the role centrally requires senior/lead/staff, mentoring, roadmap, or domain ownership absent from the master.

For `RED`, stop before generating files and ask whether the user deliberately wants a low-probability stretch application. For `AMBER`, state the exact gap before continuing. Never imply tailoring repairs an eligibility mismatch.

### 2. Build an evidence ledger before drafting

Create a private working table with:

`JD requirement | importance | evidence id | confirmed? | professional/project/public | use/omit`

Reject any row without a confirmed evidence id. Select for signal, not coverage. Prefer production outcomes and externally reviewed open-source work over another personal project.

### 3. Choose the resume shape

Use the closest shape in `references/role-shapes.md`, then adapt to the JD. Default rules:

- Put Experience first.
- Omit OBJECTIVE and the fixed descriptor by default.
- Use a summary only for a genuine role transition and keep it to 18-25 words.
- Use at most four primary-role experience bullets.
- Use at most two projects.
- Prefer OPEN SOURCE over WRITING for backend roles when verified contributions fit.
- Keep one page by cutting weak evidence, never by shrinking below 10 pt or using margins below 0.45 inches. If the existing preamble prevents this, report the layout blocker instead of silently changing it.

### 4. Draft from evidence, not from resume clichés

For each bullet, choose one main point: ownership/decision, mechanism, or outcome. Aim for 20-32 words and no more than two clauses. A longer bullet must earn its length with a concrete constraint or result.

Keep the candidate's actual nouns: system, component, protocol, constraint, measurement, and result. Use the JD's exact term only when it describes the same thing. Do not manufacture a tradeoff merely to sound senior.

Run the full writing gate. If a sentence sounds like a model summarizing a topic rather than an engineer describing work, rewrite it from the source fact or cut it.

### 5. Generate in a temporary build directory

Create a unique temporary build directory outside `out/`. Copy the root LaTeX template there as `Shubham_Ojha_Resume.tex`, along with `resume.cls`, and replace all content below the marker. The only permitted pre-marker edit in the temporary copy is increasing geometry margins to the 0.45-inch floor; never make margins smaller or alter identity, links, class, or macros.

Emit `% bullet-id: <id>` directly above every selected item. For non-item content such as a public contribution or education entry, emit a `% source-id: <id>` comment.

Create `out/<company>-<role>/` only for the passing artifact. Use the ATS-safe final filename `Shubham_Ojha_Resume.pdf`.

### 6. Validate source, PDF, and appearance

From the repo root, run against the temporary files:

```text
python scripts/tailor_check.py scan <tmp>/Shubham_Ojha_Resume.tex --family <FAMILY>
tectonic --keep-logs --outdir <tmp> <tmp>/Shubham_Ojha_Resume.tex
python scripts/tailor_check.py scan <tmp>/Shubham_Ojha_Resume.tex --family <FAMILY> --log <tmp>/Shubham_Ojha_Resume.log --pdf <tmp>/Shubham_Ojha_Resume.pdf
```

After every check passes, move or copy the passing PDF to `out/<slug>/Shubham_Ojha_Resume.pdf` and delete the temporary build directory. Do not clean, rename, or normalize other files already present in the job output directory.

Also:

- Extract the PDF with `pdftotext -layout` into the temporary directory or standard output and verify name, email, employer, title, dates, sections, and reading order.
- Render any image needed for visual inspection in the temporary directory. Reject clipped text, overflowing rows, tiny type, excessive density, broken links, or suspicious whitespace.
- Check that every number in the extracted text appears in the evidence ledger.
- Search the rendered prose for unsupported JD keywords and the writing-gate patterns.
- Treat any failed check as a blocker. Do not call the PDF submission-ready.

### 7. Keep a private audit trail

Maintain working notes during the run containing:

1. Eligibility rating and reasons.
2. Role classification and section order.
3. Evidence ledger for every rendered claim.
4. Requirements deliberately omitted and why.
5. Human-voice findings and edits made.
6. Source scan, compile, PDF-text scan, page count, and visual-inspection results.
7. Any public-source discrepancies.

Summarize the eligibility, most important omission, validation result, and any public-source discrepancy in the final response. Do not persist the audit notes in `out/`; the final job directory contains only the PDF.

Do not mark the application as submitted or modify `tracking/applications.csv` unless the user says they actually submitted it.

## Completion standard

Call the result submission-ready only when all facts trace to confirmed evidence, no selected claim conflicts with a public source, the prose passes the writing gate, the PDF passes deterministic checks, the page was visually inspected, the role is not an unacknowledged `RED` stretch, and the run left none of the four named temporary artifacts in `out/<slug>/`.

Report the output path, eligibility rating, most important omission, validation result, and that all changes remain uncommitted.
