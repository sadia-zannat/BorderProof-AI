# V4 read-only research APIs

All endpoints require a valid logged-in local session. They do not accept write operations, provider tokens or bank credentials.

- `GET /api/v1/research/summary`: frozen actual holdout results and corpus metadata (synthetic only).
- `GET /api/v1/research/cases?category=&split=holdout&offset=0&limit=20`: synthetic fixture metadata only; valid `split` is holdout/development/all; categories from `benchmarks/README.md`.
- `GET /api/v1/research/replay/{case_id}?policy=bpce_core_proxy`: independently recomputes one specified deterministic proxy's checks and returns synthetic fixture evidence nodes with the authored ground-truth label. Never initiates a transfer.

Errors: HTTP 401 unauthenticated; 404 unknown case; 422 unknown policy/filter/page size; 503 frozen results missing. Underlying API version `/api/v1` remains backward compatible; health response app version is `4.0.0`.

Example from browser (with same-site cookies):
`fetch('/api/v1/research/summary', { credentials: 'same-origin' })`.

For Next.js: base URL configurable as `NEXT_PUBLIC_API_BASE_URL`; production cross-site session/SameSite/CORS deployment needs independent security validation.
