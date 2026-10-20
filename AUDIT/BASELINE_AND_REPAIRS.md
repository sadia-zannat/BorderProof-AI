# Baseline and implemented repairs

Authoritative input: V5.2, 6,995,840 bytes, 171 archive entries, SHA-256 `65a00cae4fd1e338c85731b6e54d33e54dfca24414f900202ba6dd72e02e612c`. Original uploaded archive untouched. No older project used as implementation base.

Baseline execution: 99 backend tests passed including three optional Hypothesis tests. Initial Python environment lacked pytest and FastAPI; the failed initial command and subsequent successful dependency install are both retained. Next typecheck/build failed on `cases_heading`; lint had no configuration. Logs: `evidence/baseline/`.

| Priority | Actual finding | Implemented repair | Regression evidence |
|---|---|---|---|
| P0 | Reconciliation could race and used a mutable quote amount | Writer lock, refresh after lock, immutable recorded transfer debit; unique posting and approval indexes | Concurrent four-request reconciliation, six-request duplicate execution, exact balances and two postings |
| P0 | Conflicting duplicate invoice labels were silently ignored | Collect all matching labels, flag contradictions, reject malformed grouping/date and clarify | New duplicate amount/currency/account/institution tests and native conflicting invoice browser block |
| P0 | A new document could be followed by re-quoting old invoice evidence | Require latest document, verify every source hash and cross-document facts, renew approval | New document/stale quote/source-set tests |
| P0 | Same idempotency key could hide a changed requested outcome | Bind outcome as well as case and approval to existing key | TIMEOUT followed by changed SUCCESS returns 409 |
| P1 | Multiple audit events could fork within one transaction | Flush writes, serialize head append, preserve local chain validation | Two-event transaction, upload invalidation and concurrent transfer checks |
| P1 | GET /auth/me rotated CSRF and broke another open tab | Session-bound synchronizer token, unchanged by GET, rotated on new login | Forged token denied, cross-session reuse denied, same-session second tab works |
| P1 | Safe-plan inspected the oldest instead of latest document | Correct descending-order selection | New-document planner regression |
| P1 | Malformed model envelope could cause 500 | Typed envelope validation, 502/503, rejected tools, sanitized failure events, result hashes | Separate mocked agent contracts and native actual unavailable endpoint |
| P1 | Reloaded quote expiry lost UTC offset | Explicit UTC API serialization while keeping existing approval canonicalization | Fresh/persisted quote timestamps match |
| P1 | Next.js had no proven build and cross-host cookie defaults | Correct translation key, ESLint config, package lock, same-origin API proxy, native production server test | Clean npm ci/typecheck/lint/build and production routing |
| P1 | Standalone deep links and mobile select options failed | Real hash route handler, selected-document context, constrained form sizing | Native /demo registration and mobile three-locale checks |
| P2 | Chinese/Bangla could render missing glyphs | Locally served OFL subsets, preserved font licenses | Actual native screenshots, not generated UI images |

One pre-repair date test initially used 2026 while the original fixture's deadline was 2027. Its trigger was corrected to match a general ISO date; the original failed attempt remains in logs. The old CSRF test deliberately changes semantics: it now asserts forged-token rejection and logout, while a new test proves a previous session's token fails. This is an explicit session design change, not removal of a security assertion.

ESLint's React `set-state-in-effect` performance advisory is configured as a warning for retained mount-time initializers. Lint passes with warnings; it is not a zero-warning claim. Runtime/security assertions were not disabled. Historical V1/V2 migration scripts had stale schema expectations/sibling-folder dependence; they are now self-contained and preserve rows and balances.

Clean-room follow-up: a missing optional SOCKS dependency caused the public-reference request to raise 500 in a fresh venv. Added httpx[socks]/pinned socksio, converted missing transport configuration to honest 503 and added a negative regression. A new signup button also collided with inherited login selectors; it is now a minimal navigation link, preserving the original single sign-in action. The failed clean logs and successful repaired retest are both retained. Final clean suite: 130 passed; six inherited browser tests pass; native and OCR runs pass.
