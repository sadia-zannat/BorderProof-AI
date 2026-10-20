# V5 technical architecture and bounded reasoning

**Product:** BorderProof AI (FinVeritas) · **Competition:** International Track C, “AI as a Financial Participant” · **Domain:** synthetic cross-border tuition-payment assistance.

## Deployment architecture

1. `apps/preview`: fully static self-contained browser demo, authenticated calls to the real FastAPI server; browser session cookie is HttpOnly. Tested via Chromium with API-bridged real Uvicorn requests.
2. `apps/web`: Next.js 16 source for a multilingual, responsive, 3D-inspired student/reviewer/admin interface. It includes the V5 Evidence & support screen. Actual npm install/build and WebGL production performance have not been verified.
3. `services/api`: FastAPI, SQLAlchemy and Pydantic. SQLite used for local demo. Optional PostgreSQL needs independently verified drivers/concurrency review. Endpoints enforce logged-in principal and roles, CSRF for mutations, ownership for finance records.
4. `runtime`: locally persisted SQLite and private uploaded test documents, excluded from release archive. All synthetic bank data is held in versioned JSON fixtures.
5. `benchmarks`: immutable JSONL authored scenarios, holdout labels, executable policy proxies and results. Research endpoints only read local files, never permit transfer execution.
6. `submissions` and `docs`: editable defense and human-verifiable evidence package.

## End-to-end safety journey

1. Student creates an intent with institution, amount, target currency and destination country (all unverified until checked).
2. Upload accepts UTF-8 text, text PDFs and limited image types. Extraction is anchored label parsing, **not general financial document AI**; OCR is disabled by default.
3. Deterministic investigation checks case fields and beneficiary against **synthetic reference entries only**. A syntactic account number is not beneficial-owner verification.
4. Two internal mock providers compute quotes using hard-coded Decimal BDT conversion rates; rates are not market executable. Quotes have expiration times.
5. User consent includes specific quote/payment intent and is scoped to versioned evidence. The independent BPCE engine checks document integrity, re-extracted critical fields, synthetic beneficiary, quote conditions, policy version and dependency fingerprints.
6. Transaction simulator enforces signed in owner, transaction-specific approval, CSRF, idempotency constraints, state transitions and double-entry ledger balance. Responses label UNKNOWN timeouts rather than falsely calling them completed.
7. Receipt, local hash-chained audit and V5 export provide reviewable synthetic evidence. The export SHA-256 is **self-hashing**, not bank signed or external attestation.
8. Optional `safe-plan` chooses one bounded read-only next-step label from current stored case status; it executes no tool or money movement. `support/disputes` creates an internal guidance ticket only.

## Proposed research contribution and limitations

**BPCE** is a domain-specific engineering combination of evidence dependencies, field consistency, quote freshness and context-bound approval rechecks. Payment mandates, authorization binding, signatures and dependency checks exist in related literature and protocols (AP2, Visa TAP, agent-payment formal analyses). This project **does not claim invention of those primitives** or full AP2 interoperability. **StuPay-IntegrityBench** is an original synthetic evaluation artifact, not independent clinical/financial validation.

## SQL schema, migration and reproducibility

Schemas are initialized additively by `init_schema`: versions 1, 2, 3 and **4** (V5 local support table). Existing V2/V3 tables are retained; V5 records add `synthetic_support_cases` with case/transfer/owner FKs. `/api/v1/transfers/{id}/evidence-export` computes an output SHA-256 and never changes simulator balances. No production migration plan or database transaction isolation study is claimed. Reproducibility commands in root README.

## Frontend/interaction boundaries

Student, Reviewer, Auditor and Admin role views are implemented with backend role checks. Three locales (English, Simplified Chinese, Bangla) use mirrored message keys in Next.js, plus separate preview locale copy. Password seeding is development-only. Avoid treating the preview as a public, multi-tenant SaaS.
