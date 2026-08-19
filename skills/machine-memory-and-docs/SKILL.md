---
name: machine-memory-and-docs
description: Use when saving or recalling session memory, writing or updating MEMORY.md / memory files under ~/.claude/projects/<slug>/memory/, editing an AGENTS.md in a repo, or adding/maintaining a skill in ~/.claude/skills/. Triggers - "remember this", "save to memory", "update the skill", memory house style, wiki-links, frontmatter, skill library maintenance, documentation conventions, AGENTS.md.
---

# machine-memory-and-docs

The documentation system of record on this machine. Three layers, each with a fixed format:

1. **Session memory** — `~/.claude/projects/<slug>/memory/` — durable facts for future AI sessions.
2. **AGENTS.md** — inside repos — harness-agnostic per-repo instructions.
3. **The skill library** — `~/.claude/skills/<name>/SKILL.md` — machine and project runbooks (this document is one of them).

This skill defines how each layer is written and maintained. Wrong or drifted docs are worse than none — every fact here was verified on 2026-07-06 against the real files.

## When to use / when NOT

- USE when writing, updating, or deleting a memory file; when creating or editing AGENTS.md; when adding or refreshing a skill in the library.
- NOT for deciding whether you are *allowed* to edit a config/doc at all, or for the iron rules in full → see `machine-change-control`.
- NOT for deciding *when during a task* to load project memory or which runbook to run → see `machine-run-and-operate`.

