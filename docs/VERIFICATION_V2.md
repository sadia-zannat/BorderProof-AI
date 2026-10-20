# V2 verification report — 19 October 2026

**Scope:** backend/core finance plus separately tested standalone browser preview, **not** a tested Next.js production build. Commands run in the active execution environment using Python 3.13, FastAPI/SQLAlchemy/pytest, Chromium and globally available TypeScript source parser.

| Verification actually executed | Observed result |
|---|---|
| `python -m pytest -q services/api/tests` | **38 passed**, 0 failed, approximately 10 seconds |
| `python tests/integration/verify_v1_migration.py` | **PASS:** actual V1 SQLite DB upgraded to v2 without losing seeded legacy user/case; re-running upgrade accepted |
| `python tests/e2e/test_financial_preview.py` | **PASS:** Chromium JS/DOM + real Uvicorn API requests bridged through Python: seeded case → synthetic invoice → field extraction → evidence investigation → synthetic quote → explicit approval → completed simulation → JSON decision receipt → English/Bangla/Chinese switch → mobile layout |
| `python tests/e2e/test_preview.py` | **PASS:** V1 regression: landing → login → create case → upload TXT → switch Bangla → dashboard → mobile → logout |
| `python scripts/check_locales.py` | **PASS:** 117 matching EN/zh-CN/bn-BD keys in original Next.js locale catalog |
| TS/TSX global TypeScript `createSourceFile` | **PASS:** 11 frontend TS/TSX files parsed; 0 syntax errors; **not** a typecheck/build |
| `node --check` on preview inline JS and V2 JS | **PASS:** no JavaScript parse errors |
| `python -m compileall -q services/api/app` | **PASS:** no Python compilation errors |
| Manual screenshot inspection | V2 desktop and mobile preview displayed; some technical strings remain English in translated interfaces |

### Tested backend behavior

Core session/role/CSRF, upload signature/content restrictions, document ownership, schema v2; deterministic invoice extraction and provenance, synthetic registry match, correct amount/currency, incomplete invoice, beneficiary mismatch, prompt injection as inert text, two synthetic provider rate and fee computations, explicit authorization, one-time consumption, stale quote/file/case rejection, document mutation rejection, duplicate idempotency and no double debit, ledger balancing, decline/timeout states and reconciliation, second student privacy, insufficient synthetic balance, offline OCR fallback and bounded explanatory copilot.

### Source of browser test limitation

Sandbox Chromium blocks normal network navigation to local URLs (`ERR_BLOCKED_BY_ADMINISTRATOR`). The tests load the actual local HTML into genuine headless Chromium and replace `window.fetch` with an HTTP bridge that makes **real** requests through a Python `requests.Session` to a running Uvicorn server. All authentication, database mutations and invoice processing are real local application operations, but this is **not** evidence that real user-browser networking/CORS, hosting or production Next.js works. Screenshots are of actual app rendering, not AI illustrations.

### Not verified

- `npm install`, Next.js production build, TypeScript semantic typecheck with project dependencies, Next browser E2E. Network restriction prevented retrieval of npm packages. Global TS syntax checks do not establish build correctness.
- Docker Compose runtime/image build; Docker CLI unavailable in this environment.
- External live LLM request; no credentials. Optional config path is code-only, untested.
- Frankfurter live reference FX reachability under a real network; no fabricated rate returned on errors.
- Wise/Airwallex external sandbox; **not connected**, no provider credentials or actual API transactions.
- Image OCR output, because it requires separate Tesseract executable opt-in; 503 absence path tested.
- Compliance, real beneficiary identity, sanctions, account ownership, real payment rails, fraud-model accuracy or transaction execution against real banks.
- Concurrent high-load tests, durability under process crash, formal property-based safety suite, pentest, accessibility certification, full Chinese/Bangla localization of technical metadata, independent performance benchmarks.

Do not conflate tests of deterministic local simulation with proof of production correctness, bank endorsement, actual user savings or financial compliance.
