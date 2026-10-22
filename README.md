# RECLAIM AI 2.0 — Autonomous Civic Document Recovery Intelligence Platform
> **"Lost a document? Reclaim your next step."**

[![Agentic AI Hackathon 2026](https://img.shields.io/badge/Hackathon-Agentic%20AI%202026%20--%20Ziro.Digital-00f2fe?style=for-the-badge)](https://ziro.digital)
[![Industry](https://img.shields.io/badge/Track-Social%20Impact%20%26%20Sustainability%20AI-10b981?style=for-the-badge)](#)
[![Python 3.13](https://img.shields.io/badge/Backend-Python%203.13%20%7C%20Flask-3b82f6?style=for-the-badge&logo=python)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-29%2F29%20Passing%20(100%25)-emerald?style=for-the-badge)](https://pytest.org)

---

## 🎯 Executive Summary & Assigned Problem Statement

- **Project Name:** RECLAIM AI 2.0 — Autonomous Civic Document Recovery Intelligence Platform
- **Tagline:** *"Lost a document? Reclaim your next step."*
- **Assigned Problem Statement:** **Lost Document Reissue Guide**
- **Industry & Domain:** Social Impact & Sustainability AI
- **Primary Objective:** Empower citizens who have lost certificates or identity documents to understand legitimate official reissue procedures, supporting statutory evidence, verified fees, application steps, and genuine tracking procedures.

When citizens misplace critical documents in India (educational certificates, driving licences, PAN cards, Voter IDs, or passports), they face predatory third-party broker websites charging illegal markups, confusing circulars, and potential identity theft. **RECLAIM AI 2.0** solves this by connecting **Five Core Innovations** into one coordinated, inspectable agent loop:

```
[ OBSERVE ] ────────► Collect intake attributes without storing sensitive PII
     │
     ▼
[ RECOVERY TWIN ] ──► Construct live digital case state & 8-node dependency graph
     │
     ▼
[ INVESTIGATE ] ────► Proof-of-Truth Research Agent mines statutory claims & resolves circular conflicts
     │
     ▼
[ REASON ] ─────────► Adaptive Multi-Route Planner compares DigiLocker vs Statutory Portal vs Counter
     │
     ▼
[ ASSESS RISK ] ────► Recovery Risk Radar checks predatory brokers, fee anomalies, and SSRF threats
     │
     ▼
[ ACT SAFELY ] ─────► Prepare application draft package; pause at Step 8 Human Approval Gate
     │
     ▼
[ EXECUTE & VERIFY ]► Safe Action Sandbox submits with idempotency key; independent backend check
     │
     ▼
[ LEARN ] ──────────► Finalize Recovery Twin state & update audit timeline
```

---

## 🌟 The Five Core Innovations

### 🧬 Innovation 1: Recovery Twin (Live Digital Case Representation)
A structured digital twin representing the exact state of every recovery case:
- **Case State Tracking:** Facts categorized as *Verified Facts*, *User-Provided Facts*, and *Uncertain Claims*.
- **Topological Dependency Graph:** Evaluates 8 genuine nodes (`IDENTIFY_AUTHORITY`, `VERIFY_PROCESS`, `GATHER_EVIDENCE`, `CONFIRM_FEE`, `PREPARE_APPLICATION`, `OBTAIN_APPROVAL`, `EXECUTE_SUBMISSION`, `VERIFY_STATUS`).
- **Dynamic Node States:** `BLOCKED`, `READY`, `IN_PROGRESS`, `COMPLETED`, `NEEDS_VERIFICATION`.
- **Reactive Recalculation:** When the citizen toggles evidence checkboxes or resolves authority, the graph immediately updates, explaining why nodes are blocked and what specific evidence will unblock them.

### 📜 Innovation 2: Proof-of-Truth Research Agent & Evidence Vault
An evidence-first intelligence agent with transparent provenance tracking:
- **Provenance Tags:** Every claim is explicitly tagged (`LIVE_VERIFIED`, `CACHED`, `USER_PROVIDED`, `SYNTHETIC_DEMO`, `UNVERIFIED`).
- **Conflicting Claims Resolver:** When circulars disagree (e.g. legacy manual ₹50 driving licence booklet circular vs modern Central Motor Vehicles Rules 1989 Rule 81 ₹400 gazette), the engine displays both claims, dates, and applies transparent statutory hierarchy rules to resolve the prevailing rate.

### 🧭 Innovation 3: Adaptive Recovery Planner (Multi-Route Decision Engine)
Generates and compares three feasible recovery channels:
1. **Route 1: Instant Legal Digital Credential (DigiLocker):** Free, immediate, legally equivalent under Section 9A of IT Act 2000.
2. **Route 2: Statutory Online Reissue Portal:** Direct government postal dispatch with verified smart card/mark sheet security features.
3. **Route 3: In-Person Facilitation Center / Administrative Counter:** Manual fallback for biometric/spelling mismatches.
- **Explainable Decision Matrix:** Includes a dedicated *"Why did the agent choose this?"* panel displaying the exact statutory rules and trade-offs behind the recommendation.

### 🛡️ Innovation 4: Recovery Risk Radar (Cybersecurity & Claim Verification)
A 9-point threat analysis scanner protecting citizens against:
1. Unapproved or predatory broker domains (e.g. `quick-pan-agent.com`).
2. Server-Side Request Forgery (SSRF) and private network IP requests.
3. Unverified or exorbitant fee demands exceeding statutory caps.
4. Missing statutory evidence (e.g. stolen documents without Police DDR).
5. False government submission claims.
- **Interactive Safe-Domain Scanner:** Enables citizens to paste any web URL and receive an instant threat assessment without sharing personal PII.

### 🏛️ Innovation 5: Safe Action Sandbox & Mock Government Portal
A persistent local mock government portal backend with strict civic safeguards:
- **Idempotency Protection:** Submissions carry unique idempotency keys (`IDEMP-...`); duplicate submissions return the existing receipt without duplicate records.
- **Human-in-the-Loop Review:** Pauses execution at Step 8 for explicit citizen authorization.
- **Independent State Verification:** Backend provides `GET /api/mock-portal/verify/<ref>` to confirm genuine database persistence.
- **Mandatory Synthetic Watermark:** All demo receipts prominently display:
  `"SYNTHETIC DEMO — NOT A REAL GOVERNMENT APPLICATION"`.

---

## 🧪 Official Hackathon Test Cases (TC1 – TC4)

| Scenario | Input | Expected Outcome | Verified Result | Status |
| :--- | :--- | :--- | :--- | :---: |
| **TC1 — Lost Certificate** | Educational certificate loss (CBSE Class 12 marksheet) | Identify authority, locate verified portal, avoid hallucinating arbitrary forms. | Identified CBSE Pariksha Sangam duplicate portal (`cbse.gov.in`), cited affidavit and police loss entry, verified statutory fee of INR 250. | **`PASS`** |
| **TC2 — Unofficial Agent Website** | Retrieval results contain unofficial broker (`quick-pan-agent.com`) | Flag source, reject from official guidance, prioritize verified authority. | Risk Radar detected commercial broker, assigned `HIGH_RISK`, excluded it from recommendations, and prioritized statutory portal (`incometax.gov.in`). | **`PASS`** |
| **TC3 — Reissue Fee** | Cost inquiry for Driving Licence duplicate | Cite authoritative source or mark unverified; gate payments. | Verified exact statutory fee of INR 400 under CMVR 1989 Rule 81; simulated payment gated behind Step 8 Human Approval. | **`PASS`** |
| **TC4 — Request Number Received** | Tracking inquiry and submission verification | Report `not_submitted` prior to approval; never invent fake government numbers. | Reported `not_submitted` prior to approval; upon approval, generated simulated reference (`SIM-DL-2026-XXXX`) explicitly labelled as demo simulation. | **`PASS`** |

---

## 🚀 Quickstart & Local Execution Instructions

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Modern web browser (Chrome, Edge, Firefox, Safari)

### 2. Setup Environment
```bash
cd RERCLAIM-AI
pip install -r requirements.txt
```

### 3. Run Automated Tests (29 Tests)
```bash
python -m pytest -v
```
Expected output:
```
============================= 29 passed in 3.10s ==============================
```

### 4. Launch the Web Application
```bash
python app.py
```
Open your browser to:
👉 **`http://127.0.0.1:5000`**

---

## 📡 REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Service health, engine status, and database connectivity |
| `GET` | `/api/document-types` | List supported document categories and statutory requirements |
| `GET` | `/api/sources` | Query verified statutory source registry (`?category=...`) |
| `GET` | `/api/presets` | Get synthetic demo presets for judges and evaluators |
| `POST` | `/api/recovery/intake` | Primary intake endpoint executing the unified agent loop |
| `GET` | `/api/recovery/<case_id>/twin` | Get live Recovery Twin and dependency graph state |
| `POST` | `/api/recovery/<case_id>/twin/update` | Recalculate Recovery Twin dynamically on evidence toggle |
| `GET` | `/api/recovery/<case_id>/evidence-vault` | Get Evidence Vault claims, provenance tags, and conflicts |
| `POST` | `/api/recovery/compare-routes` | Comparative multi-route analysis and choice justification |
| `POST` | `/api/risk-radar/scan-url` | Safe-domain checker inspecting URL for SSRF and broker heuristics |
| `POST` | `/api/mock-portal/submit` | Safe Action Sandbox mock portal submission with idempotency key |
| `GET` | `/api/mock-portal/verify/<ref>` | Independent status check of mock portal database state |
| `POST` | `/api/recovery/approve` | Step 8 Human Approval decision gate (Executes Sandbox submission) |
| `GET` | `/api/recovery/<session_id>/trace` | Inspect genuine agent workflow audit trail |
| `GET` | `/api/tests` | List the 4 official hackathon scenarios and latest results |
| `POST` | `/api/tests/run` | Execute individual (`TC1`–`TC4`) or `ALL` hackathon tests |

---

## 🔒 Civic AI Security, Privacy & Ethical Guarantees

1. **Zero-PII Storage Policy:** RECLAIM AI never collects, records, or stores real Aadhaar numbers, PAN numbers, OTPs, passwords, or scanned identity files.
2. **SSRF Defense:** URL sanitization validates hostnames against private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.1`, `::1`) and cloud metadata endpoints (`169.254.169.254`).
3. **Idempotent Sandboxing:** All mock submissions use idempotency keys to prevent duplicate requests.
4. **Transparent Disclaimers:** All synthetic receipts prominently display `"SYNTHETIC DEMO — NOT A REAL GOVERNMENT APPLICATION"`. Real payment transactions are strictly out of scope.
