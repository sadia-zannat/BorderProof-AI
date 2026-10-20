# V3 Verification Record — 19 October 2026

## Test environment and evidence

- Python 3.13 in isolated execution environment; original Windows README targets Python 3.12.
- FastAPI + real SQLite in temporary directories. No fake/LLM-produced security performance metrics.
- Chromium Playwright runs actual source HTML and JavaScript. Due to the sandbox's browser navigation restrictions, normal `fetch` is bridged to **real** Uvicorn HTTP requests via Python requests.Session.
- New V3 screenshot files: `V3_BPCE_STUDENT_SCREENSHOT.png`, `V3_BPCE_MOBILE_SCREENSHOT.png`, `V3_BPCE_REVIEWER_SCREENSHOT.png`, `V3_BPCE_AUDITOR_SCREENSHOT.png`.

## Actual checks

See source tests for assertions. The final ZIP verification script re-runs tests from an independently extracted copy.

| Test | Observed outcome |
|---|---|
| `python -m pytest -q services/api/tests` | **63 passed, 1 skipped** (Hypothesis optional dependency unavailable) |
| `python tests/e2e/test_financial_preview.py` | **PASS** V2 payment journey regression against V3 source |
| `python tests/e2e/test_bpce_preview.py` | **PASS** V2 payment journey + student BPCE evidence/risk + reviewer acknowledgment + auditor audit check + EN/Bangla/Chinese + mobile |
| `python tests/integration/verify_v2_migration.py` | **PASS** old V2 database records preserved, old authorization fails closed, newly sealed V3 sandbox execution works |
| `python -m compileall -q services/api/app` | **PASS** |
| `python scripts/check_locales.py` | **PASS** 117 existing Next.js translation catalog keys across 3 locales; separate BPCE UI has tri-lingual labels |
| JavaScript parse check via `node --check` | **PASS** preview inline script |
| Global TypeScript parser for TS/TSX | **Syntax parsed**; not a semantic typecheck/Next production build |

## Deliberately unverified

- npm install / Next.js production build: npm registry inaccessible and package cache incomplete (`ENOTCACHED` for `@react-three/drei`). Do not advertise compiled Next frontend.
- Docker image build: Docker not available.
- Property-based Hypothesis tests: code present in `test_properties_optional.py`, dependency install failed; it was **skipped**, not passed.
- Live external financial provider sandbox, real banking approval, compliance, KYC, sanctions screening, real provider readback, production OCR, optional LLM inference and external attestation all **not tested/connected**.
- Large-scale concurrency stress, formal threat coverage and penetration certification not performed.

Passing deterministic local fixture cases validates those cases only; it does not establish quantified security accuracy, novelty, or real-world payment authorization.
