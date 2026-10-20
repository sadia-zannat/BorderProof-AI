# FinVeritas BorderProof AI V5.4 — Bilateral Financial Network

## Release classification

**LOCAL READ-ONLY ROUTE PLANNING: TESTED. NOT RELEASE READY for live finance, bank settlement, compliance claims, or public deployment.** This is a cumulative extension of the V5.3 audited tree. It has NOT initiated any real payment or contacted bank beneficiary verification rails.

## Scope implemented

- Region-to-currency catalog: Bangladesh BDT, China CNY, UK GBP, US USD, Canada CAD, Euro Area EUR, Australia AUD, Singapore SGD. Euro Area is a multi-country currency union; legal eligibility must be checked by member state.
- All distinct ordered pairs supported for case intake and bilateral reference research: **8 × 7 = 56** directed planning routes, with symmetric reverse paths. This **does not** mean 56 operational payment routes.
- Schema V6, additive columns `origin_country`, `source_currency`, `destination_country`, `destination_currency`, while `currency` keeps the invoice currency. Existing V5.3 cases keep default Bangladesh source, BDT, and prior target currency; previous ledger tables remain untouched.
- Real authenticated FastAPI user-scoped cases, read-only `/network/corridors`, optional public `/network/reference`, and auditable `/network/cases/{id}/assessment` plus assessment history.
- Actual invoice extraction comparisons for institution/amount/currency; stale extraction/new document detection; on-disk document-hash verification; bounded suspicious-instruction patterns; unverified beneficiary evidence clearly labeled.
- `inspect_bilateral_route` is one new read-only model-callable tool (7 total); no new payment or authorization capabilities are delegated to the LLM. User's local Qwen3 must be run to verify real model tool selection.
- Next.js interactive selectable WebGL globe with route arc plus no-WebGL SVG fallback; standalone `/demo` displays interactive SVG route network and the same real FastAPI APIs.
- Network FX example **does not** use the old internal synthetic provider pricing. Each pair request directly queries `https://api.frankfurter.dev/v2/rate/{base}/{quote}` and returns provider response hash, rate, publishing date and retrieval timestamp, or HTTP 503 on unavailable/stale sources. Published central-bank/official-source reference rates are NOT transfer quotes.

## Boundaries and safeguards

- Provider credentials, bank ownership verification, actual tuition institution attestation, KYC/AML and legal corridor eligibility are **NOT CONNECTED** and remain UNKNOWN.
- Existing internal local synthetic sandbox continues to exist **only for its old explicitly labeled compatibility workflow**. New cross-border routes MUST NOT be assigned a synthetic executable quote; a server-side guard rejects unconfigured origin/currency pairs.
- `REFERENCE_ONLY_NOT_AN_EXECUTION_QUOTE` rate is a read-only observation; it lacks provider spreads, fees and guaranteed settlement terms. USD/GBP/etc cross rates are not proof that a consumer is eligible to remit funds.
- A synthetic document, matching bank account string, or file hash is not an independently verified bank beneficiary. The application does not give such claims.
- Denied external data => explicit 503, no fabricated latest FX rate. Denied provider => `NOT_CONNECTED`, no fake bank transaction ID.
- Student-created case amounts and currency preferences are unverified self-declared inputs. Currency mismatches are recorded for human clarification.

## Test evidence / honest classification

- Focused bilateral API tests: 10 PASS in a fresh in-memory/temporary-SQLite suite, including 56 actual case writes, direction symmetry, FX transport contract **with clearly mocked network responses**, offline fails-closed, access control, suspicious user document and stale-evidence blocking.
- Original V5.3 test files executed independently during migration work: `test_api.py` 15 passed, `test_bpce_v3.py` 25, `test_finance.py` 23, `test_local_agent_v51.py` 12, `test_research_v4.py` 10, `test_v5_release.py` 11, `test_work_v53.py` 31 (137 total including 10 new network tests). Optional Hypothesis module not installed in this environment, not counted as passing.
- Real FastAPI startup/health observed HTTP 200. Current V5.4 standalone `/demo` UI interacted with via real HTTP bridge into live FastAPI and SQLite: login, network, reverse, new China→Bangladesh case creation, and persisted `REVIEW_REQUIRED` evidence check. Logs in `docs/V5_4_BROWSER_BRIDGED_REPORT.json`.
- Chromium direct localhost/file navigation returned `ERR_BLOCKED_BY_ADMINISTRATOR`. Therefore **native browser network E2E remains unverified in this environment**. No browser result is silently promoted to native.
- Static Next.js TS/TSX parsing: 17 files, 0 parser errors; standalone JS `node --check` passed. Next.js semantic `tsc`, Next.js `npm run build`, WebGL rendering, and Render/PostgreSQL live runtime **NOT verified for V5.4** because package registry/dependencies could not be installed here. Previously verified V5.3 build does not count for V5.4.
- External Frankfurter API (live outgoing HTTP) and real Qwen3 response from this environment: **NOT VERIFIED**. Both have real executable code and must be tested on the student's connected Windows PC.

## Release decision

**NOT RELEASE READY** for production or unconditional financial-availability claims. Ready for carefully labeled local software demonstration after Windows API, network provider and Qwen tests. Do not deploy or publish without explicit user approval.

## Key files

`services/api/app/network.py`, `services/api/app/network_config.py`, `services/api/app/schemas.py`, `services/api/app/models.py`, `services/api/app/db.py`, `services/api/app/finance.py`, `services/api/app/local_agent.py`, `apps/web/components/GlobalNetwork.tsx`, `apps/web/components/GlobalNetworkGlobe3D.tsx`, `apps/preview/index.html`, and `services/api/tests/test_network_v54.py`.

## Minimum checks before deployment

1. `pip install -r services/api/requirements-lock.txt`; run full `pytest services/api/tests` on the *clean-extracted* package; inspect security failures and benchmark quality.
2. `cd apps/web && npm ci && npm run typecheck && npm run lint && npm run build` with real registry, then `npm run start`; verify WebGL globe and no-WebGL fallback in desktop/mobile browser.
3. Open `http://127.0.0.1:8000/demo`, register locally and test a NEW unseeded CNY/BDT case; upload a NEW invoice and verify the `REVIEW_REQUIRED` or blocked result.
4. Request two genuinely sourced FX observations (including BDT); inspect `published_date`, `source_url`, provider and `status`, and test offline/HTTP error. If live pair unavailable, leave UNAVAILABLE.
5. Start `ollama`, model `qwen3:4b`; run `scripts/run_live_ollama_validation.ps1` with actual Ollama inference and check sanitized evidence. A failed tool-selection scenario is a failure, not a success.
6. No deployment without verified production database migration, persistent upload storage, credential reviews, independent bank/provider rails, and approval. An internal simulator test is not legal or production payment authorization.
