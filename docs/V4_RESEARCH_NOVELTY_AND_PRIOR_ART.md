# V4 research positioning and prior-art matrix — 19 October 2026

## Contribution claims — limited and falsifiable

**Engineering:** BorderProof AI adapts source provenance, case/beneficiary consistency, scope-bound approval and independent execution safeguards to an international-student tuition **internal simulator** with read-only audit/research replay. These individual security ideas already exist elsewhere; **this work has NOT demonstrated a novel payment protocol, provable security, or a published scientific contribution**.

**Evaluation:** Original `StuPay-IntegrityBench V4.1` synthetic fault-family generation with a 300-case study and holdout-policy ablations. All data and baseline implementations were authored by this project; comparative advantage is not independent validation or market superiority. No live financial LLM is measured.

## Comparison against specific prior work (links checked Oct 19, 2026)

| Prior work | Existing capability in prior art | What BorderProof actually does | Gap / nonclaim |
|---|---|---|---|
| Google AP2 Specification v0.2 | Distinct agent/credential/merchant roles, signed checkout/payment mandates, scoped approval, signed receipts | Uses a **local unsigned hash snapshot** tied to synthetic tuition invoice/beneficiary and quote | Not AP2; lacks key management, trusted signing surface, mandate chains, real merchant/provider signatures |
| AP2 Agent Authorization | Human authorization, mandate delegation, verifier proof across steps | Creates local transaction-specific approval only | No cryptographically verifiable agent delegation |
| A Formal Analysis of Agent Payment Protocols, Jiang et al. (2026) | Formal Tamarin cross-protocol models for x402/MPP/ACP/AP2, security property relationships and implementation counterexamples | Informal deterministic dependency checks and API tests | No Tamarin formal model or universal proof, no demonstrated originality over existing consistency literature |
| AgentDojo (Debenedetti et al., 2024) | Dynamic attack/defense benchmark for prompt injections in tool-using agents | Simulated untrusted instructions and V3 regex scanner | Not AgentDojo integration; no real tool-using LLM red team or adaptive attackers |
| Visa Trusted Agent Protocol | Agent-to-merchant trust/authentication ecosystem | No Visa API integration | Not affiliated, certified, integrated or interoperable |
| Flywire / Convera / Wise | Real world international payments, settlement and provider capabilities | No real money movement, quote eligibility, verified beneficiary ownership | Basic student tuition payment UI is not novel |

References:
- https://github.com/google-agentic-commerce/AP2/blob/main/docs/ap2/specification.md
- https://github.com/google-agentic-commerce/AP2/blob/main/docs/ap2/agent_authorization.md
- https://arxiv.org/abs/2609.00060
- https://arxiv.org/abs/2406.13352
- https://github.com/visa/trusted-agent-protocol
- https://www.flywire.com/ and https://wise.com/

## V4 evaluated claim

On **60 authored holdout synthetic cases**, a deterministic BPCE-proxy accepted **5 of 48 unsafe-labelled cases** and completed **9 of 12 legitimate cases**. This is a measurement of the authored rule-based evaluation set, not a measured reduction in real-world student-payment loss. The obfuscated injection cases and benign-looking quoted phrases expose failure modes rather than proving general safety.

## Evidence needed to advance novelty claim

A related-work systematic literature review, independent counterfactual baselines using comparable underlying LLMs/tools, rigorously blind expert-labeled student finance cases, statistically substantiated improvements, real execution-time end-to-end safety evidence and documented regulatory/operational constraints. Until then: classify novelty as **problem-specific engineering composition + evaluation artifact**.
