# BorderProof AI — V4 Research, IntegrityBench & Evidence Replay

**Full V1 + V2 + V3 + V4 monorepo. Team FinVeritas · Product BorderProof AI · Shenzhen International FinTechathon 2026 · International AI Topic C (Cross-border Student Finance).**

> **CRITICAL SAFETY LABEL:** ALL transactions are in the **INTERNAL SYNTHETIC SANDBOX**. There is no real money movement, bank beneficiary verification, verified university banking instructions, licensing/KYC/AML clearance, real provider settlement, live Wise/Airwallex integration or production-suitable payment authorization. Never upload real student financial/identity documents to this demo. **V4 benchmark is an authored synthetic study, NOT real-world financial effectiveness.**

## V4 highlights

- **StuPay-IntegrityBench V4.1:** 300 original generated synthetic student tuition-payment scenarios (240 development, 60 stratified held-out), deterministic fixture generator, frozen features and separate fixture labels, SHA-256 corpus metadata. Actual scenario records at `benchmarks/stupay_integritybench/v1/`.
- **Eight runnable policy comparisons:** four intentionally weak or AP2-inspired hand-coded proxies, one BPCE core proxy and three isolated ablations. These are **NOT real LLMs** or an AP2 implementation. Deployed financial safety rules are never disabled for ablations.
- **Actual measured holdout results:** heuristic proxy accepted 38/48 unsafe-labeled cases; BPCE core proxy accepted 5/48, while correctly completing 9/12 legitimate cases. **50% of injected instructions in held-out synthetic cases evade its regex detector.** This is an engineered policy-level comparison, not a validated real-world improvement or scientific novelty proof.
- **Reproducible case-by-case output:** policy results JSON and case-level CSV traces; aggregate metrics include legitimate completion, unsafe acceptance, false rejection, injection success, approval drift rejection, blocking F1 and measured CPU policy microseconds (not full workflow latency).
- **Functional read-only V4 research API:** authenticated summary, case family filter/pagination, isolated case replay, per-check explanation, and synthetic invoice evidence; never writes payments, approvals or cases.
- **Premium research dashboard:** Next.js source plus actually Chromium-tested standalone `/demo#research` showing per-policy charts, filter, replay, per-check evidence inspection, 3 languages and mobile layout. Screenshots in `docs/V4_RESEARCH_*.png`.
- **Prior-art, novelty and limitations reports:** see `docs/V4_RESEARCH_NOVELTY_AND_PRIOR_ART.md`, `docs/V4_SECURITY_LIMITATIONS.md`, `benchmarks/README.md`, `docs/V4_MODEL_DATA_CARD.md`, `docs/FEATURE_STATUS_MATRIX.md`.
- All V1–V3 features remain: authentication, student case/doc workflow, synthetic quote/approval/transfer, SQL sandbox ledger and receipts, V3 BPCE evidence seals, audit and reviewer consoles.

## Quick start — Windows PowerShell

From the extracted ZIP's **project root** (Python 3.12 recommended):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r services\api\requirements.txt
$env:DEMO_SEED_PASSWORD='SetYourOwnStrongRandomPassword123!'
.\scripts\run_preview.ps1
```

Open **http://127.0.0.1:8000/demo** and log in with `student@borderproof.test` and your configured seed password. Select **Research & IntegrityBench**. Other local demo roles: `reviewer@borderproof.test`, `auditor@borderproof.test`, `admin@borderproof.test`. Demo accounts only initialize when `ENABLE_DEMO_SEED=1` in development mode. No hard-coded password is distributed.

To demonstrate the entire internal payment flow, use **Payment lab** → attach the provided matching synthetic invoice → extract → investigate → quote → explicitly approve → execute internal simulation → receipt. The **BPCE Security kernel** shows evidence constraints, review and audit. Study pages are independent, offline, read-only fixtures.

## Run benchmark and full tests

From the extracted **root**:

```powershell
python -m benchmarks.stupay_integritybench.corpus
python -m benchmarks.stupay_integritybench.evaluator --split holdout --out benchmarks/results
python -m benchmarks.stupay_integritybench.evaluator --split development --out benchmarks/results
python -m pytest services/api/tests -q
python scripts/check_locales.py
python tests/e2e/test_research_preview.py
```

Browser test needs Python Playwright, `requests`, and system Chromium (Linux paths are used in the automated screenshots). Core FastAPI tests require `services/api/requirements.txt`. Hypothesis property test is **optional** and skipped if not installed (`services/api/requirements-dev.txt`).

A **V2→V3** migration test is included at `tests/integration/verify_v2_migration.py` and requires the *prior V2 source directory as a sibling* of this extracted root; it is not needed to start the V4 app. V4 adds no SQL migrations; it only adds read-only API endpoints and bundled fixture data.

## Optional Next.js frontend

```powershell
cd apps\web
npm install
npm run dev
```

Open **http://localhost:3000/research**. FastAPI must be running on localhost:8000. **Next.js package installation, full semantic TS typecheck, production build and deployment have NOT been verified** in the build environment; the working Chromium evidence concerns standalone `/demo`, not the Next build. Source syntactic parsing was checked.

## Optional Docker (unverified)

Set `DEMO_SEED_PASSWORD` in your local environment or `.env`, then run `docker compose up --build`. V4 Dockerfile includes the benchmark corpus/results. Docker was not available for an actual image build; do not call Docker a verified deployment.

## Project directories

- `services/api/app/` – FastAPI, local security and payment logic; `stupay_core/` isolated V4 policy evaluation.
- `apps/preview/index.html` – no-npm browser fallback with real backend interactions.
- `apps/web/` – Next.js multilingual source, including `ResearchWorkbench.tsx`.
- `benchmarks/stupay_integritybench/v1/` – synthetic cases, labels and corpus checksums.
- `benchmarks/results/` – genuine CLI results JSON and holdout CSV trace (not manufactured performance).
- `services/api/tests/` – V1–V4 API and security tests.
- `tests/e2e/` – Chromium standalone preview smoke flows (requires system browsers).
- `docs/` – architecture, release evidence, security disclosures, benchmark methodology, risk model, prior art, status and screenshots.

## Product/research boundaries

V4 does **not** have a human-validated financial fraud dataset, independent expert-labeled holdout, model-based baseline using actual LLMs, trustworthy provider FX/beneficiary identification, true AP2 compatible signing, formal protocol proof, complete KYC/AML, adversarial adaptive-LLM red team, independent distributed concurrency proof, or a verified web deployment. An impressive chart is not evidence of real-world performance.

Check `docs/V4_RELEASE_REPORT.md` for exact observed tests, gaps, reproducibility and version continuation. **V5 is NOT included and was not built in this version.**
