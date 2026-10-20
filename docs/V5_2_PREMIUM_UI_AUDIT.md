# BorderProof AI V5.2 — Minimal FinTech UI audit and release report

**Scope:** full UI copy, hierarchy and responsiveness refresh, applied to BOTH frontend implementations: `apps/preview/index.html` (the user's actual `/demo`) and `apps/web` (the optional Next.js source). Existing V1→V5.1 functionality remains in the package. This is a **presentation/UX release**, not a claim of new bank capabilities or a proven Next.js production build.

## Principle

Primary screens are for **decisions and actions**, not long internal implementation descriptions. Concise UI labels explain what an action does; technical traces and raw machine output remain accessible via progressively disclosed controls. Financial-risk warnings and the synthetic-only nature of the app are never hidden behind disclosure controls.

## Page-by-page audit

| Surface | Previously identified friction | Change in V5.2 | Essential information retained |
| --- | --- | --- | --- |
| Public shell & landing | Entire logged-in workspace sidebar visible publicly; dated version labels and exposition | Separate lightweight marketing header, distinct sign-in action, shorter headline/subtitle and three simple process steps, calmer hero spacing | SIMULATED · NO REAL PAYMENTS label |
| Sign in | Dense development explanation and confusing workspace framing | Centered sign-in card with email/password/CTA, no workspace sidebar before authentication | Local-demo safety label, actual authentication required |
| Dashboard | Large explanatory paragraphs and technical vocabulary | Compact overview heading, financial KPI cards, charts and direct action affordances | Demo/synthetic provenance and state |
| Payment cases | Internal workflow descriptions above tasks | Scan-friendly case table/details, actionable controls | Accurate case state/ownership |
| Document vault | Excess detail on extraction internals | Short instructions and succinct document metadata | Document trust and provenance limitations |
| Evidence center | Implementation description ahead of evidence | Evidence/status-first layout, concise metadata | Unverified beneficiary status and source distinctions |
| Payment corridors | Lengthy prose on price/reference distinctions | Short labels plus scannable corridor controls | Reference FX rates are not executable quotes |
| Payment lab | Dense implementation explanations and full raw JSON receipt | Five-step financial workflow, amount/quote/consent/results remain prominent; technical receipt JSON and fingerprints moved to expandable details | Payment simulated only, consent, approval/expiry, decline/timeout, ledger result |
| AI Agent | Agent implementation description and debug logs overshadowed conversation | Clear chat and case selection/composer, minimal empty state, tool trace in expandable disclosure | Read-only agent tools; unverified/synthetic source caveat |
| BPCE security kernel | Dense research/security explanation | Risk checks and graph before optional details; clear status labels | Invalidation/block decision and evidence consistency |
| Research & IntegrityBench | Technical setup copy on main canvas | Concise metric, baseline chart and scenario replay cards | Project-authored synthetic benchmark caveats, observed failures |
| Evidence & Support | Large machine-readable details | Summary-first, detailed export on demand | No real bank refund/dispute, read-only status |
| Reviewer/Auditor/Admin | Operational documentation confused with interface | Short action labels, status-oriented layout and readable tables | Restricted access, audit caveats and outcomes |
| Settings and navigation | Internal version-name and debug-level text | Simpler headings and nav labels, consistent typography/spacing | Functional language selection, sign-out |

## Design choices

- Deep navy surfaces and precise teal primary actions; reduced glare, balanced cards, fewer simultaneous accent colors.
- Public landing/login have their own compact header; authenticated areas receive workspace navigation.
- A deliberate content hierarchy: task title → relevant amounts/status → action → optional technical explanation.
- Preserve semantic controls, `prefers-reduced-motion`, mobile breakpoints, localization and meaningful action feedback.
- No deceptive live-banking copy, fabricated activity, simulated payment represented as real or unexplained financial status.
- English, Simplified Chinese and Bangla message catalogs retain exact key parity; extra copy translated.

## Actual verification evidence

The following were run on **this V5.2 source**:
- Backend/API/security regression: 96 tests passed across V1→V5.1 coverage; 1 optional Hypothesis test skipped because its dependency was not installed.
- Chromium UI smoke/regressions: 6 tests passed, including public landing/login, authenticated dashboard and AI chat, plus legacy payment, BPCE, research and support flows, driven through actual FastAPI requests using a browser bridge because sandbox direct localhost navigation is restricted.
- Preview inline JS `node --check`: passed.
- Next.js source TypeScript/TSX syntax parsing: 15 source files parsed, zero parse errors (this is not a full semantic type check or production build).
- Localization key parity: 135 keys each for English, Simplified Chinese and Bangla.
- Screenshots in `docs/V5_2_MINIMAL_*` are **real browser-generated UI renderings**, not AI-generated mockups.

### Not verified / out of scope

- No full Next.js production compile or Docker deployment was performed (npm registry not available in test environment).
- No live `qwen3:4b` inference run in the build environment. Local Ollama integration is retained as designed in V5.1; user previously confirmed model works locally at CLI.
- No external bank/provider connectivity, real money, KYC/AML clearance, independent financial evidence registry or independently peer-reviewed benchmark.
- Visual preference is subjective; tested mobile widths include 390 px, not every real device/browser combination.

## User experience testing shortcut

Visit `http://127.0.0.1:8000/demo` after extracting and launching. You should first see the marketing landing **without the private sidebar**. Sign in to see the workspace. Open AI Agent (case selector/chat composer) and Payment Lab (step-by-step). Raw receipt JSON is available on demand, rather than occupying the financial summary. Run all flows in demo mode only.
