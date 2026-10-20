# Data and model card (V5)

**Purpose:** local tuition-payment educational simulator and benchmark. **Users:** students in a controlled demo, developer QA, hackathon judges. **Not intended:** live finance, regulated advice, actual fraud screening, immigration/tuition compliance decisions.

**Synthetic inputs:** `data/fixtures/synthetic_beneficiaries.json`, sample PDF/TXT invoice and synthetic case state. Sample persons/institutions are illustrative and **not verified real payment instructions**. Proprietary or user-supplied financial data should never be put in this codebase.

**Derived data:** extraction fields with source hashes, investigation matches against synthetic records, quotes using hard-coded reference-only demonstration FX/fees, receipts and SQL ledger state. `benchmarks/stupay_integritybench/v1` is deterministic synthetic data with source and label files; no human evaluation sample.

**Models:** BPCE rules and simulated policy baselines are deterministic code. An optional configured external LLM may explain structured fields but does not plan autonomous payments or sign approvals. Real provider-backed agent tests: **not run**. No learned classifier weights shipped or calibrated probabilities.

**Risks:** distribution shift, self-authored labels, limited country cases, Euro/other corridors unsupported, model prompt injection, synthetic bias and unverifiable external compliance. **Data privacy:** only use fabricated fixtures, seeded demonstration users with passwords supplied at runtime. Live documents/IDs must not be uploaded or recorded during demos.

**Licensing:** synthetic examples authored for the project; identify and audit all third-party dependencies before publication. No external restricted data redistributed in the ZIP.
