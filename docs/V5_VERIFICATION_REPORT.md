# V5 independent verification report — 19 Oct 2026

## Observed results (actual commands in the authoring environment)

| Check | Executed command / approach | Observed result |
|---|---|---|
| All Python backend API/security/finance/research tests | `python -m pytest -q services/api/tests` | **84 passed, 1 skipped** (optional Hypothesis test suite not available) |
| Multilingual message parity | `python scripts/check_locales.py` | **119 exact keys in each** `en`, `zh-CN`, `bn-BD` |
| TS/TSX *syntax only* | `NODE_PATH=$(npm root -g) node scripts/check_frontend_syntax.cjs` | **14 source files, zero parse diagnostics**; NOT a production build or full typecheck |
| Old V1 database migration | `python tests/integration/verify_v1_migration.py` | PASS: user and case preserved |
| Old V2 database migration | `python tests/integration/verify_v2_migration.py` | PASS: preserved records, old approval blocked, new BPCE approval can complete internal simulation |
| Browser regression V1 | `python tests/e2e/test_preview.py` | PASS, executed individually in Chromium with actual FastAPI backend bridge |
| Browser regression V2 | `python tests/e2e/test_financial_preview.py` | PASS, executed individually; synthetic invoice-to-receipt flow |
| Browser regression V3 | `python tests/e2e/test_bpce_preview.py` | PASS, executed individually; student/reviewer/auditor controls |
| Browser regression V4 | `python tests/e2e/test_research_preview.py` | PASS, executed individually; research dashboard and scenario replay |
| Browser V5 | `python tests/e2e/test_v5_support_preview.py` | PASS, executed individually; plan/export/support plus EN/BN/ZH and mobile |
| Reproducible benchmark corpus | `python -m benchmarks.stupay_integritybench.corpus` | 300 project-authored synthetic cases (60 holdout) regenerated |
| Reproducible research evaluation | `python -m benchmarks.stupay_integritybench.evaluator --split holdout --out benchmarks/results` | 5/48 unsafe accepted; 9/12 legitimate completed for BPCE proxy; NOT real-world evaluation |
| PPTX read-back | `python-pptx` `Presentation(...)` | 12 readable, editable slides (with script-generated notes) |
| Silent demonstration capture | Chromium capture + `ffprobe` | Actual API-backed approximately **28.48 seconds** silent `.mp4`, **not** an edited/narrated ≤5 minute final demonstration |

## What these checks DO NOT establish

- **Next.js:** npm registry connection failed with `EAI_AGAIN`; no `npm install`, `npm run typecheck`, `npm run build`, WebGL rendering confirmation, or deployment smoke test has passed. Source syntax is not sufficient.
- **Browser technique:** tests bridge browser requests to actual local FastAPI via Playwright in the constrained container; they are not unrestricted TCP browser tests, accessibility certifications, or production-system E2E.
- **Docker:** Docker was not available and compose was not built/tested.
- **Hypothesis:** optional property suite skipped in this environment; do not count it as passed.
- **External fintech providers/LLMs:** no authorized Wise/Airwallex live sandbox keys, no payment initiation beyond internal simulation, no real LLM inference or agent baseline measurements.
- **Financial verification:** beneficiaries, institutions, quotes, balances and compliance rules are *synthetic*. This is not proof of lawful remittance, real counterparty ownership, security certification, or money movement.
- **Scientific independence:** benchmark cases, policy logic and labels were project-authored. Claims have self-evaluation bias and should not be extrapolated to live financial risk.

## Release gate and suggested independent reruns

Before a production claim or official external demo, install exact dependencies on an independent machine, execute `npm run typecheck && npm run build`, audit frontend/backend network integration, run all Python and Chromium tests, run static/security checks, test clean migration and Docker startup, and obtain independent external review. A local archive is not a submitted project.
