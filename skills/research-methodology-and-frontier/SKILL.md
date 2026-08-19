---
name: research-methodology-and-frontier
description: Use when deciding what to attempt next on this machine, turning a hunch into a testable claim, judging whether a result is real, planning experiments or benchmarks, or asked about open problems, research direction, "what should we build", or how to prove an improvement. Triggers - hypothesis, experiment, evidence, benchmark comparison, root cause, frontier, state of the art, research, falsifiable, milestone, prototype, stalled project.
---

# Research Methodology & Frontier — how results happen here, and where to aim

Part A is the discipline that turns a hunch into an accepted result ON THIS MACHINE
(every element grounded in a real local example). Part B is the frontier map — the four
bets where this setup can beat the current state of the art. User's stated goal
(2026-07-06): "maximise the results" on all fronts.

## Part A — The methodology

### The evidence bar (non-negotiable)
1. **A hypothesis predicts numbers BEFORE the run.** Write the predicted values down first;
   then run; then compare. (Post-hoc "that looks better" is not a result —
   `machine-validation-and-qa`.)
2. **One mechanism must explain ALL observations — including the negatives.** If any
   observation doesn't fit, the mechanism is incomplete: find the second mechanism, don't
   average over the anomaly.
3. **Assign yourself the refutation.** Before accepting a result, state what observation
   would falsify it, and check for exactly that.

### House worked example #1 — the helios batch-size discovery (the standard to copy)
From the 2026-05-22/23 investigation (memory + `Projects\helios\notes.md`):
- Observation: TTFT p50 at c=8 ≈ 43.7s ≈ one full batch duration; c=4→c=1 throughput
  delta only +1.3%.
- Hypothesis predicted from numbers alone: "effective batch size is 4, not 8" — BEFORE
  reading code.
- Code confirmation: `main.py` override defaulted max_batch_size=4 (mechanism 1).
- Rule 2 applied: mechanism 1 did NOT explain why throughput barely scaled even inside a
  batch → second mechanism required and found: `decode_step` ran per-request forward passes.
  Two mechanisms, each tied to specific observations.
- Later, the same discipline caught a regression: Run-4 long-prompt TTFTs formed a perfect
  ~490ms arithmetic progression → sequential chunk staggering (see
  `helios-continuous-batching-campaign`). Numbers → mechanism → fix. Also note the honesty
  in `notes.md`: a ~36% c=1 delta attributed to thermal noise, not claimed as signal.

### House worked example #2 — verification-before-write (onthejob ingest)
LLM-extracted incident fields are read BACK against the source text before being written
(the four ingest-quality rules exist because four real incidents shipped wrong —
`onthejob-operations`). Generalization: generated content gets verified against its source
BEFORE it lands, not after a reader complains.

### The idea lifecycle on this machine (observed, verified 2026-07-06)
hunch → **prototype repo/branch** (evidence: mimir@`prototyping`, synapse@`prototype`,
bifrost@`storage-engine`) → either **graduates** (helios has pyproject + CLI entry;
onthejob went live at systemsfailed.dev) or **stalls** (bifrost 2025-10, heimdall 2025-05,
mimir 2025-10, synapse 2025-12, rag-lab 2025-08) → learnings land in memory/skills.
**Stalling is a normal, documented outcome — not failure.** NEW convention introduced by
this library (2026-07-06, propose-and-use): when a prototype stalls, add a one-line status
+ reason to that project's memory (`machine-memory-and-docs`) instead of silent abandonment
— future sessions then know whether the idea died on merit or on attention.

### Where good ideas have come from here (pattern, not prescription)
1. Building infrastructure from scratch and instrumenting it (the mythology repos; helios's
   benchmark JSONs). 2. Curating external knowledge into structured form (systemsfailed.dev;
   research-papers incl. English+Sanskrit tokenizer work). 3. Dogfooding tools on own repos
   (graphify on helios). The common move: **make the thing measurable, then look at the numbers.**

## Part B — The frontier map (candidate framings, falsifiable milestones — no oversell)

