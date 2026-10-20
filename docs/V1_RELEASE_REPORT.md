# BorderProof AI — V1 Foundation release report

Release date: 19 October 2026. Track: Shenzhen FinTechathon International AI, Direction C.

## Summary

This is a runnable V1 **foundation**, NOT a completed cross-border financial agent or competition submission. The standalone no-npm browser interface was validated against real FastAPI endpoints; the Next.js frontend source was written but could not be dependency-installed or production-built in this restricted environment.

**Verified:** 15 FastAPI/security tests pass, a Chromium interaction run involving real bridged HTTP traffic passes, 116 English/Simplified Chinese/Bangla translation keys match, 10 TypeScript/TSX files parsed with zero syntax errors (not typechecked), Python code compilation passes. API creates SQLite tables with a V1 schema version and stores case/file records. Role controls, sessions and CSRF validated; live payments disabled.

**Blocked:** npm dependency install/Next.js build and normal Chromium network navigation due to sandbox networking restrictions; Docker unavailable. External provider integrations and real LLM unavailable/not implemented.

**Known incompleteness:** see full `FEATURE_STATUS_MATRIX.md` (45 entries) and `SECURITY_SELF_ASSESSMENT_V1.md`. Do not claim security certification, real payment readiness, independent benchmarking or verified beneficiary ownership.

**Demo test accounts:** student, reviewer, auditor, admin with `@borderproof.test` test emails, only created after setting a strong `DEMO_SEED_PASSWORD`. Details in root README. Do not submit actual student passports or private bank data to this code.

**Next action:** after user types `next`, continue into V2 without discarding working V1 source, implement real document parsing and financial agent workflow, including a persistent internal sandbox ledger. Retest prior V1 features.
