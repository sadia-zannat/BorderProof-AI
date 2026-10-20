# Known limitations

1. True Qwen inference, factual accuracy and live-agent benchmarks remain PENDING USER-LOCAL VERIFICATION. The unavailable-model path works. The model cannot approve or execute.
2. Every quote, account balance, beneficiary registry, transfer and receipt is an internal synthetic simulator object. There is no real provider connection, verified payee ownership, legal corridor clearance, real KYC/AML/sanctions or external bank settlement.
3. The heuristic injection scanner misses some obfuscated/multilingual text and rejects some benign quoted instructions. Original proxy holdout: 5/48 unsafe acceptances, 3/12 safe false blocks. These are serious research limitations.
4. Parsing requires labelled English text; scanned PDFs are unsupported. Optional Tesseract handles supported images locally but its text is unverified. No arbitrary-document OCR accuracy is established.
5. Cloud durable storage is absent. PostgreSQL/Docker/PowerShell/Render runtime checks were unavailable. SQLite/local files are suitable for the private reproducible demo, not durable public financial operations.
6. Registration has no identity/email verification and is development-only. Staff roles have intentionally broad local review access. No organization-level multi-tenancy, distributed lockout, MFA or recovery flow exists.
7. Local audit hashes are not signatures and cannot withstand a trusted DB administrator rewriting history. Parser subprocess isolation, external anchoring and high-volume availability were not validated.
8. Catalog parity and locale browser checks pass, while some technical strings/errors remain English. Some mount-time React performance warnings remain. No complete accessibility or user study was conducted.
9. General payment routing, wallet custody, real refunds, production administration, external financial review and independent human benchmark labels are not implemented/validated merely because a module title exists.
10. The narrated five-minute demo and official submission remain user actions. The inherited silent MP4 is historical evidence, not a finished narrated submission.
