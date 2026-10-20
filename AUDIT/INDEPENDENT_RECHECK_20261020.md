# Additional independent recheck — 2026-10-20

## Scope
Rechecked user-supplied V5.3 Work Audited archive without overwriting the application. The uploaded final archive SHA-256 is `2ea02034db87e06fba7ff009e59eddb41248b76e482f978664ca6372bf7e3cb3` and passed ZIP CRC integrity (`testzip() = None`). Recovery checkpoint SHA-256 is `1e6e34e6ebef4a577b260b88f05551333eff99547b639876a7444345b93940ef`, consistent with RESUMED_ACCEPTANCE.

## Independent backend execution
Command: `PYTHONPATH=services/api python -m pytest services/api/tests -q -x --durations=5`.
Observed locally in the independent review container: **127 passed, 1 skipped, 0 failed**, 34.78 s. The optional Hypothesis package is not installed here. Work's 130 passed claims correspond to a different dependency environment and are preserved as historical evidence, not silently substituted for this run.

## Source-level checks
`services/api/app/local_agent.py` integrates real Ollama `/api/chat` through HTTP (model configurable, default qwen3:4b) with six read-only allowlisted backend tools; rejects unknown tool or nonempty arguments. The system warns that tool data are untrusted. No payment-approval or execution tool exists in agent's allowlist. These are source inspection findings, **not** proof of real local Qwen tool-call success or comprehensive agent security.

## Current demonstrated strengths
- Actual internal synthetic transfer ledger and database-restart receipt evidence, as reported with artifacts in `AUDIT/evidence/recovery_20261020`.
- Existing financial security regressions and fresh unseen invoice evaluation in the submitted evidence.
- Next.js production-build and headless browser evidence in prior Work logs. Not re-executed in this recheck environment.

## Critical competitive and release gaps
1. **Real Qwen agent evaluation**: user-local Ollama is installed but project-to-model-to-tools is not yet verified. Run `scripts/run_live_ollama_validation.ps1` on Windows with Ollama and FastAPI up. Do not claim real autonomous financial reasoning until actual outputs/traces pass independently inspected cases.
2. **Unsafe acceptance**: existing authored BPCE rule-proxy holdout accepts **5/48** unsafe cases. Do not change test labels or suppress these failures to make the metric look better. Improve controls then rerun unchanged frozen tests plus a fresh blind set.
3. **Fraud/identity provenance**: no authentic bank beneficiary verification; provider sandbox connectors require authorized access; synthetic quotes and internal receipts must remain unmistakably labeled.
4. **Research independence**: deterministic policy proxy results, not fair head-to-head real-agent/AP2 benchmark or independent human-validated data.
5. **External readiness**: actual PostgreSQL/Render cloud execution, durable uploaded file storage, production security review and full locale/a11y certification remain pending.
6. **Competition materials**: final narrated ≤5-min video and proof of registration/submission remain separate user actions.

## Priorities for a competition-quality submission
P0: complete official submission before applicable deadline; do not postpone while pursuing perfect architecture. P0: local live Qwen tool-call and end-to-end invoice-to-internal-payment evidence; capture sanitized logs and screen video. P1: fix the measured unsafe classifications without benchmark leakage and compare fair baselines. P2: improve live university/payment evidence and external sandbox **only if genuinely available**, then post-submission product hardening. Extra visual modules are not the bottleneck.

## Honest decision
**READY FOR LOCAL SYNTHETIC DEMO** (based on archived Work evidence and backend regression). **NOT READY FOR PRODUCTION FINANCIAL SERVICES OR VERIFIED LIVE-AGENT PERFORMANCE CLAIMS.** No application code was rewritten during this supplementary audit because no reproducible new code defect was established beyond already disclosed research/security limitations. Packaging this report is documentation hardening, not a claim that those gaps were repaired.
