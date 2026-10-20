# V5.1 — Free Local Autonomous Agent: engineering and verification

## Executive verdict
V5 originally shipped with a deterministic next-step planner and an optional single explanatory LLM call. It was **not** a genuine autonomous tool-calling financial agent. V5.1 now implements a genuine *transport-ready* Ollama `/api/chat` tool-calling loop with bounded runtime, tenant-scoped read-only tools, SQLite conversation history and UI. **The model did not actually run in the build environment.** The implementation is tested by mock-model contract/security tests; real inference, quality and latency await the Windows machine.

## Architecture
Student browser → authenticated FastAPI session + CSRF → tenant-checked `agent/chat` route → Ollama local `qwen3:4b` `/api/chat` (when running) → signed-in principal bound tool dispatcher → read-only SQL evidence + BPCE quote inspection → contextual tool result to Ollama → plain-language response + actual trace → SQLite conversation. The backend never gives the model an endpoint capable of payment execution or authorization.

The six allowlisted tools:
1. `inspect_case` — user-supplied synthetic/unverified fields and document count.
2. `inspect_invoice_evidence` — latest extraction and known missing fields, explicitly unverified.
3. `inspect_investigation` — synthetic beneficiary fixture and deterministic checks.
4. `compare_sandbox_quotes` — existing internal simulated provider quotes, amounts and expiry.
5. `inspect_approval_status` — existing approval and transfer readback plus BPCE quote integrity state.
6. `inspect_demo_policy` — local corridor policy and legal/KYC unknowns.

No tool can call `approve()`, `execute()` or arbitrary HTTP/SQL/file-system operations. Unknown tool calls and calls with extra arguments are rejected. Model reasoning is capped at 5 rounds and 8 tool calls. Repeating a tool returns a note, preventing identical expensive queries. A service failure returns HTTP 503 and no model answer is fabricated or recorded.

## Trust boundaries
- User-entered fields and invoice extractions are **untrusted document content**. Data enters the tool reply with provenance and an explicit untrusted-content notice.
- LLM output is **never authoritative evidence**; a model can still make mistaken or injected claims. Consumers must independently check tool trace and source.
- BPCE's security checks remain server-side at sandbox execution. Agent tool calling cannot bypass consent, receipt status or quote seals.
- Conversations are locally stored in plaintext SQLite; avoid personal documents, passports, real banking details. Production encryption/deletion/retention policy is **not implemented**.
- Local Ollama is the recommended endpoint. Nonlocal inference endpoints are blocked unless HTTPS and `ALLOW_REMOTE_OLLAMA=1`; that can transmit data to a third party.

## Actually tested
- 84 earlier backend API/security tests passed with the V5.1 schema migration after updating their expected schema version.
- 12 newly added model-contract/API security tests passed, including tool selection/execution trace, immutable simulator balance, role/tenant separation, CSRF, forbidden tool rejection, error handling, argument injection and call budget.
- Original V5 schema → new schema `5` migration rerun on **independently extracted V5 original ZIP** preserved legacy user row.
- Inline browser-preview JavaScript syntax passed using Node `--check`.
- **No full live Qwen test was performed**, because Ollama/model were absent from the build environment.
- **No Chromium navigation-based browser E2E was performed**, because this execution environment blocked browser navigations (`ERR_BLOCKED_BY_ADMINISTRATOR`).
- **No full Next.js production build** was completed here (no npm dependency installation).

## How to obtain real observations
1. Follow `docs/START_HERE_WINDOWS_BANGLA.md`.
2. Install Ollama, pull `qwen3:4b`, start FastAPI from project root.
3. Use the `AI agent` screen to ask about an existing synthetic case.
4. Run `python benchmarks/run_real_ollama_eval.py --count 8` in a prepared Python environment.
5. This creates **genuine locally observed** output at `runtime/local_ollama_real_eval.json`; upload it for critical review. It contains no fabricated model scores. The eight scenarios/expected tool names are project-authored; this is not independent validation.

## Research vs. independent validation
The existing StuPay-IntegrityBench is 300 **project-authored synthetic** cases. It is useful for reproducible engineering tests, not independent bank verification. Its reported policy-proxy results are unchanged from V4/V5. V5.1 adds a live evaluator, not fake published Qwen results. A literature review by the code authors (or the AI developer) cannot constitute independent human peer review. No external reviewer was engaged.

## Remaining high-priority failures
- Full live Qwen tool-calling correctness, injection rate and latency **unverified**.
- No real bank or university-authenticated beneficiary ownership registry.
- No real provider sandbox credentials / settlement reconciliation.
- No expert-labeled independent holdout corpus.
- No full Next.js build/browser deployment verification.
- Browser surface still permits user-authored synthetic-only data; do not connect to real payment rails.

## Reference documentation
- Ollama tool calling: https://docs.ollama.com/capabilities/tool-calling
- Ollama REST API: https://docs.ollama.com/api
- Official Ollama Windows download: https://ollama.com/download/windows
- Qwen3 models: https://ollama.com/library/qwen3
- AP2 prior-art: https://ap2-protocol.org/
- AgentDojo: https://arxiv.org/abs/2406.13352
- FinanceBench: https://arxiv.org/abs/2311.11944

These are reference URLs; this report does not assert full-paper independent peer review.
