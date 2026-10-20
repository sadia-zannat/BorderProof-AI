# V5.1 Release Verification — observed 2026-10-19

**Package:** `BorderProof_AI_V5_1_Free_Agent.zip` — cumulative V1–V5 + V5.1 local agent upgrade.

| Check | Actual observed result |
|---|---|
| Backend regression, including V5.1 tests | **96 passed, 1 skipped** (`pytest services/api/tests`) |
| New V5.1 tests | 12 model-contract/security tests, mocked model transport, not live Qwen inference |
| Original V5 database schema migration to version 5 | PASS with previously inserted user record preserved |
| EN/Chinese/Bangla translation parity | 119 identical keys each |
| Web TS/TSX syntax parse | 14 files / 0 syntax diagnostics; NOT a full Next.js build |
| Standalone inline JS parse | Node `--check`: PASS |
| Python compile | `python -m compileall`: PASS |
| Chromium E2E with new V5.1 UI | BLOCKED BY ENVIRONMENT (`ERR_BLOCKED_BY_ADMINISTRATOR`), NOT VERIFIED |
| Real local Qwen3 live tool-calling | NOT RUN; Ollama executable/model unavailable in build environment |
| External bank/provider validation | NOT CONNECTED |
| Independent human benchmark labels | NOT PROVIDED |
| Main backend sandbox real-world settlement | NEVER ENABLED |

**Why 1 skipped:** optional Hypothesis package suite is not installed in this environment. This is not a passed property-based test.

The package includes a Windows setup guide and 8-scenario *authored internal* live-agent runner to generate real observations once installed locally. Benchmark scores from the original V4 deterministic proxies remain synthetic historical results; they are not live model results. The original V5 PPTX and silent video have **not** been updated to represent a validated Qwen demonstration.

**Full verification on the user's laptop still required:** install Ollama, pull `qwen3:4b`, run the agent UI, execute the real model evaluator, run `npm install && npm run build`, and review failures before official submission.
