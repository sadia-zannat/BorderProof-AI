# V3 Changelog — 2026-10-19

All V2 source retained. V3 versioned changes:

- `app/bpce.py`: deterministic independent evidence snapshot and recomputation, strict synthetic corridor policy, fail-closed quote checks, graph, local risk assessments, document-instruction indicator scanner.
- `app/models.py`: `EvidenceSeal`, `ReviewTicket` additive tables.
- `app/db.py`: idempotent `schema_versions` V3 upgrade; existing V1/V2 rows preserved.
- `app/finance.py`: BPCE seal on each created quote; seal-bound approval; independent execution-side full evidence check; legacy unsealed approvals rejected.
- `app/main.py`: V3 API identity/version, proactive approval invalidation on new document upload.
- `app/audit.py`: local whole-chain integrity verifier with tamper/fork detection and limitations.
- `app/bpce_routes.py`: V3 quote/proof/risk/policy, human review, audit verification, tool-claim readback and execution receipt.
- `apps/preview/index.html`: working BPCE inspector/reviewer/auditor screens, tri-lingual controls, readable graph cards and mobile layout.
- `apps/web/components/SecurityWorkbench.tsx`: V3 typed security inspector; `Workspace.tsx` navigation integrated.
- Tests: `test_bpce_v3.py`, optional `test_properties_optional.py`, migrated V2→V3 integration, V3 Chromium UI end-to-end.
- Updated architecture, attack matrix, security self-assessment, API docs, feature matrix, CI development dependency, README.

No features removed from V2. Any V2 legacy approval must be reissued using the V3 security envelope. This fail-closed migration behavior is intentional.
