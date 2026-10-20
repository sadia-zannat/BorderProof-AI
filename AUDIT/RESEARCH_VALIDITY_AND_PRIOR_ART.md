# Research validity and prior art

The reproduced original corpus matches its generator: 300 project-authored synthetic cases, 240 development and 60 holdout. Original held-out BPCE **policy proxy** accepts 5/48 unsafe-labelled cases and blocks 3/12 legitimate-labelled cases. Its obfuscated injection miss rate remains 50% on those injection cases. This result is not improved by renaming the release.

`benchmarks/work_v53_evaluation.py` freezes 96 additional scenarios with 48 reserved train, 24 development and 24 holdout rows before scoring. No model trains on the train split. Raw cases/labels/results, file hashes, confusion counts and Wilson intervals are shipped in `evidence/research/`. The new holdout proxy accepts 3/21 unsafe cases and 3/3 safe cases. These very small authored counts are not evidence of field efficacy. No policy tuning followed the new challenge-set scoring.

The original row split shares templates, recipient patterns and injection variants. Case IDs expose failure families, so they must never be supplied to a future LLM baseline. Current policies do not read case IDs. Labels remain author-defined; Work review is not independent external human adjudication. P50/P95 in the original results measure Python policy-check microseconds, not model, API or payment latency. Cost, real-agent success, tool factual correctness and human evidence attribution are NOT MEASURED.

| Primary reference | Access reviewed | Relevance and distinction |
|---|---|---|
| [Jiang et al., A Formal Analysis of Agent Payment Protocols, Aug 2026](https://arxiv.org/abs/2609.00060) | Abstract/metadata | Prior formal work on lifecycle consistency. BPCE has no Tamarin proof and cannot claim this idea as new |
| [Mao et al., SoK, revised May 2026](https://arxiv.org/abs/2604.15367) | Abstract/metadata | Cross-layer agent-commerce threat framing, not a student invoice implementation |
| [AgentDojo, 2024](https://arxiv.org/abs/2406.13352) | Abstract/metadata | Tool-output injection evaluation. BorderProof has not reproduced its benchmark |
| [InjecAgent, ACL Findings 2024](https://aclanthology.org/2024.findings-acl.624/) | Anthology metadata/abstract | Indirect injection evaluation. No claim of outperforming it |
| [Google AP2](https://github.com/google-agentic-commerce/AP2) | Repository README | Established authorization protocol ideas. The AP2-inspired proxy is not AP2 implementation |
| [Visa Trusted Agent Protocol](https://github.com/visa/trusted-agent-protocol) | Repository README | Signed agent/authorization context. Local unkeyed hashes do not implement this protocol |
| [FinanceBench](https://github.com/patronus-ai/financebench) | Repository README | Financial question-answering evidence tasks, not transaction authorization |
| [FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) | Repository README | Financial agent platform, not validated tuition settlement |
| [FinGPT](https://github.com/AI4Finance-Foundation/FinGPT) | Repository README | Financial language-model tooling, not beneficiary attestation |

These links were actually retrieved on 2026-10-19 UTC. Only abstracts/READMEs were reviewed where stated; no full-paper-reading claim. Signatures, scope binding, single-use approvals, idempotency, DB transactions and least privilege are standard techniques. The defensible contribution is a reproducible student-payment adaptation and test suite. Fundamental novelty and real-world superiority are unproven.

Additional full-system evidence comes from native invoice/API/browser tests, not from the offline policy proxies. Normal application safety is never disabled for a baseline. Real standard-agent/tool-agent/full-system comparisons remain pending reachable-model evaluation with shared inputs, hardware, settings and blinded labels.

Resumed clean verification (2026-10-20): see [current acceptance](RESUMED_ACCEPTANCE_20261020.md) and `evidence/recovery_20261020/`. Earlier measurements above are preserved with their original scope.
