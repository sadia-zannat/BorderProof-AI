# Deployment and reproducibility guide

**Verified reference runtime:** local Python 3.13, FastAPI, SQLite and Chromium via browser-API bridge. Windows guidance targets Python 3.12. No public deployment or bank integration was verified.

## Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r services\api\requirements.txt
$env:DEMO_SEED_PASSWORD='Choose-A-Unique-Strong-Password!'
.\scripts\run_preview.ps1
```

Visit `http://127.0.0.1:8000/demo`; API docs `/api/docs`. Keep demo bound to loopback. Demo data persists under `runtime/borderproof.sqlite3` and `runtime/uploads`. Never put actual personal student/financial documents in this demo. To reset, stop process, remove synthetic DB/uploads in a separate disposable local workspace, then rerun.

## Web frontend

Optional Next.js from `apps/web`: `npm install && npm run dev`. Separate FastAPI server must be running. On this machine npm registry failed with DNS `EAI_AGAIN`; no production build, semantic typecheck or WebGL behavior is verified. The global TypeScript parser check (if run) is **syntax only**. Check `NEXT_PUBLIC_API_BASE_URL` and CORS origins if using different development hosts.

## Docker

`docker compose up --build` after setting unique seed password, with the provided compose file. Docker build was NOT executed in V5 verification; do not use default credentials or Internet exposure. SQLite is not a substitute for a durable distributed payment infrastructure.

## Safety gates before actual product development

Require verified financial provider sandbox credentials with permission, independent regulatory analysis for each corridor, bank ownership evidence, authenticated quote sources, MFA, secure account lifecycle, tenant audit, transaction isolation, provider callback verification, secret management, dynamic malware scanning, independent testing and a real operational support process. V5 does **not** bypass any of these prerequisites.
