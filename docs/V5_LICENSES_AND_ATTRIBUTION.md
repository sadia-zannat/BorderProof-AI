# External reference, component licensing and attribution (V5)

The project code and synthetic fixtures were created for FinVeritas's exercise; no license to distribute real bank/provider data or logos is implied. Source release/publication license must be chosen and confirmed by project owners before public GitHub publication. No claim of automatic provider licensing.

| External component | Project use | Required release action |
|---|---|---|
| Python FastAPI, SQLAlchemy, Pydantic, Uvicorn, argon2-cffi | Runtime dependencies | Record installed versions + verify applicable package licenses/NOTICE files before public distribution |
| Next.js, React, Three, R3F, Drei, Recharts, lucide-react, Tailwind | Next.js source declarations only in this build | `npm install` then generate lockfile/SBOM; review exact dependency license notices |
| Playwright, Chromium, pytest, optional Hypothesis | Testing tools | Disclose tool versions and redistribution requirements |
| Google AP2, Visa TAP | Prior art comparison, **no copied API/protocol implementation** | Cite official specifications; do not imply affiliation/interoperability |
| World Bank, ECB, Frankfurter, Flywire, Wise, Airwallex | References in master prompt only, optional read-only FX if service available | Respect API terms; no redistributed restricted financial data |
| Benchmark fixtures | Generated local synthetic corpus authored within project | Release with source labeling/limitations and obtain team IP/licensing decision |
| Original BorderProof logo | Own source vectors | No third-party corporate branding or endorsement |

No formal software composition analysis, automated vulnerability scan, SPDX SBOM or lawyer-reviewed license analysis was executed. That is an outstanding requirement before public commercial redistribution. Use `pip freeze` and `npm ls --all` after reproducible installations and inspect package licenses.
