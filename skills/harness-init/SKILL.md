---
name: harness-init
description: Use when the user is starting a NEW project and wants harness engineering infrastructure (AGENTS.md, architectural boundaries, PROGRESS.md, DECISIONS.md, feature scope surface, verified test setup) established before any feature code is written. Triggers - new project setup, initialize harness, bootstrap this repo, harness init, day-one architecture, start a new project with an agent, greenfield agent setup.
---

# Harness Init — establish agent-reliability infrastructure before feature work begins

Based on the "Learn Harness Engineering" lecture series (Walking Labs). Initialization
and implementation are different kinds of work with opposing goals — implementation
maximizes feature output, initialization maximizes reliability for everything that
comes after. Mixing them weakens both, so this runs as its own phase, entirely before
the first feature.

## CRITICAL — this is a review loop, not a fire-and-forget build

**The user must verify every change before development proceeds.** Do not write
feature code as part of this skill, and do not silently barrel through all steps.
After the initialization phase is complete, stop, present the full checklist below
with what was created, and wait for the user's explicit confirmation before starting
on the first feature. If the user says "just do it all," confirm once that they're
waiving this checkpoint — don't assume silence means proceed.

## Steps

1. **Environment**: confirm or set up a dependency lockfile, a runtime version pin
   (`.nvmrc`/`.python-version`/etc), and a working install command. Verify it runs
   clean from a fresh clone/checkout.
2. **Test framework**: set it up and confirm it runs — even with zero or one trivial
   test. The user needs to see a real pass before any feature code exists.
3. **AGENTS.md**: create as a short entry file — overview, first-run commands,
   stack+versions, max 15 hard constraints. Leave room to link out to `docs/` later;
   don't over-write it now with detail that belongs in topic docs.
4. **Architectural boundaries as an executable rule, not prose**: agents copy
   whatever pattern already exists in a repo, so a weak first pattern propagates.
   Pick a simple layering appropriate to the stack (e.g. Types -> Config -> Repo ->
   Service -> Runtime -> UI, forward-only dependencies) and enforce it with a
   lint/grep-based check wired into the check script — not a comment asking people
   not to violate it.
5. **State files**: create `PROGRESS.md` and `DECISIONS.md`, even mostly empty,
   recording the initial setup decisions actually made (why this layering, why this
   test framework, etc).
6. **Scope surface**: create an empty `features.json` with schema
   `{id, behavior, verification, state}` (states: `not_started -> active -> blocked
   -> passing`, only settable to `passing` by a successful verification command).
7. **Checkpoint commit**: once all of the above is in place and verified working,
   make a git checkpoint commit.
8. **Report**: time from start to first passing test, plus a checklist confirming
   all 5 initialization outputs exist — runnable environment, verifiable test
   framework, a startup readiness checklist, a task breakdown with acceptance
   criteria, and the git checkpoint.

## After initialization

Tell the user explicitly: **review every file created before any feature work
starts** — this is the one-time setup every future session and every feature will be
built on top of, so mistakes here compound. Once confirmed, proceed feature-by-feature
under WIP=1: each feature gets a `features.json` entry with a concrete verification
command defined *before* implementation, and only moves to `passing` when that
command actually succeeds.
