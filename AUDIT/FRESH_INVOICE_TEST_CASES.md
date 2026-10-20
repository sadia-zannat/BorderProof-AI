# Fresh invoice coverage

Generated after extracting V5.2 using a separate seeded authoring script. These are privacy-safe newly authored supported invoices, not authentic university financial documents or independent human-labeled data. Exact bytes, hashes, seed and expectations accompany `evidence/native_final/inputs/manifest.json`.

| New input | Observed behavior |
|---|---|
| GBP, USD, CAD with new references and amounts | Actual extracted fields, synthetic registry checks, quote, approval, persisted internal completion |
| Missing account | NEEDS_CLARIFICATION with a specific correction question |
| Contradictory amount labels | Conflict issue, clarification, quote denied |
| Malformed thousands separators | INVALID_AMOUNT, no normalization into a valid payment |
| New unsupported university | Fields extracted, synthetic registry does not match, blocked |
| Malicious instructions added to invoice | BPCE quote creation blocked; text never grants tools/approval |
| Two-page PDF with facts split across pages | Actual pypdf extraction and simulator workflow |
| PNG scan with OCR disabled | Explicit 503, no invented fields |
| Same PNG with actual local Tesseract enabled | OCR engine and amount observed through real API; still unverified text |

Supported parser format is English, one labelled field per line: Institution, Invoice ID, Currency, Amount, Payment deadline (YYYY-MM-DD), Beneficiary, Account, Student. No arbitrary-layout, scanned-PDF or multilingual document intelligence is claimed. English-labelled names may contain Unicode. Parser confidence constants are heuristics, not calibrated probabilities. A corrected invoice should be uploaded as a new version and explicitly re-investigated; conflicting historical evidence can require a new case/manual review because no administrative override exists.

Resumed clean verification (2026-10-20): see [current acceptance](RESUMED_ACCEPTANCE_20261020.md) and `evidence/recovery_20261020/`. Earlier measurements above are preserved with their original scope.
