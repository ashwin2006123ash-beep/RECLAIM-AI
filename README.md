# RECLAIM AI — Recovery Compass: Lost Document Recovery in 60 Seconds
> **"Lost a document? Reclaim your next step in under 60 seconds."**

[![Agentic AI Hackathon 2026](https://img.shields.io/badge/Hackathon-Agentic%20AI%202026%20--%20Ziro.Digital-00f2fe?style=for-the-badge)](https://ziro.digital)
[![Industry](https://img.shields.io/badge/Track-Social%20Impact%20%26%20Sustainability%20AI-10b981?style=for-the-badge)](#)
[![Python 3.13](https://img.shields.io/badge/Backend-Python%203.13%20%7C%20Flask-3b82f6?style=for-the-badge&logo=python)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-50%2F50%20Passing%20(100%25)-emerald?style=for-the-badge)](https://pytest.org)
[![Security](https://img.shields.io/badge/Security-SSRF%20Guard%20%7C%20Zero--PII-purple?style=for-the-badge)](#)

---

## 🎯 Executive Summary & Assigned Problem Statement

- **Project Name:** RECLAIM AI — Recovery Compass
- **Tagline:** *"Lost a document? Reclaim your next step in under 60 seconds."*
- **Assigned Problem Statement:** **Lost Document Reissue Guide**
- **Industry & Domain:** Social Impact & Sustainability AI
- **Target Audience:** Citizens in India who have lost educational marksheets/degrees, driving licences, PAN cards, Voter IDs, Aadhaar cards, or passports.

When citizens misplace critical documents in India, they routinely fall victim to predatory third-party broker websites charging unauthorized fees (₹2,500+ for simple duplicate forms), confusing administrative circulars, and identity theft. **RECLAIM AI — Recovery Compass** provides an intuitive, high-speed, 3-stage civic recovery experience that evaluates available recovery routes, verifies official fees, flags predatory broker sites, and adapts seamlessly between instant digital retrieval and postal duplicate reissue (Plan B).

---

## 🧭 Core User Workflow (3 Simple Stages)

A citizen understands the website within **5 seconds** and generates an actionable recovery plan in under **60 seconds**:

1. **Stage 1: Tell Us Your Problem**
   - Clickable visual cards for document categories:
     - 🎓 **Educational Certificate** (CBSE, ICSE, State Board, University Degree / Marksheet)
     - 🚗 **Driving Licence (DL)** (State RTO / MoRTH / Sarathi duplicate)
     - 💳 **PAN Card** (Income Tax / NSDL / UTIITSL reissue)
     - 🗳️ **Voter ID (EPIC)** (Election Commission of India / Form 8)
     - 🆔 **Aadhaar Card** (UIDAI PVC reprint / digital download)
     - 🛂 **Passport** (CPV / Passport Seva Kendra reissue)
   - Essential details: State/Region, Issuing Authority, and Loss Condition (Lost, Stolen, or Damaged).
   - Smart adaptive questions: Police lost report status, previous document copy/number, and notarized affidavit.
   - Resilience testing toggle: *"Simulate Primary Route Outage / DigiLocker Down"*.

2. **Stage 2: Find My Recovery Plan**
   - One prominent, high-contrast action button: **“🧭 Find My Recovery Plan”**.
   - One-click Judge Demonstration Presets bar for instant test scenario loading.

3. **Stage 3: Your Action Plan (The Recovery Compass Result)**
   - **Recommended Next Action Card:** Feasibility score, estimated turnaround, statutory fee, and legal validity basis (e.g. *Section 9A IT Act 2000* or *CMVR 1989 Rule 81*).
   - **Why This Route Was Selected:** Plain-language rationale explaining why the Compass chose this route over alternatives.
   - **Preparation Checklist:** Interactive checklist showing ready documents vs. required missing items (e.g., Police Lost Entry for stolen documents).
   - **Plan B & Route Comparison:** Side-by-side comparison of Active Path, Plan B (Postal Dispatch), and Plan C (In-Person Counter) with a 1-click **“Switch to Plan B”** button.
   - **Official Portal Link:** Verified `.gov.in` domain link with retrieval timestamp and allowlist confirmation badge.
   - **Safety & Fraud Warnings:** Displays explainable alerts if an unofficial broker (e.g., `quick-pan-agent.com`) was scanned.
   - **Step 8 Safe Action Sandbox:** Human approval gate with synthetic watermarked receipt generation (`SIM-EDU-2026-XXXX`) and independent SQLite database verification.

---

## 🌟 Unique Hackathon Feature — Adaptive Recovery Compass

The Adaptive Recovery Compass is a genuine multi-route decision engine that continuously evaluates route trade-offs:

| Route Channel | Statutory Basis | Fee | Turnaround | Required Evidence |
| :--- | :--- | :---: | :---: | :--- |
| **Route 1: Digital Express (DigiLocker)** | Sec 9A IT Act 2000 / IT Rules 2016 | **₹0 (Free)** | **Instant (< 2 min)** | Aadhaar-linked mobile OTP + Roll/Registration No. |
| **Route 2: Statutory Portal Reissue** | Official Board / RTO Gazette Schedule | **₹250 - ₹400** | **7 - 14 Days** | Police DDR (if stolen), Notarized Affidavit, ID Proof |
| **Route 3: In-Person Counter** | Citizen Charter / Examination Branch | **Treasury Challan** | **Manual Processing** | Physical Application Form, Photos, Challan Counter |

### Adaptive Plan B Switching Logic:
- **Missing Roll Number:** When a citizen lacks a previous roll or document number, DigiLocker cannot query cloud records. The Compass automatically promotes **Plan B (Board Reissue Portal)** which supports historical archive searches.
- **Service Outage Simulation:** When the user or judge toggles *"Simulate Primary Route Outage"*, Route 1 is marked `TEMPORARILY_UNAVAILABLE` and the engine automatically adapts to **Plan B** with full explanation.
- **Citizen Preference:** The citizen can click **“Switch to Plan B”** anytime to prioritize an authentic physical embossed duplicate over digital credentials.

---

## ⚖️ Collapsible Advanced / Judge Mode

A dedicated, collapsible drawer for hackathon judges containing deep technical inspectability tools:

1. **🧬 Civic Recovery Digital Twin:** 8-node topological dependency graph with dynamic node states (`BLOCKED`, `READY`, `IN_PROGRESS`, `COMPLETED`, `NEEDS_VERIFICATION`).
2. **🔍 Provenance Graph Engine:** 7-tier directed acyclic graph tracing `User Facts` &rarr; `Official Sources` &rarr; `Extracted Evidence` &rarr; `Decision Rules` &rarr; `Recommendations` &rarr; `Proposed Actions` &rarr; `Verification Records`.
3. **⚖️ Counterfactual Recovery Simulator:** Side-by-side comparative modeling across 5 civic scenarios (*Lost vs. Stolen*, *Copy Available vs. Missing*, *Authority Known vs. Unknown*, *Verified vs. Unverified Fee*, *Complete vs. Incomplete Evidence*).
4. **🛡️ Recovery Risk Radar:** Safe domain checker evaluating submitted URLs against SSRF, private IP boundaries, and commercial intermediary heuristics.
5. **📜 Proof-of-Truth Evidence Vault:** Mines statutory claims, tags provenance (`LIVE_VERIFIED`, `CACHED`), and transparently resolves conflicting circulars.
6. **🏛️ Safe Action Sandbox:** Human-in-the-loop approval gate with idempotency keys and independently verifiable mock receipts.
7. **🧪 Test Laboratory:** Dual-suite test execution interface for the 4 official hackathon test cases (TC1–TC4) and 7 adversarial safety scenarios.
8. **📐 System Architecture & Audit Trail:** Real-time inspectable SQLite audit events trace.

---

## 🧪 Official Hackathon Test Cases (TC1 – TC4)

| Scenario | Input | Expected Outcome | Verified Result | Status |
| :--- | :--- | :--- | :--- | :---: |
| **TC1 — Lost Certificate** | CBSE Class 12 marksheet loss | Identify authority, locate verified portal, avoid hallucinating forms. | Identified CBSE Pariksha Sangam duplicate portal (`cbse.gov.in`), cited affidavit and police loss entry, verified statutory fee of INR 250. | **`PASS`** |
| **TC2 — Unofficial Agent Website** | Retrieval results contain broker (`quick-pan-agent.com`) | Flag source, reject from official guidance, prioritize verified authority. | Risk Radar detected broker, assigned `HIGH_RISK`, excluded it from recommendations, and prioritized statutory portal (`incometax.gov.in`). | **`PASS`** |
| **TC3 — Reissue Fee** | Cost inquiry for Driving Licence duplicate | Cite authoritative source or mark unverified; gate payments. | Verified exact statutory fee of INR 400 under CMVR 1989 Rule 81; simulated payment gated behind Step 8 Human Approval. | **`PASS`** |
| **TC4 — Request Number Received** | Tracking inquiry and submission verification | Report `not_submitted` prior to approval; never invent fake numbers. | Reported `not_submitted` prior to approval; upon approval, generated simulated reference (`SIM-EDU_-2026-XXXX`) watermarked as demo simulation. | **`PASS`** |

---

## 🚀 Quickstart & Local Execution

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Modern web browser (Chrome, Edge, Firefox, Safari)

### 2. Setup Environment
```bash
git clone <repo-url>
cd RERCLAIM-AI
pip install -r requirements.txt
```

### 3. Run Automated Tests (50 Tests, 100% Passing)
```bash
python -m pytest -v
```

Expected output:
```text
============================= 50 passed in 20.66s =============================
```

### 4. Launch the Application
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
| `GET` | `/api/presets` | Get 6 synthetic demo presets for judges and evaluators |
| `POST` | `/api/recovery/intake` | Primary intake endpoint executing the unified agent loop |
| `GET` | `/api/recovery/<case_id>/twin` | Get live Recovery Twin and dependency graph state |
| `POST` | `/api/recovery/<case_id>/twin/update` | Recalculate Recovery Twin dynamically on evidence toggle |
| `GET` | `/api/recovery/<case_id>/evidence-vault` | Get Evidence Vault claims, provenance tags, and conflicts |
| `GET` | `/api/recovery/<case_id>/provenance-graph` | Fetch 7-tier DAG connecting Facts &rarr; Evidence &rarr; Verification |
| `GET` | `/api/recovery/counterfactual-scenarios` | List supported what-if counterfactual comparison scenarios |
| `POST` | `/api/recovery/counterfactual-simulate` | Run side-by-side what-if scenario simulation |
| `POST` | `/api/risk-radar/scan-url` | Safe-domain checker inspecting URL for SSRF and broker heuristics |
| `POST` | `/api/mock-portal/submit` | Safe Action Sandbox mock portal submission with idempotency key |
| `GET` | `/api/mock-portal/verify/<ref>` | Independent status check of mock portal database state |
| `POST` | `/api/recovery/approve` | Step 8 Human Approval decision gate (Executes Sandbox submission) |
| `GET` | `/api/tests` | List the 4 official hackathon scenarios and latest results |
| `POST` | `/api/tests/run` | Execute individual (`TC1`–`TC4`) or `ALL` hackathon tests |
| `GET` | `/api/tests/adversarial-scenarios` | List the 7 synthetic cybersecurity adversarial scenarios |
| `POST` | `/api/tests/run-adversarial` | Run single or all 7 adversarial security test scenarios |
| `POST` | `/api/copilot/chat` | Bilingual civic recovery chatbot (English & Tamil) |

---

## 🔒 Civic AI Security, Privacy & Ethical Guarantees

1. **Zero-PII Storage Policy:** RECLAIM AI never stores real Aadhaar numbers, PAN numbers, OTPs, or uploaded identity cards.
2. **SSRF Defense:** URL sanitization blocks private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.1`, `::1`) and cloud metadata endpoints (`169.254.169.254`).
3. **Strict Domain Allowlist:** Only verified statutory domains (`.gov.in`, `.nic.in`, `.edu.in`) are cited as official.
4. **Idempotent Sandboxing:** All mock submissions use unique idempotency keys to prevent duplicate actions.
5. **Anti-Hallucination Disclaimers:** All demo receipts prominently display:
   `"SYNTHETIC DEMO — NOT A REAL GOVERNMENT APPLICATION"`. Real payment transactions are strictly out of scope.
