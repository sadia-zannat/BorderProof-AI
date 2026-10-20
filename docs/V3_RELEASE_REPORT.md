# BorderProof AI V3 Release Report — 2026-10-19

## Correct claim

**Functional, independently exercised Python/FastAPI internal tuition-payment simulator with V3 BPCE scope binding and role-based risk/quote/audit inspector.** This is not a bank-integrated finance product or proven production payment security.

## Major working features

1. Locally persisted approval and evidence-seal relationship; independent invoice/document/beneficiary/quote/corridor consistency checks.
2. Proactive approval invalidation on an added case document and execution-time invalidation after modified financial metadata.
3. Tamper-evident *local* audit verification (not signed or externally anchored).
4. Student-side risk / graph / review request; reviewer decision and auditor proof checks; real API-backed browser workflows.
5. All V2 internal-sandbox quote, ledger, timeout/reconciliation and receipt paths retained.

## Verified vs not verified

See `VERIFICATION_V3.md` for actual commands, test counts and limitations. Hypothesis property tests are present but could not run in this network-restricted environment. Next.js production build, Docker, production performance and real external systems were not tested.

## V4 focus (NOT yet implemented)

Actual StuPay-IntegrityBench corpus + independent labels; reproducible baseline and ablation comparisons; false rejection and injection miss measurement; advanced evidence visualization; performance and security regression workloads; source/prior-art traceability. Work must continue from **this entire V3 source tree**, not a new blank project.