### Bet 1 — systemsfailed.dev: the canonical STRUCTURED failure-taxonomy dataset
- SOTA falls short: danluu/post-mortems and k8s.af are unstructured link lists — not
  queryable, no schema, no failure-class layer.
- This setup's asset: Zod-validated schema, 30 curated incidents, codified extraction-quality
  rules, a running discovery bot, an LLM ingest pipeline (see `onthejob-phase2-campaign`).
- First three steps in-repo: Phase 1 (open-source setup) → Phase 2 step 0 (pattern-vocabulary
  consolidation: 104 tags → curated set) → one supervised end-to-end ingest run passing all
  four quality rules.
- **You have a result when:** an external contributor lands a schema-valid incident via PR,
  OR the dataset reaches 100+ validated incidents and something external consumes it
  programmatically.

### Bet 2 — sysdesignvault: interactive-widget learning at USACO-Guide standard
- SOTA falls short: systems-design education is static prose/video; nothing in the space has
  per-concept interactive widgets.
- Asset: working widget layer (13 new widgets mid-flight), 57 MDX concepts, ~170-topic
  curriculum backlog, progress tracking implemented (see `sysdesignvault-platform`).
- First three steps: close out progress-tracking verification → land the ai-foundations /
  transformer-internals expansion → search.
- **You have a result when:** coverage ≥ 3× (≈150+ concepts) with widget-first held, AND
  progress data (analytics dep is present) shows organic return usage.

### Bet 3 — helios: from-scratch continuous batching on consumer hardware, documented
- SOTA falls short: vLLM et al. are production-grade but opaque as learning artifacts; no
  well-documented consumer-GPU walkthrough exists at this depth.
- Asset: working continuous batching (43.6 → 179 tok/s at c=16), complete benchmark record
  with root-cause narratives (`notes.md`), a 5-issue hardening list, and a written next
  frontier (`plan.md`: custom Q4_K_M dequant CUDA kernel).
- First three steps: settle the Run-4 token-budget question → fix admission accounting →
  full re-benchmark (all in `helios-continuous-batching-campaign`).
- **You have a result when:** post-campaign benchmark shows near-linear throughput scaling
  until VRAM saturation with zero hangs, and the write-up lets a reader reproduce it.

### Bet 4 — The meta-frontier: cheap-model autonomy on this machine
- SOTA falls short: agent autonomy is usually demonstrated with frontier-priced models;
  the open question is whether a haiku/sonnet-class session can safely run a real machine.
- Asset: THIS library (16 skills with verification commands and change-control), default
  model already haiku (settings.json), the iron rules, per-project memory.
- First three steps: run one campaign phase end-to-end in a sonnet session using only the
  skills → log every gap/violation into memory → tighten the skill that allowed it.
- **You have a result when:** a haiku/sonnet session completes a full campaign phase with
  zero iron-rule violations and nothing for the user to fix except review-and-commit.

## When NOT to use
Routine runbook work → the project skills. Live debugging → `machine-debugging-playbook`
(this skill is for what to attempt and how to know it worked, not how to unbreak things).

## Provenance and maintenance
Authored 2026-07-06 from: helios notes.md + memory, onthejob memory + repo, branch states of
mimir/synapse/bifrost, settings.json (model haiku), sysdesignvault package.json
(@vercel/analytics present). The frontier bets are FRAMINGS — revisit quarterly or when a
milestone lands. Re-verify anchors:
```powershell
git -C C:\Users\subha\Projects\mimir rev-parse --abbrev-ref HEAD      # prototyping
(Get-Content C:\Users\subha\.claude\settings.json -Raw | ConvertFrom-Json).model   # haiku
(Get-ChildItem C:\Users\subha\Projects\onthejob\content\incidents -Filter *.md).Count  # 30 → bet-1 milestone is 100+
(Get-ChildItem C:\Users\subha\Projects\sysdesignvault\content -Recurse -Filter *.mdx).Count  # 57 → bet-2 milestone is ~150+
```
When a "you have a result when" line becomes true, record it in memory and update the bet.
