---
name: machine-build-and-env
description: Use when recreating this machine's dev environment (new machine, reinstall, disaster recovery), auditing what's installed and at which version, fixing PATH problems, setting up a repo's environment (venv, npm), or answering "is X installed here". Triggers - install, reinstall, winget, PATH, environment setup, git config, SSH keys, toolchain versions, tectonic, uv, ollama models, new machine, bootstrap.
---

# Machine Build & Environment — recreate and audit this box

How `C:\Users\subha` (Windows 11 Home, build 10.0.26200) is provisioned, and the ordered
checklist to rebuild it. **Iron rule 2 applies throughout: sessions NEVER install anything.**
Every install line below is a command FOR THE USER TO RUN; the session's job is the correct
checklist, the verification afterward, and the batching of install requests at handover
(`machine-change-control`).

## Installed toolchain (verified 2026-07-06 — versions drift, re-verify before quoting)

| Tool | Version | Location / note |
|---|---|---|
| git | 2.49.0.windows.1 | SSH auth to GitHub; **no gh CLI** |
| Python | 3.13.5 | `C:\Users\subha\AppData\Local\Programs\Python\Python313\` — THE system interpreter (graphifyy lives here) |
| uv | 0.11.15 | tool dir `%APPDATA%\uv\tools` (empty of graphifyy — see graphify-operations) |
| node / npm | 22.17.0 / 10.9.2 | **no bun on PATH** (`~\.bun` exists but inactive), **no pipx** |
| go | 1.24.3 | GOPATH `~\go` |
| rustup/cargo/rustc | 1.94.1 | `~\.cargo\bin` (clippy, miri, rust-analyzer, rustfmt) |
| java | 21.0.9 LTS | `~\.gradle`, `~\.m2` exist |
| docker | 28.0.4 | Docker Desktop via WSL distro `docker-desktop` (the only WSL distro; there is also a VirtualBox VM "Ubuntu LTS") |
| ollama | 0.17.1 | 12 models — see list below |
| VS Code | 1.127.0 | `code` on PATH |
| claude | 2.1.201 | Claude Code CLI |
| tectonic | binary at `C:\Users\subha\bin\tectonic.exe` | LaTeX engine for resume; ~\bin is on User PATH |

Ollama models (as of 2026-07-06): qwen2.5-coder:14b (+`-16k` and `-instruct-q4_K_M` variants),
qwen3:8b (+`-16k`, `-32k` custom context variants), gpt-oss:20b, deepseek-r1:7b, mistral:7b,
llama3.2:latest, and cloud passthroughs kimi-k2.6:cloud, minimax-m2.5:cloud.
The custom `-16k`/`-32k` tags are locally created Modelfile variants — if absent after a
rebuild, they must be recreated (`ollama show qwen3:8b-16k --modelfile` on the old machine
captures the recipe, if still available).

## Identity & access
- git config (verified from `~\.gitconfig`): `user.name = shubhamojha1`,
  `user.email = subham.k.ojha@gmail.com`, plus a credential helper entry for huggingface.co.
- SSH keys in `~\.ssh` (never read/print private keys). Remotes are `git@github.com:...`.
  Connectivity test the USER can run: `ssh -T git@github.com`.
- Other credentials on disk (existence only, never open): `~\.claude\.credentials.json`,
  `~\.kickbacks\auth.json`, `~\.gemini\oauth_creds.json`.

## Rebuild-from-scratch checklist (ordered; INSTALLS = USER-RUN)

1. **Package manager + Python + uv** — user: `winget install Python.Python.3.13 astral-sh.uv Git.Git OpenJS.NodeJS.LTS GoLang.Go Rustlang.Rustup Docker.DockerDesktop Ollama.Ollama Microsoft.VisualStudioCode` (adjust to taste; VS Code + Docker Desktop have GUIs).
   Session verifies each: `git --version; python --version; uv --version; node --version; go version; cargo --version; docker --version; ollama --version; code --version`.
2. **Claude Code** — user installs per docs; then restore `~\.claude\` config:
   `settings.json` (default model haiku, plugins frontend-design + superpowers), `CLAUDE.md`,
   and **this skill library** (`~\.claude\skills\` — copying the directory restores all
   machine knowledge; it is the disaster-recovery payload). Plugins reinstall via the
   claude-plugins-official marketplace.
3. **PATH additions** — the house pattern (from `~\abc.ps1`, which did this for tectonic):
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path","User") + ";$env:USERPROFILE\bin", "User")
   ```
   Put single-binary tools (tectonic.exe) in `~\bin`. New terminals only.
4. **git identity + SSH** — user: set user.name/user.email as above; generate/restore SSH
   key; `ssh -T git@github.com` must greet shubhamojha1.
5. **graphifyy** — decision point (see `graphify-operations`): recommended fresh path is
   `uv tool install graphifyy` (upstream guidance) rather than reproducing today's
   pip-into-system state; then `graphify install --platform windows`.
6. **Repos** — user clones (SSH): onthejob, sysdesignvault, resume, helios, arachne,
   personal-site, my-wiki, and the rest per `projects-atlas`. Externals: parameter-golf
   (openai org), claw-code (instructkr), leetcode-company-wise-problems (liquidslr),
   TutionProject (Oblivious19).
7. **Per-repo env** (installs user-run):
   - helios: `python -m venv venv` → `.\venv\Scripts\activate` → `pip install -r requirements.txt` → `pip install -e .` (provides the `helios` CLI); model GGUF/HF downloads per its README.
   - node repos (onthejob, sysdesignvault, arachne, personal-site): `npm install` in each.
   - resume: nothing beyond tectonic on PATH.
8. **Ollama models** — user: `ollama pull` the list above + recreate custom-context variants.
9. **Verification sweep** — session runs the health-check script
   (`machine-debugging-playbook\scripts\health-check.ps1`) and reports the table.

## Known environment traps (details in machine-debugging-playbook)
- Multiple Pythons: system 3.13.5 vs per-repo venvs vs `~\venv` (a bare, little-used
  3.13.3 venv) — always print `sys.executable` before blaming a missing package.
- PowerShell 5.1 is the default shell: no `&&`, UTF-16 Out-File default, PATH changes need
  a new terminal (User-scope PATH edits don't affect the current session).
- OneDrive redirects Desktop — don't stage build artifacts there.
- pip-vs-uv graphifyy split (works today via the single system Python; fragile by design).

## When NOT to use
Day-to-day session mechanics → `machine-run-and-operate`. Diagnosing a broken env →
`machine-debugging-playbook`. What a repo IS → `projects-atlas`.

## Provenance and maintenance
Authored 2026-07-06 from live `--version` calls, `~\.gitconfig`, `~\abc.ps1`, `ollama list`,
directory listings, and `pyvenv.cfg` of `~\venv`. Winget package IDs are the standard ones
but were NOT executed (no installs) — user should confirm IDs at install time
(`winget search <name>`). Re-verify the whole table in one shot:
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\subha\.claude\skills\machine-debugging-playbook\scripts\health-check.ps1"
```
or individually: `git --version`, `python -c "import sys; print(sys.version, sys.executable)"`,
`uv --version`, `node --version`, `ollama list`, `Get-Command tectonic`.
