# FinVeritas — BorderProof AI V5.5 Verification Checkpoint

**Cumulative V5.4 source preserved; limited, tested security fixes.** Read [V5.5 independent verification](docs/V5_5_VERIFICATION_AND_REPAIRS.md) and [V5.5 Windows guide](docs/V5_5_WINDOWS_BANGLA_START.md). This is an audited **local simulation and planning checkpoint**, **not a production or bank-payment release**. Real payment rails, live Qwen inference, independently verified FX availability, and V5.5 Next.js production build are **not verified**.

The V5.5 code checks the integrity of the **entire case document set** before network evidence assessment and blocks conflicting/invalid extracted invoice data instead of trusting just the first parsed field. Added two independent regressions. Local backend 139 passed / one optional skipped; 6 existing Chromium HTTP-bridge preview tests passed. The complete test evidence is included under `AUDIT/evidence/v55/`.

---

# FinVeritas — BorderProof AI V5.4 Bilateral Network

**Current incremental release: multi-currency, bidirectional route PLANNING; no live banking or provider verification.**

Read [V5.4 release report](docs/V5_4_ARCHITECTURE_AND_RELEASE.md) and [V5.4 Bangla Windows guide](docs/V5_4_WINDOWS_BANGLA_START.md). Previous V5.3 Work audit results remain historical. The new eight-region graph covers 56 bidirectional **planning pairs**, with 8 currencies BDT/CNY/GBP/USD/CAD/EUR/AUD/SGD, real read-only public-reference FX API requests, evidence checks, case/database updates and interactive frontend routes.

**RELEASE VERDICT: NOT RELEASE READY for real money transfer or public financial service.** No authorized provider connected; live FX and local Qwen inference must be checked on a real network/GPU; V5.4 Next.js production build needs external dependencies and verification. Demo browser test is HTTP-bridged, not native localhost E2E. Do not claim any payment availability or bank-verified ownership.

---

# FinVeritas — BorderProof AI V5.3 Work Audited

Latest resumed verification: [20 October recovery and clean acceptance](AUDIT/RESUMED_ACCEPTANCE_20261020.md). Current test evidence is in `AUDIT/evidence/recovery_20261020/`; historical reports are retained.

V5.5.2 candidate: evidence-first read-only routing for explicit inspections; Qwen Windows retest pending (see [repair report](docs/V5_5_2_EVIDENCE_FIRST_REPAIR.md)).

Evidence-consistent assistance for synthetic international-student tuition payments. Complete cumulative V5.2 source repaired and executed in an isolated working copy. Both the premium Next.js app and standalone `/demo` remain included.

**READY FOR LOCAL DEMO within the tested internal simulator scope. NOT RELEASE READY for real financial operations or an unqualified live-agent claim.** All balances, beneficiary records, payment quotes, transfers and receipts are synthetic local simulator objects. Public FX is separately labelled reference data. No real money, external provider transaction or paid inference was initiated.

Start with [Windows Bangla guide](docs/START_HERE_WINDOWS_BANGLA.md), [release verdict](AUDIT/FINAL_RELEASE_VERDICT.md), [45-module audit](AUDIT/FEATURE_STATUS_45_MODULES.md), and [real evidence](AUDIT/REAL_EXECUTION_EVIDENCE.md).

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r services\api\requirements-lock.txt
powershell -ExecutionPolicy Bypass -File scripts\run_preview.ps1
```

Open http://127.0.0.1:8000/demo and create a new local student account. For Next.js, keep API running, then `cd apps/web`, `npm ci`, `npm run build`, `npm run start`; open http://127.0.0.1:3000. No npm is required for standalone preview. No default password is supplied. Use `-SeedDemo` only with your own DEMO_SEED_PASSWORD for the optional four demo roles.

Evidence: clean backend pytest observed 130 passed; native workflow PASS; semantic Next.js production build and actual start verified in logged runs. Six inherited browser tests use a Python HTTP bridge and are separately classified. True local Qwen inference remains **PENDING USER-LOCAL VERIFICATION**, not replaced by mock scores. Run `scripts/run_live_ollama_validation.ps1` with Ollama qwen3:4b and the local API running; share only its synthetic sanitized results after review.

Reproduce tests:

```powershell
.\.venv\Scripts\python.exe -m pip install -r services\api\requirements-dev.txt -c services\api\constraints-python312.txt
.\.venv\Scripts\python.exe -m pytest -q services\api\tests
.\.venv\Scripts\python.exe scripts\check_locales.py
node scripts/check_all_locales.cjs
.\.venv\Scripts\python.exe benchmarks\work_v53_evaluation.py
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe scripts\run_real_execution.py --browser
```

Stop any local 8000/3000 servers before the native acceptance runner starts its own isolated servers. Run Next build before browser acceptance. Set BORDERPROOF_CHROMIUM only when using an existing browser binary. Backend tests include three optional Hypothesis functions. Optional OCR requires Tesseract plus ENABLE_LOCAL_OCR=1; scanned PDFs are unsupported.

The original 300-case research corpus is reproduced, and 96 new frozen offline challenge rows are supplied. These are hand-coded policy proxies and authored labels, not real LLM/AP2 implementations or external human validation. Original holdout BPCE proxy still accepts 5/48 unsafe cases and blocks 3/12 legitimate cases. See [research validity](AUDIT/RESEARCH_VALIDITY_AND_PRIOR_ART.md).

Before reusing an older runtime, back up SQLite and uploads and inspect absolute document paths. Additive migrations preserve history and fail explicitly on duplicate financial rows. PostgreSQL/Docker/Render runtime and durable cloud storage remain unverified/unfinished. No deployment/push is authorized. See [Render preparation](AUDIT/RENDER_READINESS.md).

Current submission assets are the V5.3 deck, script and captions. Older reports/screenshots/MP4/deck remain historical; original V5.2 README/screens are under docs/history. This ZIP is not proof of registration, organizer acceptance or a finished narrated submission. Source revisions: [changelog](docs/V5_3_CHANGELOG.md).


## Windows benchmark note (V5.5.2)

The UTF-8 encoding regression in the frozen synthetic research fixture test is corrected in `services/api/tests/test_research_v4.py`. See `docs/V5_5_2_WINDOWS_UTF8_TEST_FIX.md`. Live Qwen validation is a separate check.


## V5.5.3 candidate: Qwen output limit mitigation

See `AUDIT/V5_5_3_QWEN_PATCH_VERIFICATION.md`. Changes target the four observed local generation-limit failures; actual Windows Qwen retest remains pending. It does not establish production readiness.
