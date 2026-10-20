# BorderProof - AI

**Evidence-Consistent Financial Assistance for International Student Tuition Payments**

**Team:** FinVeritas  
**Competition:** 2026 Shenzhen International FinTech Competition  
**Track:** International Track - Topic C  
**Source:** https://github.com/sadia-zannat/BorderProof-AI

## Project Overview

BorderProof - AI is an evidence-first financial assistance prototype for international students planning tuition payments across borders. A tuition invoice, a receiving account, an exchange-rate reference and a payment authorization are separate facts. None should be accepted as proof of the others.

The system links them in one reviewable workflow: a student creates a tuition case, attaches invoice evidence, investigates beneficiary consistency, checks currency-planning options, reviews synthetic quotes and explicitly authorizes a local simulation. The AI assistant explains recorded evidence through read-only tools. It cannot authorize or execute payments.

This is a **local research and demonstration prototype**, not a bank-connected product. Accounts, beneficiaries, provider quotes, transfers and receipts in the simulation are synthetic. Real payments are not supported.

## Problem and Technical Approach

| Problem | Implemented approach |
| --- | --- |
| Invoice fields may be confused with independently verified payee ownership | Extract labelled fields with provenance and compare against local synthetic beneficiary data |
| Currency reference rates may be confused with executable quotes | Separate attributed public FX references from synthetic sandbox quotes |
| AI advice may be confused with authorization | Restrict AI tools to read-only inspection and enforce explicit user actions through the application backend |
| Documents or quotes can change after review | Bind simulated approval to specific evidence and quote state; check expiry and consistency |
| Payment-planning decisions lack an explanation trail | Record document digests, investigation states and simulated transaction history |

## End-to-End Student Workflow

1. **Create the case.** Enter the origin and destination, currencies, institution and invoice amount.
2. **Attach the invoice.** Upload a supported file and store a SHA-256 digest. Extract labelled fields where the document format permits.
3. **Investigate.** Compare invoice fields with the current case and the local synthetic beneficiary registry. Mark mismatches and unknown external checks explicitly.
4. **Plan the corridor.** Explore eight currencies and 56 directed planning pairs, including reverse directions. These selections do not establish payment-rail availability.
5. **Review a synthetic quote.** Inspect simulator fees, amount, expiry and evidence linkage when the local investigation permits quoting.
6. **Authorize and simulate.** Require a user-initiated authorization validated by backend controls before a permitted internal state transition. No external transfer takes place.

A failed beneficiary match or conflicting evidence can block the synthetic workflow. A local registry match is **not** independent verification of a real bank beneficiary.

## Main Capabilities

- **Eight-currency planning:** BDT, CNY, GBP, USD, CAD, EUR, AUD and SGD across 56 directed selections.
- **Document vault:** Case-linked uploads, stored hashes and structured extraction for supported formats.
- **Evidence investigation:** Case consistency checks, synthetic beneficiary matching, conflict handling and review states.
- **Payment lab:** Sandbox providers, expiring synthetic quotes, evidence-bound user authorization and simulated transfers.
- **AI assistant:** Local Qwen3:4b through Ollama, with read-only case, invoice, investigation, quote, approval, policy and corridor inspection tools.
- **Security controls:** Authenticated tenant-scoped data access, evidence integrity checks, separation of AI advice from user consent and auditability.
- **Research bench:** Internally authored synthetic cases and deterministic policy-proxy comparisons.

For architecture, trust boundaries and workflow diagrams, see [System Architecture](docs/PROJECT_ARCHITECTURE.md).

## Technology Stack

| Layer | Technology |
| --- | --- |
| Web | Next.js, React, TypeScript |
| API | FastAPI, Python 3.12 |
| Persistence | SQLAlchemy and SQLite for local use |
| Local AI | Ollama with Qwen3:4b |
| Evidence handling | SHA-256 and deterministic labelled field extraction |
| Foreign exchange | Read-only public reference-rate integration |
| Tests | Pytest and scripted local validation |

## Local Setup (Windows)

From the repository root, install Python 3.12 dependencies:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r services\api\requirements-lock.txt
```

Start the standalone FastAPI preview:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run_preview.ps1
```

Visit `http://127.0.0.1:8000/demo` and create a local demonstration account.

Run the backend tests:

```powershell
python -m pytest -q services\api\tests
```

The Next.js app can be built separately from `apps/web`:

```powershell
cd apps\web
npm ci
npm run typecheck
npm run build
npm run start
```

For optional real local model validation, run Ollama with `qwen3:4b`, keep the API running, and from a second terminal at the repository root execute:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run_live_ollama_validation.ps1
```

The generated runtime report must be inspected before sharing. Do not commit credentials, `.env`, private documents, SQLite databases or runtime artifacts.

## Measured Validation

Results below come from the reported Windows tests of October 20, 2026 and are not production certification.

| Test | Reported observation |
| --- | --- |
| Backend automated tests | 149 passed, 1 skipped, 1 deprecation warning |
| Live local Qwen requests | 9 attempted; 4 HTTP 200; 5 HTTP 502 |
| Local financial side effects | No real transfer reported |
| Synthetic research set | 300 authored cases; 60-case holdout |
| Deterministic policy proxy, holdout | 5 of 48 unsafe cases accepted (10.4%); 9 of 12 legitimate cases completed (75.0%) |

The model's HTTP 200 responses are not equivalent to correct tool choice or verified financial advice. The synthetic policy-proxy metrics are not live Qwen accuracy or real-world fraud performance.

See [Validation and Security Scope](docs/VALIDATION_AND_SECURITY_SCOPE.md) for methodological boundaries and outstanding checks.

## Operational Scope

The implementation supports controlled local planning and synthetic financial simulations. It does not establish live bank connectivity, real account ownership, legally permitted routes, executable foreign-exchange prices, licensed payment operations or production service security. External provider availability and transaction eligibility are unknown until independently verified.

Historical development records are retained under `AUDIT/`, `docs/` and `WORK_HANDOFF.md` for traceability. Their earlier checkpoint results must not be represented as a single current release verdict. The existing `SOURCE_MANIFEST_SHA256.txt` records an earlier packaged source snapshot and may not match new documentation commits.

## Team

**FinVeritas**  
Sadia Akter Zannat - Team Leader  
Md. Nazrul Islam Leon - Team Member

**Project repository:** https://github.com/sadia-zannat/BorderProof-AI
