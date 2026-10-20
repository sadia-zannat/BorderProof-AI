# Security self-assessment — V2 (NOT a certification)

**Scope:** local training/demo. No real-money transaction, real bank account access, real tuition invoice handling, public customer onboarding or production financial deployment is authorized by this implementation.

| Control / threat | V2 implementation | Verification / remaining risk |
|---|---|---|
| Session and CSRF | Hashed HttpOnly cookie token, Argon2 password verification, CSRF required on V2 mutations | API tests passed; CSRF rotation on `/auth/me` can affect multiple tabs |
| Student tenant isolation | All finance IDs checked against owner and case | Cross-user cases/receipts tests passed; reviewer views are restricted |
| Uploaded invoice prompt injection | Anchored field extraction only; raw instructions cannot execute | Attack-text negative test passed; no exhaustive injection benchmark yet |
| Beneficiary fraud | Exact match with labelled synthetic beneficiary registry | Mismatch blocks. **Does not** validate real beneficiary, account ownership, sanctions, legal compliance |
| Missing invoice data | Missing-field result blocks downstream quote | Negative test passed; arbitrary documents unsupported beyond labelled text |
| Stale amounts/evidence | Quote, approval fingerprint and execution revalidation | Mutated case/file and expired quote negative tests passed |
| Unauthorized payment | Explicit approval + CSRF required | Missing approval rejected; user-consent UX is a confirm dialog, not step-up MFA |
| Duplicate requests | Unique owner/idempotency key, SQLite serialized write at execution | Sequential duplicate tests pass; heavy concurrency/crash stress pending |
| Unknown provider response | `UNKNOWN`, no debit; dedicated simulator reconciliation | Timeout negative tests passed; real provider readback and durable outbox absent |
| Financial precision | Python Decimal and 2-decimal strings | Test ledger balances zero across entries; no general currency minor-unit library |
| Audit | Local SHA-256 linked event log and ledger | Not externally anchored or digitally signed; admins of DB may alter records |
| Secrets | Server-side env, never intentional client injection | Optional LLM endpoint/key controlled by server operator; no hardened secret vault |
| Parsing | Small 5MB uploads, simple PDF text extraction | OCR off by default; PDF parser sandbox/antivirus unavailable; don't upload sensitive or malicious files |
| Simulator model | No live payment connector; labels synthetic | Real-money transfers impossible through supplied routes; production infra review still needed |

## Severity-ranked open issues

1. **CRITICAL FOR REAL-WORLD USE:** No regulated payment service, real merchant/beneficiary verification, KYC/AML and jurisdictional eligibility validation. Prohibit live payments and sensitive use.
2. **HIGH:** App lacks enterprise secret management, per-tenant encryption at rest, independent audit anchors, formal migrations for all dialects and production account lifecycle/incident response. Do not deploy as customer platform.
3. **HIGH:** `PaymentApproval` has a hash not a cryptographically signed mandate. V2's source/quote binding is a precursor only, not a full BPCE proof. V3 must implement dependency graph and better replay/critical-attribute attacks.
4. **HIGH:** No extensive concurrent transaction fault injection, worker crash simulation, real-provider reconciliation or step-up authentication. Simulated state correctness has meaningful tests but is not externally proven.
5. **MEDIUM:** Session CSRF rotation may invalidate previously loaded tabs. Local lockout is process-local, and test user bootstrap should not be reused in production.
6. **MEDIUM:** OCR optional, scanned-PDF extraction unavailable by default, label parsing is sensitive to layout and user-supplied formats, and there is no antivirus scan.
7. **MEDIUM:** Normal browser network E2E, Next production build, Docker runtime and accessibility audit were blocked/unverified in this environment.
8. **LOW:** Standalone financial UI exposes technical state strings in English, despite major workflow strings having translations.

## Security review rules for V3

Implement independent ownership guards with query-level tenant filters, stronger transaction state machine, TOCTOU/race testing, signed/context-scoped approvals, controlled provider tool-response integrity, prompt injection threat matrix, explicit corridor policies with effective dates, manual escalation for suspected fraud and property-based tests. Keep insecure baselines isolated from deployment.
