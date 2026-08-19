---
name: machine-debugging-playbook
description: Use when something on this machine errors, hangs, or behaves unexpectedly — ModuleNotFoundError, PowerShell parser or encoding errors, Next.js/React APIs that don't match training data, Helmet provider errors, tectonic failures, docker/WSL unreachable, ollama issues, broken scrolling, command not found — or when a session should measure machine state instead of guessing. Triggers - error, exception, traceback, hang, triage, health check, which python, NativeCommandError, ExecutionPolicy, ANSI, CRLF, long path.
---

# Machine Debugging Playbook — triage before theory

Symptom → cause → discriminating check → fix, for THIS machine's recurring failure modes.
Discipline first: **reproduce → read the actual error text → form ONE hypothesis that
explains ALL observations → run the discriminating check → then fix.** (Full method:
`research-methodology-and-frontier`. Historical incidents so you don't re-debug settled
battles: `machine-failure-archaeology`.)

## Measure first — the health check (shipped with this skill, tested 2026-07-06)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\subha\.claude\skills\machine-debugging-playbook\scripts\health-check.ps1"
```
Read-only. Prints: tool versions vs expected, the Python-interpreter inventory, graphifyy
engine-vs-skill version drift, PATH audit, the runtimeads-hook safety check, dirty-repo
report, disk. Run it before any environment theory. (Without `-NoProfile` you may see a
harmless `vswhere.exe is not recognized` line — that's the user's PowerShell profile, not
the script.)

## The triage table

| Symptom | Likely cause on THIS machine | Discriminating check | Fix |
|---|---|---|---|
| `ModuleNotFoundError` for a package that "should" exist | Wrong interpreter — 4+ Pythons here: system 3.13.5, `~\venv`, repo venvs (helios\venv, joust\.venv, parameter-golf\venv), plus whatever's ACTIVE | `python -c "import sys; print(sys.executable)"`; for graphify also read `graphify-out\.graphify_python` | Run with the right interpreter (activate the repo venv or call the pinned path). Missing package = ASK USER to install (iron rule) |
| `ModuleNotFoundError: No module named 'graphify'` specifically | The pip-on-Windows setup upstream warns about; pin drifted | Compare `(Get-Command python).Source` vs `Get-Content graphify-out\.graphify_python` | See `graphify-operations` §Install reality |
| PowerShell: `The token '&&' is not a valid statement separator` | PS 5.1 (default shell) has no `&&`/`||`/ternary | `$PSVersionTable.PSVersion` → 5.1 | `A; if ($?) { B }` — or run via Bash tool for POSIX syntax |
| A file another tool reads comes out garbled/UTF-16 | PS 5.1 `Out-File`/`>` default UTF-16 LE | `Format-Hex file \| Select -First 1` (FF FE BOM) | Always `-Encoding utf8` on Out-File/Set-Content |
| Native command "fails" though it worked (NativeCommandError) | PS 5.1 wraps native stderr when redirected with `2>&1` | Did the command actually produce its output? | Don't redirect native stderr in PS; or `cmd /c "tool args 2>&1"` (the health-check does this for `java -version`) |
| `.ps1 cannot be loaded... execution policy` | Default policy blocks scripts | `Get-ExecutionPolicy` | Invoke with `powershell -NoProfile -ExecutionPolicy Bypass -File <script>` (no system-wide change) |
| Next.js/React API "doesn't exist" though you're sure it does | sysdesignvault runs Next 16.2.1 + React 19 — POST-training-data | which repo? `Test-Path node_modules\next` | Read `node_modules\next\dist\docs\` first (repo AGENTS.md doctrine) — `sysdesignvault-platform` |
| `Cannot read ... HelmetProvider` / head tags missing in onthejob | `<Helmet>` imported from react-helmet-async instead of vite-react-ssg's `<Head>` | grep the diff for `react-helmet-async` | Import `<Head>` from `vite-react-ssg` — `onthejob-operations` §Traps |
| tectonic compile fails (resume) | Unescaped LaTeX specials `% & _ # $ ~ ^` in edited prose | Read `resume_faangpath.log` next to the .tex | Escape per `resume-and-career-ops` rule 4; recompile until clean |
| `docker: error during connect` | Docker Desktop not running (docker runs via WSL distro `docker-desktop`) | `wsl -l -v` → is docker-desktop Running? | Start Docker Desktop (user-visible app) and wait for it; don't fiddle with WSL config |
| ollama errors / model unbearably slow | Model not pulled, or too big for RAM/VRAM (gpt-oss:20b = 13GB) | `ollama list` (custom 16k/32k qwen tags are local creations); `ollama ps` | Use a smaller model; pulls = ask user |
| PowerShell scrolling breaks after a graphify run | graspologic ANSI output (legacy console) | Did graphify just run? | Use Windows Terminal; close/reopen console — `graphify-operations` |
| `gh`/`pipx`/`bun` not recognized | Genuinely not installed (verified 2026-07-06) | `Get-Command gh` → nothing | Don't fake it with curl hacks; if needed, ask user to install |
| A tool installed a second ago isn't on PATH | User-scope PATH edits don't reach the current session | `[Environment]::GetEnvironmentVariable('Path','User')` contains it? | New terminal, or add to `$env:Path` for this session only |
| git: files "modified" with no content change | CRLF/LF autocrlf noise, common on Windows checkouts | `git -C <repo> diff` shows whole-file or `^M` changes | Report to user; do NOT "fix" line endings repo-wide on your own |
| Path-too-long errors (deep node_modules) | Win32 260-char limit without long-path opt-in | error mentions path >260 chars | Work from a shorter cwd; enabling LongPathsEnabled is a registry change = user decision |
| Something intercepts every prompt/tool call; weird hooks | The 2026-07-01 runtimeads infestation pattern | health-check's safety section (hooks count + `.runtimeads` existence) | If it's back: STOP, show the user — `machine-failure-archaeology` Entry 1 |
| A server "should" be up but requests fail | dev server not actually running | `netstat -ano \| Select-String ':<port>'` (onthejob preview 4173, next dev 3000, helios 8080) | Start it per `machine-run-and-operate`; never assume |

## Escalation order when the table misses
1. Health-check script (above) — environment baseline.
2. `machine-failure-archaeology` — is this a settled battle?
3. The owning repo's skill (`projects-atlas` routes you) — project-specific traps live there.
4. Systematic debugging (superpowers plugin) — hypothesis → discriminating experiment;
   write findings into project memory if novel (`machine-memory-and-docs`).

## When NOT to use
Project-domain bugs with an owning skill (helios perf → `helios-continuous-batching-campaign`;
graph quality → `graphify-operations`). Recreating the environment → `machine-build-and-env`.

## Provenance and maintenance
Authored 2026-07-06. Every row's "check" command executed or sourced from a verified
artifact that day; the health-check script was test-run clean (tool versions, 4 interpreters
found, graphifyy 0.8.25 = skill 0.8.25, hooks 0, ~\bin on PATH, C: 347GB free).
Re-verify: run the health-check script — it IS the re-verification. If a new recurring
failure mode costs a session >15 minutes, add a row with its discriminating check.
