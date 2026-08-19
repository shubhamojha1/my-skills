---
name: scout
description: >-
  Given a job description, propose the 1-2 portfolio projects Shubham should
  actually build to become a credible hire for that specific role — chosen to
  patch the gaps his existing evidence can't cover, shaped around the target
  company's real engineering domain, and specified deeply enough to start
  building the same day (goal, scope, architecture, milestones, the exact
  benchmarks to run, and the resume bullet the finished project will earn).
  Use this whenever the user runs /scout, or asks "what should I build for
  this job", "what project would get me hired at X", "how do I close the gap
  for this JD", "is my portfolio enough for this role", or shares a JD and
  wonders what's missing from their projects. Also use right after a /tailor
  run when the rationale surfaced gaps the resume couldn't answer — this skill
  is the constructive follow-up to those gaps.
argument-hint: jds/<company>/<role>.md
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, WebSearch, WebFetch
---

# /scout

Read the JD at `$0`. Produce a build spec for the
1-2 projects with the highest hiring leverage for that specific role, and write
it to `ideas/<company>-<role>.md`.

The premise: another project that re-proves something `data/master-resume.md`
already proves is close to worthless. Leverage comes from the intersection of *what
this JD demands*, *what the company actually operates*, and *what Shubham
currently has no evidence for*. Find that intersection before proposing
anything.

## What this skill does not do

It doesn't touch `resume_faangpath.tex` or `data/`. Those change only when a
project is actually built and shipped, and `data/` only ever by the user's own
hand. This skill produces a plan;
`/tailor` consumes the results later. Keeping them separate is what stops
aspirational projects from leaking into the resume as claims.

## Inputs to read first

1. **The JD** at `$0`. If it doesn't exist, tell the user to paste it
   into `jds/<company>/<role>.md` and stop.
2. **`data/master-resume.md`** — the full ground truth of what Shubham can
   already prove. Read-only here as everywhere. Note that a claim marked
   `⚠ verify` is **not** proven evidence: it's an unmeasured number, which
   often means the gap is a missing benchmark rather than a missing project.
3. **Past gap notes**: `out/*/rationale.md`. The "Gaps" sections are a
   pre-computed list of recurring holes across every JD tailored so far. A gap
   that shows up in three rationales is worth far more to close than one that
   appeared once.
4. **`notes/verification-queue.md`** — the standing list of unmeasured numbers.
   `/tailor` is forbidden from reading `notes/`; this skill is the one exception,
   because "run the Heimdall benchmark" is frequently the highest-leverage item
   and proposing it twice is waste. **Nothing from `notes/` may appear in a draft
   resume bullet** — it exists here only to stop you proposing work already
   queued.
5. **The company itself** — see below. Do this before proposing anything.

## Understand the company, not just the JD

JDs are written by recruiters and describe a stack. The project has to survive
a conversation with an engineer who works there, so you need the domain
underneath the stack: what the company's systems actually do, what breaks at
their scale, what their engineers write about.

Use web search / fetch if available: the company's engineering blog, their
open-source repos, public incident writeups, conference talks. Two or three
searches is enough. If web tools aren't available, say so in the output and
reason from the JD plus general knowledge of that industry — but flag that the
domain read is unverified.

What you're extracting:

- **Domain primitives.** A payments company thinks in idempotency keys,
  ledgers, double-entry, reconciliation, settlement windows. An ads company
  thinks in auctions, budget pacing, fraud. A trading firm thinks in
  determinism, replay, tail latency. Name the primitives explicitly — a project
  that uses the company's own vocabulary reads as domain fluency, and the
  vocabulary is what interviewers probe.
- **Their real constraint.** Every serious engineering org is dominated by one
  or two constraints: regulatory correctness, tail latency, cost per request,
  multi-region consistency, developer velocity across hundreds of services.
  Build toward the constraint, not the feature list.
- **Scale shape.** 75M users and 13k engineers is a different problem than a
  30-person startup. Distributed-systems depth matters at the former;
  end-to-end shipping speed at the latter.

## Score the gaps before choosing

Make the reasoning explicit, because the whole value of this skill is choosing
the *right* thing to build. For each JD requirement, classify:

- **Proven** — a bullet in `data/master-resume.md` already backs it, and that
  bullet is not `⚠ verify`. Never build here.
- **Claimed but unmeasured** — a bullet exists but its number is `⚠ verify`.
  The fix is a benchmark, not a project. Cheapest possible close; say so.
- **Adjacent** — something close exists, but not the thing itself (e.g. AWS EKS
  when the JD wants GCP; in-memory caching when the JD wants Redis). Cheap to
  close; a small project or a focused extension of an existing repo often does
  it.
- **Absent and central** — the JD leans on it hard and there is nothing. This
  is where the leverage is. A project here changes the hiring decision.
- **Absent and unfixable** — years of experience, a specific degree, a domain
  requiring insider access. Note it, don't build for it.

