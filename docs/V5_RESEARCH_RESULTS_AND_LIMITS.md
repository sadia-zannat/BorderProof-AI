# Reproducible research results — V5 carry-forward

## Research question

Can a project-authored, evidence-dependency rule proxy detect consistency faults more reliably than several weaker rule proxies on a fully synthetic tuition-payment task distribution? This is a **proxy engineering experiment**, not independent bank risk evidence.

## Benchmark/data lineage

`StuPay-IntegrityBench V4.1`: exactly **300 synthetic** cases, 240 development and 60 stratified holdout. Family totals: 60 legitimate, 40 missing/incomplete, 50 beneficiary conflict, 50 injection/tool poisoning, 40 authorization drift, 40 provider/recovery error, 20 corridor conflict. Ground truth and feature generation code are under this project's control. No real passport, institution payment record, bank transaction or human annotation was used.

## Actual held-out measurements

| Policy proxy (all deterministic and hand-coded) | Unsafe accepted / 48 | Legitimate completed / 12 | Caution |
|---|---:|---:|---|
| Basic heuristic assistant proxy | 38 | 12 | NOT a real LLM |
| Tool-agent proxy | 28 | 12 | NOT a real tool-using LLM |
| Static approval proxy | 28 | 12 | Simplified rules only |
| AP2-inspired proxy | 20 | 12 | NOT AP2 protocol implementation |
| BPCE core proxy | **5** | **9** | 25% false rejection; 50% injection evasion in held-out injection family |

Results are loaded from `benchmarks/results/holdout_results.json`, recomputable with:

```bash
python -m benchmarks.stupay_integritybench.corpus
python -m benchmarks.stupay_integritybench.evaluator --split holdout --out benchmarks/results
```

Metrics are proxy decision metrics on authored cases. P50/P95 timings in results are **isolated CPU microseconds**, not end-to-end payment or LLM response latency. There are no measured LLM API costs, real customer losses, audited independent labels, confidence intervals for a real population, or external dataset.

## Key falsification findings

- **5/48** unsafe-labeled holdout cases escaped the BPCE proxy; it is not fail-proof.
- **3/12** legitimate cases were falsely rejected; safety has a real availability/usability tradeoff even on synthetic data.
- Half of held-out injected instructions evade simple regex-style proxy screening.
- Proxy logic and cases authored by the same engineering effort create evaluation-design bias.

## Prior art and novelty caution

BPCE does not invent transaction binding, cryptographic hashes, provenance or payment mandates. It is a student-specific composition. Compare related work in `docs/V4_RESEARCH_NOVELTY_AND_PRIOR_ART.md` and citations therein. **Next scientifically necessary steps:** independent blinded evaluation labels, real comparable LLM agent baselines under the same tools/tasks, external financial-domain review, corridor legality and public/private data provenance checks, calibrated false rejection, independent adversarial prompts and stress tests. Do not market current numbers as superior real-world fraud protection.
