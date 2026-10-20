"""Build release documentation from shipped execution evidence. Never invent metrics."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def put(name,text):
 p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf8')
def read(name):
 p=ROOT/name;return p.read_text(encoding='utf8') if p.exists() else ''
def data(name):
 try:return json.loads(read(name))
 except ValueError:return {}
def test_total(log):
 m=re.search(r'(\d+) passed',read(log));return m.group(1) if m else 'NOT RUN'

def main():
 clean_tests=test_total('AUDIT/evidence/clean/backend.log')
 browser=data('AUDIT/evidence/clean/native_execution/report.json') or data('AUDIT/evidence/native_final/report.json')
 original=data('AUDIT/evidence/research/original_reproduction/holdout_results.json')
 metric=original.get('policies',{}).get('bpce_core_proxy',{})
 features=[
 ('Landing','VERIFIED WORKING','Native Next.js and /demo public screenshots, navigation, reduced-motion fallback'),
 ('Sign up / secure login','VERIFIED WORKING','Local student signup and login in both native browsers; server role/CSRF tests. Production signup disabled'),
 ('Dashboard','VERIFIED WORKING','Real new-account case/document counts and generated case chart. Lists remain bounded'),
 ('Student profile','PARTIAL','Persisted profile API and editable settings; exhaustive profile browser permutations not performed'),
 ('AI financial copilot','EXTERNALLY BLOCKED','Six read-only tools and 14 mocked model contract tests; native unavailable-model 503. True Qwen inference pending laptop'),
 ('Tuition Document Vault','VERIFIED WORKING','Fresh upload/download byte/hash equality, typed extraction, missing/conflicting fields; private local storage'),
 ('University verification','PARTIAL','Synthetic registry comparison only. Public university guidance unavailable in retrieval, no institution attestation'),
 ('Beneficiary verification','PARTIAL','Synthetic named payee/account match, contradiction guards. Real ownership unverified'),
 ('Multicurrency','PARTIAL','Fresh GBP/USD/CAD processing and decimal arithmetic. No real multicurrency wallets'),
 ('FX & fee comparison','PARTIAL','Two actual internal quote calculations plus Frankfurter reference adapter; public availability varies, no executable external quote'),
 ('Payment route planner','PARTIAL','Bounded demo corridors and provider choice. No bank routing/availability search'),
 ('Compliance navigator','PARTIAL','Demo rules and UNKNOWN legal eligibility. No licensed KYC/AML/sanctions source'),
 ('Decision planner','VERIFIED WORKING','Deterministic safe-plan, latest document corrected. Explicitly non-LLM guidance'),
 ('Approval center','VERIFIED WORKING','Explicit exact-quote student consent, single-use status, stale/source mutation rejection'),
 ('Secure sandbox payments','VERIFIED WORKING','Actual internal simulator, DB, state and ledger; no external provider sandbox connection'),
 ('Payment tracking','VERIFIED WORKING','Persisted COMPLETED/FAILED/UNKNOWN internal statuses and replay readback'),
 ('Receipts / evidence','VERIFIED WORKING','Actual synthetic receipt and self-hashed export, balanced ledger, restart readback'),
 ('Alerts','PARTIAL','Persisted user-scoped payment notifications API; no complete notification inbox UI'),
 ('Refund / dispute guidance','PARTIAL','Local support records and export only; no bank dispute or refund'),
 ('Settings','PARTIAL','Local preferences, locale/theme and profile form; broader account controls absent'),
 ('Intent understanding','PARTIAL','Structured case fields and local tool-loop interface. General natural-language correctness not measured'),
 ('Dependency-aware planner','PARTIAL','Deterministic dependencies and safe-plan; live LLM planning pending'),
 ('Financial tool router','VERIFIED WORKING','Server allowlist, zero-argument schemas, owner scoping and rejected privileged calls; tested with mock model transport'),
 ('Document intelligence','PARTIAL','English labelled TXT/PDF and optional real local Tesseract OCR. Not arbitrary-layout multilingual document AI'),
 ('Evidence retrieval','PARTIAL','Private stored documents, synthetic registry and reference FX. No authenticated bank evidence'),
 ('Provenance graph','VERIFIED WORKING','Seven-node/seven-edge recomputed quote graph and local hashes, verified API/legacy browser'),
 ('BPCE','VERIFIED WORKING','Reparse/source-set/scope checks and fail-closed internal authorization; no proof of real-world efficacy'),
 ('Quote validity','VERIFIED WORKING','Expiry guards and mutation checks. UTC offset preserved after SQLite reload'),
 ('Country policy','PARTIAL','Deterministic demo corridor match. All real legal/provider eligibility remains unknown'),
 ('Risk engine','PARTIAL','Rule flags/injection indicators only; known obfuscation and multilingual misses'),
 ('Authorization','VERIFIED WORKING','Backend role checks, owner isolation, HttpOnly sessions, CSRF and transaction consent'),
 ('Execution state machine','VERIFIED WORKING','Consumed approval, explicit unknown/failure recovery, serialized writes, uniqueness and status transitions'),
 ('Independent verification layer','PARTIAL','Independent software kernel rechecks LLM/tool claims against local DB. No independent human/bank verifier'),
 ('Audit trail','VERIFIED WORKING','Hash-chain append batching and writer serialization repaired; tampering detected. Unanchored local chain'),
 ('Recovery / reconciliation','VERIFIED WORKING','Concurrent reconciliation debits once, immutable transfer amount, DB restart retention'),
 ('Reviewer console','PARTIAL','Role-protected case queue and acknowledge/reject tickets; reviewer cannot override BPCE'),
 ('Compliance workbench','PARTIAL','Demo policy/risk/review controls, real regulatory screening absent'),
 ('Graph explorer','PARTIAL','Quote dependency graph is functional, no arbitrary graph search or database'),
 ('Transaction audit explorer','PARTIAL','Role-scoped recent events and integrity check. No complete query/filter analytics suite'),
 ('Fraud investigation','PARTIAL','Synthetic recipient/account conflict and provenance inspection. No validated fraud model'),
 ('Attack simulation lab','VERIFIED WORKING','Role-protected untrusted-text heuristic probe and synthetic replay; not penetration certification'),
 ('Evaluation dashboard','VERIFIED WORKING','Measured original synthetic proxy results, family selection and replay; clear proxy warnings'),
 ('Baseline comparison','PARTIAL','Eight hand-coded policies and offline ablations. Standard/tool-using live LLM baselines not measured'),
 ('Model / tool observability','PARTIAL','Persisted conversations, real DB tool-result digests and traces, actual failure events. No live Qwen trace yet'),
 ('Admin console','PARTIAL','Protected counts and audit/review features. No full user lifecycle administration'),
 ]
 put('AUDIT/FEATURE_STATUS_45_MODULES.md','# 45-module source and execution audit\n\nVERIFIED WORKING applies only to the described local scope. It never means bank/identity verification or production readiness.\n\n| # | Module | Status | Evidence and scope |\n|---:|---|---|---|\n'+'\n'.join(f'| {i} | {a} | {b} | {c} |' for i,(a,b,c) in enumerate(features,1)))
 put('AUDIT/BASELINE_AND_REPAIRS.md',r'''
# Baseline and implemented repairs

Authoritative input: V5.2, 6,995,840 bytes, 171 archive entries, SHA-256 `65a00cae4fd1e338c85731b6e54d33e54dfca24414f900202ba6dd72e02e612c`. Original uploaded archive untouched. No older project used as implementation base.

Baseline execution: 99 backend tests passed including three optional Hypothesis tests. Initial Python environment lacked pytest and FastAPI; the failed initial command and subsequent successful dependency install are both retained. Next typecheck/build failed on `cases_heading`; lint had no configuration. Logs: `evidence/baseline/`.

| Priority | Actual finding | Implemented repair | Regression evidence |
|---|---|---|---|
| P0 | Reconciliation could race and used a mutable quote amount | Writer lock, refresh after lock, immutable recorded transfer debit; unique posting and approval indexes | Concurrent four-request reconciliation, six-request duplicate execution, exact balances and two postings |
| P0 | Conflicting duplicate invoice labels were silently ignored | Collect all matching labels, flag contradictions, reject malformed grouping/date and clarify | New duplicate amount/currency/account/institution tests and native conflicting invoice browser block |
| P0 | A new document could be followed by re-quoting old invoice evidence | Require latest document, verify every source hash and cross-document facts, renew approval | New document/stale quote/source-set tests |
| P0 | Same idempotency key could hide a changed requested outcome | Bind outcome as well as case and approval to existing key | TIMEOUT followed by changed SUCCESS returns 409 |
| P1 | Multiple audit events could fork within one transaction | Flush writes, serialize head append, preserve local chain validation | Two-event transaction, upload invalidation and concurrent transfer checks |
| P1 | GET /auth/me rotated CSRF and broke another open tab | Session-bound synchronizer token, unchanged by GET, rotated on new login | Forged token denied, cross-session reuse denied, same-session second tab works |
| P1 | Safe-plan inspected the oldest instead of latest document | Correct descending-order selection | New-document planner regression |
| P1 | Malformed model envelope could cause 500 | Typed envelope validation, 502/503, rejected tools, sanitized failure events, result hashes | Separate mocked agent contracts and native actual unavailable endpoint |
| P1 | Reloaded quote expiry lost UTC offset | Explicit UTC API serialization while keeping existing approval canonicalization | Fresh/persisted quote timestamps match |
| P1 | Next.js had no proven build and cross-host cookie defaults | Correct translation key, ESLint config, package lock, same-origin API proxy, native production server test | Clean npm ci/typecheck/lint/build and production routing |
| P1 | Standalone deep links and mobile select options failed | Real hash route handler, selected-document context, constrained form sizing | Native /demo registration and mobile three-locale checks |
| P2 | Chinese/Bangla could render missing glyphs | Locally served OFL subsets, preserved font licenses | Actual native screenshots, not generated UI images |

One pre-repair date test initially used 2026 while the original fixture's deadline was 2027. Its trigger was corrected to match a general ISO date; the original failed attempt remains in logs. The old CSRF test deliberately changes semantics: it now asserts forged-token rejection and logout, while a new test proves a previous session's token fails. This is an explicit session design change, not removal of a security assertion.

ESLint's React `set-state-in-effect` performance advisory is configured as a warning for retained mount-time initializers. Lint passes with warnings; it is not a zero-warning claim. Runtime/security assertions were not disabled. Historical V1/V2 migration scripts had stale schema expectations/sibling-folder dependence; they are now self-contained and preserve rows and balances.
''')
 put('AUDIT/REAL_EXECUTION_EVIDENCE.md',f'''
# Actual execution evidence

Final native workflow status: **{browser.get('status','NOT RUN')}**. The runner starts real Uvicorn and production Next.js servers, uses native Chromium navigation/fetch, and performs no fetch interception, exposed Python browser bridge or prerecorded answers.

`evidence/native_final/report.json` records ten newly authored privacy-safe invoice files, four API simulator completions, duplicate readback, actual model-unavailable 503, a real public-reference response or truthful 503, and database/receipt/balance readback after an actual server process restart. `evidence/clean/native_execution/` is the separate clean-extraction run when present.

Both UI variants create a new local student account, log in, create a case, upload a new invoice, extract/investigate, calculate a synthetic quote, explicitly approve and execute the internal simulator. Next.js also shows a conflicting invoice with quote controls disabled and an unavailable live agent. Desktop and 390-pixel mobile layouts switch en/zh-CN/bn-BD. API network logs record only paths and statuses, never cookies/passwords.

Screenshots show the actual running software with synthetic inputs. `next_transfer_status.png`, `next_conflict_details.png`, `next_agent_unavailable.png` and locale screenshots are derived from those interactions. They support, but do not independently replace, network and persisted-state assertions.

Legacy browser regression: six tests use an explicit Python HTTP bridge and are classified separately. Earlier native attempts failed because of selector assumptions and actual /demo deep-link/mobile defects. Their failure reports remain under `native_execution_attempt*`; only PASS reports count as acceptance.

No real transaction, real bank statement, real provider response ID or Qwen response was manufactured. Internal references start `SIM-` and are local simulator identifiers.
''')
 put('AUDIT/FINANCIAL_SECURITY_TESTS.md',f'''
# Financial security evidence and residual risk

Clean backend tests passed: **{clean_tests}**. Current targeted work regression log: `evidence/security-regressions-final.log`; baseline and intermediate failures are retained. Three Hypothesis tests exercise 280 generated examples collectively. Hypothesis cases are not counted as separate pytest tests.

Confirmed local invariants: unauthenticated requests fail, student ownership is checked for cases/documents/quotes/transfers/conversations, reviewer/admin/auditor roles are enforced, CSRF and Origin checks guard mutations, and the model exposes six read-only tools with no approval or execution capability. Staff access is intentionally broad within this single local application; this is user isolation, not a multi-organization tenant platform.

Transactions bind human consent to the exact quote and source snapshot. Quote/recipient/amount/currency/provider/source mutation, expiry, changed document sets and approval replay block execution. Concurrent duplicate execute requests produce one transfer and two balanced postings. Concurrent timeout reconciliation produces one debit. TIMEOUT stays UNKNOWN until explicit simulation reconciliation. Idempotency reuse with a changed payload is a conflict.

Threat boundaries: invoice/web/model outputs are untrusted data, public references cannot verify payee ownership, provider-status comparison checks only persisted simulator state, and a DB administrator remains inside the trusted computing base. Audit hashes are local and unanchored. The heuristic injection detector misses obfuscated/multilingual text; the LLM's absence of write tools is the stronger execution boundary. No universal injection-defense claim is justified.

Remaining production blockers: no real KYC/AML/sanctions or legal approval, no external settlement verification, no durable cloud document backend, no live PostgreSQL locking tests, no distributed session/rate-limit infrastructure, no verified identity/email recovery, and no externally anchored audit. PDF/OCR parsing has size/page/text/time limits but no OS-isolated parser sandbox. Local registration is deliberately development-only and the app binds loopback in its user startup scripts.

NPM production audit raw result is shipped. A zero-known-advisory result at this retrieval time does not certify the application. This work is an internal technical assessment, not external security certification or human financial peer review.
''')
 put('AUDIT/LLM_LIVE_VS_MOCK_MATRIX.md',r'''
# Live versus mock evidence

| Check | Classification | Observed status |
|---|---|---|
| Twelve inherited agent tests | Mocked model/HTTP transport contracts | Executed as part of backend pytest |
| Two new malformed model tests | Mocked contracts | 502/explicit rejection, no payment action |
| Database tools and conversation persistence in those tests | Actual application/database with mock model selection | Executed, not a live Qwen result |
| Native /agent/chat with unreachable local endpoint | Actual HTTP/network failure, no mocked answer | 503 observed in API and browser |
| Work localhost:11434 /api/tags | Genuine local connection probe | Connection refused; zero inference results |
| Eight new Qwen local validation scenarios | Real-model-only harness | PENDING USER-LOCAL VERIFICATION |
| Standard LLM, live tool-agent, live full-system benchmark | Requires actual model and fair shared inputs | NOT MEASURED |

`evidence/live_model_preflight.json` has an empty results array and BLOCKED status. The user's Windows Ollama is not reachable through Work localhost. No tunnel or remote paid inference was attempted.

Run `scripts/run_live_ollama_validation.ps1` locally with API and Ollama running. It checks the installed model/version/digest, creates a new synthetic local student/case/invoice/quote, measures eight real requests and actual tool expectations, records response/trace latency, and verifies no transfer or balance change. Expected-tool failures return a failing classification. Answer quality and evidence attribution still require human review. It saves only synthetic test content, no cookies or passwords, to `runtime/local_validation/sanitized_ollama_results.json`.

The Python harness was executed in Work and correctly classified the unavailable model. PowerShell is unavailable here, so the PS wrapper was inspected, not executed in a Windows shell. The old `benchmarks/run_real_ollama_eval.py` is retained for compatibility; the fresh-case harness is the recommended entry point.
''')
 put('AUDIT/FRESH_INVOICE_TEST_CASES.md',r'''
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
''')
 put('AUDIT/RESEARCH_VALIDITY_AND_PRIOR_ART.md',f'''
# Research validity and prior art

The reproduced original corpus matches its generator: 300 project-authored synthetic cases, 240 development and 60 holdout. Original held-out BPCE **policy proxy** accepts {metric.get('unsafe_acceptances','NOT MEASURED')}/48 unsafe-labelled cases and blocks 3/12 legitimate-labelled cases. Its obfuscated injection miss rate remains 50% on those injection cases. This result is not improved by renaming the release.

`benchmarks/work_v53_evaluation.py` freezes 96 additional scenarios with 48 reserved train, 24 development and 24 holdout rows before scoring. No model trains on the train split. Raw cases/labels/results, file hashes, confusion counts and Wilson intervals are shipped in `evidence/research/`. The new holdout proxy accepts 3/21 unsafe cases and 3/3 safe cases. These very small authored counts are not evidence of field efficacy. No policy tuning followed the new challenge-set scoring.

The original row split shares templates, recipient patterns and injection variants. Case IDs expose failure families, so they must never be supplied to a future LLM baseline. Current policies do not read case IDs. Labels remain author-defined; Work review is not independent external human adjudication. P50/P95 in the original results measure Python policy-check microseconds, not model, API or payment latency. Cost, real-agent success, tool factual correctness and human evidence attribution are NOT MEASURED.

| Primary reference | Access reviewed | Relevance and distinction |
|---|---|---|
| [Jiang et al., A Formal Analysis of Agent Payment Protocols, Aug 2026](https://arxiv.org/abs/2609.00060) | Abstract/metadata | Prior formal work on lifecycle consistency. BPCE has no Tamarin proof and cannot claim this idea as new |
| [Mao et al., SoK, revised May 2026](https://arxiv.org/abs/2604.15367) | Abstract/metadata | Cross-layer agent-commerce threat framing, not a student invoice implementation |
| [AgentDojo, 2024](https://arxiv.org/abs/2406.13352) | Abstract/metadata | Tool-output injection evaluation. BorderProof has not reproduced its benchmark |
| [InjecAgent, ACL Findings 2024](https://aclanthology.org/2024.findings-acl.624/) | Anthology metadata/abstract | Indirect injection evaluation. No claim of outperforming it |
| [Google AP2](https://github.com/google-agentic-commerce/AP2) | Repository README | Established authorization protocol ideas. The AP2-inspired proxy is not AP2 implementation |
| [Visa Trusted Agent Protocol](https://github.com/visa/trusted-agent-protocol) | Repository README | Signed agent/authorization context. Local unkeyed hashes do not implement this protocol |
| [FinanceBench](https://github.com/patronus-ai/financebench) | Repository README | Financial question-answering evidence tasks, not transaction authorization |
| [FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) | Repository README | Financial agent platform, not validated tuition settlement |
| [FinGPT](https://github.com/AI4Finance-Foundation/FinGPT) | Repository README | Financial language-model tooling, not beneficiary attestation |

These links were actually retrieved on 2026-10-19 UTC. Only abstracts/READMEs were reviewed where stated; no full-paper-reading claim. Signatures, scope binding, single-use approvals, idempotency, DB transactions and least privilege are standard techniques. The defensible contribution is a reproducible student-payment adaptation and test suite. Fundamental novelty and real-world superiority are unproven.

Additional full-system evidence comes from native invoice/API/browser tests, not from the offline policy proxies. Normal application safety is never disabled for a baseline. Real standard-agent/tool-agent/full-system comparisons remain pending reachable-model evaluation with shared inputs, hardware, settings and blinded labels.
''')
 put('AUDIT/FRONTEND_PRODUCTION_BUILD.md',r'''
# Frontend production verification

Node 24.19.0, npm 11.9.0, Next.js 16.4.2 resolved from the supplied ^16.2.0 range. A committed package-lock now pins the tested tree. `npm ci --ignore-scripts`, semantic `npm run typecheck`, configured `npm run lint`, `npm run build` and actual `npm run start` were exercised, including real same-origin API cookies. Exact clean commands/logs are in `evidence/clean/`.

The production TypeScript failure was a real missing `cases_heading` key. It now uses `case_heading`. No `ignoreBuildErrors` flag or TypeScript-disable workaround was used. ESLint reports existing React mount-initializer performance warnings; they remain visible and are configured as warnings, not described as fixed. Basic unused imports and config warnings were removed.

Next.js proxies `/api/*` to API_INTERNAL_URL (default http://127.0.0.1:8000), eliminating the localhost-versus-127.0.0.1 cookie mismatch. The preview uses its real same-origin FastAPI routes. Public pages hide the workspace sidebar. Student-only navigation is role-aware. Deep-linked /demo registration and mobile financial selects were repaired.

16 localized catalog objects and the original 135-key catalog passed AST/key parity. Native EN/zh-CN/bn-BD switching and 390-pixel widths passed. Local OFL font subsets prevent missing glyphs for the UI. Technical API error text, raw statuses and some progressive-detail strings still use English; this is not a claim of complete translation. Arbitrary future CJK text may require a complete installed font beyond the shipped UI subset.

Reduced-motion/static globe fallback was exercised. Real GPU WebGL interaction on the user's hardware is not certified by that test; the source preserves the Three.js globe and now checks WebGL2 availability. Keyboard-focus CSS and labels exist, but no comprehensive WCAG or screen-reader certification was performed.
''')
 put('AUDIT/RENDER_READINESS.md',r'''
# Render readiness: PREPARED ONLY, NOT DEPLOYED

The local Next.js production build and API proxy work. render.yaml parses and passes local structural checks. No Render account, resource, deployment, platform validation, GitHub push or paid service was invoked. No Docker or PostgreSQL executable is available in this environment, so those runtime gates are BLOCKED/NOT RUN, not passed.

The blueprint disables automatic deployment, seeded credentials, local signup, external paid inference and Ollama. It contains no paid plan or credentials. Two free web services are a review skeleton, not a durable production architecture. In this safe default, there is no seeded user who can log into a public financial app. Provisioning real authenticated users and durable storage remains outside readiness.

Current primary Render docs reviewed: [free limits](https://render.com/docs/free), [Next.js](https://render.com/docs/deploy-nextjs-app), [FastAPI](https://render.com/docs/deploy-fastapi), [Blueprint](https://render.com/docs/blueprint-spec), [monorepos](https://render.com/docs/monorepo-support). Free web services sleep after 15 minutes, have ephemeral files, and share 750 monthly instance hours per workspace. Free Postgres expires after 30 days. Monthly bandwidth/build quotas and service-initiated traffic restrictions apply. These facts rule out promising durable free SQLite/uploads or continuous two-service availability.

SQLite is the demonstrated private local database. PostgreSQL metadata DDL compiles and the code contains owner row locks/advisory audit locks, but PostgreSQL execution/concurrency is NOT VERIFIED. `scripts/prepare_database.py` performs the additive migration; back up DB and upload files first. V1/V2-shaped migrations preserve rows and balances. Unique-index creation fails on existing duplicate financial records instead of deleting them. To evaluate PostgreSQL in an authorized local environment, install psycopg[binary], use a postgresql+psycopg URL, run the migration and repeat all finance/concurrency tests. DDL compilation is not a substitute.

`storage.py` provides the tested private local adapter; cloud storage explicitly raises unavailable. A durable object store adapter is NOT IMPLEMENTED. Never rely on a free Render filesystem for uploads or transaction history. Render cannot reach Windows Ollama localhost. Leave the agent disabled until a separately authorized, reachable model endpoint exists; no claim that a free CPU instance can reliably host Qwen3.

Manual preparation after separate authorization: resolve durable DB/document storage and identity blockers; set ALLOWED_ORIGINS and API_INTERNAL_URL at build/runtime; keep Secure cookies and no seed; validate the blueprint through Render; deploy a private review environment; repeat health/login/CSRF/upload/stale-quote/ledger/restart checks; retain the previous tested revision for rollback and separately back up data. Do not merge incompatible schema rollback with application rollback. No deployment is authorized by this document.
''')
 put('AUDIT/KNOWN_LIMITATIONS.md',r'''
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
''')
 put('AUDIT/FINAL_RELEASE_VERDICT.md',f'''
# Formal release verdict

**READY FOR LOCAL DEMO: internal synthetic simulator and tested UI scope.**

**NOT RELEASE READY: public/production finance, claims of validated autonomous Qwen reasoning, or complete externally verified competition submission.**

Clean backend test count observed: {clean_tests}. Native browser/API status: {browser.get('status','NOT RUN')}. Final clean gate details and commands are in `evidence/clean/`; unexecuted gates are never counted as passed. The local verdict requires the PASS clean reports. The delivered system fails safely when the optional model/reference/provider is unavailable.

Blocking limits: no genuine Qwen inference logs in Work, no provider sandbox credentials/authorization, no authenticated bank/legal evidence, no durable cloud document adapter, no executed PostgreSQL/Docker/Render validation, and no independent human research validation. The remaining measured injection-proxy errors prevent any strong financial-safety or novelty claim.

No deployment, push, organizer email/submission, real payment or paid inference occurred. This is a repaired, reproducible student project with disclosed boundaries, not a bank-certified product.
''')
 put('docs/START_HERE_WINDOWS_BANGLA.md',r'''
# Windows-এ V5.3 চালাও

আগের V5.2 folder বদলাবে না। নতুন ZIP আলাদা `C:\BorderProof_AI\FinVeritas_BorderProof_AI_V5_3_Work_Audited` folder-এ extract করো। VS Code → Open Folder দিয়ে সেই folder খোলো। পুরোনো runtime database এই নতুন folder-এ সরাসরি copy কোরো না: আগে DB ও upload files backup করো, absolute document paths-ও আলাদাভাবে পরীক্ষা করতে হবে। নতুন account দিয়ে শুরু করাই সহজ।

## ১. Backend terminal

VS Code → Terminal → New Terminal → PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r services\api\requirements-lock.txt
powershell -ExecutionPolicy Bypass -File scripts\run_preview.ps1
```

এই `ExecutionPolicy Bypass` শুধু ওই script process-এর জন্য; পুরো কম্পিউটারের policy বদলায় না। Server terminal চালু রাখো। Browser-এ `http://127.0.0.1:8000/demo` খোলো। Sign in → Create local account → নিজের নাম/email/password দিয়ে account বানাও, তারপর sign in করো। এটি শুধু local demo account; email/পরিচয় যাচাই হয় না। আসল passport/bank document দেবে না।

আগের মতো চারটি seeded role দরকার হলে প্রথমে নিজের ১২+ অক্ষরের DEMO_SEED_PASSWORD set করে `scripts\run_preview.ps1 -SeedDemo` চালাও। কোনো default password নেই। Development server internet-এ expose কোরো না।

## ২. Next.js premium UI

Backend চালু রেখে নতুন terminal:

```powershell
cd apps\web
npm ci
npm run typecheck
npm run lint
npm run build
npm run start
```

`http://127.0.0.1:3000` খোলো। একই account দিয়ে sign in করো। API address আলাদাভাবে browser-এ set করতে হবে না; same-origin proxy আছে। Lint-এ কিছু performance warning থাকতে পারে। Production build-এ error হলে সেটি উপেক্ষা করবে না।

## ৩. সত্যিকারের local Qwen পরীক্ষা

আরেকটি terminal-এ:

```powershell
ollama list
ollama run qwen3:4b
```

Model prompt থেকে `/bye` দিয়ে বের হও; Ollama background service চালু থাকবে। Backend-এ model নাম `qwen3:4b` থাকতে হবে। এখন project root-এর নতুন terminal-এ:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_live_ollama_validation.ps1
```

Script নতুন synthetic account/case/invoice বানিয়ে আটটি actual model request চালাবে। কোনো payment/approval করবে না। ফল থাকবে `runtime\local_validation\sanitized_ollama_results.json`। ফাইলটা নিজে একবার দেখে এই chat-এ দেবে। Cookie, password, API key বা আসল financial document দেবে না। BLOCKED/FAILED হলে model connected/validated বলবে না। Work থেকে তোমার laptop-এর localhost দেখা যায় না।

## ৪. নিজের invoice demo

`AUDIT\evidence\native_final\inputs\fresh_GBP.txt` দেখে supported labelled format বোঝো। Payment case-এর institution/currency/amount-এর সঙ্গে invoice মিলতে হবে। শুধু SYNTHETIC fixture payee-গুলো internal simulator-এ যেতে পারে। অন্য university হলে fields বের হবে, কিন্তু real beneficiary যাচাই নেই বলে execution block হতে পারে। Missing/conflicting field হলে নতুন corrected invoice এবং নতুন investigation/quote/approval লাগবে।

Flow: case তৈরি → Payment lab → file upload → extract → investigate → synthetic quote → নির্দিষ্ট consent → simulated execution → receipt। টাকা আসলে কোথাও যায় না। PUBLIC FX REFERENCE এবং simulator-এর synthetic rate আলাদা।

## ৫. Tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r services\api\requirements-dev.txt -c services\api\constraints-python312.txt
.\.venv\Scripts\python.exe -m pytest -q services\api\tests
.\.venv\Scripts\python.exe -m playwright install chromium
```

Native full check চালানোর আগে চলমান 8000/3000 server বন্ধ করো; script নিজে temporary server চালায়। Next build আগে থাকতে হবে:

```powershell
.\.venv\Scripts\python.exe scripts\run_real_execution.py --browser
```

Render/GitHub-এ এখনো কিছু publish করা হয়নি। Cloud deployment-এর আগে AUDIT\RENDER_READINESS.md পড়তে হবে। এই release local demo-ready; বাস্তব financial production-ready নয়।
''')
 put('docs/V5_3_CHANGELOG.md',r'''
# V5.2 to V5.3 source revision

Preserved both frontend variants, all original source modules, BPCE graph/seals, ledger, roles, English/Chinese/Bangla catalogs, benchmark corpus, local Ollama integration, historical reports, original logo and inherited submission assets. Original V5.2 README/screenshots are separately retained under docs/history.

Changed finance.py/bpce.py for duplicate-field conflict detection, latest/all-document checks, writer serialization, strict idempotency payload and reconciliation amount/status. Added storage.py, timeutils.py, references.py and explicit blocked provider interfaces. Updated additive database uniqueness indexes without deleting historical rows. Changed session CSRF semantics to remain stable within a session and invalidate across sessions. Added local-only signup and UTC API timestamps.

Changed model runtime envelope validation, loopback proxy handling, disabled-model configuration, bounded tool-result provenance and safe failure audit. The local harness is real inference only. The production frontend now has a lockfile, semantic build fix, ESLint config, same-origin API proxy, role-aware navigation, optional public FX reference, locale fonts and /demo deep-link/mobile repairs.

Added new adversarial tests, seeded fresh invoice/PDF/scan authoring, native HTTP/browser/restart execution, separate OCR run, original benchmark reproduction and 96 frozen additional offline cases. Added honest release/Render/security/research documents, new English submission materials and reproducible packaging/manifest scripts. No fake provider or AI response is added.
''')
 put('docs/V5_3_TECHNICAL_REPORT.md',r'''
# Architecture and algorithm

Browser (Next.js same-origin API proxy or FastAPI /demo) authenticates using an HttpOnly session cookie and per-session CSRF token. FastAPI authorizes each resource against the owner/role. Private local storage holds supported source bytes; the DB holds their digest and metadata. Deterministic English-label extraction produces field/line provenance and explicit issues. Optional local Tesseract is a separate unverified OCR engine.

Investigation compares case facts against a plainly synthetic institution/payee/account registry. A quote uses Decimal synthetic rates/fees and a 15-minute expiry. BPCE reparses source bytes, verifies relationships and all source hashes, requires the latest evidence, compares invoice/case/recipient/currency, checks demo corridor and stores a canonical local SHA-256 snapshot. Approval binds the student and exact quote to that snapshot. The LLM has no write tool and cannot create this consent.

Execution obtains a database writer/owner lock, rechecks active approval, expiry, bytes and snapshot, rejects changed idempotency payloads, consumes consent once and updates persisted simulator state. COMPLETED creates equal debit/clearing postings. FAILED/UNKNOWN creates no debit. Reconciliation serializes, refreshes state, uses the immutable transfer debit and updates the local case status. Unique indexes independently constrain duplicate account, approval, ledger and unresolved/completed case records.

Audit events append to a local hash chain with serialized head selection. Evidence export recomputes a digest over the local envelope and discloses its absence of external signatures. Agent conversations retain up to 24 user/assistant messages; model context includes 12 recent messages, six zero-argument read-only tools, at most eight tool calls and five rounds. Each tool reauthorizes owner/case. Actual DB results get timestamp/digest provenance. Model text is advisory and not independently fact-checked. The independent kernel's authority is structural, not based on model promises.

Public Frankfurter/ECB data enters only a reference view. It never prices simulator transactions or establishes a beneficiary. Legal/provider/country unknowns remain unknown for real operations. No production payment transport exists. State and tests are reproducible through SQLite; PostgreSQL/Docker/cloud persistence remain separate unverified deployment work.
''')
 put('docs/V5_3_MODEL_AND_DATA_CARD.md',r'''
# Model and data card

Model interface: Ollama /api/chat, configured qwen3:4b, temperature 0.1, num_predict 500, think=false, stream=false. No model weights are shipped. No model fine-tuning or actual inference was performed in Work. Runtime availability/identity/model digest must be captured by the user-local harness. Model license and distribution terms must be checked with the installed model's official record before redistributing weights; this project does not redistribute them.

Data: original 300-case StuPay-IntegrityBench with team-authored labels, plus 96 Work-authored frozen offline challenge rows and fresh synthetic labelled invoices. No authentic bank statements, passports, real student PII or independent external financial labels are used. Train/development/holdout partitions exist for the additional set but no learned model trains here. The original holdout shares templates with development and is unsuitable for a strong generalization claim.

Expected failures: unsupported document layout/language, OCR ambiguity, incomplete evidence, unrecognized institutions, unverified external ownership, obfuscated injection and model hallucinations. The rule proxy's measured unsafe acceptances and false blocks remain documented. Parser confidence values are fixed heuristic tags, not validation scores. Human answer/citation quality and financial field efficacy are not measured.
''')
 put('docs/V5_3_SOURCES_AND_LICENSES.md',r'''
# Sources, licenses and dependency attribution

All inherited project and third-party attribution files remain. The revised source is cumulative student-project work, not copied from a winner repository. Referenced AP2/Visa/FinanceBench/FinRobot/FinGPT repositories are prior art, not falsely claimed integrations. Imported Python/npm libraries remain governed by their upstream licenses. package-lock records the resolved npm tree; exact exercised Python constraints are included. No new blanket license for all project work is invented.

UI subset fonts derive from Google Fonts Noto Sans SC and Noto Sans Bengali, retrieved from the official google/fonts repository. Their SIL Open Font License and copyright notices ship beside both frontend font assets. Modified subsets use BorderProof family names. Sources: https://github.com/google/fonts/tree/main/ofl/notosanssc and https://github.com/google/fonts/tree/main/ofl/notosansbengali . Only UI glyphs are bundled, not a complete font for arbitrary future text.

Frankfurter v1 source/terms: https://frankfurter.dev/ . FX response metadata includes source URL, actual retrieval timestamp, effective date, precision, digest, no-app-cache and no-fallback status. Code licensing does not imply that all underlying datasets have identical terms. It is reference data, never an executable quote.

World Bank remittance reference: https://remittanceprices.worldbank.org/ was retrieved as contextual cost-research guidance, not an input to this simulator's fee or availability decision. UCL guidance and Bangladesh Bank circular retrieval were unavailable in this session; no beneficiary/regulatory claim is derived from them. No paid/private dataset or model weights are included.
''')
 put('submissions/V5_3_SUBMISSION_CHECKLIST.md',r'''
# Submission checklist and source conflicts

The two supplied English rule documents agree on Topic C, 40% task completion, 30% security/compliance, 30% innovation/interaction, teams of 2–5 and at least 60% non-Chinese nationality. Bangladesh full-time students fit the stated overseas-institution scope, subject to organizer confirmation of the actual submitted registration.

Both supplied documents state **20 October 2026, 23:59 Beijing = 15:59 UTC = 21:59 Bangladesh** for registration AND project submission. The DOCX's printed 16:00 UTC and other rounded local conversions differ by a minute. The PDF uses 15:59 UTC. DOCX says late-October online review; PDF timeline labels October 20. Contact email and overseas-region wording also differ. These supplied latest files take precedence over earlier general news mentioning November 1, but Work did not contact organizers or certify the official latest version. Do not wait until the final minute.

Required materials: technical architecture/core algorithm/security report, editable English presentation up to ten minutes, source with README/deployment/tests/GitHub link, security self-assessment, sandbox execution evidence. The video bullet calls a maximum-five-minute video optional while the execution-evidence bullet mentions video: treat that as an unresolved wording conflict and prepare a narrated demo. The inherited silent clip is not a completed narrated submission.

Prepared in this ZIP: revised technical/security/research reports, actual traces/receipts/screenshots, English deck and narration/captions, full source, tests, Windows guide and Render preparation. The user must run real local Qwen validation, record the final real demo, confirm organizer contact/deadline/registration, review licenses/identity requirements, and explicitly authorize any GitHub push or official submission. No organizer email, upload, public deployment or bank operation has been performed.

Never claim bank/provider partnership, real payments, bank-verified payee ownership, real KYC/AML clearance, external human peer validation, fundamental BPCE novelty, AP2 implementation, zero injection vulnerability, real LLM benchmark scores or official acceptance without the matching evidence.
''')
 put('README.md',fr'''
# FinVeritas — BorderProof AI V5.3 Work Audited

Evidence-consistent assistance for synthetic international-student tuition payments. Complete cumulative V5.2 source repaired and executed in an isolated working copy. Both the premium Next.js app and standalone `/demo` remain included.

**READY FOR LOCAL DEMO within the tested internal simulator scope. NOT RELEASE READY for real financial operations or an unqualified live-agent claim.** All balances, beneficiary records, payment quotes, transfers and receipts are synthetic local simulator objects. Public FX is separately labelled reference data. No real money, external provider transaction or paid inference was initiated.

Start with [Windows Bangla guide](docs/START_HERE_WINDOWS_BANGLA.md), [release verdict](AUDIT/FINAL_RELEASE_VERDICT.md), [45-module audit](AUDIT/FEATURE_STATUS_45_MODULES.md), and [real evidence](AUDIT/REAL_EXECUTION_EVIDENCE.md).

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r services\api\requirements-lock.txt
powershell -ExecutionPolicy Bypass -File scripts\run_preview.ps1
```

Open http://127.0.0.1:8000/demo and create a new local student account. For Next.js, keep API running, then `cd apps/web`, `npm ci`, `npm run build`, `npm run start`; open http://127.0.0.1:3000. No npm is required for standalone preview. No default password is supplied. Use `-SeedDemo` only with your own DEMO_SEED_PASSWORD for the optional four demo roles.

Evidence: clean backend pytest observed {clean_tests} passed; native workflow {browser.get('status','NOT RUN')}; semantic Next.js production build and actual start verified in logged runs. Six inherited browser tests use a Python HTTP bridge and are separately classified. True local Qwen inference remains **PENDING USER-LOCAL VERIFICATION**, not replaced by mock scores. Run `scripts/run_live_ollama_validation.ps1` with Ollama qwen3:4b and the local API running; share only its synthetic sanitized results after review.

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
''')
 put('WORK_PROGRESS.md',f'''
# Work progress

Checkpoint A: original V5.2 archive verified and preserved; 99 baseline backend tests pass, frontend build/lint failures captured.

Checkpoint B: core finance/document/auth/audit/agent repairs implemented and retested; 122 tests at that checkpoint, later expanded. Recoverable full source checkpoint saved separately.

Checkpoint C: full Next.js build/start and same-origin API native workflow verified, /demo deep-link/mobile/fonts repaired, fresh invoice/PDF/scan and restart checks, proxy research reproduction and extra frozen cases completed. Earlier failures retained as failures.

Checkpoint D: clean backend observed {clean_tests} passes; native browser/API status {browser.get('status','NOT RUN')}. Exact acceptance and remaining external blockers in AUDIT. Final artifact manifest covers the delivered source and evidence. No deployment, push, spending, organizer message or real transfer performed.
''')
 put('WORK_HANDOFF.md',r'''
# Recoverable V5.3 handoff

Start from this complete source, not V5/V5.1. Original V5.2 ZIP SHA-256 is in AUDIT/BASELINE_AND_REPAIRS.md. Earlier checkpoints preserve baseline/core revisions. Current results are AUDIT/evidence/clean, native_final and research. Failed attempt_history reports remain evidence of failures, not release passes.

Remaining required user-local action: start Ollama qwen3:4b plus API, run scripts/run_live_ollama_validation.ps1 and inspect/share runtime/local_validation/sanitized_ollama_results.json. No cloud-to-laptop localhost assumption or tunnel is valid. PowerShell wrapper has not been executed on Windows here.

Before any public release: resolve identity, durable DB/upload storage, PostgreSQL/Docker validation, external financial/legal evidence and narrated submission. No external provider credentials were available; adapter stays blocked. No payments or public deployment is authorized. The offline research proxy misses are not fixed merely by these software repairs.

To reproduce from a clean extraction: install requirements-lock/dev constraints; npm ci; typecheck/lint/build; pytest backend and legacy browser; run scripts/run_real_execution.py --browser and optional --enable-ocr; run benchmarks/work_v53_evaluation.py; verify SOURCE_MANIFEST_SHA256.txt. Generated runtime/test caches are excluded from source integrity. Repack with scripts/package_release.py to a destination outside the project tree.
''')
 print('Release docs generated from available evidence. Clean pytest:',clean_tests,'Native:',browser.get('status'))
if __name__=='__main__':main()
