# BorderProof Consistency Engine (BPCE_V3_1)

**Scope:** educational/internal financial simulator only. All university and beneficiary data used for successful execution are synthetic. This is **not** a live bank verification service, AP2 implementation, legal eligibility engine, or production payment system.

## Execution-time trust boundary

```text
User case + uploaded invoice (UNTRUSTED)
    │ parse invoice deterministically, record source SHA-256
    ▼
Extraction + investigation (synthetic beneficiary check)
    │ compare case amount, institution, currency, beneficiary and account
    ▼
Synthetic quote (15-minute expiry) + BPCE EvidenceSeal
    │ canonical snapshot + SHA-256, database-persisted
    ▼
User explicit approval (exact synthetic-payment acknowledgment)
    │ fingerprint = hash(V2 scope + BPCE seal)
    ▼
INDEPENDENT execution controller (NO LLM AUTHORITY)
    │ role, CSRF, tenant, idempotency, active approval, expiry
    │ source file hash + parser re-evaluation + document set
    │ beneficiary fixture & registry digest + synthetic corridor rule
    │ provider, recipient, quote amount, fee, rate and expiry
    ▼
Internal simulator + persistent transfer + balanced BDT ledger
    │ success / failure / unknown response, never live payment
    ▼
Decision receipt with transaction, approval and evidence seal
```

### What is actually bound

New `bpce_evidence_seals` rows persist a canonical JSON snapshot and SHA-256. Snapshot includes:

1. Authenticated case owner, case ID, institution, origin, destination, amount, currency.
2. Source invoice ID, document ID/hash, extraction ID, regenerated parser output digest, sorted document set (file ID, SHA-256 and size).
3. Matched **synthetic** beneficiary fixture ID, name, account-field hash and registry-file hash (not bank attestations).
4. Quote ID, provider, recipient, amount, currency, simulated rate/fee/source total and expiry.
5. Demo policy version, corridor suitability for internal simulator, and explicit unknown real-world compliance.

Any snapshot change blocks the new approval or transfer. A newly uploaded document additionally **proactively invalidates** active approvals; older V2 quote/approval records cannot execute without a V3 seal. Failed independent verification has HTTP 409 and does not debit the synthetic ledger.

### Evidence graph and UI

`GET /cases/{case_id}/bpce/quotes/{quote_id}` returns a seven-node, seven-edge source dependency graph and a decision. The security inspector renders this graph as selectable/expandable readable DOM cards. Graph nodes explicitly distinguish parsed user invoice data, fixture matches, synthetic quotes and unknown real-world compliance.

### Boundaries, not novelty claims

The concept of authorization binding, hashed authorization scope, signed payment mandates and execution-time verification predates this project. AP2 provides a substantially stronger independently verifiable mandate model involving signed credentials and payment roles. BPCE_V3_1 is a **local composition and student-finance-domain adaptation**, not equivalent to AP2. The V3 hash is **not cryptographically signed**: a database insider with write access could replace the stored snapshot and hash; all source validity is anchored in the same local system. V4 will investigate comparators, formal properties and reproducible benchmark cases.

Sources used for design comparison:
- Google AP2: https://github.com/google-agentic-commerce/AP2/blob/main/docs/ap2/specification.md
- Google agent authorization: https://github.com/google-agentic-commerce/AP2/blob/main/docs/ap2/agent_authorization.md
- OWASP LLM01 Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- OWASP LLM06 Excessive Agency: https://genai.owasp.org/llmrisk/llm062025-excessive-agency/

These standards/guides are references only; no open-source source code was copied into the kernel.
