# BorderProof AI V5.5.1 — Local Agent Hardening Candidate

**Status:** backend regression verified; **live Qwen revalidation required on Windows.**

This cumulative archive extends V5.5 and preserves all UI, 8-currency 56-route planning network, financial safety controls, browser assets, test/research artifacts and source history. No 56-route payment execution is claimed.

## Changes targeting the user's Qwen3:4b validation report (2026-10-20)

- Model prompt now tells Qwen to select relevant read-only tools and distinguish unverified versus prohibited payments.
- Requests `/no_think` as well as the existing Ollama `think:false`; increases generation budget from 500 to 900 tokens. Model-specific behavior must be checked locally; **this is not proof the thinking issue is fixed**.
- For explicit inspection requests, if Qwen returns without the required read-only observation, retry once. If still absent, fail closed with HTTP 422 instead of presenting unevidenced conclusions. Retry does **not** execute tools on the model's behalf or falsify a trace.
- Completed `<think>` spans are removed from final display; unfinished tagged reasoning and generation-limit output are withheld with explicit errors.
- Source-currency denominated synthetic quote fees now carry `fee_currency` in agent tool results, eliminating an observed ambiguity.
- Four new regression tests of retries, refusal, reasoning guard and fee currency, with preservation of other agent tests.

**Observed original live run:** 9/9 HTTP 200; 5/7 expected tool calls; failures L01 and L06; no financial side effects. This was based on a fresh Bangladesh→UK harness case, not the separate USA→China UI case.

**Verified here:** 143 backend tests passed, 1 optional skipped (mocked/model transport contracts + deterministic functions). No real Ollama runtime in this build environment; quality and tool selection must be remeasured on the user's laptop. Next.js code is unchanged and was built on the user's previous V5.5 Windows machine, not independently rebuilt for this candidate.

## Windows: retest (different extracted folder)

1. Stop previous backend in its VS Code terminal with Ctrl+C. Preserve V5.5 ZIP and project directory.
2. Extract this candidate to a **new folder**; open that root in VS Code.
3. Create and activate Python 3.12 venv, then install dependencies:

```cmd
py -3.12 -m venv .venv
.venv\Scriptsctivate.bat
python -m pip install -r servicespiequirements-lock.txt
python -m pytest -q servicespi	ests
```
4. Start backend in that terminal:

```cmd
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scriptsun_preview.ps1
```

5. Open second project-root terminal and execute:

```cmd
ollama list
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scriptsun_live_ollama_validation.ps1
```

6. Check `runtime\local_validation\sanitized_ollama_results.json`, remove any sensitive content and share only it. **Do not claim PASS until L01–L09 are human-reviewed.** Any 422/502 errors need debugging, not status inflation.

No bank integration, provider credentials, KYC, real financial transactions or production launch are enabled.
