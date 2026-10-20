# 45-module source and execution audit

VERIFIED WORKING applies only to the described local scope. It never means bank/identity verification or production readiness.

| # | Module | Status | Evidence and scope |
|---:|---|---|---|
| 1 | Landing | VERIFIED WORKING | Native Next.js and /demo public screenshots, navigation, reduced-motion fallback |
| 2 | Sign up / secure login | VERIFIED WORKING | Local student signup and login in both native browsers; server role/CSRF tests. Production signup disabled |
| 3 | Dashboard | VERIFIED WORKING | Real new-account case/document counts and generated case chart. Lists remain bounded |
| 4 | Student profile | PARTIAL | Persisted profile API and editable settings; exhaustive profile browser permutations not performed |
| 5 | AI financial copilot | EXTERNALLY BLOCKED | Six read-only tools and 14 mocked model contract tests; native unavailable-model 503. True Qwen inference pending laptop |
| 6 | Tuition Document Vault | VERIFIED WORKING | Fresh upload/download byte/hash equality, typed extraction, missing/conflicting fields; private local storage |
| 7 | University verification | PARTIAL | Synthetic registry comparison only. Public university guidance unavailable in retrieval, no institution attestation |
| 8 | Beneficiary verification | PARTIAL | Synthetic named payee/account match, contradiction guards. Real ownership unverified |
| 9 | Multicurrency | PARTIAL | Fresh GBP/USD/CAD processing and decimal arithmetic. No real multicurrency wallets |
| 10 | FX & fee comparison | PARTIAL | Two actual internal quote calculations plus Frankfurter reference adapter; public availability varies, no executable external quote |
| 11 | Payment route planner | PARTIAL | Bounded demo corridors and provider choice. No bank routing/availability search |
| 12 | Compliance navigator | PARTIAL | Demo rules and UNKNOWN legal eligibility. No licensed KYC/AML/sanctions source |
| 13 | Decision planner | VERIFIED WORKING | Deterministic safe-plan, latest document corrected. Explicitly non-LLM guidance |
| 14 | Approval center | VERIFIED WORKING | Explicit exact-quote student consent, single-use status, stale/source mutation rejection |
| 15 | Secure sandbox payments | VERIFIED WORKING | Actual internal simulator, DB, state and ledger; no external provider sandbox connection |
| 16 | Payment tracking | VERIFIED WORKING | Persisted COMPLETED/FAILED/UNKNOWN internal statuses and replay readback |
| 17 | Receipts / evidence | VERIFIED WORKING | Actual synthetic receipt and self-hashed export, balanced ledger, restart readback |
| 18 | Alerts | PARTIAL | Persisted user-scoped payment notifications API; no complete notification inbox UI |
| 19 | Refund / dispute guidance | PARTIAL | Local support records and export only; no bank dispute or refund |
| 20 | Settings | PARTIAL | Local preferences, locale/theme and profile form; broader account controls absent |
| 21 | Intent understanding | PARTIAL | Structured case fields and local tool-loop interface. General natural-language correctness not measured |
| 22 | Dependency-aware planner | PARTIAL | Deterministic dependencies and safe-plan; live LLM planning pending |
| 23 | Financial tool router | VERIFIED WORKING | Server allowlist, zero-argument schemas, owner scoping and rejected privileged calls; tested with mock model transport |
| 24 | Document intelligence | PARTIAL | English labelled TXT/PDF and optional real local Tesseract OCR. Not arbitrary-layout multilingual document AI |
| 25 | Evidence retrieval | PARTIAL | Private stored documents, synthetic registry and reference FX. No authenticated bank evidence |
| 26 | Provenance graph | VERIFIED WORKING | Seven-node/seven-edge recomputed quote graph and local hashes, verified API/legacy browser |
| 27 | BPCE | VERIFIED WORKING | Reparse/source-set/scope checks and fail-closed internal authorization; no proof of real-world efficacy |
| 28 | Quote validity | VERIFIED WORKING | Expiry guards and mutation checks. UTC offset preserved after SQLite reload |
| 29 | Country policy | PARTIAL | Deterministic demo corridor match. All real legal/provider eligibility remains unknown |
| 30 | Risk engine | PARTIAL | Rule flags/injection indicators only; known obfuscation and multilingual misses |
| 31 | Authorization | VERIFIED WORKING | Backend role checks, owner isolation, HttpOnly sessions, CSRF and transaction consent |
| 32 | Execution state machine | VERIFIED WORKING | Consumed approval, explicit unknown/failure recovery, serialized writes, uniqueness and status transitions |
| 33 | Independent verification layer | PARTIAL | Independent software kernel rechecks LLM/tool claims against local DB. No independent human/bank verifier |
| 34 | Audit trail | VERIFIED WORKING | Hash-chain append batching and writer serialization repaired; tampering detected. Unanchored local chain |
| 35 | Recovery / reconciliation | VERIFIED WORKING | Concurrent reconciliation debits once, immutable transfer amount, DB restart retention |
| 36 | Reviewer console | PARTIAL | Role-protected case queue and acknowledge/reject tickets; reviewer cannot override BPCE |
| 37 | Compliance workbench | PARTIAL | Demo policy/risk/review controls, real regulatory screening absent |
| 38 | Graph explorer | PARTIAL | Quote dependency graph is functional, no arbitrary graph search or database |
| 39 | Transaction audit explorer | PARTIAL | Role-scoped recent events and integrity check. No complete query/filter analytics suite |
| 40 | Fraud investigation | PARTIAL | Synthetic recipient/account conflict and provenance inspection. No validated fraud model |
| 41 | Attack simulation lab | VERIFIED WORKING | Role-protected untrusted-text heuristic probe and synthetic replay; not penetration certification |
| 42 | Evaluation dashboard | VERIFIED WORKING | Measured original synthetic proxy results, family selection and replay; clear proxy warnings |
| 43 | Baseline comparison | PARTIAL | Eight hand-coded policies and offline ablations. Standard/tool-using live LLM baselines not measured |
| 44 | Model / tool observability | PARTIAL | Persisted conversations, real DB tool-result digests and traces, actual failure events. No live Qwen trace yet |
| 45 | Admin console | PARTIAL | Protected counts and audit/review features. No full user lifecycle administration |
