# BorderProof AI — V5.2 Premium Minimal UI Refresh

**Updated user-facing UI for both the standalone `/demo` website and optional Next.js source.** This full cumulative project preserves the existing V5.1 free Ollama Qwen3 agent, FastAPI/security/payment simulator, BPCE, benchmarking and documentation. The release changes *presentation and language hierarchy*, **not** the financial-trust boundary. No production banking claim is made.

- Actual Chromium preview screens: `docs/V5_2_MINIMAL_LANDING_DESKTOP.png`, `V5_2_MINIMAL_LOGIN_DESKTOP.png`, `V5_2_MINIMAL_DASHBOARD_DESKTOP.png`, `V5_2_MINIMAL_AGENT_DESKTOP.png` and mobile counterparts.
- Full per-page assessment and validation results: **`docs/V5_2_PREMIUM_UI_AUDIT.md`**.
- **For the existing Windows/VS Code user upgrading from V5.1:** `docs/UPGRADE_V5_2_WINDOWS_BANGLA.md`; backup/copy your local `runtime` folder if you wish to retain previously created cases and accounts.
- V5.2 browser regression suite: 6 passed; all 96 previous/new backend tests passed, optional Hypothesis skipped; 135 locale keys per language and 15 parsed TS/TSX files (not a full Next production build).
- **Visible safeguards remain:** SIMULATED · NO REAL PAYMENTS, unverified financial evidence, transaction-specific consent, BPCE checks. Raw debugging receipt JSON and tool activity remain accessible via collapsible detail sections.

---

## Original V5.1 architecture and setup guide (still applicable)

# BorderProof AI — V5.1 Free Local Autonomous Agent Edition

**Team FinVeritas · Shenzhen FinTechathon 2026 · International Track Topic C · Cross-border & Student Finance Assistant**

> **SAFETY/VERIFICATION BOUNDARY:** All payments, quotes, university records, beneficiaries, and BDT balances in this project are **SYNTHETIC INTERNAL SIMULATOR DATA**. No live bank integration, money movement, KYC/AML clearance, verified beneficiary ownership, real provider quote, authorized refund or real compliance screening exists. **Do not upload real identity, passport, payment card, banking or student financial documents.** This release is not suitable for financial production.

## What this ZIP contains

The complete cumulative V1→V2→V3→V4→V5→V5.1 source tree—not just a patch. Working local operations include authenticated student case management, invoice parsing, synthetic evidence comparison, fee quotes, explicit approval, BPCE evidence binding, simulator transaction ledger, local audit/reviewer, research dashboard with a 300-case *project-authored* synthetic benchmark, and V5 guidance/evidence export/local support records.

V5 adds:
- **Read-only safe-plan** (`GET /api/v1/cases/{id}/safe-plan`), returns bounded next-step suggestions, never calls an execution tool.
- **Evidence JSON export** (`GET /api/v1/transfers/{id}/evidence-export`), with document hashes, quote, approval, audit-chain status, local ledger, self-contained SHA-256 digest, accurate trust limitations.
- **Synthetic dispute guidance records** (`POST/GET /api/v1/support/disputes`), not a bank dispute or refund initiation.
- **Responsive Evidence & support UI** in standalone `/demo` (Chromium tested), and Next.js source page `/support` (not fully built/tested here).
- **No-store API responses and basic security headers**, production-mode guard against seeded demo credentials.
- **Editable 12-slide English defense PPTX**, demo script/captions, technical/security/research reports and Work-mode independent-audit instructions.

## New in V5.1 — genuine free local LLM tool calling

V5.1 adds an **Ollama `/api/chat` tool-calling loop**, designed for `qwen3:4b` with no paid API. The model can autonomously request SIX tenant-scoped READ-ONLY evidence, investigation, quote, policy and authorization-status tools. The FastAPI backend authorizes every tool, limits the reasoning/tool budget, rejects invented privileged tools, and records conversation history plus actual tool traces in SQLite. **No model can create an approval or execute a payment.** V5’s BPCE implementation continues to independently govern payment simulation.

- Backend: `services/api/app/local_agent.py`, `agent_routes.py` and new conversation database table (schema version 5).
- UI: Next.js `/copilot` and standalone browser preview `/demo#agent`.
- Security: 12 new backend contract/security tests; model responses MOCKED solely in these tests. Those tests are **not evidence of live Qwen inference**.
- Live evaluation CLI: `benchmarks/run_real_ollama_eval.py` only produces real-model metrics when *you* run Ollama locally; the ZIP does **not** contain fabricated Qwen quality/latency scores.
- Windows installation guide: **`docs/START_HERE_WINDOWS_BANGLA.md`** (start there).
- Known blockers: no Ollama binary/model available in the build container, no authorized bank/provider API access, no external independent human validation, no proven Next.js production build. Your laptop can verify live inference at zero API cost.

## Fastest verified way to run — Windows PowerShell

From this ZIP's root on Python **3.12** (Python 3.13 was used in the build environment), **after installing Ollama and running `ollama pull qwen3:4b`**:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r services\api\requirements.txt
$env:DEMO_SEED_PASSWORD='Choose-Your-Own-Strong-Demo-Password!'
$env:APP_ENV='development'
$env:ENABLE_DEMO_SEED='1'
$env:OLLAMA_MODEL='qwen3:4b'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir services\api --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000/demo**, log in as **student@borderproof.test** with the password you supplied, and use the **Payment lab → BPCE Security Kernel → Research & IntegrityBench → Evidence & support** views. Other seeded roles: reviewer@borderproof.test, auditor@borderproof.test, admin@borderproof.test; same locally selected demo password. Seed only works if `APP_ENV=development` and `ENABLE_DEMO_SEED=1`; it is rejected in production mode.

