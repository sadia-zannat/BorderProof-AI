# Financial security evidence and residual risk

Clean backend tests passed: **130**. Current targeted work regression log: `evidence/security-regressions-final.log`; baseline and intermediate failures are retained. Three Hypothesis tests exercise 280 generated examples collectively. Hypothesis cases are not counted as separate pytest tests.

Confirmed local invariants: unauthenticated requests fail, student ownership is checked for cases/documents/quotes/transfers/conversations, reviewer/admin/auditor roles are enforced, CSRF and Origin checks guard mutations, and the model exposes six read-only tools with no approval or execution capability. Staff access is intentionally broad within this single local application; this is user isolation, not a multi-organization tenant platform.

Transactions bind human consent to the exact quote and source snapshot. Quote/recipient/amount/currency/provider/source mutation, expiry, changed document sets and approval replay block execution. Concurrent duplicate execute requests produce one transfer and two balanced postings. Concurrent timeout reconciliation produces one debit. TIMEOUT stays UNKNOWN until explicit simulation reconciliation. Idempotency reuse with a changed payload is a conflict.

Threat boundaries: invoice/web/model outputs are untrusted data, public references cannot verify payee ownership, provider-status comparison checks only persisted simulator state, and a DB administrator remains inside the trusted computing base. Audit hashes are local and unanchored. The heuristic injection detector misses obfuscated/multilingual text; the LLM's absence of write tools is the stronger execution boundary. No universal injection-defense claim is justified.

Remaining production blockers: no real KYC/AML/sanctions or legal approval, no external settlement verification, no durable cloud document backend, no live PostgreSQL locking tests, no distributed session/rate-limit infrastructure, no verified identity/email recovery, and no externally anchored audit. PDF/OCR parsing has size/page/text/time limits but no OS-isolated parser sandbox. Local registration is deliberately development-only and the app binds loopback in its user startup scripts.

NPM production audit raw result is shipped. A zero-known-advisory result at this retrieval time does not certify the application. This work is an internal technical assessment, not external security certification or human financial peer review.

Resumed clean verification (2026-10-20): see [current acceptance](RESUMED_ACCEPTANCE_20261020.md) and `evidence/recovery_20261020/`. Earlier measurements above are preserved with their original scope.
