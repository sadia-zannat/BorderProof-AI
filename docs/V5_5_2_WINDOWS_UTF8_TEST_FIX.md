# Windows UTF-8 Benchmark Test Compatibility Fix

Version: V5.5.2 Windows-Compatible Candidate
Date: 2026-10-20

## Issue

On Windows where the default Python text encoding is a locale encoding such as cp1252, a research test comparing `cases.jsonl` against the deterministic generator could fail on the `PROMPT_INJECTION-009` synthetic case. That case contains a deliberately confusable Cyrillic Unicode letter in the phrase `sеcurity`. The JSONL fixture is UTF-8, but `Path.read_text()` in the original test did not specify an encoding.

## Repair

Added `encoding='utf-8'` to four `read_text()` calls in `services/api/tests/test_research_v4.py`. No benchmark case, label, result, policy, financial-transaction logic, AI agent logic, or source fixture is altered by this repair. The archive's top-level folder now carries V5.5.2 rather than the incorrect V5.5.1 name.

## Validation

From the extracted project root:

```cmd
.venv\Scripts\activate.bat
python -m pytest -q services\api\tests
```

To confirm the specific regression:

```cmd
python -m pytest -q services\api\tests\test_research_v4.py -k frozen_dataset_matches_generator
```

This compatibility change does not establish successful live Qwen/Ollama inference. Run the live model validation separately; do not claim it passed unless its JSON results demonstrate that.
