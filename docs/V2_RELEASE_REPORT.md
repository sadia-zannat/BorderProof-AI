# BorderProof AI V2 — release checklist and limitations

**Release:** V2 Financial Agent & End-to-End Internal Sandbox. **Team:** FinVeritas. **Track:** International AI — Topic C. **Product:** BorderProof AI.

## Deliverables in full ZIP

- V1 preserved: app, original frontend/dashboard, private document vault, auth/profile, role-aware panels, localization, original tests and V1 screenshots.
- V2 added: database schema 2, financial extraction/agent, investigation, stored quotes, approvals, simulated ledger and transfers, receipts, notifications, local reconciliation, optional explanatory model adapter, new Next.js financial lab and complete no-npm standalone UI.
- Source fixtures labelled SYNTHETIC, evidence provenance, secure transaction safeguards, test suite, browser screenshots and documentation.
- V2 Dockerfile updated to copy the fixture registry/data needed by the API. **Not run** in this environment.

## Observed verification

- **38/38 pytest tests passed** across original V1 and new V2 API/security/financial-safety suites.
- **V1 → V2 SQLite migration independently passed**, preserving legacy user/case in an actual legacy DB.
- **Two Chromium browser test scripts passed:** original V1 interaction regression and new entire internal payment life cycle.
- **117 keys/language** present for EN, zh-CN and bn-BD. Newly added financial lab uses separate translated UI copy. Some technical diagnostics remain English.
- **11 frontend TS/TSX files passed syntax parsing, not production build/typecheck.** Preview JS syntax and Python compile passed.
- Actual screenshots saved to `docs/V2_FINANCE_BROWSER_SCREENSHOT.png`, `docs/V2_FINANCE_MOBILE_SCREENSHOT.png`, and `docs/V2_FINANCE_BANGLA_SCREENSHOT.png`.

## Explicit limitations

1. Real financial transactions: **DISABLED**. No bank/provider integration, no real FX provider quote. A simulated completed transfer only changes synthetic local ledger.
2. Institution/beneficiary verification: **only match to original local synthetic records**. Valid matches are NOT evidence of real account ownership.
3. Source extraction: anchored label parser, text PDFs and text; arbitrary invoices, scanned PDFs and image OCR not verified.
4. LLM model path: optional and only for non-authoritative explanations, cannot create payments. External credentials/network not available for test.
5. Independent BPCE kernel, policy engine, advanced audit, reviewer escalation, property tests, benchmark evaluation: **V3/V4 work**, not implemented V2.
6. Next.js build, TypeScript semantic validation with dependencies, Docker runtime: **unverified** due environment limitations.
7. Not suitable for production customers, real bank accounts, passports, or personal financial information.

## Competition timing

Uploaded International rules specify **October 20, 2026, 23:59 Beijing = October 20, 2026, 21:59 Bangladesh** as deadline for both registration AND project submission. Prior general promotional material may cite November 1; follow verified rule/organizer confirmation. No submission or registration is performed by this ZIP.

## Next version

V3: true BPCE consistency/dependency kernel, cryptographic authorization binding, origin/tenant/race hardening, prompt injection/tool response integrity, policy source evidence and adversarial security tests. **Do not** silently classify V3 scope as implemented in V2.
