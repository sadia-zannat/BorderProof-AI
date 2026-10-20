# Verified V1 results — 19 October 2026

**Environment:** Python 3.13.5, FastAPI 0.128.2, SQLAlchemy 2.0.50, Uvicorn 0.48.0, pytest 9.0.2, Node 22.16.0, Chromium headless available, TypeScript global parser available. The requirements intentionally target broad compatible ranges; this is not a pinned supply-chain lock file.

## Tests actually executed

| Check | Command / observation | Outcome |
|---|---|---|
| Backend unit/security/integration | `cd services/api && pytest -q` | **15 tests passed** |
| Python compile | `python -m compileall -q services/api/app` | **Passed** |
| Locale parity | `python scripts/check_locales.py` | **116 exact matching keys** per locale (EN/zh-CN/bn-BD) |
| TS/TSX syntax parsing | TypeScript global `createSourceFile` over `apps/web` | **10 files parsed, 0 syntax diagnostics**; **not a typecheck** |
| Browser rendering and interactions | `python tests/e2e/test_preview.py` | **Passed**: Chromium real DOM/JS -> login -> create real case -> upload actual TXT -> switch Bangla -> dashboard -> logout; real Uvicorn requests bridged through Python because sandbox blocks native Chromium navigation |
| Saved screenshot | `docs/V1_BROWSER_SCREENSHOT.png` | Rendered from actual browser UI state, not generated design mockup |
| ZIP checksum/integrity | run at archive generation | see release report outside source |

## Verification blocked / not attempted

- npm registry DNS resolved unsuccessfully (`EAI_AGAIN`); `npm install` and `npm run build` **NOT RUN**. Next frontend has not been runtime tested, typechecked with installed dependencies or smoke tested end-to-end.
- Chromium normal navigation to localhost and even intercepted HTTP routes is blocked by environment policy: `net::ERR_BLOCKED_BY_ADMINISTRATOR`. A browser DOM/JS run with Python-bridged real Uvicorn requests passed. This is meaningful but not identical to a normal browser networking test.
- `docker` executable not installed; Docker image/compose build **NOT RUN**.
- No penetration test, accessibility audit, performance benchmark, payment throughput, provider integration or security certification performed.

## Passing backend scenarios

1. Public health and verified disabled-execution state.
2. Cookie login/me/CSRF/logout and session invalidation.
3. Invalid login rejection.
4. Case draft persistence and CSRF negative test.
5. Invalid monetary amount/currency rejection.
6. Reviewer/auditor/admin role restrictions and unauthorized mutation rejection.
7. Document upload, invalid PDF rejection, SHA-256 metadata and protected readback.
8. Student isolation on another student's case.
9. Origin mismatch rejected.
10. Payment execution route does not exist.
11. Profile update is persisted.
12. Standalone `/demo` HTML route is served.
13. Uploads exceeding 5MB are rejected.
14. A second student cannot access another student's documents.
15. Schema version 1 is initialized.

No fake transaction IDs, success counters or security accuracy percentages are claimed.
