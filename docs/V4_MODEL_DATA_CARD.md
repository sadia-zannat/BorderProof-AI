# V4 synthetic benchmark data card and evaluator card

**Title:** StuPay-IntegrityBench V4.1

**Creator:** FinVeritas / BorderProof AI, independently authored fictional samples.

**Purpose:** exercise failure modes in a deterministic international tuition-payment simulator; demonstrate controlled policy ablations and honest failure reporting.

**Dataset size:** 300 authored synthetic cases, 300 authored labels. 240 development and 60 holdout. All invoices have synthetic university names; all accounts and bank/provider identifiers are fictional test fixtures. No real people, medical/financial records, or payment secrets are included.

**License/rights:** project-original programmatically generated examples (subject to contest rules and the team's repository license decision). Prior code bases or real proprietary payment records were not copied to make this corpus.

**Provenance:** `services/api/app/stupay_core/corpus.py`; SHA-256 metadata in `benchmarks/stupay_integritybench/v1/metadata.json`.

**Labeling process:** generator-assigned ground truth based on altered synthetic fields and declared failure family. No independent human/financial subject-matter-expert review. This is not blind and can encode researcher bias.

**Evaluators:** 5 deterministic hand-written proxy policies + 3 ablations, sharing the same visible fixture attributes. The BPCE proxy reuses the deployed V3 `assess_injection` and `policy_for_case` checks. It does NOT use deployed SQL execution or real provider messages. No model weights, machine-learning training, token usage or AI generation service.

**Metrics and interpretations:** unsafe acceptance is the fraction of 48 holdout cases *authored* as unsafe that a policy proxy marks complete. Legitimate completion measured on 12 holdout legitimate cases. F1 is derived from accepted/rejected labels. Prompt-injection acceptance measured on 10 authored injected holdout inputs. Timings reflect CPU evaluation logic only.

**Known biases:** cases and evaluator share engineering priors; 60-case holdout is structurally separated but not independent; detection patterns and attacks have overlapping author intent. Case distribution deliberately overrepresents problems and cannot estimate fraud prevalence. Real financial regulations/bank counterparties vary by corridor and provider; synthetic geography is not eligibility evidence. Labels are deterministic, not adjudicated.

**Do not use for:** production finance risk scoring, real student payment decisions, claims of regulatory clearance, marketing performance claims, ranking real LLMs or rigorous comparative academic research without independent evaluation.

**Recommended next study:** independently authored/peer-validated cases, safe anonymization, realistic OCR/layout variance, harder prompt injections, external policy/provider validation, manual adjudication, confidence intervals, multiple realistic LLM/tool-agent baselines and real end-to-end latency measures.
