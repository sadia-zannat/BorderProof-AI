# BorderProof AI — V3 Independent Financial Safety Kernel (BPCE)

**Full V1 + V2 + V3 source. Tested Python/FastAPI internal sandbox and standalone browser UI. The Next.js production build is still NOT independently verified because npm packages could not be installed in this environment.**

Competition: 2026 Shenzhen FinTechathon | International Track | Topic C: Cross-border & Student Finance Assistant. Team: **FinVeritas**. Product: **BorderProof AI**.

> [!WARNING]
> **NO REAL MONEY.** No bank account ownership, real university instructions, sanctions result or licensed payment route is verified. No financial advice, regulated financial services, live Wise/Airwallex connection or bank settlement is offered. Use only fictitious/synthetic data; this prototype is not suitable for real private financial files.

## What is new in V3

- **BPCE_V3_1:** Persisted quote-level evidence seal with canonical snapshot + SHA-256, including owner, case, source file/hash, parsed invoice fields, source document set, synthetic beneficiary fixture and its registry digest, quote amount/fee/rate/provider/expiry, and demo-country policy.
- **Independent execution-side revalidation:** live disk source check and reparse, source set/beneficiary/policy/quote replay check; explicit consent fingerprint binds V3 evidence seal.
- **Explicit approval invalidation:** attaching another document proactively invalidates outstanding active approvals; quote or beneficiary mutation blocks execution. Upgrading legacy V2 approval rows preserves historical records but **cannot execute them** without obtaining a new sealed V3 quote/approval.
- **Role-based investigation and inspection:** student can inspect financial rule flags, quote proof graph and request human review; reviewer can acknowledge/reject; auditor can validate entire local audit SHA-256 chain. Reviewers have no override of hard transaction checks.
- **Adversarial cases:** changed beneficiary, provider/fee/rate/amount, malicious invoice instructions, extraction tampering, forged status readbacks, legacy authorization replay, source-set changes, cross-tenant access, audit tampering.
- **Readable V3 security UI:** Next.js component and *actually Chromium-tested* standalone `/demo#bpce`, with English/Simplified Chinese/Bangla UI labels and mobile fallback.
- **V3 Decision Receipt:** simulated-transfer ledger, scoped approval, evidence seal, and explicit confidence limits.

V1/V2 functionality and full source remain, including secure local sign-in, private document upload, labelled TXT/text-PDF extraction, synthetic quote comparison, real internal database ledger and sandbox payment flows.

## Fastest local start — Windows PowerShell

Unzip, open PowerShell in the extracted project root and execute:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r services\api\requirements.txt
$env:DEMO_SEED_PASSWORD='PickYourOwnVeryStrongPassword123!'
.\scripts\run_preview.ps1
```

Open **http://127.0.0.1:8000/demo**. Sign in with `student@borderproof.test` and your configured demo password. Other seeded role emails: `reviewer@borderproof.test`, `auditor@borderproof.test`, `admin@borderproof.test` (same locally configured development-only password). Demo account seeding is not enabled in production mode.

**Demo walkthrough:** In **Payment lab** use the preseeded synthetic 12,500 GBP case → attach synthetic example invoice → extract → investigate → create `CAMPUS_SIM_A` quote → approve → simulate success → read receipt. Then open **BPCE Security kernel** → Inspect risk → Verify quote seal → inspect the evidence dependency graph → request review. Log in with Reviewer to acknowledge the case; Auditor can verify local hash-chain integrity. No real money ever moves.

## Optional Next.js frontend (unverified production build)

```powershell
# New PowerShell window after the Python service is running:
cd apps\web
npm install
npm run dev
```

Open **http://localhost:3000/bpce**. The backend defaults to localhost port 8000. `npm install` was blocked in this build environment (missing cache/registry), so the Next.js production bundle and full semantic typecheck were not verified here. Source syntax parsing and the standalone browser flows were verified instead. Do not equate syntax check with a working Next.js production deployment.

### Optional Docker (not tested in this environment)

Set a strong demo password in your local `.env`, then `docker compose up --build`. Review `docker-compose.yml`; Docker could not be run here.

## Repeat the checks

```bash
python -m pytest -q services/api/tests
python scripts/check_locales.py
python -m compileall -q services/api/app
python tests/e2e/test_preview.py
python tests/e2e/test_financial_preview.py
python tests/e2e/test_bpce_preview.py
```

These browser checks need Chromium and Playwright installed, plus Python `requests` and backend dependencies. For the isolated browser test environment, real FastAPI calls are made over a Python requests bridge because Chromium navigation to localhost is restricted. This **does not prove** ordinary web hosting/CORS works.

Extra optional property-based tests (requires externally available Hypothesis):

```bash
pip install -r services/api/requirements-dev.txt
python -m pytest -q services/api/tests/test_properties_optional.py
```

V2→V3 database migration verification (requires adjacent original V2 source folder outside the V3 ZIP):

```bash
python tests/integration/verify_v2_migration.py
```

This migration test is included for evidence/handoff but the V3 standalone ZIP does **not** require V2 source to run. A V3 application pointing at an existing V2 SQLite DB will run additive schema updates on startup. **Back up your database first.**

## Code and evidence index

- `services/api/app/bpce.py` — canonical snapshot, internal corridor rules, dependency graph, policy/reapproval checks and risk scanner.
- `services/api/app/bpce_routes.py` — scoped V3 security/reviewer/audit API endpoints.
- `services/api/app/finance.py` — existing V2 internal sandbox plus V3 enforcement at quote/approval/execution.
- `services/api/app/audit.py` — hash-linked local audit and V3 chain verifier.
- `services/api/app/models.py` and `db.py` — additive migration for `bpce_evidence_seals`, `bpce_review_tickets`.
- `apps/web/components/SecurityWorkbench.tsx` — Next.js BPCE security UI source.
- `apps/preview/index.html` — real backed no-npm preview for all V1/V2/V3 functions.
- `services/api/tests/test_bpce_v3.py` — adversarial and negative tests; `test_properties_optional.py` — Hypothesis extra.
- `docs/BPCE_V3_ARCHITECTURE.md`, `V3_ATTACK_MATRIX.md`, `SECURITY_SELF_ASSESSMENT_V3.md`, `API_V3.md`, `FEATURE_STATUS_MATRIX.md`, `VERIFICATION_V3.md`, `V3_RELEASE_REPORT.md` — evidence and limitations.
- `docs/V3_BPCE_*_SCREENSHOT.png` — actual Chromium-rendered preview screens, **not mockups**.

## Known high-priority limitations

1. No live bank beneficiary ownership or verified country/legal eligibility. No real sanctions screening, KYC, fraud risk calibration or step-up MFA.
2. Evidence seals and audit history use local SHA-256, **not digital signatures or external trusted timestamping**. A database operator may rewrite stored truth and hashes.
3. Prompt injection scanner is heuristic: obfuscated, encoded and multilingual attacks can escape it. Financial authority is always denied to untrusted document/LLM text independent of this scanner.
4. Single-instance local demo; PostgreSQL distributed concurrency, OCR scans, image security, external LLM and provider credentials, production Docker/Next builds are unverified.
5. V3 has no full StuPay benchmark/baseline research evaluation; that is V4. The 45-module status matrix names unfinished work precisely.

**Official International-track submission materials also require technical docs, an English presentation deck, code, security self-assessment and sandbox execution evidence; V3 is not a complete competition submission.** Refer to the competition documents and `docs/SOURCE_VERIFICATION.md` for the October 20 deadline and registration-form discrepancies.