Rank the "absent and central" items by how load-bearing they are in the JD, and
prefer ones that also close a recurring gap from past rationales. That's a
project that pays off across the whole job search, not just this application.

## Choose 1-2 projects, and justify the count

One project done to real depth beats two shallow ones, and the default should
be one unless a second is clearly earning its place. Propose a second only when
it covers a genuinely different axis — for example one systems-depth project
and one domain-credibility project — and say why the pair is better than
doubling down on the first.

Good projects for this purpose share some properties worth aiming for:

- **They produce a number.** Throughput, P99, error rate under fault injection,
  memory saved. A project with a measured number becomes a resume bullet; one
  without becomes a line nobody asks about. This is why the spec below demands
  a benchmark plan up front — retrofitting measurement onto a finished project
  almost never happens.
- **They fail interestingly.** The interview conversation is about what broke
  and how it was diagnosed. Prefer designs with a real failure mode (contention
  under concurrency, correctness under partition, cache invalidation) over ones
  that only have features.
- **They're finishable.** An abandoned repo is negative signal. Scope to
  something that reaches a demonstrable, benchmarked v1 in the time budget, and
  put the ambitious parts in an explicit "not building" list.
- **They speak the company's language.** Same primitives, same constraint.

Ask the user for a time budget before writing the spec if it isn't obvious from
the conversation — a two-weekend project and a two-month project are different
proposals, and guessing wrong wastes the whole output. This is also the moment
to check any assumption you'd otherwise bake in silently (existing repo to
extend vs. greenfield, languages they're willing to work in).

## Output format

Write `ideas/<company>-<role>.md` using this structure. Keep it concrete — this
document should be usable as the build's README on day one.

```markdown
# <Company> — <Role>: what to build

JD: `jds/<company>/<role>.md`. Written <date>. Time budget: <budget>.

## Company read
What they operate, the domain primitives, their dominant constraint, scale
shape. Cite sources (blog posts, repos) or mark the read as unverified.

## Gap analysis
A table: JD requirement | status (proven / claimed-but-unmeasured / adjacent /
absent-central / unfixable) | evidence or hole, citing the bullet id from
`data/master-resume.md` where one exists. Then one paragraph naming the single
highest-leverage gap and why.

## Project 1: <name>

**One-line pitch.** What it is, in the terms the company would use.

**Goal.** The specific capability it proves and the gap it closes. Tie back to
the JD line it answers.

**Why this company will care.** The domain mapping — their primitive, your
implementation of it.

**Scope — building.** Bulleted, concrete, each item independently demoable.

**Scope — explicitly not building.** Equally important; this is what keeps it
finishable.

**Stack.** Match the JD's stack where it's honest to do so — that's part of the
point. Note anything Shubham hasn't used before and how long it'll take to get
productive.

**Architecture sketch.** Components and the data/control flow between them, as
a short list or ASCII diagram. Enough that the first commit is obvious.

**The interesting failure mode.** What will break, why, and what fixing it
teaches. This is the interview story.

**Benchmark plan.** What to measure, how, against what baseline, and what
number would be good enough to put on a resume. Define this before writing
code.

**Milestones.** Numbered, each ending in something runnable, with a rough
time estimate summing to the budget.

**The bullet it earns.** A draft resume bullet in the house style, with the
metrics left as `<TBD>` placeholders to be filled from the actual benchmark —
never with invented numbers.

**Master-resume entry to add when done.** A ready-to-paste block in
`data/master-resume.md` §3 house style — heading with project name, family tags
(`[SDE] [BE] [INFRA] [AIE] [SRE] [DVO]`), an `id: proj.<slug>`, the stack/commits/
link line, and one bullet. Every number stays `⚠ verify` until the benchmark
actually runs, plus a matching unchecked line for
`notes/verification-queue.md`. Only the user pastes it in — `data/` is never
written by a skill.

## Project 2: <name>
Same structure — only if a second genuinely earns its place.

## What this still won't fix
The unfixable gaps, stated plainly, so the user knows what remains.
```

## Rules

- **Placeholders, never invented numbers.** Every metric in a draft bullet is
  `<TBD>` until a real benchmark produces it. The whole resume system depends
  on `data/master-resume.md` containing only true things; a fabricated target
  number that quietly becomes a resume claim is the one failure mode that
  actually damages the user.
- **Don't propose what already exists.** Check `data/master-resume.md` §3 first.
  If the best idea is an extension of an existing repo (Helios, SimpleMQ,
  Bifrost), say that — extending a real project is usually cheaper and more
  credible than starting a fifth one.
- **Be honest about cost.** If the highest-leverage project is a six-week
  build and the user has two weekends, say that plainly and offer the best
  version that fits, rather than pretending the small version closes the gap.
- **Never edit the resume or `data/`.** Proposals aren't evidence. Output goes
  to `ideas/<company>-<role>.md` and nowhere else.
