# Full 45-module scope — V5 evidence-based status

**PARTIAL is not complete.** V5 does not support real payment operations.  Every `IMPLEMENTED (SANDBOX ONLY)` item excludes production payment providers and verified beneficiary ownership. Next.js production build remains unverified.

| # | Module | V5 status | Actual implementation boundary |
|---:|---|---|---|
| 1 | Landing and Product Overview | PARTIAL | Next.js and local browser; Next build not independently verified |
| 2 | Sign Up and Secure Login | PARTIAL | Local login/logout; no public signup/MFA |
| 3 | Student Dashboard | PARTIAL | Working dashboard; financial lab tracks real local simulated state |
| 4 | Student Financial Profile | PARTIAL | Editable profile and synthetic BDT account |
| 5 | AI Financial Copilot | PARTIAL | Bounded deterministic explainer, optional configured non-authorizing provider LLM |
| 6 | Tuition Document Vault | PARTIAL | TXT/text-based PDF extraction with provenance; OCR opt-in only |
| 7 | University Verification Center | PARTIAL | Local synthetic university registry only; no real-world verification |
| 8 | Beneficiary Verification | PARTIAL | Exact synthetic registry matching, not account ownership |
| 9 | Multicurrency Workspace | PARTIAL | Synthetic BDT source and GBP/USD/CAD target planning |
| 10 | FX and Fee Comparison | PARTIAL | Two synthetic quotes and optional read-only dated public FX reference |
| 11 | Payment Route Planner | PARTIAL | One-case synthetic quote planning with legal eligibility unknown |
| 12 | Compliance Navigator | PARTIAL | Demo corridor allowlist and explicit unknown compliance status; no real legal policy corpus |
| 13 | Financial Decision Planner | PARTIAL | Guided evidence→quote→approval→simulation workflow |
| 14 | Payment Approval Center | IMPLEMENTED (SANDBOX ONLY) | Transaction approval sealed to versioned BPCE dependency snapshot, invalidation after new upload; no MFA |
| 15 | Secure Sandbox Payments | IMPLEMENTED (SANDBOX ONLY) | Persisted simulator state, balance, ledger and idempotency |
| 16 | Payment Tracking | PARTIAL | Transfer status history; no actual provider tracking |
| 17 | Receipt and Evidence Center | PARTIAL | Internal ledger receipts plus V5 self-hashed owner-scoped JSON export; not bank-signed |
| 18 | Alerts and Notifications | PARTIAL | Persisted status notifications, no delivery service |
| 19 | Refund and Dispute Assistance | PARTIAL | Tested local synthetic help-case creation/listing; **no actual refund, chargeback, bank contact or provider dispute** |
| 20 | Student Settings | PARTIAL | Profile, theme and language available |
| 21 | Intent Understanding Engine | PARTIAL | Structured tuition intent and read-only deterministic next-step planner; not autonomous LLM reasoning |
| 22 | Dependency-Aware Task Planner | PARTIAL | Deterministic flow only, not autonomous planner |
| 23 | Financial Tool Router | PARTIAL | Bounded fixed investigation tool sequence, not dynamic agent router |
| 24 | Document Intelligence Engine | PARTIAL | Anchored TXT/PDF field extraction; no arbitrary layouts |
| 25 | Evidence Retrieval Engine | PARTIAL | Local synthetic evidence + document provenance; no trusted web bank sources |
| 26 | Evidence Provenance Graph | PARTIAL | Persistent snapshot hashes and source dependency graph; not independently bank attested |
| 27 | BorderProof Consistency Engine | IMPLEMENTED (SANDBOX ONLY) | BPCE_V3_1 recomputes source, parser fields, synthetic beneficiary, quote, policy and document-set dependencies |
| 28 | Quote Validity Engine | PARTIAL | Quote expiry + BPCE scope revalidation and fail-close on modified recipients/fees/rates/source |
| 29 | Country Policy Engine | PARTIAL | Explicit static demo corridor rules and UNKNOWN real legal eligibility; no verified effective dated regulatory corpus |
| 30 | Financial Risk Engine | PARTIAL | Rule-based risk inspection and heuristic invoice instruction indicators; no calibrated fraud model |
| 31 | Authorization Service | PARTIAL | V3 seal-bound transaction-specific authorization, document-change invalidation; no step-up MFA |
| 32 | Execution State Machine | PARTIAL | Persisted demo statuses and duplicate prevention; no PostgreSQL distributed stress testing |
| 33 | Independent Verification Layer | PARTIAL | Execution path independently rechecks stored evidence/quote snapshot; database trust and external identity unverified |
| 34 | Audit Trail Engine | PARTIAL | Local hash-linked history and chain verifier; unanchored and database-admin rewritable |
| 35 | Recovery and Reconciliation Engine | PARTIAL | Explicit UNKNOWN reconciliation for internal simulator only |
| 36 | Reviewer Console | PARTIAL | Reviewer queue and acknowledgment/rejection for escalated test cases; cannot override financial hard blocks |
| 37 | Compliance Workbench | NOT IMPLEMENTED | Compliance investigation console not built |
| 38 | Evidence Graph Explorer | PARTIAL | Actual BPCE dependency graph and inspector in preview and Next.js sources; no full 3D graph |
| 39 | Transaction Audit Explorer | PARTIAL | Auditor history + real integrity verification API; no signed export/immutable store |
| 40 | Fraud Investigation Panel | PARTIAL | Student risk flags and reviewer tickets; no production anti-fraud investigations |
| 41 | Attack Simulation Lab | PARTIAL | V3 attack probe and 50 synthetic injection scenarios in V4; no real adaptive LLM tool red-teaming |
| 42 | Evaluation Dashboard | PARTIAL | Authenticated multilingual UI + actual 60-case synthetic holdout results; no real-world evaluation |
| 43 | Baseline Comparison | PARTIAL | 5 hand-coded simulated policies + 3 ablations; no actual LLM/AP2 benchmark |
| 44 | Model and Tool Observability | PARTIAL | Deterministic tool trace, stored transfer records and BPCE receipts; no provider tracing/cost system |
| 45 | Administration Console | PARTIAL | Admin read-only metrics, no provisioning lifecycle |

**Test evidence:** `services/api/tests/test_api.py` (V1 regressions) and `test_finance.py` (V2), `test_bpce_v3.py` (V3) and optional property tests; actual browser flows in `tests/e2e/test_financial_preview.py` and `test_bpce_preview.py`. V3 BPCE checks are implemented for **internal synthetic sandbox only**, not a production-authorized payment protocol.

V4 benchmark and V5 bounded evidence/support details: `benchmarks/README.md`, `docs/V4_RESEARCH_NOVELTY_AND_PRIOR_ART.md`, `docs/V4_SECURITY_LIMITATIONS.md`. All 45 modules remain in scope; none marked complete if real-world financial execution/evidence is missing.

## V5 support matrix addendum

V5 safe-plan is deterministic and read-only; it is **not** a real independently planned multi-tool financial agent. V5 local support records cannot affect simulated transfer state or trigger refund action. V5 export is self-hashed rather than bank-signed. Competing critical criteria remain unverified for provider execution, independent datasets, Next.js build and deployment.
