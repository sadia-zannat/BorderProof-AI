# V5.2 to V5.3 source revision

Preserved both frontend variants, all original source modules, BPCE graph/seals, ledger, roles, English/Chinese/Bangla catalogs, benchmark corpus, local Ollama integration, historical reports, original logo and inherited submission assets. Original V5.2 README/screenshots are separately retained under docs/history.

Changed finance.py/bpce.py for duplicate-field conflict detection, latest/all-document checks, writer serialization, strict idempotency payload and reconciliation amount/status. Added storage.py, timeutils.py, references.py and explicit blocked provider interfaces. Updated additive database uniqueness indexes without deleting historical rows. Changed session CSRF semantics to remain stable within a session and invalidate across sessions. Added local-only signup and UTC API timestamps.

Changed model runtime envelope validation, loopback proxy handling, disabled-model configuration, bounded tool-result provenance and safe failure audit. The local harness is real inference only. The production frontend now has a lockfile, semantic build fix, ESLint config, same-origin API proxy, role-aware navigation, optional public FX reference, locale fonts and /demo deep-link/mobile repairs.

Added new adversarial tests, seeded fresh invoice/PDF/scan authoring, native HTTP/browser/restart execution, separate OCR run, original benchmark reproduction and 96 frozen additional offline cases. Added honest release/Render/security/research documents, new English submission materials and reproducible packaging/manifest scripts. No fake provider or AI response is added.

## 2026-10-20 resumed revision

Recovered the unchanged repaired V5.3 source and preserved all earlier fixes. Extended the native verification harness to restart after both browser flows and re-authenticate owners for all six persisted receipts; compare financial rows before/after. Retained initial environment/query failures, then reran successfully. Added fresh installation/build/backend/browser/OCR/research evidence, recovery checkpoint provenance and current handoff. Product UI, financial policies, schema and agent permissions are unchanged by this resumed revision.
