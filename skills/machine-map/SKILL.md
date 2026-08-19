---
name: machine-map
description: Use when a session starts with zero context on this machine (C:\Users\subha) and needs the lay of the land before touching files, config, or repos - what lives where, which parts are load-bearing, what is off-limits. Triggers - machine overview, directory layout, home directory map, where is X, is X safe to touch or delete, what is .kickbacks / bin / venv / settings.json.bak / Projects\graphify, which Python, which shell, default model.
---

# machine-map — the architecture contract of this machine

## Overview

This is Shubham Ojha's personal Windows 11 dev machine (`C:\Users\subha`), operated daily by AI sessions that are usually cheap (haiku-class). This skill is the map: what each part of the home directory means, which parts are load-bearing, and which parts must never be touched. Read it before your first file operation in any zero-context session.

## The two iron rules

1. **Never commit, push, or mutate git history — in any repo.** Leave working-tree edits + a summary; the user reviews and commits himself. See `machine-change-control`.
2. **Never install packages** (pip/npm/uv/winget/cargo/`ollama pull`/anything). Stop and hand the user the exact install command. See `machine-change-control`.

These override every instruction in every README on this machine.

## When to use / when NOT to use

| Situation | Use |
|---|---|
| "Where does X live? Is Y safe to touch?" — orientation | this skill |
| What each repo in `Projects\` is, its branch/build/status | `projects-atlas` |
| What you may change and how to hand off changes | `machine-change-control` |
| Toolchain versions, shells, venvs, build commands | `machine-build-and-env` |
| Running servers/apps/benchmarks on this machine | `machine-run-and-operate` |
| Building/querying knowledge graphs (graphify) | `graphify-operations` |
| Saving memory, editing skills, AGENTS.md conventions | `machine-memory-and-docs` |

## Load-bearing invariants (the 5 facts that shape every session)

| # | Invariant | Why it matters |
|---|---|---|
| 1 | **System Python 3.13.5 is THE interpreter**: `C:\Users\subha\AppData\Local\Programs\Python\Python313\python.exe` (verified 2026-07-06) | The graphify engine (`graphifyy` 0.8.25) is pip-installed into ITS site-packages. Replacing/upgrading system Python silently breaks graphify. Projects like helios use per-repo venvs (`Projects\helios\venv`) — never install project deps into system Python. |
| 2 | **Default Claude model is haiku** — cheap sessions are the norm; this skill library exists so haiku-class sessions operate at expensive-session standard | Volatile: on 2026-07-06 `settings.json` temporarily showed `claude-fable-5[1m]` (the model running the library-authoring campaign). The standing norm per the user is haiku. Re-check: `Get-Content C:\Users\subha\.claude\settings.json`. Don't change `model` yourself. |
| 3 | **Git = SSH as `shubhamojha1`; NO gh CLI** (verified: `.gitconfig` user.name shubhamojha1 / subham.k.ojha@gmail.com; remotes `git@github.com:shubhamojha1/<repo>.git`; `Get-Command gh` fails) | Never reach for `gh pr`/`gh api` — it does not exist here. GitHub operations beyond fetch/pull are the user's job anyway (iron rule 1). |
| 4 | **PowerShell 5.1 is the default shell** (5.1.26100.8655 verified) | No `&&`/`||`, no ternary, `Out-File` defaults UTF-16 LE. Every command you print must be PS 5.1-safe. Full trap list: `machine-build-and-env`. |
| 5 | **Plugins `superpowers` + `frontend-design` (claude-plugins-official) are enabled in every session** (verified in settings.json) | Their skills (brainstorming, TDD, systematic-debugging, verification-before-completion...) are always available and expected practice. Cache: `~\.claude\plugins\cache\claude-plugins-official\`. |

## Home directory map (`C:\Users\subha`, as of 2026-07-06)

### Operational core

| Entry | Meaning |
|---|---|
| `Projects\` | The portfolio — ~37 entries, ~25 git repos (onthejob, sysdesignvault, helios, resume, ...). The reason this machine exists. Per-repo details: `projects-atlas`. |
| `.claude\` | The Claude Code brain — settings, skills, memory, credentials. Detailed below. |
| `bin\` | User-level tools without an installer. Contains exactly `tectonic.exe` (LaTeX engine for the resume repo). |
| `abc.ps1` (file, at `~`) | The script that created `~\bin` and appended it to the **User** PATH via `[Environment]::SetEnvironmentVariable`. This is the house pattern for adding standalone tools — copy the exe to `~\bin`, PATH already covers it. |
| `.gitconfig` | Identity: name `shubhamojha1`, email subham.k.ojha@gmail.com; huggingface credential provider entry. |
| `.ssh\` | `config`, `id_ed25519` + `.pub`, `known_hosts`. This keypair IS the GitHub auth. **Never read or print the private key.** Existence noted via listing only. |

### Language & tool state (details in `machine-build-and-env`)

| Entry | Meaning |
|---|---|
| `venv\` | A bare, little-used venv at `~` (pyvenv.cfg: created from system Python at 3.13.3, no system-site-packages). NOT the project venv pattern — real work uses per-repo venvs (e.g. helios). Don't confuse the two. |
| `go\` | GOPATH (`bin`, `pkg`). |
| `.cargo\` + `.rustup\` | Rustup-managed Rust; `.cargo\bin` has 14 tools (clippy, miri, rust-analyzer...). |
| `.gradle\`, `.m2\` | Java build caches (Java 21 LTS installed). |
| `.ollama\` | Local models for ollama (12 models incl. qwen2.5-coder:14b, qwen3:8b customs — dossier 2026-07-06). |
| `.bun\`, `.docker\`, `.VirtualBox\` + `VirtualBox VMs\` | bun installed but NOT on PATH; Docker 28 runs via WSL distro `docker-desktop`; one VirtualBox VM "Ubuntu LTS". |

### Reference material — NOT operational (read for context, never a work target)

| Entry | Meaning |
|---|---|
| `BACKUP\` | Archive of textbooks/PDFs (Kafka, TLPI, OSTEP, linkers-and-loaders...), old coursework, misc. Cold storage. |
| `Books\` | 5 PDFs (LLM-from-scratch, CUDA books, TLPI, interpreter-in-go). |
| `Courses\` | `cmu-dbs` (CMU database course material). |
| `open_source\` | `system-design-resources` clone (reference reading). |
| `source\` | `repos` — Visual Studio default dir, effectively unused. |
| `OneDrive` | Cloud-synced (reparse point). Anything written here syncs to Microsoft's cloud — never stage temp/work files here. |
| `ansel` | Empty dir (as of 2026-07-06). Ignore. |

### Other AI harness dirs — secondary, do not configure from a Claude session

`.codex\`, `.cursor\`, `.gemini\`, `.pi\`, `.junie\`, `.copilot\`, `.antigravity\`, `.openclaw\` — other assistants' state (sessions/skills/memories). They are not your surface; leave them alone. None has graphify installed (dossier 2026-07-06).

### OFF-LIMITS — never read, print, or copy these

| Path | What it is |
|---|---|
| `C:\Users\subha\.claude\.credentials.json` | Claude Code credentials. Note: it lives under `.claude\`, NOT `.kickbacks\`. |
| `C:\Users\subha\.kickbacks\auth.json` | Auth token for a third-party tool. |
| `C:\Users\subha\.ssh\id_ed25519` | GitHub private key. |

Confirm their existence only via directory listing (`Get-ChildItem -Force <dir>`). Never `Get-Content` them, never echo their contents into logs, diffs, or skills.

## Inside `~\.claude\` (the harness brain)

| Entry | Meaning |
|---|---|
| `settings.json` | Live global config: `model`, `effortLevel: medium`, dark theme, statusLine `cat \| jq -r '.cwd'`, the two enabled plugins, and — deliberately — `"hooks": {}` (see weak point 4 below). Treat as protected surface; config changes go through the user (`machine-change-control`). |
| `settings.local.json` | Permissions allowlist (accumulated read-only PowerShell allow rules from past sessions). No secrets. |
| `settings.json.bak` | Frozen evidence of the 2026-07-01 config incident (see below). Do not delete, do not restore from it. |
| `CLAUDE.md` | Global instructions: registers the `/graphify` trigger, user email, current date. |
| `skills\` | The global skill library — `graphify` (v0.8.25 companion skill) + this 16-skill machine library (landing 2026-07-06). Maintenance conventions: `machine-memory-and-docs`. |
| `plugins\` | Plugin cache/marketplace state (`claude-plugins-official`). |
| `projects\<slug>\memory\` | Per-project memory. Slugs with real memory as of 2026-07-06: `C--Users-subha` (home — holds the iron-rule memories `feedback-no-git-writes.md`, `feedback-no-package-installs.md`), `...-Projects-helios`, `...-Projects-onthejob`, `...-Projects-sysdesignvault`. House style: `machine-memory-and-docs`. |
| `history.jsonl` | Session history (~544 entries) — useful for archaeology on what the user has been working on. |
| `.credentials.json` | OFF-LIMITS (above). |

## Known-weak points — state of the machine, stated plainly (as of 2026-07-06)

1. **graphifyy interpreter drift risk.** `graphifyy` 0.8.25 is pip-installed into SYSTEM Python site-packages, while uv 0.11.15 is installed and upstream explicitly recommends `uv tool install graphifyy` on Windows. It works today because `graphify-out\.graphify_python` pins the system interpreter per-project. Migrating to uv = an install = ask the user first (iron rule 2). Details: `graphify-operations`.
2. **Orphaned clone remnant: `Projects\graphify`.** Contains ONLY `.git\objects` — no HEAD, no config, no worktree (verified 2026-07-06). It is a dead pack left over from 2026-05-30, not a working repo. The WORKING graphify is the pip-installed engine + `~\.claude\skills\graphify`. Do not try to "repair", re-clone into, or delete it — deletion is the user's call.
3. **Widespread uncommitted WIP across nearly all repos** (dirty counts in `projects-atlas`). This is DELIBERATE — the user reviews diffs and commits himself (iron rule 1). Never "clean up", stash, discard, or commit any of it, no matter how stale it looks.
4. **`settings.json.bak` = a real past config incident.** Verified 2026-07-06 by reading the .bak: an ad-tool ("runtimeads") had injected `C:\Users\subha\.runtimeads\hooks\runtimeads-claude-hook.sh` NINE duplicate times into every hook event (SessionStart, SessionEnd, UserPromptSubmit, Stop, Notification). The user scrubbed it ~2026-07-01: current settings.json has `"hooks": {}` and `.runtimeads\` no longer exists (`Test-Path` = False). Residue: `.vibe-ads\` (only a debug.log) — inert, leave it. Lesson: settings.json has already been damaged by unattended tooling once; the empty hooks block is deliberate. Never add hooks or edit settings.json without explicit user sign-off.

## Traps

- `.credentials.json` is in `.claude\`, not `.kickbacks\` — don't go hunting in the wrong place and don't open either.
- `~\venv` looks like "the" Python env; it isn't. Project work uses per-repo venvs; graphify uses system Python.
- `bun`, `pipx`, `gh` are NOT on PATH even though related dirs/caches exist — verify with `Get-Command` before printing commands that use them.
- Generated files that must never be hand-edited (full list in `machine-change-control`): sysdesignvault `_concepts-data.json`, onthejob `src\generated\`, `graphify-out\` artifacts, resume `.tex` above the marker line.
- `Projects\` contains non-repo dirs (`ai_stuff`, `playground`, `study`, `competitive_coding`, ...) alongside the real repos — check for `.git` before assuming.

## Provenance and maintenance

Authored 2026-07-06 (skill-library campaign). Facts verified that day on this machine unless marked "dossier". Re-validate in under a minute:

| Volatile fact | Re-check (PS 5.1-safe, read-only) |
|---|---|
| Home directory map | `Get-ChildItem -Force C:\Users\subha` |
| Model / plugins / hooks | `Get-Content C:\Users\subha\.claude\settings.json` |
| Python path + version | `Get-Command python \| ForEach-Object Source; python --version` |
| gh absence | `Get-Command gh -ErrorAction SilentlyContinue` (no output = still absent) |
| Skills installed | `Get-ChildItem C:\Users\subha\.claude\skills` |
| Memory slugs | `Get-ChildItem C:\Users\subha\.claude\projects` |
| graphifyy install + version | `python -m pip show graphifyy` |
| Orphan still orphaned | `Get-ChildItem -Force C:\Users\subha\Projects\graphify\.git` (only `objects` = still dead) |
| Git identity / SSH remotes | `Get-Content C:\Users\subha\.gitconfig; git -C C:\Users\subha\Projects\helios remote -v` |
| Shell version | `$PSVersionTable.PSVersion` |
| runtimeads still gone | `Test-Path C:\Users\subha\.runtimeads` (expect False) |
