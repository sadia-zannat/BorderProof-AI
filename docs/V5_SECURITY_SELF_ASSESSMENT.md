# V5 security self-assessment — synthetic only

## Trust and role tiers

| Tier | Allowed scope | Guard |
|---|---|---|
| Unauthenticated visitor | Landing, public configuration, health only | Backend auth for all case, finance, review, research data |
| Student | Only own cases, documents, quotes, approvals, transfers, support and evidence export | Session + CSRF for mutations, owner equality for reads and writes |
| Reviewer | Synthetic review queue, bounded acknowledgment/rejection | Backend role gates; cannot override payment BPCE |
| Auditor | Read local audit events/integrity view | Role gate; cannot initiate student transfer |
| Admin | Review/audit/summary views | Role checks; does not grant real provider execution |
| LLM optional (configured) | Explanation text only; not financial authorization or tools | No privileged tokens passed to model; fallback on failure |

## Tested controls and residual risks

| Control | Implemented level | Residual |
|---|---|---|
| Login, Argon2, HTTP-only session | Local testing | No MFA/account enrollment/SSO, no distributed lockout |
| CSRF + origin check | FastAPI mutations | No externally audited adversarial browser deployment |
| Tenant isolation | Query scoping and tests | Not independently penetration tested |
| Quote/evidence binding | BPCE backend checks | Local DB/trusted synthetic fixture can be altered by host admin |
| Quote expiry and invalidation | Enforced local tests | No signed external provider quote |
| Idempotency and state checking | SQL uniqueness + application guards | SQLite and multi-worker parallelism not stress-tested |
| Tool-claim integrity | Persisted simulator readback | No real-provider authenticated callbacks |
| Document security | Extension/signature checks, 5MB bound, hash on read | No malware scanning, isolation or PDF sandbox guarantees |
| Prompt injection | Untrusted text not promoted to authorization; limited regex indicators | 50% of held-out synthetic injected cases evade proxy regex filter; fail-open risk in proxy benchmark, not a comprehensive classifier |
| Audit chain | Hash-linked local events; verification endpoint | No signing/HSM/anchoring, DB administrator can replace/recompute chain |
| V5 evidence JSON export | Owner-only read, no-store, self-hash | SHA-256 is not a digital signature or legal proof |
| V5 dispute cases | Local status and guidance only | No refund, claims processing, regulated support workflow |
| Production-mode guard | Explicitly refuses demo seed in production | Does not create production-grade authentication |

## Known risks ranked

**Critical for real deployment:** Real beneficiary verification absent; no regulated payment rails/provider authorization, compliance engine, funds custody, MFA or external audit. **High:** standalone demo relies on seeded synthetic accounts and SQLite; PDF and OCR tools need adversarial security review; multi-worker concurrency and CSRF/CORS configuration must be reviewed for a real public domain. **Medium:** development rate limiting is in-memory; synthetic heuristic injection scanner incomplete; local audit reversible by DB admin; Next.js build not verified.

## Adversarial scenarios in tests

Changed amount/beneficiary/invoice fields, new document invalidation, stale quote, fake provider success, attempted replay/idempotency misuse, unauthorized transfer, cross-user reads, unknown timeout and account balance safety. V5 tests additionally assert that evidence export cannot become bank proof, support cases cannot alter transfer status, malformed inputs are rejected, and newly added endpoints enforce tenant/role/CSRF checks.

## Explicit nonclaims

No real KYC, AML, OFAC sanctions clearance, financial regulatory approval, blockchain transaction, ISO 20022 payment message transmission, PSP contract, bank guarantee, security certification, GDPR/PCI compliance or guaranteed prevention of prompt injection. All operations remain an educational synthetic simulator.
