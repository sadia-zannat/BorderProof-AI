# V3 Threat Model and Tested Attacks

**Financial assets:** sandbox balance and ledger integrity, case-to-owner isolation, approval correctness, evidence consistency, sensitive uploads. No real payment credentials are configured.

| Adversary capability / scenario | Enforced boundary | Test evidence | Remaining risk |
|---|---|---|---|
| User uploads invoice with malicious role instructions | Documents parsed as data; explicit heuristics block known instruction phrases at quote sealing | `test_new_invoice_injection_indicator_fails_closed` | Obfuscated, multilingual or multimodal injections can evade heuristics; this is NOT a general detector |
| Amount, currency, fee, rate, recipient, provider or beneficiary changes after approval | Recompute BPCE snapshot and authorization fingerprint | Parameterized `test_quote_mutation_blocks_postapproval_payment` (8 variants) | Shared DB superuser can modify source + reference simultaneously |
| Invoice field/database extraction poisoned | Fresh deterministic parser compared with saved source extraction | `test_editing_extracted_fields_invalidates_seal` | Quality of extraction and detection of document authenticity remain limited |
| New invoice added after approval | Document-set version invalidated, approval proactively set INVALIDATED | `test_new_document_upload_invalidates_approval` | External real university beneficiary changes not tracked automatically |
| Stored evidence seal corrupted | SHA-256 check plus recomputation | `test_seal_corruption_blocks_payment` | SHA-256 not signed or independently anchored |
| Old approval replayed after V2→V3 upgrade | Missing V3 seal fails closed | `test_legacy_quote_without_new_seal_is_rejected`, V2→V3 migration test | Existing historical V2 completed transfers retained only as internal test artifacts |
| Quote expired | Expiry checked at approval/execution | V2 regression `test_invalid_and_expired_quote_guard`, V3 `test_quote_change_and_expiry_both_block` | Clocks and storage are trusted locally |
| Fake successful tool/provider response to failed/unknown transfer | Compare untrusted status and reference against persisted simulator readback; no execution changes | `test_tool_status_forgery_fails_but_readback_passes` | No REAL provider-origin signature; matches prove local consistency only |
| Duplicate transfer and idempotency replay | Unique `(owner_id, idempotency_key)`, SQLite transactional serialize and case guard | V2 `test_duplicate_idempotency_no_double_debit` | Multi-host PostgreSQL locking/performance unverified |
| Tenant escalation | Backend case/document/quote/transfer ownership and role/CSRF checked | `test_other_student_cannot_get_bpce_graph_or_review_data`, V2 regressions | Reviewer visibility is administrative, not shared-tenant multi-org RBAC |
| Admin tampers with audit record or deletes intermediate event | Verify entire hash chain and parent graph | `test_audit_chain_detects_single_event_tamper`, `test_audit_chain_detects_removed_middle_event` | DB operator can reconstruct whole chain; no external anchoring |
| Manual reviewer tries to override verified hard block | Review records acknowledgment only; financial authorization independent | `test_review_request_reviewer_decision_does_not_bypass_safety` | No production escalation SOP or independent dual-control signatures |
| Forged regulator compliance assertion | Explicit `UNKNOWN_REQUIRES_LICENSED_PROVIDER` and `NOT_VERIFIED` flags | `test_synthetic_corridor_fails_closed_instead_of_regulatory_claim` | Country legal advice requires independently updated, authoritative data |

OWASP context: indirect prompt injection and excessive agency are relevant to any future LLM financial tool routing. The current execution controller does **not** accept authorization claims from LLM output and never gives the LLM payment credentials. See OWASP LLM01 and LLM06 pages linked in `BPCE_V3_ARCHITECTURE.md`.

## Practical adversarial priorities for V4

1. Hold-out attack corpus testing including obfuscated/multilingual/payload splitting; measure **false rejects** and misses, not just detected positive fixtures.
2. Concurrent SQLite/PostgreSQL process failure, retry and reconciliation under distributed workloads.
3. External attestation/signed audit root, privacy review, verified policy corpus and genuinely independent authority for beneficiary checks.

**Do not deploy for real student payments.**
