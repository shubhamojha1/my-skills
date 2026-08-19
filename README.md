# my-skills

Claude Code skills from my machine setup — each one a `SKILL.md` (plus references/scripts where needed) that teaches an agent how to run a recurring workflow: machine operations, project-specific playbooks, and writing/research helpers.

Drop a folder into `~/.claude/skills/` (or your project's `.claude/skills/`) to use it.

## Skills

- **[demo](skills/demo)** — Generate an interactive, single-page browser demo of a systems project for deployment to a `/demo` endpoint. Staged checkpoints: concept and design tokens approved before the final artifact.
- **[graphify](skills/graphify)** — Turn any input (code, docs, papers, images) into a knowledge graph — clustered communities, god-node detection, BFS/DFS query tools, HTML + JSON + audit report.
- **[graphify-operations](skills/graphify-operations)** — Running, debugging, and judging output quality from graphify: version drift, junk god nodes, confidence collapse, zero token counts.
- **[harness-audit](skills/harness-audit)** — Audit or build out harness engineering infrastructure (AGENTS.md, ARCHITECTURE.md, PROGRESS.md, DECISIONS.md, verification commands) for an existing repo.
- **[harness-init](skills/harness-init)** — Establish harness engineering infrastructure on day one of a new project, before any feature code is written.
- **[helios-continuous-batching-campaign](skills/helios-continuous-batching-campaign)** — Project-specific playbook for continuous batching / scheduler / KV-cache work on an inference engine.
- **[human-voice](skills/human-voice)** — Catches AI-writing tells (inflated significance, "delve"/"underscore" vocabulary, rule-of-three lists, em-dash overuse) and rewrites toward a specific, plainly-stated voice.
- **[installing-portfolio-demos](skills/installing-portfolio-demos)** — Wire a self-contained demo file into a Next.js personal-site app as a live route.
- **[machine-build-and-env](skills/machine-build-and-env)** — Recreate or audit a dev environment: installs, PATH, toolchain versions, repo env setup.
- **[machine-change-control](skills/machine-change-control)** — The change-control doctrine other skills defer to before any state-changing action (commits, installs, deletions, deploys).
- **[machine-debugging-playbook](skills/machine-debugging-playbook)** — Triage playbook for errors, hangs, and unexpected behavior on the machine.
- **[machine-failure-archaeology](skills/machine-failure-archaeology)** — Check odd/broken things against a log of previously-settled battles before re-debugging them.
- **[machine-map](skills/machine-map)** — Lay-of-the-land orientation for a fresh session: what lives where, what's load-bearing, what's off-limits.
- **[machine-memory-and-docs](skills/machine-memory-and-docs)** — House style for session memory, AGENTS.md, and skill-library maintenance.
- **[machine-run-and-operate](skills/machine-run-and-operate)** — Session-start routing, dev-server health checks, output placement, end-of-task handover.
- **[machine-validation-and-qa](skills/machine-validation-and-qa)** — What counts as evidence-of-done per repo, before claiming work is fixed or passing.
- **[onthejob-operations](skills/onthejob-operations)** — Project-specific playbook for an incident-postmortem site: content, validation, ingest, taxonomy.
- **[onthejob-phase2-campaign](skills/onthejob-phase2-campaign)** — Open-sourcing, patterns index, discovery bot, and LLM ingest pipeline for the same project's Phase 2.
- **[pair-programming](skills/pair-programming)** — Navigator mode: the agent explains and guides but does not write the code, for learning-focused sessions.
- **[projects-atlas](skills/projects-atlas)** — Locate which repo owns a task, and its purpose/build/test entry, across a multi-project machine.
- **[research-methodology-and-frontier](skills/research-methodology-and-frontier)** — Turn a hunch into a testable claim; judge whether a result is real; plan experiments and benchmarks.
- **[resume-and-career-ops](skills/resume-and-career-ops)** — Resume tailoring against a job description, inventory YAMLs, LaTeX compilation, career-surface positioning.
- **[sysdesignvault-platform](skills/sysdesignvault-platform)** — Project-specific playbook for an MDX-based learning platform: concepts, widgets, data pipeline, progress tracking.

## Project-specific skills

Skills that live inside a single repo's own `.claude/skills/` — scoped to that project, not general-purpose.

### heimdall
- **[demo](skills-project/heimdall/demo)** — Local variant of the root `demo` skill, tailored to this repo.

### my-wiki
- **[ingest-url](skills-project/my-wiki/ingest-url)** — Ingest a URL (blog post, article, docs page) into the wiki via the same pipeline as `raw/` sources, with a fallback past plain fetch for JS-rendered or blocked sites.

### resume
- **[scout](skills-project/resume/scout)** — Given a job description, proposes the 1-2 portfolio projects worth building to become a credible hire for that role, chosen to patch gaps existing evidence can't cover.
- **[tailor](skills-project/resume/tailor)** — Tailors the LaTeX resume to a job description: infers the role family, selects tagged bullets, applies a section-order recipe, compiles with Tectonic, writes output + rationale.

### sysdesignvault
- **[brandkit](skills-project/sysdesignvault/brandkit)** — Premium brand-kit image generation: logo systems, identity decks, visual-world presentations.
- **[design-taste-frontend](skills-project/sysdesignvault/design-taste-frontend)** — Anti-slop frontend skill for landing pages, portfolios, and redesigns that don't look templated (v2, current default).
- **[design-taste-frontend-v1](skills-project/sysdesignvault/design-taste-frontend-v1)** — Original v1 taste-skill, preserved for exact-behavior backward compatibility.
- **[full-output-enforcement](skills-project/sysdesignvault/full-output-enforcement)** — Overrides default LLM truncation: complete code generation, no placeholders, clean token-limit splits.
- **[gpt-taste](skills-project/sysdesignvault/gpt-taste)** — UX/UI and GSAP motion engineering: layout randomization, AIDA structure, editorial typography, scroll-triggered animation.
- **[high-end-visual-design](skills-project/sysdesignvault/high-end-visual-design)** — Fonts, spacing, shadows, card structures, and animations for an agency-quality feel; blocks generic AI-design defaults.
- **[image-to-code](skills-project/sysdesignvault/image-to-code)** — Generates design reference images first, analyzes them, then implements the website to match, section by section.
- **[imagegen-frontend-mobile](skills-project/sysdesignvault/imagegen-frontend-mobile)** — Premium app-native mobile screen concepts and flows (image generation only, no code).
- **[imagegen-frontend-web](skills-project/sysdesignvault/imagegen-frontend-web)** — Premium website design-reference images, one per section, with composition and palette variety enforced.
- **[industrial-brutalist-ui](skills-project/sysdesignvault/industrial-brutalist-ui)** — Swiss typographic print fused with military terminal aesthetics for data-heavy dashboards and editorial sites.
- **[minimalist-ui](skills-project/sysdesignvault/minimalist-ui)** — Clean editorial interfaces: warm monochrome palette, typographic contrast, flat bento grids.
- **[redesign-existing-projects](skills-project/sysdesignvault/redesign-existing-projects)** — Audits an existing site/app and upgrades it to premium quality without breaking functionality.
- **[stitch-design-taste](skills-project/sysdesignvault/stitch-design-taste)** — Generates agent-friendly DESIGN.md files enforcing premium, anti-generic UI standards for Google Stitch.
