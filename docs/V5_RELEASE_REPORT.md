# BorderProof AI — V5 final release report

**Team:** FinVeritas · **Track:** Shenzhen FinTechathon 2026 International AI, Topic C · **Release:** cumulative V1 → V5 on 19 October 2026.

## Included, actually implemented

1. Complete cumulative monorepo: `apps/web` Next.js TypeScript source, `apps/preview` genuine FastAPI-connected browser demo, `services/api` backend + SQLite demo persistence + schema migration, reproducible evaluation, tests and docs.
2. Core synthetic student-payment journey: session auth → synthetic invoice → parser/investigation → two simulated quotes → explicitly scoped consent → BPCE backend revalidation → stored simulator ledger and audit → internal receipt.
3. Safety boundary: scoped student/reviewer/auditor roles, CSRF controls, document hash/version rechecks, quote expiration, idempotency and explicit failure/unknown states. No LLM model can grant payment authorization.
4. V5 specific: deterministic read-only next-step planner, owner-scoped evidence JSON export with self-hash/limits, local refund/dispute guidance record (not a refund), no-store and other basic response headers, production guard against demo credential seeding.
5. English, Chinese and Bangla front-end preview + translation catalogs; 119 keys per language. Historical security, research and browser flows preserved.
6. `StuPay-IntegrityBench` 300 project-authored synthetic scenarios, 60 holdout, 5 hand-coded comparison proxies and 3 ablations; actual recorded outputs and limitations.
7. Competition materials: editable English 12-slide defense PPTX, presentation notes, 4–5-minute planned demo script, SRT captions, actual **28.48-second silent Chromium screen capture**, technical & security reports, 45-module status, data/model card, submission checklist, GitHub deployment instructions, source/license notes and independent Work handoff.

## What remains incomplete (do not market as verified)

**Highest priority blockers:** Next.js semantic typecheck/production build/hosting unverified (npm registry inaccessible); no real LLM agent or independent baselines; no real provider sandbox or verified bank beneficiary; no genuine compliance coverage, public launch or production security review; no independent benchmark labels. A complete narrated competition demo still needs manual video production, verification and publishing. Many of 45 planned modules remain partial. See `docs/V5_RELEASE_STATUS_MATRIX.md`.

## Actual verification

- Python backend/security suite: **84 passed, 1 skipped** (optional Hypothesis).
- Five Chromium preview journeys: V1, V2, V3, V4 and V5 **individually passed** with live local FastAPI bridge.
- V1-shaped and V2-shaped old DB upgrade to V5 verified, stored records retained.
- 119 locale keys in each of 3 languages; 14 TS/TSX syntax checks (not semantic build).
- Research holdout: **5 of 48 unsafe accepted**, **3 of 12 legitimate rejected** by the BPCE rule proxy, with 50% of synthetic held-out prompt injections evading its detector. These are limited simulation figures.
- Editable defense deck: 12 slides. Real silent capture: ~28.48s, not the finished submission video.
- See `docs/V5_VERIFICATION_REPORT.md` for test names and limitations.

## Execution and export

Use `README.md` for actual Windows startup. V5 services are internal-only and persist to a local SQLite file. Backend evidence export is self-hashed, **not signed or bank attested**. Public release must exclude personal files/secrets and default/demo credentials. GitHub publishing and official organizer submission were not performed.

## Version continuity and STOP

V5 incorporates functioning V1–V4 source; no patch-only release. No V6 was requested. This ZIP is the final deliverable for the five-stage build; any further repairs require a separate request.
