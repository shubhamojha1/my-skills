# Resume writing and evidence gate

Read this file on every tailoring run. The goal is clear, personal, technically exact writing—not detector evasion.

## Evidence pass

For every rendered sentence, answer:

1. Which master bullet id or confirmed note supports it?
2. Which words describe the candidate's actual action rather than the team's general work?
3. Can the candidate explain the mechanism, measurement, and tradeoff in an interview?
4. Does any public link disagree with the model, stack, metric, dates, title, or scope?

If any answer is missing, narrow or remove the claim.

Never infer:

- production impact from a PoC;
- professional experience from a personal project;
- architecture ownership from tool usage;
- leadership from individual ownership;
- scale from counts of services, environments, fields, or endpoints;
- causality from two metrics that merely changed around the same time;
- exact latency, throughput, accuracy, or percentage without a confirmed measurement.

## Human-voice pass

Prefer short, concrete statements an engineer would say aloud. Keep the real system nouns and the awkward-but-specific detail that makes the work recognizable.

Rewrite or cut:

- `leveraged`, `utilized`, `spearheaded`, `robust`, `seamless`, `cutting-edge`, `innovative`, `scalable` without a scale;
- `responsible for`, `worked on`, `helped build`, `played a key role` when actual ownership is known;
- `not just X but Y`, `rather than X`, or a manufactured alternative not present in the evidence;
- strings of exactly three adjectives, benefits, or technologies added for rhythm;
- vague outcomes such as `improved efficiency`, `enhanced performance`, `ensured reliability`, or `optimized workflows`;
- inflated phrases such as `end-to-end` or `single source of truth` unless the scope is defined;
- bullets that are mostly a stack list;
- repeated `Owned`, `Designed`, or identical `action + mechanism + result` sentence shapes across the page;
- em-dash-heavy clauses, semicolon chains, and bullets longer than about 32 words without a strong reason.

Do not mechanically rotate synonyms. Repeating `service`, `cache`, or `request` is clearer than calling the same thing a platform, solution, layer, ecosystem, and framework.

## Bullet test

A strong bullet normally contains two of these, occasionally three:

- the boundary owned;
- the change or decision;
- the important mechanism;
- the measured consequence;
- the constraint that made the work difficult.

One bullet does not need all five. Split or cut if it does.

Good shape:

> Cut authorization overhead from 120 ms to under 5 ms by resolving identity once per session across 30+ endpoints and eight permission scopes.

Avoid:

> Spearheaded a robust, end-to-end authorization solution leveraging session-based caching to seamlessly optimize performance, enhance security, and improve scalability across the platform.

## Page-level test

- The first half-page must establish level, professional stack, and two credible outcomes.
- Projects must add evidence absent from Experience.
- Skills must summarize demonstrated tools, not act as a keyword reservoir.
- Every section must justify its fixed vertical cost.
- Read every bullet aloud. If it sounds like a polished summary rather than a remembered piece of work, return to the evidence.

## Detector claim

Never tell the user a resume cannot be AI-detected. State that the final pass reduces generic AI-writing signals and maximizes factual specificity. Do not run text through a detector or humanizer; neither establishes authorship or truth.
