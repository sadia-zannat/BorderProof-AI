# StuPay-IntegrityBench V4.1 — genuine synthetic files, NOT independently validated financial research

This repository includes **300 generated, deterministic and original SYNTHETIC student-payment scenarios**, 300 fixture-authored label records, 8 executable policy proxies, 60 held-out cases (stratified 20% per category), actual generated holdout JSON/CSV results, and a replayable read-only UI.

The evaluation policies are **not real LLM agents**, not an implementation of Google AP2, not bank compliance, and do not make real financial transactions. A benchmark constructed by the same project authors as the defenses is subject to severe confirmation bias; it is a software verification artifact and a preliminary controlled experiment, not independent scientific proof.

## Quick reproduction

From the **repository root**, after installing `services/api/requirements.txt`:

```bash
python -m benchmarks.stupay_integritybench.corpus
python -m benchmarks.stupay_integritybench.evaluator --split holdout --out benchmarks/results
python -m benchmarks.stupay_integritybench.evaluator --split development --out benchmarks/results
python -m pytest -q services/api/tests/test_research_v4.py
```

The script writes `benchmarks/stupay_integritybench/v1/{cases.jsonl,labels.jsonl,metadata.json}`. Both JSONL streams contain one record per case and are SHA-256 identified by `metadata.json`. Split is based on `index % 5 == 0`, with attack subtypes cycled separately from split to prevent trivial split-vs-attack confounding. Holdout labels are authored by the generator, not evaluated by external experts. Benchmark predictions do not receive labels as inputs.

## Scenario categories

| Case family | Cases | Holdout | Ground truth rule |
|---|---:|---:|---|
| Legitimate synthetic tuition requests | 60 | 12 | expected safe with fictitious registry and approval |
| Incomplete invoice / missing provenance | 40 | 8 | must not complete until corrected |
| Beneficiary/account mismatch | 50 | 10 | must not complete |
| Malicious instructions inside untrusted content | 50 | 10 | must not complete; several obfuscated attacks bypass V3 regex |
| Changed invoice/quote/approval scope | 40 | 8 | reapproval / new evidence mandatory |
| Provider declined/timeout/forged result/duplicate | 40 | 8 | no completed transfer claim |
| Unsupported demo corridor | 20 | 4 | must not complete |
| **Total** | **300** | **60** | **48 unsafe and 12 legitimate in holdout** |

## Baselines (all isolated, hand-coded)

1. `heuristic_assistant_proxy` — checks invoice completeness, case amount/currency and corridor. **Not an LLM.**
2. `tool_agent_proxy` — previous checks plus a fixture beneficiary comparison. **Not a tool-enabled LLM.**
3. `static_approval_proxy` — prior checks plus consent and quote freshness. **Not a real agent.**
4. `ap2_inspired_proxy` — additionally checks quote/approval scope. **Not AP2-compatible and not cryptographically signed.**
5. `bpce_core_proxy` — compound deterministic checks, reuses V3 production `assess_injection` and `policy_for_case` routines, with explicit simulated consent/provenance/provider/retry checks. **Not the complete V3 SQL transaction execution endpoint.**
6–8. BPCE with provenance, approval-scope, or injection scan disabled in isolated evaluator only. The deployed application NEVER disables these guards.

`p50_policy_microseconds` and `p95_policy_microseconds` are Python computation timing only, not full API, provider, LLM or bank latency. The same input cases and evaluation conditions are used for all policies. CPU scheduling influences elapsed microseconds. Token cost is absent (`null`), not zero measured dollars.

## Key actual holdout results

| Proxy | Unsafe accepted / 48 | Unsafe acceptance | Legitimate completion | False rejection | Injection attack acceptance |
|---|---:|---:|---:|---:|---:|
| Heuristic assistant (not LLM) | 38 | 79.2% | 100% | 0% | 100% |
| Tool agent proxy | 28 | 58.3% | 100% | 0% | 100% |
| Static approval proxy | 28 | 58.3% | 100% | 0% | 100% |
| AP2-inspired (not AP2) | 20 | 41.7% | 100% | 0% | 100% |
| BPCE core proxy | 5 | 10.4% | 75% | 25% | 50% |
| BPCE without provenance | 7 | 14.6% | 75% | 25% | 50% |
| BPCE without approval scope | 7 | 14.6% | 75% | 25% | 50% |
| BPCE without injection scan | 10 | 20.8% | 100% | 0% | 100% |

These results show a **tradeoff** on the deliberately constructed synthetic cases: BPCE blocks more seeded faults but overblocks some benign quoted instructions and misses half of crafted injection variants in holdout. No statistical confidence interval/generalization claim is justified; exact sample counts are disclosed. Original dataset is not a recognized financial benchmark.

## Reproducibility notes

- Fixtures/labels are frozen and their hashes are checked by tests.
- Prediction policies see fixture features, not label strings or failure-family identifiers.
- Split selection and generated attack subtype are disentangled.
- The dashboard reads a bundled holdout results file generated by CLI; it does not generate fake numbers or silently execute payments.
- A standalone `POST` endpoint for intentionally weakening payment controls does not exist.
- No real identities, bank accounts, live provider keys or real currency quotes are included.

## Next scientifically credible experiment

Obtain independent human labels on unfamiliar anonymized or consented invoices (with no sensitive production info committed), realistic provider/registry evidence, real LLM agent and tool-agent baselines, blind holdout cases authored by a separate team, multilingual and non-regex injection attacks, error taxonomy, Wilson intervals, and real end-to-end latency/cost. Report failing legitimate requests; do not optimize solely for blocking all payments.
