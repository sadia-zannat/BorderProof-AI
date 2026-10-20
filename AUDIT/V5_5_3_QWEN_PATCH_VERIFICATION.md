# V5.5.3 Agent Output-Limit Candidate - Verification Status

Source: official V5.5.2 Windows-compatible checkpoint (unchanged except enumerated patch and documentation).

Real user-local V5.5.2 Qwen3:4b test, 2026-10-20: 5/9 HTTP 200; four HTTP 502 were exactly `Model reached generation limit; incomplete answer withheld` (L02, L04, L06, L08). Ollama was running, and model produced actual answers for five requests. No financial side effects observed. Evidence routing was deterministic server-side, not autonomous model routing.

New V5.5.3 changes:
1. Ollama non-streaming generation budget 900 -> 1600 tokens, timeout 65 -> 115 seconds.
2. Evidence-first Qwen input is a fresh, short, 3-message task, with deterministic per-tool data projection. Full raw observations stay in the authorized audit trace with evidence SHA256.
3. One retry on unusable or length-truncated model response uses a fresh bounded prompt. No rule allowing payments, changing authentication, or inventing evidence was introduced.
4. Three agent transport/evidence regression tests added.

Verification performed in container (mock model transport):
- Local agent tests: 22 PASSED (includes three new tests)
- Network, research, BPCE tests: 47 PASSED
- API, finance, release tests: 49 PASSED
- Work and optional property tests: 31 PASSED, 1 SKIPPED
TOTAL: 149 PASSED, 1 SKIPPED across four separate runs. A single combined suite was attempted but interrupted by container timeout; no combined-suite PASS is claimed.

NOT PERFORMED: Windows Qwen3:4b actual local inference for V5.5.3, revised Next.js production build, real banking/provider verification, independent human factual evaluation, production security approval.

Re-run on Windows after stopping the previous server:

Terminal 1 in this new extracted project folder:
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r services\api\requirements-lock.txt
python -m pytest -q services\api\tests
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run_preview.ps1

Terminal 2 in project root:
.venv\Scripts\activate.bat
ollama list
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run_live_ollama_validation.ps1

Human-review the JSON output at runtime\local_validation\sanitized_ollama_results.json. Even 9/9 HTTP 200 requires verifying citations, uncertainty, quote fee currency and no side effects. If output again contains generation-limit failures, provide the JSON and keep V5.5.3 labeled candidate, not validated release. Do not upload .env, local data or secrets to GitHub.
