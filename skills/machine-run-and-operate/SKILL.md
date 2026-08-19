---
name: machine-run-and-operate
description: Use when starting an AI session on this machine (Shubham's Windows 11 box), deciding which project skill and memory to load from the cwd, choosing model/effort, running or health-checking dev servers (npm run dev, next dev, helios serve, ollama, docker), deciding where outputs go (scratchpad, out/, graphify-out/, src/generated), or wrapping up with an end-of-task handover. Keywords - session start, which repo am I in, MEMORY.md, port 5173 4173 3000 8080, netstat, background server, /model, /compact, commit message, OneDrive.
---

# machine-run-and-operate — the day-to-day session playbook

## Overview

This is the operating manual for any AI session on this machine: orient, load the right
project skill and memory, run things safely, put outputs where they belong, and hand work
back to the user cleanly. It is machine knowledge, not process discipline — the superpowers
plugin covers process (see "Plugin reality" below). Two iron rules govern everything:
**never commit/push/mutate git history, never install packages** — prepare the change and
hand the exact command to the user (full rules: see `machine-change-control`).

## When to use / when NOT to use

- USE at session start (orientation), before starting any server, before writing any file
  outside a repo, and at task wrap-up.
- NOT for project-specific work — load the project skill instead (table below).
- NOT for memory/skill-file *authoring* conventions — see `machine-memory-and-docs`.
- NOT for git/install policy details — see `machine-change-control` (one-liners restated here).

## Quick reference (verified 2026-07-06)

| Thing | Value |
|---|---|
| Home / shell | `C:\Users\subha`, PowerShell 5.1 default (NO `&&`/`||`; `Out-File` defaults UTF-16 LE — use `-Encoding utf8`) |
| Settings | `~/.claude/settings.json`: `effortLevel: medium`, plugins `frontend-design` + `superpowers`, no hooks, `agentPushNotifEnabled: true` |
| Model norm | haiku is the user's standing default; field is volatile — read settings.json, don't assume |
| Durable state | ONLY `~/.claude/skills/` + `~/.claude/projects/<slug>/memory/` + uncommitted diffs. Everything else dies |
| Session temp | scratchpad dir from your system prompt (`...\Temp\claude\<hash>\<session>\scratchpad`) — dies with the session |
| Statusline | `cat \| jq -r '.cwd'` — shows cwd, not model. CAVEAT: jq not found on PATH in PS or Git Bash (2026-07-06); a blank statusline is likely that |
| Time tracking | Wakatime runs ambiently (`~/.wakatime/`, `~/.wakatime.cfg` exist) — ignore it, never kill `wakatime-cli` processes |
| OneDrive | `C:\Users\subha\OneDrive\` is cloud-synced and INCLUDES `Desktop` — never stage large/temp data there |

## 1. Session start ritual

1. **Locate yourself.** Your cwd is in the environment context. If it is under
   `C:\Users\subha\Projects\<name>`, that repo is your context. For nested dirs:
   `git rev-parse --show-toplevel`.
2. **Load the matching project skill** (invoke via the Skill tool before acting):

   | cwd / context | Load |
   |---|---|
   | `Projects\onthejob` | `onthejob-operations` |
   | `Projects\sysdesignvault` | `sysdesignvault-platform` |
   | `Projects\helios` | `helios-continuous-batching-campaign` |
   | `Projects\resume` | `resume-and-career-ops` |
   | graph questions / a `graphify-out\` dir exists | `graphify-operations` (user trigger `/graphify` loads the `graphify` skill itself) |
   | any other repo, or unsure which repo matters | `projects-atlas` |
   | home dir / machine-level task | this skill + `machine-change-control` |

   The library was authored 2026-07-06 by parallel agents; if a named sibling is missing,
   list what exists: `Get-ChildItem $env:USERPROFILE\.claude\skills`
3. **Check project memory.** Slug = absolute path with `:`→`-` and `\`→`-`:

   ```powershell
   $slug = (Get-Location).Path -replace ':', '-' -replace '\\', '-'
   $mem = "$env:USERPROFILE\.claude\projects\$slug\memory\MEMORY.md"
   if (Test-Path $mem) { Get-Content $mem } else { "no memory for $slug" }
   ```

   Memory exists (2026-07-06) for: `C--Users-subha` (home), `...-Projects-helios`,
   `...-Projects-onthejob`, `...-Projects-sysdesignvault`. MEMORY.md is the index; follow
   its links. Writing/updating memory: see `machine-memory-and-docs`.
4. **Check for a matching superpowers process skill** before acting (see "Plugin reality").

## 2. Model & effort policy

- The user's standing default is **haiku** with `effortLevel: medium` (settings.json;
  dossier 2026-07-06). The `model` field is volatile — it read `claude-fable-5[1m]` later
  that same day during library authoring. Verify, never assume:
  `Get-Content $env:USERPROFILE\.claude\settings.json`
- **haiku/sonnet + these skills is fine for runbook work**: adding an incident, tailoring a
  resume, running builds/checks, content edits, graph queries. That is the whole point of
  this library.
- **Recommend the user switch (`/model`) for architecture-level or high-risk work**:
  onthejob taxonomy changes, helios continuous-batching implementation, resume structure
  surgery, schema/data-model design, anything security-sensitive. Say plainly: "this is
  architecture-level; consider `/model` to a stronger model before I proceed." Never
  silently assume high capability — a wrong confident answer costs more than the ask.
- **Long sessions:** suggest `/compact` when context is bloated with stale tool output
  (the user already uses it). Do this BEFORE quality degrades, not after.

## 3. Where outputs belong

| Output | Destination | Notes |
|---|---|---|
| Temp files, intermediate data, scratch scripts | session scratchpad (path in your system prompt) | Dies with the session. NEVER reference scratchpad paths from durable files (skills, memory, repo files) |
| Tailored resumes | `Projects\resume\out\<company>-<role>\` | resume.pdf + tex copy + rationale.md (see `resume-and-career-ops`) |
| Knowledge graphs | `<repo>\graphify-out\` | Pipeline-produced; never hand-edit (see `graphify-operations`) |
| onthejob generated index | `Projects\onthejob\src\generated\` | Gitignored; rebuilt by predev/prebuild (`tsx scripts/build-index.ts`). NEVER hand-edit |
| sysdesignvault concepts data | `..._concepts-data.json` | NEVER hand-edit; write MDX then `node scripts/build-concepts.js` |
| Durable knowledge for future sessions | `~/.claude/skills/` or `~/.claude/projects/<slug>/memory/` | The ONLY session-to-session state. See `machine-memory-and-docs` |
| Work product for the user | uncommitted working-tree edits in the repo | He reviews and commits himself |

Trap: `C:\Users\subha\OneDrive\` (which includes the redirected `Desktop`) is cloud-synced —
staging build output or large temp data there burns sync bandwidth and pollutes his cloud
storage. Repos live in `C:\Users\subha\Projects\` (not under OneDrive); keep it that way.

## 4. Long-running processes: start in background, then PROVE they're up

Never assume a server started. Start it, wait a few seconds, then check the port or hit a
health endpoint. Use your shell tool's `run_in_background` parameter — PowerShell 5.1 has
no trailing-`&` job syntax, and a foreground server call blocks the session.

Known services and their ports (ports verified from configs/READMEs 2026-07-06; servers
NOT started during authoring):

| Service | Start (from repo root, in background) | Port | Up-check |
|---|---|---|---|
| onthejob dev | `npm run dev` (predev builds index + OG cards first — takes a bit) | 5173 (Vite default; `vite.config.ts` sets no override) | port check below |
| onthejob preview | `npm run build` then `npm run preview` | 4173 (per README) | port check |
| sysdesignvault dev | `npm run dev` (`next dev`) | 3000 (Next default; no `-p` in script) | port check |
| helios | `helios serve` (needs the repo venv: `.\venv\Scripts\Activate.ps1` first) | 127.0.0.1:8080 | `/health` check below |
| ollama | usually ALREADY running as a desktop app — check before starting `ollama serve` | 11434 (documented default — unverified locally) | `ollama ps` (also proves server is up) |
| Docker Desktop | GUI app (engine runs in WSL distro `docker-desktop`) — if down, ask the user to launch it | n/a | `docker info` fails if engine down; `docker version` shows client regardless |

Check commands (PS 5.1-safe):

```powershell
# Is anything listening on the port?
netstat -ano | Select-String ':5173.*LISTENING'

# HTTP health check (helios example; -UseBasicParsing required on PS 5.1)
try { (Invoke-WebRequest -Uri 'http://127.0.0.1:8080/health' -UseBasicParsing -TimeoutSec 5).StatusCode }
catch { "DOWN: $($_.Exception.Message)" }
```

For the Vite/Next servers, swap the port into the netstat line or GET `http://localhost:<port>/`.
A dev server can take 10-30 s to bind (onthejob's predev runs two tsx scripts first) — poll
the check, don't declare failure on the first miss.

Stopping: kill only processes YOU started this session (`Stop-Process -Id <pid> -Confirm:$false`
on the PID you observed, or the harness's kill-shell affordance for background shells). Never
kill ollama, Docker, or wakatime processes you did not start — they are the user's.

## 5. Plugin reality: superpowers is active

`enabledPlugins` (verified): `frontend-design@claude-plugins-official`,
`superpowers@claude-plugins-official`. No hooks configured. Sessions on this machine are
expected to invoke the matching process skill BEFORE acting:

| Situation | Invoke first |
|---|---|
| Creating features / components / new behavior | `superpowers:brainstorming` |
| Any bug, test failure, unexpected behavior | `superpowers:systematic-debugging` |
| About to claim "done" / "fixed" / "passing" | `superpowers:verification-before-completion` |
| Building or reshaping UI | `frontend-design:frontend-design` |

This skill library and superpowers are complementary, not competing: this library carries
MACHINE and PROJECT knowledge (paths, ports, doctrines, traps); superpowers carries PROCESS
discipline (how to brainstorm, debug, verify). Load both kinds when both apply.

## 6. End-of-task handover protocol

The change-control rules, operationalized. Every task that touched files ends with this
(full policy: `machine-change-control`):

1. **Do NOT commit, push, or install. Ever.** Leave edits uncommitted in the working tree.
   The user reviews diffs and commits himself. Expect repos to already contain unrelated
   uncommitted WIP — never "clean it up", revert it, or fold it into your summary as yours.
2. **List every file you changed** — absolute paths, one line each on what/why.
3. **Point at what to review first** — the riskiest or most judgment-laden diff, and any
   place you were unsure.
4. **Offer a suggested commit message** the USER may use (subject + short body). Label it
   "suggested"; he commits himself.
5. **Batch install requests at the END**, exact commands, one block — e.g.
   "blocked on: `npm install <pkg>` (run it yourself, then re-invoke me)". Never scatter
   install asks mid-task and never run them (iron rule 2).
6. **Report verification evidence**, not assertions: what command you ran, what it output
   (`superpowers:verification-before-completion`). "The build passes" requires having seen
   the build pass.
7. **Offer durable-knowledge capture** if the session learned something future sessions
   need: a memory entry or skill edit, per `machine-memory-and-docs`. Ask; don't silently
   write doctrine.

Push notifications are enabled (`agentPushNotifEnabled: true`), so long background work is
fine — the user gets pinged when you finish. Prefer finishing with a complete handover over
streaming partial updates.

## 7. Traps

- **Assuming the server is up** because the start command returned. Vite/Next print a URL
  only after binding; helios needs its venv. Always run the port/health check.
- **Assuming you're a capable model.** Default is haiku. Check settings.json; recommend
  `/model` for architecture work instead of soldiering on.
- **Writing temp files into the repo or OneDrive** instead of the scratchpad. Repo = only
  intended deliverables; OneDrive = cloud-synced.
- **Referencing scratchpad paths in durable files.** The scratchpad dies with the session;
  embed content instead of linking it.
- **Hand-editing generated files** (`src\generated\`, `_concepts-data.json`, `graphify-out\`,
  resume tex above the marker). Regenerate via the documented command instead.
- **PS 5.1 syntax burns:** `&&`/`||` are parser errors; `Out-File` writes UTF-16 LE by
  default (breaks tools reading the file — use `-Encoding utf8`); native-exe `2>&1`
  wraps stderr lines in error records.
- **Blank statusline confusion:** the configured statusline pipes through `jq`, which is not
  on PATH (2026-07-06). If the user wants it fixed, installing jq is HIS command to run
  (iron rule 2).
- **Committing, pushing, or installing "to be helpful".** Never. See `machine-change-control`.

## Provenance and maintenance

Authored 2026-07-06 from the machine dossier plus direct read-only verification the same
day. Servers were NOT started during authoring; check commands are documented forms, port
sources are configs/READMEs. Re-verify volatile facts:

| Fact | Re-check (read-only) |
|---|---|
| Model / effort / plugins / hooks / notif | `Get-Content $env:USERPROFILE\.claude\settings.json` |
| Skill library contents | `Get-ChildItem $env:USERPROFILE\.claude\skills` |
| Memory dirs present | `Get-ChildItem $env:USERPROFILE\.claude\projects\*\memory\MEMORY.md` |
| onthejob ports/scripts | `Get-Content C:\Users\subha\Projects\onthejob\package.json` and `vite.config.ts` (no port override = 5173/4173) |
| sysdesignvault port | `Get-Content C:\Users\subha\Projects\sysdesignvault\package.json` (`next dev`, no `-p` = 3000) |
| helios port/endpoints | `Get-Content C:\Users\subha\Projects\helios\README.md` (127.0.0.1:8080, `/health`) |
| Wakatime present | `Test-Path $env:USERPROFILE\.wakatime.cfg` |
| jq still missing | `Get-Command jq -ErrorAction SilentlyContinue` (empty = missing) |
| ollama/docker binaries | `Get-Command ollama, docker` |
| OneDrive Desktop redirect | `Test-Path C:\Users\subha\OneDrive\Desktop` |

Unverified-this-pass facts carried from the dossier (2026-07-06): Claude Code 2.1.201;
ollama 0.17.1 and its model list; docker 28.0.4 via WSL; ollama port 11434 (upstream
documented default); `/model` and `/compact` usage frequency from history.jsonl.
