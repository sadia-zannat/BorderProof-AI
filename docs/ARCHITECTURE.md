# BorderProof AI V1 technical architecture

## Runtime components

```text
            Next.js 16 / React / TypeScript (source only; npm unavailable)
                        │ credentials: include, CSRF header
                        ▼
            FastAPI /api/v1/* ────── httpOnly session cookie
            │      │       │
        Student   Reviewer  Auditor / Admin   [Role/owner guards]
            │      │       │
            └──────┼───────┘
                   ▼
          SQLAlchemy 2 + SQLite (local) / configurable DB URL
            Users | Sessions | Cases | Document metadata | Audit events
                   │
       private runtime/uploads/ (5 MB max; not publicly served)

    In parallel: /demo standalone no-npm browser frontend
      SAME FastAPI, SAME authorization, SAME SQLite persistence

  Payment executor: NOT PRESENT in V1 (intentional fail closed)
```

## API design

- FastAPI OpenAPI: `/api/docs` and `/api/openapi.json`.
- Public metadata/health routes are separate from logged-in data routes.
- Cookie-based auth sessions stored as SHA-256 hashes of random bearer secrets. CSRF tokens are hashed and compared server-side; `/auth/me` rotates the CSRF token.
- Mutable endpoints require CSRF plus strict student role/owner checks; reviewer/auditor/admin endpoints are read-only.
- Strong Argon2 password hashing; user accounts only development-seeded with an explicit environment-supplied password.
- Monetary amounts validated by `decimal.Decimal`, capped at 1,000,000 and two decimal places, stored as precision-preserving strings for V1. **Not** a ledger or financial arithmetic engine yet.
- Uploaded PDF/PNG/JPEG/TXT files stored only after type/size/signature validation; database stores owner, case scope and checksum. V1 **does not parse or trust file contents**.
- Local audit events contain SHA-256 references to preceding event; this supports casual tamper detection only. V3 must add concurrency ordering, authenticated signatures and independent anchoring where viable.
- Database baseline uses SQLAlchemy declarative initialization and a recorded `schema_versions=1`. Structural upgrades are NOT automated in V1; add tested revisions before changing deployed schemas.

## User interface

- Primary intended product: `apps/web` Next.js 16 App Router and shared client workspace, typed fetch client, English/Chinese/Bangla localization, CSS depth components, lazy-loaded React Three Fiber globe, chart based on actual DB case counts, accessible static fallback and reduced motion.
- `apps/preview` is **not** a fake dashboard: a dependency-free HTML/CSS/JS UI hitting the same API, useful for offline testing when npm installation is blocked. It does not have every Next.js visual refinement.
- The project uses a custom CSS design system and Tailwind 4 import. **No shadcn/ui components have been installed/configured** in V1, despite being in the long-term style request.
- Mobile styles exist; no comprehensive WCAG audit has been performed.

## V1 data sources

Everything in the seeded case is **SYNTHETIC**, not a real university beneficiary, fiat provider rate, executed quote or proof of payment. Any user-entered case data is likewise *unverified*. No external API requests, sanctions lists, or live bank connectors are made in V1.

## Extension seams

V2: parse/upload evidence, provenance registry, structured agent tools, exchange-rate reference vs executable quote classification, persistence-based sandbox ledger.
V3: independent BPCE policy kernel, hash/version-bound consent, state machine, idempotency/race control, policy and agent prompt-security boundaries.
V4: benchmark, attacks, ablation, interactive provenance graph and measured results.
V5: documentation, defense deck, accessibility and production hardening, deployment evidence.
