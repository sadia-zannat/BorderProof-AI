# BorderProof AI V5.5.2 - Evidence-first local Qwen repair candidate

Date: 2026-10-20. Original V5.5.1 ZIP must be preserved as a separate backup.

## Failure background

The user-observed V5.5.1 Windows retest had 9 local agent HTTP requests, 4 HTTP 200 and 5 HTTP 502. The Ollama model was accessible for some requests, so connection failure is not established as the root cause. The exact exception for each failed request is recorded in the user's `runtime/local_validation/sanitized_ollama_results.json` (not provided in this archive). V5.5.1 asked the model to choose read-only tools, retried absent calls and rejected incomplete reasoning. Long Qwen planning could consume the generation limit. Those conditions are *plausible* reasons for the 502 responses; the logs alone do not prove which condition occurred in each case.

## Changes

1. Explicit tool-inspection questions are matched by a deterministic server-side router to tenant-scoped read-only inspection methods. The returned trace is marked `selected_by=SERVER_DETERMINISTIC_ROUTER_NOT_MODEL`. The model is not claimed to have autonomously selected those tools. In particular, the L08 evidence-review question retrieves case, invoice and investigation evidence.
2. For the routed cases, Qwen receives the observations as untrusted data and only generates a short cited explanation. The Ollama API still performs real local inference; no mock or fake model response is substituted into production.
3. Reject tool-call proposals after evidence-first inspection, incomplete reasoning and obvious planning-only responses. Retry one concise answer when possible. Any repeated model failure remains HTTP 502, rather than a fabricated success.
4. The no-permission-to-pay boundary, authenticated case ownership, deterministic BPCE financial checks and synthetic disclaimers remain in place. No new financial execution capability is added.
5. Live validator reports its routing method and explicitly refuses to treat server-directed evidence lookups as an autonomous model tool-selection score.

## Local testing recorded here

- Source has been syntax-checked and new agent mock-transport regressions have been executed.
- Backend unit and contract suite (without optional Hypothesis): 146 passed in two disjoint runs (82 + 64).
- Optional Hypothesis module: not executed; Hypothesis not installed in this container.
- Real Windows Ollama/Qwen run: NOT executed here. The user's Windows retest is still REQUIRED.
- No new Next.js code modifications; full frontend build not rerun in this patch.

## Windows quick verification

Close the previous API (`Ctrl+C`); do not delete the original V5.5.1 directory. Extract V5.5.2 separately, then open it in VS Code.

Terminal 1 (CMD) in the extracted project root:

```cmd
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r services\api\requirements-lock.txt
python -m pytest -q services\api\tests
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run_preview.ps1
```

Terminal 2 (CMD) in the same project root:

```cmd
.venv\Scripts\activate.bat
ollama list
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run_live_ollama_validation.ps1
```

Review `runtime\local_validation\sanitized_ollama_results.json`. Share the file after checking it contains only synthetic data. Before including scores in submissions, separately review answers for unsupported fee currency, bank verification claims, false citations and misleading payment approvals. A successful internal check is not a certification of legal or banking compliance.

## If failures remain

The JSON's `results[*].error` distinguishes model failure from readiness. For each failed L01-L09 provide id, HTTP status and sanitized `error` string. Do not share API keys, cookie headers, or personally identifiable documents. Do not enable Gemini or other external model services just to mask an Ollama failure.
