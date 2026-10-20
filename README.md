# BorderProof AI

### Evidence-Consistent Financial Assistance for International Student Payments

**Team:** FinVeritas  
**Competition:** 2026 Shenzhen International FinTech Competition  
**Track:** International Track - Topic C  
**Institution:** Daffodil International University, Bangladesh  
**Version:** V5.5.3 - Qwen Output Limit Repair Candidate

## 1. Project Overview

BorderProof AI is a financial assistance prototype designed to improve evidence consistency, decision transparency, and user control in cross-border tuition payment planning.

The system integrates tuition invoice processing, structured evidence investigation, multi-currency route planning, AI-assisted financial analysis, and evidence-bound authorization controls.

The prototype uses synthetic financial accounts, beneficiaries, payment quotes, and transaction records. It does not initiate real bank transfers.

## 2. Core Capabilities

### Cross-Border Financial Network

- Eight supported currencies: BDT, CNY, GBP, USD, CAD, EUR, AUD, and SGD.
- 56 directed currency planning routes.
- Forward and reverse route selection.
- Interactive financial network visualization.
- Read-only public foreign exchange reference integration.

### Document Processing and Investigation

- Tuition invoice upload and structured field extraction.
- Document integrity verification using SHA-256.
- Invoice, beneficiary, account, and payment information consistency checks.
- Synthetic beneficiary registry matching.
- Conflict detection and evidence-based blocking.

### Financial Simulation

- Synthetic payment quote generation.
- Currency conversion and fee simulation.
- Quote expiration checks.
- Evidence-bound user authorization.
- Simulated payment execution and transaction history.
- Duplicate execution prevention.

### AI Financial Assistant

- Local Qwen3:4b integration through Ollama.
- Read-only backend inspection tools.
- Case, invoice, investigation, quote, approval, policy, and corridor inspection.
- Tool execution provenance and evidence references.
- Restricted financial permissions.
- Controlled failure handling for incomplete model responses.

### BPCE Security Controls

- Evidence consistency validation.
- User authorization separated from AI recommendations.
- Quote and document integrity checks.
- Authorization invalidation when relevant evidence changes.
- Audit records and tenant-scoped access controls.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Web application | Next.js, React, TypeScript |
| Backend API | FastAPI, Python 3.12 |
| Database | SQLAlchemy with local SQLite |
| Local AI | Ollama, Qwen3:4b |
| Testing | Pytest and browser workflow tests |
| Document processing | Structured extraction and SHA-256 |
| Financial reference data | Read-only public FX API |

## 4. System Architecture

The application separates the user interface, application API, evidence validation, AI-assisted analysis, and financial simulation components.

The AI assistant can inspect authorized case information but cannot independently authorize or execute financial transactions.

Financial simulation is governed by backend controls and explicit user actions.

## 5. Local Installation

### Requirements

- Python 3.12
- Node.js and npm for the Next.js application
- Ollama with qwen3:4b for optional local AI inference

### Backend Setup

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r services\api\requirements-lock.txt
```

### Start the Local API

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run_preview.ps1
```

Open:

http://127.0.0.1:8000/demo

### Run Backend Tests

```powershell
python -m pytest -q services\api\tests
```

### Optional Next.js Application

From the `apps/web` directory:

```powershell
npm ci
npm run typecheck
npm run build
npm run start
```

The Next.js build must be checked independently for the current source revision.

## 6. Verification Results

### Backend Testing

The latest reported Windows test execution for V5.5.3 produced:

- Passed: 149
- Skipped: 1
- Warnings: 1
- Failed: 0

These results were observed in the local Python test environment on October 20, 2026.

### Live Qwen Validation

The latest local Qwen3:4b evaluation attempted nine agent scenarios.

- Total attempts: 9
- HTTP 200 responses: 4
- HTTP 502 responses: 5
- Overall status: FAILED_OR_PARTIAL

Local model inference and backend integration were exercised, but reliable tool selection and complete answer generation remain unresolved.

### Financial Safety

The available local tests did not report real financial transfers. The assistant operates with read-only inspection permissions and cannot independently approve or execute payments.

### Controlled Research Evaluation

The project includes 300 internally authored synthetic evaluation cases and a 60-case holdout set.

The BPCE deterministic policy proxy produced:

- Unsafe acceptance: 10.4%
- Legitimate completion: 75.0%

These figures represent synthetic policy-proxy evaluation, not live Qwen accuracy or real-world financial safety performance.

## 7. System Scope

BorderProof AI is a locally tested research and financial simulation prototype.

The current implementation does not include authorized real-bank payment connectivity, verified beneficiary bank ownership, or production financial settlement.

Public FX reference data is provided for information and planning, not as an executable payment quote.

Live model reliability, independent security validation, and public financial deployment require additional verification.

## 8. Documentation and Reproducibility

The repository includes source code, setup scripts, technical documentation, security-related checks, testing resources, and historical audit records.

Selected technical references:

- [V5.5 Verification and Repairs](docs/V5_5_VERIFICATION_AND_REPAIRS.md)
- [V5.5.2 Evidence-First Repair](docs/V5_5_2_EVIDENCE_FIRST_REPAIR.md)
- [V5.5.3 Qwen Patch Verification](AUDIT/V5_5_3_QWEN_PATCH_VERIFICATION.md)
- [Research Validity and Prior Art](AUDIT/RESEARCH_VALIDITY_AND_PRIOR_ART.md)

Historical validation results refer to their respective source versions and should not be interpreted as current V5.5.3 acceptance results.

## 9. Repository

GitHub: https://github.com/sadia-zannat/BorderProof-AI

Submission source revision: `873fd6e0ab06547ac00873d0a3c859c70e858b43`

## 10. Team

**FinVeritas**

Sadia Akter Zannat - Team Leader  
Md. Nazrul Islam Leon - Team Member

Department of Computer Science and Engineering  
Daffodil International University, Bangladesh

**Project:** BorderProof AI  
**Competition:** 2026 Shenzhen International FinTech Competition
