---
name: harness-audit
description: Use when the user wants to audit or build out harness engineering infrastructure (AGENTS.md, ARCHITECTURE.md, CONSTRAINTS.md, PROGRESS.md, DECISIONS.md, verification commands, feature-state scope surface, cleanup checklist) for an EXISTING project/repository. Triggers - harness audit, audit the harness, agent-readiness, AGENTS.md setup, make this repo agent-friendly, fresh session test, knowledge visibility gap, harness engineering.
---

# Harness Audit — build agent-reliability infrastructure into an existing repo

Based on the "Learn Harness Engineering" lecture series (Walking Labs). A harness is
everything outside the model weights that determines whether an agent can execute
reliably: Instruction, Tool, Environment, State, and Feedback subsystems. Core rule:
**the repo is the spec** — anything the agent can't see doesn't exist for it.

## CRITICAL — this is a review loop, not a fire-and-forget build

**The user must verify every change before development proceeds.** Do not run all
phases silently and present a wall of new files at the end. After each phase below:
stop, summarize what was created/changed (diff-level, not just "done"), and wait for
the user's explicit go-ahead before starting the next phase. If the user says
"just do it all," confirm once that they're waiving per-phase review — don't assume
silence means proceed.

## Phase 0 — Audit (always first, no files created)

1. Score the repo 1-5 on each of the five subsystems: Instruction, Tool, Environment,
   State, Feedback.
2. Run a "fresh session test": pretend you just opened this repo cold. List every
   question you cannot answer from repo contents alone — stack versions, first-run
   commands, architecture, hard constraints, current in-progress work, how to verify
   a change. This list is the Knowledge Visibility Gap.
3. Report the scores and the gap list. **Do not create any files yet.** Wait for the
   user's go-ahead before Phase 1.

## Phase 1 — Instruction Subsystem

- Create or rewrite `AGENTS.md` (and `CLAUDE.md` if relevant) as an entry file:
  50-200 lines, one-paragraph overview, first-run commands, max 15 hard constraints,
  one-line links to topic docs with applicability conditions.
- If deep detail is needed, push it into `docs/*.md` (50-150 lines each), linked from
  `AGENTS.md` with a condition like "read this when touching X" — not front-loaded.
- Create `ARCHITECTURE.md` per major module directory, next to the code it describes.
- Create `CONSTRAINTS.md` for hard rules pulled out of prose.
- Put critical constraints at the top or bottom of the entry file — never buried
  mid-document (models attend worse to the middle of long files).

Stop. Show the user a summary/diff. Wait for confirmation.

## Phase 2 — State Subsystem

- Create `PROGRESS.md`: latest commit, test status, completed work, in-progress work,
  known issues, next steps.
- Create `DECISIONS.md`: seed it with real architectural decisions inferable from the
  current code/git history — what was chosen, why, what was rejected.
- Add a clock-in/clock-out routine to `AGENTS.md`: what to read/verify at session
  start, what to update/commit at session end.

Stop. Show the user a summary/diff. Wait for confirmation.

## Phase 3 — Feedback Subsystem

- Identify or create verification commands: test, typecheck, lint, and one combined
  "check" command. Actually run each and confirm it reports pass/fail correctly.
- If end-to-end/integration tests are missing for core user flows, flag this
  explicitly rather than silently skipping it — this is usually the single
  highest-leverage gap. Unit tests alone miss interface mismatches, state
  propagation errors, resource leaks, and environment-dependent failures.

Stop. Show the user a summary/diff. Wait for confirmation.

## Phase 4 — Scope Surface

- Create a machine-readable feature/task list (e.g. `features.json`) with
  `{id, behavior, verification command, state}` for currently-planned or
  in-progress work. States: `not_started -> active -> blocked -> passing`.
  Only a successful verification command may set state to `passing` — never the
  agent's own judgment.

Stop. Show the user a summary/diff. Wait for confirmation.

## Phase 5 — Cleanup Discipline

- Add a "clean state" checklist to `AGENTS.md`: build passes, tests pass,
  `PROGRESS.md` updated, no stale debug artifacts/TODOs, startup path verified
  functional. State explicitly that a session isn't done until all five hold.

Stop. Show the user a final summary of everything created across all phases.

## After the audit

Tell the user explicitly: **review every file created or modified before starting
any feature work** — these documents become the source of truth future agent
sessions will trust unquestioningly, so an error here propagates into every session
after it. Suggest they read each file once end-to-end rather than skimming diffs.
