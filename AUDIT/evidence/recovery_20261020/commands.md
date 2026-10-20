# Resumed clean acceptance commands (2026-10-20 UTC)

A new extraction of FinVeritas_BorderProof_AI_V5_3_Recovery_Checkpoint_20261020.zip was used, never the original V5.2 tree. A new Python venv and fresh node_modules were installed. Logs retain actual versions, exit codes and runtime-specific absolute paths. The native harness was copied after its verification-only enhancement and rerun in that clean tree; 113 shipped application/data/test/build-script files were compared byte for byte.

```bash
python3 -m venv <fresh-venv>
<fresh-venv>/bin/python -m pip install -r services/api/requirements-lock.txt -r services/api/requirements-dev.txt
<fresh-venv>/bin/python -m pytest services/api/tests -q --junitxml=<out>/backend.xml
cd apps/web
npm ci --ignore-scripts
npm run typecheck
npm run lint
npm run build
npm audit --omit=dev --json
cd ../..
node scripts/check_all_locales.cjs
<fresh-venv>/bin/python benchmarks/work_v53_evaluation.py
<fresh-venv>/bin/python scripts/validate_postgres_schema.py
<fresh-venv>/bin/python scripts/validate_local_agent.py --output <out>/live_model_preflight.json
BORDERPROOF_CHROMIUM=<headless-shell> <fresh-venv>/bin/python -m pytest tests/e2e -q --junitxml=<out>/legacy-browser-headless.xml
BORDERPROOF_CHROMIUM=<headless-shell> <fresh-venv>/bin/python scripts/run_real_execution.py --browser --output <out>/native_verified_execution --seed 2026102005
<fresh-venv>/bin/python scripts/run_real_execution.py --enable-ocr --output <out>/ocr_execution --seed 2026102002
```

The model preflight returns 2 / BLOCKED and zero inference results. That is not a passed model benchmark. Default Playwright CDN download failed; its full log is retained. Official Chrome for Testing 156.0.8078.4 and headless-shell archives were downloaded from Google's public storage; source URLs, exact bytes and hashes are in the runtime JSON files. Full Chrome was unable to create its process-singleton Unix socket in this environment. The supported headless-shell executable passed the browser runs, without application fetch interception in the native harness. Six inherited tests use their explicitly disclosed Python HTTP bridge. Windows normally uses Playwright's installed Chromium without BORDERPROOF_CHROMIUM.

Final pytest suites: 130 + 6 passed, zero failures/errors/skips. Historical failed runs remain under attempt_history; they are not reclassified as passes.
