#!/usr/bin/env bash
set -euo pipefail
export APP_ENV=development ENABLE_LOCAL_SIGNUP=1
if [ -n "${DEMO_SEED_PASSWORD:-}" ]; then
  export ENABLE_DEMO_SEED=1
else
  export ENABLE_DEMO_SEED=0
fi
cd "$(dirname "$0")/.."
exec python -m uvicorn app.main:app --app-dir services/api --host 127.0.0.1 --port 8000
