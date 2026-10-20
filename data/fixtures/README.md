# Synthetic V2 finance fixtures — no real-world payment details

- `synthetic_invoice_UK.txt` and `synthetic_invoice_UK.pdf` contain a fabricated 12,500 GBP Northbridge tuition sample, fake recipient and account. They are not signed or issued by any real institution.
- `synthetic_beneficiaries.json` contains three locally manufactured university/recipient records for UK, US and Canada. A matching ID such as `TEST-UK-001` means only **DEMO FIXTURE MATCH**, not university authentication, bank beneficiary ownership, AML/KYC clearance or corridor legality.
- Simulated FX rates are programmed in `services/api/app/finance.py`, are not from live markets, and are intentionally marked SYNTHETIC.
- Source code and UI never need passports or real banking credentials to demonstrate V2. Never upload live sensitive financial documents.

A dev account is seeded only with `APP_ENV=development`, `ENABLE_DEMO_SEED=1` and a strong environment-provided `DEMO_SEED_PASSWORD`. This is local demonstration data only.
