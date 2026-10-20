# Resumed acceptance — 20 October 2026

Recovery succeeded from the existing modified V5.3 tree. All 669 pre-resume manifest entries matched, and the prior delivered ZIP matched SHA-256 `af743d4afdf25b187fd3bd60121065f39b6e3e7c1e2530c30b418744f39e5838`. No V5.2 overwrite occurred. Before any continuation, a complete recovery checkpoint was saved: **30,675,301 bytes**, SHA-256 `1e6e34e6ebef4a577b260b88f05551333eff99547b639876a7444345b93940ef` (673 manifested files).

The remembered 122 backend tests belong to Checkpoint B. Actual recovered final logs showed 130; this resumed clean run independently observed 130 again. Existing security, UI, database and research repairs were retained. One verification harness was extended: after both browser flows, restart FastAPI again, log in as every synthetic owner, read all six receipts through authorized API endpoints, and compare persisted transfers, balances and ledger before/after. Its initial query used the wrong column; that failure is preserved and the corrected query passed on rerun.

| Fresh check | Observed result | Evidence under `evidence/recovery_20261020/` |
|---|---|---|
| Backend/security/property suite | 130 passed, 0 failed/errors/skipped; 62.55 s, one deprecation warning | backend.log / backend.xml |
| Inherited browser regressions | 6 passed, 0 failed/errors/skipped; 30.68 s; Python HTTP bridge | legacy-browser-headless.log / XML |
| Native browser → API → SQLite | Both production Next and /demo pass; six locale checks, zero page errors | native_verified_execution/report.json |
| Financial persistence | 6 internal completed transfers, 12 ledger entries, sum 0.00; all 6 owner receipts read after final process restart; balances/ledger unchanged | final_restart_persistence + receipt JSON files |
| Fresh inputs | 10 native plus 10 OCR-run inputs; no SHA overlap with pre-resume shipped inputs | fresh-input-novelty.json + input manifests |
| Invalid/malicious inputs | Missing, contradictory, malformed and unsupported payee paths block/clarify; injected instructions cannot create quote | native report, backend negative tests |
| OCR | 10-case API run passed; actual local Tesseract amount extraction; text still unverified | ocr_execution/report.json |
| Frontend | Fresh npm ci, semantic typecheck, lint and production build pass; 11 lint warnings | frontend-commands.json, build.log, lint.log |
| Localization | 16 catalogs have key parity; EN/zh-CN/bn-BD mobile browser checks pass | locale-parity.log + real PNGs |
| Public FX | Actual HTTP 200; published 2026-10-19 reference, no invented fallback; not an execution quote | native report public_fx |
| Research | 300 original + 96 frozen authored cases reproduced; offline policy proxies only | research/ |
| Source revision | 113 application/data/test/script files match the clean tested copy; one harness extension this resume | tested-application-sha256.json |
| Render / PostgreSQL | Local YAML checks and PostgreSQL DDL compilation pass; runtime/platform execution unavailable | render-local-validation.json, postgres-ddl.log |
| Live Qwen | BLOCKED: connection refused, no model binary, zero inference responses | live_model_preflight.json |

Four new screenshots were visually reviewed: Next landing, internal receipt, Bangla mobile and Chinese /demo mobile. Premium navy/teal identity and reduced-motion fallback remain. Technical field names, status enums and some backend messages are still English; this is not a complete translation/accessibility certification.

Actual rerun BPCE rule-proxy holdout: 5/48 unsafe acceptances, 3/12 safe false blocks, injection acceptance 50%. Policy-only P50/P95: 14.907/32.209 microseconds on this run. New challenge holdout: 3/21 unsafe acceptances, 3/3 safe approvals. These are constructed, team/Work-authored offline measurements, not live model/bank performance or independent human validation. Original raw timings are preserved separately.

Failed attempts remain failures in `attempt_history`: six full-Chrome launch failures, one native full-Chrome launch failure, and the first extended harness run's SQL column error. The final headless reruns passed without weakening assertions. Default browser-download failure and runtime recovery are recorded separately from application tests.

**READY FOR LOCAL SIMULATION DEMO. NOT RELEASE READY for public/production finance or validated live-agent claims.** Remaining blockers: genuine user-local Ollama/Qwen results, provider credentials and separate authorization, verified financial/legal evidence, durable cloud DB/upload storage, PostgreSQL/Docker/Render and Windows execution, complete translation/accessibility, external human research validation and the final narrated competition video. No deployment, push, official submission, payment or paid inference occurred.
