# V1 API Contract

FastAPI publishes the actual runtime schema at `http://localhost:8000/api/openapi.json` and UI at `/api/docs`.

`GET /api/v1/health`, `GET /api/v1/public/config` are public.

`POST /api/v1/auth/login` sets an HttpOnly session cookie and returns a CSRF token. `GET /api/v1/auth/me` ROTATES the session's CSRF token; the client must save the latest token. `POST /api/v1/auth/logout` requires it.

Student: `GET/PATCH /api/v1/me/profile`, `GET /api/v1/dashboard`, `GET/POST /api/v1/cases`, `GET /api/v1/cases/{id}`, `GET/POST /api/v1/documents`, `GET /api/v1/documents/{id}/download`. Mutations require `X-CSRF-Token`.

Reviewer: `GET /api/v1/reviewer/queue` (read-only).
Auditor: `GET /api/v1/audit` (read-only).
Admin: `GET /api/v1/admin/summary` (read-only).

V1 has NO `/payments/execute` API by design; a request to it returns 404. No LLM inference endpoint exists.

## V2

FastAPI auto-generates current OpenAPI at `/api/openapi.json` and `/api/docs` from `finance_routes.py`; see `docs/API_V2.md` for summary. All finance create/mutate endpoints require a session cookie, student role, and `X-CSRF-Token`. Data carrying simulated reference IDs must not be confused with actual bank identifiers. Machine-generated OpenAPI schemas are authoritative for current route signatures; a manually copied spec is not maintained.
