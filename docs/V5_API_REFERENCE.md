# V5 API reference (all private routes require login)

Base: `/api/v1`. Use an HTTP-only `bp_session` cookie. **Mutation routes require `X-CSRF-Token`** returned from `POST /auth/login` or `GET /auth/me`; API no-store header is applied. Response JSON strings below are demonstrative types, not exact IDs.

| Method and path | Role | Description |
|---|---|---|
| `GET /release/capabilities` | Authenticated | Explicit nonproduction and synthetic capability flags |
| `GET /cases/{case_id}/safe-plan` | Owner student | Read-only deterministic recommendation, no payment tool |
| `GET /transfers/{transfer_id}/evidence-export` | Owner student | JSON envelope `evidence`, canonical self-hash, local audit status; not bank proof |
| `POST /support/disputes` | Owner student + CSRF | Creates **local guidance** record, never bank/refund action |
| `GET /support/disputes` | Student | Own local assistance records only |

POST support input:
```json
{
  "transfer_id":"32_hexadecimal_like_identifier",
  "category":"REFUND_GUIDANCE",
  "message":"Please clarify this synthetic simulator result."
}
```
Allowed categories: `STATUS_QUERY`, `PAYMENT_ERROR`, `REFUND_GUIDANCE`, `OTHER`; one OPEN record per transfer at a time. Rejects unknown transfers or cross-user IDs with HTTP 404. `evidence-export` has `Content-Disposition: attachment; filename="borderproof-synthetic-<id>.json"`, `Cache-Control: no-store`, a self-hash over canonical JSON and provenance caveats.

**Earlier APIs:** `docs/API_V2.md`, `docs/API_V3.md`, `docs/API_V4.md`. Swagger at `/api/docs` on the local instance.
