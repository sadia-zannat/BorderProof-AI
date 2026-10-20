# BorderProof AI V2 — implemented architecture

```text
Next.js app (source, NOT production-build verified)
    | browser fetch with httpOnly session cookie & X-CSRF-Token
FastAPI 2.0 /api/v1/*  ◄─────────  HTML/CSS/JS local preview (/demo)
    ├─ Role-aware auth & CSRF (V1)
    ├─ Private file storage + SHA-256 & download isolation
    ├─ pypdf text extraction / TXT anchored parser / optional OCR
    ├─ Deterministic missing-field + discrepancy inspector
    ├─ Local SYNTHETIC beneficiary registry; NOT real verification
    ├─ Synthetic quote calculator (Decimal, fixed non-market rates)
    ├─ Approval fingerprint binds critical amount, institution, quote,
    │  provider, recipient, hash and expiry
    ├─ Independent execution guards and durable idempotency key
    ├─ Synthetic BDT account, balanced BDT ledger, transfer state
    ├─ Timeout → UNKNOWN, explicit simulator-only reconciliation
    └─ DB audit + notifications + JSON Decision Receipt
        SQLAlchemy SQLite database schema v2
        (auto-additive V1 → V2; PostgreSQL needs appropriate driver)
```

## Verified vertical flow

1. Upload a user document (or attach labelled, explicitly synthetic fixture).
2. Extract anchored fields with page/line? V2 stores **line numbers from extracted text**, not PDF page-level bounding boxes. Field confidence is parser heuristic, not probability of authenticity.
3. Compare institution/amount/currency against saved case and beneficiary/account against exact matching **SYNTHETIC** fixture.
4. Missing fields → `NEEDS_CLARIFICATION`. Conflicts → `BLOCKED`. Match → `SANDBOX_FIXTURE_MATCH`. Unknown real-world provider eligibility never becomes verified.
5. Compare internally configured fixed synthetic provider rates and fees. Quotes expire in 15 minutes; no market data is used to price these simulations.
6. Explicit user approval generates a fingerprint with case and quote details. It is invalid for changed case details, document digest, expiry or already consumed approval.
7. `execute()` uses an atomic SQLite write transaction (`BEGIN IMMEDIATE`) plus an owner/idempotency unique constraint to suppress duplicate debits; **concurrent stress testing is not yet exhaustive**.
8. Internal simulator returns `COMPLETED` on simulated success with balanced BDT ledger, `FAILED` on decline, `UNKNOWN` on timeout. Timeout does not debit funds until simulated reconciliation to success.
9. Receipt shows provider-prefixed simulated reference, decision scope fingerprint, source digest, status, actual DB ledger entries and explicit non-bank label.

## API security boundary

- V1 HTTP-only session, same-site cookies, Argon2 passwords and CSRF for all new mutations remain operative.
- Every V2 case, extraction, investigation, quote, approval, transfer and receipt is owner-scoped. Student-only create/mutate operations; reviewer/admin read-only V1 consoles are separate.
- An LLM can optionally **explain structured fields** through an OpenAI-compatible API chosen by server environment variables. It receives no actual password, API session cookie, document binary or payment execution authority. It cannot generate an approval or bypass deterministic checks.
- Browser UI sends no server secrets. The same authorization runs whether using Next.js or standalone preview.
- Uploads are capped at 5MB, signature-validated, and stored outside public paths with restrictive local permissions. No malware scanner/secure rendering sandbox exists in V2.

## Data classifications

| Data | Truth claim |
|---|---|
| Case amount / user document | User-entered or unverified; never evidence of legal entitlement |
| Extracted text and parser confidence | Unverified user-supplied data; line of extracted text |
| `TEST-UK-001` etc | Locally authored **SYNTHETIC** fixture match, not actual beneficiary ownership |
| Simulator quotes | Fixed synthetic FX rate and fee; not a bank executable quote |
| Frankfurter read-only API if reachable | Public FX reference dated by provider; not a live payment quote |
| BDT balances, state transitions, receipts | Actual persisted **simulation** state, no real-money movement |
| Optional LLM response | Non-authoritative textual explanation only |

## Still not implemented

Full BPCE graph/independent hash dependency engine, independent verified university payment sources, authoritative corridor-policy engine, live partner sandbox adapter, prompt-injection evaluation, advanced role/tenant models, signed external audit anchoring, production session/user management, browser accessibility audits and reproducible security benchmarks. These are V3–V5 work, not hidden V2 features.
