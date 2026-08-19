---
name: helios-continuous-batching-campaign
description: Use when working on Projects\helios performance, scheduler, engine, or KV-cache code — finishing/hardening continuous batching, chunked prefill regressions, TTFT or throughput analysis, benchmark runs, or the five open issues. Triggers - helios, TTFT, tokens/sec, decode_step, prefill chunk, token budget, FCFS admission, memory pages, benchmark JSON, request hang, engine_torch, llama-cpp state corruption.
---

# Helios — Continuous-Batching Campaign (finish & harden)

Helios (`C:\Users\subha\Projects\helios`) is the user's from-scratch local LLM inference
server (FastAPI + custom scheduler + TorchEngine, OpenAI-compatible routes). **Continuous
batching already landed** (2026-05-24 commit "continuous batching sort of works") and produced
a 4.1× throughput win. This campaign is about *finishing the job*: resolving one measured
regression, five documented open issues, and re-establishing a clean benchmark record.

**Do not re-implement continuous batching.** A stale analysis (project memory
`project_continuous_batching.md`, dated 2026-05-23) describes `decode_step` as a sequential
loop — that was fixed the next day. Trust `notes.md` in the repo and the code itself.

## When to use / when not

- USE for: perf work, scheduler/engine/memory changes, benchmark interpretation, the open issues.
- NOT for: environment setup from scratch (`machine-build-and-env`), repo orientation
  (`projects-atlas`), the knowledge graph in `graphify-out\` (`graphify-operations`),
  evidence standards in general (`machine-validation-and-qa`).

## Lab map (verified 2026-07-06)

| Path | Role |
|---|---|
| `main.py` | wires engine + memory manager + scheduler + uvicorn |
| `scheduler\scheduler.py` | async control loop: submit → prefill → decode → emit |
| `scheduler\fcfs.py` | FCFSStrategy, admission control (now memory-gated) |
| `engine\engine_torch.py` | TorchEngine: chunked `prefill()` (chunk_size=256), batched `decode_step()` (left-pad KV, attention mask, position_ids) |
| `engine\engine.py` | OLD llama-cpp engine — state-corrupt under concurrency (open issue #1) |
| `memory\manager.py` | page-based KV allocator (256 pages × 16 tokens/page) |
| `core\config.py` | `max_batch_size: int = 8` (line 17) — count gate no longer used for admission |
| `api\` | FastAPI server + pydantic models (open issues #4, #5) |
| `benchmarks\throughput.py` | the harness (`python -m benchmarks.throughput`, needs server up) |
| `benchmarks\output\throughput_*.json` | the benchmark record (5 files, 2026-05-22 … 05-30) |
| `notes.md` | **primary source**: run-by-run benchmark history + root-cause analyses |
| `issues.md` | **primary source**: 5 open issues with file:line |
| `plan.md` | future: custom Q4_K_M dequant CUDA kernel (frontier item) |
| `tests\`, `conftest.py`, `engine\test_torch_engine.py` | pytest surface |

Model: Qwen2.5-3B-Instruct (HF transformers 5.8.0, bfloat16, CUDA). Per-repo venv at
`venv\` — activate with `.\venv\Scripts\activate` from the repo root.

Working tree as of 2026-07-06: 6 modified files uncommitted (`benchmarks/throughput.py`,
`core/types.py`, `engine/engine_torch.py`, `helios_cli.py`, `main.py`,
`scheduler/scheduler.py`) + 3 untracked benchmark JSONs + `graphify-out/`. This WIP is the
Run-3/Run-4 work — **do not "clean it up" or commit it** (see `machine-change-control`).

## The benchmark record (memorize the shape, quote the files)

All runs: `python -m benchmarks.throughput` against `helios serve` on 127.0.0.1:8080,
max_tokens=256, streaming TTFT measured client-side. Prompts are defined IN the harness:
`SHORT_PROMPT` (~12 tokens) and `LONG_PROMPT` (~600 tokens, spans multiple 256-token chunks).

| Run | Date / JSON | Change | Short-prompt result (c=1/4/8/16 tok/s) | Verdict |
|---|---|---|---|---|
| 1 | 05-22 `_132213` | baseline: count-gated cohorts + serial decode | 23.2 / 23.5 / 35.2 / 43.6; TTFT p50 43.7s @c8; 4 requests hung ~2.6h @c16 | broken |
| 2 | 05-24 `_200446` | **continuous batching**: memory-gated admission + batched decode (left-pad KV, attn mask, RoPE position_ids, DynamicCache 5.8 API) | 21.7 / 74.8 / 124.2 / **179.0**; TTFT p50 729ms @c16; no hangs | the win |
| 3 | 05-25 `_014815`, `_100152` | chunked prefill (interleave prompt chunks with decode) | 19.9 / 62.4 / 94.4 / 138.2 short; long-prompt c=8 TTFT 1,409ms | mixed: ~20% short-prompt regression |
| 4 | 05-30 `_023958` | token budget per step (prefill_budget = 256) | 12.8 / 49.7 / 82.0 / 125.4 short; long c=4 TTFT 1,557ms | **regression** — root-caused |

Run 4 root cause (from `notes.md`, verified): with budget = chunk_size, one 256-token chunk
exhausts the whole step budget, so exactly one request prefills per step. Long-prompt TTFTs
formed an arithmetic progression (598, 1084, 1557, 1985ms — ~490ms apart) = sequential
staggering. Run 3 processed all chunks for all PREFILL requests each step, giving everyone
~equal TTFT. Short-prompt c=1 variance (~36%) is suspected thermal/environmental noise
across days — 12-token prompts never trigger the budget.

**Comparison discipline:** only compare runs with the same prompt set + max_tokens; treat
< ~10-15% single-config deltas as noise unless reproduced; Run 2 is the short-prompt
baseline-to-beat; Run 3 is the long-prompt reference.

## Bug ledger

Resolved (do not re-fix): main.py max_batch_size=4 override (removed; only
`core\config.py:17` default 8 remains, unused as an admission gate) · serial decode_step
(now batched, `engine\engine_torch.py:100-170`) · transformers DynamicCache API drift.

OPEN (from `issues.md`, verified 2026-07-06 — re-read it before starting, line numbers may drift):
1. `engine\engine.py:60,99` — llama-cpp path is **state-corrupt** under multi-request decode
   (shared Llama context; prefill resets clobber each other).
2. `scheduler\scheduler.py:82` — `_lock` held across `_step()` including blocking GPU calls
   → `submit()`/`cancel()` stall during generation; cancel cannot interrupt.
3. `scheduler\fcfs.py:39` — admission reserves by `req.max_tokens`, not prompt tokens +
   generation capacity → KV budget accounting wrong both directions.
4. `api\models.py:6` + `scheduler\scheduler.py:124` — no lower-bound validation on
   max_tokens (0/negative accepted, still burns prefill).
5. `api\server.py:84` — endpoints assume `app.state.scheduler`; bare
   `uvicorn api.server:app` returns 500s instead of a clear startup error.

## Campaign phases (decision-gated; correctness gate before perf gate, always)

### P0 — Re-establish ground truth (every new session, ~5 min, read-only)
```powershell
git -C C:\Users\subha\Projects\helios log -1 --format='%cs %s'
git -C C:\Users\subha\Projects\helios status --porcelain
Get-ChildItem C:\Users\subha\Projects\helios\benchmarks\output
```
- If new commits exist past 2026-05-24 or notes.md gained a "Run 5", this skill's tables are
  stale — read `notes.md` first and update this skill (see Provenance).
- Check the model exists: `Get-ChildItem C:\Users\subha\Projects\helios\models` — if empty,
  serving/benchmarks are blocked; ask the user to download (no installs/downloads yourself).
- Establish test state: `.\venv\Scripts\activate` then `pytest -q` from repo root. Record
  pass/fail counts BEFORE changing anything — that's your correctness baseline.
- GPU sanity (read-only): `python -c "import torch; print(torch.cuda.is_available())"`.

### P1 — Settle the Run-4 question (the live perf decision)
The token-budget change (Run 4) is in the uncommitted working tree and measured worse.
Options, ranked; PREDICT numbers before running anything (write them down first):
1. **Fair-interleave fix**: budget loop takes ONE chunk per PREFILL request per step
   (round-robin) instead of draining the budget on one request. Prediction: long-prompt
   TTFTs equalize (~Run-3 values, no arithmetic progression), short-prompt unaffected.
2. **Revert to Run-3 behavior** (all chunks each step): simplest; accepts prefill bursts
   delaying decode under many long prompts.
3. Keep Run 4: rejected by the data — only if a new workload argument appears.
Fenced: random chunk_size tuning without a mechanism hypothesis; benchmarking option deltas
with different prompts/max_tokens than the record.
GATE: chosen option implemented → long-prompt c=4 TTFT p50 back to ≤ ~800ms class and no
arithmetic-progression pattern in per-request TTFTs; short-prompt c=4 within ~10% of 62-75 tok/s band.

### P2 — Admission accounting (open issue 3; correctness for the whole design)
Reserve = ceil((prompt_tokens + max_tokens)/16) pages at admission (or lazy-allocate decode
pages with a documented eviction answer — that's a design fork for the user to pick).
Write the failing unit test FIRST (long prompt + small max_tokens must not under-reserve).
GATE: new pytest green; benchmark re-run shows no hangs at c=16 with mixed prompt lengths.

### P3 — Lock granularity (open issue 2)
Snapshot scheduler state under `_lock`, run GPU work outside it (or per-phase locks).
GATE: a `cancel()` issued mid-long-prefill returns promptly (measure: < ~100ms, candidate
threshold) and the cancelled request stops consuming decode steps; pytest green.

### P4 — Input validation + server hardening (open issues 4, 5; small)
max_tokens ≥ 1 validation at the pydantic layer + clear startup error when
`app.state.scheduler` missing. GATE: bad-request tests (max_tokens=0, -1) return 422, not
inference work; bare `uvicorn api.server:app` fails loudly with the configured message.

### P5 — The llama-cpp engine decision (open issue 1)
Menu for the user (do not decide silently): (a) fence it — document torch-only concurrency,
guard engine.py to reject concurrent use; (b) fix with per-request contexts (memory-heavy);
(c) delete the path (plan.md's dequant-kernel future makes llama-cpp removal plausible).
Prepare the recommendation with evidence; user picks.

### P6 — Re-benchmark & close
Full matrix, BOTH prompts: server up (`helios serve`), then `python -m benchmarks.throughput`.
New JSON lands in `benchmarks\output\`. Deliverable to user: side-by-side table (this run vs
Run 2 and Run 3), pytest summary, uncommitted-diff summary. Success = numbers, never adjectives.
Perf claims without the JSON violate `machine-validation-and-qa`.

### Frontier (after P6): `plan.md` — custom Q4_K_M dequant CUDA kernel
(`csrc/dequant_q4km.cu`; prerequisite per plan.md: PyTorch attention path complete).
See `research-methodology-and-frontier`. Do not start it mid-campaign.

## Fenced wrong paths
- Re-implementing continuous batching or "fixing" decode_step's loop — it's already batched.
- Raising `max_batch_size` to fix latency (the count gate is gone; it moves nothing now).
- Switching to vLLM (defeats the from-scratch purpose) or PagedAttention-first.
- Trusting the 2026-05-23 memory file's "Bug 2 not fixed yet" — superseded by notes.md.
- Comparing benchmark runs across different prompts/max_tokens/thermal conditions.

## Iron rules (see machine-change-control)
No commits/pushes — the 6-file WIP stays the user's to review. No pip installs into the venv
— missing packages are an ask-the-user item. Benchmarks occupy the GPU for minutes — say so
before starting one.

## Provenance and maintenance
Authored 2026-07-06 from: repo state (git log/status), `notes.md`, `issues.md`, `plan.md`,
`benchmarks\throughput.py`, `engine\engine_torch.py` (decode_step lines 100-170),
`core\config.py:17`, benchmark JSONs (5 files), and helios project memory (noting its
2026-05-23 analysis is partially stale). Re-verify:
```powershell
git -C C:\Users\subha\Projects\helios log -1 --format='%cs %s'          # still 2026-05-24 "continuous batching sort of works"?
git -C C:\Users\subha\Projects\helios status --porcelain                 # still 6 M + 3 ?? JSONs + graphify-out?
Get-ChildItem C:\Users\subha\Projects\helios\benchmarks\output           # new runs beyond 20260530?
Select-String -Path C:\Users\subha\Projects\helios\issues.md -Pattern '^\s*\d\.' | Measure-Object   # still 5 open issues?
Select-String -Path C:\Users\subha\Projects\helios\core\config.py -Pattern 'max_batch_size'         # still config.py:17 default 8?
```
If `notes.md` gains runs or `issues.md` shrinks, update the tables here and date-stamp the edit.
