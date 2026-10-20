# V2 changelog vs complete V1 source

- Preserved the V1 Next.js landing/dashboard/components, no-npm preview, backend and original 15 API tests.
- Implemented new `finance.py` domain service and `finance_routes.py` with additive SQLAlchemy entities for structured invoice extraction, investigations, synthetic quotes, approvals, durable simulation transfers, ledger entries, synthetic accounts and notifications.
- Implemented new version-2 schema marker and auto-additive migration from V1 (`schema_versions 1 → 2`); maintained all original tables.
- Added tagged synthetic beneficiary registry and UK tuition-invoice demo fixture, plus guarded fixture-attach endpoint.
- Added exactly anchored TXT/PDF field extraction, optional explicitly configured Tesseract OCR and user-visible field provenance.
- Added deterministic evidence checks and blocked/clarification states.
- Added two synthetic provider profiles with Decimal rate/fee math and 15-minute expirations. Read-only external reference-rate endpoint is separate.
- Added transaction-specific approval hashes and execution-time dependency guards, explicit simulation outcome selection, SQLite write serialization, idempotency and balanced BDT ledger.
- Added receipts, notifications, unknown timeout and simulator-only reconciliation.
- Added optional server-configured non-authoritative OpenAI-compatible explanatory copilot, with honest deterministic fallback.
- Added Next.js `FinancialWorkbench.tsx`, V2 financial dashboard navigation, local preview finance workflow, multilingual lab labels, responsive financial CSS and new actual-browser screenshots.
- Expanded backend suite to 38 passing tests including negative security/payment tests. Real browser E2E now proves a complete synthetic payment path.
- Updated Dockerfile for local fixtures and separated V2 architecture/security reports.

**Not done:** full BPCE independent kernel, real provider credentials/adapters, production sign-up/KYC/policies, benchmark comparisons, real tested Next.js production build. See security self-assessment for severity.
