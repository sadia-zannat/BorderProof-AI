# BorderProof AI V5.5 — Independent repair and verification

Date: 2026-10-20. Starting artifact: original FinVeritas BorderProof AI V5.4 bilateral network ZIP, 717 archive entries; ZIP CRC passed. Original V5.4 archive is preserved independently of this V5.5 workspace. All inherited features, tests, architecture documentation, screenshots, and submission assets remain in this source tree.

## Scope and code changes (not a new financial product)

1. **Network document-set integrity repaired** (`services/api/app/network.py`): previously, network assessment re-read/verified only the newest extracted invoice. A deleted or changed **earlier** uploaded document was still reported as `REVIEW_REQUIRED`. Now, every case document must resolve inside private storage and match its recorded SHA-256; otherwise assessment is `BLOCKED_CONFLICT` with `DOCUMENT_SET_INTEGRITY_FAILED` and execution remains forbidden. This is a *local tamper check*, not a bank/notary signature.
2. **Invalid parser findings fail closed**: a parsed amount matching the intended case could hide a second, conflicting amount in that invoice. The network now consults `Extraction.issues_json`, returning `EXTRACTION_PARSER_SAFETY_ISSUES` for conflicting, invalid or overlong-line findings. Extracted document hash must also match the referenced newest document metadata. The status remains a planning/review decision; no bank verification is created.
3. Added two targeted API regressions (`test_network_v54.py`) reproducing changed older documents and conflicting amount fields. Updated package/API metadata to version 5.5.0 and added this documentation. **No changes** to financial transfers, synthetic simulator pricing, provider execution adapters, Ollama authorization policies, database schema or intended user routes.

## Fresh tests run in this environment

| Check | Observed result | Precise scope |
| --- | --- | --- |
| Backend complete `python -m pytest -q services/api/tests` | **139 passed; 1 skipped**, exit 0 | Temporary SQLite and FastAPI TestClient; two new regressions; optional Hypothesis property tests not installed |
| Backend core before repairs (separate test groups) | **96 + 41 = 137 passed**, exit 0 | Reproduced V5.4 previously claimed backend suite, before adding 2 repairs tests |
| Focused network tests after repairs | **12 passed**, exit 0 | Real application logic, TestClient, temp SQLite, mocked HTTP FX response in one test |
| Chromium preview browser suite `python -m pytest -q tests/e2e` | **6 passed**, exit 0 | Real browser DOM + Python HTTP bridge to live FastAPI/SQLite; **not** native Next.js browser/network E2E |
| TS/TSX syntax/transpilation + standalone JS + Python compile | **18 source TS/TSX files parsed with zero syntax diagnostics**, exit 0 | Static parser and Python source compilation only; **NOT** semantic TypeScript verification or Next build |
| `npm ci --ignore-scripts --no-audit --no-fund` | **FAILED**, exit 1 | Registry tarballs returned `EAI_AGAIN`; npm reported exit-handler error. `typecheck`, lint and Next build **not executed** for V5.5 |

Evidence log files: `AUDIT/evidence/v55/backend_full.log`, `preview_browser.log`, `static_typescript.log`, `npm_ci.log`, `network_regression.log`, corresponding `.exit` files. Earlier V5.3/V5.4 reports inside `AUDIT/` and `docs/` are historical evidence, not freshly repeated checks unless listed above.

## Clean-extraction acceptance

A separately packaged V5.5 candidate was opened in a fresh directory. ZIP member paths were unique and safe; archive CRC passed and **all 732 SHA-256 manifest entries matched**. From that independently extracted candidate, the full backend suite **again returned 139 passed, 1 skipped** and all **six HTTP-bridged Chromium E2E tests passed**. Logs: `AUDIT/evidence/v55/clean_backend.log`, `clean_browser.log`, and `candidate_clean_extraction_verification.json`. The final archive adds only these audit records/doc updates before re-packaging; application code was not changed after clean tests. Final archive CRC and manifest will be separately verified after packaging.

The Python language catalog checker passed English/Chinese/Bangla **135 keys per language**. The separate Node language checker could not start without local `apps/web/node_modules/typescript`; this is a **dependency availability block, not a JavaScript locale PASS**. See `AUDIT/evidence/v55/locales.log`.

## Remaining release gates — DO NOT CLAIM VERIFIED

- **Real Qwen3 tool calling:** no local Ollama model runtime in this environment. Mock/tool-contract tests do not establish true inference accuracy or agent reliability. Use the Windows PowerShell validation script on your actual Ollama installation.
- **Public FX:** live Frankfurter responses per currency pair, including BDT availability, were not received/verified. The mocked successful transport plus offline-failure tests cannot substitute for an actual fresh provider quote; reference rates are never executable prices.
- **Real finance:** 56 directional planning pairs / eight currencies, **zero confirmed operational bank settlement routes**; no provider account, KYC/AML, sanctions, beneficiary ownership or university attestation verified. Synthetic simulator transfers remain separate and labelled.
- **Production:** no V5.5 Next.js production build; no Docker/Postgres/cloud persistence/Render execution, Windows PowerShell execution, independent model evaluation, MFA, distributed rate limits or security penetration certification in this run. No deployment, Git push or paid service was performed.
- **Risk research:** inherited deterministic proxy/benchmark limitations remain, including unsafe acceptance and false rejections. Do not overstate research novelty or effectiveness.

## Reproduce on Windows

Follow `docs/V5_5_WINDOWS_BANGLA_START.md`. Use a clean-extracted package, real Python 3.12, Node 22+, and no sensitive real documents. Do NOT delete the old V5.4 ZIP/source/database. Submit only after checking live model, FX, Next browser, security, and actual competition rules independently.

## Verdict

**PASS for bounded, local technical checkpoint and existing preview workflows. NOT RELEASE READY for production financial services or real-money movement.** Confidence is limited by unavailable external and browser/build verification.
