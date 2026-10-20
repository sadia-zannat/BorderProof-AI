# V3 BPCE API — relative to /api/v1

All routes require an authenticated cookie. POST routes require a matching CSRF token; role restrictions apply.

| Method | Endpoint | Role | Purpose |
|---|---|---|---|
| GET | `/security/capabilities` | all authenticated | Implemented/absent security capabilities |
| GET | `/cases/{case_id}/bpce/risk` | case owner | Local rule flags / policy unknown |
| GET | `/cases/{case_id}/bpce/policy` | case owner | Static INTERNAL demo corridor, real legal status unknown |
| GET | `/cases/{case_id}/bpce/quotes/{quote_id}` | case owner | Rerun evidence seal validation, render dependency graph |
| POST | `/cases/{case_id}/bpce/review-request` | student owner | Open one outstanding human review ticket (`reason`) |
| GET | `/cases/{case_id}/bpce/review-requests` | student owner | Ticket history for case |
| GET | `/review/bpce-queue` | reviewer/admin | Review all pending tickets |
| POST | `/review/bpce-tickets/{ticket_id}/decide` | reviewer/admin | `decision=ACKNOWLEDGED/REJECTED`, explanation; never bypass hard blocks |
| GET | `/security/audit-integrity` | auditor/admin | Verify full local audit event chain |
| POST | `/security/attack-probe` | reviewer/auditor/admin | Read-only indicator scan `{untrusted_text}` |
| POST | `/transfers/{transfer_id}/verify-tool-claim` | student owner | Compare untrusted `{claimed_reference,claimed_status}` against DB readback; never changes status |
| GET | `/transfers/{transfer_id}/decision-receipt` | student owner | Structured evidence/approval/ledger receipt for INTERNAL simulation |

All V1/V2 REST endpoints remain. Read-only decision graph API returns `can_proceed_to_approval=false` and reasons when snapshot changes. Actual execution still rejects independently server-side. Demo UI is at `/demo#bpce`. Note that role-based reviewer visibility is broader than student ownership by design and must be redesigned for actual multi-organization deployments.
