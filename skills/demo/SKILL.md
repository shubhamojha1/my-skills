---
name: demo
description: Generate an interactive, single-page browser demo of one of Shubham's systems projects (Helios, SimpleMQ, Bifrost, Chronos, Rakshak, etc.) for deployment to a /demo endpoint on shubham-ojha.com. Use whenever the user runs /demo, asks to "make a demo for [project name]", "build a playable version of [project name]", "create a portfolio demo", or wants visitors to interact with a project without cloning the repo. Also use when iterating on an existing demo (adding an inspector view, changing the simulation, restyling). Works in staged checkpoints — never generate the final artifact without the user approving the demo concept and design tokens first.
---

# /demo — repo to interactive portfolio demo

Turn a repository into a single-page React demo artifact that a visitor can play with in the browser. The demo must capture the *mechanics* of the project honestly (scheduling, contention, data flow), even when the underlying compute is simulated. The audience is recruiters and engineers spending 30–60 seconds: the demo's job is to prove "this person built a real system," not to teach a tutorial.

The output of a full run is one `.jsx` file (self-contained, no backend, stateless) ready to drop into the personal site's `/demo` route.

## Non-negotiables

- **Honesty labeling.** If compute is simulated (e.g. GPU inference replaced by a scripted token stream), the demo must say so visibly in the UI — a "simulated" badge in the header and a one-line footnote explaining exactly what is and isn't real. Never present fake output as live model output.
- **Systemic over sequential.** Default to one live system where mechanics emerge from interaction (queues filling, blocks stalling, caches evicting) rather than a step-by-step component walkthrough. A component-tour reads as a lecture; contention under load reads as proof-of-work.
- **Stateless.** No persistence, no backend calls. All state lives in React memory and resets on reload.
- **Checkpoints are real.** Stop and wait for the user's answer at the end of Stage 1 and Stage 3. Do not barrel through to code generation in one shot — the whole reason this is a skill and not an autonomous agent is that mode selection and design are the user's calls.

## Workflow

### Stage 0 — Locate inputs

1. Identify the target repo (argument to /demo, or ask).
2. Look for the project inventory YAML (the same one the `/tailor` resume system reads). If it exists and has a `demo_strategy` entry for this project, treat it as a strong prior for Stage 1 and say so. If the file or field is missing, proceed without it and offer to write the chosen strategy back into the inventory at the end (see Stage 5).

### Stage 1 — Read repo, propose concept + simulation mode ⛔ CHECKPOINT

Read the repo enough to understand: what the system *does*, what its hardest/most impressive mechanic is, and what resources it needs at runtime.

Then propose, in a short message (not a document):

1. **What the demo should teach** — one sentence. The single mechanic a visitor should walk away understanding (e.g. for an inference engine: "paged KV blocks are contended, and the scheduler stalls/admits requests around that contention").
2. **Simulation mode** — pick one and justify:
   - **live/WASM** — the real code (or a faithful port) runs in-browser. Fits pure-CPU, dependency-light projects (message brokers, hash joins, parsers, classifiers with small models).
   - **traced replay** — real runs are recorded offline (latency, scheduling decisions, state transitions) and the demo replays/visualizes the trace. Fits anything needing hardware the browser lacks (GPU inference, QEMU, kernels).
   - **scripted mechanics** — the *resource-management logic* is reimplemented faithfully in JS (admission, block allocation, stalls, eviction), while the expensive compute is replaced by scripted output. Fits when the interesting part is the scheduler, not the compute.