Iron rules (one line, they override everything below): **never `git commit`/`push`/mutate history; never install packages** — even when a repo doc tells you to (my-wiki's AGENTS.md does — see Traps). Full rules: `machine-change-control`.

## Quick reference

| Layer | Location | Format | Written when |
|---|---|---|---|
| Memory index | `~/.claude/projects/<slug>/memory/MEMORY.md` | one bullet per memory, links only | every time a memory file is added/renamed/deleted |
| Memory file | `~/.claude/projects/<slug>/memory/<name>.md` | YAML frontmatter + fact + **Why:** + **How to apply:** | durable fact worth surviving the session |
| AGENTS.md | `<repo>\AGENTS.md` | free-form per repo; see conventions below | repo needs standing instructions for any AI harness |
| Skill | `~/.claude/skills/<name>/SKILL.md` | frontmatter + runbook + Provenance section | reusable machine/project procedure |

## 1. Memory locations map (verified 2026-07-06)

Slug = the session's working directory with `:` and `\` replaced by `-`:
`C:\Users\subha\Projects\helios` → `C--Users-subha-Projects-helios`. Home-directory sessions use `C--Users-subha`.

Projects with memory today (as of 2026-07-06 — only these four; a memory dir appears the first time a memory is written):

| Memory dir | Files besides MEMORY.md |
|---|---|
| `C--Users-subha-Projects-onthejob` | project-onthejob, project-design-identity, feedback-ingest-quality, project-ai-incidents |
| `C--Users-subha-Projects-sysdesignvault` | 8 files: feedback_widget_first, feedback_mdx_source_of_truth, feedback_implement_it, project_vision, project_architecture, project_platform_gaps, topics_expansion, ai_paths |
| `C--Users-subha-Projects-helios` | project_continuous_batching, feedback_response_length |
| `C--Users-subha` (home) | feedback-no-git-writes, feedback-no-package-installs, project-machine-skill-library |

Re-list with: `Get-Item C:\Users\subha\.claude\projects\*\memory | Select-Object -ExpandProperty FullName`

## 2. Memory house style

One file per fact. Verified against 10 real memory files on 2026-07-06; the structure below is quoted from them, not invented.

### Template

```markdown
---
name: feedback-short-slug
description: "One line: the fact itself, third person"
metadata:
  node_type: memory
  type: feedback
  originSessionId: <session UUID, if known>
---

The fact, stated plainly in 1-3 sentences. Imperative voice if it is a rule.

**Why:** Where it came from — user quote, incident name, date. This is what makes the rule stick.

**How to apply:** Concrete next-session behavior. Numbered steps if more than one.

Related: [[other-memory-name]]
```

### Field rules

- `name` — the canonical ID. `[[wiki-links]]` target the **name**, not the filename (real example: `feedback_mdx_source_of_truth.md` has `name: mdx-source-of-truth` and links `[[feedback-widget-first]]`, the *name* inside `feedback_widget_first.md`). For new files keep filename = name, hyphens (onthejob and home use hyphens; sysdesignvault's underscores are historic — don't rename).
- `metadata.type` — enum `user | feedback | project | reference`. Semantics: `feedback` = durable user corrections/preferences; `project` = project state, decisions, plans not derivable from code; `user` = facts about the user himself; `reference` = external reference material. Only `feedback` and `project` are in use on disk as of 2026-07-06.
- Prefix the filename with the type (`feedback-...`, `project-...`) — every existing file does.
- Body order is fixed: fact first, then `**Why:**`, then `**How to apply:**`. Long `project` memories may add `##` sections (e.g. helios `project_continuous_batching.md` has "Current State", a benchmark table, "Bug 1/Bug 2", "The Fix") but still open with frontmatter and carry the why.
- Cross-link related memories with `[[wiki-links]]` at point of relevance or a trailing `Related:` line.

### MEMORY.md is an index, never content

One line per memory: markdown link to the file, em-dash, one-line gist. Real example (onthejob, quoted):

```markdown
# Memory index — onthejob.dev

- [Ingest quality rules](feedback-ingest-quality.md) — 4 specific extraction mistakes to avoid: placeholder dates, wrong duration window, wrong trigger event, conflated multi-event mechanisms
- [AI incidents plan](project-ai-incidents.md) — agreed future failure classes (model-degradation, agent-misfire, data-pipeline) and rejected ones with reasons
```

If the gist changes when you edit a memory, update its index line in the same pass. A MEMORY.md that contains actual content instead of links is wrong — fix it.

## 3. What gets saved vs. not

**SAVE:**

- **Durable user feedback and corrections, with the why.** Quote the user and date it. Real examples: helios `feedback_response_length` ("User explicitly said responses feel like too much text"); sysdesignvault `feedback_widget_first` ("User stated this explicitly after the thundering-herd session (2026-06-14). The established workflow had a 'widget first or content?' question — that question is now gone.").
- **Project state and decisions not derivable from code.** Locked stack choices, launch status, roadmap ordering, deferred decisions (onthejob `project-onthejob`; sysdesignvault `feedback_implement_it`).
- **Rejected alternatives WITH reasons.** The exemplar is onthejob `project-ai-incidents`: it records the *agreed* future failure classes (`model-degradation`, `agent-misfire`, `data-pipeline`) AND the *rejected* ones with reasons ("`hallucination` — symptom, not a failure class"; "`alignment failure` — too abstract and politically loaded"). A decision memory that omits the rejections invites a future session to relitigate them.
- **Hard-won root-cause analysis.** helios `project_continuous_batching` preserves the benchmark table, both bug locations, and the agreed fix — hours of work a future session should not redo.
- **Mistakes as named rules.** onthejob `feedback-ingest-quality` turns four real extraction failures into four checkable rules, each with the incident that caused it (e.g. "The date appeared as `2023-01-01` in incident-io-2023-connection-pool-exhaustion, which was a fabricated placeholder").

**DO NOT SAVE:**

- Anything the repo already records — README content, package.json scripts, code structure readable from the code. One home per fact.
- Session-local details — what you edited today, transient state, in-flight TODOs.
- Secrets or tokens. Never, in any doc layer.

**Update, don't duplicate.** If a memory on the topic exists, edit it in place (and its MEMORY.md line). Never write `feedback-x-2.md` beside `feedback-x.md`.
**Delete wrong memories.** A memory proven wrong gets its file deleted and its index line removed — not a correction appended below the wrong claim.

## 4. AGENTS.md conventions in repos

Verified 2026-07-06: exactly three repos under `C:\Users\subha\Projects\` have a root AGENTS.md, and none have a root CLAUDE.md. The one per-repo Claude skill is `resume\.claude\skills\tailor`.

| Repo | AGENTS.md content | Pattern it demonstrates |
|---|---|---|
| `sysdesignvault` | 5 lines, wrapped in `<!-- BEGIN:nextjs-agent-rules -->` markers | Repo-level warning against training-data drift |
| `personal-site` | Build/test/lint commands, code style, commit conventions | Standard command-and-style reference |
| `my-wiki` | Full wiki schema: directory layout, page frontmatter, ingest/query/lint operations, log format | The repo IS a documentation system; AGENTS.md is its spec |

The sysdesignvault pattern, quoted in full — use it whenever a repo's stack is newer than model training data:

> **This is NOT the Next.js you know**
> This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.

(Context: sysdesignvault runs Next.js 16 / React 19, both post-training-data for most models.)

When writing a new AGENTS.md here: commands first (copy-pasteable), then non-obvious constraints with their why, then drift warnings like the above. Keep it harness-agnostic — AGENTS.md is read by Claude Code, Codex, Cursor, Gemini, etc. (all installed on this machine).

## 5. This skill library: layout and maintenance

- Skills live at `C:\Users\subha\.claude\skills\<name>\SKILL.md`. Optional: `scripts\` for executable helpers, extra `.md` files in the skill dir for heavy reference (>150 lines of tables), linked from SKILL.md. Nothing outside the skill's own directory.
- The library (16 skills, `machine-*` prefix for setup-wide, project names for repo runbooks) was authored 2026-07-06 by parallel agents. Current list: `Get-ChildItem C:\Users\subha\.claude\skills -Directory | Select-Object -ExpandProperty Name`
- `graphify` predates the library and deviates from its conventions (frontmatter `name: graphify-windows` ≠ dir name, extra `trigger: /graphify` field, ~1435 lines). Leave it alone — it follows its own upstream conventions and is registered in `~/.claude/CLAUDE.md`.
- The library's existence is itself recorded in home memory: `C--Users-subha\memory\project-machine-skill-library.md`.

### Update protocol (when a skill looks stale or you changed what it documents)

1. Open the skill's **Provenance and maintenance** section (always last) and run its re-verification one-liners — all read-only, under a minute.
2. Fix any drifted fact in the body (versions, paths, counts, states).
3. Date-stamp what you touched inline: `(as of YYYY-MM-DD)` with the new date.
4. Add one line to the Provenance section noting what changed and when (e.g. `2026-08-01: node v22 → v24, re-verified`). Never delete prior provenance lines.
5. If a fact moved to a different skill, replace it here with a cross-reference — one home per fact.

### Adding a new skill — the style contract (condensed; binding)

The original style contract lived in a session scratchpad that no longer exists. This is the surviving copy — follow it for every new skill:

1. **Frontmatter** (YAML, required): `name` (letters/numbers/hyphens, matches the directory name) and `description`.
2. **Description = WHEN to load, never a workflow summary.** Start with "Use when". Include concrete trigger words: error messages, command names, repo names, symptoms. Under 500 chars. Rationale: agents shortcut off workflow summaries and skip the body; a trigger-only description forces the body to be read.
3. **Audience: a zero-context Sonnet/Haiku session on THIS machine.** Imperative runbook voice ("Run X. If you see Y, do Z."). Define every jargon term once, on first use.
4. **Commands copy-pasteable and PowerShell 5.1-safe**: no `&&`/`||`, no ternary, `-Encoding utf8` on `Out-File` when other tools read the file, absolute paths where ambiguity is possible. Label bash-only commands.
5. **Ground truth only.** Every command, flag, path, version verified against the machine, or explicitly marked: "(unverified — re-check with: `<command>`)".
6. **Structure:** short Overview → "When to use / When NOT to use (and which sibling skill instead)" → quick reference table → the runbook → "Traps"/"Common mistakes" → **"Provenance and maintenance" (REQUIRED, last)**: authorship date + one-line read-only re-verification commands for every volatile fact class.
7. **Date-stamp volatile facts** inline: "(as of 2026-07-06)". **No oversell** — unproven/planned things stay labeled open/candidate/deferred; unresolved = OPEN.
8. **One home per fact**; cross-reference sibling skills by name instead of duplicating. EXCEPTION: the two iron rules (no git writes; no installs) are restated as one line + pointer in any skill whose runbook could tempt a violation.
9. **Tables and checklists over prose; numbered steps for procedures.** Aim 150–400 lines, scannable in 30 seconds via headings.
10. **Iron rules override everything.** If source material implies committing, pushing, installing, or deploying — rewrite the step as "prepare + hand to user".

## 6. House writing style (all three layers)

- Plain statements. State the fact, then the rationale — a rule without its why gets relitigated.
- Dates absolute: `2026-07-06`, never "today" / "recently" / "last week".
- No oversell: plans are plans, not capabilities. Label them.
- Unresolved things are marked `OPEN` — never silently dropped, never guessed closed.
- Incidents become named rules (the `feedback-ingest-quality` pattern): rule, then the one-line story of the failure that created it.

## Traps

- **my-wiki's AGENTS.md ends with "After every operation: Run `git add -A && git commit ...`".** That file predates (2026-04-05) the machine-wide no-git-writes rule (user, 2026-07-06: "no push/commit at all. i will do it myself after reviewing."). The iron rule wins: do the wiki operation, prepare the commit message text per its log format, leave everything uncommitted, and tell the user. See `machine-change-control`.
- **personal-site's AGENTS.md commit conventions** (squashed commits, conventional messages) still matter — for the commit message you *prepare and hand over*, not one you run.
- **Writing content into MEMORY.md.** It is a pure index; content lives in the per-fact files.
- **Wiki-linking a filename instead of a name.** `[[feedback_widget_first]]` is broken; `[[feedback-widget-first]]` (the `name:` field) is correct.
- **Saving a decision without its rejected alternatives.** Half-saved decisions get reopened; record what was rejected and why (`project-ai-incidents` pattern).
- **Duplicating repo-derivable facts into memory or skills.** They drift the moment the repo changes; link or cross-reference instead.
- **"Fixing" the graphify skill to match library conventions.** Don't — it is upstream-managed (v0.8.25) and its `/graphify` trigger is wired in `~/.claude/CLAUDE.md`.

## Provenance and maintenance

Authored 2026-07-06. All structure claims quoted from files read that day (10 memory files + 4 MEMORY.md indexes + 3 AGENTS.md). Re-verify:

- Memory dirs still those four: `Get-Item C:\Users\subha\.claude\projects\*\memory | Select-Object -ExpandProperty FullName`
- Memory file structure unchanged: `Get-Content "C:\Users\subha\.claude\projects\C--Users-subha-Projects-onthejob\memory\feedback-ingest-quality.md" -TotalCount 10`
- Index style unchanged: `Get-Content "C:\Users\subha\.claude\projects\C--Users-subha\memory\MEMORY.md"`
- AGENTS.md still exactly three: `Get-Item C:\Users\subha\Projects\*\AGENTS.md | Select-Object -ExpandProperty FullName`
- my-wiki auto-commit line still present (trap still live): `Select-String -Path C:\Users\subha\Projects\my-wiki\AGENTS.md -Pattern "git add"`
- Skill list current: `Get-ChildItem C:\Users\subha\.claude\skills -Directory | Select-Object -ExpandProperty Name`
- graphify still deviates from library frontmatter: `Get-Content C:\Users\subha\.claude\skills\graphify\SKILL.md -TotalCount 5`