Linux/macOS: install requirements, set `DEMO_SEED_PASSWORD`, then `bash scripts/run_preview.sh`. The standalone preview is the tested full demo; it does not need Node or npm.

### Student demo path

1. Sign in; use the existing **Sample tuition planning case** or create the matching synthetic case.
2. In **Payment lab**, attach the provided synthetic invoice → extract → investigate → compare synthetic quotes.
3. Read source warnings → explicitly authorize → execute **INTERNAL SIMULATION** → inspect receipt.
4. In **BPCE Security Kernel**, inspect the dependency graph and versioned evidence snapshot.
5. In **Evidence & support**, inspect the safe next step, export JSON proof, create a local-only support record.
6. In **Research & IntegrityBench**, compare policy proxies and replay a synthetic fault case.

### API and evaluation commands

```powershell
python -m pytest -q services/api/tests
python scripts/check_locales.py
python -m benchmarks.stupay_integritybench.corpus
python -m benchmarks.stupay_integritybench.evaluator --split holdout --out benchmarks/results
python tests/e2e/test_v5_support_preview.py
```

Browser tests require Playwright and Chromium. The build container blocked direct Chromium navigation, so V5.1 browser interaction remains unverified here. Existing scripts in `tests/e2e` exercise V1–V4 UI. `docs/V5_VERIFICATION_REPORT.md` states which tests were observed actually passing in this environment.

### Optional Next.js frontend (NOT independently verified here)

```powershell
cd apps\web
npm install
npm run dev
```

Go to http://localhost:3000 with FastAPI running separately. The Next.js frontend consumes the local backend via `NEXT_PUBLIC_API_BASE_URL`. **npm registry access failed (`EAI_AGAIN`), so TypeScript semantic build, WebGL loading and Next.js production deployment have not been verified.** A static TypeScript parser check does not substitute for a build.

### Optional Docker

`docker compose up --build` with locally set `DEMO_SEED_PASSWORD` (see `.env.example`). Docker images were **not** built in this environment. Avoid public exposure of demo accounts, public database access or default/example passwords.

## Competition deliverables

- `submissions/BorderProof_AI_FinVeritas_10min_Defense.pptx` — editable English 12-slide deck with notes
- `submissions/DEMO_VIDEO_SCRIPT_EN.md` + `submissions/DEMO_CAPTIONS_EN.srt` — planned 4–5 minute script and captions for a future narrated video
- `submissions/BorderProof_AI_V5_Actual_Browser_Capture_SILENT.mp4` — **actual ~28.48s silent API-backed browser capture**, not the complete narrated competition demo
- `docs/V5_TECHNICAL_REPORT.md` — architecture, components and algorithm description
- `docs/V5_SECURITY_SELF_ASSESSMENT.md` — role boundaries, failure tests and known risks
- `docs/V5_RESEARCH_RESULTS_AND_LIMITS.md` — benchmark methodology, actual synthetic results, fair disclaimers
- `docs/V5_DATA_MODEL_CARD.md` — data and model provenance, bias/validation caveats
- `docs/V5_API_REFERENCE.md` — V5 endpoints and sample response shapes
- `docs/V5_RELEASE_STATUS_MATRIX.md` — honest 45-module state
- `docs/V5_SUBMISSION_CHECKLIST.md` — submission readiness and registration risks
- `docs/V5_DEPLOYMENT_GUIDE.md` — repeatable startup and portability checks
- `docs/V5_LICENSES_AND_ATTRIBUTION.md` — dependencies/reference attribution and license gaps
- `WORK_HANDOFF.md` — independent Work-mode QA and final repair instructions
- `SOURCE_MANIFEST_SHA256.txt` — hash of archive source entries

## Benchmark disclosure

`StuPay-IntegrityBench V4.1` has **300 project-authored synthetic cases**, including **60 stratified holdout**. The BPCE **rule proxy**, not a full production agent, accepted **5/48 unsafe-labeled** holdout cases; it also rejected **3/12 legitimate-labeled** cases. The heuristic fails on 50% of held-out synthetic prompt-injection cases. Comparisons are against **hand-coded** policy proxies, not genuine LLM/AP2 protocol implementations. Neither claims novelty proof nor banking safety. Re-run from the checked-in exact data to verify results.

## Status and deadlines

The organizers' **user-supplied** rule files specify a registration **and project submission** deadline of **2026-10-20 23:59 Beijing (21:59 Bangladesh)**. The registration workbook, DOCX and PDF conflict on identity scans, recipient addresses and UTC minute; refer to `docs/SOURCE_VERIFICATION.md` and verify with organizers. **A local ZIP is not official registration or submission.** No GitHub push, organizer email, completed narrated submission video or platform submission has been performed by this build; only a short genuine silent browser capture exists.

V5.1 addendum: `docs/V5_1_AGENT_REPORT.md` · Version report: `docs/V5_RELEASE_REPORT.md` · Last audit: `docs/V5_VERIFICATION_REPORT.md` · Independent handoff: `WORK_HANDOFF.md`.
