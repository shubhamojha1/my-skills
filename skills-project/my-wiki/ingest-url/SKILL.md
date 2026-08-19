---
name: ingest-url
description: Use when the user gives a URL (blog post, article, docs page) to add to this wiki, instead of a file in raw/ — fetches the page content, falling back past plain WebFetch when the site is JS-rendered or blocked, then runs the AGENTS.md ingest workflow.
---

# Ingest URL

## Overview

Same ingest workflow as `raw/` sources in AGENTS.md, except the source is a
URL and fetching it reliably takes more than one WebFetch call.

**Always read `AGENTS.md` at the repo root before ingesting** — it is the
source of truth for wiki structure, frontmatter, and the ingest steps below.
This skill only covers step 0: getting clean article text out of a URL.

## Step 0: Fetch the content

Try in order, stopping at the first one that yields real article text (not
nav/cookie-banner/JS-shell boilerplate):

1. **WebFetch the URL directly.** Works for static pages, server-rendered
   blogs, most docs sites.
2. **If the result is thin, mostly boilerplate, or empty** (React/Vue/Next
   SPA that WebFetch can't render), retry via a reader proxy that executes
   JS server-side and returns clean markdown/text:
   `WebFetch("https://r.jina.ai/" + original_url)`
3. **If the site blocks fetching entirely** (paywall, bot-block), try the
   Wayback Machine's latest snapshot: WebFetch
   `https://web.archive.org/web/2/<original_url>`.
4. **If all of the above fail**, tell the user which methods you tried and
   ask them to paste the article text directly.

Judge "thin" by content, not status code — a 200 response containing only
`<div id="root">` and script tags is a failure, not a success.

## Step 1: Stage it like a raw source

`raw/` is untracked and immutable-by-convention for files that arrive there.
For a URL ingest, write the fetched plaintext to `raw/` yourself first (pick
a slug filename, e.g. `raw/2026-07-07-some-post-title.md`) with the source
URL at the top of the file. This gives you a stable local copy to re-read
without re-fetching, and matches AGENTS.md's assumption that a source
document exists on disk.

## Step 2: Run the normal ingest

Follow `AGENTS.md` § Ingest exactly, with one adjustment: wherever it says
"list of raw source filenames," also record the **original URL** in the
page's `sources:` frontmatter and in the `wiki/sources/` summary page, since
`raw/` won't be pushed and the URL is the only durable pointer back to the
source.

1. Read the staged file fully.
2. Discuss key takeaways with the user before writing anything.
3. Create the summary page in `wiki/sources/` (include the URL).
4. Create/update entity pages for named things.
5. Create/update concept pages for key ideas.
6. Update `wiki/index.md`.
7. Append to `wiki/log.md` — `## [YYYY-MM-DD] ingest | <source title>`.
8. Commit per AGENTS.md's "After every operation" step.

## Common mistakes

- Treating a JS-shell WebFetch result as real content because it returned
  200 and some HTML — check that actual prose is present.
- Skipping the raw/ staging step and losing the fetched text if the
  conversation needs to re-check something later.
- Forgetting to put the URL in frontmatter/summary — without it, the source
  is unrecoverable once `raw/` is gone (it's not in git).
