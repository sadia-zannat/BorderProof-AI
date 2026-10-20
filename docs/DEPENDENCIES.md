# Dependency and license considerations (V2)

**No external repository was cloned.** The application source and synthetic fixtures were authored for this project. Licensing of transitive dependencies must be re-reviewed before any public commercial deployment.

- FastAPI/Starlette, Pydantic, Uvicorn, SQLAlchemy, Argon2-cffi, HTTPX, pytest, python-multipart: standard Python open-source packages; check current authoritative license text and versions prior to release.
- `pypdf`: permissive BSD-3-Clause open-source PDF text extraction (not a model/OCR). The AGPL/commercial PyMuPDF dependency was deliberately **removed** from V2 runtime dependencies to reduce licensing and installation risk.
- Pillow and pytesseract: optional optical character recognition support when external Tesseract is installed; disabled by default.
- React, Next.js, TypeScript, lucide-react, Recharts, react-three-fiber, Drei, Three.js and Tailwind: included as declared dependencies, **not installed/build-verified** here.
- Synthetic fixtures contain no copied bank data, third-party invoice or payment-provider secrets.
- Optional public reference API: Frankfurter; no redistribution of its private data and no executable payment quote.

All third-party packages must be checked against their licenses for the intended public distribution. No legal assurance is made.
