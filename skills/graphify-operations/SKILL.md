---
name: graphify-operations
description: Use when running, debugging, upgrading, or judging output from graphify on this machine — /graphify runs, graphify-out artifacts, graph quality problems (junk god nodes, confidence collapse, zero token counts), ModuleNotFoundError for graphify, version drift, or choosing whether a graph is worth building. Triggers - graphify, graphifyy, graph.json, GRAPH_REPORT.md, .graphify_python, knowledge graph, god nodes, EXTRACTED INFERRED AMBIGUOUS, uv tool install, pip mismatch.
---

# Graphify Operations — running the knowledge-graph tool on THIS machine

graphify turns a folder (code/docs/papers/images) into a queryable knowledge graph
(`graphify-out\graph.json` + `GRAPH_REPORT.md` + `graph.html`). Upstream:
github.com/safishamsi/graphify, PyPI package **`graphifyy`** (double-y), CLI `graphify`.

**Boundary:** the VENDOR skill at `~\.claude\skills\graphify\` (1,435-line pipeline runbook,
`/graphify` trigger) is shipped by the package — follow it to RUN the pipeline; NEVER edit it
(upgrades regenerate it). THIS skill is the machine-specific layer: install reality, quirks,
quality judgment, maintenance.

## When to use graphify / when not
- USE: a codebase/corpus too big to hold in context; architecture questions across many
  files; a repo you're new to. helios already has a graph (stale — see below).
- DON'T: corpus fits in a context window (the helios report itself says its ~7.3k words
  "may not need a graph"); a plain Grep answers it; cost-sensitive sessions (semantic
  extraction of docs/papers costs LLM tokens — code-only corpora are AST-only and free).

## Install reality (verified 2026-07-06 — the load-bearing quirk)

| Fact | Value |
|---|---|
| Engine | `graphifyy` **0.8.25**, pip-installed into SYSTEM Python 3.13 (`python -m pip show graphifyy`) |
| Vendor skill | v**0.8.25** (`Get-Content C:\Users\subha\.claude\skills\graphify\.graphify_version`) — IN SYNC |
| Interpreter pin | per-project `graphify-out\.graphify_python`; helios's → `C:\Users\subha\AppData\Local\Programs\Python\Python313\python.exe` (system) — consistent, works |
| uv | installed (0.11.15) but does NOT manage graphifyy |

Upstream README explicitly warns against `pip install` on Windows (interpreter-mismatch →
`ModuleNotFoundError: No module named 'graphify'`) and recommends `uv tool install graphifyy`.
This machine runs the warned-against configuration; it works BECAUSE everything pins to the
one system Python. It breaks if: a venv is active when the skill re-detects Python, or system
Python is upgraded/moved. Triage for ModuleNotFoundError → `machine-debugging-playbook`.
Migration to uv = reinstall = **user decision + user-run commands** (`machine-change-control`):
user runs `uv tool install graphifyy`, then `graphify install --platform windows`, then
delete stale `.graphify_python` files so they re-detect.

## Command quick reference (verified against `python -m graphify --help`, 0.8.25)

| Task | Command (safe class) |
|---|---|
| Ask the graph | `python -m graphify query "question" [--dfs] [--budget N]` (read-only) |
| Explain a node | `python -m graphify explain "X"` · path: `path "A" "B"` · impact: `affected "X"` |
| Refresh after code edits | `python -m graphify update <path>` (AST-only, no LLM cost) — has a **shrink-guard**: refuses to overwrite if the rebuild has fewer nodes (protects against ghost-node wipes); after real deletions override with `--force` or `GRAPHIFY_FORCE=1` |
| Full extraction | `python -m graphify extract <path> --backend ollama` (ollama = local/free; gemini/kimi/claude/openai/deepseek need API keys) — COSTS tokens/time, announce first |
| Quality diagnostics | `python -m graphify diagnose multigraph` · `python -m graphify benchmark` (both read-only) |
| Architecture page | `python -m graphify export callflow-html` |
| Git-hook auto-rebuild | `graphify hook install/status/uninstall` — installs a post-commit hook = **ask the user first** (state-changing, and commits are his domain) |

`/graphify` in PowerShell: use `graphify .` or `python -m graphify` — a leading `/` is a
path separator in PowerShell. Env-var knobs exist for most behaviors (GRAPHIFY_OUT,
GRAPHIFY_MAX_WORKERS, GRAPHIFY_API_TIMEOUT, GRAPHIFY_VIZ_NODE_LIMIT, GRAPHIFY_OLLAMA_NUM_CTX,
GRAPHIFY_SKIP_HOOK, …) — grep the installed source at
`C:\Users\subha\AppData\Local\Programs\Python\Python313\Lib\site-packages\graphify\` for the full set.

## Edge epistemics (the tool's honesty contract — never violate when extracting)
- `EXTRACTED` (explicit in source) → confidence 1.0 · `INFERRED` → forced-rank one of
  0.95/0.85/0.75/0.65/0.55, never 0.5 · `AMBIGUOUS` (uncertain, kept visible) → 0.1–0.3.
- Honesty rules from the vendor skill: never invent an edge; always show token cost; show
  raw cohesion numbers; warn before HTML viz on >5,000 nodes.

## Judging a graph — the quality checklist (born from the real helios graph)

The helios graph (`Projects\helios\graphify-out\`, built 2026-05-31 on an older engine)
exhibits the known failure modes — read its `GRAPH_REPORT.md` as the teaching example:
1. **Primitive-type god nodes**: `str`, `int`, `bool` as top-connected nodes with edges like
   "str --uses--> Engine" = extractor noise (upstream filtered language builtins in 0.8.21,
   #916/#726 — the graph predates it).
2. **Docstring-fragment labels** ("Runs the prompt through the model (prefill pass). Popul…")
   and duplicate `main()` nodes = node-identity noise.
3. **Confidence collapse**: avg INFERRED confidence 0.54 with >50% at 0.5 = the rubric was
   ignored (the forced-rank ladder exists precisely because of this).
4. **Token cost 0/0** despite a semantic pass = usage numbers never written back; the cost
   figures are meaningless.
5. 25 isolated nodes / thin communities = missing edges or genuinely disconnected files.
A graph failing ≥2 of these → rebuild on the current engine rather than trust it. The helios
graph fails 1–4 → **stale-version artifact; rebuild before relying on it** (mostly code →
AST-only → free; announce anyway).

## Maintenance & drift
- After ANY upgrade (user-run): `.graphify_version` must equal `pip show graphifyy` version;
  if not, user runs `graphify install --platform windows` to refresh the vendor skill.
- Newer upstream versions: `pip index versions graphifyy` (network — announce) or check
  github.com/safishamsi/graphify releases. Local 0.8.25 dates to ~2026-05-29 upstream.
- The orphaned `Projects\graphify` folder is NOT the tool (see `machine-failure-archaeology`).

## When NOT to use this skill
Running the actual pipeline steps → the vendor skill (`/graphify`). Python env triage →
`machine-debugging-playbook`. Whether building a graph is worth it for a task → the
"When to use" table above decides in ~10 seconds.

## Provenance and maintenance
Authored 2026-07-06 from: `python -m pip show graphifyy`, `python -m graphify --help`,
`.graphify_version`, helios `GRAPH_REPORT.md` + `.graphify_python`, vendor SKILL.md (read in
full), upstream history mined from the pack remnant (v1–v8 lines; embed-only). Re-verify:
```powershell
python -m pip show graphifyy | Select-String '^Version'          # 0.8.25 as of 2026-07-06
Get-Content C:\Users\subha\.claude\skills\graphify\.graphify_version   # must match the line above
python -m graphify --help | Select-Object -First 5               # CLI alive?
Get-Content C:\Users\subha\Projects\helios\graphify-out\.graphify_python  # still system python?
```
