# V2 endpoint reference

API root `http://127.0.0.1:8000/api/v1` with authenticated session. All mutable finance endpoints require student role and `X-CSRF-Token` from `/auth/login` or `/auth/me`. OpenAPI automatically generated at `/api/docs`.

| Method | Route | Purpose |
|---|---|---|
| GET | `/finance/capabilities` | Mode, synthetic rates, data provenance and optional LLM availability |
| GET | `/finance/account` | Synthetic BDT balance (student) |
| GET | `/finance/reference-fx?base=EUR` | Optional dated external reference; 503 if unavailable, never used for payment execution |
| POST | `/cases/{case_id}/synthetic-invoice` | Attach UK 12,500 GBP example with explicit fixture origin |
| POST | `/cases/{case_id}/documents/{document_id}/extract` | Parse labelled TXT/PDF, optional OCR; return field provenance and issues |
| GET | `/cases/{case_id}/extractions` | Owner-scoped extraction records |
| POST | `/cases/{case_id}/investigations` | Body `{"extraction_id":"..."}`; inspect fields and synthetic registry |
| GET | `/cases/{case_id}/investigations` | Owner-scoped records, negative decisions retained |
| POST | `/cases/{case_id}/quotes` | Body `{"investigation_id":"...","provider":"CAMPUS_SIM_A"}` |
| GET | `/cases/{case_id}/quotes` | Owner-scoped quote records and expiry |
| POST | `/cases/{case_id}/approvals` | Body `{"quote_id":"...","confirmation":"I AUTHORIZE THIS INTERNAL SANDBOX PAYMENT"}` |
| GET | `/cases/{case_id}/approvals` | Approval scope hashes and states |
| POST | `/cases/{case_id}/transfers` | Body `{"approval_id":"...","idempotency_key":"...","simulated_outcome":"SUCCESS"}` |
| GET | `/cases/{case_id}/transfers` | Owner-scoped internal transfer states |
| GET | `/transfers/{transfer_id}/receipt` | Raw receipt and balancing ledger records |
| POST | `/transfers/{transfer_id}/reconcile` | Body `{"simulated_confirmation":"CONFIRMED_FAILED"}` or `CONFIRMED_SUCCESS` (simulated only) |
| GET | `/finance/notifications` | Owner-scoped persisted status events |
| POST | `/cases/{case_id}/copilot` | Body `{"extraction_id":"...","question":"..."}` bounded explanation, NEVER permission to execute |

Existing V1 routes remain available. None of these endpoints call a live payment provider or real bank.
