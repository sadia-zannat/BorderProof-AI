# Security self-assessment — V1 (NOT a financial-production approval)

## Implemented and tested

- Authentication: Argon2 password hashes for local seeded test users; HTTP-only SameSite=Lax sessions with random opaque cookie. Auth tested, session loss after logout tested.
- Session-side CSRF hash check for state-changing endpoints, including profile, case and file mutation. Origin allowlist on session mutations and login (test included for logout).
- Role-based and ownership controls on case/document endpoints; reviewer queue, auditor event log and admin summary are read-only and independently guarded server-side.
- Critical payment safety: **no payment execution API or provider adapter exists**, so V1 cannot accidentally execute live money transfers.
- Decimal validation rejects negative, infinite, NaN, excessive precision and values over a documented cap.
- Upload: 5 MiB cap, restricted extensions, PDF/PNG/JPEG signature checks, UTF-8 validation for text, disk storage outside static route, random generated paths, SHA-256 checksums. Stored documents are marked `STORED_UNVERIFIED`.
- Local event hash chain for simple trace linkage (NOT signed/anchored).
- Development fixtures must be opted into with a >=12-character user-defined seed password. Tests show no execution route is enabled.

## Limitations and known risks — DO NOT DEPLOY PUBLICLY

1. No signup/forgot password/MFA/email verification or secure self-service enrollment.
2. In-memory per-instance failed-login throttling is not distributed, is not persistent and may be defeated across workers/restarts. Needs rate limiting at gateway and shared store.
3. No automatic runtime key rotation or strong device/session management UI. Cookies require HTTPS with `COOKIE_SECURE=1` or `APP_ENV=production` in actual deployment.
4. CSRF token rotation on each `/auth/me` call can cause stale tokens in separate browser tabs; coordinate per-session CSRF across clients or adopt a suitable rotation policy.
5. No document malware scanning, PDF sanitization, at-rest encryption, retention schedule, institutional identity verification, PII classification, tenant-wide encryption isolation, or file content extraction. **Never upload real sensitive files in V1.**
6. Hash-linked audit events lack database append-only constraints, digital signatures, independent anchoring, canonical ordering under concurrency or a trusted timestamp. They are not tamper-proof.
7. SQLite used by default; not concurrency-tested for simultaneous production user financial operations. PostgreSQL path needs a driver and production migrations.
8. No BPCE, model prompt-injection defense, authorization-to-execution binding, quote expiry logic, sandbox execution state machine, idempotency under concurrency, AML/KYC, sanctions screening, compliance control or beneficiary ownership verification yet.
9. No penetration test, dependency CVE/SBOM audit, privacy review, security review or independent deployment validation. npm packages could not be installed in current environment.
10. No implemented provider settlement/chargeback/refund workflow. No financial guarantees or advice.
11. Standalone HTML preview uses inline JS/CSS for local convenience. Tighten CSP, introduce a build pipeline, secure hosting, and trusted origins before internet exposure.
12. Next frontend has not completed actual `npm run build`/browser E2E; a syntax parse is not a typecheck or security audit.

## Recommended V2/V3 threat prioritization

- P0: only trusted transaction authorization can permit simulation; prevent stale consent after recipient/quote changes.
- P0: differentiate uploaded untrusted documents/data from instructions; prevent exfiltration/tool privilege escalation.
- P0: hard tenant isolation and idempotency for every payment transition; race, retry and timeout scenarios.
- P1: rate limit, secure cookie deployment, secrets, file retention/scan and access audit.
- P1: ordered signed events and independent audit verification.

**Security verdict:** suitable for supervised local technical demonstrations of draft-case workflows only. Not production-ready for collecting real student identity or banking data.