3. **Interaction surface** — 2–4 things the visitor can actually do (enqueue requests, tune a knob, trigger pressure, inspect a request's timeline).

Offer 1–2 alternatives briefly if the choice is genuinely close. Then **stop and wait for the user to pick.**

### Stage 2 — Confirm scope

One short exchange, folded into the Stage 1 approval if the user's reply already covers it:

- Which metrics/panels are in (keep it to ~4 metrics max — this is an instrument panel, not Grafana).
- Whether an inspector/forensic view is in scope (click an entity → see its lifecycle timeline: admitted at tick N, block allocated, stalled at tick M, freed at completion). Recommend it when the mechanic involves per-entity state over time; it converts "show me the internals" into something the visitor caused rather than a slideshow.
- Any real numbers to bake in (actual benchmark figures from the repo's README or trace files) versus derived formulas.

### Stage 3 — Design tokens ⛔ CHECKPOINT

Read the frontend-design skill if available in the environment (`/mnt/skills/public/frontend-design/SKILL.md`) and follow its process. Then propose a compact token plan:

- **Palette** — 4–6 named hex values. Derive it from the project's *world* (an inference engine is an instrument panel; a message broker is a switchboard; an OS is a boot console), not from a generic template. Dark, low-chroma backgrounds with one hot accent for "active/pressure" states suit systems demos well; avoid the stock AI-generated looks (cream + terracotta serif, near-black + acid green).
- **Type** — display/body/utility roles. Monospace-forward is the house style for these systems demos (labels, metrics, and identifiers in mono; longer prose in a plain sans), but vary the specific faces per project so the demos don't all look identical side by side on the site.
- **Signature element** — the one visual thing this demo will be remembered by (e.g. a color-coded memory-block grid where each cell's owner is visible at a glance). One per demo; keep everything else quiet and disciplined.

All demos on the site should feel like siblings — same restraint, same honesty labeling, same instrument-panel discipline — without being reskins of each other. **Stop and wait for sign-off.**

### Stage 4 — Build

Generate a single self-contained `.jsx` file following these conventions:

**Structure**
- Default export, functional component, no required props.
- No browser storage (localStorage/sessionStorage break in hosted artifact contexts), no external fetches, no form tags — use onClick/onChange handlers.
- Only import from allowed libraries (react, lucide-react, recharts, d3, lodash — prefer zero dependencies beyond react when possible).
- One engine tick loop (setInterval in a useEffect, ~250–400ms per tick) driving all state transitions. Every metric shown is computed from actual simulated state — never random numbers dressed up as telemetry.

**Layout**
- Header: project name, a "simulated" or "traced" badge where applicable, and a one-line subtitle naming the real techniques and hardware context (e.g. "continuous batching · paged KV cache · [model name] on [hardware] (traced, not live)").
- Main split: interaction + output stream on one side, instrument panel (state visualization + metrics) on the other. The signature element lives in the instrument panel.
- Footnote at the bottom stating plainly what is simulated and what mirrors the real system's logic.

**Interaction**
- Provide 3–5 one-click example inputs so a visitor gets a payoff in under five seconds, plus a free-text input where it makes sense. If free text can't drive real behavior, it replays a fixed script — and the placeholder text says so.
- A pause/run control for the engine loop.
- Entities in flight should be individually visible (cards with status: queued / active / stalled / done), color-coded consistently with the state visualization so a visitor can match a request to its resources at a glance.
- Make resource pressure reachable: with enough concurrent inputs, the visitor should be able to cause stalls/eviction/backpressure and see it labeled as such. This moment is the demo's proof-of-work.

**Simulation fidelity**
- Keep the simulation model small but *truthful to the real system's rules*: if the real scheduler admits on free-block availability, the JS one must too; if eviction is LRU, simulate LRU. The rule is: every behavior shown must be defensible in an interview as "yes, that's how the real one works."
- Where real numbers are known (from Stage 2), use them; otherwise derive metrics from simulated state with formulas simple enough to explain.

**Quality floor**
- Responsive down to mobile; visible keyboard focus on interactive elements; respect reduced-motion preferences for any animation.
- Empty states invite action ("no requests yet — pick a prompt above"); errors explain what happened and how to fix it; labels use sentence case and say what happens ("send", not "Submit").
- Restraint: one signature element, one accent color for heat, minimal animation (a status pulse and a block-free flash go a long way; more starts to look AI-generated).

### Stage 5 — Deliver + record

1. Present the `.jsx` file.
2. Summarize in 3–5 bullets what the visitor can do and what's real vs simulated (this doubles as copy for the site's demo page intro).
3. **REQUIRED SUB-SKILL:** Use `installing-portfolio-demos` to actually wire the file into `personal-site/app/demo/<slug>` as a working route — don't hand-roll the install steps here.
4. If a project inventory YAML was found in Stage 0, offer a `demo_strategy` snippet to add to it, e.g.:

```yaml
helios:
  demo_strategy:
    mode: scripted-mechanics
    teaches: paged KV cache contention under continuous batching
    signature: color-coded block grid
    artifact: demos/helios-demo.jsx
    status: shipped
```

## Iterating on an existing demo

When the user asks to modify a demo that already exists (add an inspector, change pacing, restyle), skip Stages 0–2. Re-run Stage 3 only if the change is visual; otherwise go straight to Stage 4 edits on the existing file. Preserve the existing token system unless explicitly asked to change it.
