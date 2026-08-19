---
name: installing-portfolio-demos
description: Use when a self-contained project demo .jsx file (e.g. from the /demo skill) needs to go live as a route on the personal-site Next.js app — moving a demo out of its source repo into personal-site/app/demo/<slug>, wiring the page route, and verifying it compiles and serves.
---

# Installing a portfolio demo into personal-site

## Overview

`personal-site` (`C:\Users\subha\Projects\personal-site`) is a Next.js App Router site with `strict: true` TypeScript. Project demos are generated elsewhere (often via the `/demo` skill, output as a single `.jsx` file) and need a `/demo/<slug>` route here. This skill is the mechanical install step, not the demo-authoring step.

## Steps

1. **Target location:** `personal-site/app/demo/<slug>/`. Create it if missing.
2. **Move the file in as `.jsx`, not `.tsx`.** Keep the original extension. `tsconfig.json` has `strict: true`, and the generated demos are untyped JS (implicit `any` everywhere) — renaming to `.tsx` produces dozens of `TS7006` errors. `.jsx` files aren't in tsconfig's `include` list, so `tsc --noEmit` skips them entirely while Next.js still compiles and serves them fine.
3. **Add `"use client";`** as the first line if missing. App Router defaults to server components; these demos use `useState`/`useEffect` and need the directive.
4. **Add a `page.tsx` wrapper** in the same folder:
   ```tsx
   import DemoComponent from "./DemoComponent.jsx";

   export default function Page() {
     return <DemoComponent />;
   }
   ```
   Import with the explicit `.jsx` extension. No `@ts-expect-error` needed — the import target isn't type-checked.
5. **Verify types:** `npx tsc --noEmit -p tsconfig.json 2>&1 | grep -i <slug>` from the personal-site root. Expect no output.
6. **Smoke test:** start `npm run dev` in the background, `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/demo/<slug>`, expect `200`, then check the dev log for compile errors before killing the server (`taskkill //F //IM node.exe` on Windows).
7. Leave committing to the user unless they've asked for it — this only moves/creates files.

## Common mistakes

- Renaming the demo to `.tsx` "for consistency" — triggers the strict-mode error wall above. Don't.
- Forgetting `"use client"` — hooks silently fail or Next throws a server/client boundary error.
- Not curling the route after `npm run dev` — Turbopack errors only surface on first request to that route, not at server start.
