# Frontend production verification

Node 24.19.0, npm 11.9.0, Next.js 16.4.2 resolved from the supplied ^16.2.0 range. A committed package-lock now pins the tested tree. `npm ci --ignore-scripts`, semantic `npm run typecheck`, configured `npm run lint`, `npm run build` and actual `npm run start` were exercised, including real same-origin API cookies. Exact clean commands/logs are in `evidence/clean/`.

The production TypeScript failure was a real missing `cases_heading` key. It now uses `case_heading`. No `ignoreBuildErrors` flag or TypeScript-disable workaround was used. ESLint reports existing React mount-initializer performance warnings; they remain visible and are configured as warnings, not described as fixed. Basic unused imports and config warnings were removed.

Next.js proxies `/api/*` to API_INTERNAL_URL (default http://127.0.0.1:8000), eliminating the localhost-versus-127.0.0.1 cookie mismatch. The preview uses its real same-origin FastAPI routes. Public pages hide the workspace sidebar. Student-only navigation is role-aware. Deep-linked /demo registration and mobile financial selects were repaired.

16 localized catalog objects and the original 135-key catalog passed AST/key parity. Native EN/zh-CN/bn-BD switching and 390-pixel widths passed. Local OFL font subsets prevent missing glyphs for the UI. Technical API error text, raw statuses and some progressive-detail strings still use English; this is not a claim of complete translation. Arbitrary future CJK text may require a complete installed font beyond the shipped UI subset.

Reduced-motion/static globe fallback was exercised. Real GPU WebGL interaction on the user's hardware is not certified by that test; the source preserves the Three.js globe and now checks WebGL2 availability. Keyboard-focus CSS and labels exist, but no comprehensive WCAG or screen-reader certification was performed.

Resumed clean verification (2026-10-20): see [current acceptance](RESUMED_ACCEPTANCE_20261020.md) and `evidence/recovery_20261020/`. Earlier measurements above are preserved with their original scope.
