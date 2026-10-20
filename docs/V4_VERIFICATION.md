# V4 verification — observed local commands (19 October 2026)

Observed from development tree:

- `python -m pytest services/api/tests -q --disable-warnings` → **73 passed, 1 skipped** (Hypothesis optional not installed). These include all prior V1/V2/V3 backend tests and the V4 research API/corpus/ablation tests.
- `python -m benchmarks.stupay_integritybench.corpus` → actual 300 synthetic cases + 300 labels + SHA-256 manifest.
- `python -m benchmarks.stupay_integritybench.evaluator --split holdout --out benchmarks/results` → **60 evaluated holdout cases, 8 policies**, real result JSON + CSV. Details and methodological caveats in `benchmarks/README.md`.
- `python tests/e2e/test_research_preview.py` → PASS actual Chromium DOM: login, chart, 8 baselines, filter/replay against FastAPI, BN/EN/ZH and mobile screenshots.
- `python tests/integration/verify_v2_migration.py` → PASS after restoring separately archived prior V2 source alongside V4: V2 data preserved, old approval rejected, new sealed payment simulated.
- `node` TypeScript compiler syntactic parse: **13 TS/TSX files, 0 parse errors**. **Not semantic typecheck.**
- `python scripts/check_locales.py`: **118 translation keys each** in EN/zh-CN/bn-BD; V4 research screen has additional local translated strings.

**Not verified:** Next.js dependency install, actual production build, Docker container execution, production-scale concurrency, human security penetration test, real provider/LLM integration, external academic replication.

**Browser method caveat:** System Chromium blocks direct localhost navigation in this environment. Chromium renders actual HTML/JS and bridges fetch requests to live Uvicorn+SQLite using Python `requests`. This proves relevant interactive DOM and API behavior under the bridge, NOT normal deployed browser networking / CORS or Next.js production.

The V4 source manifest and clean archive verification results are appended to `V4_RELEASE_REPORT.md` at packaging time.
