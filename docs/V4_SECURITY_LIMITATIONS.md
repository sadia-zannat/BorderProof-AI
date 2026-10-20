# V4 security and benchmark limitations

**No changes to V3 payment permissions:** V4 adds only authenticated **GET** `/api/v1/research/*` endpoints. Benchmark policies do not write to production database or call payment execution. Ablations cannot be enabled through the app. A command-line runner works on separate immutable synthetic corpus files.

Potential risks and limitations:
- No external KYC, AML, beneficiary-bank ownership, real sanctions data, production policy attestation or payment service authorization.
- Regex-based malicious instruction detector misses 50% of authored holdout injection variants; some quoted benign instructions are rejected. **Do not rely on lexical screening as the trust boundary.**
- Dataset generation and the preferred policy are both designed by project authors; labels are authored alongside scenarios, not adjudicated; risk of experimenter bias is high. Holdout is a structural split, not an independent external test set.
- Baseline proxies are not live GPT/LLM, official AP2 or model-grade finance agents; a claimed win over those systems would be false.
- `provenance_id` checks for a supplied **synthetic** provenance pointer, not verification of a bank-issued credential. An arbitrary nonempty pointer can pass the offline proxy; deployed BPCE uses fixture bytes hashed and validated, not these artificial objects.
- The V4 benchmark evaluator shares only selected V3 detection/corridor functions; it is **not an end-to-end SQL execution benchmark**. The existing 63 V3 backend tests remain the evidence for actual sandbox endpoint behaviors.
- Read-only research API exposes only synthetic public fixtures but still requires login. No live documents/payments are ingested.
- No SQL/PostgreSQL horizontal scaling or disaster recovery test. No independently verified Next.js production bundle, Docker production deployment or real multi-tenant bank environment. Desktop/mobile evidence is the standalone no-npm browser preview.
- Independent finance judgment, fair market FX rates, genuine provider quotes, regulatory compliance and institutional banking trust remain outside implemented scope.

Higher confidence requires external testing, security review, human-labeled cases and independent provider-side proofs.
