# BorderProof AI V4 release report — working tree evidence

Release name: `BorderProof_AI_V4_Research_Evaluation.zip`.

**Included:** full V1–V4 source, original synthetic corpus/labels and hashes, 8 executable policy proxies, results JSON/CSV, V4 authenticated read-only research endpoints, Next.js dashboard source and independently Chromium-tested standalone frontend, release/risk/novelty/data documentation.

**Observed tests:** 73 passed; 1 optional Hypothesis skipped. V4 Chromium browser workflow passed; V2 migration to V4 code path passed with previous V2 source restored for that integration test; 118 EN/zh-CN/bn-BD translation keys matched; 13 TS/TSX source files parsed without syntax errors. Exact commands in `docs/V4_VERIFICATION.md`.

**Numerical caveat:** BPCE policy proxy returned 5/48 unsafe acceptance and 9/12 legitimate completion on synthetic holdout cases. These are **not** external-agent accuracy or actual real-world financial safety. More on `benchmarks/README.md`.

**Security caveat:** Deployed internal simulator and V3 consistency kernel remain in place. V4 only introduces read-only GET research endpoints; benchmarks cannot trigger real/synthetic wallet activity. Real bank/KYC/AML and provider integrations remain unavailable.

**Build limitations:** Next.js npm install/production build and Docker unavailable/unverified here. V4 Next.js JSX syntax passed parser, but semantic typechecking/deployment not proved. No external expert validation. Prior art establishes that authorization binding and signed payment mandates are not original inventions of BorderProof AI.

**Next version (requires new explicit `next`):** V5 submission artifacts, production/frontend verification, independent security benchmark and external integration review if legitimate provider credentials exist. The project is NOT yet submitted to the organizers.

**Archive-level SHA, byte size, entry count and clean-extraction results:** reported alongside the delivered ZIP link. The ZIP checksum cannot be embedded inside itself without changing the checksum.
