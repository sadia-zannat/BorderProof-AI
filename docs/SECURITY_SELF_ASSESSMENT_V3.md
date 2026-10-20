# V3 Security Self-Assessment

Status: **locally tested internal synthetic sandbox**. Assessment date: 2026-10-19.

## Controls tested

- Authenticated cookie session, CSRF mutation checks, owner-scoped data and role boundaries.
- Independent BPCE snapshot proof at quote creation, authorization and execution.
- SHA-256 file readback, deterministic source reparsing, issuer/beneficiary exact synthetic registry checks and evidence-set invalidation.
- Transaction-specific explicit approval, expiry, no legacy-approval reuse, idempotency and sandbox ledger invariants.
- Role-restricted human review record; acknowledgment never bypasses backend hard blocks.
- Audit hash-chain verification and tamper detection against local record edits/deletions.
- Read-only tool-claim inspection and injection-indicator probe; neither can authorize or execute.

## Known gaps / explicit residual risk

**Critical if used outside internal demo:** real beneficiary ownership not verified; no production processor integration; financial regulations and sanctions not validated; no licensed money movement. The application must NEVER be deployed as a real payment rail without substantial security, regulatory and institutional review.

**High:** no step-up MFA, login lockout local-process only, local disk upload encryption not provided, no signed externally anchored audit, trust in SQLite root database and fixture data, incomplete LLM prompt-injection coverage, no independent external provider settlement reconciliation, no multi-tenant organization boundaries.

**Medium:** Next.js production build not run in restricted environment; Docker not run; no formal runtime stress/penetration test; incomplete non-English technical metadata; OCR image/PDF processing not fully tested; optional LLM credentials/read-only reference FX not exercised here; dependency lockfiles absent.

**Other:** No public signup, no secrets in repo, no logged real credentials. Optional OCR requires external local executable. Real sanctions endpoints deliberately not called; making a sanctions "clear" statement based on a demo fixture would be misleading.

## Evidence, not assurance

`python -m pytest -q services/api/tests`, `python tests/e2e/test_bpce_preview.py`, and `python tests/integration/verify_v2_migration.py` generate reproducible local evidence. A passing local test suite is not an accreditation or certification.
